#!/usr/bin/env python3
"""
Ingest repo-resident feature specs into the features.json contract.

Teams that keep Gherkin under version control rather than pasting it into a tracker
have made a defensible call -- two copies of a spec drift. But it leaves Product and
QA unable to review the spec where they work, and leaves a feature map with nothing
to score. This adapter reads the repo directly so those features get a real verdict
instead of a "not assessable" zero.

Expected layout (both shapes work):

    <root>/                          <root>/
      <epic>/                          features/
        <feature>/                       <feature>/
          acceptance.feature               acceptance.feature
          nfrs.md                          nfrs.md
          eval_criteria.yaml               eval_criteria.yaml
          feature_source.md                feature_source.md

A directory is treated as a feature when it contains at least one *.feature file or a
feature_source.md. The artifact names are the ones govkit-feature-refine already
declares in its Inputs section, so a repo laid out for refinement needs no changes.

Usage:
    python repo_ingest.py <root> [-o features.json] [--epic AI-123] [--key-from dir|feature]
    python repo_ingest.py <root> --merge tracker.json -o features.json
"""

import argparse
import json
import os
import re
import sys

FEATURE_EXT = ".feature"
SOURCE_NAMES = ("feature_source.md", "source.md", "README.md")
NFR_NAMES = ("nfrs.md", "nfr.md")
EVAL_NAMES = ("eval_criteria.yaml", "eval_criteria.yml", "evals.yaml", "evals.yml")

KEY_RE = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")
DIR_KEY_RE = re.compile(r"^([a-zA-Z]+)(\d+)[_-]")


# ---------------------------------------------------------------- gherkin

def parse_feature_file(text):
    """Parse Gherkin into the contract's rules[] shape.

    Scenarios are grouped under the Rule: they follow. Gherkin without explicit
    Rule: blocks is still valid -- those scenarios land under a single unnamed rule,
    which the rubric's "rule coverage" dimension will correctly mark as a gap rather
    than silently inventing rules that the author never wrote.
    """
    rules, cur_rule, cur_scen = [], None, None
    title = description = ""
    in_desc = False
    pending_tags = []

    def flush_scenario():
        nonlocal cur_scen
        if cur_scen and cur_scen["steps"]:
            cur_rule["scenarios"].append(cur_scen)
        cur_scen = None

    def flush_rule():
        nonlocal cur_rule
        flush_scenario()
        if cur_rule and cur_rule["scenarios"]:
            rules.append(cur_rule)
        cur_rule = None

    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("@"):
            # Tag line; attaches to the next Scenario. Slice (@mvp/@v1/@v2) and
            # size (@small/@medium/@large) tags are govkit-feature-slice's output.
            in_desc = False
            pending_tags.extend(t for t in line.split() if t.startswith("@"))
            continue

        if line.startswith("Feature:"):
            title = line[len("Feature:"):].strip()
            in_desc = True
            pending_tags = []  # feature-level tags are not scenario tags
            continue

        if line.startswith("Rule:"):
            in_desc = False
            flush_rule()
            cur_rule = {"rule": line[len("Rule:"):].strip(), "scenarios": []}
            pending_tags = []
            continue

        if line.startswith(("Scenario Outline:", "Scenario:", "Example:")):
            in_desc = False
            flush_scenario()
            if cur_rule is None:
                cur_rule = {"rule": "", "scenarios": []}
            name = line.split(":", 1)[1].strip()
            cur_scen = {"name": name, "steps": [], "tags": pending_tags}
            pending_tags = []
            continue

        if line.startswith(("Given ", "When ", "Then ", "And ", "But ")):
            in_desc = False
            if cur_scen is not None:
                cur_scen["steps"].append(line)
            continue

        if line.startswith(("Background:", "Examples:", "Scenarios:", "|", '"""')):
            in_desc = False
            continue

        if in_desc:
            description += (" " if description else "") + line

    flush_rule()
    return title, description, rules


# ---------------------------------------------------------------- nfrs

NFR_ROW = re.compile(r"^\|(.+)\|\s*$")


def parse_nfrs(text):
    """Read an NFR markdown table. Columns are matched by header name, so column
    order does not matter and unknown columns are ignored."""
    rows, headers = [], None
    for raw in text.splitlines():
        m = NFR_ROW.match(raw.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        if headers is None:
            headers = [c.lower() for c in cells]
            continue
        row = dict(zip(headers, cells))

        def pick(*names, default=""):
            for n in names:
                for h, v in row.items():
                    if n in h:
                        return v
            return default

        nfr = {
            "id": pick("id", "#", default=f"N{len(rows)+1}"),
            "dim": pick("dimension", "dim", "category", "area"),
            "req": pick("requirement", "req", "constraint", "description"),
            "threshold": pick("threshold", "target", "value"),
            "evidence": pick("evidence", "proof", "artifact"),
            "gap": pick("gap", "note", "status"),
        }
        if any(nfr[k] for k in ("dim", "req")):
            rows.append(nfr)
    return rows


def parse_evals(text):
    """Read eval criteria from YAML if available, otherwise fall back to a shallow
    parse so a missing PyYAML does not silently drop the whole evidence contract."""
    try:
        import yaml  # noqa: PLC0415

        data = yaml.safe_load(text) or {}
        items = data.get("evaluation_criteria") or data.get("evals") or data
        if isinstance(items, dict):
            items = [dict(v, id=k) if isinstance(v, dict) else {"id": k, "type": str(v)}
                     for k, v in items.items()]
        out = []
        for it in items or []:
            if not isinstance(it, dict):
                continue
            out.append({
                "id": str(it.get("id", "")),
                "type": str(it.get("type", "")),
                "rule_link": str(it.get("rule_link", it.get("rule", ""))),
                "method": str(it.get("method", "")),
                "pass_threshold": str(it.get("pass_threshold", it.get("threshold", ""))),
                "gate": str(it.get("gate", "")),
            })
        return out
    except ImportError:
        print("  note: PyYAML unavailable, eval_criteria parsed shallowly", file=sys.stderr)
        out, cur = [], None
        for raw in text.splitlines():
            s = raw.strip()
            if s.startswith("- "):
                if cur:
                    out.append(cur)
                cur = {"id": "", "type": "", "rule_link": "", "method": "",
                       "pass_threshold": "", "gate": ""}
                s = s[2:].strip()
            if cur is not None and ":" in s:
                k, v = s.split(":", 1)
                k = k.strip().lower()
                if k in cur:
                    cur[k] = v.strip().strip("'\"")
        if cur:
            out.append(cur)
        return out


# ---------------------------------------------------------------- source md

SECTION = re.compile(r"^#{1,4}\s*(.+?)\s*$")


def parse_source(text):
    """Pull intent, scope, out of scope, open questions and DoD out of a source
    markdown file by heading name. Headings are matched loosely because teams name
    them differently and a strict match would silently drop real content."""
    out = {"userContext": "", "scope": [], "outOfScope": [],
           "openQuestions": [], "dod": [], "privacy": ""}
    # Order matters: "out of scope" also contains "scope", so the more specific
    # bucket has to be tested first or every exclusion lands in the scope list.
    buckets = {
        "outOfScope": ("out of scope", "not in scope", "out-of-scope", "excluded", "deferred"),
        "scope": ("in scope", "functional scope", "scope"),
        "openQuestions": ("open question", "question", "unresolved", "decision needed"),
        "dod": ("definition of done", "done when", "dod", "acceptance evidence"),
    }
    prose = {
        "userContext": ("user context", "intent", "user story", "why", "purpose", "outcome"),
        "privacy": ("privacy", "confidential", "data handling"),
    }

    cur, cur_prose = None, None
    for raw in text.splitlines():
        m = SECTION.match(raw)
        if m:
            h = m.group(1).lower()
            cur = cur_prose = None
            for k, names in buckets.items():
                if any(n in h for n in names):
                    cur = k
                    break
            else:
                for k, names in prose.items():
                    if any(n in h for n in names):
                        cur_prose = k
                        break
            continue
        s = raw.strip()
        if not s:
            continue
        if cur and s.startswith(("- ", "* ", "+ ")):
            out[cur].append(s[2:].strip())
        elif cur and re.match(r"^\d+[.)]\s", s):
            out[cur].append(re.sub(r"^\d+[.)]\s*", "", s))
        elif cur_prose:
            out[cur_prose] += (" " if out[cur_prose] else "") + s
    return out


# ---------------------------------------------------------------- walk

def derive_key(dirname, feature_title, source_text, mode, epic):
    if mode == "feature":
        m = KEY_RE.search(feature_title or "")
        if m:
            return m.group(1)
    m = KEY_RE.search(dirname)
    if m:
        return m.group(1)
    m = DIR_KEY_RE.match(dirname)
    if m:
        return f"{m.group(1).upper()}-{m.group(2)}"
    m = KEY_RE.search(source_text[:400]) if source_text else None
    if m:
        return m.group(1)
    return f"{epic or 'FEATURE'}-{dirname}"


def read_first(d, names):
    for n in names:
        p = os.path.join(d, n)
        if os.path.isfile(p):
            return open(p, encoding="utf-8", errors="replace").read()
    return ""


def ingest_dir(d, mode, epic):
    files = os.listdir(d)
    fpaths = sorted(f for f in files if f.endswith(FEATURE_EXT))
    src = read_first(d, SOURCE_NAMES)
    if not fpaths and not src:
        return None

    title, desc, rules = "", "", []
    for f in fpaths:
        t, dsc, r = parse_feature_file(
            open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
        )
        title = title or t
        desc = desc or dsc
        rules.extend(r)

    name = os.path.basename(d.rstrip("/"))
    meta = parse_source(src) if src else {
        "userContext": "", "scope": [], "outOfScope": [],
        "openQuestions": [], "dod": [], "privacy": "",
    }
    nfr = parse_nfrs(read_first(d, NFR_NAMES))
    evals = parse_evals(read_first(d, EVAL_NAMES))

    feat = {
        "key": derive_key(name, title, src, mode, epic),
        "title": title or name.replace("_", " ").replace("-", " ").title(),
        "source": "repo",
        "sourcePath": d,
        "status": "",
        "workstream": "",
        "phases": [],
        "clientVisible": False,
        "consumes": [],
        "produces": [],
        "userContext": meta["userContext"] or desc,
        "scope": meta["scope"],
        "outOfScope": meta["outOfScope"],
        "rules": rules,
        "ruleCount": len(rules),
        "scenarioCount": sum(len(r["scenarios"]) for r in rules),
        "nfr": nfr,
        "nfrTbd": [n for n in nfr if "TBD" in (n.get("threshold") or "").upper()
                   or not (n.get("threshold") or "").strip()],
        "evals": evals,
        "openQuestions": meta["openQuestions"],
        "dod": meta["dod"],
        "privacy": meta["privacy"],
    }
    return feat


def walk(root, mode, epic):
    found = []
    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith((".", "__", "node_modules"))]
        f = ingest_dir(dirpath, mode, epic)
        if f:
            found.append(f)
            dirnames[:] = []  # a feature dir does not contain nested features
    return sorted(found, key=lambda x: x["key"])


# ---------------------------------------------------------------- merge

MERGE_PREFER_REPO = ("rules", "ruleCount", "scenarioCount", "nfr", "nfrTbd", "evals")


def merge(tracker, repo):
    """Overlay repo specs onto tracker records, keyed by feature key.

    The tracker owns status, workstream, phase, ownership and the artifact chain --
    things a repo does not know. The repo owns the spec itself. Where a tracker record
    is empty and the repo has content, the repo wins; that is the whole point.
    """
    by_key = {f["key"]: f for f in tracker}
    for r in repo:
        t = by_key.get(r["key"])
        if t is None:
            by_key[r["key"]] = r
            continue
        for k in MERGE_PREFER_REPO:
            if r.get(k):
                t[k] = r[k]
        for k, v in r.items():
            if k in MERGE_PREFER_REPO or k == "key":
                continue
            if v and not t.get(k):
                t[k] = v
        t["source"] = "tracker+repo"
        t["sourcePath"] = r.get("sourcePath", "")
    return sorted(by_key.values(), key=lambda x: x["key"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("-o", "--out", default="features.repo.json")
    ap.add_argument("--epic", default="")
    ap.add_argument("--key-from", choices=["dir", "feature"], default="dir")
    ap.add_argument("--merge", help="tracker features.json to overlay these specs onto")
    a = ap.parse_args()

    if not os.path.isdir(a.root):
        print(f"not a directory: {a.root}")
        return 2

    feats = walk(a.root, a.key_from, a.epic)
    if not feats:
        print(f"no feature directories found under {a.root}")
        print("expected a dir containing *.feature or feature_source.md")
        return 1

    if a.merge:
        feats = merge(json.load(open(a.merge)), feats)

    json.dump(feats, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"{len(feats)} feature(s) -> {a.out}")
    for f in feats:
        flag = "" if f.get("ruleCount") else "   <- no Gherkin parsed"
        print(f"  {f['key']:<12} {f.get('ruleCount', 0):>2} rules  "
              f"{f.get('scenarioCount', 0):>3} scenarios  {len(f.get('nfr') or []):>2} nfr  "
              f"{len(f.get('evals') or []):>2} evals  [{f.get('source', 'tracker')}]{flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

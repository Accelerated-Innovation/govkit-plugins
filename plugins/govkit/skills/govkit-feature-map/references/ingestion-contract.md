# Ingestion contract

Every adapter normalizes into the same `features.json`: a JSON array of feature objects. The renderer and the scoring fan-out both read this and nothing else, so a new source only ever needs a new adapter — never a change to scoring or rendering.

## Contents

- [Schema](#schema)
- [Minimum viable feature](#minimum-viable-feature)
- [Jira adapter](#jira-adapter)
- [Aha adapter](#aha-adapter)
- [Repo directory adapter](#repo-directory-adapter)
- [Merging a tracker record with a repo spec](#merging-a-tracker-record-with-a-repo-spec)
- [Artifact naming](#artifact-naming)

## Schema

```jsonc
{
  "key": "AI-124",                  // required, unique; the badge and anchor key
  "title": "Guided Session Shell",  // required
  "url": "https://.../browse/AI-124",// optional; makes the card key a link
  "source": "jira",                 // jira | aha | repo | tracker+repo
  "sourcePath": "features/ai124/",  // repo-sourced features only

  "status": "Ready - Delivery Intake",
  "workstream": "Experience",       // becomes the lane; free text
  "phases": [2, 3, 4],
  "clientVisible": true,

  "consumes": ["context-pack"],     // artifact names; drives the chain
  "produces": ["capsule"],

  "userContext": "As a client stakeholder, I want …",
  "scope": ["…"],
  "outOfScope": ["…"],

  "rules": [                        // the Gherkin
    {
      "rule": "The client is never asked for what the platform already knows",
      "scenarios": [
        {
          "name": "The session opens on a prepared capsule",
          "steps": ["Given a context pack exists", "When the session begins", "Then …"]
        }
      ]
    }
  ],
  "ruleCount": 7,                   // denormalized for the card metrics
  "scenarioCount": 15,

  "nfr": [
    {"id": "N1", "dim": "Performance", "req": "Turn response time",
     "threshold": "TBD", "evidence": "Session telemetry", "gap": "Unset"}
  ],
  "nfrTbd": [ /* subset of nfr with unset or TBD thresholds */ ],

  "evals": [
    {"id": "no_jargon_leak", "type": "policy_compliance",
     "rule_link": "No internal vocabulary reaches the client",
     "method": "assert the banned-term list is absent",
     "pass_threshold": "zero occurrences", "gate": "pr"}
  ],

  "openQuestions": ["P0-7: how vision sensitivity is calculated"],
  "dod": ["All scenarios automated and passing"],
  "privacy": "Free text on confidentiality handling",
  "specNote": "Shown on the card when rules[] is empty — say where the spec lives"
}
```

Every field except `key` and `title` is optional. Missing fields degrade the card gracefully; they do **not** get invented. An empty `nfr` array means this feature declares no NFRs, and the rubric will score that honestly.

## Minimum viable feature

Scoring needs `rules` to say anything useful. A feature with `key`, `title` and nothing else will score near zero — which is correct, and should carry `notAssessable` if the spec exists somewhere the ingestion could not reach. Set `specNote` so the card explains itself rather than looking like an oversight.

## Jira adapter

Use the Atlassian MCP tools.

1. `searchJiraIssuesUsingJql` with `parent = <epic>` or `"Epic Link" = <epic>` to enumerate features.
2. `getJiraIssue` per key for description and custom fields.

| Contract field | Jira source |
|---|---|
| `key` | issue key |
| `title` | summary |
| `url` | browse URL |
| `status` | status name |
| `workstream`, `phases`, `clientVisible` | labels, by convention (e.g. `map-ws-experience`, `map-p2`, `map-client-visible`) |
| `consumes` / `produces` | labels `map-in-<artifact>` / `map-out-<artifact>` |
| `rules` | Gherkin parsed out of the description or the Acceptance Criteria field |
| `nfr`, `evals` | custom fields, or tables in the description |
| `openQuestions` | a description section, or linked issues |

Label conventions vary per organisation. Confirm the convention with the user rather than assuming, and record it in the map's lede so a reader knows the chain is derived from labels.

Jira descriptions arrive in ADF or wiki markup. Convert to plain text before parsing Gherkin, and expect `Given`/`When`/`Then` to survive as line-leading tokens.

## Aha adapter

Use the Aha MCP tools. `find_project` resolves the workspace; `read_records` and `search_records` pull features. Call `fields_metadata` first — Aha! custom field keys are workspace-specific and guessing them silently produces empty specs.

| Contract field | Aha! source |
|---|---|
| `key` | reference number (e.g. `PRJ-123`) |
| `title` | name |
| `url` | record URL |
| `status` | workflow status |
| `workstream` | initiative, epic name, or a custom field |
| `phases` | release, or a custom field |
| `rules` | Gherkin in the description, or a custom field holding acceptance criteria |
| `nfr`, `evals` | custom fields; confirm keys via `fields_metadata` |
| `consumes` / `produces` | a custom field, or tags |

Aha! features often carry requirements as child records. If the Gherkin lives there rather than on the feature, pull requirements and fold them into `rules` — one rule per requirement, scenarios beneath.

## Repo directory adapter

`scripts/repo_ingest.py` walks a directory tree. A directory is treated as a feature when it contains at least one `*.feature` file or a `feature_source.md`.

```
<root>/
  <epic>/
    <feature>/
      acceptance.feature      -> rules[]
      nfrs.md                 -> nfr[]      (markdown table, columns matched by header name)
      eval_criteria.yaml      -> evals[]
      feature_source.md       -> userContext, scope, outOfScope, openQuestions, dod, privacy
```

These are the artifact names `govkit-feature-refine` already declares in its Inputs section, so a repo laid out for refinement needs no changes to be mappable.

Feature keys are derived from the directory name — `ai204_content_and_gates` → `AI-204` — or from a key appearing in the `Feature:` line. Pass `--key-from feature` to prefer the latter.

Gherkin without explicit `Rule:` blocks parses into a single unnamed rule. That is deliberate: the rubric's rule-coverage dimension will mark it as a gap rather than the adapter inventing rules the author never wrote.

`feature_source.md` sections are matched loosely by heading name, because teams name them differently. "Out of scope" is tested before "scope" — otherwise every exclusion lands in the scope list.

## Merging a tracker record with a repo spec

```bash
python scripts/repo_ingest.py <repo-root> --merge tracker-features.json -o features.json
```

Matched by `key`. The repo wins on spec content — `rules`, `ruleCount`, `scenarioCount`, `nfr`, `nfrTbd`, `evals`. The tracker keeps everything it uniquely knows: status, workstream, phases, ownership, and the `consumes`/`produces` arrays that build the chain. Any other field the tracker left empty is filled from the repo. Merged features are marked `"source": "tracker+repo"`.

This is the case worth designing for. A team that deliberately keeps its spec in the repo — because two copies of a spec drift — should not be badged as though it has no spec.

## Artifact naming

The chain is built by matching strings in `produces` against strings in `consumes`. Normalize to kebab-case during ingestion. A chain that silently drops edges because two features spelled `context-brief` and `Context Brief` differently is worse than no chain at all, because it looks complete.

After ingesting, print the artifact ledger and check it with the user. Artifacts with no producer, or produced but never consumed, are usually either genuine boundary cases or a naming mismatch — and the difference matters.

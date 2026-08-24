# Plan: Skill-Flow Review Fixes

**Date:** 2026-08-24
**Source:** Full-suite review of all nine skills (eight govkit + val-rapid-validation), both
rubrics, refine's PM/QA checklists, the map's references and scripts, `compute_size.py`,
the metrics event schema. Requested as a lean/agile shift-left review before feeding
specs into the GovKit delivery harness.
**Status legend:** `[ ]` not started · `[~]` in progress · `[x]` done
**Status: ALL ITEMS COMPLETE — shipped as govkit 0.7.0 (2026-08-24).** Naming decision confirmed by user: token records at `.govkit/tokens/<feature-key>.json`.

## Context and thesis

The pipeline (epic → features → refine → slice → readiness → synthetic data → coding →
metrics, map as portfolio view) is structurally sound: two-gate design, blockers-not-scores,
script-owned arithmetic, no-invented-numbers everywhere.

The systemic finding: **the authoring skills (`govkit-epic-create`, `govkit-feature-create`)
shift the conversation left but not the contract.** Draft 0 comes out missing fields and
structures that the very next gates (`govkit-feature-refine`, `govkit-feature-readiness`)
score on. Fixes A1–A5 align the authoring templates to the gate contracts so specs stop
arriving pre-gapped.

**User clarification (2026-08-24):** `plan.md` and `architecture_preflight.md` are created
*later*, by the GovKit platform process/skills — they are not required or desired at
authoring time. So original finding D shrinks to a documentation note (D1 below); do NOT
make feature-create scaffold a preflight or plan.

## Work items, in priority order

### A. Align authoring templates to the gate contracts (one batch — all in govkit-feature-create / govkit-epic-create files)

- [x] **A1 — NFR categories 5 → 10.** Feature-create Step F7 and epic-create Step 8 walk
  Performance, Security, Scalability, Reliability, Compliance. The gates review ten:
  Performance, Security, Privacy, Reliability, Observability, Accessibility, Data quality,
  Compliance, Cost, Supportability (refine SKILL.md Step 7; readiness rubric dim 7; QA
  evidence checklist). Change both skills (and `feature-template.md` / `epic-template.md`
  guidance) to walk the gate's ten-area list. Keep the GenAI add-on categories. Drop or
  fold "Scalability" (not on the gate's list — fold into Performance/Reliability guidance).
  Epic-level note stays: epic NFRs are cross-feature standards, but walk the same list.
- [x] **A2 — Add Owner to the NFR table.** `feature-template.md` nfrs.md table gains an
  `Owner` column (gates require it: refine Step 7, readiness dim 7 "conditions, thresholds,
  evidence, and owner"). Optionally a `Release impact` column (refine checks it). Confirm
  `repo_ingest.py:parse_nfrs` tolerates it (it matches by header name and ignores unknown
  columns — no script change needed, but verify).
- [x] **A3 — Add owner + evidence artifact (+ data source) to eval_criteria.yaml.** Schema in
  `feature-template.md` (and `metrics-and-evaluation.md`'s epic_eval_criteria.yaml) gains
  `owner`, `evidence` (the artifact that lands in the PR/release review), and optionally
  `data_source` distinct from `method`. `repo_ingest.py:parse_evals` ignores extra fields —
  no downstream break. Keep `EPIC-` id prefixes and `applies_to` at epic level.
- [x] **A4 — Ask the agentic-behavior question at creation.** Feature-create GenAI mode asks
  refine's exact question ("Agentic behavior: yes or no?" — autonomous planning/multi-step
  tool use/orchestration vs single-shot or none), records the PM's explicit answer as
  `multi_agent: true|false` in eval_criteria.yaml, leaves it unset + listed as a gap if
  unanswered. Never infer — same rule as refine. Refine then confirms rather than
  discovers; its batch mode can already read the flag from the record.
- [x] **A5 — Business rules step + `Rule:` blocks.** Two parts:
  1. Feature-create Feature mode gains an explicit "enumerate the business rules" step
     between F5 (description) and the acceptance-criteria step — rules are what the PM
     knows and the agent must not invent. Renumber F-steps accordingly (or insert as F5b).
  2. `gherkin-tagging.md` required structure gains `Rule:` blocks — one per business rule,
     scenarios grouped beneath. Downstream everything organizes on rules: refine dim 3,
     readiness dim 3, Example Mapping Rules cards, `evals[].rule_link`,
     `repo_ingest.py` rule grouping, map cards' RULE headers ("(no Rule declared)" today).
  Update the eval fixtures/assertions in feature-create's evals.json to expect Rule blocks
  and the ten NFR areas where relevant.

### B. Give the map's chain a repo-first data source

- [x] **B1 — Structured Produces/Consumes in feature_source.md.** `feature-template.md`
  gains `## Produces` / `## Consumes` sections (kebab-case artifact names, per the map's
  artifact-naming rule). Feature-create's Epic mode already *generates* this knowledge as
  scope boundaries ("A owns it, B consumes it") — capture it structurally instead of
  flushing to prose. Story-mapping.md: boundary format explicitly feeds these sections.
- [x] **B2 — Parse them in `repo_ingest.py`.** Add `produces` / `consumes` buckets to
  `parse_source` (heading matches: "produces", "consumes", "depends on"? — keep it tight:
  "produces", "consumes" only, to avoid mis-bucketing prose dependencies), normalize to
  kebab-case, populate the feature object's arrays instead of hardcoded `[]`. Also stop
  dropping the Dependencies heading silently — either bucket it into openQuestions-like
  prose or leave documented as prose-only.
- [x] **B3 — Note in ingestion-contract.md** repo adapter row: chain now derivable from
  repo packages; tracker labels remain the tracker-side convention.

### C. Make the Development Token machine-readable exhaust

- [x] **C1 — Readiness writes a structured token record.** When issuing a decision,
  `govkit-feature-readiness` writes `features/<key>/.govkit-token.json` (or agreed path/name
  — check what the platform expects; metrics reads `.govkit/marker.json` at repo root, so
  maybe `.govkit/tokens/<key>.json`) with: `feature_id`, `decision`
  (approved|approved_with_edits|blocked), `score`, `blockers[]`, `draft_version`, `ts`.
  This unlocks the reserved `refinement.token.issued` event → Tier 2 metrics (refinement
  lead time Draft 0→Token, blocked-token rate). Decide the exact path WITH the user —
  it must match what govkit-metrics-emit / the platform will read.
- [x] **C2 — Fix the stale attribution** in `event_schema.md` (reserved event says
  govkit-feature-refine writes the token; the repo's settled rule is refine *recommends*,
  readiness *issues*). Note: event_schema.md belongs to govkit-metrics-emit in this repo,
  so it is editable here.

### D. Documentation of the platform seam (reduced per user clarification)

- [x] **D1 — Name when plan.md / architecture_preflight.md appear.** One short note (likely
  in readiness SKILL.md Inputs and/or govkit plugin README lifecycle section): these are
  produced later by the GovKit platform process, after the token — not at authoring time.
  Consequence for metrics: a feature's completeness score (which weights plan.md at 45/100)
  climbs as it moves through the platform stages; a fresh post-token package scoring ~55-70
  is expected, not a defect. Do NOT add these artifacts to any authoring skill.

### E. Readiness batch mode + verifier scale

- [x] **E1 — Batch mode section in govkit-feature-readiness SKILL.md**, mirroring refine's:
  skip interactive flow, emit one raw JSON verdict per feature, 12 dimensions in rubric
  order, same no-invented-content guardrails, notAssessable semantics where the package is
  unreachable. Define the output schema (readiness analog of refine's batch schema).
- [x] **E2 — `verify_scores.py --scale readiness`**: 12 dimensions in readiness rubric
  order, bands Approved ≥10, Approved-with-edits 8.5–<10, Blocked <8.5, blockers gate.
  Default remains the 10-dim refine scale. Update scoring.md's "Current limitation" note
  and the map SKILL's rubric-selection table to say the verified path now exists.

### F. Consolidate the write protocol (three near-copies)

- [x] **F1 —** Extract the canonical preview-confirm protocol + Jira/Aha adapter tables to
  one reference; slice's `tracker-writeback.md`, feature-create's and epic-create's
  `tracker-adapters.md` become thin deltas (write-back vs create vs update specifics).
  Follow the map's precedent for cross-skill reads (`../govkit-feature-refine/references/…`).
  Open question: plugin skills are installed together, so relative cross-skill paths work —
  verify path form used by scoring.md and match it. If cross-skill reference feels fragile,
  fallback: pick one file as canonical and have the other two state "the protocol in X is
  canonical; this file carries only the deltas."

### G. Align GenAI detection

- [x] **G1 —** One canonical keyword + implied-behavior list, verbatim across epic-create,
  feature-create (val-rapid and refine phrase theirs behaviorally; align keyword lists where
  they exist). Union of current lists.
- [x] **G2 —** Feature-create inherits `genai: true` from the epic package when present
  (epic.md header `GenAI: yes`) instead of independently re-detecting; re-detection stays
  as fallback when no epic exists.

### H. Small seams

- [x] **H1 —** Feature-create Step E3 anchors slice proposals to the epic's confirmed
  `initial_scope` when an epic package exists (one sentence).
- [x] **H2 —** Provenance notation: epic-create adopts P2's `[E]/[I]/[A]` marks (or states
  the explicit mapping measured→[E], estimated→[I], unknown→[A]) in problem-framing.md,
  metrics-and-evaluation.md, and epic-template.md.
- [x] **H3 —** Soften epic-create Related-table overclaim ("the epic's success metrics are
  what a release-weakness read is judged against" — the map doesn't ingest epics).
- [x] **H4 —** Story-mapping/E7: recommend creating MVP-slice stubs now and deferring
  V1/V2 stubs as the default (deferred commitment); PM can override to create all.
- [x] **H5 —** Readiness rubric dim 6 names `out_of_scope.md`, which nothing produces —
  reword to "the package's out-of-scope section (e.g. in feature_source.md) or source
  notes."
- [x] **H6 —** feature_source.md header gains a `Source` row (tracker/system of record)
  for readiness dim 2 traceability.

### Bookkeeping (do last, once per released batch)

- [x] Bump `plugins/govkit/.claude-plugin/plugin.json` version (0.6.0 → 0.7.0) + mirror
  description/keyword changes in `.claude-plugin/marketplace.json` if descriptions change.
- [x] govkit README version-history row summarizing the contract-alignment release.
- [x] Update eval fixtures/assertions touched by A1–A5 (feature-create evals expect Rule
  blocks, 10 NFR areas, multi_agent asked; epic-create evals unaffected except provenance
  marks in H2 — check eval 2 wording).
- [x] `claude plugin validate .` + JSON validity + link check.

## Explicitly rejected / out of scope

- Feature-create scaffolding `architecture_preflight.md` or `plan.md` — platform-owned,
  later-stage (user decision 2026-08-24).
- Adding a 4th delivery-phase tag (`@future`) — removed earlier; vocabulary is closed at
  `@mvp/@v1/@v2`.
- Map ingesting epics — noted as overclaim (H3 softens the text); building epic ingestion
  is not planned.
- Post-delivery learn-loop (re-reading epic success metrics against outcomes) — real lean
  gap, but out of scope for this batch; candidate future skill.

## Verified-fine (do not "fix")

- Epic-MVP / feature-slice / scenario-tag layering: altitude-stratified, not duplicated.
- Refine-recommends / readiness-issues two-gate split: deliberate, well-guarded.
- val-rapid ↔ epic-create boundary: documented from both sides; epic consumes P2 evidence.
- Synthetic-data guardrails: consistent with the suite.
- `repo_ingest.py` NFR/eval parsers: header-matched and unknown-field-tolerant — A2/A3
  additions are non-breaking.

## Key file map (for resuming after context loss)

| Area | Files |
|---|---|
| Feature authoring | `plugins/govkit/skills/govkit-feature-create/{SKILL.md, references/{feature-template,gherkin-tagging,story-mapping,tracker-adapters}.md, evals/}` |
| Epic authoring | `plugins/govkit/skills/govkit-epic-create/{SKILL.md, references/{epic-template,metrics-and-evaluation,problem-framing,tracker-adapters}.md, evals/}` |
| Gates | `govkit-feature-refine/SKILL.md` (Steps 7–8, batch schema), `govkit-feature-readiness/{SKILL.md, references/govkit-readiness-rubric.md}` |
| Map | `govkit-feature-map/{SKILL.md, references/{ingestion-contract,scoring}.md, scripts/{repo_ingest,verify_scores,render_map}.py}` |
| Metrics | `govkit-metrics-emit/{SKILL.md, references/event_schema.md}` |
| Slice (write protocol source) | `govkit-feature-slice/references/tracker-writeback.md` |
| Manifests | `plugins/govkit/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |

# govkit

Governed, AI-assisted delivery for feature teams: seven skills that take a feature from a
blank page to gated, evidence-backed execution — feature creation from an epic, refinement,
sizing and release slicing, a repo-side readiness gate, a corpus-wide feature map, synthetic
test data, and delivery metrics.

## What it does

GovKit's premise is that AI-assisted coding is safe when the spec is a contract: Gherkin the
whole team understands, NFRs with thresholds, evaluation criteria with gates, and an explicit
go/no-go — the **Development Token** — before any coding agent starts. The skills cover that
lifecycle in order:

1. **`govkit-feature-create`** — the generator. A Product Discovery coach that breaks an
   epic into workflow-aligned feature stubs (lightweight story mapping, MVP slicing, overlap
   checks) and authors one feature's full Draft 0 package: user stories, tagged Gherkin,
   `nfrs.md` with `TBD` where the team hasn't set thresholds, `eval_criteria.yaml`, Definition
   of Done, and privacy notes. Reads Aha!/Jira/Azure DevOps via MCP when connected but always
   asks before creating or modifying any record. Never scores its own output — Draft 0 goes
   to refine.
2. **`govkit-feature-refine`** — the 3 Amigos review of a generated Draft 0 (from
   `govkit-feature-create`, Aha!, an LLM, or a human). Scores against a 10-dimension quality rubric, finds blockers and evidence
   gaps, suggests rewritten Gherkin, and produces a Development Token *recommendation*. Also
   exposes a non-interactive batch mode that other callers use to score many features at once.
3. **`govkit-feature-slice`** — scenario sizing on the Scenario Complexity Matrix (Data &
   State, Integration, UI/UX at 1–3 points each) and MoSCoW release slicing onto `@mvp` /
   `@v1` / `@v2` Gherkin tags. Recommends; the PM decides. Proposes splits for Large (8–9
   point) scenarios and flags Large scenarios on the MVP critical path. Can write the tagged
   spec back to Jira or Aha! after an explicit confirmation.
4. **`govkit-feature-readiness`** — the repo-side 12-dimension gate that actually issues the
   Development Token once the package (`acceptance.feature`, `nfrs.md`, `eval_criteria.yaml`)
   is in the repository. No token, no coding.
5. **`govkit-synthetic-data`** — a seeded, repeatable Python Faker generator derived from the
   feature's Gherkin scenarios, plus committed data files.
6. **`govkit-metrics-emit`** — structured Tier 1 metric events (NDJSON) from a governed repo's
   exhaust: spec completeness, gate readiness, velocity/quality inputs.
7. **`govkit-feature-map`** — the cross-cutting corpus view: a self-contained HTML page with a
   producer/consumer chain diagram, one card per feature with its full spec, readiness badges
   from the refine or readiness rubric, and size badges with MVP/V1/V2 slice views. Ingests
   from Jira, Aha!, or a repo directory, and merges tracker records with repo-resident Gherkin.

What it does **not** do: write implementation code, create step definitions, replace Product /
QA / Engineering judgment, or write to a tracker without a previewed, explicitly confirmed
update. Batch scores are advisory — the blocker list is the gate, never the number.

### When to use it

Reach for govkit when you hear:

- "Break this epic into features" / "draft a spec for this new feature" → create
- "Review this spec / these acceptance criteria before we build" → refine
- "Is this ready for AI-assisted coding?" / "issue the token" → readiness
- "Slice this feature", "what's the MVP?", "how big is this?" → slice
- "Map this epic", "where is the release weakest?", "score all of these" → feature map
- "Generate test data for this feature" → synthetic data
- "Which features aren't gate-ready?" / "emit delivery metrics" → metrics

## Installation

```bash
claude plugin marketplace add Accelerated-Innovation/govkit-plugins   # once per machine
claude plugin install govkit@aipos
```

### Prerequisites

- **Python 3.11+** on PATH — the bundled scripts (map ingest/render/verify, sizing
  arithmetic, metrics emission, data generation) are plain Python.
- **PyYAML** (optional) — richer `eval_criteria.yaml` parsing during ingestion; a shallow
  fallback runs without it.
- **Faker** (`pip install faker`) — only for running generators produced by
  `govkit-feature-synthetic-data`.
- **Atlassian and/or Aha! MCP connectors** (optional) — required only for tracker ingestion
  and write-back; every skill also accepts pasted or file-based specs.

## Usage

The skills trigger from natural phrases (see above) — no slash commands. Run them in
lifecycle order: create → refine → slice → repo handoff → readiness → synthetic data →
coding → metrics, with the feature map at any point as the portfolio view. Each skill states
its own handoff: create emits Draft 0 and points to refine; refine recommends the token,
readiness issues it; slice recommends tags, the PM confirms them.

## Examples

### Example: Break an epic into feature stubs

- **Prompt:** `Break this epic into features for us. Epic: Client self-service portal. Elevator pitch: give agency clients a portal to see project status, review deliverables, and answer approval requests instead of emailing their account manager. Success metrics: 60% fewer status emails, approvals under 2 business days. Don't create anything in the tracker yet.`
- **Expected:** A workflow backbone of 4–7 user activities, an MVP/V1/V2 slice proposal
  tied to the success metrics, and a numbered feature candidate list (name, one-line scope
  boundary, slice) — with stub creation only *offered*, behind an explicit yes/no, never
  performed unprompted.
- **Safe to auto-run:** yes
- **Inputs:** none — the epic is inline; a tracker MCP is optional and used read-only here.

### Example: Review a Draft 0 spec

- **Prompt:** `Review this Draft 0 feature spec before refinement. Feature: Invoice approval routing. Rule: Invoices of $10,000 or more require finance manager approval. Scenario: High-value invoice routes to manager approval - Given a finance analyst has submitted an invoice for $12,500, When the invoice enters the approval workflow, Then the invoice status is "Pending manager approval".`
- **Expected:** A short prose summary of the feature (paragraphs, no headings or bullets),
  then a stop that asks the team to confirm the summary and answer the explicit "agentic
  behavior: yes or no?" question before any score, blocker list, or token recommendation is
  shown.
- **Safe to auto-run:** yes
- **Inputs:** none — the spec is inline.

### Example: Size and slice a feature's scenarios

- **Prompt:** `Size the scenarios of this feature and recommend MVP/V1/V2 slices. Feature: Password reset. Scenario: User resets a forgotten password - Given a registered user requests a reset link, When they follow the link and set a new password, Then they can sign in with the new password. Scenario: Reset links expire - Given a reset link older than 24 hours, When the user follows it, Then the reset is refused and a new link is offered.`
- **Expected:** A sizing table with three dimension judgments (integers 1–3) per scenario,
  points equal to the sum of the dimensions, a Small/Medium/Large band, a recommended slice
  with a one-line rationale per scenario — then a pause asking the PM to confirm or correct
  the recommendations. No tags are applied and nothing is written anywhere.
- **Safe to auto-run:** yes
- **Inputs:** Python 3 on PATH (the skill runs its bundled `compute_size.py` for the
  arithmetic).

### Example: Build a feature map from a repo directory

- **Prompt:** `Map the feature specs under ./features into a feature map with readiness scoring.`
- **Expected:** A `features.json` ingested from the directory (with per-feature rule and
  scenario counts shown before scoring), batch rubric scores verified by
  `verify_scores.py`, and a self-contained `feature-map.html` with the chain diagram, one
  card per feature, readiness badges, and the artifact ledger.
- **Safe to auto-run:** no
- **Inputs:** a directory of feature packages (`acceptance.feature` and friends); writes
  JSON and HTML files to the working directory.

### Example: Write tagged Gherkin back to Jira

- **Prompt:** `Apply the slices we agreed and update PROJ-142's acceptance criteria in Jira.`
- **Expected:** The exact final field content shown verbatim, a one-line delta summary, the
  named destination ("the Acceptance Criteria field of PROJ-142 in Jira"), a single explicit
  yes/no question — and only after a yes, the write, followed by a read-back verification.
- **Safe to auto-run:** no
- **Inputs:** Atlassian MCP connected with write access to the project.

## Limits and gotchas

- **The blocker list is the gate; scores are advisory.** A feature can score 7.5/10 and
  still be Blocked. Badges and dashboards built from these scores carry that caveat on their
  face.
- **Two rubric scales exist** — refine's 10 dimensions for tracker drafts, readiness's 12
  for repo packages. A 7.5 does not mean the same thing on both, and the map labels which
  one produced each badge.
- A spec that lives outside the ingested record scores near zero with a `notAssessable`
  flag — that means *unreviewable from this record*, not bad.
- Slice tags never land without the PM's confirmation; batch sizing recommendations render
  clearly marked as recommendations.
- The feature map writes local files (`features.json`, `scores.json`, `feature-map.html`);
  tracker write-back edits the record it read from and never creates or deletes records.
  Only `govkit-feature-create` creates records or package files — and only after showing
  the exact content, naming the destination, and getting an explicit yes; a standing
  "proceed" never authorizes creation.
- `govkit-feature-create` output is Draft 0: NFR and evaluation thresholds the team hasn't
  set are emitted as `TBD`, and the package is not reviewed, scored, or coding-ready until
  it has been through refine and readiness.
- Sizing points are complexity, not story points — don't feed them into sprint capacity math.

## Components

| Kind | Name | What it does |
|---|---|---|
| Skill | `govkit-feature-create` | Epic → story-mapped feature stubs; authors one feature's Draft 0 package (Gherkin, NFRs, eval_criteria.yaml, feature_source.md) |
| Skill | `govkit-feature-refine` | 3 Amigos review of Draft 0; token recommendation; batch scoring mode |
| Skill | `govkit-feature-slice` | Scenario sizing, MoSCoW slicing, `@mvp`/`@v1`/`@v2` tags, tracker write-back |
| Skill | `govkit-feature-readiness` | Repo-side 12-dimension gate; issues the Development Token |
| Skill | `govkit-feature-map` | Corpus map: chain, cards, readiness + size badges, slice filter |
| Skill | `govkit-synthetic-data` | Seeded Faker generator + data files from Gherkin scenarios |
| Skill | `govkit-metrics-emit` | Tier 1 NDJSON metric events from repo exhaust |
| Script | `compute_size.py` (slice) | All sizing arithmetic: points, bands, rollups, risk flags |
| Script | `repo_ingest.py`, `verify_scores.py`, `render_map.py` (map) | Ingest, score verification gate, HTML renderer |

## Version history

| Version | Change |
|---|---|
| 0.5.0 | Added `govkit-feature-create`: epic breakdown with story mapping and MVP slicing, feature stub creation (always confirm before creating), and Draft 0 package authoring aligned to the formats refine, readiness, map, and metrics already parse. |
| 0.4.0 | Added `govkit-feature-slice`; size badges, sizing panel, and MVP/V1/V2 slice filter in the feature map; scenario tags preserved through ingestion. |
| 0.3.0 | Added `govkit-feature-map` with batch scoring; clarified that refine recommends and readiness issues the Development Token. |
| 0.1–0.2 | Initial skills: refine (with quality rubric and checklists), readiness, metrics-emit, synthetic-data. |

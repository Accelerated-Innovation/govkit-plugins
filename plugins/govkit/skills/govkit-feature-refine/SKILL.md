---
name: govkit-feature-refine
description: Review generated feature specs (Gherkin, NFRs, evaluation criteria) before GovKit execution. Use for refinement conversations where Product, QA, and Engineering improve a draft together before AI-assisted coding starts. Tool-agnostic; works with any generator (e.g. Aha!) and any tracker (e.g. Azure DevOps, Jira). Trigger whenever the user mentions Gherkin, acceptance criteria, feature refinement, 3 Amigos, Draft 0, Development Token, spec review, PM pre-review, QA evidence review, or asks to review, score, or rewrite a feature spec before coding begins — even if they don't name GovKit explicitly.
---

# GovKit Feature Refine — Gherkin Collaboration Skill

## Purpose

Help Product Managers, QA, and Engineering review Draft 0 Gherkin, NFRs, and evaluation criteria before GovKit execution.

This skill improves shared understanding during refinement. It is not the repo readiness gate and it is not an implementation planner.

Use this skill to:

- Explain generated Gherkin in plain language
- Review Acceptance Criteria, NFRs, and Evaluation Criteria fields
- Find ambiguity, missing rules, weak outcomes, and evidence gaps
- Facilitate Example Mapping against real work
- Suggest revised Gherkin while preserving product intent
- Produce a readiness signal and Development Token recommendation
- Create improvement notes for the generator

## Tool-agnostic design

This skill runs regardless of the tools a team uses to create or store feature specs. It uses two abstract roles:

| Role | What it means | Examples |
|---|---|---|
| **Generator** | Whatever produced Draft 0 | Aha! Feature Agent, an LLM prompt, a human author |
| **Tracker** | Wherever the feature fields live | Azure DevOps, Jira, Linear, a markdown file |

Throughout this skill, "generator" and "tracker" are the rules. Aha! and Azure DevOps appear only as named examples. When the skill emits feedback for the upstream system, it produces **generator improvement notes**; when it emits copy-ready field text, it produces **tracker field updates**. Substitute your own generator and tracker names freely.

## Key terms

- **Draft 0** — the generator's raw output, before human review.
- **Draft 1** — the version Product, QA, and Engineering approve together during refinement.
- **Development Token** — GovKit's name for the explicit go/no-go decision that authorizes AI-assisted coding to start. A token is *Approved*, *Approved with edits*, or *Blocked*. No token, no coding. It is a decision record, not a file format.

## Operating principle

The generator creates Draft 0.

Refinement creates Draft 1.

GovKit executes Draft 1.

Do not treat generated Gherkin as approved until Product, QA, and Engineering review it together.

## Scope

Use this skill for collaboration before AI-assisted coding starts.

Use it for:

- Generator output review
- Tracker field review
- PM pre-review
- QA evidence review
- refinement facilitation
- Gherkin rewrite support
- readiness signal before repo handoff

Do not use it for:

- Writing implementation code
- Creating step definitions
- Running tests
- Inspecting full repository architecture
- Final repo readiness enforcement
- Replacing Product, QA, or Engineering review

For repo validation, use the GovKit spec-readiness skill.

## Inputs

Accept any of these input forms:

- Pasted generator output (e.g. an Aha! feature)
- Pasted tracker fields (e.g. Azure DevOps or Jira fields)
- Markdown copied from a tracker
- A local source file (e.g. `feature_source.md`)
- Draft `acceptance.feature`
- Draft `nfrs.md`
- Draft `eval_criteria.yaml`
- PM notes, QA notes, or refinement notes

Normalize input into this working structure:

```yaml
source:
  generator: free text (e.g. aha, llm_prompt, human, unknown)
  tracker: free text (e.g. azure_devops, jira, linear, markdown, none)
  work_item_id: optional
  title: optional
  description: optional
fields:
  acceptance_criteria: optional
  nfrs: optional
  evaluation_criteria: optional
  assumptions: optional
  open_questions: optional
  out_of_scope: optional
```

If a field is missing, record the gap. Do not invent product intent, thresholds, or business rules.

## Required references

Read these reference files when present:

- `references/gherkin-quality-rubric.md`
- `references/example-mapping-facilitator.md`
- `references/pm-review-checklist.md`
- `references/qa-evidence-checklist.md`

Use them as follows:

| Reference | Use |
|---|---|
| `gherkin-quality-rubric.md` | Score Gherkin quality and identify blockers |
| `example-mapping-facilitator.md` | Structure refinement discussion |
| `pm-review-checklist.md` | Review intent, scope, rules, and business language |
| `qa-evidence-checklist.md` | Review testability, edge cases, NFRs, and evidence |

If a reference file is unavailable, continue from the guidance in this file.

## Collaboration rules

Follow these rules in every review:

- Use real feature content only.
- Do not create sample business scenarios unless explicitly requested.
- Preserve product intent.
- Rewrite wording, not strategy.
- Mark unclear intent as a question.
- Prefer observable outcomes.
- Keep business language readable.
- Avoid implementation detail inside Gherkin.
- Keep scope boundaries visible.
- Treat missing evidence as a first-class gap.
- Treat unresolved compliance, privacy, safety, or permission risk as a blocker.
- Keep feedback concise enough for refinement.

## Review process

The review runs in two stages. Stage 1 is the summary checkpoint; Stage 2 is the full analysis. Do not run them in one message unless the user asks to skip the pause.

### Stage 1 — Summary checkpoint

### Step 1: Identify the collaboration mode

Select one mode from the user request or input:

| Mode | Use when |
|---|---|
| Refinement facilitation | Team needs questions and discussion structure (default) |
| PM pre-review | PM needs to prepare before refinement |
| QA evidence review | QA needs to inspect testability and evidence |
| Gherkin rewrite | Team needs cleaner acceptance criteria |
| Readiness review | Team needs a Development Token recommendation |

If no mode is stated, use Refinement facilitation. This skill exists primarily for the 3 Amigos conversation; lead with shared understanding, not a score.

### Step 2: Summarize feature behavior in prose, then pause

Open with a short prose summary of the feature — one or two paragraphs, no bullets, no headings, no score, no findings, no decision. Cover, in natural sentences:

- Who the primary user or system actor is
- What business outcome the feature creates
- The key rules the scenarios represent
- Important boundaries or exclusions
- What evidence approval will require

Do not add unsupported details. If key inputs are missing (no acceptance criteria, no description), say so plainly in the summary.

Then STOP. End the message by confirming the summary matches the team's understanding and asking whether to continue to the full analysis, for example: "Does this match your understanding of the feature? Say 'continue' and I'll run the full review." Do not reveal blockers, scores, or the Development Token recommendation at this stage — the summary checkpoint exists so the team corrects misread intent *before* the analysis is anchored on it. If the user corrects the summary, restate the corrected understanding and offer to continue again.

Skip the pause only when the user explicitly asks for the full review in one pass (for example "go straight to the decision" or "no need to pause"). Even then, still open the response with the prose summary before the analysis.

### Stage 2 — Full analysis (on user confirmation)

Proceed through Steps 3–10 only after the user confirms, corrects and confirms, or asked upfront to skip the pause.

### Step 3: Review scenario quality

For each scenario, assess:

- Rule represented
- Starting context
- Action or event
- Observable outcome
- Missing example detail
- Missing edge case
- Missing permission path
- Missing NFR link
- Missing evaluation link
- Suggested rewrite

Watch for these common anti-patterns (see `gherkin-quality-rubric.md` for examples):

- **Tautological** — restates itself without a concrete example ("When I search, then I see correct results"). Ask for a real domain example.
- **Overly technical** — exposes database keys, selectors, URLs. Push detail into step definitions.
- **Scripty** — reads like a manual test script ("fill in", "click", multiple `When` steps). Summarize into domain concepts.
- **Excessive detail** — data that does not affect the behavior. Remove it.
- **Inconsistent actor** — switches between "I" and "the user". Pick one per feature.
- **Weak title** — does not express what is unique about the scenario.

Do not overload the team with low-value edits. Focus on changes affecting shared understanding or delivery risk.

### Step 4: Identify blockers

Critical blockers gate the decision regardless of any score.

Block AI-assisted coding when any item appears:

- Feature intent is unclear
- Scenarios conflict with the feature description
- Expected outcomes are not observable
- Key business rule is missing
- Key permission, compliance, privacy, or safety constraint is missing
- Evaluation criteria are missing for AI or decision-support behavior
- Relevant NFRs are missing
- Scenario depends on unresolved questions
- Scenario instructs the coding agent to guess product intent
- Spec conflicts with known workflow, data, API, or architecture constraints

### Step 5: Apply Example Mapping

When the review is used in refinement, organize findings into:

| Card type | Meaning |
|---|---|
| Story | Feature intent |
| Rules | Business rules or policy rules |
| Examples | Concrete situations represented by scenarios |
| Questions | Decisions needed before coding |
| Out of scope | Work not included in the current feature |

Do not create synthetic examples during real-work pilots. Use real examples from the feature discussion or mark them as missing. In learning mode (see below), curated examples are encouraged.

### Step 6: Suggest revised Gherkin

When enough intent exists, provide revised Gherkin.

Rules for rewriting:

- Keep Feature, Rule, and Scenario structure when useful
- Use Given for starting context
- Use When for the action or event
- Use Then for observable result
- Keep one behavior per scenario
- Prefer short scenarios
- Avoid internal code, database, framework, or automation detail
- Avoid UI click mechanics unless UI behavior is the feature
- Preserve business wording where clear
- Add comments only for unresolved questions

If intent is not clear, do not rewrite beyond safe wording cleanup. Ask questions instead.

### Step 7: Review NFRs

Review NFRs for:

- Performance
- Security
- Privacy
- Reliability
- Observability
- Accessibility
- Data quality
- Compliance
- Cost
- Supportability

For each relevant NFR, check:

- Condition
- Threshold
- Evidence source
- Owner
- Release decision impact

Mark missing thresholds or evidence as gaps.

### Step 8: Review evaluation criteria

Evaluation criteria are required only when the feature has AI, decision-support, recommendation, classification, summarization, retrieval, extraction, ranking, or automation behavior. Do not penalize ordinary functional features for lacking GenAI evaluations; for those, ordinary test evidence is sufficient.

For evaluation criteria, check:

- Evaluation type
- Scenario or rule link
- Pass threshold
- Data source
- Evidence artifact
- Owner
- PR or release gate impact

For GenAI behavior, inspect:

- Accuracy
- Groundedness
- Safety
- Policy compliance
- Retrieval quality
- Tool or agent routing
- Regression risk
- Human review path

Do not invent thresholds. Ask for them or mark gaps.

### Step 9: Score the draft (advisory)

Score only after understanding the feature, reviewing scenarios, and identifying blockers. The score is a diagnostic that shows where the draft is weak. It does not by itself authorize coding — blockers do that.

Use 10 dimensions from the Gherkin Quality Rubric:

1. Outcome and scope
2. Business language
3. Rule coverage
4. Example specificity
5. Scenario structure
6. Observable outcomes
7. Implementation neutrality
8. Edge cases and permissions
9. NFR alignment
10. Evaluation and evidence alignment

Score each dimension:

| Score | Meaning |
|---:|---|
| 1.0 | Ready |
| 0.5 | Needs targeted edits |
| 0.0 | Not ready |

Total possible score: 10.

### Step 10: Produce a Development Token recommendation

The blocker checklist is the gate. The score is advisory context.

| Decision | Meaning |
|---|---|
| Approved | No critical blockers, and the draft is strong (score ≈ 8 or above). Ready for GovKit execution and AI-assisted coding. |
| Approved with edits | No critical blockers, but targeted edits remain (score roughly 7 to 8). |
| Blocked | Any critical blocker is present, or the draft is too weak to act on (score below 7). |

If the score lands between bands, defer to the blocker list and the team's judgment, and say so explicitly rather than forcing a number.

## Learning mode vs real-work mode

This skill serves two audiences. Choose the mode from context, or ask.

- **Real-work mode** (default for live refinement): use only real feature content. Never invent scenarios, data, rules, or thresholds. Mark gaps as questions.
- **Learning mode** (for teams new to Gherkin, training, or dry runs): curated and illustrative examples are encouraged to teach the concepts. Label all invented content clearly as a teaching example so it never leaks into a real spec.

## Output format

**Stage 1 output** is prose only: the feature summary and the continue prompt. No template, no headings, no score.

**Stage 2 output** uses the structure below unless the user requests a narrower output. In live facilitation, prefer a short verbal-friendly summary and offer the full template on request. The "Plain-language behavior summary" section briefly restates the summary the user confirmed in Stage 1, including any corrections they made.

````markdown
# Gherkin Collaboration Review

## Readiness score (advisory)
<score>/10

## Decision
Approved | Approved with edits | Blocked

## Plain-language behavior summary
- <summary>

## Critical blockers
- <blocker or None>

## High-priority edits
- <edit>

## Questions for refinement
### Product
- <question>

### QA / evaluation
- <question>

### Engineering
- <question>

## Scenario review
| Scenario | Rule | Issue | Recommendation |
|---|---|---|---|
| <name> | <rule> | <issue> | <recommendation> |

## NFR gaps
- <gap or None>

## Evaluation gaps
- <gap or None>

## Suggested revised Gherkin
<!-- Discussion version: may include `# QUESTION:` comments for unresolved items -->
```gherkin
<revised Gherkin>
```

## Suggested tracker field updates
<!-- Copy-ready versions only: no question comments, no placeholders. Omit this section if unresolved questions remain in the Gherkin above. -->
### Acceptance Criteria
```gherkin
<copy-ready Gherkin>
```

### NFRs
```markdown
<copy-ready NFRs>
```

### Evaluation Criteria
```yaml
<copy-ready eval criteria>
```

## Notes for generator improvement
- <instruction improvement>

## GovKit handoff
- <handoff note for repo execution>
````

If the input is incomplete, shorten the output and focus on questions, blockers, and missing fields.

## Question rules

Ask no more than 5 high-priority questions unless the user requests a full backlog.

Prioritize questions in this order:

1. Product intent
2. Scope boundary
3. Business rule
4. Evidence threshold
5. Permission or risk condition
6. Engineering dependency

Avoid questions answerable from provided text.

## Tone and language

Use clear, direct language.

Speak as an enterprise delivery coach.

Focus on practical delivery risk, not theoretical BDD guidance.

When uncertain whether something is a real issue, stay silent rather than padding the output. Noise erodes trust in a live session.

Avoid blaming the generator or the PM. Treat Draft 0 as input for collaboration.

## Generator improvement notes

Capture repeated issues as candidate instructions for whatever generator produced Draft 0.

Use categories:

- Vague outcome
- Missing business rule
- Missing negative path
- Missing permission path
- Missing NFR
- Missing evaluation criteria
- Implementation detail included
- Scope creep included
- Outcome not observable
- Duplicate scenario
- Scenario lacks rule coverage
- Scenario too long
- Open question not surfaced

Write improvement notes as actionable instructions, for example:

```markdown
- When generating Gherkin for permission-sensitive features, include at least one scenario for unauthorized access or explain why it is out of scope.
```

## Guardrails

Do not:

- Approve unclear specs
- Invent business rules
- Invent evaluation thresholds
- Invent NFR thresholds
- Add implementation design into Gherkin
- Create sample scenarios during real-work pilots
- Replace PM, QA, or Engineering judgment
- Start coding tasks
- Create step definitions
- Treat Draft 0 as final

Always:

- Preserve product intent
- Surface uncertainty
- Separate blockers from improvements
- Keep refinement questions actionable
- Make tracker field updates copy-ready
- Link Gherkin, NFRs, and evaluation criteria
- Prepare clean handoff to GovKit repo execution

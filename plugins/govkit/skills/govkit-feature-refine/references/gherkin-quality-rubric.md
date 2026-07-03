# Gherkin Quality Rubric

> **Tool-agnostic.** *Generator* = whatever produced Draft 0 (e.g. Aha!, an LLM prompt, a human author). *Tracker* = wherever the feature fields live (e.g. Azure DevOps, Jira, Linear, a markdown file). Named tools are examples, not requirements.

## Contents

- [Purpose](#purpose)
- [Applies to](#applies-to)
- [Review principle](#review-principle)
- [Scoring model](#scoring-model)
- [Critical blockers](#critical-blockers)
- [Rubric dimensions](#rubric-dimensions)
- [Reviewer responsibilities](#reviewer-responsibilities)
- [Review output](#review-output)
- [Development Token decision](#development-token-decision)
- [Skill response format](#skill-response-format)
- [Generator feedback rules](#generator-feedback-rules)
- [Repo readiness note](#repo-readiness-note)

## Purpose

Use this rubric to review generated Gherkin before AI-assisted coding starts.

The goal is not perfect syntax. The goal is shared understanding across Product, QA, and Engineering.

GovKit treats Gherkin as a behavior contract. The contract is ready when the team agrees on:

* What the feature does
* Which rules matter
* Which outcomes prove success
* Which quality constraints apply
* Which evidence will be produced
* Which assumptions remain open

## Applies to

Use this rubric for:

* generated Feature Acceptance Criteria
* tracker Acceptance Criteria fields
* Refinement / Spec Alignment reviews
* GovKit collaboration skill reviews
* GovKit repo readiness checks
* AI coding agent handoff reviews

## Review principle

The generator creates Draft 0.

Refinement creates Draft 1.

GovKit executes Draft 1.

Do not treat AI-generated Gherkin as approved until Product, QA, and Engineering review it together.

## Scoring model

Score each dimension from 0 to 1.

| Score | Meaning              |
| ----: | -------------------- |
|   1.0 | Ready                |
|   0.5 | Needs targeted edits |
|   0.0 | Not ready            |

Total possible score: 10.

The critical blocker list is the gate. The numeric score is advisory: it shows where the draft is weak but does not by itself authorize coding. If any critical blocker is present, the decision is Blocked regardless of score.

| Total score    | Decision (when no blocker is present)  |
| -------------- | -------------------------------------- |
| ≈ 8 or above   | Ready for GovKit execution             |
| roughly 7 to 8 | Needs targeted edits before execution  |
| below 7        | Block AI-assisted coding               |

If the score lands between bands, defer to the blocker list and the team's judgment, and say so explicitly rather than forcing a number. SKILL.md is the canonical source for the decision rules; this rubric elaborates on how to score each dimension.

## Critical blockers

Block AI-assisted coding when any item below is present:

* Feature intent is unclear
* Scenarios conflict with the feature description
* Expected outcomes are not observable
* Key business rule is missing
* Key permission, compliance, privacy, or safety constraint is missing
* Evaluation criteria are missing for AI or decision-support behavior
* Relevant NFRs are missing
* Scenario depends on unresolved questions
* Scenario instructs the coding agent to guess product intent
* Spec conflicts with known workflow, data, API, or architecture constraints

This list is identical to the critical blocker list in SKILL.md. If the two ever differ, SKILL.md wins.

## Rubric dimensions

### 1. Outcome and scope

The feature has one clear responsibility, and each scenario belongs inside the feature boundary.

| Score | Guidance                                                                          |
| ----: | --------------------------------------------------------------------------------- |
|   1.0 | Scenarios stay inside the feature scope and support the stated outcome.           |
|   0.5 | Most scenarios fit, but some scope or outcome wording needs refinement.           |
|   0.0 | Scenarios mix multiple features, introduce hidden work, or miss the main outcome. |

Review prompts:

* What outcome should this feature create?
* Which scenario feels outside the current feature?
* What work belongs in a later feature?

### 2. Business language

Scenarios describe behavior in language Product, QA, and Engineering understand together.

| Score | Guidance                                                                  |
| ----: | ------------------------------------------------------------------------- |
|   1.0 | Language is clear, business-facing, and readable by non-engineers.        |
|   0.5 | Meaning is understandable, but wording needs cleanup.                     |
|   0.0 | Language is technical, vague, or hard for business reviewers to validate. |

Review prompts:

* Would a PM explain this scenario to a stakeholder without translation?
* Does the scenario describe user or system behavior?
* Which phrase needs plainer wording?

### 3. Rule coverage

Important business rules are represented by scenarios.

| Score | Guidance                                        |
| ----: | ----------------------------------------------- |
|   1.0 | Each key rule has scenario coverage.            |
|   0.5 | Some rules are covered, but gaps remain.        |
|   0.0 | Rules are implied, missing, or buried in prose. |

Review prompts:

* What rule is this scenario proving?
* Which rule lacks a scenario?
* Which scenario exists without a clear rule?

### 4. Example specificity

Scenarios include concrete roles, states, inputs, events, and outcomes where useful.

| Score | Guidance                                                                      |
| ----: | ----------------------------------------------------------------------------- |
|   1.0 | Scenarios are concrete enough for QA and Engineering to validate.             |
|   0.5 | Scenarios are mostly clear, but some inputs, states, or outcomes need detail. |
|   0.0 | Scenarios are generic, abstract, or open to multiple interpretations.         |

Review prompts:

* What concrete situation does this scenario represent?
* What data, role, state, or event is missing?
* What would cause two people to interpret this differently?

### 5. Scenario structure

Each scenario follows clear Given / When / Then structure.

| Score | Guidance                                                                     |
| ----: | ---------------------------------------------------------------------------- |
|   1.0 | Scenario has clear context, action, and outcome. Steps are short and direct. |
|   0.5 | Structure is understandable, but steps are too long, mixed, or uneven.       |
|   0.0 | Context, action, and outcome are confused or missing.                        |

Guidance:

* Prefer 3 to 5 steps for common scenarios.
* Use Given for starting context.
* Use When for the action or event.
* Use Then for observable outcome.
* Use And only when it improves readability.

Review prompts:

* Is the Given a true starting state?
* Is the When a single meaningful action or event?
* Is the Then an outcome, not another action?

### 6. Observable outcomes

Then steps describe visible, testable, or auditable results.

| Score | Guidance                                                                             |
| ----: | ------------------------------------------------------------------------------------ |
|   1.0 | Outcomes are observable through UI, API, event, report, audit trail, metric, or log. |
|   0.5 | Outcomes are partly observable, but evidence needs detail.                           |
|   0.0 | Outcomes rely on hidden implementation or unstated assumptions.                      |

Review prompts:

* How will QA prove this outcome occurred?
* What artifact, response, event, record, or metric proves success?
* Is the expected result visible outside internal code paths?

### 7. Implementation neutrality

Gherkin states behavior without prescribing internal design.

| Score | Guidance                                                                                                        |
| ----: | --------------------------------------------------------------------------------------------------------------- |
|   1.0 | Scenarios avoid code, database, framework, and internal design detail unless essential to the feature contract. |
|   0.5 | Some implementation detail appears, but the behavior remains clear.                                             |
|   0.0 | Scenario reads like a technical task list instead of behavior criteria.                                         |

Review prompts:

* Is this behavior or implementation?
* Would a different implementation still satisfy the scenario?
* What technical detail belongs in the engineering plan instead?

### 8. Edge cases and permissions

Relevant failure paths, boundaries, invalid states, duplicate actions, and permissions are considered.

| Score | Guidance                                                                                              |
| ----: | ----------------------------------------------------------------------------------------------------- |
|   1.0 | Important negative, boundary, permission, and exception paths are included or intentionally deferred. |
|   0.5 | Some edge cases are included, but key risks remain open.                                              |
|   0.0 | Only the happy path exists, with no decision about risk paths.                                        |

Review prompts:

* What happens when input is missing, invalid, duplicated, late, or unauthorized?
* Which role is allowed to perform the action?
* What failure would create production risk?

### 9. NFR alignment

Scenarios link to relevant quality constraints.

| Score | Guidance                                                            |
| ----: | ------------------------------------------------------------------- |
|   1.0 | Relevant NFRs are present and measurable.                           |
|   0.5 | NFRs exist, but thresholds, conditions, or evidence are incomplete. |
|   0.0 | Relevant NFRs are missing or vague.                                 |

NFR areas to check:

* Performance
* Security
* Privacy
* Reliability
* Observability
* Accessibility
* Data quality
* Compliance
* Cost
* Supportability

Review prompts:

* Which NFR applies to this scenario?
* What threshold makes the NFR measurable?
* What evidence proves the NFR passed?

### 10. Evaluation and evidence alignment

Scenarios connect to evaluation criteria, test evidence, or release evidence.

| Score | Guidance                                                    |
| ----: | ----------------------------------------------------------- |
|   1.0 | Each important scenario maps to pass/fail evidence.         |
|   0.5 | Evidence is named, but thresholds or artifacts need detail. |
|   0.0 | The team has no clear way to prove success.                 |

Evidence types:

* Automated test result
* Manual test result
* Evaluation report
* Golden dataset result
* Trace or log evidence
* Security review result
* Performance report
* Accessibility scan
* Data quality report
* PR checklist item

Review prompts:

* What evidence will be attached to the PR?
* What threshold decides pass or fail?
* Who owns the evidence?

## Reviewer responsibilities

### Product Manager

Owns:

* Feature intent
* Business rules
* User value
* Scope boundaries
* Out-of-scope decisions
* Final product acceptance language

The PM should challenge:

* Vague outcomes
* Missing rules
* Hidden scope
* Confusing business language
* Scenarios misaligned with the feature goal

### QA / evaluation owner

Owns:

* Testability
* Edge cases
* Evaluation criteria
* Evidence expectations
* Pass/fail thresholds
* Risk coverage

QA should challenge:

* Outcomes with no evidence path
* Missing negative paths
* Missing permission checks
* Missing data conditions
* Missing evaluation thresholds

### Engineering

Owns:

* Repo fit
* Architecture constraints
* Implementation feasibility
* Test automation path
* AI coding agent readiness
* Technical assumptions

Engineering should challenge:

* Implementation detail inside Gherkin
* Missing dependencies
* Missing API, event, or data contract detail
* Contradictions with existing architecture
* Ambiguity dangerous for coding agents

## Review output

A completed review should produce:

* Final Gherkin for the tracker Acceptance Criteria field
* Final NFRs for the tracker NFRs field
* Final evaluation criteria
* Resolved questions
* Deferred questions
* Out-of-scope notes
* GovKit readiness score
* Development Token decision

## Development Token decision

Use this decision language:

| Decision            | Meaning                                                  |
| ------------------- | -------------------------------------------------------- |
| Approved            | Ready for GovKit execution and AI-assisted coding.       |
| Approved with edits | Minor changes required before execution.                 |
| Blocked             | Do not start AI-assisted coding. Resolve blockers first. |

## Skill response format

Use the output format defined in SKILL.md (`# Gherkin Collaboration Review`). Do not use a different template. SKILL.md's template is canonical; it includes the plain-language behavior summary, scenario review table, tracker field updates, and GovKit handoff sections in addition to the score, decision, blockers, edits, questions, gaps, revised Gherkin, and generator notes.

## Generator feedback rules

When the review finds a repeated issue, add an improvement note for the generator.

Common feedback categories:

* Too vague
* Too many steps
* Missing negative path
* Missing permission path
* Missing NFR
* Missing evaluation criteria
* Implementation detail included
* Scope creep included
* Outcome not observable
* Scenario duplicates another scenario
* Rule missing scenario coverage

## Repo readiness note

This rubric supports collaboration review. Repo-based readiness still requires GovKit validation against:

* Existing architecture
* Existing tests
* Existing step definitions
* Local GovKit configuration
* CI workflow
* Test data strategy
* Evaluation runner

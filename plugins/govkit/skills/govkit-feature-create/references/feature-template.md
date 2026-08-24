# Feature Package Templates

> **Tool-agnostic.** These are the artifacts the rest of GovKit reads. The same content pastes into any tracker's fields — see `tracker-adapters.md` for the field mapping.

## Contents

- [The package](#the-package)
- [feature_source.md](#feature_sourcemd)
- [User stories](#user-stories)
- [Structured description](#structured-description)
- [nfrs.md](#nfrsmd)
- [Definition of Done](#definition-of-done)
- [Privacy impact](#privacy-impact)
- [eval_criteria.yaml](#eval_criteriayaml)

## The package

One directory per feature, named by its tracker key or a slug when there is no tracker:

```text
features/<key>/
  feature_source.md      # stories, description, DoD, privacy — always
  acceptance.feature     # tagged Gherkin — always
  nfrs.md                # measurable constraints — always
  eval_criteria.yaml     # GenAI mode only
```

These filenames are not arbitrary. `govkit-feature-map`'s repo ingester and `govkit-feature-readiness`'s gate both look for exactly these names — writing them means the feature is readable by every downstream skill with no conversion step.

Stubs get the directory and a `feature_source.md` containing only the stub fields. The other files arrive in Feature mode.

## feature_source.md

```markdown
# <Feature Name>

| | |
|---|---|
| **Key** | <tracker key, or `—`> |
| **Epic** | <epic name and link, or `—`> |
| **Release** | <release / slice> |
| **Type** | <feature type> |
| **Owner** | <owner> |
| **Primary persona** | <persona> |
| **GenAI** | yes / no |
| **Status** | Draft 0 — not yet refined |

## Primary user story

As a <primary persona>, I need <capability> so that <outcome>.

## Secondary user stories

- As a <persona>, I need <capability> so that <outcome>.

## Summary

<2–4 sentences in plain language. What becomes possible that wasn't before.>

## Functional scope

- <what this feature does>

## Out of scope

- <what it deliberately does not do, and where that lives instead>

## Dependencies

- <system, team, or feature this depends on, and what happens if it isn't ready>

## Key user flows

1. <flow name> — <the path the user takes, in one line>

## Definition of Done

<checklist — see below>

## Privacy impact

<section — see below>

## Open questions and gaps

- <anything unresolved, unmeasured, or assumed. This section is a feature, not an admission.>
```

The **Status** line matters. Draft 0 is unreviewed by definition, and the header says so on the artifact itself, where it survives being pasted somewhere without context.

## User stories

```
As a <persona>, I need <capability> so that <outcome>.
```

The persona is a specific role, not "the user" where a real role is known. The capability is what they can do, not how the system does it. The outcome is why they care.

The most common defect is a restated capability in the `so that`:

| | |
|---|---|
| ✗ | …so that the claim is routed. |
| ✓ | …so that high-value claims reach a senior adjuster before the SLA clock runs out. |

If the `so that` can be deleted without losing information, it isn't an outcome yet.

Secondary stories exist for other personas or other outcomes of the same capability. Zero secondary stories is a valid, common answer — do not manufacture them for symmetry.

## Structured description

| Section | What belongs in it | Failure mode when skipped |
|---|---|---|
| **Summary** | Plain language, no jargon, 2–4 sentences | The feature means different things to different readers |
| **Functional scope** | What it does, as capabilities | Scope creeps because nothing said where it ends |
| **Out of scope** | What it deliberately doesn't do, and where that lives | The single largest source of rework |
| **Dependencies** | What must exist first, and the consequence if it doesn't | Discovered mid-sprint |
| **Key user flows** | The paths through the feature, one line each | Scenarios get written without a journey behind them |

**Out of scope is not optional.** It is the section PMs skip most and the one that prevents the most rework. If the PM has nothing to put in it, prompt once from the adjacent features on the story map: what would someone reasonably assume this covers that it doesn't?

## nfrs.md

A markdown table. The column names matter — this is the shape `govkit-feature-map` and `govkit-feature-readiness` parse.

```markdown
# Non-Functional Requirements — <Feature Name>

| ID | Dimension | Requirement | Threshold | Evidence | Gap |
|---|---|---|---|---|---|
| N1 | Performance | Claim routing completes within the submission request | p95 < 400 ms | Load test in CI | |
| N2 | Security | Only adjusters in the assigned region can open a claim | 0 cross-region reads | Authz integration test | |
| N3 | Compliance | Routing decisions are retained for audit | 7 years | Retention policy doc | Threshold unconfirmed |
```

Categories to walk, in order: **Performance · Security · Scalability · Reliability · Compliance**.

In GenAI mode, also walk: **Latency** (user-perceived, including model time) · **Token cost** (per request or per period) · **Model and vendor constraints** (which models are permitted, data residency, no-train guarantees) · **Observability** (what is logged about model behavior, and for how long) · **Evaluation cadence** (how often the eval set runs, and what a regression blocks).

**An NFR without a threshold is a wish.** `govkit-feature-readiness` blocks on unmeasurable NFRs, so a missing number is going to surface either way. Write the requirement, leave `Threshold` empty, and name it in `Gap`. Never invent the number: a fabricated `p95 < 200 ms` becomes a commitment the moment someone reads this file without you in the room.

## Definition of Done

```markdown
## Definition of Done

- [ ] All acceptance criteria scenarios pass
- [ ] Automated tests written and passing in CI
- [ ] NFR thresholds verified with evidence
- [ ] Code reviewed and merged
- [ ] Security checks completed          <!-- if the feature touches authn/authz/sensitive data -->
- [ ] Performance checks completed       <!-- if the feature has a performance NFR -->
- [ ] GenAI evaluation thresholds met    <!-- GenAI mode -->
- [ ] Privacy mitigations implemented    <!-- if the feature processes personal data -->
- [ ] Documentation updated
```

Include the conditional lines only when they apply — a DoD full of permanently-inapplicable items trains people to skim it. Add team-specific items when the PM names them.

## Privacy impact

Ask directly: *does this feature process personal or sensitive data?*

If no, record the answer and move on:

```markdown
## Privacy impact

No personal or sensitive data is processed by this feature.
```

If yes:

```markdown
## Privacy impact

**Data processed:** <categories — name them; "user data" is not a category>
**Lawful basis / purpose:** <why this data, for this purpose>
**Retention:** <how long, and what happens after>
**Access:** <who can see it, and how that is enforced>
**Mitigations:**
- <minimization, masking, encryption, access control, audit logging — whichever apply>
**Residual risk:** <what remains, and who accepted it>
```

Then add `@privacy` scenario coverage to the Gherkin. A privacy claim with no scenario proving it is a paragraph, not a control — and a missing privacy path is a named blocker at the readiness gate.

Where a Data Protection Impact Assessment is required, say so and name it as a dependency. Do not attempt to write one here.

## eval_criteria.yaml

GenAI mode only. This is the shape `govkit-feature-map` parses and `govkit-feature-readiness` checks.

```yaml
evaluation_criteria:
  - id: E1
    type: groundedness
    rule_link: "Summaries reflect only the uploaded claim documents"
    method: "LLM-as-judge over a 200-item labelled eval set"
    pass_threshold: ">= 0.95"
    gate: blocking

  - id: E2
    type: latency
    rule_link: "Summary returns within the adjuster's review flow"
    method: "p95 over the eval set, measured end to end"
    pass_threshold: "< 3s"
    gate: blocking

  - id: E3
    type: safety
    rule_link: "No claimant PII appears in a summary shown to an external partner"
    method: "PII detector over eval set outputs"
    pass_threshold: "0 detections"
    gate: blocking
```

| Field | Meaning |
|---|---|
| `id` | Stable identifier, referenced from `@evaluation` scenarios |
| `type` | What is being measured — groundedness, accuracy, latency, cost, safety, toxicity, refusal rate |
| `rule_link` | The business rule this evaluates, in the feature's own words |
| `method` | How it is measured, specifically enough that someone else could run it |
| `pass_threshold` | The number, with its comparator |
| `gate` | `blocking` or `advisory` — whether a failure stops the release |

Every criterion needs a `method` and a `pass_threshold`. Criteria without thresholds are a named readiness blocker, and a threshold you invented is worse than a gap you flagged: write `pass_threshold: "TBD"` with the gap listed in `feature_source.md` and let the PM supply the number.

Keep this draft narrow. Full evaluation design belongs to refinement and to the team's eval tooling — this file's job is to make sure the feature arrives at refinement with the evaluation question already asked.

---
name: govkit-feature-readiness
description: Validate whether an approved feature package (Gherkin, NFRs, evaluation criteria) is complete, consistent, repo-aware, and safe for AI-assisted coding. The repo-side readiness gate that runs after the feature refinement. Tool-agnostic;
---

# GovKit Feature-Readiness Skill

## Purpose

Decide whether an approved feature package is ready for GovKit repo execution and AI-assisted coding.

This skill is stricter than the GovKit Gherkin Feature Refine skill. Collaboration improves shared understanding during refinement. Readiness validates that the feature package is complete, internally consistent, repo-aware, and safe for a coding agent to execute without guessing.

Use this skill to:

- Validate a feature package copied into the repo
- Check Gherkin, NFRs, and evaluation criteria against the readiness rubric
- Confirm repo fit, evidence path, and AI coding agent safety
- Identify critical blockers before coding starts
- Produce a readiness report and Development Token decision

## Tool-agnostic design

This skill runs regardless of the tools a team uses. It uses two abstract roles:

| Role | What it means | Examples |
|---|---|---|
| **Generator** | Whatever produced Draft 0 | Aha! Feature Agent, an LLM prompt, a human author |
| **Tracker** | Wherever the feature fields live | Azure DevOps, Jira, Linear, a markdown file |

Aha! and Azure DevOps appear only as named examples. Substitute your own generator and tracker freely.

## Key terms

- **Draft 0** — the generator's raw output, before human review.
- **Draft 1** — the version Product, QA, and Engineering approved together during refinement (the input to this skill).
- **Feature package** — the set of repo files that carry Draft 1 into execution (see below).
- **Development Token** — GovKit's name for the explicit go/no-go decision that authorizes AI-assisted coding to start. *Approved*, *Approved with edits*, or *Blocked*. No token, no coding.

## Operating principle

The generator creates Draft 0.

Refinement approves Draft 1.

GovKit validates repo readiness.

AI-assisted coding starts only after the feature package passes this readiness gate.

## Scope

Use this skill for repo-side readiness validation after collaboration review is complete.

Use it for:

- Approved feature packages copied into the repo
- Pre-coding readiness checks
- AI coding agent handoff reviews
- PR preparation checks
- Development Token decisions

Do not use it for:

- Improving shared understanding during refinement (use the refine skill)
- Writing implementation code or step definitions
- Inventing product intent, rules, NFR thresholds, or evaluation thresholds
- Rewriting architecture to fit the feature
- Replacing human approval for risk-sensitive decisions

## Inputs

Inspect the feature package and supporting repo context.

Expected feature package:

```text
/features/<work-item-id>/
  acceptance.feature
  nfrs.md
  eval_criteria.yaml
```

Optional files:

```text
/features/<work-item-id>/
  architecture_preflight.md
  plan.md
```

Also inspect, when available: repo architecture docs, existing tests, existing step definitions, GovKit config, and the CI pipeline. If an input is missing, record the gap and decide whether it blocks implementation.

## Required references

Read this reference when present:

- `references/govkit-readiness-rubric.md`

It provides the 12 scoring dimensions, the critical blocker list, the Development Token rules, and the required readiness report format. If it is unavailable, continue from the guidance in this file.

## Readiness process

1. **Confirm package completeness.** Verify `acceptance.feature` exists; verify `nfrs.md` and `eval_criteria.yaml` exist where relevant; confirm source traceability back to the approved generator/tracker record.
2. **Validate the behavior contract.** Check Gherkin structure, behavior clarity, observable outcomes, and rule/edge-case coverage.
3. **Validate quality constraints.** Check NFRs for measurable thresholds, evidence, and owners. Check evaluation criteria only where AI, decision-support, or data behavior is present.
4. **Validate repo fit.** Confirm the spec aligns with architecture, existing tests, conventions, and that target areas are identifiable.
5. **Validate the evidence path.** Confirm the team knows how each outcome will be proven (tests, eval runs, CI evidence).
6. **Check AI coding agent safety.** Confirm the agent has enough context, that open questions are resolved or deferred, and that the spec does not ask it to invent intent.
7. **Identify critical blockers.** The blocker list is the gate (see rubric).
8. **Score (advisory) and decide.** Produce the readiness report and Development Token decision.

## Decision model

The critical blocker list is the gate. The 12-dimension score is advisory context that shows where the package is weak; it does not by itself authorize coding.

| Decision | Meaning |
|---|---|
| Approved | No critical blockers, and the package is strong (score ≈ 10 of 12 or above). Ready for execution. |
| Approved with edits | No critical blockers, but targeted edits remain (score roughly 8.5 to <10). Fix before coding starts. |
| Blocked | Any critical blocker is present, or the package is too weak to act on (score below 8.5). |

If the score lands between bands, defer to the blocker list and state that explicitly rather than forcing a number.

## Output format

Produce the readiness report defined in `references/govkit-readiness-rubric.md`. In short, it includes: work item, advisory score, decision, Development Token, critical blockers, required edits, spec package status, scenario/NFR/evaluation readiness tables, repo fit, AI coding agent instructions, "do not assume" list, deferred items, and the next GovKit step.

## Failure handling

When blocked, do not rewrite the spec into an approved state. For each blocker, return: the blocker, the likely owner, the exact change needed, the file or field, and why coding should not start.

## Guardrails

Do not:

- Invent product intent, business rules, NFR thresholds, or evaluation thresholds
- Hide unresolved questions
- Start implementation when blocked
- Rewrite architecture to fit the spec
- Treat collaboration approval as repo readiness approval
- Replace human approval for risk-sensitive decisions

Always:

- Validate the package as written
- Separate blockers from improvements
- Preserve traceability to the approved source
- Surface repo conflicts early
- Keep the Development Token decision explicit
- Produce a clean handoff for AI-assisted coding

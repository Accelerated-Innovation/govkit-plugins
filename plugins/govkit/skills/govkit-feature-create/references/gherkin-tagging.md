# Gherkin Structure and Automatic Tagging

> **Tool-agnostic.** These are standard Cucumber/Gherkin tags. A team can run `cucumber --tags @mvp` and execute exactly the MVP slice — that is the point, not a coincidence.

## Contents

- [Required structure](#required-structure)
- [Scenario writing rules](#scenario-writing-rules)
- [Tag vocabulary](#tag-vocabulary)
- [Automatic tag assignment](#automatic-tag-assignment)
- [GenAI mode requirements](#genai-mode-requirements)
- [Validation checks](#validation-checks)
- [Interop with govkit-feature-slice](#interop-with-govkit-feature-slice)

## Required structure

Always emit a complete, syntactically valid Gherkin artifact — never a fragment, never a bare list of scenarios.

```gherkin
@feature
Feature: <Feature Name>

  As a <primary persona>
  I want <capability>
  So that <outcome>

  Background:
    Given <shared setup, only when genuinely shared>

  @mvp @functional
  Scenario: <Clear scenario title>
    Given <precondition>
    When <the single action under test>
    Then <observable outcome>
```

Rules:

- Always include the `Feature:` header and the persona intent block. The intent block is what makes the file readable six months later by someone who never attended the refinement.
- Use `Background:` **only** when setup is genuinely shared by every scenario in the file. A `Background` that applies to three of five scenarios is a bug: it silently changes the meaning of the other two.
- Keep scenarios atomic — one behavior, one `When`.
- No implementation detail. "When the user submits the form", not "When a POST is sent to `/api/claims`". The Gherkin outlives the endpoint.
- Prefer several concise scenarios over one long one. A scenario with four `When` steps is usually three scenarios.
- Use `Scenario Outline` for genuine data variation of one behavior, not to compress unrelated cases into a table.

## Scenario writing rules

Every scenario needs an **observable outcome** — something a person or a test can check from outside the system. `Then the record is saved` is not observable; `Then the claim appears in the adjuster's queue with status "Pending review"` is.

This is the single most common Draft 0 defect and it is a named blocker in `govkit-feature-readiness`. Catching it here costs one sentence; catching it at the gate costs a round trip.

Ground every scenario in the feature's stated rules. If a scenario would require a business rule nobody has stated, that is a gap to surface — not a rule to invent.

## Tag vocabulary

### Delivery phase — exactly one required

| Tag | Meaning |
|---|---|
| `@mvp` | Critical path. The journey cannot fundamentally function without it. |
| `@v1` | Operational stability: common errors, validation, permissions. |
| `@v2` | Optimization, advanced UX, edge cases, secondary personas. **V2 or later** — this is also where explicitly deferred work goes. |

Exactly one per scenario. Never two. A scenario the PM has not decided on stays untagged and is reported as undecided — do not default it into a phase to make the file look complete.

**These three tags are the entire vocabulary.** Do not invent a fourth. `@v2` already means "V2 or later", so work the PM has parked indefinitely is `@v2`, and the *reason* it was parked belongs in the Out of Scope section of `feature_source.md` where it can carry an explanation a tag never could. A tag outside this set is not merely unrecognized downstream — it is silently discarded; see [Interop](#interop-with-govkit-feature-slice).

### Classification — at least one required

| Behavior | Tag |
|---|---|
| User-visible business behavior | `@functional` |
| Error handling, invalid input, failure paths | `@edge-case` |
| Authentication, authorization, security constraint | `@security` |
| Latency, throughput, load validation | `@performance` |
| Regulatory or statutory rule | `@compliance` |
| Personal or sensitive data handling | `@privacy` |
| Model-generated behavior | `@genai` |
| A measurable evaluation threshold | `@evaluation` |
| Invocation of an external tool or function by a model | `@tool-use` |
| Harm, abuse, or unsafe-output prevention | `@safety` |

More than one is normal and expected: `@v1 @edge-case @security` is a well-tagged scenario.

Preserve any tag this skill does not own — `@wip`, `@smoke`, team conventions — exactly as found.

## Automatic tag assignment

**Derive tags. Do not ask the PM to pick them.**

Delivery phase comes from the feature's confirmed slice. Classification comes from the scenario's own behavior, using the table above. Both are mechanical enough that asking wastes the PM's attention on the one part of the process where their judgment adds nothing.

Ask for clarification **only** when:

1. The feature's slice is genuinely unknown (no slice was confirmed in Epic mode and none was given).
2. A scenario spans delivery phases — part of it is MVP and part is not. That is usually a split, so propose the split rather than the tag.
3. The scenario's intent cannot be classified from its text, which normally means the scenario itself is unclear and needs rewriting first.

When derivation is ambiguous but the scenario is sound, pick the tag the scenario's text best supports and note the call in one line rather than stopping the flow.

## GenAI mode requirements

When GenAI mode is active, the file must satisfy all of:

- At least one scenario tagged `@genai` — the model-generated behavior itself.
- At least one scenario tagged `@evaluation` with a **measurable, threshold-based** outcome.
- Any scenario where the model invokes an external tool or function tagged `@tool-use`.
- Hallucination, groundedness, or unsafe-output validation tagged `@compliance` or `@safety`.

Generate these without prompting the PM. They are the difference between a GenAI feature that can be gated and one that ships on vibes.

An `@evaluation` scenario must assert a number, and the number must come from the PM or from inherited epic criteria — never from you:

```gherkin
  @mvp @genai @evaluation
  Scenario: Summaries stay grounded in the source claim
    Given a claim file with 12 uploaded documents
    When the assistant generates a claim summary
    Then every factual statement in the summary is traceable to a source document
    And the groundedness score is at least 0.95 across the evaluation set
```

If the PM has not given a threshold, write the scenario with the threshold marked as an open gap (`Then the groundedness score is at least <TBD — threshold needed>`) and list it in the summary as a gap. A `0.95` you invented will be treated as a commitment by everyone downstream.

## Validation checks

Run these before presenting Gherkin. Fix what fails — a missing tag is a defect to correct, not a question to ask.

1. Every scenario has **exactly one** delivery-phase tag (or is deliberately untagged and reported as undecided).
2. Every delivery-phase tag is one of `@mvp`, `@v1`, `@v2` — nothing else. Anything outside that set is discarded silently downstream.
3. Every scenario has **at least one** classification tag.
4. No scenario is untagged by accident.
5. No scenario carries two delivery-phase tags.
6. GenAI mode: `@genai` present, `@evaluation` present, tool use tagged `@tool-use`, safety validation tagged `@compliance` or `@safety`.
7. Delivery tags are consistent with the feature's confirmed slice — an `@mvp` scenario in a V2 feature is either a mis-tag or a scoping error, and both are worth a line.
8. Every `@evaluation` scenario asserts a threshold, or marks the threshold as an open gap.
9. Every scenario has an observable outcome.
10. The file parses: `Feature:` header present, persona block present, no orphaned steps.

Correcting a tag needs no announcement. **Hiding the result does** — always present the full Gherkin plus a one-line coverage summary so the tagging is inspectable even though it was automatic:

> `5 scenarios · 2 @mvp, 3 @v1 · 3 @functional, 1 @edge-case, 1 @genai + @evaluation`

If a check fails in a way you cannot fix without a product decision — a scenario with no observable outcome because nobody has said what the system should do — say so explicitly. That is a gap, not a formatting problem.

## Interop with govkit-feature-slice

`govkit-feature-slice` owns the `@mvp` / `@v1` / `@v2` vocabulary for **re-slicing existing scenarios**, per-scenario, using the Scenario Complexity Matrix and MoSCoW. This skill assigns the delivery tag once, at creation, from the feature's confirmed slice.

Two consequences worth stating plainly:

- **These tags are a starting position, not a final release commitment.** When slice re-decides a scenario, its decision wins — it judged the scenario; this skill judged the feature.
- **The vocabulary is closed, and enforced by code downstream.** `mvp` / `v1` / `v2` are hard-coded in `govkit-feature-slice`'s `compute_size.py` (`SLICES`) and `govkit-feature-map`'s `render_map.py` (`SLICE_TAGS`). A delivery tag outside that set fails silently and in three separate ways:

| Where | What happens to an unrecognized delivery tag |
|---|---|
| `render_map.py` — `scen_slice()` | Returns `""`, so the scenario gets no `data-slice` attribute: dimmed under every release filter, selectable by none |
| `render_map.py` — card rendering | Tag chips render only for known slice and size tags, so the tag is not displayed at all |
| `compute_size.py` — validation | `taggedSlice` outside `SLICES` fails the verdict outright; via tags it resolves to `null` and the scenario's points fall into the `untagged` bucket |

  None of these produce an error the PM will see. The scenario simply stops counting. Emit only the three tags above.

Size tags (`@small` / `@medium` / `@large`) belong to `govkit-feature-slice` and are computed from its script. **Never emit a size tag here** — a size judged before the scenarios were reviewed is a guess wearing a badge.

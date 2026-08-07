# 7 — Viability brief

**Produces:** the **Validation Decision** — go, no-go, or revise.

This is not the seventh item on a list. It is Pillar 2's primary output and the hard gate
between Build-to-Learn and Build-to-Earn — in the AIPOS's words, *"the single most
consequential gate"* and *"the moment specifications are born."* Everything else in this
skill exists to feed it.

Treat it accordingly. The brief is decision-grade, not ceremonial: someone reads it and
commits or declines production engineering capacity.

## Before you start

Ask what evidence exists, then say plainly what's thin. A viability brief assembled over
gaps is still worth writing — but only if the gaps are visible in it. A brief that reads
as confident when three of its four legs are assumption is the most dangerous artifact this
skill can produce, because it travels further than the person who wrote it and gets quoted
by people who never saw the evidence.

If the honest answer is *we don't know enough to decide*, that is a legitimate output.
Write **revise**, name the one or two things that would settle it, and say how long they'd
take. That is a better outcome than a manufactured go.

## The three questions

The decision must answer all three. The brief is organised around them because that is what
makes it readable by someone who wasn't in any of the sessions.

1. **Is the problem real and worth solving?** — interview guide, problem sizing
2. **Will the proposed solution actually solve it?** — prototype, demand test, eval stub
3. **Is it technically and economically feasible within acceptable constraints?** —
   feasibility spike, including data and context readiness

For each, state the answer, the evidence behind it, and your confidence. Where there is no
evidence, say so in the same voice — an empty cell is information.

## Output template

```markdown
# Viability brief — <opportunity>
## Validation Decision: **GO / NO-GO / REVISE**

<One paragraph. The decision, the single most important reason for it, and the biggest
risk being accepted by making it. Someone should be able to read only this and act
correctly.>

---

## Evidence base
<the four-line header from evidence-intake.md>

**Validation work completed:**
| Artifact | Done | Result |
|---|---|---|
| Interview guide | <date / not run> | <finding> |
| Problem sizing | | |
| Visual prototype | | |
| Demand test | | |
| Feasibility spike | | |
| Eval stub | | |

<Gaps stay visible. "Not run" is a finding.>

---

## 1. Is the problem real and worth solving?
**Answer:** <yes / no / partly> · **Confidence:** <high / medium / low>

<What we learned, marked [E/I/A]. Size, who has it, what it costs them, what they do
today.>

**What would change this:** <...>

## 2. Will the proposed solution actually solve it?
**Answer:** <...> · **Confidence:** <...>

<Prototype results — including whether users trusted it, not just whether they completed
the task. Demand signal against its baseline. Output quality against the stub's threshold.>

**What would change this:** <...>

## 3. Is it feasible and economic within acceptable constraints?
**Answer:** <...> · **Confidence:** <...>

<Spike findings. Data and context readiness verdict. Cost to serve at the volume the
sizing implies. The break point.>

**What would change this:** <...>

---

## Gap and risk log
| # | Gap or risk | Impact if wrong | Status | Owner |
|---|---|---|---|---|
| 1 | | | Open / accepted / retired | |

<Accepted risks are the honest part of a go decision. List them, so that when one lands
later it was a known bet rather than a surprise.>

## Output quality summary
<Where the eval stub landed, on which dimensions, and how the safety cases went. If no
stub was run and the feature is model-based, say so — it is a material gap in a go.>

## Recommended MVP scope
**In:** <the smallest thing that delivers the validated value>
**Out:** <what validation showed can wait — and what evidence says so>
**Why this line:** <...>

<Scope that narrowed because of what validation taught is the clearest sign the work paid
for itself. Say what changed and why.>

## Handoff to Build-to-Earn
<Name what Pillar 3 will need. Name only — writing them out is Pillar 3's job, and
producing them here applies production governance to work that hasn't earned it yet.>
- **Problem statement:** <one line, ready to be specified>
- **MVP scope:** as above
- **Evaluation criteria to be derived from:** <the stub's dimensions and thresholds>
- **Guardrail requirements to be derived from:** <the safety cases and boundary findings>
- **Known architecture and data constraints:** <from the spike>

## If NO-GO or REVISE
**What we learned that was worth the cost:** <...>
**What would have to be true to revisit:** <...>
**Where the evidence goes:** <so the next person doesn't redo this>

<A no-go that produces reusable learning is a successful Pillar 2, not a failed one.
Failing here is what prevents failure in the much more expensive half that follows.>
```

## Writing the decision itself

- **Lead with it.** The decision goes in the first line, not the conclusion. Readers who
  stop after a paragraph should stop with the right answer.
- **Confidence is not optional.** A go at low confidence is a real and sometimes correct
  position — but it must be labelled, because it changes how much the organisation should
  bet.
- **Name what you're accepting.** Every go accepts risk. Listing it converts a future
  surprise into a recorded bet, and it is what makes the decision defensible later.
- **Don't let scope drift in.** If validation didn't test it, it doesn't belong in the MVP
  scope. The most common way a viability brief goes wrong is quietly restoring everything
  the prototype deliberately left out.
- **Revise is a real answer.** Under-used, because it feels indecisive. It is usually the
  most accurate one: the problem is real, the solution isn't right yet, and here is the
  narrower thing worth testing next.

## After the decision

Remind the PM once:

> Record the decision and its evidence against the opportunity — with a verdict and a
> signal strength — so the discovery engine picks it up and the next person doesn't redo
> this work.

Offer to write it back to the tracker. Do it only on explicit approval.

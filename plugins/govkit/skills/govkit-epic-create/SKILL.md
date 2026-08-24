---
name: govkit-epic-create
description: Coach a Product Manager through creating or improving an Epic via a structured, problem-first interview — core metadata, a rigorous problem statement, impacted personas, business alignment, measurable success metrics, evidence, MVP scope, risks, and NFRs, plus GenAI evaluation criteria when the epic involves model behavior. Produces the epic package that govkit-feature-create breaks into features. Tool-agnostic; writes a markdown epic by default, and can optionally create or update records in Jira or Aha! after explicit confirmation. Trigger whenever the user wants to write, draft, create, improve, or review an epic, initiative, or program brief, asks for help framing a problem statement, defining success metrics or OKR alignment, quantifying a problem's impact, or turning a validated opportunity into something a delivery team can plan against — even if they don't say GovKit or "epic".
---

# GovKit Epic Create — Problem-First Epic Authoring

## Purpose

Coach a Product Manager through the interview that produces a complete, governed Epic: one whose problem statement contains a problem, whose metrics carry targets, whose evidence is real, and whose scope has an edge.

You operate **only within the epic template**. You never invent fields and you never drift outside it. Within it, you push hard on quality — a template filled with confident vagueness is the failure mode this skill exists to prevent.

## Position in the lifecycle

```
val-rapid-validation → Validation Decision → govkit-epic-create → govkit-feature-create → Draft 0 → refine → readiness → Development Token
```

This skill sits at the seam between the two AIPOS pillars. Pillar 2's viability brief *names* the handoff inputs Build-to-Earn will need — problem statement, MVP scope, evaluation criteria, guardrail requirements — and deliberately stops there. **This skill is where those get written out.** When a viability brief exists, it is the single best input this skill can receive; ask for it before asking the PM to recall anything from memory.

The epic this produces is the input to `govkit-feature-create`, which maps it into features.

## Tool-agnostic design

| Role | What it means | Examples |
|---|---|---|
| **Tracker** | Wherever the epic record lives | Jira, Aha!, Azure DevOps, Linear, a markdown file, nothing at all |
| **Repo** | Where the epic package is written | `epics/<key>/` in the working directory |

**The skill works with no tracker at all.** The interview plus a markdown epic is the complete supported path, not a degraded one.

## Key terms

- **Problem-first framing** — the epic states a problem people have, not a solution someone wants built. The distinction is the whole discipline.
- **Impacted persona** — a named role that experiences the problem. Locked once confirmed, and inherited by every downstream feature.
- **Success metric** — a measurable outcome with a baseline, a target, and a way to observe it. Three parts; two is not a metric.
- **Epic evaluation criteria** — GenAI mode only. The thresholds every feature under this epic inherits.
- **Epic package** — the repo artifact: `epics/<key>/epic.md`, and in GenAI mode `epic_eval_criteria.yaml`.

## Operating principle

**Problems, not solutions. Numbers, not adjectives. Evidence, not confidence.**

Three rules follow, and they are the reason this skill exists rather than a template file:

1. **Ask one primary question at a time.** Summarize after each major section, then default forward.
2. **Never write into a record without explicit approval.** For updates, modify only the sections the PM asked for — an "improve the metrics" request is not permission to rewrite the problem statement.
3. **Never let a solution into the User Problem(s) section.** This is the single most common epic defect and the hardest to reverse: once the solution is in the problem statement, every downstream feature inherits an unexamined assumption, and nobody ever revisits it. See `references/problem-framing.md`.

This skill is transparent about how it works. Its rubrics live in `references/` and are meant to be read — if the PM asks why their problem statement was pushed back on, show them the test it failed.

## Scope

Use this skill for:

- Creating a new epic through a structured interview
- Improving or reviewing specific sections of an existing epic
- Reframing solution-shaped requests into problem statements
- Defining measurable success metrics and OKR alignment
- Establishing epic-level GenAI evaluation criteria that features inherit
- Writing the epic package, or a tracker record after confirmation

Do not use it for:

- Deciding whether the opportunity is worth pursuing (`val-rapid-validation` — that is Pillar 2, and it runs first)
- Breaking the epic into features (`govkit-feature-create`)
- Writing Gherkin, feature-level acceptance criteria, or NFRs scoped to one feature (`govkit-feature-create`)
- Reviewing or scoring a spec (`govkit-feature-refine`)
- Roadmap sequencing, capacity planning, or estimation

## Inputs

Everything is optional. Accept any of:

- A viability brief or other Pillar 2 artifacts (**the best possible input** — read it before asking questions)
- An existing epic record to improve, pasted or fetched via a tracker MCP
- A rough idea in the PM's own words
- Workspace personas, OKRs, or organizational NFR standards

Normalize into:

```yaml
intent: new | update
source:
  tracker: jira | aha | markdown | none
  epic_key: optional
  viability_brief: optional
epic:
  name, elevator_pitch, user_problems, personas, business_alignment,
  success_metrics, evaluation_criteria, evidence, initial_scope,
  risks, nfrs, target_release, owner, category      # all optional
genai: true | false
update_sections: []      # update intent only — the sections the PM named
```

These field names are deliberate: they are the `epic:` input contract `govkit-feature-create` reads. Writing them means the handoff needs no translation.

**Never invent** personas, metrics, baselines, targets, evidence, quotes, or thresholds. A gap recorded as a gap is a legitimate output; a plausible-looking number is not, because it will be quoted back as fact within a week.

## Required references

| Reference | Use |
|---|---|
| `references/problem-framing.md` | The solution-in-problem test and reframing scripts, persona handling, impact quantification, benefits, the final problem statement, and evidence quality. Read before Step 2. |
| `references/metrics-and-evaluation.md` | The success-metric quality bar, OKR alignment, and the full GenAI evaluation criteria model. Read before Step 4. |
| `references/epic-template.md` | The epic package shape, every field's content rules, and the MVP scope, risks, and NFR templates. Read before writing anything. |
| `references/tracker-adapters.md` | Repo package writer, create and update protocols, per-tracker adapters. Read before writing anywhere. |

If a reference is unavailable, continue from this file and say which rules you are applying from memory.

## Proceed protocol

Treat **"proceed", "continue", "looks good", "approved", "yes", "go"** as confirmation of the most recent summary — continue without restating it. Where options were presented, accept the option name, its number, or **"default"** (the recommended path).

Only pause when ambiguity genuinely exists, or when the next step is a write.

**The one exception:** a bare "proceed" never authorizes creating or modifying a tracker record. That needs the explicit, destination-named confirmation in `references/tracker-adapters.md`, every time.

## GenAI detection

Switch on GenAI mode silently and announce it once.

**Keywords:** AI, GenAI, LLM, GPT, RAG, embeddings, retrieval, model behavior, summarization, classifier, agent, hallucination, groundedness, reasoning, chatbot, OpenAI, Claude, Azure, Bedrock.

**Implied behavior:** text generation · natural-language interpretation · reasoning or decision-making · document retrieval · personalization · transcript analysis · multi-step automation.

> This epic involves GenAI behavior, so I'll include evaluation criteria and the GenAI NFR categories. Say the word if you'd rather not.

Proceed in GenAI mode unless explicitly disabled. It changes three sections: success metrics gain evaluation criteria, MVP scope gains evaluation gates, and NFRs gain the model categories.

**Epic evaluation criteria are inherited by every feature under this epic.** A threshold set here propagates to `govkit-feature-create` and lands in each feature's `eval_criteria.yaml`. Say this out loud when setting them — PMs treat the numbers very differently once they understand they are setting a contract rather than an aspiration.

---

# The interview

## Step 0 — New or update

**New:**

> We're creating a new epic. I'll take you through it step by step — one question at a time, and we'll summarize as we go.

**Update:**

> Tell me what you'd like to improve, or say "review all".

For updates, **touch only the named sections.** Read the rest for context, and if you spot a problem outside the requested scope, mention it in one line at the end — do not fix it uninvited. An unrequested rewrite of a field someone negotiated with three stakeholders is how a tool loses trust permanently.

## Step 1 — Core metadata

Ask in sequence, one at a time:

1. A short, outcome-focused working title
2. The target release or timeframe
3. The category or product area
4. The primary owner

Titles are worth one push: *"Claims triage improvements"* names an area, not an outcome. *"Cut adjuster time-to-first-action from 9 hours to under 2"* names one. Offer a reframe once, accept the PM's answer.

Summarize the four, then proceed unless corrected.

## Step 2 — The problem statement

The core of the epic, worked through in five tasks per `references/problem-framing.md`:

| Task | Question | Watch for |
|---|---|---|
| **1. Core problem** | What's the main issue we're trying to solve? | A solution in problem's clothing — apply the reframing script |
| **2. Impacted users** | Which personas experience this? | Offer workspace personas if they exist; capture new groups descriptively without creating persona records |
| **3. Quantified impact** | What measurable impact does this have — time, cost, errors, risk, satisfaction? | Adjectives standing in for numbers |
| **4. Benefits of solving** | What positive outcomes do you expect? | Benefits that restate the solution instead of the outcome |
| **5. Final statement** | — | Assemble and confirm |

The final statement follows one structure:

> The problem of **[X]** affects **[Y]**, resulting in **[Z]**, and solving it will lead to **[benefits]**.

Summarize after each task and proceed unless corrected. **Do not continue past Task 5 if the statement still has structural problems** — a solution embedded in the problem, no identified sufferer, or an impact nobody can measure. Everything downstream inherits this paragraph.

Lock the personas once confirmed; downstream steps and `govkit-feature-create` both use them.

## Step 3 — Business alignment

> Which business objectives or OKRs does this epic support?

Map to known objectives where the workspace exposes them. Where alignment is asserted but not evident, ask how this epic moves that objective — an epic aligned to everything is aligned to nothing, and that conversation is cheaper now than at a portfolio review.

## Step 4 — Success metrics

> What measurable outcomes define success? Aim for three to five, each with a target.

Apply the quality bar in `references/metrics-and-evaluation.md`: every metric needs a **baseline**, a **target**, and an **observation method**. Push for quantification, once per metric. If the baseline genuinely isn't known, record it as a gap and say so in the epic — "we don't measure this yet" is a real finding, and often the first thing the epic should fix.

Three to five is the guidance. Twelve metrics means nobody knows which one matters.

### GenAI mode

> We also need evaluation criteria defining acceptable model behavior.

Ask in sequence:

1. Which GenAI behaviors matter most — groundedness, correctness, tone, safety, retrieval, reasoning, tool use?
2. What thresholds do those need?
3. Are there required golden test cases or edge scenarios?
4. Should evaluation run continuously, or only pre-release?

Produce the structured criteria per `references/metrics-and-evaluation.md`. Every criterion needs a method and a threshold; a criterion without a threshold is a topic, not a gate. Where the PM doesn't have a number, mark it `TBD` and list it as a gap — never supply one yourself.

## Step 5 — Evidence and insights

> What evidence confirms this problem exists? Interviews, analytics, support tickets, compliance findings?

Organize into **qualitative** (interviews, shadowing, support themes) and **quantitative** (analytics, incident counts, cycle times). Record what each source actually establishes, and its date — evidence ages, and an eighteen-month-old analytics snapshot is a different claim from last week's.

Where a stated impact in Step 2 has no evidence behind it, say so plainly and mark it an assumption. Do not quietly downgrade it; the gap is the finding.

**GenAI mode:** also ask what data or past failures should inform evaluation. Prior incidents make the best golden test cases.

## Step 6 — Initial scope / MVP

> What must be in the MVP to deliver meaningful value — and what's explicitly out of scope?

Both halves. **Out of scope is not optional**: it is the section that prevents the most downstream argument, and the one PMs skip most.

Test the MVP against Step 4: if nothing in it moves a stated success metric, either the scope or the metrics are wrong. Surface it either way.

**GenAI mode:** ask which evaluation thresholds must be met before MVP release, and which belong to later phases. That distinction is the difference between a gate and a wish.

## Step 7 — Risks and mitigations

> What key risks should we document — delivery, technical, compliance, adoption, data?

Capture as risk + mitigation pairs. A risk without a mitigation is worth recording, but say plainly that it is unmitigated rather than writing a mitigation that amounts to "monitor it".

Walk the categories if the PM stalls; adoption and compliance are the two most often forgotten.

## Step 8 — Non-functional requirements

Walk the standard categories: **Performance · Security · Scalability · Reliability · Compliance**.

**GenAI mode** adds: latency and token cost constraints · model and vendor constraints · data handling constraints · observability and drift monitoring.

Epic-level NFRs are the constraints that apply across every feature. Feature-specific thresholds belong to `govkit-feature-create`; what belongs here is the standard each feature must meet or explicitly except itself from. Prefer a stated organizational standard over a number invented in the moment.

## Step 9 — Final assembly

Produce the complete epic mapped to the template fields in `references/epic-template.md`:

Epic Name · Elevator Pitch · User Problem(s) · Personas · Alignment to Business Objectives · Success Metrics · GenAI Evaluation Criteria (if applicable) · Evidence & Insights · Initial Scope / MVP · Risks & Mitigations · NFRs · Target Release · Owner(s) · Category / Product Area · Open Questions & Gaps

Then ask:

> Would you like me to write this — to the repo epic package, the tracker record, or both? You can approve all, name specific sections, or ask for changes.

Write only what is explicitly approved, following `references/tracker-adapters.md`. Close by naming the next step: `govkit-feature-create` turns this epic into features.

---

## Output format

````markdown
# Epic — <name>

## Summary of what we captured
| Section | Status |
|---|---|
| <each template section> | complete / gaps noted / not covered |

## The epic
<the full package per references/epic-template.md>

## Open questions and gaps
- <every unmeasured baseline, unevidenced claim, and TBD threshold>

## Ready to write
<destination named, awaiting explicit approval>
````

The gaps list is a required section, not a courtesy. An epic with no gaps has usually not been examined hard enough — say so if the list comes out empty.

## Guardrails

Do not:

- Let a solution appear in the User Problem(s) section
- Invent personas, baselines, targets, evidence, quotes, or evaluation thresholds
- Write to a record without explicit, destination-named approval — a bare "proceed" never covers a write
- Modify sections the PM did not ask you to modify, on an update
- Add fields the epic template does not contain
- Accept an adjective where a number belongs, without at least one push
- Continue past the problem statement while it still has structural problems
- Set a GenAI threshold without saying that every feature will inherit it
- Ask more than one primary question at a time

Always:

- Read a viability brief or prior evidence before asking the PM to recall it
- Summarize after each major section, then default forward
- Record gaps as gaps, with the reason they are gaps
- Date the evidence
- Push once for a baseline, a target, and an observation method on every metric
- Keep the out-of-scope list non-empty
- Name `govkit-feature-create` as the next step when handing off

## Related

| Skill | Owns | Relationship |
|---|---|---|
| `val-rapid-validation` (aipos-p2) | Whether to build at all | Runs first. Its viability brief *names* the problem statement, MVP scope, and evaluation criteria this skill writes out. If no Validation Decision exists, say so once — an epic for an unvalidated opportunity is a well-documented guess |
| `govkit-feature-create` | Story mapping and Draft 0 authoring | Consumes this epic. This skill's field names are that skill's `epic:` input contract; personas and evaluation criteria are inherited wholesale |
| `govkit-feature-refine` | Spec quality | Two levels down. Epic-level evaluation criteria are what refine checks feature specs against |
| `govkit-feature-map` | The corpus view | Renders the features derived from this epic; the epic's success metrics are what a release-weakness read is judged against |

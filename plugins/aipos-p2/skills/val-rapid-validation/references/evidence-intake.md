# Evidence intake

Every artifact in this skill starts here. The job is to find out what is actually known
before writing anything that implies knowledge.

## The three paths

Ask once, plainly:

> Do you have evidence to work from — an Aha! record or similar, notes and transcripts you
> can share, or are we starting from your read of the situation?

### Path A — A record in a tracker

The PM names an Aha! opportunity, a Jira issue, a Linear ticket, a Productboard item.

Read it before asking anything. If there is a connector available, use it; if not, ask the
PM to paste the record. Then summarise back what you found and ask them to correct it. Do
not ask for facts already on the record — that is the fastest way to signal you didn't read
it.

**Aha! Discovery evidence-triage records** have a specific shape worth knowing. They carry a
promoted-from-triage block with a composite score and five components:

| Component | Low value means |
|---|---|
| `evidence_strength` | The problem itself still needs confirming |
| `revenue_impact` | No dollar value has been attached yet |
| `persona_breadth` | Pain is concentrated in one role — or breadth is untested |
| `recency` | The evidence is aging |
| `validation_signal` | **Nothing has been tested with a user yet** |

Read the components as a risk map and say so out loud — it tells the PM where the artifact
should focus. A near-zero `validation_signal` is the signature of an opportunity that has
never met a real user; almost anything in this skill will move it. A low `evidence_strength`
means start at artifact 1 or 2, not at a prototype.

Also read the persona list and its breadth. If ten personas span two genuinely different
populations, say so — narrowing to one without naming the choice throws away the strongest
signal on the record.

**Evidence refs are often read-only.** Triage engines commonly link out to source calls or
tickets you cannot open. Say so rather than implying you read them: *"13 refs across 13
sources, read-only from the engine — I have the problem statement and the score shape, not
the underlying quotes."* Then mark accordingly.

### Path B — Material the PM shares

Interview notes, call transcripts, support tickets, survey exports, a sales deck, an
analytics screenshot.

Read all of it before writing. Pull out: recurring phrases in the user's own words,
concrete numbers with their source, named roles, and anything that contradicts the PM's
framing. That last one earns its keep — a contradiction the PM hasn't noticed is the most
valuable thing you can hand back.

Quote sparingly and exactly. A real quote in a user's own words is worth more in an
interview guide or viability brief than any paraphrase, and paraphrase is where invention
creeps in.

### Path C — Nothing

This is legitimate and common. Do not treat it as a failure or make the PM feel behind.

Interview them instead: what they've observed, who they think has the problem, what they
believe is true but haven't checked. Capture it as **assumption**, which is exactly what it
is — and assumptions are the raw material of validation, not a defect.

Then say once, without lecturing:

> Worth knowing: with no evidence behind it, the strongest thing this artifact can do is
> make your assumptions explicit and testable. If you want something that carries weight
> with other people, artifacts 1 and 2 are how you get there.

If the PM asked for a **prototype brief or a viability brief** on Path C, be more direct.
A prototype brief with invented personas produces a test that validates nothing, and a
viability brief with no evidence is an opinion in a document's clothing. Offer the
interview guide or problem sizing first. If they still want to proceed, proceed — but the
evidence-base header has to say plainly that this rests on the PM's judgment alone.

## Provenance marking

Every artifact marks its claims. This is the single most useful convention in the skill:
without it, a document built from a hunch is visually indistinguishable from one built from
thirteen customer calls, and six weeks later nobody can tell which they're holding.

| Marker | Meaning |
|---|---|
| `[E]` | **Evidence-backed** — traceable to a named source you actually read |
| `[I]` | **Inferred** — reasoned from evidence, but nobody said it |
| `[A]` | **Assumption** — the PM's judgment or yours, untested |

Mark at the claim level, not the section level. Inside one paragraph a sized market may be
`[E]` while the adoption rate applied to it is `[A]` — and that distinction is the whole
value of the estimate.

Do not mark decorative or structural text. Mark claims someone could act on or be wrong
about.

## The evidence-base header

Every artifact opens with this block. It takes four lines and it is the first thing a
reader should see.

```markdown
## Evidence base
**Source:** <Aha! OPP-5 (13 refs, read-only) | 6 interview transcripts | PM interview only>
**What's backed:** <the problem statement, the persona set>
**What isn't:** <the urgency claim, every number in the sizing>
Claims below are marked [E] evidence-backed, [I] inferred, [A] assumption.
```

Write it honestly, including when the honest version is unflattering. An artifact that
admits it rests on assumption is useful. One that hides it is a liability that gets more
dangerous the further it travels from the person who wrote it.

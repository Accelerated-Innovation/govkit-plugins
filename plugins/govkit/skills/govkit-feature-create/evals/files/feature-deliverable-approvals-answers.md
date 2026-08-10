# Feature stub — Deliverable approvals (Epic AI-300, slice: MVP)

**Name:** Deliverable approvals
**Epic:** AI-300 Client self-service portal
**Release:** 2026.Q4 · **Type:** New capability · **Owner:** Priya (PM)
**Description:** Clients review a submitted deliverable in the portal and approve it or
request changes, with an auditable decision record.

---

## PM's answers (collected ahead of the session — use these, don't re-ask)

- **Primary persona:** Client stakeholder. Secondary: Account manager (needs to see
  decision status and history).
- **Intent, in plain language:** A client opens a deliverable we submitted, sees the files
  and our note, and either approves it or sends it back with a comment. Every decision is
  recorded with who and when, because approvals are contractual.
- **Size feel:** Fits in two sprints — the portal shell and auth already exist from the
  status-visibility feature.
- **Rules the PM stated:**
  - Only client users on that account can decide; agency staff can never approve on a
    client's behalf.
  - A change-request must include a comment; an approval may have one.
  - Once approved, a deliverable is locked — a new version requires a new submission.
- **Out of scope:** Multi-approver chains (V1), e-signatures (V2), client-authored change
  requests unrelated to a deliverable.
- **Dependencies:** Portal auth (existing), file storage service (existing), notification
  digest feature (AI-204) for decision notifications.
- **NFR notes:** Decision record must be immutable and auditable. No stated latency or
  volume numbers yet — team will set thresholds in refinement.
- **Privacy:** Deliverable files may contain client-confidential material; decisions store
  name, timestamp, and comment of the deciding user.
- **Agentic behavior:** No. Plain workflow feature, no AI of any kind.

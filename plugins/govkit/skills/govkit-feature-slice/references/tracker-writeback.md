# Tracker write-back

How the tagged spec gets back into the tracker record. Update-in-place only: this skill edits the fields of the record it read from; it never creates, deletes, or re-parents records. Splitting a feature into child records per slice is a heavier write with tracker-specific hierarchy rules — deliberately out of scope for now.

## Contents

- [The preview-confirm protocol](#the-preview-confirm-protocol)
- [Jira adapter](#jira-adapter)
- [Aha adapter](#aha-adapter)
- [Azure DevOps](#azure-devops)
- [Copy-ready fallback](#copy-ready-fallback)

## The preview-confirm protocol

Writing to a tracker is outward-facing — teammates see the record change, automations may fire on it. Every write follows this sequence, no exceptions:

1. **Preview the exact content.** Show the final field text verbatim — the tagged Gherkin as it will be written, not a summary of it.
2. **Summarize the delta.** In one or two lines: "3 scenarios tagged `@mvp`, 5 `@v1`, 2 `@v2`; scenario 'Bulk reschedule' split into two." If the field currently holds content that the write will replace wholesale, say so.
3. **Name the destination precisely.** Tracker, record key, field name. "Write this to the Acceptance Criteria field of AI-124 in Jira?"
4. **One explicit yes.** Ask a single closed question and write nothing until it is answered. One record per confirmation — never batch confirmations across records.
5. **Read back and verify.** After writing, fetch the record and confirm the field matches what was previewed. Report the result either way; a silent partial write is worse than a failed one.

If any step fails — the field key is wrong, the MCP errors, the read-back differs — stop, report, and fall back to copy-ready output rather than retrying blind.

Optionally offer to add a comment to the record noting that sizing/slicing was applied and by what rubric — useful provenance in a team tracker, but the user's call, not a default.

## Jira adapter

Atlassian MCP tools.

| Step | Tool |
|---|---|
| Fetch current field content | `getJiraIssue` |
| Write the updated field | `editJiraIssue` |
| Read-back verification | `getJiraIssue` again, compare |

- The Gherkin usually lives in the description or a dedicated Acceptance Criteria custom field. Write to **the field it was read from** during ingestion; do not relocate the spec.
- Jira rich-text fields hold ADF or wiki markup. Write the Gherkin in the same format the field already uses — if it arrived as a wiki-markup code block, return it as one. Tags are plain `@word` tokens and survive any of these formats.
- If the record's Gherkin came from linked issues rather than a field, that is not update-in-place territory — fall back to copy-ready output and say why.

## Aha adapter

Aha! MCP tools.

| Step | Tool |
|---|---|
| Resolve custom field keys | `fields_metadata` — keys are workspace-specific; never guess |
| Fetch current content | `read_records` |
| Write the updated field | `manage_record` (update) |
| Read-back verification | `read_records` again, compare |

- If the Gherkin lives on the feature record (description or a custom field), update that field.
- Aha! features often carry requirements as child records, one per rule or scenario group. Updating an existing requirement's content is still update-in-place — do it one requirement per preview-confirm cycle. Creating new requirement records (e.g., for a split scenario) is not; put the new scenario in the same requirement as its parent, or fall back to copy-ready and let the PM create the record.

## Azure DevOps

No MCP adapter in the current toolset — use the copy-ready fallback. (For teams with their own tooling: the Acceptance Criteria field is `Microsoft.VSTS.Common.AcceptanceCriteria`, writable via the work item REST API; the same preview-confirm protocol applies.)

## Copy-ready fallback

When no tracker MCP is connected, when the adapter hits a case it cannot do in place, or when the user declines the write: emit the same copy-ready block `govkit-feature-refine` uses, ready to paste.

````markdown
## Tracker field updates — <KEY>

### Acceptance Criteria
```gherkin
<final tagged Gherkin, no placeholders, no question comments>
```
````

Copy-ready means copy-ready: no unresolved questions, no `TBD`, no draft markers. If the PM has not confirmed all slices yet, there is nothing copy-ready to emit — go back to the decision step instead of shipping a half-decided spec to the tracker.

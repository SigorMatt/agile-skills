# The retro skill's first three runs, banked verbatim

`retro` 0.1.0, rendered and installed, executed by **context-free subagents** — each given a
workspace path and nothing else, told to read `RECORD-NOTICE.md` and the skill's own files and
execute the skill, and told not to read anything outside its directory. None of them saw this
repository, the findings ledger, or each other.

| File | Engagement | What it is |
|------|-----------|-----------|
| `iteration-2-retro.md` | `iteration-2-tidy`, 11 items | ground-truth calibration (META-140) |
| `iteration-3-retro.md` | `iteration-3-mdtab`, 6 items | ground-truth calibration (META-140) — the marquee case |
| `live-recall-4c-retro.md` | `recall-4c`, 4 items | the live pipeline dispatch (META-141) |
| `*-journal-entry.md` | | the `retro` journal entry each execution appended to its epic |

The two calibration reports are the **first** run of each engagement, unedited. `retro` 0.2.0
changed one step afterwards in response to what they missed; the re-run under 0.2.0 is
`iteration-3-retro-0.2.0.md`, and it is a check that the new instruction is followable, **not**
an independent measurement — the change was made after reading the miss. `meta/FINAL-REPORT-4.md`
§4 says so where the numbers are.

## What the copies were, and what they were missing

Each workspace is `meta/harness/evidence/<iteration>/{tracker,docs}` copied to scratch, with the
current toolkit installed. Two things were not banked with those records and could not be
supplied: the **product source tree** (so `validate-workspace` reports
`claim.citation.unresolved` against files that were never kept — 181, 13 and 48 respectively,
and no other code) and the **commit history**. Each copy carried a `RECORD-NOTICE.md` saying so,
instructing that `workspace-valid` be recorded as **failed with that reason** rather than
skipped or passed, and noting that the installed contracts are newer than the versions the
record names. Nothing else was waived.

All three runs wrote exactly two files — the report and their own journal entry on the epic —
verified by modification time across `tracker/` and `docs/` after the fact, not taken on trust.

## Read these three things first

1. **`iteration-2-retro.md` P-3.** F-061 was filed as an observation with *"Direction: none
   required now… Revisit when the retro skill exists."* This is the retro skill revisiting it and
   finding the mechanism the original finding did not: the sign-off's option B, which
   `spec/question.md` §2 obliges every sign-off to offer, promises an ending the status model
   forbids, because creating the follow-up item destroys the rest the ending requires.
2. **`live-recall-4c-retro.md` P-1.** A claims gate scoped to a work item's branch diff is empty
   *by construction* at every item close — verified independently against the current kernel and
   filed as **F-076**.
3. **`iteration-3-retro.md` P-12 against `meta/findings/FINDINGS.md` F-062.** The honest miss.
   The report found that fifteen human answers were never checked against each other and that two
   narrow an earlier one; it did not find what the record shows happening next.

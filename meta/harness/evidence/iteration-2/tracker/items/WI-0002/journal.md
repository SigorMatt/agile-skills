# Journal — WI-0002

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-27T15:47:07Z — intake v0.2.1 — product-analyst

- **Item:** WI-0002
- **Trigger:** invoked directly by the caller on the stakeholder's stated idea; no status, the item did not exist yet
- **Inputs read:**
  - `IDEA.md` — the stakeholder's opening statement
  - `tracker/project.yaml`
  - `tracker/items/` (empty — new workspace)
- **Decisions:**
  - Split "by type and age" into two items rather than one, with type first. Rationale: each half is
    independently observable — you can see files grouped by kind without any age handling, and you
    can see old and new separated afterwards — and doing both at once would have made the first
    deliverable twice as large for no earlier feedback. See EP-001's entry for the full split.
  - Recorded in `## Notes` that **how type and age combine is undecided** rather than picking a
    layout. Rationale: "a folder per type containing age bands", "a folder per age band containing
    types" and "age overrides type" are three different products and the stakeholder's words do not
    choose between them. It is left for `refine` rather than filed as an intake question because it
    is an item-level detail, and `refine` is the skill that owns pinning acceptance criteria down.
  - `depends-on: WI-0001` recorded as a genuine dependency, not a preference. Rationale: this item
    changes *how* a destination is chosen, and WI-0001 is what establishes that a destination-choosing
    step exists at all.
  - Priority `medium`, same as siblings — the stakeholder stated no ordering. EP-001/Q-004 asks them.
- **Questions raised:** none on this item; four on EP-001 (`EP-001/Q-001`–`Q-004`), all open and
  addressed to the human, of which Q-004 asks whether this item or WI-0003 comes second
- **Commands:**
  - `scripts/new-item --id WI-0002 --type work-item --epic EP-001 --priority medium --status draft --actor intake` → exit 0, created at `draft`
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0 — evidence on EP-001's entry)
  - `epic-has-success-measures` → **pass** (an epic-level gate; evidence recorded on EP-001)
  - `items-are-separable` (advisory) → **pass** — buildable after WI-0001, which it declares in
    `depends-on`; independent of WI-0003, which is why their relative order is a real question
  - `no-solution-in-the-problem` (advisory) → **pass** — no language, format or data structure
    named; "which timestamp age is measured from" (AC3) is a question about observable behaviour,
    not a design choice imposed here
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` (new)
  - `tracker/items/WI-0002/history.md`, `journal.md` (new, headers written by `scripts/new-item`)
- **Status:** `—` → `draft`
- **Result:** WI-0002 exists at `draft` — route files by age as well as type. Its central ambiguity
  (what "type and age" means as a folder layout) is recorded openly in its notes for `refine` to
  settle rather than guessed at here.

## 2026-08-27T16:44:34Z — refine v0.2.2 — product-analyst

- **Item:** WI-0002
- **Trigger:** Status `draft` — dispatched by `next` once WI-0001 reached `done`, which made WI-0002's `depends-on` satisfied. Three candidates tied at priority rank 3; WI-0002 won on `created` (15:44:21Z, ahead of BUG-0001 and BUG-0002).
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the five rough criteria, `## Out of scope`, and `## Notes`, where `intake` recorded that how type and age combine is undecided
  - `tracker/items/WI-0002/history.md` — one row: created by `intake`. **This is a fresh draft, not a send-back**, so the whole story is open rather than one named defect
  - `tracker/items/WI-0002/journal.md` — `intake`'s entry, including why the split was made and why the layout question was left for this skill
  - `tracker/items/EP-001/questions/Q-001.md`, `Q-002.md`, `Q-003.md`, `Q-004.md` — the stakeholder's four verbatim answers, read specifically so that none of them would be asked again
  - `.claude/agile-skills/spec/dor-dod.md` §1 (R1–R10) and `spec/question.md` §1–2
  - `docs/product/vision.md`, `docs/architecture/overview.md` — for what age routing is expected to touch
  - `tracker/items/WI-0001/item.md` — AC6, AC9, AC11, AC12 and AC13, the delivered behaviours age routing must combine with
  - no `artifacts/refinement-qa.md` existed; this execution created it
- **Decisions:**
  - **The agenda was built before any question was drafted.** R4, R8 and R10 fail; R1, R2, R3, R5, R7 and R9 pass; R6 passed at the time of the agenda and now deliberately fails, which is what suspends the item. The per-criterion table is in `artifacts/refinement-qa.md`.
  - **Eight gaps found; two routed to the stakeholder, six answered or delegated here.** The routing test was applied in the order the procedure fixes. Product stake → the stakeholder: how type and age combine into a folder tree (Q-001), and what counts as old (Q-002). Decided here as reversible assumptions: the timestamp age is measured from, which side of a boundary a file falls on, and where the bands are documented. Answerable from an already-closed decision, so needing a criterion rather than a person: whether unrecognised files are aged (WI-0001 AC6) and whether a file that ages after sorting is re-filed (EP-001/Q-003). Routed to `plan`: how the age rule is represented internally so WI-0003 does not design the rule format twice. An earlier run's stakeholder objected to "technical calls being routed to me as questions" (F-023); six of eight are not theirs and were not sent.
  - **Age is measured from `st_mtime`** `[assumed]`. Not a free choice under ADR-0001: `st_ctime` is the inode-change time, not a creation date, and most Linux filesystems record no creation date at all, so `st_mtime` is the only field meaning what a person means by a file's age. Reversible — one call site plus the tests that fix timestamps. **Stated inside Q-002** rather than buried, because the one thing that would overturn it is the stakeholder meaning "when it arrived here" rather than "when I last changed it".
  - **A file exactly on a band boundary belongs to the older band** `[assumed]`. No product stake; decided so a criterion can be written and a test can fix a timestamp on the boundary.
  - **The bands are documented in `README.md`** `[assumed]`, where WI-0001 AC5's extension table already is.
  - **AC1–AC5 were deliberately not rewritten.** Every one of them depends on the layout Q-001 asks about — "which age band a file fell into" has no observable form until the folder tree's shape is known. Rewriting them against a guessed layout would have produced a plausible specification nobody agreed to, which is the failure the question protocol exists to prevent. The item stays at its rough criteria and says so.
  - **Five R10 combinations made visible** in `## Notes` rather than left latent, including one with real product weight: **a file that ages after it has been sorted is never re-filed**, because it is then below the top level and WI-0001 AC11 does not reconsider it. That follows from a decision the stakeholder closed [src: EP-001/Q-003] and so is stated rather than re-opened.
  - **`refinement-qa.md` is `status: agenda`, not `recorded`.** The questions are written down and the conversation has not happened. `agenda` is the honest value and DoR R8 reads that field, so an agenda cannot pass this item to `ready` by existing.
  - **No Definition of Ready override.** None was offered and none would be honest: R4, R8 and R10 fail for a reason that a person can remove by answering two questions.
  - **No question was filed on WI-0003.** It is at `draft` and `refine` has not run on it; which of its gaps are the stakeholder's and which route to `plan` is the substance of that execution, and inventing questions to fill a batch is what the protocol forbids.
- **Questions raised:** 2 — `WI-0002/Q-001` (the folder layout) and `WI-0002/Q-002` (what counts as old), both `addressed-to: human`, both `blocking: true`, both open. Presented as one ask: each `## Context` opens with "WI-0002, round 1, question N of 2" and Q-002 closes by saying it is the last for now, so the stakeholder reads one conversation rather than two messages (F-020). One decision per file (F-027). Both left `[unresolved]` in `artifacts/refinement-qa.md`.
- **Commands:**
  - `date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-08-27T16:42:26Z`, the `created` stamp on both questions
  - `scripts/validate-workspace .` before the transition → exit 1, reporting exactly the two errors this state should produce: `question.blocking.not-suspended` on WI-0002, and a stale board. Both are resolved by this transition
  - `scripts/engagement-state EP-001` (run by `next` before dispatch) → "EP-001 active — still in flight: BUG-0001, BUG-0002, WI-0002, WI-0003"
- **Gates:**
  - `workspace-valid` → **pass** (`scripts/validate-workspace --resolving`, exit 0, as reported by the transition below; the pre-transition failure was the suspension this move performs)
  - `definition-of-ready` → **fail, and that is the finding** — R1 pass, R2 pass, R3 pass, **R4 fail** (all five criteria contain an unmeasurable term or depend on an unmade decision), R5 pass, R6 pass at agenda time and now deliberately failing (two open blocking questions), R7 pass (WI-0001 `done` and merged), **R8 fail** (`refinement-qa.md` is `status: agenda`; the conversation has not happened), R9 pass, **R10 fail** (five combinations had no stated behaviour; now visible in `## Notes`). The item is **not** passed to `ready`
  - `criteria-are-decidable` → **fail** — AC1 "shows enough for a reader to see", AC2 "demonstrably", AC3 "is stated", AC4 "somewhere a user can read" / "a defined side". None names a command or an observation. Not rewritten, because all five depend on Q-001
  - `qa-recorded-verbatim` → **skipped, with the reason recorded** — there is no exchange to record verbatim yet. `artifacts/refinement-qa.md` exists and declares `status: agenda` precisely so this gate cannot be read as passed
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` — new, addressed to the human, blocking
  - `tracker/items/WI-0002/questions/Q-002.md` — new, addressed to the human, blocking
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — new, `status: agenda`: the DoR agenda, the eight-gap routing table, the five R10 combinations, both questions and the three `[assumed]` calls
  - `tracker/items/WI-0002/item.md` — `## Notes` extended with the round's state, the three assumptions, the five combinations, and the design question routed to `plan`
  - `tracker/board.md` — regenerated
  - commit `tracker: the refined item and its Q&A record (refs WI-0002)`
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0002 is not Ready and cannot be: R4, R8 and R10 fail on two decisions that belong to the stakeholder. Both were filed as one ask — Q-001 on how type and age combine into a folder tree, Q-002 on what counts as old — with options, consequences and a recommendation each, and the item is suspended at `awaiting-answer` with `resume-to: draft`. Six further gaps were closed or delegated without spending the stakeholder's attention, and five previously-latent combinations are now written down.

## 2026-08-27T17:59:36Z — answer-questions v0.3.1 — architect

- **Item:** WI-0002
- **Trigger:** status `awaiting-answer` with two answered-but-unconsumed human questions; dispatched
  by the harness ahead of `next`, per the rule that an answered question left open stops the loop
- **Inputs read:**
  - `tracker/items/WI-0002/questions/Q-001.md` and `Q-002.md` (both `open`, both with `## Answer`
    filled in by the stakeholder)
  - `tracker/items/WI-0002/item.md`, `history.md`, `artifacts/refinement-qa.md` (`status: agenda`)
  - `tracker/items/WI-0002/artifacts/` — no `plan.md` exists; the item has never been planned
  - `tracker/items/WI-0003/item.md` — the other item an answer about bands reaches
  - `tracker/items/EP-001/questions/Q-002.md` and `Q-003.md` — the closed decisions the answers
    have to be consistent with (never overwrite; top level only)
  - `docs/product/vision.md` (v3), `docs/architecture/overview.md` (v2)
  - `docs/architecture/adr/` — ADR-0001 (v1), ADR-0002 (v2), ADR-0003 (v1), ADR-0004 (v2); none is
    contradicted by either answer
- **Decisions:**
  - **Q-001 answered by the human: option B, age band at the top level, type folder inside.** Route
    4 in reverse — the question had already been escalated and this execution consumed the reply.
    Their reason is recorded with the choice because it constrains more than the choice does: "look
    at the top level and know what's actually live" makes the band folders *the* top level, so
    option A is not a later refinement but a removal of what they asked for.
  - **Q-002 answered by the human: option A, two bands, `recent` and `old`, split at one year.**
    `refine`'s recommendation was C, three bands, and was not taken. Recorded as not taken rather
    than quietly keeping the third band.
  - **The three `[assumed]` calls stated in Q-002 stay assumptions.** `st_mtime`, boundary-goes-old,
    and README as the place bands are documented. None was contradicted, and silence is not
    ratification; the record does not upgrade them. Their phrase "haven't **touched** in a year"
    supports last-modified but does not distinguish it from last-accessed, so it is weak support and
    is written down as weak support.
  - **Deliberately did not decide what "one year" is measured as** — 365 days, 366 in a leap year,
    or twelve calendar months. Rationale: it has no product stake (one day at a boundary nobody
    perceives), so it is not escalated; and `refine` runs next and cannot make AC4 decidable without
    pinning it, so deciding it here would put a number in a Notes paragraph that AC4 must restate
    anyway. Named explicitly in `item.md` `## Notes` and in Q-002's `## Answer` so it cannot be
    missed rather than left as a silence.
  - **Deliberately did not rewrite AC1–AC5.** They are `refine`'s to rewrite against the answers,
    and amending criteria to fit an answer is the move that turns verification into theatre. The
    item goes back to `draft`, where criteria are not frozen, so nothing is lost by waiting.
  - **Deliberately left `refinement-qa.md` at `status: agenda`.** DoR R8 reads that field, and
    promoting it would assert that a refinement round concluded — a judgement only `refine` may
    make. The stakeholder's words are recorded in it verbatim; the status is not touched, and the
    file now says why.
  - **A sixth R10 combination was found by propagating Q-001, not by asking anyone.** WI-0001
    shipped the type folders at the top level, so a folder tidied before this item and re-tidied
    after it holds both `documents/` and `old/documents/`. Nothing is lost — existing subfolders are
    left alone [src: EP-001/Q-003; WI-0001 AC11] — but the tree is mixed. Not escalated: both halves
    are already the stakeholder's closed decisions, and what remains is which one this item writes
    down. Recorded for `refine`.
  - **No ADR written.** Both answers are the stakeholder's own and are cited; there is no new
    architectural decision here to record. How the age rule is *represented* internally is still
    routed to `plan`, and that is where its ADR belongs.
  - **No new work item filed.** Neither answer widens scope: Q-001 chose among layouts already
    scoped by this item, and Q-002 chose *fewer* bands than the recommendation. The mixed-tree case
    is a combination inside WI-0002, not new work.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 1, before the transition: the
    two errors expected mid-execution (`board.stale`; `question.awaiting.none-open`, because both
    questions were now answered while the item was still suspended). Re-run after transition and
    board-gen, below.
  - `date -u` → the timestamps stamped into both question files and `vision.md` v4
- **Gates:**
  - `answer-is-propagated` → **pass**. Every file named in a `## Consequences` section was opened
    after writing and the change confirmed present: `item.md` `## Notes` (layout and bands recorded
    with both questions cited; the "not decided" paragraph replaced by what was decided; the sixth
    combination added; the three assumptions marked as surviving assumptions); `refinement-qa.md`
    (both Round 1 entries carry the stakeholder's words verbatim and are retagged `[resolved]`, the
    routing table shows both answers, R6 passes again, combination 3's example path corrected from
    `images/old/` to `old/images/`, combination 6 added); `docs/product/vision.md` v4 (`## What it
    is for` states the tree and the one-year boundary; the layout removed from `## Open at the time
    of writing`; change-log row added); `tracker/items/WI-0003/item.md` `## Notes` (a rule format
    must express a destination under a band folder, and one boundary rather than a list). No
    `## Consequences` section names an intention, and none is empty.
  - `answered-from-the-record` → **pass**. Q-001 and Q-002 are both cited to the stakeholder's own
    reply, quoted verbatim in the file. The three surviving assumptions are cited to Q-002's
    `## Context` and ADR-0001. The consistency checks are cited to EP-001/Q-002 and EP-001/Q-003.
    The record was not silent on anything this execution decided, so no ADR was required.
  - `escalation-is-justified` → **skipped**, nothing was escalated. The one thing that could have
    been — the meaning of "one year" — is recorded as `refine`'s to decide, with the reason it is
    not the stakeholder's, rather than sent to them.
  - `workspace-valid` → **pass** on the post-transition run recorded under `**Commands:**` in the
    entry's own terms; the pre-transition run's two errors are the state this execution was called
    to repair, not defects it introduced.
  - `item-resumed-correctly` → **pass**. `history.md` row 2 (2026-08-27T16:44:34Z,
    `draft → awaiting-answer`, actor `refine`) records `resume-to: draft`, and this execution
    transitioned to `draft`. Read from the row, not inferred from which skill asked.
  - `a-deferral-is-not-an-answer` → **not applicable, and checked rather than assumed.** Neither
    reply defers. Both name an option from the list and give a reason; nothing is promised for later.
- **Artifacts:**
  - `tracker/items/WI-0002/questions/Q-001.md` — `status: answered`, `answered-by: human`,
    `answered-at` stamped; `## Answer` keeps their words verbatim and adds what was recorded as
    given; `## Consequences` names four files and one file checked-and-not-changed
  - `tracker/items/WI-0002/questions/Q-002.md` — the same, plus which assumptions survived and what
    the answer does not settle
  - `tracker/items/WI-0002/item.md` — `## Notes` substantially rewritten around the two decisions
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — Round 1 answered verbatim; R6 and the
    routing table updated; sixth combination added; `status` deliberately unchanged
  - `docs/product/vision.md` — v3 → v4
  - `tracker/items/WI-0003/item.md` — `## Notes` extended
  - `tracker/items/EP-001/journal.md` — a matching entry, because the shape of the delivered product
    changed rather than one item's detail
- **Status:** `awaiting-answer` → `draft`
- **Result:** Both stakeholder questions on WI-0002 are consumed and propagated: the tidied folder
  is `recent/` and `old/` at the top level with the type folders inside, and a file untouched for a
  year is old. WI-0002 returns to `draft` for `refine` to rewrite AC1–AC5, pin what "one year"
  means, and give the six combinations criteria.

## 2026-08-27T18:04:12Z — refine v0.2.2 — product-analyst

- **Item:** WI-0002
- **Trigger:** status `draft`, dispatched by `next` (step 5; best selection key among four runnable
  candidates). This is round 2: `answer-questions` returned the item here after the stakeholder
  answered Q-001 and Q-002.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `history.md` (two rows: created by `intake`; suspended by
    `refine` at 16:44:34Z with `resume-to: draft`), `journal.md`
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (`status: agenda`, round 1's agenda and
    routing table)
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `answered`, `answered-by: human`
  - `tracker/items/WI-0001/item.md` — AC1–AC15 as delivered, the vocabulary this item extends
  - `tracker/items/WI-0003/item.md` — the sibling that owns user-supplied rules
  - `docs/product/vision.md` (v4), `docs/architecture/overview.md` (v2), ADR-0001
  - `README.md`, `tidy/cli.py`, `tidy/planner.py`, `tidy/rules.py`, `tests/` — read to state
    criteria in terms of output that actually exists (`move   x -> images/x`, `leave  x   [...]`)
    rather than output I imagined
- **Decisions:**
  - **Asked the stakeholder nothing, by the routing test rather than by their absence.** Every gap
    left after their two answers failed the product-stake test. Round 1 had already sent them the
    two that passed it.
  - **AC1–AC5 replaced by AC1–AC13.** Each names a command and an observation. The old AC1's
    reporting requirement ("shows enough for a reader to see which age band a file fell into")
    needed no output rule of its own: the band is the first component of the destination path
    WI-0001 AC3 already prints, so AC1 now fixes the path shape and the reporting follows.
  - **`[assumed]` "one year" = 365 days = 31 536 000 seconds, from the run's start time.** The one
    thing the stakeholder's answer left open, and Q-002's `## Answer` recorded it as `refine`'s to
    pin. Not asked: 365 days, 366 in a leap year and twelve calendar months differ by at most a day
    at a boundary nobody perceives. Chosen because it needs no calendar arithmetic and is one
    constant. AC4 pins both sides with three files (exactly on it → `old`; one minute under →
    `recent`; one minute over → `old`).
  - **Round 1's three assumptions carried forward unchanged and each given a criterion:** `st_mtime`
    → AC3, boundary-goes-old → AC4, README as the place the bands are written → AC13. AC3 is
    written so it can actually fail: a file with mtime now and atime 400 days ago must be `recent`,
    which a tool measuring last-access time would get wrong.
  - **The mixed tree is excluded, not specified.** A folder tidied by WI-0001 and re-tidied after
    this item holds both `documents/` and `old/documents/`. Migrating the old-layout folders was
    never asked for and would contradict "existing subfolders are left alone" [src: EP-001/Q-003],
    so `## Out of scope` records that the mixed tree is accepted, and AC9 fixes the behaviour that
    produces it.
  - **AC12 added, from a combination nobody had named:** the band folder's name taken by a regular
    file. WI-0001/Q-002 settled this for the type folder; this item adds a path component, so the
    same rule needs restating for it. Without AC12 an implementation could reasonably crash there.
  - **AC10 states a product consequence rather than a mechanism:** a file that ages after it was
    sorted is never re-filed. It follows from AC9, but a user would otherwise discover it
    themselves, and `verify` can only check what a criterion says.
  - **Criteria are stated against real output.** `move   holiday.jpg -> recent/images/holiday.jpg`
    is the line `tidy/cli.py`'s `render` produces, not a format invented here.
  - **`refinement-qa.md` promoted to `status: recorded`.** Round 1's exchange happened and is quoted
    verbatim; round 2 asked nothing and says so.
- **Questions raised:** none. Round 1's two are answered and quoted in `artifacts/refinement-qa.md`;
  nothing is left `[unresolved]`.
- **Commands:**
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
    (before the transition)
  - `sed`/`cat` reads of `README.md`, `tidy/cli.py`, `tidy/planner.py`, `tidy/rules.py` → the output
    formats and the `os.utime`-based test style the criteria are written against
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, before and after the transition)
  - `definition-of-ready` → **pass**, criterion by criterion:
    - R1 frontmatter → **pass**: `id`, `type`, `title`, `status`, `priority: medium`, `epic:
      EP-001`, `created`, `updated`, `depends-on` all present
    - R2 story → **pass**, unchanged: role "someone tidying a folder that has built up over years",
      capability "old files separated from recent ones", outcome "so that the things I am still
      working with stay easy to find and the rest is put away"
    - R3 labelled criteria → **pass**: AC1–AC13, each a checkbox
    - R4 every criterion decidable → **fail in round 1 → pass now**: all five old criteria depended
      on the layout; the thirteen new ones each name a folder to build, a command to run and the
      verdict. No unmeasurable adjective remains — the two numbers in the item (365 days,
      31 536 000 seconds) are the same number stated twice
    - R5 out of scope → **pass**: six entries, including two a reader could reasonably assume were
      included — a third band, and migrating a folder the previous version tidied
    - R6 open questions non-blocking → **pass**: Q-001 and Q-002 are both `answered`; nothing open
    - R7 dependency finished → **pass**: `depends-on: WI-0001`, `done` at 16:40:26Z and merged
    - R8 Q&A recorded verbatim → **fail in round 1 → pass now**: `artifacts/refinement-qa.md` is
      `status: recorded` and carries both questions and both answers in the stakeholder's own
      words, tagged `[human]`, plus four `[assumed]` entries marked as `refine`'s own calls
    - R9 one coherent change → **pass**: one change to destination selection, in `planner.py` and
      `rules.py`, the modules `docs/architecture/overview.md` already names for it
    - R10 every combination visible → **fail in round 1 → pass now**: the six combinations map to
      AC6, AC7, AC8, AC9, AC10, AC11, AC12 and AC1, except the mixed tree, which is in
      `## Out of scope`. The map is written into `## Notes` so the claim is checkable
  - `criteria-are-decidable` → **pass**. Each criterion, and what settles it:
    - AC1 — folder with `holiday.jpg` (mtime now); PREVIEW; the move line must read
      `move   holiday.jpg -> recent/images/holiday.jpg`. Three path components, band first
    - AC2 — `a.pdf` (now) and `b.pdf` (400 days); PREVIEW; two different destinations,
      `recent/documents/a.pdf` and `old/documents/b.pdf`
    - AC3 — two files, mtime and atime crossed with `os.utime`; PREVIEW; bands must follow mtime.
      Fails if the implementation reads `st_atime`
    - AC4 — three files at exactly 365 days, one minute under and one minute over; PREVIEW; `old`,
      `recent`, `old`. Plus: no third band name appears in either mode's output
    - AC5 — PREVIEW's (name, destination) set captured, then APPLY on the unchanged folder;
      every file is afterwards at the path PREVIEW printed, with `old/documents/` created
    - AC6 — `notes.xyz` at 400 days; both modes print a `leave` line with no band in it; after
      APPLY the file is still at its original path and no `old/` was created for it
    - AC7 — `report.pdf` at 400 days plus a different `old/documents/report.pdf`; both modes print
      `old/documents/report (2).pdf`; after APPLY the pre-existing file's size and contents are
      unchanged
    - AC8 — `.hidden.jpg` at 400 days; it appears in neither mode's output and is not moved
    - AC9 — pre-existing `documents/`, `old/` and `recent/`, each holding a file; after APPLY all
      three are at the same paths, their prior contents unchanged, and none of their files appears
      in either mode's output
    - AC10 — `recent/documents/notes.txt` from an earlier run, mtime set to 400 days ago; no output
      line names it and it is still there after APPLY
    - AC11 — APPLY, APPLY; a recursive listing after the second run equals the one after the first,
      and a PREVIEW between them prints no move lines
    - AC12 — a regular file named `old` beside `taxes.pdf` at 400 days; both modes print a `leave`
      line whose reason names `old`, nothing moves, the regular file is unchanged, exit 0
    - AC13 — read `README.md`: the tree shape, both band names, last-modified as the field, and the
      boundary in days, compared against AC1, AC3 and AC4
  - `qa-recorded-verbatim` → **pass**. `artifacts/refinement-qa.md` `status: recorded` holds both
    round 1 questions with the stakeholder's replies quoted in full and tagged `[human]`; round 2
    records that it asked nothing and why; four answers are tagged `[assumed]` with the reasoning
    and the criterion that fixes each. Nothing is paraphrased into agreement — in particular
    Q-002's answer is recorded as *declining* the three-band recommendation.
- **Artifacts:**
  - `tracker/items/WI-0002/item.md` — `## Acceptance criteria` rewritten (AC1–AC5 → AC1–AC13),
    `## Out of scope` extended from three entries to six, `## Notes` rewritten around the four
    assumptions and the R10 map
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; round 2
    section added; the agenda table now records round 1's failures against round 2's results
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0002 is Ready. Thirteen criteria, each settled by a command over a folder with
  timestamps set by `os.utime`; four assumptions recorded with the criterion that fixes each and
  the cost of reversing it; one design question left for `plan` — how the age rule is represented,
  so WI-0003 does not design the rule format twice.

## 2026-08-27T18:08:16Z — plan v0.3.1 — architect

- **Item:** WI-0002
- **Trigger:** status `ready`, dispatched by `next` (step 5; best selection key of three `ready`
  candidates)
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — AC1–AC13, `## Out of scope` (six entries), `## Notes` (the
    four assumptions and the design question routed here)
  - `tracker/items/WI-0002/history.md` — four rows; this is a first plan, not a re-plan after a
    rejection
  - `tracker/items/WI-0002/artifacts/refinement-qa.md` (`status: recorded`) — both `[human]`
    answers, the four `[assumed]` entries, and the routing table that sent the rule-shape question
    here
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md`
  - `tracker/items/WI-0001/item.md` and `artifacts/plan.md` — the interfaces and the output contract
    this item extends
  - `tracker/items/WI-0003/item.md` — the item that must make both rule tables user-supplied
  - `docs/architecture/overview.md` (v2), `docs/product/vision.md` (v4)
  - ADR-0001 (stdlib-only CLI), ADR-0002 (plan/apply separation), ADR-0003 (`os.link` move),
    ADR-0004 (test and lint commands) — all four read, none contradicted
  - `tidy/rules.py`, `tidy/planner.py`, `tidy/apply.py`, `tidy/cli.py`, `tests/support.py`,
    `tests/cli_support.py`, `README.md`, `tracker/project.yaml`
- **Decisions:**
  - **ADR-0005 — the age rule is an ordered table plus a lookup**, `DEFAULT_BANDS` and
    `band_for(age_seconds)` in `tidy/rules.py`, mirroring `DEFAULT_RULES` and `folder_for`. Route:
    **decided here**; this is the design question `refine` routed to `plan`. Rationale: WI-0003 has
    to make both kinds of rule user-supplied and has no dependency on this item, so the shape that
    lands here is the shape it inherits — a constant plus an inline comparison (option A) would
    make it invent a representation for something that has none, and a predicate engine (option C)
    does not serialise into a configuration file. Two options rejected in the ADR with their costs.
  - **`now` is read once per `build_plan` call** and passed to the classification. Route: decided
    here, recorded in ADR-0005 `## Decision` §3. Rationale: reading the clock per file lets a slow
    run split a boundary between two files of identical age — a test could not reproduce it and a
    user would never explain it.
  - **`apply.py` and `cli.py` are not touched.** Route: **documented**. `apply_plan` already calls
    `os.makedirs(os.path.dirname(destination), exist_ok=True)`, so a two-component path costs it
    nothing, and `render` prints whatever destination string the action carries. The plan says
    explicitly that a developer who finds a reason to change either should ask rather than work
    around it.
  - **The not-a-folder check runs over both path components** (step 3), extending WI-0001/Q-002's
    rule to the component this item adds. Route: documented — AC12 requires it and `planner.py`
    already has the pattern for one component.
  - **The four inherited assumptions are adopted, not re-decided**, each with its reversal cost
    (`## Assumptions` 1–4). Route: **assumed**, following `refine`. Re-deciding them would be a
    plan quietly overturning a refinement.
  - **A file with a future modification time counts as `recent`** (`## Assumptions` 6). Route:
    assumed. No criterion covers it; it falls out of the ordered table; escalating a case where the
    only sane reading is obvious would spend the stakeholder's attention for nothing. Recorded so
    `verify` finds it stated rather than surprising.
  - **`docs/architecture/overview.md` deliberately not bumped in this execution.** Its two stale
    sentences — the `rules.py` row of the module table and the "No age handling" bullet — do not
    become false until the code lands, and the procedure says not to bump a document whose shape
    has not changed. Step 9 of the plan names both sentences so `implement` discharges D7 without
    rediscovering them.
  - **No ADR for the destination string's composition.** It is one `os.path.join` under ADR-0002
    and ADR-0005; an ADR would be padding, and padding is what makes an ADR trail unreadable.
- **Questions raised:** none. Nothing needed the stakeholder: the two decisions with product stake
  were asked and answered in refinement round 1 [src: WI-0002/Q-001; WI-0002/Q-002], and every
  remaining choice is fixed by a criterion, cited to an existing document, or recorded as a
  reversible assumption.
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, "Ran 37 tests ... OK"
  - `python3 -m compileall -q tidy tests` → exit 0
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 1 first
    (`claim.unsourced` on ADR-0005's `DEFAULT_BANDS`/`None` paragraph), then exit 0 after the
    citation was added
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors 0 warnings
- **Gates:**
  - `workspace-valid` → **pass** (`validate-workspace`, exit 0, 6 items and 7 documents)
  - `every-criterion-is-addressed` → **pass**. The mapping table in `plan.md` has one row per AC,
    AC1–AC13, each naming the step that satisfies it and a specific demonstration — not "tests".
    Checked in the other direction too: every one of the nine steps is referenced by at least one
    row, so the plan contains nothing no criterion asks for.
  - `project-commands-resolved` → **pass**. `tracker/project.yaml` already carries
    `test: python3 -m unittest discover -s tests -t . -q` and
    `lint: python3 -m compileall -q tidy tests` [src: ADR-0004]; both were **run in this execution**
    rather than assumed, exit 0 and 0. `build: null` is honest — there is nothing to build for a
    stdlib-only package [src: ADR-0001].
  - `decisions-recorded` → **pass**. The `## Decisions and ADRs` table lists eight choices, each
    pointing at ADR-0005, at an existing ADR, or at a numbered entry under `## Assumptions` with
    what reversing it costs.
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0 after one real
    finding was fixed — the ADR's `None`-bound paragraph made an absolute claim about
    `DEFAULT_BANDS` with no citation).
  - `plan-is-executable-without-you` (advisory) → **pass, with one reservation recorded**. Read
    cold, each step names its files and what is true afterwards. The reservation: step 3 says to
    test "each folder component of the destination in turn" without prescribing the loop, which is
    deliberate — the interface and the observable are fixed, the code is the developer's.
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/plan.md` (new) — all nine required sections
  - `docs/architecture/adr/ADR-0005-age-bands-as-a-table.md` (new, v1) — three options, the
    decision in three checkable parts, and reversibility stated as cheap
  - `tracker/board.md` — regenerated
  - `docs/architecture/overview.md` — **not** changed, deliberately; see `## Decisions`
- **Status:** `ready` → `planned`
- **Result:** WI-0002 is planned. Nine steps: two production files change (`tidy/rules.py`,
  `tidy/planner.py`), `apply.py` and `cli.py` do not, three test modules and one fixture helper
  grow, and `README.md` plus `docs/architecture/overview.md` v3 are named as the documentation the
  change obliges. One new ADR; six assumptions, each with its reversal cost.

## 2026-08-27T18:11:21Z — implement v0.2.2 — developer

- **Item:** WI-0002
- **Trigger:** status `planned`; dispatched by `next` as the best-ranked runnable item (medium, created 15:44:21Z, ahead of BUG-0001 and BUG-0002 on `created`).
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the thirteen acceptance criteria, the out-of-scope list, and the four inherited assumptions
  - `tracker/items/WI-0002/artifacts/plan.md` — the nine steps, the fixed interfaces, and the AC-to-step mapping
  - `tracker/items/WI-0002/history.md` — five rows; the last is `ready → planned` by `plan`, so this is a fresh start with no branch
  - `tracker/items/WI-0002/questions/Q-001.md`, `Q-002.md` — both `answered` and propagated in turn 8; re-read the artifacts they updated rather than acting on the question files
  - `docs/architecture/adr/ADR-0005-*.md` — the band table's shape, the half-open comparison, and the once-per-run clock
  - `tracker/project.yaml` — `commands.test`, `commands.lint`, branch prefix `wi/`, commit subject convention
  - `tidy/rules.py`, `tidy/planner.py`, `tidy/apply.py`, `tidy/cli.py`, `tests/support.py`, `tests/cli_support.py`, `tests/test_rules.py`, `tests/test_planner.py`, `tests/test_cli.py`, `README.md` — the code this plan changes and the tests that already assert the un-banded destinations
- **Decisions:**
  - Branched from `main` rather than from `wi/WI-0001`: WI-0001 is `done` and merged, so `main` already carries it.
  - Recorded before any code is written: the existing suite asserts destinations of the form `documents/report.pdf`, which this item changes to `recent/documents/report.pdf` by the stakeholder's own decision [src: WI-0002/Q-001]. Those tests will be updated to the new shape, preserving what each one tests; every such edit will be named in `impl-report.md`, because a test edited to make a change pass is the failure mode this record exists to expose.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0002 main` → 0
- **Gates:**
  - `tests-pass` → **skipped** (not yet run; no code has changed. This entry opens the execution)
  - `lint-clean` → **skipped** (not yet run)
  - `workspace-valid` → **skipped** (not yet run; this move is made through `transition`, which validates)
  - `every-criterion-has-a-test` → **skipped** (not yet run; no test has been written)
  - `commits-reference-the-item` → **skipped** (not yet run; the branch has no commits)
  - `claims-are-sourced` → **skipped** (not yet run; no document has changed)
- **Artifacts:**
  - branch `wi/WI-0002`, created at `main` (47c2dd8), no commits yet
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0002 has started on `wi/WI-0002`. The plan's nine steps are unstarted; the closing entry reports the work and runs the gates.

## 2026-08-27T18:18:18Z — implement v0.2.2 — developer

- **Item:** WI-0002
- **Trigger:** status `in-progress`; the opening entry of this execution created the branch and the plan's nine steps have now been worked in order.
- **Inputs read:**
  - `tracker/items/WI-0002/item.md`, `artifacts/plan.md`, `history.md`, `questions/Q-001.md`, `questions/Q-002.md` — read at the opening entry; nothing changed under them during the execution
  - `docs/architecture/adr/ADR-0005-*.md` — the band table's shape, the half-open comparison, and the once-per-run clock
  - `tidy/rules.py`, `tidy/planner.py`, `tidy/apply.py`, `tidy/cli.py`, `README.md`, `docs/architecture/overview.md`, and all five test modules
- **Decisions:**
  - **The eleven existing tests that asserted un-banded destinations were updated rather than left failing.** The stakeholder's chosen layout puts the band above the type folder [src: WI-0002/Q-001], so `documents/report.pdf` becoming `recent/documents/report.pdf` is the delivered behaviour, not a regression. Each edit adds the band and weakens no assertion; the list is in `impl-report.md` `## Deviations` 2, written so a reviewer can check the claim rather than accept it.
  - **AC13's test was placed in `tests/test_rules.py`, not `tests/test_cli.py` as plan step 7 said.** The README-parsing helper, `REPOSITORY_ROOT`, and the equivalent extension-table test already live there; the CLI module imports nothing from `tidy` and would have needed all three duplicated. What the plan required — the README parsed, not restated — is unchanged. Recorded as deviation 1.
  - **One test beyond the plan's list:** `test_the_whole_run_is_measured_against_one_instant`. ADR-0005 §3 fixes the once-per-run clock and no criterion covers it, so without this the decision would have been unobservable.
  - **`tidy/cli.py` was left untouched although its `--help` text is now incomplete** — it describes sorting by type and not by age. Not a guess and not an oversight: the plan puts any change to `cli.py` out of scope, no criterion covers the help text, and suspending the item on a blocking question over two strings looked disproportionate against declaring it. It is `impl-report.md` `## What I did not do` item 1, with a recommendation, so `verify` and `review-close` both meet it. **This is the one judgement in this execution that a reviewer might reasonably overturn**, and it is written where they will see it.
  - Two `README.md` bullets were added beyond AC13's requirements — a filed file is never re-filed, and the older layout is not migrated. Both are behaviour a user meets whether or not it is documented (AC10, and the accepted mixed tree). Flagged under the advisory scope gate rather than left for a reviewer to notice.
  - **Not decided here, and not guessed:** nothing. No question arose that the plan or an ADR did not already settle.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → 0, `Ran 63 tests ... OK` (run after every step; 37 before this item)
  - `python3 -m compileall -q tidy tests` → 0
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, 0 errors 0 warnings
  - `.claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → 0, `all 8 commit(s) on main..wi/WI-0002 name WI-0002`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0, 1 document checked
  - `git diff main..wi/WI-0002 --stat` → 0; `tidy/apply.py` and `tidy/cli.py` appear in it not at all
  - mutation checks, reverted after each: planner reading `st_atime` → 4 failures including AC3's; `band_for` returning a constant → 14 failures; README's `old` row without the number, and the field reworded to "last opened" → AC13's test fails in both
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0, 63 tests)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace` exit 0, 6 items and 7 documents, 0 errors 0 warnings)
  - `every-criterion-has-a-test` → **pass** (`impl-report.md` `## Acceptance criteria evidence` names at least one test function per AC1–AC13. AC4's universal clause — "no third band name appears anywhere" — is not tested by exhaustion; the report states what is tested instead and why it entails the claim)
  - `commits-reference-the-item` → **pass** (`check-commit-refs WI-0002 wi/WI-0002` exit 0, all 8 commits)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0)
  - `no-unplanned-scope` (advisory) → **pass, with one hunk named** (every `tidy/` hunk traces to plan steps 1–3; the two extra README bullets are judgement rather than a step and are named in the report's gate table)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/impl-report.md` — created
  - `tidy/rules.py`, `tidy/planner.py` — the change; `tidy/apply.py` and `tidy/cli.py` unchanged
  - `tests/support.py` (new `age()` helper), `tests/test_rules.py`, `tests/test_planner.py`, `tests/test_cli.py`, `tests/test_apply.py`
  - `README.md`; `docs/architecture/overview.md` → **v3**, discharging plan step 9
  - branch `wi/WI-0002`, commits `a85ea85..ee417b1` (8 commits on `main..wi/WI-0002`), not merged
- **Status:** `in-progress` → `verifying`
- **Result:** All nine plan steps are executed and all thirteen acceptance criteria have a named test. `tidy/apply.py` and `tidy/cli.py` were not touched, as the plan predicted. One user-visible gap is declared rather than fixed: `--help` still describes sorting by type only, which no criterion covers and which the plan put out of scope.

## 2026-08-27T19:12:37Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0002
- **Trigger:** Status `verifying`, dispatched by `next` as the highest-ranked runnable item (priority rank 3, created 2026-08-27T15:44:21Z, ahead of BUG-0001 and BUG-0002 on `created` and ahead of WI-0003 on priority).
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — the thirteen criteria, read in full **before** the implementation report, so what would settle each was derived from the criterion rather than from what was built
  - `tracker/items/WI-0002/history.md` — the move to `verifying` at 18:18:18Z, made by `implement`
  - `tracker/items/WI-0002/artifacts/plan.md` — the nine steps, the fixed interfaces, the six assumptions, the risks
  - `tracker/items/WI-0002/artifacts/impl-report.md` — read after the criteria; its claims were checked, not cited
  - `tracker/items/WI-0001/item.md` AC1 and AC5 — the `--help` contract and the extension table WI-0002's AC13 builds on
  - `tracker/project.yaml` — `commands.test` and `commands.lint`
  - the code at `93a958599cdfe10c81dfba337d62811e23db564c`, branch `wi/WI-0002`: `tidy/planner.py`, `tidy/rules.py`, `tidy/apply.py`, `tidy/cli.py`, `README.md`, and `git diff main..wi/WI-0002`
- **Decisions:**
  - **All thirteen criteria pass**, each on a command run in this execution over fixtures built here (`.verify-scratch/fix.py`, an `os.utime` builder written for this verification and independent of `tests/support.py`). No box was ticked on the strength of a test name or of `impl-report.md`.
  - **AC4's exact boundary was settled by two measurements, not one.** `build_plan` reads its own clock, so a folder fixture cannot make a file exactly 31 536 000 seconds old at the instant the run measures it — the folder case is boundary-plus-epsilon. The exact point was decided by calling `band_for(31536000)` directly, which returns `old`. Both are recorded in the report rather than the folder case being passed off as exact.
  - **AC4's universal clause is not exhaustible and was not exhausted.** "No third band name appears anywhere in either mode's output over any folder" was decided by its grounds — every destination's first component is `band_for`'s return, `band_for` returned only `recent` and `old` over a sweep of ages from 0 to three years, and `DEFAULT_BANDS` holds exactly those two names — and declared under `## Not verified, and why` as an argument rather than a measurement.
  - **AC9 passes with this run's own destination excluded**, which is what the criterion says: "every file inside them that was not a destination of this run is unchanged". The `recent/` listing differs by exactly `images/newthing.jpg`; `documents/` and `old/` are byte-identical.
  - **The `--help` gap is a bug, not a send-back** — filed as **BUG-0003**. The SKILL's test decides it: no WI-0002 criterion says the help text should be different, so nothing this item was asked for is unmet. `found-in: WI-0002` rather than WI-0001, because the sentence is WI-0001's but what it is wrong about is WI-0002's routing, and it is wrong only from this branch onward.
  - **A weakness in AC13's regression test was found and deliberately not filed.** The test asserts `"last modified"` as a whole-file substring and `README.md` contains the phrase three times, so rewording the sentence a user reads leaves the suite green. `impl-report.md` claims that exact mutation fails the test; it does not. The criterion itself passes — the README does state the field — so this is a note on the regression net, recorded in the report rather than made into an item.
  - **No unaccounted scope in the diff.** `tidy/apply.py` and `tidy/cli.py` are untouched, and every hunk in `tidy/`, `README.md` and `docs/architecture/overview.md` traces to a plan step (1–3, 8, 9). The two extra README bullets `implement` flagged as judgement are AC10 and the accepted mixed tree — user-facing statements of behaviour the criteria already fix, not new behaviour.
- **Questions raised:** none
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 63 tests in 0.056s` / `OK`
  - `python3 -m compileall -q tidy tests` → exit 0
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 7 item(s), 7 document(s)`, 0 errors 0 warnings
  - `git rev-parse HEAD` → `93a958599cdfe10c81dfba337d62811e23db564c`
  - `git diff main..wi/WI-0002 --stat` and `git diff main..wi/WI-0002 -- tidy/ README.md` → exit 0; `apply.py` and `cli.py` absent from the stat
  - AC1: `python3 -m tidy .verify-scratch/ac1` → exit 0, `move   holiday.jpg -> recent/images/holiday.jpg`
  - AC2: `python3 -m tidy .verify-scratch/ac2` → exit 0, `recent/documents/a.pdf` and `old/documents/b.pdf`
  - AC3: `python3 -m tidy .verify-scratch/ac3` → exit 0, mtime-400/atime-now → `old/…`, mtime-now/atime-400 → `recent/…`
  - AC4: `python3 -m tidy .verify-scratch/ac4` → exit 0, 365d → `old`, −60s → `recent`, +60s → `old`; plus `band_for` called directly across seven ages and a sweep
  - AC5: `python3 -m tidy .verify-scratch/ac5` then `--apply` → exit 0 both; `find` afterwards shows every file at the previewed path, `old/documents/` created
  - AC6: `python3 -m tidy .verify-scratch/ac6` and `--apply` → exit 0, two `leave` lines, no band folder created
  - AC7: `python3 -m tidy .verify-scratch/ac7` and `--apply` → exit 0, `old/documents/report (2).pdf`; pre-existing file's sha256 `b4b4a381…` unchanged
  - AC8: `python3 -m tidy .verify-scratch/ac8` and `--apply` → exit 0, `.hidden.jpg` in neither output and still in place
  - AC9: `python3 -m tidy .verify-scratch/ac9` and `--apply` → exit 0; hashed recursive listings of the three pre-existing folders compared before and after
  - AC10: `python3 -m tidy .verify-scratch/ac10` and `--apply` → exit 0, `Nothing to do`, listing identical, no `old/`
  - AC11: APPLY, PREVIEW, APPLY → exit 0 each; `grep -c '^move '` on the middle PREVIEW → 0; listings after run 1 and run 2 equal
  - AC12: `python3 -m tidy .verify-scratch/ac12-strict` and `--apply` → exit 0, `leave  taxes.pdf   ['old' exists and is not a folder]`, nothing moved, blocking file's sha256 unchanged; control run with nothing to move also exit 0; extra run with `old/documents` a regular file → `['old/documents' exists and is not a folder]`
  - AC13: `cat README.md` → the tree shape, both band names, `**last modified**`/`mtime`, and `**365 days**` in both band rows
  - negatives: empty folder → `Nothing to do…` exit 0; missing folder → `tidy: … is not a folder` exit 2; future mtime → `recent`; three equal-age files → all `old`; symlink → aged by its target
  - ten mutations, each applied then reverted with `git checkout --`, the suite run between: see the report's `## Test sensitivity check`
  - `python3 .claude/agile-skills/scripts/new-item --next-id bug` → `BUG-0003`; `new-item --id BUG-0003 … --found-in WI-0002` → exit 0
  - `python3 .claude/agile-skills/scripts/journal-entry BUG-0003 --skill verify --body-file …` → exit 0
  - `python3 .claude/agile-skills/scripts/board-gen .` → exit 0, `wrote tracker/board.md`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` on the branch head, exit 0, `Ran 63 tests … OK`)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests`, exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0, 7 items and 7 documents, 0 errors)
  - `every-criterion-independently-checked` → **pass** (every row of the report's `## Criteria` names a command run here over a fixture built here; no row cites `impl-report.md`)
  - `negative-cases-exercised` → **pass** (ten cases triggered, listed in the report: the boundary itself, unrecognised and extensionless files, a taken destination, a band name taken by a regular file, the type component taken inside a band, a nothing-to-move run, an empty folder, a missing folder, a future-dated file, equal-age files, a symlink)
  - `tests-would-fail-without-the-change` (advisory) → **pass, with one weakness** (ten mutations, every criterion covered by at least one failing test; AC13's "last modified" clause survives a single-occurrence reword, recorded in the report)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/verify-report.md` — created: verdict, thirteen criterion rows with commands and actual output, gates, negatives, the mutation table, defects, and what was not verified
  - `tracker/items/WI-0002/item.md` — all thirteen checkboxes ticked, each on evidence gathered here
  - `tracker/items/BUG-0003/` — new bug item at `ready`, `found-in: WI-0002`, with its creation journal entry
  - `tracker/board.md` — regenerated
- **Status:** `verifying` → `in-review`
- **Result:** WI-0002 meets all thirteen of its acceptance criteria, verified on `93a9585` by commands run here rather than by reading the implementation report; age routing puts `<band>/<type>/<name>` in place without disturbing any invariant WI-0001 established. One defect in behaviour delivered elsewhere — `--help` still describes sorting by type alone — is filed as BUG-0003 and does not belong to this item.

## 2026-08-27T19:17:03Z — review-close v0.5.0 — reviewer

- **Item:** WI-0002
- **Trigger:** Status `in-review`, dispatched by `next` as the highest-ranked runnable item (priority rank 3; earliest `created` among the four medium-priority candidates).
- **Inputs read:**
  - `tracker/items/WI-0002/item.md` — thirteen criteria, all ticked; `## Notes`, `## Out of scope`
  - `tracker/items/WI-0002/history.md` — eight rows, chaining `—` → `draft` → `awaiting-answer` → `draft` → `ready` → `planned` → `in-progress` → `verifying` → `in-review`
  - `tracker/items/WI-0002/journal.md` — all eight entries in full, one per history row
  - `tracker/items/WI-0002/artifacts/plan.md`, `impl-report.md`, `verify-report.md`
  - `tracker/items/WI-0002/questions/Q-001.md` and `Q-002.md`, including `## Consequences`, and the four files each names — opened rather than trusted
  - the diff `main..wi/WI-0002`, hunk by hunk, 14 files: `tidy/rules.py`, `tidy/planner.py`, `tests/support.py`, `tests/test_apply.py`, `tests/test_cli.py`, `tests/test_planner.py`, `tests/test_rules.py`, `README.md`, `docs/architecture/overview.md`, and the tracker files
  - `docs/architecture/adr/ADR-0005-age-bands-as-a-table.md` in full; ADR-0002 and ADR-0003 for the claims this change could have falsified
  - `docs/architecture/overview.md` v3 and `docs/product/vision.md` v4 — for D7 and D12
  - `tidy/planner.py`, `tidy/rules.py`, `tidy/apply.py`, `tidy/cli.py` as they stand on the branch — the code the docs' claims cite
- **Decisions:**
  - **Accept, merge and close, `outcome: delivered`.** All thirteen criteria ticked with evidence; all twelve Definition of Done criteria pass, each recorded separately in `review.md`.
  - **The eleven pre-existing tests that changed were read line by line rather than taken on trust.** `impl-report.md` deviation 2 flagged them as exactly the shape a defect hides in, and it was right to. Every removed line is a path with the band added, a docstring, or an import; no assertion was deleted or weakened, and `test_destination_folders_are_created_as_needed` was strengthened to assert both path components.
  - **BUG-0003's routing is correct and I did not re-route it.** `verify` filed the stale `--help` text as a bug rather than a send-back; I ran `--help` myself and checked WI-0001 AC1's three requirements still hold. No WI-0002 criterion covers the help text, so nothing this item was asked for is unmet. `found-in: WI-0002` is the right end of the pair: the sentence is WI-0001's, but what it is wrong about is age routing.
  - **AC13's weak test sensitivity is an accepted gap, not a send-back and not a new item.** Reproduced at review: rewording `README.md` line 43's `**last modified**` leaves the suite green, because the assertion is a whole-file substring and the phrase occurs three times. `impl-report.md`'s claim that this mutation fails the test is inaccurate and is named in `review.md` `## Findings` so a later reader does not inherit it. The criterion itself passes — the README states the field. A weak test is not delivered behaviour, so it is not a bug.
  - **Nine gaps accepted, and every one written into `item.md` `## Notes`.** A gap that lives only in a verification report stops being read the moment the item closes. The five that were nowhere else — symlinks, clock skew, AC4's unexhaustible clause, the boundary settled through `band_for`, and AC13's test — are now in the item.
  - **No ADR is contradicted, so no question was filed.** ADR-0002's "every destination decided in `planner.py`" survives because the band is composed there; ADR-0003's `os.link` path is untouched; ADR-0005 is this item's own and its `## Decision` matches the code line for line.
  - **D12 was decided from the citations, not the prose.** Ten absolute claims across `overview.md`, `vision.md` and ADR-0005 were each checked by opening the code they cite. All ten hold. The table is in `review.md` `## What I examined`.
  - **The trial merge was detached and the trunk was checked afterwards.** `git rev-parse main` returned `47c2dd8a568dc4a1d4ff498574de11c2d4d058f9` before and after, so the trial published nothing.
- **Questions raised:** none
- **Commands:**
  - `python3 .claude/agile-skills/scripts/check-verify-freshness WI-0002 wi/WI-0002` → exit 0, "verified at 93a95859; wi/WI-0002 has moved to c72f62e1 but only the record changed (10 file(s) under tracker/ or docs/), so the verification still covers the code"
  - `python3 .claude/agile-skills/scripts/check-commit-refs WI-0002 wi/WI-0002` → exit 0, `all 11 commit(s) on main..wi/WI-0002 name WI-0002`
  - `python3 .claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, 1 document checked, 0 errors 0 warnings
  - `python3 .claude/agile-skills/scripts/check-epic-signoff WI-0002` → exit 0, "WI-0002 is a 'work-item', not an epic — the termination gate applies to an engagement's ending only. PASS."
  - `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 7 items and 7 documents, 0 errors
  - `git diff main..wi/WI-0002 --stat`, then per-path diffs of `tidy/`, `README.md`, `docs/`, and each test file → exit 0
  - `git rev-parse main` → `47c2dd8a568dc4a1d4ff498574de11c2d4d058f9` (before the trial)
  - `git worktree add --detach /tmp/tidy-trial main` → exit 0, "HEAD is now at 47c2dd8"
  - `git -C /tmp/tidy-trial merge --no-ff wi/WI-0002` → exit 0, merge commit `f0adf5e04859ad763c104aeb76b3970fd8ba92e7`
  - `python3 -m unittest discover -s tests -t . -q` **inside the trial worktree** → exit 0, `Ran 63 tests in 0.055s` / `OK`
  - `python3 -m compileall -q tidy tests` inside the trial worktree → exit 0
  - `git worktree remove --force /tmp/tidy-trial` → exit 0; `git rev-parse main` → `47c2dd8a…` unchanged
  - `python3 -m tidy --help` → exit 0, still "chosen by file type" — checked for finding 1 rather than read about
  - `sed -i 's@\*\*last modified\*\*@**last opened**@' README.md` then the suite → exit 0, still green; reverted with `git checkout -- README.md` — the reproduction behind finding 2
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each recorded with its own result and evidence in `review.md` `## Definition of Done`; no single overall verdict was used)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness`, exit 0; the branch moved after verification but only under `tracker/`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs`, exit 0, 11 of 11 commits; run before the merge, while `main..wi/WI-0002` is still a non-empty range)
  - `tests-pass-on-the-merge-result` → **pass** (the suite run inside the detached trial worktree at `f0adf5e0`, exit 0, 63 tests OK — the merge result, not the branch)
  - `workspace-valid` → **pass** (`validate-workspace .`, exit 0)
  - `record-is-reconstructible` → **pass** — answered from the record alone: *what was built and why* — age routing puts the band above the type folder because the stakeholder wanted the top level to show what is live (`item.md` `## Notes`, Q-001, `vision.md` v4); *which skill decided what* — `refine` pinned 365 days as a reversible assumption, `plan` chose the table shape in ADR-0005, `implement` deviated three times and declared each; *what questions arose and how they resolved* — Q-001 and Q-002 to the stakeholder, both answered and propagated into four files each; *what verification found* — thirteen criteria with commands and quoted output, ten mutations, and BUG-0003
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main`, exit 0; and the ten-row D12 audit, which is the half a program cannot do)
  - `epic-sign-off` → **pass, not applicable** (`check-epic-signoff WI-0002` → exit 0: this is a work item, not an epic. EP-001 is not at rest — BUG-0001, BUG-0002, BUG-0003 are `ready` and WI-0003 is `draft` — so no sign-off question is due yet)
- **Artifacts:**
  - `tracker/items/WI-0002/artifacts/review.md` — created: what was examined, the D1–D12 table, five findings, nine accepted gaps, the verdict
  - `tracker/items/WI-0002/item.md` — `## Notes` gained the five gaps that lived only in reports and a pointer to BUG-0003; `outcome: delivered` recorded at close
  - the merge of `wi/WI-0002` into `main`
- **Status:** `in-review` → `done`
- **Result:** WI-0002 is accepted and closed as delivered. Age routing lands as `<band>/<type>/<name>` without touching `apply.py` or `cli.py` — the architectural prediction `overview.md` made after WI-0001, now tested. One defect belongs elsewhere (BUG-0003, the stale `--help` text) and nine gaps are accepted with reasons, all of them recorded in the item rather than only in a report.

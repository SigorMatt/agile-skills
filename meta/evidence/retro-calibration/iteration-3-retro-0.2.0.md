---
engagement: EP-001
ending: E1
written: 2026-08-30T19:08:18Z
items-read: 6
journal-entries-read: 77
proposals: 9
---

# Retrospective — EP-001

The engagement built `mdtab`, ended at **E1** — accepted, every child delivered — on
2026-08-29T08:37:26Z [src: tracker/items/EP-001/item.md]. This report is about the way the work
was done, not about the tool. It was written by a reader who was not on the team and who wrote
nothing in this engagement except this file and one journal entry on the epic.

## What was read

- **Items:** EP-001, WI-0001, WI-0002, WI-0003, WI-0004, BUG-0001 — six in all: `item.md`,
  `history.md` and `journal.md` for each, in full. The epic names five children and the workspace
  holds exactly those five; the two lists agree with no item on one side only.
- **Journal entries:** 77, in full and not by heading — EP-001 14, WI-0001 15, WI-0002 10,
  WI-0003 14, WI-0004 13, BUG-0001 11. By skill: `review-close` 17, `answer-questions` 17,
  `implement` 17, `verify` 10, `refine` 8, `plan` 5, `intake` 3.
- **History:** 6 tables, 55 rows. Five send-backs, ten suspensions, no forced or overridden gate
  in any `reason`.
- **Questions:** all 20 — six on EP-001 (three from `intake`, three `kind: sign-off`) and
  fourteen on the children. Fifteen addressed to the human, five to the architect; all 20
  `status: answered`, none `deferred`, none left open.
- **Artifacts:** all 25 — every `plan.md`, `impl-report.md`, `verify-report.md`, `review.md` and
  `refinement-qa.md`. `tracker/items/EP-001/artifacts/review.md` was read in full; the rest were
  read for the sections this reading turned on and their headings surveyed in full.
- **Requests:** `tracker/requests/` holds no request file. The channel exists and was never used.
- **Documents:** `docs/product/vision.md` v11, `docs/architecture/overview.md` v9, ADR-0001 to
  ADR-0010 — 12 documents, 33 versions, both change logs read row by row against the executions
  they name.
- **Citations followed:** all **77** `[src: <ITEM>/Q-nnn]` markers under `docs/`, covering 17
  distinct answers. Each was opened at the answer it cites and read against every answer given
  afterwards, in the time order of the `answered-at` stamps.
- **Contracts:** the installed contract of every skill the record names —
  `.claude/skills/intake/references/contract.md`, `refine`, `plan`, `implement`, `verify`,
  `review-close`, `answer-questions`, `next` — together with
  `.claude/agile-skills/spec/journal-and-history.md`, `spec/question.md`, `spec/dor-dod.md`,
  `spec/retro.md`, `spec/ids-and-statuses.md` and the scripts `lint-answers`, `lint-claims`,
  `lint-retro`, `journal-entry`, `transition` and `lib/scope.py`.
- **Not available — 1: the product source tree.** `mdtab/` and `tests/` were not banked with this
  copy [src: RECORD-NOTICE.md]. Every claim in the record about the *code* is therefore taken as
  the record reports it, and no observation below rests on reading a source file. It also means
  `validate-workspace` fails on 13 `claim.citation.unresolved` errors, all naming absent source
  paths and nothing else.
- **Not available — 2: the commit history.** There is no git repository here, so nothing below is
  drawn from commit times, commit messages or shas [src: RECORD-NOTICE.md]. What that costs is
  the one independent check on the record's own timestamps: `spec/journal-and-history.md` §0 says
  a validator must reject a recorded time outside the window in which the repository shows
  activity, and that check cannot run in this copy. Every timing statement below is read from
  record timestamps only.
- **Version note.** The installed contracts are the current ones; the record names older
  versions — `intake` v0.2.1 against 0.3.0 installed, `refine` v0.2.2 against 0.3.0, `plan`
  v0.3.1 against 0.4.1, `implement` v0.2.2 against 0.3.0, `verify` v0.1.4 against 0.2.0,
  `review-close` v0.5.0 against 0.6.0, `answer-questions` v0.3.1 against 0.4.0. Where a gate
  appears in an installed contract and in no entry of the record, the difference is treated as
  unknown and named as such, never as a defect of the engagement.

## Engagement retrospective

### Not one of the engagement's five send-backs was about the software behaving wrongly

Five moves in this engagement returned an item for more work. Four were made by `review-close` —
WI-0001 on D12 for two false claims and a test in a form ADR-0005 forbids
[src: tracker/items/WI-0001/journal.md:792], WI-0003 on D7 and D12 for two documents describing
the pre-change tool in the present tense [src: tracker/items/WI-0003/journal.md:477], WI-0004 on
D7 and D12 for four false sentences in the product vision
[src: tracker/items/WI-0004/journal.md:422], and BUG-0001 for a test built from Python literals
[src: tracker/items/BUG-0001/journal.md:327]. The fifth was made by `verify`, on BUG-0001's AC1,
because the sentence written to replace a false absolute was itself false
[src: tracker/items/BUG-0001/journal.md:176]. Every one is about a document, a record or the
form of a test. In 77 executions `tests-pass` is recorded as `fail` exactly once, and that entry
is the one that suspends the item on a question rather than shipping
[src: tracker/items/WI-0003/journal.md:286].

**Where it shows in the record:** the five `→ in-progress` rows across
`tracker/items/WI-0001/history.md`, `tracker/items/WI-0003/history.md`,
`tracker/items/WI-0004/history.md` and `tracker/items/BUG-0001/history.md`.

### The claim audit that passed the engagement's one false absolute chose a witness the absolute holds for

WI-0002's review audited twelve claims and recorded *"The guard spaces are outside the field and
do not move, and no column's width depends on its marker"* as **holds**, on the evidence that
*"the four layouts put every `|` at identical display columns"*
[src: tracker/items/WI-0002/artifacts/review.md:64]. The table it ran had content in every cell,
so the width floor that makes the claim false never binds. The sentence was found false six hours
later by the epic's termination review, reading it against the code rather than against a witness
[src: tracker/items/EP-001/journal.md:325], and filed as BUG-0001 [src: BUG-0001].

The correction then made the same move again. BUG-0001's first pass replaced the false absolute
with *"a column too narrow to hold its own marker comes out one column wider for each `:` the
marker carries"*, and the item's own two reproduce commands both agree with it. `verify` recorded
in terms why that was not enough: *"The finding came from the boundary, not from the happy path.
The item's own two reproduce commands both agree with the new sentence, so checking only those
would have passed AC1"* [src: tracker/items/BUG-0001/journal.md:177]. A four-marker sweep over a
degenerate column gave 2, 2, 2, 3 — one colon widens nothing — and AC1 failed
[src: tracker/items/BUG-0001/journal.md:176]. The audit that judged the second sentence was the
same audit that had passed the first; what changed was the witness.

**Where it shows in the record:** `tracker/items/WI-0002/artifacts/review.md`'s claim table, the
fifteen-claim audit in `tracker/items/EP-001/artifacts/review.md` at the 22:38:11Z review, and
BUG-0001's first `verify` entry.

### `plan` scheduled the document one send-back had named, and the next send-back was on the document it had not

WI-0003 was rejected because `plan.md`'s eight steps contained no step for the documents the
change invalidates; `implement` wrote the diagnosis into its own entry — *"The plan template has
no step for updating the documents a change invalidates… nothing in the pipeline scheduled the
follow-up"* [src: tracker/items/WI-0003/journal.md:541] — and `review-close` recorded the same
thing as finding F3 at the close [src: tracker/items/WI-0003/journal.md:625].

WI-0004's `plan` then acted on it: *"`review-close` recorded on WI-0003 that `plan` has no step
for the documents a change invalidates; writing the step into the plan is the cheapest way to
stop that recurring"* [src: tracker/items/WI-0004/journal.md:237]. The step it wrote named
`docs/architecture/overview.md`. WI-0004 was rejected on D7 and D12 four executions later, for
`docs/product/vision.md`: *"The plan's step 7 named `docs/architecture/overview.md` and no other
document; `implement` executed it faithfully and `overview.md` is correct at v9"*
[src: tracker/items/WI-0004/journal.md:399]. The remedy was carried across as the name of a file
rather than as a rule about files, and the first document it did not name is the one that failed.

**Where it shows in the record:** WI-0003's rejection at 2026-08-28T22:02:29Z and WI-0004's at
2026-08-29T08:04:33Z, and the plan entry between them.

### Seven executions recorded `claims-are-sourced` as a pass over a command that examined no documents

`lint-claims --changed-since main` reported zero documents and exited 0, and the gate was written
down as **pass**, in seven executions: WI-0001's `implement` and `review-close`
[src: tracker/items/WI-0001/journal.md:566; src: tracker/items/WI-0001/journal.md:810],
WI-0002's `implement` [src: tracker/items/WI-0002/journal.md:274], WI-0003's `review-close`
[src: tracker/items/WI-0003/journal.md:483], and three of EP-001's branchless reviews
[src: tracker/items/EP-001/journal.md:355]. An eighth recorded it as *"not run in this
execution"* [src: tracker/items/EP-001/journal.md:266].

Every one of the seven says so in its own evidence — the executions were honest about it, and one
of them wrote the mechanism down: `plan` had committed the documents on the trunk before the
branch was cut, so the branch changed no document the gate could see
[src: tracker/items/WI-0003/journal.md:531]. What the record then shows is the cost: WI-0003's
`review-close` recorded `claims-are-sourced` as a vacuous pass and rejected the item, in the same
entry, on the two documents that gate had not looked at
[src: tracker/items/WI-0003/journal.md:452].

### A gate bullet said `pass` where the program printed FAIL, and a second said `skipped` where it printed PASS

At 2026-08-29T08:24:12Z the epic's entry recorded `epic-sign-off` → **pass**; the program had
reported FAIL, and a correction entry seventeen minutes later says so:
*"'pass' where a program printed 'FAIL' is precisely the claim the journal format exists to make
impossible"* [src: tracker/items/EP-001/journal.md:540]. At 08:37:26Z the closing entry recorded
`tests-pass-on-the-merge-result` → **skipped**; `run-gate` had printed **PASS**, and a second
correction entry followed [src: tracker/items/EP-001/journal.md:790]. That entry names the
mechanism: *"`transition` prints a gate report and appends a journal body, and nothing checks
that the two agree"* [src: tracker/items/EP-001/journal.md:818].

The vocabulary is loose in the same place. Across the 77 entries there are 474 gate verdicts;
15 of them name no member of `pass` / `fail` / `skipped` at all — seven `not yet run`, four
`not applicable`, one `not run in this execution`, one `partial`, one `failing by design`, and
one that reads `the reason this execution exists`. Thirty-one more are a member of the set with a
qualifier attached. One `implement` entry omits a contract gate outright: WI-0002's opening entry
lists six of the seven and drops `no-unplanned-scope`, which every other `implement` entry in the
engagement lists [src: tracker/items/WI-0002/journal.md:227].

### Every question in the engagement was closed-form and carried the team's own recommendation, and the stakeholder's own channel was never used

All 20 question files have the same five sections, and every one offers between two and four
lettered options and a recommendation — 15 to the human, 5 to the architect, and not one open
question in the set [src: tracker/items/EP-001/questions/Q-001.md;
src: tracker/items/WI-0004/questions/Q-003.md]. None carries `kind: elicitation`; the only
non-`decision` kind used is `sign-off`, three times, all at an ending
[src: EP-001/Q-004; src: EP-001/Q-005; src: EP-001/Q-006]. `tracker/requests/` is empty.

The consequence is a shape, not an incident: the stakeholder was asked fifteen times, and every
time about something the team had already decided was the question. The two things they said that
changed the engagement most — *"if the tool then can't recognise a table it laid out itself,
that's a fault in the tool"* [src: WI-0002/Q-002], which created WI-0003, and *"One thing before
I sign… Markers are for normal cells, not those"* [src: EP-001/Q-005], which created WI-0004 —
both arrived as remainders inside answers to questions about something else.

### A sentence standing on the stakeholder's own words was repaired in place, and no question ever put their two statements to them together

Answering `WI-0002/Q-001` on 2026-08-28T20:18:09Z the stakeholder said *"Whatever the marker
says, that's where the text sits in the cell — every row, every column, no exceptions"*
[src: WI-0002/Q-001]. Three sentences under `docs/` were written on it
[src: docs/product/vision.md:58; src: docs/architecture/adr/ADR-0007-alignment-is-placed-inside-the-cells-field.md:33;
src: docs/architecture/adr/ADR-0010-a-cell-that-contains-a-line-break-ignores-its-columns-marker.md:26].
Answering `EP-001/Q-005` on 2026-08-29T07:18:00Z the same person asked for the exception that
makes the sentence false, and settled its shape at `WI-0004/Q-001`, `Q-002` and `Q-003` twelve
minutes later [src: WI-0004/Q-002].

None of WI-0004's four questions names `WI-0002/Q-001` anywhere in its context, question or
options. What the record shows instead is the second of the two possible moves: `implement`
rewrote the sentence, inside a Definition-of-Done send-back, and declared it —
*"`## What it does` said the alignment markers are honoured 'in every column without exception',
quoting `WI-0002/Q-001`'s 'no exceptions' — and a cell holding a `br` tag is exactly the
exception this item introduced"* [src: tracker/items/WI-0004/journal.md:455]. The document is
correct at v9, the citation still resolves, `lint-claims` passes, and the only evidence that
anything happened is the pair of answers and the edit between them
[src: docs/product/vision.md:234].

**Where it shows in the record:** the two `answered-at` stamps, and the v9 change-log row that
names both.

### The obligation to amend WI-0001's AC12 was recorded by three skills across three executions before any skill filed the question that could discharge it

`plan` found at 18:57:30Z that AC12's two clauses cannot both hold for a degenerate column and
recorded it under `## Assumptions` and `## Risks`
[src: tracker/items/WI-0001/journal.md:369]. `verify` confirmed it at 19:16:18Z and wrote that
the wording is what should be amended [src: tracker/items/WI-0001/journal.md:603].
`review-close` accepted it as a gap at 19:21:09Z and routed the amendment to `answer-questions`
[src: tracker/items/WI-0001/journal.md:752]. Nothing dispatched `answer-questions`, because
nothing had filed a question. The second `verify` pass filed `Q-005` at 19:47:17Z and said why:
*"Four artifacts say AC12's wording must be amended and that the amendment belongs to
`answer-questions`; `answer-questions` runs only when a question is open, and no skill had filed
one. Had this execution passed the item on in silence, the obligation would have died when
`review-close` closed the item"* [src: tracker/items/WI-0001/journal.md:992].

**Where it shows in the record:** `WI-0001/Q-005`, filed fifty minutes and three executions after
the defect was first written down.

### Four criteria counted artefacts of the test suite; the one that named them instead is the only one of the four that never needed amending

`WI-0001 AC12` fixed a column's width by arithmetic that one column cannot satisfy, and was
amended at `WI-0001/Q-005` [src: WI-0001 AC12]. `WI-0002 AC14` required WI-0001's shipped suite
to run *unchanged* while the item necessarily changed two places in it, and its checking clause
was amended at `WI-0002/Q-003` [src: WI-0002 AC14]. `WI-0003 AC9` named *"exactly one"* of 65
tests as changing — measured against a prototype before it was written — and was amended at
`WI-0003/Q-002` to *"exactly two"*, then still passed with an arithmetic slip its own verifier
recorded twice [src: WI-0003 AC9; src: tracker/items/WI-0003/journal.md:402]. `verify` named the
pattern at the third occurrence: *"the fourth criterion in this project to count artefacts and
need reconciling after the fact"* [src: tracker/items/WI-0003/journal.md:560].

`WI-0004 AC5` is the control. `refine` wrote it by naming twenty tests individually rather than
counting them, citing the rule the previous item's review had produced
[src: tracker/items/WI-0004/journal.md:142]. It is the only one of the four that reached `done`
without an amendment [src: WI-0004 AC5].

### An in-place edit turned a sentence in WI-0003's `## Notes` into a heading, and it survived two reviews and the epic's claim audit

Line 204 of the item begins with three hashes followed by a cross-reference to a heading further
down, and then continues as ordinary prose into the next line
[src: tracker/items/WI-0003/item.md:204]. An edit that opened a line with a backticked
cross-reference turned a sentence into a level-three heading; the section it now opens begins
mid-clause, and the heading it points at appears again, correctly, twenty-six lines below.
It was written at 2026-08-28T21:15:20Z, in the execution that added the real heading
[src: tracker/items/WI-0003/journal.md:122]. Two closes of this item walked its notes and the
epic's claim audit read the record again [src: tracker/items/WI-0003/journal.md:611;
src: tracker/items/EP-001/artifacts/review.md:68], and it is still there — a reminder that the
structure of a record is checked by nothing, only its citations and its statuses.

## Positive record

### Two mis-journalled gate verdicts were found and corrected by the record itself, not by anyone auditing it

Both corrections were written by the same skill that made the mistake, minutes later, naming the
wrong value, the right one and the reason both exist
[src: tracker/items/EP-001/journal.md:540; src: tracker/items/EP-001/journal.md:790]. Neither was
found by a program. The append-only rule is what made the correction the only available move —
the wrong entry stands and a later entry says what was wrong — and that is the mechanism working
exactly as `spec/journal-and-history.md` describes it
[src: .claude/agile-skills/spec/journal-and-history.md].

### A verification caught its own mutation harness reporting a clean suite for a mutation it had not applied

*"One `sed`-based mutation silently matched nothing during this execution and reported a clean
suite, which would have been recorded as 'the test is sensitive' when nothing had been changed.
It was caught and re-run; the assertion is now the harness's first act"*
[src: tracker/items/WI-0001/journal.md:996]. The same execution threw away and redid an AC11
check that had passed vacuously because the document it used was never laid out
[src: tracker/items/WI-0001/journal.md:625]. Both are the failure the skill exists to catch,
caught in its own instrument.

### The stakeholder overruled the team's recommendation three times, so the closed-form questions did not steer the answers

`WI-0001/Q-001` was answered with option C against a recommendation of A
[src: tracker/items/WI-0001/journal.md:112]; `WI-0002/Q-002` with option A against a
recommendation of B [src: tracker/items/WI-0002/journal.md:98]; `WI-0004/Q-001` with option C
against a recommendation of B [src: tracker/items/WI-0004/journal.md:99]. Each entry records the
overrule explicitly rather than describing the answer as agreement. Twenty of twenty questions
were answered; none was deferred and none reached the ending open [src: EP-001].

### Every one of the 33 document versions names a skill and an item that has a journal entry

Both change logs were read row by row against the record: `docs/product/vision.md`'s eleven rows
and `docs/architecture/overview.md`'s nine, plus thirteen ADR versions
[src: docs/product/vision.md; src: docs/architecture/overview.md]. Every row's `by` and `for`
pair resolves to an execution with an entry, and every row's timestamp falls inside that
execution's window. There is no version in this workspace that nobody owns.

### The ending was not taken when the record pointed at it

At 2026-08-28T22:29:11Z the stakeholder accepted the engagement and every child was `done` with
`outcome: delivered` [src: EP-001/Q-004]. Nine minutes later the same skill's claim audit found
one false absolute and filed BUG-0001 rather than closing, knowing the cost:
*"Filing the bug knowingly costs a second sign-off, and that is the correct price"*
[src: tracker/items/EP-001/journal.md:326]. `check-epic-signoff` then refused the acceptance
already in hand, because it named three children where there were now four
[src: tracker/items/EP-001/journal.md:417], and the engagement spent two more sign-offs and two
more items before it ended. A gate that refuses an acceptance the team already has is the
expensive kind, and it held.

### Ten things were surfaced to the stakeholder as candidate work and declined, and not one was filed anyway

Five caveats at `Q-004`, three gaps at `Q-005`, two at `Q-006`
[src: tracker/items/EP-001/artifacts/review.md:146]. Each decline was written into the epic's
item and into the product vision rather than left in a question file, with the reason given in
terms: *"A decline that lives in a Q&A file reads, on a later reading, as a gap nobody looked at
— which is exactly the shape that invites a future execution to file the work"*
[src: tracker/items/EP-001/journal.md:291]. No follow-up item exists for any of the ten.

### A rule derived from one item's send-back was carried into the next item's refinement and worked

`review-close` derived on WI-0003 that a criterion should name tests rather than count them;
`refine` applied it on WI-0004 and produced the only criterion of that shape in the engagement
that never needed amending [src: tracker/items/WI-0004/journal.md:142; src: WI-0004 AC5]. The
same round refused to invent a fourth question to check three answers it already had
[src: tracker/items/WI-0004/journal.md:141]. Learning across items is visible in this record and
it is not decoration; it is the counter-case that makes the specimen-shaped remedy in the
observations above legible as a defect rather than as bad luck.

## Proposed toolkit findings

### P-1 — PROPOSED — a claim audit that chooses its own witness chooses one the claim holds for

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** methodology (`review-close`), `spec/dor-dod.md` D12 and DE6
- **Symptom:** D12 and DE6 require every claim in `docs/` to be *"checked by reading it against
  the code"* and say nothing about which case to read it against
  [src: .claude/agile-skills/spec/dor-dod.md]. WI-0002's review recorded the absolute *"no
  column's width depends on its marker"* as holding, on a table whose cells were wide enough that
  the rule making it false never applies
  [src: tracker/items/WI-0002/artifacts/review.md:64]; the epic's termination review found it
  false and filed the engagement's only bug [src: tracker/items/EP-001/journal.md:325].
  BUG-0001's own replacement sentence then repeated the shape, agreed with the item's two
  reproduce commands, and was caught only by a sweep over the degenerate case
  [src: tracker/items/BUG-0001/journal.md:177].
- **Counterfactual:** any engagement whose documents state an absolute over a domain that has a
  degenerate case reaches this. The auditor opens the cited code, picks an example, and a
  representative example is by construction one an absolute holds for; the criterion is satisfied
  by a measurement that could not have failed. Nothing about this project's subject matter is
  load-bearing in that sentence — the same audit passes any quantified claim about any behaviour
  with an edge.
- **Recurrence:** twice in this engagement, both on the same sentence one generation apart —
  WI-0002's review at 2026-08-28T21:03:12Z and BUG-0001's first `implement` pass at
  2026-08-28T22:49:57Z. Caught once, by a boundary sweep, at
  2026-08-28T22:54:49Z [src: tracker/items/BUG-0001/journal.md:192].
- **Direction:** where a claim in `docs/` is *quantified* — `no`, `every`, `always`, `only` — the
  audit records the extreme of the quantifier it was decided against, not merely the artifact it
  cites. The existing `ABSOLUTE_RE` in `scripts/lib/claims.py` already identifies which sentences
  those are; what is missing is that the audit's evidence column must name the witness and say
  why that witness is the hard one.
- **Status:** proposed — not filed. Triage upstream.

### P-2 — PROPOSED — the documents a change invalidates are scheduled by name, so the first one nobody named is the one that fails

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** methodology (`plan`), `spec/dor-dod.md` D7
- **Symptom:** `plan`'s step 8 updates `docs/architecture/overview.md` *"if this change alters the
  shape of the system"*, and its contract's outputs table names no other document
  [src: .claude/skills/plan/references/contract.md]. `docs/product/` is named nowhere in the
  skill's steps or outputs. WI-0003 was rejected on D7 and D12 with both documents stale, and
  `implement` wrote the diagnosis: *"The plan template has no step for updating the documents a
  change invalidates"* [src: tracker/items/WI-0003/journal.md:541]. WI-0004's `plan` acted on
  that finding by writing a step naming `docs/architecture/overview.md`
  [src: tracker/items/WI-0004/journal.md:237], and WI-0004 was rejected on D7 and D12 for
  `docs/product/vision.md` [src: tracker/items/WI-0004/journal.md:399].
- **Counterfactual:** any engagement with more than one standing document under `docs/` reaches
  this. The plan enumerates documents by name; a document no plan step names is scheduled by
  nobody; and the only check that reads the whole document set is a review-stage criterion whose
  remedy is a send-back after implementation and verification are already complete. The subject
  matter is irrelevant — what is load-bearing is that `plan` names one document and D7 governs
  all of them.
- **Recurrence:** two send-backs in this engagement — WI-0003 at 2026-08-28T22:02:29Z and WI-0004
  at 2026-08-29T08:04:33Z — plus the same class filed as a bug at BUG-0001 and two instances
  accepted rather than sent back at WI-0002's close
  [src: tracker/items/WI-0002/journal.md:382]. Four items of five met it.
- **Direction:** `plan` writes a step whose subject is *the set of documents this change makes
  false*, derived rather than listed: every document under `docs/` carrying a claim about the
  behaviour this item touches. The step names the documents it found and states, in the plan,
  that it read all of them — so a document nobody looked at is visible as an absence before
  implementation rather than as a send-back after verification.
- **Status:** proposed — not filed. Triage upstream.

### P-3 — PROPOSED — the journal's gate verdict is free prose and nothing reconciles it with the gate runner's output

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** `scripts/journal-entry` (`check_body`), `scripts/transition`,
  `spec/journal-and-history.md` §2.2
- **Symptom:** `transition` runs the gates, prints a report, and appends the caller's journal body
  without comparing the two; `check_body` requires the `**Gates:**` bullet to be *present* and
  never reads the verdicts under it
  [src: .claude/agile-skills/scripts/journal-entry]. The record was written wrong twice and
  corrected itself twice — `epic-sign-off` journalled `pass` where the program printed FAIL
  [src: tracker/items/EP-001/journal.md:540], and `tests-pass-on-the-merge-result` journalled
  `skipped` where it printed PASS, whose correction states the mechanism outright:
  *"`transition` prints a gate report and appends a journal body, and nothing checks that the two
  agree"* [src: tracker/items/EP-001/journal.md:818]. In the same 474 verdicts, 15 name no member
  of `pass` / `fail` / `skipped`, and one entry omits a contract gate entirely
  [src: tracker/items/WI-0002/journal.md:227].
- **Counterfactual:** any engagement reaches this, because every skill writes its gate bullet from
  what it believes it ran and the tool that actually runs the gates never reads the bullet. The
  two failures found here were caught by an unusually careful reader of its own output; the
  mechanism guarantees that a less careful one is not caught at all. Nothing about the project's
  subject is involved — the defect is in the seam between two scripts.
- **Recurrence:** twice as an outright contradiction (2026-08-29T08:24:41Z and
  2026-08-29T08:37:50Z, both corrected), once as a silently omitted contract gate
  (2026-08-28T20:33:03Z), and fifteen times as a verdict outside the closed set, across all six
  items.
- **Direction:** the transition tool owns the `**Gates:**` bullet the way it already owns
  `**Status:**` — it writes the verdicts from its own gate report and leaves the caller the
  evidence sentence beside each. Where a skill records a gate the tool did not run, the verdict
  word comes from a closed set the body check enforces, and `skipped` carries a reason. This is
  the F-049 move applied to the one bullet where a wrong word is indistinguishable from a check
  that never happened.
- **Status:** proposed — not filed. Triage upstream.

### P-4 — PROPOSED — a criterion that counts artefacts of the test suite is invalidated by the item's own work

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (`refine` step 6a), `spec/dor-dod.md` R4
- **Symptom:** R4 accepts a criterion as decidable when it names an observation, and a count of
  tests is observable, so *"exactly one of its 65 tests changes; all other 64 pass unmodified"*
  passes R4 [src: .claude/agile-skills/spec/dor-dod.md]. `refine` measured that count against a
  prototype before writing it and it was still wrong, because the fixture the item later needed
  broke a second test [src: tracker/items/WI-0003/journal.md:148;
  src: tracker/items/WI-0003/journal.md:272]. It was amended mid-implementation at
  `WI-0003/Q-002` and still carried an arithmetic slip at close
  [src: tracker/items/WI-0003/journal.md:402]. `refine`'s step 6a states the naming rule for a
  criterion whose subject is *other criteria* and not for one whose subject is the suite
  [src: .claude/skills/refine/SKILL.md].
- **Counterfactual:** any engagement whose item necessarily changes part of an existing suite
  reaches this. The number is fixed before the work exists, the work then discovers one more test
  it must touch, and the criterion becomes false through the item doing its job — so it is
  amended after the fact by the one skill permitted to amend it. Nothing about the subject matter
  is load-bearing; what is load-bearing is that a count is checkable and therefore passes R4.
- **Recurrence:** three times in this engagement — `WI-0001 AC12` amended at `WI-0001/Q-005`,
  `WI-0002 AC14` at `WI-0002/Q-003`, `WI-0003 AC9` at `WI-0003/Q-002` — named as a pattern by
  `verify` at the third [src: tracker/items/WI-0003/journal.md:560]. The engagement produced its
  own control: `WI-0004 AC5` names twenty tests individually and needed no amendment
  [src: WI-0004 AC5].
- **Direction:** extend `refine` step 6a from *criteria* to *any artefact of the suite a criterion
  quantifies over*: name the tests, fixtures or documents by identifier and say what must be true
  of each, never how many there are. A count is admissible only as evidence beside the names,
  which is what makes it survive the item discovering one more.
- **Status:** proposed — not filed. Triage upstream.

### P-5 — PROPOSED — an obligation recorded in an artifact has no owner and no dispatch trigger

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (`next` steps 2–6, `answer-questions`), `spec/work-item.md`
- **Symptom:** `next` dispatches on an open request, an open human question, an open architect
  question, a runnable status, or an engagement's state
  [src: .claude/skills/next/SKILL.md]. A finding written into `plan.md`, `review.md` or an item's
  `## Notes` is none of those, so it reaches nobody. Three skills recorded across three
  executions that `WI-0001 AC12` had to be amended and that only `answer-questions` could do it
  [src: tracker/items/WI-0001/journal.md:369; src: tracker/items/WI-0001/journal.md:603;
  src: tracker/items/WI-0001/journal.md:752]; the amendment happened only because a fourth
  execution volunteered a question and said what would otherwise have followed:
  *"Had this execution passed the item on in silence, the obligation would have died when
  `review-close` closed the item"* [src: tracker/items/WI-0001/journal.md:992].
- **Counterfactual:** any engagement in which a skill that may not amend a criterion finds one
  wrong reaches this — `plan`, `implement`, `verify` and `review-close` are all in that position
  by contract. The finding is legible in the artifact and invisible to the orchestrator, and
  whether it is discharged depends on a later execution choosing to file a question nothing
  requires it to file. The subject matter does not enter the sentence.
- **Recurrence:** once as a real delay in this engagement — three executions and fifty minutes on
  `WI-0001 AC12` — and twice more in the same shape where the finder happened to file within its
  own execution (`WI-0002/Q-003`, `WI-0003/Q-002`), which is luck rather than mechanism.
- **Direction:** a recorded obligation that only another skill can discharge is written as an open
  non-blocking question at the moment it is recorded, not as prose in an artifact — the item is
  not held up, and step 4 of the orchestrator already dispatches on exactly that. The skill that
  finds it owns filing it; an accepted gap that names a skill other than the recording one is the
  shape to refuse.
- **Status:** proposed — not filed. Triage upstream.

### P-6 — PROPOSED — every human answer in this engagement was consumed without being read against the answers before it

- **Classification:** observation
- **Severity:** correctness of the record, medium
- **Component:** this engagement's record — the fifteen human-answered questions across EP-001,
  WI-0001, WI-0002, WI-0003 and WI-0004
- **Symptom:** none of the 20 question files carries a `## Cross-answer check` section, and no
  entry in the 77 mentions one. Run against the current toolkit,
  `run: .claude/agile-skills/scripts/lint-answers --context epic → exit 1, 15 errors, all
  answer.cross-check.missing`. The consequence is visible at one place in `docs/`: a sentence
  standing on `WI-0002/Q-001`'s *"no exceptions"* was made false by the same person's later
  request, and it was repaired in place by `implement` inside a Definition-of-Done send-back
  rather than put back to them [src: tracker/items/WI-0004/journal.md:455;
  src: docs/product/vision.md:234]. No question in WI-0004 quotes `WI-0002/Q-001`
  [src: WI-0004/Q-002].
- **Direction:** none is proposed, and that is the finding's substance. The record names
  `answer-questions` v0.3.1 [src: tracker/items/WI-0004/journal.md:86]; the installed contract is
  v0.4.0 and carries a hard `cross-answer-consistency` gate, a required `## Cross-answer check`
  section, and `scripts/lint-answers`, whose own documentation names *this* incident as the case
  it exists for [src: .claude/skills/answer-questions/references/contract.md]. Whether that gate
  would have caught this instance cannot be established from this copy; what can be established
  is that the defect is real, that it is this engagement's, and that the current toolkit already
  carries a remedy aimed at it. Recorded so a triager can confirm the match rather than receive
  it as new.
- **Status:** proposed — not filed. Triage upstream.

### P-7 — PROPOSED — a gate whose command examined nothing was recorded as a pass seven times, and the record said so each time

- **Classification:** observation
- **Severity:** correctness of enforcement, medium
- **Component:** this engagement's record — `claims-are-sourced` as invoked by `implement` and
  `review-close`
- **Symptom:** seven executions recorded the gate as **pass** on
  `lint-claims --changed-since main` reporting zero documents, and an eighth as *"not run"*
  [src: tracker/items/WI-0001/journal.md:566; src: tracker/items/WI-0003/journal.md:483;
  src: tracker/items/EP-001/journal.md:355]. The engagement diagnosed it correctly four separate
  times and had nowhere to send it — *"it is a defect in the contract rather than in this
  engagement — noted again rather than filed, because no item in this project can fix a skill
  contract"* [src: tracker/items/EP-001/artifacts/review.md:92].
- **Direction:** none is proposed. The installed `scripts/lib/scope.py` now models a diff window
  in three states and fails a degenerate one as `claim.scope.degenerate`, and `lint-claims`
  consumes it [src: .claude/agile-skills/scripts/lib/scope.py]. The residual worth a triager's
  attention is not the gate but the latency: this engagement identified the defect at
  2026-08-28T19:10:21Z and the only channel that could export it — this report — did not run
  until the engagement had ended, twenty-four hours and five items later.
- **Status:** proposed — not filed. Triage upstream.

### P-8 — PROPOSED — the stakeholder was never asked anything that was not on the team's agenda

- **Classification:** observation
- **Severity:** methodology gap, low
- **Component:** this engagement's question set — all 20 files across the six items
- **Symptom:** every question is closed-form with two to four lettered options and a
  recommendation, and the only `kind` used besides the default is `sign-off`
  [src: EP-001/Q-001; src: WI-0004/Q-003]. No question carries `kind: elicitation`, and
  `tracker/requests/` holds no request. The two changes of direction the engagement actually took
  both arrived as remainders inside answers to questions about something else
  [src: WI-0002/Q-002; src: EP-001/Q-005], which is what an engagement with no open channel looks
  like from the outside.
- **Direction:** none is proposed. `spec/dor-dod.md` now carries **DE8** — the stakeholder was
  asked at least once an open question that was not about the team's agenda, and it was answered
  — and `spec/question.md` defines `kind: elicitation` for it
  [src: .claude/agile-skills/spec/dor-dod.md]. The epic's termination review walked DE1 to DE7
  and DE8 does not appear in it [src: tracker/items/EP-001/artifacts/review.md:76], which is
  consistent with the record naming `review-close` v0.5.0 against v0.6.0 installed. Recorded as
  the shape a reader of this record should expect to see change, not as a defect of the run.
- **Status:** proposed — not filed. Triage upstream.

### P-9 — PROPOSED — the engagement needed three sign-offs, and two of the three were the system working

- **Classification:** project-circumstance
- **Severity:** methodology gap, low
- **Component:** this project — its stakeholder, and the document audit that ran at its first
  ending
- **Symptom:** `Q-004` accepted an engagement of three children on 2026-08-28T22:29:11Z
  [src: EP-001/Q-004]. Nine minutes later a claim audit filed BUG-0001 and the engagement left
  rest [src: tracker/items/EP-001/journal.md:326]. `Q-005` then declined to accept the
  four-child engagement and named one more behaviour as the condition of signing —
  *"One thing before I sign, though: a cell with a line break or a `<br>` in it should just sit
  top-left, plain"* [src: EP-001/Q-005] — which created WI-0004. `Q-006` accepted all five
  [src: EP-001/Q-006]. Three termination reviews, two extra items, and roughly ten hours of
  engagement time after the first acceptance.
- **Direction:** none for the toolkit. The rule that produced the cost — one acknowledgment per
  rest, and an acceptance covers only what its own sign-off put in front of the person — is the
  one that stopped an engagement closing on an acceptance that named three children where there
  were four [src: tracker/items/EP-001/journal.md:417]. The counterfactual cannot be written
  without naming this stakeholder, who thought of one more requirement at the last gate, and this
  audit, which found a false sentence five minutes after the first acceptance; a different
  engagement with a settled stakeholder and a clean document set signs once. Recorded because it
  is the most expensive thing that happened in this run and because it is not a defect in
  anything.
- **Status:** proposed — not filed. Triage upstream.

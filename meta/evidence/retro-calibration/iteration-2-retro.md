---
engagement: EP-001
ending: E1
written: 2026-08-30T18:48:38Z
items-read: 11
journal-entries-read: 88
proposals: 10
---

# Retrospective — EP-001

## What was read

- **Items:** EP-001, WI-0001, WI-0002, WI-0003, WI-0004, BUG-0001, BUG-0002, BUG-0003,
  BUG-0004, BUG-0005, BUG-0006 — eleven in all. `item.md`, `history.md` and `journal.md` for
  every one, in full. The eleven directories under `tracker/items/` and the ten children the
  epic names agree exactly; nothing exists that the epic does not name and nothing is named
  that does not exist.
- **Journal entries:** 88, across the eleven items, read end to end rather than by heading.
- **History rows:** 88, one per journal entry
  [src: run: grep -h '^| 2026' tracker/items/*/history.md | wc -l → 88].
- **Questions:** 19 files across six items — the six on EP-001 including both sign-offs, two on
  WI-0001, two on WI-0002, three on WI-0003, one on WI-0004, two on BUG-0002, two on BUG-0004
  and one on BUG-0005. Eleven were addressed to the human, eight to the architect.
- **Artifacts:** all 45 files under `tracker/items/*/artifacts/` — every `plan.md`,
  `impl-report.md`, `verify-report.md`, `review.md` and `refinement-qa.md`, plus the epic's own
  `review.md`.
- **Documents:** `docs/product/vision.md` v9, `docs/architecture/overview.md` v11, and
  ADR-0001 through ADR-0014, including all 46 change-log rows, each matched against the
  execution its `by` and `for` name.
- **Contracts and specs:** the installed contracts for `intake`, `refine`, `plan`, `implement`,
  `verify`, `review-close`, `answer-questions` and `next`, and
  `.claude/agile-skills/spec/` — `journal-and-history.md`, `question.md`, `dor-dod.md`,
  `doc-header.md`, `ids-and-statuses.md`, `work-item.md`, `workspace-layout.md`, `retro.md`.
  Also `scripts/check-commit-refs`, `scripts/validate-workspace`, `scripts/lint-retro` and
  `scripts/lib/claims.py`, where a gate's behaviour had to be checked rather than assumed.
- **Requests:** `tracker/requests/` holds only `.gitkeep`; the stakeholder-initiated channel was
  never used [src: run: ls -A tracker/requests → .gitkeep].

**Not available:**

- **The product's source tree.** This is a banked copy of the record and `tidy/`, `tests/` and
  `README.md` were not kept with it [src: RECORD-NOTICE.md]. Every claim the engagement made
  *about* the code therefore had to be read from the record's own transcripts rather than
  re-checked against the code, and no citation in this report names a source file. What that
  cost the reading: the one thing this retro cannot do is what `review-close`'s D12 did twelve
  times — open what a sentence cites and decide from what is there.
- **The commit history.** `git` does not work in this copy, so nothing here is drawn from
  commit times, commit messages or shas. Timings are read from record timestamps only, and the
  merge shas the record quotes are taken as recorded rather than verified.

**Gate results for this execution:**

- `engagement-has-ended` → **pass**
  [src: run: .claude/agile-skills/scripts/engagement-state EP-001 → exit 0, EP-001 ended, rest reached at 2026-08-28T15:41:23Z].
- `workspace-valid` → **fail**, for the reason the notice names and no other
  [src: run: .claude/agile-skills/scripts/validate-workspace → exit 1, 181 errors, 0 warnings].
  All 181 are `claim.citation.unresolved`; 179 of them name a file in the absent source tree
  (`tidy/cli.py` 56 times, `tidy/planner.py` 29, `README.md` 28, and so on). The remaining two
  are a citation form the current resolver refuses,
  `tracker/items/WI-0002/questions/Q-001.md:114` and the same line of `Q-002.md`, which write
  an item ID followed by a section name. Whether that form resolved under the resolver in force
  during the engagement is unknown — `validate-workspace` reported zero errors at every point
  the record records — so it is noted rather than counted against the work.
- `retro-report-is-well-formed`, `scope-was-not-degenerate`, `the-record-was-not-touched` — see
  the journal entry accompanying this report.

---

## Engagement retrospective

### The opening entry of an `implement` execution was written eleven times and three different ways

`implement` makes two transitions and writes two entries, and its contract has one gate list.
Nothing says what the first entry records, because at that point none of its gates can have
run. The eleven opening entries settled it eleven times: six say `**skipped**` or
`**not yet run**` for the same six gates, one says `**not run**`, and across the whole record 44
of 540 gate lines carry a verdict that is not one of the three
`spec/journal-and-history.md` §2.2 admits
[src: run: grep -rho '\*\*not yet run\*\*' tracker/items/*/journal.md | wc -l → 40]
[src: tracker/items/WI-0001/journal.md; src: tracker/items/WI-0002/journal.md].

The split is not random. Every one of the six bug items lists the advisory gate
`no-unplanned-scope` in its opening entry; not one of the five work-item entries does
[src: tracker/items/WI-0003/journal.md; src: tracker/items/BUG-0004/journal.md]. The rule that
a contract gate must appear even when skipped is the one §2.2 says the format exists to
enforce, and it is the one that drifted.

**Where it shows in the record:** the eleven `implement` opening entries; and
`validate-workspace`, whose `journal.bullet.missing` check tests that the `**Gates:**` label
exists and never reads what is under it, while its own hint says "a declared gate that is
silently omitted is the failure this format exists to prevent"
[src: .claude/agile-skills/scripts/validate-workspace].

### A hard gate was recorded as failed on a move that then proceeded

WI-0001's suspension entry records `commits-reference-the-item` → **fail, not blocking**,
because the branch carried no commits and `main..wi/WI-0001` was empty; the item moved to
`awaiting-answer` anyway [src: tracker/items/WI-0001/journal.md:437]. The contract's `on
failure` for that gate is `stay`. The move was legitimate — `transition` gates only a skill's
completion move — but the entry has no vocabulary for "a hard gate that failed on a move this
skill is not gated on", so it invented one.

The same empty range produced two opposite readings elsewhere in the record. BUG-0003 and
BUG-0004 call it a "false failure" and predict its recurrence
[src: tracker/items/BUG-0003/journal.md; src: tracker/items/BUG-0004/journal.md]; BUG-0005
calls the same event a failure "correctly and unavoidably"
[src: tracker/items/BUG-0005/journal.md]. Both readings are defensible and the record contains
both, which is the finding.

### A skill filing an item during another item's execution recorded its gates five different ways

Six items were created mid-execution by a skill other than `intake`. `verify` recorded its own
`every-criterion-independently-checked` gate as **pass** on BUG-0001 and BUG-0002 — evidenced
against the criteria of the item it was *verifying*, not the item it was filing
[src: tracker/items/BUG-0001/journal.md; src: tracker/items/BUG-0002/journal.md] — and as
**skipped** on BUG-0003 and BUG-0004, on the reasoning that the new item's criteria are unmet by
construction [src: tracker/items/BUG-0003/journal.md; src: tracker/items/BUG-0004/journal.md].
`review-close` recorded RB1–RB5, the bug Definition of Ready, in place of its own eight
contract gates on BUG-0005 [src: tracker/items/BUG-0005/journal.md], and on BUG-0006 named all
eight in prose and pointed at the entry where they were evaluated
[src: tracker/items/BUG-0006/journal.md]. `answer-questions` did the same on WI-0004, plus two
of its six [src: tracker/items/WI-0004/journal.md].

Five treatments, three skills, one situation. None is dishonest; each was reasoned about in the
entry that used it.

### The stakeholder was offered an ending the status model could not deliver, and paid for it with a second sign-off

`EP-001/Q-005`'s option B — the option `spec/question.md` §2 requires a sign-off to offer —
told the stakeholder that accepting with a named follow-up meant "the engagement still closes
as delivered, and the new work is opened" [src: EP-001/Q-005]. They chose it. Half of it was
not executable: an engagement ends only from rest, rest requires every child terminal, and the
follow-up item is created at `draft` [src: .claude/agile-skills/spec/ids-and-statuses.md;
src: tracker/items/EP-001/journal.md]. The epic returned to `open`, WI-0004 ran, and a second
sign-off was filed 90 minutes later [src: EP-001/Q-006].

The record handled it as well as it could: `answer-questions` wrote the discrepancy into the
question's own `## Consequences` and into the epic's `## Notes` rather than quietly resolving
it, and `review-close` rewrote option B correctly in `Q-006`. But the correction lives in one
question file of one engagement.

**Where it shows in the record:** `EP-001/Q-005` `## Options considered` against `## Consequences`;
`EP-001/Q-006` option B, which reads "the epic stays `open` until that work is finished and you
are asked again".

### Thirty-eight decisions were taken under a delegation about the language and the delivery order, and one of them reached the stakeholder

Two intake answers delegated a choice — *"Whatever's easiest for you to build and test"*
[src: EP-001/Q-001] and *"whichever's easier for you"* [src: EP-001/Q-004]. `refine` read them
as standing deferrals over a category and decided under them: preview-by-default, the
seven-folder extension table, what happens to an unrecognised file, whether hidden files are
tidied, which timestamp measures age, which side of a boundary a file falls, where the config
file lives, and whether a broken rule file at that location stops the run
[src: tracker/items/WI-0001/artifacts/refinement-qa.md;
src: tracker/items/WI-0004/artifacts/refinement-qa.md]. The four `refinement-qa.md` files carry
38 `[assumed]` markers between them.

Every one was recorded, tagged, and carried into the item's `## Notes` — the protocol was
followed exactly. What nothing in the toolkit does is bound the delegation's reach or route any
of the resulting assumptions back to the person who delegated. Exactly one ever did: the
refusal of an unusable default rule file, because `review-close` chose to put it in the second
sign-off, where the stakeholder confirmed it in their own words [src: EP-001/Q-006;
src: tracker/items/WI-0004/item.md]. WI-0001's plan named the exposure at the time: "Five
assumptions are load-bearing and none was confirmed by the stakeholder"
[src: tracker/items/WI-0001/artifacts/plan.md].

### Six closes recorded the merge they created in three different places, three of them by editing the entry after it was stamped

`check-commit-refs` reads `main..branch`, which merging empties, so the item must close before
it merges — and the journal entry that reports the close is therefore written before the merge
exists. WI-0003, BUG-0004 and BUG-0005 each filled the sha into the already-stamped entry and
declared the edit inside it: *"the sha was filled into this bullet after the merge, which is the
only thing in this entry not true at the moment the entry was stamped"*
[src: tracker/items/WI-0003/journal.md:514; src: tracker/items/BUG-0004/journal.md:432;
src: tracker/items/BUG-0005/journal.md:374]. BUG-0002 used a follow-up commit on the trunk
instead [src: tracker/items/BUG-0002/journal.md]; BUG-0001 and BUG-0003 put the sha in
`review.md` [src: tracker/items/BUG-0001/artifacts/review.md].

A seventh entry was edited for a different reason and said so: BUG-0001's close corrected its
own `epic-sign-off` verdict from `skipped` to `pass` in place, on the grounds that recording
`skipped` for a gate that ran would misdescribe the execution
[src: tracker/items/BUG-0001/journal.md:403]. `spec/journal-and-history.md` permits exactly one
in-place edit, a restamped `when`, and this is not it.

### Two acceptance criteria were built against premises an unrelated merge falsified between filing and building

BUG-0006 was filed at a moment when two of the citations it names were exact, and its AC2 says
so — "the latter two are exact and must stay so" [src: BUG-0006 AC2]. WI-0003's merge, 57
minutes later, moved both by twenty-one lines. `plan`, `verify` and `review-close` each
recorded the departure with the evidence rather than quietly satisfying the criterion, and
`review-close` upheld it [src: tracker/items/BUG-0006/journal.md]. AC3's literal "version: 2"
had become unsatisfiable the same way, and satisfying it would have violated the
`spec/doc-header.md` §3 that AC3 itself invokes
[src: tracker/items/BUG-0006/artifacts/verify-report.md].

Nothing in the toolkit noticed. A criterion is frozen at `ready` and nothing re-reads it when
the world it describes moves; the three skills that met it did the right thing by hand.

### The engagement asked the stakeholder eleven questions and never asked what they had not been asked

Eleven questions went to the human across four items and the epic, every one closed-form and
every one from the team's own agenda [src: EP-001/Q-002; src: WI-0002/Q-001;
src: WI-0004/Q-001]. `tracker/requests/`, the one channel that does not begin with a skill
asking, was never used and nothing in the record shows the stakeholder being told it exists
[src: run: ls -A tracker/requests → .gitkeep].

Under the rules in force during the engagement this was complete. Under the installed rules it
is not: `kind: elicitation` and Definition of Done DE8 were added on 2026-08-29
[src: .claude/agile-skills/spec/question.md; src: .claude/agile-skills/spec/dor-dod.md], the day
after the engagement ended. The observation is not that the engagement missed a rule; it is
that the record is a clean example of the gap that rule was written for, and it is silent about
whether anything was lost.

### One of forty-six document version rows names an execution that was not running when it was stamped

Every change-log row in `docs/` names a skill, an item and a time, and forty-five of the
forty-six fall inside an execution of that skill on that item. The exception is
`docs/architecture/overview.md` v9, attributed to `implement` on WI-0003 at 22:05:00Z
[src: docs/architecture/overview.md]. `implement`'s two entries on WI-0003 are stamped
21:42:51Z and 21:53:03Z, and the closing one lists overview v9 among its artifacts
[src: tracker/items/WI-0003/journal.md]. At 22:05:00Z the item was at `awaiting-answer` and
`review-close` had suspended it a minute earlier [src: tracker/items/WI-0003/history.md].

`validate-workspace`'s `doc.updated` check tests the field's format and its ceiling and nothing
else [src: .claude/agile-skills/scripts/validate-workspace], so the row is the one self-reported
field in the record with no machine behind it and no comparison against the executions it
names.

### The one gate that repeatedly caught something is the one no program runs

Twelve document defects were caught in this engagement, every one by D12's read — the reviewer
opening what a sentence cites rather than reading the sentence: three at WI-0001's close, two at
BUG-0002's, one at BUG-0003's, two at BUG-0004's, one at WI-0003's, one at BUG-0005's and two
at WI-0004's [src: tracker/items/WI-0001/artifacts/review.md;
src: tracker/items/BUG-0004/artifacts/review.md; src: tracker/items/WI-0004/artifacts/review.md].
`lint-claims` exited 0 across every one of them, and three reviews said so in as many words:
*"it passed while both claims were false, and it passes now that they are true. It checks that
citations resolve, never that they support the sentence"*
[src: tracker/items/BUG-0002/journal.md].

That is the division of labour working. It is recorded here because it is also the engagement's
largest single dependency on a human-style read, and the thing a later reader should know
before trusting any automated claim gate.

---

## Positive record

### The record is complete: 88 executions, 88 journal entries, 88 history rows, no gap on any of eleven items

Every history row has a matching journal entry and every entry a matching row
[src: run: grep -h '^| 2026' tracker/items/*/history.md | wc -l → 88]. Every entry carries the
ten bullets `spec/journal-and-history.md` §2.2 requires, and every heading names a skill, a
version and a persona [src: tracker/items/EP-001/journal.md]. Four items were suspended and
resumed and every one returned to the `resume-to` its own suspending row recorded, read from
the row rather than inferred from which skill asked [src: tracker/items/BUG-0004/journal.md].

### Verification was independent enough to catch two implementation reports in a false claim

`verify` built its own fixtures from the item's own words rather than from the project's test
helpers, and it caught what that buys twice. On WI-0002 it found that
`impl-report.md`'s claim about a specific mutation was untrue — rewording the README sentence a
user reads leaves the suite green, because the assertion is a whole-file substring and the
phrase occurs three times [src: tracker/items/WI-0002/artifacts/verify-report.md]. `review-close`
reproduced it rather than taking the report's word
[src: tracker/items/WI-0002/artifacts/review.md]. On BUG-0006 it corrected the implementation
report in the item's favour, on evidence the report had not gathered
[src: tracker/items/BUG-0006/journal.md].

### Every gap accepted at review was copied out of the report and onto the item

Six reviews accepted gaps rather than sending work back, and every one wrote them into the
item's `## Notes` with the same reason: a gap recorded only in a verification report stops being
read the moment the item closes. Five on WI-0001, nine on WI-0002, eight on WI-0003, seven on
BUG-0001, six on BUG-0003, five on BUG-0005, three on WI-0004
[src: tracker/items/WI-0001/artifacts/review.md; src: tracker/items/WI-0002/artifacts/review.md;
src: tracker/items/BUG-0001/artifacts/review.md].

### The refusals held: four skills stopped at the edge of their authority rather than fixing what they found

`implement` filed two questions and wrote no code rather than guess a decision the plan had not
taken [src: WI-0001/Q-002]. `review-close` suspended three items rather than edit an ADR it may
not edit [src: BUG-0002/Q-001; src: BUG-0004/Q-002; src: BUG-0005/Q-001]. `answer-questions`
declined to close an epic when the answer plainly implied the ending, because recording an
outcome is `review-close`'s move [src: tracker/items/EP-001/journal.md]. `implement` on WI-0002
left a user-visible stale `--help` string alone because the plan put `cli.py` out of scope, and
declared it instead — which is how BUG-0003 came to exist
[src: tracker/items/WI-0002/artifacts/impl-report.md].

### Six of the ten delivered items are defects the pipeline found in its own work

BUG-0001 through BUG-0006 were filed by `verify` and `review-close` against work the pipeline
had just produced, and every one was found by exercising an edge a previous stage had
*declared* rather than by chance: WI-0001's plan named the hard-link fallback as the one place
a criterion rests on untestable code, and BUG-0002 is that
[src: tracker/items/WI-0001/artifacts/plan.md]; its implementation report named the unreadable
folder as a candidate bug item, and BUG-0001 is that
[src: tracker/items/WI-0001/artifacts/impl-report.md]; WI-0002's report named the stale help
text and recommended the item, and BUG-0003 is that
[src: tracker/items/WI-0002/artifacts/impl-report.md]. The declaring habit is what made the
finding cheap.

### Both sign-offs showed the stakeholder the tool running rather than a list of closed tickets

`Q-005` quotes five real runs made at the moment of asking — a preview leaving the folder
unchanged, an apply matching it, a subfolder untouched, the never-overwrite suffix, and a
rule-file error in one line — and `Q-006` does the same for the tenth item, saying out loud
that its transcripts point at a scratch config directory rather than a real home
[src: EP-001/Q-005; src: EP-001/Q-006]. Both name every child by ID with a verdict, and both
put the accepted gaps in front of the stakeholder as named options rather than leaving them in
a closed item's report [src: tracker/items/EP-001/journal.md].

### The engagement's own toolkit observation is in the installed script today

BUG-0003's implementation report proposed one condition to fix `check-commit-refs`' empty-range
misdiagnosis: *"when the branch head equals the trunk head, say 'no commits yet' instead"*
[src: tracker/items/BUG-0003/artifacts/impl-report.md]. The installed script now carries exactly
that branch, with a comment citing F-035 as its reason
[src: .claude/agile-skills/scripts/check-commit-refs]. What remains is the failure itself, not
the message — see P-1.

---

## Proposed toolkit findings

### P-1 — PROPOSED — a skill that makes two transitions has one gate list, and nothing says what its first entry records

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`implement`), `spec/journal-and-history.md` §2.2,
  `scripts/validate-workspace`
- **Symptom:** `implement`'s SKILL.md requires an opening journal entry at the move to
  `in-progress`, "`**Gates:**` recording that the completion gates have not run yet"
  [src: .claude/skills/implement/SKILL.md], while
  `spec/journal-and-history.md` §2.2 admits only `pass`, `fail` and `skipped`. Across eleven
  opening entries the record used three vocabularies — `skipped`, `not yet run`, `not run` —
  and 44 of its 540 gate lines carry a verdict outside the three
  [src: run: grep -rho '\*\*not yet run\*\*' tracker/items/*/journal.md | wc -l → 40]. The
  advisory gate `no-unplanned-scope` appears in all six bug items' opening entries and in none
  of the five work items'
  [src: tracker/items/BUG-0004/journal.md; src: tracker/items/WI-0003/journal.md]. One hard
  gate, `commits-reference-the-item`, is recorded as **fail, not blocking** on a move that
  proceeded [src: tracker/items/WI-0001/journal.md:437] — it fails at the opening transition of
  every `implement` execution, because the branch it inspects has no commits yet. Nothing
  reports any of this: `validate-workspace`'s `journal.bullet.missing` tests that the
  `**Gates:**` label exists and never compares its contents with the acting skill's contract,
  though its hint claims that is what it prevents
  [src: .claude/agile-skills/scripts/validate-workspace].
- **Counterfactual:** any engagement that runs `implement` reaches this, twice per item. The
  first entry is required by the skill, its gates cannot have run, the journal format offers no
  word for that, and a hard gate that reads a commit range must fail on an empty one. Nothing
  about a file-organising tool is load-bearing in that sentence.
- **Recurrence:** eleven times in this engagement, once per `implement` execution, plus five
  further entries in which a `review-close` or `answer-questions` execution had the same problem
  and solved it differently.
- **Direction:** give the format a fourth verdict for a gate that will run later in the same
  execution, and make the check that reads the `**Gates:**` bullet compare its gate names against
  the contract of the skill in the heading rather than only testing that the label is present.
  Separately, decide whether a gate that cannot hold at a skill's opening transition belongs in
  that entry at all.
- **Status:** proposed — not filed. Triage upstream.

### P-2 — PROPOSED — a `path:line` citation resolves for ever, whatever is at the line

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** `spec/doc-header.md` §4a, `scripts/lib/claims.py`, `scripts/lint-claims`
- **Symptom:** §4a lists a workspace-path citation written as `src/store.py:42`, which "resolves
  when the file exists in the workspace"
  [src: .claude/agile-skills/spec/doc-header.md:245], and the resolver takes everything before
  the first colon as the path [src: .claude/agile-skills/scripts/lib/claims.py]. So a line
  number is never checked. BUG-0006 was filed because an ADR cited a blank line for a claim
  whose statement had moved [src: BUG-0006]; planning for it found that **all three** surviving
  `path:line` citations in `docs/` pointed at lines that do not support their sentences, and
  that two of them had drifted twenty-one lines under an unrelated merge before the item was
  touched [src: tracker/items/BUG-0006/artifacts/plan.md]. `lint-claims` exited 0 throughout
  [src: tracker/items/BUG-0006/journal.md]. The same class had already been met once, one ADR
  earlier [src: BUG-0004/Q-002].
- **Counterfactual:** any engagement whose documents cite code by line reaches this. The
  citation resolves whatever the file now contains, while `dor-dod.md` D12's own procedure tells
  a reviewer to open what a sentence cites and decide from what is there — so the gate says yes
  and the procedure lands the reader on the wrong line. Nothing about this project's subject
  matter is in that sentence.
- **Recurrence:** three citations in this engagement, across two ADRs, found twice — once as
  BUG-0004/Q-002 and once as the whole of BUG-0006.
- **Direction:** either drop `path:line` from §4a's forms so the convention matches what the
  gate can decide, or make the resolver check that the cited line is non-blank and contains a
  token the citing sentence names. The engagement settled it locally as ADR-0013 — citations
  name a file and the prose names the symbol — which binds one project and nothing else
  [src: ADR-0013].
- **Status:** proposed — not filed. Triage upstream.

### P-3 — PROPOSED — the sign-off's required option B promises an ending the status model forbids

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`review-close`), `spec/question.md` §2 (`kind: sign-off`),
  `spec/ids-and-statuses.md` §3.5
- **Symptom:** §2 requires a sign-off to offer "accept with named follow-up items"
  [src: .claude/agile-skills/spec/question.md]. Written out, that option told the stakeholder
  "the engagement still closes as delivered, and the new work is opened" [src: EP-001/Q-005].
  They took it. Opening the follow-up item at `draft` destroys rest, and an engagement ends only
  from rest, so only the second half was executable; the epic returned to `open` and a second
  sign-off followed 90 minutes later [src: tracker/items/EP-001/journal.md; src: EP-001/Q-006].
  The engagement recorded the discrepancy rather than hiding it, and wrote the option correctly
  by hand the second time — where nothing carries it forward.
- **Counterfactual:** any engagement whose stakeholder takes the option the protocol obliges it
  to offer reaches this, because creating the item the option describes is what makes the ending
  it promises unreachable. The subject matter of the work is irrelevant to the argument.
- **Recurrence:** once, at `EP-001/Q-005`; corrected locally in `EP-001/Q-006`'s own wording.
- **Direction:** the option's consequence line should say what actually happens — the epic stays
  `open`, the follow-up is built like any other item, and a fresh sign-off is due at the next
  rest — either in the spec's own description of option B or in whatever `review-close` uses to
  compose it. The stakeholder should not learn the mechanics after they have chosen.
- **Status:** proposed — not filed. Triage upstream.

### P-4 — PROPOSED — the close-before-merge order leaves the merge unrecordable in the entry that reports it

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`review-close`), `spec/journal-and-history.md`,
  `scripts/check-commit-refs`
- **Symptom:** `check-commit-refs` inspects `main..branch`, which merging empties, so the close
  must precede the merge — every review in this engagement says so
  [src: tracker/items/WI-0002/artifacts/review.md]. The closing journal entry is therefore
  written before the merge exists, and the journal is append-only with exactly one sanctioned
  in-place edit, a restamped `when`
  [src: .claude/agile-skills/spec/journal-and-history.md]. Six closes solved this three ways:
  three edited the stamped entry to fill in the sha and declared the edit inside it
  [src: tracker/items/WI-0003/journal.md:514; src: tracker/items/BUG-0004/journal.md:432;
  src: tracker/items/BUG-0005/journal.md:374], one used a follow-up commit on the trunk
  [src: tracker/items/BUG-0002/journal.md], and two put the sha in `review.md` instead
  [src: tracker/items/BUG-0001/artifacts/review.md].
- **Counterfactual:** any engagement that closes any item on a branch reaches this. The gate's
  ordering requirement and the record's append-only rule are both correct and they are jointly
  unsatisfiable for one field. Nothing about the product being built enters the argument.
- **Recurrence:** six closes, three different workarounds, three entries edited after stamping.
- **Direction:** give the record a sanctioned place for a fact created after the entry — a
  second, tiny entry appended after the merge, or a named field the transition tool fills in on a
  later invocation — so that the honest answer is not "edit the entry and say so".
- **Status:** proposed — not filed. Triage upstream.

### P-5 — PROPOSED — a standing delegation has unbounded scope and no route back to the person who gave it

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (`refine`, `review-close`), `spec/question.md` §1,
  `spec/dor-dod.md` R8
- **Symptom:** two stakeholder answers about the implementation language and the delivery order
  [src: EP-001/Q-001; src: EP-001/Q-004] were read as standing deferrals over a whole category,
  and 38 `[assumed]` decisions were taken under them across four items
  [src: tracker/items/WI-0001/artifacts/refinement-qa.md;
  src: tracker/items/WI-0003/artifacts/refinement-qa.md]. Several carry real product weight —
  what happens to a file the tool does not recognise, whether hidden files are tidied, whether a
  broken rule file stops every run [src: WI-0001 AC5; src: WI-0004 AC2]. All 38 were recorded,
  tagged and carried into `## Notes`; the protocol was followed exactly. Exactly one reached the
  stakeholder, and it did so because a reviewer chose to put it in a sign-off
  [src: EP-001/Q-006]. `refine`'s own plan named the exposure at the time: "Five assumptions are
  load-bearing and none was confirmed by the stakeholder"
  [src: tracker/items/WI-0001/artifacts/plan.md].
- **Counterfactual:** any engagement whose stakeholder answers one question with "whichever is
  easier for you" hands every later `refine` execution a licence nothing bounds. The Definition
  of Ready records an assumption and the sign-off template names children and accepted gaps;
  neither surfaces the assumptions, and no rule says how far a category delegation reaches.
  Nothing about tidying folders is load-bearing.
- **Recurrence:** four refinement rounds across four items, 38 assumption markers, one surfaced.
- **Direction:** two halves. Make a delegation's scope something the answer records rather than
  something each later execution re-derives — the skill that consumes it writes down what
  category it takes the answer to cover. And give the sign-off a place for the assumptions taken
  under it, alongside the children and the accepted gaps, so that surfacing one is the default
  rather than a reviewer's initiative.
- **Status:** proposed — not filed. Triage upstream.

### P-6 — PROPOSED — `review-close`'s recorded step order fails its own `workspace-valid` gate

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, low
- **Component:** methodology (`review-close`), `scripts/validate-workspace`
  (`item.outcome.premature`)
- **Symptom:** WI-0003's close records that `outcome: delivered` had to be written **after** the
  transition rather than before it, because `item.outcome.premature` is not among the codes
  `validate-workspace --resolving` downgrades — "so setting the outcome first, which is the
  order `review-close`'s step 9 reads as, fails the `workspace-valid` hard gate on the very move
  that would make it true" [src: tracker/items/WI-0003/journal.md:513]. The execution complied
  and said so; the five other closes are silent about which order they used.
- **Counterfactual:** any engagement closing any item meets it, because the outcome and the
  status change together and one of the two orders is refused by a hard gate every skill runs.
  The product is irrelevant.
- **Recurrence:** recorded once, at WI-0003; the other five closes do not say, which is itself
  the reason to fix the instruction rather than the execution.
- **Direction:** either make the procedure state the order explicitly, or add
  `item.outcome.premature` to the codes `--resolving` downgrades for the move that resolves it.
  The skill should not have to discover that its own written order is illegal.
- **Status:** proposed — not filed. Triage upstream.

### P-7 — PROPOSED — a document's version row is a self-reported field with nothing behind it

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, low
- **Component:** `spec/doc-header.md` §3, `spec/journal-and-history.md` §0,
  `scripts/validate-workspace` (`doc.updated`)
- **Symptom:** §0 requires a journal entry's timestamp, skill and persona to come from a machine,
  because those were the fields real runs invented
  [src: .claude/agile-skills/spec/journal-and-history.md]. The rule was never extended to a
  document's `updated` field or its change-log `when`, `by` and `for`, which carry the same
  claim about the same things. Forty-five of this record's forty-six version rows fall inside an
  execution of the skill and item they name; `docs/architecture/overview.md` v9 is attributed to
  `implement` on WI-0003 at 22:05:00Z [src: docs/architecture/overview.md], twelve minutes after
  that execution's closing entry and while the item sat at `awaiting-answer`
  [src: tracker/items/WI-0003/journal.md; src: tracker/items/WI-0003/history.md].
  `validate-workspace` checks the field's format and its ceiling and never compares it against
  the executions [src: .claude/agile-skills/scripts/validate-workspace].
- **Counterfactual:** any engagement reaches it, because a change-log row is typed by the same
  worker whose journal heading the toolkit already refuses to let them type. The check that
  would catch it — is there an execution of this skill on this item around this time — needs
  only the tracker.
- **Recurrence:** once in forty-six rows in this engagement. Low, and that is the honest number:
  the discipline held forty-five times without anything checking it.
- **Direction:** extend §0's rule to document headers, and have `validate-workspace` match each
  change-log row against the journal of the item it names, reporting a row whose actor was not
  executing then.
- **Status:** proposed — not filed. Triage upstream.

### P-8 — PROPOSED — an exactly-on-the-boundary criterion cannot be settled through this product's own interface

- **Classification:** project-circumstance
- **Severity:** methodology gap, low
- **Component:** this project — `tidy`'s age bands and its once-per-run clock (ADR-0005), and
  the criteria written against them
- **Symptom:** WI-0002 AC4 pins the behaviour of a file whose age is exactly the boundary
  [src: WI-0002 AC4], and no folder fixture can produce one: the planner reads its own clock, so
  a file set to exactly 365 days old is fractionally older by the time the run measures it.
  Verification settled the exact point by calling the lookup directly and recorded both
  measurements rather than passing the folder case off as exact
  [src: tracker/items/WI-0002/artifacts/verify-report.md]. WI-0003 AC5 met the same wall with a
  user-supplied 90-day boundary [src: WI-0003 AC5;
  src: tracker/items/WI-0003/artifacts/impl-report.md].
- **Counterfactual:** it cannot be written without this product. A different engagement reaches
  it only if its own subject has a clock-relative boundary a fixture cannot pin, and most do
  not. This is `tidy`'s difficulty, not the toolkit's — the criteria were decidable, and what
  they needed was two observations instead of one.
- **Direction:** for this project, keep the value-level check beside the folder-level one and
  say so in the criterion itself, as WI-0003's criteria already do, so a verifier is not left to
  discover that the exact case is unreachable.
- **Status:** proposed — not filed. Triage upstream.

### P-9 — PROPOSED — this product's safety guarantee rests on a filesystem primitive its tests cannot exercise

- **Classification:** project-circumstance
- **Severity:** correctness of enforcement, medium
- **Component:** this project — ADR-0003's `os.link` move and its fallback, and WI-0001 AC9
- **Symptom:** the never-overwrite promise is the stakeholder's one stated hard constraint
  [src: EP-001/Q-002], and it is kernel-enforced only on the primary path; the fallback for
  filesystems that refuse hard links is a check-then-act, and no test in the project reaches it
  without patching the call. WI-0001's plan named it as "the one place where a criterion (AC9)
  rests on code that automated tests do not reach"
  [src: tracker/items/WI-0001/artifacts/plan.md; WI-0001 AC5]; verification confirmed it and
  filed BUG-0002 from it [src: tracker/items/WI-0001/artifacts/verify-report.md], and both later
  reports state that what was proven is the branch's behaviour given an injected error rather
  than any real filesystem's [src: tracker/items/BUG-0002/artifacts/verify-report.md].
- **Counterfactual:** it cannot be written without `os.link`, exFAT and this product's promise.
  A different engagement hits it only if its own guarantee happens to rest on a primitive its
  environment cannot withhold.
- **Direction:** for this project, the accepted gap is recorded in three places and that is the
  right handling; if it ever matters, the answer is an environment that can provide such a
  volume, not another test.
- **Status:** proposed — not filed. Triage upstream.

### P-10 — PROPOSED — this record predates two rules the installed toolkit would now refuse it under

- **Classification:** observation
- **Severity:** doc error, low
- **Component:** `spec/question.md` revisions 7 and 8, `spec/dor-dod.md` revision 6 — read
  against this record
- **Symptom:** run against the installed toolkit, the ended engagement fails two gates it passed
  at the time. `check-epic-signoff` refuses it for having asked the stakeholder no open question
  [src: run: .claude/agile-skills/scripts/check-epic-signoff EP-001 → exit 1, Definition of Done DE8],
  and `lint-answers` reports four consumed human answers with no `## Cross-answer check` section
  [src: run: .claude/agile-skills/scripts/lint-answers --item EP-001 → exit 1, 4 errors];
  no file anywhere in the workspace contains that section
  [src: run: grep -rl "Cross-answer check" tracker → exit 1, no output]. Both rules are dated
  2026-08-29 [src: .claude/agile-skills/spec/question.md;
  src: .claude/agile-skills/spec/dor-dod.md], the day after the engagement ended on 2026-08-28
  [src: tracker/items/EP-001/history.md].
- **Direction:** none, and that is the point of recording it. A triager reading the nine
  proposals above should know that two of the toolkit's newest rules would have bitten this
  record, and that neither absence is a failure of the engagement. It is also a small piece of
  evidence for those rules: an engagement that did everything the protocol asked still put
  eleven closed-form questions to its stakeholder and never once asked what they had not been
  asked.
- **Status:** proposed — not filed. Triage upstream.

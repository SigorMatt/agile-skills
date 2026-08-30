---
engagement: EP-001
ending: E1
written: 2026-08-30T18:43:52Z
items-read: 4
journal-entries-read: 37
proposals: 6
---

# Retrospective — EP-001

## What was read

- **Items:** EP-001, WI-0001, WI-0002, WI-0003 — `item.md`, `history.md` and `journal.md` for
  each, in full. Four items; the epic names three children and the workspace holds exactly those
  three, with no item outside the engagement.
- **Journal entries:** 37, read end to end, not skimmed — 9 on EP-001, 10 on WI-0001, 9 on
  WI-0002, 9 on WI-0003.
- **History:** 31 rows across the four tables — 6, 9, 7 and 9 — read before any journal.
- **Questions:** 10, all `status: answered`, all `addressed-to: human` — six on EP-001 including
  `EP-001/Q-004` (`kind: elicitation`) and `EP-001/Q-006` (`kind: sign-off`), two on WI-0001, two
  on WI-0003. No question was ever addressed to the architect and none was deferred.
- **Artifacts:** all 16 — three `refinement-qa.md`, three `plan.md`, three `impl-report.md`,
  three `verify-report.md`, and four `review.md` including the epic's.
- **Requests:** `tracker/requests/` holds no request; the stakeholder opened nothing on their own
  initiative after the engagement began.
- **Documents:** `docs/product/vision.md` v7 and `docs/architecture/overview.md` v6 in full,
  including both change logs; ADR-0001 to ADR-0009, including the `## Corrections` sections of
  ADR-0005 and ADR-0008.
- **Contracts:** the installed contracts for `intake` 0.3.0, `refine` 0.3.0, `plan` 0.4.1,
  `implement` 0.3.0, `verify` 0.2.0, `review-close` 0.6.0, `answer-questions` 0.4.0, `next` 0.4.0
  and `retro` 0.1.0, with their gate tables, plus `pipeline.yaml` 0.6.0 and
  `spec/journal-and-history.md`. **These are the current versions; every journal entry names the
  version that acted, and the two agree** — no entry in this record names a version other than
  the one installed here. Where an entry's behaviour differs from a contract, this report says
  which version the record names and treats the difference as unknown rather than as a defect.
- **Gates re-run by this reading:** `run: .claude/agile-skills/scripts/engagement-state EP-001 →
  exit 0, "EP-001 ended"`, and `run: .claude/agile-skills/scripts/lint-claims --all → exit 1, 48
  errors, all claim.citation.unresolved`.
- **Not available:** the product source tree. `recall/` and `tests/` were not banked with this
  copy of the record, so every claim about the code — and there are many, in `overview.md`, in the
  ADRs and in every `review.md` — was read as a claim *about* something absent. This reading can
  say what an execution reported it opened and whether two reports about the same code agree; it
  cannot open the code. Every one of the 48 `claim.citation.unresolved` errors
  `validate-workspace` and `lint-claims` report names a source file, and no other kind of error
  appears; that is a property of this copy, not of the engagement.
- **Not available:** the commit history. `git log` does not work here, so nothing below is drawn
  from commit times, commit messages or shas. Every timing in this report is read from a record
  timestamp, and every sha named in the record was taken as written rather than resolved.

## Engagement retrospective

### A universal claim about the tests was audited as true three times, written into a document by the third audit, and falsified by the fourth

`docs/architecture/overview.md` `## How it is checked` ends v5 asserting that *"every test that
runs the tool sets `RECALL_CARD_FILE` to a path inside a temporary directory and clears
`XDG_DATA_HOME` from the child's environment"*, and the engagement's own ending found two tests
that do neither [src: docs/architecture/overview.md:170]. What makes it worth writing down is not
the sentence but its history through four D12/DE6 claims audits, each of which opened something.

The same universal is already in `plan.md` before any code exists — step 6 says *"Every test sets
`RECALL_CARD_FILE` to a path inside a fresh `tempfile.TemporaryDirectory`"*
[src: tracker/items/WI-0001/artifacts/plan.md:103] — and the same document's own criteria mapping
describes the test that will not, *"with `RECALL_CARD_FILE` unset"*
[src: tracker/items/WI-0001/artifacts/plan.md:124]. The contradiction is between two rows of one
plan and nothing read it.

Then: WI-0001's review audits the weaker form of the claim and records **true**, having opened the
test class's shared fixture [src: tracker/items/WI-0001/artifacts/review.md:37]. WI-0002's review
audits it again and records **true**, naming `test_add` explicitly as a module that sets the
variable and pops the other [src: tracker/items/WI-0002/artifacts/review.md:32]. WI-0003's review
audits it a third time, records **true** having opened one helper in one file —
`tests/test_delete.py`'s `environment()` — and, on the strength of that reading, writes the
universal into the document [src: tracker/items/WI-0003/artifacts/review.md:37]. The ending's
audit reads `tests/test_add.py` and finds the two tests that falsify it
[src: tracker/items/EP-001/artifacts/review.md:133].

Each audit did what D12 asks: it opened what the citation named. For a claim quantified over a
family of tests, what the citation named was the family's shared fixture, and the exceptions were
in a member no citation named. The ending caught it because its scope was the whole document set
rather than a diff, and because it happened to open the one file the old citations omitted.

**Where it shows in the record:** the same section of the same document, at v5 and v6, nine
minutes apart, written and then repaired by the same skill at two different scopes.

### `claims-are-sourced` ran over an empty window at every work-item execution that could have caught something, and five executions said so

The gate is `lint-claims --changed-since {{trunk}}` for `implement`, `verify` and `review-close`,
and `--uncommitted` for `plan`. A work item's branch changes no document by construction: `plan`
writes its ADRs on the trunk before the branch exists, and `spec/doc-header.md` §5 forbids
`implement` and `verify` to write to `docs/` at all. So the window is empty, the gate exits 0, and
the pass is a pass over nothing.

Five executions recorded this rather than quietly banking the green.
`plan` on WI-0003: *"the absolute-claim half of that gate examined **zero documents**"*
[src: tracker/items/WI-0003/journal.md:586]. `implement` on WI-0003: *"**and it looked at
nothing**"* [src: tracker/items/WI-0003/journal.md:748]. `review-close` on WI-0001: the window
*"was **empty** when this execution began"*, so `--all` was run as well
[src: tracker/items/WI-0001/journal.md:684]. `review-close` on WI-0002: *"before the repair the
same command read `0 document(s) in 0 path(s)` and exited 0 having looked at nothing"*
[src: tracker/items/WI-0002/journal.md:571]. `review-close` on WI-0003, which ran it twice and
quoted both: *"green over nothing"* then *"a green over something"*
[src: tracker/items/WI-0003/journal.md:875].

Every false sentence this engagement found in `docs/` — five of them across three closes and the
ending — was found by a hand read, and each hand read was performed because a worker chose to,
not because a gate required it. The gate that is named `claims-are-sourced` proved that new
citations resolve; it never examined a claim that was already there.

**Where it shows in the record:** the same gate, four skills, five executions, one verdict.

### A criterion no environment could execute was ticked on a declared substitution, and the tick carries no mark of it

WI-0001 AC2 requires that *"the machine has been restarted"* [src: WI-0001 AC2]. `plan` named the
problem before any code existed [src: tracker/items/WI-0001/artifacts/plan.md:190]; `implement`
declared it under `## What I did not do`; `verify` weighed filing it as `ambiguous` and decided
against, because that *"costs a round trip on a criterion whose observable content is fully
decidable"*, and substituted a syscall trace and a post-exit read by another process
[src: tracker/items/WI-0001/journal.md:602]; `review-close` accepted it as a gap
[src: tracker/items/WI-0001/artifacts/review.md:101] and wrote it into the item's `## Notes`
[src: tracker/items/WI-0001/item.md:155]. WI-0002's close inherited it as an accepted gap and
WI-0003's close inherited it again. The epic's ending recorded success measure 8 as *"met as to the
file; the reboot itself is untested"* and the sign-off told the stakeholder so before they answered
[src: EP-001/Q-006].

Nothing in that chain is careless — it is the most thoroughly declared gap in the record. What the
record cannot do is show it in the one place a later reader looks: `item.md` carries `- [x] AC2`,
the same mark as the seven criteria settled by the observation they name, and the qualification
lives in five other places. Four consecutive skills each declared the substitution and each passed
it on; the item closed `delivered` on a criterion nobody could execute, and the person who could
have changed the criterion's wording was not asked about it until the engagement was over.

### Two ADR sequences share one citation form, and the record cites the toolkit's by the project's numbers

The record repeatedly cites `ADR-0008 §3` for the rule that a skill may not reconcile two of the
stakeholder's statements by editing a document — for example *"nothing was escalated under
ADR-0008 §3"* [src: tracker/items/WI-0003/journal.md:537], *"ADR-0008 §3's refused repair does not
arise"* [src: tracker/items/WI-0003/journal.md:701], and *"Not escalated as a conflict under
ADR-0008 §3"* [src: tracker/items/WI-0003/artifacts/refinement-qa.md:175]. The document meant is
the toolkit's own `meta/adr/ADR-0008-cross-answer-consistency.md`, which one artifact does name in
full [src: tracker/items/WI-0002/artifacts/refinement-qa.md:158]. This workspace's ADR-0008 is
*"Where the card file lives, and how it is written"* [src: ADR-0008], which has no §3 about
anything of the kind.

The collision is not present when the citation is written: `answer-questions` uses the form on
EP-001 at 11:20:13Z [src: tracker/items/EP-001/journal.md:102] and the project's ADR-0008 does not
exist until `plan` allocates it at 11:55:01Z [src: docs/architecture/overview.md:174]. Nothing is
mechanically broken — these are prose references, not source markers, so no gate resolves them —
and the record is internally consistent about which document it means. The cost falls entirely on
a later reader, who follows a number into the wrong document.

### One journal entry of 37 lists no gates at all, and it is the one entry that records no execution of its own

`spec/journal-and-history.md` §2.2 requires every gate in the acting skill's contract to appear
under `**Gates:**`, skipped ones included with the reason. Thirty-six entries do it: every
`verify` entry lists all seven of its contract's gates, every `review-close` entry all nine, every
`implement` entry all eight. The exception is EP-001's `answer-questions` entry of 11:50:33Z, which
reads *"**Gates:** none apply to this entry; it records no transition and takes no decision"*
[src: tracker/items/EP-001/journal.md:308].

The entry is not a lapse of care — it exists on purpose, to put two scope decisions taken on child
items in front of a reader of the epic, and it says so under `**Decisions:**`. It is the format
meeting a case it has no vocabulary for: an entry *about* other executions has no gates, and the
rule that every contract gate must appear has no third answer beyond pass, fail and skipped.

### The same gate on the same epic was recorded `not applicable` and then `skipped`, ten minutes apart, by the same skill

`review-close` v0.6.0 wrote `verification-postdates-the-code` → **not applicable** at 13:29:13Z
[src: tracker/items/EP-001/journal.md:352] and `verification-postdates-the-code` → **skipped** at
13:39:15Z [src: tracker/items/EP-001/journal.md:444], with the same reason both times — an epic has
no branch. Elsewhere the same situation produced `pass, vacuously`
[src: tracker/items/WI-0002/journal.md:457], `skipped, not applicable`
[src: tracker/items/WI-0003/journal.md:820], `pass, not applicable`
[src: tracker/items/WI-0002/journal.md:579] and `not applicable to this execution`
[src: tracker/items/WI-0003/journal.md:877]. `implement`'s opening entries recorded eight
not-yet-run gates as `skipped` on WI-0001 [src: tracker/items/WI-0001/journal.md:531] and as
`not yet run` on WI-0003 [src: tracker/items/WI-0003/journal.md:647].

The spec's vocabulary is three words; the record used at least six, all of them clear to a human
and none of them equal to another for a program. Nothing here is wrong. It is a place where a
reader counting gates has to read prose, and where a future check that counted verdicts would find
a record it could not parse.

### The stakeholder's four questions came in one round and their next two rounds came one item at a time, because the loop stops on the first open question

`next` step 3 stops the whole loop on any open human-addressed question. `refine` filed two on
WI-0001 at 11:32:14Z; WI-0003 was `draft`, runnable, and had two askable questions of its own. Under
the pipeline as written those would have waited for WI-0001's answers. They did not, because the
harness overrode it: WI-0003's `refine` entry names its own trigger as *"the harness's batching rule
(amendment A): file every question that can already be stated before the turn ends, so one
stakeholder round trip carries them all instead of one per turn"*
[src: tracker/items/WI-0003/journal.md:38]. The two rounds were then answered together, at
11:38:16Z and 11:43:03Z [src: WI-0001/Q-001] [src: WI-0003/Q-001].

The override is declared, and it bought exactly what it claims. It is worth recording because the
thing it worked around is in the pipeline: `next`'s own contract forbids dispatching two skills in
one run, so there is no move inside the loop that collects the questions an asynchronous
stakeholder could answer in one sitting.

### `refine` decided thirteen things without asking and recorded every one as ours, and the one that brushed a stakeholder sentence was argued rather than assumed

Across three items `refine` took thirteen decisions under the standing delegation *"As for how
it's actually built — whatever you think is best"* [src: EP-001/Q-004], each tagged `[assumed]` in
a `refinement-qa.md` with the deferral it rests on, and none recorded as something the stakeholder
said [src: tracker/items/WI-0001/artifacts/refinement-qa.md]
[src: tracker/items/WI-0002/artifacts/refinement-qa.md]
[src: tracker/items/WI-0003/artifacts/refinement-qa.md]. Two of them were tested against the
product question first rather than assumed into the deferral: the order due cards are offered in,
which was settled from the stakeholder's own request to be able to hand-check a session against
the file [src: tracker/items/WI-0002/artifacts/refinement-qa.md], and AC6's numbered prompt, which
runs against *"I don't need a numbered list for this"* [src: WI-0003/Q-001] and is argued as
compatible with the scope of their sentence stated, rather than reconciled by editing anything of
theirs [src: tracker/items/WI-0003/artifacts/refinement-qa.md:175].

## Positive record

### The elicitation question earned its place: it is why a third of the delivered product exists

`EP-001/Q-004` was filed by `intake` at 11:06:26Z, at the start of the engagement, addressed to the
human, `blocking: false`, and it listed the eight exclusions intake had inferred back to the
stakeholder to push against [src: EP-001/Q-004]. They pushed: *"I want to be able to delete a card;
editing can wait."* WI-0003 was filed the same round with `arose-from: EP-001/Q-004`
[src: WI-0003], against an epic whose `## Out of scope` had excluded deletion, and it shipped as
one of three delivered children [src: tracker/items/EP-001/artifacts/review.md:48]. This is a rule
that can be shown to have caught something rather than one that merely ran.

### Two of the stakeholder's own sentences were put back to them instead of being reconciled, twice

`intake` recorded that *"no cap on how many come up at once"* [src: EP-001/Q-003] and *"a review
taking more than a couple minutes to get through"* being a failure [src: EP-001/Q-004] cannot both
hold on a backlog, and escalated it as `EP-001/Q-005` with the recommendation line reading
*"none — this is yours to settle"* [src: EP-001/Q-005]. They settled it themselves, and the answer
became ADR-0003, two epic success measures and WI-0002's AC2, AC10 and AC11 [src: ADR-0003]
[src: WI-0002 AC10]. The second occasion is quieter and is the better test: `EP-001/Q-005`'s
refusal of a cap and `WI-0003/Q-002`'s request for a confirmation prompt pull in opposite
directions, and the record names the tension, argues why it is not a contradiction, and states
plainly that *"nothing was reconciled by us"* [src: WI-0003/Q-002].

### The termination gate refused twice and the epic was suspended rather than closed

`review-close` reached the epic at rest and filed the sign-off rather than recording an ending:
`check-epic-signoff EP-001` exited 1 both before and after the question existed, and the entry
records the second failure as the gate doing its job — *"the engagement waits on the stakeholder,
which is the point of the gate"* [src: tracker/items/EP-001/journal.md:344]. The epic went to
`awaiting-answer` with `resume-to: open`, the ending was recorded only after the reply arrived, and
the same script then exited 0 [src: tracker/items/EP-001/journal.md:436]. The sign-off itself
disclosed five things the stakeholder had no other way to know, including that no reboot was ever
tested, and the caveat travelled into the epic's `## Notes` rather than being dropped by the
acceptance [src: EP-001/Q-006] [src: EP-001].

### An advisory gate found a real ambiguity before any code was written

`plan-is-executable-without-you` is advisory and was not in `plan`'s at-a-glance hard-gate list.
Run on WI-0002 it found that step 3 said `_ask()` *"re-asks the same prompt"* while AC13's
demonstration requires the card's front to appear twice, so a developer could satisfy the sentence
and fail the test; the plan was amended before implementation began
[src: tracker/items/WI-0002/journal.md:205]. The entry names the gate as advisory and names what it
bought, which is the only way an advisory gate can be shown to be worth running.

### Verification had teeth, and the one mutation that survived was explained rather than dropped

Thirty-eight criteria across three items, each settled by a command `verify` ran itself with its
output quoted, and the implementation report cited as evidence nowhere
[src: tracker/items/WI-0001/artifacts/verify-report.md]
[src: tracker/items/WI-0002/artifacts/verify-report.md]
[src: tracker/items/WI-0003/artifacts/verify-report.md]. Thirty-two mutations were applied and
reverted. One survived, and rather than being quietly dropped it was shown to be an equivalent
mutant — two expressions that agree on every rung — and two mutations that genuinely change the cap
were run instead [src: tracker/items/WI-0002/journal.md]. `verify` also re-ran a criterion whose
first seed made it undecidable, at a rung where the two outcomes differ, and reported the first
attempt as what it was.

### Two gates caught the record's own repairs, including the reviewer's

`validate-workspace` refused `review-close`'s own documentation repair on WI-0001 twice — a change
log not newest-first, and a correction without its own version — and both were fixed before the
entry was written [src: tracker/items/WI-0001/journal.md:684]. `lint-answers` refused a
cross-answer check that cited a stakeholder reply not yet consumed, which moved the reasoning out
of the checked list and into prose where it belongs
[src: tracker/items/WI-0001/journal.md:171]. Neither is a gate on the work; both are gates on the
record, and both fired on the skill that was auditing everyone else.

## Proposed toolkit findings

### P-1 — PROPOSED — a claims gate scoped to a work item's branch diff is empty by construction, so it greens over nothing at every item close

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** methodology (`plan`, `implement`, `verify`, `review-close`), `scripts/lint-claims`,
  `spec/doc-header.md` §5
- **Symptom:** `claims-are-sourced` is `lint-claims --changed-since {{trunk}}` on three skills and
  `--uncommitted` on `plan`. `spec/doc-header.md` §5 forbids `implement` and `verify` to write to
  `docs/`, and `plan` writes its ADRs on the trunk before the branch exists, so the window the gate
  examines is empty at exactly the executions the gate names. Five executions in this engagement
  reported the empty window in their own journal entries rather than banking the green:
  [src: tracker/items/WI-0003/journal.md:586], [src: tracker/items/WI-0003/journal.md:748],
  [src: tracker/items/WI-0001/journal.md:684], [src: tracker/items/WI-0002/journal.md:571],
  [src: tracker/items/WI-0003/journal.md:875]. Every false sentence found in `docs/` during the
  engagement was found by a hand read the gate does not require and cannot perform.
- **Counterfactual:** any engagement reaches this. The emptiness follows from two toolkit rules
  meeting — documents are written on the trunk by `plan`, and two of the four skills that run the
  gate are forbidden to write documents at all — and not from anything about a project's subject.
  A consumer that never notices simply records four green gates that examined nothing.
- **Recurrence:** five times in this engagement, across four skills and three items, plus twice
  more where the same executions ran `lint-claims --all` on their own initiative to get a scope.
- **Direction:** the gate's scope should be chosen so that it cannot be empty when the execution
  had documents to be true about — for a work item, the documents the item's own artifacts cite,
  or the whole set, rather than the branch diff. Failing that, an empty window should be a distinct
  outcome the journal must record as such, so that "passed over nothing" is not spelled the same as
  "passed".
- **Status:** proposed — not filed. Triage upstream.

### P-2 — PROPOSED — a claim quantified over a family is audited by opening the family's shared fixture, and the exception lives in a member

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`review-close`'s D12, `plan`), `spec/dor-dod.md` D12,
  `scripts/lint-claims`
- **Symptom:** D12 asks whether each claim in `docs/` is still true and is satisfied by opening
  what the claim cites. For a claim of the form "every X does Y", what a citation names is the
  shared fixture, and the member that falsifies it is not cited. In this engagement the same
  universal was audited **true** three times, at three item closes, each opening something real —
  a test class's fixture [src: tracker/items/WI-0001/artifacts/review.md:37], four test modules
  named in one row [src: tracker/items/WI-0002/artifacts/review.md:32], one helper in one file
  [src: tracker/items/WI-0003/artifacts/review.md:37] — and the third audit wrote it into the
  document on the strength of that reading [src: docs/architecture/overview.md:170]. The ending's
  audit, whose scope was the whole document set, opened the one file the citations had omitted and
  found two members that falsify it [src: tracker/items/EP-001/artifacts/review.md:133]. The same
  document carried a second claim of the same shape — a module having no operation it in fact does
  not have — through four versions and three items [src: tracker/items/WI-0003/artifacts/review.md].
- **Counterfactual:** any engagement whose documentation describes a property of a family — every
  test, every caller, every handler, no path — reaches this. The auditor opens the citation, the
  citation names the general case because that is what the sentence is about, and the exception is
  in a member the sentence does not name. Nothing about this project's subject is load-bearing;
  `lint-claims` proves a citation resolves and states in its own docstring that it never proves the
  citation supports the sentence.
- **Recurrence:** twice in this engagement in the same document, one of them surviving three audits
  and being restated more strongly by the third.
- **Direction:** treat a quantifier as a distinct kind of claim. A sentence containing an absolute
  over a set should require the auditor to name the set's members and say how the set was
  enumerated, so that "I opened the fixture" and "I enumerated the members" are different entries in
  the audit rather than the same one; the absolutes the gate already detects in `docs/` are the
  place to hang it.
- **Status:** proposed — not filed. Triage upstream.

### P-3 — PROPOSED — a criterion the environment cannot execute is ticked on a substitution, and the tick carries no mark of it

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** methodology (`verify`, `review-close`), `spec/work-item.md`, `spec/dor-dod.md`
- **Symptom:** WI-0001 AC2 requires a machine restart [src: WI-0001 AC2]. No execution could
  perform one. `verify` considered the `ambiguous` route and declined it as a round trip on a
  criterion whose observable content is decidable, substituted a syscall trace and a post-exit
  read, and ticked [src: tracker/items/WI-0001/journal.md:602]. `plan`, `implement`, `verify` and
  `review-close` each declared the substitution in their own artifact
  [src: tracker/items/WI-0001/artifacts/plan.md:190]
  [src: tracker/items/WI-0001/artifacts/verify-report.md:111]
  [src: tracker/items/WI-0001/artifacts/review.md:101], and it reached the item's `## Notes`
  [src: tracker/items/WI-0001/item.md:155]. In `item.md` the criterion is `- [x] AC2`, spelled
  identically to the seven settled by the observation they name. Every downstream reader — WI-0002's
  close, WI-0003's close, the epic's DE3 — had to re-derive the qualification from prose, and the
  person who could have changed the criterion's wording heard about it first in the sign-off, after
  the work was done [src: EP-001/Q-006].
- **Counterfactual:** any engagement with a criterion naming something its runs cannot do — a
  reboot, a real device, a year elapsing, a second machine — reaches this. The skill's honest
  choices are a tick with a declared substitution or an `ambiguous` that costs a round trip, and the
  tick that follows is indistinguishable in the item from one settled directly. Nothing about
  flashcards is load-bearing.
- **Recurrence:** once as a criterion, and three more times as an inherited accepted gap at the two
  later closes and the ending.
- **Direction:** a criterion settled by something other than the observation it names should be
  marked where the criterion is, not only where the reasoning is — a distinct tick state, or a
  required annotation on the criterion line — and the substitution should oblige somebody to put
  the criterion's wording to the stakeholder while the engagement can still act on the answer,
  rather than disclosing it at sign-off.
- **Status:** proposed — not filed. Triage upstream.

### P-4 — PROPOSED — the loop stops on the first human question, so an asynchronous stakeholder is asked one item at a time

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** methodology (`next`), `pipeline.yaml` `orchestrator.steps` 3 and 5
- **Symptom:** `next` step 3 stops the whole loop on any open human-addressed question, and its
  contract forbids dispatching more than one skill per run. When `refine` suspended WI-0001 with two
  questions, WI-0003 was `draft`, runnable, and had two askable questions of its own; under the
  pipeline as written they would have waited for the first pair to be answered. They did not,
  because this run's harness overrode the one-action rule — WI-0003's `refine` entry names its own
  trigger as *"the harness's batching rule (amendment A)"*
  [src: tracker/items/WI-0003/journal.md:38] — and the four questions were answered in two rounds
  minutes apart [src: WI-0001/Q-001] [src: WI-0003/Q-001]. The workaround is declared, which is why
  it is visible; the thing worked around is in the pipeline.
- **Counterfactual:** any engagement with a stakeholder who answers asynchronously and more than one
  item needing refinement questions reaches this: the cost is one stakeholder round trip per item
  rather than per round, and the only remedy available inside the pipeline is to violate the
  one-action rule. Nothing about this project's subject appears in that sentence.
- **Recurrence:** once in this engagement, and it is the only place the run had to step outside the
  orchestrator's algorithm.
- **Direction:** separate "collect what can be asked" from "dispatch work". A pass that lets every
  currently-runnable item file the questions it can already state, before the loop stops on the
  human, would make one round trip carry them all without giving the scheduler judgement or letting
  two skills run against unwritten state.
- **Status:** proposed — not filed. Triage upstream.

### P-5 — PROPOSED — the toolkit's own ADRs and a consumer's ADRs share one citation form and one number space

- **Classification:** toolkit-defect
- **Severity:** doc error, low
- **Component:** `spec/doc-header.md` §4a, `scripts/lib/claims.py`, and the skill prose that cites
  `meta/adr/` by bare number
- **Symptom:** the record cites `ADR-0008 §3` for the toolkit's cross-answer-consistency rule at
  [src: tracker/items/WI-0003/journal.md:537], [src: tracker/items/WI-0003/journal.md:701] and
  [src: tracker/items/WI-0003/artifacts/refinement-qa.md:175], and names the document in full once
  [src: tracker/items/WI-0002/artifacts/refinement-qa.md:158]. This workspace's ADR-0008 is *"Where
  the card file lives, and how it is written"* [src: ADR-0008]. The citation form `ADR-nnnn` is
  defined to resolve inside `docs/architecture/adr/`, so a reader following the number lands on the
  wrong document. The collision is created after the fact: the form is used on EP-001 at 11:20:13Z
  [src: tracker/items/EP-001/journal.md:102] and the project's ADR-0008 is not allocated until
  11:55:01Z [src: docs/architecture/overview.md:174]. Nothing mechanical breaks — these are prose
  references rather than source markers, so no gate resolves them, which is also why nothing
  caught it.
- **Counterfactual:** every consumer reaches this the moment its own ADR sequence passes the numbers
  the toolkit's `meta/adr/` uses, which is to say within the first ten decisions of any project.
  The skills' own prose and specs cite those ADRs by bare number, and a worker quoting the rule it
  is following writes the number down. No project's subject matter is involved.
- **Recurrence:** four times in this engagement, in three different artifacts, all on one item.
- **Direction:** give the toolkit's own decisions a distinguishable citation form in the prose a
  consumer's workers copy from — a prefix, or the path — so that a bare `ADR-nnnn` in a consumer's
  record always means the consumer's own. Resolving the form mechanically in tracker prose, rather
  than only inside a source marker, would then make the collision a finding rather than a reading hazard.
- **Status:** proposed — not filed. Triage upstream.

### P-6 — PROPOSED — the interaction between two stakeholder answers made one refinement question unaskable until the other landed

- **Classification:** project-circumstance
- **Severity:** methodology gap, low
- **Component:** this project — WI-0003's identification of a card, and WI-0001's duplicate-front
  behaviour
- **Symptom:** `refine` on WI-0003 found a real Definition-of-Ready gap — what happens when the
  identifier matches nothing, or matches several cards — and could not ask it, because whether
  "several" was even possible depended on `WI-0001/Q-001`, which was open in the same round. It
  recorded the gap as `[unresolved]` with the reason and what would settle each half
  [src: tracker/items/WI-0003/artifacts/refinement-qa.md], rather than asking the stakeholder to
  reason about a combination of two answers they had not yet given. When both answers arrived,
  `answer-questions` decided it under the authority `WI-0003/Q-001` had recorded in writing when it
  was filed, as AC5 and AC6 [src: WI-0003 AC6] [src: ADR-0005].
- **Direction:** none for the toolkit. This is recorded because it went well and the mechanism that
  made it go well is worth keeping: a question filed with an explicit note of what it delegates back
  to the team once a sibling answer lands, and a Q&A file that keeps "not yet askable" distinct from
  "nobody noticed". The difficulty itself is the domain's — it exists because two flashcards may
  share a front side — and it would not arise in an engagement whose identifiers are unique.
- **Status:** proposed — not filed. Triage upstream.

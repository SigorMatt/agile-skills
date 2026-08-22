---
id: WI-0003
type: work-item
title: Import expenses from a bank CSV export instead of typing them
status: blocked
priority: medium
epic: EP-001
created: "2026-08-22T01:34:58Z"
depends-on:
  - WI-0001
  - WI-0002
updated: "2026-08-22T03:40:17Z"
---

## Story

As the person in the group who exports their bank statement anyway, I want to point the tool at
that CSV file and have its rows become recorded expenses, so that I do not retype spending the
bank has already written down.

## Acceptance criteria

- [ ] AC1 — a command takes the path of a CSV file, the payer, the people the imported expenses
      are shared by, and an optional date range compared against each row's own date, and records
      an expense for each row inside that range — one payer and one set of sharers for the whole
      run, split equally (`ADR-0007`). It takes **no** column-mapping options: which columns become
      the date, the amount and the description is fixed in this criterion, read off the
      stakeholder's own export (`Q-003`, `ADR-0010`). Those column names, the delimiter, the date
      format and the amount convention are still to be written here, and wait on one thing only —
      the sample file, which nothing else can supply
- [ ] AC2 — expenses imported from a CSV appear in the same expense list, and count towards the
      same "who owes whom" report, as expenses entered by hand
- [ ] AC3 — a row the tool cannot turn into an expense is reported on stderr, identified by its
      line number and with the reason, and does not silently vanish. What makes a row unusable is
      not yet enumerable — it depends on the file's shape, so this criterion waits on the sample
      and on nothing else
- [ ] AC4 — a file that is not readable, or is not the expected shape at all, is refused with a
      message and a non-zero exit code, and leaves the recorded data unchanged. "The expected
      shape" is now a fixed thing rather than an option (`ADR-0010`), but what it *is* waits on
      the sample
- [ ] AC5 — importing the same file twice does not produce a doubled set of expenses, or, if it
      does, the behaviour is stated and the person is warned before it happens. Which of the two
      this becomes waits on the sample as well: recognising an already-imported row needs
      something in the file that identifies one. `refine` expects to decide it toward skipping,
      and reporting how many rows were skipped, because WI-0001 shipped with no way to delete an
      expense

## Out of scope

- Talking to a bank, or any network access; the input is a file the person already has.
- Supporting more than the CSV shape this item settles on.
- Categorising or classifying transactions.

## Notes

**Waiting on the CSV sample, and no longer asking for it.** `EP-001/Q-002` asked for a sample of
the bank CSV and for the rule by which a bank row becomes a shared expense. `refine` split those
into `Q-001` (the sample) and `Q-002` (the rule); `Q-002` is answered (`ADR-0007`) and `Q-001` was
deferred twice. `Q-003` then asked the choice underneath the deferral — where the importer should
learn the file's shape from — and the stakeholder answered it: **"No — just wait for my file. I
don't want a name-the-columns version."** That is option A, recorded as `ADR-0010`.

So the *choice* is settled and the *fact* is not. `refine` MUST NOT attempt this item while the
sample is missing, and MUST NOT ask for it a fourth time. If no CSV exists under
`tracker/items/WI-0003/artifacts/` — `ADR-0010` names `bank-sample.csv` as where it should land —
`refine` records the impasse and moves this item to `blocked`, which is the status for something
only a human can resolve (`spec/ids-and-statuses.md` §3.1). Any skill may move it back to `draft`
once the file is there (§4).

**Ordering.** `EP-001/Q-001` settled that this item ships — the stakeholder was explicit that it
is not optional — but is built last. That is why `priority` is `medium` rather than `high`: the
selection key in `pipeline.yaml` orders by priority rank, and `medium` is the only mechanism the
orchestrator offers for "important, and built last". It is not a statement that the import
matters less. `depends-on` now also names WI-0002, because AC2 below cannot be verified until the
who-owes-whom report exists.

The two facts that were missing, and where each now stands:

- **Still missing — the actual shape of the stakeholder's bank CSV**: its columns, header row,
  delimiter, date format, and how amounts and signs are written. Deferred twice
  (`EP-001/Q-002`, then `Q-001`), and `Q-003` established that this is the only place it can come
  from — the stakeholder refused both alternatives. Nothing on disk derives it and no skill may
  guess it.
- **Settled — how a bank row becomes a *shared* expense.** The stakeholder chose option B on
  `Q-002`: they name the payer and the sharers when they run the import, and limit it to a date
  range. `ADR-0007` records it, together with the two details their answer left open — the range
  is optional, and a row outside it is skipped silently rather than reported as a failure. AC1
  above now says so.

AC5 is deliberately written as an either/or. Whether re-import is idempotent or additive is a
real choice, and `refine` should make it one criterion, not two.

### Settled inputs from WI-0001's refinement, 2026-08-22T01:55:49Z

Two of the stakeholder's answers on WI-0001 constrain this import, and neither changes the fact
that the CSV sample is still missing:

- **An expense carries a date, defaulting to today** (`WI-0001/Q-003`, `WI-0001` AC7). The
  stakeholder was asked this precisely because the import was confirmed and every bank row has a
  date. So the field exists and the import must carry each row's date onto the expense it
  creates, rather than stamping today. This will need a criterion once the sample arrives and the
  file's date format is known.
- **Amounts are plain two-decimal numbers with no symbol and no thousands separator**
  (`WI-0001` AC6, `ADR-0002`). Bank exports commonly write `€12,50`, `1,234.56` or a trailing
  minus. Normalising those into the accepted form is this item's job; `ADR-0002` deliberately did
  not widen what the hand-entry command accepts in order to make the import easier.

### `refine` reached this item at 2026-08-22T02:42:09Z and did not refine it

As this section already instructed. The two missing facts were filed as questions to the
stakeholder — `Q-001` (the CSV sample) and `Q-002` (how a row becomes a shared expense), both
citing `EP-001/Q-002` and superseding it per `spec/question.md` §3 rule 6 — and the item is
suspended at `awaiting-answer` with `resume-to: draft`.

**No Definition of Ready assessment was made and no acceptance criterion was read against R4**,
because assessing criteria that must be rewritten from a file nobody has seen would produce a
verdict about the wrong criteria. The next `refine` execution, after the answers arrive, owns
both the assessment and the rewrite.

The questions were filed now, rather than when the orchestrator next selects this item, because
the sample is the longest-lead thing in this epic: it is the one input that has to come from
outside the workspace, it has already been deferred once, and this item cannot start without it.
Filing it in the same round trip as `WI-0002/Q-001` costs the stakeholder one reply instead of
two. It does not make this item runnable — `depends-on` still names WI-0002, which is not `done`.

**AC5 was not asked about.** Whether re-import is idempotent or additive cannot be put as a
question until the sample says what identifies a row; the reasoning, and the direction `refine`
expects to take, are in `artifacts/refinement-qa.md` under "Deliberately not asked in this batch".

### `Q-002` answered, `Q-001` deferred a second time — propagated 2026-08-22T02:52:26Z

The stakeholder replied to both questions. One is an answer and one is not:

- **`Q-002` — answered.** "B — let me say who paid and who it's shared with when I run the
  import, and let me limit it to a date range. That's basically what a trip looks like anyway."
  Recorded as `ADR-0007`; AC1 amended (legitimate — the item is at `draft`, so criteria are not
  frozen). This closes the second of the two blocking facts and settles what the command *is*.
- **`Q-001` — deferred again.** "I'll send you a sample later", for the second time. Marked
  `answered` because that is what they said and it has a consequence, exactly as `EP-001/Q-002`
  was; the consequence is that this item still cannot be refined.

**Why the item goes back to `draft` rather than to `blocked`.** `blocked` is terminal and needs a
human to move an item out of it, and this item is not due yet: `depends-on` names WI-0002, which
is at `draft`, so the orchestrator will not select WI-0003 for a long time and the sample may
well arrive before it does. At `draft` the item is inert but self-healing — when `refine` is
finally dispatched it reads these notes, and if the sample is still missing it files a fresh
question and suspends again. Marking it `blocked` now would claim an impasse the pipeline has not
actually reached.

**No third question was filed for the sample in this execution.** The stakeholder has been asked
twice and has twice said "later"; asking a third time before any skill can use the answer would
spend their attention on a request they have already heard and would stop the loop while WI-0002
— the item that *is* runnable — waits. The instruction to ask stands, in writing, at the point
where the answer is actually needed.

**AC2, AC3, AC4 and AC5 were not touched.** Each depends on the file's shape, which is `Q-001`'s
missing fact. AC5 in particular — whether re-import is idempotent or additive — cannot be settled
until something identifies a row; `artifacts/refinement-qa.md` records the direction `refine`
expects to take and why it was not asked.

### `refine` reached this item again at 2026-08-22T03:28:24Z and filed `Q-003` instead of refining

WI-0002 closed, this item became runnable for the first time, and the CSV sample still had not
arrived — nothing under this project holds a CSV file or a header row. `## Notes` above instructed
`refine` to file a fresh question citing `Q-001` and suspend, and that is what happened. The item
is at `awaiting-answer` with `resume-to: draft`.

**What was *not* done, and why it is not the same as last time.** The stakeholder has now been
asked for the sample twice and has twice replied "I'll send you a sample later". A third identical
request would spend their attention on something they have already declined and would leave this
item waiting on a file that may never arrive. `Q-003` therefore supersedes `Q-001` and asks the
choice underneath it: **where should the importer learn the file's shape from?**

- **A — a sample sent now.** The column mapping and the formats go straight into the criteria; the
  command needs no options beyond the payer, sharers and date range `ADR-0007` already settled.
- **B — a fixed format the stakeholder converts their export into** before importing. Buildable
  today; rejected in the recommendation because converting the file at every import is the
  retyping the idea asked to stop.
- **C — the mapping given as options at import time** (`--date-column`, `--amount-column`,
  `--description-column`, `--date-format`), with the delimiter detected and an amount normaliser
  accepting a stated list of forms. Recommended: it takes the sample off the critical path without
  guessing anything, because the missing facts become arguments stated by the person holding the
  file.
- **D — drop the import.** Listed to be rejected; `EP-001/Q-001` settled that it ships.

**No acceptance criterion was rewritten and no Definition of Ready verdict was reached.** AC1 would
have to be written three different ways depending on the answer, and AC3 and AC4 differ between the
options in what "the expected shape" even means. R6 fails by construction while `Q-003` is open;
that is the suspension working, not a finding. `artifacts/refinement-qa.md` carries round 2 with
the question tagged `[unresolved]` and nothing tagged `[human]`, because the stakeholder has not
answered it.

**AC5 stays unasked** — whether a second import of the same file skips rows already imported or
adds them again. It still cannot be put well until something identifies a row, which depends on
which option is chosen. It is now named inside `Q-003` itself so the stakeholder sees it coming.
`refine` still expects to decide it toward skipping, and reporting how many rows were skipped,
because WI-0001 shipped with no way to delete an expense.

### `Q-003` answered, and the item is now an impasse rather than a question — 2026-08-22T03:33:27Z

The stakeholder answered `Q-003`: **"No — just wait for my file. I don't want a name-the-columns
version."** Read as option **A**, with **B** refused as well — "just wait" only makes sense if they
intend to hand over the export as it is, since under B there would be nothing to wait for.
`ADR-0010` records it.

**What is settled.** The importer is written against the stakeholder's real export. The column
mapping, the delimiter, the date format and the amount convention become fixed facts in AC1 once
the file exists, and the sample itself becomes the fixture the tests read. The command's arguments
are the file path, the payer, the sharers and the optional date range (`ADR-0007`) — and nothing
else. AC1 above says so now; the clause about the mapping becoming a run-time argument is gone,
because two of the three options that clause hedged against were refused.

**What is not settled, and cannot be by any skill.** The file's shape. AC1's mapping, AC3's
unusable row, AC4's "expected shape" and AC5's duplicate detection are all statements about a file
nobody here has seen. Each now says, in the criterion itself, that it waits on the sample and on
nothing else — which is a smaller and more honest statement than it was before `Q-003`, when it
also waited on a choice.

**Why no fourth question.** Three questions have now been addressed to the stakeholder about this
one file (`EP-001/Q-002`, `Q-001`, `Q-003`). The third was answered with an instruction, so they
know what is wanted and have said what they will do. A fourth would spend their attention on
something already settled, and `spec/question.md` §4 does not license a question whose answer is
already recorded.

**Why `blocked` is the right status next, and why this execution did not set it.** `blocked` is
"a documented impasse that no skill can resolve" and it is exactly what this is: the missing input
is outside the workspace and only a person can supply it. This execution returned the item to
`draft` because that is its recorded `resume-to` and `answer-questions` may not substitute its own
judgement for the status the suspending skill recorded. The move to `blocked` belongs to the next
`refine` execution, which owns `draft` items and is the skill that would otherwise ask a fourth
time. The instruction to do it is at the top of these notes, in writing, because the session that
carries it out will not be this one.

**No Definition of Ready verdict was reached here either.** `answer-questions` does not assess the
DoR; `refine` does, and it cannot while AC1, AC3, AC4 and AC5 are unwritable. R6 still fails by
construction, and that remains the situation working rather than a finding.

### The Definition of Ready was assessed for the first time, and it fails — 2026-08-22T03:38:34Z

`refine` was dispatched on this item at `draft` with every question on it answered. Previous
executions declined to assess the Definition of Ready at all, because the criteria were about to
be rewritten from a file nobody had seen and a verdict about criteria that are about to change is
a verdict about the wrong criteria. That reasoning has now run out: `Q-003` settled *where* the
file's shape comes from, so the criteria are no longer about to change shape — they are simply
unwritable. So the checklist was applied.

**Eight of the ten criteria pass. R4 and R10 fail, both on the same missing input.**

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: medium`; `validate-workspace` exit 0 |
| R2 | pass | `## Story` names the role ("the person in the group who exports their bank statement anyway"), the capability ("point the tool at that CSV file and have its rows become recorded expenses") and the outcome ("so that I do not retype spending the bank has already written down") |
| R3 | pass | AC1–AC5 exist, labelled and as checkboxes |
| **R4** | **fail** | Only AC2 is decidable today. AC1 cannot name the columns, the delimiter, the date format or the amount convention; AC3 cannot enumerate what makes a row unusable; AC4's "not the expected shape at all" has no referent; AC5 is still an either/or rather than a criterion. All four wait on the sample |
| R5 | pass | `## Out of scope` names three, including "Supporting more than the CSV shape this item settles on" — which a reader could reasonably assume is included |
| R6 | pass | first time it has passed on this item: `Q-001`, `Q-002` and `Q-003` are all `answered`, so no open question of any kind remains |
| R7 | pass | `depends-on` names WI-0001 and WI-0002; both are `done` |
| R8 | pass | `artifacts/refinement-qa.md` records rounds 1 and 2 verbatim, each answer tagged `[human]`, `[assumed]` or `[unresolved]` |
| R9 | pass | one command, one parser, one coherent change. `ADR-0007` and `ADR-0010` between them fix the command's whole argument list, and nothing in it suggests a split |
| **R10** | **fail** | see below — the combinations that do not depend on the file's shape are now visible; the ones that do cannot yet be enumerated |

**R10, and what was salvaged from it.** R10 asks that every combination of the behaviours this
item introduces be *visible* — stated in a criterion, excluded, or recorded here as deliberately
unconstrained. Some of those combinations do not depend on the CSV's shape at all, so they were
knowable today and are recorded below rather than left to be rediscovered. The rest do depend on
it, and "we cannot yet list the combinations" is not the same as a combination left deliberately
open, so R10 fails rather than passing on a technicality.

Left **open, by `refine`**, to be settled by the execution that unblocks this item. None of these
is a guess and none is a decision; they are the questions the eventual criteria have to answer:

- **a payer who is not a recorded person**, and **a sharer who is not a recorded person** — refuse
  the whole import, or record the person, or import the rows it can? WI-0001 AC1 requires people to
  be recorded before an expense names them, so refusal is the likely answer, but nothing says it.
- **a date range that matches no row** — succeed having imported nothing, or exit non-zero?
  `ADR-0007` settled that a row outside the range is skipped silently; it did not settle what
  happens when every row is.
- **whether the range bounds are inclusive** at each end.
- **an import whose rows are all unusable under AC3** — AC3 says each is reported; it does not say
  whether the run as a whole then fails.
- **the interaction of AC3's rejected rows with AC5's duplicate detection** — whether a row that
  failed to import on the first run is a row "already imported" on the second. This one *does*
  depend on the sample, because it depends on what identifies a row.

Not open, and deliberately so: the import's interaction with the repayments WI-0002 delivered.
An imported expense is an ordinary expense (AC2), and repayments are their own record
(`ADR-0001`), so there is no combination to state.

### Blocked, 2026-08-22T03:38:34Z — waiting on a file, not on an answer

The item moves to `blocked` with `resume-to: draft`. `blocked` is "a documented impasse that no
skill can resolve", and this is one: R4 and R10 fail on a single input — a sample of the
stakeholder's bank CSV export — which exists only outside this workspace and which no skill may
guess (`Q-001`, `ADR-0010`).

**Why not another question.** The stakeholder has been asked three times (`EP-001/Q-002`,
`Q-001`, `Q-003`) and answered the third with an instruction: "just wait for my file". There is no
question left to ask. `spec/question.md` §4 licenses an escalation when the record is silent or
intent is unrecorded; here the record is explicit and the intent is known. A fourth question would
be the pipeline asking for a file, which is not what the question protocol is for, and it would
stop the whole loop while `BUG-0001` — which is `ready` and runnable — waits.

**Why not `awaiting-answer`.** That status means a blocking question is open. None is, and
manufacturing one to hold the item there would put a false entry in the record and re-stop the
orchestrator on every future turn for a question nobody needs to answer.

**How this item comes back.** Put the sample at
`tracker/items/WI-0003/artifacts/bank-sample.csv` — 3–5 lines including the header row, with the
merchant names and amounts changed to anything; the shape is what matters, not the spending. Any
CSV under `tracker/items/WI-0003/artifacts/` will do. Any skill may then move the item from
`blocked` back to `draft` (`spec/ids-and-statuses.md` §4), and the next `refine` execution has
everything it needs: `ADR-0007` fixes what the command does with a row, `ADR-0010` fixes that the
mapping is read off the file rather than typed as options, and the open combinations above are
already listed. Nothing else about this item is outstanding.

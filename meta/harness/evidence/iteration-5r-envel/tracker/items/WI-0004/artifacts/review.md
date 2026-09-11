# Review — WI-0004

## What I examined

- **The diff, hunk by hunk**, `main...wi/WI-0004` — `git diff main...HEAD -- envel/ docs/` and
  `-- tests/`, read in full rather than the reports about it. Five files:
  - `envel/envelopes.py` — one function appended, `move(store, source, destination, cents, on)`.
    Traces to plan steps 1 and 2. Six refusals in the plan's recorded order, then a deep copy,
    `at` bound once and `day` formatted once, two appends, one line. Nothing else in the file
    changed: `git diff main...HEAD -- envel/envelopes.py` deletes no line, so `balance`,
    `record_spend` and the rest are untouched.
  - `envel/cli.py` — the `move` subparser (plan step 3), the dispatch branch (step 4), and
    `metavar="{new,add,list,spend,move}"`. The last is the hunk that looks unrelated to this item
    and is not: `WI-0001` AC14 requires the usage message to list the subcommands the tool has,
    and the plan named it as interface decision 3 and as its first risk.
  - `tests/test_envelopes.py` and `tests/test_cli.py` — one `Move` class each, plan steps 5 and 6.
  - `docs/architecture/adr/ADR-0006-…` — the erratum closing the one invalidation entry disposed
    `to-update`. Version 1 → 2, a change-log row and a `## Corrections` row.

  **Unrequested scope: none.** Every hunk maps to a plan step or to an invalidation row. Three
  tests go beyond what the plan's steps enumerate — `test_the_same_envelope_is_checked_before_the_amount`,
  the fourth malformed date `2026-13-01`, and `test_a_move_carries_no_description` — and all three
  are declared as deviations or justified in `impl-report.md`; each protects a decision the plan or
  the item took explicitly, and none adds behaviour.

- **Would I maintain it?** Yes, and the specifics rather than a feeling: `move` is a pure function
  of (document, arguments) like its four siblings, so the new subcommand adds no new shape to the
  module; the six refusals are a flat sequence of guards with the order justified in the docstring
  and fixed by two tests, so the one thing that could silently drift is pinned; `at` and `day` are
  each bound to a local before either append, which is what makes the two halves of a move unable
  to disagree; and the success line is built from the **new** document, not the old one, which is
  the trap the plan named in its fourth risk and `record_spend` had already stepped around.

- **The record.** `history.md` chains without a gap — eight rows, `— → draft → awaiting-answer →
  draft → ready → planned → in-progress → verifying → in-review` — and its last row matches
  `item.md`'s status. `journal.md` carries eight entries, one per row. `Q-001` is `answered` with
  `## Consequences` naming six real edits to `item.md`, all of which are present in it.

- **The two documents the invalidation set does not name** — `ADR-0003` and `ADR-0004`, read in
  full for D7's open question. Neither is falsified; the reads and their falsifiers are below.

- **The claims audit**, run as this execution's own reads against a scratch store holding all
  three entry kinds at once. Commands and output under `## Definition of Done` D12.

- **The trial merge**, in a detached worktree at `main`, with the project's test command run on
  the merge result.

- Also read in full: `item.md`, `plan.md` (the seven steps, the AC mapping, the nineteen
  invalidation rows, the seven binding ADRs), `impl-report.md`, `verify-report.md`, `journal.md`,
  `Q-001.md`, and all seven ADRs.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox settled | **pass** | Thirteen `- [x]` in `item.md`, no `- [ ]` and no `- [~]`. `grep -c "^- \[x\] AC"` → 13. No substitution was claimed, and none was needed: AC1 and AC6 name the store file under `ENVEL_FILE`, an observation this environment can make. |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | `## Criteria` carries one row per AC1–AC13, each naming the command run and quoting its actual output. Spot-checked three against the artefact and re-ran two here — AC3's boundary (`30.01` refused against `30.00`, `30.00` allowed) and AC13's four wrong argument counts — and both reproduce. No row cites `impl-report.md` as its evidence, which is the failure this criterion exists to catch. |
| D3 | all declared gates passed on the **final** state of the code | **pass, with the forcing examined** | `verify`'s nine gates all ran on `fdff4fb`, the branch head, and I re-ran the two that bear on the code here: `python3 -m unittest discover -s tests -t .` → exit 0, 119 tests, and `python3 -m compileall -q envel tests` → exit 0. Two earlier transitions carry `[gates forced]` — `plan` and `implement` — and the forcing is the **`workspace-valid` gate alone**, for the F-084 ordering deadlock; both journal entries record every other gate run by hand with its command and exit code, and `validate-workspace` reports 0 errors on the current state. I ran it again: 0 errors, 0 warnings. No gate was forced that bears on whether the code works, and none was recorded as passed without being run. Noted in `## Findings` as a toolkit observation rather than a defect of this item. |
| D4 | no open blocking question | **pass** | `WI-0004` has one question, `Q-001`, at `status: answered` with `answered-by: human`, `answered-at: 2026-09-11T05:21:43Z`. `grep -l 'status: open' tracker/items/*/questions/Q-*.md` returns nothing, anywhere in the workspace. |
| D5 | a journal entry per execution, history chains | **pass** | Eight history rows, eight journal entries, and the timestamps pair up row for row: `02:14:53` answer-questions, `05:13:15` refine, `05:22:31` answer-questions, `05:33:18` refine, `05:41:18` plan, `05:42:08` and `05:53:59` implement, `06:05:57` verify. `validate-workspace` → 0 errors, which is where the chain is checked mechanically. |
| D6 | every design-changing decision is in an ADR, cited from the plan or journal | **pass** | One decision changed the design: a move is **two** entries rather than one. It is `ADR-0007`, cited from `plan.md` `## Approach` and `## Decisions and ADRs`, and it records the rejected one-entry alternative and why — a two-envelope entry would special-case `balance`, the function every command depends on. The other six rows of the plan's decision table are answered-from-the-documents or reversible assumptions with their cost stated (`dest="source"`/`metavar="from"` because `from` is a keyword; the refusal order; the present-balance check), and none changes a decision an ADR records. |
| D7 | invalidation set confirmed | **pass** | `## Invalidation set confirmation` below — nineteen rows, all disposed; the one `to-update` updated with a version bump and a change-log row; the two `owned-by-ending` untouched; and the question the set cannot answer for itself answered by reading the two documents it does not name. `lint-documents --rule invalidation-set-is-disposed --item WI-0004` → exit 0, 19 entries against 19 rows. |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, *all 4 commit(s) on main..wi/WI-0004 name WI-0004*. |
| D9 | merged into the trunk | **pass** | Trial-merged clean into a detached worktree at `main` (`git worktree add --detach`), merge result `b90c317`, 12 files changed; the real merge follows this close, per the ordering the procedure requires, and its sha is recorded by `scripts/record-merge`. |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness WI-0004 wi/WI-0004` → exit 0: *verified at fdff4fba; wi/WI-0004 has moved to e9f9e122 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code.* The five files are `verify`'s own output. Run, not judged by eye. |
| D11 | `review.md` exists and says what was examined; every accepted gap is dispatchable | **pass** | This document. What was examined comes first and names the diff by file and hunk. The accepted-gaps table carries seven rows, each with an owner and a disposition; `lint-documents --rule accepted-gaps-are-dispatchable --item WI-0004` → exit 0. |
| D12 | claims in `docs/` about the behaviour this item touched are still true | **pass** | Six absolute claims audited below as this execution's own reads, each with its falsifier. |
| D13 | the plan's `binding-adrs` list is **complete** | **pass** | `find docs -name "*.md"` returns nine documents, seven of them ADRs — `ADR-0001` to `ADR-0007` — and the plan's binding list names all seven. The list is complete by exhaustion: there is no ADR in the project it could have missed. Conformance per ADR is `verify`'s verdict and is not re-decided here; `lint-documents --rule adr-conformance-is-decided --item WI-0004` → exit 0, *7 binding ADR(s), 7 conformance row(s)*. |

### D12 — the claims audit, with falsifiers

Run against a scratch store holding **all three entry kinds at once** (income `100.00`, a spend of
`12.50` dated `2026-09-01`, a move of `20.00` dated `2020-01-01`), because a fresh store exercises
none of the boundaries these sentences have.

| claim, and where it lives | falsifier — what a counterexample would look like, and why what I opened could have produced one | verdict |
|---|---|---|
| `ADR-0006` `## Consequences`, the clause **this change wrote**: *"`WI-0003` sums a month's spending by `on`, a month's moves by `on` [src: ADR-0007], and a month's income by `at`, with no branch on what a date means"* | A kind carrying `on` that the clause does not name, or a kind whose `on` means something other than the day the money moved. The store I read carries a move dated six years before the run — exactly the case where `on` could have turned out to be the recording day — and it shows `income` with no `on`, `spend` with `on: 2026-09-01`, and `move` with `on: 2020-01-01` twice, every `at` stamped `2026-09-11T06:09:0…`. Three kinds, three clauses, `on` meaning the same thing on both kinds that carry it. **Declared limit:** the half of the sentence about what `WI-0003` *will* do is not checkable against code, because `WI-0003` is not built; what is checkable is the field each kind carries, and that is what I checked. | **holds** |
| `docs/architecture/overview.md` `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | A `print` or `sys.exit` in a function the sentence does not name — and the new `move` is precisely such a function, added below `cli` after the sentence was written. `grep -n "print(\|sys.exit" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → exit 1, no hits. `move` returns `Ok` or `Refusal` as a value and `envel/cli.py:120` is what prints it. | **holds** |
| `docs/architecture/overview.md` `## The data`: *"a balance is the sum of an envelope's entries rather than a stored number"* | An entry kind `balance` has to special-case — and `move` is the first new kind since a spend, and the first that appends two entries at once. On the three-kind store, `envel list` prints `groceries  67.50` and `fun  20.00`, against a hand-computed `100 − 12.50 − 20` and `+20`. Nothing is stored and nothing is special-cased. | **holds** |
| `ADR-0007` `## Consequences`: *"the tool gains one entry kind and no field that some other kind does not already carry"* | A field on a `move` entry that no other kind carries. Set-differenced `move`'s field set against the union of `income`'s and `spend`'s on a store holding all three: **empty**. | **holds** |
| `docs/product/vision.md` `## What it deliberately is not`, bullet 2: *"no server, no sync, no bank import, no network"* | An import this change added that can open a socket. `grep -rn "socket\|urllib\|http\|requests\|ssl" envel/ bin/envel` → exit 1, no hits; the change added no import at all. | **holds** |
| `ADR-0001` `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | A conversion between cents and text in the new code. `grep -rn "int(whole)\|% 100\|// 100\|\* 100" envel/*.py` returns exactly two lines, `money.py:34` and `money.py:42`. `move` calls `money.format_amount` four times and converts nothing itself. | **holds** |

## Invalidation set confirmation

Nineteen entries in `plan.md`. Every one carries a disposition; `lint-documents --rule
invalidation-set-is-disposed --item WI-0004` → exit 0, *19 invalidation entr(y/ies) against 19
row(s) in the verification report*.

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/architecture/overview.md` — `## The parts`, the `envelopes.py` row | verified-still-true | Disposition present; `verify` reopened it and read five operations where the row claims five. I re-read `grep -n "^def " envel/envelopes.py`: `create`, `add_income`, `record_spend`, `listing`, `move`, plus four helpers. |
| `docs/architecture/overview.md` — `## The shape of it`, nothing below `cli` prints or exits | verified-still-true | Disposition present; reopened here, D12 row 2. |
| `docs/architecture/overview.md` — `## The data`, the move sentences | verified-still-true | Disposition present; the store I read carries two `move` entries, `-2000` and `+2000`, one `on` and one `at` on both, and no field linking them. |
| `docs/architecture/overview.md` — `## The data`, a balance is a sum | verified-still-true | Disposition present; reopened here, D12 row 3. |
| `docs/architecture/overview.md` — `## Conventions`, a date is `YYYY-MM-DD` and nothing else | verified-still-true | Disposition present; `verify` enumerated both `--on` call sites and refused a bad form on each. |
| `docs/architecture/overview.md` — `## What is not decided yet`, three items | verified-still-true | Disposition present; the board carries exactly `WI-0003`, `WI-0005` and `WI-0006` unstarted, `ADR-0007` exists, and `envel/store.py:11` still reads `FORMAT = 1`. |
| `docs/architecture/overview.md` — `## Engagement state` | owned-by-ending | **Left alone, and confirmed so**: no commit matching `WI-0004` touches the section, and it still reads *"`WI-0001` is the first item to be designed"*. Stale, and the ending's to restate — not this item's defect. |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` — `## Decision`, the JSON pair and the six bullets | verified-still-true | Disposition present; read field for field against a real store. |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` — `## Decision`, `format` stays `1` | verified-still-true | Disposition present; `envel/store.py` is untouched on this branch (`git diff main...HEAD -- envel/store.py` is empty) and line 11 is `FORMAT = 1`. |
| `docs/architecture/adr/ADR-0007-a-move-is-two-entries.md` — `## Consequences`, one kind and no new field | verified-still-true | Disposition present; reopened here, D12 row 4. |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` — `## Decision`, `at` on every kind | verified-still-true | Disposition present; the back-dated move in my store carries `at = 2026-09-11T06:09:07Z`, the recording moment, not `2020-01-01`. |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` — `## Consequences`, the enumeration of `WI-0003`'s sums | **to-update** | **Updated as claimed.** `ADR-0006` frontmatter reads `version: 2`, `updated-by: implement`, `updated-for: WI-0004`; the `## Change log` carries a version 2 row; and a `## Corrections` row records the erratum and why the surviving clause still holds. The new clause is audited at D12 row 1. |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — `## Decision`, balance is the sum of `cents` | verified-still-true | Disposition present; reopened here — D12 row 3 is the same claim one document along. |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — `## Decision`, `entries` is append-only and ordered as written | verified-still-true | Disposition present; `verify` captured the entry list either side of a move and found the prefix identical with exactly two appended. `move` deep-copies and appends and does nothing else to the list. |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` — `## Decision`, two functions in `money.py` | verified-still-true | Disposition present; reopened here, D12 row 6. |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` — `## Decision`, the two commands | verified-still-true | Disposition present; both commands were run by me on the branch head and again on the merge result, exit 0 each. |
| `docs/product/vision.md` — `## What it is for`, moving money | verified-still-true | Disposition present; the sentence now describes delivered behaviour and matches it. Its reason — an overspend is refused rather than shown negative — still holds: `envel spend groceries 1000` against `67.50` exits 1 and no envelope goes negative. |
| `docs/product/vision.md` — `## What it deliberately is not`, bullet 2 | verified-still-true | Disposition present; reopened here, D12 row 5. |
| `docs/product/vision.md` — `## Engagement state` | owned-by-ending | **Left alone, and confirmed so**: no `WI-0004` commit touches `vision.md` at all. |

### Did this change falsify a document the set does not name?

**No — and this is a claim against an enumerated set, not a memory.** `find docs -name "*.md"`
returns **nine** documents. Seven are in the invalidation set. The two that are not are
`ADR-0003-store-location.md` and `ADR-0004-invocation-package-and-shim.md`, and I read both in
full rather than inferring from their titles.

- **`ADR-0003`.** Its checkable sentences are the path resolution order, that missing parents are
  created on write and never on read, and *"One function in `envel/store.py` resolves the path and
  nothing else knows about it"*. The falsifier for the last is a second place in the tool that
  knows the path — and this change adds an operation that could plausibly have wanted one.
  `grep -rn "store_path\|ENVEL_FILE\|XDG_DATA_HOME\|\.local/share" envel/ bin/envel` returns four
  lines: three inside `envel/store.py` and one call site, `envel/cli.py:86`. `envelopes.move`
  takes a document and knows nothing about a file. `envel/store.py` is untouched on this branch.
  **Not falsified.**
- **`ADR-0004`.** Its checkable sentences are that there are two entry points *"both reaching the
  same `main`"*, that the shim's body is a `sys.path` line, an import and a call, and that no
  third-party dependency is introduced. The falsifier for the first is a subcommand reachable from
  one entry point and not the other — exactly the kind of thing adding a subcommand could cause.
  Ran both: `python3 -m envel` and `python3 bin/envel` each print
  `usage: envel [-h] {new,add,list,spend,move} ...`, and `python3 -m envel move a b 3` and
  `python3 bin/envel move b a 1` both exit 0 against a scratch store. `bin/envel` and
  `envel/__main__.py` are untouched on this branch, and the shim's body is still three lines.
  **Not falsified.**

Engagement-state sentences are excluded from this scope by `doc-header.md` §4a; both are stale and
both belong to the ending.

## Sections restated at the ending

`not an ending` — this is an item close. `EP-001` is `open` and `scripts/engagement-state EP-001`
reports `active`, with `WI-0003`, `WI-0005` and `WI-0006` still in flight. No `## Engagement state`
section was touched by this execution, and none was touched by this item.

## Findings

**No defect. Nothing sends this item back, and no bug belongs to another item.**

Four things worth recording rather than acting on. Findings 1 and 3 are about the toolkit
rather than about this change, and both are for whoever triages it.

1. **Two of this item's transitions carry `[gates forced]`, and the forcing is sound but it is the
   fourth occurrence of F-084 in this engagement.** A skill that writes a `docs/` change-log row
   for the item it is transitioning cannot pass `workspace-valid` from inside that transition:
   `doc.changelog.no-execution` looks for an execution of that skill in that item's journal, and
   the only entry that could satisfy it is the one `transition` appends *after* its gates run.
   `--resolving '<ITEM>:from->to+journal'` does not cover it. Both journal entries record every
   other gate run by hand with its command and exit code, and I re-ran the two that bear on the
   code plus `validate-workspace` — all green. `implement`'s entry also records why it did not
   restamp the change-log row to escape the deadlock: `spec/journal-and-history.md` §0 requires the
   `when` to be read from a clock at the moment it is written. That is the right call, and the
   record is honest about the cost. A finding about the toolkit, not about `WI-0004`, and not a
   send-back.
2. **A test in this change once passed against a deliberately broken implementation**, and the
   record says so rather than hiding it. `test_both_halves_carry_the_same_day_and_the_same_moment`
   asserted that a move's two halves share one `at`; with the real clock's one-second resolution it
   passed whether `at` was computed once or twice. `implement` found it by mutation, rewrote it to
   install a clock returning a different value per call, and recorded the whole sequence. I read
   the test as it now stands and it does install that clock, with `addCleanup` restoring the
   original. This is the methodology working, and it is worth naming as such.
3. **`accepted-gaps-are-dispatchable` silently dropped two of this review's seven gap rows, and
   the cause is a word.** `lint-documents`' `GAP_NONE_RE` is `^(none|no gaps?|nothing)\b`, applied
   to the **gap** column so that a review with nothing to declare can write one row saying `none`.
   Two of my rows opened *"Nothing computes `WI-0003`'s net moved figure…"* and *"Nothing in this
   epic corrects or deletes a recorded move…"* — both real gaps, both matched the sentinel, and the
   gate reported *"5 accepted gap(s)"* over a seven-row table and exited 0. I caught it only by
   reading the count against the table rather than the exit code, and reworded both rows so they
   are gated; the gate now reports seven. The failure mode is quiet and in the wrong direction: a
   gap is dropped from the check by how its sentence happens to start, and the run still passes.
   A sentinel that has to be distinguished from prose wants its own column or an exact match on
   the whole cell, not a prefix.

4. **`ADR-0006`'s `## Consequences` edit leaves one over-long line** — the `WI-0005` sentence now
   runs past the file's wrap width because the replacement was made mid-paragraph. Cosmetic, in a
   document whose meaning is correct; not worth a send-back or a bug, and noted so that whoever
   next edits that ADR reflows it.

## Accepted gaps

Seven gaps were declared — five across `verify-report.md` `## Not verified, and why` and
`impl-report.md` `## What I did not do`, and two more the item's own `## Out of scope` records.
Each is accepted, and each is disposed here rather than left as prose a reader would have to act
on.

| gap | owner | disposition | why that disposition |
|-----|-------|-------------|----------------------|
| That a move's `at` is **computed** once rather than computed twice and coincidentally equal cannot be observed here, the clock having one-second resolution (`verify-report.md`) | none | no-owner | Settled by a read of `envel/envelopes.py:242`, where `at = now()` is bound once before either append, and by `test_both_halves_carry_the_same_day_and_the_same_moment`, which installs a stepping clock precisely so the observation is possible in a test where it is not at a terminal. No work remains. |
| `WI-0003`'s net moved figure is not computed anywhere yet; this item only makes it possible (`impl-report.md`) | WI-0003 | item-filed:WI-0003 | The item exists on the board at `ready` with `depends-on: WI-0004`, so closing this item is what makes it runnable. |
| A move's date is never shown back to a person; it is observable only in the store file (`verify-report.md`) | WI-0003 | item-filed:WI-0003 | `WI-0003`'s summary is the first thing that renders a move's date, and `WI-0003` AC2 already carries the sentence that does it. |
| The two entries of a move carry no identifier linking them, so nothing can later identify the pair (`impl-report.md`) | none | no-owner | `ADR-0007` records it as the decision's own cost with the reversal priced — one field, one file, no migration — and nothing in this epic reads the pair. A limitation recorded, not work deferred. |
| The timezone edge — `at` is a UTC timestamp and `on` is the machine's local calendar day, so they can differ late in the evening — was not exercised (`impl-report.md`) | none | no-owner | `ADR-0006` `## Consequences` already records this as a deliberate and **correct** consequence: *"the person's calendar is the local one, and a summary of their August is the August they lived… the two fields are not convertible into each other and no code should try."* A move inherits it unchanged from the delivered spend, no criterion of this item reaches it, and there is no decision left to take. |
| Behaviour on a store whose `format` is not `1`, and on a damaged file, was not exercised here (`verify-report.md`) | none | no-owner | Owned by `ADR-0002` and delivered and verified under `WI-0001`; `envel/store.py` is untouched on this branch, so there is nothing this item could have changed about it. |
| Correcting or deleting a recorded move is not covered anywhere in this epic — `WI-0005` is scoped to spends (`item.md` `## Out of scope`) | none | no-owner | Recorded deliberately rather than deferred: a move is self-reversing, `WI-0003` AC2's moved figure is a **net** number so a mistake and its reversal cancel, and `--on` now lets a reversal be dated into the month the mistake landed in. The stakeholder named the cost themselves at `WI-0004/Q-001` — *"I can fix a spend afterwards and I can't fix a move"* — and the epic's sign-off is where it reaches them again, since it is a scope question rather than a defect. |

## Verdict

**Accept, `outcome: delivered`.** Thirteen criteria settled and each backed by a command; the diff
carries no unrequested scope; seven binding ADRs conform and the list is complete by exhaustion;
nineteen invalidation entries disposed, with the two documents the set does not name read and found
untouched; six absolute claims re-audited here with falsifiers, all holding; 119 tests green on the
merge result in a detached worktree, with `main` unmoved.

`in-review → done`, then the branch merges into `main`.

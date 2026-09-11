# Review — WI-0003

## What I examined

- **The item and its record.** `item.md` (fourteen criteria, `## Out of scope`, three rounds of
  refinement notes), `history.md` (10 rows), `journal.md` **in full** (10 entries), `plan.md`,
  `impl-report.md`, `verify-report.md`, and all five questions with their `## Consequences`.
- **The diff, hunk by hunk**, over `main..wi/WI-0003` — 13 files, 1333 insertions, 43 deletions.
  Every hunk mapped to a criterion or a plan step:
  - `envel/dates.py` — `_MONTH`, `MONTH_LENGTH`, `parse_month`, `this_month`, `month_of` (plan
    step 1, AC5/AC12); plus a module-docstring reword, which traces to **no** criterion and no
    step and is declared as deviation 3 in the implementation report. Examined: the old sentence
    said *"These three functions"* and there are now six, so it had become false in the commit
    that made it so. Repairing it is correct and it is source rather than `docs/`.
  - `envel/summary.py` (new, 101 lines) — `entry_month` (step 2, AC8), `figures` (step 3,
    AC2/AC3), `row` (step 5, AC2/AC11), `summarise` (step 4, AC4/AC7/AC9/AC10).
  - `envel/cli.py` — the `summary` subparser and the dispatch branch (step 6, AC1/AC14), and
    `summary` added to the top-level `metavar`, which is `WI-0001` AC14 reaching this change.
  - `tests/test_dates.py` `Month` (9 tests), `tests/test_summary.py` (27), `tests/test_cli.py`
    `Summary` (21). I listed all 57 by name against the criteria: every one maps to a criterion,
    to an ADR constraint (`NothingIsWritten` and `test_a_summary_writes_nothing_to_the_store` to
    `ADR-0002`; `test_an_entry_naming_an_envelope_that_is_not_there_is_in_no_row` to `ADR-0008`
    point 5; `test_months_compare_as_strings_in_calendar_order` to `ADR-0008` point 2), or to a
    delivered criterion this change could falsify (`test_the_tools_own_usage_names_the_new_subcommand`
    to `WI-0001` AC14). **No unrequested scope.**
  - `docs/product/vision.md` — the one `to-update` row; `tracker/` — the record.
- **The record's mechanics**, run rather than eyeballed: 10 journal entries against 10 history
  rows in the same order (`intake`, `refine`, `answer-questions`, `refine`, `answer-questions`,
  `refine`, `plan`, `implement`, `implement`, `verify`); the last history row `verifying →
  in-review` matches `item.md`'s status; every `## Consequences` path resolves on disk.
- **Six absolute claims, audited from their citations** — see D12. Each row names what I opened,
  a falsifier, and where a boundary applies, the boundary.
- **The merge**, in a `--detach`ed worktree at `main`, with the suite run on the merge result.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every checkbox settled | **pass** | `grep -c '^- \[x\] AC' item.md` → **14**; `grep -c '^- \[ \] AC\|^- \[~\] AC'` → **0**. No substitution was claimed, so no criterion carries a wording question back to the stakeholder |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | `## Criteria` there has fourteen rows, one per AC, each naming a command and quoting its actual output. I spot-checked the three that carry the item's weight by re-running them myself: AC3's worked example → `groceries  in 0.00  spent 20.00  moved 30.00  left 60.00`; AC9's boundary → `summary 2026-10` exit 1 and `summary 2026-09` exit 0; AC13's ten-invocation matrix → all ten on the stream and exit code they promise |
| D3 | all declared gates passed on the **final** state of the code | **pass, with one forcing examined** | `verify`'s nine gates ran on `6eb35e3`, the branch head at the time, and I re-ran the two that bear on the code, on the **merge result**: `python3 -m unittest discover -s tests -t .` → exit 0, 176 tests, and `python3 -m compileall -q envel tests` → exit 0. One transition carries `[gates forced]`: `implement`'s close forced `workspace-valid` for F-084 — the change-log row it rejected was outside this execution's journal window only until the closing entry existed. I did not take that on trust: `validate-workspace .` → **exit 0, 0 errors**, and the row now sits inside the window (06:30:02Z … 06:47:20Z contains 06:38:45Z) |
| D4 | no open blocking question | **pass** | all five questions on this item are `status: answered`; `validate-workspace` agrees |
| D5 | a journal entry per execution, history chains to the current status | **pass** | 10 entries against 10 rows, enumerated above and matched pairwise by skill and timestamp; the two `implement` entries are the opening and closing halves of one execution, which is the only place two entries share a skill |
| D6 | every design decision is in an ADR, cited from the plan or journal | **pass** | Two decisions changed the design and both are ADRs: `ADR-0008` (the month rule, the string form, the filtered sums, nothing precomputed, the absent envelope) and `ADR-0009` (the report's module). Both are cited from `plan.md` `## Decisions and ADRs`, which also records six further choices with where each was settled and on whose authority — the five under `## Assumptions` are reversible and priced, not design changes |
| D7 | every invalidation entry disposed; `to-update` entries really updated | **pass** | See `## Invalidation set confirmation`. `lint-documents --rule invalidation-set-is-disposed --item WI-0003` → exit 0, *27 entries against 27 rows*. The one `to-update` names `docs/product/vision.md`, which went `version: 2` → `3` with a change-log row. The two `owned-by-ending` entries were left alone: `git diff main...HEAD -- docs/` has exactly three hunks, all in `vision.md` — front matter, `## What it is for`, and the change-log table — and none in any `## Engagement state`. The question the set cannot answer for itself is answered by enumeration below |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → exit 0, *all 6 commit(s) on main..wi/WI-0003 name WI-0003* |
| D9 | merged into the trunk | **pass** | Trial-merged clean into a detached worktree at `main` (`git worktree add --detach`), merge result `c6854f6`; 176 tests and `compileall` both green **inside the trial**; `git rev-parse main` returned `34e811c` before and after, so the trial moved nothing. The real merge follows this close, per the ordering the procedure requires, and its sha is recorded by `scripts/record-merge` |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness WI-0003 wi/WI-0003` → exit 0: *verified at 6eb35e31; wi/WI-0003 has moved to 61aea9be but only the record changed (5 file(s) under tracker/ or docs/)*. Run, not judged by how the last commit looked |
| D11 | `review.md` exists and says what was examined; every accepted gap is dispatchable | **pass** | This document, with `## What I examined` first and naming the diff by file and hunk. `## Accepted gaps` carries seven rows, each with an owner and a disposition; `lint-documents --rule accepted-gaps-are-dispatchable --item WI-0003` → exit 0 |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass** | Six absolute claims audited from their citations, below, each with a falsifier and — where the rule has one — checked **at** the boundary. The one the item itself rewrote is audited first and hardest |
| D13 | `binding-adrs` is complete | **pass** | `find docs/architecture/adr -name '*.md'` → **9 files**, and the plan's `## Binding ADRs` names **9**: `ADR-0001` … `ADR-0009`. Complete by exhaustion — there is no ADR in this project the list omits, so no ADR can be engaged and unlisted. Conformance per ADR is `verify`'s verdict and is not re-decided here |

### D12 — the claims audit

| claim | what I opened | falsifier, and the boundary | verdict |
|-------|---------------|-----------------------------|---------|
| `vision.md`: *"the summary's **last** column is a balance rather than a monthly remainder — the fourth of the four figures in a row"* `[src: WI-0003 AC2 "each row shows four figures for that"]` — the sentence this item wrote | `item.md` AC2, in full. It names four figures and lists them in order: *"the money put into it during that month, the money spent from it during that month, the money moved into or out of it during that month, and the amount left in it at the end of that month"* — the balance **last**, fourth of four | Falsifier: AC2 naming a different count, or putting the balance anywhere but last; either would make the repaired sentence false in the same way the old one was. **Boundary**: a *monthly remainder* and a *balance* are indistinguishable in a month where money went in, so I read the case where they differ — an envelope with no activity at all that month. `summary 2026-09` → `groceries  in 0.00  spent 0.00  moved 0.00  left 60.00`. A remainder would have printed `0.00`; it printed the carried-over 60.00 | **holds** |
| `overview.md` `## Conventions`: *"A date typed at the command line is written `YYYY-MM-DD`, and a month `YYYY-MM`, and nothing else"* | `WI-0002` AC11 — *"`--on` accepts the full `YYYY-MM-DD` form and nothing else"* — and `WI-0003` AC5 — *"A month is written `YYYY-MM` — four-digit year, hyphen, two-digit month"*. Both cited, both say what the sentence says | Falsifier: a third command-line form accepted anywhere. **Boundary**: the one string that is a perfectly good *date* offered where a *month* is wanted — `bin/envel summary 2026-08-01` → exit 1, `'2026-08-01' is not a month`. The rule the sentence denies does apply to that input, so the check could have said no | **holds** |
| `overview.md` `## The parts`: *"`cli` knows about all five modules below it"* `[src: envel/cli.py:13]` | `envel/cli.py:13` → `from . import dates, envelopes, money, store, summary` | Falsifier: a sixth import, or a fifth that is not below `cli`. **Boundary**: the module this change *added* is the one that could have made "five" wrong — `summary` is one of the five, and `ls envel/*.py` offers no sixth candidate (`__init__.py` is empty, `__main__.py` sits above `cli`) | **holds** |
| `ADR-0007` `## Decision`: *"`WI-0003`'s net figure … positive when more arrived than left, which is the sentence `WI-0003` AC2 already contains"* | `item.md` AC2 → it contains, verbatim, *"The moved figure is one net number, positive when more arrived than left"* | Falsifier: AC2 not containing that sentence, which would make the ADR's claim about AC2 false regardless of the code. **Boundary**: the *giving* side, which the word "positive" says nothing directly about — `giver  in 100.00  spent 0.00  moved -30.00  left 70.00` against `taker … moved 30.00`, the same pair read from both ends | **holds** |
| `ADR-0006` `## Consequences`: *"`WI-0003` sums a month's spending by `on`, a month's moves by `on` `[src: ADR-0007]`, and a month's income by `at`"* | `ADR-0007` `## Decision`, line 78: *"**`on` is the day the move is held against**, written `YYYY-MM-DD`"* — so a move does carry the field this sentence sums it by | Falsifier: a move entry with no `on`, which would make the clause unsatisfiable. Checked in data: a move written by `bin/envel move` carries `on`, and a spend recorded **without** `--on` carries `on='2026-09-11'` — the case `ADR-0006` itself calls out and the one where the fallback could have bitten | **holds** |
| `overview.md` `## The data`: *"it is what lets a month's net moved figure be a sum with a filter rather than a special case"* `[src: WI-0003 AC2 "The moved figure is one net number, positive when more arrived than left"]` | `item.md` AC2, which carries those words, and `envel/summary.py:54` — `moved = sum(entry["cents"] for entry in in_month if entry["kind"] == "move")` | Falsifier: a special case — sign handling, or pairing the two halves of a move. The line has neither; the two halves are ordinary members of the same sum, which is why reading the pair from both ends gives `30.00` and `-30.00` without the code knowing they belong together | **holds** |

## Invalidation set confirmation

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/architecture/overview.md` (7 entries: the `summary` row, the dependency sentence, the print/exit absolute, the three beats, the `at`/`on` data sentence, the two-form conventions clause, the amounts clause, the streams clause, `## What is not decided yet`) | verified-still-true ×9 | `lint-documents --rule invalidation-set-is-disposed` → exit 0; `verify` reopened each against the branch head and recorded the enumeration; I re-ran the two that carry an absolute — `grep -n 'print(\|sys\.exit'` over the five modules below `cli` → exit 1 with the same grep finding 3 in `cli.py`, and `sed -n '13p' envel/cli.py` → five imports |
| `docs/architecture/overview.md` `## Engagement state` | owned-by-ending | Left alone. `git diff main...HEAD -- docs/` touches this file not at all |
| `docs/architecture/adr/ADR-0001` … `ADR-0009` (13 entries) | verified-still-true ×13 | Each reopened by `verify` with a clause and a line; I re-read the three this change could most plausibly have broken — `ADR-0001`'s *"only places the two forms meet"* (`grep -rn` over `envel/*.py` → 2 lines, both `money.py`), `ADR-0002`'s append-only entries (`md5sum` of a store unchanged across three summary runs), and `ADR-0008`'s *"nothing computes the carried-in figure"* (the four sums at `envel/summary.py:52-55`, none of them over months **before** the month asked for) |
| `docs/product/vision.md` `## What it is for`, the column ordinal | **to-update** | Updated: `version: 2` → `3`, `updated-by: implement`, `updated-for: WI-0003`, a new change-log row, and the sentence itself rewritten. Audited in D12's first row rather than accepted because it was edited |
| `docs/product/vision.md` (3 further entries: item 4 of four, the "not connected" bullet, the "no forecasts"/"no interface" bullets) | verified-still-true ×3 | Reopened; the sharpest is the forecasts bullet, which this change put at risk by adding the tool's first report — and the report **refuses** a future month rather than projecting one, so the one place a projection could have appeared does not have one |
| `docs/product/vision.md` `## Engagement state` | owned-by-ending | Left alone, and this is the one worth confirming rather than assuming, because the file *was* edited: the diff has three hunks — front matter, `## What it is for`, and the change-log table — and none of them is in this section |

**Did this change falsify a document the invalidation set does not name?** The question has a
mechanical answer here, and it is worth stating as one. `find docs -name '*.md'` returns **11
documents**: nine ADRs, `overview.md` and `vision.md`. Extracting the paths the set names gives
the **same 11**. The set is exhaustive over `docs/`, so there is no document it does not name and
no document this change could have falsified unseen. That is a stronger answer than F-087's
question usually gets, and it is the plan's doing rather than this review's.

## Sections restated at the ending

`not an ending`. `engagement-state EP-001` reports **`active`** — *still in flight: WI-0003,
WI-0005, WI-0006* — so this is an item close and the `## Engagement state` sections stay exactly
as they are. `lint-documents --rule engagement-state-is-restated --item WI-0003 --context
work-item` → exit 0, *NOT APPLICABLE — an item close is not an ending*. Recorded as not
applicable, never as passed.

## Findings

Three, none of them a send-back.

1. **`envel/dates.py`'s module docstring was reworded, and no criterion or plan step asks for it.**
   It is the one hunk in the diff that maps to neither. Examined and accepted: the old sentence
   said *"These three functions are the only conversions…"*, this change makes six, so the
   sentence was false in the commit that made it so. Repairing a false sentence in the file you
   are editing is correct, it is source rather than `docs/`, and `implement` declared it as
   deviation 3 rather than letting me find it. It is recorded here because a reader of the diff
   will ask, not because anything should change.
2. **`verify`'s own harness produced a false negative and then left the workspace looking broken**,
   and both are written up in `verify-report.md` `## Test sensitivity check`. I checked the claim
   rather than taking it: the AC10 and AC11 mutants are both 4864 bytes against a 4880-byte
   original, so CPython's mtime-and-size bytecode check cannot tell them apart within one second.
   This is the second engagement in a row where a mutation harness, not the code, produced the
   surprising result — `WI-0004`'s finding 3 was the same hazard wearing a different mask. The
   value of the write-up is the second half: a verifier who had stopped at *17 failures with a
   clean `git diff`* would have sent a sound item back. Nothing here is a defect of `WI-0003`.
3. **One store used in verification is not a store the tool could produce.** `/tmp/vfy/e.json`
   puts a spend before the income that funds it, which `envel spend` refuses. `verify` declared it
   under `## Not verified, and why` rather than leaving it to be found. Examined: the store is
   legal JSON of `ADR-0002`'s shape, the row's arithmetic is correct, and the criterion it
   demonstrates — AC8's asymmetry — needs two entries typed at the same moment with different
   months, which the delivered commands cannot produce at all. Accepted, and recorded as gap G4.

## Accepted gaps

| gap | owner | disposition | why that disposition |
|-----|-------|-------------|----------------------|
| G1 — the month-boundary race: `cli` defaults to `dates.this_month()` and `summarise` compares against `dates.this_month()`, so a run at exactly midnight on the first of a month could refuse the month it had just defaulted to (`impl-report.md`, `verify-report.md`) | none | no-owner | A limitation recorded, not work deferred. The plan named it as a risk, `implement` declared why closing it was not free — it means giving `summarise` the current month as a parameter, and `ADR-0009` states that signature — and `verify` found no criterion that reaches it. The cost is one refused invocation that succeeds on retry, so filing an item would put a change to an ADR'd interface on the board for a fault worth one retry. |
| G2 — AC5 and AC9 are about *the month today falls in*, and every observation was made on 2026-09-11; the rollover itself was never watched (`verify-report.md`) | none | no-owner | No skill can be dispatched to make a month end; this is a limit of when the run happened rather than deferred work. What could be checked was checked: both sides of AC9's boundary on the day, plus `dates.this_month()` against `datetime.date.today()` in the unit suite. |
| G3 — income's month is a UTC month and a spend's is a local one, so east or west of UTC an income typed late on the last evening can fall in the next month (`verify-report.md`) | none | no-owner | A consequence of a delivered decision that `ADR-0006` records as **correct**, saying the two fields are not convertible and no code should try. This item is the first to read both fields in one calculation, which is why it surfaced here, and `ADR-0008` `## Consequences` already carries it as a cost of the design. |
| G4 — four verification stores were seeded as JSON rather than built by the commands, and one of them could not be produced by the tool at all (`verify-report.md`) | none | no-owner | Forced by the criteria themselves: AC3, AC7 and AC8 are about months that have ended, and no command creates an envelope into the past or back-dates income. Each seed uses only the fields the delivered operations write, and its shape was cross-checked against a store built entirely through the commands. |
| G5 — two runs at once against one store was never tried (`verify-report.md`) | none | no-owner | Out of scope for every criterion of every item so far. What would be under test is `ADR-0002`'s atomic write, and nothing has asked for that yet; there is no criterion for a skill to work from. |
| G6 — income entered later than the month it arrived in stays in the month it was typed, with no way to correct it; `WI-0005` is scoped to spends (`item.md` `## Notes`) | none | no-owner | The stakeholder was shown this as option B's cost at `WI-0003/Q-003` and declined the work in as many words: *"I'm not paying for rework on a command that already works for a case I don't have; if it turns out to bite me after a couple of months, I'll tell you then."* They named their own route back, a new request under `tracker/requests/`. Filing a question would re-ask something they have answered. |
| G7 — a fourth entry kind would silently break AC3's reconciliation: it would land in `left` and in none of the three activity columns (`plan.md` `## Risks`, `ADR-0008`) | none | no-owner | Written into `ADR-0008` `## Consequences` as the cost of the decision, which is where a future author of a fourth kind meets it. `ADR-0002`'s `kind` field exists to allow one, but no item proposes one, so this engagement has nothing to dispatch. |

## Verdict

**Accept.** `WI-0003` is delivered and closed as `delivered`.

Fourteen criteria settled, each on a command `verify` ran and three of which I re-ran myself.
Thirteen Definition-of-Done criteria walked with their own result and evidence. Six absolute
claims audited from their citations with a falsifier each, and at a boundary where the rule has
one — including the one sentence this item rewrote, which is the row an audit is most tempted to
wave through because we wrote it. Twenty-seven invalidation entries confirmed, and D7's open
question answered by enumeration rather than by memory: the set names all eleven documents in the
project. Nine binding ADRs, complete by exhaustion against an index of nine. Seven gaps accepted,
every one disposed and every one genuinely a limitation rather than work quietly dropped. The
merge result is clean and green with `main` unmoved.

`EP-001` stays `open`: `WI-0005` and `WI-0006` are still `draft`, and closing this item is what
makes the first of them the next thing the board dispatches.

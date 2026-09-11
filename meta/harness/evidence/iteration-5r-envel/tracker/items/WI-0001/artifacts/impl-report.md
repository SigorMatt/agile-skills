# Implementation report — WI-0001

## The second execution, and what it changed

This item has been implemented twice. The first execution built the tool; `verify` sent it back
with AC15 failing, and this execution is that defect and nothing else. Everything below the next
heading is the first execution's report, amended in place where this one changed the answer; the
amended rows are AC8, AC9, AC14 and AC15 in `## Acceptance criteria evidence`, deviation 5, and
the gate table, which was re-run on the new branch head.

`verify-report.md` `## Defects found` listed three things. All three are done:

1. **AC15 — the usage message.** `envel/cli.py` used `parse_args`, which notices an extra
   argument only *after* it has returned from the subparser, so `envel new a b`,
   `envel add groceries 10 20` and `envel list extra` printed `usage: envel [-h] {new,add,list}
   ...` — the tool's usage, not the subcommand's. `main` now uses `parse_known_args` and reports
   anything left over through the subcommand's own parser, which prints
   `usage: envel new [-h] name`. All five invocations the criterion names now print a usage
   message for the subcommand that was misused.
2. **The test that asserted less than its criterion.** `test_the_wrong_number_of_arguments`
   checked only `assertTrue(run.stderr.strip())` — that stderr was non-empty, which is AC16's
   claim and not AC15's, and is why a green suite hid the defect. It now asserts the first line
   of stderr is a usage line, that it names the subcommand, and that it is **not** the tool's own
   usage, whose signature is the list `{new,add,list}`. `test_no_subcommand_and_an_unknown_one`
   was given the opposite assertion for AC14, so the two messages cannot drift back together
   without a test failing.
3. **The amount at the cent.** `verify` found that `format_amount` could be mutated to drop the
   units-of-cents digit and all 51 tests still passed, because every amount anywhere in the suite
   was a whole multiple of ten cents. Added: `test_an_amount_whose_cents_are_not_a_round_ten_is_exact`
   (12.57 + 0.03 = 12.60, through the command line) and two cases in
   `test_exactly_two_decimal_places` (`format_amount(1257)`, `format_amount(1)`).

**AC14 and AC16 were re-checked, not assumed.** `verify-report.md` warned that they come from the
same code path as AC15 and should be treated as unverified after any fix. The change touches only
what happens to *leftover* arguments; no subcommand and an unknown subcommand still fail at the
top level and still print the tool's usage, confirmed by running both, and every refusal still
goes to stderr with a non-zero exit.

**The three fixes were checked by mutation, the way `verify` checked the first execution:**
reverting the `parse_known_args` change fails `test_the_wrong_number_of_arguments`; rounding the
last cent digit away now fails `test_an_amount_whose_cents_are_not_a_round_ten_is_exact` and
`test_exactly_two_decimal_places`; and routing AC14's failures through a subcommand parser fails
sixteen tests. None of the three was insensitive.

## What was built

The tool, from nothing. There was no source code in this repository before this branch.

- `envel/money.py` — `parse_amount(text)` and `format_amount(cents)`, the only two places text
  and cents meet [src: ADR-0001].
- `envel/store.py` — `store_path()`, `load(path)`, `save(path, document)`, `empty_store()` and
  `StoreError`. A missing file is the empty store; a file that exists and cannot be read as this
  format raises, and nothing is written [src: ADR-0002] [src: ADR-0003].
- `envel/envelopes.py` — `create`, `add_income`, `listing`, plus `fold`, `find` and `balance`.
  Each operation returns `Ok(store, lines, changed)` or `Refusal(message)`; none of them prints
  or exits, and each deep-copies before changing anything, so a refusal cannot leave a
  half-changed store behind.
- `envel/cli.py` — the parser, the dispatch, and the only `print` and the only exit code in the
  package. Argument-shape failures are `argparse`'s: a failure of the tool is the top-level
  parser's and prints the tool's usage, a failure of a subcommand is that subparser's and prints
  its own.
- `envel/__main__.py` and `bin/envel` — the two entry points [src: ADR-0004].
- `tests/test_money.py`, `tests/test_store.py`, `tests/test_envelopes.py`, `tests/test_cli.py` —
  52 tests [src: run: python3 -m unittest discover -s tests -t . → exit 0, 52 tests, OK].

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `envel new <name>` calls `envelopes.create`, which appends the envelope and returns a line naming it; `cli.main` prints it to stdout and returns 0 | `tests/test_cli.py::CommandLine::test_new_creates_and_says_so`; `tests/test_envelopes.py::Create::test_creates_and_reports` |
| AC2 | `envel add <name> <amount>` parses the amount, appends an income entry, and returns a line naming the envelope and its new balance | `tests/test_cli.py::CommandLine::test_add_reports_the_amount_now_in_it`; `tests/test_envelopes.py::AddIncome::test_adds_and_reports_the_new_amount` |
| AC3 | `envelopes.listing` returns one line per envelope, sorted by the case-folded name, and nothing else | `tests/test_cli.py::CommandLine::test_list_is_one_line_per_envelope_in_order_with_no_total`; `tests/test_envelopes.py::Listing::test_one_line_per_envelope_ordered_by_folded_name`, `::test_no_total_line` |
| AC4 | the whole document is read and written on every command, so nothing is held between them | `tests/test_cli.py::CommandLine::test_three_separate_invocations_and_the_listing_still_has_it` — three separate subprocesses sharing one `ENVEL_FILE`; `tests/test_store.py::LoadAndSave::test_save_then_load_round_trips` |
| AC5 | `add_income` returns `Refusal` when `find` gives `None`, before anything is written | `tests/test_cli.py::CommandLine::test_income_to_an_envelope_that_does_not_exist` — asserts the envelope is absent from a following listing; `tests/test_envelopes.py::AddIncome::test_an_envelope_that_does_not_exist_is_refused_and_not_created` |
| AC6 | `load` treats a missing file as the empty store, and `listing` returns one line for it | `tests/test_cli.py::CommandLine::test_listing_with_no_envelopes_says_so_and_exits_zero` — also asserts the store file was not created by the read; `tests/test_store.py::LoadAndSave::test_a_missing_file_is_the_empty_store_and_creates_nothing` |
| AC7 | `create` returns `Refusal` naming the existing envelope and its amount, and does not deep-copy, so the caller's document is untouched | `tests/test_cli.py::CommandLine::test_creating_a_name_already_taken_changes_nothing` — asserts `400.00` is still listed afterwards; `tests/test_envelopes.py::Create::test_a_name_already_taken_is_refused_and_nothing_is_emptied` |
| AC8 | `parse_amount` accepts one or two decimal digits and raises `AmountError` naming decimal places for more; `format_amount` always writes two | `tests/test_money.py::ParseAmount::test_one_decimal_place_means_two`, `::test_three_decimal_places_is_refused`; `tests/test_money.py::FormatAmount::test_exactly_two_decimal_places` — which now covers `format_amount(1257)` and `format_amount(1)`, the digit no case in the suite exercised; `tests/test_cli.py::CommandLine::test_too_many_decimal_places`, `::test_an_amount_whose_cents_are_not_a_round_ten_is_exact` |
| AC9 | amounts are integers throughout, and each invocation re-reads and re-writes the whole store | `tests/test_cli.py::CommandLine::test_a_hundred_separate_additions_of_a_penny_total_exactly_one` — a hundred separate subprocesses, then a listing containing `1.00`; and `::test_an_amount_whose_cents_are_not_a_round_ten_is_exact` — `12.57` then `0.03` across two invocations, listing asserted equal to `['g  12.60']`, which is the case that fails if the last digit is rounded away |
| AC10 | `add_income` returns `Refusal` when `cents <= 0`, before any copy is made | `tests/test_cli.py::CommandLine::test_zero_and_negative_income`; `tests/test_envelopes.py::AddIncome::test_zero_and_negative_are_refused` |
| AC11 | `fold` is `str.casefold`, and `find` compares folded names; `create` refuses a folded match | `tests/test_cli.py::CommandLine::test_capitalisation_reaches_one_envelope_shown_as_first_typed` — one line listed, `10.00` in it, and a second `new Groceries` refused; `tests/test_envelopes.py::AddIncome::test_another_capitalisation_reaches_the_same_envelope` |
| AC12 | the document stores the name as first typed and `listing` prints that, never the folded form | `tests/test_cli.py::CommandLine::test_capitalisation_reaches_one_envelope_shown_as_first_typed` — the listed line starts `groceries` after income was added to `Groceries`; `tests/test_envelopes.py::Listing::test_the_name_is_shown_as_first_typed` |
| AC13 | `create` refuses only the empty name and one that differs from `name.strip(" ")`; nothing else is restricted | `tests/test_cli.py::CommandLine::test_names_may_hold_spaces_and_punctuation_but_not_edges_or_nothing`; `tests/test_envelopes.py::Create::test_spaces_and_punctuation_inside_a_name_are_accepted`, `::test_an_empty_name_is_refused`, `::test_a_leading_or_trailing_space_is_refused` |
| AC14 | the subparsers are `required=True` with `metavar="{new,add,list}"`, so both cases fail at the **top level** — before any subcommand is chosen — and argparse prints the tool's own usage, which carries the three names | `tests/test_cli.py::CommandLine::test_no_subcommand_and_an_unknown_one` — asserts each of `new`, `add` and `list` appears in stderr, that the first line of stderr is the tool's usage (it contains `{new,add,list}`, which a subcommand's usage never does), and that the store file was not created |
| AC15 | a missing positional is the subparser's own error and always was. A leftover positional is collected by `parse_known_args` and reported through `subcommand_parsers[arguments.command].error(...)`, so the usage printed is that subcommand's | `tests/test_cli.py::CommandLine::test_the_wrong_number_of_arguments` — the five invocations the criterion names, each asserting the first line of stderr is a usage line, names the subcommand, and is not the tool's own; then a listing asserted equal to `['groceries  400.00']`. Observed directly: `envel list extra` → `usage: envel list [-h]` / `envel list: error: unrecognized arguments: extra`, exit 2 |
| AC16 | `cli.main` is the only place that writes to a stream or returns a code: `Refusal` and both exceptions go to stderr with 1, `Ok` goes to stdout with 0, argparse uses stderr with 2 | `tests/test_cli.py::CommandLine::test_every_refusal_goes_to_stderr_with_a_non_zero_exit` — subtests keyed `AC5`, `AC7`, `AC8`, `AC10`, `AC13`, `AC14`, `AC15`, each asserting stderr non-empty, stdout empty, exit non-zero; `::test_every_success_goes_to_stdout_with_exit_zero` — subtests keyed `AC6`, `AC1`, `AC2`, `AC3` |
| AC17 | `_AMOUNT` matches an optional `-`, digits, and an optional decimal part and nothing else; `format_amount` emits only digits, a point and a possible `-` | `tests/test_money.py::ParseAmount::test_forms_that_are_not_amounts_are_refused`, `::test_a_negative_amount_parses`; `tests/test_money.py::FormatAmount::test_no_currency_symbol`; `tests/test_cli.py::CommandLine::test_an_amount_is_a_plain_number_in_and_out` |

## Documents

| document | entry it closes | claim kind | what I checked, and against what | new version |
|----------|-----------------|------------|----------------------------------|-------------|
| `docs/product/vision.md` | `## Engagement state`, bullets 1 and 2 | engagement-state | Nothing. Both are false and both belong to the ending; `review-close` restates them after the sign-off. The section was not opened for editing. | — (unchanged) |
| `docs/product/vision.md` | `## What it is for`: *"The command is `envel`"* | cited-fact | Reopened and read against `bin/envel`, whose filename is `envel`, and against `envel/cli.py`'s `ArgumentParser(prog="envel")`. Still true. The sentence cites `EP-001/Q-006`, a stakeholder answer, and nothing in this change touched what they decided. | — (unchanged) |
| `docs/product/vision.md` | `## What it deliberately is not`: *"Not connected to anything: no server, no sync, no bank import, no network."* | quantified | **Set:** every import in the shipped tool. **Enumerated with:** `grep -rn "^import \|^from \|^    import \|^    from " envel/ bin/envel` → 15 lines. **Members:** `pathlib`, `sys` (`bin/envel`); `argparse`, `sys`, `envel.envelopes/money/store` (`cli.py`); `copy`, `dataclasses`, `datetime`, `envel.money` (`envelopes.py`); `sys`, `envel.cli` (`__main__.py`); `re` (`money.py`); `json`, `os`, `pathlib` (`store.py`). **Verdict per member:** every one is either the standard library or this package, and not one of them opens a connection. **Falsifier:** an import of a networking module, or a shell-out to one — a member the sentence does not name. `grep -rnE "socket\|urllib\|http\|requests\|ssl\|asyncio\|subprocess" envel/ bin/envel` → exit 1, no matches, so no such member exists. Still true. | — (unchanged) |
| `docs/product/vision.md` | `## What it is for`: *"the tool starts, does one thing, and exits … nothing runs between invocations"* — **row added by this execution** | quantified | **Set:** the four entry paths into the process — `bin/envel`, `envel/__main__.py`, and the two ways `cli.main` returns. **Enumerated with:** `ls envel/` plus reading both entry files. **Verdict per member:** each calls `cli.main` once and passes its return value to `sys.exit`; `cli.main` contains no loop, no thread, no timer and no server. **Falsifier:** a background thread or a process that outlives the call — the `subprocess`/`asyncio` grep above finds none. Still true. | — (unchanged) |
| `docs/architecture/overview.md` | `## The parts`, the module table | cited-fact | **False, and repaired.** The table said the shim is `envel` at the repository root. A file of that name cannot exist beside the package directory `envel/`: `echo hi > envel` in a directory holding `envel/` fails with *"Is a directory"* (exit 1). The row now names `bin/envel` and cites it. | **2** |
| `docs/architecture/overview.md` | `## The shape of it`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | quantified | **Set:** the modules below `cli.py` — `envel/money.py`, `envel/store.py`, `envel/envelopes.py`, `envel/__init__.py`. **Enumerated with:** `ls envel/` → `cli.py`, `envelopes.py`, `__init__.py`, `__main__.py`, `money.py`, `store.py`; `__main__.py` is above `cli`, not below. **Verdict per member:** `grep -rn "print(\|sys\.exit\|sys\.stdout\|sys\.stderr" envel/money.py envel/store.py envel/envelopes.py` → exit 1, no matches, and `__init__.py` is empty. **Falsifier:** a `print` or an exit in one of those four — there is none. Still true. | — (unchanged) |
| `docs/architecture/overview.md` | `## The data`: *"a balance is the sum of an envelope's entries rather than a stored number"* | cited-fact | Reopened and read against `envel/envelopes.py`'s `balance`, which sums `entry["cents"]` over the entries, and against the stored document, which has no balance field [src: envel/envelopes.py]. Still true. | — (unchanged) |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | Nothing. The section was not opened for editing, and the version bump above did not touch it. | — |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | quantified | **Set:** every site in the package where text and cents convert. **Enumerated with:** `grep -rn "format_amount\|parse_amount\|def .*amount" envel/` → 8 lines, and `grep -rnE "float\(\|int\(\|%\.2f\|:\.2f\|round\(" envel/` → 4 lines, of which three are `print(` matching `int(` and one is `envel/money.py:34`. **Members:** the two definitions in `money.py`; six call sites (`cli.py:44`, `envelopes.py:71, 83, 99, 101, 114`); and the arithmetic at `money.py:34`. **Verdict per member:** every call site calls one of the two functions rather than converting for itself, and the only arithmetic is inside `parse_amount`. **Falsifier:** a conversion done somewhere else — a `float()`, a `%.2f`, a hand-written split — and the second grep finds none outside `money.py`. Still true. | — (unchanged) |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` | `## Decision`, the JSON document and the atomic-write clause | cited-fact | Reopened field by field against a store written by the tool: `format`, `envelopes` with `name` and `created`, `entries` with `kind`, `envelope`, `cents` and `at` — all present and named as the ADR says [src: envel/store.py]. The atomic write is a temporary file beside the target and `os.replace`, covered by `tests/test_store.py::LoadAndSave::test_save_leaves_no_temporary_file_behind`. The missing-file and damaged-file clauses are covered by the three refusal tests in the same class. Still true. | — (unchanged) |
| `docs/architecture/adr/ADR-0003-store-location.md` | `## Decision`, the three-step path resolution | cited-fact | Reopened against `envel/store.py`'s `store_path`, and against the three tests in `tests/test_store.py::StorePath`, one per step, which assert the resolution in order. Still true. | — (unchanged) |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` | `## Decision`, the two entry points | cited-fact | **False in two clauses, and repaired as one erratum rather than superseded** — the decision (a package, a shim, no install step) is unchanged and no code has to change to satisfy the new text. (1) *"an executable file at the repository root"* is impossible beside the package directory, as above. (2) *"the shim's body is an import and a call"* — `bin/envel` also puts the repository root on `sys.path`, because it is no longer beside the package. Both quoted verbatim in the ADR's new `## Corrections` section with the evidence, as a single entry because one fact — the shim cannot live beside the package — is what makes both false. That the two entry points reach the same `main` is covered by `tests/test_cli.py::CommandLine::test_the_two_entry_points_agree`. | **2** |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` | `## Decision`: *"The test command exits 5 while no test exists"* | cited-fact | Reopened. The clause is scoped to the empty suite and predicts its own expiry — *"becomes exit 0 as soon as `implement` writes the first test"*. Re-measured now that tests exist: `python3 -m unittest discover -s tests -t .` → exit 0, 51 tests, OK. That is what the sentence says would happen, so the assertion stands and nothing in it is false. | — (unchanged) |

**The second execution wrote no document, and needed to.** It changed `envel/cli.py` and two test
files. Every sentence under `docs/` that could speak to it was reopened: `grep -rn
"argparse\|usage\|subcommand\|argument" docs/` returns two lines, both in
`docs/architecture/overview.md` — *"a command is a function from (store, arguments) to (new store,
output, exit code)"* and the module row *"`envel/cli.py` | the command line: parsing arguments,
dispatching, printing, and the exit code"*. Both are still true of the new code, which parses
arguments in `cli.py` and nowhere else. No entry was added to the invalidation set, because
nothing was falsified; no version was bumped, because nothing was repaired.

**Did the first execution falsify a document the set does not name?** One, and it was added to the
set rather than left out: the vision's sentence about the tool starting, doing one thing and exiting,
which had nothing behind it until there was code. `docs/process/` holds no document. No other
sentence in `docs/` describes behaviour this item touched.

## Deviations from the plan

1. **The shim is `bin/envel`, not `./envel` at the repository root** (plan step 5, `ADR-0004`).
   The plan's arrangement cannot exist: a file named `envel` and the package directory `envel/`
   share one name, and `echo hi > envel` in a directory holding `envel/` fails with *"Is a
   directory"*. This is a *how* and not a *what* — the deliverable is a runnable `envel` with no
   install step, and `bin/envel` delivers it, arguably better, since putting `bin/` on a `PATH`
   exposes the command and nothing else. `ADR-0004` was corrected by erratum rather than
   superseded, because the decision it records is untouched.
2. **`Ok` carries a `changed` flag** that the plan did not name. Without it, `envel list` would
   save the store it had just read, which would create the file during a read and contradict
   `ADR-0003`'s *"never on a read"*. `tests/test_cli.py::CommandLine::test_listing_with_no_envelopes_says_so_and_exits_zero`
   asserts the file is still absent afterwards.
3. **The operations deep-copy before changing anything** rather than mutating in place. The plan
   says each returns a new store; this is what makes that literally true, and it is what lets the
   refusal tests assert that the document they passed in is byte-for-byte unchanged.
4. **`tests/test_cli.py` runs the tool with a minimal environment** (`PATH` and `ENVEL_FILE`
   only), so a stray `XDG_DATA_HOME` or `HOME` on the machine running the suite cannot reach a
   real store. The plan said to point `ENVEL_FILE` at a temporary path; this is that, made
   airtight.

5. **Argument-shape failures are still argparse's, but not all of them are the top-level
   parser's** (plan step 4, and the plan's `## Decisions and ADRs` row *"Argument-shape failures
   are left to `argparse` rather than hand-written"*). That decision is honoured — there is no
   hand-rolled parser, and `main` still does not validate argument counts itself. What changed is
   which parser reports the failure. The same table row glosses the decision as *"AC14 and AC15
   constrain the stream and the exit code, not the wording"*, and that gloss is wrong: AC15 also
   says **"a usage message for that subcommand"**, which is not wording but which message. The
   criterion is the contract and the plan cannot narrow it, so the code follows the criterion.
   I have not edited that row — the design is not this skill's to rewrite — and record it here
   instead. The change is six lines in `envel/cli.py`; reversing it is deleting them.

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, **52 tests**, OK, on branch head `81441cd` |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `validate-workspace` → exit 0 |
| `every-criterion-has-a-test` | pass | the table above names a test function for all seventeen; none is demonstrated by reading the code. AC15's test now asserts what AC15 says rather than what AC16 says |
| `commits-reference-the-item` | pass | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, all **6** commits on `main..wi/WI-0001` |
| `no-unplanned-scope` | pass, advisory | every hunk is a plan step or AC15's defect; the five deviations above are the only departures and each is recorded |
| `cross-answer-consistency` | pass | `lint-answers --changed-since main` → exit 0 |
| `claims-are-sourced` | pass | `lint-claims --changed-since main --plan-documents WI-0001` → exit 0. **Scope printed by the run:** 7 documents in 7 paths — 2 paths differing from `main` under `docs/`, plus the 7 named by WI-0001's plan. A non-empty window |
| `document-writes-are-declared` | pass | `lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main` → exit 0, 2 documents written on the branch, both in the plan's set. **This execution wrote none** |

## Two things the toolkit forced, recorded rather than hidden

1. **The two change-log rows this execution wrote carry `2026-09-11T02:43:44Z`, which is when
   this execution *began*, not the minute the edits were made.** `doc.changelog.no-execution`
   checks the row's `when` against the item's journal and treats an execution as closing at its
   last entry. `implement` writes two entries, and the second is appended by the transition
   *after* its gates have run — so while the work is being done the only window the checker can
   see is the single instant of the opening entry, and any later timestamp is rejected with
   *"no execution of implement on WI-0001 was running then"*. `--resolving
   'WI-0001:in-progress->verifying+journal'` does not widen it; that was tested. The row names
   the right skill, the right item and a real clock value from this execution, and this
   paragraph is here so nobody reads it as a claim that the edit happened in the same second the
   branch was cut. It is the third face of F-084 in this engagement.
2. **The two errata on `ADR-0004` are one `## Corrections` entry, not two.** Written as two,
   `adr.correction.changelog` refuses them — *"2 correction(s) and only 2 change-log row(s)"* —
   because every correction is a version. They have one cause between them, so one entry
   quoting both removed clauses is the honest shape as well as the passing one.

## What I did not do

- **Nothing was ticked in `item.md`.** The checkboxes are `verify`'s, not this skill's. AC15 is
  the one left unticked by the last verification, and re-ticking it is not this skill's to do.
- **The plan's `## Decisions and ADRs` row about argparse was not edited**, though its gloss on
  what AC15 demands is wrong. The design is not this skill's to rewrite; deviation 5 records it.
- **No `pyproject.toml` and no install step**, per `ADR-0004` and the plan's `## Out of scope`.
  `envel` is on a `PATH` only if the user puts `bin/` there.
- **The `at` and `created` fields are written and never read.** No criterion of this item observes
  either; they exist so `WI-0003` is not a migration [src: ADR-0002].
- **Nothing was built for the five later items** — no spend, no summary, no move, no correction,
  no per-envelope history — and `envel/store.py`'s `FORMAT` is the only concession to them.
- **No style or type checking was run**, because the project has none [src: ADR-0005].

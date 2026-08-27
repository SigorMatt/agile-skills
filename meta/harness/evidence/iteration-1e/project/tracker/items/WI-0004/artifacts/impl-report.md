# Implementation report — WI-0004

> **This report covers two executions of `implement`.** Everything down to `## What I did not do`
> is round 1 (2026-08-27T01:14:36Z–01:19:22Z), which built the item. `review-close` then rejected
> the item on Definition of Done D7 and D12 [src: tracker/items/WI-0004/artifacts/review.md], and
> round 2 — `## Round 2`, at the end of this file — is the fix. Round 1's text is left as it was
> written, with one bullet corrected in place and the correction stated rather than the wrong
> sentence removed.

## What was built

Two commands, `person delete <NAME>` and `expense delete <NUMBER>`, and the leading position
column in `expense list` that gives the second one something to name. The change is the plan's
eleven steps and nothing else: no new module, no change to the stored record shape, no change to
`expenses/settle.py` or `expenses/money.py`.

- `expenses/store.py` gains `naming_expenses(data, name)`, `delete_person(data, name)` and
  `delete_expense(data, number)`. All three refuse before they mutate, which is what makes "a
  refusal changes nothing on disk" a property of the layering rather than a promise each handler
  keeps. `delete_person` is where ADR-0007's invariant is enforced: it refuses while any stored
  expense names the person, saying how many do.
- `expenses/cli.py` gains the two subparsers, the two handlers, `parse_position`, and the number
  column in `expense_list`. Each handler calls `store.save()` only after its store function has
  returned, so no refusal reaches the disk. `expense delete` takes its argument as text and
  converts it in `parse_position`, so `0`, `-1` and `abc` are all this tool's own one-line
  refusal on stderr with exit 2, rather than argparse's usage text and its own exit code.
- `tests/test_store.py` and `tests/test_cli.py` gain the coverage listed below.
- `README.md` documents both commands, the numbered sample listing, the refusal, and the
  renumbering.

Commits on `wi/WI-0004`, in order:

| sha | subject |
|-----|---------|
| `46dead0` | `store: naming_expenses, delete_person and delete_expense (refs WI-0004)` |
| `ff28637` | `cli: person delete and expense delete, and a numbered expense list (refs WI-0004)` |

## Acceptance criteria evidence

Every row names a test that fails if the behaviour is removed. All are in
`python3 -m unittest discover -s tests -t .`, which ran 120 tests and exited 0 on the branch head.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 — `person delete Ben` with no expenses prints `deleted Ben`; `person list` then prints `Ana` | `store.delete_person` removes the name; `cli.person_delete` prints `deleted %s` and exits 0 | `tests.test_cli.WI0004AC1DeletingAPersonNobodysExpensesName.test_ben_goes_and_ana_is_all_that_is_left` asserts exit 0, stdout exactly `"deleted Ben\n"`, then `person list` stdout exactly `"Ana\n"`. Store-level: `tests.test_store.DeletePersonTests.test_an_unused_person_is_removed_and_the_stripped_name_returned` |
| AC2 — numbered listing; `expense delete 2` prints `deleted expense 2`; the rest renumber; the last one leaves `no expenses` | `cli.expense_list` prints `index + 1`; `store.delete_expense` pops the position, so renumbering is a consequence of the list | `tests.test_cli.WI0004AC2DeletingAnExpenseAndTheRenumberingThatFollows` — `test_the_listing_numbers_its_lines_from_one` (first fields `["1", "2"]`, rest of each line unchanged from WI-0001 AC3), `test_deleting_the_second_leaves_the_taxi_renumbered_to_one` (stdout exactly `"deleted expense 2\n"`, then one line beginning `1` for the 30.00 taxi), `test_deleting_the_last_one_leaves_no_expenses` (`"no expenses\n"`). Store-level: `tests.test_store.DeleteExpenseTests` (first, last, all-in-turn) |
| AC3 — `person delete Ben` and `person delete Ana` refused, stdout empty, stderr names the person and `2`, file bytes unchanged | `store.delete_person` raises `ExpensesError("%s is named in %d expense(s); delete those first")` before touching `data`; the handler never reaches `save()` | `tests.test_cli.WI0004AC3DeletingAPersonNamedInAnExpenseIsRefused.test_both_ana_and_ben_are_refused_with_their_name_and_the_count` — subtests for `Ben` and `Ana`, each asserting non-zero exit, stdout `""`, the name and `"2"` in stderr, `hashlib.md5(store.read_bytes())` equal before and after, and `person list` still `"Ana\nBen\n"`. Store-level: `tests.test_store.DeletePersonTests.test_a_person_named_in_an_expense_is_refused_with_the_name_and_the_count` |
| AC4 — with both expenses gone, `person delete Ben` exits 0 and prints `deleted Ben` | the refusal is computed from `naming_expenses`, so it lifts when the expenses go | `tests.test_cli.WI0004AC4TheRefusalIsAboutTheExpensesNotThePerson.test_ben_can_go_once_both_expenses_have`. Store-level: `tests.test_store.DeletePersonTests.test_the_refusal_lifts_once_the_expenses_are_gone` |
| AC5 — deletions survive the process exiting | each handler calls `store.save()` on success, so the deletion is on disk before the process ends | `tests.test_cli.WI0004AC5DeletionsSurviveTheProcessExiting` — `test_a_deleted_person_is_still_gone_from_a_fresh_process` and `test_a_deleted_expense_is_still_gone_from_a_fresh_process`, both running `subprocess.run([sys.executable, "-m", "expenses"], ...)` and comparing its stdout with the in-process listing |
| AC6 — `settle` follows the deletion; a refused `person delete` leaves it byte-identical | `settle.py` is untouched; ADR-0007's invariant is what keeps it correct | `tests.test_cli.WI0004AC6TheSettlementFollowsTheDeletion` — `test_deleting_the_expense_squares_the_group` (`"Ben pays Ana 15.00\n"` then `"no payments needed\n"`), `test_a_refused_person_deletion_leaves_the_settlement_byte_identical`, and `test_no_name_settle_computes_over_is_missing_from_person_list` |
| AC7 — seven refusals against the two-expense store, two against an empty one | `delete_person` refuses an unknown, wrong-cased or empty name; `parse_position` refuses `0`, `-1` and `abc`; `delete_expense` refuses out of range; nothing calls `save()` on any of these paths | `tests.test_cli.WI0004AC7DeletingSomethingThatIsNotThereIsRefused` — `test_every_case_against_the_two_expense_store_changes_nothing` loops all seven of the item's argument vectors as subtests, each asserting non-zero exit, stdout `""`, non-empty stderr and an unchanged md5; `test_against_an_empty_store_neither_deletion_creates_a_file` covers the two empty-store cases, asserting `self.store.exists()` is false afterwards. Store-level: `tests.test_store.DeletePersonTests.test_an_unknown_name_a_wrong_case_and_an_empty_name_are_all_refused`, `tests.test_store.DeleteExpenseTests.test_zero_negative_and_out_of_range_are_refused_and_change_nothing`, `tests.test_store.DeletionsLeaveTheFileAloneWhenRefusedTests` |
| AC8 — `README.md` documents both commands, the numbered sample, the refusal and the renumbering | `README.md` gains a `person delete` section, an `expense delete` section, and a renumbered `expense list` sample | Read `README.md`: (a) `### \`person delete <NAME>\`` and `### \`expense delete <NUMBER>\`` each show a worked example with the line it prints — `deleted Ben` and `deleted expense 2`; (b) the `expense list` sample is `1  2026-08-01  …` / `2  2026-08-02  …`; (c) "**Deleting a person named in a recorded expense is refused**, and the message says how many expenses stand in the way. Delete those expenses first, and then the person"; (d) "**The numbers renumber after a deletion.** … delete expense 2 and what was 3 becomes the new 2". Partly automated by `tests.test_cli.WI0004AC8TheReadmeDocumentsBothCommands` — see the deviation below |

Verification of AC7's `expense delete -1` case was run by hand as well as by test, because it is
the one argument argparse could have intercepted:

```
$ EXPENSES_STORE=/tmp/wi4store.json python3 -m expenses expense delete -1
expense '-1' is not a positive whole number
  exit=2
```

argparse's negative-number matcher passes `-1` through as a positional, because no option string
on that subparser looks like a negative number. It therefore reaches `parse_position` and comes
back as this tool's ordinary refusal, which is what AC7 requires of all seven cases alike.

## Deviations from the plan

1. **A test class was added for AC8, which the plan's fourth assumption said would not be.** The
   plan's reasoning was that a test would "pin wording that AC8 deliberately leaves open", and it
   recorded the reversal cost as "a new test class and nothing else". The class added,
   `WI0004AC8TheReadmeDocumentsBothCommands`, pins only things AC8 itself fixes: the two literal
   command strings AC8(a) names, the two output lines AC1 and AC2 already fix exactly, and AC8(b)'s
   requirement that every sample listing line begin with the position. It asserts nothing about
   the prose of AC8(c) or AC8(d), which is where the wording is genuinely open — `verify` still
   reads those. This changes how a criterion is demonstrated, not what is delivered.
2. **`delete_person` refuses an empty name with `'' is not in the group` rather than a bare
   ` is not in the group`.** The plan's contract for the function wrote this refusal as
   `"..." is not in the group`; interpolating an empty name into `add_expense`'s message shape
   directly would have produced a message beginning with a space and naming nothing. The name is
   quoted with `%r` in that one branch. AC7 requires only a message on stderr.
3. **`store.delete_expense`'s refusal message is `there is no expense <n>`.** The plan's step 3
   required a message "naming the number" without fixing the string; this is that string. No
   criterion constrains it.

4. **AC7 has seven argument vectors against the two-expense store, not nine.** The plan's AC
   mapping table says "a class looping the nine argument vectors"; AC7 as written in `item.md`
   enumerates seven (`person delete Nobody`, `person delete ana`, `person delete ""`,
   `expense delete 3`, `expense delete 0`, `expense delete -1`, `expense delete abc`), plus the
   two empty-store cases the plan counts separately in the same row. The test covers exactly what
   the criterion names; the plan's "nine" appears to be a miscount of the criterion rather than a
   requirement for two more cases.

Nothing else departs from the plan. Steps 1–11 were executed in order.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 120 tests`, `OK`, on the branch head `ff28637` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records that this project installs nothing and the standard library ships no linter. This gate checked nothing |
| `workspace-valid` | **pass** | `.claude/agile-skills/scripts/validate-workspace .` → exit 0, `7 item(s), 9 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-has-a-test` | **pass** | the table above names a test function for AC1–AC7 and both the reading and the partial test coverage for AC8 |
| `commits-reference-the-item` | **pass** | `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → exit 0, `all 2 commit(s) on main..wi/WI-0004 name WI-0004` |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main..HEAD --stat`: `README.md` (step 10), `expenses/cli.py` (steps 4–6), `expenses/store.py` (steps 1–3), `tests/test_cli.py` (steps 7 and 9), `tests/test_store.py` (step 8), and the tracker's own record of this execution. No hunk is outside those steps |
| `claims-are-sourced` | **pass** | `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0. It reports `checked no documents changed since main`: this item changed no file under `docs/`, and `README.md` is outside the set that script inspects. The `[src: …]` markers added to `README.md` were checked by hand against the two ADR filenames on disk |

## What I did not do

- **BUG-0002 is not fixed here**, although `person delete` and `expense delete` add two more
  callers of `store.save()` and so two more commands that would produce a traceback rather than a
  message if the operating system refused the write. The plan excludes it explicitly; it has its
  own item.
- ~~**`docs/architecture/overview.md` was not updated.** The plan's approach section states the
  one-way layering is unchanged and lists no step for it; the two new store functions and two new
  handlers sit inside layers the overview already describes.~~
  **Corrected after the send-back.** This bullet was the defect, not a handover. The document was
  not merely un-updated: its `## What is coming` section described *this item's delivered work* as
  forthcoming, and while doing so claimed `store.py` gains "two new functions" when it gains three
  [src: tracker/items/WI-0004/artifacts/review.md]. Declaring an omission does not make it
  admissible when a Definition of Done criterion requires it. It is fixed in `## Round 2` below.
  The reasoning above is also wrong on its own terms — "the layering is unchanged" was true and
  irrelevant, because D7 is about documents the change *invalidated*, not about documents the
  change restructured. Also note the count in that very bullet: "the two new store functions".
  There were three. The plan's `## Approach` summary says two, and every restatement of it —
  the overview, this bullet — inherited the miscount without anyone opening `store.py`.
- **No test asserts the prose of AC8(c) or AC8(d).** `verify` reads the README for those two, as
  the plan intended. Named here so it is a handover rather than a discovery.
- **`store.VERSION` and the stored record shape are untouched**, and no migration path was added.
  ADR-0006 chose the position handle precisely to avoid needing one.

---

## Round 2 — the fix for the send-back on D7 and D12

`review-close` rejected this item at 2026-08-27T01:27:21Z, back to `in-progress`, on one finding:
F1 in `tracker/items/WI-0004/artifacts/review.md`. Its verdict on the change itself was that the
code is sound — eight criteria evidenced, a diff mapping hunk-for-hunk onto the plan, no ADR
contradicted, no unrequested scope, a clean trial merge with 120 tests passing. What failed was
the record of it in `docs/`.

### What was built

One document, `docs/architecture/overview.md`, at **version 5**. No code file, no test and no
acceptance criterion was touched; `git diff af331b8..HEAD --stat` is that one file. F1 named four
things and all four are done:

1. **Deletion left `## What is coming` for the body.** The `expenses/store.py` and
   `expenses/cli.py` entries under `## The pieces, and why each exists` now describe the delivered
   commands. This is the same move version 3 made for `settle` when WI-0002 delivered it.
2. **The count is right.** The store.py piece names the three functions — `naming_expenses`,
   `delete_person`, `delete_expense` — rather than repeating "two". Checked against
   `grep -n "^def " expenses/store.py`, which is what nobody did the first time.
3. **ADR-0007's invariant is stated where the code that enforces it is described**, as a property
   of the delivered code with its two write points named, rather than as a plan.
4. **`## What is coming` keeps WI-0003**, which is still coming, and now says it will have to
   honour that invariant.

The change-log row and the `version`/`updated`/`updated-by`/`updated-for` header fields were
updated with it, which is the D7 requirement in full.

### Acceptance criteria evidence

**Unchanged from round 1, and deliberately so.** No acceptance criterion covers
`docs/architecture/overview.md` — AC8 is about `README.md`, which round 1 delivered and `verify`
checked. The evidence table above stands as written; the tests it names all still pass. The
send-back was on the Definition of **Done**, which is `review-close`'s list, not this item's
criteria. Re-running the suite confirms round 2 changed nothing they cover: `Ran 120 tests`, `OK`
— the same 120 as round 1, because no test was added or removed.

### Every claim round 2 wrote, and what was opened to check it

D12 is what caught the first version of this document. Each new claim was checked against the
code rather than against the plan, the review or a neighbouring sentence:

| claim written | what was opened | verdict |
|---------------|-----------------|---------|
| "WI-0004 added three module-level functions here — `naming_expenses`, `delete_person` and `delete_expense`" | `grep -n "^def " expenses/store.py` → eleven functions, three of them these | **true** |
| "The first reports every stored expense that names a given person, as `paid_by`, in `shared_by`, or as a key of `shares_minor`" | `expenses/store.py:126-142` — the three-way `or` in `naming_expenses` | **true** |
| "`delete_person` … refuses while any expense still names the person and says how many do" | `expenses/store.py:151-155` — `"%s is named in %d expense(s); delete those first" % (stripped, len(named_in))` | **true** |
| "Nothing was added to `load`" | `git diff main..wi/WI-0004 -- expenses/store.py` — one hunk, at `@@ -121,3 +121,47 @@`, zero deleted lines; `load` is at line 33 and outside it | **true** |
| "`VERSION` is still 1" | `expenses/store.py:15` | **true** |
| "Each noun has three actions: `add`, `list` and `delete`" | `expenses/cli.py:32,34,35` (person) and `:42,53,54` (expense) | **true** |
| "`expense list` prints that position as its leading column" | `expenses/cli.py:139-147` — `"%d  %s  %s  paid by %s  shared by %s" % (position, …)` over `enumerate(recorded, start=1)` | **true** |
| "after a deletion the remaining expenses renumber" | `expenses/store.py:162-166` — `recorded.pop(number - 1)` on the stored list, which `expense list` re-enumerates | **true** |

### Deviations from the plan

**One, and it is the send-back itself.** The plan has no step for
`docs/architecture/overview.md`; its eleven steps stop at the README and the gate run. Round 2
executes work the plan does not contain, because Definition of Done D7 requires it and
`review-close` instructed it concretely. Nothing about the design changed: no ADR was added,
amended or superseded, no acceptance criterion was touched, and no code moved. Round 1's four
declared deviations stand as written and were re-read and confirmed by the review (its finding
F3).

That the plan omitted this step is worth carrying forward: `plan` wrote the overview's version 4
itself, under "What is coming", and did not plan the step that moves it into the body on delivery
— even though version 3's change-log row shows exactly that move being made for WI-0002.

### Gates — re-run on the branch head `e2a0b3d`

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 120 tests in 1.204s`, `OK` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records why this project has no linter. This gate checked nothing, in round 2 as in round 1 |
| `workspace-valid` | **pass** | `.claude/agile-skills/scripts/validate-workspace .` → exit 0 |
| `every-criterion-has-a-test` | **pass** | the round-1 evidence table names a test function for AC1–AC7 and the reading plus the partial test class for AC8; round 2 changed no criterion and no test |
| `commits-reference-the-item` | **pass** | `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → exit 0, `all 6 commit(s) on main..wi/WI-0004 name WI-0004` |
| `no-unplanned-scope` (advisory) | **pass** | `git diff af331b8..HEAD --stat` → `docs/architecture/overview.md` only. It traces to Definition of Done D7 and to review finding F1 rather than to a plan step; see the deviation above |
| `claims-are-sourced` | **pass** | `.claude/agile-skills/scripts/lint-claims --changed-since main` → exit 0, `checked 1 document(s) changed since main`, `0 errors, 0 warnings`. Unlike round 1, this gate had something to check: round 2 is the first change this item made under `docs/` |

### What I did not do in round 2

- **F2 was left alone, deliberately.** `naming_expenses` returns `(position, expense)` pairs and
  `delete_person` reads only `len()` of them. The review recorded this as non-blocking and said
  explicitly not to change it as part of this fix, because the shape is the architect's and
  narrowing it would be scope no criterion covers.
- **No other document was touched.** `docs/product/vision.md` was audited by the review and its
  deletion claim is true in the present tense [src: tracker/items/WI-0004/artifacts/review.md];
  ADR-0006 and ADR-0007 were audited claim by claim and all four of their audited claims hold.
- **BUG-0002 is still not fixed here**, for the same reason as in round 1: it has its own item.
- **The two gaps `verify` declared are still open and still need recording in `item.md`'s
  `## Notes` when this item closes**, per the review's `## Accepted gaps`: that `lint-clean`
  checks nothing on this project (ADR-0004), and that AC8(c) and AC8(d) are verified by reading
  only, so a future edit removing those two README sentences would not be caught by the suite.
  Those are `review-close`'s to record at the close, not this skill's.
- **Nothing was merged.** The branch is left at `e2a0b3d`, unmerged, for `verify` and then
  `review-close`. Note for whoever runs the next trial merge: `git worktree add <path> main`
  checks out the real trunk branch and is not a throwaway copy of it — the last review did that
  and fast-forwarded `main` before rewinding it [src: tracker/items/WI-0004/artifacts/review.md].

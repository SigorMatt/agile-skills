# Implementation report — WI-0001

> **Third pass, 2026-08-21.** `review-close` rejected the second pass with four findings
> (`artifacts/review.md` F1–F4). F1, F2 and F3 are fixed; F4 was accepted by the review and is
> deliberately untouched. What changed is in `## Third pass — the review's F1, F2 and F3` at the
> end of this file. **AC8's evidence row below is superseded by it**: the second pass's AC8
> coverage was real but never reached a store that passes `store.load()`, which is where the
> traceback was.
>
> **Second pass, 2026-08-21.** `review-close` rejected the first pass with two findings
> (`artifacts/review.md` Findings 1 and 2). Both are fixed; what changed is in
> `## Second pass — the two review findings` at the end of this file. Everything above that
> section describes the first pass and is left as it was written, because the record is
> append-only in spirit: it says what was believed at the time. Two statements in it are now
> superseded and are marked there.

## What was built

Five modules and two test files, on `wi/WI-0001`, following `plan.md` steps 1–7 in order.

- `expenses/__init__.py`, `expenses/__main__.py` — `python3 -m expenses` runs.
- `expenses/errors.py` — `ExpensesError`, the single failure type.
- `expenses/store.py` — `store_path()`, `empty()`, `load()`, `save()`. The only module that knows
  the path or the format.
- `expenses/people.py` — `normalise()`, `match_key()`, `add()`, `listing()`. Pure; no I/O.
  *(Superseded: in the first pass `match_key()` was defined but never called. Fixed in the second
  pass; see the end of this file.)*
- `expenses/cli.py` — `argparse` with `add-person NAME` and `people`; the only layer that prints
  or chooses an exit status.
- `tests/test_store.py` (5 tests), `tests/test_cli.py` (13 tests).

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `cli.build_parser` registers both subcommands; `cmd_people` prints one bare name per line in list order | `tests/test_cli.py::CliTest::test_help_lists_both_commands`; `::test_listing_prints_one_bare_name_per_line_in_insertion_order` asserts stdout is exactly `"Alice\nBob\n"` |
| AC2 | `store.save` writes JSON to disk; `store.load` reads it back | `::test_the_roster_survives_into_a_fresh_process` — three separate `subprocess.run` interpreters, the third asserting `"Alice\nBob\n"` |
| AC3 | `people.add` compares `existing.lower()` against `normalise(name).lower()` and raises naming the person already there; the stored spelling is the first one appended | `::test_a_duplicate_is_refused_however_it_is_spelled` (subTests `Alice`, `alice`, `ALICE`, `"  Alice  "`, each asserting non-zero exit, `Alice` on stderr, and the listing still exactly `"Alice\n"`); `::test_the_first_spelling_is_the_one_kept` |
| AC4 | `cmd_people` prints the empty-group message and returns 0 when the roster is empty | `::test_listing_an_empty_group_succeeds_and_says_so` |
| AC5 | `store.load` returns `empty()` on `FileNotFoundError`; `store.save` calls `mkdir(parents=True)` | `tests/test_store.py::test_missing_store_loads_as_an_empty_group`, `::test_save_creates_missing_parent_directories`; `tests/test_cli.py::test_the_store_is_created_on_first_use_with_no_setup_step` |
| AC6 | `store.load` raises `ExpensesError` naming the path on unparseable JSON or a document that is not a store; `cmd_add_person` calls `load()` before `save()`, so a write aborts first | `tests/test_cli.py::test_a_damaged_store_is_fatal_to_reads_and_writes_and_is_left_alone` (subTests `people` and `add-person Bob`, each comparing the file's bytes before and after); `tests/test_store.py::test_damaged_store_is_fatal_to_reads_and_is_left_alone`, `::test_a_store_that_is_json_but_not_a_store_is_fatal` |
| AC7 | `people.normalise` raises on `None`, on empty, and on whitespace-only; argparse handles the missing argument | `::test_an_empty_or_missing_name_is_refused` (subTests `""`, `"   "`, and no argument, each also asserting the roster is still empty) |
| AC8 | `cli.main` has one `except ExpensesError` that prints to stderr and returns 2; nothing below `cli` imports `sys` or prints | `assertFailedCleanly()` is applied in every failing case in `tests/test_cli.py` — 9 invocations across 5 tests — asserting non-zero exit, no `"Traceback"` in either stream, non-empty stderr and empty stdout. `::test_no_command_at_all_fails_cleanly` and `::test_an_unknown_command_fails_cleanly` cover the argparse paths |

Two tests exist for `ADR-0006` rather than for a criterion, and are declared here rather than
left for `verify` to wonder about: `::test_a_name_containing_a_newline_is_refused` and
`::test_a_name_may_contain_a_comma_and_non_ascii_text`. They pin down the name rule the ADR
decided, which AC7 alone does not reach.

## Deviations from the plan

- **`store.load` validates the document's *shape*, not only that it is JSON.** The plan said
  "parses to something that is not a dict with the expected keys" raises, so this is the plan
  executed rather than departed from; it is called out because the resulting behaviour — a store
  containing `["Alice", "Bob"]` is refused — is one a reader might not expect from AC6's wording,
  which speaks of a file that "cannot be read or parsed".
- **`main()` takes optional `out` and `err` streams.** Not in the plan. It costs two lines and
  makes the domain testable in-process later without a subprocess; the end-to-end tests do not use
  it, because AC2 and AC8 must cross the process boundary. No behaviour depends on it.
- **`.gitignore`** was modified and then reverted in commit `7d02a68`: rules that were already
  present were appended by mistake. The net diff for this item contains no `.gitignore` change.
  Recorded because the mistaken commit is in the history and a reviewer will see it.

## Gates

Run on the branch head (`7d02a68`), after the last change.

- `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 18 tests
  … OK`.
- `lint-clean` → **skipped**, not passed. `tracker/project.yaml` has `commands.lint: null` by
  decision, because there is no linter in the standard library — `ADR-0001` §4, which also says
  any skill recording this skip should say so rather than letting it read as an oversight.
- `workspace-valid` → **pass**. `validate-workspace` → exit 0, 0 errors, 0 warnings. It reported
  `journal.execution.missing` in the window between the `in-progress` transition and this journal
  entry; see the journal.
- `every-criterion-has-a-test` → **pass**. Every one of AC1–AC8 has a row above naming a test by
  its full name, and no row says "implemented" or "see the code".
- `commits-reference-the-item` → **pass**. `git log --grep WI-0001 --oneline` returns every commit
  on this branch; each subject follows `<scope>: <summary> (refs WI-0001)`.

## What I did not do

- **No `verify`-side check that a test would fail if the behaviour were removed.** The tests
  assert on exact stdout, on exit status, and on the file's bytes before and after, so they are
  not vacuous — but I did not mutate the implementation to confirm each one goes red. That is
  worth `verify` doing for AC3 and AC6 in particular, where the assertion is about something
  *not* changing.
- **`str.lower()` rather than `str.casefold()`** for AC3's comparison. `ADR-0006` records this as
  accepted; a name whose case mapping is multi-character would be treated as two people. Not
  tested, because the ADR declines to require it.
- **Nothing for WI-0002 or WI-0003.** `money.py`, `expenses.py`, `balances.py` and `settle.py` are
  named in `docs/architecture/overview.md` and were deliberately not created, per the plan's
  `## Out of scope for this item`.
- **The empty-group and confirmation wording is asserted by substring only** ("Nobody",
  "Alice"), per the plan's assumption 4, so the exact sentences stay changeable.

## Second pass — the two review findings

`review-close` rejected the first pass. Neither finding was a failure of an acceptance criterion
— AC1–AC8 were met and stay ticked, and **no criterion was edited** — so this pass changed only
what the two findings named.

### Finding 1 — `match_key()` was dead and AC3's rule was written out twice

`plan.md` step 4 specifies `add()` as raising *"if `match_key` collides"*, and the first pass
inlined `stripped.lower()` and `existing.lower()` instead, leaving `match_key()` defined and
called by nothing. Fixed as the plan specified rather than by deleting the function, because
`match_key` is the name the plan gives AC3's comparison key and WI-0002 needs exactly that key to
match a sharer against the roster:

```python
    key = match_key(stripped)
    for existing in data["people"]:
        if match_key(existing) == key:
```

`match_key`'s docstring now says it is the single place the rule lives, so the next person to
revisit `str.lower()` versus `casefold()` — which `ADR-0006` line 92 records as a known-imperfect
choice — changes one function and not two.

The review said "either wire it in, or delete it and say so". Wiring it in was chosen: deleting it
would have left WI-0002 to re-derive the rule, which is the same duplication arriving one item
later.

### Finding 2 — the ordering tests could not distinguish insertion order from alphabetical order

Both ordering tests used `Alice` then `Bob`, and `sorted(["Alice", "Bob"])` is unchanged, so
`listing()` could have been replaced by `sorted(...)` with the suite green. The test data is now
`Alice`, `Zoe`, `Carol` — deliberately not alphabetical — in both
`test_listing_prints_one_bare_name_per_line_in_insertion_order` and
`test_the_roster_survives_into_a_fresh_process`, each asserting `"Alice\nZoe\nCarol\n"`.

### One test added

`tests/test_cli.py::test_matching_goes_through_one_key_function` — asserts
`people.match_key("  ALICE  ") == people.match_key("alice")` directly, and then that the CLI
refuses the duplicate. The direct assertion is what keeps `match_key` referenced by a test as well
as by production code, so it cannot become unreferenced again without a test going red.

### Sensitivity confirmed by mutation, not assumed

This is what the first pass declared under `## What I did not do` and what the review found. Each
behaviour was disabled, the suite run, and the file restored:

| behaviour disabled | how | result |
|--------------------|-----|--------|
| insertion order | `listing()` returns `sorted(data["people"])` | **red** — `test_listing_prints_one_bare_name_per_line_in_insertion_order`, `test_the_roster_survives_into_a_fresh_process` |
| the single matching rule | `if existing == stripped` instead of comparing `match_key`s | **red** — `test_a_duplicate_is_refused_however_it_is_spelled`, `test_matching_goes_through_one_key_function` |

Both mutations left the suite green before this pass. Tree restored afterwards and re-run: exit 0,
19 tests, `OK`.

### Gates, second pass

Run on the branch head after the last change.

- `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 19 tests`,
  `OK`.
- `lint-clean` → **skipped**, not passed. `commands.lint` is null by `ADR-0001` §4. Worth noting
  against Finding 1: a dead function is exactly what a linter would have caught, and this project
  has decided to have none. Recorded in `item.md` `## Accepted gaps` by `review-close`.
- `workspace-valid` → **pass**. Exit 0, 0 errors, 0 warnings.
- `every-criterion-has-a-test` → **pass**. The first pass's mapping table above is unchanged;
  AC1 and AC2 now additionally have test data that can actually fail.
- `commits-reference-the-item` → **pass**. Exit 0, all commits on `main..wi/WI-0001` name WI-0001,
  including this pass's `fix:` commit. (`review-close` repaired the branch topology that made this
  gate fail before; see `review.md` Finding 3.)

### What I did not do, second pass

- **Nothing else in the review was actioned, deliberately.** Findings 3, 4 and 5 were not for this
  skill: 3 was repaired by `review-close` itself, 4 is a journal correction, and 5 is an accepted
  gap now recorded in `item.md` `## Accepted gaps`.
- **The bare-invocation behaviour was left exactly as it is.** It is an accepted gap, not a
  defect, and changing it here would be the "fixing things you noticed on the way" this skill is
  told not to do.
- **No acceptance criterion was touched.** All eight remain ticked from the first verification;
  `verify` decides whether those ticks still stand against the new commit.

---

## Third pass — the review's F1, F2 and F3

`review-close` rejected the second pass (`artifacts/review.md`, 2026-08-21T03:23:10Z) with four
findings. F1, F2 and F3 are actioned here; F4 was recorded by the review as an accepted gap and
written into `item.md`, so it is deliberately **not** touched — see `## What I did not do, third
pass`.

The findings are not the same defect twice. The first review's two are confirmed still fixed
(`match_key` is still the single home of the comparison rule; the ordering tests still use
`Alice/Zoe/Carol`). What the review found this time is a class of input nobody upstream had
tried: a store that **passes** `store.load()`'s shape check and then breaks something above it.

Commit: `fcf3cf4 fix: reject a roster entry that is not a name, stop match_key validating, and
back cli.main with a catch-all (refs WI-0001)`.

### F1 — a store whose `people` list holds a non-string reached the user as a traceback

`store.load()` checked that `people` and `expenses` were lists. It never checked what was in
them, so `{"version":1,"people":[123],"expenses":[]}` parsed cleanly, and the first thing above
the store that touched an element — `people.normalise()`, via `match_key(existing)` — raised
`AttributeError`. `cli.main` caught `ExpensesError` and nothing else, so it escaped: exit 1, and a
traceback on stderr. AC8 forbids that without qualification.

**The change**, in `store.load()`, after the existing top-level shape check:

```python
for entry in data["people"]:
    if not isinstance(entry, str):
        raise ExpensesError(
            "cannot read {}: its list of people contains {}, which is not a name. "
            "Nothing has been changed; fix or move the file and try again.".format(
                path, type(entry).__name__
            )
        )
```

It is in `store` and not in `cli` or `people` on purpose. `overview.md` says everything above the
store "sees a plain dictionary", and that promise has to hold at the *element* level or it is not
a promise — a caller that has to re-check what the store handed it is doing the store's job. One
check here fixes both commands and every future caller at once.

Verified by running it, not by reasoning about it. For each of `[123]`, `[{"name":"Alice"}]`,
`[["Alice"]]` and `[None]`, **both** commands now exit 2 with no traceback and this on stderr:

```
cannot read <path>: its list of people contains int, which is not a name.
Nothing has been changed; fix or move the file and try again.
```

and the file's bytes are unchanged. That closes the read-path half of the finding too: `python3 -m
expenses people` used to exit **0** and print `123` as a member of the group, which missed
`ADR-0002` decision 6 just as badly as the crash did.

### F2 — a bad name already in the store blamed the name being typed

`add()` compared through `match_key(existing)`, and `match_key` called `normalise`, which
*validates*. So every name already in the roster was re-validated on every add, and a stored name
that today's rules reject made the **new** name look wrong: with `Al\x07ice` in the store,
`add-person Carol` failed with `a name cannot contain control characters (found '\x07')`.

**The change** is one line in `match_key`, plus the docstring that says why:

```python
def match_key(name):
    return name.strip().lower()          # was: normalise(name).lower()
```

The obvious alternative — a separate key function for the stored side — was rejected because it
recreates the first review's Finding 1 exactly: the comparison rule written in two places, drifting
apart. Splitting *validation* from *comparison* instead keeps one key function used on both sides,
which is what that finding asked for, and puts validation where it belongs: at the point a name
enters the roster, once, on the input side. `add()` still calls `normalise` on its argument first,
so nothing about what may be *added* has changed.

Now: with `Al\x07ice` and `Bob` stored, `add-person Carol` exits 0, and `people` prints
`Al\x07ice`, `Bob`, `Carol`. The bad name is left alone rather than being repaired or rejected —
see `## What I did not do, third pass`.

### F3 — the architecture overview stated something that was not true

`overview.md` v1 claimed the no-traceback property was *"a property of one function rather than a
discipline applied everywhere"*. F1 was the counter-example. There were two ways to resolve it:
correct the document, or make the code match the claim. **Both** were done, and the second is the
substantive one.

`cli.main` now has a second handler behind the first:

```python
except Exception as exc:
    print("an internal error in expenses ({}: {}). This is a bug in the tool, "
          "not something you did wrong.".format(type(exc).__name__, exc), file=err)
    return FAILURE
```

Three deliberate details:

- **It reports rather than swallows.** The exception type and message are on the line, so the
  failure stays diagnosable without a traceback, and it says plainly whose fault it is.
- **`BaseException` is not caught**, so `KeyboardInterrupt` and `SystemExit` are unaffected.
- **It does not claim "nothing was written."** An unexpected failure can land after
  `store.save()`, and a reassurance this function cannot verify is worse than none.

This deviates from `plan.md` step 5, which says `cli.main` "dispatches, catching `ExpensesError`
once", and the deviation is declared in `## Deviations from the plan, third pass` rather than
folded in quietly.

`overview.md` is at **v2** with a change-log row: the `cli` bullet now states both handlers and
says which one is load-bearing; the `store` bullet says the plain-dictionary promise has to hold
at element level; the module diagram says what damage detection actually covers.
`expenses/errors.py`'s docstring made the same false claim in the same words and was corrected
too — the review noted the sentence had spread to three places, which is the pattern `spec/dor-dod.md`
D12 exists to catch.

### Tests added, and confirmed sensitive

Four new tests, 19 → 23. Each was confirmed to **fail** with its fix reverted, and the source
restored afterwards — a test that passes against an absent implementation would make these
findings look closed forever.

| test | covers | with the fix reverted |
|------|--------|-----------------------|
| `test_store.py::test_a_roster_entry_that_is_not_a_string_is_fatal` | F1 at the store level; names the path and the offending type | `FAILED (failures=1)` |
| `test_cli.py::test_a_roster_entry_that_is_not_a_name_is_fatal_to_both_commands` | F1 end to end — six junk types × both commands, asserting exit, no traceback, the path on stderr, and unchanged bytes | `FAILED (failures=6)` |
| `test_cli.py::test_a_stored_name_todays_rules_would_reject_does_not_blame_the_new_name` | F2 — `add-person Carol` succeeds against a store holding a control-character name | `FAILED (failures=1)` |
| `test_cli.py::test_an_unexpected_exception_is_reported_not_dumped` | F3's backstop — `store.load` patched to raise `RuntimeError`, asserting exit 2, no traceback, empty stdout, and the type on stderr | `FAILED (failures=1)` |

The last one drives `cli.main` through its `out`/`err` parameters, which is the first thing in the
item to exercise them. That is a side effect, not a fix: F4 is still an accepted gap, because the
parameters remain unused by any *caller*.

### Deviations from the plan, third pass

1. **`cli.main` catches `Exception` as well as `ExpensesError`.** `plan.md` step 5 specifies one
   `except ExpensesError`, and its `## Acceptance criteria mapping` for AC8 assumes that is
   enough. It is not, and F1 is the proof. This changes behaviour a user could notice, so the test
   for whether it was mine to decide is whether a criterion covers it — AC8 does, unconditionally
   and in this item, so no question was filed. `plan.md`'s paragraph at lines 24–29 ("made true by
   construction rather than by remembering") is now the last uncorrected copy of the claim F3
   found; see below.
2. **`store.load()` validates the elements of `people`, which no plan step mentions.** `plan.md`
   step 3 describes `load` as raising "if it is not a store". Element types are the same check
   carried one level down, so this is *how* rather than *what*.

### Gates, third pass

Run on the branch head `fcf3cf4`, after the last change.

- `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 23 tests`,
  `OK`.
- `lint-clean` → **skipped, not passed**. `commands.lint` is null by `ADR-0001` §4. Worth repeating
  a third time: the `# noqa: BLE001` comment on the new catch-all names a rule no tool in this
  project enforces. It is there for the human reader.
- `workspace-valid` → **pass**. Exit 0, 0 errors, 0 warnings — after two failures on the
  `overview.md` change log, which wants rows newest-first and the top row's version to match the
  frontmatter. Both fixed before committing.
- `every-criterion-has-a-test` → **pass**. AC1–AC7's mapping is unchanged. AC8's is materially
  stronger: it was nine failing invocations reached through argument parsing or `load()`'s own
  rejection, and it now also covers a store that passes `load()` (six junk element types × two
  commands) and an arbitrary unexpected exception.
- `commits-reference-the-item` → **pass**. `check-commit-refs WI-0001 wi/WI-0001` → exit 0,
  `all 10 commit(s) on main..wi/WI-0001 name WI-0001`.

### What I did not do, third pass

- **F4 is untouched**, by design. `review-close` accepted it and wrote it into `item.md`
  `## Accepted gaps`; acting on an accepted gap would put a change in this diff that no finding
  asked for.
- **`plan.md` lines 24–29 still carry the corrected claim** — *"`cli.main()` wraps the whole
  dispatch in one `except ExpensesError` … There is then exactly one place to check, and adding a
  new failure later cannot forget the rule."* That is the third copy F3 identified, and it is now
  the only one left. It was **not** edited: `plan.md` is `plan`'s artifact and the reasoning it
  records was true when written. Flagging it is the honest move; rewriting another skill's record
  to match a later discovery is not. **`review-close` or `plan` should decide** whether it is
  amended in place or left as a historical record with a pointer.
- **`expenses` list elements are still unvalidated.** F1's fix covers `people` only. The same
  latent crash exists for expense records, but this item's commands never read them and WI-0002
  has not yet decided what an expense record *is* — inventing a schema here would pre-empt that
  item's plan. **WI-0002 must extend `store.load()`'s check when it defines the shape**, and it is
  named here so it is a handover rather than a rediscovery.
- **A stored name today's rules would reject is left in place**, not repaired and not rejected on
  read. Rejecting it would make a hand-edited store unusable rather than merely odd, which is a
  stricter contract than `ADR-0002` decision 6 asks for; repairing it would edit a user's file
  without being asked. The tool cannot create such a name, so it is only reachable by hand-editing.
- **Nothing was done about `argparse`'s two-line failures**, which `verify` flagged against AC8's
  "one-line" wording and `plan.md` step 5 chose deliberately. Unchanged and still that decision.

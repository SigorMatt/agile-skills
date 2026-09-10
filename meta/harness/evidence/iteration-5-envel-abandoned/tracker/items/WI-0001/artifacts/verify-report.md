# Verification report — WI-0001

Verified-commit: 6aacc951fbd9fa1b82ec797869a7065d097d7d20

Every command below was run by this execution against that commit, on branch `wi/WI-0001`, with
`PATH="$PWD/bin:$PATH"` and `ENVEL_FILE` inside a `mktemp -d` created fresh for each criterion.
Nothing here is taken from `impl-report.md`; the report was read after the criteria and after the
runs, and where it and this execution differ the difference is recorded.

## Verdict

**Pass.** All eleven acceptance criteria are satisfied, each by a command this execution ran, with
the output quoted. No criterion is `substituted` and none is `ambiguous`. No defect in this item's
own criteria was found, and no bug belonging to another item was found — WI-0001 is the first item
of the epic, so no delivered behaviour exists elsewhere to be broken.

One hard gate of the **previous** stage, `claims-are-sourced`, was recorded as failed and its
transition forced under `WI-0001/Q-003`. This execution re-ran it, confirms it still fails on the
same single line, and confirms the failure is not about this item's code. See `## Gates`.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `envel new groceries` on a fresh `ENVEL_FILE` | `exit=0`, `stdout=[]`, `stderr=[]`, `stderr_bytes=0` | "writes nothing to stderr" checked by byte count, not by eyeball |
| AC2 | **pass** | `envel list` immediately after AC1's command, `od -c` on stdout | `exit=0`; `g r o c e r i e s \n` and nothing else | "a line whose only content is `groceries`" checked byte for byte |
| AC3 | **pass** | `envel new a`; `envel new b`; `envel list` — three separate processes, one `ENVEL_FILE`, nothing in between | `exit=0` on each; `od -c` of the third: `a \n b \n` | the persistence criterion. Three real process invocations, not one in-process call |
| AC4 | **pass** | `envel new Zebra`; `envel new apple`; `envel new Ant`; `envel list` twice, `cmp` the two stdouts | `Ant`, `Zebra`, `apple`; `cmp` reports the two runs identical; `printf 'Ant\nZebra\napple\n' \| cmp -` matches | chosen so byte order and case-insensitive alphabetical order **disagree** — alphabetical would be `Ant, apple, Zebra`. A pass here cannot be got by sorting the easy way |
| AC5 | **pass** | (a) `envel new groceries` twice; (b) then `envel new Groceries`; `envel list` after each | (a) `exit=1`, stderr `envel: an envelope named 'groceries' already exists`; (b) `exit=1`, **same** stderr; `envel list` after each: `g r o c e r i e s \n`, `grep -c '^groceries$'` = 1 | both halves. The case half is the discriminating one: the message names the **stored** envelope, so `Groceries` does not appear |
| AC6 | **pass** | `ls -la` the temp dir and `test -e "$ENVEL_FILE"` first, then `envel list` | store absent confirmed; `exit=0`, stderr 0 bytes, 1 stdout line: `No envelopes yet. Create one with: envel new <name>` | this stdout is the **reference** AC9 and AC10 compare against; it was saved to a file and reused verbatim |
| AC7 | **pass** | `envel new Groceries` on an empty store, then `envel list`, `od -c` | `exit=0`; `G r o c e r i e s \n` | capitalisation survives; the store is not folded on the way in |
| AC8 | **pass** | `envel new "eating out"`, then `envel list`, `od -c` | `exit=0`; `e a t i n g   o u t \n` | the space is kept, and the line is the name and nothing else |
| AC9 | **pass** | `envel new ""`, then `envel list`, `cmp` against the AC6 reference file | `exit=1`, 1 stderr line `envel: an envelope name cannot be empty`; following list stdout **byte-identical** to the reference (`cmp -s` silent, exit 0) | also checked, beyond the criterion: the store file was still absent afterwards, so the refusal wrote nothing at all |
| AC10 | **pass** | `envel new "   "`, then `envel list`, `cmp` against the AC6 reference | `exit=1`, 1 stderr line `envel: an envelope name cannot be empty`; list stdout byte-identical to the reference | |
| AC11 | **pass** | `envel new groceries`; `envel new "  groceries  "`; `envel list`, `od -c`, `grep -c '^groceries$'` | second `exit=1`, stderr `envel: an envelope named 'groceries' already exists`; list: `g r o c e r i e s \n`, exact-match lines = 1 | the criterion's other half — "stored with leading and trailing whitespace removed" — was exercised separately on a fresh store: `envel new "  eating out  "` → `exit=0`, `envel list` gives `e a t i n g   o u t \n`, and the store file itself holds `"name": "eating out"` |

## ADR conformance

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|-----|---------|--------------------------------|-----------------------------------|
| `ADR-0001` | **conforms** | *"This project is written against the Python 3 standard library and declares no third-party dependency, for its runtime, its tests or its checks."* | Enumerated rather than eyeballed. Every `Import`/`ImportFrom` node in `envel/**.py`, `tests/**.py` and `bin/envel` was parsed with `ast` and each top-level module checked against `sys.stdlib_module_names`: `non-stdlib, non-local imports: none`. The import sites, in full: `envel/store.py:9`, `envel/store.py:10`, `envel/store.py:11` (`json`, `os`, `tempfile`); `envel/cli.py:11` (`sys`); `envel/envelopes.py:7` (`__future__` only); `tests/test_cli.py:9` to `tests/test_cli.py:12` (`os`, `subprocess`, `tempfile`, `unittest`); `tests/test_envelopes.py:3` (`unittest`); and the local `envel` at `envel/cli.py:13`. No `requirements.txt`, `pyproject.toml`, `setup.py` or `Pipfile` exists at the root. The two recorded commands were run by this execution: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests`, `OK`; `python3 -m compileall -q envel tests` → exit 0 |
| `ADR-0002` | **conforms** | *"The repository contains an executable file `bin/envel` with a `#!/usr/bin/env python3` shebang. It resolves the repository root from its own location, puts it at the front of `sys.path`, imports `envel.cli`, and exits with what `main()` returns"* | Each of the four acts, in order: shebang `bin/envel:1`; root resolved from `__file__` and inserted at index 0, `bin/envel:7`; `from envel.cli import main`, `bin/envel:9`; `raise SystemExit(main())`, `bin/envel:11`. The `main()` whose return value it exits with is `envel/cli.py:27`, and it returns an `int`. The demonstration form the ADR prescribes is the one every criterion above was run in. **Noted, not repaired:** the clause's trailing aside says *"four statements"* and the file contains five Python statements (`import os`, `import sys`, the `sys.path.insert`, the import of `main`, the `raise`). The four *acts* it names are each satisfied and each cited, so the binding content holds; the count is loose. `verify` writes no document, so this is recorded here and in `## Defects found` rather than edited |
| `ADR-0003` | **conforms** | *"`$ENVEL_FILE`, if it is set and not empty — used as given, without expansion or interpretation"*, and *"A store file that does not exist is an empty store and not an error"*, and *"replaces the file atomically: write a temporary file in the same directory, then `os.replace`"* | Path order at `envel/store.py:27`–`:36`: `ENVEL_FILE` returned unchanged, then `XDG_DATA_HOME`, then `~/.local/share/envel/store.json`. Every criterion above was observed **through** the `ENVEL_FILE` branch, so the first clause is exercised eleven times over. Absent-file-is-empty at `envel/store.py:45`–`:46`, and it is what AC6, AC9 and AC10 turn on. `os.replace` after `tempfile.mkstemp(dir=directory, ...)` at `envel/store.py:63`–`:69`. The document's shape was read off a real store written by the tool: `{"version": 1, "envelopes": [{"name": "eating out"}]}` — one JSON document, `version` present, `envelopes` a list of objects, UTF-8 with the characters as typed |
| `ADR-0004` | **conforms** | Rule 1: *"the message names the **stored** envelope rather than what was typed — `envel new Groceries` after `envel new groceries` must put `groceries` on stderr"*; rule 2: *"A name whose identity is empty is refused"*; and *"identity is `name.strip().casefold()`. Its display form is `name.strip()`"* | Rule 1 checked at the boundary that could break it, not the happy path: `envel new Groceries` after `envel new groceries` put `envel: an envelope named 'groceries' already exists` on stderr — `Groceries` does not appear. Implemented at `envel/envelopes.py:53` (`raise DuplicateName(clash["name"])`) and `envel/cli.py:56`. Rule 2 at `envel/envelopes.py:49`, exercised by AC9 and AC10, which cover the empty string and spaces-only with the one rule. Identity and display at `envel/envelopes.py:31` and `:36` |

No ADR outside the plan's binding list was found engaged by this change.

## Invalidation set

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/product/vision.md` | `owned-by-ending` | Left exactly as it is, and checked that this item left it so: `git diff main...HEAD -- docs/product/vision.md` is **empty**. The three `## Engagement state` bullets are false today — the epic has five children rather than three, the five intake questions are answered, and something has now been designed and built — and that is the disposition working, not a defect. `review-close` restates the section at the ending (`spec/doc-header.md` §4a, `spec/dor-dod.md` DE4). This execution wrote nothing here either |
| `docs/process/ways-of-working.md` | `to-update` | The document exists, at `version: 1`, with a `## Change log` row for that version naming `answer-questions` and WI-0001. Reopened against the branch head: its subject is `WI-0001/Q-003`, the convention it states is the one the previous stage acted under, and its two `[src:]` citations resolve — `.claude/agile-skills/spec/dor-dod.md` and `.claude/agile-skills/spec/doc-header.md` both exist. It was written by `answer-questions`, not by `implement`, and the set names it so that no path under `docs/` in the branch diff is unaccounted for |
| `docs/architecture/overview.md` | `to-update` | Updated: `version: 2`, with a `## Change log` row for version 2 naming `implement` and WI-0001. Reopened line by line against the branch head rather than accepted. Every citation in `## The shape` was resolved with `sed -n '<n>p'`: `bin/envel:9` → `from envel.cli import main`; `bin/envel:11` → `raise SystemExit(main())`; `envel/cli.py:27` → `def main(argv=None) -> int:`; `envel/cli.py:13` → `from envel import envelopes, store`; `envel/envelopes.py:29` → `def identity`; `:48` → `def add`; `:60` → `def listing`; `envel/store.py:27` → `def store_path`; `:39` → `def load`; `:58` → `def save`. "Eleven lines" — `wc -l < bin/envel` = 11. The dependency-direction sentence is the one that could most easily be stale, so it was checked as a claim about imports rather than read as prose: `envel/envelopes.py` imports only `from __future__ import annotations`, so it imports neither `os` nor `store`; `envel/store.py` contains no envelope rule. The sentence was already weakened by `implement` to what is checkable, and what it now says is true |

No entry is disposed `verified-still-true`, so no such claim was outstanding. No entry was left without a disposition.

## Gates

- `tests-pass` → **pass**. This execution ran `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests in 1.014s`, `OK`, on `6aacc95`.
- `lint-clean` → **pass**. `python3 -m compileall -q envel tests` → exit 0.
- `workspace-valid` → **pass**. `scripts/validate-workspace .` → exit 0, `checked 6 item(s), 7 document(s)`, `0 errors, 0 warnings`.
- `every-criterion-independently-checked` → **pass**. The `## Criteria` table's `command run` and `actual output` columns are this execution's own runs. What each criterion needed was derived from its sentence before `impl-report.md` was opened; AC4's and AC5's cases were chosen to be ones a wrong implementation would fail, which is why AC4 uses `Ant`/`Zebra`/`apple` and AC5 checks that `Groceries` is **absent** from stderr.
- `negative-cases-exercised` → **pass**. Every criterion naming an error, an empty input or a missing file was triggered: AC5 (duplicate, twice — exact and case), AC6 (missing store, confirmed missing with `test -e` first), AC9 (empty name), AC10 (whitespace-only name), AC11 (duplicate after trimming). Beyond the criteria, and reported below: no arguments, `new` with none and with two, `list` with an argument, an unknown command, and a corrupt store on both commands.
- `a-criterion-about-criteria-is-read` → **pass**, vacuously and by enumeration rather than by assumption. AC1–AC11 were enumerated and read: the subject of every one is a command's exit status, its stdout or its stderr. None has an acceptance criterion as its subject, and WI-0001 is the epic's first item, so there are no earlier criteria for one to cover. The gate has nothing to bite on here; it will on WI-0002, whose AC set is written against this item's behaviour.
- `adr-conformance-is-decided` → **pass**. `scripts/lint-documents --rule adr-conformance-is-decided --item WI-0001` → exit 0 once `## ADR conformance` above existed. (It reported `document.adr.section.missing` when run before the report was written, which is what the rule is for.)
- `invalidation-set-is-disposed` → **pass**. `scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0001` → exit 0, same story.
- `tests-would-fail-without-the-change` → **pass** (advisory). See `## Test sensitivity check`.

**The gate this item carries forward.** `scripts/lint-claims --changed-since main --plan-documents WI-0001` → **exit 1**, one error, re-run by this execution at the branch head:

```
docs/product/vision.md:79: ERROR [claim.unsourced] an absolute claim ('no') about
'EP-001/Q-001' with no citation
```

It is `implement`'s gate, not one of this skill's nine, and it was recorded as failed and forced
under `WI-0001/Q-003`. This execution confirms independently that the finding is not about
WI-0001's code: line 79 is inside `docs/product/vision.md`'s `## Engagement state` section, and
`git diff main...HEAD -- docs/product/vision.md` is empty, so nothing on this branch wrote it.
`review-close` will meet the same error — it runs `lint-claims --all` — and
`docs/process/ways-of-working.md` records why.

## Negative and boundary cases exercised

Every one of these was run; the output is quoted from the run.

| condition | command | result |
|-----------|---------|--------|
| duplicate, exact | `envel new groceries` twice | `exit=1`, `envel: an envelope named 'groceries' already exists`, one line in `list` |
| duplicate, case only | `envel new Groceries` after `groceries` | `exit=1`, same message, `Groceries` **absent** from stderr |
| duplicate, whitespace only | `envel new "  groceries  "` after `groceries` | `exit=1`, same message, one line in `list` with no surrounding space |
| empty name | `envel new ""` | `exit=1`, `envel: an envelope name cannot be empty`; store file still **absent** afterwards |
| whitespace-only name | `envel new "   "` | `exit=1`, same message; `list` byte-identical to the AC6 reference |
| store missing | `envel list` with the path confirmed non-existent | `exit=0`, `No envelopes yet. Create one with: envel new <name>`, stderr empty |
| no arguments | `envel` | `exit=2`, `usage: envel new <name> \| envel list` |
| `new` with no name | `envel new` | `exit=2`, `usage: envel new <name>` |
| `new` with two names | `envel new a b` | `exit=2`, `usage: envel new <name>` |
| `list` with an argument | `envel list extra` | `exit=2`, `usage: envel list` |
| unknown command | `envel frobnicate` | `exit=2`, `envel: unknown command 'frobnicate'` then the usage line |
| corrupt store, read | `printf 'not json at all' > $ENVEL_FILE; envel list` | `exit=1`, `envel: <path> is not valid JSON: Expecting value: line 1 column 1 (char 0)` |
| corrupt store, write | `envel new x` against the same file | `exit=1`, same message, **and the file was left byte-for-byte as it was** (`not json at all`) |

The last row is the one worth having. Plan assumption P4 says a damaged store must not be treated
as empty, because the next `new` would overwrite it; that is a claim about data loss, so it was
checked by looking at the file afterwards rather than at the exit status.

## Test sensitivity check

Six mutations, applied one at a time to the branch head and reverted immediately. Each is a
plausible wrong implementation, not a syntax break, and the suite was restored to 24 passing
after every one (`git status --short` clean, `Ran 24 tests`, `OK`).

| # | mutation | tests that failed |
|---|----------|-------------------|
| M1 | `listing` sorts by `name.casefold()` instead of `name.encode("utf-8")` | 2 — `test_ac4_listing_is_sorted_byte_wise_and_repeatable`, `test_listing_is_byte_wise_ascending_not_alphabetical` |
| M2 | `identity` returns `name.strip()`, no `casefold` | 4 — `test_ac5_a_name_differing_only_in_case_is_refused`, `test_add_refuses_a_name_differing_only_in_case`, `test_duplicate_reports_the_stored_spelling_not_the_input`, `test_identity_folds_case` |
| M3 | `display` returns `name`, no `strip` | 2 — `test_add_stores_the_trimmed_name_as_typed`, `test_display_strips_but_does_not_fold` |
| M4 | the duplicate message prints `rest[0]` (what was typed) instead of `clash.existing` | 1 — `test_ac5_a_name_differing_only_in_case_is_refused` |
| M5 | `load` raises on an absent file instead of returning `empty()` | 10 — `test_ac1` … `test_ac8` and `test_ac11` end to end, and `test_ac6_list_before_anything_exists` |
| M6 | `add` no longer refuses an empty identity | 4 — `test_ac9_...`, `test_ac10_...`, `test_add_refuses_an_empty_name_and_changes_nothing`, `test_add_refuses_an_all_whitespace_name_and_changes_nothing` |

Per criterion, at least one test is sensitive: AC1, AC2, AC3, AC8 by M5; AC4 by M1; AC5 by M2 and
M4; AC6 by M5; AC7 and AC11's storage half by M3; AC9 and AC10 by M6; AC11's comparison half by
M5.

**One coverage gap, stated rather than glossed.** M3 — `display` stopping trimming — broke only
the two unit tests, and no end-to-end test. `test_ac7` uses `Groceries`, which has no surrounding
whitespace, and `test_ac11` passes `"  groceries  "` as a **duplicate**, so `add` raises before
`display` is reached. Nothing in `tests/test_cli.py` creates a *new* envelope from a name with
surrounding whitespace. This execution ran that case by hand — `envel new "  eating out  "` on a
fresh store lists `eating out` and stores `"name": "eating out"` — so AC11's storage half is
verified, by a command in this report rather than by the suite. It is not worth a send-back: the
behaviour is correct, the unit test `test_add_stores_the_trimmed_name_as_typed` is sensitive to
it, and the missing case is one line. It is written here so that WI-0002, which will add income
and spending against names, knows the end-to-end suite does not currently exercise
trim-on-create.

**A note on the first execution's own mutation run.** `impl-report.md` reports four mutations;
these six are this execution's, chosen independently from the criteria, and M3, M5 and M6 are not
among the developer's four. The overlap that exists (case folding, the echoed message) reproduced
the same result.

## Defects found

**None against this item's acceptance criteria, and no bug item filed.** WI-0001 is the epic's
first item; no behaviour delivered elsewhere exists for this change to have broken.

Two observations that are not defects and are recorded so `review-close` does not have to
rediscover them:

1. **`ADR-0002`'s "four statements" does not match the file's five Python statements.** The four
   acts the clause names are each satisfied and each cited (`bin/envel:1`, `:7`, `:9`, `:11`), so
   the decision holds and the verdict is `conforms`. The aside is loose rather than false under
   the reading that it enumerates the four acts just listed. `verify` writes no document, and this
   is neither a criterion failure nor behaviour delivered elsewhere, so it is recorded rather than
   sent back or filed. If the architect wants the sentence tightened, that is a one-line edit by
   `answer-questions` on some later question, not a round of its own.
2. **The store-failure message family is more specific than the plan's `## Approach` table
   suggests.** The table has one row, `envel: <path> could not be read as an envel store:
   <detail>`; the code raises five distinct sentences (`could not be read`, `is not valid JSON`,
   `is not an envel store: ...` ×3). This is not a deviation: plan **step 1** says a read error, a
   parse error or a bad shape "raises `StoreError` carrying the path and what was wrong", and the
   code does exactly that. The table row was a summary. No criterion covers the wording; plan
   assumption P1 owns it.

## Not verified, and why

- **AC5's, AC6's, AC9's, AC10's and AC11's message wording** is not verified against anything,
  because no criterion fixes it. The criteria fix the stream, the exit status and — for AC5 and
  AC11 — that `groceries` appears; all of those were checked. The sentences themselves are plan
  assumption P1 and could change without any criterion noticing.
- **Behaviour under a non-UTF-8 locale.** Plan assumption P5 and a recorded risk: printing a name
  with a non-ASCII character under `LC_ALL=C` would raise `UnicodeEncodeError`. No acceptance
  criterion exercises it, so this execution did not make it a verdict. It is a known, recorded
  gap, and the stakeholder was promised the characters in a name would not be restricted
  (`WI-0001/Q-002`) — which is about the store, and the store is written UTF-8 with
  `ensure_ascii=False`, so the gap is display-only. Flagged for WI-0002, which will print more.
- **Two processes writing at the same instant.** The plan records under `## Risks` that the second
  save overwrites a document the first had already changed; there is no lock and no criterion
  about concurrency. Not exercised, and it is not this item's to fix.
- **The default store location** — `$XDG_DATA_HOME/envel/store.json` and
  `~/.local/share/envel/store.json`. Every criterion was observed through the `ENVEL_FILE`
  branch, which is what makes them observable at all. The other two branches were read at
  `envel/store.py:31`–`:36` and not exercised, because doing so writes into the real home
  directory of whoever runs the suite. Declared rather than quietly passed.
- **`envel new` on a store whose parent directory cannot be created.** `save` turns the `OSError`
  into a `StoreError` at `envel/store.py:73`; that path was read, not triggered. No criterion
  covers it.

# Verification report — WI-0004

Verified-commit: aefa6d017f821e22e5cad24d7245c0391aa6d08f

Everything below was produced by commands this skill ran against that commit. The sample folder
`S` was rebuilt from WI-0003's definition by a script this skill wrote (`budget.csv`,
`holiday.jpg`, `report.pdf`, `notes.xyz`, `.hidden.jpg` written now; `taxes.pdf` at 400 days),
and every criterion was driven through the real command line — `python3 -m tidy` in a subprocess
with a real environment — rather than through the project's own test helpers. The suite was run
too, but it is corroboration here, not evidence: a criterion checked only by the tests written to
satisfy it is checked by the implementation's own reasoning.

## Verdict

**Pass.** All ten acceptance criteria are met. No criterion of this item failed, so there is no
send-back; no defect belonging to another item was found, so no bug was filed. Two things are
routed to `review-close` under `## Defects found` and `## Not verified, and why`: the
`--rules ""` behaviour change, and one stale sentence in `docs/architecture/overview.md`.

## Criteria

`D` is `$XDG_CONFIG_HOME/tidy/rules.ini` throughout, with `XDG_CONFIG_HOME=/tmp/v4/cfg`.
`F1` is `[types]\n.csv = data`, `F3` is `[types]\n.csv = tables`, `F4` is the 90-day
`current`/`archive` band file.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `F1` at `D`: `env XDG_CONFIG_HOME=… python3 -m tidy /tmp/v4/S`; then the same with `--rules F1.ini`; then `--apply` for each over a freshly rebuilt `S`; then both again with `F4` | PREVIEW stdout: `move   budget.csv -> recent/data/budget.csv` / `move   holiday.jpg -> recent/images/holiday.jpg` / `leave  notes.xyz   [no rule for '.xyz']` / `move   report.pdf -> recent/documents/report.pdf` / `move   taxes.pdf -> old/documents/taxes.pdf`, exit 0. `diff` of the default-location and `--rules` stdouts: **identical**. APPLY tree: `./recent/data/budget.csv`, `./recent/documents/report.pdf`, `./recent/images/holiday.jpg`, `./old/documents/taxes.pdf`, `./notes.xyz`, `./.hidden.jpg` — `diff` against the `--rules` tree: **identical**. With `F4`: `move   taxes.pdf -> archive/documents/taxes.pdf`, the other three under `current/`, and the two APPLY trees again identical | The equality verdict AC1 asks for was taken as `diff` over captured stdout and over `find`ed trees, not by eye. Each APPLY ran over a rebuilt `S`, so the two runs saw the same starting folder |
| AC2 | **pass** | empty config directory, both modes; `env -u XDG_CONFIG_HOME -u HOME python3 -m tidy /tmp/v4/S`; `env -u HOME XDG_CONFIG_HOME= …`; and separately **`git checkout main -- tests/` then the suite against this branch's `tidy/`** | All three runs print WI-0003 AC1's five lines and exit 0; the APPLY tree is the built-in one (`recent/spreadsheets/budget.csv`, `old/documents/taxes.pdf`, …). Suite on the branch head: `Ran 203 tests … OK`, exit 0. **`main`'s 158 tests, byte-unedited, against this branch's code, in a clean environment: `Ran 158 tests … OK`** | See the note below the table — this is the one criterion that needed a judgement, and it is the one `plan` predicted an argument about |
| AC3 | **pass** | `F1` at `D`, `python3 -m tidy /tmp/v4/S --rules /tmp/v4/F3.ini`, streams captured separately | stdout line 1 is `move   budget.csv -> recent/tables/budget.csv`; the other four lines are AC1's; exit 0. stderr: `tidy: using rules from /tmp/v4/F3.ini`. `grep` for `D` in stderr: **absent** | The "names `F3`'s path and not `D`" clause was checked with two greps, not by reading |
| AC4 | **pass** | `F1` at `D` and via `--rules`, PREVIEW and APPLY, streams (a) captured separately and (b) merged with `2>&1 \| head -3`; then a no-rules run | Separately: stderr line 1 is `tidy: using rules from /tmp/v4/cfg/tidy/rules.ini`, on its own line (`cat -A` shows the line ending); stdout contains the path **0** times and `using rules` **0** times. Merged, PREVIEW: `tidy: using rules from …` / `tidy: preview only …` / `move   budget.csv -> …`. Merged, APPLY: the same with `tidy: moving files. …`. With `--rules`: `tidy: using rules from /tmp/v4/F1.ini` in both modes. No-rules run: `using rules` count 0 on **both** streams, and its stdout is byte-identical to AC2's | The ordering clause was settled with a real `2>&1` pipe — genuine OS-level interleaving of two file descriptors, which is a stronger check than the in-process buffer the suite uses |
| AC5 | **pass** | all eleven exhibits of WI-0003 AC8's classes written to `D` in turn, each in **both** modes, with `sha256sum` of every file under `S` taken before and after | 22 runs, every one: `exit=2`, `stdout=0B`, `stderr=1L`, the line names `D`, and the before/after sha256 listings are equal. Example: `tidy: /tmp/v4/cfg/tidy/rules.ini cannot be used: 'newer' and 'older' in [bands] are both 'same'; the two bands need different names` | The criterion says "six classes"; the classes have eleven exhibits between them (two classes have more than one shape), and all eleven were run |
| AC6 | **pass** | a mode-`000` file at `D`, both modes; and a dangling symlink at `D`, both modes; sha256 listings before and after each | mode `000`: `tidy: /tmp/v4/cfg/tidy/rules.ini cannot be used: Permission denied`, exit 2, stdout 0 B, one stderr line, tree unchanged — in both modes. Dangling symlink: `… cannot be used: No such file or directory`, same four observations, both modes | The operating system's own reason is in the message, as the criterion requires. The symlink case is the one that distinguishes `lexists` from `exists`, and it is exercised, not reasoned about |
| AC7 | **pass** | a zero-byte file at `D` (`ls -l` shows size 0), PREVIEW and APPLY | PREVIEW stdout `diff`ed against a no-rules run's: **identical**; stderr carries `tidy: using rules from /tmp/v4/cfg/tidy/rules.ini`; exit 0. APPLY: exit 0, the same stderr line, and the built-in tree | Both halves hold at once — the file changed no sorting *and* was reported as used |
| AC8 | **pass** | `F1` at `D` over an `S` extended with `holiday/pic.jpg` and a pre-existing `recent/data/budget.csv`, both modes | `move   budget.csv -> recent/data/budget (2).csv   [recent/data/budget.csv exists]` in **both** modes; `hidden` appears 0 times on stdout and 0 on stderr and `.hidden.jpg` is still in place after APPLY; `holiday/` and `pic.jpg` appear 0 times on stdout and `holiday/pic.jpg` is still in place; `leave  notes.xyz   [no rule for '.xyz']` still printed; the pre-existing file's sha256 is `379d2257…5d29f` before **and** after APPLY | All four clauses of the criterion, each with its own observation |
| AC9 | **pass** | `grep -c "There is no default location" README.md`; then the new `### Where tidy looks when you do not say` section read against AC1–AC7 | `0`. The section states `D` in both forms in a code block; "`--rules PATH` overrides it"; "there is no search"; that neither variable set means no default location; that nothing inside the folder being tidied is read as rules; "A run says which rule file it used, on stderr" and "A run that used no rule file prints no such line"; "If it is there but tidy cannot use it, the run stops … exit status 2, and nothing moved … covers both a file with a mistake in it and one tidy is not allowed to read"; "If it is not there at all, that is not an error"; "An empty file there is a rule file, and it changes nothing" | Every clause AC9 enumerates is present. The section's worked example was checked against a real run and matches it line for line |
| AC10 | **pass** | `python3 -m tidy --help \| grep -c "no default location"`; `… \| grep -n "rules.ini\|XDG_CONFIG_HOME\|overrides"` | `0`. The `--rules` help reads `overrides the default location, which is $XDG_CONFIG_HOME/tidy/rules.ini or, when that variable is unset, ~/.config/tidy/rules.ini`, and the epilog says `--rules PATH overrides it` | Guarded by `tests/test_cli.py::HelpNamesTheDefaultLocationTests`, so it cannot go stale unnoticed the way BUG-0003 did. Both of its tests fail when the help text is reverted (see `## Test sensitivity check`) |

**AC2's second clause — "with no existing test edited to accommodate this item" — is the one
judgement in this verification, and it is recorded rather than assumed.**

`tests/support.py` *was* edited: `FolderTestCase.setUp` now points `XDG_CONFIG_HOME` at a
throwaway directory and removes `HOME`. `plan` named this as a risk and invited the argument. Two
things decide it, and both are measurements rather than readings:

1. **No existing test was edited.** In `tests/test_cli.py` and `tests/test_ruleset_file.py` the
   only removed lines in the whole diff are one docstring line and one `import` line each
   (`git diff main..HEAD -- <file> | grep '^-'`); no test function body and no assertion changed.
   `tests/support.py` and `tests/cli_support.py` have **no** removed lines at all — both are
   purely additive.
2. **The edit does not accommodate the item.** `main`'s 158 tests, restored byte-for-byte with
   `git checkout main -- tests/` and run against this branch's `tidy/` in a clean environment,
   give `Ran 158 tests … OK`. The item therefore needs no change to any existing test to make the
   existing suite pass. Run the *same* unedited 158 with a rule file at the caller's
   `XDG_CONFIG_HOME`, and 8 of them fail — which is the environment dependency the item
   introduces and precisely what the `setUp` edit removes.

So the edit changes what the suite is *exposed to*, not what it *asserts*. The strictest possible
reading — "`tests/support.py` is part of the tests and it was touched" — would fail the clause,
and a reader who prefers that reading has the evidence above to act on; I do not, because the
criterion's words are "edited **to accommodate this item**", and measurement 2 shows nothing
needed accommodating. Flagged for `review-close` rather than left in a footnote.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` on `aefa6d0` → exit 0, `Ran 203 tests in 0.339s`, `OK`. Re-run after every mutation was reverted, same result |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 11 item(s), 16 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | the table above. Every row's evidence is a command this skill ran in a subprocess against a folder it built, with the output quoted. `impl-report.md` was read after the criteria and is cited nowhere as evidence |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — 22 malformed runs, 4 unreadable runs, 3 empty-environment runs, 2 empty-file runs, 1 collision, all triggered |
| `tests-would-fail-without-the-change` | **pass** (advisory) | see `## Test sensitivity check` — seven mutations, each reverted, each naming the tests that failed |

## Negative and boundary cases exercised

Every one of these was **produced**, not read about. The command and its result are in the
criteria table; this section is the inventory, so a reader can see what was *not* skipped.

- **Nothing at `D`, three ways:** a config directory with no `tidy/` subfolder; `XDG_CONFIG_HOME`
  and `HOME` both unset; `XDG_CONFIG_HOME` set to the empty string with `HOME` unset. All three:
  the built-in output, exit 0, and no line naming a rule file.
- **Eleven malformed rule files at `D`, in both modes — 22 runs:** unparseable, a destination with
  a separator, an empty destination, an extension without a dot, three bands, one band, a
  non-numeric boundary, a zero boundary, an empty band name, a band name with a separator, two
  bands with the same name. Each: exit 2, empty stdout, exactly one stderr line naming `D`, and
  `S` byte-identical by sha256 afterwards.
- **A file at `D` that exists and cannot be read, in both modes:** mode `000` →
  `Permission denied`, exit 2, nothing moved.
- **A dangling symlink at `D`, in both modes:** exit 2 with the operating system's reason, nothing
  moved. This is the case that distinguishes present-but-unusable from absent.
- **A zero-byte file at `D`, in both modes:** exit 0, built-in sorting, and the file still named on
  stderr.
- **A destination that already exists:** `recent/data/budget.csv` pre-created with different
  contents; both modes print `budget (2).csv`, and the pre-existing file's sha256 is unchanged
  after APPLY.
- **`--rules ""` with a valid file at `D`:** exit 2. See `## Defects found`.
- **A rule file at the caller's own `XDG_CONFIG_HOME` while the suite runs:** `Ran 203 tests … OK`
  with the isolation, `FAILED (failures=11, errors=32)` without it.

## Test sensitivity check

Seven behaviours were removed one at a time, the suite run, and the change reverted. Every
criterion has at least one test that fails when its behaviour is gone. The working tree was
confirmed identical to `aefa6d0` afterwards (`git diff HEAD --stat` empty).

| mutation | tests that failed | criterion covered |
|----------|-------------------|-------------------|
| `resolve` never consults `D` (`path = None`) | `DefaultLocationSortsTheFolderTests` ×4, `MalformedAtTheDefaultLocationTests` ×12, `UnreadableAtTheDefaultLocationTests` ×4, `NamingTheRuleFileTests` ×2, `EmptyFileAtTheDefaultLocationTests` ×2, `DefaultRulesChangeNothingElseTests` ×1, `ResolveTests` ×4 | AC1, AC5, AC6, AC7, AC8 |
| the `lexists` guard removed, so absent reads as present | `NothingAtTheDefaultLocationTests::test_preview_prints_exactly_the_built_in_lines`, `::test_apply_lands_every_file_where_the_built_in_rules_say`, `::test_a_config_directory_that_exists_but_has_no_tidy_folder`, `ResolveTests::test_no_flag_and_nothing_at_the_default_path_is_a_no_rules_run`, **and ~35 pre-existing tests** | AC2 — and the collateral is itself the finding: the pre-existing suite is now genuinely sensitive to this behaviour rather than blind to it |
| the `tidy: using rules from` write removed | `NamingTheRuleFileTests` ×4, `EmptyFileAtTheDefaultLocationTests` ×2, `TheFlagBeatsTheDefaultLocationTests` ×1 | AC3, AC4, AC7 |
| `os.path.lexists` → `os.path.exists` | `UnreadableAtTheDefaultLocationTests::test_a_dangling_symlink_stops_the_run`, `ResolveTests::test_a_dangling_symlink_at_the_default_path_is_present_and_refused` | AC6 |
| `argument is not None` → truthiness | `ResolveTests::test_an_empty_flag_is_refused_rather_than_falling_back` | ADR-0014 point 3 (no AC of this item) |
| the `HOME` fallback removed from `default_path` | `DefaultPathTests::test_home_is_the_fallback`, `::test_an_empty_xdg_config_home_falls_through_to_home` | AC2's second sentence, and the `D` definition in the criteria preamble |
| the `--help` text reverted to `main`'s | `HelpNamesTheDefaultLocationTests::test_help_names_the_rule_file_and_says_the_flag_overrides_it`, `::test_help_no_longer_says_there_is_no_default_location` | AC10 |

AC9 has no test and cannot have one that is worth having; it is checked by the two `grep`s and the
reading in its row, which is what the criterion itself specifies.

## Defects found

**None that fail an acceptance criterion of this item**, so there is no send-back. **No defect
belonging to another item was found**, so no bug item was filed. Two observations are routed
rather than dropped:

1. **`--rules ""` changed from a silent no-rules run to exit 2, and nothing tells the user.** On
   `main`: `python3 -m tidy S --rules ''` prints the preview and exits 0. On this branch:
   `tidy:  cannot be used: No such file or directory`, exit 2. Both verified by running the two
   revisions against the same folder. This is **planned**, not unrequested — ADR-0014 point 3
   decides it and `plan` listed it as a risk — and no criterion of this item covers it, which is
   why it is not a send-back. But it is user-visible, it was not asked for by the stakeholder, and
   `README.md` says nothing about it. Note also that the message has a double space where the
   empty path would be (`tidy:  cannot be used:`) and names no path, so a user who hits it is told
   nothing actionable. **Not filed as a bug**, because `review-close` already handled the
   *previous* state of this same question as a recorded gap on WI-0003 rather than as a bug, and
   because the decision of whether it should ship at all belongs to the Definition of Done review,
   not to a new item that would pre-empt it.
2. **`docs/architecture/overview.md` line 123 says WI-0004 "is planned and not yet built".** True
   of `main`, false of this branch. `impl-report.md` declares this deliberately undone and hands
   it to `review-close`'s D7 and D12; this verification confirms the sentence is still there and
   that the rest of the overview's WI-0004 material — `default_path`, `resolve`, the default
   location, ADR-0014 — is accurate.

## Not verified, and why

- **`~/.config/tidy/rules.ini` was never read from a real home directory.** Every `HOME`-based
  check used a `HOME` this skill set to a temporary directory. Reading a developer's actual home
  is both outside this project and the exact dependency the item removes, so the fallback branch
  is verified as *a path computation over a mapping* (`DefaultPathTests`, and a live run with
  `HOME` pointed at a scratch directory) and not against a real `~`.
- **Windows and macOS path spellings.** All evidence is Linux, `os.sep` `/`. Nothing in the item
  or the project claims another platform, and `default_path` uses `os.path.join`, but no run on
  another platform was made.
- **A relative `XDG_CONFIG_HOME`.** Plan assumption A1 says it is used as given rather than
  ignored, which the XDG convention says should be the other way round. No criterion names the
  case and I did not exercise it; the assumption stands as `plan` recorded it.
- **A rule file whose parent directory is unsearchable.** Plan assumption A3 says `lexists`
  returns `False` there, so such a run is a no-rules run rather than exit 2 — the one place where
  present-but-unusable reports as absent. No criterion names it and it was not exercised.
- **`## Defects found` item 1's wider question** — whether `--rules ""` should exit 2 at all — is
  not mine to decide and is not verified either way. It is stated so `review-close` decides it
  knowingly.
- **The stderr line's exact wording** is `plan`'s under the standing delegation (assumption A2),
  and AC4 constrains only the stream, the ordering and that the path is present. I checked those
  three and did not judge the wording.

# Verification report — WI-0001

Verified-commit: 7c552ef65886523149a1f5f128ee31a794c7b9ed

## Verdict

**Pass.** All nine acceptance criteria hold, each demonstrated by a command run during this
verification against `bin/recall` on `PATH` — not by reading `impl-report.md` and not by reading
the test suite. The criteria were read and the checks derived from them before the implementation
report was opened.

One defect was found, outside every criterion, and filed as **BUG-0001** rather than sent back:
a filesystem error on the deck file that is not a content problem escapes as a Python traceback.
WI-0001 is not responsible for it under `verify`'s classification rule, and the reasoning is in
`BUG-0001` `## Summary`.

Every check below ran with `HOME` pointed at a scratch directory under `.harness/verify/`, which
is git-ignored, and `PATH="$PWD/bin:$PATH"`. Output is quoted as it appeared.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `recall list`; `recall add --question "capital of France" --answer "Paris"`; `recall list` — the criterion's own literal invocation | before: `The deck is empty. Add a card with: recall add --question "..." --answer "..."` (exit 0, 0 card lines). add: `Added. The deck now holds 1 card(s).` exit 0. after: `capital of France \| Paris` (exit 0, 1 card line) | 0 → 1 is one more card |
| AC2 | **pass** | six refusals, each bracketed by `recall list` and `sha256sum` of the deck, against a deck holding one card | every case exit 2; e.g. `recall add: refusing -- --question must be given and must not be blank. The deck was not touched.`; `list output identical: yes`; `deck sha256 unchanged: yes` for all six | the five cases AC2 names, plus a tabs case because AC2 names tabs and no other case has one |
| AC3 | **pass** | `recall add --question "Der  Bahnhof" --answer "The  STATION"` then `recall list \| cat -A` | `capital of France \| Paris$` / `Der  Bahnhof \| The  STATION$` | `cat -A` is how "exactly as it was given" was checked rather than assumed: the internal double space survives and `STATION` is not case-folded |
| AC4 | **pass** | `HOME=$H sh -c 'recall add ...; echo pid=$$ exiting'` then, separately, `HOME=$H sh -c 'echo pid=$$; recall list'` | `adding process pid=680389 exiting` / `reading process pid=680391` / `el puente \| the bridge`, exit 0 | two different pids: the writing process had exited before the reading one started, and no save step was invoked |
| AC5 | **pass** | `ls -la $H` and `test -e $H/.local` on an empty scratch home, then `recall add --question "capital of France" --answer "Paris"`, then `find $H` | before: `parent absent: ok`. add: exit 0. after: `~/.local`, `~/.local/share`, `~/.local/share/recall`, `~/.local/share/recall/deck.json` | nothing was created or configured by hand first |
| AC6 | **pass** | `recall list` against an empty scratch home | `The deck is empty. Add a card with: recall add --question "..." --answer "..."`, exit 0 | a line saying so, on stdout, exit 0 — not an error and not a blank page |
| AC7(a) | **pass** | `grep -n "local/share/recall/deck.json" docs/process/using-recall.md` | line 56: `~/.local/share/recall/deck.json` | the project's own documentation states the path |
| AC7(b) | **pass** | `find $H -type f` before and after one `recall add`, then `grep -c "capital of France"` on the result | created: `~/.local/share/recall/deck.json`, `count: 1`; card present: `1` | exactly one file; the atomic write leaves no temporary file beside it |
| AC7(c) | **pass** | `python3 -c` printing `store.deck_path().resolve()` against the **ambient** home, and `is_relative_to` for `$HOME`, `/tmp`, `/var/tmp`, `$TMPDIR` | `deck_path() = /home/msi/.local/share/recall/deck.json`; `under home: True`; `under /tmp: False`; `under /var/tmp: False`; `TMPDIR set: None` | checked against the real home, not the scratch one — a scratch home is itself inside `/tmp`, so checking there would prove nothing. Also `grep`ed `store.py` for `environ`/`getenv`/`XDG`/`argv`: no lookup exists, so the path derives from the home directory alone |
| AC8 | **pass** | six kinds of damaged deck, each × `add` and `list`, with `sha256sum` before and after | all twelve invocations exit 3 and name the deck file. Truncated `{"cards": ` → `it is not valid JSON (Expecting value, line 1)`; `this is not json` → same; `[1, 2, 3]` → `its top level is not a JSON object`; `{"version": 1}` → `it has no 'cards' array`; a card missing `rung` → `card 1 has no 'rung'`; an empty file → `it is not valid JSON`. `bytes unchanged: yes` and `files still in dir: deck.json` in all six | three more damage kinds than the test suite covers. Nothing was rewritten, truncated or repaired in any case |
| AC9 | **pass** | `recall add --question "capital of France" --answer "Paris, again"` against a deck already holding that question, then `recall list` | `Added. The deck now holds 3 card(s).` exit 0; list shows `capital of France \| Paris` and `capital of France \| Paris, again` as separate lines | allowed, produces two cards, no deduplication and no refusal |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` run by this skill on `7c552ef` → exit 0, `Ran 16 tests in 1.938s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0. Narrow by construction: `ADR-0003` §3 records it as a syntax check, and it does not cover `bin/recall`, which has no `.py` extension |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0 before this execution wrote anything, and again after the board was regenerated. It went red mid-execution on three expected counts — a stale board, an 87-character title on the new bug, and a `verify` history row with no journal entry yet — all three resolved before the transition |
| `every-criterion-independently-checked` | **pass** | the Criteria table: every row names a command this skill ran and quotes its actual output. No row cites `impl-report.md`, and no row's evidence is "a test passes" |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — 25 conditions triggered, not read about |
| `a-criterion-about-criteria-is-read` | **not applicable** | All nine criteria were read for this shape. None has criteria as its subject: AC1–AC9 each describe an observable behaviour of the tool directly, and none says "the earlier criteria still hold" or names another criterion as the thing being asserted. AC7 has three lettered parts, but they are three observations of one behaviour, not assertions about other criteria. Recorded as not-applicable rather than passed, because there was nothing to read |
| `tests-would-fail-without-the-change` (advisory) | **pass** | see `## Test sensitivity check` — eleven mutations, run by this skill |

## Negative and boundary cases exercised

Every one of these was *triggered* and its output recorded. Twenty-five conditions:

- **AC2's refusals, six of them** — `--question` omitted, `--answer` omitted, `--question ""`,
  `--answer ""`, `--answer "   "`, `--question " \t "`. Each against a deck that already held a
  card, so "the deck is exactly as it was" had something to be true about. All six: exit 2, the
  missing option named on stderr, `recall list` byte-identical before and after, deck `sha256`
  unchanged.
- **AC8's unreadable decks, six kinds × two subcommands = twelve invocations** — truncated JSON,
  text that is not JSON at all, JSON that is not an object, an object with no `cards` array, a
  card missing a required field, and a zero-byte file. All twelve: exit 3, the deck file named,
  bytes unchanged, and the directory still holding exactly `deck.json`.
- **AC5/AC6's empty states** — `recall list` with no deck file and no parent directory; `recall
  add` as the first thing that ever runs.
- **Beyond every criterion, five more**, because they are where an implementation diverges from
  intent without any criterion noticing:

  | condition | result | assessment |
  |---|---|---|
  | `recall` with no subcommand | `usage: recall [-h] {add,list} ...` / `recall: error: the following arguments are required: subcommand`, exit 2 | consistent with `ADR-0001` §5. No criterion covers it |
  | `recall frobnicate` | `recall: error: argument subcommand: invalid choice: 'frobnicate' (choose from 'add', 'list')`, exit 2 | as above |
  | `python3 -m recall list` | `The deck is empty. ...`, exit 0 | `ADR-0005` §3 promises this and it works. No criterion covers it, and no test exercises it — declared below |
  | the deck's directory is not writable (`chmod 500`) | `PermissionError: [Errno 13] ...deck.json.5u4wwd96.tmp`, a full traceback, exit 1 | **defect** → `BUG-0001` |
  | a directory sits at the deck path | `IsADirectoryError: [Errno 21] ...`, a full traceback, exit 1 | **defect** → `BUG-0001`, same root cause |

- **One further observation, not a defect.** A question side containing a newline is stored and
  printed faithfully, so `recall list` shows that card across two lines:
  `recall add --question "$(printf 'line one\nline two')" --answer a` then `recall list \| cat -A`
  gives `line one$` / `line two \| a$`. AC3 requires the text exactly as given and forbids
  trimming, case change and truncation — all of which hold. No criterion says a card occupies one
  line; that is `plan.md`'s own assumption, recorded there with its reversal cost. Nothing
  currently parses `list` output, so nothing is broken today. Recorded here because WI-0004 will
  need to name a card, and whoever refines it should decide this deliberately rather than inherit
  it.

## Test sensitivity check

Eleven mutations, applied by this skill one at a time to the working tree, the full suite run
after each, and the file restored from disk afterwards. `git status` was clean and the suite
green (`Ran 16 tests ... OK`) after the last restore. The harness is at `.harness/verify/mutate.py`,
which is git-ignored — it is evidence of how this was done, not a project artifact.

| AC | behaviour removed | tests that noticed |
|----|-------------------|--------------------|
| AC1, AC4 | `cmd_add` never calls `store.save` | `test_add_exits_zero_and_adds_one`, `test_survives_process_exit`, `test_first_run_creates_storage`, `test_one_file_under_home_not_tmp`, `test_lists_both_cards_verbatim`, `test_duplicate_question_allowed` |
| AC2 | blank sides accepted (`value.strip()` check dropped) | `test_blank_sides_refused` |
| AC3 | `cmd_list` lowercases and collapses whitespace | `test_lists_both_cards_verbatim`, `test_add_exits_zero_and_adds_one` |
| AC4 | `store.load` always returns an empty deck | nine tests, including `test_survives_process_exit`, `test_unreadable_deck_refused`, `test_malformed_json_raises_rather_than_returning_empty` |
| AC5 | `save` no longer creates the parent directory | `test_first_run_creates_storage` and seven others |
| AC6 | the empty-deck message is not printed | `test_empty_deck_message` |
| AC7(a) | `docs/process/using-recall.md` deleted | `test_docs_state_the_path` |
| AC7(b) | the atomic rename replaced by a copy, leaving the temporary file | `test_one_file_under_home_not_tmp` |
| AC7(c) | `deck_path()` returns `/tmp/recall/deck.json` | `test_deck_path_is_under_home_and_not_boot_cleared` and six others |
| AC8 | `cmd_add` catches `DeckUnreadable` and starts a fresh empty deck | `test_unreadable_deck_refused` |
| AC9 | `Deck.add` deduplicates by question | `test_duplicate_question_allowed` |

Every mutation was caught, and in each case by the test `plan.md`'s mapping table names for that
criterion — so the mapping is real and not merely plausible. The AC8 mutation is the one that
matters most: it is the shortcut `plan.md` predicted ("the easy way to satisfy AC5 breaks AC8"),
written the way an implementation would actually take it, and the suite refuses it.

## Diff against the plan

Fifteen files differ from `main`. Ten are code, tests and documentation; five are `tracker/`
records. Every module and every public function traces to a plan step: `deck.py` → step 2,
`store.py` → step 3, `cli.py` → step 4, `bin/recall` and `__main__.py` → step 5, the four test
files → steps 1 and 6, `docs/process/using-recall.md` → step 7.

Four functions exist that the plan does not name: `build_parser`, `_report_unreadable`,
`_card_from` and `_card_to_entry`. All four are private or structural, and each implements a
contract the plan does state — the `argparse` setup of step 4, the single catch site the approach
section requires, and the "entries have the four expected keys" clause of `load`. None introduces
behaviour a criterion does not cover. **No unrequested scope was found.**

The three deviations `impl-report.md` declares were checked against the code and are accurate as
described. The AC7 one is the substantive one and the right call: the table's single test could
not have honestly asserted "not under `/tmp`" while running inside a temporary home.

## Defects found

**BUG-0001** — *A filesystem error on the deck file surfaces as a traceback, not a message.*
Filed at `ready`, `found-in: WI-0001`, priority medium, with both reproductions and their
verbatim output. `cli.py` catches `store.DeckUnreadable` and nothing else, so a `PermissionError`
or an `IsADirectoryError` on the deck reaches the person as a traceback.

**Not a send-back, and the reasoning matters.** AC8 is the only criterion in the neighbourhood
and its own text scopes it to a deck that "cannot be read as a deck — it is truncated, malformed,
or not the format the tool writes": a statement about contents. All six content cases pass. An
unwritable directory is a write failure; a directory at the deck path is not a content problem.
No criterion of WI-0001 says either should behave differently, which is exactly `verify`'s test
for a bug rather than a send-back. Nothing is lost in either case — no deck is truncated,
overwritten or replaced — so the stakeholder's stated failure condition is not in play.

## Not verified, and why

- **`python3 -m recall`** works — checked once by hand, exit 0 — but no acceptance criterion
  covers it and no test exercises it. `ADR-0005` §3 offers it as a convenience and says plainly
  it is not what the criteria are written against. It is therefore unprotected against regression:
  a change to `recall/__main__.py` would break it silently. Declared rather than fixed, because
  adding a criterion is `refine`'s work and adding an unrequested test is scope.
- **`bin/recall` is not covered by `commands.lint`.** The declared command compiles `recall` and
  `tests`, and `bin/recall` is in neither. All nine acceptance checks execute it as the child
  process, so a syntax error in it would fail everything loudly — but the lint gate does not see
  it. `impl-report.md` declares this too; this verification confirms it independently by reading
  `tracker/project.yaml`.
- **`commands.lint` proves very little in general.** It is `compileall`, a syntax check, on a
  machine where no style linter is installed (`ADR-0003` §3). A green `lint-clean` here should be
  read as "it parses", nothing more.
- **AC7's "survives a reboot" was not tested by rebooting.** It was checked the three ways AC7
  itself specifies — the documented path, exactly one file created, and that path being under the
  home directory and outside `/tmp`, `/var/tmp` and `$TMPDIR`. The criterion was written to be
  decidable without a reboot and it was decided that way. `$TMPDIR` is unset on this machine, so
  that clause of the check was vacuous here; the `/tmp` and `/var/tmp` clauses were not.
- **Concurrency was not exercised.** Two `recall add` processes writing at once is neither
  specified by any criterion nor excluded by the item, and the `os.replace` discipline is about
  interrupted writes rather than simultaneous ones. The epic is one person at one terminal, so
  this is out of scope rather than a gap — recorded so that nobody later reads a passing AC4 as a
  statement about concurrent access.
- **Nothing was verified about `rung` or `due` beyond their presence in the stored file.** No
  WI-0001 criterion reads them back. `save`/`load` round-tripping was observed while exercising
  AC8's "card missing a field" case, which required a well-formed card to contrast against, but
  the scheduling semantics belong to WI-0002 and WI-0003.

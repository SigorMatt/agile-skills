# Verification report — WI-0001

Verified-commit: f22f9c0b0dace18718b02c819984e49d131c8648

## Verdict

**Pass.** All eight acceptance criteria hold, each demonstrated by a command run in this
execution against the head of `wi/WI-0001`, with the actual output recorded below. No defect was
found; no bug item was filed; nothing was sent back.

One limitation is declared rather than glossed: AC2 names a machine restart, and no machine was
restarted. What was substituted for it is stated under `## Not verified, and why`, and it is
stronger than reading the code — the syscalls the writing process actually makes were traced.

Every check below was run with the tool's own command line, in scratch directories created for
this verification and removed afterwards, with `RECALL_CARD_FILE` or `XDG_DATA_HOME` pointed at
them. The criteria were read and the checks derived from them before `impl-report.md` was opened.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `python3 -m recall add bonjour hello` then `grep -c '^front: ' cards.txt` | `Added: bonjour`, exit `0`, `1` | The confirmation names the front side; exactly two arguments, front first; one card in the file |
| AC2 | **pass** | `python3 -m recall add 'l'\''été "chaud" \ ünïcode<TAB>tab' 'the "hot" summer'`, then, **after that process exited**, `od -c cards.txt` and an independent Python read of the raw bytes | `front line byte-identical: True`, `back line byte-identical: True`; `od -c` shows `l ' 303 251 t 303 251 " c h a u d " \ 303 274 n 303 257 c o d e \t t a b` | Quotes, a backslash, a literal tab and non-ASCII all survive unescaped. See `## Not verified, and why` for the restart |
| AC3 | **pass** | three `add` runs with `bonjour`/`chat`/`livre`, then `grep -c` per label | `front=3 back=3 rung=3 due=3`, and the file shows three blocks, each front directly above its own back | None overwrote another; each carries its own rung and due date |
| AC4 | **pass** | `date +%F` (independent of the tool) and `grep '^due: ' cards.txt \| sort -u` | `2026-08-30` and `due: 2026-08-30` | The due date of every newly added card equals the calendar date it was added |
| AC5 | **pass** | `env -u RECALL_CARD_FILE XDG_DATA_HOME=<dir> python3 -m recall add …` then `find`; and `env -u XDG_DATA_HOME HOME=<dir> …`; then `file` and a UTF-8 decode of the bytes | `<XDG_DATA_HOME>/recall/cards.txt`; `<HOME>/.local/share/recall/cards.txt`; `ASCII text`; `decodes as UTF-8: True`; `control characters other than newline: []` | Both paths are the ones `docs/architecture/overview.md:44` states. Both sides and both scheduling fields are plain labelled lines, read with the tool not running; nothing is compressed, binary or encoded |
| AC6 | **pass** | `add bonjour hello` then `add bonjour "good day"`, with the streams separated | exit `0`; standard error: `Warning: a card with the front 'bonjour' already exists; adding this one as well.`; standard output: `Added: bonjour`; the file holds two `front: bonjour` blocks with `back: hello` and `back: good day` | A second, distinct card, not a refusal and not a replacement |
| AC7 | **pass** | four refusals (`"" hello`, `bonjour ""`, `"   " hello`, `bonjour "  <TAB> "`), then `sha256sum` around a refusal on an existing file, then `add bonjour ""` on a file already holding `bonjour` | each: `The front/back side is empty.` + `Nothing was added.`, exit `1`, `file exists after: no`; sha256 `ef49f065…c26` identical before and after; the duplicate case printed no `already exists` line and left `1` record | The message names which side. The file is byte-identical after a refusal, and absent when it was absent. AC7's stated precedence over AC6 holds |
| AC8 | **pass** | `RECALL_CARD_FILE=<dir>/deep/deeper/cards.txt` where `<dir>` did not exist (`ls` → `No such file or directory`), then `add bonjour hello` | `Added: bonjour`, exit `0`; `1` record; `front byte-identical: True`, `back byte-identical: True` | See the next section: AC8's subject includes AC1 and AC2 |

### AC8 is a criterion about criteria

AC8 ends *"after the first ever `add`, AC1 and AC2 hold"*, so its subject is two other criteria.
It names them by ID, and each was read against the behaviour in that situation and then
exercised, rather than inferred from a green suite:

- **AC1, in the no-file case** — *"adds one card, prints a confirmation naming the front side …
  and exits zero"*. Still true: the run above printed `Added: bonjour`, exited `0`, and left
  exactly one record. **Verdict: holds.**
- **AC2, in the no-file case** — *"reading the card file with an ordinary text tool shows that
  card, with both sides byte-identical"*. Still true: reading the newly created file's raw bytes
  after the process exited gives `front: bonjour` and `back: hello` exactly. **Verdict: holds**,
  with the same restart limitation as AC2 itself.

**Non-intersection does not exist here**, and that is stated positively rather than assumed:
`tests/test_add.py::test_the_first_add_creates_the_file_and_its_directory` exercises the new
behaviour (a path three directories deep into nothing) *and* both older criteria's observations
in the same test — the exit code and the confirmation for AC1, the bytes on disk for AC2. The
manual run above does the same. No criterion needed waiving.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 26 tests in 1.177s`, `OK`, run by this skill on `f22f9c0` |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → exit 0, 4 items and 10 documents, 0 errors 0 warnings |
| `every-criterion-independently-checked` | **pass** | the table above: every row is a command this execution ran with its quoted output. `impl-report.md` was read after the checks were derived and is cited nowhere as evidence |
| `negative-cases-exercised` | **pass** | see the next section — seven conditions triggered, not read about |
| `a-criterion-about-criteria-is-read` | **pass** | AC8's per-criterion read of AC1 and AC2 above, with the intersecting case named |
| `tests-would-fail-without-the-change` | **pass (advisory)** | eight mutations, below |

## Negative and boundary cases exercised

| condition | command | what happened |
|-----------|---------|---------------|
| empty front, empty back, whitespace-only front, tab-and-space back | `python3 -m recall add "" hello` and three more | `The <side> side is empty.` + `Nothing was added.`, exit `1`, no file created |
| refusal against an existing file | `add chat "   "` after a successful add | exit `1`, sha256 unchanged |
| duplicate front with an empty back | `add bonjour ""` on a file holding `bonjour` | exit `1`, the empty-side message only — no duplicate warning; still one record |
| a line break inside a side | `add "$(printf 'bon\njour')" hello` | `The front side contains a line break.`, exit `1`, no file created |
| too few arguments | `python3 -m recall add only-one` | `usage: recall add [-h] front back` … `the following arguments are required: back`, exit `2` |
| no subcommand, and an unknown one | `python3 -m recall`; `python3 -m recall review` | `usage: recall [-h] {add} ...`, exit `2`; `invalid choice: 'review' (choose from 'add')`, exit `2` |
| a card file the tool did not write | a hand-written file with `bakc:` for `back:`, then `add chat cat` | `…/cards.txt: line 2: expected a line starting 'back: ', found 'bakc: hello'`, exit `1`, and the existing file byte-identical afterwards — nothing was dropped or repaired |
| an unwritable location | `RECALL_CARD_FILE` inside a directory with mode 500 | `…: [Errno 13] Permission denied: …`, exit `1`, no traceback |
| a 500-character back and a side with leading and trailing spaces | `add "  spaced front  " "xxx…"` | exit `0`; `leading/trailing spaces kept: True`, `500-character back kept: True` |

## Test sensitivity check

Each mutation was applied to the branch, the named tests run, and the file restored with
`git checkout --`. The suite is green again afterwards (`OK`, 26 tests) and `git status` is
clean.

| criterion | behaviour removed | result |
|-----------|-------------------|--------|
| AC1 | the confirmation no longer names the front (`print("Added.")`) | `test_add_prints_confirmation_and_exits_zero` **failed** |
| AC2 | values written through `{0!r}`, i.e. escaped | `test_card_is_on_disk_after_the_process_exits` **failed** |
| AC3 | `cards.append(...)` replaced by `cards = [...]` | `test_three_cards_are_three_records` **failed** |
| AC4 | today's date replaced by a fixed `2020-01-01` | `test_new_card_is_due_today_at_the_bottom_rung` **failed** |
| AC5 | the default path changed to `<data>/elsewhere/cards.txt` | 3 tests **failed**, including `test_default_path_is_the_documented_one` |
| AC6 | the duplicate comparison replaced by `if False:` | `test_duplicate_front_adds_a_second_card_and_warns` **failed** |
| AC7 | the emptiness check deleted | 6 tests **failed** |
| AC8 | `os.makedirs` removed from `save()` | `test_the_first_add_creates_the_file_and_its_directory` **failed** |

No test survived the removal of the behaviour it claims to cover.

## Defects found

None.

The diff against `main` was read against `plan.md`. Every hunk traces to a plan step or a
criterion. Three things in the code go beyond the plan's literal text, and none is unrequested
behaviour: the second refusal line `Nothing was added.` and the card file's path prefixed to an
error message, both declared in `impl-report.md` under the plan's assumption 2 on wording; and
`store._card`'s check that `rung` is within 0 to 4, which is `ADR-0007`'s definition of the field
rather than new behaviour. `tests/test_store.py` is a second test file the plan did not name; it
covers the plan's steps 1 to 3 and no criterion depends on it.

## Not verified, and why

- **AC2's machine restart.** No machine was restarted, and none can be inside this run. Three
  things were substituted, and they are recorded here so a reader can judge the gap rather than
  assume it away: (1) the card file was read by a *different* process after the writing process
  had exited, and held the exact bytes; (2) `strace -f -e trace=fsync,rename` on a real `add` run
  shows `fsync(3) = 0`, then `rename(".cards-….tmp", "cards.txt") = 0`, then a second
  `fsync(3) = 0` — the file is flushed, atomically renamed, and the directory entry flushed,
  before the process exits; (3) the file lives on an ordinary filesystem at the documented path.
  Nothing is held in a buffer, a cache the tool owns, or a temporary location that a reboot would
  discard. That is why AC2 is ticked. If the stakeholder or `review-close` reads AC2 as requiring
  a literal reboot, this criterion cannot be settled in any automated environment and the wording
  is what needs revisiting — not this implementation. `plan.md`'s `## Risks` raised this before
  any code existed, and `impl-report.md` declared it too.
- **Behaviour of a second `recall` process writing at the same moment.** Not exercised. No
  criterion mentions concurrency, the tool is single-user by `ADR-0001`, and the rename-based
  save makes a torn file unlikely rather than impossible. Named because it is unchecked, not
  because it is suspected.
- **Non-UTF-8 or invalid-encoding arguments**, and filesystems that do not support `fsync` on a
  directory. Neither is named by any criterion and neither was triggered.

# Review — WI-0001

Reviewed commit `d12754a7aa0ed24504ac76584c77aecbe600ffd1`, the head of `wi/WI-0001`, against
`main` at `5c667e021aeba6963b59d5cf7d62f050dc963466`.

## What I examined

- **The diff, hunk by hunk**, over `git diff main..wi/WI-0001` — 11 files, 917 insertions.
  `recall/store.py` (162 lines), `recall/cli.py` (70), `recall/__main__.py` (7),
  `tests/test_add.py` (195), `tests/test_store.py` (101), and this item's tracker files. Each
  hunk was mapped to a plan step and a criterion; the mapping is under `## Findings`.
- **The record:** `item.md`, `history.md` (8 rows), `journal.md` (9 entries, read in full),
  `plan.md`, `impl-report.md`, `verify-report.md`, `refinement-qa.md`, and both questions
  `Q-001` and `Q-002`.
- **The recorded decisions:** `ADR-0001`, `ADR-0002`, `ADR-0004`, `ADR-0006`, `ADR-0007` and
  `ADR-0008`, each read against the code that is supposed to implement it.
- **The trial merge:** `wi/WI-0001` merged `--no-ff` into a detached worktree of `main`
  (`c3b2f609467fc83ca8287665261fc1cfb74cd03d`), with the project's test and lint commands run
  inside it. The worktree was removed and `git rev-parse main` returned `5c667e02` both before
  and after, so the trial published nothing.

### The claims I audited for D12, and what I opened to decide each

Each sentence below was decided by opening the thing it cites, not by reading a neighbouring
document. All are absolute claims in `docs/` about behaviour this item delivered.

| # | claim, and where it is | what I opened | verdict |
|---|------------------------|---------------|---------|
| 1 | `overview.md` §Where the cards live: the card file is `$XDG_DATA_HOME/recall/cards.txt` when `XDG_DATA_HOME` is set, else `~/.local/share/recall/cards.txt`; `RECALL_CARD_FILE` overrides both | `card_file_path()` [src: recall/store.py], plus two runs with the variables set to an empty value | **false at one edge — repaired.** See finding 1 |
| 2 | `ADR-0008` §Decision, the same two sentences | the same function and the same two runs | **false at one edge — repaired.** See finding 1 |
| 3 | `overview.md`: the directory and the file are created on first use | `save()`'s `os.makedirs(directory, exist_ok=True)` [src: recall/store.py]; AC8's run in `verify-report.md` | true |
| 4 | `overview.md`: every save rewrites the whole file through a temporary file and a rename, so an interrupted run leaves the previous file intact | `save()` — `tempfile.mkstemp` in the same directory, `flush`, `os.fsync`, `os.replace`, then a directory fsync [src: recall/store.py] | true |
| 5 | `overview.md` and `ADR-0007`: a value is everything after the first `: ` to the end of the line, verbatim — nothing escaped, quoted or trimmed | `_render()` and `_value()`'s `line[len(prefix):]` [src: recall/store.py]; AC2's byte-identical read in `verify-report.md` | true |
| 6 | `overview.md` and `ADR-0007`: `rung` is `0` for a card never answered, `1` to `4` for the ladder's intervals | `LOWEST_RUNG`, `HIGHEST_RUNG` and `_card()`'s range check [src: recall/store.py]; `NEW_CARD_RUNG` [src: recall/cli.py] | true |
| 7 | `overview.md`: a subcommand exits `0` when it did what was asked and non-zero when it did not; confirmations to standard output, warnings and refusals to standard error | `add()` and `main()` [src: recall/cli.py] — `EXIT_OK`, `EXIT_REFUSED`, every non-confirmation `print` carrying `file=sys.stderr` | true |
| 8 | `overview.md`: only `add` is planned so far, the other two subcommands are named for where they will attach | `_parser()` registers `add` and nothing else [src: recall/cli.py] | true |
| 9 | `overview.md`: tests drive the command-line entry point against a card file in a temporary directory using `RECALL_CARD_FILE`, so a test run does not touch a real deck | `AddTests.recall()` and `setUp` [src: tests/test_add.py]; the `TemporaryDirectory` fixtures in [src: tests/test_store.py] | true |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | AC1 to AC8 all `[x]` in `item.md`; `validate-workspace .` → exit 0 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | the report's `## Criteria` table gives each of AC1 to AC8 its own row naming the command run and quoting the actual output; AC8's row is followed by a per-criterion read of AC1 and AC2, which AC8's text names |
| D3 | the item's gates passed on the final state of the code | **pass** | `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 26 tests`, `OK`, and `python3 -m compileall -q recall tests` → exit 0, both run by this review on the trial merge `c3b2f60`, which is the state the trunk receives |
| D4 | no open blocking question remains | **pass** | `Q-001` and `Q-002` are both `status: answered`, `answered-by: human`, each with `## Consequences` naming files that exist |
| D5 | a journal entry per execution; history chains to the current status | **pass** | 9 entries against 8 history rows — the extra is the `answer-questions` execution of 11:18:49Z that consumed `EP-001`'s answers without moving this item. Rows chain `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review`, and the last row matches `item.md` |
| D6 | every design decision is in an ADR cited from the plan or the journal | **pass** | `plan.md` §Decisions and ADRs maps eight decisions to `ADR-0006`, `ADR-0007`, `ADR-0008` or to its own `## Assumptions`; the five assumptions are reversible and each is named there |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` v1→v2 and `docs/architecture/adr/ADR-0008-where-the-card-file-lives-and-how-it-is-written.md` v1→v3, both by this execution, each with its change-log rows; the ADR's two errata are in its append-only `## Corrections` section (`doc-header.md` §4b) |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 4 commits on `main..wi/WI-0001` name WI-0001 |
| D9 | the change is merged into the trunk | **pass** | merged into `main` after this item was closed; the merge commit is named in the journal entry for this execution |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: verified at `f22f9c0b`, the branch has moved to `d12754a7` but the 5 files that changed are all under `tracker/`, so the verification still covers the code |
| D11 | the review record exists and says what was examined | **pass** | this file; `## What I examined` names the diff range, the artifacts, the ADRs, the trial merge and the nine claims audited |
| D12 | claims in `docs/` about the behaviour this item touched are still true; absolute claims carry a resolvable citation | **pass, with a repair** | the nine-row audit above, each decided by opening the cited code. Two were false at the empty-variable edge and were repaired in place (finding 1). `lint-claims --context work-item --changed-since main` → exit 0 over `2 document(s) in 2 path(s)`; `lint-claims --all` → exit 0 over every document under `docs/` |

## Findings

**1 — Two documented sentences about the card file's location were false for a variable set to an
empty value. Repaired in place; no code changed.** `card_file_path()` treats an empty
`RECALL_CARD_FILE` or `XDG_DATA_HOME` as unset [src: recall/store.py], which is what the XDG Base
Directory Specification asks for and what the plan specified — *"`RECALL_CARD_FILE` if set and
non-empty"* [src: tracker/items/WI-0001/artifacts/plan.md]. The two documents that a reader
consults instead said only *"set"*:

- with `XDG_DATA_HOME` set to an empty value, the card file is not `$XDG_DATA_HOME/recall/cards.txt`
  [src: run: cwd=/tmp/xdgprobe, XDG_DATA_HOME= HOME=/tmp/xdgprobe/home python3 -m recall add bonjour hello -> exit 0, wrote /tmp/xdgprobe/home/.local/share/recall/cards.txt];
- with `RECALL_CARD_FILE` set to an empty value, it does not override
  [src: run: RECALL_CARD_FILE= XDG_DATA_HOME=/tmp/xdgprobe/home2/data python3 -m recall add chat cat -> exit 0, wrote /tmp/xdgprobe/home2/data/recall/cards.txt].

The code is right and the prose was loose, so this is a correction and not a supersession — no
reader has to change any code to satisfy the new text (`doc-header.md` §4b). `ADR-0008` carries
two `erratum` entries quoting the removed clauses verbatim, and `overview.md`'s statement of the
path — the sentence AC5 requires the documentation to make — now says the same thing the code
does. AC5 itself is unaffected: it asks that the data live at a path stated in the documentation,
and both the stated path and the actual path were, and are, `$XDG_DATA_HOME/recall/cards.txt` or
`~/.local/share/recall/cards.txt`.

**2 — `main()` does not dispatch on the subcommand it parsed. Correct today, and a trap for
WI-0002.** `main()` calls `add(arguments.front, arguments.back)` unconditionally
[src: recall/cli.py]. That is sound while `add` is the only registered subcommand and
`add_subparsers(required=True)` refuses everything else with exit `2`, and the code says so in a
comment. It is not a defect and not a send-back: no criterion is affected and the behaviour is
the one `verify` exercised (`python3 -m recall review` → exit `2`, `invalid choice`). It is
recorded because the moment WI-0002 registers a second subcommand, this line silently runs `add`
for it — and an `AttributeError` on `arguments.front` is the good case. Carried into `item.md`'s
`## Notes` so that WI-0002's plan meets it before its implementation does.

**3 — No defect was found in the delivered behaviour.** Every hunk in the diff traces to a plan
step: `store.py` to steps 1 to 3, `cli.py` and `__main__.py` to steps 4 and 5, the two test
modules to step 6 and to steps 1 to 3 respectively. The code implements `ADR-0007`'s format and
`ADR-0008`'s location and write discipline as written, and contradicts no ADR. The three things
beyond the plan's literal text — the second refusal line, the path-prefixed error message, and
`_card()`'s rung range check — are declared in `impl-report.md` under the plan's assumption 2 or
are `ADR-0007`'s own definition of the field, and `verify` reached the same reading independently.

## Accepted gaps

Each of these is now in `item.md`'s `## Notes`, because once this item is `done` nobody reads its
verification report again.

- **AC2's literal machine restart was not performed**, and cannot be in this environment. What
  was substituted is stronger than a code read: a separate process read the exact bytes after the
  writing process exited, and `strace -f -e trace=fsync,rename` on a real `add` shows
  `fsync` → `rename` → `fsync`. Accepted. If anyone reads AC2 as requiring a reboot, the wording
  is what needs revisiting with the stakeholder, not this implementation — `plan.md`'s `## Risks`
  raised it before any code existed and `impl-report.md` and `verify-report.md` both declared it.
- **Two `recall` processes writing at the same moment** were not exercised. No criterion mentions
  concurrency and `ADR-0001` fixes the tool as single-user; the rename-based save makes a torn
  file unlikely rather than impossible. Accepted as unchecked, not as safe.
- **Non-UTF-8 arguments, and a filesystem that does not support `fsync` on a directory**, were
  not exercised. `_fsync_directory()` swallows an `OSError` from either the `open` or the `fsync`
  [src: recall/store.py], so the save still completes on such a filesystem with a weaker
  durability guarantee than `ADR-0008` describes. No criterion names either case.

## Verdict

**Accepted, and closed as `delivered`.** All eight acceptance criteria hold on evidence a reader
can re-run; the record reconstructs the item from the stakeholder's two answers through the plan,
the branch and the verification without a gap; the trial merge is green on the project's own test
and lint commands. One documentation defect was found and repaired in place, one forward-looking
trap was recorded for WI-0002, and three gaps were accepted into `item.md`.

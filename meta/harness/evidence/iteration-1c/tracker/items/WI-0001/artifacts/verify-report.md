# Verification report — WI-0001

Verified-commit: 5288776aeb93ae5d80a74323ba016adda2e49f46

## Verdict

**Pass.** All eight acceptance criteria were checked independently, by deriving from each
criterion what would settle it and running that against the branch head, before reading
`impl-report.md`'s evidence column. Every criterion passes on the commit above. No defect was
found in this item's own behaviour and no bug item was filed against another item.

## Criteria

Every command below was run from the repository root on branch `wi/WI-0001`. `$T` is
`/tmp/vwi1/store.json` and did not exist when its first criterion started; other criteria use
their own fresh paths, named in the command column.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `./expenses add-person Ana --data-file "$T"` then `./expenses list-people --data-file "$T"` | `stdout=[Added Ana] stderr=[] exit=0`; then `stdout=[Ana] stderr=[] exit=0` | stdout, stderr and exit code all compared; stderr was empty on both |
| AC2 | **pass** | a third, separate invocation in a new shell: `bash -c './expenses list-people --data-file /tmp/vwi1/store.json'` | `Ana`, `exit=0` | three distinct processes; nothing could have been held in memory between them |
| AC3 | **pass** | `cp "$T" before.json; ./expenses add-person " ana " --data-file "$T"` | `exit=1 stdout=[] stderr=[Ana is already registered]`, `cmp` reports the file unchanged, `list-people` prints `Ana` and `wc -l` reports 1 | the message names the *stored* spelling, as the criterion quotes; the refusal stored nothing |
| AC4 | **pass** | `./expenses list-people --data-file /tmp/vwi1/absent.json` | `exit=0 stdout=[No one is registered yet] stderr=[]`, and `test -e` reports the file was not created | exit 0, not 1 — "nothing to show" is a true answer (ADR-0005 clause 4) |
| AC5 | **pass** | `./expenses add-person "" `, `"   "`, `"Smith, Jr"`, each `--data-file "$T"` | `exit=1 stderr=[A person's name cannot be blank]` twice, then `exit=1 stderr=[A person's name cannot contain a comma]`; stdout empty each time | `cmp` reports the data file unchanged after all three, and the listing is byte-identical to before |
| AC6 | **pass** | `add-person Cass`, `add-person ana`, `add-person " Ben "` into a fresh file, then `list-people \| cat -A` | `ana$`, `Ben$`, `Cass$` — exactly three lines, in that order | `cat -A` confirms one name per line with no trailing spaces; ` Ben ` was stored trimmed as `Ben`, and `ana` kept its lower-case first spelling |
| AC7 | **pass** | `env HOME=/tmp/vwi1/home ./expenses add-person Ana` with that directory empty, then `ls -A`, then `env HOME=… ./expenses list-people` | `exit=0 stdout=[Added Ana]`; `entries in HOME: [.expenses.json] count=1`; then `Ana`, `exit=0` | exactly one new file, and `README.md` line 54 documents `~/.expenses.json` as the default, which is what the criterion points at |
| AC8 | **pass** | `printf 'not a data file' > $W`, then `./expenses list-people --data-file "$W"` and `./expenses add-person Ana --data-file "$W"` | both: `exit=1 stdout=[] stderr=[Cannot read /tmp/vwi1/garbage.json: it is not valid JSON]`, no `Traceback`, `cmp` reports the file unchanged | the message names the file, as required; the file was not overwritten by either command |

All eight checkboxes in `item.md` were ticked after — and only after — the run recorded above.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` on the branch head → `Ran 27 tests in 1.042s`, `OK`, exit 0. Run by this skill, not read from the report |
| `lint-clean` | **pass** (weak by design) | `python3 -m compileall -q expenses expenses_tool tests` → exit 0. ADR-0007 clause 4 records that this is a syntax check and not a style linter; see `## Not verified, and why` |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the eight rows above, each with a command this skill ran and its quoted output. What each criterion needed was derived from the criterion's own wording before `impl-report.md`'s evidence column was read |
| `negative-cases-exercised` | **pass** | AC3, AC4, AC5 and AC8 are all negative cases and were triggered rather than read about; plus the five extra cases in the next section |

## Negative and boundary cases exercised

Beyond the criteria themselves:

- **A data file claiming a future schema.** `{"schema": 2, "people": []}` →
  `Cannot read …: it uses data file schema 2, and this version understands 1`, exit 1. The tool
  refuses rather than guessing, which is ADR-0006 clause 4.
- **A JSON document that is not an object.** `[]` →
  `Cannot read …: its top level is not a JSON object`, exit 1.
- **Usage errors.** `./expenses add-nobody` → exit 2; `./expenses add-person` with no name →
  exit 2; `./expenses` with no subcommand → exit 2. ADR-0005 clause 3 fixes that code; the item's
  `## Notes` leaves the wording unconstrained, and no assertion was made about it.
- **A whitespace-only name and an empty name** were exercised separately in AC5 rather than
  treated as one case, because they reach the same message by different routes.
- **A duplicate that differs by both case and surrounding whitespace** (` ana ` against `Ana`)
  — the exact combination WI-0001's story exists to prevent.

## Test sensitivity check

Three behaviours were removed in turn, the suite re-run, and the code restored with
`git checkout -- expenses_tool` each time. `git status` afterwards showed no modifications, and
the suite returned to `Ran 27 tests … OK`.

| what was broken | edit | result |
|-----------------|------|--------|
| identity ignores case | `normalise` returns `name.strip()` without `.casefold()` | **FAILED (failures=5)** |
| a refusal is not an error | `EXIT_REFUSED = 0` | **FAILED (failures=6)** |
| an unreadable file reads as an empty store | `load` returns `empty_data()` instead of raising on invalid JSON | **FAILED (failures=3)** |

Each of the three touches a different criterion group (AC3/AC6, AC3/AC5, AC8), and each produced
failures rather than passing silently. The tests are sensitive to the behaviour they claim to
test.

## Defects found

None. No criterion of this item failed, and nothing was found that another item delivered, so no
bug item was filed.

The diff against `main` was read for unaccounted scope: 8 source and documentation files, all
named in `plan.md` steps 1–11, plus the tracker files this pipeline writes. The only code the
plan does not name is the two usage-error tests, which `impl-report.md` declares under
`## Deviations from the plan`. `item.md`'s diff shows only `status`, `branch` and
`updated` changed — no acceptance criterion was touched by `implement`.

## Not verified, and why

- **Style, as opposed to syntax.** `commands.lint` is `compileall`, which proves the files
  parse and nothing more. No style linter is installed and none can be installed here (ADR-0007
  clause 4). Nothing in this verification says anything about naming, unused imports or dead code.
- **The optional `PATH` install.** Every criterion runs `./expenses` from the repository root,
  so the symlink path that ADR-0008 clause 2 exists to support was not exercised. `plan.md`
  `## Risks` names this as the most likely way a real user's first run fails, and it remains
  unchecked by any criterion.
- **An unwritable `--data-file` path.** The item's `## Notes` records this as deliberately
  unconstrained, and `impl-report.md` states plainly that such a path produces a traceback. Not
  verified, because there is no criterion to verify it against — recorded here so that the gap is
  visible rather than absent.
- **Concurrency and crash-during-write.** `store.save` writes to a temporary file and calls
  `os.replace`, which the unit tests exercise for correctness but not for atomicity: killing the
  process mid-write is not something this suite can arrange. The claim in ADR-0006 clause 5 rests
  on `os.replace`'s documented behaviour, not on a test.
- **Non-ASCII names.** `normalise` case-folds but does not fold accents (ADR-0003, option C
  declined). A unit test asserts `José` and `Jose` stay distinct, but no end-to-end criterion
  covers non-ASCII input through the command line.

# Verification report — WI-0001

Verified-commit: fb54eeffc3924e67008e9d48a3de7fbf060ce0a4

Branch `wi/WI-0001`. Every command below was run by this skill against that commit, with
`EXPENSES_STORE` pointed at a fresh directory under `/tmp` so that no result depends on data left
by an earlier check. The outputs quoted are what those runs printed.

## Verdict

**Pass.** All nine acceptance criteria are met, each demonstrated by a command run here rather
than by reading `impl-report.md`. Every criterion that describes a refusal, an empty input or a
boundary was triggered rather than read about — nineteen refusals in total. For every criterion,
a mutation of the code makes its test fail, so no criterion is covered by a test that would pass
against an absent implementation.

One defect was found, and it is not this item's: `BUG-0001`, a documentation defect in
`docs/product/vision.md`, filed at `ready` with `found-in: WI-0001`. It does not affect any
criterion here.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `person add Ana`; `person list`; `person add Ana` again; `person list \| grep -c '^Ana$'`; `person add ana`; `person list` | `added Ana` exit 0; `Ana` exit 0; `Ana is already in the group` exit 2 with the message on stderr only and stdout empty; the count is `1`; `added ana` exit 0; then `Ana` and `ana` on separate lines | the stream split was checked explicitly: `2>/dev/null` prints nothing, `2>&1 1>/dev/null` prints the message |
| AC2 | **pass** | `expense add --amount 30 --paid-by Ana --shared-by Ana,Ben,Cara` against a store holding Ana, Ben and Cara, then reading the JSON | exit 0; the record is `amount_minor: 3000`, `paid_by: "Ana"`, `shared_by: ["Ana","Ben","Cara"]`, `shares_minor: {"Ana":1000,"Ben":1000,"Cara":1000}` | `sum(shares) == amount_minor` evaluated to `True`; 3000 minor units is 30.00 and each share of 1000 is 10.00 |
| AC3 | **pass** | three expenses recorded with different dates, payers, sharer lists and descriptions, then `expense list` | exit 0, three lines: `2026-08-01  30.00  paid by Ana  shared by Ana,Ben,Cara  dinner`, `2026-08-02  12.50  paid by Ben  shared by Ben,Cara  taxi home`, `2026-07-30  4.00  paid by Cara  shared by Ana,Cara  coffee` | one entry per expense, each carrying all five fields. The third was deliberately given the earliest date and still prints last, which is what "in the order the expenses were recorded" requires |
| AC4 | **pass** | `person list` and `expense list` each run twice as separate processes against the store AC3 left, output captured to files and compared with `cmp` and `md5sum` | `cmp` reported no difference for both pairs; the two `person list` captures hash `d29a0147815844fc2c715ea938e608f6` and the two `expense list` captures hash `a3d3be42ee266334be19272e81b57492` | repeated once more from separate subshells: the same `expense list` hash both times |
| AC5 | **pass** | with Ana, Ben and one recorded expense: `expense add --amount 30 --paid-by Ana --shared-by Ana,Dan`, then the same with `--paid-by Dan --shared-by Ana,Ben`; `expense list` captured before and after each | both exit 2, stdout empty, stderr `Dan is not in the group`; `cmp` reports the `expense list` capture byte-identical after each attempt | the data file's own md5 is unchanged across both attempts (`e6eb87b2cb5436ee896a70a4a4d35a1a` before and after), so nothing was written and then undone |
| AC6 | **pass** | all ten inputs the criterion names, each run against a store holding two people and one expense, with both listings captured before and re-compared after every attempt | ten exit codes of 2, ten distinct-enough stderr messages, and `unchanged` for both listings in all ten cases — see `## Negative and boundary cases exercised` for the table | `--amount 0` is refused as "must be greater than zero" and `--amount -4` as not a number, which are different reasons for different inputs rather than one catch-all |
| AC7 | **pass** | four `expense add` runs — neither flag, `--description taxi` alone, `--date 2026-08-01` alone, `--description ""` — then `expense list` and a read of the stored records | all four exit 0. Stored: `('2026-08-27','')`, `('2026-08-27','taxi')`, `('2026-08-01','')`, `('2026-08-27','')`. `expense list` shows today's date on the entry with neither flag | today was computed in the same run as `2026-08-27` rather than hard-coded. Entry 0 and entry 3 compare equal, so `--description ""` records what omitting it records. The flags are independent in both directions |
| AC8 | **pass** | the same four-command sequence run against two fresh, separate stores: add Ana, Ben, Cara, then `expense add --amount 10 --paid-by Ana --shared-by Ana,Ben,Cara --date 2026-08-01`; `expense list` from each compared with `cmp` | exit 0 both times; `cmp` reports the two `expense list` outputs byte-identical; both stores hold `{'Ana': 334, 'Ben': 333, 'Cara': 333}`, summing to 1000 against `amount_minor` 1000 | the shares sum exactly, and the rule is fixed rather than incidental. Which sharer takes the extra unit is not judged here — the criterion deliberately does not name one |
| AC9 | **pass** | `person list` and `expense list` against `EXPENSES_STORE` pointing into a directory that does not exist, and again against a file containing an empty dataset | `no people` exit 0 and `no expenses` exit 0, in both situations | the directory still did not exist afterwards, so a listing does not create the store |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` run by this skill on `fb54eef` → exit 0, `Ran 50 tests in 0.465s`, `OK` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records why the project has no linter. Nothing was checked, so this is not a pass — see `## Not verified, and why` |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 0 errors, 0 warnings, after BUG-0001 was filed and its journal entry written |
| `every-criterion-independently-checked` | **pass** | every row of the criteria table names a command this skill ran and quotes what it printed. `impl-report.md` is not cited as evidence for any criterion |
| `negative-cases-exercised` | **pass** | nineteen refusals triggered: AC1's duplicate, AC5's two unknown names, AC6's ten inputs, and six more boundary probes below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | nine mutations, one per criterion, each making that criterion's test fail — see `## Test sensitivity check` |

## Negative and boundary cases exercised

Every case was run; none is inferred. In each, both listings were captured before the attempt and
compared afterwards.

| input | exit | stderr | listings after |
|-------|------|--------|----------------|
| `--amount 0` | 2 | `amount '0' must be greater than zero` | unchanged |
| `--amount -4` | 2 | `amount '-4' is not a number with at most two decimal places` | unchanged |
| `--amount abc` | 2 | `amount 'abc' is not a number with at most two decimal places` | unchanged |
| `--amount 1.005` | 2 | `amount '1.005' is not a number with at most two decimal places` | unchanged |
| `--shared-by ""` | 2 | `an expense needs at least one sharer, named` | unchanged |
| `--shared-by Ana,Ana` | 2 | `Ana is named twice as a sharer` | unchanged |
| `--date 2026-13-01` | 2 | `date '2026-13-01' is not a real date` | unchanged |
| `--date yesterday` | 2 | `date 'yesterday' is not in YYYY-MM-DD form` | unchanged |
| `person add ""` | 2 | `a person needs a name` | unchanged |
| `person add "   "` | 2 | `a person needs a name` | unchanged |
| `person add Ana` twice | 2 | `Ana is already in the group` | unchanged, and `Ana` appears exactly once |
| `--shared-by Ana,Dan` (unknown sharer) | 2 | `Dan is not in the group` | unchanged, data file md5 identical |
| `--paid-by Dan` (unknown payer) | 2 | `Dan is not in the group` | unchanged, data file md5 identical |

Boundaries beyond the criteria, probed because they are where this design could plausibly break:

- **A store that does not exist at all** — both listings answer and neither creates the file.
- **A store whose parent directory does not exist** — created on the first write; the listing
  before it left nothing behind.
- **An existing file holding an empty dataset** — the same `no people` / `no expenses` answers, so
  AC9 does not depend on the file being absent.
- **`--amount -4` as the first thing after the flag** — argparse does not swallow it as an option;
  it reaches the amount parser and is refused there.
- **An expense whose payer is not among its sharers** — accepted, which is what the item's notes
  say should happen.
- **A date in the future (`2026-08-01` is past, so this was checked against the record rather than
  re-run)** — the item's notes say a future date is accepted rather than second-guessed, and
  `parse_date` applies no such rule; nothing here contradicts it.

## Test sensitivity check

For each criterion, the behaviour it rests on was disabled in a working copy, the criterion's own
test class was run, and the file was then restored from the original text held in memory. The
working tree was confirmed clean afterwards (`git status --short` printed nothing) and the whole
suite re-run to `Ran 50 tests ... OK`.

| AC | what was broken | result |
|----|-----------------|--------|
| AC1 | the duplicate check removed from `store.add_person` | `FAILED (failures=1)` — `test_adding_the_same_person_twice_is_refused_and_leaves_one_ana` |
| AC2 | `amount_minor` stored one unit higher than the amount parsed | `FAILED (failures=1)` — `test_thirty_shared_by_three_records_ten_each_summing_to_thirty` |
| AC3 | the description dropped from the printed line | `FAILED (failures=1)` — `test_each_entry_shows_amount_payer_sharers_date_and_description_in_order` |
| AC4 | `person list` shuffled before printing | `FAILED (failures=1)` — `test_both_listings_are_byte_identical_from_a_fresh_process` |
| AC5 | the "every sharer is known" check removed from `store.add_expense` | `FAILED (failures=1)` — `test_an_unknown_sharer_is_refused_by_name_and_changes_nothing` |
| AC6 | the amount pattern widened to match anything | `FAILED (failures=2, errors=1)` — three of the ten sub-cases |
| AC7 | the default date replaced with a fixed `1999-01-01` | `FAILED (failures=2)` — the two tests that assert on today |
| AC8 | the remainder dropped from `split_equally` | `FAILED (failures=1)` — `test_ten_over_three_sums_to_exactly_ten` |
| AC9 | `no people` replaced with an empty line | `FAILED (failures=1)` — `test_person_list_says_no_people` |

No test survived the removal of the behaviour it claims to cover.

## Defects found

- **BUG-0001** — two absolute claims in `docs/product/vision.md` carry their source in prose but
  not in the citation marker `spec/doc-header.md` section 4a requires, so
  `lint-claims --all` exits 1 while the trunk-scoped run every contracted gate uses exits 0.
  Filed at `ready`, `found-in: WI-0001`, priority `low`. It is a defect in a delivered document,
  not in the tool, and no acceptance criterion of WI-0001 covers `vision.md` — which is why it is
  a bug rather than a send-back. `implement` found the same two errors, recorded them under
  `## What I did not do`, and could not file them: `pipeline.yaml` gives it no creation authority.

Nothing else. No criterion of this item failed.

## Observations that are not defects

Recorded because reading the diff against the plan is part of this skill, and because behaviour
nobody specified is behaviour nobody will verify next time.

- **`store.load` fills in missing `people` and `expenses` keys** rather than refusing a file that
  has `version: 1` and neither. No criterion and no ADR speaks to it; the effect is that a
  truncated file is read as an empty dataset instead of being rejected the way a bad `version` is.
  It cannot be reached through the tool's own commands — `save` always writes both keys — so it is
  not a defect against anything currently asked for. Worth a decision if WI-0003's importer or
  WI-0004's deletion ever writes the file by another path.
- **Four deviations from the plan are declared in `impl-report.md`** — tests committed with their
  module rather than in one pass, `main` taking optional streams, `store` exposing
  `people`/`expenses`/`empty_dataset`, and the confirmation wording. Reading the diff, each is
  where the report says it is, none changes what is delivered, and no hunk in the diff traces to
  anything other than a plan step or a criterion.

## Not verified, and why

- **Lint.** The project declares no lint command (ADR-0004), so nothing checked style, unused
  imports or dead code on this branch. That is the honest state, not a pass. If the constraint on
  installing tools is ever lifted, this is the gate that starts saying something.
- **The default store location.** Every check here set `EXPENSES_STORE`, deliberately: verifying
  the `XDG_DATA_HOME` and `~/.local/share` branches for real would write into the account running
  this session. Their resolution is covered by unit tests that read the resolver's return value
  (`test_store.StorePathTests`, four tests), which is evidence about the path chosen, not about
  writing to it. No acceptance criterion names a location.
- **Concurrent use.** Two processes writing at once is out of scope for the epic and no criterion
  asks for it; it was not attempted.
- **Large datasets.** The largest store used here holds four expenses. Nothing asks for a
  performance bound and none was measured.
- **`--date` in the future.** Judged against the record rather than re-run, as noted above.
- **Behaviour of a hand-edited data file** beyond the `version` and not-JSON refusals that
  `test_store` covers — for instance shares that do not sum to their amount. ADR-0003 accepts that
  a hand-edited file is believed, and no criterion contradicts it.

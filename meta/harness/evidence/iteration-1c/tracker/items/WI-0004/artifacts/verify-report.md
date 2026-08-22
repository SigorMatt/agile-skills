# Verification report — WI-0004

Verified-commit: 89cce7e6bae6a2538d97ab13b4e1e5de70813159

**This is the second verification of this item.** The first, against
`909b394e9154657a04908128163513ccd890f908`, passed all eleven criteria; `review-close` then rejected
the item on **D7** — `README.md` had not been touched and still said, under "What it does not do
yet", that importing a bank CSV export was the next piece of work. `implement` fixed the README and
touched no code. This report replaces the first (which remains in git history and is what
`review.md` cites) and carries the current commit, because the head moved and a verification older
than the code it verifies does not count.

## Verdict

**Pass.** All eleven criteria were re-run end to end against `89cce7e` — not carried over — and all
eleven still hold. Every factual claim the new README makes was checked against the tool, including
running each of its console blocks and comparing the output to what the file says. No defect was
found, no bug item was filed, nothing is sent back.

## What changed since the first verification

`git diff --stat 909b394..89cce7e` is `README.md` plus tracker files. Restricting it to source —
`git diff --stat 909b394..89cce7e -- expenses expenses_tool tests` — produces **no output at all**:
the launcher, all six modules and all six test files are byte-identical to what was verified before.
That fact is established mechanically here rather than assumed, because it is what makes it
defensible to describe this as a re-verification of a documentation change.

The eleven criteria were nevertheless re-run in full. Carrying eleven verdicts across a moved head
on the strength of an empty diff would be an inference, and this skill exists to run commands.

## Criteria

Setup as before: `$T` a fresh data file under `/tmp/reverify/`, `Ana`, `Ben` and `Cass` registered
first, `$F` the two-row example file, `$M` the four mapping options.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | the import against `$F` with `$M` | exactly `Imported 2026-08-14 30.00 Dinner at Luigi — paid by Ana, shared by Ana, Ben, Cass` then `Imported 2026-08-02 9.00 Taxi home — …`; stderr empty; `exit=0` | file order preserved; `Balance` ignored |
| AC2 | **pass** | `./expenses list-expenses` after that import | `2026-08-02 9.00 Taxi home — …` then `2026-08-14 30.00 Dinner at Luigi — …` | today is 2026-08-22 and neither expense carries it |
| AC3 | **pass** | `diff <(list-expenses "$T") <(list-expenses "$U")` and the same for `report`, `$U` built by hand | both empty | reported above as "list identical, report identical" |
| AC4 | **pass** | the three-row `$G` | `exit=0`; stderr exactly `Skipped line 3: 30/02/2026,12.00,Bad date,1188.00`; two lines on stdout | |
| AC5 | **pass** | `--amount-column Value`; a zero-byte file; a header-only file run twice | `Column not found in /tmp/reverify/f.csv: Value` (`exit=1`, data file byte-identical by `cmp`); `/tmp/reverify/empty.csv has no header line`; `No rows imported from /tmp/reverify/h.csv` **on both runs**, so a zero-expense import is still not remembered | |
| AC6 | **pass** | `--shared-by Ana,Dan,Eve` against a file that otherwise imports | `Unknown person: Dan`, `exit=1`, data file unchanged by `cmp` | first unknown named, nothing imported |
| AC7 | **pass** | the import repeated; a `cp` under a new name; then `--again` | `This file was already imported on 2026-08-22. Pass --again to import it anyway`, `exit=1`, for both the original and the renamed copy; after `--again`, `list-expenses` shows **4** lines | identity is the contents, not the name |
| AC8 | **pass** | a non-existent path; a file containing `\xff\xfe\x00` | `Cannot read /tmp/reverify/nope.csv: No such file or directory`; `Cannot read /tmp/reverify/bad.csv: it is not valid UTF-8` | no traceback in either |
| AC9 | **pass** | `cmp` after each refusal above; `grep -cE "open\(\|store\.save\|json\.dump\|os\.replace" expenses_tool/bankcsv.py` | every `cmp` identical; the grep returned **0** | |
| AC10 | **pass** | four runs, each omitting one mapping option | `date-column=exit2 amount-column=exit2 description-column=exit2 date-format=exit2` | |
| AC11 | **pass** | the quoted-and-padded row; the same file prefixed with `\xef\xbb\xbf` | both printed exactly `Imported 2026-08-14 30.00 Dinner, drinks and a taxi — paid by Ana, shared by Ana, Ben, Cass` | |

## The README, which is what this pass was really about

The send-back was a documentation defect, so the documentation is checked the way the criteria are —
by running it, not by reading it approvingly.

| claim | how checked | result |
|-------|-------------|--------|
| the `### Commands` row for `import-csv` lists the right options | `./expenses import-csv --help` | usage line matches the row exactly: `FILE`, `--paid-by`, `[--shared-by]`, the four mapping options, `[--again]`, `[--data-file]` |
| "Every command accepts `--data-file PATH`" (was "Both accept", F6) | `--help` for all six subcommands, grepped for `--data-file` | six of six: yes |
| the import console block | run verbatim | printed the two `Imported …` lines exactly as the README shows them |
| the skipped-row console block | run verbatim | printed `Skipped line 3: 30/02/2026,12.00,Bad date,1188.00` then the one `Imported …` line, exactly as shown |
| the duplicate-file console block | run verbatim | printed `This file was already imported on 2026-08-22. Pass --again to import it anyway`, `exit=1`, exactly as shown |
| "Any other column in the file is ignored" | AC1 | true — `Balance` appears nowhere in the output |
| "it keeps the date from its own row rather than today's" | AC2 | true |
| "Leave `--shared-by` out and everyone registered at that moment shares" | AC6 | true |
| the new exit-codes row: a partial import prints skips on stderr, the rest on stdout, exit 0 | AC4 | true |
| "a file already imported" among the exit-1 refusals | AC7 | true |
| `%d/%m/%Y` for `14/08/2026` | AC1 uses exactly that pairing | true |
| F1: no sentence anywhere says the import is still to come | `grep -n "once the report lands\|Both accept\|will take\|next piece of work" README.md` | no matches outside the `## What it does not do yet` heading itself |
| the pre-existing `### Who owes whom` block | re-run against a fresh ledger | reproduces exactly: `Ana is owed 15.00` / `Ben is square` / `Cass owes 15.00` / blank / `Cass pays Ana 15.00` |
| the pre-existing `### Recording expenses` block | re-run against a fresh ledger | the **behaviour** matches; the transcript shows `2026-08-14` where a run today prints `2026-08-22`, because the example omits `--date` and the default is today. Judged **not** a defect: it is a dated transcript, and the behaviour it illustrates is stated correctly in the bullet above it ("`--date` defaults to today on this machine"). Recorded so it is visible that this was checked and judged rather than missed |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 145 tests in 15.391s` / `OK`, exit 0, on `89cce7e` |
| `lint-clean` | **pass** | `python3 -m compileall -q expenses expenses_tool tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → exit 0 |
| `every-criterion-independently-checked` | **pass** | the table above — eleven criteria, each re-run in this execution against `89cce7e`, none carried over from the first report and none citing `impl-report.md` |
| `negative-cases-exercised` | **pass** | re-run this pass: a wrong column, a zero-byte file, a header-only file twice, an unknown person, a repeat import, a renamed copy, a missing file, a non-UTF-8 file, four missing options, and a `cmp` of the data file after each refusal |
| `tests-would-fail-without-the-change` (advisory) | **pass, on a sample, with the reasoning declared** | The eleven mutations of the first verification were run against code that is byte-identical to this head, which the empty source diff establishes, so they apply unchanged. To keep this pass from being a claim about a previous one, two were re-run here: `utf-8-sig` → `utf-8` killed `AC11ReadingConventions` (1 failure), and replacing AC7's warning text killed `AC7ARepeatImportWarnsAndNeedsAgain` (4 failures). Both reverted; suite green and `git status` clean |

## Negative and boundary cases exercised

A wrong `--amount-column`; a zero-byte file; a header-only file imported twice (to confirm a
zero-expense import is still not remembered); an unknown sharer with a second unknown behind it; a
repeat import; a renamed copy; `--again` and the resulting four listed expenses; a path that does
not exist; a file of invalid UTF-8; each of the four mapping options omitted; a quoted field
containing a comma; padded cells; a leading byte-order mark; a three-row file with an unusable
middle row; and `cmp` of the data file after every refusal.

## Test sensitivity check

Two mutations re-run this pass, both killing their tests and both reverted — see the gate table.
The other nine were run at the first verification against identical code.

**A finding rather than a gap:** `grep -rn "README" tests/` returns one match, and it is a comment.
**No test asserts anything about `README.md`.** The defect that caused this send-back — documentation
claiming a delivered feature does not exist — is invisible to every automated gate this project has,
which is precisely why it survived three closes before `review-close` read the file. Recorded here
because the fix does not remove the exposure: the README can go stale again tomorrow and nothing
will fail.

## Defects found

**None.**

## Not verified, and why

- **AC7's "most recent import date"** — unchanged from the first verification: every import in a
  session happens on one day, so the CLI cannot distinguish the last matching record from the first.
  Covered one layer down by
  `tests/test_store.py::ImportedFiles::test_imported_on_returns_the_last_matching_date`.
- **Atomicity under a real interruption** — AC9 asks for an inspection and it passes; killing the
  process mid-write would test `store.save`, which is WI-0001's code and unchanged here.
- **Behaviour against the stakeholder's real bank export** — nobody has it, by their own decision in
  Q-006, and nothing depends on it. The two likeliest surprises are named in the plan's risks: a
  quoted thousands separator and charges written as negative amounts. Both are skipped-and-reported
  under AC4 rather than silently mishandled.
- **A failing `store.save` still raises a traceback out of `main()`** — pre-existing across every
  command, covered by no criterion of any item.
- **The README's freshness has no automated guard**, as above. What was verified is that it is true
  *now*, at `89cce7e`, by running every claim it makes about this item. Nothing verified that it
  will still be true after the next change, and on this project's evidence it will not be.
- **The nine mutations not re-run this pass** — declared rather than implied. They were run at the
  first verification against byte-identical code; two of the eleven were re-run here as a check on
  that reasoning.

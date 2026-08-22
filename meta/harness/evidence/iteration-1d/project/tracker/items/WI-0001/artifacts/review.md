# Review — WI-0001

Branch `wi/WI-0001`, reviewed at `4c31fb96`. Verification ran at `49dd2a0c`; every commit since is
`tracker/` or `docs/` only, so the verification still covers the code — checked with
`check-verify-freshness`, not assumed.

## What I examined

**The record's mechanics.** `history.md` chains without a gap across eight rows —
`— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review` —
and its last row matches `item.md`'s status. `journal.md` holds nine entries against those eight
transitions; the ninth is a `plan` correction at 02:12:20Z that adds the advisory gate the
preceding entry omitted, written as a new entry rather than an edit, which is what the append-only
rule requires. Every actor named in the history has an entry. All twelve criteria are ticked and
all five questions are `answered` with `## Consequences` naming files that exist — I opened
`docs/product/vision.md` and `docs/architecture/adr/ADR-0002-amount-format-and-rounding.md` from
`Q-001` and `Q-002`'s consequence lists and found the changes they claim.

**The diff**, `main..4c31fb9`, hunk by hunk. Five modules under `expenses/`, six test files,
`docs/architecture/overview.md`, and the tracker's own record.

- `model.py` — `ValidationError`, `_AMOUNT_RE`, `_DATE_RE` (AC6, AC7); `normalise_name` (AC1);
  `parse_name`, `parse_description` (AC1, AC3); `parse_amount`, `format_amount` (AC6, `ADR-0004`);
  `parse_date`, `today` (AC7); `Person`, `Expense`, `Repayment`, `Ledger` with `to_dict`/
  `from_dict` (`ADR-0003`); `find_person` (AC1). Every hunk maps to a criterion or a plan step.
- `store.py` — `resolve_path` (AC9, `ADR-0003`'s precedence), `load`, `save` (AC9, AC10).
- `cli.py` — the parser, `main`, and six handlers, one per command in the plan's interface block.
- `__main__.py` — the entry point named in `ADR-0005`.
- The six test files, mapped in `impl-report.md`'s evidence table and re-derived independently in
  `verify-report.md`'s.

Nothing in the diff serves neither a criterion nor a plan step.

**The ADRs, against the code.** `ADR-0004` specifies `parse_amount` as accepting exactly
`^[0-9]+(\.[0-9]{1,2})?$` above zero; `expenses/model.py:20` is that regex character for
character. `ADR-0003` specifies the JSON shape, the three insertion-ordered arrays, `amount_minor`
as an integer, names stored in display form, the `--file` → `EXPENSES_LEDGER` → XDG precedence,
and an atomic same-directory `os.replace`; `expenses/store.py` and `Ledger.to_dict` implement each
clause. `ADR-0001` requires two record kinds neither expressible as the other; `Expense` and
`Repayment` share no field that would let one stand in for the other, and `AC12`'s listings were
demonstrated separate. `ADR-0005` requires the standard library only; the import lines across the
three modules are `re`, `dataclasses`, `datetime`, `json`, `os`, `tempfile`, `pathlib`, `argparse`
and `sys`. No ADR is contradicted.

**D12 — the claim audit, from the citations rather than from the prose.** Each absolute sentence
in `docs/` about behaviour this item touched, and what I opened to decide it:

| claim | what I opened | verdict |
|-------|---------------|---------|
| `overview.md`: "`cli.py` … is the only module that writes to stdout or stderr and the only one that exits" | `expenses/cli.py`, `expenses/model.py`, `expenses/store.py`, `expenses/__main__.py` | **wrong on the second half.** `cli.main` returns an int and never exits; `__main__.py`'s `raise SystemExit(main(...))` is the only statement in the package that ends the process. Corrected in v3 — see `## Findings` |
| `overview.md`: "`model` imports neither of the others", dependency one-way | the import lines of all three modules | true: `model` imports only `re`, `dataclasses`, `datetime`; `store` imports `model`; `cli` imports both |
| `overview.md`: "no float ever holds money" | every `/`, `float` and `round` in the three modules | true: `format_amount` uses `//` and `%` on ints, and the only `/` operators are `pathlib` joins |
| `overview.md`: "A missing file reads as an empty ledger" | `store.load` | true: `FileNotFoundError` returns `Ledger()` |
| `overview.md`: "`store.py` … knows the file format and nothing about commands" | `expenses/store.py` in full | true: no command name appears in it |
| `overview.md` v2's correction: "`find_person` computes it on each comparison and scans `people` in order" | `Ledger.find_person` | true — this is the sentence v2 fixed, and the fix is accurate |
| `overview.md`: "`--file` … placed after it, `argparse` reports an unrecognised argument and exits 2" | ran `python3 -m expenses people --file /tmp/x.json` | true: `error: unrecognized arguments: --file /tmp/x.json`, exit 2 |
| `overview.md`: "An expense stores its total and the names of its sharers, never a per-person amount" | `Expense.to_dict`, and a written ledger file | true: exactly five keys, none per-sharer |
| `vision.md`: "Nothing is hosted … nothing leaves the machine" | the import lines of all three modules | true: no networking module is imported anywhere |
| `vision.md`: "the tool never holds two groups at once and never compares them" | `store.resolve_path`, `cli.main` | true: one path resolved, one ledger loaded, per run |
| `vision.md`: "An expense is shared equally … no way to say that one person owes more" | `add-expense --help`, `Expense.to_dict` | true: no option and no field for it |
| `ADR-0003`: "Names in `payer`, `sharers`, `from` and `to` are stored in the display form the person first typed" | a written ledger after `add-expense --payer ANA --shared-by "  ben  "` | true: stored `Ana` and `Ben` |

One claim I am recording rather than passing: `overview.md` says keeping the validators in
`model.py` "is what lets WI-0003's importer reuse them, so the import **cannot** accept an amount
or a date the hand-entry command would refuse". WI-0003 does not exist, so nothing enforces this
yet — it is an intention stated as a guarantee. It is true of the module boundary and false as a
property of a program nobody has written. Left as written because it reads as design intent in
context, and flagged here so that whoever closes WI-0003 re-audits it rather than re-quoting it.

**The declared gaps** in `verify-report.md`'s `## Not verified, and why` and `impl-report.md`'s
`## What I did not do` — all eleven entries, judged individually. Five are accepted and are now
written into `item.md`'s `## Notes`; the rest are restatements of things this review confirmed.

**The trial merge.** `wi/WI-0001` merged into a throwaway branch off `main`: clean, no conflicts.
`python3 -m unittest discover -s tests -t . -q` on the **merge result** → exit 0, `Ran 83 tests`,
`OK`; `compileall` → exit 0; `validate-workspace` → exit 0. The trial branch was then deleted
unmerged, and the item closed before the real merge, because `check-commit-refs` reads
`main..wi/WI-0001` and merging first empties that range.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion checkbox ticked | **pass** | `grep -c "^- \[x\] AC" tracker/items/WI-0001/item.md` → 12, and no `- [ ] AC` remains |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | its criteria table has a row per AC1–AC12, each with the command `verify` ran and the output it produced; I spot-checked AC6 and AC9 by re-running the amount refusals and the mode-500 case and got the outputs the table records |
| D3 | all declared gates passed on the **final** state of the code | **pass** | `implement`'s seven gates ran at `5e83721`; `verify`'s six at `49dd2a0`; the only commits after `49dd2a0` are `tracker/` and `docs/`, so no gate is older than the code it covers. Re-run here at `4c31fb9`: tests exit 0, lint exit 0, `validate-workspace` exit 0, `lint-claims` exit 0 |
| D4 | no open blocking question | **pass** | all five questions on the item are `status: answered`, `answered-by: human`; no question anywhere in the workspace is `open` |
| D5 | a journal entry per execution; history chains without a gap | **pass** | eight history rows chaining `—`→`in-review`, each `from` equal to the previous `to`; nine journal entries, one per row plus the `plan` correction at 02:12:20Z; `validate-workspace` → 0 errors |
| D6 | every design decision is in an ADR, cited from the plan or journal | **pass** | `ADR-0003` (one JSON ledger, XDG default, atomic write), `ADR-0004` (integer minor units) and `ADR-0005` (standard library only) were written by `plan` and are cited in `plan.md`'s `## Decisions and ADRs` table; `ADR-0001` and `ADR-0002` predate the plan and are cited from it and from the criteria. No decision in the diff lacks a record |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` v1 → v2 by `implement` (the `find_person` index claim), v2 → v3 by this review (the "only one that exits" claim), each with its own change-log row. `docs/product/vision.md` was read against the code and needed no change |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 12 commit(s) on main..wi/WI-0001 name WI-0001" |
| D9 | the change is merged into the trunk | **pass** | merged after the close, in the order step 8 requires; the merge commit is named in the journal entry for this execution |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: "verified at 49dd2a0c; wi/WI-0001 has moved to 4c31fb96 but only the record changed (9 file(s) under tracker/ or docs/)". Compared, not assumed |
| D11 | `review.md` exists and states what was examined | **pass** | this document; `## What I examined` is its first section |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, checked against the code; absolute claims written here carry a resolvable citation | **pass, after one correction** | the twelve-row audit table above, each row naming what I opened. One claim was wrong and is corrected in `overview.md` v3. `lint-claims --changed-since main` → exit 0 |

## Findings

1. **`overview.md` claimed `cli.py` is "the only one that exits"; it is not.** `cli.main` returns
   an int and `expenses/__main__.py`'s `raise SystemExit(main(...))` is the only statement in the
   package that ends the process. The sentence survived from v1 through v2. Fixed here rather than
   sent back: it is one sentence in a document, no code is wrong, and a send-back would cost a
   full `implement` → `verify` → `review-close` cycle to change a clause. Recorded as
   `overview.md` v3 with its own change-log row. This is the D12 failure mode exactly — a
   confident sentence nobody re-read against the code — caught by opening the modules rather than
   by re-reading the sentence.
2. **`--file ""` silently falls through to the default location.** `store.resolve_path` tests
   `if cli_file:`, so an empty string is treated as "not given". Confirmed:
   `python3 -m expenses --file "" add-person Ana` exits 0 and writes to the XDG default. Not a
   send-back — no criterion covers an empty path, and the behaviour mirrors `ADR-0003`'s explicit
   rule that an empty `EXPENSES_LEDGER` falls through — but it is now an accepted gap in
   `item.md`, flagged for WI-0003, which is the first item that will pass paths programmatically.
3. **`cmd_add_person` calls `ledger.find_person(name)` twice on the duplicate path** — once to
   test, once to interpolate into the message. Cosmetic at this scale and not worth a change;
   named so that it is a known shape rather than a discovery.
4. **BUG-0001, filed by `verify`, is correctly routed.** I re-ran its reproduction: with the
   ledger's directory at mode 500, `add-person` prints `Added Cara.` on stdout, `error: cannot
   write the ledger at …` on stderr, and exits 1. WI-0001's criteria define a refusal as a stderr
   message, a non-zero exit and unchanged data — all three hold — so this is genuinely outside
   this item's criteria and belongs in its own item rather than as a send-back. Agreed with the
   classification.

Nothing found rises to a rejection. No hunk is unrequested, no ADR is contradicted.

## Accepted gaps

Five, all now written into `item.md`'s `## Notes` under "Gaps accepted at close", because a gap
recorded only in a report that nobody reopens is not accepted but lost:

1. The on-disk `version` field is written and never read, so a future incompatible ledger would be
   parsed as version 1 rather than refused.
2. Two concurrent writers can lose an update; `os.replace` gives atomicity, not serialisation.
3. `--file ""` falls through to the default rather than being refused (finding 2).
4. `lint-clean` is a `compileall` syntax check, so unused imports, shadowed names and type errors
   are outside every gate this project runs (`ADR-0005`).
5. The literal `~/.local/share/expenses/ledger.json` was never written to; `XDG_DATA_HOME` and
   `HOME` were redirected instead, which is what the tool sees as "no location given".

Each names who should pick it up. One further gap — that `overview.md`'s "the import **cannot**
accept an amount or a date the hand-entry command would refuse" is an intention about WI-0003
rather than a property of anything that exists — is recorded in `## What I examined` for whoever
closes WI-0003.

## Verdict

**Accepted, and closed as `delivered`.** All twelve criteria are met with evidence gathered
independently by `verify` and spot-checked here; the Definition of Done passes on all twelve
criteria, one after a documentation correction made in this review; the branch merges cleanly and
the full suite passes on the merge result. The record answers, from the tracker and `git log`
alone, what was built and why, which skill decided what, what the five stakeholder questions were
and how their answers reached the artifacts, and what verification found — including the one
defect it found that no criterion covers, which is now BUG-0001.

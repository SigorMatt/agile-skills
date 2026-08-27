# Verification report — WI-0004

Verified-commit: beb522ed117436107fd317c850a85d46782260d5

This is the **second** verification of WI-0004. The first, at `f4e8319`, passed all eight
criteria; `review-close` then rejected the item on Definition of Done D7 and D12 — the record in
`docs/`, not the code — and `implement` fixed that and sent it back here. The first report is kept
in full as an appendix at the end of this file.

## Verdict

**Pass.** All eight acceptance criteria are met on `beb522e`. Every verdict below rests on a
command this execution ran against the branch head, in `/tmp/v5/` scratch stores created fresh
for each case. No criterion was inherited from the previous verification and none was taken from
`impl-report.md`; the checkboxes in `item.md` were already ticked when this execution started, and
each was re-demonstrated before it was left ticked. No defect was found and no bug item was filed.

**One mechanical fact frames the whole of it, and it was established rather than assumed:**
`git diff --stat f4e8319..HEAD -- expenses/ tests/ README.md` is **empty**. The code, the tests
and the README under verification are byte-identical to what the first verification examined. The
three commits since are `af331b8` and `beb522e` (tracker) and `e2a0b3d` (`docs/`). That does not
excuse re-running anything — it is the reason the criteria all still pass, not a substitute for
checking that they do.

## Criteria

Every command below was run with `EXPENSES_STORE` pointing into `/tmp/v5/`, with the store file
deleted and rebuilt before each case. "TWO-EXPENSE STORE" is the four-command sequence `item.md`
defines.

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `person add Ana`; `person add Ben`; `python3 -m expenses person delete Ben`; `python3 -m expenses person list` | delete → exit 0; stdout `od -c` first line identical to that of `printf 'deleted Ben\n'`. list → exit 0; stdout `od -c` identical to `printf 'Ana\n'` | compared as bytes through `od -c`, because "exactly … followed by a newline" is a claim about bytes, not about what a terminal shows |
| AC2 | **pass** | TWO-EXPENSE STORE; `expense list`; `awk '{print $1}'`; `expense delete 2`; `expense list`; `expense delete 1`; `expense list` | listing → exit 0, `wc -l` = 2, first fields `1 2`; the lines were `1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  Taxi` and `2  2026-08-02  10.00  paid by Ben  shared by Ana,Ben`. `expense delete 2` → exit 0, stdout bytes = `deleted expense 2\n`. Listing after → `wc -l` = 1, exactly `1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  Taxi`. `expense delete 1` → exit 0; listing after → bytes = `no expenses\n` | the renumbering is checked by the string equality of the remaining line, which begins `1` where it had begun `1` and would have begun `2` had the position been stored rather than computed |
| AC3 | **pass** | for `Ben` then `Ana`, against a freshly rebuilt TWO-EXPENSE STORE each time: `md5sum`; `person delete <NAME>`; `md5sum`; `person list` | `Ben` → exit 2, stdout `wc -c` = 0, stderr `Ben is named in 2 expense(s); delete those first`. `Ana` → exit 2, stdout 0 bytes, stderr `Ana is named in 2 expense(s); delete those first`. md5 identical before and after in both cases. `person list` → `Ana,Ben,` (newlines shown as commas) | both tokens the criterion demands are present in each message: the name, and `2` as the count. "prints nothing at all to stdout" is measured with `wc -c`, not eyeballed |
| AC4 | **pass** | TWO-EXPENSE STORE; `expense delete 1`; `expense delete 1`; `expense list`; `person delete Ben`; `person list` | listing after the two deletions → `no expenses`; `person delete Ben` → exit 0, stdout bytes = `deleted Ben\n`; `person list` → bytes = `Ana\n` | the second `expense delete 1` removes what the renumbering made expense 1, which is the criterion's point. It passes, so AC3's refusal is about the expenses and not a blanket refusal |
| AC5 | **pass** | `/tmp/v5/ac5.py`: the deletion **and** the listing are run by calling `expenses.cli.main` twice inside **one** Python process, capturing stdout; the same listing is then run as a separate `python3 -m expenses` subprocess; the two strings are compared | person: one-process `'Ana\n'`, fresh-process `'Ana\n'`, identical. expense: one-process `'1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  Taxi\n'`, fresh-process identical. Script exit 0 | deliberately built this way. Every other command in this report is already its own process, so comparing two shell runs would test nothing: the point of AC5 is that the deletion reached the **disk**, not merely the in-memory dataset the deleting process still holds |
| AC6 | **pass** | store = Ana, Ben, one 30.00 paid by Ana shared by both. Part 1: `settle`; `expense delete 1`; `settle`. Part 2, store rebuilt: `settle > s3`; `person delete Ben`; `settle > s4`; `cmp s3 s4` | Part 1: `settle` → exit 0, bytes = `Ben pays Ana 15.00\n`; after the deletion → exit 0, bytes = `no payments needed\n`. Part 2: `person delete Ben` → exit 2, `Ben is named in 1 expense(s); delete those first`; `cmp` → exit 0, byte-identical, still `Ben pays Ana 15.00` | checked positively as well, by loading the stored JSON and differencing every `paid_by`, every `shared_by` entry and every `shares_minor` key against `data["people"]`: **no names in expenses but not in people**. That is ADR-0007's invariant, observed on the data rather than argued from the code |
| AC7 | **pass** | seven cases against a rebuilt TWO-EXPENSE STORE, each bracketed by `md5sum`; then the two cases against a store whose file does not exist, with `[ -e $S ]` afterwards | all seven → exit 2, stdout 0 bytes, non-empty stderr, md5 unchanged: `Nobody is not in the group`; `ana is not in the group`; `'' is not in the group`; `there is no expense 3`; `expense '0' is not a positive whole number`; `expense '-1' is not a positive whole number`; `expense 'abc' is not a positive whole number`. Empty store: `person delete Ana` → 2, `Ana is not in the group`; `expense delete 1` → 2, `there is no expense 1`; `[ -e $S ]` false after both | `expense delete -1` is the case worth running rather than reasoning about: argparse could have claimed it as an option. It does not, and the tool's own refusal is what appears. `person delete ana` confirms names are compared exactly, as WI-0001 AC1 requires |
| AC8 | **pass** | `grep -c "person delete" README.md` and the same for `expense delete`; `grep -n -A4 '^\$ python3 -m expenses person delete'` and the `expense delete` equivalent; `sed -n '/\$ python3 -m expenses expense list/,/^```$/p' README.md`; read of lines 48–72 and 108–126 | (a) 3 occurrences of each literal; `### \`person delete <NAME>\`` shows `$ python3 -m expenses person delete Ben` → `deleted Ben`, and `### \`expense delete <NUMBER>\`` shows `$ python3 -m expenses expense delete 2` → `deleted expense 2`. (b) the sample listing is `1  2026-08-01  30.00  …` / `2  2026-08-02  10.00  …` — every line begins with its position. (c) "**Deleting a person named in a recorded expense is refused**, and the message says how many expenses stand in the way. Delete those expenses first, and then the person", followed by a worked example showing the real message. (d) "**The numbers renumber after a deletion.** They are positions in the listing you are looking at, not names that stay with an expense: delete expense 2 and what was 3 becomes the new 2." | all four checks are present. AC8's closing sentence is met: the refusal is shown with its actual message and the renumbering with a worked example, so a reader who has not seen this item learns both what the commands do and what they refuse |

## The change since the last verification, and what was checked about it

This round's only change is `docs/architecture/overview.md`, from version 4 to version 5. **No
acceptance criterion covers that file** — AC8 is about `README.md` — so it cannot be passed or
failed here, and the Definition of Done judgement on it (D7 and D12) belongs to `review-close`.
What this skill can do is record observations, made by opening the code:

- The document is at `version: 5`, `updated-by: implement`, `updated-for: WI-0004`, with a
  change-log row naming the item.
- `grep -c "two new functions" docs/architecture/overview.md` → **0**. The phrase the review
  called false is gone.
- The `expenses/store.py` piece now says "three" and names `naming_expenses`, `delete_person` and
  `delete_expense`. `grep -n "^def " expenses/store.py` returns exactly those three among its
  eleven functions, so the count matches the code.
- `## What is coming` now contains WI-0003 and nothing else. The deletion commands are described
  in `## The pieces, and why each exists`, under `expenses/store.py` and `expenses/cli.py`.
- The invariant stated there — every name in a stored expense is a name in `data["people"]` — is
  the same one AC6's positive check above observed holding in the stored data.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` run by this skill on `beb522e` → exit 0, `Ran 120 tests in 1.214s`, `OK` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 is the standing decision that this project installs nothing and the standard library ships no linter. This gate checked nothing — it is not a pass. See `## Not verified, and why` |
| `workspace-valid` | **pass** | `.claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 7 item(s), 9 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | the Criteria table records, for each of AC1–AC8, the command **this execution** ran and the output it produced. No row cites `impl-report.md` or the appendix |
| `negative-cases-exercised` | **pass** | AC3's two refusals, all seven AC7 argument vectors, AC7's two empty-store cases, AC6's refused `person delete`, and AC2's boundary (deleting the last remaining expense) were each triggered. See the section below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | five probes, below. Each behaviour was disabled in the working tree, the tests claiming to cover it were run, and the tree was restored with `git checkout --`; `git status --short` is empty afterwards and the full suite returns to `Ran 120 tests`, `OK` |

## Negative and boundary cases exercised

Each was produced by running the command, not by reading that it exists. Exit codes and stderr
are quoted from this execution.

- **AC3 — a person named in expenses, as payer and as sharer:** `person delete Ben` → exit 2,
  `Ben is named in 2 expense(s); delete those first`; `person delete Ana` → exit 2,
  `Ana is named in 2 expense(s); delete those first`. md5 unchanged across both.
- **AC7 — a name not in the group:** `person delete Nobody` → `Nobody is not in the group`.
- **AC7 — a name differing only in case:** `person delete ana` → `ana is not in the group`.
- **AC7 — an empty name:** `person delete ""` → `'' is not in the group`.
- **AC7 — a position past the end:** `expense delete 3` → `there is no expense 3`.
- **AC7 — zero, a negative, and a non-number:** `expense delete 0`, `expense delete -1`,
  `expense delete abc` → `expense '<n>' is not a positive whole number`, all exit 2.
- **AC7 — a store that does not exist:** `person delete Ana` and `expense delete 1` against a
  missing file, both exit 2, and `[ -e $S ]` false afterwards — neither created the file.
- **AC2 — deleting the last remaining expense:** the listing afterwards is `no expenses`, not an
  empty listing and not a crash.
- **AC6 — a refused deletion followed by `settle`:** `cmp` on the settlement before and after
  → identical.

## Test sensitivity check

Five probes, run by this execution. The full suite was `OK` before and after.

| # | behaviour disabled | tests run | result |
|---|--------------------|-----------|--------|
| A | the position column removed from `cli.expense_list` | `WI0004AC2…`, `AC3ExpenseListShowsEveryField` | `Ran 5 tests … FAILED (failures=3)` — AC2's numbering and the WI-0001 order test both catch it |
| B | `store.delete_person`'s refusal short-circuited (`named_in = []`) | `WI0004AC3…`, `WI0004AC6…`, `test_store.DeletePersonTests` | `Ran 9 tests … FAILED (failures=5)` |
| C | `store.save()` dropped from both delete handlers (2 call sites patched) | `WI0004AC5…`, `WI0004AC1…`, `WI0004AC4…` | `Ran 4 tests … FAILED (failures=4)` |
| D | `store.delete_expense`'s range check removed | `test_store.DeleteExpenseTests`, `WI0004AC7…` | `Ran 7 tests … FAILED (failures=2, errors=5)` |
| E | `README.md` reverted to `main`'s version | `WI0004AC8…` | `Ran 3 tests … FAILED (failures=3)` |

Coverage: AC1 by C; AC2 by A and C; AC3 by B; AC4 by C; AC5 by C; AC6 by B; AC7 by D; AC8 by E.
Every criterion has at least one test that stops passing when its behaviour is taken away.

After the last probe: `git status --short` → empty, and
`python3 -m unittest discover -s tests -t .` → `Ran 120 tests in 1.209s`, `OK`.

## Defects found

**None.** No criterion of this item failed, and nothing delivered by WI-0001 or WI-0002 was found
broken. Two cross-item checks, because this item changes output another item delivered:

- `expense list`'s leading column does not break WI-0001 AC3 — the listing observed above shows
  the date, amount, payer, sharers and description in recorded order with the position prepended,
  and `AC3ExpenseListShowsEveryField` passes in the 120-test run.
- `settle` is untouched by this round: `git diff --stat f4e8319..HEAD -- expenses/` is empty, and
  AC6's settlements above are byte-exact.

The diff was read against the plan again this round (`git diff main..HEAD -- expenses/`). The
hunks are the same set the first verification traced: `store.py` → plan steps 1–3, `cli.py` →
steps 4–6 (`parse_position`, `person_delete`, `expense_delete`, the two subparsers, the two
`HANDLERS` entries and the `expense_list` line change), `tests/` → steps 7–9, `README.md` →
step 10. Nothing outside them.

## Not verified, and why

- **`lint-clean` checked nothing.** `commands.lint` is `null`, so no tool looked at this item's
  diff for style, unused imports or dead code — only human reading. ADR-0004 is the standing
  decision behind that; it is a known project-wide gap, not one this item introduced.
- **AC8(c) and AC8(d) were verified by reading, not by a test.** That is what AC8 asks for, but a
  future edit deleting the refusal sentence or the renumbering sentence from `README.md` would
  not be caught by the suite. This should be recorded in `item.md`'s `## Notes` at close.
- **The refusal message strings are not pinned by any criterion.** AC3 requires only the name and
  the count. A reworded message keeping both would pass AC3 unchallenged.
- **`docs/architecture/overview.md` v5 was inspected but not judged.** The observations above are
  facts this skill checked; whether they satisfy Definition of Done D7 and D12 is
  `review-close`'s decision, and this report does not pre-empt it.
- **Nothing was verified on any platform but this one**, no dataset written by an older version
  was tested (none exists — `store.VERSION` is unchanged), and **concurrency was not tested**;
  the product is one person at one terminal on one machine.

---

# Appendix — the first verification, at `f4e8319`

Kept verbatim. Its verdict was superseded only in the sense that the item left `verifying` and
came back; nothing in it was found wrong. Its `Verified-commit` line is quoted below rather than
left as a header, so that only this round's line is machine-readable.

> **Verified-commit (first verification): `f4e8319c2e58bf6daae6e41264ddc1f0c0525f85`.**

### Verdict

**Pass.** All eight acceptance criteria are met. Every verdict below rests on a command run in
this execution against the branch head, in a fresh shell with `EXPENSES_STORE` pointed at a
scratch path under `/tmp/v4/` that did not exist beforehand — not on anything
`artifacts/impl-report.md` claims. No defect was found in this item's behaviour and no bug item
was filed.

What was checked *from the criteria first*: each criterion's own text was turned into a command
and an observation before the implementation was read, which is why the evidence below is shell
output and `od -c` byte dumps rather than test names. The test suite was then run as a gate, and
its sensitivity probed separately.

### Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `person add Ana`; `person add Ben`; `python3 -m expenses person delete Ben`; `python3 -m expenses person list` | `person delete Ben` → exit 0, stdout `od -c`: `d e l e t e d   B e n \n` (12 bytes, nothing else). `person list` → exit 0, stdout `od -c`: `A n a \n` (4 bytes) | stdout compared byte-for-byte with `od -c`, not by eye: "exactly `deleted Ben` followed by a newline" is a byte claim |
| AC2 | **pass** | against the TWO-EXPENSE STORE: `expense list`; `expense list \| awk '{print $1}'`; `expense delete 2`; `expense list`; `expense delete 1`; `expense list` | listing → exit 0, two lines: `1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  Taxi` and `2  2026-08-02  10.00  paid by Ben  shared by Ana,Ben`; first fields `1` then `2`. `expense delete 2` → exit 0, stdout `d e l e t e d   e x p e n s e   2 \n`. Listing after → exactly one line, `1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  Taxi` (`wc -l` = 1). `expense delete 1` → exit 0, `deleted expense 1`. Listing after → `n o   e x p e n s e s \n` | the remaining fields are what WI-0001 AC3 requires — date, amount, payer, sharers, description — with the position prepended |
| AC3 | **pass** | against the TWO-EXPENSE STORE, for `Ben` then `Ana`: `md5sum $S`; `python3 -m expenses person delete <NAME>`; `md5sum $S`; `person list` | `person delete Ben` → exit 2, stdout 0 bytes, stderr `Ben is named in 2 expense(s); delete those first`. `person delete Ana` → exit 2, stdout 0 bytes, stderr `Ana is named in 2 expense(s); delete those first`. md5 `efab820fb30908cd3f279d8d6941333d` before **and** after both attempts. `person list` still prints `Ana` and `Ben` | both required tokens are in each message: the name, and `2` as the count. stdout was measured with `wc -c` = 0, so "prints nothing at all to stdout" is checked rather than assumed |
| AC4 | **pass** | against the TWO-EXPENSE STORE: `expense delete 1`; `expense delete 1`; `expense list`; `person delete Ben`; `person list` | the two deletions print `deleted expense 1` twice and leave `no expenses`; `person delete Ben` → exit 0, stdout `d e l e t e d   B e n \n`; `person list` → `A n a \n` | this is the criterion that rules out an implementation refusing every person-deletion. It passes, so AC3's refusal is about the expenses |
| AC5 | **pass** | the deletion and the listing run in **one** python process (calling `expenses.cli.main` twice, capturing stdout), then the same listing run as a fresh `python3 -m expenses`, then `cmp` on the two captures — once for `person delete Ben`, once for `expense delete 2` | person: in-process listing `'Ana\n'`; fresh-process listing `A n a \n`; `cmp` → identical. expense: in-process `'1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  Taxi\n'`; fresh-process byte-identical; `cmp` → identical | run this way deliberately. Every other command in this report is already a fresh process, so comparing two shell invocations would not have tested what AC5 asks — that the deletion reached the disk rather than only the in-memory dataset |
| AC6 | **pass** | store = Ana, Ben, one 30.00 paid by Ana shared by both. Part 1: `settle`; `expense delete 1`; `settle`. Part 2 (rebuilt store): `settle > s3`; `person delete Ben`; `settle > s4`; `cmp s3 s4` | Part 1: `settle` → exit 0, `B e n   p a y s   A n a   1 5 . 0 0 \n`; after the deletion → exit 0, `n o   p a y m e n t s   n e e d e d \n`. Part 2: `person delete Ben` → exit 2, `Ben is named in 1 expense(s); delete those first`; `cmp` → byte-identical, `Ben pays Ana 15.00` | the second half is the one that matters: the refusal is what stops `settle` ever computing over a name `person list` does not show. Confirmed positively as well — every `paid_by` and every `shares_minor` key in the stored file is in the `person list` output |
| AC7 | **pass** | seven cases against the TWO-EXPENSE STORE, each wrapped in `md5sum` before and after; then two cases against a store whose file does not exist, with `[ -e $S ]` afterwards | `person delete Nobody` → 2, 0B stdout, `Nobody is not in the group`. `person delete ana` → 2, 0B, `ana is not in the group`. `person delete ""` → 2, 0B, `'' is not in the group`. `expense delete 3` → 2, 0B, `there is no expense 3`. `expense delete 0` → 2, 0B, `expense '0' is not a positive whole number`. `expense delete -1` → 2, 0B, `expense '-1' is not a positive whole number`. `expense delete abc` → 2, 0B, `expense 'abc' is not a positive whole number`. md5 unchanged for all seven. Empty store: `person delete Ana` → 2, `Ana is not in the group`, file does not exist; `expense delete 1` → 2, `there is no expense 1`, file does not exist | `expense delete -1` was the case worth watching: argparse could have intercepted it as an option. It does not — no option string on that subparser looks like a negative number — so it reaches the tool's own refusal and behaves like the other six. All seven are exit 2, the tool's documented refusal status |
| AC8 | **pass** | `grep -n "person delete\|expense delete" README.md`; `sed -n '/\$ python3 -m expenses expense list/,/^```$/p' README.md`; read of `README.md` lines 50–70 and 111–126 | (a) both literal strings present; `### \`person delete <NAME>\`` shows `$ python3 -m expenses person delete Ben` → `deleted Ben`, and `### \`expense delete <NUMBER>\`` shows `$ python3 -m expenses expense delete 2` → `deleted expense 2`. (b) the `expense list` sample is `1  2026-08-01  …` / `2  2026-08-02  …` — every line begins with the position. (c) "**Deleting a person named in a recorded expense is refused**, and the message says how many expenses stand in the way. Delete those expenses first, and then the person". (d) "**The numbers renumber after a deletion.** They are positions in the listing you are looking at, not names that stay with an expense: delete expense 2 and what was 3 becomes the new 2." | AC8's closing sentence — that a reader who has not seen the item can tell what the commands do and what they refuse to do — is met: the refusal is shown with its actual message, and the renumbering is stated with a worked example. The two `[src: …]` markers added point at `ADR-0006-an-expense-is-addressed-by-its-position-in-the-listing.md` and `ADR-0007-referential-consistency-is-enforced-where-data-is-written.md`, both of which exist on disk |

### Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` run by this skill on `f4e8319` → exit 0, `Ran 120 tests in 1.206s`, `OK` |
| `lint-clean` | **skipped** | `commands.lint` is `null` in `tracker/project.yaml`; ADR-0004 records that this project installs nothing and the standard library ships no linter. This gate checked nothing — see `## Not verified, and why` |
| `workspace-valid` | **pass** | `.claude/agile-skills/scripts/validate-workspace .` → exit 0, `checked 7 item(s), 9 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | the Criteria table above records, for each of AC1–AC8, the command this skill ran and the output it produced. No row cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | AC3's two refusals, all seven of AC7's argument vectors, AC7's two empty-store cases, AC6's refused `person delete`, and AC2's boundary — deleting the last remaining expense — were each triggered, not read about. See `## Negative and boundary cases exercised` |
| `tests-would-fail-without-the-change` (advisory) | **pass** | six probes, below; each behaviour was disabled, the relevant tests were run, and the working tree was restored with `git checkout -- <path>` and confirmed clean by `git status --short` |

### Negative and boundary cases exercised

Each of these was produced by running the command, not by reading that it exists.

- **AC3 — a person named in expenses, both as payer and as sharer.** `person delete Ben` and
  `person delete Ana`, both refused, both with the count in the message, md5 unchanged across
  both attempts.
- **AC7 — a name that is not in the group:** `person delete Nobody` → `Nobody is not in the group`.
- **AC7 — a name that differs only in case:** `person delete ana` where the group holds `Ana` →
  `ana is not in the group`. Names are compared exactly, as WI-0001 AC1 requires.
- **AC7 — an empty name:** `person delete ""` → `'' is not in the group`.
- **AC7 — a position past the end:** `expense delete 3` against two expenses →
  `there is no expense 3`.
- **AC7 — zero and a negative position:** `expense delete 0` and `expense delete -1`, both
  `expense '<n>' is not a positive whole number`, both exit 2. The `-1` case reaches the tool's
  own refusal rather than argparse's error path.
- **AC7 — a position that is not a number:** `expense delete abc`, same shape.
- **AC7 — a store that does not exist:** `person delete Ana` and `expense delete 1` against a
  missing file, both refused, and `[ -e $S ]` false afterwards — neither created the file.
- **AC2 — deleting the last remaining expense:** the listing afterwards prints `no expenses`
  rather than an empty listing or a crash.
- **AC6 — a refused deletion followed by `settle`:** byte-identical output before and after.
- **Beyond the criteria, from plan step 4's "afterwards" list:** `person delete --help` → exit 0,
  `expense delete --help` → exit 0, and `python3 -m expenses expense` with no action → exit 2,
  which is what it did before this item.

### Test sensitivity check

Six probes. In each, the behaviour was disabled in the working tree, the tests that claim to
cover it were run, and the tree was then restored with `git checkout --` and verified clean.

| # | behaviour disabled | tests run | result |
|---|--------------------|-----------|--------|
| 1 | the position column removed from `cli.expense_list` | `WI0004AC2…`, `AC3ExpenseListShowsEveryField` | `Ran 5 tests … FAILED (failures=3)` — AC2's numbering and WI-0001's repaired order test both catch it |
| 2 | `store.delete_person`'s refusal short-circuited (`named_in = []`) | `WI0004AC3…`, `WI0004AC6…`, `test_store.DeletePersonTests` | `Ran 9 tests … FAILED (failures=5)` |
| 3 | `cli.parse_position`'s refusal replaced by `int()` with a `0` fallback | `WI0004AC7…` | `Ran 2 tests … OK` — **the tests correctly did not fail.** This probe did not remove the behaviour, it moved it: `0`, `-1` and `abc` all reduce to a position `store.delete_expense` refuses anyway, so every AC7 observation still holds. Probe 5 is the one that removes the behaviour, and it fails |
| 4 | `store.save()` dropped from both delete handlers | `WI0004AC5…`, `WI0004AC1…`, `WI0004AC2…`, `WI0004AC4…` | `Ran 7 tests … FAILED (failures=6)` — AC5 is the criterion this targets and it catches it |
| 5 | `store.delete_expense`'s range check removed | `test_store.DeleteExpenseTests`, `WI0004AC7…` | `Ran 7 tests … FAILED (failures=2, errors=5)` |
| 6 | `README.md` reverted to `main`'s version | `WI0004AC8…` | `Ran 3 tests … FAILED (failures=3)`; restored, then `OK` |

Every criterion has at least one probe that fails when its behaviour is removed: AC1 and AC4 and
AC5 by probe 4, AC2 by probes 1 and 4, AC3 and AC6 by probe 2, AC7 by probe 5, AC8 by probe 6.

### Defects found

**None.** Nothing in this item's behaviour failed its own criteria, and nothing in behaviour
delivered by WI-0001 or WI-0002 was found broken by it. Two things were checked specifically
because this item changes output another item delivered:

- `expense list`'s new leading column does not break WI-0001 AC3, which requires each entry to
  show its amount, payer, sharers, date and description in recorded order. Checked directly:
  `1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  dinner` /
  `2  2026-08-02  12.50  paid by Ben  shared by Ben  taxi`. All five fields, recorded order,
  position prepended.
- `settle`'s output is untouched by this item; WI-0002's own tests pass unchanged in the 120-test
  run.

The diff against the plan was read (`git diff main..HEAD -- expenses/ README.md`). Every hunk
traces to a plan step: `store.py` to steps 1–3, `cli.py` to steps 4–6, `README.md` to step 10.
Two pieces of behaviour exist that no criterion names, both recorded in the plan rather than
introduced quietly: `naming_expenses` checks `shares_minor`'s keys as well as `paid_by` and
`shared_by` (plan assumption 2 — it can only ever refuse more), and `parse_position` strips
surrounding whitespace, which is what `parse_date` and `add_person` already do with their input.
Neither is unrequested scope.

`artifacts/impl-report.md` was read after the criteria were checked, and its four declared
deviations were confirmed against the code: the AC8 test class exists and pins only AC8(a)'s
literals, AC1/AC2's exact output lines and AC8(b)'s numbered sample; the empty-name refusal is
`'' is not in the group`; `delete_expense`'s message is `there is no expense <n>`; and AC7's
criterion does enumerate seven vectors plus two empty-store cases, so the report's correction of
the plan's "nine" is right.

### Not verified, and why

- **`lint-clean` checked nothing.** `commands.lint` is `null`. Nothing in this item's diff was
  checked for style, unused imports, or dead code by any tool — only by reading. ADR-0004 is the
  standing decision behind that, so this is a known and accepted gap rather than a new one.
- **AC8(c) and AC8(d) were verified by reading, not by a test**, which is what AC8 asks for —
  it is a documentation criterion "checked by reading the file". The test class covers (a) and
  (b) only. A future edit that removes the refusal sentence or the renumbering sentence from
  `README.md` would not be caught by the suite.
- **The refusal message strings are not pinned by any criterion.** AC3 requires only the name and
  the count; `Ben is named in 2 expense(s); delete those first` is the plan's choice. A change to
  that wording that kept the name and the count would pass AC3 and would not be caught.
- **Nothing was verified on any platform but this one**, and no dataset written by an older
  version of the tool was tested — no such dataset exists, since `store.VERSION` is unchanged and
  this item alters no stored record shape.
- **Concurrency was not tested** — two processes deleting at once. Nothing in the epic asks for
  it; the vision is one person at a terminal on one machine.

# Verification report — WI-0004

Verified-commit: 0a26e4ae8ee5fa216fe205e3e24332fc58f5efde

## Verdict

**Pass.** All ten acceptance criteria were checked by running commands against stores this
verification created, and all ten hold. Every criterion below was decided from its own wording
before `impl-report.md` was consulted, and no verdict rests on that report.

Two findings are recorded under `## Defects found`. Neither is a failure of this item's criteria
and neither belongs to another item, so neither is a send-back and neither is a bug item — but
one of them is an inaccurate claim in `impl-report.md`, and `review-close` should weigh it.

Every check was run through the delivered `./recall` executable with `RECALL_FILE` pointing at a
store under `/tmp/vfy4/` and `HOME` redirected there, so nothing touched a real card store.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | three `recall add`s, then `recall delete 2`, then `recall list` | `delete` → exit 0, `wc -l` of stdout = `1`, stdout `Deleted card 2\tder Hund\tthe dog`; `list` → exit 0, `1\tdie Katze\tthe cat` and `3\tdas Pferd\tthe horse` | exactly one line, the line names the card, and card 2 is absent from the later listing |
| AC2 | **pass** | `recall delete 2 < /dev/null` on a three-card store | exit 0; stdout `1` line, `Deleted card 2\tder Hund\tthe dog`; stderr `0` bytes (`wc -c`) | the line contains `2`, `der Hund` and `the dog`, checked by three separate `grep`s. Strengthened beyond the criterion's own wording: re-run as `timeout 5 ... recall delete 2 < <(sleep 30)` — a stdin that stays open for 30 seconds — and it still exited **0**, not 124. It does not merely tolerate a closed stdin; it never reads stdin at all |
| AC3 | **pass** | the store was parsed before and after AC1's deletion and cards 1 and 3 compared field by field | numbers before `[1, 2, 3]`, after `[1, 3]`; cards 1 and 3 equal on `number`, `question`, `answer`, `due`, `interval` — both printed in full and identical | nothing renumbered: card 3 is still card 3 |
| AC4 | **pass** | one card due today, `recall delete 1`, then `recall review < /dev/null` | `delete` exit 0; `review` → `Nothing is due today.`, exit 0 | |
| AC5 | **pass** | `recall delete 9` on a three-card store, with `md5sum` of the store taken before and after | exit **1**; stdout `0` bytes; stderr `recall delete: there is no card 9`; md5 `6fffae2e262d9995c29bdf5a1ac36616` before and after | non-zero ✓, names the number ✓, silent on stdout ✓, byte-identical ✓. See finding F2 — the *test* guarding this is weaker than the criterion |
| AC6 | **pass** | `recall delete 1` with `RECALL_FILE` at a path confirmed absent (`ls` → `No such file or directory`) | exit **1**; stderr `recall delete: there is no card 1`; `[ -e ... ]` afterwards → still absent | no file created |
| AC7 | **pass** | one card, `recall delete 1`, then `recall list`, then `recall add "der Hund" "the dog"` | `delete` exit 0; `list` → `No cards yet.`, exit 0; `add` → `Added card 1.`, exit 0; the store re-read as valid `"version": 3` JSON with one card | an emptied store is still a store the tool reads and writes |
| AC8 | **pass** | four runs on a three-card store — `delete` (no argument), `delete 1 2`, `delete two`, `delete 0` — each with `md5sum` before and after | all four exit **2**, all four print `usage: recall delete <card number>` on stderr, all four leave the store's md5 unchanged | checked as four separate runs, not one parametrised assertion. `ls -a` of the store directory afterwards showed no stray `.recall-*.tmp` |
| AC9 | **pass** | a store containing the literal `{ not json`, then `recall delete 1`, md5 before and after | exit **1**; stderr `recall: /tmp/vfy4/broken.json is not a readable card store: it is not JSON (Expecting property name enclosed in double quotes: line 1 column 3 (char 2))`; md5 unchanged; `cat` shows the file still reads `{ not json` | the path is named in the message, as the criterion requires |
| AC10 | **pass** | the `### recall delete <card number>` section was read out of `README.md`'s `## Commands`, and its worked example was then **executed verbatim** | the section carries a `###` heading naming the invocation, prose, and a fenced example — the same three parts `add`, `list` and `review` each have. Running its example produced `1\tdie Katze\tthe cat` / `2\tder Hunt\tthe dog`, then `Deleted card 2\tder Hunt\tthe dog`, then `1\tdie Katze\tthe cat` — byte-identical to what the README prints | the "what happens when the number names no card" half is the paragraph beginning **If the number names no card** — and its claims were checked against behaviour, not just read: "leaving the file exactly as it was" is AC5's md5 result, "Deleting from a pile you have not started yet does the same thing" is AC6's, and "Either way the exit code is 1" matches both. The neighbouring claim that "a deleted card never comes round in `recall review`" was also run and holds |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` run by this skill on the branch head → exit 0, `Ran 101 tests in 7.318s` / `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` run by this skill → exit 0 |
| `workspace-valid` | **pass** | `scripts/validate-workspace .` → exit 0, `checked 5 item(s), 11 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | the table above gives, for each of AC1–AC10, a command this skill ran and the output it produced. No cell cites `impl-report.md`, and no verdict was taken from it |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — every error, empty-input and boundary case in the criteria was triggered, plus three the criteria do not name |
| `tests-would-fail-without-the-change` (advisory) | **pass, with a qualification** | seven mutations were applied and reverted by this skill; six turned the intended criterion's test red. The seventh, M1, did not — see `## Test sensitivity check` and finding F2 |

## Negative and boundary cases exercised

Every one of these was *triggered*, not read about.

1. **A number naming no card in a populated store** (AC5) — `recall delete 9` on cards 1–3. Exit 1, stderr names `9`, stdout empty, md5 unchanged.
2. **A number naming no card in a store that does not exist** (AC6) — `recall delete 1` at an absent path. Exit 1, and the path was still absent afterwards.
3. **No argument at all** (AC8) — `recall delete`. Exit 2, usage on stderr, store unchanged.
4. **Two arguments** (AC8) — `recall delete 1 2`. Exit 2, usage on stderr, store unchanged.
5. **A non-numeric argument** (AC8) — `recall delete two`. Exit 2, usage on stderr, store unchanged.
6. **The zero boundary** (AC8) — `recall delete 0`. Exit 2, usage on stderr, store unchanged.
7. **A store that is not JSON** (AC9) — a file containing `{ not json`. Exit 1, the path named on stderr, the file's bytes and visible content unchanged.
8. **The emptying boundary** (AC7) — deleting the only card, then reading and writing the store again. Both succeeded.
9. **Beyond the criteria — a stdin that stays open.** `timeout 5 ... recall delete 2 < <(sleep 30)` exited 0, proving AC2's "never asks" rather than only that a closed stdin is survivable.
10. **Beyond the criteria — an unwritable store directory.** `chmod 500` on the store's directory, then `recall delete 1`: exit 1, stderr `recall: cannot write /tmp/vfy4/ro/cards.json: Permission denied`, store byte-identical, no stray temp file left behind. No acceptance criterion covers this; it is `impl-report.md`'s declared deviation 3, and it behaves as `add` and `review` already do rather than raising a traceback.
11. **Beyond the criteria — stray temp files.** `ls -a` of the store directory after every run above. The write protocol's `.recall-*.tmp` files are all gone; nothing was left behind by any failure path.

## Test sensitivity check

Seven mutations were applied to the branch head by this skill, the full suite run against each,
and the tree restored with `git checkout --` afterwards. The suite was confirmed green again at
the end. None of these mutations is in any commit.

| mutation | criteria it should break | tests that turned red | verdict |
|----------|--------------------------|-----------------------|---------|
| M1 — the `if card is None` branch replaced by `if False`, so a missing card falls through | AC5, AC6 | `test_deleting_with_no_store_file_at_all_creates_nothing` only | **AC6's test bites; AC5's does not** — see F2 |
| M2 — survivors renumbered `1..n` after a delete | AC1, AC3 | `test_deleting_a_card_removes_it_from_the_pile`, `test_the_surviving_cards_are_untouched_and_are_not_renumbered` | both bite |
| M3 — the argument check replaced by a bare `int()` | AC8 | `test_a_wrong_command_line_is_refused_and_changes_nothing` | bites (on the `0` case) |
| M4 — a prompt printed to stderr and the confirmation split over two stdout lines | AC2 | `test_deleting_acts_immediately_and_says_what_went`, `test_deleting_a_card_removes_it_from_the_pile` | bites, and both streams are pinned as AC2 asks |
| M5 — an unreadable store caught and treated as empty | AC9 | `test_a_store_that_cannot_be_read_is_refused_rather_than_repaired` | bites |
| M6 — the README's `delete` entry deleted | AC10 | `test_the_readme_documents_the_delete_command_beside_the_others`, `test_the_readme_says_what_delete_does_when_the_number_names_no_card` | bites |
| M7 — the card returned but never removed from the list | AC1, AC4, AC7 | five tests, including `test_a_deleted_card_is_never_offered_for_review_again` and `test_deleting_the_last_card_leaves_a_store_the_tool_still_reads` | bites broadly |

## Defects found

Neither finding is a failure of this item's acceptance criteria — all ten pass against the
delivered code, checked directly — and neither is behaviour delivered by another item. So there
is no send-back and no bug item. Both are recorded here for `review-close`.

### F1 — `impl-report.md` overstates what its mutation runs demonstrated

`impl-report.md`'s `## Gates` row for `every-criterion-has-a-test` states that the mutation runs
confirmed "the AC1, AC3, AC5, AC8 and AC10 tests failing when the behaviour is removed", and its
`## Acceptance criteria evidence` section attributes its mutation A — "saving on the not-found
path" — to AC5.

That attribution is wrong, and this skill established it by re-running the report's own mutation:

```
$ # impl-report's mutation A: save(path, document) added before the not-found return
$ python3 -m unittest discover -s tests -t .
FAIL: test_deleting_with_no_store_file_at_all_creates_nothing
Ran 101 tests in 7.366s
FAILED (failures=1)
```

The single test that fails is **AC6's**, not AC5's. No mutation run by either skill has made
AC5's test fail. AC5 itself passes — the delivered code does exactly what the criterion says, as
the criteria table records — so the defect is in the report's evidence claim, not in the code.

### F2 — AC5's test cannot distinguish a correct implementation from a crashing one

This is why F1's claim could be made without anyone noticing, and it is the more useful of the
two findings. Under M1 — the not-found branch removed entirely — `test_a_number_that_names_no_card_is_refused_and_changes_nothing`
still passes, against an implementation that raises. Reproduced directly:

```
$ RECALL_FILE=/tmp/vfy4/m1.json ./recall delete 9    # with M1 applied
exit=1
stdout empty: yes
store byte-identical despite the spurious save: yes
--- stderr under M1:
Traceback (most recent call last):
  ...
  File "/home/msi/agile-skills-throwaway/recall/recall.py", line 402, in cmd_delete
    print(f"Deleted card {card['number']}\t{card['question']}\t{card['answer']}")
TypeError: 'NoneType' object is not subscriptable
```

Each of the test's four assertions survives for its own accidental reason:

- **exit non-zero** — an uncaught exception is also non-zero.
- **stdout empty** — the crash happens before the confirmation line is printed.
- **the store byte-identical** — the spurious `save` rewrites a document that was never
  modified, and `save` is deterministic, so the bytes match. A byte comparison cannot detect an
  idempotent write.
- **`assertIn("9", stderr)`** — satisfied by the traceback's *line numbers* (`line 489`,
  `line 402`), not by any message naming card 9.

The criterion is sound and the code satisfies it; the test is what is weak. The narrow fix is to
assert the message rather than a substring of it — that stderr contains `there is no card 9`, or
at least that it does not contain `Traceback`.

## Not verified, and why

- **That deleting from the middle of a large pile leaves the rest untouched.** AC3 is worded
  against the three-card store AC1 uses, and that is what was checked. `delete_card` pops one
  element by index, so position should be irrelevant, but that is an argument from the code
  rather than an observation — the same gap the plan declared under `## Risks` and
  `impl-report.md` repeated under `## What I did not do`. Nothing this verification ran
  contradicts it; nothing confirms it either.
- **Behaviour on argument shapes no criterion names** — `01`, `+1`, ` 1`, `1.0`, and digits from
  other scripts. `impl-report.md` declares these as refused with exit 2, and the code reads that
  way, but AC8 names only `two` and `0` and this verification exercised only what AC8 names. They
  are the plan's declared, reversible assumption; they are not verified behaviour.
- **Concurrent invocations**, an interrupted write, and a store on a filesystem that fails
  mid-write. `ADR-0004`'s write protocol is inherited unchanged from earlier items and no
  criterion of this item covers it.
- **Nothing was skipped for want of an environment.** Both project commands ran, every criterion
  was reachable, and no gate was recorded as skipped.

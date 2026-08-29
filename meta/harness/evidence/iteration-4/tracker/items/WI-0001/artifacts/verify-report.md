# Verification report — WI-0001

Verified-commit: f23fe67548d96862adf96f2a406b1cb1dd2cbded

## Verdict

**Pass.** All nine acceptance criteria were checked by running commands against the head of
`wi/WI-0001` and reading the actual output; all nine pass and are ticked in `item.md`. No
criterion was ambiguous, no question was filed, and no defect was found in behaviour delivered
by another item. One side effect of this verification's own mutation testing is declared under
`## Not verified, and why` — it is a finding about how I checked, not about the code.

Every command below was run with the repository root on `PATH`, so the invocations are the ones
the criteria are written in, and with `RECALL_FILE` pointing into a fresh `mktemp -d` unless the
criterion was specifically about the default path.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | `recall add "die Katze" "the cat"`, then `"der Hund" "the dog"`, then `"das Pferd" "the horse"` | `Added card 1.` / `Added card 2.` / `Added card 3.`, each `exit=0` | One line each, each containing the number identifying the card just added; numbers start at 1 and increase by 1 |
| AC2 | **pass** | `recall list` in a separate process after those adds, piped into a comparison of the printed sides with the arguments | `1\tdie Katze\tthe cat` … and `number='1' question_identical=True answer_identical=True` | Byte-identical on both sides, against the number AC1 reported |
| AC3 | **pass** | `recall add "same" "same"` twice, then `recall list` | `Added card 1.`, `Added card 2.`, then `1\tsame\tsame` and `2\tsame\tsame` | Two separate cards, different numbers, both listed |
| AC4 | **pass** | `recall add "" "the cat"`; `recall add "die Katze" ""`; `recall list` after each | `recall add: the question side is empty` `exit=2`; `recall add: the answer side is empty` `exit=2`; `No cards yet.` `exit=0` after each; no store file was created | Each message names the side that is empty. Also checked `recall add "" ""` → the question side is reported, `exit=2` |
| AC5 | **pass** | `RECALL_FILE=$T/cards.json recall add "a" "b"`; `cat $T/cards.json`; `file $T/cards.json`; `env -u RECALL_FILE HOME=$T/home recall add "d" "e"`; `grep -n -e '~/.recall.json' -e 'RECALL_FILE' README.md` | the card is in `$T/cards.json` as pretty-printed JSON; `file` reports `JSON text data`; with `RECALL_FILE` unset the card lands in `$T/home/.recall.json`; `README.md:55` names `~/.recall.json` and `:56` names `RECALL_FILE` | Also checked the "and non-empty" half: `RECALL_FILE="" HOME=$T/home recall add "f" "g"` fell back to the default and printed `Added card 2.` |
| AC6 | **pass** | `recall add --deck german "die Katze" "the cat"`; `recall list`; then three cards added, their order **reversed in the file** by hand, and `recall list` again | `usage: recall add <question side> <answer side>` `exit=2` and `No cards yet.` afterwards; with the file holding `[3, 2, 1]`, the listing is `1\ta\t1`, `2\tb\t2`, `3\tc\t3` | The deck option is rejected and stores nothing; the ascending order is produced by the tool, not by the file's order |
| AC7 | **pass** | `recall add "Grüße" "greetings"`; `recall add "日本語" "Japanese"`; `recall list` compared with the inputs; `cat` of the store | `1\tGrüße\tgreetings`, `2\t日本語\tJapanese`, both comparisons `True`; the store file contains `Grüße` and `日本語` as themselves | Checked a second, non-Latin script as well as the accented case the criterion names |
| AC8 | **pass** | `recall list` with no store file, and again with a file holding `{"version": 1, "cards": []}`, stdout and stderr captured separately | both: `exit=0`, `stdout lines=1`, `content=[No cards yet.]`, `stderr=[]` | A single plain line, nothing else, exit 0, in both readings of "no cards stored" |
| AC9 | **pass** | `recall add`; `recall add "die Katze"`; `recall add "die Katze" "the cat" "extra"`, each with stdout and stderr captured, then `recall list` and a check for the store file | each `exit=2`, `stdout=[]`, `stderr=[usage: recall add <question side> <answer side>]`; `No cards yet.` afterwards; `store exists: no` | The usage line is on stderr and names both arguments it expects; nothing is stored in any of the three cases |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` at the branch head → `Ran 21 tests in 1.503s`, `OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → `checked 4 item(s), 7 document(s)`, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the table above; every cell in `command run` is a command this execution ran, and every `actual output` cell is what it printed. The implementation report was read after the criteria and is not cited as evidence for any of them |
| `negative-cases-exercised` | **pass** | see the section below — every error, empty-input and boundary case named by a criterion was triggered, not read about |
| `tests-would-fail-without-the-change` (advisory) | **pass** | nine separate mutations, one per criterion; see `## Test sensitivity check` |

## Negative and boundary cases exercised

- Empty question side, empty answer side, and **both** sides empty (AC4). The last is not in the
  criterion; it resolves which side gets reported when either could be — the question side.
- `recall add` with zero, one and three positional arguments (AC9), each checked for exit code,
  empty stdout, the usage line on stderr, and that nothing was stored.
- A deck-style option, `--deck german`, in front of two valid sides (AC6).
- An empty listing in both of its readings: no store file at all, and a store file holding zero
  cards (AC8).
- `RECALL_FILE` set to the empty string — the "and non-empty" half of AC5, which the criterion
  states but does not give an observation for.
- A card side beginning with a dash, `recall add "-x" "minus x"` → `Added card 1.`, listed as
  `1\t-x\tminus x`. Positional-only arguments mean it is text, not an option [src: ADR-0005].
- A store file containing `not json`: `recall add` and `recall list` both exit 1 with
  `recall: <path> is not a readable card store: it is not JSON (Expecting value: line 1 column 1
  (char 0))`, and the file's contents were **unchanged** afterwards [src: ADR-0004].
- A store path whose parent directory does not exist: exit 1,
  `recall: <path>: No such file or directory` after `recall: cannot write`, and the directory was
  not created [src: ADR-0004].
- No command at all, and an unknown command: both exit 2 with `usage: recall <add|list>` on
  stderr. No criterion covers either; recorded here because they are user-visible.

## Test sensitivity check

Nine mutations, one per criterion, each applied on its own to a **throwaway copy of the tree
under `/tmp`** and the whole suite run against it. Every mutation was rejected by at least one
test, and the tree under verification was never modified.

| AC | behaviour removed | test that failed |
|----|-------------------|------------------|
| AC1 | the confirmation line no longer carries the number | `test_add_exits_zero_and_prints_the_card_number`, `test_card_numbers_start_at_one_and_increment` |
| AC2 | the listing prints only the number, not the sides | `test_a_card_added_in_one_process_is_listed_by_another` |
| AC3 | `add_card` reuses an existing card with identical text | `test_identical_text_twice_gives_two_cards_with_different_numbers` |
| AC4 | the empty-question check is disabled | `test_empty_question_side_is_rejected_by_name` |
| AC5 | `store_path` ignores `RECALL_FILE` | `test_recall_file_decides_the_path`, and 16 others |
| AC6 | the listing is no longer sorted by card number | `test_listing_is_in_ascending_card_number_order` |
| AC7 | the question side is stripped to ASCII on the way out | `test_non_ascii_text_survives_a_round_trip` |
| AC8 | the empty listing prints nothing | `test_a_store_with_no_cards_prints_one_line_and_exits_zero`, `test_no_store_file_at_all_prints_one_line_and_exits_zero` |
| AC9 | the argument-count check is relaxed from `!= 2` to `< 2` | `test_wrong_argument_counts_are_rejected_with_a_usage_line` |

## Defects found

None — no criterion of this item failed, and nothing was found in behaviour delivered by another
item. No bug item was filed.

Two observations, recorded because they are behaviour no acceptance criterion covers, and both
of which the implementation report already declares:

1. `recall list` with an argument exits 2 with `usage: recall list`. No criterion covers it. It
   is consistent with AC6's flat pool and with ADR-0005's positional-only rule, and it is
   declared in `impl-report.md` as deviation 2, so it is not undeclared scope. Nothing here
   contradicts a criterion, so it is not a send-back.
2. No command, and an unknown command, both exit 2 with `usage: recall <add|list>`. Unavoidable
   in a command dispatcher and not covered by any criterion.

Both are noted for `review-close` rather than raised as defects.

## Not verified, and why

- **Multi-line card text.** Explicitly out of scope for this item, so there is no criterion to
  check and I did not invent one. A newline inside an argument would break the one-line-per-card
  listing; that is declared in the implementation report and is not a defect against WI-0001.
- **The durability claim behind the write protocol.** ADR-0004 says a crash part-way through a
  write leaves the old document or the new one. I checked the mechanism's observable
  consequences — the store is only ever replaced whole, an unwritable path fails without
  creating anything, and an unreadable file is refused rather than overwritten — but I did not
  kill the process mid-write to prove atomicity. No acceptance criterion states it; it is
  ADR-0004's claim, not WI-0001's.
- **Behaviour on a store file that is valid JSON in some other shape.** `load` rejects it, and I
  exercised the not-JSON case; I did not enumerate the malformed-schema cases, because no
  criterion covers them.
- **`~` resolution when `HOME` is unset.** AC5's default path was checked with `HOME` redirected
  to a temporary directory. The no-`HOME` case is not in any criterion and was not exercised.
- **A side effect of this verification, declared in full.** The AC5 mutation — making
  `store_path` ignore `RECALL_FILE` — meant the mutant's subprocesses resolved the store to the
  checker's real `HOME` rather than to the temporary store, and the suite's own fixtures were
  written to `~/.recall.json` outside this project. The file did not exist beforehand and every
  one of its 18 cards was a fixture from this suite, so nothing was overwritten or lost; it was
  removed. The mutation was rejected by 17 tests, which is the result the check wanted, but a
  test suite that redirects `RECALL_FILE` and not `HOME` cannot contain a mutation of the path
  resolution itself. That is a limitation of `tests/support.py`, not of the delivered tool: no
  unmutated code writes outside the store the environment names, which every other case above
  confirms.

# Verification report — WI-0002

Verified-commit: e3974907cdf2cae8269b14fa0099c0f4eadf9ea4

Branch `wi/WI-0002`, working tree clean at the time of every command below.

## Verdict

**Pass.** All ten acceptance criteria are met, each demonstrated by a command run here against
the delivered executable rather than by the test suite or the implementation report. The item
goes to `in-review`.

Two findings are recorded in `## Defects found`. Neither is a criterion failure and neither is
filed as a bug item; both are handed to `review-close`, with the reason each could not be filed
stated there.

**How this verification was derived.** Each criterion's check was written from the criterion's
own text before the implementation was looked at, and run as a shell command against `recall`
in a scratch store of this skill's own — `RECALL_FILE=<tmp>/cards.json`, which is what
[src: WI-0001 AC5] exists to make possible. The test suite was run as a gate, but no criterion's
evidence below is "a test passes": every row quotes output this skill produced.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | two cards added, then `printf '\ny\n\nn\n' \| recall review` | `die Katze` / `[Enter] to see the answer, q to stop` / `the cat` / `[y] right, [n] wrong, q to stop` / `der Hund` / `[Enter] …` / `the dog` / `[y] …` / `Reviewed 2, right 1.`, exit 0 | the four strings appear in the order the criterion names. That the reveal is *caused by* the Enter was checked separately, because the ordering alone does not show it: `printf 'q\n'` over the same two cards printed `die Katze` and the prompt and nothing else — no `the cat`, no `der Hund` — and `printf '\ny\n'` printed `der Hund` and its prompt but never `the dog` |
| AC2 | **pass** | the AC1 session, then `cat <tmp>/cards.json` in a new process | card 1 `"result": "right"`, card 2 `"result": "wrong"` | recorded after the process ended, and the two records differ. `grep` on `README.md` line 123: `` \| `result` \| how the last review went: `"right"` if you answered `y`, `"wrong"` if you answered `n`, and `null` for a card you have never reviewed \| `` — the field and both values are named |
| AC3 | **pass** | `recall review </dev/null` against (a) no store file, (b) a store holding `{"version": 2, "cards": []}`, (c) the store immediately after the AC1 session | `Nothing is due today.`, exit 0, in all three | one line, no card presented. Counted mechanically on (c): stdout is 1 line and stderr is 0 bytes |
| AC4 | **pass** | the AC1 session, then `recall review </dev/null` against the same store | `Nothing is due today.` | neither `die Katze` nor `der Hund` appears. The store shows why: both cards' `due` moved from `2026-08-29` to `2026-08-30` |
| AC5 | **pass** | three cards; `printf '\ny\nq\n' \| recall review`, then `printf '\ny\n\ny\n\ny\n' \| recall review`; and from the copied starting state `printf '\ny\n\nq\n' \| recall review`, then `printf 'q\n' \| recall review` | first: `das Pferd` never appears, store is `[(1,'right','2026-08-30'), (2,None,'2026-08-29'), (3,None,'2026-08-29')]`; the following session presents `der Hund` and `das Pferd` and not `die Katze`. second: `the dog` *was* revealed, `das Pferd` never appears, store is identical to the first — card 2 still `None` and still dated today; the following run presents `der Hund` | both moments checked, from the same starting state, restored from a copy in between. In both, the recorded result is kept and every unreached card is still due |
| AC6 | **pass** | `printf '\ny\n\nn\n' \| recall review \| tail -1` and `printf '\ny\nq\n' \| recall review \| tail -1` | `Reviewed 2, right 1.` and `Reviewed 1, right 1.` | the last line on stdout in both endings; contains `2` and `1`, and `1` and `1`. `grep -c Reviewed` on the `q` session is `1`, so it is a single line. AC3's empty session prints no summary, which is not a conflict: AC3 requires *a single plain line* there, and the plan's output contract row for "nothing is due" says the same |
| AC7 | **pass** | `recall review --deck german </dev/null >out 2>err`, then `printf '\ny\n\ny\n\ny\n' \| recall review` | exit **2**; stdout **0 bytes**; stderr `usage: recall review`; the store's three results all still `None`. The following session then printed all six sides and `Reviewed 3, right 3.` | non-zero, no card presented, nothing recorded, and every due card covered by one uninterrupted session from the one flat pool |
| AC8 | **pass** | three cards, `due` set by hand in the store file to `2026-08-27` (card 3) and `2026-08-28` (cards 1 and 2), the file copied aside, then `printf '\ny\n\ny\n\ny\n' \| recall review` twice with the copy restored between | run 1: `das Pferd` / `the horse` / `die Katze` / `the cat` / `der Hund` / `the dog`. run 2, over the restored state: identical | oldest-due first, ties broken by ascending number (cards 1 and 2 share a date and come out 1 then 2), and the same order twice. The hand edit went through `due`, which `README.md` documents |
| AC9 | **pass** | every command in this table is a pipe with nobody at the keyboard. For the ending case: `printf '\ny\n' \| recall review` over two due cards | `die Katze` / prompt / `the cat` / prompt / `der Hund` / prompt / `Reviewed 1, right 1.`, exit 0; store `[(1,'right','2026-08-30'), (2,None,'2026-08-29')]`; a following `printf 'q\n'` session presents `der Hund` | card 1's result recorded, card 2 left due, the AC6 line printed, exit 0 — identical to what `q` does at the same point. Also checked with input that is empty from the start (`printf ''`): `Reviewed 0, right 0.`, exit 0 |
| AC10 | **pass** | one due card, `printf 'x\n\nz\ny\n' \| recall review` | `die Katze` / `[Enter] …` / `[Enter] …` / `the cat` / `[y] …` / `[y] …` / `Reviewed 1, right 1.`, exit 0; store `[(1, 'right')]` | each prompt printed **twice** — the stray line was ignored and the prompt repeated — no result recorded for it, and the session did not end. Pushed further with `printf 'x\nY\n y \n\n Y\nn\n'`: `Y` and ` y ` are also ignored at both moments (the reveal prompt appears four times), and the card is finally recorded `wrong` |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` on `e397490` → `Ran 55 tests in 3.812s` / `OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '[.]claude' .` → exit 0, no output |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 4 item(s), 8 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | **pass** | the table above gives, for each of AC1–AC10, a command this skill ran and the output it produced. No row's evidence is a test name or a line of `impl-report.md` |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — nine conditions triggered, not read about |
| `tests-would-fail-without-the-change` (advisory) | **pass** | see `## Test sensitivity check` — twelve mutants, every one detected |

## Negative and boundary cases exercised

Each was produced here, and the output quoted is real.

| # | condition | what happened |
|---|-----------|---------------|
| 1 | `recall review` with no store file at all | `Nothing is due today.`, exit 0. No file created |
| 2 | a store holding an empty `cards` array | same line, exit 0 |
| 3 | every due card already reviewed today | same line, exit 0, stdout exactly one line and stderr empty |
| 4 | `recall review --deck german` | exit 2, stdout 0 bytes, `usage: recall review` on stderr, store unchanged |
| 5 | input that ends mid-session (`printf '\ny\n'`, two cards) | ends like `q`: card 1 recorded, card 2 left due, summary printed, exit 0 |
| 6 | input that is empty from the start (`printf ''`) | `Reviewed 0, right 0.`, exit 0, nothing recorded |
| 7 | a **version-1** store written by WI-0001, with no `due` and no `result` on its card | the card is due and is reviewed: `alt` / `old` / `Reviewed 1, right 1.`, exit 0 — and the file is upgraded in place to `"version": 2` with `due` and `result` written. This is the cross-item boundary that matters most and it holds |
| 8 | a store claiming `"version": 3` | `recall: …/v3.json is not a readable card store: its version is 3, and this recall reads versions 1, 2`, exit 1. `md5sum` before and after are **identical** — the file was not touched |
| 9 | a card carrying `"result": "maybe"`, and a store that is not JSON | `… card 1 has a 'result' that is not 'right', 'wrong' or null` and `… it is not JSON (Expecting value: line 1 column 1 (char 0))`, both exit 1, both files left as they were |

## Test sensitivity check

The suite was re-run against **twelve** mutants of `recall.py`, one behaviour removed at a time,
each restored immediately afterwards. `git status` was clean before and after the sweep, and the
harness confirmed the file was byte-identical to the original after each run.

| behaviour removed | detected by |
|-------------------|-------------|
| the answer side is printed without waiting for the Enter (AC1) | 1 test — `test_ac1_an_answer_side_is_not_shown_before_its_enter_is_read` |
| the result is never saved to disk (AC2) | 9 tests |
| nothing is printed when no card is due (AC3) | 2 tests — both AC3 cases |
| a reviewed card's `due` is not moved past today (AC4) | 8 tests |
| `q` at the answer side records a wrong answer instead of ending (AC5) | 1 test — `test_ac5_q_at_the_answer_side_records_nothing_for_that_card` |
| the summary line is not printed (AC6) | 4 tests |
| `review` accepts and ignores extra arguments (AC7) | 1 test — `test_ac7_review_takes_no_deck_tag_or_filter_argument` |
| due cards are not ordered (AC8) | 3 tests |
| a wrong answer records the same value as a right one (AC2) | 3 tests |
| an unrecognised line ends the session (AC10) | 1 test — `test_ac10_a_line_outside_the_key_map_is_ignored_and_the_prompt_repeats` |
| end of input is treated as a blank line (AC9) | the suite **hung** — the mutant loops forever reprinting the grade prompt. Detected, but as a hang rather than a failure, which is why the next row exists |
| end of input is treated as the key that was expected (AC9) | 1 test — `test_ac9_input_that_ends_mid_session_ends_it_exactly_as_q_does`. This mutant terminates, so it establishes the AC9 distinction with a clean failure rather than a timeout |

Every criterion has at least one mutant that a named test catches. The first AC9 mutant is
recorded as a hang rather than quietly counted as a pass: a suite with no per-test timeout does
not distinguish "hangs forever" from "still running", and anyone repeating this sweep should
expect to kill it.

## Defects found

**None that fail this item's acceptance criteria, so there is no send-back and no bug item.**
Two findings are recorded for `review-close` to rule on. Neither could be filed as a bug: RB3
requires `## Expected behaviour` to cite an acceptance criterion, document or ADR that the
behaviour contradicts, and neither of these contradicts one.

**F1 — a `due` that is a string but not a date silently removes a card from every review.**

1. `printf '{"version": 2, "cards": [{"number": 1, "question": "a", "answer": "b", "due": "tomorrow", "result": null}]}\n' > cards.json`
2. `RECALL_FILE=cards.json recall review </dev/null` → `Nothing is due today.`, exit 0
3. `RECALL_FILE=cards.json recall list` → `1	a	b`, exit 0

`load` accepts any string as `due`; `due_cards` compares it lexically, and `"tomorrow"` sorts
above every `YYYY-MM-DD` date, so the card is never due and never will be. The card is still
listed, so it does not look lost. This is reachable by a path the criteria endorse rather than a
hypothetical: AC8 requires the checker to hand-edit `due` in the store file, and WI-0001 AC5
exists so that a person opens and edits this file. Why it is not a bug item: ADR-0006 states the
format (`"a date as YYYY-MM-DD"`) but nothing requires `load` to enforce it, and no criterion of
this item or of WI-0001 covers a malformed date — so RB3 has nothing to cite. Why it is not a
send-back: no acceptance criterion of WI-0002 says this should behave differently. Worth
`review-close`'s attention because WI-0003 will write to this same field and inherits the gap.

**F2 — `cmd_review`'s `input_stream` parameter is unreachable and therefore unverified.**

`cmd_review(arguments, input_stream=None)` widens the signature the plan's interface table fixed
(`cmd_review(arguments)`). `main` calls it with one argument and every test drives the real
executable through a real pipe, so `input_stream` is never passed a value anywhere in the
delivered tree — checked with `grep -rn "input_stream" .` outside the definition itself. The
developer declared it as deviation 4 rather than leaving it to be found, which is the right
handling; it is recorded here because "declared" and "verified" are different things, and this
is the one piece of the diff that no criterion and no plan step accounts for. It is one keyword
argument with a default and deleting it is a one-line change.

## Not verified, and why

- **Behaviour at a real terminal.** Every check here, and every test, drives the session through
  a pipe. That is what the item asks for — `## Out of scope` excludes anything requiring a
  terminal, and AC9 requires pipe-drivability — but it means nobody has confirmed the tool is
  pleasant, or even usable, with a person at a keyboard. The plan's `## Risks` names this and
  asks for prompts on their own lines, which the implementation does; that mitigation was read,
  not exercised.
- **The interval ladder.** A card answered right returns tomorrow, exactly as a wrong one does.
  This is ADR-0006's declared placeholder and WI-0003's job, and no criterion of this item
  constrains it, so it was not checked beyond confirming AC4 — that the card does not return
  *today*.
- **Anything after local midnight.** `today()` reads the real clock. A session spanning midnight,
  or a store carried between timezones, was not produced: both are recorded in ADR-0006 and the
  plan's `## Risks` as accepted, and neither has a criterion.
- **Concurrency and interrupted writes.** ADR-0004's write-by-rename protocol was inherited
  unchanged from WI-0001 and re-verified only through its visible effects (case 8 above, where a
  refused store is byte-identical afterwards). No kill-mid-write test was performed; the same gap
  was accepted at WI-0001.
- **`recall add` and `recall list` beyond what this item changed.** Their WI-0001 criteria were
  verified when that item closed. Here they were exercised only as setup, and as the two commands
  that must keep working across the version bump — cases 7, 8 and 9 above cover that.

# Implementation report — WI-0001

## What was built

droll, in five files under `droll/` and five under `tests/`, on branch `wi/WI-0001` in three code
commits (the branch also carries commits that write only the record). The plan's seven steps were executed in order and none was skipped.

- `droll/expression.py` — `ExpressionError` (carrying `.text`, the offending input),
  `DiceExpression` (`count`, `sides`, `modifier`, `text`) and `parse`. One compiled pattern,
  `[0-9]*[dD][0-9]+([+-][0-9]+)?`, matched against the input with surrounding whitespace removed,
  plus the positive-integer check that rejects `0d6` and `3d0` after they match the shape.
- `droll/roller.py` — `RollResult` with a `total` property, and `roll(expression, randint=…)`,
  one call to `randint(1, sides)` per die.
- `droll/formatting.py` — `format_roll`, producing `3d6+2 -> 13   [4, 5, 2] +2`, and
  `format_rejection`, producing `cannot interpret '3x6': expected one dice term with an optional
  modifier, like 3d6+2 or d20`.
- `droll/cli.py` — `PROMPT`, `QUIT_WORDS` and `run(stdin, stdout, randint=…)`, dispatching each
  line exactly as the plan's table specifies, with every write flushed.
- `droll/__main__.py` — `sys.exit(run(sys.stdin, sys.stdout))`, so `python3 -m droll` starts a
  session.
- `tests/support.py`, `tests/test_expression.py`, `tests/test_roller.py`,
  `tests/test_formatting.py`, `tests/test_cli.py` — 27 tests, all passing.

## Acceptance criteria evidence

Deciding whether these criteria are **met** is `verify`'s. What is below is the evidence each one
has, which is what this skill owes.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `run` writes `PROMPT` and flushes before reading; a parsed line produces one roll line; the loop then writes the prompt again | `tests.test_cli.StartingAndRolling.test_a_prompt_is_written_before_anything_is_read` asserts the whole transcript equals `"> 3d6+2 -> 13   [4, 5, 2] +2\n> \n"`. By hand: `printf '3d6+2\n' \| python3 -m droll` → `> 3d6+2 -> 13   [4, 4, 3] +2` then `> `, exit 0 |
| AC2 | `format_roll` writes the faces in a bracketed list and the modifier with its sign, beside the total | `tests.test_formatting.RollLine.test_three_dice_and_a_positive_modifier` asserts the exact string `3d6+2 -> 13   [4, 5, 2] +2`; 4 + 5 + 2 + 2 = 13, so the shown faces and the shown modifier re-add to the shown total |
| AC3 | `roll` calls `randint(1, sides)` once per die, with the standard library's generator by default | `tests.test_cli.TheDiceAreActuallyRolled.test_two_hundred_d6_rolls_span_at_least_three_faces_and_none_outside_one_to_six` drives 200 `1d6` lines through a whole session with the real generator, scrapes the faces back out of what was printed, and asserts 200 faces, at least 3 distinct, and none outside 1-6. By hand: `yes 1d6 \| head -200 \| python3 -m droll \| grep -o '\[[0-9]*\]' \| sort \| uniq -c` → `30 [1]`, `36 [2]`, `33 [3]`, `48 [4]`, `23 [5]`, `30 [6]` — six distinct faces, none outside the range |
| AC4 | `parse` raises `ExpressionError` for anything outside the pattern or with a non-positive count or die size; `run` writes `format_rejection` and takes the next turn | `tests.test_expression.RejectedExpressions.test_each_named_input_is_rejected` covers all eight named inputs as subtests and asserts `.text` is the input; `tests.test_cli.Rejection.test_each_named_input_is_rejected_and_the_prompt_returns` drives all eight through a session and asserts each line names the text, that no line contains `->`, and that the prompt was written nine times for eight inputs. By hand: `printf '3x6\nd\n3d\n0d6\n3d0\n1d8+1d6\n4d6kh3\nhello\n' \| python3 -m droll` → eight `cannot interpret …` lines and no total |
| AC5 | the pattern is ADR-0001's grammar, with an omitted count meaning one die | `tests.test_expression.AcceptedExpressions.test_each_named_expression_parses_to_its_three_numbers` asserts `d20`→(1,20,0), `2d10`→(2,10,0), `3d6+2`→(3,6,+2), `4d8-2`→(4,8,-2), and `…test_an_omitted_count_means_one_die`. By hand: `printf 'd20\n2d10\n3d6+2\n4d8-2\n' \| python3 -m droll` → four roll lines, none rejected |
| AC6 | `run` loops until end of input or a quit word | `tests.test_cli.StartingAndRolling.test_two_expressions_are_rolled_in_one_run` asserts one `run` call driven with `"d20\n3d6+2\n"` produced `["d20 -> 17   [17]", "3d6+2 -> 13   [4, 5, 2] +2"]` — two lines from one call, so nothing was restarted. By hand: `printf 'd20\n3d6+2\n' \| python3 -m droll` |
| AC7 | `format_roll` renders the bracketed face list unconditionally, so one die prints in the same field as three | `tests.test_formatting.RollLine.test_a_bare_d20_prints_in_the_same_shape` asserts the exact string `d20 -> 17   [17]`: the face is shown, and 17 equals the total |
| AC8 | the modifier field is written only when the modifier is non-zero | `tests.test_formatting.RollLine.test_two_dice_and_no_modifier` asserts `2d10 -> 12   [8, 4]` (two faces, no modifier field, 8+4=12); `…test_four_dice_and_a_negative_modifier` asserts `4d8-2 -> 14   [5, 3, 6, 2] -2` (four faces, `-2`, 5+3+6+2-2=14) |
| AC9 | `parse` accepts `[dD]`, strips surrounding whitespace, and rebuilds `text` with the `d` lower-cased — so equal spellings produce equal values and print identically | `tests.test_expression.CaseAndWhitespace` asserts `parse("D20") == parse("d20")`, `parse("3D6+2") == parse("3d6+2")`, `parse("  3d6+2  ") == parse("3d6+2")`, and that `parse("3 d 6")` raises; `tests.test_formatting.RollLine.test_a_capital_d_renders_identically` asserts the rendered lines are equal. By hand: `printf 'D20\n3D6+2\n  3d6+2  \n3 d 6\n' \| python3 -m droll` → `d20 -> …`, `3d6+2 -> …`, `3d6+2 -> …`, then `cannot interpret '3 d 6': …` |
| AC10 | `run` returns 0 on a quit word and on end of input; `__main__` passes that to `sys.exit` | `tests.test_cli.EndingTheSession.test_quit_exit_and_end_of_input_all_end_it_with_status_zero` covers `"quit\n"`, `"exit\n"`, `"QUIT\n"` and `""` as subtests, asserting status 0 and no `->` in the output; `…test_quitting_writes_no_further_line` asserts the whole output is just the prompt. By hand: `printf 'quit\n' \| python3 -m droll; echo $?` → 0, and likewise for `exit` and for empty input |
| AC11 | the rejection branch writes and continues rather than returning | `tests.test_cli.Rejection.test_a_roll_after_a_rejection_is_a_normal_roll` asserts the first line names `'3x6'`, the second is exactly `3d6+2 -> 13   [4, 5, 2] +2`, and the status is 0. By hand: `printf '3x6\n3d6+2\n' \| python3 -m droll` |

**Every one of these tests can fail.** Three mutations were applied to the branch and the suite was
run against each, then reverted: dropping the bracketed face list from `format_roll` → 9 failures;
removing the positive-integer check from `parse` → 2 failures and 1 error; removing the quit-word
branch from `run` → 3 failures and 1 error. The suite is green again at the branch head
[src: run: python3 -m unittest discover -s tests -t . → exit 0, Ran 27 tests, OK].

## Documents

| document | entry it closes | claim kind | what I checked, and against what | new version |
|----------|-----------------|------------|----------------------------------|-------------|
| `docs/product/vision.md` | `## Engagement state`, *"Three questions are open with them, all filed at intake"* | engagement-state | Nothing. Disposed `owned-by-ending`; `review-close` restates it at the ending. No edit was made to this file on this branch | — |
| `docs/product/vision.md` | `## Engagement state`, *"Two work items exist, both at `draft`…"* | engagement-state | Nothing, same reason | — |
| `docs/product/vision.md` | `## What it deliberately is not`, *"the elicitation question on the epic is the place where any of them can be contradicted"* | engagement-state | Nothing, same reason. It is the row that exists so the ending finds a sentence sitting outside the delimited section | — |
| `docs/architecture/overview.md` | `## Components`, the five module paths and what each holds; `## Conventions`, *"Started as a module: `python3 -m droll`"* | cited-fact | Reopened against the tree. `ls droll/*.py` → `cli.py`, `expression.py`, `formatting.py`, `__init__.py`, `__main__.py`, `roller.py`: all five named paths exist and each holds what its row says. The entry point works [src: run: printf '3d6+2\n' \| python3 -m droll → exit 0, one prompt and one roll line]. **`verified-still-true`** | unchanged |
| `docs/architecture/adr/ADR-0002…` | `## Consequences`, *"`plan` created both as empty files"* about `droll/__init__.py` and `tests/__init__.py` | cited-fact | Reopened against the tree. Both files are still zero bytes [src: run: wc -c droll/__init__.py tests/__init__.py → 0 and 0]. The test helpers went into `tests/support.py`, a new module, precisely so that neither package marker would acquire behaviour. **`verified-still-true`** | unchanged |
| `docs/architecture/overview.md` | `## Shape`, *"Only the loop touches the outside world — the streams it was handed, and the random number generator"* — **a row `implement` added** | quantified | Repaired. See the enumeration below. **`to-update`** | 1 → 2 |
| `docs/architecture/overview.md` | `## Components`, *"`cli` knows about streams and not about the grammar"* — **a row `implement` added** | cited-fact | Repaired. `droll/cli.py:7` reads `from droll.expression import ExpressionError, parse`, so `cli` does know about the grammar's interface; what is true is that the grammar's own definition is not restated outside `expression`. The replacement says that and cites `droll/expression.py`. **`to-update`** | 1 → 2 |
| `docs/architecture/adr/ADR-0004-…md` | the whole document — **a row `implement` added on resume** | cited-fact | Reopened against the branch. Written by `answer-questions` while this item was suspended on `Q-002`, and declared in neither section of the plan, so `document-writes-are-declared` reported it `document.write.undeclared` against `WI-0001`. Nothing in this change falsifies it: it decides how one gate is cleared and asserts nothing about droll. Recorded, not repaired — the row is the work. **`verified-still-true`** | unchanged (v1) |

### The enumeration the quantified claim owes

- `docs/architecture/overview.md` `## Shape` — the outside-world sentence
  - **Enumeration:** *"Only the loop touches the outside world — the streams it was handed, and
    the random number generator"*
    - **Set:** the Python files under `droll/`
    - **Enumerated by:** `ls droll/*.py` → `droll/cli.py`, `droll/expression.py`,
      `droll/formatting.py`, `droll/__init__.py`, `droll/__main__.py`, `droll/roller.py`;
      then `grep -n "sys\.\|open(\|\.write(\|\.readline(\|random\." droll/*.py` over all six
    - **Members:** `__init__.py`, `__main__.py`, `cli.py`, `expression.py`, `formatting.py`,
      `roller.py`
    - **Verdict:** the sentence is **false** in two members. `droll/__main__.py:10` names
      `sys.stdin` and `sys.stdout` — the loop is handed them, but something has to reach for them
      and that something is not the loop. `droll/roller.py:24` has `randint=random.randint` and
      calls it, so the generator is touched by rolling, not by looping. True of the other four:
      `cli.py` is the loop; `expression.py` and `formatting.py` matched nothing in the grep;
      `__init__.py` is empty. The sentence now reads *"Three of the six files under `droll/` touch
      the outside world"* and names which three does what.
    - **Falsifier:** a module outside `cli.py` that reads a stream, opens a file or calls the
      generator. The grep was run over **all six** files rather than over the ones the sentence
      expects to be clean, which is how the two counterexamples appeared; had it been run only
      over `cli.py` it could not have contradicted the sentence at all. `open(` matched nowhere,
      which is the separate claim in the same section that there is no file droll reads or writes.

## Deviations from the plan

1. **`tests/support.py` was added, and the plan's step 6 named four test modules rather than
   five.** It holds `fixed_randint`, `session` and `roll_lines` — the three helpers every test
   module needs and none of which is a test. Adapting *how*, not *what*: no acceptance criterion
   changed and no interface under `droll/` changed. It is also the reason ADR-0002's claim about
   the empty package markers survived: the helpers had somewhere to go that was not
   `tests/__init__.py`.
2. **`3d6+0` prints as `3d6+0 -> 11   [4, 5, 2]`, where the plan's Assumption 2 illustrated it as
   `3d6 -> 11   [4, 5, 2]`.** The plan states two rules that pull against each other for this one
   input: normalisation canonicalises *"the letter `d` … and surrounding whitespace … and nothing
   else"*, while Assumption 2's example rewrites the echoed expression too. The normalisation rule
   was followed, because it is the one AC9 rests on, and the assumption's content — *"a modifier
   of zero is not printed"* — is honoured in the breakdown, where the modifier field is absent. No
   criterion mentions `+0`. `tests.test_formatting.RollLine.test_a_modifier_of_zero_is_not_printed`
   pins the behaviour that shipped.
3. **The plan's `## Approach` still says *"Only the loop touches a stream or the random number
   generator"*, which is the same sentence this execution repaired in the overview and is false
   for the same reason.** It was left alone: `implement` writes the disposition column and the rows
   it appends, and nothing else in `plan.md`. Recorded here so that `verify` and `review-close`
   read it knowing it is a known-false line in a superseded-by-events part of the design, not an
   instruction that was disobeyed.

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, Ran 27 tests, OK |
| `lint-clean` | pass | `python3 -m compileall -q droll tests` → exit 0 |
| `workspace-valid` | pass | `validate-workspace` → exit 0 |
| `every-criterion-has-a-test` | pass | the table above: eleven rows, each naming a test function by its dotted path and a by-hand command with its output. No row says "implemented" and none says "see the code" |
| `commits-reference-the-item` | pass | `check-commit-refs WI-0001 wi/WI-0001` → exit 0 over three commits |
| `no-unplanned-scope` | pass | advisory. `git diff main..HEAD --stat` is ten files: five under `droll/` and five under `tests/`, each traceable to a plan step; plus `docs/architecture/overview.md` and `plan.md`'s disposition column, both of which step 4a requires |
| `cross-answer-consistency` | pass | `lint-answers --changed-since main` → exit 0 |
| `claims-are-sourced` | **fail**, overridden once under ADR-0004 v2 | `lint-claims --changed-since main --plan-documents WI-0001` → exit 1, exactly one error: `docs/product/vision.md:67: ERROR [claim.unsourced] an absolute claim ('all') about 'EP-001/Q-001' with no citation`. Window: 3 paths differing from `main` under `docs/` plus 4 documents named by the plan — non-empty. The claim sits inside `## Engagement state` (heading at line 65, next heading at 77), which no skill may write before the ending. **This row read `pass` in the first version of this report and that was wrong**; `Q-002` was filed because the gate failed. ADR-0004 v2's four properties — code, file, section, sentence — all match, so the bounded override applies and the transition was made with `--force` |
| `document-writes-are-declared` | pass | `lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main` → exit 0. It was **fail** on resume — `ADR-0004`, written on this branch by `answer-questions`, was named in neither section of the plan — and the repair is the invalidation row above. Three documents written on this branch, nine invalidation rows, all disposed |

### ADR-0004's four conditions, checked on the transition

`verify` and `review-close` should re-run these rather than trust the table.

| # | condition | how it was met |
|---|-----------|----------------|
| 1 | a full `run-gate --all --resolving` first, with every verdict recorded | `run-gate --skill implement --item WI-0001 --all --resolving 'WI-0001:in-progress->verifying'` → exit 1. Nine verdicts: six `PASS`, two `MANUAL` (`every-criterion-has-a-test`, `no-unplanned-scope`), one `FAIL`. All nine are in the journal entry for this execution, which is what replaces the run `--force` skips |
| 2 | `claims-are-sourced` is the only hard gate failing | the run's own closing line: `run-gate: 1 hard gate(s) failed: claims-are-sourced`. `document-writes-are-declared`, which failed on the previous resume, exits 0 since `ADR-0004` was declared in the plan's invalidation set |
| 3 | exactly one error, and it is the one ADR-0004 v2's table admits | `lint-claims: 1 error, 0 warnings`. Code `claim.unsourced`; file `docs/product/vision.md`; section `## Engagement state` — the reported line 67 sits between the heading at 65 and the next heading at 77, read with `awk` rather than assumed; sentence reported as an absolute `'all'` about `'EP-001/Q-001'`, which is *"Three questions are open with them, all filed at intake"*. The line number is **not** one of the four properties and v2 says why [src: WI-0001/Q-003] |
| 4 | the history reason names the ADR | the row for this transition names `ADR-0004` |

## What I did not do

- **Nothing in the plan was left undone.** All seven steps were executed.
- **No acceptance criterion was ticked.** The checkboxes in `item.md` are untouched; deciding
  whether a criterion is met is `verify`'s, and this report offers evidence rather than a verdict.
- **`docs/product/vision.md` was not edited at all**, at any of its three rows. They are
  engagement-state sentences and the ending owns them.
- **The upper bound on count and die size is still absent**, deliberately: `100d1000` rolls, and
  the item records that as unconstrained with who left it so. `tests.test_roller.Rolling.test_the_number_of_dice_is_the_count`
  exercises `100d1000` to show it is not accidentally capped.
- **No packaging** — no `pyproject.toml`, no console script, no version number. Out of scope in
  the plan, and `python3 -m droll` is the declared way in.
- **No history, and no way of asking for one.** That is `WI-0002`.

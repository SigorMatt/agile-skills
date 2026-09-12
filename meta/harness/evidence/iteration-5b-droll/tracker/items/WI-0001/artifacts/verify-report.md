# Verification report — WI-0001

Verified-commit: 5dd1dc3dd79f2cb4cc3a2bc2fb9e011239f8a8c0

## Verdict

**Pass.** All eleven acceptance criteria are met, each settled by the observation the criterion
itself names — starting `python3 -m droll`, typing the given text at its prompt, and reading what
was printed. No criterion needed a substitution and none was ambiguous, so every box is `- [x]`
and none is `- [~]`. `WI-0001` goes to `in-review`.

The evidence below is this execution's own. `impl-report.md` was read after the criteria and after
the commands were run, and is cited nowhere as evidence for a verdict.

One defect was found and it is **not** this item's: a stray file named `planned`, carrying captured
`run-gate` output, sits at the repository root and is tracked by git. It is filed as `BUG-0001` and
does not affect any criterion here — see `## Defects found`.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `printf '3d6+2\n' \| python3 -m droll \| cat -A` | `> 3d6+2 -> 15   [5, 3, 5] +2$` then `> $`, exit 0 | Started with no arguments. The prompt precedes the roll line and returns after it; `cat -A` shows the trailing `> ` is really there rather than inferred from a newline |
| AC2 | pass | `yes '3d6+2' \| head -50 \| python3 -m droll`, each line re-added mechanically | `checked 50 lines, 0 mismatches` | The criterion is an arithmetic identity, so it was checked as one over 50 independent rolls rather than on one line: every line shows exactly three faces and a `+2`, and faces + 2 = the shown total in all 50 |
| AC3 | pass | `yes '1d6' \| head -200 \| python3 -m droll \| grep -o '\[[0-9]*\]' \| sort \| uniq -c` | `25 [1]`, `38 [2]`, `32 [3]`, `38 [4]`, `31 [5]`, `36 [6]` | 200 faces, **six** distinct values against the required three, none outside 1-6 |
| AC4 | pass | `printf '3x6\nd\n3d\n0d6\n3d0\n1d8+1d6\n4d6kh3\nhello\n' \| python3 -m droll` | eight lines of the form `cannot interpret '<text>': expected one dice term with an optional modifier, like 3d6+2 or d20`, then `> `, exit 0 | Each of the eight named inputs: a message naming the offending text, no `->` and so no total, and a ninth prompt proving the session survived. See `## Negative and boundary cases exercised` for the `0d6`/`3d0` boundary |
| AC5 | pass | `printf 'd20\n2d10\n3d6+2\n4d8-2\n' \| python3 -m droll` | `d20 -> 7   [7]`, `2d10 -> 17   [9, 8]`, `3d6+2 -> 12   [4, 3, 3] +2`, `4d8-2 -> 18   [8, 4, 2, 6] -2` | All four rolled, none rejected. The grammar itself is judged against ADR-0001 under `## ADR conformance`, not here |
| AC6 | pass | `printf 'd20\n3d6+2\n' \| python3 -m droll` | `> d20 -> 20   [20]`, `> 3d6+2 -> 10   [3, 2, 3] +2`, `> `, exit 0 | Two roll lines from one invocation; the process was started once, so nothing was restarted between them |
| AC7 | pass | `yes 'd20' \| head -40 \| python3 -m droll`, face compared to total mechanically | `40 lines, 0 mismatches; single bracketed face shown alongside total in every line` | Checked over 40 rolls rather than one, because "the shown die result equals the shown total" is falsifiable only by a line where it does not. The bracketed field is the same field `3d6+2` prints its three faces in |
| AC8 | pass | 40 × `2d10` and 40 × `4d8-2` through one session, each line re-added mechanically | `2d10: 40 lines (two faces, no modifier field); 4d8-2: 40 lines (four faces, -2 modifier); 0 mismatches` | The match was anchored: `2d10` lines were required to end after `]` — a line carrying a modifier field would not have matched and would have been reported `UNPARSED` |
| AC9 | pass | `printf 'D20\n3D6+2\n  3d6+2  \n3 d 6\n' \| python3 -m droll \| cat -A` | `> d20 -> 19   [19]$`, `> 3d6+2 -> 16   [4, 6, 4] +2$`, `> 3d6+2 -> 11   [5, 1, 3] +2$`, `> cannot interpret '3 d 6': …$` | "Rolled exactly as" is readable off the line: `D20` prints as `d20`, `3D6+2` prints as `3d6+2`, and the space-padded form prints identically to the bare one. `3 d 6` takes AC4's path, with the same message shape |
| AC10 | pass | `printf 'quit\n' \| python3 -m droll; echo $?` and the same for `exit` and for empty input; plus `printf '3d6+2\nquit\n' \| python3 -m droll` | `quit` → output `> `, exit 0. `exit` → output `> `, exit 0. empty stdin → `> ` and a newline, exit 0. After a roll: `> 3d6+2 -> 16   [6, 3, 5] +2` then `> `, exit 0 | All three ways out give status 0. "Nothing further that looks like a roll" checked as the absence of `->` after the quit word, on a session that had already printed a roll — the case where a stray line would actually have somewhere to come from |
| AC11 | pass | `printf '3x6\n3d6+2\n' \| python3 -m droll` | `> cannot interpret '3x6': …`, `> 3d6+2 -> 16   [4, 6, 4] +2`, `> `, exit 0 | The roll after the rejection is the same shape as AC1's roll with no rejection before it, which is the "does not change what a later roll prints" half |

## ADR conformance

The plan's `## Binding ADRs` names three. A fourth, ADR-0004, is engaged by this change and is not
on that list; its row is below, and the plan itself asks for it — *"`verify` and `review-close`
should check the bound rather than the conclusion"*.

| ADR | verdict | clause quoted from its Decision | file and line, or why not engaged |
|-----|---------|--------------------------------|-----------------------------------|
| ADR-0001 | conforms | *"`count` is a positive integer. When it is omitted the expression means one die, so `d20` and `1d20` are the same roll."* | `droll/expression.py:50` `count = int(written_count) if written_count else 1`, and `:52-53` `if count < 1 or sides < 1: raise ExpressionError(stripped)`. Observed: `0d6` rejected, `1d6` rolled |
| ADR-0001 | conforms | *"`sides` is a positive integer, and is not defaulted or restricted to the familiar solids: `d3` and `d100` are as acceptable as `d20`."* | `droll/expression.py:15`, `(?P<sides>[0-9]+)` with no whitelist, and the same positivity check at `:52`. Observed at the clause's own examples: `printf 'd3\nd100\nd20\n' \| python3 -m droll` → `d3 -> 1   [1]`, `d100 -> 63   [63]`, `d20 -> 5   [5]`; and `3d0` rejected |
| ADR-0001 | conforms | *"`modifier`, when present, is a non-negative integer preceded by `+` or `-`, and is added to or subtracted from the sum of the dice."* | `droll/expression.py:15` `(?P<modifier>[+-][0-9]+)?` — the sign is required and the digits are unsigned; `droll/roller.py:21` `return sum(self.dice) + self.expression.modifier`. Observed as arithmetic over 90 lines under AC2 and AC8 |
| ADR-0001 | conforms | *"Anything that is not of this form is not accepted, and is reported by `WI-0001` AC4's error path rather than rolled"* | `droll/expression.py:44-46` raises on a non-match; `droll/cli.py:37-40` routes `ExpressionError` to `format_rejection` rather than to `roll`. Observed on all eight of AC4's inputs plus `3 d 6` |
| ADR-0002 | conforms | *"droll takes no third-party package, for the product or for its own tooling."* | `droll/roller.py:6` `import random` and `droll/expression.py:9-10` `import dataclasses` / `import re` are the only non-project imports in the product, and `tests/support.py:5` `import io` the only one added by the tests. Enumerated rather than asserted: every `import`/`from` line in `droll/` and `tests/` is `__future__`, a `droll.`/`tests.` module of this project, or one of `random`, `dataclasses`, `re`, `sys`, `io`, `unittest` — each of which `importlib.util.find_spec` resolves under `/usr/lib/python3.12` or to `built-in`/`frozen`. No `pyproject.toml`, `setup.py` or `setup.cfg` exists |
| ADR-0002 | conforms | *"Tests are `unittest.TestCase` classes under `tests/`, discovered from the repository root."* | `tests/test_cli.py:14`, `tests/test_expression.py:16`, `tests/test_formatting.py:17`, `tests/test_roller.py:12` and six more. Ten `class …(unittest.TestCase)` across `tests/test_cli.py`, `test_expression.py`, `test_formatting.py`, `test_roller.py`; `python3 -m unittest discover -s tests -t .` → exit 0, Ran 27 tests. `tests/support.py` declares no test and holds only helpers |
| ADR-0002 | conforms | *"The test command does **not** pass vacuously. With no test module present it exits 5, not 0"* | `tracker/project.yaml:12` carries that command verbatim, and `tests/test_cli.py:76` is the last assertion of the 27 it discovers. The gate run reports `Ran 27 tests`, not `NO TESTS RAN`, so the command is not passing on an empty suite here |
| ADR-0003 | conforms | *"Every line droll writes during a session — the prompt, a roll line, and the message for an expression it cannot interpret — is written to standard output."* | `droll/cli.py` writes only to `stdout` — `droll/cli.py:22` prompt, `droll/cli.py:27` end-of-input newline, `droll/cli.py:40` rejection, `droll/cli.py:42` roll line. Checked at the clause's hardest member, the rejection: `printf '3x6\n' \| python3 -m droll 2>stderr >stdout` → stdout carries the prompt and `cannot interpret '3x6': …`; **stderr is 0 bytes** |
| ADR-0003 | conforms | *"The prompt is flushed before the program waits for input, so that a person sees it before typing."* | `droll/cli.py:22`, `droll/cli.py:23` and `droll/cli.py:25`: `stdout.write(PROMPT)`, `stdout.flush()`, then `stdin.readline()`, in that order |
| ADR-0004 | conforms | *"`implement` is authorised to make `WI-0001`'s `in-progress → verifying` transition with `--force`, under four conditions, all of them checkable by `verify` and `review-close`"* | `tracker/items/WI-0001/history.md:16`, the `in-progress → verifying` row, is the transition the clause authorises, and it names the ADR and carries `[gates forced]`. Re-checked rather than read: see `## The ADR-0004 override, re-checked`. All four conditions hold |

## The ADR-0004 override, re-checked

The plan asks for the bound to be compared against its four properties rather than against a
coordinate, so this execution re-ran the identical command:
`python3 .claude/agile-skills/scripts/run-gate --skill implement --item WI-0001 --all --resolving 'WI-0001:in-progress->verifying'` → exit 1.

| # | condition | what this execution found |
|---|-----------|---------------------------|
| 1 | a full `run-gate --all --resolving` first, every verdict recorded | The re-run produces nine verdicts — six `PASS` (`tests-pass`, `lint-clean`, `workspace-valid`, `commits-reference-the-item`, `cross-answer-consistency`, `document-writes-are-declared`), two `MANUAL` (`every-criterion-has-a-test`, `no-unplanned-scope`), one `FAIL`. `impl-report.md`'s `## Gates` table records the same nine |
| 2 | `claims-are-sourced` is the only hard gate failing | The run's own closing line: `run-gate: 1 hard gate(s) failed: claims-are-sourced` |
| 3 | exactly one error, matching code / file / section / sentence | `lint-claims: 1 error, 0 warnings`. **code** `claim.unsourced` ✓. **file** `docs/product/vision.md` ✓. **section** read with `awk` rather than assumed: the reported line 67 lies between `## Engagement state` at line 65 and `## Change log` at line 77 ✓. **sentence** the run reports *an absolute claim ('all') about 'EP-001/Q-001'*, and `docs/product/vision.md:68` is *"Three questions are open with them, all filed at intake: `EP-001/Q-001`, …"* ✓. The coordinate is again `:67` — the first line of the bullet chunk, one line above the claim's own sentence, which is exactly the paragraph-offset behaviour ADR-0004 v2 documents and deliberately does not bind on |
| 4 | the history reason names the ADR | The `in-progress → verifying` row reads *"overridden once under ADR-0004 v2 … [gates forced]"* |

The override was applied within its bound. It remains a forced hard gate in this item's history,
and `review-close` inherits the same re-runnable check.

## Invalidation set

Nine rows in `plan.md`. Every one carries a disposition. Nothing below was repaired by this
execution; no file under `docs/` was written.

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/product/vision.md` — `## Engagement state`, *"Three questions are open with them, all filed at intake"* | owned-by-ending | Left exactly as it is, and checked that it **was** left alone: `git diff main..HEAD -- docs/product/vision.md` touches three hunks — the header, `## What it is for`, and the change log. None is inside `## Engagement state` (lines 65-76). No defect |
| `docs/product/vision.md` — `## Engagement state`, *"Two work items exist, both at `draft`…"* | owned-by-ending | Same diff, same finding: untouched by this item. No defect |
| `docs/product/vision.md` — `## What it deliberately is not`, closing paragraph | owned-by-ending | Same diff: the paragraph at lines 61-63 appears only as unchanged context. Untouched. No defect |
| `docs/architecture/overview.md` — `## Components`, the five module paths and what each holds; `## Conventions`, *"Started as a module: `python3 -m droll`"* | verified-still-true | **Reopened.** Enumeration below. Still true |
| `docs/architecture/adr/ADR-0002-standard-library-only-including-the-tooling.md` — `## Consequences`, *"`plan` created both as empty files"* | verified-still-true | **Reopened.** Enumeration below. Still true |
| `docs/architecture/overview.md` — `## Shape`, the outside-world sentence | to-update | The document was updated: v1 → v2, header `version: 2`, and a `## Change log` row at v2 naming `implement` and `WI-0001` and describing this repair. The replacement sentence was read against the tree as well — see the enumeration below |
| `docs/product/vision.md` — `## What it is for`, closing sentence | to-update | The document was updated: v3 → v4, header `version: 4`, and a `## Change log` row at v4 naming `answer-questions` and `WI-0001`. The sentence now carries `[src: WI-0001/Q-001; EP-001]` |
| `docs/architecture/overview.md` — `## Components`, *"`cli` knows about streams and not about the grammar"* | to-update | Covered by the same v1 → v2 bump and change-log row. The replacement at `overview.md:45-47` reads *"`cli` owns the streams and calls `parse`, but what is accepted and what is not lives in `expression` and is not restated anywhere else"*, which matches `droll/cli.py:7` importing `parse` and `ExpressionError` |
| `docs/architecture/adr/ADR-0004-an-engagement-state-sentence-can-block-a-gate-nobody-may-clear.md` — the whole document | to-update | The document was updated: v1 → v2, header `version: 2`, and a `## Change log` row at v2 naming `answer-questions` and `WI-0001`. **`impl-report.md`'s `## Documents` table still records this row as `verified-still-true … unchanged (v1)`** — stale, and contradicted by `plan.md`, which is the authoritative carrier of the disposition column. Recorded under `## Defects found` as a record inconsistency, not a send-back |

### The two `verified-still-true` rows, reopened

**`overview.md` `## Components` — the five module paths and what each holds.**

- **Set:** the five rows of the `## Components` table.
- **Enumerated by:** reading the table's path cells → `droll/expression.py`, `droll/roller.py`,
  `droll/formatting.py`, `droll/cli.py`, `droll/__main__.py`; then `ls droll/*.py` → those five
  plus `droll/__init__.py`; then `grep -oE 'from droll\.[a-z_]+' droll/<each>.py`.
- **Verdict, per member:** all five paths exist. `expression.py` imports nothing from `droll` and
  its row says *"Depends on: nothing"*. `roller.py` imports `expression` and its row says
  *"`expression`, `random`"*. `formatting.py` imports `roller`; its row says `roller`. `cli.py`
  imports `expression`, `formatting` and `roller`; its row says *"all three above"*. `__main__.py`
  imports `cli`; its row says `cli`. The prose claim that *"the dependency arrows run one way, down
  the table"* holds: no module imports one listed below it.
- **Falsifier:** a named path that no longer exists, a row whose `Depends on` cell omits a real
  import, or an import running **up** the table. The grep was run over all five modules, not only
  the ones the table expects to be leaves, so an upward import would have appeared. None did.
  `droll/__init__.py` is absent from the table and is not a counterexample: the row asserts what
  five named paths hold, and `## Shape` separately accounts for all six files.
- **`## Conventions`, third bullet:** *"There is no installed console script and no packaging
  metadata yet"* — checked at its falsifier. `pyproject.toml`, `setup.py` and `setup.cfg` all
  absent; `git ls-files` outside `droll/`, `tests/`, `docs/`, `tracker/` and `.claude/` returns
  `.gitignore`, `CONSUMER-PROMPT.md`, `IDEA.md`, `SIMULATION-NOTICE.md` and `planned` — none of
  which is packaging metadata. `python3 -m droll` starts a session, observed eleven times above.
  (`planned` is the stray file filed as `BUG-0001`.) Still true.

**`docs/architecture/adr/ADR-0002-standard-library-only-including-the-tooling.md` `## Consequences` — *"`plan` created both as empty files"*.**

- **Set:** the two files the bullet names, `droll/__init__.py` and `tests/__init__.py`.
- **Enumerated by:** `wc -c droll/__init__.py tests/__init__.py` → `0` and `0`, and then
  `open(p,'rb').read()` on each → `b''` and `b''`.
- **Verdict:** true of both members.
- **Falsifier:** a byte in either file — a docstring, a re-export, a test helper. This is an
  absolute with its boundary at zero bytes, so it was checked **at** the boundary rather than by
  eyeballing the file: `wc -c` alone would have read `0` for a file of nothing, and the `repr`
  confirms there is not even whitespace. The plausible counterexample was real and was avoided
  by construction — `implement` put `fixed_randint`, `session` and `roll_lines` in
  `tests/support.py`, a separate module, which is the declared deviation 1. Still true.

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 27 tests`, `OK`, run by this execution on the branch head |
| `lint-clean` | pass | `python3 -m compileall -q droll tests` → exit 0. ADR-0002 states what this does not cover, so the code was read as well (`## Defects found`) |
| `workspace-valid` | pass | `validate-workspace` → exit 0, 3 items, 6 documents, 0 errors, 0 warnings |
| `every-criterion-independently-checked` | pass | `## Criteria` above: eleven rows, each naming a command this execution ran and quoting its actual output. `impl-report.md` is cited as evidence in none of them |
| `negative-cases-exercised` | pass | `## Negative and boundary cases exercised`: AC4's eight inputs plus `3 d 6` triggered through a live session, the positive-integer boundary crossed in both directions, the blank and whitespace-only lines, and the empty-stdin path |
| `a-criterion-about-criteria-is-read` | pass | Ran, and vacuous: AC1-AC11 were each read and none has criteria as its subject — every one names an input to type and an output to read. `WI-0001` is the first item in this engagement, so there are no earlier criteria for one to cover |
| `adr-conformance-is-decided` | pass | `lint-documents --rule adr-conformance-is-decided --item WI-0001` → exit 0 once `## ADR conformance` was written. Ten quoted clauses across ADR-0001/0002/0003, plus the engaged-but-unlisted ADR-0004 |
| `invalidation-set-is-disposed` | pass | `lint-documents --rule invalidation-set-is-disposed --item WI-0001` → exit 0 once `## Invalidation set` was written. Nine rows, all disposed; the two `verified-still-true` rows reopened with enumerations |
| `tests-would-fail-without-the-change` | pass | advisory. Twelve mutations, `## Test sensitivity check` |

## Negative and boundary cases exercised

- **AC4's eight named inputs**, triggered through a live session rather than read about:
  `3x6`, `d`, `3d`, `0d6`, `3d0`, `1d8+1d6`, `4d6kh3`, `hello`. Eight messages, no `->` on any
  line, and a ninth prompt.
- **The positive-integer boundary, crossed in both directions in one session.**
  `printf '0d6\n1d6\n3d0\n3d1\n1d1\n' | python3 -m droll` → `0d6` rejected, `1d6 -> 5   [5]`,
  `3d0` rejected, `3d1 -> 3   [1, 1, 1]`, `1d1 -> 1   [1]`. This is the interesting half of
  ADR-0001's *"positive integer"*: rejecting `0d6` is cheap to get right by rejecting `1d6` too,
  and `3d1`/`1d1` are what rule that out.
- **Whitespace inside the expression:** `3 d 6` → `cannot interpret '3 d 6': …`, the same path
  and message shape as AC4's eight.
- **The empty input line**, twice over: `printf '\n   \n3d6+2\n' | python3 -m droll` → `> > > ` then
  the roll line. A bare newline and a whitespace-only line each re-prompt silently and print
  nothing, which is plan Assumption 4 and is what AC10's *"Ctrl-D on an empty line"* presumes.
- **Empty stdin** — the end-of-input path with nothing before it: `printf '' | python3 -m droll`
  → `> ` and a newline, exit 0.
- **Quitting with a roll already printed:** `printf '3d6+2\nquit\n' | python3 -m droll` → the roll
  line, then `> `, exit 0. Nothing further that looks like a roll, checked on the only session
  where a stray line would have had a source.
- **The parser's declared over-acceptance** (plan `## Risks`), triggered rather than assumed:
  `03d6 -> 11   [3, 5, 3]`, `3d6+0 -> 12   [3, 6, 3]`, and `100d1000 -> 46489   [726, 743, …]`
  with a hundred faces. All three are outside every criterion and none is forbidden by one; the
  unbounded count and die size are recorded in `item.md` with who left them so.
- **The case-insensitive quit word** (plan Assumption 5): `printf 'QUIT\n' | python3 -m droll` →
  `> `, exit 0.
- **ADR-0003's stream split:** a rejection with the two streams captured separately — stdout
  carries prompt and message, stderr is 0 bytes.

## Test sensitivity check

Twelve mutations were applied to the branch head one at a time, the suite run against each, and
each reverted with `git checkout --` before the next. Every mutation produced at least one
failure, so no criterion's named test passes against an absent implementation.

| # | behaviour removed | criteria it serves | result |
|---|-------------------|--------------------|--------|
| M1 | `run` no longer writes `PROMPT` | AC1, AC4, AC6 | 4 failures, incl. `test_a_prompt_is_written_before_anything_is_read` |
| M2 | the quit-word branch in `run` | AC10 | 1 failure, `test_quitting_writes_no_further_line` |
| M3 | the modifier field dropped from `format_roll` | AC2, AC8 | 5 failures, incl. `test_three_dice_and_a_positive_modifier`, `test_four_dice_and_a_negative_modifier` |
| M4 | the bracketed face list dropped from `format_roll` | AC2, AC7, AC8 | 9 failures, incl. `test_a_bare_d20_prints_in_the_same_shape` |
| M5 | the `count < 1 or sides < 1` check in `parse` | AC4 | 2 failures + 1 error, at subtests `0d6` and `3d0` |
| M6 | the grammar widened to accept `3x6` | AC4 | 3 failures + 1 error, at subtest `3x6` |
| M7 | `[dD]` narrowed to `[d]` | AC9 | 3 errors, incl. `test_a_capital_d_parses_exactly_as_a_small_one` |
| M8 | `text.strip()` removed from `parse` | AC9 | 3 errors, incl. `test_surrounding_whitespace_is_ignored` |
| M9 | `randint(1, sides)` replaced by the constant `4` | AC3 | 12 failures, incl. `test_two_hundred_d6_rolls_span_at_least_three_faces_and_none_outside_one_to_six` |
| M10 | `format_rejection` stops naming the offending text | AC4, AC11 | 10 failures, incl. `test_it_names_the_text_it_could_not_interpret` |
| M11 | an omitted count means two dice | AC5 | 3 failures + 3 errors, incl. `test_an_omitted_count_means_one_die` |
| M12 | `run` returns after the first roll | AC6, AC11 | 3 failures, incl. `test_two_expressions_are_rolled_in_one_run` |

Two things this check turned up that the table does not show:

1. **One assertion is insensitive, and it is worth naming because it looks like the one that
   covers AC10.** Under M2, `test_quit_exit_and_end_of_input_all_end_it_with_status_zero` still
   **passed**: with the quit branch gone, `quit` falls through to `parse`, is rejected, and the
   session then ends at end-of-input with status 0 and no `->` in the output — so both of that
   test's assertions hold against the absent behaviour. AC10 is nonetheless covered, by
   `test_quitting_writes_no_further_line`, which fails. Noted rather than fixed: writing tests is
   not this stage's to do, and the criterion has a sensitive test.
2. **The first pass of this check was contaminated and was re-run from scratch.** Applying a
   mutation, running the suite and restoring with `git checkout --` all complete inside one
   second, and `git checkout` stamps the restored file with the current time. Python compares a
   `.pyc`'s recorded source mtime for **equality**, so a restore landing in the same second as
   the mutated compile leaves the stale bytecode looking current, and the next mutation's run
   reports failures belonging to the previous one — which is how a `droll/cli.py` mutation
   appeared to break `tests/test_formatting.py`. Every result above comes from a second pass that
   deletes every `__pycache__` directory before and after each mutation. A mutation check that
   does not do this can report a test as sensitive when what failed was the run before it.

## Defects found

**`BUG-0001` — a stray file named `planned` is tracked at the repository root.** Not this item's
behaviour and not covered by any of its criteria, so it is filed rather than sent back. It is 3289
bytes of captured `run-gate` output and it entered at commit `6788e55`, the `plan` execution for
`WI-0001`, which is `main`'s tip and this branch's base — so it is not in `main..HEAD` and no gate
on this item ever had it in scope. Its content shows how: the first line records
`--resolving WI-0001:ready-` and `exited 2`, the truncation of `WI-0001:ready->planned` by an
unquoted shell redirect, which then created the file it was named after. Filed at `ready` with
`found-in: WI-0001`. Priority `low`: nothing depends on it and droll is unaffected.

**A stale row in `impl-report.md`, recorded and not repaired.** Its `## Documents` table records
the `ADR-0004` entry as `verified-still-true … unchanged (v1)`. That was true when written and
stopped being true when `answer-questions` amended the ADR to v2 and moved the row in `plan.md` to
`to-update`. `plan.md` — the authoritative carrier of the disposition column — is correct, and the
document really was updated with a version bump and a change-log row, so the substance is sound and
only the report's copy of it is stale. Not a send-back: no acceptance criterion, ADR or gate
depends on it, and `impl-report.md` is a report of an execution rather than a live document.
`review-close` should read the `plan.md` row.

**Read of the diff against the plan (`no-unplanned-scope`, by hand).** `git diff main..HEAD` adds
ten files under `droll/` and `tests/`, and every one traces to a plan step: `expression.py` (1),
`roller.py` (2), `formatting.py` (3), `cli.py` (4), `__main__.py` (5), the four test modules (6),
and `tests/support.py`, which is `implement`'s declared deviation 1. No hunk was found that no
criterion and no plan step accounts for. The two remaining declared deviations were checked and
both are honest: `3d6+0` echoes as `3d6+0` rather than `3d6` — the plan states two rules that
conflict on that one input and the normalisation rule, which AC9 rests on, was the one followed —
and `plan.md`'s `## Approach` still carries the outside-world sentence that `implement` repaired in
`overview.md`, left alone because `implement` may not rewrite a plan's prose.

**No defect was found in droll's behaviour.** The code was read in full, as ADR-0002 asks a reader
to do given what `compileall` does not cover, and nothing was found that the criteria, the ADRs and
the mutation check between them do not already pin.

## Not verified, and why

- **The `## Engagement state` claim that ADR-0004's override leaves standing** is not cleared by
  this execution and could not be: the section belongs to the ending. It is a live
  `claims-are-sourced` failure at `docs/product/vision.md:67` and `review-close` inherits it as
  ADR-0004 condition 4 describes. What was verified is that the override stayed inside its bound,
  not that the claim is now sourced — it is not.
- **AC3 is statistical and was observed once**, at 200 rolls giving six distinct faces. The
  criterion asks for at least three, and a correct implementation can in principle fail it; the
  plan prices that below 10^-40. A pass here is evidence that the generator is being called per
  die, not a proof about its distribution, and the vision declines any claim about statistical
  quality in any case.
- **No test drives a real terminal.** Every observation in `## Criteria` reads a pipe, so what was
  checked is the flushed stream rather than what a person at a tty sees. ADR-0003's one-stream
  decision and the flush after every write are what make the two the same order; a future change
  writing to a second stream would break that equivalence without breaking anything above.
  Verifying it properly needs a pty, which was not used here.
- **`lint-clean` is a compile check only.** Unused imports, undefined names on unexecuted
  branches and shadowed builtins are outside it, by ADR-0002's own statement. The code was read to
  compensate; a read is not a linter.
- **Long-run behaviour was not exercised** beyond the 200-roll session: no test runs droll for
  thousands of inputs or checks memory, and no criterion asks for it.
- **`BUG-0001`'s fix is not verified** — the bug is filed, not fixed, and this execution did not
  touch the file. `verify` repairs nothing.

# Plan — WI-0001 Roll a dice expression and show the result with its breakdown

## Problem

droll does not exist yet: this item creates the whole of it except the session history. Someone at
a terminal starts the tool, types a dice expression such as `3d6+2` at a prompt, and is shown one
plain-text line carrying the total together with each die's face and the modifier separately, so
that adding up what they can see reproduces the total. They can type expression after expression
in the same run, mistype one and be told which text was not understood without losing the session,
and end it with `quit`, `exit` or end-of-input. The constraints are fixed and all of them are
already recorded: the accepted expression is one dice term with an optional integer modifier
[src: ADR-0001]; the breakdown's content is the stakeholder's own choice and its layout is ours
[src: WI-0001/Q-001]; a session is one run of one long-lived prompt [src: EP-001/Q-001]; and
nothing is written to disk [src: EP-001/Q-003]. The remembering half is `WI-0002` and is out of
scope here.

## Approach

One process, one loop, three pure steps between the two ends — the shape recorded in
`docs/architecture/overview.md`, created by this execution. Text comes in, is parsed into a
`DiceExpression` or rejected, a `DiceExpression` is rolled into a `RollResult`, and a `RollResult`
is rendered as one line. Only the loop touches a stream or the random number generator.

The interfaces below are the contract between the modules. They are what `implement` must provide;
how each body is written is `implement`'s.

**`droll/expression.py`**

```python
class ExpressionError(ValueError):
    """Raised for text that is not an accepted expression. Carries `.text`, the offending input."""

@dataclasses.dataclass(frozen=True)
class DiceExpression:
    count: int        # how many dice, always >= 1
    sides: int        # faces per die, always >= 1
    modifier: int     # added to the sum of the dice; 0 when the expression carried none
    text: str         # the normalised source, e.g. "3d6+2" — see "Normalisation" below

def parse(text: str) -> DiceExpression: ...
```

The accepted shape is `[count]d<sides>[(+|-)modifier]` [src: ADR-0001], recognised against the
input with surrounding whitespace removed. A missing count means one die. `count` and `sides` are
positive integers, so `0d6` and `3d0` match the shape and are still rejected — the grammar's own
wording, not an extra rule. Anything else raises `ExpressionError` carrying the text it was given.

**Normalisation.** `text` is rebuilt from what was matched, with two things canonicalised and
nothing else: the letter `d` is lower-cased, and surrounding whitespace is gone. An omitted count
stays omitted and digits are reproduced as typed. So `D20` normalises to `d20`, `  3D6+2  ` to
`3d6+2`, and `d20` to itself. This is what makes AC9 observable by reading one line: the two
spellings do not merely roll the same, they print the same.

**`droll/roller.py`**

```python
@dataclasses.dataclass(frozen=True)
class RollResult:
    expression: DiceExpression
    dice: tuple[int, ...]          # one face per die, in the order rolled
    @property
    def total(self) -> int: ...    # sum(dice) + expression.modifier

def roll(expression: DiceExpression, randint=random.randint) -> RollResult: ...
```

`randint` is a parameter with the standard library's function as its default. The vision declines
any claim about statistical quality, reproducibility or seeding [src: docs/product/vision.md], so
nothing configures a generator; the parameter is there so a test can substitute a known sequence
and assert on an exact printed line.

**`droll/formatting.py`**

```python
def format_roll(result: RollResult) -> str: ...
def format_rejection(text: str) -> str: ...
```

The roll line is the expression, the total, the faces, and the modifier when there is one:

```
3d6+2 -> 13   [4, 5, 2] +2
d20 -> 17   [17]
2d10 -> 12   [8, 4]
4d8-2 -> 14   [5, 3, 6, 2] -2
```

Three spaces separate the total from the breakdown; one space separates the faces from the
modifier; the modifier carries its sign. A modifier of zero prints as none at all, which is the
same thing said twice. The rejection line names the text it could not interpret and what was
expected:

```
cannot interpret '3x6': expected one dice term with an optional modifier, like 3d6+2 or d20
```

**`droll/cli.py`**

```python
PROMPT = "> "
QUIT_WORDS = frozenset({"quit", "exit"})

def run(stdin, stdout, randint=random.randint) -> int: ...
```

Per turn of the loop: write `PROMPT` to `stdout` and flush it, then read one line from `stdin`.

| what was read | what happens |
|---------------|--------------|
| `""` — end of input | write a newline, return `0` |
| a line that is blank once stripped | write nothing, take the next turn |
| a stripped line in `QUIT_WORDS`, compared lower-cased | return `0`, writing nothing |
| anything else that `parse` accepts | write `format_roll(roll(...))` and a newline |
| anything else that `parse` rejects | write `format_rejection(...)` and a newline, take the next turn |

Every write goes to `stdout` [src: ADR-0003] and is followed by a flush, so a transcript captured
from a pipe is in the order a person at a terminal would have seen it. The streams are parameters
rather than `sys.stdin` and `sys.stdout` reached for directly: AC6 and AC11 are about what happens
across two inputs in one run, and a test that can hand the loop two strings is the only way to
observe them without driving a terminal.

**`droll/__main__.py`** calls `sys.exit(run(sys.stdin, sys.stdout))` under the usual
`if __name__ == "__main__":` guard, so `python3 -m droll` starts a session.

## Steps

1. **Write `droll/expression.py`.** Provide `ExpressionError`, `DiceExpression` and `parse` with
   the signatures above. Afterwards: `parse` returns a `DiceExpression` for each of `d20`,
   `2d10`, `3d6+2`, `4d8-2`, `D20`, `3D6+2` and `  3d6+2  `, with `text` normalised as described;
   and it raises `ExpressionError` for each of `3x6`, `d`, `3d`, `0d6`, `3d0`, `1d8+1d6`,
   `4d6kh3`, `hello` and `3 d 6`, with `.text` equal to the input stripped of surrounding
   whitespace.

2. **Write `droll/roller.py`.** Provide `RollResult` and `roll`. Afterwards: `roll` produces
   exactly `expression.count` faces, each obtained by one call to `randint(1, expression.sides)`,
   and `total` equals their sum plus `expression.modifier`. With a substituted `randint` returning
   4, 5 then 2 for `3d6+2`, `dice` is `(4, 5, 2)` and `total` is `13`.

3. **Write `droll/formatting.py`.** Provide `format_roll` and `format_rejection`. Afterwards:
   `format_roll` on the `(4, 5, 2)` result above returns exactly `3d6+2 -> 13   [4, 5, 2] +2`;
   on a `d20` result rolling 17 it returns `d20 -> 17   [17]`; on a `2d10` result rolling 8 and 4
   it returns `2d10 -> 12   [8, 4]`; on a `4d8-2` result rolling 5, 3, 6 and 2 it returns
   `4d8-2 -> 14   [5, 3, 6, 2] -2`. `format_rejection("3x6")` returns a single line containing
   `'3x6'` and no digits that could be read as a total.

4. **Write `droll/cli.py`.** Provide `PROMPT`, `QUIT_WORDS` and `run`, dispatching exactly as the
   table under `## Approach` says. Afterwards: driving `run` with a `StringIO` containing
   `"d20\n3d6+2\n"` writes two prompts and two roll lines and returns `0` at end of input; with
   `"3x6\n3d6+2\n"` it writes a rejection line and then a roll line; with `"quit\n"` and with
   `"exit\n"` it returns `0` having written only the prompt; with `""` it returns `0`.

5. **Write `droll/__main__.py`.** Afterwards: `printf '3d6+2\n' | python3 -m droll` prints a
   prompt and one roll line and exits `0`, and `printf 'quit\n' | python3 -m droll` exits `0`.

6. **Write the tests under `tests/`**, as `unittest.TestCase` classes [src: ADR-0002], one module
   per module under test: `tests/test_expression.py`, `tests/test_roller.py`,
   `tests/test_formatting.py` and `tests/test_cli.py`. The observable results named in steps 1-5
   are the assertions; the `## Acceptance criteria mapping` table below says which test each
   criterion is demonstrated by. `tests/test_cli.py` also carries the two whole-session
   observations that no single function can show: the two-hundred-roll spread (AC3) and the
   end-of-input path (AC10). Afterwards:
   `python3 -m unittest discover -s tests -t .` exits `0`, having run more than zero tests.

7. **Run the declared gate commands and record their output**:
   `python3 -m unittest discover -s tests -t .` and `python3 -m compileall -q droll tests`. Both
   are in `tracker/project.yaml`, put there by this execution.

Deciding whether each acceptance criterion is met is `verify`'s, not `implement`'s; steps 1-7 say
what to build and what to observe, and the checkboxes in `item.md` are ticked by nobody else.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 4, 5 | `tests/test_cli.py` — a session driven with `"3d6+2\n"` writes `PROMPT` and then one line whose first field is `3d6+2 -> <total>`; and by hand, `printf '3d6+2\n' \| python3 -m droll` |
| AC2 | 3, 4 | `tests/test_formatting.py` — `format_roll` on a `3d6+2` result rolling 4, 5, 2 returns exactly `3d6+2 -> 13   [4, 5, 2] +2`, so the three faces and the `+2` are each present separately and 4+5+2+2 = 13 |
| AC3 | 2, 4, 6 | `tests/test_cli.py` — a session driven with two hundred `1d6` lines and the real `randint`; the bracketed faces are collected from the output, and the test asserts at least three distinct values and none outside 1-6. By hand: `yes 1d6 \| head -200 \| python3 -m droll \| grep -o '\[[0-9]*\]' \| sort -u` |
| AC4 | 1, 3, 4 | `tests/test_expression.py` — `parse` raises `ExpressionError` for each of the eight inputs AC4 names, as a table-driven case. `tests/test_cli.py` — a session driven with those eight lines writes eight rejection lines, each containing the offending text, and no roll line. By hand: `printf '3x6\nd\n3d\n0d6\n3d0\n1d8+1d6\n4d6kh3\nhello\n' \| python3 -m droll` |
| AC5 | 1 | `tests/test_expression.py` — `parse` returns a `DiceExpression` for each of `d20`, `2d10`, `3d6+2` and `4d8-2`, with `count`, `sides` and `modifier` asserted as 1/20/0, 2/10/0, 3/6/+2 and 4/8/-2 |
| AC6 | 4 | `tests/test_cli.py` — one `run` call driven with `"d20\n3d6+2\n"` writes two roll lines in that order; the second is written by the same call, so no restart occurred. By hand: `printf 'd20\n3d6+2\n' \| python3 -m droll` |
| AC7 | 1, 3 | `tests/test_formatting.py` — `format_roll` on a `d20` result rolling 17 returns exactly `d20 -> 17   [17]`: the face is shown in the same bracketed field as `3d6+2`'s three faces, and it equals the total |
| AC8 | 3 | `tests/test_formatting.py` — `2d10` rolling 8 and 4 returns exactly `2d10 -> 12   [8, 4]`, which carries two faces and no modifier field and 8+4 = 12; `4d8-2` rolling 5, 3, 6, 2 returns exactly `4d8-2 -> 14   [5, 3, 6, 2] -2`, which carries four faces and `-2` and 5+3+6+2-2 = 14 |
| AC9 | 1, 3 | `tests/test_expression.py` — `parse("D20")` and `parse("d20")` return equal `DiceExpression` values, as do `parse("3D6+2")`, `parse("3d6+2")` and `parse("  3d6+2  ")`; and `parse("3 d 6")` raises `ExpressionError`. Because `text` is part of the value, equal values render identically, which is what makes "rolled exactly as" readable off one line. By hand: `printf 'D20\n3D6+2\n  3d6+2  \n3 d 6\n' \| python3 -m droll` |
| AC10 | 4, 5 | `tests/test_cli.py` — `run` returns `0` for each of `"quit\n"`, `"exit\n"` and `""`, and in each case the captured output contains no `->`. By hand, for the exit status: `printf 'quit\n' \| python3 -m droll; echo $?` and the same for `exit` and for `printf '' \| python3 -m droll; echo $?` |
| AC11 | 4 | `tests/test_cli.py` — one `run` call driven with `"3x6\n3d6+2\n"` writes a rejection line naming `3x6` and then a normal roll line, and returns `0` at end of input. By hand: `printf '3x6\n3d6+2\n' \| python3 -m droll` |

## Assumptions

Five, each reversible, and none of them taken under a delegation from the stakeholder. The one
delegation this engagement has spent is `EP-001/Q-002`, which covers the notation inside a dice
expression; a prompt string, an entry point and the punctuation of an output line are not dice
notation, so it does not reach any of these. Saying so is the requirement, not a formality —
claiming that licence here would be the unbounded reading it exists to prevent.

1. **The layout of the roll line** — `3d6+2 -> 13   [4, 5, 2] +2`. The stakeholder chose what the
   line contains and the question told them the spacing and punctuation were ours
   [src: WI-0001/Q-001]; the item records the layout as routed here for that reason
   [src: WI-0001]. The shape is the one their chosen option illustrated, with `->` in place of the
   arrow character so the output survives a terminal that is not reading UTF-8.
   *Reversing it:* `format_roll` in `droll/formatting.py`, one function, plus the exact strings in
   `tests/test_formatting.py`. Nothing is persisted and nothing else reads the line — except
   `WI-0002`'s history listing, which is why formatting is a function both can call rather than
   something written inline in the loop.

2. **A modifier of zero is not printed.** `3d6+0` parses, and prints as `3d6 -> 11   [4, 5, 2]`.
   No criterion mentions `+0`, and ADR-0001 permits it because it treats the modifier as a
   non-negative integer with a sign [src: ADR-0001]. Treating "modifier of zero" and "no modifier"
   as one output keeps one shape for every roll.
   *Reversing it:* one condition in `format_roll`.

3. **The prompt is `> `.** No criterion constrains what the prompt looks like, only that one is
   printed and that it comes back.
   *Reversing it:* the `PROMPT` constant in `droll/cli.py`, and the literal in the tests that
   assert on a transcript.

4. **A blank line re-prompts silently.** Pressing enter at the prompt prints nothing and asks
   again. It is not in AC4's list of rejected inputs and it is not an expression; treating it as
   an error would put a message on the screen every time someone taps enter, and AC10's
   *"Ctrl-D on an empty line"* takes for granted that an empty line is a thing one can be sitting
   at.
   *Reversing it:* one branch in `run`.

5. **`quit` and `exit` are matched without regard to case**, so `QUIT` also ends the session.
   AC10 names the two words in lower case and says nothing about case; matching the way AC9 makes
   `D` match `d` is the consistent reading.
   *Reversing it:* dropping one `.lower()` call in `run`.

And one decision that is **not** an assumption because a document settles it: rolling uses
`random.randint` from the standard library, because the vision declines any claim about
statistical quality, reproducibility or seeding [src: docs/product/vision.md] and the item puts
choosing or configuring a generator out of scope [src: WI-0001].

## Decisions and ADRs

| decision | where it is recorded | branch of the preference order |
|----------|---------------------|-------------------------------|
| The accepted expression grammar | ADR-0001 (already existed; this plan is constrained by it, not re-deciding it) | documented |
| Test and lint tooling: `unittest` and `compileall`, no third-party dependency | **ADR-0002**, written by this execution | decided, with the alternatives priced |
| Rejection messages go to standard output, not standard error | **ADR-0003**, written by this execution — the question `refinement-qa.md` A2 routed here | decided, with the alternatives priced |
| The module split, the three seams, and the entry point `python3 -m droll` | `docs/architecture/overview.md`, created by this execution | decided; the entry point is also Assumption 1's neighbour and is additive to reverse |
| Roll line layout, zero modifier, prompt string, blank line, quit-word case | `## Assumptions` 1-5 above | reversible assumption |
| The random number generator | `## Assumptions`, last paragraph | documented (`docs/product/vision.md`) |

No question was put to the stakeholder by this execution: nothing here is irreversible, and
nothing depends on intent the record does not already carry.

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/product/vision.md` | `## Engagement state`, second bullet: *"Three questions are open with them, all filed at intake"* | engagement-state | All three are `answered`, as is `WI-0001/Q-001`. The sentence counts open questions, which is a fact about the engagement rather than about droll. Already false before this change; carried here because `WI-0001/Q-001`'s own consequences recorded that the item had no plan yet to hold the row | owned-by-ending |
| `docs/product/vision.md` | `## Engagement state`, third bullet: *"Two work items exist, both at `draft`; nothing has been refined, designed, built or delivered"* | engagement-state | `WI-0001` is refined and this execution designs it; the steps above deliver it. Every clause of the bullet is about where the engagement has got to | owned-by-ending |
| `docs/product/vision.md` | `## What it deliberately is not`, closing paragraph: *"the elicitation question on the epic is the place where any of them can be contradicted"* | engagement-state | `EP-001/Q-003` is `answered`, so it is no longer a place anything can be contradicted. It is an engagement-state sentence sitting **outside** the delimited section, which is why it is named here explicitly rather than left to be found | owned-by-ending |
| `docs/architecture/overview.md` | `## Components`, the five module paths and what each holds; and `## Conventions this project has adopted`, third bullet, *"Started as a module: `python3 -m droll`"* | cited-fact | This change creates those files. Each row asserts that a named path holds a named responsibility, and an implementation that splits, merges or renames a module makes the row point at nothing | verified-still-true |
| `docs/architecture/adr/ADR-0002-standard-library-only-including-the-tooling.md` | `## Consequences`, first bullet: *"`plan` created both as empty files"* about `droll/__init__.py` and `tests/__init__.py` | cited-fact | Both are scaffolding. If implementation puts code in either — package exports, a test helper — the bullet stops being true of the file it names | verified-still-true |
| `docs/architecture/overview.md` | `## Shape`, the sentence *"Only the loop touches the outside world — the streams it was handed, and the random number generator"* | quantified | **Added by `implement`.** It quantifies over the modules, and two of them falsify it: `droll/roller.py` calls the generator, and `droll/__main__.py` names the real streams. The enumeration is in `artifacts/impl-report.md` | to-update |
| `docs/product/vision.md` | `## What it is for`, closing sentence: *"Without them there is no product, only a shorter way to write `random.randint`"* | cited-fact | **Added by `answer-questions`** while answering `WI-0001/Q-002`. Not falsified by this change — it was an unsourced absolute before this branch existed — but `lint-claims` reads it because this plan names the file, so it is a document this item's branch had to touch and therefore a document this set has to name (`spec/dor-dod.md` D7). Repaired as provenance only; `vision.md` v3 → v4 | to-update |
| `docs/architecture/overview.md` | `## Components`, the sentence *"`cli` knows about streams and not about the grammar"* | cited-fact | **Added by `implement`.** `droll/cli.py` imports `parse` and `ExpressionError` from `droll.expression`, so as written the clause is false; what is true is that the grammar's own definition is not restated outside `expression` | to-update |
| `docs/architecture/adr/ADR-0004-an-engagement-state-sentence-can-block-a-gate-nobody-may-clear.md` | the whole document | cited-fact | **Added by `implement`.** Written on this branch by `answer-questions` while `WI-0001` was suspended on `Q-002`, and named in neither section of this plan, so `document-writes-are-declared` reports it `document.write.undeclared` against **this** item — the gate reads every document the branch touched, whichever skill touched it. Nothing in this change falsifies it. The row is the same act `answer-questions` performed one line above for the file it edited, applied to the file it created [src: run: python3 .claude/agile-skills/scripts/lint-documents --rule document-writes-are-declared --item WI-0001 --changed-since main → exit 1, document.write.undeclared at ADR-0004]. **Disposition changed by `answer-questions`** from `verified-still-true` to `to-update`: answering `WI-0001/Q-003` amended the document to v2, so the row now records a repair rather than a reading | to-update |

`implement` closes each row and may add rows; discovering a sixth document mid-change is the case
that cannot be enumerated from here.

## Deliverable documents

`none`. No acceptance criterion on this item has a document as its subject: all eleven are settled
by typing at the prompt and reading what is printed. The documents above are at risk from this
change, which is a different thing from being asked for by it.

## Binding ADRs

- **ADR-0001** — the accepted expression grammar. Binds step 1 in full: what `parse` accepts and
  rejects, that a missing count means one die, and that `count` and `sides` are positive integers.
  It is what AC4, AC5 and AC9 are checked against.
- **ADR-0002** — standard library only. Binds step 6 (tests are `unittest.TestCase` classes) and
  step 7 (the two gate commands), and forbids reaching for a third-party package anywhere in
  steps 1-5.
- **ADR-0003** — one stream. Binds step 4: the rejection line is written to `stdout`, and the
  transcript AC4 and AC11 are read from is the standard output alone.

## Known gate exception

**`claims-are-sourced` will fail on `WI-0001`'s completion transition, and `implement` is
authorised to override it once.** `WI-0001/Q-002` reported two unsourced absolute claims in
`docs/product/vision.md` that this item did not write. One, at `:42`, was repaired by
`answer-questions`. The other, at `:66`, is inside `## Engagement state`, which no skill may write
between `intake` and the ending — not `implement`, not `answer-questions`, and not `review-close`
at an item close. It is already carried as the first row of the invalidation set above, disposed
`owned-by-ending`.

**ADR-0004** records the decision and bounds the override to four conditions, all checkable:
`implement` runs `scripts/run-gate --skill implement --item WI-0001 --all --resolving
'WI-0001:in-progress->verifying'` first and records every verdict that run produced;
`claims-are-sourced` is the only hard gate failing; its failure is exactly one error, and that
error is the one ADR-0004's table admits — code `claim.unsourced`, file `docs/product/vision.md`,
section `## Engagement state`, sentence *"Three questions are open with them, all filed at
intake"*, quoted verbatim in the journal entry as the run printed it; and the history reason names
ADR-0004. If any of the four does not hold, the authorisation does not apply and the item stays at
`in-progress`.

**The line number is not one of the four properties, and ADR-0004 v2 says why** [src: WI-0001/Q-003].
v1 wrote the error as `docs/product/vision.md:66`; the run reports `:67`. `lint-claims` rule 2
reports at the first line of the blank-line-separated chunk a claim sits in rather than at the
claim's own line, so what it prints is the offset of the whole `## Engagement state` bullet list
and it shifts when anything above it changes length — which is what v1's own execution did to it.
`implement` stopped rather than reading the disqualifier away, which is why this paragraph exists
[src: WI-0001/Q-003].

`verify` and `review-close` should check the bound rather than the conclusion: re-run the same
command and compare it against the four properties, not against a coordinate. `verify` did, and
recorded the four-property comparison in `artifacts/verify-report.md`
[src: tracker/items/WI-0001/artifacts/verify-report.md].

**A second bounded override, for the close — ADR-0004 v3** [src: WI-0001/Q-004]. The same claim
fails `claims-are-sourced` again at `review-close`'s `in-review → done` transition, and ADR-0004
v2's authorisation named `implement` and the `in-progress → verifying` move only. ADR-0004 v3
adds point 4, authorising `review-close` to make the close with `--force` under four conditions of
the same shape: a full `run-gate --skill review-close --item WI-0001 --all --resolving
'WI-0001:in-review->done'` first with every verdict recorded; `claims-are-sourced` the only hard
gate failing; exactly one error matching v2's four properties; and the history reason naming the
ADR [src: ADR-0004].

**The close failed for a different mechanical reason than the transition did, and v3's point 4a
records it.** `review-close`'s gate carries no `--plan-documents`, so what puts
`docs/product/vision.md` in its window is that the file differs from the trunk — which is true
because ADR-0004 point 1 ordered the `:42` repair on this branch. The repair that cleared one
claim is what brought the file into the later gate's scope [src: ADR-0004]. It also bounds this:
once `WI-0001` merges, the file matches the trunk and leaves that window for any later item that
does not edit it.

## Scaffolding

- `droll/__init__.py` — empty. `python3 -m compileall -q droll tests` cannot run against a
  directory that is not a package, and the command had to be run before it could be declared.
- `tests/__init__.py` — empty. `python3 -m unittest discover -s tests -t .` refuses a start
  directory that is not importable, which was observed rather than assumed
  [src: run: python3 -m unittest discover -s tests -t . → ImportError: Start directory is not importable].

Neither file contains a statement. Both are named in ADR-0002's consequences and in the
invalidation set above, so an implementation that puts behaviour in either has a row to close
about it.

## Risks

- **AC3 is a statistical observation and could in principle fail on correct code.** Two hundred
  rolls of a fair `1d6` yielding fewer than three distinct faces has a probability below
  10^-40; the criterion was written to be overwhelmingly safe, and `refinement-qa.md` A1 records
  that the numbers were invented by refinement under no licence. If it ever does fail, the fault
  is far more likely to be in how the test scrapes faces out of the transcript than in the dice.
- **The lint command catches syntax errors and nothing more** [src: ADR-0002]. An unused import,
  an undefined name in a branch no test reaches, or a shadowed builtin will pass it. `verify` and
  `review-close` should read the code rather than read the gate.
- **The parser accepts more than the criteria name.** `03d6` (a leading zero), `3d6+0` and
  `100d1000` all parse. The last is deliberate and recorded: the item leaves the count and die
  size unbounded, with who left them so [src: WI-0001]. The first two are consequences of the
  grammar's shape that no criterion forbids. If any of them turns out to be unwanted it is a
  condition in `parse`, not a redesign.
- **A transcript captured from a pipe is not a terminal.** Every observation command in the
  mapping table redirects droll's output, so what is read is the flushed stream rather than what
  a person sees. ADR-0003's decision and the flush after every write are what keep the two the
  same order; a future change that writes to a second stream would break the equivalence without
  breaking any test that does not check ordering.
- **The interfaces above are a commitment `WI-0002` will inherit.** `RollResult` is what a history
  entry will be, and `format_roll` is what a history listing will call. If either turns out to be
  the wrong shape, the cost lands on that item rather than this one.

## Out of scope for this item

- The session history and any way of asking for it — `WI-0002` [src: WI-0001].
- Any expression form outside ADR-0001's grammar: sums of several dice terms, keep-highest,
  keep-lowest, advantage, exploding dice and multiplication [src: ADR-0001].
- Choosing, configuring or seeding the random number generator [src: WI-0001].
- Packaging: no `pyproject.toml`, no installed console script, no version number. `python3 -m
  droll` is the way in, and adding an entry point later changes nothing below `droll/cli.py`.
- Any configuration file, environment variable or command-line option. droll is started with no
  arguments [src: WI-0001 AC1 "Started with no arguments"].

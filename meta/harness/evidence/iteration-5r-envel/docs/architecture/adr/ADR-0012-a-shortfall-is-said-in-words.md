---
title: A balance is never printed with a minus sign; a shortfall is said in words
version: 2
status: current
updated: 2026-09-11T11:57:12Z
updated-by: answer-questions
updated-for: BUG-0001
---

# ADR-0012 — A balance is never printed with a minus sign; a shortfall is said in words

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for BUG-0001
- **Supersedes:** —

## Context

`BUG-0001` is the one place the stakeholder's rule *"No negative envelopes anywhere in this tool"*
[src: WI-0005/Q-004] is not kept. A month that has already ended can close short, because two of
their own decisions meet: a spend counts in the month it happened [src: WI-0002/Q-001] while
income counts in the month it was typed and carries no date of its own [src: WI-0003/Q-003]. So
last month's shopping, typed in after this month's income, takes last month's closing figure below
zero. The tool prints that as a minus:

```
groceries holds -250.00 at the end of 2026-08
groceries  in 0.00  spent 250.00  moved 0.00  left -250.00
```

The remedy was not ours to choose: each of the four ways out put to them reverses something they
had already decided [src: BUG-0001/Q-001]. It was put to them as `BUG-0001/Q-001`, and they chose
to keep recording the spend and to stop printing the minus:

> *"'Groceries was 250.00 short at the end of 2026-08' tells me exactly what I need and still
> gives me the figure, and a figure I can read is what the adding-up rule was about; a minus sign
> in front of it is what I don't want."* [src: BUG-0001/Q-001]

They refused refusing the spend, refused dating income, and refused qualifying the rule
[src: BUG-0001/Q-001]. What is left for this ADR is *where* in the code the change goes and what
it must not disturb — which is a design decision and has more than one defensible answer.

What must survive, because other decisions rest on it: every figure is a filtered sum over the
entries, and the reconciliation of `WI-0003` AC3 is a property of that arithmetic rather than
something the code arranges [src: ADR-0008]; every amount is rendered by `envel/money.py` and by
nothing else [src: ADR-0001]; and the reports print nothing and exit nothing, returning lines to
`envel/cli.py` [src: ADR-0009].

There is also a distinction this bug forces into the open and nobody has had to name before. Two
different things are printed as amounts:

- a **balance** — what an envelope holds or held at some moment. `envel list`, the opening and
  closing lines of `envel entries`, and the `left` column of `envel summary`;
- a **transaction figure** — how much moved and which way. The `-250.00` on a spend's own line in
  a listing, the `-30.00` on the side a move left, and the summary's `moved` column, which is one
  net number and is negative for an envelope that gave more away than it received
  [src: WI-0003 AC2 "The moved figure is one net number, positive when more arrived than left"].

The stakeholder's rule is about the first. The entry line carrying `-250.00` was printed verbatim
in `Q-001`'s context and the option they chose left it alone [src: BUG-0001/Q-001].

## Options considered

**A — render the shortfall in `envel/money.py`, so no amount anywhere prints a minus.** One
function, one place, and the rule becomes true of the whole tool by construction. Cost: it is
false to the distinction above. It would reword the `-250.00` on a spend's own line and the
`moved` column, which is delivered behaviour the stakeholder has accepted and which two frozen
assertions in `tests/test_entries.py` require [src: BUG-0001 AC5 "with no edit to any assertion that exists at"].
It also makes a transaction's direction unreadable: *"spend groceries 250.00 short"* is not
English and *"spend groceries 250.00"* loses the sign that says money left.

**B — clamp the balance to `0.00` when it is negative.** The smallest possible change and it
satisfies the two criteria that say *no amount less than zero*. Cost: it fails the criterion the
stakeholder's own condition became — the line would no longer add up
[src: BUG-0001 AC6 "The worded closing line still reconciles"] — and it destroys information the
person needs, which is how short they are. They asked for the figure, twice.

**C — change the rendering of a balance only, in `envel/summary.py` and in no other module,
leaving the stored figures and the arithmetic untouched** [src: envel/summary.py]. The three lines that print a balance from a bounded sum get their
sentence from one helper each, and that helper words the negative case. Cost: the rule is true of
these surfaces by a check in one module rather than of the whole tool by construction, so a fourth
surface that prints a balance later would have to remember to use the helper. That cost is named
in the consequences and is the reason the helpers, and not a formatting flag, are the interface.

## Decision

**C.**

1. **`figures()`, `bounded_balance()`, `balance_before()` and `balance_through()` are unchanged,
   and keep returning signed cents.** The reconciliation of `WI-0003` AC3 stays a property of the
   arithmetic [src: ADR-0008], `summary.figures` keeps returning `(0, 0, -3000, 0)` for an
   envelope that only gave money away [src: tests/test_summary.py:149], and nothing about the
   stored document changes. This is the sentence the whole ADR turns on: the fix is a rendering
   fix and reaches no sum.

2. **Two new rendering functions in `envel/summary.py`, and the wording lives in them and nowhere
   else.**

   - `balance_line(name, cents, moment, verb, month)` returns the sentence that brackets a
     listing. For `cents >= 0` it returns what is printed today —
     `"{name} {verb} {amount} at the {moment} of {month}"`, giving
     `groceries held 0.00 at the start of 2026-08` and
     `groceries holds 30.00 at the end of 2026-08`. For `cents < 0` it returns
     `"{name} was {amount} short at the {moment} of {month}"`, giving
     `groceries was 250.00 short at the end of 2026-08` — the sentence the stakeholder was shown
     and accepted [src: BUG-0001/Q-001]. `verb` is unused in the negative case, which is what
     makes *was … short* read the same at either end of the month.
   - `left_column(cents)` returns the summary row's last column: `"left {amount}"` when
     `cents >= 0`, and `"short {amount}"` when it is negative, giving
     `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00`. The label changes rather than
     the number gaining a word after it, because the row is read as label-and-figure pairs and
     `left 250.00 short` breaks that shape.

3. **The amount is still rendered by `envel/money.py` and by nothing else** [src: ADR-0001].
   Both helpers pass `-cents` to `money.format_amount` in the negative case, so the amount keeps
   its two decimal places and acquires no currency symbol
   [src: WI-0003 AC11 "Every figure the summary prints is a plain decimal with exactly two decimal places"].
   `money.format_amount` itself is not touched: it keeps its minus sign, because transaction
   figures still need one.

4. **Transaction figures keep their signs.** `entry_line`'s amount and the summary's `moved`
   column are unchanged [src: WI-0003 AC2 "The moved figure is one net number, positive when more arrived than left"].
   The scope line is the distinction in `## Context`: a figure that answers *how much does this
   hold* is worded; a figure that answers *how much moved, and which way* is signed.

5. **The current-balance messages are untouched.** `envel list`, and the *"which now holds
   30.00"* clause on a successful `new`, `add`, `spend`, `move`, `fix` and `remove`, all print a
   balance as of now, and a balance as of now cannot be negative — a spend, a correction and a
   removal that would take one below zero are each refused already
   [src: WI-0002 AC5 "The listing never shows a negative amount for any envelope"]
   [src: WI-0005 AC9 "below zero"]. They are left alone because no input reaches them, not because
   they are out of this bug's scope by fiat.

## Consequences

**Easy: the bug closes without any sum changing.** Both surfaces are the same filtered sum bounded
by a month [src: envel/summary.py:68] [src: envel/summary.py:196], and neither is touched. There
is no migration, no change to the document, no new field, and nothing recomputes.

**Easy: the reconciliation the stakeholder asked for survives, and is checkable.** The worded line
carries the same magnitude the signed one did, so the opening figure plus the entry lines still
equals the closing one once *short* is read as the minus it replaces
[src: BUG-0001 AC6 "The worded closing line still reconciles"]. That is exactly what distinguishes
this from option B.

**Hard: the rule is now true of three call sites rather than of the whole tool.** A future report
that prints a bounded balance without calling `balance_line` or `left_column` would print a minus
again, and no check in this codebase would stop it — the guard is a branch inside each helper
rather than a property of the type
[src: BUG-0001 AC1 "prints no amount less than zero on either of its **balance** lines"]. The mitigation is that the helpers *are* the
interface — there is no flag to forget to pass, and a reviewer can find every balance printed by
finding the callers of the two functions. Whoever adds a fourth balance surface owes it one of
these two helpers, and this is where that obligation is written down, as `ADR-0008` writes down
the one about a fourth entry kind.

**Hard: two sentences of prose become the tool's contract.** *"was 250.00 short"* and
*"short 250.00"* are now behaviour, asserted by tests, and changing the words is a change to
delivered output. They are the stakeholder's own words from `Q-001` rather than ours, which is why
they are recorded here verbatim.

**Reversibility: easy, and it stays easy.** Reversing to today's behaviour is deleting two
functions and inlining the two `format_amount` calls they wrapped — one module, no stored shape
[src: envel/store.py:11], no migration, no published interface beyond the printed lines. Nothing
is lost on the way, because nothing is discarded: the signed figure is still what the arithmetic
produces and the rendering is the only thing that reads it.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-09-11T11:57:12Z | answer-questions | BUG-0001 | One `provenance` correction, recorded below: `## Consequences`' citation for *"Both surfaces are the same filtered sum bounded by a month"* moved from `envel/summary.py:173` to `envel/summary.py:196`, because this ADR's own implementation pushed `bounded_balance` down by 23 lines. The assertion is unchanged and no code has to change to satisfy the new text, so this ADR is corrected rather than superseded [src: toolkit: doc-header.md section 4b "add a citation to an existing sentence"]. Answering `BUG-0001/Q-002`. |
| 1 | 2026-09-11T11:13:17Z | plan | BUG-0001 | Created. Records where the shortfall wording goes and what it must not disturb, after the stakeholder chose at `BUG-0001/Q-001` to keep the backdated spend and stop printing the minus. |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T11:57:12Z | answer-questions | BUG-0001 | provenance | `## Consequences`, first paragraph: *"Both surfaces are the same filtered sum bounded by a month"* cited `[src: envel/summary.py:68]` `[src: envel/summary.py:173]`. The first is unchanged and still `left = sum(...)` [src: envel/summary.py:68]. The second was `def bounded_balance(store, name, within):` when this ADR was written, and `BUG-0001`'s own change — the two rendering helpers this ADR decided — inserted 23 lines above it, so line 173 became `if "description" in entry:`, inside `entry_line()`. That is the **signed transaction figure**, which `## Decision` 4 of this very ADR exists to distinguish from a balance, so the citation resolved to the one line that contradicts the sentence it was supporting. The citation now reads `[src: envel/summary.py:196]` [src: envel/summary.py:196]; the assertion is unchanged, and `verify` measured the identity directly on a month that closed short — `left − (in − spent + moved)` equals `balance_before` at both bounds. Found by `review-close` resolving all 35 `envel/*.py:<line>` citations in `docs/` against the branch head. Answering `BUG-0001/Q-002`. |

# Plan — BUG-0001 A past month's closing figure can show an envelope holding a negative amount

## Problem

A month that has already ended can close short, and the tool prints the shortfall as a minus
number — `groceries holds -250.00 at the end of 2026-08` from `envel entries`, and
`left -250.00` from `envel summary`. That breaks the stakeholder's unqualified rule *"No negative
envelopes anywhere in this tool"* [src: WI-0005/Q-004], which `EP-001` carries as a success
measure [src: EP-001]. It is reachable from the workflow they described rather than from an edge
case: typing last month's shopping in *"a couple of days after the month has ended with the
statement in front of me"* [src: WI-0005/Q-001] dates the spends into last month while the income
that covers them sits in this month, because income carries no date [src: WI-0003/Q-003].

They chose the remedy themselves at `BUG-0001/Q-001`: keep recording the spend, and say the
shortfall in words instead of printing a minus, with the figure still readable so the line adds
up. The constraint that shapes this plan is that **no sum changes** — the arithmetic is what makes
`WI-0003` AC3 reconcile [src: ADR-0008] — so the whole change is in how three lines are rendered,
in `envel/summary.py`, and the signs on transaction figures are deliberately left alone.

## Approach

`ADR-0012` records the decision and why the two alternatives were rejected. In short: two new
rendering helpers in `envel/summary.py`, called from the three places that print a bounded
balance, and nothing else in the module or anywhere else changes.

```python
def balance_line(name, cents, moment, verb, month):
    """Return the sentence bracketing a listing: 'groceries held 0.00 at the start of 2026-08',
    or 'groceries was 250.00 short at the end of 2026-08' when the balance is below zero."""

def left_column(cents):
    """Return a summary row's last column: 'left 60.00', or 'short 250.00' below zero."""
```

`moment` is the literal `"start"` or `"end"`; `verb` is the literal `"held"` or `"holds"` and is
used only when `cents >= 0`, because *was … short* reads the same at either end of the month.
Both helpers render the amount with `money.format_amount`, passing `-cents` in the negative case,
so `envel/money.py` stays the only place an amount becomes text [src: ADR-0001] and keeps its own
minus sign for transaction figures.

## Steps

1. **Add `left_column(cents)` to `envel/summary.py`**, above `row()`. Returns
   `"left {}".format(money.format_amount(cents))` when `cents >= 0` and
   `"short {}".format(money.format_amount(-cents))` when it is negative. Afterwards the function
   exists and nothing calls it yet.

2. **Call it from `row()` in `envel/summary.py`** (currently at lines 72–82). The format string's
   trailing `left {}` becomes a bare `{}` filled by `left_column(left)`; the other three columns
   are unchanged and still come from `money.format_amount`. `figures()` is **not** touched and
   still returns signed cents. Afterwards `envel summary 2026-08` prints
   `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00` for a month that closed short, and
   prints exactly what it prints today for every month that did not.

3. **Add `balance_line(name, cents, moment, verb, month)` to `envel/summary.py`**, above
   `list_entries()`. Returns `"{} {} {} at the {} of {}"` with `money.format_amount(cents)` when
   `cents >= 0`, and `"{} was {} short at the {} of {}"` with `money.format_amount(-cents)` when
   it is negative. Afterwards the function exists and nothing calls it yet.

4. **Call it from `list_entries()` in `envel/summary.py`** (currently the opening line built at
   lines 232–238 and the closing line appended at lines 245–251). The opening line becomes
   `balance_line(stored_name, balance_before(store, stored_name, month), "start", "held", month)`
   and the closing line becomes
   `balance_line(stored_name, balance_through(store, stored_name, month), "end", "holds", month)`.
   The entry lines between them, and the `nothing was recorded against …` line, are unchanged.
   Afterwards `envel entries groceries --month 2026-08` prints
   `groceries was 250.00 short at the end of 2026-08` for a month that closed short, and prints
   exactly what it prints today for every month that did not.

5. **Add tests to `tests/test_entries.py`**, appended as a new test class so that no assertion
   existing at `127664a` is edited. Reproduce the bug's steps 1–4 at the `summary.list_entries`
   level — an envelope created, income added, a spend dated into an earlier month — and assert:
   the closing line is `groceries was 250.00 short at the end of 2026-08`; no line of the result
   contains a token matching `-\d`; the entry line for the spend still carries `-250.00`, which is
   what pins step 4 to the balance lines only. Add the opening-line case too: a month whose
   *previous* month closed short opens `groceries was 250.00 short at the start of 2026-09`.

6. **Add tests to `tests/test_summary.py`**, appended as a new test class for the same reason.
   Reproduce steps 1–4 plus step 7's earlier `created` stamp at the `summary.summarise` level and
   assert the row is `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00`. Assert
   separately that `summary.figures` still returns the signed `left` for the same document, which
   is what proves the arithmetic was not clamped, and that an envelope that only gave money away
   still prints `moved -20.00`.

7. **Run the project's commands**: `python3 -m unittest discover -s tests -t .` and
   `python3 -m compileall -q envel tests`. Afterwards the suite is green with the new tests in it
   and every assertion that existed at `127664a` unmodified.

8. **Close every row of the invalidation set below**, repairing what this change made false and
   recording a verdict for what it did not, per `spec/doc-header.md` §5.

No step changes `envel/money.py`, `envel/cli.py`, `envel/envelopes.py`, `envel/store.py` or
`envel/dates.py`. If a step seems to need one of them, the design is wrong and it is a question
for the architect, not a widening.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — no negative on either balance line of `envel entries` | 3, 4 | the new `tests/test_entries.py` class of step 5: closing line equals `groceries was 250.00 short at the end of 2026-08`, opening-line case equals `groceries was 250.00 short at the start of 2026-09`, and no balance line matches `-\d`. Plus the bug's steps 1–6 run at the command line and the output read. |
| AC2 — no negative in any column of the `envel summary` row | 1, 2 | the new `tests/test_summary.py` class of step 6: the row equals `groceries  in 0.00  spent 250.00  moved 0.00  short 250.00`. Plus the bug's steps 1–4 and 7 run at the command line and the output read. Note the `moved` column is `0.00` in this scenario, so the criterion is decidable as written without reaching transaction signs. |
| AC3 — the input is not refused; step 4 exits 0 and `envel list` shows `groceries  50.00` | none — no step changes the write path | running the bug's step 4 and capturing both streams and the exit code, then `envel list`. The demonstration is that nothing in `envel/envelopes.py` or `envel/cli.py` is in the diff, so no refusal was added. |
| AC4 — a test for AC1 and a test for AC2, both failing at `127664a` and passing after | 5, 6 | `git stash` the `envel/` change and run the two new classes → both fail; restore and run → both pass. The exact commands are `implement`'s to record. |
| AC5 — the four delivered test modules run unmodified | 5, 6, 7 | `git diff 127664a -- tests/` shows only appended classes in `tests/test_entries.py` and `tests/test_summary.py` and no change at all to `tests/test_envelopes.py` or `tests/test_corrections.py`; `python3 -m unittest discover -s tests -t .` exits 0. |
| AC6 — the worded line still reconciles, naming `250.00` rather than `0.00` | 1, 3 | the step 6 assertion that `summary.figures` still returns signed cents for the short month, read together with the step 5 and 6 assertions on the printed magnitude: the printed `250.00` is `abs()` of the figure the arithmetic produced, so opening + entries = closing still holds with *short* read as the minus. A clamp would print `0.00` and fail both. |

## Assumptions

- **The summary's short row reads `short 250.00` in place of `left -250.00`** — the label changes
  rather than a word being appended after the figure. The stakeholder was shown *"the summary's
  last column showing the same thing"* [src: BUG-0001/Q-001] without being shown the exact
  wording, so this is ours. Reversing it is one branch of `left_column()` and its two assertions:
  one file, no data, no stored shape. **Not** under delegation — no answer of theirs licenses a
  category here, and this is recorded as ours rather than written up as though they chose it.
- **The opening line words the negative case as `was … short at the start of`** — by symmetry with
  the closing line they did approve. Reversing it is one branch of `balance_line()` and one
  assertion. Not under delegation, for the same reason.
- **The new tests are appended to the two existing modules rather than put in a new file.**
  `AC5`'s evidence is `git diff 127664a -- tests/` *showing additions only in those files*, which
  a new module would sit outside. Reversing this is moving two classes into a new file, and it
  costs nothing but would have to be argued against AC5 first.

## Decisions and ADRs

- **Where the wording goes, and what it must not disturb** — `ADR-0012`. Three options weighed:
  rendering it in `envel/money.py` so the rule holds tool-wide (rejected — it would reword
  transaction figures and break two assertions AC5 freezes), clamping the balance to `0.00`
  (rejected — fails AC6, which is the stakeholder's own condition), and rendering a balance only,
  in `envel/summary.py` (chosen). Reversibility: easy, and recorded as such in the ADR.
- **Transaction figures keep their signs** — `ADR-0012` §Decision 4, and it is the distinction the
  bug forced into the open: a figure answering *how much does this hold* is worded, a figure
  answering *how much moved and which way* is signed.
- **No sum changes** — `ADR-0012` §Decision 1, following `ADR-0008`: the reconciliation is a
  property of the arithmetic and a clamp would put the code between the two numbers.
- **The current-balance messages are untouched** — `ADR-0012` §Decision 5. Not an assumption: a
  balance as of now cannot be negative, because three refusals already guard it.

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/product/vision.md` | `## What it is for`, the paragraph added at v8: *"`envel entries` and `envel summary` say how short the month closed, in words, rather than printing a negative"* | cited-fact | the sentence is currently false of the delivered code and this change is what makes it true; the wording it describes must be the wording delivered, or it stays false in a new way | verified-still-true |
| `docs/product/vision.md` | `## What it is for`, the paragraph sourced to `WI-0005/Q-004`: *"A correction that would take an envelope below zero is refused and says how short the envelope is"* | cited-fact | it is the nearest sentence in the document to what this change does, and it is about the **current** balance; confirm this change leaves it true rather than assuming it | verified-still-true |
| `docs/product/vision.md` | `## Engagement state`, all four bullets | engagement-state | a sentence about the engagement, not the product; nobody but the ending may write one | owned-by-ending |
| `docs/architecture/overview.md` | `## Conventions this project has adopted`, the bullet *"Amounts are printed with exactly two decimal places and no currency symbol"* | quantified | a universal over every amount the tool prints, and this change adds a new way of printing one; the shortfall must satisfy it or the bullet becomes false | verified-still-true |
| `docs/architecture/overview.md` | `## The parts`, the `envel/money.py` row: *"the only two places text and amounts meet: parse and format"* | quantified | a universal over the places an amount becomes text, and this change adds two functions that produce text containing an amount; true only while both delegate to `money.format_amount` | verified-still-true |
| `docs/architecture/overview.md` | `## The parts`, the `envel/summary.py` row: *"the reports, both of them"* | cited-fact | the module gains two functions and the row describes what it owns | verified-still-true |
| `docs/architecture/overview.md` | `## What is not decided yet` | cited-fact | it said *"Nothing"* and named `WI-0005` as the last design taken; `ADR-0012` is a twelfth. **Already repaired by this execution** rather than left for `implement`: `plan` owns this section and the sentence is false the moment this ADR exists, so `docs/architecture/overview.md` went to v10 in this run and the row is here only so the set names every path this branch touches | to-update |
| `docs/architecture/overview.md` | `## Engagement state` | engagement-state | as above | owned-by-ending |
| `docs/architecture/adr/ADR-0008-a-month-is-a-string-and-every-figure-is-a-filtered-sum.md` | `## Decision` 3's filter table, the `left` row, and `## Consequences` first paragraph | cited-fact | this change is on the printing side of exactly these figures; the ADR must still be true that every figure is a filtered sum and that nothing derives the carried-in figure by subtraction | verified-still-true |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` | `## Consequences`: *"a module that prints an amount without going through"* `money` | quantified | a universal over modules that print amounts, and this change adds two call sites | verified-still-true |
| `docs/architecture/adr/ADR-0009-reporting-lives-in-its-own-module.md` | `## Consequences`: *"`summary` prints nothing and calls no `sys.exit`"* | quantified | the new helpers return strings and must not print; stated so it is confirmed rather than assumed | verified-still-true |
| `docs/architecture/adr/ADR-0011-a-correction-edits-the-entry-in-place.md` | `## Decision` 3, the below-zero refusal on `fix` and `remove` | cited-fact | it is the other half of the no-negative rule and this change must not weaken it | verified-still-true |

Every row was closed by `implement`; none was added, because no document outside this set
appeared in the branch's diff — `git diff main...wi/BUG-0001 --name-only -- docs/` prints nothing.
The audit for each is in `artifacts/impl-report.md` `## Documents`.

Originally:  The set was assembled by reading
the four documents and the standing ADRs, not from recollection; the three seeds used were the
documents these steps cite, the documents describing the behaviour AC1–AC3 name, and every
universal sentence about a printed amount.

## Deliverable documents

`none`. No acceptance criterion of `BUG-0001` is about a document: AC1, AC2, AC3 and AC6 are about
printed output, AC4 and AC5 are about tests. The repairs listed in the invalidation set are
repairs, not deliverables.

## Binding ADRs

- **`ADR-0001` — amounts are integer cents.** Binds: the shortfall's magnitude must be rendered by
  `money.format_amount` and by nothing else, so no new formatting code produces a decimal.
- **`ADR-0002` — the store is a JSON entry log.** Binds: a balance is the plain sum of an
  envelope's entries with no branch on `kind`. Nothing in this change may store, cache or clamp a
  figure.
- **`ADR-0008` — a month is a string and every figure is a filtered sum.** Binds most tightly:
  `figures()`, `bounded_balance()`, `balance_before()` and `balance_through()` keep returning
  signed cents, so `WI-0003` AC3's reconciliation stays a property of the arithmetic.
- **`ADR-0009` — reporting lives in its own module.** Binds: the helpers go in `envel/summary.py`,
  return strings, and print nothing and exit nothing.
- **`ADR-0012` — a balance is never printed with a minus sign.** Binds: this change's own
  decision, including which figures are worded and which keep their signs.

`ADR-0003` through `ADR-0007`, `ADR-0010` and `ADR-0011` were read and none constrains this change:
they settle the file's location, the invocation shim, stdlib-only checks, a spend's date, a move's
two entries, an entry's reference and what a correction does — and no step here touches any of
those. `ADR-0011` appears in the invalidation set because its below-zero refusal is the neighbouring
rule, not because it constrains the design.

## Scaffolding

`none`. Both of `tracker/project.yaml`'s commands already run in this project and were run this
execution; no file was created outside `tracker/` and `docs/`.

## Risks

- **The wording is now behaviour.** *"was 250.00 short"* and *"short 250.00"* become asserted
  output, and the stakeholder approved only the first of the two. If the summary's wording is
  wrong for them, it is a one-branch change and a new assertion — but it will only be found at
  the ending, because nothing between here and there puts printed prose in front of them.
- **The rule is true of three call sites, not of the tool.** A future report that prints a
  bounded balance without calling `balance_line` or `left_column` reintroduces the bug and no
  check would catch it. `ADR-0012` names the obligation; nothing enforces it.
- **A month whose spends are corrected after the fact can still cross zero in the other
  direction** — a shortfall that a later correction removes. Nothing here caches, so the line is
  recomputed and the wording follows; the risk is only that a test written against a fixed
  document would not notice. Step 6 asserts `figures()` directly for this reason.
- **`AC4` requires the new tests to fail at `127664a`.** If a test is written against the helper
  functions rather than against `row()` and `list_entries()`, it will fail at `127664a` with an
  `AttributeError` rather than an assertion — which is still a failure, but a weak one. Step 5 and
  step 6 are written against the two entry points for that reason.

## Out of scope for this item

- **Giving income a date.** Declined by the stakeholder at [src: WI-0003/Q-003] and again at
  [src: WI-0005/Q-006], and refused a third time as option D of [src: BUG-0001/Q-001]. It is the
  root of the asymmetry and it is not ours to revisit.
- **Refusing a backdated spend that takes a past month below zero.** Refused as option B of
  [src: BUG-0001/Q-001].
- **The sign on a transaction figure** — a spend's own line, the side a move left, and the
  summary's `moved` column. `ADR-0012` §Decision 4, and `BUG-0001` AC5 freezes the two assertions
  that pin it [src: tests/test_entries.py:173] [src: tests/test_entries.py:310].
- **`envel list` and the *"which now holds …"* clauses.** A balance as of now cannot be negative;
  `ADR-0012` §Decision 5.
- **The neighbouring finding that a spend dated before its envelope existed appears in no summary
  row at all.** Recorded in `EP-001`'s `artifacts/review.md` under `## Findings`; it is a question
  about `WI-0003` AC7 and not this bug.

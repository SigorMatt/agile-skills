---
id: BUG-0001
type: bug
title: A past month's closing figure can show an envelope holding a negative amount
status: done
priority: high
epic: EP-001
created: "2026-09-11T10:52:56Z"
updated: "2026-09-11T11:54:58Z"
found-in: WI-0003
arose-from: EP-001
branch: wi/BUG-0001
outcome: delivered
merge-commit: b5fd4333ac469efd7ad2962e35300b8c0fd6aa6d
---

## Summary

`envel entries <name> --month <past month>` and `envel summary <past month>` can both print a
negative amount against an envelope. The stakeholder's rule is that they never do —
*"No negative envelopes anywhere in this tool, and that includes here … seeing a minus number is
not [fine]"* [src: WI-0005/Q-004] — and `EP-001`'s success measures carry it as *"No envelope
ever shows a negative amount"* [src: EP-001].

The current balance is never negative: the overspend refusal [src: WI-0002 AC5 "The listing never
shows a negative amount for any envelope"] and the below-zero refusals on `fix` and `remove`
[src: WI-0005 AC9 "below zero"] all guard it, and `envel list` is correct. What is unguarded is a
**month-end** balance. `left` in a summary row, and the opening and closing lines of a listing,
are the same filtered sum bounded by a month [src: envel/summary.py:68]
[src: envel/summary.py:173], and nothing bounds *that* sum below zero. A spend dated into an
earlier month with `--on` moves money out of the earlier month while the income that covers it
stays in the month it was typed in — income carries no date of its own and cannot be backdated
[src: WI-0003/Q-003] — so the earlier month closes short.

It is reachable from the workflow the stakeholder described rather than from an edge case. They
said they sit down to this *"a couple of days after the month has ended with the statement in
front of me"* [src: WI-0005/Q-001], which is exactly the act of dating last month's spends into
last month after this month's income has been recorded.

No single item's acceptance criteria were broken. Each of the guards above says *the listing*, or
*this operation*, and each holds. The sentence that is false is the stakeholder's own unqualified
one, which no item carries, which is why this was found at the epic's Definition of Done walk
(DE3) and not at a close.

## Steps to reproduce

The current month is `2026-09` when these steps are written. In a later month, read `2026-08` as
*any month before the one you run them in* and `2026-09` as *the month you run them in*.

1. `export ENVEL_FILE=/tmp/bug1/store.json` — and `mkdir -p /tmp/bug1` — so nothing touches a
   real store.
2. `python3 -m envel new groceries`
3. `python3 -m envel add groceries 300.00`
4. `python3 -m envel spend groceries 250.00 "august shop" --on 2026-08-14` — last month's shop,
   entered now with the statement in front of you.
5. `python3 -m envel list` — the current balance, which is correct and is not what this bug is
   about.
6. `python3 -m envel entries groceries --month 2026-08` — **the first surface.**
7. For the second surface, the envelope has to have existed in the month being summarised, and
   the tool stamps `created` itself, so that part is probed on the store file rather than through
   the command line: set `envelopes[0].created` to `"2026-08-01T09:00:00Z"` in
   `/tmp/bug1/store.json`, then run `python3 -m envel summary 2026-08`. Without step 7 the same
   command prints `no envelopes existed in 2026-08`, because a row is only printed for an
   envelope that existed by the end of the month [src: WI-0003 AC7 "existed by the end of"] —
   which is why the summary surface needs the probe and the listing surface does not.

## Expected behaviour

No amount printed against an envelope is less than zero, on any command, in any month. The
stakeholder stated it without qualification, twice: *"I don't want to see a negative envelope"*
[src: EP-001/Q-002] and *"No negative envelopes anywhere in this tool, and that includes here"*
[src: WI-0005/Q-004]. `EP-001`'s `## Success measures` records it as a measure of the engagement
[src: EP-001], and `docs/product/vision.md` records
the reason they wanted it
[src: docs/product/vision.md].

What the tool should do **instead** was put to the stakeholder at `Q-001` and is now decided
[src: BUG-0001/Q-001]. The spend is still recorded, exactly as it is today; what changes is how a
month that closed short is printed. The closing and opening lines of `envel entries`, and the
`left` column of an `envel summary` row, say how short the envelope was in words and carry the
figure unsigned — the shape they were shown was *"groceries was 250.00 short at the end of
2026-08"* in place of *"holds -250.00"*. The figure has to stay readable as a number, because that
is the condition they put on it: *"a figure I can read is what the adding-up rule was about; a
minus sign in front of it is what I don't want"* [src: BUG-0001/Q-001]. Clamping the figure to
`0.00` is therefore not open; nor is refusing the backdated spend, nor giving income a date — see
`## Notes`.

The entry lines between the two balance lines are **not** in scope. A spend prints as `-250.00`
there, and a move out as `-30.00`, because the sign says which way the money went rather than what
the envelope holds. That line was printed verbatim in `Q-001`'s context and the option the
stakeholder chose left it alone [src: BUG-0001/Q-001].

## Actual behaviour

Step 6, verbatim, exit 0:

```
$ python3 -m envel entries groceries --month 2026-08
groceries held 0.00 at the start of 2026-08
2  2026-08-14  spend  groceries  -250.00  august shop
groceries holds -250.00 at the end of 2026-08
```

Step 7, verbatim, exit 0:

```
$ python3 -m envel summary 2026-08
groceries  in 0.00  spent 250.00  moved 0.00  left -250.00
```

Step 5, for contrast — the current balance is right and stays right, exit 0:

```
$ python3 -m envel list
groceries  50.00
```

## Acceptance criteria

- [x] AC1 — After steps 1–4, `python3 -m envel entries groceries --month 2026-08` prints no
      amount less than zero on either of its **balance** lines — the opening line giving what the
      envelope held at the start of the month and the closing line giving what it holds at the end
      of it. A month that closed short says so in words on that line, naming the envelope and the
      amount it was short, and the amount is written unsigned in the project's two-decimal form
      [src: WI-0003 AC11 "Every figure the summary prints is a plain decimal with exactly two
      decimal places"]. The entry lines between them are out of scope and keep their signs, per
      `## Expected behaviour`. Decided by running the command and reading its output.
      This criterion was amended after it was written: it said *"on any of its lines — opening,
      entry or closing"*, which reached the entry lines too and contradicted AC5. The amendment is
      recorded at `questions/Q-001.md` `## Consequences` with the stakeholder's answer as its
      basis.
- [x] AC2 — After steps 1–4 and the store-file probe of step 7,
      `python3 -m envel summary 2026-08` prints no amount less than zero in any column of the
      `groceries` row. The `left` column of a month that closed short says so in words and carries
      the amount unsigned, the same way AC1's closing line does [src: BUG-0001/Q-001]. Decided by
      running the command and reading its output.
- [x] AC3 — The input is **not** refused. Step 4 exits 0, prints nothing on stderr, and records
      the spend: after it, `python3 -m envel list` prints `groceries  50.00`. The stakeholder chose
      this over refusing — *"B refuses to record a shop that actually happened, which is no use to
      me"* [src: BUG-0001/Q-001] — so AC1 and AC2 carry the whole remedy. Decided by running step 4,
      capturing both streams and the exit code, and running `envel list` after it.
      This criterion was amended after it was written: it offered a refusing branch and a
      non-refusing branch, and `Q-001` settled which. The amendment is recorded at
      `questions/Q-001.md` `## Consequences`.
- [x] AC4 — A test in `tests/` reproduces steps 1–4 and asserts AC1, and a second asserts AC2.
      Both fail against the code as it stands at the commit this bug was filed on, `127664a`, and
      pass after the fix. Decided by running the new tests at `127664a` with the fix reverted and
      again at the fix.
- [x] AC5 — The guards that already hold still hold, and the tests that state them pass
      unmodified: `tests/test_envelopes.py`, `tests/test_summary.py`, `tests/test_entries.py`
      and `tests/test_corrections.py` run under
      `python3 -m unittest discover -s tests -t .` with no edit to any assertion that exists at
      `127664a`. Decided by `git diff 127664a -- tests/` showing additions only in those files,
      and by the suite exiting 0.
- [x] AC6 — The worded closing line still reconciles: the amount it names, read as a shortfall,
      is the amount the opening line plus the entry lines between them add up to. For steps 1–4
      that is `0.00 + (-250.00) = -250.00`, and the closing line must name `250.00` as the
      shortfall — not `0.00`, which is what clamping the figure would print. The same applies to
      the `left` column of AC2's row against the other three columns of it. This is the condition
      the stakeholder attached to their answer — *"still gives me the figure, and a figure I can
      read is what the adding-up rule was about"* [src: BUG-0001/Q-001] — and it is what keeps
      [src: WI-0003 AC3 "The figures reconcile"] and
      [src: WI-0006 AC9 "the figures reconcile"] true without either being amended. Decided by
      running the two commands of AC1 and AC2 and doing the arithmetic on what they print.

## Out of scope

- Changing what `envel list` prints, or any of the three refusals that already guard the current
  balance. They are correct and AC5 keeps them that way.
- Giving income a date. The stakeholder declined it twice [src: WI-0003/Q-003]
  [src: WI-0005/Q-006], and a fix that reaches for it is proposing a decision they have already
  taken, not fixing a defect.
- The neighbouring observation that a spend dated into a month **before** its envelope existed
  appears in no summary row at all, being excluded from the earlier month by
  [src: WI-0003 AC7 "existed by the end of"] and from the later one by its own date. That is a
  second, separate question about `WI-0003` AC7 and it is not this bug; it is recorded in
  `EP-001`'s `artifacts/review.md` under `## Findings` so it is not lost.

## Notes

- **The remedy was the stakeholder's call and they have made it** [src: BUG-0001/Q-001]. Four
  options were put to them and they chose to keep recording the spend and say the shortfall in
  words. The three they refused are recorded here because each of them is a thing a designer might
  otherwise reach for:
  - *Refuse the backdated spend.* Refused: *"B refuses to record a shop that actually happened,
    which is no use to me."* There is no money to move *into last month* either — income cannot be
    backdated [src: WI-0003/Q-003] — so a refusal would have had no second step.
  - *Give income a date, so the month closes level.* Refused: *"D is dating income, which I have
    now turned down twice and am not revisiting"*, the two earlier refusals being
    [src: WI-0003/Q-003] and [src: WI-0005/Q-006]. It remains out of scope, as `## Out of scope`
    already said.
  - *Qualify the rule so it covers only the current balance.* Refused: *"I said no minus numbers
    without qualification and I meant it."* `EP-001`'s success measure is therefore unchanged.
  - *Clamp the shortfall to `0.00`* is not one of the four and is not open either: it would satisfy
    AC1 and AC2 and fail AC6, because the line would no longer add up.
- **Neither `WI-0003` AC3 nor `WI-0006` AC9 is amended, and neither item reopens.** Option C was
  put to the stakeholder with the warning that both would need amending by a follow-up item, and
  their reply removed the need: *"a figure I can read is what the adding-up rule was about; a minus
  sign in front of it is what I don't want."* A worded shortfall carrying its figure still
  reconciles, and AC6 above is what holds this item to that.
- Both surfaces are the same expression bounded by a month, so a fix in one place is likely to
  reach both: `summary.figures`' `left` [src: envel/summary.py:68] and
  `summary.bounded_balance` [src: envel/summary.py:173].
- Found by `review-close` at `EP-001`'s DE3 walk on 2026-09-11, against `main` at `127664a`,
  with the suite green at 299 tests [src: run: python3 -m unittest discover -s tests -t . → exit 0, 299 tests].

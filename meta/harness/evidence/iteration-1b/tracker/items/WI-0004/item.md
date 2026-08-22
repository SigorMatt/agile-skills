---
id: WI-0004
type: work-item
title: Record a settlement payment and net it off the balances
status: done
priority: high
epic: EP-001
branch: wi/WI-0004
outcome: delivered
created: "2026-08-21T18:54:29Z"
updated: "2026-08-21T20:35:22Z"
depends-on:
  - WI-0003
---

## Story

As a member of the group who has just handed money to someone I owed, I want to record that
payment, so that the tool stops reporting a debt that has already been paid and its numbers keep
meaning something after the first time we settle up.

## Acceptance criteria

The two subcommands are fixed by ADR-0006. Their arguments are pinned here:

```
python3 -m expenses add-payment <amount> --from <name> --to <name>
python3 -m expenses payments
```

Both flags are required and each may be given at most once. The amount obeys ADR-0003: at most
two decimal places, so `10`, `10.0` and `10.00` are the same thing.

**What a payment means for the arithmetic:** a payment of `A` from `X` to `Y` moves `A` from what
`X` owes to what `Y` owes — `X`'s net position rises by `A` and `Y`'s falls by `A`. Net positions
are otherwise exactly as WI-0003 defines them, and `who-owes-whom` is unchanged apart from now
including payments.

"Exits non-zero" means, throughout: a message on standard error, an exit status other than `0`,
nothing added to the record, and no Python traceback — standard error contains no line matching
`Traceback (most recent call last)`.

Every criterion below assumes `Alice`, `Bob`, `Carol` and `Sam Okafor` have been added with
`add-person`, and starts from a record with no expenses and no payments unless it says otherwise.

- [x] AC1 — `python3 -m expenses add-payment 10 --from Bob --to Alice` prints
  `Recorded 10.00 paid by Bob to Alice.` on standard output and exits `0`.
- [x] AC2 — Persistence: with the payment above recorded by one invocation, a separate, later
  invocation of `python3 -m expenses payments` lists it. Nothing is re-entered.
- [x] AC3 — `python3 -m expenses payments` prints one line per payment, in the order they were
  recorded, numbered from `1`, and exits `0`. After AC1 the single line is exactly:
  `1. Bob paid Alice 10.00`. Every amount carries exactly two decimal places (ADR-0003 point 2)
  and every person is shown with the spelling first entered for them (ADR-0005 point 4).
- [x] AC4 — `python3 -m expenses payments` with nothing recorded prints exactly
  `No payments have been recorded yet.` on standard output and exits `0` (ADR-0006 rule 2).
- [x] AC5 — A payment reduces what its payer owes. After
  `add-expense 30 --paid-by Alice --shared-by Alice,Bob,Carol` — where `who-owes-whom` prints
  `Bob pays Alice 10.00` and `Carol pays Alice 10.00` — recording
  `add-payment 10 --from Bob --to Alice` makes `who-owes-whom` print exactly
  `Carol pays Alice 10.00` and nothing else.
- [x] AC6 — A part payment reduces the debt by what was paid. From the same starting record,
  `add-payment 4 --from Bob --to Alice` instead makes `who-owes-whom` print exactly:
  ```
  Carol pays Alice 10.00
  Bob pays Alice 6.00
  ```
  Carol comes first because her debt is now the larger.
- [x] AC7 — When the payments cover every debt, `who-owes-whom` produces the same settled outcome
  as when nothing has been recorded at all. From AC5's record, recording
  `add-payment 10 --from Carol --to Alice` as well makes `who-owes-whom` print exactly
  `Everybody is settled up.` and exit `0`.
- [x] AC8 — Overpaying is accepted and reverses the direction. From AC5's starting record,
  `add-payment 30 --from Bob --to Alice` — three times what Bob owed — is recorded, exits `0`, and
  `who-owes-whom` then prints exactly:
  ```
  Alice pays Bob 10.00
  Carol pays Bob 10.00
  ```
  Alice comes first because the two debts are equal and `alice` sorts before `carol`.
  The tool records what actually happened rather than refusing it (EP-001 `Q-001`: the human chose
  recorded payments over a reset).
- [x] AC9 — A person who is not in the group is refused, and identity keys decide membership
  (ADR-0005 point 5):
  - `add-payment 10 --from Dave --to Alice` prints `Dave is not in the group.` on standard error
    and exits non-zero; `payments` afterwards prints the empty-list message and `people` does not
    list `Dave`;
  - `add-payment 10 --from "sam okafor" --to Alice` **succeeds**, and `payments` shows the payer
    as `Sam Okafor`.
- [x] AC10 — A payment must be between two different people:
  `add-payment 10 --from Alice --to Alice` and `add-payment 10 --from "ALICE" --to Alice` each
  print `A payment must be between two different people.` on standard error and exit non-zero.
  Sameness is the identity key, not the spelling.
- [x] AC11 — A malformed or out-of-range amount is refused, and nothing is recorded:
  - `add-payment ten --from Bob --to Alice` → `ten is not an amount.`;
  - `add-payment 10.005 --from Bob --to Alice` →
    `Amounts have at most two decimal places: 10.005.`;
  - `add-payment 0 --from Bob --to Alice` and `add-payment -5 --from Bob --to Alice` →
    `A payment must be for more than zero.`
- [x] AC12 — The command line itself is checked, and each failure exits non-zero with a message on
  standard error:
  - `add-payment --from Bob --to Alice` — no amount — → `add-payment needs an amount.`;
  - `add-payment 10 --to Alice` → `add-payment needs --from.`;
  - `add-payment 10 --from Bob` → `add-payment needs --to.`;
  - `add-payment 10 --from Bob --from Carol --to Alice` → `--from was given more than once.`;
  - `add-payment 10 --from Bob --to Alice --for dinner` → `Unknown option: --for.`;
  - `payments extra` → `payments takes no arguments.` (ADR-0006 rule 2).
- [x] AC13 — Every refusal in AC9 to AC12 records nothing and creates nothing: after any of them,
  `payments` and `expenses` print exactly what they printed before, `people` is unchanged, and
  standard error carries no `Traceback (most recent call last)`. **On a record where no file
  exists yet, a refused `add-payment` leaves no file behind** — checked by looking for the path in
  `EXPENSES_FILE`.
- [x] AC14 — Recording a payment does not disturb what WI-0001 and WI-0002 recorded: after AC5,
  `people` still prints `Alice`, `Bob`, `Carol` and `Sam Okafor` in the order they were added, and
  `expenses` still prints the expense with its shares unchanged.
- [x] AC15 — A payment between two people who share no expense is accepted: with no expenses at
  all, `add-payment 10 --from Bob --to Alice` exits `0`, and `who-owes-whom` then prints exactly
  `Alice pays Bob 10.00` — Bob has paid money he did not owe, so the group owes it back to him.

## Out of scope

- Deleting or amending a payment once recorded. EP-001 `## Out of scope` excludes corrections for
  expenses on the same grounds, and a payment is the same kind of fact. A payment entered wrongly
  is corrected by recording the opposite payment, which AC8 and AC15 show is possible.
- Any "settle everybody at once" or "reset to zero" action. The human chose recordable payments
  (EP-001 `Q-001`, option B) over a reset; a group squaring up all at once records the payments
  they actually made.
- **Refusing an overpayment, or warning about one.** AC8 accepts it deliberately. A tool that
  refused would be refusing to record something that really happened.
- Reminding, chasing, or notifying anyone that a payment is due.
- Deciding *which* payments to make — that is WI-0003's output, which this item consumes.
- What a payment was *for*: no description, label, date or note, for the same reason an expense
  has none (`docs/product/prd.md` v2 § *The facts the tool holds*, item 4: "Nothing else").

## Notes

### What was decided, and by whom

This item exists because of the human's answer to `EP-001/Q-001`: "being able to mark that
someone's paid up matters. Otherwise the numbers just keep racking up forever and stop meaning
anything." It was created by `answer-questions` running `intake`'s creation procedure, after the
epic had already been broken down.

**ADR-0001** fixes the invocation, exit-code and stream contract; **ADR-0003** fixes amounts as
whole minor units with at most two decimal places on entry and exactly two on display;
**ADR-0005** fixes who a named person is; **ADR-0006** fixes these two subcommand names;
**ADR-0004** fixes what `who-owes-whom` prints, and AC5 to AC8 and AC15 are that same calculation
with payments included.

### Inherited from two earlier reviews, and pinned here

Three things were handed to this item by name. Two of them are not acceptance criteria, because
they are not observable from outside the tool; they are instructions to `plan`, recorded here so
they are not lost:

1. **"A refusal creates no record file" was pinned for `add-person` and not for `add-expense`**
   (WI-0002 `## Notes` 3, from its review). It is now an acceptance criterion for `add-payment`:
   the last clause of AC13. `verify` found that two mutations survived on WI-0002 precisely
   because nothing asserted it there.
2. **`group.net_positions`' ordering is a contract nothing asserts** (WI-0003 `## Notes` 2).
   `plan.md` § *Assumptions* 1 on WI-0003 states that it returns everybody in the order they were
   added; sorting the result by amount passes the whole suite. **This item extends that function**,
   so `plan` should have it asserted by a unit test. It is not a criterion here because the order
   is not observable through any command.
3. **WI-0003's purity test for `who-owes-whom` uses a record with one expense** (WI-0003
   `## Notes` 3), so a rewrite that merely reorders would pass it. **`plan` should use a
   multi-expense, multi-payment record** for the equivalent assertion on this item. Also not a
   criterion, for the same reason.

### Assumptions this refinement made without the human

The human answers asynchronously and was not present. Nothing here needed them: the scope decision
is theirs and already recorded, and what remained was syntax and wording, which they have twice
declined to be asked about (`WI-0001/Q-001` and `Q-003`). Each is `[assumed]` in
`artifacts/refinement-qa.md` and none was confirmed by them:

1. **`add-payment <amount> --from <name> --to <name>`**, mirroring `add-expense`'s positional
   amount. `--from` and `--to` rather than `--paid-by` and `--paid-to`, because a payment has a
   direction and those are the words for it.
2. **The exact wording of every message**, and the listing line `1. Bob paid Alice 10.00` — past
   tense, where `who-owes-whom` says `pays`, because one records what happened and the other
   proposes what to do.
3. **A self-payment is refused** (AC10). It records nothing and is almost certainly a typo for a
   real payment; accepting it would leave a line in `payments` that no arithmetic can see.
4. **An overpayment is accepted** (AC8). This one is closest to being a question for the human,
   and it is not asked because their answer to `EP-001/Q-001` already contains the principle: the
   tool records the payments the group actually made. Refusing would mean the tool declining to
   record a thing that happened.

### Left deliberately unconstrained (R10)

- **The stored shape of a payment.** `ADR-0009` fixes an expense's shape and `ADR-0007` point 2
  makes adding a `payments` key free; the exact JSON of one payment is `plan`'s to choose and
  should be a short ADR, since it is data.
- **Whether `payments` and `expenses` share a listing helper.** A code question with no observable
  consequence. Left so by `refine`.

### Accepted gaps, recorded at close (review-close, 2026-08-21)

Delivered as `delivered`. `artifacts/review.md` carries the Definition of Done table, the epic's
four success measures run end to end, and three findings; these are the gaps it accepted:

1. **The `payments` shape check is required by `ADR-0011` point 5 and `plan.md` step 1, is
   correctly implemented, and is asserted by no test.** Deleting it passes all 115 tests. `verify`
   probed the behaviour by hand — a non-list, a string amount, a missing field, a bad nesting —
   and each was refused correctly with the file left untouched. This is the **third** gap of the
   same shape in this epic, and the pattern is worth more than the instance: *a plan step or an
   ADR clause with no acceptance criterion behind it is not checked by anything.*
2. **A payment recorded twice is indistinguishable from two real payments**, because nothing links
   a payment to the debt it discharges (`ADR-0011` § *Consequences*).
3. **A hand-edited record naming somebody outside the group in a payment prints that name.** Same
   as for expenses; the tool cannot write such a record itself.
4. **`EP-001`'s `## Out of scope` says "free-text expense history beyond a description"**, which
   reads as though an expense may carry a description. None does, and `docs/product/prd.md` (v2)
   is explicit that it may not. The product is coherent and the PRD governs, but the epic's own
   wording points the other way — the one place the record contradicts itself, and probably the
   first thing the group will ask for.
5. **`lint-clean` is a syntax check, not a linter** (`ADR-0008`): about 700 lines of Python
   shipped across this epic with review as the only style check.


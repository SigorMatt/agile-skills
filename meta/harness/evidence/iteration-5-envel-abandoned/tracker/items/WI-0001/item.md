---
id: WI-0001
type: work-item
title: Create and list named envelopes that survive between runs
status: done
priority: critical
epic: EP-001
created: "2026-09-10T13:14:46Z"
updated: "2026-09-10T14:56:33Z"
branch: wi/WI-0001
outcome: delivered
merge-commit: bab15095aea872983937c667a174d3028caf7063
---

## Story

As someone who budgets by dividing money into named pots, I want to set up my envelopes by name
and list them back, so that the set of pots I budget into exists in the tool before I start
putting money anywhere.

## Acceptance criteria

- [x] AC1 — `envel new groceries` exits 0 and writes nothing to stderr
- [x] AC2 — after AC1, `envel list` writes a line whose only content is `groceries` to stdout, and
      exits 0. **[superseded: `WI-0002/Q-001` — an `envel list` line now carries the envelope's balance as well as its name; see `## Notes`]**
- [x] AC3 — `envel new a`, then `envel new b`, then `envel list`, each a separate invocation of the
      process with no other step in between: the third writes a line `a` and a line `b` to stdout
      and exits 0. **[superseded: `WI-0002/Q-001` — an `envel list` line now carries the envelope's balance as well as its name; see `## Notes`]**
- [x] AC4 — `envel list` writes its envelope lines sorted by name, ascending, byte-wise; running it
      twice in a row produces byte-identical stdout
- [x] AC5 — `envel new groceries` run a second time exits non-zero, writes a message to stderr
      containing `groceries`, and a following `envel list` writes the line `groceries` once and
      only once. The same holds when the second invocation differs only in case — `envel new
      Groceries` after `envel new groceries` exits non-zero, writes a message to stderr containing
      `groceries`, and leaves `envel list` writing the line `groceries` once and only once
      (`WI-0001/Q-002`). **[superseded: `WI-0002/Q-001` — an `envel list` line now carries the envelope's balance as well as its name; see `## Notes`]**
- [x] AC6 — `envel list` run before any envelope has ever been created exits 0, writes at least
      one line to stdout, and writes nothing to stderr. Its stdout is the reference output that
      AC9 and AC10 compare against; what the line says is `plan`'s to word
- [x] AC7 — an envelope is listed back with the capitalisation it was created with: `envel new
      Groceries` on an empty store, then `envel list`, writes a line whose only content is
      `Groceries` (`WI-0001/Q-002`). **[superseded: `WI-0002/Q-001` — an `envel list` line now carries the envelope's balance as well as its name; see `## Notes`]**
- [x] AC8 — a name containing a space is accepted: `envel new "eating out"` exits 0, and a
      following `envel list` writes a line whose only content is `eating out` (`WI-0001/Q-002`). **[superseded: `WI-0002/Q-001` — an `envel list` line now carries the envelope's balance as well as its name; see `## Notes`]**
- [x] AC9 — `envel new ""` exits non-zero and writes at least one line to stderr, and a
      following `envel list` writes stdout byte-identical to the AC6 reference output
      (`WI-0001/Q-002`)
- [x] AC10 — `envel new "   "`, a name of spaces only, exits non-zero and writes at least one
      line to stderr, and a following `envel list` writes stdout byte-identical to the AC6
      reference output (`WI-0001/Q-002`)
- [x] AC11 — a name is compared and stored with leading and trailing whitespace removed:
      `envel new groceries`, then `envel new "  groceries  "`, exits non-zero on the second with
      a message on stderr containing `groceries`, and a following `envel list` writes the line
      `groceries` once and only once, with no leading or trailing space on that line. **[superseded: `WI-0002/Q-001` — an `envel list` line now carries the envelope's balance as well as its name; see `## Notes`]**

## Out of scope

- Any notion of money: balances, income and spending are WI-0002.
- Renaming, deleting or archiving an envelope.
- Creating more than one envelope in a single invocation.
- Any option, flag or switch on `new` or `list`. In this item both take a name or nothing, and
  nothing else; an option is a later item.
- Grouping, nesting or categorising envelopes.
- Choosing where the data is stored from the command line. Where it lives is `plan`'s to decide
  (see `## Notes`); making it configurable is not in this item.

## Notes

**Answered by the stakeholder, and written into the criteria above:**

- `WI-0001/Q-001` — the command name is `envel`, option A. "`envel` is fine — keep it. It's short
  and I'll be typing it several times a day; I'm not going to spend a round renaming things." No
  criterion changed, here or on WI-0002 and WI-0003: they already said `envel`, and what changed
  is that the word is now the stakeholder's choice rather than a project-directory accident.
- `WI-0001/Q-002` — option B. Two names are the same envelope when they differ only in case, and
  an envelope is listed back with the capitalisation it was created with; spaces are allowed and
  the characters are otherwise unrestricted; an empty or all-whitespace name is refused. "I'd
  rather be told it already exists than end up with two. I want spaces — 'eating out' is one of
  mine — so don't restrict the characters." AC5 now fires on a case difference, and AC7–AC10 are
  the criteria that could not be written before this answer landed.

**Open design questions, routed to `plan` and not to the stakeholder.** The answer to each would
be the same whoever the stakeholder was.

- **Where the store lives, and whether its location can be overridden.** AC6, AC9 and AC10 all
  begin "before any envelope has ever been created", and AC3 requires three separate processes to
  share a store. Neither is observable unless whoever runs them can reach a clean store without
  destroying a real one — so the location has to be overridable by the environment, or relative to
  the working directory, or otherwise reachable from a test. `plan` decides which; this item only
  records that the criteria are unobservable without one of them.
- **What happens to a name containing a character that would break the store's own format.** The
  stakeholder forbade restricting the characters a name may contain (`WI-0001/Q-002`), so this is
  a constraint on `plan`'s choice of format — the format must survive any name — rather than a
  rule about names. It is not a criterion here because there is no observable behaviour to state:
  the requirement is that nothing breaks.
- **The exact wording of the messages in AC5, AC6, AC9, AC10 and AC11.** The criteria constrain
  the stream, the exit status and, where it matters, that `groceries` appears. They deliberately
  do not fix the sentence.

**Decided here, and by whom:**

- **AC4's ordering** — sorted by name, ascending, byte-wise — was not asked of anyone, and
  nothing licensed it. It was chosen because AC2, AC3 and AC5 are otherwise not decidable: with
  the order unstated, "writes a line `a` and a line `b`" cannot be checked against a fixed output.
  It is the one criterion on this item that the stakeholder has neither stated nor confirmed. If
  they want creation order or any other order, that is a change to AC4 and it lands on this item
  as a send-back to `refine`, not on `plan` or `implement`.
- **AC5's refusal of a duplicate name is no longer an assumption.** Refinement round 1 chose it
  under no licence; the stakeholder then answered `WI-0001/Q-002` with "I'd rather be told it
  already exists than end up with two", which is that behaviour in their own words. It is now
  recorded as theirs in `artifacts/refinement-qa.md`.
- **AC11's whitespace trimming** was not asked of anyone and nothing licensed it. It follows the
  principle they did state in `WI-0001/Q-002` — being told an envelope already exists is better
  than ending up with two — applied to a difference they did not mention. It is written as a
  criterion rather than left silent so that a disagreement is visible; if they want `  groceries  `
  to be a second envelope, that is a change to AC11 and lands as a send-back to `refine`.

**Answered by the architect, during implementation:**

- `WI-0001/Q-003` — the `claims-are-sourced` gate refuses this item's move to `verifying` over an
  unsourced absolute inside `docs/product/vision.md`'s `## Engagement state` section. No
  acceptance criterion changed. The finding is outside the rule the gate implements —
  `spec/dor-dod.md` D12 puts engagement-state sentences out of scope — and the repair belongs to
  `review-close` at the engagement's ending. `implement` records the gate as failed with the run's
  own output and forces the move, under the convention now written in
  `docs/process/ways-of-working.md`.

**Answered by the architect, after this item closed:**

- `WI-0001/Q-004` — the two test-coverage gaps `review-close` accepted are carried by `BUG-0001`,
  whose `## Notes` now name them as steps its plan must take: a unit test pinning `store_path`'s
  XDG and home branches with a fake `environ`, and an end-to-end case creating an envelope from a
  name with surrounding whitespace. Not a new item and not a limitation. No acceptance criterion
  changed — this item is `done` and its criteria are frozen — and `artifacts/review.md` is left as
  it was written, its two gap rows still disposed `question-filed:WI-0001/Q-004`. The convention
  behind the choice is in `docs/process/ways-of-working.md`.

**The stakeholder changed what `envel list` must print, after this item closed:**

- `WI-0002/Q-001` — asked whether the balance of each envelope should appear on the existing
  `envel list` line or on a second command, and answered **A**, in their own words: "`envel list`
  shows the balances. The number is the whole reason I open the tool; I'm not going to type a
  second command to see it. Change the criteria on the earlier item, that's fine by me — I'm
  asking for it. I don't need a flag to hide the balances."
- **Six of this item's criteria are marked `superseded` above**, and they are the six whose
  subject is what a line of `envel list` *contains*: AC2, AC3, AC5, AC7, AC8 and AC11. Each says,
  in one form or another, that a line's only content is an envelope's name, and from `WI-0002`
  onward a line carries the name and that envelope's balance. The requirement they state has been
  replaced; the observation each records was genuinely made, at this item's verification and
  review, and that is why the box stays ticked and the text is left as it was written.
- **Five are not superseded, and it is worth saying which and why**, because the question that
  asked this named "two of its acceptance criteria" and the true count is six. AC1 constrains
  `envel new`, not `list`. AC4 constrains the *order* of the lines and their byte-stability
  across two runs, and a balance column changes neither. AC6, AC9 and AC10 are all about the
  output of `envel list` on a store with no envelopes in it, where there is no envelope line to
  carry a balance.
- **This item was not re-opened and its criteria were not rewritten.** `answer-questions` may
  amend a criterion when it propagates an answer (`spec/work-item.md` §2), and rewriting these six
  would have left a `done` item asserting behaviour that nothing in its own record ever observed —
  the ticked box would then be a claim about the new text rather than about the old. The new
  requirement is stated where it will actually be built and checked, as criteria on `WI-0002`, and
  `WI-0002`'s own AC12 gives each of this item's eleven criteria a verdict when that item is
  verified.

**R10 — combinations:** this item introduces exactly two behaviours, `new <name>` and `list`, and
neither takes an option (see `## Out of scope`). The pairs that exist are covered: `new` then
`list` (AC2), `new` twice then `list` (AC5), `list` with nothing created (AC6), and `list` twice
(AC4). `WI-0001/Q-002` added a third dimension to `new` — the shape of the name — and its pairs
with `list` are covered too: a name differing only in case (AC5), a name whose capitalisation must
survive the round trip (AC7), a name containing a space (AC8), a name that is refused, after which
`list` must produce the AC6 reference output unchanged (AC9, AC10), and a name differing only in
surrounding whitespace (AC11).

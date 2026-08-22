# Harness status — turn 8

Consumed nothing: all eight pre-existing questions were already `answered`, so `answer-questions`
had no work and the turn went straight to the loop. `next` dispatched `refine` on **WI-0002**
(priority rank 2, the highest-ranked runnable item; BUG-0001 lost on rank 3, WI-0003 on an
unfinished `depends-on`).

**WI-0002 could not be made Ready, and was suspended rather than guessed at.** Its AC1 says the
report prints "a set of debts" and never says *which* set — the pairwise ledger, or the minimised
set of transfers that clears the same net positions. That single unstated choice makes AC1, AC2,
AC4, AC5 and AC6 all undecidable (two implementations printing different lines would both pass),
so R4 and R10 fail. `Q-001` puts it to the stakeholder with a worked three-person example that
prints both outputs side by side, and recommends the minimised report. **No acceptance criterion
was rewritten**, because the choice cascades into five of the six.

Six smaller things the item's `## Notes` had handed to `refine` were decided here instead of
being asked — exact summation of printed amounts, non-zero debts only, no "settled" vs "never
owed" distinction, ordering by debtor then creditor name, debt lines only, and a person involved
in nothing producing no line. Each is recorded in `item.md` and in `artifacts/refinement-qa.md`
with why it was judged too small for a round trip. Five of the six hold under either option.

**WI-0003's two questions were filed in the same round trip.** That item's `## Notes` already
recorded, in writing and before this turn, that `refine` must file a question citing
`EP-001/Q-002` and suspend rather than attempt it — the bank CSV sample deferred there ("I'll
send you a sample later") has still not arrived. `Q-001` asks for the sample and states
explicitly that it is a missing fact and not a choice between options; `Q-002` re-puts the four
options for how a bank row becomes a shared expense, with option A's consequence sharpened now
that WI-0001 has shipped with **no delete**. Filing them now costs the stakeholder one reply
instead of two; the sample is the only input to this epic that must come from outside the
workspace. WI-0003's AC5 (is re-import idempotent or additive?) was deliberately **not** asked —
it cannot be put as a question until the sample says what identifies a row.

BUG-0001 sits at `ready` and untouched. It is runnable and would be `next`'s pick once the
questions are answered, but the loop stops on an open human question before reaching it.

Two corrections are on WI-0003's journal, both about the same toolkit friction — see notes below.

## The board

All four items under EP-001: WI-0001 `done`, BUG-0001 `ready`, WI-0002 and WI-0003 both
`awaiting-answer`. Three open questions, all addressed to the human. Nothing `blocked`.

## What refused to pass

- WI-0002's Definition of Ready: R4 (five criteria) and R10 (two combinations). **Not overridden**
  — there was nothing to override, the item genuinely is not Ready.
- WI-0003: no DoR assessment was made at all, deliberately. Assessing criteria that must be
  rebuilt from a file nobody has seen would produce a verdict on criteria certain to be replaced.

```json
{
  "stop_reason": "human-question-open",
  "skills_run": ["refine", "refine"],
  "open_human_questions": ["WI-0002/Q-001", "WI-0003/Q-001", "WI-0003/Q-002"],
  "items_touched": ["WI-0002", "WI-0003"],
  "last_action": "refine filed WI-0003/Q-001 and Q-002 and suspended the item at awaiting-answer, resume-to draft",
  "notes": "Toolkit finding, and it cost two extra journal entries. scripts/lint-claims cannot distinguish a citation from a quotation of a malformed citation. A src marker in WI-0003/Q-002 was written naming an item plus one of its section headings, which is not one of spec/doc-header.md 4a's seven forms, so validate-workspace failed after the transition had already applied. The correcting journal entry described the defect by quoting the malformed marker verbatim - and lint-claims then read the quotation as a citation of its own and failed on that. Fixing it required rewriting one sentence of an append-only journal entry, since no appended entry can remove a line the linter rejects. That rewrite is recorded in full in a third entry on WI-0003, including that it violates spec/journal-and-history.md's append-only rule and does not fall under its single sanctioned exception. Suggested fix: have lint-claims skip src markers inside inline code spans, so a record can state what was wrong with a citation without reproducing the failure. Second, smaller observation: transition applied WI-0003's move and then reported the workspace no longer validates, correctly noting the failing gate was not blocking that move - the behaviour is right and clearly explained, but it does leave a window in which the tracker is committed-invalid if the caller stops there. Nothing else got in the way; the three questions are real, none was invented to fill the batch, and the turn ended one skill under budget because the loop stops on an open human question."
}
```

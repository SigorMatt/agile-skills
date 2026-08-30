---
title: Confirming a deletion asks once, and declining is not a failure
version: 1
status: current
updated: 2026-08-30T04:37:28Z
updated-by: plan
updated-for: WI-0004
---

# ADR-0009 — Confirming a deletion asks once, and declining is not a failure

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0004, applying the stakeholder's answer to `WI-0004/Q-002`
- **Supersedes:** —

## Context

WI-0004 adds `recall delete`, the only operation this tool has that cannot be taken back
[src: WI-0004]. The stakeholder was asked whether it should stop and check first, and chose the
option that does: *"B — show me the card and ask first. I'd rather have one extra keypress than
lose a card to a typo."* [src: WI-0004/Q-002]. They rejected the variant with a `--yes` flag, so
there is no way to delete without confirming [src: WI-0004].

That makes `delete` the **second** subcommand to read standard input, after `review`
[src: ADR-0001]. The two now have to agree or differ deliberately, because
`docs/architecture/overview.md` v4 describes `cli.py` as holding "the loop that prompts, waits,
and re-asks when the answer is not one it recognises" — written when `review` was the only
subcommand that prompted [src: docs/architecture/overview.md]. `review` re-asks on an
unrecognised response and does not move on until it has one of exactly two recognised ones
[src: WI-0002 AC3; recall/cli.py].

A deletion cannot copy that loop, and the reason is in the stakeholder's own words rather than in
a preference of ours. The text of the option they chose says what happens to everything that is
not a yes: it *"removes the card on `y` and leaves the deck untouched on anything else"*
[src: WI-0004/Q-002]. `refine` wrote that into a criterion covering four replies — `n`, an
unrecognised word, an empty line, and closed standard input [src: WI-0004 AC6].

Two things about `review` do not carry over. Its loop exists because a sitting that accepted an
unrecognised keystroke as a grade would record the wrong grade, and there is no safe default —
neither "right" nor "wrong" is the harmless reading [src: WI-0002 AC3]. Here there is a safe
default, and it is the one the guard was asked for: not deleting. And end of input during a
sitting means the person stopped part-way, which they said they would do
[src: WI-0002/Q-001], and `review` returns 0 for it [src: recall/cli.py]; end of input at a
deletion prompt means no confirmation was given, which is the same situation as `n`.

The remaining question the record does not settle is what `recall delete` exits with when the
person declines. `ADR-0001` §5 reserves non-zero for "a refused or failed operation"
[src: ADR-0001]. `refine` recorded exit 0 as an assumption rather than asking, on the grounds
that exit codes fall inside the stakeholder's standing deferral over how things are worded —
*"nothing fancier than that"* [src: EP-001/Q-001; WI-0004]. This ADR is where that assumption
becomes a decision, because it is interface-visible and two subcommands now depend on the reading.

## Options considered

- **A — ask once; anything that is not `y` cancels; declining exits 0.** Cost: `delete` and
  `review` read standard input differently, so `cli.py` holds two prompt shapes rather than one,
  and the difference has to be documented or it reads as an oversight. Risk: a person who types
  `yes` instead of `y`, or fumbles a key, is told nothing was deleted and has to run the command
  again — mildly annoying, and never destructive. A caller redirecting from `/dev/null` gets exit
  0 and no deletion, which is only safe because AC6 requires the run to say so on stdout
  [src: WI-0004 AC6].
- **B — re-ask on an unrecognised response, as `review` does.** Cost: one prompt shape across the
  whole tool, and `cli._read_grade`'s loop generalises to it. Risk: it contradicts the text of the
  option the stakeholder chose, which says anything but `y` leaves the deck untouched
  [src: WI-0004/Q-002], and it turns a fumbled key at the most dangerous prompt in the tool into a
  second chance to hit `y`. It also has no answer for closed standard input except to loop or to
  invent a default, which is how the loop that protects a sitting becomes a hazard here.
- **C — ask once, but exit non-zero when the person declines.** Cost: the same as A. Risk: it
  reads a deliberate `n` as a failed operation, which `ADR-0001` §5 does not say and a person
  would not recognise [src: ADR-0001]. Its one advantage is that a script could tell "deleted"
  from "not deleted" by the exit code alone — and nothing in this project is scripted; the
  stakeholder runs it by hand, once a day [src: EP-001/Q-001].

## Decision

**A.**

1. **`recall delete` prints both sides of the matched card and asks once.** The prompt is issued
   a single time. There is no loop and no re-asking.
2. **Only `y` deletes.** Every other reply — `n`, an unrecognised word, an empty line, end of
   input — cancels, and the run says on standard output that the card was not deleted. The
   comparison is the same shape `review` uses for its two grades: surrounding whitespace stripped
   and case folded, so `Y` and ` y ` are a yes [src: recall/cli.py].
3. **Cancelling exits 0**, and writes nothing to the deck file. Declining is the tool doing what
   it was told, so it is not the "refused or failed operation" `ADR-0001` §5 means
   [src: ADR-0001]. The outcome is legible from standard output rather than from the exit code,
   which clause 2 is what guarantees.
4. **A refusal before the prompt still exits non-zero**: a missing or blank `--question`, a
   question matching no card, a question matching two, and a deck that cannot be read
   [src: WI-0004 AC4; WI-0004 AC5; WI-0004 AC7; WI-0004 AC8]. Those are refusals in `ADR-0001`
   §5's sense — the tool declined to do what was asked — and none of them reaches the prompt.
5. **`review` is not changed.** Its loop stays exactly as WI-0002 built it. This ADR records why
   the two subcommands differ; it does not make them agree.

## Consequences

- `cli.py` gains a second, simpler input shape: one read, compared against one accepted value.
  It does not reuse `_read_grade`, whose loop is the thing being rejected here, but it does reuse
  `_read_line`, whose end-of-input handling is exactly what clause 2 needs.
- The difference between the two prompts has to be visible to a person, not only to a reader of
  this file. `docs/process/using-recall.md` is where that lands when the command is built.
- A person who types `yes` sees the card survive and runs the command again. That is the price of
  clause 2, and it falls on the side of keeping cards.
- **Reversibility: high.** Every clause is `cli.py`'s `cmd_delete` and nothing else — no stored
  data, no deck-file field, no other subcommand. Moving to option B is adding a loop around one
  read; moving to option C is changing one return value. Neither needs a migration, and neither
  touches `deck.py` or `store.py`. What is *not* freely reversible is the guard itself: removing
  the prompt would contradict the stakeholder's answer, and that is theirs to change rather than
  ours [src: WI-0004/Q-002].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-30T04:37:28Z | plan | WI-0004 | First version, recording how WI-0004's confirmation prompt behaves and why it differs from `review`'s |

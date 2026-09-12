---
title: Error messages go to standard output, alongside the prompt
version: 1
status: current
updated: 2026-09-11T21:58:28Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — Error messages go to standard output, alongside the prompt

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`WI-0001` AC4 requires that an expression the tool cannot interpret produces a message naming
what it could not interpret [src: WI-0001 AC4 "produces a message naming what it could not
interpret"], and AC11 requires that the prompt carries on afterwards [src: WI-0001 AC11 "A rejected expression does not end the session"]. Neither
says which stream that message is written to.

Refinement declined to put the question to the stakeholder, on the ground that the answer would
be the same whoever they were, and routed it here in terms: *"Where a disagreement lands: with
`plan`, as an ADR"* [src: WI-0001/Q-001]. Its record is `artifacts/refinement-qa.md` A2, which
also records that **no** delegation from the stakeholder licensed that routing — it is the
pipeline's own judgement about what is worth a person's attention, not a licence they granted
[src: tracker/items/WI-0001/artifacts/refinement-qa.md].

The original form of the question included the exit code. That half is already settled and is not
decided here: AC10 fixes the process exit status at 0 for each of the three deliberate ways a
session ends [src: WI-0001 AC10 "the process exit status is 0"], and this item produces no other
exit.

What the documents say about the setting: droll is one interactive prompt, started once and quit
when the person is done [src: EP-001/Q-001]. The vision records that its reader is a person at a
terminal rather than another program [src: docs/product/vision.md].

## Options considered

- **A — write the message to standard output, the same stream as the prompt and the roll lines.**
  Cost: a shell pipeline that filtered droll's output would receive the error text mixed in with
  roll lines. Risk: if droll later grows a non-interactive mode meant to be piped, that mode
  would want the split and would have to introduce it.
- **B — write the message to standard error, the conventional place for a diagnostic.**
  Cost: two streams with independent buffering feeding one terminal. When output is not a
  terminal — which is exactly how a test or a scripted observation drives this program — Python
  block-buffers stdout and line-buffers stderr, so the error line and the prompt that preceded it
  can arrive out of order in a captured transcript. Risk: an acceptance criterion observed by
  reading a transcript (AC4, AC11) becomes sensitive to buffering rather than to behaviour, and
  a verifier reading a scrambled transcript sees a defect that is not there.
- **C — write to standard error and flush both streams after every write.**
  Cost: the ordering problem goes away, at the price of a rule every future write has to
  remember. Risk: the rule is invisible — the failure it prevents only appears when output is
  redirected, so a missed flush is not noticed by anyone typing at the tool.

## Decision

Every line droll writes during a session — the prompt, a roll line, and the message for an
expression it cannot interpret — is written to standard output.

- The message names the offending input and what was expected, on one line, and no total is
  printed for that input [src: WI-0001 AC4 "and no total"].
- A rejected expression is not a failure of the run: the prompt returns and the process exit
  status is unaffected [src: WI-0001 AC11 "A rejected expression does not end the session"].
- The prompt is flushed before the program waits for input, so that a person sees it before
  typing. That is a property of the prompt, not of the error path, and it holds under A without
  any stream-ordering rule.

The deciding argument is B's cost rather than A's benefit. The two consumers a split stream
serves — a shell pipeline and a log collector — are both excluded by the product
[src: docs/product/vision.md], while the reader a split stream costs is the one this tool has:
someone reading a terminal, or a verifier reading a captured transcript of one.

## Consequences

- AC4 and AC11 can be observed by capturing standard output alone, without redirecting or
  interleaving a second stream. `verify` therefore needs no stream-merging incantation to read
  what happened, and a reproduce command in an item record stays short enough to retype.
- A future non-interactive mode — droll reading expressions from a pipe and writing results for
  another program — would need the split this decision declines. That mode is outside this
  product today [src: docs/product/vision.md].
- **Reversible, and the cost is bounded and known.** The change is the stream argument at the one
  place the message is written, plus AC4's and AC11's observation commands. Nothing is persisted,
  no interface is published, and no data is migrated. What reversal would also have to carry is
  option C's flushing rule, which is the part that is easy to forget rather than the part that is
  hard to write.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-11T21:58:28Z | plan | WI-0001 | First version: the message for an uninterpretable expression is written to standard output, deciding the design question refinement routed to plan as A2 |

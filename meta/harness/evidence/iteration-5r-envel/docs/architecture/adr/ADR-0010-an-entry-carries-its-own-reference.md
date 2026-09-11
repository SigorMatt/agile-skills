---
title: An entry carries its own reference, and the document counts them
version: 3
status: current
updated: 2026-09-11T18:55:51Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0010 — An entry carries its own reference, and the document counts them

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0006
- **Supersedes:** —

## Context

`WI-0006` prints a reference beside each entry and `WI-0005` takes that reference back as the
argument to `envel fix` and `envel remove`
[src: WI-0006 AC3 "The reference on a line is a number counted once across everything recorded"],
[src: WI-0005 AC1 "The reference is one number counted once across everything recorded"]. The
stakeholder chose what it counts: *"one number across everything … what I care about is copying
one thing off the line in front of me and typing it back"* [src: WI-0005/Q-008].

Two properties come with that choice, and both are theirs rather than ours. The number is counted
once across the store, not within an envelope [src: WI-0005/Q-008]. And it stays with its entry:
*"a number written down last week still means what it meant"* is the promise `Q-008`'s own context
made while putting the options in front of them, and `WI-0005` AC1 writes it as a criterion —
nothing is renumbered when an entry is removed, and a number is not handed to a later entry.

The store as delivered gives an entry no identity at all. It is a JSON document with an
append-only `entries` list, and an entry carries `kind`, `envelope`, `cents`, `at`, and `on` or a
description where it has them [src: ADR-0002], [src: envel/envelopes.py:105]. Nothing in the file
distinguishes one entry from another that happens to look the same.

The decision is forced now rather than later because `WI-0005` will remove entries
[src: WI-0005/Q-007], and a reference that is wrong after a removal is wrong in the most expensive
way this tool has: the person types a number they read last week and corrects an entry that is not
the one they meant. No message tells them, because every part of the command succeeded.

## Options considered

- **A — the entry's position in the `entries` list, computed when the listing runs.** Cost:
  nothing at all is stored, and `WI-0006` alone would be correct, because the list is append-only
  within a run and ordered as written [src: ADR-0002] so appending moves nobody. Risk: it breaks
  the first time `WI-0005` removes an entry, and it breaks **silently** — every entry after the
  removed one shifts down one number, and a reference the person wrote down now names its
  neighbour. The failure is a wrong correction to real money with no error message anywhere.
- **B — a `ref` stored on each entry, the next one taken as `max(ref) + 1`.** Cost: one key per
  entry and no counter in the document. Risk: removing the highest-numbered entry lowers the
  maximum, so the next entry recorded takes a number that has already been on the screen. That is
  the *"a number is not handed to a later entry"* half of `WI-0005` AC1 broken, and it fails in
  the same silent way as A, on a narrower set of days.
- **C — a `ref` stored on each entry, with a `next-ref` counter in the document.** Cost: one key
  per entry and one key in the document; the four places an entry is appended have to take a
  number from the counter and advance it; and the document's shape changes, so `format` goes to 2
  and a file written by the delivered code has to be read anyway. Risk: the counter is a second
  piece of state that can disagree with the entries — a file edited by hand could carry a
  `next-ref` below an existing `ref`.

## Decision

Option **C**.

1. An entry carries `ref`, a positive integer, written when the entry is appended and never
   changed afterwards.
2. The document carries `next-ref`, the number the next entry will take. Appending an entry takes
   the current value and advances the counter by one. A move appends two entries
   [src: ADR-0007] and therefore takes two consecutive numbers, one for each side, which is what
   lets `WI-0006` AC6 show a move from either envelope and `WI-0005` AC13 refuse a correction
   aimed at one.
3. `store.FORMAT` becomes `2`. `store.save` writes `2`. `store.load` accepts `1` and `2` and
   refuses anything else, as it already refuses a `format` it does not know
   [src: envel/store.py:56].
4. A document read at `format: 1` is **upgraded in memory**: each entry takes a `ref` in the order
   the list already holds them, starting at 1, `next-ref` is set one past the last, and `format`
   becomes 2. Nothing is written to disk by the upgrade itself — the file is saved only when a
   command changes something [src: envel/cli.py:217] — and the upgrade is deterministic, so a
   format-1 file read twice yields the same references both times.
5. The counter is the only source of a new reference. Nothing derives one from a position, a
   length or a maximum.

## Consequences

**Easy.** A reference survives a removal because it is stored rather than derived, so `WI-0005`
inherits the property rather than having to arrange it
[src: WI-0005 AC1 "The number an entry is given stays that entry's"]. The listing needs no state of
its own: it prints `entry["ref"]` and the number the person types back is looked up by equality
over the same key. The store stays a file a person can open in a text editor and understand, which
ADR-0002 chose deliberately for someone whose current tool is a spreadsheet.

**Hard.** There are now two pieces of state that have to agree, and `next-ref` is the one a
hand-edited file can get wrong. This ADR does not add a repair for that: `store.load` already
refuses a document it cannot read as this format and writes nothing when it does
[src: envel/store.py:56], and a `next-ref` that is merely *low* is not unreadable. What it would
cause is a duplicate reference, which `WI-0006` AC3 makes observable. Deciding what the tool does
about a hand-damaged counter is left to whoever meets one; inventing a repair now would be code no
criterion asks for.

**Reversibility: hard, and it gets harder with use.** While the stakeholder has recorded nothing,
this is one module and one test file. Once they have read a number off the screen, the numbers are
data they are holding outside the tool — written on a statement, remembered — and changing what a
number means is not a code change but a change to something we cannot reach. Reversing to option A
or B would also need a third `format`, because a file carrying `ref` and `next-ref` has to be
readable by whatever comes after. This is the reason the decision is being taken here, by an ADR,
rather than assumed in a plan step: it is the one choice on this item that cannot be undone
cheaply.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-11T18:55:51Z | answer-questions | EP-001 | One `provenance` correction, recorded below: `## Context`'s citation for what an entry carries moved from `envel/envelopes.py:92` to `envel/envelopes.py:105`. The assertion is unchanged. Answering `EP-001/Q-007`, which did not ask about this one — `EP-001`'s review recorded it as holding *with a mark* and left the choice to this pass. Answering it here keeps one treatment for one class. |
| 2 | 2026-09-11T10:40:54Z | answer-questions | WI-0005 | One provenance correction, recorded below: `## Decision` 4's citation for *"the file is saved only when a command changes something"* moved from `envel/cli.py:140` to `envel/cli.py:217`. Found while answering `WI-0005/Q-009` about the same defect elsewhere; the assertion is unchanged. |
| 1 | 2026-09-11T08:01:24Z | plan | WI-0006 | First version: an entry carries `ref`, the document carries `next-ref`, `format` goes to 2, and a format-1 document is upgraded in memory on load. |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T18:55:51Z | answer-questions | EP-001 | provenance | `## Context`, fourth paragraph: *"an entry carries `kind`, `envelope`, `cents`, `at`, and `on` or a description where it has them"* cited `[src: envel/envelopes.py:92]`, which is `add_income`'s docstring. The dict the sentence describes is thirteen lines below it, at `envel/envelopes.py:105` [src: envel/envelopes.py:105], and `record_spend` is what adds `on`, at `envel/envelopes.py:171`. The citation now reads `[src: envel/envelopes.py:105]`; the assertion is unchanged. This one still landed inside the right function, which is why `EP-001`'s review marked it rather than reporting it — repaired here so that the five citations this pass touched are treated alike. Answering `EP-001/Q-007`. |
| 2026-09-11T10:40:54Z | answer-questions | WI-0005 | provenance | `## Decision` 4: *"Nothing is written to disk by the upgrade itself — the file is saved only when a command changes something"* cited `[src: envel/cli.py:140]`. That line is now a comment about how `argparse` reports an unrecognised argument, and on `main` before `WI-0005` it was a closing parenthesis inside a dispatch branch — so unlike the `ADR-0011` citation this question was filed about, this one was **already** off its line before this item, moved by `WI-0006`. The statement it names is `if result.changed:` [src: envel/cli.py:217], and the citation now reads `[src: envel/cli.py:217]`. The assertion is unchanged. Repaired here rather than left, because `WI-0005/Q-009`'s answer settles the policy for exactly this shape and the sentence is a standing clause of a `## Decision` rather than a dated `## Context` statement. |

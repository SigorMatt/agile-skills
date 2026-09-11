---
title: A spend carries the date it happened, in its own field, beside the moment it was recorded
version: 3
status: current
updated: 2026-09-11T18:55:51Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0006 — A spend carries the date it happened, in its own field, beside the moment it was recorded

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0002
- **Supersedes:** —

## Context

The stakeholder chose to be able to date a spend: *"Today unless I say otherwise. I will not
always sit down with the receipts on the day, and a Saturday shop landing in the wrong month
would make the monthly summary wrong"* [src: WI-0002/Q-001]. `WI-0002` turns that into a
criterion about the stored file — a spend written with `--on 2026-08-28` has to be held against
`2026-08-28` and not against the day it was typed
[src: WI-0002 AC9 "A spend can be recorded with a date other than today, written as"].

The store already has a date-shaped field. `ADR-0002` [src: ADR-0002] fixes every entry as
carrying `at`, and says in as many words that *"`at` is when the tool recorded the entry"*. That
sentence and `WI-0002` AC9 cannot both be satisfied by one field unless one of them gives, so
somebody has to say which field a spend's date lives in. `refine` routed exactly this here:
whether the spend's date is a new field or a redefinition of `at` is `plan`'s to settle, and the
criteria are written so that either satisfies them [src: WI-0002].

Two further recorded answers bear on it, and they pull in opposite directions, which is what
makes this a decision rather than a detail:

- Income is **not** dated. *"I put income in when it arrives — that's the one thing I'm never
  late on"* [src: WI-0003/Q-003], and `WI-0003` states the consequence: a month's money-in figure
  is the income **recorded** in that month [src: WI-0003 AC8 "A month's money-in figure is the income"].
  So the summary reads a recording time for income and an event date for a spend.
- Correcting a spend that was already recorded is work the stakeholder asked for
  [src: EP-001/Q-005] and is filed as `WI-0005` [src: WI-0005]. Whatever that item does, it is
  easier to do when the file still says when each entry was written.

## Options considered

- **A — redefine `at` on a spend to mean the date it happened.** Cost: no new field, and the one
  date in an entry is the one the summary wants. Risk: `at` then means two different things
  depending on `kind`, so every reader of the file — `WI-0003`'s summary first — has to branch on
  the kind before it can say what the date is, which is the confusion this option was meant to
  avoid. It also falsifies `ADR-0002`'s own sentence about `at` and so needs that ADR superseded
  rather than extended. And it throws away when the spend was typed, which is the one fact
  `WI-0005` [src: WI-0005] would want and could not recover.
- **B — a new field on a spend entry holding the date it happened; `at` unchanged.** Cost: one
  more field, and two date-shaped things in an entry that a reader opening the file has to tell
  apart. Risk: the two can disagree, and a bug that writes the wrong one into the wrong field is
  invisible until a month is summarised.
- **C — the same new field on every entry, filled in for income with the day it was recorded.**
  Cost: the same as B, and every reader gets one uniform field to sum by. Risk: a file in which
  income carries a date of its own is a file that says income can be dated, which is the thing
  the stakeholder decided against [src: WI-0003/Q-003]; the next person to read it would
  reasonably add `envel add --on`, and `WI-0003` AC8 would stop being true.

## Decision

Option B. A spend entry carries `on`, a calendar date written `YYYY-MM-DD`, being the day the
money was spent. `at` keeps the meaning `ADR-0002` [src: ADR-0002] gave it — when the tool
recorded the entry — on every entry of every kind, and income gains nothing.

```json
{"kind": "spend", "envelope": "groceries", "cents": -1250,
 "on": "2026-09-07", "at": "2026-09-11T04:00:30Z", "description": "lunch"}
```

- `on` is present on every spend entry, including one recorded without `--on`, where it is the
  day the tool was run [src: WI-0002 AC8 "is accepted with nothing extra typed"]. It is never absent and
  never null, so a reader never has to fall back to `at`.
- `description` is present only when one was typed
  [src: WI-0002 AC10 "and it can be recorded without one"]. Absent means there was none.
- `cents` on a spend is **negative**, so that an envelope's balance stays the plain sum of
  `cents` over its entries, exactly as `ADR-0002` [src: ADR-0002] defines it. This is read off
  that ADR rather than decided here; storing a positive number under a `spend` kind would
  falsify its sentence and make every balance in the tool a special case.
- The document's `format` stays `1`. A store written before this item is still a valid store —
  it has no spend entries, so there is nothing in it that should have carried `on` and does not —
  and a store written after it is readable by anything that reads format 1 and ignores fields it
  does not know. There is no migration, which is the property `ADR-0002` was shaped to have.

## Consequences

Easy: `WI-0003` sums a month's spending by `on`, a month's moves by `on` [src: ADR-0007], and a
month's income by `at`, with no branch on what a date means; the asymmetry the stakeholder chose
is visible in the file rather than hidden in the code that reads it. `WI-0005` [src: WI-0005] can correct a spend's date without losing
when the original was entered, and `WI-0006` [src: WI-0006] has a date to show beside each spend.

Hard: an entry now carries two date-shaped fields that can disagree, and nothing in `WI-0002`
prints `on` back, so a spend filed against the wrong day is invisible until `WI-0003` exists —
which is why `WI-0002`'s own criteria are observed against the store file
[src: WI-0002 AC8 "The store file is where this item's dates are read"]. The second cost is
timezone-shaped: `at` is a UTC timestamp and `on` is the machine's local calendar day, so on a
machine well east or west of UTC a spend recorded late in the evening carries an `on` that is not
the date part of its `at`. That is correct — the person's calendar is the local one, and a
summary of their August is the August they lived — but it means the two fields are not
convertible into each other and no code should try.

**Reversibility: cheap now, a data migration later.** No code in this tool writes a spend entry
yet [src: run: grep -rn spend envel → exit 1, no output], so today this is one field name and
the module that builds an entry.
Once the stakeholder has recorded a spend, changing it means code that reads the old shape and
writes the new one — the same position `ADR-0002` is in, and the reason `format` exists.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-09-11T18:55:51Z | answer-questions | EP-001 | One `erratum` correction, recorded below, and it corrects an earlier **correction row** rather than this ADR's prose — the route `ADR-0013` [src: ADR-0013] decides. The `2026-09-11T05:50:35Z` row cites `envel/envelopes.py:245` for where `on` is written, and that line is now a refusal branch. The earlier row is untouched, as it must be. Answering `EP-001/Q-008`. |
| 2 | 2026-09-11T05:50:35Z | implement | WI-0004 | One erratum, recorded below: `## Consequences` enumerated the sums `WI-0003` makes and named two of what are now three. `ADR-0007` [src: ADR-0007] gives a move an `on` of its own, so the list had to gain a third clause. The decision — a spend carries `on` beside `at` — is unchanged, and no code changed to satisfy the new text. |
| 1 | 2026-09-11T04:00:30Z | plan | WI-0002 | First version |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T18:55:51Z | answer-questions | EP-001 | erratum | The row stamped `2026-09-11T05:50:35Z` in this section says *"`on` is the day the money moved on a spend and on a move alike [src: envel/envelopes.py:245]"*. That citation no longer supports it: `envel/envelopes.py:245` is `return Refusal(` [src: envel/envelopes.py:245], inside `move`'s *a move has to be more than zero* check. The assertion is true and the lines that establish it are `"on": dates.format_date(on),` in `record_spend` [src: envel/envelopes.py:171] and `"on": day` on each half of a move [src: envel/envelopes.py:269] [src: envel/envelopes.py:275]. The earlier row is left exactly as it stands — `## Corrections` is append-only and this row corrects it by sitting beside it, per `ADR-0013` [src: ADR-0013]. Found by `EP-001`'s claims audit at the ending; answering `EP-001/Q-008`. |
| 2026-09-11T05:50:35Z | implement | WI-0004 | erratum | `## Consequences`, first sentence, said *"`WI-0003` sums a month's spending by `on` and a month's income by `at`, with no branch on what a date means"*. Both halves are still true of spending and of income, and the sentence is nevertheless wrong as it stands: it is an enumeration of the sums `WI-0003` makes, and `WI-0004` adds a third kind of entry that carries `on` [src: ADR-0007], so a reader taking the list as complete would conclude that a move has no date or that `WI-0003` reads `at` for one. A clause naming moves was added and `ADR-0007` cited. The clause *"with no branch on what a date means"* survives and is true: `on` is the day the money moved on a spend and on a move alike [src: envel/envelopes.py:245], and nothing reads a date without knowing which field it came from. No decision changed, and no code had to change to satisfy the new text. |

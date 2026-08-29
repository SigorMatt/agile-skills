---
id: WI-0003
type: work-item
title: Schedule the next review with simple spaced repetition
status: done
priority: high
epic: EP-001
created: "2026-08-29T10:45:17Z"
updated: "2026-08-29T13:12:14Z"
depends-on:
  - WI-0002
branch: wi/WI-0003
outcome: delivered
---

## Story

As someone reviewing daily, I want a card I got right to come back less often and a card I got
wrong to come back soon, so that my review time goes to the things I have not learned yet.

## Acceptance criteria

Every criterion below is checked by running `recall` against a store of its own
(`RECALL_FILE=<tmp>/cards.json`) and reading that file back. Putting a card on a particular rung
is done by **editing the store file by hand**, which is the mechanism `README.md` already
documents for `due` and the one `WI-0002` AC8 was checked with. AC4 is what makes that possible
for the rung: the row it requires in `README.md`'s card-field table names the field to edit and
the values it may hold, so a checker with no context can set up AC2, AC3, AC5, AC6, AC7 and AC9
from the documentation alone. "Today" means the date `date +%F` prints on the machine running the
check.

- [x] AC1 — A newly added card is due on the day it is added: after
      `recall add "die Katze" "the cat"` the card's `due` in the store file is today's date, and
      `recall review` in that store presents it.
- [x] AC2 — A card answered right moves up one rung of the ladder 1 day → 3 days → 7 days → 30
      days. Checked one rung at a time: hand-edit a card so that it sits on the rung under test
      and its `due` is today, run `printf '\ny\n' | recall review`, and read the file back. A
      card on the 1-day rung is then due 3 days after today, one on the 3-day rung 7 days after
      today, and one on the 7-day rung 30 days after today; in each case the card's rung field
      records the rung it has moved to. A card already on the 30-day rung stays on it and is due
      30 days after today. The new date is measured from **the day of the review**, never from
      the card's old `due`: a card hand-edited onto the 3-day rung with a `due` ten days in the
      past is, after a right answer, due 7 days after today — not 7 days after the date it had
      been due.
- [x] AC3 — A card answered wrong returns to the bottom rung, whatever rung it was on: with the
      card hand-edited onto any rung and due today, `printf '\nn\n' | recall review` leaves it
      due the day after today with its rung field recording the 1-day rung. Setting that card's
      `due` back to today and answering it right then makes it due 3 days after today — one rung
      up from the bottom, not back to the interval it had reached.
- [x] AC4 — The ladder is written down in `README.md`: the four intervals in order, what a right
      answer and a wrong answer do to a card's rung, and a row in the card-field table naming the
      rung field and the values it may hold. A reader with a card's stored fields and `README.md`
      can state that card's next due date after a right or a wrong answer without reading any
      code.
- [x] AC5 — Scheduling state survives ending and restarting the program: after a session that
      moves a card up the ladder, a second `recall` process — `recall list`, and a `recall
      review` on a later date simulated by hand-editing `due` — sees the same rung and the same
      due date, and the store file on disk holds them.
- [x] AC6 — A card that has never been answered sits **below** the bottom rung, so its first
      right answer schedules it one day out: in an empty store, `recall add "die Katze" "the cat"`
      followed by `printf '\ny\n' | recall review` leaves that card due the day after today,
      with its rung field recording the 1-day rung. Setting that card's `due` back to today and
      answering it right again then makes it due 3 days after today — so successive right answers
      on a new card give 1 day, 3, 7, 30 in that order, and a card reaches the top rung after four
      right answers, not three. On that first review a wrong answer produces the same rung and the
      same due date as a right one (AC3); only the stored `result` distinguishes them, and the
      stakeholder accepted that cost when they chose this reading [src: WI-0003/Q-001].
- [x] AC7 — A card whose review was not answered keeps its rung and its due date: with two cards
      due today, `printf '\ny\nq\n' | recall review` moves the first card up the ladder and
      leaves the second card's rung and `due` exactly as they were, and so does a session whose
      input runs out at the question side (`printf '\ny\n\n' | recall review`).
- [x] AC8 — A store written before this item keeps working and is upgraded in place: given a
      hand-written store whose cards carry `due` and `result` but no rung field, `recall list`
      and `recall review` read it without error, every such card is treated as one that has never
      been answered, and the file written by the next review carries the rung field on every card
      it holds.
- [x] AC9 — A scheduling value the tool cannot read stops it rather than being ignored: in a
      store where one card's `due` is `tomorrow`, or whose rung field holds a value `README.md`
      does not list, `recall list`, `recall review` and `recall add "a" "b"` each print a message
      on stderr naming the file, exit 1, and leave the file byte-identical (`cmp` before and
      after). No command silently drops the card.

## Out of scope

- Any per-card or per-user tuning of the schedule, and any second algorithm to choose between.
- Time of day: due-ness is decided by date, not by clock time.
- Catching up: a card that became due while the user was away is simply due, with no penalty or
  compensation — and no credit either. Its next due date is measured from the day it is actually
  reviewed (AC2), so days spent overdue neither shorten nor lengthen the interval that follows.
- Any change to what the review session prints. The schedule is visible in the store file and in
  `README.md`; the session's output stays exactly as `WI-0002` delivered it, and in particular it
  does not announce when a card will next be due.
- Any command for inspecting or setting a card's schedule — no `recall due`, no `recall
  schedule`, no flag to bring a card forward. Hand-editing the store file is the only way to move
  a card, and it is the way `README.md` already documents.
- A card's review history. The store keeps the last result and the current rung and nothing else;
  how a card got to its rung is not recorded, in line with the epic's exclusion of statistics.

## Notes

### Where a brand-new card stands — settled by the stakeholder

`Q-001` is **answered**. `ADR-0001` fixed the four intervals and said a right answer moves a card
up one rung, but never said which rung a card starts on; the stakeholder chose option B: *"B —
tomorrow. When I said one day, then three, then a week, then a month, that's the order I meant to
actually see, starting from a new card."* A card that has never been answered therefore sits
below the bottom rung, and its first right answer puts it on the 1-day rung. `ADR-0001` v2
records it. AC6 is the criterion it settles; AC2's rung-to-rung moves and AC3's reset never
depended on it, because a wrong answer returns a card to the bottom **rung** rather than to the
never-answered state — so the answer unblocked one criterion rather than three, which is what
writing them that way bought.

Routed to `plan`, not asked of anyone — each of these would have the same answer whoever the
stakeholder was:

- What the rung field is called and how it is represented — a rung index, or the interval in days
  it stands for. AC4 requires only that `README.md` name it and its values.
- Whether the store's `version` becomes 3, and how a card without a rung field is upgraded
  (AC8 fixes the behaviour, not the mechanism).
- Where the four intervals live in the code, and whether the never-answered state is a distinct
  stored value or the absence of one. `Q-001`'s answer fixes what that state *means* — a card
  below the bottom rung — but not how it is represented, which stays `plan`'s.
- How AC9's refusal is implemented — which existing error path `load` reports it through, given
  that `README.md` already says an unreadable store is reported and left alone.

### R10 — the combinations this item introduces, and where each is settled

A card's stored state is a rung and a due date, and a review either moves it or does not. The
combinations: right on each of the four rungs (AC2, including the top rung staying put); wrong on
each of the four rungs (AC3); right on a never-answered card (AC6); wrong on a
never-answered card (AC3 — it returns to the bottom rung like any other, and the never-answered
state is not a rung a card can return to); a card not reached in the session, by `q` or by the
input ending (AC7); a card with no rung field at all, from a store written before this item
(AC8); a rung or due value that is not readable (AC9); and a card whose due date is in the past
because the user was away — `## Out of scope` settles that it is simply due, and AC2's last
sentence settles the part that is observable rather than definitional, namely that the interval
which follows is measured from the review and not from the date the card had been due.

Deliberately left unconstrained, by `refine`: the exact wording of AC9's message and of the rung
row in `README.md`, under the stakeholder's standing deferral on `WI-0001/Q-002` — *"Whatever you
think is best, you know this better than I do."*

### Two things WI-0002 handed to this item, recorded by `review-close` when WI-0002 closed

Both concern the `due` field, which this item's ladder writes.

1. **A `due` that is a string but not a date silently removes a card from every review.** `load`
   accepts any string as `due`; `due_cards` compares it lexically, so `"tomorrow"` sorts above
   every `YYYY-MM-DD` value and the card is never due again — while `recall list` still shows it.
   Reproduced during WI-0002's verification. It was not filed as a bug because RB3 has nothing to
   cite: `ADR-0006` states the format without requiring `load` to enforce it, and no criterion of
   WI-0002 covers it. **Decided here, in refinement, as AC9**: an unreadable scheduling value is
   an unreadable store, reported and left alone, which is what `README.md` already promises for a
   store that cannot be read. It is not left alone, because this item makes hand-editing the
   documented way to move a card and so makes a typo in that field far likelier.
2. **WI-0002 writes a placeholder next-due date that this item replaces.** Both a right and a
   wrong answer currently set `due` to the day after the review, which is `ADR-0006`'s declared
   placeholder. AC2 and AC3 are what replace it: the wrong-answer path already matches `ADR-0001`
   and is expected to stay, so this item changes the right-answer path.

### Where the criteria came from

`EP-001/Q-002` is answered: *"A card I get right comes back later each time — one day, then
three, then a week, then a month. Get it wrong and it goes back to the start."* The concrete
ladder is in AC2–AC4, and `ADR-0001` is the authoritative record of it, including why it has four
rungs rather than the five the question's option A offered — the stakeholder's enumeration named
four, and it was taken literally rather than padded.

`WI-0003/Q-001` is answered, and `ADR-0001` v2 carries the result: a card that has never been
answered sits below the bottom rung, so the intervals the stakeholder enumerated are the ones
experienced in order from a new card. AC6 is written from it.

`answer-questions` amended AC2, AC3 and AC4 while the item was at `draft`, and amended the
epic's SM4 in the same pass: SM4 said a wrong answer made a card due "no later than the day of
the review", which cannot hold alongside `WI-0002` AC4 (nothing reviewed today is shown again
today). "Back to the start" is the 1-day rung, so the card returns tomorrow.

Depends on WI-0002 because there is no result to schedule from until reviews record one.

### What was not checked — accepted at review, recorded so it survives the close

`review-close` accepted these five gaps rather than sending the item back. They are here because a
gap recorded only in `verify-report.md` stops being read the moment the item is `done`.

1. **A JSON float equal to a ladder rung is accepted.** `interval: 1.0` is read as the 1-day rung
   and the next write canonicalises it to `1`. Verification judged this inside AC9 rather than a
   failure of it — JSON has one number type, so `1.0` and `1` denote the same value and
   `README.md` lists the number 1; the contrast is with JSON `true`, a boolean that was silently
   reinterpreted as a rung nobody wrote and which AC9 now refuses. No card is dropped and no
   schedule differs. The reasoning is in `artifacts/verify-report.md` and `artifacts/review.md` so
   that anyone who disagrees can find it and file against it.
2. **No behaviour was observed across a real change of date.** Everything was run on 2026-08-29,
   with other dates simulated by hand-editing `due` — the mechanism the criteria themselves
   prescribe.
3. **Timezones and clock changes were not probed.** `due` is a local date with no zone;
   `ADR-0006` records that as a known limitation and this item's `## Out of scope` excludes it.
4. **AC9's probe is a search, not a proof.** Thirty malformed stores across three commands each,
   attacking wrong type, wrong shape, wrong position in the file, and equal-but-not-identical to a
   ladder value. It cannot show no other class exists.
5. **Stores larger than two cards, and concurrent processes, were not exercised.** No criterion
   covers either. `due_cards`' string comparison of `due` and `cmd_review`'s save-per-card were
   both looked at and left as `WI-0002` delivered them: no criterion here touches either, and the
   string comparison is correct for every value `load` now admits.

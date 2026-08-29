---
status: recorded
---

# Refinement Q&A — WI-0003

`status: recorded`. Two rounds. Round 1 put one question to the stakeholder and settled everything
that did not depend on the reply; the stakeholder answered it, `answer-questions` propagated the
answer, and round 2 re-read the Definition of Ready against the amended item, found one gap the
answer had made visible, closed it without asking, and passed the item.

Answers are tagged `[human]` where the stakeholder said it, `[assumed]` where `refine` proposed
or decided it under a standing deferral or a routing rule, `[unresolved]` where it was asked and
is not settled.

## Round 1 — asked of the stakeholder, reply received 2026-08-29

**Q1 (`Q-001`) — The first time you answer a brand-new card correctly, should it come back
tomorrow (one day), or in three days?**

`[human]` — *"B — tomorrow. When I said one day, then three, then a week, then a month, that's
the order I meant to actually see, starting from a new card."*

Filed 2026-08-29T12:20:26Z, answered 2026-08-29T12:26:01Z, propagated by `answer-questions`. The
stakeholder chose **option B** and gave the reason the option was recommended on: their
enumeration is the sequence of waits they expect to experience, counted from a new card. So a
card that has never been answered sits below the bottom rung; its first right answer puts it on
the 1-day rung and it is next due the day after that review. `ADR-0001` is at version 2 with the
never-answered state written into its Decision, and AC6 is now a criterion someone with a
terminal can settle. The cost the option named is accepted and recorded in AC6: on a brand-new
card's first review, right and wrong produce the same rung and the same due date, and only the
stored `result` tells them apart.

The reasoning below is what round 1 wrote before the reply, and is kept as the record of why this
was asked rather than decided.

Why the stakeholder and not `refine`, by the addressee test in step 3 of this skill:

- **Product stake.** It decides what happens the first time a new card is answered right, which
  is the most frequent single event in the tool's life. Tomorrow and three-days-from-now are both
  behaviours the user would notice on their second day of use.
- **Not already answered.** Their reply to `EP-001/Q-002` — *"one day, then three, then a week,
  then a month"* — is honestly readable both ways: as the four places a card can rest (so a new
  card already rests at one day, and the first right answer produces three) or as the sequence of
  waits a card actually gives you (so the first right answer produces one day). `ADR-0001` fixed
  the intervals and did not fix the starting point. `WI-0002`'s refinement recorded the gap and
  routed it here rather than deciding it; `review-close` recorded it again when WI-0002 closed.
- **Not covered by the standing deferral.** `WI-0001/Q-002`'s *"whatever you think is best"*
  answers a category — naming, wording, exit codes, file layout, how a thing is checked. The
  shape of the schedule is the one subject the stakeholder has answered specifically and at
  length, twice; deciding a visible part of it under a deferral aimed at file layout would be
  taking their words for more than they cover.
- **Not implementation-only.** The answer differs depending on who the stakeholder is: someone
  who wants a new card drilled hard says B, someone who resents seeing a card they already know
  says A.

The precedent that made this worth a round trip rather than a guess: `ADR-0001` has four rungs
instead of the five that were recommended, because the stakeholder's enumeration named four and
it was taken literally. Applying the same literalism here would give B — but the literalism was a
decision about *their words*, and it is theirs to apply or not.

Nothing else was filed with it. The four other things this round settled are below, and each is
either theirs already or not theirs at all; filing them would have told them their deferral was
not heard, which is F-023.

## Decided by `refine` in round 1, not asked

- **How a card's rung and due date are inspected, and how a card is put on a given rung: by
  reading and hand-editing the store file.** `[assumed]`, under the standing deferral on
  `WI-0001/Q-002` — the category is "file layout, and how a thing is checked". This is the thing
  the item's `## Notes` recorded that `refine` owed it: without it, AC2, AC3 and AC5 could only be
  checked by waiting a month. `README.md` already documents editing `due` by hand as how a user
  brings a card forward, and `WI-0002` AC8 was verified exactly this way, so the mechanism is
  established rather than invented here. It is now stated at the head of the criteria so that
  every one of them means one thing.
- **`README.md` is "the project's documentation" AC4 names, and the rung field gets a row in its
  card-field table.** `[assumed]`, same deferral, and the same resolution `WI-0001` AC5 took for
  the same phrase. AC4 previously said "the project's documentation" without naming a file, which
  is not something a verifier can open.
- **AC9 is new: an unreadable scheduling value stops the tool instead of being ignored.**
  `[assumed]`. `WI-0002`'s `review-close` handed this item a reproduced defect — a `due` of
  `"tomorrow"` is accepted by `load`, sorts above every real date, and removes the card from every
  review for ever while `recall list` still shows it — and said in terms that this refinement
  should decide it rather than inherit it by silence. Decided: it is a store that cannot be read,
  which `README.md` already promises is reported and left alone rather than overwritten, and
  `ADR-0004` already makes refusing-not-overwriting the rule for a store the tool does not
  understand. So this is the existing documented behaviour extended to a field the tool has been
  reading without checking, not a new product decision. What is new is that this item makes
  hand-editing that field the documented way to move a card, which makes a typo in it much likelier
  than it was.
- **AC7 is new: a card the session never reached keeps its rung and its due date.** `[assumed]`.
  `WI-0002` AC5 already says a session ended with `q` keeps what it recorded; nothing said what
  happens to the cards it did *not* record, and this item is the first one for which those cards
  carry state worth preserving.
- **AC8 is new: a store written before this item is read and upgraded in place.** `[assumed]`,
  by precedent rather than by taste — `ADR-0006` did exactly this for a version-1 store when
  WI-0002 added `due` and `result`, and a user's cards surviving the tool's own upgrades is the
  behaviour the epic's SM5 rests on. Whether the `version` integer changes is `plan`'s.
- **AC1 and AC5 now name their observation.** `[assumed]`. AC1 said "a newly added card is due on
  the day it is added" without saying where that is seen; AC5 said scheduling state "survives"
  without naming a second process or a file. Both are restatements in observable form, not new
  decisions — AC1 in particular is a regression criterion over behaviour `WI-0001` and `WI-0002`
  already deliver.
- **Three exclusions added to `## Out of scope`.** `[assumed]`: the review session's output does
  not change (the schedule is visible in the file and in `README.md`); there is no command to
  inspect or set a card's schedule; and no review history is kept. The first two are the things a
  reader would most reasonably assume this item includes, and the third follows the epic's
  exclusion of statistics.

## Routed to `plan`, not to anyone's inbox

Written into the item's `## Notes`: what the rung field is called and how it is represented,
whether the store `version` becomes 3 and how a card without a rung is upgraded, where the four
intervals live in the code, whether the never-answered state is a stored value or an absence, and
which error path AC9's refusal is reported through. Each would have the same answer whoever the
stakeholder was.

## Definition of Ready — state at the end of round 1, superseded by round 2's table below

The table immediately below was written before `Q-001` came back. It is kept as round 1 left it,
because this file is a record of the exchange rather than a scoreboard; round 2's table is the
current verdict.

## Definition of Ready — state at the end of round 1

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `created`, `updated`, `depends-on: WI-0002` |
| R2 | pass | `## Story` names the role (someone reviewing daily), the capability (a card got right comes back less often, one got wrong comes back soon), and the outcome ("so that my review time goes to the things I have not learned yet") |
| R3 | pass | AC1–AC9, each a labelled checkbox |
| R4 | **fail** | AC6 is a placeholder: it states the two candidate behaviours and names `Q-001` as what chooses between them, which is not decidable by observation. Every other criterion now names a command and the verdict that follows — AC1 `recall add` then the file's `due`; AC2 a hand-edited rung, `printf '\ny\n' \| recall review`, and the resulting date and rung, once per rung; AC3 the same with `n` and then a right answer; AC4 a read of `README.md`; AC5 a second process and the file on disk; AC7 `printf '\ny\nq\n'` and `printf '\ny\n\n'` over two due cards; AC8 a hand-written store with no rung field; AC9 a store with `due: "tomorrow"`, three commands, exit 1 and `cmp`. No criterion carries an unmeasurable adjective |
| R5 | pass | `## Out of scope` names six exclusions, three of which a reader could reasonably assume were included: any change to the session's output, any command for seeing or setting a card's schedule, and a card's review history |
| R6 | **fail** | `Q-001` is open and blocking — deliberately, and it is what this item is suspended on |
| R7 | pass | `depends-on: WI-0002` is recorded and WI-0002 is `done`, so the dependency is both sequenced and finished |
| R8 | **fail** | this file is `status: agenda`; the stakeholder has not replied, and the one answer that would make it `recorded` is the one thing round 1 could not decide |
| R9 | pass | one coherent change: a rung per card, a ladder that moves it, and the documentation and validation of the field that carries it. It is not two items — the store is WI-0001's, the session is WI-0002's, and what is left is the schedule alone |
| R10 | pass | the item's R10 paragraph enumerates the combinations — right and wrong on each of the four rungs and on a never-answered card, a card the session never reached, a card with no rung field, an unreadable value, and a card overdue because the user was away — each covered by a criterion, excluded, or named as deliberately unconstrained with who left it so |

R4, R6 and R8 fail together and for one reason: the stakeholder has not replied to `Q-001` yet.
No Definition of Ready override was recorded, and none could be: an override is the stakeholder's
to request, and they are not in this session.

---

## Round 2 — nothing asked; the reply consumed and one gap closed

Round 2 asked the stakeholder nothing. The one question this item had was answered, and re-reading
the item against the Definition of Ready turned up exactly one thing that was not settled — and it
was not theirs.

- **AC2 now says the new due date is measured from the day of the review, not from the card's old
  `due`.** `[assumed]`, and the honest description is that round 1 could not see this gap. Every
  criterion round 1 wrote sets the card under test to `due` today, so "3 days after today" and "3
  days after the card's old due date" were the same value in every check and the item never had to
  choose. The overdue card is a real case — `## Out of scope` already names it ("a card that became
  due while the user was away is simply due") — and R10 requires the combination to be *visible*,
  which under round 1's wording it was not: the exclusion settles that the card is due, and said
  nothing about the interval that follows the review.

  Decided rather than asked, on three grounds that agree. `ADR-0001` already words both moves from
  the review — "a card at 1 day becomes due **in** 3 days", "next due **one day after the review**"
  — so measuring from the review is the ADR's own reading rather than a new one. `WI-0002` already
  ships it: `ADR-0006`'s placeholder writes the day after the review, whatever the card's previous
  `due` was, and that behaviour is merged and verified. And the alternative is one no stakeholder
  would choose — a card ten days overdue would come back overdue, or immediately due again, which
  is the "penalty for having been away" that `## Out of scope` already refuses. Under the addressee
  test this is "already answered" rather than "product stake", so filing it would have spent a
  round trip re-asking something `ADR-0001` and the shipped code both already say.

  Recorded in three places so it cannot be lost: AC2's last sentence (the observable check — a card
  on the 3-day rung with a `due` ten days in the past is, after a right answer, due 7 days after
  today), the `## Out of scope` catching-up bullet, which now says no credit as well as no penalty,
  and the item's R10 paragraph.

- **The criteria preamble now says AC4 is what makes the hand-edits possible.** `[assumed]`, and a
  clarification rather than a decision. Six criteria are checked by hand-editing a rung field whose
  name `plan` has not chosen yet; AC4 requires `README.md` to carry a row naming that field and its
  values, so a checker with no context can set up every one of them from the documentation. Round 1
  established the mechanism and left the order of operations implicit.

- **Nothing else changed.** The five design questions stay routed to `plan`, the two things
  `WI-0002` handed forward stay decided as round 1 decided them, and no criterion was weakened.

## Definition of Ready — state at the end of round 2, and the verdict this item passed on

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | `[auto]` — frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `created`, `updated`, `depends-on: WI-0002`; `validate-workspace` exits 0 |
| R2 | pass | `## Story` names the role (someone reviewing daily), the capability (a card got right comes back less often, one got wrong comes back soon) and the outcome ("so that my review time goes to the things I have not learned yet") — unchanged since round 1 |
| R3 | pass | `[auto]` — AC1–AC9, each a labelled checkbox |
| R4 | **pass**, was fail | The one failing criterion was AC6, a placeholder naming `Q-001`. It is now settled by the stakeholder's answer and states its own check: `recall add` into an empty store, `printf '\ny\n' \| recall review`, the card due the day after today on the 1-day rung, then 3 days after a second right answer. Every criterion now names a command and the verdict that follows — AC1 `recall add` then the file's `due`; AC2 a hand-edited rung and `printf '\ny\n' \| recall review`, once per rung, plus the overdue case; AC3 the same with `n` then a right answer; AC4 a read of `README.md`; AC5 a second process and the file on disk; AC7 `printf '\ny\nq\n'` and `printf '\ny\n\n'` over two due cards; AC8 a hand-written store with no rung field; AC9 a store with `due: "tomorrow"`, three commands, exit 1 and `cmp`. No criterion carries an unmeasurable adjective |
| R5 | pass | `## Out of scope` names six exclusions, three of which a reader could reasonably assume were included: any change to the session's output, any command for seeing or setting a card's schedule, and a card's review history |
| R6 | **pass**, was fail | `[auto]` — `Q-001` is `status: answered`; no question on this item is open, blocking or otherwise |
| R7 | pass | `[auto]` — `depends-on: WI-0002` is recorded and WI-0002 is `done` |
| R8 | **pass**, was fail | `[auto]` — this file is `status: recorded`, and it holds both rounds: the question as it was asked, the stakeholder's reply verbatim tagged `[human]`, and every `[assumed]` decision with the deferral or precedent it rests on. Nothing is `[unresolved]` |
| R9 | pass | one coherent change: a rung per card, a ladder that moves it, and the documentation and validation of the field that carries it. The store is WI-0001's, the session is WI-0002's, and what is left is the schedule alone |
| R10 | pass | the item's R10 paragraph enumerates every combination — right and wrong on each of the four rungs and on a never-answered card, a card the session never reached, a card with no rung field, an unreadable value, and the overdue card, which round 2 moved from "excluded" to "excluded *and* checked" — each covered by a criterion, excluded, or named as deliberately unconstrained with who left it so |

All ten pass. **No Definition of Ready override was recorded, and none was needed.**

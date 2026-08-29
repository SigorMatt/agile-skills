---
status: recorded
---

# Refinement Q&A — WI-0001

`status: recorded`. Two rounds. Round 1 put two questions to the stakeholder and they answered
both; `answer-questions` wrote their replies in verbatim and propagated them into the criteria.
Round 2 asked them nothing, because nothing left had product stake — see "Round 2" below for the
test that was applied and what it decided instead.

Every answer below is tagged: `[human]` where the stakeholder said it, `[assumed]` where `refine`
proposed it or decided it under a deferral they gave.

## Round 1 — asked of the stakeholder, replies received 2026-08-29

**Q1 (`Q-001`) — When you add a card, do you type both sides on the command line in one go, or
does the tool ask you for each side in turn?**

`[human]`

> *"Both sides on the command line in one go — `recall add "front" "back"`. I'm sitting at a
> terminal, I don't need it to ask me twice."*

Option A, as recommended. Why the stakeholder and not `refine`: it is what they type every time
they add a card, and it decides the wording of AC1 and AC4 — including what "an empty side" even
looks like. It is not a choice that would come out the same whoever the stakeholder was.

Propagated by `answer-questions`: AC1 now states `recall add "<question side>" "<answer side>"`
as one command with both sides as arguments; AC4 states the two empty-side invocations exactly,
`recall add "" "the cat"` and `recall add "die Katze" ""`. Nothing on this item is checked by
driving an interactive prompt.

**Q2 (`Q-002`) — Where should the card file live: one file in the home directory, or one per
directory you run the command in?**

`[human]` — the deferral itself, verbatim. What was decided under it is `[assumed]`.

> *"Whatever you think is best, you know this better than I do."*

This is a **deferral that authorises a decision**, not a choice between the options offered
(`spec/question.md` §2, move 1). `answer-questions` decided it under the deferral and recorded
it as `ADR-0002`: the store is one JSON file at `~/.recall.json`, with the environment variable
`RECALL_FILE` overriding the path when it is set and non-empty. Option C — a file per working
directory — was rejected outright as contradicting the single flat pool the stakeholder asked
for in `EP-001/Q-004`.

Recorded honestly: the stakeholder did **not** pick `~/.recall.json`. The architect did, on the
basis they gave. `Q-002` carries `answered-by: answer-questions` for that reason.

Propagated by `answer-questions`: AC5 names the default path and the override, citing
`ADR-0002`.


## Round 2 — nothing asked of the stakeholder, and why

`refine` returned to this item once `Q-001` and `Q-002` were answered, and applied the
who-is-this-for test to every remaining gap. Nothing passed the first branch — product stake —
so nothing was filed. The stakeholder was asked no second round.

What was left, and where each thing went:

- **Where AC5's "the project's documentation" actually is.** Naming a file. Their standing
  deferral on `Q-002` — *"Whatever you think is best, you know this better than I do."* — covers
  this category, and step 3 of this skill says a standing deferral applies to the category and
  not only to the question that produced it. Decided: `README.md`. `[assumed]`
- **How the no-deck-argument half of AC6 is observed.** As written it stated an absence, which
  nobody can run a command against. Decided: `recall add` takes exactly the two positional
  arguments and rejects a deck-like option, checked with
  `recall add --deck german "die Katze" "the cat"` exiting non-zero. This is a restatement of
  `EP-001/Q-004`'s flat pool in observable form, not a new decision. `[assumed]`
- **The order `recall list` prints cards in.** Unspecified, and AC2, AC3 and AC6 all read its
  output. Decided: ascending card number — the order the numbers are handed out in, which is
  also what makes AC3's "two cards, different numbers" easy to see. A different order would be a
  product decision; this one is the absence of one. `[assumed]`
- **What `recall add` does with the wrong number of arguments.** Round 1 recorded this as
  deliberately unconstrained, on the grounds that it could not be settled before the command's
  shape was. The shape is now settled, so it was settled too, as **AC9**: exit non-zero, print a
  usage line on stderr naming the two arguments, store nothing. This is the negative case step 6
  of this skill asks for, and it is one every command-line tool has. `[assumed]`
- **The exact wording of every message** — the confirmation line (AC1), the two empty-side
  messages (AC4), the empty listing (AC8), the usage line (AC9). Each criterion requires the
  message to exist and to name the right thing; none dictates a sentence. Left deliberately
  unconstrained and recorded as such in the item's R10 paragraph, under the same standing
  deferral. `[assumed]`
- **The store's schema, its crash-safety, whether it is created eagerly or lazily, and what
  happens when `RECALL_FILE` names an unwritable path.** Implementation-only: the answer is the
  same whoever the stakeholder is. Routed to `plan` via the item's `## Notes`, not asked.

Nothing is `[unresolved]`.

## Decided by `refine`, not asked

Each of these is a choice that would come out the same whoever the stakeholder was, or one their
recorded answers already settle. They are recorded here so that the stakeholder can overturn any
of them by saying so, and so that `plan` and `verify` can see who decided what.

- **The tool is called `recall`.** `[assumed]` — `tracker/project.yaml` already names the
  project `recall`, and the stakeholder has not named a command. Used in AC2, AC3, AC6, AC7, AC8.
- **The two commands this item delivers are `recall add` and `recall list`.** `[assumed]` — the
  epic's vocabulary; AC2 needs an observation that shows a card survived a restart, and the
  stored file alone (AC5) is a poor thing to make a user read.
- **A card is identified by a number, starting at 1 and increasing by 1.** `[assumed]` — AC1
  already required the confirmation to identify the card; a number is the smallest identifier
  that a person can read back to the tool later, and it makes AC3 (two identical cards are two
  cards) checkable.
- **`recall list` with no cards prints one plain line and exits 0.** `[assumed]` — the same
  shape the stakeholder's own review flow gets in WI-0002 AC3; an empty pile is not an error.
- **Card text is stored and listed byte-identical, including non-ASCII.** `[assumed]` — the
  stakeholder said the cards are vocabulary (`EP-001/Q-004`: *"It's just vocab, one pile is
  fine."*), and vocabulary in most languages is not ASCII. Written as AC7 rather than left
  implicit in AC2 because it is exactly the case an implementation gets wrong.
- **Card sides are a single line of plain text.** `[assumed]` — recorded in `## Out of scope`,
  flagged there as an assumption rather than as something they said, so they can overturn it.

## Routed to `plan`, not to the stakeholder

These would have the same answer whoever the stakeholder was, so they are in the item's
`## Notes` as open design questions rather than in anyone's inbox: how a write survives an
interruption, and whether the store is created lazily or eagerly.

Round 2 added one to this list: what `recall` does when `RECALL_FILE` names a path it cannot
write. Same test — the answer would be the same whoever the stakeholder was.

The store's **file format** was on this list and has since been taken off it. `ADR-0002` fixes it
as JSON, because both of the options `Q-002` put to the stakeholder named a `.json` file and
leaving it open would have left the record saying two different things about one path. What is
inside the file remains `plan`'s to decide.

## Definition of Ready — state at the end of round 1

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | `item.md` frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `created`, `updated` |
| R2 | pass | `## Story` names the role (someone building up a set of things to memorise), the capability (add a card with two sides), and the outcome ("so that … is still there the next time I open the tool") |
| R3 | pass | AC1–AC8, each a labelled checkbox |
| R4 | **fail** | AC1 and AC4 say "the tool's add command" without saying what is typed or printed, which `Q-001` decides; AC5 does not name a location, which `Q-002` decides. AC2, AC3, AC6, AC7, AC8 are decidable as written |
| R5 | pass | `## Out of scope` names editing and deleting, decks, scheduling, multi-line and non-plain-text card sides, and any command beyond add and list |
| R6 | **fail** | `Q-001` and `Q-002` are open and blocking — deliberately, and this is what the item is suspended on |
| R7 | pass | `depends-on` is empty; nothing precedes this item |
| R8 | **fail** | this file is `status: agenda`; the conversation has not happened |
| R9 | pass | one coherent change: a store, an add command and a list command, deliverable as one branch |
| R10 | pass | the combinations are enumerated in `## Notes`, each either covered by a criterion, excluded, or named as deliberately unconstrained |

R4, R6 and R8 failed together and for the same reason: at the end of round 1 the stakeholder had
not replied yet. No Definition of Ready override was recorded, because nobody has asked for one —
an override is the stakeholder's to request, and they are not in this session.

**This table is the state at the end of round 1 and is now out of date.** The replies are in
(above), `Q-001` and `Q-002` are answered, and `answer-questions` has rewritten AC1, AC4 and AC5
to state exactly what is typed and where the cards are stored. R4 and R6 have therefore changed
since this table was written. Re-judging the Definition of Ready and setting this file's `status`
is `refine`'s job, not `answer-questions`', so neither has been done here — the item goes back to
`draft`, which is where `refine` picks it up.

## Definition of Ready — state at the end of round 2

This is the table that stands. The round-1 table above is kept as the record of where the item
was before the stakeholder replied.

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | `item.md` frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `created`, `updated`; `depends-on` is absent and `blocks: WI-0002` is recorded |
| R2 | pass | `## Story` names the role (someone building up a set of things to memorise), the capability (add a card with two sides), and the outcome ("so that … is still there the next time I open the tool") |
| R3 | pass | AC1–AC9, each a labelled checkbox |
| R4 | pass | every criterion names a command and a verdict. AC1 `recall add "<q>" "<a>"` → exit 0 and a numbered confirmation; AC2 `recall list` in a fresh process → the same text and number; AC3 two identical adds → two numbers, both listed; AC4 `recall add "" "the cat"` and `recall add "die Katze" ""` → non-zero, the empty side named, nothing stored; AC5 `RECALL_FILE=<tmp>/cards.json recall add "a" "b"` → the card in that file, and both paths named in `README.md`; AC6 `recall add --deck german …` → non-zero, and `recall list` in card-number order; AC7 `recall add "Grüße" "greetings"` → listed byte-identical; AC8 `recall list` with an empty store → one line, exit 0; AC9 `recall add`, `recall add "die Katze"`, `recall add "a" "b" "c"` → non-zero, a usage line on stderr, nothing stored. No criterion contains an unmeasurable adjective |
| R5 | pass | `## Out of scope` names editing and deleting, decks, scheduling, multi-line and non-plain-text card sides, and any command beyond add and list — the first of which a reader could easily assume was included |
| R6 | pass | `Q-001` and `Q-002` are both `status: answered`; no question on this item is open |
| R7 | pass | `depends-on` is empty; nothing precedes this item |
| R8 | pass | this file, `status: recorded`, holds both rounds — the two questions and the stakeholder's verbatim replies, and round 2's decisions each tagged `[assumed]` with the deferral they rest on |
| R9 | pass | one coherent change: a store, an add command and a list command, deliverable as one branch |
| R10 | pass | the item's R10 paragraph enumerates every combination — both sides, either side empty, duplicate text, non-ASCII text, a deck-like option, the wrong argument count, listing with and without cards, and the store resolving with and without `RECALL_FILE` — each covered by a criterion, excluded, or named as deliberately unconstrained with who left it so |

No Definition of Ready override was recorded, and none was needed: every criterion passes on its
own terms. An override is the stakeholder's to request, and they did not request one.

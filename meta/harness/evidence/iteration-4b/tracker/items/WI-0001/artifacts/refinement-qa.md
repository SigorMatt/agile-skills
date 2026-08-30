---
status: recorded
---

# Refinement Q&A — WI-0001

## How this exchange happened

The stakeholder on this project answers asynchronously, in files, and is not present in the
session that runs a skill (`SIMULATION-NOTICE.md`). So the exchange below is not a transcript of
a conversation: it is the record of which questions this refinement needed answered, where each
answer came from, and — for the ones nobody was asked — what was assumed instead and on whose
authority.

Three of the answers below are the stakeholder's own words, taken verbatim from the questions
`intake` filed on the epic and they answered: `EP-001/Q-001`, `EP-001/Q-002` and `EP-001/Q-003`.
They are quoted, not paraphrased. Everything tagged `[assumed]` is this skill's, and says so.

**This refinement filed no new question to the stakeholder.** That is a result, not an omission,
and the reasoning for each candidate is below. Every gap this item had was closed by an answer
they had already given, by a deferral of theirs that covers a whole category, or by a design
decision that would be the same whoever the stakeholder was — which `refine`'s procedure routes
to `plan`, not to a person.

---

## Round 1 — the questions this item needed answered

### Q&A 1 — What does a person type to add a card? (DoR R4)

Every criterion on this item said what must be true rather than what to run, because the shape
of the interface was undecided. R4 cannot pass in that state.

**Answer** `[human]`, from `EP-001/Q-002`, verbatim:

> A command-line tool — I'm doing this at a terminal once a day, so option A works fine.

Recorded as `ADR-0001`, which fixes the surface far enough for a criterion to name it: one
executable `recall`, subcommands `add`, `list`, `review`, and `recall add --question <text>
--answer <text>` taking its two sides as options rather than prompting. AC1 to AC6 are written
against that.

### Q&A 2 — Where does the deck live, and in what format? (DoR R4, and AC7)

**Answer** `[human]`, from `EP-001/Q-001`, verbatim:

> Storage should just be a file on my machine that survives a reboot.

**Challenged once, and the challenge is recorded here rather than sent:** "a file on my machine"
does not say *which* file or in what format, and a criterion cannot be decided against "a file".
The sentence was read as a deferral over the whole category — they said "just", and they said it
in answer to a question that invited anything at all on their mind — so what it constrains was
separated from what it leaves open:

- Constrained, and now AC7: exactly one file; durable across a reboot; under the user's home
  directory; not in `/tmp`, `/var/tmp` or `$TMPDIR`; and its path stated in the project's
  documentation, so they can point at it.
- Left open, and routed to `plan` under an ADR rather than back to them: which path, and which
  format.

Not asked again, per `refine`'s step 3: re-asking a category they have already deferred tells
them their answer was not heard.

### Q&A 3 — What must this item store that it never reads back? (DoR R9, R10)

Not a question for the stakeholder. Answered from the record: `ADR-0002`, itself written from
their answer to `EP-001/Q-003`, quoted here for the reader's benefit:

> Just right or wrong, no rating scale. If I get it right it comes back later each time — a day,
> then three, then a week, then a month or so. If I get it wrong it goes back to the start.

Consequence for this item: a card carries a ladder position and a next-review date, and carries
no ease factor. A new card is due the day it was added. Recorded in `## Notes` so `plan` designs
storage that WI-0002 and WI-0003 can use without reopening this item. No criterion here reads
those fields back — that would be WI-0002's and WI-0003's work, and is in `## Out of scope`.

### Q&A 4 — What happens if the deck file is there but unreadable?

Considered as a question for the stakeholder and **not** asked, because they have already stated
the principle that settles it. `EP-001/Q-001`, verbatim:

> Mainly this: don't lose my progress — that's the one thing that would make this a failure

An implementation that meets AC5 by treating an unparseable file as "no deck yet" and writing a
fresh one over it destroys exactly what they said would make the tool a failure. AC8 therefore
requires the opposite and requires it observably: refuse, name the file, exit non-zero, and leave
the bytes identical. `[human]` for the principle; `[assumed]` for reading it as far as "refuse
rather than repair", which is the conservative direction and is reversible.

### Q&A 5 — May two cards have the same question side?

**Answer** `[assumed]` — nobody was asked. R10 requires this combination to have a stated
behaviour or be visibly unconstrained, and stating it costs nothing. Decided: duplicates are
allowed, and `recall list` shows both (AC9). Reasoning, recorded so it can be argued with: they
are learning vocabulary, and a vocabulary deck legitimately holds two cards with the same prompt
and different senses. Refusing would be the more surprising behaviour, and deduplication is a
small change if they want it.

Not escalated, because it changes nothing about what the tool is for, and because a question a
stakeholder would answer "whatever you think" is one this protocol says to decide.

### Q&A 6 — Is a side of only spaces an empty side?

**Answer** `[assumed]`. AC2 treats it as blank and refuses. They asked for a card with two sides;
a side of three spaces is not one. Reversible, and named in `## Notes` as an assumption.

### Q&A 7 — Is the deck's location configurable?

**Answer** `[assumed]`, and it is an exclusion rather than a behaviour: no flag, no environment
variable, no config file. Put in `## Out of scope` where a reader can contradict it. They said a
file on their machine; they did not ask to choose which, and the epic already excludes syncing
and second machines. If they want it, it is a new item, not a widening of this one.

---

## What was deliberately not asked, and why

`refine`'s step 3 applies a test in order to every gap, and stops at the first that fits. The
results for this item, so a reader can check the routing rather than take it on trust:

| Gap | Route taken | Why |
|-----|-------------|-----|
| How a card is added | Already answered | `EP-001/Q-002`, and `ADR-0001` |
| Whether progress can be lost | Already answered | `EP-001/Q-001`; became AC7 and AC8 |
| Which file, which format | Standing deferral | *"just a file on my machine"* covers the category; routed to `plan` |
| Implementation language, runtime, `PATH` | Implementation-only | The answer is the same whoever the stakeholder is; in `## Notes` for `plan` |
| Interactive prompt as a fallback for `add` | Implementation-only | `ADR-0001` already left it to `plan`; the option form is required either way |
| Duplicates, blank sides, text normalisation | Decided and marked assumed | Reversible, no product stake, stated so R10 can see them |

Nothing on this item met the first test — product stake — that was not already answered. Filing
a question anyway would have spent a round trip of the stakeholder's attention, which is the
scarcest thing in this loop, and `refine`'s own contract calls that out as the failure mode
opposite to guessing.

## Cross-answer check

Checked against: `EP-001/Q-001`; `EP-001/Q-002`; `EP-001/Q-003`. Those are every recorded human
answer in this workspace.

- `EP-001/Q-001` — **compatible** with everything written here. AC7 and AC8 are derived from it
  directly; the assumptions in Q&A 5, 6 and 7 are all in areas it does not speak to.
- `EP-001/Q-002` — **compatible**. AC1 to AC6 use the interface it chose, as fixed by `ADR-0001`.
  Nothing here asks the tool to do something a command line cannot.
- `EP-001/Q-003` — **compatible**. It settles scheduling, which this item stores fields for and
  never reads back; `## Out of scope` says so explicitly, so there is no criterion here that
  could contradict it.

No conflict was found, so no question was filed under `ADR-0008` §3, and no sentence of theirs
was rewritten anywhere.

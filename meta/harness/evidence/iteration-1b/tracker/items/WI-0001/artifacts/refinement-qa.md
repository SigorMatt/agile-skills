# Refinement Q&A — WI-0001

Every question put to the person who stated the idea, and every answer, in order and verbatim.
Answers are tagged `[human]` when they said it, `[assumed]` when `refine` proposed it and it was
not contradicted, and `[unresolved]` when it was asked and not settled.

This project's stakeholder answers **asynchronously, in the question files** — they are not
present in the session that refines an item. So the questions below were filed as
`questions/Q-002.md`, `Q-003.md` and `Q-004.md`, the item was suspended at `awaiting-answer`, and
their answers were written into those files and propagated by `answer-questions` before this
refinement resumed. The exchange is reproduced here in full because this file, not the question
directory, is what `verify` and `review-close` are pointed at.

Nothing in this file is paraphrased. Where an answer was short or deferred, it is short or
deferred here.

---

## Round 1 — filed 2026-08-21T19:06:00Z, answered before 2026-08-21T19:11:21Z

### Q1 (`Q-003`) — What should the two subcommands be called?

> **Asked because:** R4 fails on AC1, AC2 and AC4 as `intake` wrote them. Every criterion has to
> name something a person can actually type, and `ADR-0001` deliberately left the subcommand names
> to this refinement. Options offered: **A** `add-person <name>` / `people`; **B** `person add` /
> `person list`; **C** `add` / `list`. Recommendation: A.

**Answer** `[human]`:

> Whatever you think is best, you know this better than I do.

**Challenged once, as the procedure requires** — the challenge was already in the question: it
carried three concrete options and a recommendation, so "whatever you think is best" is an answer
to a specific proposal rather than to an open prompt. `refine` did not re-file it. Pressing a
second time for a preference on a question already answered with a delegation would spend the
scarcest thing in this loop on nothing.

**Recorded as** `[assumed]` in substance, decided by `answer-questions` as **ADR-0006**: option A.
`add-person <name>` and `people` here; `add-expense` / `expenses`, `add-payment` / `payments` and
`who-owes-whom` for the rest of the epic, by the rule that a command which records a fact is
`add-<noun>` and one which lists facts is the bare plural noun.

### Q2 (`Q-002`) — When someone types a name that is already in the group, what happens?

> **Asked because:** R4 and R10 fail on AC4 as `intake` wrote it — "produces a stated outcome
> rather than a silent duplicate" names neither what makes two names the same person nor what the
> tool does about it. Options offered: **A** exact match only, refuse; **B** match ignoring case
> and surrounding spaces, refuse, naming the spelling that exists; **C** match ignoring case,
> succeed quietly. Recommendation: B.

**Answer** `[human]`:

> Go with B. If someone types "sam" and Sam's already in the group, just tell them and don't add a
> duplicate — I don't want two half-right versions of the same person messing up the totals.

**Recorded as** `[human]`. This is AC6. It became **ADR-0005** points 3 and 4, together with the
answer to Q3.

### Q3 (`Q-004`) — May a name contain spaces, and is reserving `,` and `=` acceptable?

> **Asked because:** R4 fails on AC1 and AC4 — neither says what a name may be, so a verifier
> cannot tell whether `add-person "Anna Karin"` is supposed to work. Reserving the two characters
> is free while the group is empty and expensive afterwards, because this epic has no rename
> command. Options offered: **A** single word, `,` and `=` reserved; **B** any text, `,` and `=`
> reserved; **C** any text, nothing reserved, sharers named with a repeated flag.
> Recommendation: B.

**Answer** `[human]`:

> Go with B — allow spaces. We've actually got two people who go by the same first name, so full
> names matter.

**Recorded as** `[human]`. This is AC1, AC7 and AC8, and **ADR-0005** points 1 and 2. Their second
sentence is a durable fact about the group rather than an answer to the question asked, so it was
also written into `docs/product/prd.md` (v2).

---

## Round 2 — decided by `refine`, not put to the human

Everything below is detail the human has twice declined to be asked about (Q1 here, and `Q-001`
before it, both answered "whatever you think is best"). Filing more questions on the same subject
would stop the pipeline for a round trip and, on the evidence of two identical answers, return
nothing. Each is therefore `[assumed]`: proposed by `refine`, **not** confirmed by the human, and
carried in the item's `## Notes` so that `plan`, `implement` and `verify` inherit them as
assumptions rather than as requirements.

### Q4 — What exactly does each message say?

**Answer** `[assumed]`: exact text, because "a stated message" is not decidable — two verifiers
could disagree about whether some output counts. Pinned:

- success: `Added Sam Okafor.` on standard output
- empty group: `No one is in the group yet.` on standard output
- duplicate: `Sam Okafor is already in the group.` on standard error — naming the spelling that is
  already there, which is what the human's answer to Q2 asked for
- empty name: `A name cannot be empty.` on standard error
- reserved character: `A name cannot contain a comma or an equals sign; those are reserved.` on
  standard error

The wording is cosmetic and reversible; what is not reversible cheaply is leaving it unstated,
because then `verify` has to invent a standard after the code exists.

### Q5 — In what order does `people` list the group?

**Answer** `[assumed]`: the order people were added, one name per line, nothing else printed.
Insertion order needs no tie-break rule and no decision about how to sort names differing in case
or carrying accents — both of which ADR-0005 has just made significant. Alphabetical order would
have required a third decision on top of two the human has already had to make about names.

### Q6 — `add-person Sam Okafor`, unquoted: two arguments. Joined, or refused?

**Answer** `[assumed]`: refused, with a message saying the name must be a single argument and
should be quoted. Joining is friendlier and was rejected on the same grounds as the duplicate
rule: a mistyped `add-person Sam Okafor Smith` would silently create a third spelling of somebody,
and this epic has no way to remove them.

### Q7 — Where is the data stored?

**Answer** `[unresolved]`, deliberately, and recorded in `## Notes` as unconstrained rather than
carried as a risk. The human's requirement is "data must survive between runs", which AC3 states
in full. Where the file lives and what is in it is a design decision for `plan`, it has no
observable consequence at this item's level, and it governs all four items rather than this one —
so deciding it here would put an epic-wide choice in the wrong place. `plan` records it as an ADR.

---

## Definition of Ready — where each criterion stands

| # | Verdict | Evidence |
|---|---------|----------|
| R1 | pass | `validate-workspace` exits 0; `type`, `epic`, `priority` all set |
| R2 | pass | `## Story` names the role, the capability and the "so that" |
| R3 | pass | AC1–AC11, each a labelled checkbox |
| R4 | pass | every criterion names a command and the output that settles it; the three answers above removed the last three that did not |
| R5 | pass | `## Out of scope` names five things, including two a reader would reasonably assume are here: where the data is stored, and what happens with two people running the tool at once |
| R6 | pass | no open question remains on this item; all four are `answered` |
| R7 | pass | no `depends-on` |
| R8 | pass | this file |
| R9 | pass | one coherent change: add a person, list the group, persist both |
| R10 | pass | the two subcommands' combinations are all stated (AC5 empty listing, AC6 duplicate, AC7/AC8 invalid names, AC9 accents, AC10 arity, AC11 unknown subcommand), and the two things left open are named in `## Notes` with who left them so |

No override was needed or taken.

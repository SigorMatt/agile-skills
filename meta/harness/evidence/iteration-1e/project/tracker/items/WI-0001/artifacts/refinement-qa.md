---
status: recorded
---

# Refinement Q&A — WI-0001

`status: recorded`. Round 1's three questions were filed as `WI-0001/Q-001`, `Q-002` and
`Q-003`, all addressed to the human; the stakeholder replied to all three, `answer-questions`
propagated the replies on 2026-08-26, and refinement resumed and closed the item out. Every
question asked and every answer received is below, verbatim, tagged `[human]` where the
stakeholder said it and `[assumed]` where refinement decided it and says so.

**Round 2 asked nothing.** That is a decision with a reason, and it is recorded below under
"Round 2" rather than left as an absence — this file being `recorded` asserts that the
conversation is complete, so it has to say why one more round was not needed.

This file also records what refinement settled **without** asking, and why each of those was not
the stakeholder's to decide. That half is not provisional: it is the analysis this round
produced, and it is written down so the next execution folds in three answers rather than
starting over.

---

## Definition of Ready — where the item stands, criterion by criterion

Assessed against `spec/dor-dod.md` §1, on `item.md` as `intake` left it.

| # | Verdict | Why |
|---|---------|-----|
| R1 | **pass** | `id`, `type`, `epic`, `priority`, `created`, `updated` all present and set |
| R2 | **pass** | `## Story` names the role (someone who shares costs with friends), the capability (add people, record an expense with its payer and sharers) and the outcome ("so that what we spent lives in one place… and is still there tomorrow") |
| R3 | **pass** | five criteria, labelled `AC1`–`AC5`, each a checkbox |
| R4 | **FAIL** | every criterion says "a documented command" and names none, so nobody with a terminal can run one. AC2 does not say what an amount looks like or what makes one invalid; AC5 says a command "fails" without saying how that is observed. See "What refinement settled" — most of this is refinement's own to fix and is fixed below |
| R5 | **pass** | `## Out of scope` names four things, including editing and deleting, which a reader would reasonably assume was included |
| R6 | **pass** | no question existed on this item before this round |
| R7 | **pass** | `depends-on` is absent; nothing is unfinished ahead of it |
| R8 | **FAIL** | this file did not exist. It exists now at `status: agenda`, which does **not** satisfy R8 — only `recorded` does |
| R9 | **pass** | one coherent change: one data model, one store, four commands over it. Splitting "people" from "expenses" would leave an item whose whole value is a name list nobody can do anything with, and the two cannot be ordered independently — recording an expense needs people to exist |
| R10 | **FAIL** | the behaviours this item introduces have combinations nothing states: adding a name that already exists, an expense shared by nobody, a payer who is not among the sharers, the same name given twice in one sharer list, a zero or negative amount, an amount with more precision than money has, and what a split that does not divide evenly does with the remainder |

R4, R8 and R10 are what this round is closing. R4 and R10 are closed partly by decisions
refinement is entitled to take (below) and partly by the three answers, which have now arrived
and are folded in below. R8 is closed when `refine` sets this file to `recorded`; all three
verdicts stay as written above because they describe `item.md` as `intake` left it, and `refine`
re-assesses them when it resumes.

---

## Round 1 — asked of the stakeholder, and answered

Three questions, filed together as one ask. Each was one decision. None of them was a technical
call: each changes what the tool is for, what counts as correct, or what is in this item. All
three came back answered; the replies are verbatim in the question files and are quoted here.

### Q-001 — How does an expense divide between the people who shared it?

**Answered: equal split between the named sharers** (option A). Traces to R4 (AC2 and AC3 could
not be made decidable without it) and R10.

> [human] Equal split, keep it simple. If a bill's uneven we'll just enter it as separate
> expenses.

So a 30 dinner shared by three people is 10 each. There is no per-person amount on an expense and
no weighting; the "Ana had the steak, Ben had the soup" case is recorded as two expenses, which
the stakeholder chose knowing that was the cost. `--shared-by` therefore stays a bare list of
names, which is the surface A1 already assumed. A6 below is unchanged and now bites: 10 shared by
three still has to add up to 10.00, so the remainder rule matters and is `plan`'s.

### Q-002 — Does an expense carry a description, and a date, or only an amount?

**Answered: both, as option C** — an optional description and a date that defaults to today.
Traces to R4 (AC3 could not say what the listing shows) and R10.

> [human] Yeah, add both — description and date. I'll want to know what a charge was for when
> I'm looking back over the list.

They accepted the option that offered both fields, which is C. Option B — a *required*
description and no date — was not chosen, so the description stays optional exactly as C
described it; and their stated reason, wanting to know what a charge was for when reading the
list back, is served by having the field rather than by being forced to fill it. `--date`
defaults to the day the expense is recorded.

Neither field takes part in any arithmetic. They exist for reading the list back, and they are
what lets WI-0003's importer carry a bank row's own date and description through instead of
discarding them.

### Q-003 — Can a person or an expense be corrected or removed once recorded?

**Answered: deletion yes, editing no, and not in this item** — option C, narrowed. Traces to R5
and R10.

> [human] Hadn't really thought about it, but if I have to pick — being able to delete a mistake
> matters more to me than editing one. Timing's up to you, doesn't need to hold up the
> who-owes-whom feature.

Three things follow. Deletion is wanted, so append-only (option A) is refused. Editing was
offered in the same breath and not chosen, so it is out of scope and nothing is scheduled for it;
a correction is a delete and a re-record. And the timing was delegated with one constraint — it
must not delay WI-0002 — which is option C rather than option B.

`answer-questions` filed **WI-0004** ("Delete a person or an expense recorded by mistake") at
`draft` under EP-001, `arose-from: WI-0001/Q-003`, `depends-on: WI-0002`, priority `medium`.
WI-0001 stays append-only. This item's `## Out of scope` now names both halves of the answer.

## What refinement settled without asking, and why

Each of these would have the same answer whoever the stakeholder was, or is a naming call. A
stakeholder in an earlier run of this methodology objected that "three of the four were things
I'd expect a team to just decide on their own… technical calls being routed to me as questions"
(F-023), and these are those. Each is recorded so that `plan`, `implement` and `verify` inherit a
decision rather than a gap. Every one is marked `[assumed]` because **the stakeholder was not
asked**; none of them is being reported as something they said.

**A1 — The command surface.** `[assumed — refine, not asked]`

    python3 -m expenses person  add <NAME>
    python3 -m expenses person  list
    python3 -m expenses expense add --amount <AMOUNT> --paid-by <NAME> --shared-by <NAME>[,<NAME>...] \
                                    [--description <TEXT>] [--date <YYYY-MM-DD>]
    python3 -m expenses expense list

`--description` and `--date` were added to this surface by `Q-002`'s answer, after A1 was first
written; they are the stakeholder's, not an assumption.

Reason: R4 requires criteria a person with a terminal and no context can decide, and that is
impossible while every criterion says "a documented command". What things are called is a team
call. `python3 -m expenses` is chosen because it needs no installation step and no entry-point
machinery, which suits "python3 and the standard library only". `plan` may not quietly change
this — the acceptance criteria will be written against it — but may propose a change with a
recorded reason before the item is planned.

**A2 — Exit codes and streams.** `[assumed — refine, not asked]` A command that does what was
asked writes its output to stdout and exits 0. A command that refuses — an unknown person, a bad
amount, a name that already exists — writes a message to stderr, changes nothing on disk, and
exits non-zero. Reason: this is the ordinary contract of a Unix command-line tool, it is what
makes AC5 decidable at all, and no stakeholder preference is involved.

**A3 — A person is identified by their name.** `[assumed — refine, not asked]` The name as typed,
with surrounding whitespace stripped, is the identifier; comparison is exact, so `Ana` and `ana`
are two different people. `person add` with a name already in the group changes nothing and exits
non-zero. Reason: the stakeholder said "add people" and named no other attribute, so a name is
all there is to identify one by. Exact comparison is the behaviour that never silently merges two
people; the cost is that a typo makes a new person, which Q-003's answer may give them a way to
undo.

**A4 — Amounts are money.** `[assumed — refine, not asked]` An amount is a decimal number with at
most two decimal places and must be strictly greater than zero. `12`, `12.5` and `12.50` are all
accepted and mean the same thing; `0`, `-4`, `abc` and `1.005` are refused per A2. Reason:
expenses are money, and two decimal places is what money is written in. Zero and negative are
refused because an expense of nothing has no meaning and a negative one is a refund, which the
epic puts out of scope. Currency is not named anywhere and is not converted — EP-001 already
excludes conversion.

**A5 — Sharers.** `[assumed — refine, not asked]` `--shared-by` must name at least one person. The
payer does **not** have to be among the sharers: paying for something you did not share in is
normal. The same name twice in one sharer list is refused per A2, because it is far more likely a
typo than an intent to count someone twice. Reason: all three follow from "shared by some or all"
and none of them is a preference.

**A6 — A split must be exact.** `[assumed — refine, not asked]` However an expense divides, the
shares must add up to exactly the amount paid: no fraction of a unit may be created or lost.
Reason: this is not a choice — any other behaviour is a bug, and WI-0002's settlement list cannot
balance if the inputs do not. **Which** sharer absorbs an indivisible remainder is a genuine
design decision with no stakeholder stake, and is left to `plan` as an open design question in
`## Notes`; the only constraint refinement places on it is that it be deterministic, so the same
data always produces the same shares.

**A7 — Where the data lives is `plan`'s.** `[assumed — refine, not asked]` The path and the file
format are not fixed here, and no acceptance criterion will name them. AC4 is written so that it
can be decided by running the listing commands in a fresh process and comparing the output, which
is what the stakeholder actually cares about ("data must survive between runs"). Reason: they
said nothing about where their data should sit, and any answer would be the same whoever they
were. `plan` must document the location so a person can find their own data.

---

## Round 2 — what refinement considered asking, and did not

Refinement resumed with three answers in hand and re-ran the Definition of Ready. R4 and R10
still needed work, and the question is whether closing them needs the stakeholder again. Applying
the skill's own ownership test, item by item, it does not — and the candidates are written down
so that "nothing was asked" is auditable rather than merely asserted.

| Considered asking | Verdict | Why |
|---|---|---|
| Should the description be **required** rather than optional? | **not asked** | Already answered. They were shown option B (required, no date) and option C (optional, with date) and chose C. Re-asking would tell them their answer was not heard (F-023). Recorded as theirs, in `Q-002`. |
| What should `--date` accept, and is a future date allowed? | **not asked** — A8 below | Implementation-only. The answer would be the same whoever the stakeholder was, and nothing they would ever notice turns on it. Decided and marked `[assumed]`. |
| What does an empty `--description ""` mean? | **not asked** — A9 below | Same. Two readings, neither with product stake; the tool must simply not have an unstated behaviour (R10). |
| What do the listings print when the store is empty? | **not asked** — A10 below | Same. This is output wording, which is a team call; what matters for R4 is that a criterion names something decidable, which AC9 now does. |
| In what order do the listings print? | **not asked** — A11 below | Same, and it is forced anyway: AC4 requires byte-identical output across runs, so the order has to be fixed by a rule. |
| May a person's name be empty or whitespace-only? | **not asked** — A12 below | Same. `intake` and round 1 already settled that a name is the identifier, stripped and compared exactly; the empty case is the boundary of a decision already taken. |
| Which sharer absorbs an indivisible remainder? | **not asked, and not decided here** | Implementation-only, and routed to `plan` rather than settled by refinement, because it is a design decision with a real trade-off. It is in `item.md` under open design questions for `plan`, per R10's "recorded as deliberately unconstrained with who left it so". |
| Where does the data file live, and in what format? | **not asked, and not decided here** | Same — `plan`'s, and already recorded there. |

Nothing on this item is `[unresolved]`. No question was asked and abandoned.

## What refinement settled in round 2

Same rule as A1–A7: each would have the same answer whoever the stakeholder was, and each is
marked `[assumed]` because **the stakeholder was not asked**. None is reported as something they
said.

**A8 — Dates.** `[assumed — refine, not asked]` `--date` takes a calendar date written
`YYYY-MM-DD`. Anything that is not one — `2026-13-01`, `yesterday`, `01/08/2026` — is a refusal
per A2. A date is **not** otherwise constrained: a future date is accepted, because a person
recording something they have already committed to is ordinary and refusing it would invent a
rule nobody asked for. When `--date` is omitted the expense takes the date on which it is
recorded, which is what `Q-002` chose. Reason: `YYYY-MM-DD` is unambiguous, sorts correctly and
is what the standard library parses without help.

**A9 — An empty description is no description.** `[assumed — refine, not asked]`
`--description ""` records the same thing as omitting the flag. Reason: the description is
optional, so there is no difference worth having between "absent" and "empty", and refusing it
would be a refusal with nothing behind it.

**A10 — The empty listings say so.** `[assumed — refine, not asked]` `person list` with no people
recorded exits 0 and prints `no people`; `expense list` with no expenses exits 0 and prints
`no expenses`. Reason: an empty store is not an error, so exit 0; and printing nothing at all
leaves a person unable to tell "none recorded" from "the command did nothing". The exact strings
are fixed here rather than left open so that AC9 is decidable by someone with a terminal;
`plan` may print more around them but must keep those strings.

**A11 — Listings print in the order things were recorded.** `[assumed — refine, not asked]`
Reason: AC4 requires two runs over the same data to print byte-identical output, so *some* order
has to be fixed. Insertion order is the one that needs no extra decision and matches what a
person who typed the entries expects to see.

**A12 — A person's name must have something in it.** `[assumed — refine, not asked]`
`person add ""` and `person add "   "` are refusals per A2. Reason: A3 already makes the
whitespace-stripped name the identifier, so a name that strips to nothing has no identifier at
all. This is the boundary of a decision already taken, not a new one.

## Acceptance criteria — as installed in `item.md`

These are the criteria this execution wrote into the item. Each names a command to run and the
verdict that follows, which is what R4 and the `criteria-are-decidable` gate require. Where a
criterion rests on something the stakeholder said, the question is cited.

- **AC1** — `python3 -m expenses person add Ana` exits 0; `python3 -m expenses person list` then
  exits 0 and its stdout contains a line for `Ana`. Running `person add Ana` a second time exits
  non-zero, writes a message naming `Ana` to stderr, and `person list` still shows `Ana` exactly
  once. `person add ana` after `person add Ana` exits 0, and `person list` then shows both, since
  a person is their name compared exactly (A3).
- **AC2** — with `Ana`, `Ben` and `Cara` added, `python3 -m expenses expense add --amount 30
  --paid-by Ana --shared-by Ana,Ben,Cara` exits 0, and the expense is recorded with amount 30.00,
  payer `Ana`, sharers `Ana`, `Ben` and `Cara`, and an **equal** share of 10.00 each, the three
  shares summing to exactly 30.00. *(equal split: `Q-001`)*
- **AC3** — `python3 -m expenses expense list` exits 0 and prints one entry per recorded expense,
  each showing that expense's amount, its payer, its sharers, its date and its description, in
  the order the expenses were recorded. *(date and description: `Q-002`; order: A11)*
- **AC4** — after every command above has exited, running `python3 -m expenses person list` and
  `python3 -m expenses expense list` again in a new process prints byte-identical stdout to the
  previous run.
- **AC5** — `expense add --amount 30 --paid-by Ana --shared-by Ana,Dan`, with no person `Dan` in
  the group, exits non-zero, writes a message naming `Dan` to stderr, and leaves `expense list`
  printing byte-identical stdout to before the attempt. The same holds for
  `--paid-by Dan --shared-by Ana,Ben`, where the unknown name is the payer.
- **AC6** — each of `--amount 0`, `--amount -4`, `--amount abc`, `--amount 1.005`,
  `--shared-by ""`, `--shared-by Ana,Ana`, `--date 2026-13-01`, `--date yesterday`,
  `person add ""` and `person add "   "` exits non-zero, writes a message to stderr, and leaves
  both `person list` and `expense list` printing byte-identical stdout to before the attempt.
  *(A4, A5, A8, A12)*
- **AC7** — `expense add --amount 12 --paid-by Ana --shared-by Ana,Ben` with neither
  `--description` nor `--date` exits 0 and records the expense with the current date and no
  description; `expense list` shows that entry carrying today's date. The two flags are
  independent: `--description taxi` alone, and `--date 2026-08-01` alone, each exit 0 and record
  the value given with the default for the other. `--description ""` records the same thing as
  omitting it. *(`Q-002`, A8, A9)*
- **AC8** — `expense add --amount 10 --paid-by Ana --shared-by Ana,Ben,Cara`, an amount that does
  not divide evenly by three, exits 0 and the three recorded shares sum to exactly 10.00. Running
  the same sequence of commands against a fresh empty store a second time prints byte-identical
  `expense list` output, so which sharer carries the extra unit is fixed by a rule rather than by
  chance. The rule itself is `plan`'s and this criterion does not name one. *(A6, and `plan`'s
  open design question)*
- **AC9** — against an empty data store, `python3 -m expenses person list` exits 0 and its stdout
  contains `no people`, and `python3 -m expenses expense list` exits 0 and its stdout contains
  `no expenses`. *(A10)*

## Definition of Ready — the verdict this execution recorded

Re-assessed on `item.md` as this execution leaves it. The table near the top of this file is
`intake`'s draft as round 1 found it, and is left as written — it is a record of where the item
stood, not a claim about where it stands.

| # | Verdict | Why |
|---|---------|-----|
| R1 | **pass** | frontmatter complete; `type`, `epic` and `priority` all set |
| R2 | **pass** | unchanged from round 1: role, capability and "so that" all present |
| R3 | **pass** | AC1–AC9, each labelled and a checkbox |
| R4 | **pass** | every criterion names a command and the observation that settles it. No criterion contains an unmeasurable adjective; the two places where wording could have drifted — the empty listings and the remainder — are fixed by exact strings (A10) and by a byte-identical repeat run (AC8) rather than by an adjective |
| R5 | **pass** | `## Out of scope` names five things, including deleting and editing, both with the stakeholder's own words on them |
| R6 | **pass** | all three questions on this item are `answered`; none is open |
| R7 | **pass** | no `depends-on`; nothing is unfinished ahead of it |
| R8 | **pass** | this file, at `status: recorded`, holding both rounds verbatim with every answer tagged |
| R9 | **pass** | unchanged from round 1: one data model, one store, four commands over it |
| R10 | **pass** | every combination the item introduces is now stated somewhere. `--description` × `--date`, present or absent: AC7. Bad amounts, bad dates, empty and duplicate sharers, empty names: AC6. Unknown payer and unknown sharer: AC5. Duplicate person and case-differing person: AC1. Empty store: AC9. Uneven split: AC8. Deleting and editing: `## Out of scope`. Deliberately unconstrained, and recorded as such with who left them so: the remainder rule and the store's path and format, both named in `## Notes` as `plan`'s |

## Override

None. No criterion has been overridden, and the item is not being passed to `ready`.

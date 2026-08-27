---
status: recorded
---

# Refinement Q&A — WI-0002

`status: recorded`. **This round asked the stakeholder nothing**, and that is a decision with a
reason rather than an omission. The one question on this item that carried product stake was
already put to them and answered — `EP-001/Q-002`, which settled that "who owes whom" means a
list of payments — and its answer went further: it said explicitly that the settlement *rule* is
not theirs to decide. Everything else this round had to close is a naming, wording or arithmetic
call whose answer would be the same whoever the stakeholder was.

So this file records three things: where the item stood against the Definition of Ready, what the
stakeholder has already said that binds this item (verbatim, tagged `[human]`), and what
refinement settled on its own authority (tagged `[assumed]`, each with the reason it was not
theirs to decide). Nothing below is reported as something a person said unless it is tagged
`[human]` and quoted.

---

## Definition of Ready — where the item stood, criterion by criterion

Assessed against `spec/dor-dod.md` §1, on `item.md` as `answer-questions` left it on
2026-08-26T23:31:59Z.

| # | Verdict | Why |
|---|---------|-----|
| R1 | **pass** | `id`, `type`, `epic`, `priority`, `created`, `updated` all present and set; `depends-on` names WI-0001 |
| R2 | **pass** | `## Story` names the role (someone who shares costs with friends), the capability (ask the tool who owes whom at any point) and the outcome ("so that we can settle up without anybody doing the arithmetic by hand") |
| R3 | **pass** | four criteria, `AC1`–`AC4`, each a checkbox |
| R4 | **FAIL** | every criterion says "a documented command" and names none, so nobody with a terminal can run one. AC2 says the command "prints that no payments are needed" without saying what it prints. AC3 states a property with no dataset and no procedure to check it against. AC4 says "the same payments in the same order" without saying how sameness is observed |
| R5 | **pass** | `## Out of scope` names four things, including net positions per person, which a reader could reasonably assume was included |
| R6 | **pass** | no question has ever been filed on this item; none is open |
| R7 | **pass** | `depends-on: WI-0001`, which is `done` |
| R8 | **FAIL** | this file did not exist |
| R9 | **pass** | one coherent change: one read-only command over the data WI-0001 already stores. There is nothing here to split — a settlement list without the arithmetic behind it is nothing, and the arithmetic without the printing is unobservable |
| R10 | **FAIL** | the command this item introduces has cases nothing states: no people at all; people but no expenses; expenses that leave everybody square; a person added after the expenses, whose position is zero; a payer who is not among the sharers; an expense whose amount does not divide evenly; and whether running the command writes anything |

R4, R8 and R10 are what this round closes. R8 closes when this file reaches `recorded`. R4 and
R10 close on the decisions recorded below and the criteria rewritten from them.

---

## What the stakeholder has already said that binds this item

Quoted from the answered question files, not re-asked. Re-asking a stakeholder something they
already answered is the fastest way to lose them (F-023), and all three of these are on the
record with their own provenance.

### The shape of the answer — `EP-001/Q-002`

> [human] The list of payments that settles it — that's what actually saves us the arguing after
> a trip.

Option B of three. The tool prints **specific payments**, not each person's net position; option
C (both) was available and not taken. This is the criterion AC1 is written against, and it is why
`## Out of scope` still refuses to print positions.

That answer also settled who owns the rest of the design, in the record's own words: *"What the
rule is — which of several equally valid settlements to prefer, and in what order to print it —
is not decided here and is not the stakeholder's to decide; it is refinement's, and then
`plan`'s."* Everything under "What refinement settled" below is taken under that delegation, and
it is why this round filed no question.

### How an expense divides — `WI-0001/Q-001`

> [human] Equal split, keep it simple. If a bill's uneven we'll just enter it as separate
> expenses.

Every figure this item prints follows from this. A person's position is what they paid minus an
equal share of every expense they are named a sharer in. There are no per-person amounts and no
weights to handle, and no arithmetic decision is left over: the indivisible-unit rule was decided
by `plan` on WI-0001 and is recorded in ADR-0003.

### What is not wanted — `WI-0001/Q-003`

> [human] Hadn't really thought about it, but if I have to pick — being able to delete a mistake
> matters more to me than editing one. Timing's up to you, doesn't need to hold up the
> who-owes-whom feature.

Relevant here only as a boundary: deleting is WI-0004's, and *"doesn't need to hold up the
who-owes-whom feature"* is why WI-0004 depends on this item rather than the other way round.
Nothing in this item removes or amends anything.

---

## Round 1 — what refinement considered asking, and did not

The skill's ownership test, applied to each gap in turn. The candidates are written down so that
"nothing was asked" is auditable rather than merely asserted.

| Considered asking | Verdict | Why |
|---|---|---|
| What should the command be called? | **not asked** — B1 below | Naming is a team call, and the same one was taken without asking on WI-0001 (A1 in that item's Q&A). Nothing about what the tool is *for* turns on the word. |
| Should the settlement minimise the number of payments? | **not asked** — B3 below | This is precisely "which of several equally valid settlements to prefer", which `EP-001/Q-002`'s answer put on refinement and `plan`. Asking anyway would tell them their answer was not heard. |
| May the tool tell Ana to pay Cara when they never shared an expense? | **not asked** — B3 below | Same question wearing different clothes: it is a property of which settlement is chosen. It is the one consequence of B3 a reader might not expect, so it is recorded in `## Out of scope` rather than left to be discovered. |
| What should the command print when there is nothing to settle? | **not asked** — B4 below | Output wording, a team call — the same reasoning that fixed `no people` and `no expenses` on WI-0001 (A10 there). What R4 needs is an exact string, not a preferred one. |
| What does a payment line look like? | **not asked** — B5 below | Same. Fixed here only so AC1 is decidable by someone with a terminal. |
| In what order are the payments printed? | **not asked, and not decided here** | Implementation-only, and forced anyway: AC4 demands byte-identical output across runs, so *some* order must be fixed by a rule. Which rule is `plan`'s, and it is recorded in `## Notes` as such. |
| Should asking who owes whom record anything? | **not asked** — B6 below | There is no reading of the item under which it should. `## Out of scope` already refuses "recording that a debt has been paid off", and every other reading is a bug. Made decidable rather than assumed, as AC5. |
| Should the list be filterable — by trip, by date, by person? | **not asked** | Nobody has asked for it, on this item or in `IDEA.md`. Inventing a flag to ask about would be inventing scope. Named in `## Out of scope` so the absence is visibly a decision. |

Nothing on this item is `[unresolved]`. No question was asked and abandoned, and no question was
filed to anyone.

---

## What refinement settled without asking

Each of these would have the same answer whoever the stakeholder was, or is a naming or wording
call. Every one is marked `[assumed]` because **the stakeholder was not asked**; none is being
reported as something they said.

**B1 — The command.** `[assumed — refine, not asked]`

    python3 -m expenses settle

A third top-level command beside `person` and `expense`. It takes no sub-action and no flags,
because there is exactly one thing it does. Reason: R4 cannot pass while every criterion says "a
documented command", and what things are called is a team call — the same authority under which
`python3 -m expenses` itself was chosen on WI-0001. `settle` is the vocabulary the record already
uses for this output ("a list of payments that settles the group", `EP-001/Q-002`).

The one risk in the name is that `settle` could be read as *doing* the settling — recording that
the money moved — which this item explicitly does not do. That risk is not left to the reader's
good sense: B6 makes it a behaviour, and AC5 makes it decidable. `plan` may propose a different
name with a recorded reason before the item is implemented, but may not change it quietly, since
the criteria are written against this one.

**B2 — What a position is.** `[assumed — refine, not asked]` A person's **position** is the sum of
the amounts of the expenses they paid, minus the sum of the shares recorded against them across
all expenses. Positive means the group owes them; negative means they owe the group. Reason: this
is not a choice — it is the only reading of the equal-split rule the stakeholder gave in
`WI-0001/Q-001`. It also needs no rounding: WI-0001 stores each expense's shares as whole minor
units that already sum to exactly the amount paid, so every position is exact and all the
positions sum to exactly zero. Nothing in this item creates or loses a unit, and no new rounding
rule is needed or permitted.

**B3 — Which settlement is printed.** `[assumed — refine, not asked]` Taken under
`EP-001/Q-002`'s delegation. Refinement fixes the properties; `plan` fixes the algorithm.

The printed list must satisfy all of:

- every amount is strictly greater than zero;
- no name appears both as a payer and as a receiver — the list is computed from the positions of
  B2, not from who shared what with whom;
- a person whose position is zero appears nowhere in it;
- the number of payments is at most one fewer than the number of people whose position is not
  zero;
- for every person, what they pay in the list minus what they receive in it equals the negative
  of their position — that is, the list settles the group exactly.

Reason: these are what make the output *useful* rather than merely correct, they are forced by
"who owes whom" being a list of payments, and the last of them is the property AC3 already
demanded. Which debtor is matched against which creditor, and in what order the lines print, is
left to `plan`, constrained only to be deterministic.

The second property has a consequence worth naming: the list may tell Ana to pay Cara even though
no expense involved them both. That is inherent to settling a group in few payments rather than
unwinding every pairwise debt, and it is what the stakeholder chose the shape of when they chose
option B. It is recorded in `## Out of scope` so that a reader can tell it from an oversight.

**B4 — When there is nothing to settle.** `[assumed — refine, not asked]` If every position is
zero — no people recorded, or people but no expenses, or expenses that happen to leave everybody
square — the command prints exactly

    no payments needed

on stdout and exits 0. Reason: nothing here is an error, so exit 0; and printing nothing at all
would leave a person unable to tell "the group is square" from "the command did nothing", which
is the same reasoning that fixed `no people` and `no expenses` on WI-0001. The exact string is
fixed so that AC2 is decidable; `plan` may print more around it but must keep it.

**B5 — What a payment line looks like.** `[assumed — refine, not asked]` One payment per line:

    Ben pays Ana 10.00

The payer's name as recorded, the word `pays`, the receiver's name as recorded, and the amount in
the same two-decimal form the rest of the tool already prints. Reason: fixed only so that AC1 can
be decided by comparing output rather than by interpreting it. Names are printed exactly as they
were recorded, which follows from a person being their name compared exactly (WI-0001).

**B6 — Asking is not doing.** `[assumed — refine, not asked]` The command reads and prints. It
writes nothing, changes nothing on disk, and where no data file exists it does not create one —
which is already how the two listing commands behave. Reason: the item is about answering a
question, and `## Out of scope` already refuses to record that a debt was paid off. Any write
would be a defect; making it a criterion (AC5) is what stops the name `settle` from quietly
acquiring a meaning nobody chose.

**B7 — What is deliberately left unconstrained.** `[assumed — refine, not asked]` Nothing is said
about how many people or expenses the command must cope with, or how quickly. Reason: the
stakeholder described a friend group, `docs/product/vision.md` records one person on one machine,
and a threshold nobody asked for is a threshold nobody believes. Recorded here and in `## Notes`
as unconstrained, with refinement named as who left it so, rather than left invisible.

---

## Acceptance criteria — as installed in `item.md`

Each names a command to run and the verdict that follows. `$S` below is a scratch data file, set
with `EXPENSES_STORE`, which WI-0001 documents as a supported way to keep a dataset separate.

- **AC1** — against a store holding `Ana`, `Ben`, `Cara` and one expense of 30 paid by Ana and
  shared by all three, `python3 -m expenses settle` exits 0 and its stdout is exactly two lines
  which, sorted, are `Ben pays Ana 10.00` and `Cara pays Ana 10.00`.
- **AC2** — three stores, each of which prints exactly `no payments needed` and exits 0: one where
  nothing has been recorded; one where `Ana` and `Ben` have been added and no expense has; and one
  where `Ana` and `Ben` have been added and the only expense is 10 paid by Ana and shared by Ana
  alone, so that every position is zero.
- **AC3** — the settlement-exactness properties of B3, checked on a five-person dataset that
  contains an uneven split, an expense whose payer did not share in it, and a person who shared
  nothing. Decidable by arithmetic on the printed lines; the expected figures are stated in the
  criterion so no interpretation is needed.
- **AC4** — the same store, two fresh processes, byte-identical stdout.
- **AC5** — the data file's bytes are unchanged across a `settle` run, and a `settle` against a
  path with no data file leaves that path non-existent.
- **AC6** — `README.md` documents the command, its output and its no-payments case.

## Definition of Ready — the verdict this execution recorded

Re-assessed on `item.md` as this execution leaves it. The table near the top of this file is left
as written; it records where the item stood, not where it stands.

| # | Verdict | Why |
|---|---------|-----|
| R1 | **pass** | frontmatter complete; `type`, `epic`, `priority` set; `depends-on` names WI-0001 |
| R2 | **pass** | unchanged: role, capability and "so that" all present |
| R3 | **pass** | AC1–AC6, each labelled and a checkbox |
| R4 | **pass** | every criterion names the commands that set it up, the command that settles it, and the observation. The three places wording could have drifted are fixed by exact strings (B4), by an exact expected pair of lines (AC1) and by byte comparison (AC4, AC5) rather than by an adjective. No criterion contains an unmeasurable adjective |
| R5 | **pass** | `## Out of scope` names seven things, including net positions, filtering, and the pairwise-debt reading of the output |
| R6 | **pass** | no question exists on this item, so none is open or blocking |
| R7 | **pass** | the only entry in `depends-on` is WI-0001, which is `done` |
| R8 | **pass** | this file, at `status: recorded`, holding what was already answered verbatim and what refinement settled, each tagged |
| R9 | **pass** | unchanged: one read-only command over data that already exists |
| R10 | **pass** | every case the command introduces is now stated somewhere. No people, people without expenses, and everybody square: AC2. A person with a zero position standing among people with non-zero ones: `Eve` in AC3's dataset, who must appear nowhere in the output. A payer who did not share in what they paid for: AC3's second expense, paid by Ben and shared by Cara and Dan. An amount that does not divide evenly: AC3's third expense, 10 between three. Whether the command writes anything: AC5. Deliberately unconstrained, with who left it so: the size of the group and how fast the command runs (B7, refinement), and which debtor is matched to which creditor and in what order the lines print (B3, left to `plan`) |

## Override

None. No Definition of Ready criterion has been overridden.

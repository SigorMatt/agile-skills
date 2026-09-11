---
status: recorded
---

# Refinement Q&A — WI-0006

`status: recorded`, as of round 2. Four questions were written down and put to the stakeholder,
and on 2026-09-11 all four came back answered; `## Answers — round 1` below carries the replies
verbatim and `answer-questions` propagated them into `item.md`. Round 2, recorded under
`# Round 2` at the foot of this file, rewrote the criteria against those answers, settled the two
things round 1 had left itself, spent the one delegation it had named in advance, and walked the
Definition of Ready criterion by criterion. The exchange below is what was actually said, and
round 2 put no further question to the stakeholder — so the conversation on this item is finished
and the field says so (`spec/dor-dod.md` R8).

The first of the four asks whether this item should exist at all. That is not a formality: it
is the instruction `answer-questions` left in the item's own `## Notes` — *"`refine`'s first job
is to put it to the stakeholder — including the option of closing it"* — and it is the honest
thing to do with the one item in this epic nobody asked for.

## What the Definition of Ready says is missing

Read criterion by criterion against `spec/dor-dod.md` §1, before the questions were written.

| # | Verdict | Why |
|---|---------|-----|
| R1 | pass | Frontmatter complete; `type`, `epic`, `priority` set; `arose-from: WI-0002/Q-002` resolves. |
| R2 | pass | `## Story` names the role, the capability (look at the spends recorded against an envelope) and the outcome (*"so that I can find the one I am wondering about"*). |
| R3 | pass | Three criteria, `AC1`–`AC3`, each a checkbox. |
| R4 | **fail** | AC1 says *"There is an `envel` command that lists the spends recorded against a named envelope"* — no command name, no ordering, no output form, and no statement of how many spends are in scope. AC2's *"a line saying so"* names no line. AC3 is the closest to decidable and still names no command. None of the three can be settled from a terminal. |
| R5 | pass | Three exclusions, and the first — that the monthly summary is untouched — is one a reader would reasonably assume was included. |
| R6 | **fail by construction** | Four blocking questions are now open on this item; this clears when they are answered. |
| R7 | pass | `depends-on` is empty. `WI-0002`, which this item needs for there to be spends to list, is `done`, so the dependency is satisfied either way; recording it in the frontmatter belongs with the criteria rewrite in round 2. |
| R8 | **fail** | This file declares `status: agenda`. |
| R9 | **pass, provisionally** | One command that prints a listing is one coherent change under every option offered. The one answer that could change this is Q-004 option C — a running balance implies starting from the beginning, which sits badly with Q-002's single month; if both come back that way, round 2 reconsiders the split rather than building a contradiction. |
| R10 | **fail** | The item introduces a command with at least two optional things — which envelope, which month — and nothing states what they do together, because neither is chosen yet. Q-002 and Q-003 are those two axes and Q-004 is a third; round 2 writes the combinations out. |
| R11 | pass | No criterion on this item counts anything. Nothing to measure. |
| R12 | pass, vacuously | No `[assumed]` answer recorded yet, so no delegation spent. Two decisions anticipated below, both named in advance. |

## Questions put to the stakeholder — round 1

Filed as `questions/Q-001.md` through `questions/Q-004.md`, all `addressed-to: human`, all
`blocking: true`, all `status: open`. Four artifacts, one conversation: each `## Context` carries
the *"`WI-0006`, round 1, question N of 4"* frame, questions 2 to 4 each say to ignore them if
question 1 closes the item, and Q-004 says that is all of them (`spec/question.md` §2).

1. **Q-001 — do you want this at all, or should it be closed?** Three options including closing
   it, and the argument against building it is made from the stakeholder's own words rather
   than left implicit. It also says plainly that `WI-0005` is **not** a reason to say yes,
   because `WI-0005/Q-001` puts that need to them directly.
2. **Q-002 — all the spends, or a month's?** The output of option A grows without limit; option
   B is the shape `envel summary` already has.
3. **Q-003 — must an envelope be named, or can you ask across all of them?** The case that
   argues for "all" is the one the stakeholder actually described doing: checking a card
   statement, where the envelope is the thing you do not know.
4. **Q-004 — spends only, or everything that moved the envelope?** The cross-answer one. At
   `WI-0003/Q-001` they said *"I won't use a report whose rows don't add up… a number I can't
   account for costs me an evening."* A spends-only listing of an envelope does not add up to
   its balance, because income and moves are missing. That answer was given about the monthly
   summary and this is a different report, so the rule is put to them rather than applied.

## Why these four went to the stakeholder and nothing else did

`refine` step 3, question by question. Q-001 is scope in its purest form — whether a piece of
work exists. Q-002, Q-003 and Q-004 each change how much of their data the tool puts on screen,
which is the axis they have pushed back on twice (*"that is the spreadsheet I am trying to get
away from"*, `EP-001/Q-003`), so none of them has an answer that would be the same whoever the
stakeholder was.

Two decisions are **not** going to them, recorded here so the licences are visible before they
are spent rather than after:

- **The ordering of the listing** — oldest first, by the date the spend happened, with the
  recording order breaking a tie. This is the project's delivered convention rather than a new
  decision: `WI-0003` AC10 orders the summary's rows and cites `WI-0001` AC3 for it as an
  existing convention. It is not taken under a delegation at all; it is taken under precedent,
  and if the stakeholder disagrees the disagreement lands on this item's AC and costs one
  amendment.
- **The spelling of the command** — the subcommand's name, whether the envelope and the month
  are plain words or named options, the wording of a refusal. Settled by `WI-0003/Q-004`:
  *"I'd rather everything in this tool be typed the same way than have one command that's
  special."* It cannot be fixed until Q-002 and Q-003 say what arguments exist, so it is round
  2's, and when taken it will carry `**Under delegation:** WI-0003/Q-004 — argument style: a
  plain word for the argument a command normally takes, a named option for the one it rarely
  does` (R12).

Nothing was routed to `plan`. The whole of this item is what appears on a screen, so every open
choice on it is one the stakeholder can see.

## What happens next

The item moved to `awaiting-answer` with `resume-to: draft`. All four replies have arrived,
`Q-001` came back as **build it**, and `answer-questions` has propagated them; the item returns to
`draft`. Round 2 rewrites the criteria against the answers — `answer-questions` has recorded them
as AC1–AC7, which is a record of what was decided and not yet a Definition-of-Ready pass — states
the combinations R10 wants, settles the one thing these answers leave open (below), records the
two decisions above, and sets this file to `status: recorded`.

## Answers — round 1

Received 2026-09-11, all four, verbatim. Consumed by `answer-questions`
(`questions/Q-001.md` … `Q-004.md`, each `status: answered`, `answered-by: human`).

**Q-001 — should this item exist?** → **A**, build it.

> [human] A — build it. You have not over-read me: I meant reading those notes back, and when I am
> checking a month against the statement I need to see what is behind an envelope's balance. Keep
> it small and keep it last. It does not reopen the monthly summary — I still don't want individual
> spends in that.

**Q-002 — how far back does the listing go?** → **B**, a month at a time.

> [human] B — a month at a time, this month unless I name one, and named the same way as the
> summary. I work a month at a time and I don't want a command whose output gets longer every year
> I use it.

**Q-003 — must an envelope be named?** → **B**, the envelope is optional.

> [human] B — let me leave the envelope out and see the lot. The case I actually have is a 34.99 on
> the statement I cannot place, and that is precisely the moment I cannot name an envelope. One
> month across ten envelopes is a page I can read; that is why I want the month on it.

**Q-004 — spends only, or everything that moved the envelope?** → **B**, income and moves too.

> [human] B — everything that moved the envelope, with each line saying which kind it is. Yes, that
> rule travels: a list I cannot add up costs me an evening whichever report it is on. I don't need
> a running balance down the side.

## Cross-answer check — round 1, on the replies

Written on each question file as it was consumed; the per-ID verdicts are there in full. Collected
here because this is the page a reader following this item's story passes through.

- **No conflict was found.** The pair the questions were filed to watch — `EP-001/Q-003`,
  *"I definitely don't want every individual spend listed"*, against an item whose whole purpose is
  listing individual entries — was drawn by the stakeholder themselves, unprompted, in `Q-001`'s
  reply: *"It does not reopen the monthly summary — I still don't want individual spends in that."*
  The sentence is about that report, and they have now said so in their own words. Nothing under
  `docs/` sourced to it was edited.
- `Q-004`'s reply **extends** `WI-0003/Q-001` rather than contradicting it. That answer — *"I won't
  use a report whose rows don't add up"* — was given about the monthly summary, and round 1 asked
  whether the rule travelled instead of assuming it. They said it does: *"whichever report it is
  on."* The monthly summary itself is untouched.
- `Q-002` and `Q-003` apply `EP-001/Q-004`'s month convention and `WI-0003/Q-004`'s consistency
  preference to a second command. Neither reopens `envel summary`.
- **One sequencing tension, and it is not a conflict.** *"Keep it small and keep it last"*
  (`Q-001`) sits beside *"That does mean the listing command has to exist, and I am saying yes to
  that separately"* (`WI-0005/Q-001`). *Last* is about size and priority; the dependency is about
  the order the work can be done in. Both can stand, and which item is built first is `refine`'s
  and `next`'s to settle — it is recorded in both items' `## Notes` rather than put back to the
  stakeholder as a contradiction they did not make.

## What round 1's answers left for round 2

1. **How a single month's listing adds up.** `Q-004` asks for a list that reconciles and `Q-002`
   asks for a list that covers one month; the money carried in from earlier months is not among the
   lines. Round 1 said in `Q-004`'s cross-answer check that this part was the team's to decide —
   *"We would handle that by printing the carried-in figure as an opening line, the way `WI-0003`
   AC3 already reconciles a month"* — so round 2 decides it and writes it as a criterion.
   `answer-questions` left it open rather than taking it, because it is what the stakeholder reads
   on screen and `refine` had claimed it.
2. **Whether the reference of `WI-0005/Q-001` is per-envelope or global.** AC4's envelope-less
   listing is what makes it matter. The same note is on `WI-0005`.
3. **The spelling of the command**, under the `WI-0003/Q-004` delegation named above, now that
   `Q-002` and `Q-003` have said what arguments exist.
4. **R10's combinations**, which are now writable: a named envelope or none, the current month or a
   named one, an empty result, an envelope that does not exist.

---

# Round 2

Held 2026-09-11, against the four answers `answer-questions` had propagated and against the
`WI-0005/Q-008` answer the stakeholder gave on a sibling item in between. The stakeholder is not
in this session (`SIMULATION-NOTICE.md`); this round asked them nothing, because everything it
had to settle was either already answered by them, covered by a licence they had granted, or
named in advance by round 1 as the team's to take.

## Definition of Ready — round 2's walk

| # | Verdict | Why |
|---|---------|-----|
| R1 | pass | frontmatter complete; `type`, `epic`, `priority` set; `arose-from: WI-0002/Q-002` resolves. `validate-workspace` agrees |
| R2 | pass | `## Story` names the role (a person budgeting their own money at a terminal), the capability (look at what has been recorded against an envelope) and the outcome (*"so that I can find the entry I am wondering about and see what is behind the envelope's balance"*) |
| R3 | pass | fifteen criteria, `AC1`–`AC15`, each a checkbox |
| R4 | **pass** | every criterion names a line to type and an outcome to observe; `## How each criterion is decided` below gives the command and the verdict for each. Round 1's failure was that AC1 named no command at all — the command is now `envel entries`, with its arguments, its ordering, its output fields and its refusals all stated |
| R5 | pass | six exclusions, and two of them — that the monthly summary is untouched, and that the envelope-less listing carries no opening and closing figure — are things a reader would reasonably assume were included |
| R6 | pass | no question is open on this item. Round 1's four are answered and this round filed none |
| R7 | pass | `depends-on` is empty and both items this one needs are `done` — `WI-0001` for envelopes and `WI-0002` for entries to list. The dependency that matters runs the other way: `WI-0005` records `depends-on: WI-0006`, which is what sequences the two |
| R8 | pass | this file declares `status: recorded`, and the exchange below it is what was said |
| R9 | **pass** | one command that prints one listing. Round 1 marked this provisional against one risk — `Q-004` option C, a running balance, which implies starting from the beginning and sits badly with `Q-002`'s single month. The stakeholder chose B and said *"I don't need a running balance down the side"*, so the risk did not arrive and the provisional verdict becomes a plain one |
| R10 | **pass** | the combinations are written out in `## R10 — what the options do together` below: envelope named or not, `--month` given or not, an empty result under each, an envelope that does not exist, a month that is refused, and a move seen from each side |
| R11 | pass | no criterion counts a project artefact. AC6's *"two lines"* and AC2's *"one line"* count the tool's own output, which is what the criterion is about; AC14 names `WI-0003`'s criteria by ID and asks for a read of them rather than a count of tests; AC15 names the refusals and successes it checks rather than counting them |
| R12 | **pass, one licence spent and three assumptions taken under none** | recorded in `## Decided this round, and by what authority` |

## Decided this round, and by what authority

- **`envel entries [<envelope>] [--month <YYYY-MM>]`.** `[assumed]`.
  **Under delegation:** `WI-0003/Q-004` — argument style and the naming of commands and options:
  *"I'd rather everything in this tool be typed the same way than have one command that's
  special."* The licence is spent this way, and what was weighed is worth writing down because
  the obvious alternative is the stakeholder's own `envel summary`:
  - The envelope is the plain word, because it is the argument this command is *about*.
  - The month is `--month`, a named option, even though `envel summary` takes its month as a
    plain word. The delegation's own reading — recorded when it was spent on `WI-0005` — is that
    the argument a command normally takes is a plain word and the one it rarely takes is a named
    option. For `summary` the month is the only argument and the stakeholder said naming it is
    *"the normal case"*; here they chose the opposite default, *"this month unless I name one"*
    [src: WI-0006/Q-002], so the month is the rare one.
  - Two optional plain words — `envel entries [<envelope>] [<month>]` — was rejected rather than
    overlooked. It cannot be disambiguated without a rule of our own invention, because envelope
    names have their characters unrestricted [src: WI-0001/Q-004] and an envelope may legally be
    called `2026-08`. A rule that reads a bare word as a month would make that envelope
    unreachable from this command, which is a rule about *their* data taken on their behalf.
  - The subcommand is `entries` rather than `list`, which already means *the envelopes and their
    balances* [src: WI-0001 AC3 "one line per envelope, each line containing that envelope's name and the amount currently in it"].
  If the stakeholder dislikes any of it, the cost is an amendment to AC1 and AC15 and no design.
- **The ordering of the listing — oldest first, ties broken by the order entries were recorded**
  (AC8). `[assumed]`, under **no** delegation. Round 1 named this decision in advance, before the
  stakeholder was asked anything, and said plainly that nothing licensed it. What it is taken on
  is that the order has to be total for the listing to be reproducible, and the store's own order
  is the only tie-break available that does not invent a comparison [src: ADR-0002]. A
  disagreement lands on AC8 and costs one amendment.
- **How a month's listing adds up, with an envelope named** (AC9). `[assumed]`, under **no**
  delegation, and it is a promise being kept rather than a licence being spent: `Q-004`'s own
  `## Cross-answer check` told the stakeholder *"we would handle that by printing the carried-in
  figure as an opening line, the way `WI-0003` AC3 already reconciles a month"*, and they
  answered `Q-004` with that sentence in front of them.
- **And with no envelope named — no opening and closing figure** (AC10). `[assumed]`, under
  **no** delegation, and this half was *not* in front of them. The reason it was decided rather
  than asked: across ten envelopes there is no single balance for an opening figure to reconcile
  against, and per-envelope opening and closing lines on a page of interleaved entries would be
  the monthly summary with the individual entries put back into it — which is the one thing they
  have refused twice [src: EP-001/Q-003], [src: WI-0006/Q-001]. The case they described for this
  form is finding *"a 34.99 on the statement I cannot place"* [src: WI-0006/Q-003], which needs
  the entry and not the arithmetic. A disagreement lands on AC10 and costs one amendment.
- **Refusing a future month and an unreadable one** (AC13). `[assumed]`, under **no** delegation,
  taken on precedent: `WI-0003` AC9 and AC12 already do both for the only other month-keyed
  command, and the stakeholder's reason for the first is on the record — *"A page of figures with
  the wrong year at the top is exactly the sort of thing I'd read straight past, and I'd rather
  be stopped"* [src: WI-0003/Q-005]. An empty listing and a mistyped month would otherwise be
  indistinguishable, which is the failure that sentence is about. A disagreement lands on AC13.

**Nothing was routed to `plan`**, and one thing was written into `## Notes` for it: AC4's promise
that a reference is not moved onto another entry constrains how the number is produced, and the
note says so rather than leaving `plan` to discover it when `WI-0005`'s removal arrives.

**No question was put to the stakeholder this round.** Each candidate was tested against
`refine` step 3 and fell to one of the first three tests: the reference's numbering was *already
answered*, by them, on `WI-0005` [src: WI-0005/Q-008]; the command's spelling is *covered by a
standing delegation*; the ordering, the reconciliation and the month refusals were *named in
advance by round 1* as the team's, with where a disagreement lands written down. Filing any of
them would have cost the stakeholder a round trip for an answer they had given or delegated.

## R10 — what the options do together

| envelope | `--month` | what happens | criterion |
|----------|-----------|--------------|-----------|
| named | absent | that envelope's entries for the month today falls in, bracketed by an opening and a closing line | AC1, AC7, AC9 |
| named | given | the same, for the named month | AC1, AC7, AC9 |
| absent | absent | the envelopes together for the month today falls in, each line naming its envelope, no opening or closing figure | AC1, AC7, AC10 |
| absent | given | the same, for the named month | AC1, AC7, AC10 |
| named | either | the envelope exists but has nothing in the month: the opening and closing lines print and a line says there is nothing between them | AC9, AC11 |
| absent | either | nothing at all was recorded in the month: one line says so, exit 0 | AC11 |
| does not exist | either | refused on stderr naming what was typed, non-zero, nothing on stdout — and the envelope is checked before the month is | AC12 |
| either | later than this month, or unreadable | refused on stderr, non-zero, nothing on stdout | AC13 |
| either | either | a move touching the named envelope shows one line; with no envelope named both of its lines show | AC6 |
| either | either | wrong shape — an extra word, `--month` with nothing after it, an option this subcommand does not take | AC15 |

## How each criterion is decided

The `criteria-are-decidable` gate, criterion by criterion. Each is observed in a store of its own
— `ENVEL_FILE` pointing at a path that does not exist [src: ADR-0003] — set up with `envel new`,
`envel add`, `envel spend` and `envel move`, and read back with `envel entries`, `envel list` and
`envel summary`.

| AC | Run this | Verdict |
|----|----------|---------|
| AC1 | `envel entries`, `envel entries groceries`, `envel entries --month 2026-08`, `envel entries groceries --month 2026-08` | each exits 0 and prints a listing; the first two cover the month today falls in and the last two cover August |
| AC2 | `envel entries groceries` over a store with an income, a spend with a description, a spend without one, and a move | each line carries a reference, a date, a kind, the envelope, an amount in the `0.00` form; the described spend carries its description and the other does not |
| AC3 | record entries into two envelopes, then `envel entries` | no two lines carry the same reference, and the references do not restart at the second envelope |
| AC4 | `envel entries`, note the references; `envel spend` once more; `envel entries` again | every reference from the first run points at the same line's entry, and the new entry's reference is one none of them had |
| AC5 | an income typed today, a spend recorded `--on 2026-08-28`, then `envel entries --month 2026-08` and `envel entries` | the spend appears under `2026-08-28` in August's listing; the income appears under today's date in this month's |
| AC6 | `envel move groceries fun 10.00`, then `envel entries groceries`, `envel entries fun`, `envel entries` | the first shows one line out, the second one line in, the third both, same date and same amount in opposite directions |
| AC7 | `envel entries --month 2026-08` run twice with a September entry recorded in between | both runs print the same lines |
| AC8 | a store with two entries on the same date recorded in a known order, plus one earlier and one later | the listing reads earliest to latest and the two same-date entries appear in the order they were recorded; a second run is byte-identical |
| AC9 | an envelope holding 50.00 at the end of July, then 20.00 spent and 30.00 moved in during August; `envel entries groceries --month 2026-08` | the opening line reads 50.00, the closing line 60.00, and the lines between sum to +10.00; `envel list` agrees with the closing figure when the month is the current one |
| AC10 | `envel entries --month 2026-08` | no opening or closing figure is printed, and each line names its envelope |
| AC11 | `envel entries groceries --month 2026-01` on an existing envelope with nothing that month, then `envel entries --month 2026-01` | the first prints the opening and closing lines and a line saying there is nothing between them; the second prints one line saying so; both exit 0 with nothing on stderr |
| AC12 | `envel entries nosuch`, then `envel entries GROCERIES` | the first writes to stderr naming `nosuch` and exits non-zero with nothing on stdout; the second is the same listing as `envel entries groceries` |
| AC13 | `envel entries --month 2027-03`, `--month 2026-8`, `--month august`, `--month 2026-13`, `--month 2026-08-01` | each writes to stderr and exits non-zero with nothing on stdout |
| AC14 | `envel entries --help` output and a listing, read for a balance column; then `envel summary 2026-08` before and after this item, and `WI-0003`'s delivered tests | no running-balance column; the summary's output is unchanged; `WI-0003` AC1–AC14 re-read against `envel entries`' behaviour with the suite as evidence, and any criterion no test exercises alongside this command gets a covering case |
| AC15 | the cases named in AC15 itself | each refusal on stderr with a non-zero exit and nothing on stdout; each success on stdout with exit 0 |

## Cross-answer check — round 2

`scripts/lint-answers --item WI-0006` passes, and the read behind it is this. Round 2 recorded no
new answer from the stakeholder — it wrote criteria from answers already consumed — so the check
is over the answers those criteria are built on.

Checked against: WI-0006/Q-001; WI-0006/Q-002; WI-0006/Q-003; WI-0006/Q-004; WI-0005/Q-001;
WI-0005/Q-008; WI-0003/Q-004; WI-0003/Q-005; WI-0003/Q-003; EP-001/Q-003; WI-0001/Q-004.

- **No conflict was found**, and one near-pair is worth naming. `WI-0003/Q-004` says a month is
  typed as a plain word *"because naming a month is the normal case"*; `WI-0006/Q-002` says the
  normal case here is **not** naming one. Those are two different commands and the stakeholder
  gave the reason that separates them, so AC1's `--month` follows their reasoning rather than
  contradicting their sentence. It is recorded above as the licence being spent, which is where a
  disagreement about it would land — not as a conflict to put back to them.
- `EP-001/Q-003` and `WI-0006/Q-001` — *"I still don't want individual spends in that"* — stay
  true, and AC14 makes the summary's untouchedness observable rather than assumed.
- `WI-0005/Q-008` is consumed here for the first time on this item. It was answered on `WI-0005`
  and it decides what **this** item prints; `WI-0005`'s own `answer-questions` run recorded the
  hand-off in both items' notes rather than editing this item's criteria, and AC3 is this item
  taking it up.
- `WI-0006/Q-001`'s *"keep it small and keep it last"* against `WI-0005/Q-001`'s *"the listing
  command has to exist"* is the sequencing tension round 1 recorded. It is settled and it was not
  settled by us reconciling two of their sentences: `WI-0005` records `depends-on: WI-0006`, so
  *last* holds as size and priority and the dependency holds as order.

## Answers — round 2

None. Round 2 put no question to the stakeholder; every decision it took is recorded above as
`[assumed]`, with the licence that granted it or the plain statement that none did.

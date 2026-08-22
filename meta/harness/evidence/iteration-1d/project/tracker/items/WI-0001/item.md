---
id: WI-0001
type: work-item
title: Record people and shared expenses that survive between runs
status: done
priority: critical
epic: EP-001
created: "2026-08-22T01:34:53Z"
updated: "2026-08-22T02:36:32Z"
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone who pays for things on behalf of my friend group, I want to record the people in the
group and each expense — who paid it, how much, what it was for, and who shared it — so that the
group has one record of shared spending that is still there the next time I open the tool.

## Acceptance criteria

Every criterion below is decidable by running the tool and looking at what it printed, what it
exited with, or what it wrote to the data location named in AC9. "Refused" always means the same
three things together: a message on stderr naming what was wrong, a non-zero exit code, and no
change to the recorded data.

- [x] AC1 — a command adds a person by name and exits 0, after which that person appears in AC2's
      listing. A name that is empty or only whitespace is refused. A name that matches one already
      recorded is refused: two names match when they are equal after trimming surrounding
      whitespace and ignoring case, so `ana`, ` Ana ` and `ANA` all match `Ana`
- [x] AC2 — a command lists the recorded people, one per line, each in the form it was first
      typed, in the order they were added. When no people are recorded it prints a line saying so
      and exits 0, rather than printing nothing
- [x] AC3 — a command records an expense from a payer, an amount, a description and a set of
      sharers, and exits 0. The payer and every sharer must already be a recorded person, matched
      by AC1's rule; a name that is not is refused. The payer need not be one of the sharers. The
      same person named twice among the sharers — including as two spellings that match under
      AC1 — is refused. A description that is empty or only whitespace is refused
- [x] AC4 — recording an expense without naming any sharers shares it among every person recorded
      **at that moment**, and stores them by name, so a person added afterwards is not
      retrospectively a sharer of it
- [x] AC5 — an expense stores one amount and a set of sharers, and never a per-person amount:
      after recording 60 shared by three people, the data at AC9's location holds the single
      amount 60 and the three sharers, and holds no separate amount per sharer. The recording
      command offers no option for stating one, which its own usage output shows. Each sharer's
      share is therefore the total divided by the number of sharers, computed where the debts are
      (WI-0002), under `ADR-0002`
- [x] AC6 — an amount is written as one or more digits, optionally followed by a decimal point
      and one or two digits, and must be greater than zero. `12`, `12.5` and `12.50` are accepted,
      and `12.5` and `12.50` mean the same amount. Each of `0`, `0.00`, `-5`, `+5`, `12.`, `.5`,
      `12.505`, `1,234.56`, `€12.50`, `abc` and the empty string is refused
- [x] AC7 — an expense carries a date. A command may state one, written `YYYY-MM-DD`; when none is
      stated the date recorded is the machine's current local date. Each of `22/08/2026`,
      `2026-8-1`, `2026-13-01`, `2026-02-30` and `today` is refused
- [x] AC8 — a command lists the recorded expenses, in the order they were recorded, showing for
      each its date, its payer, its amount, its description and the names of its sharers. When no
      expenses are recorded it prints a line saying so and exits 0
- [x] AC9 — the tool reads and writes one data location. Given no location, every run uses the
      same default one, so what one run records the next run lists. A run may be given a different
      location instead: what is recorded under a given location is listed only by runs using that
      same location, and does not appear in a run that uses the default. A location that does not
      exist yet is created when something is first recorded; a location that cannot be read or
      written is refused
- [x] AC10 — after adding people, expenses and repayments, exiting the process, and running the
      listing commands again in a **new** process against the same location, the same people,
      expenses and repayments are listed, with the same fields and in the same order
- [x] AC11 — a command records a repayment — one recorded person paid another recorded person an
      amount — and exits 0. The amount follows AC6 and the date follows AC7. A name that is not a
      recorded person is refused, and so is a repayment whose payer and payee are the same person
      under AC1's matching rule. A repayment is accepted even when no expense involves either
      person
- [x] AC12 — a command lists the recorded repayments, in the order they were recorded, showing for
      each its date, who paid whom, and how much; when none are recorded it prints a line saying so
      and exits 0. A repayment never appears in AC8's expense listing and an expense never appears
      in this one, per `ADR-0001`

## Out of scope

- Computing balances or who owes whom; that is WI-0002. In particular the rule that the payer
  absorbs the rounding remainder of an unequal division (`ADR-0002`) is applied where debts are
  computed, not here — this item stores an expense's total and its sharers, never per-person
  shares.
- Uneven splits: an expense where some sharers owe more of it than others. The stakeholder
  settled this on `Q-001` — "equal split's fine for now" — and asked for it to be revisited only
  if a real case turns up.
- Reading expenses from a file; that is WI-0003.
- Editing or deleting a person, an expense or a repayment once recorded. There is no undo: a
  mistyped expense stays in the data unless the file is edited by hand.
- Netting repayments off the debts in the who-owes-whom report; this item only records
  and stores them. Using them is WI-0002.
- Any output other than the listings AC2, AC8 and AC12 describe — no filtering by person or
  date, no sorting other than the order things were recorded, and no export format.
- Migrating an existing data file to a new shape. Nothing has been built yet, so there is no
  older format to read.

## Notes

Five unknowns were carried here by `intake` and put to the stakeholder by `refine`. All five are
now settled and the criteria above have been amended accordingly by `answer-questions` — see the
dated block at the end of this section for exactly what changed and why.

- **Splits.** Equal only (`Q-001`). AC5.
- **Amount format and the rounding remainder.** Plain two-decimal numbers, no symbol, no
  separators (`Q-002`, stakeholder); the payer absorbs the remainder of an uneven division
  (`Q-002`, delegated to the architect and decided in `ADR-0002`). AC6 here; the remainder rule
  belongs to WI-0002.
- **Dates.** An expense carries a date, defaulting to today (`Q-003`). AC7.
- **Data location.** A default location, overridable per run (`Q-004`). AC9.
- **Name matching.** Trimmed and case-ignoring; `ana` is `Ana` (`Q-005`). AC1, AC3.
- **Repayment storage.** `ADR-0001` fixes that a repayment is its own kind of record rather than
  a negative expense. The storage format itself is still `plan`'s to settle.

Still open, and deliberately not decided here:

- **The exact command names and the invocation shape.** The criteria say "a command" on purpose;
  naming them is design, and `plan` owns it. That includes how a run is pointed at a different
  data location in AC9 — flag, environment variable or both.
- **Where the default data location is, and the file format.** The architect's, at `plan` time.
  `Q-004` asked the stakeholder only whether the location is theirs to choose.

### Definition of Ready, as assessed by `refine` at 2026-08-22T01:49:06Z

Not Ready. R1, R2, R3, R5, R7, R8 and R9 pass or are satisfiable without the stakeholder; **R4
fails on AC1, AC3 and AC6**, and **R10 fails**, because the behaviours those criteria introduce
have combinations nobody has stated. Five questions are open to the stakeholder — `Q-001`
(equal or uneven splits), `Q-002` (amount format and who absorbs the rounding remainder), `Q-003`
(does an expense carry a date), `Q-004` (fixed data file or pointable), `Q-005` (is `ana` the same
person as `Ana`). The item is suspended at `awaiting-answer` with `resume-to: draft` and the
acceptance criteria above are **unchanged** — none was rewritten on a guess. `artifacts/refinement-qa.md`
carries the batch and, deliberately, no answers.

### Criteria amended by `answer-questions` at 2026-08-22T01:55:49Z

The stakeholder answered all five questions. The criteria above were amended to state the
behaviour they settled, which is permitted here because this item is at `draft` and its criteria
are not yet frozen. The old numbering does not survive: what was AC5 (list expenses) is now AC8,
what was AC6 (persistence) is now AC10, and AC7/AC8 (repayments) are now AC11/AC12. Nothing was
deleted; five criteria were added.

| was | now | change |
|-----|-----|--------|
| AC1 | AC1 | duplicate detection defined as trimmed, case-ignoring; display form fixed (`Q-005`) |
| AC2 | AC2 | display form stated (`Q-005`) |
| AC3 | AC3 | sharer and payer lookup uses AC1's matching rule (`Q-005`) |
| AC4 | AC4 | unchanged |
| — | AC5 | new: splits are equal, and no per-person amount is accepted or stored (`Q-001`) |
| — | AC6 | new: the amount format, with its accepted and refused forms (`Q-002`, `ADR-0002`) |
| — | AC7 | new: an expense carries a date, defaulting to today (`Q-003`) |
| AC5 | AC8 | the expense listing now shows the date (`Q-003`) |
| — | AC9 | new: a default data location, overridable per run (`Q-004`) |
| AC6 | AC10 | persistence now stated against a location, so AC9's override is testable (`Q-004`) |
| AC7 | AC11 | a repayment carries a date and its amount follows AC6 |
| AC8 | AC12 | the repayment listing shows the date |

**One extension the stakeholder did not state.** `Q-003` asked about expenses and its answer
speaks about expenses. AC11 and AC12 apply the same date rule to repayments. The architect made
that call rather than asking, because the alternative is a store with a date on one record kind
and not the other, and `ADR-0001` deliberately settled both record kinds before any data exists
precisely so the second one is not retrofitted. Adding a date to repayments later would migrate a
file that has real money in it; the cost is asymmetric enough that this is not a coin flip. It is
recorded here so that `refine` can put it back to the stakeholder if they disagree.

**Not Ready yet, and not for `answer-questions` to say.** These amendments remove the reasons
`refine` gave for failing R4 and R10, but the Definition of Ready is `refine`'s to assess, on
criteria it has not yet seen. `artifacts/refinement-qa.md` still lacks the verbatim exchange R8
requires; the answers are now recorded there, but the next `refine` execution owns that file and
the assessment.

### Gaps accepted at close by `review-close` at 2026-08-22T02:33:32Z

The item is closed with these known gaps. They are written here, not only in
`artifacts/verify-report.md` and `artifacts/impl-report.md`, because nobody reads those again
once an item is `done`. None of them fails an acceptance criterion; each is a place a later item
has to look.

| gap | why it was accepted | who should pick it up |
|-----|---------------------|-----------------------|
| The on-disk `version` field is written and never read. A ledger written by a future, incompatible version would be parsed as if it were version 1 rather than refused (`Ledger.from_dict` uses `raw.get("version", 1)`) | There is no second version and nothing on disk to migrate, so a check now would be speculative. `ADR-0003` puts the field there precisely so a later change has somewhere to branch | whichever item first changes the on-disk shape; it must add the check in the same change |
| Two processes writing the same ledger at once can lose one of the two changes. `os.replace` makes each write atomic but not serialised | One operator on one machine [src: docs/product/vision.md]; nothing in the epic implies concurrent use. The guarantee delivered is "never a half-written file", not "never a lost update" | nobody, unless the tool grows a second operator |
| `--file ""` silently falls through to `EXPENSES_LEDGER` and then to the default location, rather than being refused. Observed: `python3 -m expenses --file "" add-person Ana` exits 0 and writes to the default | No criterion covers an empty path, and the behaviour mirrors `ADR-0003`'s explicit rule that an empty `EXPENSES_LEDGER` falls through. It is a marginal input, not a data risk | WI-0003, which will pass paths programmatically and is the first place an empty one could arrive by accident |
| `lint-clean` is a `compileall` syntax check, so unused imports, shadowed names and type errors are outside every gate this project runs (`ADR-0005`) | No linter is installed and the project takes no third-party dependencies. Read a green lint gate as "every file parses" | any item that adds a dependency, which would make a real linter cheap |
| The literal default location `~/.local/share/expenses/ledger.json` was never written to during verification; `XDG_DATA_HOME` and then `HOME` were redirected to scratch directories instead | Redirecting is what the tool sees as "no location given", and writing to the operator's real home during a test run is the wrong trade | nobody; the path choice was confirmed by observation |

**BUG-0001** is the one finding that is its own item rather than an accepted gap: all three
recording commands print their success line before the save is attempted, so a failed write
reports success on stdout and failure on stderr in the same run. It is filed at `ready` under
`EP-001` with `found-in: WI-0001`.

### Definition of Ready, as assessed by `refine` at 2026-08-22T02:02:13Z — **passed**

All ten criteria pass; nothing was overridden. The per-criterion record is in this execution's
journal entry under `**Gates:**`. The criteria were rewritten again in this execution — the
numbering and the meaning of AC1–AC12 are unchanged from the `answer-questions` amendment above,
so that table still reads true; what changed is that each criterion now names what would be
observed, and the error cases were filled in.

**Nine decisions were taken by `refine` and not put to the stakeholder.** They are listed here
rather than buried in the Q&A because `plan`, `implement` and `verify` inherit them, and because
each one is a place a stakeholder could reasonably disagree. Every one is presentation or input
syntax, is reversible before there is data on disk, and follows the stakeholder's own standing
instruction on this item — "whatever's easiest to type" (`Q-002`) and "otherwise just use a
sensible default" (`Q-004`). None of them changes what the tool records or what it is for; had
one done so, it would have been a question.

| # | assumed | why not asked |
|---|---------|---------------|
| 1 | Dates are typed `YYYY-MM-DD` (AC7) | Input syntax. Unambiguous, sorts, and is the form every other date in this workspace uses. `22/08/2026` is the only real alternative and is ambiguous with `08/22/2026`. |
| 2 | "Today" means the machine's current **local** date (AC7) | The stakeholder is one person on one machine. UTC would print yesterday's date for a late-evening dinner. |
| 3 | An amount is digits with at most two decimals and must be **greater than zero** (AC6) | Tightens "no symbols or commas" into something `verify` can test. Zero and negative amounts were listed as refused in `Q-002`'s option A, which the stakeholder chose. |
| 4 | Listings print in the order things were recorded (AC2, AC8, AC12) | Presentation. Any order works; an unstated one is untestable, and insertion order is the only one that needs no extra data. |
| 5 | An empty listing prints a line saying so and exits 0 (AC2, AC8, AC12) | Mirrors WI-0002 AC3, which already says the report must say so explicitly rather than print nothing. Consistency across the tool's commands. |
| 6 | An empty or whitespace-only person name or description is refused (AC1, AC3) | Nobody wants a nameless person in the ledger, and it is the boundary case `verify` would otherwise have to invent an answer for. |
| 7 | Naming the same person twice among an expense's sharers is refused (AC3) | A genuine either/or — refuse, or silently de-duplicate. Refusing surfaces a typo; de-duplicating hides one. Cheap to reverse. |
| 8 | The payer need not be among the sharers (AC3) | Ordinary: one person pays for a round they did not drink. Stating it prevents an implementer from requiring it. |
| 9 | A repayment carries a date on the same terms as an expense (AC11, AC12) | Inherited from `answer-questions`, not decided here: `Q-003`'s answer speaks about expenses. `ADR-0001` settled both record kinds before any data exists precisely so the second is not retrofitted, and a date added to repayments after the file holds real money is a migration. `refine` considered putting it back to the stakeholder and did not, because it is reversible until `implement` runs and the answer is very unlikely to be "no". |

If the stakeholder disagrees with any of these, the cheap moment is before `implement` writes a
store; after that, 1, 2 and 9 become data migrations and the rest stay cheap.

### R10 — every combination this item introduces, and where it is settled

| combination | where |
|-------------|-------|
| expense with no sharers stated × no people recorded yet | cannot arise: AC3 refuses it first, because the payer is not a recorded person |
| expense with no sharers stated × exactly one person recorded | AC4 — the payer is the only sharer. Allowed, and it contributes nothing to any debt |
| expense with no sharers stated × a person added afterwards | AC4 — sharers are fixed at the moment of recording, not recomputed |
| an amount that does not divide evenly among its sharers | `ADR-0002` — the payer absorbs the remainder, applied in WI-0002; AC5 keeps the per-person share out of this item's storage entirely |
| a name matching an existing one only by case or spacing × add / expense / repayment | AC1 fixes the matching rule; AC3 and AC11 both cite it |
| a date stated × a date omitted × a malformed date | AC7 |
| default data location × a location given per run × two different locations | AC9 |
| a location that does not exist × one that cannot be read or written | AC9 |
| repayment between two people who share no expense | AC11 — accepted. Whether a repayment can exceed a debt, and how that reads, is WI-0002's (its AC5) |
| repayment where payer and payee are the same person | AC11 — refused |
| a repayment in the expense listing, or an expense in the repayment listing | AC12 — neither, per `ADR-0001` |
| any refusal × what is left on disk | stated once at the head of the criteria: a refusal changes no recorded data |
| an expense or repayment imported from a CSV | out of scope here; WI-0003, which inherits AC6's amount form and AC7's date |

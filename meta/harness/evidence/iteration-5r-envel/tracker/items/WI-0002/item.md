---
id: WI-0002
type: work-item
title: Record spending against an envelope and see what is left
status: done
priority: high
epic: EP-001
depends-on:
  - WI-0001
created: "2026-09-11T01:57:13Z"
updated: "2026-09-11T05:01:31Z"
branch: wi/WI-0002
outcome: delivered
merge-commit: 23dc901e84201710f50cf8d8122e3a950c5d9e21
---

## Story

As a person budgeting my own money at a terminal, I want to record what I spend against the
envelope it came out of, so that the amount left in that envelope tells me what I still have to
spend on it.

## Acceptance criteria

- [x] AC1 — `envel spend <envelope> <amount>` records a spend of `<amount>` against the
      envelope named `<envelope>` — the envelope first and the amount second, the same order as
      `envel add` [src: WI-0001 AC2 "`envel add <name> <amount>` adds `<amount>` of income to the envelope called"]. The
      subcommand name `spend` is `[assumed]`, under no delegation
      (`artifacts/refinement-qa.md`).
- [x] AC2 — After recording a spend, the listing
      [src: WI-0001 AC3 "one line per envelope, each line containing that envelope's name and
      the amount currently in it"]
      shows that envelope's amount reduced by exactly the amount spent, and no other envelope's
      amount changed.
- [x] AC3 — Recording a spend against an envelope that does not exist is refused, with a message
      naming the envelope, and nothing is recorded.
- [x] AC4 — A spend recorded in one invocation is still reflected in the listing in a later,
      separate invocation of the tool.
- [x] AC5 — Recording a spend larger than the amount currently in the envelope is refused: the
      spend is not recorded, the envelope's amount is unchanged, and the message names the
      envelope and says how much is left in it. The listing never shows a negative amount for
      any envelope.
- [x] AC6 — Recording a spend of `0`, or of a negative amount, is refused with a message, and
      the envelope's amount is unchanged — the same rule the stakeholder set for income
      [src: WI-0001/Q-003].
- [x] AC7 — Recording a spend prints the envelope's new remaining amount, so the result is
      visible without running the listing.
- [x] AC8 — Recording a spend without `--on` is accepted with nothing extra typed, and records
      it as happening today. Observed in a store of its own — `ENVEL_FILE` set to a path that
      does not exist [src: ADR-0003] — by creating one envelope, adding income to it, recording
      one spend with no date and one further spend with `--on 2020-01-01`: the store file then
      holds two spend entries, and the one recorded without a date carries today's date while
      the other carries `2020-01-01`. The store file is where this item's dates are read,
      because nothing this item delivers prints a spend's date back; `WI-0003`'s summary is
      where it becomes visible without opening the file.
- [x] AC9 — A spend can be recorded with a date other than today, written as `--on <date>`,
      and it is held against that date rather than the day it was typed: after
      `envel spend groceries 12.50 --on 2026-08-28` in the store of AC8, that spend's entry in
      the store file carries `2026-08-28`. That is what makes a spend entered on the 3rd of
      September belong to August for the purposes of `WI-0003`'s summary [src: WI-0002/Q-003].
- [x] AC10 — A spend can be recorded with a short description of what it was for, written as
      a plain word after the amount and needing no option before it —
      `envel spend groceries 12.50 "lunch"` — and it can be recorded without one. Leaving it out
      is not refused and nothing prompts for it. Either of the description and the date may be
      given without the other, and both may be given on the same line:
      `envel spend groceries 12.50 "lunch" --on 2026-09-07` [src: WI-0002/Q-003]. Observed in
      the store of AC8: the entry for a spend recorded with `"lunch"` contains `lunch`, and the
      entry for one recorded without a description carries none.
- [x] AC11 — `--on` accepts the full `YYYY-MM-DD` form and nothing else. `2026-09-07` is
      recorded; `7/9`, `09-07`, `yesterday` and anything else that is not that form are each
      refused with a message, with nothing recorded and the envelope's amount unchanged
      [src: WI-0002/Q-004].
- [x] AC12 — A date given with `--on` that is later than today is refused with a message saying
      the date is in the future; nothing is recorded and the envelope's amount is unchanged
      [src: WI-0002/Q-005]. Today's own date is accepted, being the default of AC8.
- [x] AC13 — Every refusal this item specifies writes its message to stderr and exits non-zero,
      and recording a spend successfully writes its output to stdout and exits 0. It is the
      project's recorded convention [src: docs/architecture/overview.md] and the rule the
      delivered item already follows [src: WI-0001 AC16 "Every refusal this item specifies
      writes its message to stderr and exits non-zero"]. Checked case by case against the
      criteria that name them: refusals at AC3, AC5, AC6, AC11, AC12 and AC14; success at AC1,
      AC7, AC8, AC9 and AC10.
- [x] AC14 — `envel spend` with no arguments, `envel spend groceries` with no amount, and
      `envel spend groceries 12.50 "lunch" extra` with a word beyond the description each print
      a usage message for the subcommand to stderr and exit non-zero, and nothing is recorded —
      the same treatment the delivered subcommands already get [src: WI-0001 AC15 "A subcommand
      given the wrong number of arguments prints to stderr a usage message for that subcommand
      and exits non-zero"].

## Out of scope

- Correcting or deleting a spend once recorded — asked for at `EP-001/Q-005` and filed as
  `WI-0005`, not this item.
- Moving money between envelopes — asked for at `EP-001/Q-005` and filed as `WI-0004`. It is
  the route the stakeholder wants when AC5 refuses a spend.
- Categories, tags, payees, and any grouping of spending other than by envelope.
- The monthly summary, which is `WI-0003`.

## Notes

- `refine` round 1's two questions are both answered and propagated. `WI-0002/Q-001` — option
  B: today unless a date is given (AC8, AC9). `WI-0002/Q-002` — option B: an optional
  description (AC10). This item is still **not** Ready: R4 fails, because nobody has settled
  what to type below `envel`, how a date is written on the command line, or what the command
  prints. That is `refine` round 2's ask, and these go with it:
- `depends-on: WI-0001` was added by this round. The dependency is real — there is nothing to
  spend from until envelopes can be created and funded — and AC2 is written against `WI-0001`'s
  listing. Recording it here is what sequences the work; it also means the orchestrator will not
  dispatch anything on this item until `WI-0001` is `done`, which is the pipeline's own rule and
  is noted so that a later reader knows it was chosen rather than overlooked.
- Assumed here, under no delegation (`artifacts/refinement-qa.md`): AC6's symmetry with income,
  and AC7's printing of the new remaining amount. Each costs one line of code to change. The
  symmetry half of that assumption now has an answer behind it — the stakeholder refused zero
  and negative income at `WI-0001/Q-003` — but they were asked about income, not about spending,
  so AC6 is still ours until they say otherwise.
- The amount and envelope-name rules the stakeholder settled at `WI-0001/Q-002` and
  `WI-0001/Q-004` apply here too and are recorded once, on `EP-001` `## Notes`.
- Open **design** questions, routed to `plan` rather than to the stakeholder:
  - how a spend is stored alongside the envelope balances, and whether a balance is stored or
    derived by replaying entries;
  - what the tool does when the store holds a spend against an envelope that is no longer there.
- Open points round 1's answers left behind. **Round 2 has now disposed of all of them**, either
  by asking or by deciding — see `## Notes` under *`refine` round 2* below:
  - what happens when a date is given that the tool cannot read, and whether a date in the
    future is refused. AC9 says a date can be given; nobody has said what an unusable one does,
    and guessing it here would manufacture a requirement. **Round 2:** the unreadable date is
    decided (refused, nothing recorded, on the convention every other malformed input already
    follows); the future date is asked, as `WI-0002/Q-005`, because it is a policy about their
    money rather than a reading of text.
  - whether a description has a length limit, and whether it may contain anything at all.
    **Round 2:** decided — no limit, no restriction, assumed under no delegation.
  - whether a spend's date and description can be corrected as well as its amount — that is
    `WI-0005`, and it is recorded there. Unchanged.

- **`refine` round 2** filed three blocking questions and rewrote no criterion. All three are one
  ask about one thing, the line that records a spend:
  - `WI-0002/Q-003` — are the optional date and description named options (`--on`, `--note`),
    extra plain words in a fixed order, or a mixture? It is what they type daily, and `WI-0001`
    deliberately gave the first three commands no options at all.
  - `WI-0002/Q-004` — which ways of writing a date are accepted, and if a short form like `7/9`
    is wanted, which of its two readings is theirs? Nobody has said where they live, and the two
    readings differ by two months.
  - `WI-0002/Q-005` — is a date in the future refused, recorded, or recorded with a warning? The
    same keystrokes are a mistyped year and a direct debit they know about.

  Decided by round 2 rather than asked, each recorded with its authority in
  `artifacts/refinement-qa.md` `## Decided here, and by what authority — round 2`:
  - the subcommand is `spend`, as `envel spend <envelope> <amount>` — `[assumed]`, under no
    delegation, on the same footing as `WI-0001`'s `new`, `add` and `list`. A disagreement lands
    on AC1.
  - a date the tool cannot read is refused with a message and nothing is recorded — `[assumed]`,
    under no delegation, on the convention `WI-0001` AC13 and AC17 already deliver.
  - a description has no length limit and no character restriction — `[assumed]`, under no
    delegation. `WI-0001/Q-004` is about names, not descriptions, and is deliberately **not**
    read as licensing this.
  - success on stdout with exit 0 and every refusal on stderr with a non-zero exit — **not** an
    assumption but the project's recorded convention
    [src: docs/architecture/overview.md] and their own
    [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits
    non-zero"].

  **No criterion was rewritten**, deliberately: AC1, AC7, AC9 and AC10 still say what round 1
  left them saying, and round 3 rewrites them once from the replies rather than renumbering the
  list twice while citations elsewhere point into it.
- The stakeholder's answer to `WI-0002/Q-002` implies something no item covered: they said they
  would put a description on *"the ones I might query later"*, and nothing in this epic lets
  them query a spend. That was filed as `WI-0006` at `draft` rather than added here, and
  `WI-0006` `## Notes` says plainly that it was derived rather than asked for.
- `EP-001/Q-002` is answered and AC5 is no longer a placeholder: the stakeholder chose to refuse
  an overspend — *"I don't want to see a negative envelope; if the money has to come from
  somewhere else then I want to move it there myself and record the spend after."* Moving money
  is `WI-0004`, which they asked for in the same breath at `EP-001/Q-005`.
- `EP-001/Q-006` is answered: the command is `envel`, and AC1 now says so.

- **Round 2's three answers are in, and this is what they settled.** `answer-questions` consumed
  them on 2026-09-11; the stakeholder's words are quoted verbatim in
  `artifacts/refinement-qa.md` `## Answers — round 2`.
  - `WI-0002/Q-003` — option **C**: the description is a plain word, the date is `--on`. Their
    reason was the typing: *"The description is the bit I'll actually type, so make that the
    cheap one… I don't want to be typing `--note` on the weekly shop."* AC1, AC9 and AC10 now
    say so.
  - `WI-0002/Q-004` — option **A**: `2026-09-07` and nothing else. AC11 is new and says so. They
    also volunteered, for a short form nobody is building: *"if you ever do add one, `7/9` means
    the 7th of September to me."* That is recorded here and nowhere else — it is a conditional
    about work they did not ask for, so no item was filed for it, and anyone who does add a
    short form later has their reading without having to ask again.
  - `WI-0002/Q-005` — option **A**: a future date is refused. AC12 is new and says so, and their
    reason ties it to a decision they had already made: *"Same reasoning as the overspend: stop
    me rather than take something I didn't mean."*
- **Round 2 deferred the criteria rewrite to round 3; `answer-questions` did it instead, and
  here is why.** Round 2's reason for not rewriting was that it would mean either guessing the
  answers or renumbering the list twice while citations elsewhere point into it
  (`artifacts/refinement-qa.md` `## What round 2 has not settled`). Neither cost applies now:
  the answers are in, so nothing is guessed, and AC1, AC9 and AC10 were amended **in place**
  with AC11 and AC12 **appended**, so no existing criterion changed its number and every
  citation naming `WI-0002 AC<n>` still resolves to the criterion it named. An answer that had
  not reached the criteria would have left `item.md` saying the old thing to the next reader,
  which is the failure the propagation gate exists to prevent. `refine` round 3 therefore walks
  the Definition of Ready against these criteria and confirms them; it does not have to write
  them.
- **What round 2 assumed is undisturbed by the answers.** The subcommand `spend`, a description
  with no length or character limit, and success-on-stdout / refusal-on-stderr are exactly as
  round 2 left them; AC1 still carries the `[assumed]` tag for the subcommand name. AC11 does
  make round 2's *unreadable date* assumption concrete rather than replacing it: round 2 decided
  that text the tool cannot read is refused, and `Q-004`'s answer is what says which text that
  is.

- **`refine` round 3 took this item to Ready, and asked the stakeholder nothing.** Its full
  record is `artifacts/refinement-qa.md` `## Round 3`. Two Definition-of-Ready criteria were
  failing and neither was theirs: R4, because AC8, AC9 and AC10 described a spend's date and
  description while nothing this item delivers prints either back, and because no criterion said
  which stream a message goes to; R10, because four combinations of the two new options had no
  stated behaviour. What changed: AC8, AC9 and AC10 gained a repeatable observation against the
  store file and lost none of what the stakeholder chose; AC13 and AC14 were appended. No
  criterion changed its number — `grep -rn 'WI-0002 AC' tracker docs` finds one cross-item
  citation, `WI-0003` AC8 on `WI-0002` AC9, and it quotes AC9's opening words, which this round
  left untouched.
- **Deliberately unconstrained, and left so by `refine` round 3.** `[assumed]`, **under no
  delegation** — nothing the stakeholder has said covers any of these, and each is recorded here
  rather than decided because a reasonable implementation may settle it either way without
  surprising them. `plan` may settle any of them and should say so if it does.
  - **Which message is printed when more than one refusal applies at once** — say
    `envel spend nosuch 0 --on 2099-01-01`, where AC3, AC6 and AC12 all refuse. Every criterion
    involved is satisfied by any of them: the spend is refused, nothing is recorded, and the
    message names the envelope. A disagreement lands on whichever of those criteria is read as
    promising its own message first, and costs the order of a few checks.
  - **A description that is empty (`""`) or only whitespace.** AC10 says a description is
    optional and unbounded; it does not say whether an empty one is a description. A
    disagreement lands on AC10.
  - **`--on` given twice on one line.** A disagreement lands on AC9 or AC11 and costs one
    argument-parser setting.
  - **The wording of every message**, exactly as `WI-0001` left it. The criteria say what a
    message must contain — the envelope's name, the amount left, that the date is in the future —
    and never how it reads.
- **Still routed to `plan`, and sharpened by round 3:** `ADR-0002`'s `at` field is *"when the
  tool recorded the entry"*, and AC9 now requires a spend to be held against a date that may not
  be that. Whether the spend's date is a new field or a redefinition of `at` is `plan`'s to
  settle; the criteria are written so that either satisfies them, because they say the entry
  *carries* the date and never what it is called.

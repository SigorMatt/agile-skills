# Refinement Q&A — WI-0003

> **Round 3: no questions asked. The item is blocked, 2026-08-22T03:38:34Z.** With every question
> answered and the sample still absent, `refine` applied the Definition of Ready for the first
> time. Eight criteria pass; **R4 and R10 fail**, both on the same missing input. There is nothing
> left to ask — the stakeholder has answered every question put to them — so the item moves to
> `blocked` with `resume-to: draft` rather than to a fourth question. See `## Round 3` at the foot
> of this file.
>
> **Round 2 answered, 2026-08-22T03:33:27Z.** The stakeholder chose **A**: "No — just wait for my
> file. I don't want a name-the-columns version." The importer is written against their own export
> and takes no column-mapping options (`ADR-0010`). AC1 was rewritten and AC3, AC4 and AC5 now each
> state that they wait on the sample and on nothing else. **The sample itself still has not
> arrived**, so the item remains unrefinable — but it is now waiting on a fact rather than on a
> decision, and no fourth question may be filed for it.
>
> **Round 2 filed, 2026-08-22T03:28:24Z.** `Q-003` supersedes `Q-001`: after two
> deferrals of the same request, `refine` stopped asking for the sample and asked instead *how the
> importer should learn the file's shape* — from a sample, from options typed at run time, or from
> a fixed format the stakeholder converts to. Only one of the three needs the sample. The item was
> suspended at `awaiting-answer` with `resume-to: draft` and **no acceptance criterion was
> rewritten**, because two of the three options change what the command's arguments even are.
>
> **Round 1 half answered, 2026-08-22T02:52:26Z.** `refine` did not attempt this item; it filed
> two questions and suspended, as `item.md`'s `## Notes` instructed. The stakeholder has now
> replied to both. `Q-002` is a real answer — option B, recorded as `ADR-0007`. `Q-001` is
> "I'll send you a sample later" for the second time, so the item is still not refinable and the
> next `refine` execution must file a fresh question for the sample and suspend again.
>
> The stakeholder is asynchronous and has never been in a session with this pipeline. Every
> `[human]` line below is their written answer in a question file, quoted exactly.

## Round 1 — filed 2026-08-22T02:42:09Z, replied to 2026-08-22T02:52:26Z

| # | question | file | DoR criterion it unblocks | answer |
|---|----------|------|---------------------------|--------|
| 1 | Please paste 3–5 real lines of your bank's CSV export, including the header row | `questions/Q-001.md` | R4 (AC1, AC3, AC4 not decidable), R10 | **deferred a second time** — "I'll send you a sample later". Still not supplied |
| 2 | How should a bank row become a shared expense — who paid it, and who shared it? | `questions/Q-002.md` | R4 (AC1, AC2 not decidable), R9, R10 | **B — payer, sharers and a date range given at import time.** `ADR-0007` |

### Why two questions rather than one

`EP-001/Q-002` asked both together and got a reply that answered neither. They are separable — a
sample tells the importer how to *read* the file, the rule tells it what to *do* with each row —
and `spec/question.md` §2 requires one answerable question per file. Filing them as two also
means a partial reply is usable: a sample with no rule still unblocks the parsing criteria.

`Q-001` states explicitly that it is a missing fact and not a choice between options, which
`spec/question.md` §2 permits and requires to be said out loud. `Q-002` carries the four options
`EP-001/Q-002` offered, unchanged in substance, with one consequence sharpened: WI-0001 shipped
with no delete, so an import that records the wrong thing cannot be undone from the tool.

### The exchange, so far

- `[refine]` `Q-001` — asked for the sample, listing the six things that would otherwise have to
  be guessed (header, delimiter and quoting, date format, sign and symbol conventions, which
  column becomes the description, preamble and total rows).
- `[refine]` `Q-002` — asked how a row becomes a shared expense, recommending **B** (payer and
  sharers named once for the whole import, with a way of limiting which rows are taken) and
  arguing explicitly against **A** on the no-delete ground.
- `[human]` on `Q-001`: "I'll send you a sample later." The same words as on `EP-001/Q-002`, and
  the second deferral of the same fact. Nothing about the file's shape is known, so nothing about
  parsing it can be written down.
- `[human]` on `Q-002`: "B — let me say who paid and who it's shared with when I run the import,
  and let me limit it to a date range. That's basically what a trip looks like anyway."
- `[answer-questions]` `Q-002`'s answer follows `refine`'s recommendation and adds the limiting
  mechanism the option left open — a date range rather than a description match. Recorded as
  `ADR-0007`, which also settles two things the answer did not say: the range is **optional**
  (omitting it imports every row), and a row outside the range is **skipped silently** rather
  than reported under AC3, because filtering is the point of the range and a filtered row is not
  a row the tool failed to understand. **AC1 was rewritten** to state the payer, the sharers and
  the range, and to say in the criterion itself that the column mapping still waits on `Q-001`.
- `[answer-questions]` AC2, AC3, AC4 and AC5 were **not** read against the Definition of Ready
  and **not** rewritten. Each of them depends on the file's shape. No DoR verdict exists for this
  item and none was attempted.

## Deliberately not asked in this batch

**AC5 — whether re-importing the same file is idempotent or additive.** `item.md`'s `## Notes`
flags this as a real either/or that `refine` must turn into one criterion. It is not in this batch
because it cannot yet be asked well: recognising a row as one already imported requires knowing
what identifies a row, which is `Q-001`'s sample, and what an imported row becomes, which is
`Q-002`'s rule. Asking now would produce a question whose options I could not state.

The likely resolution, recorded so that it is visible rather than sprung later: given that
WI-0001 shipped with no delete, an accidental double import is unrecoverable from the tool, which
argues for skipping rows already imported and reporting how many were skipped. `refine` expects
to take that decision itself once the sample arrives, and to put it to the stakeholder only if the
sample makes duplicate detection genuinely ambiguous.

## Where this item stands after the reply

Not refinable, and not blocked either. `Q-002` closed; `Q-001` did not. The item returns to
`draft`, where the orchestrator will leave it alone — `depends-on` names WI-0002, which is at
`draft` — until WI-0002 is `done`. Whichever `refine` execution is dispatched then reads
`item.md`'s `## Notes` and, if the sample still has not arrived, files a fresh question citing
`Q-001` and suspends. No third request for the sample was filed now: the stakeholder has been
asked twice, and asking again before any skill could use the answer would stop the loop on the
item that *is* runnable.

## Round 2 — filed 2026-08-22T03:28:24Z, replied to 2026-08-22T03:33:27Z

| # | question | file | DoR criterion it unblocks | answer |
|---|----------|------|---------------------------|--------|
| 3 | How should the importer learn the shape of your bank's CSV — from a sample you send now (A), from options you type when you run it (C), or from a fixed format you convert your export into (B)? | `questions/Q-003.md` | R4 (AC1, AC3, AC4, AC5 not decidable), R9, R10 | **A — the sample; no name-the-columns version.** `ADR-0010`. The sample has still not arrived, so R4 remains failed on the parsing criteria |

### Why this is a different question, not the same one asked a third time

The stakeholder has been asked for the sample twice and has twice said "later". `spec/question.md`
§4 is about whether a question belongs to the human at all, and this one does — it depends on
intent no document records — but a third identical request would spend their attention on
something they have already declined twice, and would leave this item stuck behind a file that may
never arrive.

So `Q-003` reframes it as the choice it actually is. The importer has to learn four things about
the file — which columns carry the date, the amount and the description, and how the date and the
amount are written. There are exactly three places that knowledge can come from: a sample sent
now (**A**), options typed at import time (**C**), or a fixed shape the stakeholder converts their
export into before importing (**B**). Only **A** needs the sample. **C** removes it from the
critical path entirely by making the missing facts into run-time arguments — nothing is guessed,
the person with the file states them at the moment they have it open.

`refine` recommends **C**, with **A** named as genuinely better *if* the sample is easy to
produce, and argues against **B** on the stakeholder's own words: converting the export in a
spreadsheet at every import is the retyping they asked to stop doing. **D** — dropping the import
— is listed only to be rejected, because `EP-001/Q-001` settled that it ships.

### Why no acceptance criterion was rewritten this round

Under **A** the command takes the payer, the sharers and a date range, and nothing else. Under
**C** it takes five more options and their error behaviour. Under **B** it takes the same
arguments as **A** but gains a criterion about refusing a file whose header is not the fixed one.
AC1 would have to be written three different ways, and AC3 (a row that cannot be turned into an
expense) and AC4 (a file that is not the expected shape) differ between them in what "the expected
shape" means. Writing any of them now would be recording a guess as a requirement.

**No Definition of Ready verdict was reached**, for the same reason `refine` gave at
2026-08-22T02:42:09Z: assessing criteria that are about to be rewritten produces a verdict about
the wrong criteria. R6 fails by construction while `Q-003` is open, and that is the suspension
doing its job rather than a finding.

### The exchange, round 2

- `[refine]` `Q-003` — asked which of three sources the importer should learn the file's shape
  from, with the cost of each stated, recommending **C** and arguing against **B** from the
  stakeholder's own statement of the idea. Superseded `Q-001` explicitly.
- `[human]` on `Q-003`: "No — just wait for my file. I don't want a name-the-columns version."
- `[answer-questions]` read that as **A**, and as a rejection of **B** as well: "just wait" only
  makes sense if the export is to be handed over as it is, since under B there is nothing to wait
  for. `refine`'s recommendation of **C** was overruled by name. Recorded as `ADR-0010`, which also
  settles three things the answer did not say — that the import command gains no column-mapping
  options at all, that the sample should land at
  `tracker/items/WI-0003/artifacts/bank-sample.csv`, and that no fourth question may be filed for
  it. **AC1 was rewritten** to drop the run-time-argument hedge and state that the mapping is fixed
  and read off the stakeholder's export; **AC3, AC4 and AC5 each gained a clause** naming the
  sample as the one thing they wait on.
- `[answer-questions]` the item returned to `draft`, its recorded `resume-to`. It is **not**
  refinable: the choice is settled but the file is not here. The next `refine` execution moves it
  to `blocked` rather than asking again — see `item.md` `## Notes`.

### Still deliberately not asked

**AC5 — whether re-importing the same file skips rows already imported or adds them again.**
Unchanged from round 1, and stated inside `Q-003` itself so the stakeholder could see it coming
rather than have it sprung on them. It still cannot be asked until something identifies a row —
which, now that A is chosen, means it waits on the sample rather than on the choice. `refine` still
expects to decide it toward skipping, and to report how many rows were skipped, because WI-0001
shipped with no way to delete an expense. It goes to the stakeholder only if the sample turns out
to make duplicate detection genuinely ambiguous.

## Where this item stands after round 2

**Two of the three unknowns are now closed and the third is not.** What the tool does with a row is
settled (`ADR-0007`); where the tool learns the file's shape from is settled (`ADR-0010`); what
that shape *is* is not, and there is no longer any question outstanding that would produce it —
only a file that has to arrive.

That is a different state from every previous round, and it is worth naming: this item is no longer
waiting on the stakeholder's *attention*, which the question protocol exists to allocate. It is
waiting on their *action*. The protocol has nothing further to offer, so the next `refine`
execution stops using it: it moves the item to `blocked`, which is the status that says a human
must act, and which any skill may move it out of once the file exists
(`spec/ids-and-statuses.md` §4). Nothing else in the epic is affected — `BUG-0001` is `ready`, and
WI-0001 and WI-0002 are `done`.

**No Definition of Ready verdict exists for this item and none was attempted in this round either.**
`answer-questions` does not assess the DoR. R4 fails on AC1, AC3, AC4 and AC5 by construction while
the sample is missing, and writing any of them now would record a guess as a requirement.

## Round 3 — 2026-08-22T03:38:34Z — no questions asked

**Nothing was put to the stakeholder in this round, and that is the round's substance.** The
Definition of Ready needs one input this item has never had, and three questions have already been
addressed to them about it. The third was answered with an instruction rather than a deferral:

- `[human]` on `Q-003`: "No — just wait for my file. I don't want a name-the-columns version."

That closes the question protocol on this item. `spec/question.md` §4 licenses an escalation when
intent is unrecorded or the record is silent; here the intent is recorded and explicit. A fourth
question would be the pipeline asking a person to send a file — which is not a question, and which
would stop the orchestrator on every subsequent turn while `BUG-0001`, which is `ready`, waits.

### The Definition of Ready, criterion by criterion

Applied for the first time on this item. Earlier executions declined to apply it because the
criteria were about to be rewritten from a file nobody had seen; `Q-003` ended that, because the
criteria are no longer about to change *shape* — they are simply unwritable until the file exists.

R1 pass · R2 pass · R3 pass · **R4 fail** · R5 pass · R6 pass · R7 pass · R8 pass · R9 pass ·
**R10 fail**. The evidence for each is in `item.md` `## Notes`, in the section
`### The Definition of Ready was assessed for the first time, and it fails`.

- **R4** fails because only AC2 is decidable. AC1 cannot name the columns, the delimiter, the date
  format or the amount convention; AC3 cannot enumerate what makes a row unusable; AC4's "not the
  expected shape at all" has no referent; AC5 is an either/or rather than a criterion.
- **R10** fails because the combinations that depend on the file's shape cannot be enumerated at
  all. The ones that do **not** depend on it were knowable today and are now written into
  `item.md` `## Notes` as open, left open by `refine`: a payer or sharer who is not a recorded
  person, a date range matching no row, whether the bounds are inclusive, and whether a run all of
  whose rows fail exits non-zero. That is the part of R10 that could be satisfied without the
  sample, and it was.
- **R6 passes for the first time** — `Q-001`, `Q-002` and `Q-003` are all `answered`, so no open
  question remains on this item at all. Every previous round failed it by construction.

### No override was recorded, and none could be

`spec/dor-dod.md` §1 lets the stakeholder force an item to `ready` without meeting the checklist.
That is their call, and `refine` may not make it for them: an override needs a stated reason from
the person overriding, and they have not offered one — they said the opposite, that they would
send the file. Recording an override here would be inventing the stakeholder's consent to ship an
unspecified parser, which is the one thing this checklist exists to prevent.

### Where this item stands

`blocked`, with `resume-to: draft`. It is waiting on the stakeholder's **action**, not their
attention — a file, at `tracker/items/WI-0003/artifacts/bank-sample.csv` (any CSV in that
directory will do), 3–5 lines including the header, with merchant names and amounts changed to
anything. Any skill may then move it back to `draft`
[src: .claude/agile-skills/spec/ids-and-statuses.md], and the next `refine` execution starts with
`ADR-0007` fixing what the command does with a row, `ADR-0010` fixing that the mapping is read off
the file, and R10's open combinations already listed. Nothing else about this item is outstanding.

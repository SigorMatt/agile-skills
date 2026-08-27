# Iteration 1e — the termination-model regression run

Run 2026-08-26T23:20:37Z … 2026-08-27T02:44:25Z against the toolkit as of commit `f2cc2a3`
(builder session 2.5, META-102…109 complete). Config:
`harness/iterations/iteration-1e-expenses.json`. Persona: `cooperative-pm`. Project:
`expenses-1e`, provisioned from nothing with `provision.py --wipe`.

**The probe is 1d's, byte for byte.** `probes/iteration-1e-expenses.md` and
`probes/iteration-1d-expenses.md` are the same file — sha256
`9f51368f493b62ee5ed4d3afe6339d8b6b5aae3d30dd80b6d987ede385bb4497`. The config differs from 1d's
in `id`, `project` and `max-turns` and in nothing else. The toolkit is the only variable, which
is what makes the difference in the ending attributable to the fix.

## What it was for

1d reached an impasse and stopped there, and both sides of the engagement recorded the same gap.
The stakeholder went looking for the acceptance question and wrote down that it never came
(F-045), and separately noticed a bug the pipeline had filed and never mentioned to them
(F-046). Builder 2.5 derived the termination model in response (`meta/adr/ADR-0006`): an
engagement has four legal endings, and every one of them passes through a blocking question that
names every child item as delivered or not.

1e asks one question: **does the engagement now end through the stakeholder?**

## Outcome

**STOP: `blocked-no-recourse`** at turn 20 — `blocked: EP-001, WI-0003; no question is open to
the human`. Terminal, and this time the epic is blocked *as a recorded ending*, not left open.

| | 1d | 1e |
|---|---|---|
| turns | 16 | **20** (13 worker, 7 sim) |
| wall clock | 148 min | **200 min** |
| cost | $71.75 | **$100.23** |
| tool calls | 837 | **1120** |
| contamination violations | 0 | **0** |
| permission denials | — | **0** |
| items delivered | WI-0001, WI-0002, BUG-0001 | WI-0001, WI-0002, WI-0004, BUG-0001, BUG-0002 |
| items not delivered | WI-0003 `blocked` | WI-0003 `blocked` |
| epic's final state | `open` — the engagement never ended | **`blocked` — ending E3, recorded** |
| sign-off question | **never filed** | **`EP-001/Q-004`, filed, answered, acted on** |

`validate-workspace` over the final project: **0 errors, 0 warnings.**

## The difference, in the record

The epic's `history.md` is the whole proof — three rows that did not exist as a possibility
before this session:

```
02:31:08  open            → awaiting-answer  review-close      resume-to: open
          engagement at rest with five of six children delivered; sign-off question Q-004
          filed naming every child and asking the stakeholder whether they accept

02:35:13  awaiting-answer → open             answer-questions
          EP-001/Q-004 answered by the stakeholder: they did not accept the engagement,
          naming the undelivered bank CSV import (WI-0003) as what is missing

02:40:24  open            → blocked          review-close      resume-to: open
          ending E3, the impasse: the stakeholder answered the sign-off Q-004 with a refusal
          … so the engagement ends without acceptance; epic DoD DE1-DE7 recorded in
          artifacts/review.md, no outcome because blocked is not a closure
```

### The statement named every child, including the two bugs (F-046)

`Q-004`'s `## Question` lists all six children by ID with what became of each, and it puts the
undelivered one in front of the stakeholder rather than implying it by absence:

> So: five of the six delivered, and the bank CSV import — which you told us was part of what you
> asked for, not an optional extra — not delivered, for want of a sample of your bank's export.

Both bugs are in the list, labelled as the pipeline's own findings rather than folded into the
stakeholder's ask. That is exactly what 1d's stakeholder said they had not been given.

### The stakeholder answered, in persona (P4)

> [human] No, not as it stands — the bank import was part of what I asked for and it isn't there.
> Everything else looks right. I'll send the file and then we can finish it.

### And said so again on the closing turn

> Q-004's tally matches what I asked for in `IDEA.md` item for item, and the two extra fixes
> (BUG-0001, BUG-0002) were found by their own testing, not requested by me, and correctly
> labelled as such rather than folded into my ask. … The epic sits at `blocked`, not `done`,
> which is the correct place for it to sit given my answer.

## What else the run exercised

- **F-028, organically and early.** WI-0003 was parked at `blocked` on **turn 4**, where 1d took
  until turn 14. `answer-questions` took step 3a's first move — deciding *under* the deferral
  rather than recording one — and said so in the question: *"the decision taken under the
  deferral … park WI-0003 and deliver the rest of the epic."* The ten turns that bought are why
  1e delivered five items where 1d delivered three.
  Note what this means for coverage: `status: deferred` itself was **not** exercised. The fork was.
- **`scripts/engagement-state`** was called by the worker on nearly every turn, unprompted — it
  is `next` step 6's input and the workers used it as one.
- **`review-close` filing a bug it found (F-029.2).** BUG-0001 is a defect in the *vision
  document's* citations, found during a review of something else. Under the old pipeline that
  skill had nowhere to put it.
- **`answer-questions` creating an item (F-029.1).** WI-0004 (delete a person or an expense)
  exists because an answer widened the scope, and it carries the provenance to prove it.

## Two things that went wrong, both filed

- **H-008 — the driver called an impasse on one blocked item, not on the engagement.** Found live
  at turn 6, with three of four items still to build. Fixed mid-run (commit `3b6a94b`) and the
  run resumed; see H-008 for the state repair, recorded because it was a hand edit.
- **The turn budget was raised from 18 to 24** at turn 13, and the reasoning is in
  `meta/CHECKPOINT.md` under META-110 and in `meta/FINAL-REPORT-2.5.md` §6. 24 is the ceiling 1d
  itself was given. The config file still says 18; the raise was a command-line flag.

## Reading order

1. `project/tracker/board.md` — where the work got to.
2. `project/tracker/items/EP-001/questions/Q-004.md` — the termination question, in full. This is
   the artifact the session exists to produce.
3. `project/tracker/items/EP-001/history.md` — the three rows above.
4. `run/SIM-LOG.md` — the stakeholder's own account. `[PLANTED:` is coverage, `[ORGANIC]` is
   signal.
5. `run/iteration-log.jsonl` — durations, costs, the driver's observed status after each turn.

## A note on the transcripts

`run/007-sim.*` is not here: turn 7 was scheduled as a sim closing turn by the H-008 defect, was
killed before it wrote anything to `SIM-LOG.md`, and re-ran as a worker turn. The partial
transcript stayed in the working run directory rather than being banked, because the turn it
records never happened. Everything else in `run/` is what the driver wrote.

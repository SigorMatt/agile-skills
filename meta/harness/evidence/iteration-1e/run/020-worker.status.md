# Harness status — turn 20

This turn did nothing to the workspace, and that is the correct outcome: the pipeline has
reached a genuine stop.

- **Answers consumed first (amendment B): none were outstanding.** All eight human-addressed
  questions across EP-001, WI-0001 and WI-0004 are already `status: answered` with
  `answered-by: human`, `answered-at` set, and `## Consequences` naming real files. Nothing was
  left open by turn 19, so `answer-questions` had nothing to run on.
- **`next` ran and dispatched nothing.** Steps 1–7 of `pipeline.yaml`'s orchestrator, in order:
  the workspace validates (0 errors, 0 warnings, 7 items, 11 documents); `tracker/requests/`
  holds only `.gitkeep`, so no stakeholder request is open; no question is open at all, human- or
  architect-addressed; the runnable set is **empty** — five items are `done` and the only two
  non-`done` items, WI-0003 and EP-001, are both `blocked`, a status whose `owner` is `null`;
  and no epic remains at `open`, so step 6 had nothing to end. `scripts/engagement-state EP-001`
  reports `ended` ("the epic is 'blocked'; the engagement has ended", rest reached
  2026-08-27T02:28:28Z), which is step 7's required verdict.
- **Nothing was filed.** `next`'s contract forbids it from filing questions, and there was no
  real new question to file from anywhere else: the one thing this project is waiting on —
  a sample of the stakeholder's bank CSV export — was already asked in `EP-001/Q-001`, was
  answered with a deferral (*"I'll send you a sample later"*), and that deferral is exactly why
  WI-0003 is parked. Re-asking would be noise, not a question.
- **Nothing was committed.** `git status` is clean; `board-gen` reported the board already
  current and declined to rewrite its timestamp.

## Where the project actually stands

EP-001 ended at **E3, the impasse**, on turn 19. Five of six children delivered (WI-0001,
WI-0002, WI-0004, BUG-0001, BUG-0002); WI-0003 — the bank CSV import — did not, and the
stakeholder refused the sign-off over it: *"No, not as it stands — the bank import was part of
what I asked for and it isn't there. Everything else looks right. I'll send the file and then we
can finish it."* The epic carries no `outcome`, deliberately, because `blocked` is not a closure.

**Exactly one thing restarts this project, and it is the stakeholder's to supply:** a sample of
their bank's CSV export — or its header row plus two or three example rows, naming which column
holds the amount, the date and the description. `WI-0003/item.md` §Notes says so in those terms.
That file arriving moves WI-0003 from `blocked` back to its recorded `resume-to: draft`, refine
picks it up, and a delivered WI-0003 puts the engagement back at rest with every child delivered
— at which point a fresh sign-off is due and the ending can be E1 instead of E3.

Until that file exists, no skill in the pipeline can advance anything. No status has an owner
that would touch either blocked item, and inventing a CSV layout to unblock WI-0003 is precisely
the guess the question protocol exists to prevent.

## Note for the owner

The 3-skill turn budget was not touched — zero skill executions, because zero were runnable.
This is the second consecutive turn in which the loop's only legitimate move is to stop, and the
blocker is external to the pipeline in a way the toolkit has no channel for: `tracker/requests/`
is the stakeholder's inbound channel and only they can open one, and a question can only be filed
by a skill that owns a runnable item. There is currently no mechanism by which the pipeline can
say "we are still waiting on you for the file you promised" other than this status file. That may
be worth a toolkit finding: a *pending-input* channel, distinct from a question, for an item
parked on an artifact the stakeholder owes.

```json
{
  "stop_reason": "nothing-runnable",
  "skills_run": [],
  "open_human_questions": [],
  "items_touched": [],
  "last_action": "next ran steps 1-7 and dispatched nothing: no open request, no open question, empty runnable set (WI-0003 and EP-001 both blocked with null owner), and engagement-state EP-001 reports the engagement already ended at the E3 impasse",
  "notes": "The project is stalled on one external artifact: the stakeholder's bank CSV export sample, promised in EP-001/Q-001 and again at sign-off in EP-001/Q-004, never delivered. WI-0003 is blocked with resume-to: draft awaiting it; EP-001 ended at E3 (impasse) with no outcome recorded. Workspace validates clean (0 errors, 0 warnings), git is clean, board is current. No toolkit defect encountered this turn. Observation worth recording: the pipeline has no channel for telling the stakeholder it is waiting on an artifact they owe -- questions require a runnable owning item, and tracker/requests/ is inbound-only. Every future turn will stop here identically until that CSV sample appears in the project."
}
```

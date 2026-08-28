---
title: Exit 1 means at least one intended move failed, whatever fraction that is
version: 2
status: current
updated: 2026-08-28T13:39:28Z
updated-by: answer-questions
updated-for: BUG-0005
---

# ADR-0012 — Exit 1 means at least one intended move failed, whatever fraction that is

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for BUG-0005
- **Supersedes:** —

## Context

`README.md` enumerates three exit statuses and a reader uses that list to predict one. Its third
clause says 1 is what you get "when some file could not be moved while others were", and there is
a run whose status the list therefore does not let a reader predict: when *every* move fails,
`tidy` also exits 1 and nothing was moved alongside [src: BUG-0005; src: README.md].

The code has never made the distinction the sentence implies. `cli.main` ends with
`return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0`, so the status turns on
one predicate — did any intended move fail — and not on how many succeeded [src: tidy/cli.py;
src: ADR-0007]. The three other things a run can do are already outside that predicate: a file
that was never going to move gets a `leave` line and does not affect the status, a move carried by
ADR-0003's fallback is a success that says so, and a run that cannot start at all exits 2
[src: ADR-0007; src: ADR-0003; src: ADR-0006].

So the behaviour is settled and only the contract's wording is in question — but *which* wording
is not a free choice, because BUG-0005's own `## Notes` names the alternative: a distinct status
for a total failure. That would add a number to a published contract, which is a decision rather
than an edit, and it is why this is an ADR instead of a plan step [src: BUG-0005].

## Options considered

- **A — Keep three statuses and say what 1 actually means.** `README.md`'s third clause becomes
  "1 when a file that was going to move could not be", with the "while others were" condition
  dropped, so the sentence describes the predicate the code evaluates. Cost: one paragraph, and a
  reader who had inferred that 1 implies partial success has to unlearn it — which is the point.
  Risk: the sentence gets longer, and the exit-2 clause it sits beside is already long
  [src: BUG-0001 AC2; src: WI-0003 AC12].
- **B — A fourth status, 3, for a run in which nothing moved at all.** Cost: a new number in a
  contract `README.md` and ADR-0006 both bound to 0, 1 and 2, plus a code change in `cli.py` and
  a criterion nobody has asked for; scripts written against the old contract start seeing a status
  they do not know. Risk: it is the same growth ADR-0006 declined for the unusable-target case —
  "the contract grows faster than the tool" — and that argument, not the availability of a
  workaround, is what decides it here [src: ADR-0006]. A script that cares does have a way to tell
  the two runs apart without a fourth status, but it is dearer than reading a status: it compares
  stdout's `move` lines with the filesystem afterwards, as `## Consequences` sets out
  [src: tidy/cli.py]. That is a weaker case against B than version 1 of this ADR recorded, and it
  is left standing as the weaker one deliberately: if a per-file check is judged too dear to ask
  of a script, B is worth reopening on that ground rather than on a cheaper one that does not
  exist [src: BUG-0005/Q-001].
- **C — Leave the sentence as it is; "some file could not be moved" is true in an all-fail run.**
  Cost: none today. Risk: this is the reading `verify` recorded during BUG-0002 and
  `review-close` disagreed with, which is why the item exists; the paragraph is an enumeration a
  reader uses to predict a code, and leaving a run it does not cover means the next person to ask
  the question re-derives it from the source [src: BUG-0005].

## Decision

**A.** The tool keeps exactly three exit statuses — 0, 1 and 2 — and `README.md` states 1 as the
predicate the code evaluates: **at least one file that was going to move could not be moved** —
one of them, some of them, or all of them. No code changes [src: README.md; src: ADR-0006;
src: tidy/cli.py].

Checkable against the code as: `tidy/cli.py`'s last statement is a single `any(...)` over
`outcome.kind == "failed"` with no count or ratio in it, and every status the module returns is
one of 0, 1 and 2 [src: tidy/cli.py; src: run: grep -n "return " tidy/cli.py → exit 0, nine
hits: six numeric returns of 2, 2, 2, 0, 0 and the final 1-or-0, plus `parser`, `line` and a
rendered string].

Three things this decision does **not** disturb, each of which the same paragraph states and a
rewrite could break by accident:

1. **0 still covers a run in which files were left where they are.** A `leave` is not a failed
   move [src: ADR-0009].
2. **0 still covers a run that fell back for every file.** Those files arrived; the run says so on
   stderr and exits 0 [src: ADR-0007; src: BUG-0002 AC1].
3. **2 still covers the four ways a run cannot start**, including the `--rules` file, which
   WI-0003 requires this paragraph to name [src: ADR-0006; src: WI-0003 AC12; src: BUG-0001 AC2].

## Consequences

- A reader can predict the status of any run from the paragraph alone, including the all-fail run
  in BUG-0005's reproduction, without reading `cli.py`.
- A script that wants to distinguish "nothing moved" from "some moved" cannot get it from the
  exit status, and stderr will not give it to them cheaply either. No phrase runs through all
  five of `apply_plan`'s failure messages — `was left where it is` is in three of them and
  `could not` in three, and the two sets are not the same three — and whichever a script greps
  for, the failure lines arrive interleaved with the banner and with ADR-0003's fall-back line,
  which reports a *success* [src: tidy/apply.py; src: ADR-0007; src: ADR-0003;
  src: run: grep -n "Outcome(\"failed\"" tidy/apply.py → exit 0, five distinct messages].
  What such a script can do is read stdout — one `move` line per intended move, printed before
  anything is attempted — and then look at the folder: every source named in a `move` line that
  is still where it was is a file the run did not move away, and if that is all of them, nothing
  moved [src: tidy/cli.py; src: run: python3 -m tidy FOLDER --apply, on a folder whose band
  directory is mode 0500 → exit 1, a `move` line for each file, and each source still at the top
  level]. The one case that reading does not distinguish is the failure in which a copy reached
  the destination and the original could not be removed: that file is still where it was, and the
  run did not move it away, but a copy of it did arrive [src: tidy/apply.py; src: ADR-0007]. That
  is a real cost of A — a per-file check against the filesystem rather than a number to read —
  and nobody has asked to pay it the other way.
- The regression test BUG-0005 AC3 asks for pins the behaviour this wording describes, so a later
  change to `cli.py`'s last statement fails the suite rather than silently making the README wrong
  — which is how this defect was made in the first place [src: BUG-0005].
- **Reversibility: cheap for the prose, dearer for the contract.** Rewording again is one
  paragraph. Moving to B later means a new status in a published contract: a code change in
  `cli.py`, a README rewrite, a criterion, and any script already relying on 1 for the all-fail
  case. That asymmetry is the reason to say plainly now what 1 means rather than to add a number.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-28T13:39:28Z | answer-questions | BUG-0005 | Corrected the two sentences telling a reader to count `could not be moved` lines on stderr: only one of `apply_plan`'s five failure messages contains that string, and the all-fail run this ADR is about emits none of it. `## Consequences` now names the observable that exists — stdout's `move` lines checked against the folder afterwards — and option B's risk now rests on ADR-0006's contract-growth argument, with the workaround stated at its real cost. The decision is unchanged |
| 1 | 2026-08-27T22:17:46Z | plan | BUG-0005 | First version: three exit statuses are kept and 1 is stated as "at least one intended move failed", rather than adding a fourth status for a run in which nothing moved |

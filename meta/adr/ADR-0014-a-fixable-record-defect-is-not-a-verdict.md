# ADR-0014 — A fixable record defect is not a verdict on the engagement

- **Status:** accepted
- **Date:** 2026-09-11
- **Unit:** META-171
- **Amends:** `harness/run_iteration.py` — `Driver.decide`'s validator branch, the run loop's
  H-004 reschedule, and `TERMINAL_STOPS["validator-failed"]`'s recovery sentence. Adds
  `harness/prompts/repair-turn.md` and the `repair-turns` config key. Nothing in the toolkit
  (`methodology/`, `spec/`, `scripts/`, `adapters/`) changes: this is a decision about what the
  **harness** does when the workspace it is driving stops validating.
- **Findings:** answers **H-022** (*should a fixable citation error halt the whole engagement?* —
  question-shaped). Rests on **H-010** (a budget bounds work, not the engagement) and **H-002**
  (an interruption and a verdict need opposite recoveries). Occasioned by **F-113**, but not
  fixed by F-113's fix: the halt-vs-continue question outlives the specific defect that raised it.

## Context

Iteration 5 stopped at turn 11 with `stop-reason: validator-failed`, mid-`WI-0002`, and was never
resumed. The workspace it stopped over is banked at
`meta/harness/evidence/iteration-5-envel-abandoned/`. The line that killed it:

```
tracker/items/WI-0002/history.md:14: ERROR [claim.citation.unresolved] 'path:line' is not a
citation form this gate can check
```

`[src: path:line]` is not a citation. It is `verify` naming the citation *form*, in prose, to
describe four real citations it had just found falsified. The same execution wrote the same
phrase three times; two were inside backticks and were masked, one was not. At that moment all
nineteen of the item's acceptance criteria passed, all seven binding ADRs conformed, and 69 tests
were green on the branch head.

Both readings in H-022 are real and the finding declines to pick between them. **Correct for the
harness:** fail hard, surface the defect, study it — which is exactly what happened, and it
worked; F-113, F-114, ADR-0013 and META-170 all came out of that stop. **Wrong for consumer
modeling:** a real engagement does not die of a punctuation defect in one sentence of one history
row. A consumer would fix the line and carry on, and a harness whose failure mode is unavailable
to its consumers is measuring something the consumer will never experience.

The decision below keeps both. The defect still stops everything until it is fixed; what changes
is *who is asked to fix it*, and whether the engagement dies when the answer is "the worker
could have".

Six reasons were derived before the code was read. All six were then tested against the code.
Four survive as stated, two needed correcting, and the corrections are in the numbered sections.

## 1. H-010's principle carries; H-010's *mechanism* does not — and that matters

H-010 settled the analogous question one level up: five runs hit the turn budget, twice landing
between the termination gate filing the sign-off and the stakeholder answering it, and the driver
called that a verdict. The lesson written into the code is that **a budget bounds work, not the
engagement**. H-022 is the same shape: a fact about one line of prose, converted into a verdict on
an engagement that was passing every check it had.

**The correction.** H-010's *mechanism* was resumability — `turn-budget` moved into
`CONDITIONAL_STOPS`, and `stop_is_resumable` is consulted in exactly one place:

```python
if self.state and self.state.get("status") == "stopped" and not self.args.fresh:
    reason = self.state.get("stop-reason")
    if stop_is_resumable(reason, scan_project(self.project_dir)):
```

That branch runs when a **human reruns the command**. It cannot help here, because the whole gap
is *inside* the run (§6). So this reason survives as a principle and not as a precedent for the
implementation; the mechanism had to be new.

There is also a real asymmetry to state rather than paper over. The turn budget is the driver's
own counter — a fact about the harness. A failing validator is a fact about the **workspace**, and
the harness has no business overruling the disk (H-014 is the rule that says so). What this ADR
claims is narrower than "ignore the disk": the disk says the record is broken, the driver believes
it completely, and nothing advances until it is fixed. The only thing denied is the inference from
*the record is broken* to *the engagement is over*.

## 2. Bounded, because nothing else in `decide` would ever stop the loop

An unbounded allowance would be ADR-0011 Context (b)'s loop in a new costume: try, fail, repeat
until the budget is spent. The instinct is that some other guard would catch it. **It would not,
and the code is explicit about why.** The validator branch is the *first* test in `decide`, and
every other stop — including the stall check —

```python
fingerprints = self.state.get("fingerprints", [])
if len(fingerprints) >= 3 and fingerprints[-1] == fingerprints[-2] == fingerprints[-3]:
```

sits **below** it and is unreachable while the validator is red. A worker that edits something
every turn and never fixes the defect changes the fingerprint every turn anyway, so even a
reachable stall check would not fire. Without a bound, the only thing that ends a repair loop is
the turn budget — which is precisely the outcome H-010 spent an ADR preventing. The bound is what
makes this *work* rather than denial.

## 3. Consecutive, because a repair that worked is progress

The counter resets the moment `validate-workspace` exits 0. N therefore bounds **this defect**,
not the run's lifetime supply of them: a run that hits three unrelated, individually fixable
defects across twenty turns fixes all three, and a run that cannot fix one stops on it. A lifetime
counter would punish a long, healthy engagement for having been long. Survives as stated, and the
test `a success between two failures gives the second a fresh allowance` is what keeps it true.

## 4. The original error, because the first error is the finding — *with a limit*

The value of iteration 5's trail is the first error. Whatever the workspace exits on after two
repair turns may be a symptom of the repair rather than the defect, so a stop reporting only the
last error would report the wrong thing, and the study this harness exists for would start from
the wrong line. The stop detail therefore names both.

**The correction, found in the code.** What is preserved is the validator's *verdict line*, not
the error:

```python
"validator-tail": (validator.stdout + validator.stderr).strip().split("\n")[-1:],
```

The driver keeps the **last line only**, which for `validate-workspace` is its summary —
`validate-workspace: 1 error, 0 warnings`. That is exactly what iteration 5's `state.json` says,
and it names no defect at all. So the reason survives in form (original, not last) and is thin in
substance (a count, not a line number). Widening the driver's reading of the validator is a
separate change with its own blast radius — every stop detail's shape — and it is **not made
here**; it is written down in Consequences as a deferral rather than left as a silent weakness.
The repair turn itself does not depend on it: the prompt's first instruction is to run
`validate-workspace` and read what it says.

## 5. Repair turns count against the turn budget, and the closing-turn contrast holds

A repair turn is work, and H-010's principle is that a budget bounds work. Exempting repair turns
would make `--max-turns 12` mean a different amount of work depending on the health of the record.

**The contrast was checked and it holds.** The one existing exemption is in the loop:

```python
if self.state.get("next-job") == "closing":
    say(... "the closing turn is not the budget's to spend — giving it")
```

It is exempt for a reason that does not reach a repair turn: it exists for the **engagement's**
benefit rather than the work's (the stakeholder sees the ending of every run, not only the short
ones), it is **one** turn, it is given **once** (`closing-turn-given`), and it is the **last**
thing that happens. A repair turn is none of those. The test
`repair turns are not exempt from the turn budget` reads the budget block and asserts the word
`repair` never appears in it.

And the cost of counting them is bounded, which was checked rather than assumed:
`engagement_terminal` reads endings off the items and the engagement state and never consults the
validator, so a broken workspace is **not** terminal — a run that spends its budget mid-repair
stops `turn-budget`, which is resumable, and `state.json` still carries `next-job: repair`, the
counter and the original error. Nothing is lost by counting.

## 6. Not resumability, because resumability asks the human

The alternative shape was to move `validator-failed` into `CONDITIONAL_STOPS` beside
`turn-budget`. It fails on two code facts.

First, resumability is about **a human rerunning the command** (§1): the run has already ended,
the trail is closed, and somebody has to come back. The gap F-113 exposed is inside the run — the
worker was alive, held the context, and was better placed than anyone to repair a line it had just
written.

Second, the recovery sentence being replaced was not merely wrong in emphasis, it was partly
false:

```python
"validator-failed": "the workspace no longer validates; fix it, then --fresh or --reaudit",
```

`--reaudit` re-runs the contamination rules over stored transcripts and clears only a
contamination stop — `if self.state.get("stop-reason") == "contamination"`. It could never clear
`validator-failed`. Of the two exits offered, one did not exist and the other, `--fresh`, archives
the run's logs, state and transcripts and starts over. The old sentence asked a human to repair a
record the worker could have repaired, and then offered them a door that was painted on.

## Decision

**On a non-zero `validate-workspace` after a worker turn, the driver grants a bounded self-repair
allowance instead of stopping.**

- **How many.** `--repair-turns N`, else the iteration config's `repair-turns`, else **2** — read
  exactly the way `--max-turns` is read, so no existing iteration config has to carry the key.
- **Consecutive.** The count is of consecutive failing **worker** turns. A sim turn neither burns
  nor resets it: the contamination boundary confines the stakeholder to answers and requests, so
  it can neither break the record nor repair it.
- **What a repair turn is.** A worker turn given different instructions —
  `harness/prompts/repair-turn.md`, recorded per turn as `prompt: repair-turn` with its own
  version — whose only job is making the validator green: no `/next`, no dispatch, no advancing an
  item, no editing anything under `.claude/`, and no deleting a sentence to silence a gate.
- **Green resets.** The counter clears and the engagement resumes where it was — re-derived from
  disk by the same branches that decide every other turn, so "where it was" is not remembered, it
  is read.
- **Exhaustion is terminal.** N+1 consecutive failures stop the run `validator-failed`, and the
  detail names **both** the error that opened the allowance and the one it still exits on (when
  they differ; one line when they do not).
- **Not reschedulable.** The H-004 guard that hands a worker turn to the sim when human questions
  are open does not fire on a repair turn. Its premise — that the turn would halt at orchestrator
  step 2 having done nothing — is false for a turn that never runs the orchestrator, and firing
  would spend one of a bounded number of repair turns on something that cannot repair anything
  *and* lose the repair job, because `decide` re-derives `next-job` after a sim turn.
- **Not exempt from the turn budget** (§5).
- **Answerable from the log.** `repair-granted`, `repair-succeeded`, `repair-exhausted` and
  `repair-keeps-the-turn` go to `iteration-log.jsonl`, so *why did this run stop* stays answerable
  without opening a transcript — the standard the existing stop code is written to.
- **What survives a resume.** `repair-turns-used`, `repair-original-detail` and
  `repair-last-detail` live in `state.json`, because `state.json` is the whole of what survives a
  killed driver.

## Consequences

**The harness keeps its hard failure, and moves it.** The run still dies on a record defect — but
on one that defeated the worker across N consecutive turns of trying, which is a much stronger
finding than "one line of prose did not parse". Iteration 5's stop remains exactly as valuable as
it was, and would have been *more* valuable: it would have recorded whether the worker could
recognise and repair its own citation defect, which is an open question about the toolkit that the
old stop made unanswerable.

**A new way for a run to lie, and what bounds it.** A worker told to make a gate pass can make a
gate pass dishonestly — delete the sentence, weaken the claim, edit the validator. The prompt
forbids all three by name, and the contamination audit already fails the run if a worker writes
outside the project. It is not enforced beyond that: a dishonest repair inside the workspace is
visible in the diff and in the repair turn's own journal entry, and detecting it is a judgement,
not a rule. **This is the cost, stated plainly**, and the reason `repair-turns` defaults to 2
rather than something generous.

**Deferred, deliberately: the driver reads one line of the validator.** §4's correction. The stop
detail and the repair prompt both carry `validate-workspace: N error(s), M warnings` rather than
the error line itself. Widening `scan_project`'s `validator-tail` changes the shape of every stop
detail the driver writes and belongs to its own unit; until then the first thing a repair turn
does is run the validator itself, and the console log of the turn that failed has the full output.

**`--fresh` still discards the engagement, and now it is rarer.** The only route to
`validator-failed` is a spent allowance, so the terminal stop's recovery sentence describes that
and no longer offers `--reaudit`, which never worked for it.

## Alternatives rejected

- **Leave it terminal (the status quo).** Defensible for the harness alone, and the finding says
  so. Rejected because the harness's purpose is to model a consumer engagement, and no consumer
  engagement dies of a fixable line in a history row. A failure mode the consumer cannot
  experience teaches nothing about the consumer.
- **Make `validator-failed` resumable.** §6.
- **Unbounded self-repair.** §2. It converts a verdict into a loop that spends the turn budget on
  one defect, with no other guard in `decide` able to reach it.
- **A lifetime rather than consecutive bound.** §3. It ends long healthy runs for the crime of
  length.
- **Repair inside the ordinary worker prompt** (an amendment saying "if the validator is red, fix
  it first"). Rejected on the record rather than on taste: the per-turn `prompt-version` is how
  the log says which instructions ran, and a turn that is sometimes a repair and sometimes not
  makes that record unreadable. It also gives a worker holding a broken record permission to keep
  dispatching work, which is the opposite of what the defect calls for.
- **Exempt repair turns from the turn budget.** §5.

# Final report — builder session four: the retro skill

Date: 2026-08-30. Units META-132 … META-143, 32 commits. Predecessor: `meta/FINAL-REPORT-3.md`,
which stamped ROADMAP §2 and opened the gated tracks. This session took the first of them.

`./scripts/check` is green across **30 steps** (was 28). `harness/tests/test_harness.py` is 74
tests (was 70). `scripts/lib/selftest.py` is 252 cases (was 213). `fixtures/broken-workspace` is
**82 codes, unchanged** — which is the proof of the migration, not an absence of work.

---

## 1. What was built

**`retro` 0.2.1** — a ninth skill, and the first one whose subject is the record rather than the
work. It reads an ended engagement's trail and writes one report with two audiences: an
engagement-local retrospective for the team that ran it, and candidate toolkit findings marked
`PROPOSED`, in the ledger's own format, for a human to send upstream. It is the community
feedback engine of the open-source era: every consumer's real run can generate findings about the
method, and none of them can file one.

Everything it is, is derived in **`meta/adr/ADR-0009-retrospective-reading.md`** before any code
was written. Five decisions carry the design:

1. **Its input is the record and the installed contracts, and nothing else.** No SIM-LOG, no
   harness, no upstream ledger. A consumer has none of those, and calibrating a skill on an input
   no consumer has overstates everything it can do in the field. The contracts are the one
   non-record input, because *"did that gate pass on the contract or on the worker's
   discipline?"* is unanswerable without them and every consumer has them.
2. **It is read-only over the engagement it audits, and the boundary is two paths.**
   `artifacts/retro.md` and its own journal entry on the epic. No history row, no bug, no
   reopening, and — less obviously — **no questions**: after an ending a blocking question has
   nowhere to resume to, and a human-addressed one asks a person who has already been told the
   work is finished. An auditor that can edit its subject cannot show it did not edit the
   evidence into agreement with its conclusions.
3. **Dispatch keys on the engagement's state, not on a status.** `scripts/engagement-state` gains
   a fifth verdict, **`closed`** — ended *and* the report exists — so `ended` now means the retro
   is still owed. `next` 0.4.0 gains one step that dispatches on `ended`, and it terminates
   because writing the report changes the verdict. F-045's lesson applied a second time: the
   orchestrator does not decide what "over" means, and it does not decide what "fully closed"
   means either. One function, three consumers.
4. **Nothing already valid became invalid.** `validate-workspace` does not require a report, no
   gate depends on one, and the retro is *dispatched* automatically and *enforced* nowhere —
   because after an ending there is nobody left to escalate a refusal to. Proved by execution:
   `./scripts/check` copies `examples/toy-project`, validates it clean, adds a report, validates
   it clean again, and asserts the verdict moves `ended → closed`.
5. **The quality bar ships inside `process.md`.** The eighty-seven filed findings are why this
   project's findings are written the way they are, and a consumer gets none of them. So the bar
   is written into the procedure — evidence first, class over specimen, severity honest,
   positives recorded — with two worked examples that differ only in whether the counterfactual
   can be written without naming the project's subject.

Supporting it: **`spec/retro.md`** (the report schema, the `PROPOSED` format, the closed
classification set), **`scripts/lint-retro`** and **`fixtures/retro/`** (25 codes and a
must-pass report), `spec/ids-and-statuses.md` §3.6, a new `process-analyst` persona, and
`pipeline.yaml` 0.6.0.

### The classification, and the failure mode it exists to prevent

Three classes: `toolkit-defect`, `project-circumstance`, `observation`. The failure mode is
filing *"this project was hard"* as *"the skill is broken"* — the cheap failure, because a
difficult engagement produces friction everywhere and every piece of friction can be phrased as a
complaint about a tool. A ledger that fills with those stops being read, and the real defects
then arrive into a channel nobody is reading.

Nothing mechanical decides a classification. What is mechanical is that the distinguishing work
was **written down**: `Counterfactual:` and `Recurrence:` are required on every `toolkit-defect`,
and the rule is that a proposal whose counterfactual cannot be stated without this project's
subject matter *is* a `project-circumstance`. That is ADR-0008 §4's move — make the wrong call
attributable rather than absent — used again.

### Non-vacuity, the one thing a program can check here

A retro that opened no files and a diligent retro of a flawless engagement produce the same empty
report. `## What was read` is therefore declared, and `lint-retro --require-scope` checks it
against the workspace: every item named or explicitly not read, counts that cannot exceed what
exists. F-033 and F-066 are that same defect twice in this project's own scripts, and reading is
this skill's whole job.

---

## 2. The record-model library (cluster 2)

`meta/FINAL-REPORT-3.md` §6.3 named the residual: *"a rule about a record's structure,
implemented against lines or against a state"* — F-069 and F-073, twice in one session.
**`scripts/lib/record.py`** is where that rule is now implemented once. It owns where a bullet
ends, how far a labelled declaration runs, what a fence is, what a section is, and what an entry
is. `workspace.py`, `claims.py`, `lint-answers`, `lint-claims`, `validate-workspace`,
`transition` and `lint-retro` all read it.

Two granularities are exposed on purpose and the difference is documented: `blocks()` (a bullet
**with** its continuations) and `paragraphs()` (blank-line separated, fences skipped, and
deliberately *not* split on bullets, because a claim and the clause qualifying it live in one
paragraph however the author wrapped it). Collapsing them would have changed `lint-claims`'
findings, which is not what "behaviour-identical" means.

**The proof is that nothing changed:** 82 broken-workspace codes, every gate step, all fixtures.
The proof that the model is load-bearing is that it was mutation-tested — reverting the
bullet-end rule to "the next bullet only", or making a declaration one line, fails
`./scripts/check` at the crossed-answers fixture *and* at the self-test.

**The migration found F-074**, which is the class a third time and in the loader every validator
reads through: `load_journal` took a bullet's first line as its value. So `journal.item` passed on
a wrapped bullet and would have failed without one — `examples/toy-project` has carried such an
entry since META-067 — and a wrapped `**Status:**` bullet yields no claim at all, leaving F-019's
exact failure unchecked. It survived F-073's fix because that fix went where the defect had been
*seen* rather than to the thing two scripts were both doing.

---

## 3. Cluster 3, and one correction

**H-017** fixed as filed: the driver reads the turn number out of the status file's own heading
and refuses a file stamped for another turn, beside H-005's mtime test — 4c's turn 16 is the case
only the stamp catches, because it exited cleanly and the file it left was not stale, it was
somebody else's.

**H-017's companion was reported with the wrong cause, and the ledger says so.** `board-gen`'s
notice was already on stdout. What made four runs read it as a failure is that `run-gate` merges
a command's two streams into one tail, and the wording — *"not rewriting the timestamp"* —
describes a refusal. The fix is the wording. Implementing what the finding literally asked for
would have changed nothing.

**H-018** (an archived run directory saying `status: running`, with a pid) and **H-019** (the
iteration-4 configs budgeting 24 turns for a run that needed 27) filed and fixed. H-019 was fixed
in **both** config files rather than only the one the mission named: correcting one and leaving
its twin is fixing the specimen instead of the class.

---

## 4. The ground-truth test — the numbers, and how to read them

The subset was written down and **committed before anything ran** (`meta/journal.md`, META-140
part one). Ten findings were filed across iterations 2 and 3. **Five are workspace-visible.**
The five that are not are all harness findings whose evidence is a run transcript, a driver log
or the sim's own skill file — nothing a consumer's project contains. That exclusion is the
honest half of the number and it is written down with its reasoning per finding.

Two engagements, two context-free subagents, each given a workspace path and told to read the
skill's own files and execute it. Neither saw this repository or the other.

### Recall — 1 full hit, 2 partial, 2 misses

**Strictly, full hits only: 1 of 5 — 20%. Counting partials at half credit: 2 of 5 — 40%.**

| Target | Result |
|--------|--------|
| **F-061** | **full hit, sharper than the filing** — see §4.1 |
| **F-062** | **partial, and a miss on the marquee case** — it found the *absence* of any cross-answer check and asserted that two answers narrow an earlier one; it never reached the sentence in `vision.md` that `implement` repaired instead of putting back to its author |
| **F-063** | miss — the word "recommendation" does not appear in the report |
| **F-064** | miss in iteration 3 — though the *class* was found in iteration 2's run: *"asked the stakeholder eleven questions and never asked what they had not been asked"* |
| **F-065** | partial — its class, aimed at D12 audits rather than at the criterion-about-criteria specimen |

**The marquee case was missed.** The mission's bar was *"a retro that reads that record and does
not surface the contradiction's handling has failed the concept"*, and `retro` 0.1.0 did not
surface the handling. That is stated here rather than argued around.

### Precision — 28 proposals, nine verified in depth, zero unfounded

22 `toolkit-defect`, 4 `project-circumstance`, 2 `observation`. Nine were checked against the
current `spec/`, `methodology/` and `scripts/` (iteration-2 P-2/P-3/P-6, iteration-3
P-3/P-4/P-8/P-12, live P-1/P-2): **none is unfounded.** Two are duplicates of findings already in
the ledger — which is not noise, because ADR-0009 §8 hands de-duplication to the triager for a
reader that has not seen the ledger. The remaining nineteen are not individually verified and
nothing here claims they are.

**All four `project-circumstance` entries are correctly classified**, each with a counterfactual
that genuinely cannot be written without the project's subject: *"two flashcards may share a
front side"*, an exactly-on-the-boundary criterion in the product's own interface, a filesystem
primitive the tests cannot exercise, a stakeholder who decided something new after seeing the tool
work. The failure mode ADR-0009 §5 was designed against did not occur, in readings with every
incentive to inflate.

### 4.1 The result worth keeping

F-061 was filed as an observation and closed with *"Direction: none required now… **Revisit when
the retro skill exists.**"* The retro revisited it, from the record alone, and found the mechanism
the original never had:

> `EP-001/Q-005`'s option B — **the option `spec/question.md` §2 requires a sign-off to offer** —
> told the stakeholder that accepting with a named follow-up meant *"the engagement still closes
> as delivered, and the new work is opened"*. They chose it. Half of it was not executable: an
> engagement ends only from rest, rest requires every child terminal, and the follow-up item is
> created at `draft`.

The second sign-off is not the price of a conditional acceptance. It is the price of the protocol
promising an ending its own status model forbids, in the sentence it obliges every sign-off to
print. Recorded as an addendum to F-061; the spec change is the owner's.

### 4.2 The re-run, and what it is not

The miss was locatable: `process.md` step 5 **named** the F-062 shape instead of **instructing the
join**, and nothing told the reader to consider the questions as a *set* — which is what F-063 and
F-064 both are. Filed as **F-078** and fixed in **`retro` 0.2.0**: the questions are read as a set
with three counted questions, and step 5b instructs the join outright — follow every
`[src: <ITEM>/Q-nnn]` under `docs/` to the answer it cites and the answers that came after it,
and say which of two things the record shows.

Re-run over the same record by a fresh context-free subagent: **3 full hits and 1 partial** of
iteration 3's four targets, against 0.1.0's 0 and 2. F-062 comes back with the quote, the three
documents standing on it, both `answered-at` stamps and the `implement` entry that repaired it.

**This is not an independent measurement and must never be quoted as one.** The change was made
after reading the miss. What it establishes is that the instruction is *followable* and that the
misses were procedural rather than inherent in reading a record. **The calibration reading remains
0.1.0's: 1 full, 2 partial, 2 misses.**

Two behaviours in the re-run exceed what the ADR claims. `P-8` rediscovers F-064 and then
**declines to file it as a defect**, because it opened the installed contracts and found `DE8` and
`kind: elicitation` already there. And the positive record carries the counter-evidence to its own
F-063 observation: *"The stakeholder overruled the team's recommendation three times, so the
closed-form questions did not steer the answers."*

---

## 5. The live test

A context-free subagent, given only `recall-4c`'s workspace copied to scratch:

- `next` reached step 7, quoted the verdict — *"EP-001 ended … the retrospective has not been
  written"* — and dispatched `retro`.
- `retro` wrote **exactly two files**. Verified independently by modification time across
  `tracker/` and `docs/`, not taken on trust.
- `next` run again reported **`closed`** and stopped.

The report's own two strongest proposals are the ones that made the session worth running: *a
claims gate scoped to a work item's branch diff is empty by construction*, and *a claim quantified
over a family is audited by opening the family's shared fixture, and the exception lives in a
member* — which is F-001's standing residual sharpened into something a rule could bite on.

The live test also found **F-075**: `lint-retro` read a `[src: …]` quoted inside backticks as a
real citation, failed the gate three times on correct prose, **and the execution reworded its
prose until the gate passed** — F-073's pathology exactly. The cause is F-037's class:
`claims.py` has carried the mask for this since F-037 and `lint-claims` uses it; `lint-retro`,
written three units later in the session that made *one parser, every reader* its theme, did not.

---

## 6. Findings

Nine entries this session — F-074 … F-079, H-017 … H-019 — plus addenda to F-061 and F-075.

| # | What | Status |
|---|------|--------|
| F-074 | the validator read a journal bullet one line deep (F-073's class, third occurrence) | fixed |
| F-075 | a quoted citation read as a real one; the run reworded prose to pass | fixed |
| F-076 | `implement`'s claims gate examines an empty window **by construction** | **deferred** |
| F-077 | a `path:line` citation resolved for ever, whatever was at the line | fixed |
| F-078 | the retro's step 5 named a shape instead of instructing the join | fixed (0.2.0) |
| F-079 | the retro must journal and had nowhere legal to put the entry body | fixed (0.2.1) |
| H-017 | a turn that exits without writing a status leaves the driver reading a stale one | fixed, with a correction to its companion's cause |
| H-018 | an archived run directory says it is still running, with a pid | fixed |
| H-019 | the iteration-4 configs budget 24 turns for a run that needs 27 | fixed |

**F-076 is deferred deliberately and the reason belongs in this report.**
`spec/doc-header.md` §5 says `implement` does not write to `docs/`; `implement` carries a hard
`claims-are-sourced` gate scoped to its branch diff; so the gate's window is empty every time, by
the toolkit's own rules. But §5 is also violated in practice — a D7/D12 send-back has had
`implement` edit `vision.md`. **Both cannot stand.** Choosing between them is the
*document-as-deliverable* derivation (F-057, F-058), not a patch. Rescoping a hard gate on one
session's reading, in the session that also introduced the reader, is how a gate gets weakened by
the thing it was meant to check.

### Positive record (2026-08-30, the retro's first four runs)
Four executions by four independent context-free subagents, no two sharing a context. **All four
wrote exactly two files**, verified by mtime afterwards — the read-only boundary held under
execution and not only in the contract. All four recorded `workspace-valid` as **failed with its
reason** rather than skipped or passed, on a gate failing for something outside their control.
All four declared a scope that `--require-scope` checked against the workspace and accepted. Three
of the four wrote a `project-circumstance` entry rather than inflating it, and one withheld two
proposals because the installed toolkit already fixed them, putting them in the positive record
instead. Two of the four hit a gate on their own correct work and **neither weakened the work to
pass it**: one declared a stray scratch file in the gate's own bullet rather than tidying it away
(F-079), and one recorded `workspace-valid` as failed with its reason on every run.

---

## 7. Versions bumped

| Skill | From | To | Why |
|-------|------|----|-----|
| `retro` | — | **0.2.1** | new; the set reading and the citation join (F-078); the journal body on stdin (F-079) |
| `next` | 0.3.0 | **0.4.0** | orchestrator step 7 and the `ended-engagements-are-read` gate |

`pipeline.yaml` 0.5.0 → **0.6.0**. `spec/skill-contract.md` revision 5 (`process-analyst`),
`spec/ids-and-statuses.md` revision 5 (§3.6), `spec/retro.md` revision 1. No other skill contract
changed — the retro was added to the pipeline without touching the seven skills that do the work,
which is the property ROADMAP §2 condition 1 is about.

---

## 8. What the next session should do

**Not another feature. Run the retro inside a real iteration.** Every reading so far has been of
a *banked* record — no product source, no commit history, and contracts newer than the ones the
record names. The next harness iteration should end with `next` dispatching `retro` as the last
step of the run, on a live workspace with its source tree and its git log present, and the report
read as part of the findings pass. That closes the loop the skill exists for and it is the only
thing that tests the two inputs no banked copy can supply.

Three things to carry into it, in order:

1. **The owner's triage of 37 proposals.** Four reports are banked in
   `meta/evidence/retro-calibration/`. They are the first output of the feedback engine and
   nobody has triaged them. The strongest are named in §4.1 and §5. This is a reading session,
   not a building one.
2. **The two deferred classes, now with a third member.** *document-as-deliverable* (F-057,
   F-058) has gained **F-076**, which sharpens it into a question with two answers that cannot
   both be right. *half-written record* (F-036, F-043, F-051, F-053) is unchanged and F-053 was
   independently rediscovered by the retro, which is evidence it is still being paid for.
3. **Calibration, if the owner wants a number rather than a reading.** The honest way to get one
   is a *held-out* engagement: bank a run, write its ground-truth subset, and do not change the
   skill afterwards. This session cannot supply that number, because the procedure was changed
   after reading the miss, and §4.2 says so where the figure appears.

**What this session does not claim.** That the retro finds most of what is in a record: it found
one of five on its first honest reading. That the classification is reliable: it is judgement,
defended by a required sentence, and four correct calls out of four is a good sign and not a
result. That the reports are all sound: nineteen of twenty-eight proposals were not individually
verified. The retro's value is demonstrated — it found a live defect in the current kernel that
nothing else had, and it answered a question the ledger had been holding open for three days —
and its recall is not.

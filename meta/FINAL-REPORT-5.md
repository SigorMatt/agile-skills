# Final report — builder session five: document-as-deliverable, E4, and the accepted backlog

Date: 2026-09-10. Units META-144 … META-165, 60 commits before this one. Predecessor:
`meta/FINAL-REPORT-4.md`, which stamped ROADMAP §3 and left three things for this session: the
*document-as-deliverable* class, the E4 mechanism, and 19 accepted retro proposals sitting in the
ledger with nobody assigned to them.

Every unit was executed by a **dedicated sub-agent**; the orchestrator held only the mission,
`meta/plan.md`, `meta/CHECKPOINT.md` and each unit's verdict. That execution model is itself a
result and §6 reports what it produced.

`./scripts/check` is green: **`check: all steps passed`, 45 steps** (was 30 at the close of
session four). `fixtures/broken-workspace` is **108 codes** (was 82). `scripts/lib/selftest.py`
is **356 cases** (was 252). `harness/tests/test_harness.py` is **110 tests** (was 74). The ledger
holds **133 entries** (was 117), every one carrying a current status.

Every number in this report was read out of the repository for this report. Where the session
checkpoint's account of a unit differed from what the files say, the files win and §9 lists the
differences.

---

## 1. The derivation — ADR-0010, and the two ADRs it made necessary

### 1.1 ADR-0010 — document-as-deliverable (META-145, 699 lines, `3701069`)

Eight findings filed across five runs by four different actors — F-053, F-057, F-058, F-076,
F-087, F-092, F-093, F-095 — were one design debt. Every one of them is a question about a
document that the methodology answered by reaching for a rule about `docs/` as a *place*, when
the thing that decides the case is what the sentence is *about*. Five decisions carry the model.

1. **Record and deliverable are properties of sentences, not of files.** A *record* sentence says
   what happened or was decided and later work cannot falsify it. A *deliverable* sentence says
   what the product now is, and the next change can make it false. One file holds both, and
   `docs/product/vision.md` demonstrably holds three kinds at once. Every rule that decides on the
   directory is deciding the wrong question, which is why F-057 and F-058 are the same case seen
   from the skill's side and the gate's side.

2. **One rule generates the authority table, so the next case is decided rather than argued:**
   *a skill may write a document sentence exactly when it is the skill that causes the sentence's
   subject to change, and only if it is not the skill whose work that sentence is the standard
   for.* The table is the nine lifecycle events that change a document (L1 … L9, `review-close`
   appearing twice because an item close and an ending are different events) × the five document
   kinds, and its **nobody-cells are as
   load-bearing as the cells that name an actor** — F-057's whole complaint was a nobody-cell
   nobody had written down. Six nobody-cells are deliberate design (`verify` writes no document
   ever; `retro` writes none ever; `plan` does not revise intent; nobody writes a K8 sentence
   except `intake` at the start and `review-close` at the ending; nobody corrects a superseded
   ADR; nobody rewrites a claim sourced to a human answer). A seventh is a **residual gap the ADR
   does not close and names anyway**: a false sentence discovered after the engagement is closed
   has no owner.

3. **`spec/doc-header.md` §5's absolute does not survive, and the ADR says which line.** *"`implement`
   and `verify` do not write to `docs/`"* becomes: `verify` does not; `implement` writes only
   inside the invalidation set and deliverable set its plan declared, never a sentence that is the
   standard its own work is judged against, and never a claim sourced to a human answer. This is a
   real rule weakened, and §7 of the ADR says so in those words. It is the branch of F-076's
   two-way question that keeps an obligation on the actor whose work falsifies documents; the
   other branch — delete `implement`'s claims gate — was rejected with reasons.

4. **Three claim kinds, one audit obligation each.** *Cited fact* (a resolving citation, and D12's
   read for whether it supports the sentence); *quantified claim* (an enumeration entry naming the
   set, the method, the members and the verdict — because F-095's universal was audited **true**
   three times and was false, by opening what it cited rather than enumerating what it quantified
   over); *engagement-state statement* (K8 — owned by the ending, because by the time such a
   sentence is false every item is closed, which is F-093).

5. **The invalidation set is a `plan` output.** The pipeline asked what a change *touched* — a
   diff, with machinery built on it — and never asked what it *falsified*, which is not a diff,
   had no owner, and was first asked at the last gate (F-087). The question moves to the first
   stage that can act on it, and being wrong about it becomes attributable. The ADR's honest claim
   is exactly that narrow: completeness is obligation 12 and nothing decides it.

**The enforcement boundary is written per obligation, twenty rows, before any code existed.**
Twelve are `[auto]`; six are judgement with a mechanical shell that makes the judgement
attributable; **three — 10, 12 and 17 — are decided by nobody**, and the ADR names obligation 10
as the one to watch. §7 also predicts the failure mode of its own weakening: *"if a later run finds
`implement` widening its own scope through `docs/`, this section is where it was predicted."*

### 1.2 ADR-0011 — stakeholder silence and abandonment (META-150, 627 lines, `94606f5`)

Nothing in the pipeline could declare a stakeholder gone. E4 existed as a row with only a
withdrawal route, which requires the stakeholder to speak in order to be recorded as silent.

- **The unit is a silent round, and the two obvious units were rejected with reasons.**
  Wall-clock is wrong **in both directions**: an engagement resumed after a fortnight would
  declare a patient stakeholder abandoned on the first pass, and a harness iteration finishes
  inside an hour, so no threshold long enough for the first case can ever fire in the second. A
  clock measures how long the *pipeline* was not running. Turns are the harness's word and the
  toolkit must never learn it (ADR-0005). What is left is the pipeline's own asks: **one
  orchestrator halt on the human that observed no inbound change since the previous one.**
  "Inbound" is exhaustive and load-bearing — a reply in a `## Answer`, or a file under
  `tracker/requests/`. Nothing a skill writes is inbound.
- **The count is derived, never stored.** The trailing run of equal inbound digests over an
  append-only log at `tracker/waiting/<EP-ID>.md`. ADR-0003's argument applied again.
- **The halt is recorded before state is read, and the reader never writes** — which is why
  `scripts/record-halt` is a **separate program** from `engagement-state`. The property is
  structural rather than promised.
- **The threshold is `termination.silence.threshold_rounds: 3` in `pipeline.yaml`**, with
  `declared_by: review-close, and only review-close`. The orchestrator reads a verdict and decides
  nothing — F-045's lesson again: the orchestrator does not decide what "over" means.
- **E3 versus E4 in one test: did the stakeholder's own words arrive?** The asymmetry — E3 leaves
  the epic `blocked`, E4 closes it `done` — is defended rather than assumed, and the ending
  statement is a **document, not a question**, because at E4 there is nobody to address.

### 1.3 ADR-0012 — when the loop stops on the human (META-162, `b4f1909`)

F-097 asked for a collect-askable-questions pass before the loop stops on the human. The ADR
**rejected its literal Direction** — that pass is several actions plus a judgement inside the
scheduler, and *the collect pass it asks for already existed: it is the loop.* What was broken was
the step order.

- **One predicate, two clauses.** The loop stops on the human only when an **outstanding ask**
  exists (`addressed-to: human`, `open`, `blocking: true`, `## Answer` empty), and it stops there
  **last**, below every dispatching step. A **standing ask** — the elicitation among them — is
  surfaced at every halt, causes none, holds no rest, and accrues no round; `blocking: false`
  finally executes.
- **The one-action rule is preserved, unamended.**
- **The ADR-0011 reconciliation was checked, not assumed, and half of it failed.** §1 survives:
  `silent_rounds()` takes rows and returns a trailing run of digests, never reading a question,
  status or addressee, so changing which questions halt cannot change what a round is. §4 does
  **not**: *"a halt requires a question addressed to `human` that is `open`"* is false under the
  new predicate, since a standing ask is all three and produces no halt. Narrowed, not reversed,
  in the ADR and in `ids-and-statuses.md` §3.5a's copy of it.
- **A fourth deadlock site was found by derivation and fixed rather than moved**: DE5 demands the
  question closed, `abandoned` is the only honest closure, and DE8 accepted `abandoned` only at
  E4 — F-013's shape. DE8 now accepts it at any ending and asks in exchange for the half it never
  had: the waiting log must show the question was **surfaced**.

---

## 2. What each cluster changed

### Cluster 1 — document-as-deliverable (META-145 … META-149)

The ADR (§1.1), then `spec/doc-header.md` §4a/§5 and `spec/dor-dod.md` D7/D12/D13/DE4/DE6
(`c1fbde8`; **D13 is new and marked `[skill]` honestly**), then six skill contracts — `plan`,
`implement`, `verify`, `review-close` (`5e6434d`) and `intake` + `answer-questions` (`9adff0e`),
the last two found by the unit before them rather than rediscovered later as a finding. **`intake`
gets no `lint-claims` gate**, which is F-076's shape appearing in a new place and is recorded as
such.

Then the enforcement half, in two units:

- **The window** (`5ae1539`). `scripts/lib/scope.py` gains a **fourth state**,
  *out-of-scope-by-construction*: a window that could not have failed **passes with a mark**,
  never silently. `constrained()` takes the permission knowledge **from the caller**, because
  **no diff distinguishes "nobody wrote a document" from "nobody was allowed to"**. Five of eight
  cases failed against the pre-change scripts.
- **The obligations** (`a843114`). `scripts/lint-documents` implements the eight `[auto]`
  obligations that the contract units had been forced to write as `manual_check`, one rule per
  invocation, **the rule's name being the gate's name** so a procedure cannot drift from its
  contract silently (F-059). Non-vacuity was proved twice, the second time with **every rule body
  stubbed** — because moving the script aside only proves the file is needed.

META-148c was **absorbed rather than skipped**: its historical cases already ran as by-execution
`./scripts/check` steps landed by the two units before it, and re-authoring them would have put
one assertion in two places. What was genuinely left of it — F-053's class as the lifecycle-state
input — is a status decision and moved to META-149.

Cluster 1's ledger pass (`f474027`) fixed F-076, F-087, F-092, F-093, F-095, F-057 and F-058 with
resolving citations, recorded **F-053 as NOT fixed**, and filed F-100…F-103.

### Cluster 2 — the E4 mechanism (META-150 … META-153c)

The ADR (§1.2), then the model on paper (`877ee85`) across `ids-and-statuses.md` §3.5/§3.5a,
`question.md` (`status: abandoned`, the fourth question status and the pipeline's only vocabulary
for absence), `dor-dod.md`, `workspace-layout.md` §1.4 and `pipeline.yaml`'s `termination.silence`
block plus two transition rows the derivation found missing.

**ADR-0006 was repaired by a header pointer, not by a `## Corrections` entry**, argued four ways:
stretching §4b in the file its own ledger watches would be this repository failing F-067.

Then the programs (`4d1b7ce`): `record-halt` as a separate script; `engagement-state`'s
`abandoned` verdict; `check-epic-signoff`; `validate-workspace`; `next` step 3 and `review-close`
step 10. **The transition registry grew a `satisfied_by` class rather than taking a false triple**
— pinning the actor is what makes the registry bite. The threshold's single-sourcing was proved
by execution across all three consumers.

`fixtures/abandoned-engagement/` (`e9f8d79`) exercises E4 both ways, with digests **computed**
rather than transcribed, and **three defects reported rather than bent around**.

Harness side (`b845342`, separate commit): a sim job that legitimately declines to answer, and the
driver recognising a declared E4 as a terminal epic-done-class stop. 74 → 105 tests. **The driver
asks** rather than reimplementing the rule, and a test forbids the threshold's mechanics from the
driver's source. `abandoned` is checked **first**; an undeclared abandonment is **not** a stop;
the declared one takes no closing sim turn.

**META-153c is the cluster's most important unit and it exists because a findings pass disagreed
with the code.** H-020's fix (`4a59a9a` + `a98dbd0`): the driver now reads **current state**
(`done` plus `outcome: dropped`), not an append-only derivation. Restoring the old predicate
produces five failures, and a **false negative was removed** — E4 **by withdrawal** is now
recognised, which the old reading missed. **No toolkit change was needed and none was made.**

### Cluster 3 — enforcement mechanics (META-154 … META-158)

- **The gates bullet gets an owner** (`1ebba5a` + `e5a9bb8`). `transition` now **composes the
  whole `Gates:` bullet from the contract** — one line per gate, in contract order, verdict from the
  run, evidence from the caller — so F-091's completeness symptom is *unwritable*. A contradicted
  verdict is **replaced and named on stdout**, never silently overwritten. Two things stay the
  caller's because nothing decided them: a `manual_check`'s verdict, and the whole bullet under
  `--force`. The **fourth verdict is `pending`** — *no verdict is owed* — legal in exactly one
  **derived, not named** situation: a move into a status the acting skill's own `dispatch.on_status`
  contains. Two alternatives were tested against the transition table and rejected.
  **F-080's open question is answered: yes, the gate belongs in the entry**, because an entry
  naming a gate as not-owed-here is *stronger* evidence than silence — it shows nobody was
  surprised. The comparison is **version-scoped**: an entry records an execution under the contract
  of its own time. The unit also found `implement`'s procedure **factually false** (the gates *had*
  run; what was true is that nothing was owed) and a verbatim duplicated bullet in one file.
- **The record catches up** (`8804bd7` + `d788007`), F-081/F-083/F-084. `item.md` gains
  `merge-commit`, written by a new `scripts/record-merge` and nothing else — a second journal
  entry was rejected (it would force the tool to invent `Inputs read`/`Decisions`/`Gates` to
  record an anti-fabrication fact) and an amendment convention was rejected (a second in-place
  exception to append-only, which §0 forbids by name). **F-035 is not reintroduced structurally,
  not carefully**: `vcs.merge_problems` answers four questions once, `record-merge` refuses on it,
  and `validate-workspace` re-asks it every run. **F-083 is the ORDER, not the gate** — a legal
  order already existed and the procedure never named it, so downgrading the code would have
  legalised the one order that leaves a committable-invalid workspace behind.
- **A criterion's identity** (`181e69d` + `3ae7bcd`), F-094/F-096. **F-077's mechanism did not
  generalise, and the reason is the finding's substance**: F-077's fix is a *bound*, and the
  equivalent bound for `ITEM ACn` was **already the behaviour F-094 reports as fooled**. A bound
  cannot distinguish a moved target from a standing one; only the target's content can. So the
  *place* was extended rather than a second mechanism added. F-096 adds a third checkbox state
  `- [~]`, written by `verify` alone, which follows `scope.py`'s exit-0-and-say-so shape and then
  departs from it in the harder direction: a `- [~]` **MUST** name a question on this item.
- **The F-099 sweep** (`f61ce10` + `715ef26`) — §4.

### Cluster 4 — ending contracts (META-159, `bb76d7d` + `83541cf`)

**F-085**: a gate row gains `applies_to` + `not_applicable`, reusing `pipeline.yaml`'s scoping key,
syntax and meaning. **No third verdict word is coined** — a contract-declared non-subject is
`skipped` reached *deliberately* rather than through a null placeholder; one fact, one word, and
what changed is only who noticed it. The load-bearing case:
`tests-pass-on-the-merge-result` resolves `{{commands.test}}`, which an epic **has**, so it **ran
the suite and reported PASS at an ending that merged nothing**; iteration-4b's worker recorded it
skipped, `run-gate` disagreed by running it, and they had to correct their own entry. Now
unwritable.

**F-086**: `dor-dod.md` §4a — DE1/2/3/5/6 and DE4's first half go **before** the engagement's
account of itself; DE4's restatement, DE7 and DE8 follow it. It is ADR-0011's E4 ordering,
unified by one argument: a late DE6 finding invalidates an acceptance at E1–E3, and at E4 it files
a bug, which is a child, which the `## Ending statement` must name — the same audit broken by a
second route.

**F-061**: one sentence, as specified. **No mechanism was needed and none was filed** — the
mechanism worked (the engagement reopened, built and asked again); the *label* lied, and a gate
here would have to decide whether prose is true.

Two things this unit refused: `epic-sign-off` self-passing on a work item (the same shape from the
other side) was left **deliberately unscoped**, because scoping it would flip every work-item
entry from `pass` to `skipped` across banked fixtures for something F-085 did not ask; and
**F-086 ships with no fixture, with the reason stated rather than skipped** — `definition-of-done`
is a `manual_check`, so its verdict is the caller's word by design (F-091), and nothing in a
workspace distinguishes a checklist applied before an acceptance from one applied after.

### Cluster 5 — planning, criteria and the stakeholder protocol (META-160 … META-162)

- **F-089/F-090/F-088** (`5e43182` + `4bdcbf1`). F-089 lands as DoR **R11** and is marked
  `[skill]` **with evidence, not opinion**: the narrowest regex catching its own three criteria
  flags **26 of the 53** criteria in the must-pass toy project for **2 true positives**, and that
  measurement is written into `dor-dod.md` §1 beside the rule. **F-089 is smaller than billed and
  says so**: its own evidence shows no criterion was ever reshaped around what was built, so R11
  removes a round trip, not a correctness failure. F-090 defines acceptance time as the execution
  that accepts the gap, before its closing transition; on a `done` item the gate reports NOT
  APPLICABLE in those words. Dispatch sets are **derived from `pipeline.yaml`, not restated** —
  `intake`, `next` and `retro` are reachable by neither route, so a gap owned by one is inert
  wherever it is written. **F-088's diagnosis transferred from `scope.py`'s fourth state; the
  mechanism did not** — an audit row is prose with no window to re-read. What transferred is the
  *shape of the verdict*: a pass that could not have failed is marked, never spelled like an
  ordinary pass. The new `Falsifier:` label's **reach is under-claimed on purpose and stated in
  both specs** — nothing mechanical reads `review.md`'s `## What I examined` or
  `verify-report.md`, before this change or after it.
- **F-082** (`cb344f4` + `bf1caa9`). A consumed delegation records one labelled line in ADR-0008's
  `Checked against:` shape, read by the same `record.blocks()`, and read both as a block **and
  nested inside another block**, because `plan.md`'s natural home for it is under the assumption
  bullet it belongs to. The sign-off gains a **sixth rule** naming every answer spent under
  delegation; at **E4**, where there is nobody to address, the same list goes into the
  `## Ending statement`. Enforced at `review-close`'s **existing** `cross-answer-consistency`
  gate — nothing new dispatched. The `[skill]` mark is justified **by measurement, in the spec
  beside the rule**: `[assumed]` is not a usable proxy — the toy project records **eight** assumed
  answers, six confirmed by the human, one taken under *no* licence, and exactly **one** a real
  delegation quoted in prose with no ID. Eight fires, one true positive. What the lint cannot see
  is stated ADR-0008-§5 style, the largest being *a delegation relied on and never written down at
  all*.
- **F-097 + F-104** (`b4f1909` + `6e02a61` + `aee1c88`) — §1.3. F-109 and F-110 filed; **F-110 is
  proved by execution and deliberately not fixed**, because its fix moves digests three banked
  fixtures assert.

### Cluster 6 — triage (META-163, `c662d8c`)

Every remaining entry got a decision. **130 entries read by last status, 133 after filing, 133
current: 108 fixed, 21 open, 1 rejected, and 3 entries that are tombstones or a merge pointer
rather than findings.** Of the 21 open, **none says only "open"**: 17 are deferred behind a named
gate, 2 are known-derived-and-accepted with their standing *confirmed* rather than restated, 1 is
open-unstarted-and-sequenced with its gate met, and 1 was re-gated on scope after its stated
blocker went away. 24 status blocks were appended; nothing was rewritten.

Three results from that unit matter beyond the tidying:

- **Two deferrals had already been fixed and nobody had noticed. F-053 and F-043, at `8804bd7`
  (META-156), incidentally**, while that unit was fixing F-083's *ordering*. **META-149's own
  status on F-053, written this session, says *"`transition` still has no `--outcome`"*** — true
  when written and false seven units later. The append-only ledger is what let that stand and be
  corrected below rather than quietly edited. This is evidence about the process, not only about
  the code: a fix can land as a side effect of an adjacent unit and go unrecorded for the rest of
  a session unless somebody re-reads every entry.
- **F-010's gate has been met since 2026-08-30** — its gate *is* ROADMAP §2, whose stamp that day
  named F-010 among the tracks it opened. The entry read `deferred (gated)` for eleven days, and
  META-128's triage that same day recorded it as *already gated on ROADMAP §2* without checking
  whether §2 had been stamped.
- **The trap was filed and fixed, because its subject was the unit itself.** The obvious command,
  `grep 'Status: open'`, names 24 entries of which **13 are already resolved**, **misses F-076
  entirely** (that entry's first status reads `deferred`), is blind to F-061's `###`-heading
  status, and three entries carried no status line at all — wrong in both directions and blind to
  one form. Filed as **F-112** and fixed in the same unit: `./scripts/check` step **17c** now
  requires every entry to carry a status and the header to state that the **last** one is current.
  Proved non-vacuous three ways.

### Staging (META-164, `8e61fdb`) — verified, nothing run

Both regression configs provisioned into a scratch root **outside the repository**, validated,
and torn down: both projects removed, the root `rmdir`'d and confirmed absent, `harness/runs/`
`diff`-identical to its 19-entry baseline, and the default `~/agile-skills-throwaway` checked
first and still empty. **10 rules, both configs, 10/10 each** — including that the install matches
what the repo renders, that `validate-workspace` passes on a fresh workspace, that the allow-list
equals `USAGE.md` §4 in order, that all **18** shipped scripts import **from the install** (F-072's
check run one layer further out), and that this session's new material ships: `record-halt`,
`record-merge`, `lint-documents`, `tracker/waiting/.gitkeep`, and all nine contracts at source
versions. **Idempotence was tested rather than repeated from the docstring**: a second run exits 0,
HEAD unchanged, md5 manifest byte-identical. **`--trust` was deliberately not used** (it writes
`~/.claude.json`, outside both the repo and the throwaway root), so the allow-list is *installed
and checked*, not *exercised* — stated rather than glossed.

---

## 3. Versions bumped

Read from the files, not from the log. Nine skill contracts exist; **eight moved, and only `retro`
did not.**

| Skill | From | To | The bumps, and what caused each |
|-------|------|----|-------------------------------|
| `intake` | 0.3.0 | **0.5.1** | ADR-0010 row L1, the initial `## Engagement state` section (`9adff0e`); the `[auto]` obligations become commands (`a843114`); the `**Gates:**` bullet (`1ebba5a`) |
| `refine` | 0.3.0 | **0.6.0** | the `**Gates:**` bullet; F-094/F-096; F-089/F-090; F-082 |
| `plan` | 0.4.1 | **0.6.2** | ADR-0010 (invalidation set, deliverable documents, binding ADRs); the obligations; the gates bullet; F-082 |
| `implement` | 0.3.0 | **0.6.0** | ADR-0010's widened claims window; the obligations; the gates bullet |
| `verify` | 0.2.0 | **0.5.1** | ADR-0010's per-ADR conformance verdict; the obligations; the gates bullet; F-096's `- [~]`; F-088 |
| `review-close` | 0.6.0 | **0.14.0** | ADR-0010's K8 restatement and completeness criterion; the obligations; E4's step 10; the gates bullet; the merge sha and close order; F-085/F-086/F-061; F-089/F-090/F-088; F-082's sixth sign-off rule; ADR-0012's halt predicate |
| `answer-questions` | 0.4.0 | **0.6.2** | ADR-0010 row L7; the obligations; the gates bullet; F-090 |
| `next` | 0.4.0 | **0.6.0** | the silence gate and the waiting-log write (`4d1b7ce`); ADR-0012's step order (`6e02a61`) |
| `retro` | 0.2.1 | 0.2.1 | **unchanged** |

`methodology/pipeline.yaml` **0.6.0 → 0.10.0**: ADR-0010's gate rows (`5e6434d`), the
`termination.silence` block and E4's transition rows (`877ee85`), the programs (`4d1b7ce`),
ADR-0012's halt predicate (`6e02a61`).

Spec revisions, base → head:

| Spec | Revisions |
|------|-----------|
| `spec/doc-header.md` | 4 → **9** |
| `spec/dor-dod.md` | 6 → **13** |
| `spec/ids-and-statuses.md` | 5 → **8** |
| `spec/journal-and-history.md` | 3 → **6** |
| `spec/question.md` | 8 → **12** |
| `spec/skill-contract.md` | 5 → **7** |
| `spec/work-item.md` | 1 → **4** |
| `spec/workspace-layout.md` | 4 → **6** |
| `spec/request.md`, `spec/retro.md` | unchanged (1) |

New ADRs: `ADR-0010`, `ADR-0011`, `ADR-0012`. New programs: `scripts/lint-documents`,
`scripts/record-halt`, `scripts/record-merge`, `scripts/lib/documents.py`, `scripts/lib/vcs.py`.
New fixture trees: `fixtures/document-obligations/`, `fixtures/abandoned-engagement/`.

**ADR-0010 §7 predicted this and it should be read as a thermometer rather than explained away:**
*"A version bump on almost everything, again… ROADMAP §2's 'a full consumer run with zero version
bumps' moves further away. This is the second consecutive derivation of which that is true."* It is
now the third, and this session moved eight of nine contracts.

---

## 4. The F-099 sweep — what it swept, what it found, and why "one phantom" is a claim

F-099 said the toolkit checks that a finding's citations resolve *out* of the ledger and never
that a reference *into* the ledger resolves at all, so the durable record could cite phantom
findings indefinitely. `./scripts/check` step **17b** (`f61ce10`) now reads **every git-tracked
file** and requires every three-digit `F-###`/`H-###` in it to match a `## ` heading in
`FINDINGS.md`, reporting a phantom as `path:line`.

**The scope is wider than the finding's own Direction, for the finding's own reason.** F-099
proposed `meta/**.md`. That is too narrow: a phantom in `adapters/claude-code/dist/` reaches a
user, one in `fixtures/` teaches a wrong number, one in `harness/` sits inside the instrument. **No
path is excluded.** What is not read is stated: untracked files (they are not the record), implied
numbers (`F-080..F-098` cites two numbers, not nineteen), and other citation forms — of which none
exists, checked rather than assumed. One tracked path cannot be read as text at all,
`meta/harness/evidence/iteration-1-full/project`, a gitlink; it is **named on stdout on every
run** rather than passed over, and its 129 files were checked by hand.

**The first run's full yield, over the tree at `8bd792a`: 3276 citations, 128 distinct numbers,
127 filed, across 1662 tracked files — one phantom.** That phantom is **H-001**, cited in banked
evidence and in the journal and never filed: the H-numbering begins at H-002, and the defect those
two lines describe was **fixed instead of filed** in META-081. It is F-071's mirror — there a
number was named 66 seconds too early, here a fix outran its record.

**Disposition: a tombstone, and neither citing file was edited.** One is banked evidence and the
other an append-only journal. A tombstone makes the standing citation resolve while the evidence
stays byte-identical — F-071's precedent turned into the mechanism.

**The calibration is what makes "one phantom" a claim rather than an assumption.** A sweep that
found one thing might be a sweep that finds nothing. Run as committed against a detached worktree
at **`ff8be8a^`** — the tree the instant *before* F-071's tombstone was written — the step reports
`PHANTOM F-071 -> meta/harness/evidence/iteration-3b/README.md:27`: the known instance, at the
exact line. It also reports H-001 at its two sites and `F-101` at two fixture paths that cited it
ahead of its filing, which is the one recurring false-positive shape and resolves itself the
moment the filing lands.

Non-vacuity was proved in the strong form and it establishes something about the rest of the gate:
with the resolution stubbed and H-001 still unfiled, the step reported **PASS** and the whole gate
reported *"check: all steps passed"* — so **nothing else in `./scripts/check` catches a phantom
citation**, and this step's body is what decides. With the file walk stubbed it reported **SKIP**,
named in the closing summary rather than dressed as a pass.

**A subtle property, worth recording: the report of a phantom must quote the phantom.** With the
H-001 heading removed the sweep flags the tombstone's own body alongside the citations it
corrects. A ledger design without tombstones would be unable to describe its own gaps.

**Commit order was load-bearing.** `f61ce10` is red by construction — the step's first run *is* the
finding — and `715ef26` is green. The reverse order would have filed the tombstone before the
instrument that found it, citing a sha that did not yet exist: F-024's trap.

Today the same step reports **4278 citations, 133 numbers, 133 filed, over 1675 tracked files, 0
phantoms.**

---

## 5. Findings

The ledger went **117 → 133 entries**. Sixteen were appended: **F-100 … F-112**, **H-020**,
**H-021**, and the **H-001** tombstone.

| # | What | Status |
|---|------|--------|
| H-001 | a number cited in evidence and the journal that was never filed | tombstone |
| F-100 | a document the plan hands `implement` to read is one `implement` may be forbidden to repair | open, deferred behind a named gate |
| F-101 | a deliverable document declared outside `docs/` is inside the window and outside the rule | open, deferred with F-100 |
| F-102 | nothing decides whether a K8 sentence was written where the mechanism can see it | open — known, derived and accepted (ADR-0010 obligation 10) |
| F-103 | a universal carried by a bare plural is recognised as quantified by nothing | open — known, derived and accepted (obligation 5) |
| F-104 | `next` halts on any human-addressed question, so an unanswered elicitation deadlocks every ending | fixed (ADR-0012, `6e02a61`) |
| F-105 | the termination gate refuses an epic nobody was asked about and prints no reason | open, deferred behind a named gate |
| F-106 | the termination gate passes a sign-off claiming a reply whose `## Answer` is empty | open, deferred with F-105 |
| F-107 | `engagement-state` prints `rest reached at <t>` on engagements that never reached rest | open, deferred with F-110 |
| F-108 | `examples/toy-project`'s change-log rows were typed, not stamped | open, deferred to F-068's release gate |
| F-109 | `next` still stops on a human answer that has already arrived — F-011's other half | fixed with F-097 |
| F-110 | a question **we** file resets the silence clock, which the mechanism's own docstring forbids | open, deferred — the fix moves digests three banked fixtures assert |
| F-111 | a fresh install's contents are not a function of what git tracks | open, deferred behind the next unit that opens `install.py` |
| F-112 | the ledger's own status cannot be read by the obvious command | fixed in the unit that found it |
| H-020 | the driver's recognition of a declared E4 rested on a display rule, not a contract | unsound half fixed (`4a59a9a`); residual deferred with H-015 |
| H-021 | a re-provision overwrites the project's `.gitignore`; two programs disagree about who owns it | open, deferred behind H-015's harness gate |

**Nothing was rejected.** Every entry examined at triage was founded. The two closest to a
rejection — F-102 and F-103 — are accepted gaps by construction, named at derivation time rather
than discovered afterwards, and confirming their standing without restating them is what the unit
asked for.

---

## 6. What this session's method produced

Two things recurred often enough to be reported as findings about the method rather than as
incidents.

### 6.1 The strong-form non-vacuity proof caught fresh mistakes at least as often as old ones

The discipline is: after a step passes, stub each deciding body one at a time and confirm the step
fails, distinctly, for each. It was adopted to prove that a new gate bites. What it actually did,
repeatedly, was catch a defect in the **unit's own new tests** — a rule with no case at all, a
branch the fixture never reached, an assertion that could not fail.

| Unit | The unit's own defect | How it surfaced |
|------|----------------------|-----------------|
| META-156 | the first draft of the F-083 case **passed with both `--outcome` guards disabled**, because the move it used was refused by a *gate* instead | stub 3 of 6. Rewritten to walk `WI-0003` to `in-review` with the gates forced, make only legal moves, and read each refusal for the reason it gives |
| META-157 | the step's anchored citation and its `[~]` question citation both sat on a criterion's **first** line, so removing the continuation-line join left the step green | stub 4 of 7. Both rewritten onto the wrapped line, where a real one lands |
| META-160 | two of the new rule's findings — `document.gaps.empty` and `document.gaps.row.malformed` — had **no case at all** and would have shipped unexercised | found by probing the rule's own branches. Both now fire, and the first is F-090's *literal* historical shape. The step went 13 → 15 observations |
| META-161 | the fixture exercised the **sign-off branch only**: the E4 branch, the deliberately-silent branch and the cites-an-existing-request path had **no case at all** | found by looking for a branch with no case. Stubs 9 and 11 are the proof the new cases bite |
| META-162 | an assertion `"R-001" in line` **could never fail**, because every one of those messages cites `ADR-0012`, which contains the substring `R-001` — on a branch of `dispatchable()` that had had no case at all until it wrote one | stub 9 **passed** at first. Now matches the whole clause, *"an open stakeholder request: R-001"* |

**The count is five, not seven, and the record says seven.** META-156 through META-162 is a run of
seven consecutive units — there is no META-155 — and the checkpoint reads that run as seven
catches. It is not. **META-158 records no defect in its own new case at all**: its two stubs both
bit, and its only own-case sentence is a positive confirmation (removing the `## H-001` heading
puts the step back to FAIL, so the tombstone is load-bearing). **META-159's is a different event
in the same clothes**: inverting its scoping to fire everywhere failed 5 of its observations —
that is its cases catching a hypothetical bad implementation, not a stub catching a bad case, and
nothing in its fixture was rewritten as a result. The journal's own ordinals disagree with each
other about it: META-159's entry says *"the third unit in a row"* while META-161 says *"Sixth"*
and META-162 says *"Seventh"*, and those two numbers can only be reached by counting META-158,
which the first number excludes.

So the honest form is: **in a run of seven consecutive units, five caught a defect in their own
new tests by stubbing their own deciding bodies.** That is still the result worth keeping, and it
is a different result from the one it is usually stated as: the proof's value here was **not**
mostly in demonstrating that new gates bite. Five of the seven times it ran, it found that the
unit's own evidence was weaker than the unit believed — including one assertion that was
tautologically true and one fixture covering one branch of four. A gate proved only by "it passes
now and it failed before" would have shipped all five.

### 6.2 Sub-agents corrected the account handed down to them, by reading the code

The execution model gives each unit a brief written by an orchestrator that has not read the code
for several units. That brief was wrong often enough to be a finding about the method. In every
instance below the correction is backed in the entry by an execution or a code citation, and none
of them was later shown wrong.

- **F-105 is unreachable on every input, not merely late** (META-153b). The account handed down
  described a block sitting *after* an early `return 1`. The code says the only path that reaches
  it requires `accepted` to be set, which requires a sign-off to exist, and the E4 branch that can
  pass with no sign-off returns two statements earlier. **There is no input for which that block
  prints.** Checked against `git show 77a5d96:scripts/check-epic-signoff` to establish it predates
  the E4 work rather than being introduced by it.
- **F-107 fires under every verdict** (META-153b). The condensed account had it as a false
  *"rest reached at `<t>`"* line on engagements that never reached rest. `describe()` appends it
  whenever `rest_since` is set — **under every verdict, `active` included** — because `rest_since`
  is a boundary any engagement with a moved child has. (The discovering unit, META-152, had
  already noted this; what was corrected is the summary, not the original observation.)
- **F-111 is wider than reported, and its reported consequence does not survive the code**
  (META-163). Reported: one `.pyc` from one ignored directory, with the consequence that
  `--uninstall`'s *"remove exactly what was installed"* varies by machine. Measured: **13 `.pyc`
  files from two** git-ignored `__pycache__` directories, `hooks/` and
  `dist/agile-skills/scripts/lib/`. And the consequence is false — `uninstall()` rmtree's the
  shared directory wholesale. The narrower **true** claim was filed instead: a fresh install's
  contents depend on untracked local state. In the same pass **H-021** reversed a judgement in the
  other direction: a `.gitignore` reprint that a previous unit had explicitly judged *not a defect
  because it converges* in fact **destroys** what the project added, `provision.py` writing where
  `workspace-init` appends — proved by inserting `/build/` between two provisions and finding it
  gone.
- **META-148 and META-148b filed contradictory reports and execution settled it** (META-149).
  META-148 named an edge: `implement`'s widened window can contain an `owned-by-ending` document
  it may read but not write. META-148b reported it *avoided by construction*, because the
  quantified rule reads only paragraphs new in the diff. Both cannot stand. The scoping is real
  but belongs to `lint-documents` on `answer-questions` — **a different rule on a different
  skill**; `lint-claims` rule 2, the hard gate on `implement`, has no such scoping and walks every
  prose paragraph in the window. Proved in a throwaway repo at `a843114`: the gate exits 1 with
  `claim.unsourced` on line 16 of a document the branch never opened, and the repair that fixes it
  makes the other hard gate fail. **Two hard gates, jointly unsatisfiable, no legal repair** —
  filed as F-100. This one is a sub-agent correcting *another sub-agent*, not the orchestrator.
- **A locus the brief did not name** (META-162). `record-halt` had re-derived *what a halt is* for
  itself, and moving the halt below dispatch made its condition **necessary and no longer
  sufficient**. Recorded as an honest **downgrade of an ADR-0011 claim** rather than a silent fix.
- **The orchestrator's own account of META-163's trap was hearsay too**, and it is the only
  instance where the entry names the orchestrator directly: its list of stale entries was 12; the
  measured set is 13 by the naive grep and 16 by first-versus-last status, adding F-057, F-058,
  F-061 and H-020 — and F-076, which it named as showing `open`, shows `deferred`. The journal
  calls this *"META-153b's lesson in a third place."*

**One claim in that list does not survive its own check.** The checkpoint says META-153b
*"corrected the orchestrator's summary in three places"*. The journal itemizes **two** (F-105 and
F-107; F-106 is recorded as *"exactly as described"*). There are three or more further corrections
in the same entry — H-020 turning out to be two findings with the serious half being that the
reading is *unsound* rather than merely unpromised, and F-104 having a second locus in no ADR —
but the entry does not say which three the count refers to. The number is the summary's own and
cannot be resolved from the record.

**What the two subsections say together.** The method's yield was not that a fresh reader finds
old bugs. It is that **a summary decays fast and a second reader who opens the file is worth more
than a careful one who does not** — five times against the unit's own fresh evidence, six times
against an account handed down. The mitigations already in the repository are the ones that
worked: briefs that name the exact files to read, a definition of done that requires execution
rather than agreement, and an append-only ledger that lets META-149's wrong status on F-053 stand
above META-163's correction instead of being quietly edited away.

---

## 7. What is not proven

The house standard is FINAL-REPORT-4 §4.2 and §8, which said in three places that a procedure fix
made after reading a miss is not a measurement. The equivalents here:

- **No live run has produced an E4.** Everything in cluster 2 is fixture and unit test:
  `fixtures/abandoned-engagement/` both ways, 36 harness tests added, `./scripts/check` step *the
  abandoned ending, end to end*. Not one line of it has been exercised by a stakeholder who
  actually went silent. **Iteration 5b is what would test it**, and it has not been run.
- **Nothing in cluster 1 has been exercised by a real engagement.** The document-as-deliverable
  model is derived, specified, enforced and fixtured, and it has never met a live workspace. Its
  weakening of `doc-header.md` §5 — `implement` may now write to `docs/` — is protected by three
  shape checks and a contract rule standing where one absolute stood, and no run has tested
  whether that holds.
- **The eight `[auto]` obligations each decide LESS than the `manual_check` text they replaced.**
  This is deliberate and each one says so in its own gate description. `engagement-state-is-delimited`
  checks the shape of the sections that exist and **nothing about the sentences that are not in
  one**; `adr-conformance-is-decided` checks that a verdict exists and quotes a clause, never that
  the verdict is right; `invalidation-set-is-disposed` checks that an entry was disposed, never
  that `verified-still-true` is true. Under-claiming is the correct failure mode here, and a
  reader who reads "eight manual checks became commands" as "eight judgements became mechanical"
  has read it wrong.
- **Obligation 10 is claimed by nothing, and the whole K8 mechanism rests on it.** Whether a
  sentence that *is* an engagement-state claim was written **inside** a `## Engagement state`
  section rather than left loose in the prose has no mechanical half at all. A document with no
  such section and six such sentences in its body passes every gate in this session's work.
  **F-093's own sentence was written loose.** It is filed as F-102 and marked *known, derived and
  accepted*, not fixed.
- **Two obligations are completeness and nothing decides them either** (12 and 17): whether the
  invalidation set names every document the change falsifies, and whether `binding-adrs` is
  complete. What changed is that being wrong is now attributable, not that it is caught.
- **F-086 has no fixture** and the reason is stated rather than skipped: nothing in a workspace
  distinguishes a checklist applied before an acceptance from one applied after.
- **`--trust` was not exercised in staging.** The allow-list was installed and checked against
  `USAGE.md` §4, never used.
- **Several findings were fixed incidentally and noticed only at triage.** F-053 and F-043 were
  fixed at `8804bd7` by a unit aimed at F-083's ordering, and a status written seven units earlier
  in this same session asserted the opposite. F-085's section-3/4 half was already fixed before its
  unit opened and is recorded rather than re-claimed; so is F-082's half 1, where `refine` step 3
  already said to name the deferral. That is evidence about the process: this session's own record
  of what it had done was wrong in both directions until somebody re-read the code.
- **The rules added this session are scoped, and every scope was measured before it was chosen.**
  Report the measurement, not the rule:
  * **F-084** — the execution match applies only while the item is not yet `done`. Without that
    boundary the rule reports **ten** rows in the must-pass `examples/toy-project`, six of them
    run-produced; repairing those would mean rewriting a record to make a gate green. With it, the
    rule reports nothing in the example, everything in the must-fail fixture, and the row F-084 was
    filed for. The cost is filed as F-108 rather than hidden.
  * **F-089** — R11 is `[skill]`, and the narrowest regex that catches its own three criteria
    flags **26 of the 53** criteria in that same toy project for **2 true positives**.
  * **F-094** — an anchor is not required everywhere because **84 standing `ITEM ACn` citations**
    exist across the repository, and requiring one would invalidate all 84 retroactively, which
    §4a's own grandfathering paragraph forbids. An unanchored citation is refused only at `draft`
    and `ready`, the statuses at which the list may still be rewritten.
  * **F-082** — `[assumed]` is not a usable proxy: the toy project records **eight** assumed
    answers, six confirmed by the human, one taken under no licence, and exactly **one** a real
    delegation. **Eight fires, one true positive.**
  * **F-098** — deferred, and this session made it *more expensive* rather than changing the
    answer: **97 bare `ADR-nnnn` citations over 11 numbers, 37 of them written this session**; the
    surface went 60 → 97, and the collision is already exhibited in-repo, since
    `examples/toy-project` holds a real, different ADR-0001…ADR-0010.
- **Of the twenty-one open findings, seventeen are deferred behind a named gate**, two are
  known-derived-and-accepted (F-102, F-103), one is open-unstarted-and-sequenced with its gate
  already met (F-010), and one was re-gated on scope after its stated blocker went away (H-015).
  The gates are written down; **none of them has been taken.**

---

## 8. Iteration 5, and the recommended launch order

**Explicit confirmation, as the mission requires: iteration 5 was neither run nor read.**
`run_iteration.py` was never invoked in any mode, in any unit of this session. `harness/runs/` is
`diff`-identical to the 19-entry baseline taken before staging began. The held-out probe
`harness/skills/simulated-human/probes/iteration-5-envel.md` was **not read**; its existence was
established by `os.path.isfile` and `getsize` only, and META-163's journal entry records it under
*"NOT read, deliberately"*. Iteration 5b was likewise staged and not run.

### The order, and what each step is for

**1. Run iteration 5 (`envel`, `pragmatic-manager`, 30 turns).** It carries two jobs. The planted
probe fires at the end — a partial acceptance at sign-off, targeting **E2, delivered-partial**,
which has never executed. And it is the **held-out calibration engagement** FINAL-REPORT-4 §8 asked
for: the engagement ends with `next` dispatching `retro` live, with the product source tree and the
git history present — the two inputs no banked record can supply, and the confounds §8 named. It
runs first because it is the only step whose value is destroyed by anything happening before it: a
calibration engagement stops being held out the moment somebody reads it or changes the skill in
response to something else.

**2. The owner reviews the trail independently and writes the findings down.** This is the strict
protocol in the queue entry, and the order is the whole point. A reviewer who has read the retro's
report cannot then produce an independent ground truth against it. FINAL-REPORT-4 §4.2 is the
precedent: the re-run there was not a measurement because the procedure changed after the miss was
read, and it said so where the figure appeared.

**3. Read the retro's report and score it against step 2's list.** Only now. This is the first
recall number for `retro` that would be honest to quote — 0.2.1 unchanged, ground truth written
first, live inputs present. Whatever it says, it belongs in the ROADMAP §3 track, which is open and
not finished.

**4. Run iteration 5b (`droll`, `ghosting-founder`, 20 turns).** A cheap mechanism regression, not
a calibration engagement: normal findings pass applies. It is the first live test of everything in
cluster 2 — the silence threshold, `review-close`'s abandonment declaration, the ending statement
listing delivered and orphaned children by ID, and the driver recognising a declared E4 as a
terminal stop rather than a stall. It runs last because it is the step most likely to produce a
toolkit change, and a toolkit change before step 3 would contaminate the calibration. The queue
entry says the same thing in its own words: *"Run after iteration 5's calibration review
completes."*

Success for 5b is the engagement ending **through** the mechanism with an honest record, and the
run stopping on a terminal reason whose trail explains what happened and why. A 5b that ends E4 by
the driver's stall detection rather than by the pipeline's declaration is a failure of this
session's work, however tidy the transcript looks.

---

## 9. Where the session's own record was wrong

Three units this session established that an orchestrator's summary is hearsay, and META-163
found the checkpoint's account of a trap wrong in four particulars. So this report checked
`meta/CHECKPOINT.md` against the repository rather than transcribing it.

**The load-bearing numbers held.** 45 steps, `check: all steps passed`; 108 must-fail codes; 356
self-test cases; 110 harness tests; 133 ledger entries with 108 fixed / 21 open / 1 rejected; the
117 → 133 growth; 74 → 105 → 110 on the harness side; the F-099 first-run yield of 3276 citations,
128 numbers, one phantom; the ten-rows, 26-of-53, 84-citations, eight-fires-one-true-positive and
97-bare-ADR-citations measurements; the nineteen-entry `harness/runs/` baseline; and every version
number in §3, which was read out of `skill.yaml` at both ends rather than off the log. **Four
things did not.**

1. **"Seven times running" is five.** The checkpoint's per-unit notes number the non-vacuity
   catches 1 … 7 across META-156 … META-162. Five of those units record a defect in their own new
   tests (§6.1). **META-158 records none** — both its stubs bit and its own-case sentence is a
   positive confirmation. **META-159's is a different event**: its cases caught a hypothetical bad
   implementation, and nothing in its fixture was rewritten. The journal's own ordinals contradict
   each other on exactly this point: META-159 says *"the third unit in a row"*, META-161 says
   *"Sixth"*, META-162 says *"Seventh"*, and the last two are reachable only by counting the unit
   the first one excludes. Five in a run of seven is still the result; seven is not.
2. **"Corrected the orchestrator's summary in three places" cannot be resolved to three.**
   META-153b's journal entry itemizes **two** — F-105 and F-107 — and records F-106 as *"exactly
   as described"*. Further corrections exist in the same entry (H-020 being two findings, F-104's
   second locus) but the entry never says which three the count refers to. The number is the
   summary's own.
3. **"3 tombstones that had carried no status at all"** is three entries, of which **two are
   tombstones** (H-001, F-071) and the third, **F-042, is a merge pointer** — *"not a finding of
   its own, merged into F-029"*. META-163's journal entry and the ledger header both say
   *"tombstones and pointers"*. Corrected in §2 above.
4. **The checkpoint's own account of META-163's trap was hearsay**, which META-163 recorded
   rather than the checkpoint: the orchestrator's list of stale entries was 12; the measured set
   is 13 by the naive grep and 16 by first-versus-last status, adding F-057, F-058, F-061 and
   H-020 — and F-076, which the summary named as showing `open`, shows `deferred`.

Two facts a reader would otherwise have to infer, stated instead: **there is no META-155** — the
unit numbering skips it — and **META-144 has no journal entry**, it being the planning unit, so
`meta/journal.md`'s record of this session is 24 entries running META-145 … META-164, plus this
one. The unit that closed the session's execution order was META-163, after META-164, which is why
the journal's last two entries read out of numeric order.

## 10. What the next session should do

Not another derivation. **Run the two staged iterations, in the order in §8, and read what they
say.** This session produced three ADRs, eight contract bumps, five new programs, two new fixture
trees, fifteen check steps and sixteen ledger entries, and **none of it has met a stakeholder.**
The ratio of derived-and-fixtured to run-and-observed is the worst it has been in five sessions,
and §7 is longer than §2 for that reason.

After the runs, in order of what the ledger already says is owed:

1. **The ADR-0010 amendment unit** — F-100 first (a jointly unsatisfiable pair of hard gates
   outranks an overstated scope line), then F-101.
2. **The `check-epic-signoff` unit** — F-106 first (a hard gate reaching the wrong verdict
   outranks a right verdict said badly), then F-105, whose valuable half is giving
   `TERMINATION_CASES` an expected **message**: today it asserts only a non-zero exit and cannot
   tell a right refusal from a wrong one.
3. **The `engagement.py` unit** — F-110 and F-107 together, same file, cheaper together.
4. **The citation-form sweep** — F-098, in one unit, before release; half a sweep leaves two
   conventions in the prose a consumer's workers copy from.
5. **The next harness change window** — H-015, H-020's residual and H-021, which are gated on
   scope rather than on safety now that no run is in flight.
6. **`new-item`'s write-both-or-neither shape** — F-051 with F-036, the residue of the
   *half-written record* class now that two of its four members are fixed.

**What this session does not claim.** That the document model is right: it is derived and it has
never been run. That E4 works: it executes in fixtures and in the harness's tests, and no
stakeholder has ever gone silent in front of it. That the eight new commands decide what the eight
manual checks asked for: they decide less, on purpose, and say so. That the ledger is now clean:
21 entries are open, 17 of them behind named gates nobody has taken. What this session does claim is
narrower and it is the whole of it — **the undefined region is defined, the E4 route exists and is
reachable, every rule added ships with the measurement that scoped it, and every one of them can
now be graded by a run.**

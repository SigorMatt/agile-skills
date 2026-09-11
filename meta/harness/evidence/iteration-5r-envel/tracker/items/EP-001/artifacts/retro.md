---
engagement: EP-001
ending: E1
written: 2026-09-11T19:28:20Z
items-read: 8
journal-entries-read: 87
proposals: 10
---

# Retrospective — EP-001

## What was read

- **Items:** `EP-001`, `WI-0001`, `WI-0002`, `WI-0003`, `WI-0004`, `WI-0005`, `WI-0006`,
  `BUG-0001` — all eight. Every `item.md` and every `history.md` in full; the epic's `item.md` and
  `artifacts/review.md` in full.
- **Journal entries:** 87, across 8 items, at two declared depths.
  - **In full, every bullet:** `EP-001` (8 entries), `WI-0001` (11), `WI-0002` (15),
    `BUG-0001` (9), and the first 6 of `WI-0004`'s 9 — **49 entries**.
  - **Every bullet except `Inputs read`, `Commands` and `Artifacts`** (and, on `WI-0003`,
    `WI-0005` and `WI-0006`, except `Gates` — their gate lines were instead read across all
    eight items by the survey below): `WI-0004`'s last 3, `WI-0003` (11), `WI-0005` (12),
    `WI-0006` (12) — **38 entries**. `Decisions`, `Cross-answer check`, `Questions raised`,
    `Status` and `Result` were read in full for every one of them, which is where this skill's
    four per-entry questions are answered.
  - Said this way rather than claimed as 87-in-full because the difference is real, and because a
    reading that overstates its own scope is the thing this report exists not to be.
- **Questions:** all 39 files, frontmatter for every one, and the body of 14 in full —
  `EP-001/Q-001`, `Q-003`, `Q-005`, `Q-007`, `Q-008`, `Q-009`; `BUG-0001/Q-001`, `Q-002`;
  `WI-0001/Q-002`; `WI-0002/Q-001`; `WI-0003/Q-003`; `WI-0005/Q-004`, `Q-009`; `WI-0006/Q-001`.
- **Artifacts:** `EP-001/artifacts/review.md` in full; the other items' `plan.md`,
  `impl-report.md`, `verify-report.md` and `review.md` were read **through their journals'
  accounts of them** rather than opened, except where a journal claim was checked against the
  artifact directly.
- **Documents:** `docs/product/vision.md` v10 in full including its ten change-log rows;
  `docs/architecture/overview.md` v12's `## Engagement state` and all twelve change-log rows;
  `ADR-0002` and `ADR-0012` at the sentences named below; the other eleven ADRs by their
  citations rather than end to end.
- **The citation set:** every question citation under `docs/`, enumerated with `grep` over the
  marker text and deduplicated — **28 distinct answers across 13 files**
  [src: run: grep -rlF "/Q-0" docs/ | wc -l → 13] — and each one followed to the answer it cites
  and read against the answers that came after it, which is step 5b.
- **Code:** `envel/summary.py` `left_column()` and `balance_line()`, opened to check the one
  claim written into `docs/` after the last full audit.
- **Contracts:** the installed contracts for `answer-questions` 0.6.3, `review-close` 0.14.1 and
  `retro`, and `pipeline.yaml`'s status table.
- **Scripts, read as source:** `scripts/lib/record.py` (`execution_windows`, `executed_at`),
  `scripts/validate-workspace` (`doc.changelog.no-execution`), `scripts/lint-documents`
  (`GAP_NONE_RE`, `QUANTIFIER_RE`, `rule_engagement_state_is_restated`), `scripts/lint-answers`.
  Two of the findings below are readings of these rather than of the engagement.
- **Not available:** nothing. `git log` is present, every artifact named in the tracker exists,
  and no input this skill's contract lists was missing.

## Engagement retrospective

### A hard gate was overridden on twelve transitions, always the same rule, and every `plan` execution in the engagement was one of them

`[gates forced]` appears on twelve history rows across all eight items — seven `plan`, four
`implement`, one `review-close` [src: run: grep -h "gates forced" tracker/items/*/history.md | wc -l → 12].
Every one is `workspace-valid` failing on `doc.changelog.no-execution`, and every one is the same
shape: the execution versioned a document, the change-log row says *this skill changed this at
this time for this item*, and the journal entry that opens the window containing that time is the
one the same transition is about to write [src: tracker/items/WI-0004/journal.md:271].

Seven of seven `plan` executions were forced. `WI-0001`'s `plan` entry diagnosed it and predicted
it would recur *"for the first item it plans"*; `WI-0004`'s recorded that the prediction was too
narrow — *"it recurs on every item whose plan touches a document, which is most of them"*
[src: tracker/items/WI-0004/journal.md:274]. Three positions were tried and recorded as having no
legal one: gate-then-write fails, `--resolving` does not cover the rule, and writing the entry
first raises `journal.status.unmatched` instead [src: tracker/items/WI-0001/journal.md:200].

`implement` escaped it on `WI-0002` and the reason is recorded as luck rather than technique: that
repair's change-log row happened to carry the opening entry's own timestamp, landing on the
inclusive upper bound of a window that already existed [src: tracker/items/WI-0004/journal.md:271].

### The transition rewrote every gate verdict a skill wrote in words other than pass or fail, and the contract had told the skill to use one of those words

`review-close`'s contract says to journal `engagement-state-is-restated` as
`not applicable - an item close`, **never** `passed`
[src: toolkit: review-close/SKILL.md §Journaling "not applicable - an item close"].
Every one of the ten item-close entries records it as `**pass**`
[src: run: grep -rn "engagement-state-is-restated. → " tracker/items/*/journal.md → 14 lines, all `**pass**`],
because the transition rewrites the verdict token from the gate run — which exits 0 while printing
`NOT APPLICABLE` — and leaves the rest of the sentence standing. The seam is visible in the text:
five entries read `→ **pass** (applicable — an item close`, the remains of *"not applicable"* with
its first word overwritten [src: tracker/items/WI-0004/journal.md:610].

The same rewrite reaches two other shapes. Three entries read `→ **pass** (/fail per the run this
transition made**`, from a skill that wrote `**pass/fail per the run this transition made**`
[src: tracker/items/WI-0001/journal.md:102]. And on `WI-0002`'s **rejection** —
an execution that deliberately merged nothing — `tests-pass-on-the-merge-result` is recorded
`→ **pass** (run** — there is no merge result` [src: tracker/items/WI-0002/journal.md:606]. That
entry's own prose says no merge was attempted; the verdict above it says the tests passed on the
merge result.

### The engagement's own question count was stated four times, three of them wrong, and the last one reached a sentence in `docs/`

There are 39 question files [src: run: ls tracker/items/*/questions/Q-*.md | wc -l → 39]: 35
addressed to the human and 4 to the architect. The four executions that stated a count:

- the first at-rest review, *"all 34 question files in the engagement"* — correct at that moment
  [src: tracker/items/EP-001/journal.md:116];
- the second, *"33 questions across the engagement"*, when there were 36
  [src: tracker/items/EP-001/journal.md:176];
- the third, *"34 files before this execution filed the thirty-fifth"*, when there were 38
  [src: tracker/items/EP-001/journal.md:294];
- the ending, *"all 35 questions answered"*, when there were 39
  [src: tracker/items/EP-001/history.md].

35 is not a random error. It is the number `lint-answers` prints — *"checked 35 consumed human
answer(s)"* — which counts a **subset**, the human-addressed ones
[src: run: .claude/agile-skills/scripts/lint-answers --item EP-001 → checked 35 consumed human answer(s)].
A gate's output describing one set was read as a count of another, and nothing recomputed it.

It did not stay in the tracker. `docs/product/vision.md` v10 `## Engagement state` now says
*"Thirty-five questions were filed across the engagement and each is `answered`"*
[src: docs/product/vision.md:165]. The second half is true and was checked by a grep that does not
depend on the count; the first half is false. This report may not repair it — `retro` is read-only
over the engagement it audits — and P-5 says what would.

### Two of the three send-backs in the engagement were about prose, and each had already passed two audits that printed the evidence contradicting it

Three send-backs occurred: `WI-0001` `verifying → in-progress` on AC15
[src: tracker/items/WI-0001/history.md], `WI-0002` `in-review → in-progress` and `WI-0006`
`in-review → in-progress` [src: tracker/items/WI-0002/history.md]. The second and third are
document claims, not behaviour, and neither needed a line of code.

`WI-0002`'s is the sharper one. `docs/architecture/overview.md` said *"`envelopes` knows about
`store`, `money` and `dates`"* while `envel/envelopes.py:12` is `from . import dates, money`. That
invalidation row was disposed `verified-still-true` by `implement` and again by `verify` — *"each
of which printed the two-module import line and then called the three-module claim true"*
[src: tracker/items/WI-0002/journal.md:575]. The repair names the mechanism: both executions ran
the right enumeration and asked it the falsifier they had come looking for — *does any of these
import something above it?* — rather than the sentence's own subject
[src: tracker/items/WI-0002/journal.md:674].

`WI-0001`'s behavioural send-back has the same shape one layer down: AC15 failed and *"the test
that should have caught it asserts only that stderr is non-empty"*
[src: tracker/items/WI-0001/journal.md:396] — a test that asserted a neighbouring criterion's
weaker claim and was named as AC15's evidence.

### `implement` and `verify` filed no question in the whole engagement; all 39 came from the four skills that may ask

By `from-skill`: `intake` 6, `refine` 27, `plan` 1, `review-close` 5
[src: run: grep -h "^from-skill:" tracker/items/*/questions/Q-*.md | sort | uniq -c → 6 intake, 1 plan, 27 refine, 5 review-close]. The two
skills the protocol built the question artifact **for** — the ones that may never ask a person —
used it zero times [src: toolkit: question.md §1 "The reason `implement` and `verify` may never ask directly"].

The record shows this as plans holding rather than as silence: `implement` entries repeatedly walk
the escalation test and record why it does not fire — *"Nothing was decided that was not mine to
decide"* [src: tracker/items/WI-0004/journal.md] — and `verify` classified four candidate defects
without filing, each with the test it applied [src: tracker/items/WI-0005/journal.md]. It is
recorded here because it is a property of the set that no single entry shows, and because a
protocol whose main users never use it is worth knowing about either way.

### One class of defect was repaired four times, and the first repair predicted the other three in writing

A `[src: <file>:<line>]` citation going stale when an insertion moves the line: `WI-0005/Q-009`
(three citations), `BUG-0001/Q-002` (one), `EP-001/Q-007` (four, plus a fifth found in the same
sweep), and `EP-001/Q-008` (two inside append-only `## Corrections` rows, which needed `ADR-0013`
to invent a repair) [src: WI-0005/Q-009] [src: BUG-0001/Q-002] [src: ADR-0013].

`WI-0005/Q-009` wrote the prediction down: *"Every later item whose plan cites a line its own
implementation then moves will land in the same place"*, and `BUG-0001`'s answer recorded that it
had come true on the very next item [src: tracker/items/BUG-0001/journal.md:592].

The `BUG-0001` instance is the one that shows why resolution is not support: `ADR-0012`'s citation
for *"the same filtered sum bounded by a month"* came to rest on `if "description" in entry:`,
inside the function rendering the **signed transaction figure** that the same ADR's Decision 4
exists to distinguish from a balance [src: tracker/items/BUG-0001/journal.md:526]. Every
mechanical check passed, because the line exists.

### A gate silently read only part of the table it was given

`review-close` on `WI-0004` found `accepted-gaps-are-dispatchable` reporting **5** gaps over a
seven-row table, because two rows' gap cells began with the word *"Nothing"*
[src: tracker/items/WI-0004/journal.md:619]. The cause is in the script:
`GAP_NONE_RE = ^(none|no gaps?|nothing)\b`, matched against the first cell of every row and used
to drop it as the `none` sentinel [src: toolkit: lint-documents §GAP_NONE_RE "none|no gaps?|nothing"].

It was caught only because that execution read the gate's own printed count against the table
rather than its exit code. Two real gaps had been passed over by the gate that exists to stop a
gap being passed over.

### The stakeholder was asked 39 times in one shape, and the one question that was not shaped that way carried the most consequential sentence in the engagement

Of 39 questions, 37 are `kind: decision`, closed-form, with options and a recommendation; one is
the `kind: sign-off`; one is the `kind: elicitation`
[src: run: grep -h "^kind:" tracker/items/*/questions/Q-*.md | sort | uniq -c → 1 elicitation, 1 sign-off, the other 37 carrying no kind field and so decision by default]. 34 of the 35
human-addressed ones are `blocking: true`; the elicitation is the only one that is not.

`EP-001/Q-001` — the elicitation, filed by `intake` at 01:58:15Z, four minutes into the
engagement — is where the stakeholder volunteered the rule nobody had thought to ask about:
*"money left in an envelope at the end of a month stays in that envelope; rolling over is the
whole point of doing it this way"*. It became a success measure, a paragraph in the vision and
`WI-0003` AC3 [src: tracker/items/EP-001/journal.md:63]. The engagement's single non-closed-form
question produced its single most load-bearing requirement.

### The scope moved four times, always through the protocol rather than around it, and three of the four additions were things nobody had asked for in words

`WI-0004` and `WI-0005` were filed by `answer-questions` from `EP-001/Q-005`
[src: tracker/items/WI-0004/journal.md:17]; `WI-0006` from a single phrase of the stakeholder's,
*"the ones I might query later"*, with its own derivation written into the first line of its
`## Notes` and `refine` instructed to offer closing it [src: tracker/items/WI-0006/journal.md:16];
`BUG-0001` by `review-close` against the pipeline's own delivered work, at a termination review
[src: tracker/items/BUG-0001/journal.md:19].

`WI-0006` is the one worth recording: it was offered for closure at `WI-0006/Q-001`, the
stakeholder kept it — *"You have not over-read me"* — and at the sign-off they listed it among the
seven things they actually needed [src: WI-0006/Q-001] [src: EP-001/Q-009].

### Three dependencies were discovered after the item was first refined, each because a stakeholder answer had changed what the item was

`WI-0002` recorded `depends-on: WI-0001` in round 1 [src: tracker/items/WI-0002/journal.md:48];
`WI-0003` recorded `WI-0002` in round 1 and then `WI-0004` in round 3, the second because the
stakeholder's answer at `WI-0003/Q-001` had put a **moved** column in the report after round 1 had
already fixed the dependency list [src: tracker/items/WI-0003/journal.md]; `WI-0005` found in
round 2 that it and `WI-0006` were circular over who owns the entry reference, and resolved it
from the stakeholder's own sentence rather than by choosing [src: tracker/items/WI-0005/journal.md].

Each was recorded with the cost stated: `pipeline.yaml`'s `runnable` rule freezes an item's own
**refinement** behind its dependencies' delivery, so three executions deliberately withheld a true
`depends-on` until the questions had been asked [src: tracker/items/EP-001/journal.md:69].

## Positive record

### The ordering rule in `dor-dod.md` §4a caught two real failures before the stakeholder was asked, and each became work instead of a retracted acceptance

The engagement reached rest three times. The first at-rest review failed **DE3**: the success
measure *"No envelope ever shows a negative amount"* was false of the delivered tool at two
surfaces, found by running the tool rather than by reading the verification reports
[src: tracker/items/EP-001/journal.md:148]. The second failed **DE6** on four citations that
resolved without supporting [src: tracker/items/EP-001/journal.md:183]. Neither filed a sign-off.
`BUG-0001` and `Q-007`/`Q-008` are what those failures became.

This is the rule written from F-086, working as its derivation says it should: a criterion applied
after the account is written is applied to a state the account no longer describes
[src: toolkit: dor-dod.md §4a "A DE1–DE6 failure at the ask is not an ending. It is work."]. Had
the order been the other way, the stakeholder would have accepted an engagement whose own success
measure was false, and then been asked again.

### The falsifier requirement earned its place three separate times

- `WI-0002`'s send-back is a falsifier that was **not** aimed at the sentence's subject, and the
  repair says so in those terms [src: tracker/items/WI-0002/journal.md:674].
- `WI-0004`'s shared-moment test passed against a deliberately broken implementation until it was
  rewritten; found by mutation, not by reading [src: tracker/items/WI-0004/journal.md].
- `verify` on `WI-0002`, `WI-0004` and `BUG-0001` each caught a **false green** in its own
  sensitivity harness — a mutation that patched a twin function, an append instead of a
  replacement, an unconfirmed edit — and recorded the void result rather than banking it
  [src: tracker/items/WI-0002/journal.md:729].

### The refusal that ADR-0008 exists to enforce held at the one moment it was tested

Across 28 distinct `[src: <ITEM>/Q-nnn]` citations under `docs/`, exactly one cited answer was
overtaken by a later answer of the stakeholder's: `EP-001/Q-003`, *"That is the thing I actually
want to see"* about the monthly summary, against `EP-001/Q-009`, *"I asked for it at the start and
I've changed my mind"*. The sentence carrying that citation — `ADR-0002`'s *"what went in that
month, what was spent, and what is left"* — was **not** rewritten
[src: docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md:25], and the consuming execution
recorded that the reconciliation was the stakeholder's own rather than ours
[src: tracker/items/EP-001/journal.md:367].

The two sentences in `docs/` that **were** edited under a `[src: <ITEM>/Q-nnn]` were each declared
as ordinary repairs with the test applied — an ordinal made wrong by a later answer about a
different thing, and a paraphrase of ours widened to match their own later answer — and the first
was independently re-read by `review-close` rather than accepted from `implement`
[src: tracker/items/WI-0003/journal.md:411].

### The one delegation the stakeholder granted had its scope written down before it was spent, and every spend of it reached them

`WI-0003/Q-004` — *"I'd rather everything in this tool be typed the same way"* — is the only
standing licence in the engagement. `WI-0005`'s round 1 wrote the
`**Under delegation:** WI-0003/Q-004 — argument style` line **before** anything was taken under it
[src: tracker/items/WI-0005/journal.md:558]; `WI-0006` spent it and recorded the alternative it was
weighing against and why [src: tracker/items/WI-0006/journal.md:146]; and the sign-off named the
answer, the category, both decisions taken under it, and the rejected alternative with its reason
[src: EP-001/Q-009]. F-082's failure — 38 assumptions under two licences, one of which reached the
person — did not recur here.

### `next` step 4 sitting above the halt let four items be refined while the stakeholder owed an answer on another

`WI-0003`'s round 1 ran while `WI-0002` had three open blocking human questions
[src: tracker/items/WI-0003/journal.md:18]; `WI-0004`'s ran while `WI-0003` had two
[src: tracker/items/WI-0004/journal.md:43]; `WI-0006`'s ran while `WI-0005` had five
[src: tracker/items/WI-0006/journal.md:41]. Each pass filed its own questions and suspended its
own item, and the loop then stopped once with all of them in front of the person. That is ADR-0012
§2's design producing exactly the round-trip saving it was derived for.

### The pipeline filed a bug against its own delivered work, and the stakeholder chose the remedy

`BUG-0001` was found by an epic-level DE3 walk that ran the tool against the stakeholder's eight
success measures end to end — something no child item's `verify` had scope to do
[src: tracker/items/EP-001/journal.md:129]. `plan` then refused to design it, because three of the
stakeholder's own answers met there and one had to give, and put all four remedies to them with
the cost of each [src: tracker/items/BUG-0001/journal.md:75]. They chose C and attached a
condition, which became AC6 [src: BUG-0001/Q-001].

## Proposed toolkit findings

### P-1 — PROPOSED — a change-log row cannot fall inside the execution window that legitimises it, and on a completion transition that makes the legal move unreachable

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, high
- **Component:** `scripts/validate-workspace` (`doc.changelog.no-execution`),
  `scripts/lib/record.py` (`execution_windows`), `scripts/transition` (`--resolving`),
  `spec/doc-header.md` §3
- **Symptom:** a journal entry's window is `(previous entry, this entry]`
  [src: toolkit: record.py §execution_windows "The lower bound is the entry before it on the same item"]. A skill that versions a document and
  journals through its own transition therefore writes a row whose only legal window is created by
  the entry the transition appends **after** the gates run. Twelve transitions in this engagement
  were taken with `--force` for exactly this
  [src: run: grep -h "gates forced" tracker/items/*/history.md | wc -l → 12], including every one
  of the seven `plan` executions. `--resolving` was tested against it three times and does not
  cover it [src: tracker/items/WI-0004/journal.md:271]; writing the entry first raises
  `journal.status.unmatched` instead [src: tracker/items/WI-0001/journal.md:200].
- **Counterfactual:** any engagement in which a skill's own transition both journals the execution
  and carries a document version bump reaches this — which is every `plan` execution that touches
  a document, every `implement` repair that takes longer than one clock second after its opening
  entry, every `answer-questions` propagation into `docs/`, and every ending that restates the
  engagement-state sections. Nothing about envelope budgeting is load-bearing in that sentence.
- **Recurrence:** 12 forced transitions across 8 items: `plan` ×7 (`WI-0001`, `WI-0002`,
  `WI-0003`, `WI-0004`, `WI-0005`, `WI-0006`, `BUG-0001`), `implement` ×4, `review-close` ×1 at
  the ending. Two further executions hit the rule without forcing: `answer-questions` recorded
  `workspace-valid → fail` on an ungated transition and proceeded
  [src: tracker/items/EP-001/journal.md:270], and one `implement` escaped only because its row
  landed on a window's inclusive upper bound by luck [src: tracker/items/WI-0004/journal.md:271].
- **Direction:** the shape of the fix is to make the window a property of the **execution** rather
  than of the entry that closes it. Either `resolved_by_move` downgrades `doc.changelog.no-execution`
  for the pending transition the way it already downgrades `journal.execution.missing` — the two
  are the same ordering problem one rule apart, and one of them is already solved — or the row is
  checked against the entry the transition is about to write rather than against the entries that
  exist. What should not be the fix is restamping rows backwards; `spec/journal-and-history.md` §0
  forbids it and three executions correctly refused to
  [src: tracker/items/WI-0004/journal.md:271].
- **Status:** proposed

### P-2 — PROPOSED — the transition rewrites a gate's verdict token and leaves the sentence around it, so a skill told to journal a non-verdict word cannot comply

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, high
- **Component:** `scripts/transition` / `scripts/journal-entry` (the `**Gates:**` rewriter),
  `spec/journal-and-history.md` §2.2a, and `review-close`'s contract
- **Symptom:** three distinct non-verdict openings were overwritten with `**pass**`, leaving the
  remainder of the author's sentence in place and self-contradicting. *"not applicable — an item
  close"* became `**pass** (applicable — an item close`, on all ten item closes
  [src: tracker/items/WI-0004/journal.md:610]; *"pass/fail per the run this transition made"*
  became `**pass** (/fail per the run this transition made**`
  [src: tracker/items/WI-0001/journal.md:102]; and *"not run"* became
  `**pass** (run** — there is no merge result` on a **rejection** that merged nothing
  [src: tracker/items/WI-0002/journal.md:606]. The last is the damaging one: the record now says
  the suite passed on the merge result of an item that was sent back and never merged.
  `review-close`'s own contract instructs the opposite word and the tool overrules it
  [src: toolkit: review-close/SKILL.md §Journaling "never passed"].
- **Counterfactual:** any engagement using `review-close` produces the `not applicable → pass`
  rewrite on every item close, because the instruction and the rewriter disagree by construction.
  No project subject matter is involved.
- **Recurrence:** 14 gate lines across 7 items — 10 item closes plus 4 epic-level executions for
  `engagement-state-is-restated`, 3 for the `pass/fail` form, 1 for `tests-pass-on-the-merge-result`
  [src: run: grep -rn "engagement-state-is-restated. → " tracker/items/*/journal.md → 14 lines].
- **Direction:** the verdict vocabulary the rewriter writes has to include the ones the contracts
  ask for — `not applicable` and `not run` at least — and a gate whose subject column gives it no
  subject on this item type should be written from that column rather than from the exit code of a
  script that returns 0 while printing `NOT APPLICABLE`. Failing that, the rewriter should replace
  the **whole** verdict clause rather than its first token, so that the entry cannot read as two
  authors disagreeing mid-sentence.
- **Status:** proposed

### P-3 — PROPOSED — `[src: <file>:<line>]` is a citation form for a pointer nothing holds still

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** `spec/doc-header.md` §4a *Citation forms*, `scripts/lint-claims`
- **Symptom:** four separate repairs in one engagement, across seven documents, every one a
  citation that still **resolved** and no longer **supported**: `WI-0005/Q-009` (three citations,
  plus a fourth found in the same sweep), `BUG-0001/Q-002`, `EP-001/Q-007` (four, plus a fifth),
  `EP-001/Q-008` (two inside append-only `## Corrections` rows, which required a new decision,
  `ADR-0013`, because §4b forbids editing them) [src: WI-0005/Q-009] [src: ADR-0013]. The
  `BUG-0001` instance landed on the one line in the file that contradicts the sentence it was
  supporting [src: tracker/items/BUG-0001/journal.md:526]. `validate-workspace` and `lint-claims`
  exit 0 on every one of them, because the line exists.
- **Counterfactual:** any engagement in which a plan cites a line and that plan's own
  implementation then inserts above it. `WI-0005/Q-009` wrote this as a prediction before it
  recurred — *"Every later item whose plan cites a line its own implementation then moves will
  land in the same place"* — and it then recurred three times
  [src: tracker/items/BUG-0001/journal.md:592]. Line numbers, not budgeting.
- **Recurrence:** 4 repairs, 10 citations, in one engagement of 8 items.
- **Direction:** a claim about a **statement** should cite something the statement carries with it
  — a symbol, a function name, a quoted line — rather than its ordinal position in a file, in the
  way an acceptance-criterion citation already anchors to the criterion's words rather than to its
  number. The `path:line` form stays right for a claim about a **moment** (an implementation report
  saying what was read), which is the distinction the engagement's own answers drew twice when
  deciding which stale citations to leave alone [src: WI-0005/Q-009].
- **Status:** proposed

### P-4 — PROPOSED — a gate treats a real row as its own "nothing to report" sentinel when the row begins with the word "Nothing"

- **Classification:** toolkit-defect
- **Severity:** correctness of enforcement, medium
- **Component:** `scripts/lint-documents` (`GAP_NONE_RE`, `rule_accepted_gaps_are_dispatchable`)
- **Symptom:** `GAP_NONE_RE = ^(none|no gaps?|nothing)\b` is matched against the first cell of
  every `## Accepted gaps` row and used to drop the row from the check
  [src: toolkit: lint-documents §GAP_NONE_RE "none|no gaps?|nothing"]. On `WI-0004` two real gaps whose text
  opened with *"Nothing…"* were dropped, and the gate reported **5** gaps over a seven-row table
  while exiting 0 [src: tracker/items/WI-0004/journal.md:619]. It was caught only because that
  execution compared the gate's printed count against the table rather than trusting its exit code.
- **Counterfactual:** any review whose gap prose begins with a negation — a common way to open a
  sentence describing a limitation — has that row silently unchecked. The same shape exists in the
  neighbouring `NO_MEMBERS_RE`, which is at least documented as *recognised, marked, and passed*
  [src: toolkit: documents.py §NO_MEMBERS_RE "Recognised, marked, and passed"]; this one is silent.
- **Recurrence:** once observed in this engagement, at `WI-0004`, and it was the executing skill
  rather than the gate that noticed.
- **Direction:** the sentinel should be a whole-cell match, not a prefix match — a table saying
  *there are no gaps* is one row whose cell **is** `none`, not any row that happens to start with
  a negative word. Where a row is dropped as a sentinel, say so in the output, as the
  enumeration rule already does for an empty member list.
- **Status:** proposed

### P-5 — PROPOSED — a count of the record's own artifacts is asserted rather than measured, and no gate recomputes it

- **Classification:** toolkit-defect
- **Severity:** correctness of the record, medium
- **Component:** `spec/dor-dod.md` R11 (scope), `review-close` (`record-is-reconstructible`, DE5),
  `spec/doc-header.md` §4a
- **Symptom:** the number of questions in this engagement was stated in four executions and three
  were wrong, drifting further as the engagement grew: 34 (correct), 33 (was 36), 34/35 (was 38),
  35 (was 39) [src: tracker/items/EP-001/journal.md:176]
  [src: tracker/items/EP-001/journal.md:294]. The wrong number is `lint-answers`' *"35 consumed
  human answer(s)"*, which counts a subset. It was then carried forward rather than recomputed,
  and the ending wrote it into `docs/product/vision.md` v10 `## Engagement state`
  [src: docs/product/vision.md:165], where it is now a false sentence in a closed engagement's
  product document. **`retro` may not repair it** and does not; a later execution must, through a
  new request.
- **Counterfactual:** `spec/dor-dod.md` R11 already requires that *a wanted count is measured
  first and carried as a command-outcome citation*, and it applies only to **acceptance
  criteria** [src: toolkit: dor-dod.md R11 "a criterion **names** the artefacts it constrains rather than counting them"].
  Any engagement whose review or whose `docs/` prose states a count of items, questions,
  documents or criteria reaches this gap, because nothing extends R11's rule to those places. The
  sentence names no subject matter.
- **Recurrence:** 4 statements of one count in one engagement, 3 of them wrong, 1 of them
  propagated into `docs/`. The same shape appears once more and was caught: a review recorded
  sweeping *"all 35 of them"* while reporting one [src: tracker/items/BUG-0001/journal.md:520].
- **Direction:** extend R11's measurement rule beyond acceptance criteria: a count of workspace
  artifacts asserted in `review.md` or written into `docs/` is a **quantified claim** and owes the
  same thing a quantified claim owes — the command that enumerated it, carried as a
  `[src: run: … → …]` citation. That makes it checkable by the same machinery that already checks
  an enumeration, and it makes carrying a previous review's number visible as the unmeasured claim
  it is.
- **Status:** proposed

### P-6 — PROPOSED — `review.md` has no rule for an artifact written more than once on the same item

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** `review-close` contract (`outputs`), `spec/workspace-layout.md` §1.2
- **Symptom:** `EP-001` was reviewed four times — three rests, and the third rest produced both an
  ask-and-stop review and an ending review — and each execution overwrote the file before it. The
  contract declares `review.md` an output written *always* and `spec/question.md` §2 expressly
  contemplates more than one rest, and nothing says whether a later review appends, supersedes or
  replaces [src: tracker/items/EP-001/artifacts/review.md]. Four executions chose *replace*, and
  the only thing that makes the earlier three findable is a table those executions chose to write.
  `WI-0001`, `WI-0002` and `WI-0006` have the same gap at item scope: each was reviewed twice.
- **Counterfactual:** any engagement whose epic leaves rest and returns, or whose item is rejected
  once, produces two reviews and one file. Both are ordinary, and both happened here.
- **Recurrence:** 4 overwrites on `EP-001`; 1 each on `WI-0001`, `WI-0002` and `WI-0006`.
- **Direction:** either declare the artifact append-only with a delimited section per execution,
  the way `## Corrections` already is on an ADR, or require the replacing review to carry the
  predecessor's commit and verdict — which is what these executions improvised. The important half
  is that it be a rule rather than a habit, because a reader who finds one review of an engagement
  reviewed four times has no way to know.
- **Status:** proposed

### P-7 — PROPOSED — `answer-questions`' step 6a cannot be executed after the item it names is closed, and the measurement exists

- **Classification:** toolkit-defect
- **Severity:** methodology gap, medium
- **Component:** `answer-questions` SKILL step 6a, `scripts/lint-documents`
  (`invalidation-set-is-disposed`)
- **Symptom:** step 6a requires a document changed on an item's branch to be added to that item's
  invalidation set. `WI-0005/Q-009` probed it directly: adding the row made
  `lint-documents --rule invalidation-set-is-disposed` **fail**, because the set is checked against
  `verify-report.md`'s table, which belongs to a skill that has already run and cannot run again on
  a `done` item [src: tracker/items/WI-0005/journal.md:755]. `BUG-0001/Q-002` reached the same
  conclusion independently and cited the measurement rather than repeating it
  [src: tracker/items/BUG-0001/journal.md:595].
- **Counterfactual:** any `answer-questions` execution dispatched on a gap that `review-close` made
  dispatchable at a close — which is the route `accepted-gaps-are-dispatchable` exists to create —
  lands here. The rule and the route are both the toolkit's.
- **Recurrence:** twice in this engagement, both measured rather than assumed.
- **Direction:** step 6a should be scoped to a **live branch** in its own words, and the case of a
  post-close repair given its own home — `review.md`'s answer to *did this change falsify a
  document the set does not name* is where both executions in fact recorded it, and saying so
  would turn an improvisation into the rule.
- **Status:** proposed

### P-8 — PROPOSED — the question artifact was never used by the two skills it was built for

- **Classification:** observation
- **Severity:** methodology gap, low
- **Component:** `spec/question.md` §1, `implement`, `verify`
- **Symptom:** 39 questions, none from `implement` and none from `verify`
  [src: run: grep -h "^from-skill:" tracker/items/*/questions/Q-*.md | sort | uniq -c → 6 intake, 1 plan, 27 refine, 5 review-close]. The
  protocol's stated reason for existing is that those two skills may never ask a person
  [src: toolkit: question.md §1 "The reason `implement` and `verify` may never ask directly"].
  In this engagement they instead recorded, repeatedly, the escalation test they applied and why
  it did not fire [src: tracker/items/WI-0004/journal.md]. `review-close` filed 5 and `refine`
  filed 27.
- **Direction:** nothing is proposed. One engagement cannot distinguish *plans were complete
  enough* from *the escalation bar sits too high for a skill mid-build*, and both readings are
  consistent with a record that shows the test being applied rather than skipped. It is worth
  counting across engagements: if the two skills that may never ask also never file, the artifact
  is carrying less of the protocol than its derivation assumes.
- **Status:** proposed

### P-9 — PROPOSED — refinement cost the stakeholder thirteen rounds because their answers kept opening questions nobody could have asked earlier

- **Classification:** project-circumstance
- **Severity:** methodology gap, low
- **Component:** this project's `WI-0003`, `WI-0005` and `WI-0006` refinements
- **Symptom:** `WI-0002`, `WI-0003` and `WI-0005` each took three refinement rounds and
  `WI-0003`'s round 2 had to **withdraw** one of its own round-1 assumptions, because the
  stakeholder's answer to `Q-002` made a future month print a plausible-looking report rather than
  an empty one [src: tracker/items/WI-0003/journal.md:125]. `WI-0005` found in round 2 that it and
  `WI-0006` were circular over who owns the entry reference
  [src: tracker/items/WI-0005/journal.md:589].
- **Direction:** nothing generalisable. The counterfactual cannot be written without this
  stakeholder and this domain — a person who wanted a summary, then a moved column in it, then a
  correction command, then changed their mind about the summary — and an engagement with settled
  requirements does not reach it. Recorded because it is the largest single cost in this
  engagement's calendar, and because the rounds were caused by answers rather than by imprecision:
  every one of the thirteen ended with something the record could not have derived.
- **Status:** proposed

### P-10 — PROPOSED — the stakeholder withdrew interest in a delivered feature at the sign-off, and the ending had no vocabulary for it

- **Classification:** project-circumstance
- **Severity:** methodology gap, low
- **Component:** this project's `EP-001/Q-009`, `WI-0003`
- **Symptom:** *"The monthly summary I'm parking — don't build on it, don't keep it open as work
  … I asked for it at the start and I've changed my mind"* [src: EP-001/Q-009], about
  `WI-0003`, which was delivered, verified and closed. The four endings offered are accept /
  accept-with-follow-ups / do-not-accept / withdraw [src: toolkit: question.md §2 "accept with named follow-up items"],
  and none of them is *accept, and stop investing in one delivered part*. The consuming execution
  recorded it in the epic's `## Notes` and the ending recorded it in the vision, both of which are
  places a reader finds it and neither of which is a status
  [src: tracker/items/EP-001/journal.md:362].
- **Direction:** nothing is proposed for the toolkit. The reply was an acceptance and E1 is the
  honest ending; what was needed was somewhere to record a **parked** part of a delivered scope,
  and `## Notes` served. A different engagement would reach this only if its stakeholder also
  changed their mind about something already built, which is theirs rather than the method's.
- **Status:** proposed

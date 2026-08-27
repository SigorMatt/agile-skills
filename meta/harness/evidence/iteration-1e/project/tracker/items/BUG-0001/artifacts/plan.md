# Plan — BUG-0001 Two absolute claims in docs/product/vision.md carry no citation marker

## Problem

`docs/product/vision.md` v3 says two things absolutely — that the product has **no** per-person
amounts and no weights, and that a record **cannot** be edited in place — in paragraphs that name
their source only in prose, as a backticked question reference in brackets. The methodology
requires an absolute claim about something named as code or as a path to carry a resolvable
inline source marker, and the claims linter reports both paragraphs as errors when it is run over
the whole tree [src: BUG-0001; .claude/agile-skills/spec/doc-header.md]. Nothing a user of the
tool sees is wrong; nothing in `expenses/` is wrong; the two sentences are true
[src: BUG-0001]. What is wrong is that a reader cannot follow either claim to its source in one
hop by a route a program can also take, which is the whole point of the rule
[src: .claude/agile-skills/spec/doc-header.md]. The constraints are the item's own: the claims
must still say the same thing afterwards, the document must reach version 4 with a change-log
row, and the workspace must still validate [src: BUG-0001 AC2; BUG-0001 AC3; BUG-0001 AC4].

## Approach

Add one source marker to each of the two paragraphs, at the end of the sentence that carries the
absolute, and change nothing else about what either paragraph says. Each marker names two things:
the stakeholder answer that decided it, and the file where the decision is visible in the code —
so the claim can be checked either against intent or against behaviour, which is what makes a
citation worth more than an attribution.

- The equal-split paragraph's absolute is about the shape of a stored expense, and that shape
  lives in `expenses/store.py`: `add_expense` takes an amount, a payer and a list of sharers, and
  builds `shares_minor` from an equal split, with no weight and no per-person amount anywhere in
  its signature or in the record it appends [src: expenses/store.py].
- The deletion paragraph's absolute is about the command surface, and that lives in
  `expenses/cli.py`: each noun has `add`, `list` and `delete`, and there is no `edit`
  [src: expenses/cli.py].

**The existing bracketed question references stay.** They are prose attribution, and the marker
is the checkable form; the two are redundant on purpose. Removing a bracketed reference would
also remove the only backticked name in the second paragraph, and it is that name which makes the
rule apply there at all — so the linter would fall silent because it had stopped looking, not
because the claim had been sourced. That is a criterion passing for the wrong reason, and step 5
exists to prove it did not happen.

Two things about scope belong here rather than in a step. First, `vision.md` carries other
absolutes — "no accounts, no sync", "No network access" — which the linter does not flag, because
they name nothing as code or as a path; sourcing them would be unrequested work with no criterion
behind it, and it is listed under `## Out of scope for this item`. Second, the linter reads the
**whole tree**, so an unresolvable marker written anywhere in this item's own artifacts fails AC1
just as surely as one in `vision.md`; this was confirmed while writing this plan, when a marker
naming this file before it existed turned the run red [src: BUG-0001].

## Steps

1. **`docs/product/vision.md` — source the equal-split paragraph.** At the end of the sentence
   that ends "not one complicated one", before the full stop, add an inline source marker naming
   `WI-0001/Q-001` and `expenses/store.py`, in the marker form `spec/doc-header.md` §4a defines
   and the rest of this project's documents already use. Change no other word of the paragraph,
   and leave the bracketed `WI-0001/Q-001` and `WI-0001/Q-002` references where they are.
   Afterwards: the paragraph says exactly what it said, and carries a citation that resolves.

2. **`docs/product/vision.md` — source the deletion paragraph.** At the end of the sentence that
   ends "so a correction is a delete and a re-record", before the full stop, add an inline source
   marker naming `WI-0001/Q-003` and `expenses/cli.py`. Change no other word, and leave the
   bracketed `WI-0001/Q-003` and `WI-0004` references where they are. Afterwards: the same, for
   the second claim.

3. **`docs/product/vision.md` — front matter and change log.** Set `version: 4`, `updated` to the
   UTC timestamp of the edit, `updated-by: implement`, `updated-for: BUG-0001`, and add the
   matching top row to `## Change log` saying that the two absolute claims gained resolvable
   citations and that neither claim changed. Afterwards: the document satisfies the versioning
   rule that every content change bumps the version and adds a row
   [src: .claude/agile-skills/spec/doc-header.md].

4. **Run the claims linter over the whole tree** — `python3 .claude/agile-skills/scripts/lint-claims --all`
   — and paste its output into `impl-report.md`. Afterwards: exit 0, 0 errors, 0 warnings. If it
   reports an unresolved citation in this item's own `plan.md`, `impl-report.md` or journal, that
   is the same defect in a new place and it is fixed the same way, not excluded.

5. **Prove the linter is still watching, and record it.** Take one of the two markers out, run
   the linter again, confirm the error for that line comes back, and put the marker back. Paste
   both runs into `impl-report.md`. Afterwards: there is evidence in the record that AC1 passes
   because the claims are sourced and not because the paragraphs stopped being detected — the one
   way this fix can be wrong while looking right.

6. **Run `python3 .claude/agile-skills/scripts/validate-workspace .`** and record its output.
   Afterwards: exit 0, 0 errors — every marker this item added resolves, in `vision.md` and in
   the tracker artifacts alike.

7. **Run the project's test command** — `python3 -m unittest discover -s tests -t .` — and record
   the count. Afterwards: exit 0, 123 tests, unchanged, because nothing under `expenses/` or
   `tests/` is touched by this item
   [src: run: python3 -m unittest discover -s tests -t . → exit 0, 123 tests, OK].

8. **Write `impl-report.md`** with the four command outputs above, the diff of `vision.md`, and
   both edited sentences quoted in full so a reviewer can check AC2 without opening the file.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `lint-claims --all` exits 0 with 0 errors and 0 warnings | 1, 2, 4 | the linter's own stdout and exit code, pasted into `impl-report.md`; and step 5's removal-and-restore, which shows the two lines are still being examined |
| AC2 — the document still says the same two things, in the same two paragraphs; the fix adds citations and deletes nothing | 1, 2 | `git diff main -- docs/product/vision.md` in `impl-report.md`, showing changes confined to the two sentences and the front matter and change log, with no paragraph removed; plus both sentences quoted in full after the edit |
| AC3 — front matter at `version: 4` with a matching change-log row | 3 | the front-matter block and the top change-log row, both quoted in `impl-report.md`, with `4` in each |
| AC4 — `validate-workspace .` exits 0 with 0 errors | 6 | the command's own output and exit code, pasted into `impl-report.md` |

## Assumptions

- **Each marker names the stakeholder answer and one source file, in that order.** The criteria
  fix only that a resolving citation exists [src: BUG-0001 AC1], so which sources it names is
  this plan's choice. Naming both is the useful pair: the question says why the product is that
  way, the file shows that it is. Reversing it is editing one bracketed marker in one file, with
  nothing depending on it.
- **The markers go at the end of the sentence carrying the absolute**, rather than at the end of
  the paragraph or immediately after the absolute word. The rule is per paragraph
  [src: .claude/agile-skills/spec/doc-header.md], so all three positions satisfy it; sentence-end
  reads best and matches how `docs/architecture/overview.md` places its own. Reversing it is
  moving two markers.
- **The change-log row's wording is the implementer's**, within what step 3 states it must say.
  A row that describes the change in actionable terms is the rule; the exact sentence is not
  fixed here.

## Decisions and ADRs

| decision | where it came from | record |
|----------|--------------------|--------|
| `implement` edits `docs/product/vision.md`, rather than `plan`, `answer-questions`, or nobody | decided — the methodology's writer table and the Definition of Done point in different directions for a document-only defect, and this item is the first to make the conflict unavoidable | **ADR-0009** |
| The judgement that the document is wrong must already be on the record before the edit; a skill that reaches that judgement itself still files a question | decided | ADR-0009 §1 |
| `updated-by` records the skill that made the change, not the one the table would prefer | decided | ADR-0009 §2 |
| The bracketed question references stay, and the fix is additive | decided — removing them would stop the paragraph being examined rather than source it | `## Approach`, and step 5, which checks it |
| Which sources each marker names | assumed, reversible | `## Assumptions`, first entry |
| Where in the sentence the marker goes | assumed, reversible | `## Assumptions`, second entry |
| No test is written, and none is possible for this | documented — BUG-0001's own notes settle it: the check is the linter, AC1 runs it, and the project's test command has no reach into `docs/` [src: BUG-0001] | `tracker/items/BUG-0001/item.md` `## Notes` |
| No new test framework and no lint command | documented | ADR-0004, and `tracker/project.yaml` already carries the test command |

## Scaffolding

none. This item touches one file that already exists, plus its own tracker artifacts.

## Risks

- **The whole-tree linter makes this item's own paperwork part of its acceptance criterion.**
  AC1 is `lint-claims --all`, which reads `tracker/` and `docs/` alike, so an unresolvable marker
  in `plan.md`, `impl-report.md`, `verify-report.md`, `review.md` or any journal entry fails the
  criterion for a reason that has nothing to do with `vision.md`. It happened once while this
  plan was being written. Every skill downstream should treat a marker it writes as a claim it
  must be able to resolve.
- **The fix can pass for the wrong reason.** If an edit removes the backticked name a paragraph
  makes its absolute claim about, the linter stops flagging that paragraph and AC1 goes green
  with nothing sourced. Step 5 is the mitigation and it is the step not to skip.
- **`updated-by: implement` on the product vision is a recorded departure from the writer table,
  not a routine entry.** A reviewer who reads the table alone and not ADR-0009 will read it as a
  defect. The mitigation is that ADR-0009 states the reasoning and the reversal cost, and that
  this plan cites it from a step.
- **Two paragraphs is the whole of the change, and that is easy to over-deliver on.** The
  document has other absolutes the linter does not flag, and sourcing them would be work no
  criterion asks for and nobody verifies. They are listed as out of scope below rather than left
  to the implementer's taste.

## Out of scope for this item

- **The unflagged absolutes elsewhere in `vision.md`** — "no accounts, no sync, no sharing of the
  dataset", "No network access, no hosted service, no bank connection". The rule applies to
  absolutes about something named as code or as a path, and these name nothing
  [src: .claude/agile-skills/spec/doc-header.md]. Sourcing them is a change no criterion covers.
- **Changing what either claim says.** AC2 forbids it, and the claims are true
  [src: BUG-0001 AC2].
- **`expenses/`, `tests/` and `README.md`.** Nothing in the tool's behaviour is implicated; step
  7 runs the suite to show the tree is unchanged, not because anything in it is expected to move.
- **Making the whole-tree linter a contracted gate.** Every skill's `claims-are-sourced` gate is
  scoped to what changed since the trunk, by design, and that scoping is why three skills passed
  over this defect [src: BUG-0001]. Changing it is a change to the toolkit, not to this project.
- **`docs/architecture/overview.md`.** This item alters nothing about the shape of the system, so
  it gets no version bump; a bump with no substantive change devalues every other one.

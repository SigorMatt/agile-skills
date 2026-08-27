---
id: BUG-0001
type: bug
title: Two absolute claims in docs/product/vision.md carry no citation marker
status: done
priority: low
epic: EP-001
created: "2026-08-27T00:11:41Z"
updated: "2026-08-27T02:28:28Z"
found-in: WI-0001
arose-from: WI-0001
branch: wi/BUG-0001
outcome: delivered
---

## Summary

`docs/product/vision.md` v3 makes two absolute claims about named things and sources neither of
them in the form the spec requires, so `scripts/lint-claims` fails over the document. Found while
verifying WI-0001, by running the claims linter over the whole tree rather than over that item's
diff. Nothing about the tool's behaviour is wrong: this is a defect in a delivered document, and
it is filed here rather than sent back to WI-0001 because no acceptance criterion of WI-0001 says
anything about `vision.md`.

The two sentences do point at their source — each names a question in backticks, as
`(WI-0001/Q-001)` and `(WI-0001/Q-003)`. What is missing is the citation marker that
`spec/doc-header.md` makes mandatory, which is the form a machine can check and a reader can
follow in one hop.

## Steps to reproduce

1. From the repository root, run:

       python3 .claude/agile-skills/scripts/lint-claims --all

2. Read the two errors it reports against `docs/product/vision.md`.
3. For contrast, run the scoping the contracted gates use, which passes — and which is why
   `plan`, `implement` and `review-close` did not catch this:

       python3 .claude/agile-skills/scripts/lint-claims --changed-since main

## Expected behaviour

Step 1 exits 0 with no errors. `spec/doc-header.md` section 4a requires that a paragraph making
an absolute claim — `no`, `cannot`, and the rest of that list — about something named as code or
as a path must carry at least one citation, written inline as a marker, and the citation-forms
table gives a question reference as one resolving form. Both paragraphs qualify and neither
carries the marker.

The document is not exempt on age. Section 4a says a record written before the convention existed
is not retroactively invalid, but that the next execution to edit a document is the one that must
source what it writes. `vision.md` is at `version: 3`, `updated-by: answer-questions`,
`updated-for: WI-0001`, which is after the convention existed.

## Actual behaviour

Step 1, with the two multi-line hint lines elided because they contain the literal marker syntax
and the workspace validator reads them as citations of this file:

    $ python3 .claude/agile-skills/scripts/lint-claims --all
    lint-claims: checked the whole tree under /home/msi/agile-skills-throwaway/expenses-1e
    docs/product/vision.md:31: ERROR [claim.unsourced] an absolute claim ('no') about 'WI-0001/Q-001' with no citation
        hint: ... (elided)
    docs/product/vision.md:38: ERROR [claim.unsourced] an absolute claim ('cannot') about 'WI-0001/Q-003' with no citation
        hint: ... (elided)
    lint-claims: 2 errors, 0 warnings
    $ echo $?
    1

Line 31 is *"The product deliberately has **no** per-person amounts and no weights"*; line 38 is
*"It **cannot** be edited in place"*.

Step 3, for contrast:

    $ python3 .claude/agile-skills/scripts/lint-claims --changed-since main
    lint-claims: checked no documents changed since main
    lint-claims: 0 errors, 0 warnings
    $ echo $?
    0

## Acceptance criteria

- [x] AC1 — `python3 .claude/agile-skills/scripts/lint-claims --all` exits 0 and reports 0 errors
      and 0 warnings.
- [x] AC2 — `docs/product/vision.md` still says the same two things, in the same two paragraphs:
      that the product has no per-person amounts and no weights, and that a record cannot be
      edited in place. The fix adds citations; it does not remove or soften a claim, and it does
      not delete either paragraph.
- [x] AC3 — the document's front matter is at `version: 4` with a matching `## Change log` row,
      which `spec/doc-header.md` requires of any edit to a versioned document.
- [x] AC4 — `python3 .claude/agile-skills/scripts/validate-workspace .` exits 0 with 0 errors.

## Notes

- **RB5, the regression test.** There is no test to write, and that is deliberate: the check *is*
  `scripts/lint-claims`, and AC1 runs it. The project's own test command covers the `expenses`
  package and has no reach into `docs/`; a test that shelled out to a toolkit script would be
  testing the toolkit rather than this project.
- **Why this is not a send-back to WI-0001.** No acceptance criterion of WI-0001 mentions
  `vision.md`, and the `claims-are-sourced` gate WI-0001 must pass is scoped to what changed
  since the trunk, which passes. `found-in: WI-0001` records that the text arrived when
  `answer-questions` propagated that item's answers into the vision.
- **Why `implement` did not file this itself.** It found the same two errors and recorded them in
  WI-0001's implementation report under `## What I did not do`. `pipeline.yaml` has no creation
  row whose actor is `implement`, so it had no authority to file a bug and handed it to `verify`,
  which does.
- **Priority is low deliberately.** No contracted gate fails, no behaviour a user sees is wrong,
  and the fix is two citation markers and a version bump.
- **A note for whoever fixes this.** Writing the marker syntax literally inside a tracker artifact
  makes the validator try to resolve it, which is how the first attempt at filing this bug turned
  the workspace red. Put the citations in `vision.md` itself, where they resolve, and describe
  rather than quote them anywhere else.

### Added at close by `review-close`

These are the gaps this review accepted rather than sent back. They are here, and not only in
`artifacts/review.md`, because a report stops being read once an item is `done`.

- **`lint-clean` never ran on any execution of this item.** `tracker/project.yaml` records
  `lint: null` and ADR-0004 is the decision behind it, so every skill recorded the gate as skipped
  rather than passed. For an item that adds no code, that leaves nothing meaningful unchecked.
- **The other absolute claims in `vision.md` are still unsourced.** "no accounts, no sync, no
  sharing of the dataset" and "No network access, no hosted service, no bank connection" name
  nothing as code or as a path, so the rule does not reach them and the linter does not flag them.
  Accepted rather than deferred: there is no defect to fix, and sourcing them would be a change no
  criterion asks for.
- **The gate scoping that let this defect through is unchanged, and is out of this project's
  reach.** Every contracted `claims-are-sourced` gate reads only what changed since the trunk,
  which is why three skills ran clean over `vision.md` while the whole-tree form failed. What
  survives this item is the practice: `lint-claims --all` finds document defects the contracted
  gate cannot, and it is worth running by hand.
- **`check-verify-freshness` counts `docs/` as record, not as deliverable.** Its message on this
  item was that only the record had changed, `docs/` included. For a document-only item like this
  one, an edit to the delivered file made after verification would be classified the same way and
  D10 would pass over it. It did not happen here — the range was checked directly and no file
  under `docs/` moved after the verified commit — and no bug item is filed, because the script
  belongs to the toolkit and nothing in this project can change it.

---
id: BUG-0005
type: bug
title: README does not say what tidy exits with when every move fails
status: done
priority: low
epic: EP-001
created: "2026-08-27T20:05:34Z"
updated: "2026-08-28T13:47:59Z"
found-in: WI-0001
arose-from: BUG-0002
branch: wi/BUG-0005
outcome: delivered
---

## Summary

`README.md`'s exit-status paragraph enumerates three cases — 0 on success, 2 for a folder that
cannot be used, and "1 when some file could not be moved while others were" — and a real run falls
outside all three. When *every* move fails and nothing is left behind that succeeded, `tidy` exits
**1**, which the README describes only as the partial-failure code. A reader scripting the tool
learns what 0 and 2 mean and is told about 1 only for a case that did not happen, so they cannot
tell from the document what an all-fail run exits with.

The behaviour is right; the sentence is incomplete. Nothing in `tidy/cli.py` distinguishes a
partial failure from a total one — `return 1 if any(outcome.kind == "failed" ...) else 0` — so 1
means "at least one file could not be moved", which is what the README should say.

The clause dates from WI-0001 (`49be3d7`) and survived BUG-0001's rewrite of the same paragraph
(`068cecd`), which restated the exit-2 case as one rule covering three situations and left the
exit-1 clause as it was. `found-in: WI-0001` names the item that delivered both the wording and
the behaviour it describes.

## Steps to reproduce

Run from the repository root, on `main` (or on `wi/BUG-0002`; the exit code in this case is the
same before and after that item, which is why this is not a BUG-0002 defect).

1. Build a folder whose destinations cannot be created, so that no move can land:

   ```
   mkdir -p .harness/rc/allfail/recent
   echo a > .harness/rc/allfail/photo.jpg
   echo b > .harness/rc/allfail/doc.pdf
   chmod 0500 .harness/rc/allfail/recent
   ```

2. Run `python3 -m tidy .harness/rc/allfail --apply; echo "EXIT: $?"`
3. Confirm nothing moved: `find .harness/rc/allfail -type f`
4. Clean up: `chmod 0700 .harness/rc/allfail/recent && rm -rf .harness/rc`
5. Read `README.md`'s exit-status paragraph (the one beginning "Exit status is 0 on success") and
   look for the case you just ran.

Step 2 skips under root or on a filesystem that does not enforce mode `0o500`, where the writes
succeed and both files move.

## Expected behaviour

`README.md` states what exit status a run gets when no file moved at all. The natural fix is to
drop the "while others were" condition — 1 means at least one file could not be moved — but the
wording is for `plan` to settle. The observable is that a reader of the exit-status paragraph can
predict the exit code of the run in `## Steps to reproduce`.

## Actual behaviour

```
$ python3 -m tidy .harness/rc/allfail --apply; echo "EXIT: $?"
tidy: moving files. Nothing will be overwritten.
tidy: could not create the folder for recent/documents/doc.pdf: [Errno 13] Permission denied: '.harness/rc/allfail/recent/documents'; doc.pdf was left where it is
tidy: could not create the folder for recent/images/photo.jpg: [Errno 13] Permission denied: '.harness/rc/allfail/recent/images'; photo.jpg was left where it is
move   doc.pdf -> recent/documents/doc.pdf
move   photo.jpg -> recent/images/photo.jpg
EXIT: 1

$ find .harness/rc/allfail -type f
.harness/rc/allfail/doc.pdf
.harness/rc/allfail/photo.jpg
```

Neither file moved, and the run exited 1. `README.md` says:

> Exit status is 0 on success — including when there was nothing to do — 2 when the folder you
> named cannot be used, which covers all of: it does not exist, it is not a folder, or it cannot
> be read — and 1 when some file could not be moved while others were.

## Acceptance criteria

- [x] AC1 — `README.md`'s exit-status paragraph describes the exit code of a run in which no file
      moved. Checkable by running `## Steps to reproduce` and then reading the paragraph: the run
      exits 1 and the paragraph must account for that run without the reader having to infer it.
- [x] AC2 — The paragraph still describes the partial case and the two other codes correctly:
      0 for a successful run including nothing-to-do, and 2 for a folder that cannot be used,
      covering all three of does-not-exist, not-a-folder and cannot-be-read. Checkable against
      BUG-0001 AC2, which is what put the exit-2 sentence in its present form.
- [x] AC3 — A regression test in `tests/` asserts that a run in which every move fails exits 1,
      so the behaviour the README will then describe is pinned. It must skip, rather than fail,
      under root or on a filesystem that does not enforce mode `0o500`, as
      `tests.test_cli.FallbackExitStatusTests.test_a_genuine_failure_alongside_a_fallback_still_exits_1`
      already does.

## Notes

Filed by `review-close` while reviewing BUG-0002. BUG-0002's own four criteria all pass — see
`tracker/items/BUG-0002/artifacts/verify-report.md` — and this defect is in prose that BUG-0002
did not change and no BUG-0002 criterion covers.

`verify` looked at the same sentence during BUG-0002 and deliberately did not file it, recording
the reasoning in `verify-report.md` `## Defects found`: that "some file could not be moved" is
true in an all-fail run, so the sentence is loose rather than false, and inviting `review-close`
to take a different view with the evidence in front of it. This item is that different view. The
disagreement is narrow and worth stating: the paragraph is an enumeration of exit codes, a reader
uses it to predict one, and there is a run whose code it does not let them predict. Whether that
is worth an edit is now the stakeholder's call at sign-off rather than a judgement buried in a
closed item's verification report.

A regression test (AC3) is required because the behaviour is testable, so the exemption in
`spec/work-item.md` §3 does not apply. Only `README.md` is expected to change; if `plan` concludes
the code should change instead — for instance a distinct exit code for a total failure — that is a
new exit status, which `README.md` and ADR-0006 both bound to 0, 1 and 2, and would need an ADR.

### Gaps accepted at review, 2026-08-28

Recorded on close so they survive the reports. Full reasoning in `artifacts/review.md`
`## Accepted gaps` and `## Accepted gaps — round 2`.

- **The delivered clause's internal em dash.** The exit-status sentence separates its three
  top-level clauses with em dashes and the new third clause contains a fourth. It resolves —
  "whether" cannot open an exit-code clause — and it is the wording `plan` fixed, delivered
  verbatim as the plan required. AC1 asks only that a reader can predict the code.
- **`AllMovesFailExitStatusTests`'s docstring quotes the `README.md` clause verbatim**, so a later
  rewording leaves it stale. The drift-proofing this project used for the help text (deriving the
  expectation from the table the tool routes by) does not transfer: the test asserts behaviour,
  and deriving a docstring from `README.md` would be worse than the problem.
- **`README.md`'s exit-0 clause and a failing run's stderr share the phrase "left where they
  are".** Examined twice — by `verify` and by both review rounds — and not a defect: the 0 clause
  is governed by "on success". Not fixable here either, because AC2 and `plan.md` step 2 both
  protect that clause for BUG-0001 AC2 and WI-0003 AC12. Provenance if anyone files it: the phrase
  entered at `1156654` (BUG-0004), the stderr message at `49be3d7` (WI-0001).
- **Everything under `## Not verified, and why` in `verify-report.md`** — behaviour under root or
  on a filesystem that does not enforce mode `0o500`, which the criteria themselves make
  conditional, and the declaration that implementation and verification ran in the same session.
- **`ADR-0006:26-29` paraphrases `README.md`'s exit-status contract in words `README.md` no longer
  uses** (review round 2, F4). Judged historical `## Context` rather than a live claim, because the
  same sentence ends with the BUG-0001 defect that ADR-0006's own decision removed — a reader
  cannot take the paragraph as a description of today. What would change that verdict is a project
  convention that ADR contexts be written in the past tense, which is a `ways-of-working` question
  and not this item's. Provenance: the exit-2 half went stale at `068cecd` (BUG-0001), the exit-1
  half at `05be040` (this item).

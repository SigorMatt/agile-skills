---
id: BUG-0003
type: bug
title: "--help still says files are sorted by type alone, after age routing landed"
status: done
priority: medium
epic: EP-001
created: "2026-08-27T19:10:49Z"
updated: "2026-08-27T20:41:15Z"
found-in: WI-0002
branch: wi/BUG-0003
outcome: delivered
---

## Summary

`python3 -m tidy --help` describes the tool as sorting "into subfolders chosen by file type", and
points the reader at "The extension-to-folder table" as though there were one table. Both
sentences were true before WI-0002 and are false or incomplete after it: a file's age now chooses
the top-level folder, and there are two rule tables. A user who reads only `--help` is not told
that age chooses a folder at all, and will not expect `recent/` and `old/` at the top level of the
folder they just tidied.

Found on branch `wi/WI-0002` at commit `93a958599cdfe10c81dfba337d62811e23db564c` while verifying
WI-0002. The strings are in `tidy/cli.py:22` (`description`) and `tidy/cli.py:24` (`epilog`).
`tidy/cli.py` is byte-for-byte unchanged by WI-0002, which is exactly how the text went stale
without anyone editing it.

No WI-0002 acceptance criterion covers the help text — AC13 fixes what `README.md` must say and
nothing else — so this is not a failure of WI-0002 and WI-0002 was not sent back for it.
WI-0001 AC1, the only criterion about `--help`, requires it to name the folder argument, the apply
flag, and the preview default; it still does all three, so this is not a failure of WI-0001
either. `found-in: WI-0002` names the item whose delivered behaviour the text contradicts: the
sentence is WI-0001's, but what it is wrong about is WI-0002's routing, and it is wrong only from
this branch onward.

## Steps to reproduce

1. Check out `wi/WI-0002` (or `main` once WI-0002 is merged) and work from the repository root.
2. Run `python3 -m tidy --help`.
3. Read the description line above `positional arguments:` and the epilog below `options:`.
4. For contrast, run a real preview and see a band in every destination:

   ```
   mkdir -p /tmp/bug3 && echo x > /tmp/bug3/holiday.jpg
   python3 -m tidy /tmp/bug3
   ```

   prints `move   holiday.jpg -> recent/images/holiday.jpg` — a top-level folder `--help` never
   mentions.

## Expected behaviour

`--help` describes how a destination is chosen, consistently with what the tool does and with
`README.md`. `README.md` §"Where each file goes" is the standard the text should agree with:
every file that moves ends up at `<band>/<type>/<name>`, age chooses the band, and there are two
rule tables rather than one.

What the wording should be is for `plan` to settle; the observable is that a reader of `--help`
learns that age takes part in choosing the destination, and is not told there is exactly one
table when there are two.

## Actual behaviour

```
$ python3 -m tidy --help
usage: tidy [-h] [--apply] folder

Sort the files sitting directly in a folder into subfolders chosen by file
type.

positional arguments:
  folder      the folder to tidy; only the files directly inside it are
              considered

options:
  -h, --help  show this help message and exit
  --apply     actually move the files; without this flag tidy only previews
              and moves nothing

Without --apply, tidy previews only: it prints every move it would make and
changes nothing on disk. The extension-to-folder table is in README.md.
Subfolders are never entered or moved, names beginning with '.' are left
alone, and no file is ever overwritten.
```

Meanwhile the tool's own output on the same branch:

```
$ python3 -m tidy .verify-scratch/ac1
move   holiday.jpg -> recent/images/holiday.jpg
```

## Acceptance criteria

- [x] AC1 — `python3 -m tidy --help` exits 0 and its output states that a file's **age** takes
      part in choosing where it goes, naming both band folders `recent` and `old`. Checkable by
      grepping the help output for `recent`, `old`, and a word for age; today it contains none of
      them.
- [x] AC2 — The help output no longer implies there is a single rule table. It either names both
      tables or refers to `README.md` without the word "extension-to-folder" qualifying it.
      Checkable by reading it against `README.md` §"Where each file goes", which describes two.
- [x] AC3 — Everything WI-0001 AC1 requires of `--help` is still true: it names the target folder
      as the first positional argument, names the flag that selects APPLY, and says that without
      that flag the tool only previews. Checkable by the same grep WI-0001's verification used.
- [x] AC4 — A regression test in `tests/` asserts AC1 and AC3 against the actual `--help` output,
      and fails when the description is reverted to the current wording. It must not restate the
      help text as a literal, or it will fail on every future rewording rather than on the thing
      it guards.

## Notes

Filed by `verify` while verifying WI-0002. WI-0002 itself passes all thirteen of its own criteria
— see `tracker/items/WI-0002/artifacts/verify-report.md`.

`implement` declared this gap in `tracker/items/WI-0002/artifacts/impl-report.md` under
`## What I did not do`, item 1, and recommended either a bug item or a one-line amendment during
review. It was declared rather than fixed because the plan's `## Out of scope` says any change to
`cli.py` is a signal worth a question. That declaration is not this item's evidence: the help
output above was run in this execution and compared against the tool's behaviour and against
WI-0001 AC1.

It is two strings and no logic, but it is a real user-visible inaccuracy, and it is the kind of
staleness that only gets found by someone reading the help text — which is to say, by a user.

### Gaps accepted at review, 2026-08-27

Recorded here rather than only in `artifacts/review.md`, because a gap that lives in a report
stops being read the moment an item closes. The reasoning for each is in `review.md`
`## Findings`.

1. **Reverting the `description` alone does not fail the suite.** Under the strict reading of AC4
   — `description` meaning the argparse argument named by line number in `## Summary` — the
   delivered test does not satisfy the criterion; under the loose reading (the tool's description
   of itself) it does, and three artifacts support the loose one. Measured: reverting
   `description` to "...chosen by file type." while keeping the new epilog leaves
   `python3 -m unittest discover -s tests -t . -q` at `Ran 69 tests ... OK`. The residual hole is
   that a future edit could revert the description, leave the epilog correct, and produce a
   self-contradictory help text no test objects to. Widening the guard is a decision about the
   criterion rather than a defect in the code; whoever takes it will find the experiment in
   `artifacts/verify-report.md` `## Defects found` rather than having to repeat it.
2. **`DEFAULT_RULES` is unguarded in the direction `DEFAULT_BANDS` now is.** The help text names
   no extensions — it points at `README.md` — so there is nothing for a test to compare. ADR-0008
   `## Consequences` records this and says what should happen if a later item makes the help list
   extensions.
3. **The age assertion's failure message names nothing.** `assertTrue(any(re.search(...)))` fails
   with `False is not true`; the band loop's `assertRegex` prints its pattern. Diagnostic quality,
   not correctness — no criterion asked for it, and the four-word vocabulary is explained by the
   comment above it.
4. **`--help` was exercised under this environment's default locale only.** Nothing in the change
   is locale-sensitive — the strings are ASCII and `argparse` does not translate them — but that
   is an inference, not an observation.
5. **Whether the wording is *good*, as opposed to true and complete, was not judged.** `plan` was
   asked to settle the wording and did; no criterion constrains readability.
6. **The rest of `README.md` was not audited.** AC2 needs only §"Where each file goes", which was
   read and does document two tables. BUG-0005 is open against a different part of the same file.

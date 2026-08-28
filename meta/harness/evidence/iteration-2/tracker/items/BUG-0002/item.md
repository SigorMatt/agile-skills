---
id: BUG-0002
type: bug
title: A fully successful apply exits 1 on a filesystem that refuses hard links
status: done
priority: medium
epic: EP-001
created: "2026-08-27T16:31:21Z"
updated: "2026-08-27T20:16:13Z"
found-in: WI-0001
branch: wi/BUG-0002
outcome: delivered
---

## Summary

On a filesystem that refuses hard links, `tidy <folder> --apply` moves every file correctly and
then exits **1**, reporting the successful moves on stderr as though they had failed. ADR-0003
designs the `shutil.move` fallback as a *success* path — "it still satisfies the criterion
[src: WI-0001 AC9]" — but `tidy/apply.py` returns its note in the same list it uses for genuine
failures, and `tidy/cli.py` ends with `return 1 if failures else 0`. Found on branch
`wi/WI-0001` at commit `6b1873161b148392d8ee5cb6ff5824a4ab404289` while verifying WI-0001.

No WI-0001 acceptance criterion constrains the exit status of a successful APPLY — AC3's "exit
status is 0" is about PREVIEW, and AC15's is about the nothing-to-do case — so this is not a
failure of WI-0001 and is filed here rather than sent back. WI-0001's `impl-report.md` predicted
it under `## What I did not do`; this item is that prediction, confirmed by running it.

It is unreachable on ordinary Linux and macOS filesystems, which is why no test in WI-0001's
suite covers it. It bites on the filesystems people actually point a tidying tool at: some SMB
and NFS mounts, some FUSE filesystems, exFAT and FAT32 removable media. Anything scripting the
tool — `tidy ~/Downloads --apply && notify-send done` — silently treats a completely successful
run as a failure there.

## Steps to reproduce

The condition is a filesystem that refuses `os.link`. Reproduce it directly by making `os.link`
raise the error such a filesystem raises, which exercises exactly the branch in question:

1. Check out `wi/WI-0001` (or `main` once WI-0001 is merged) and work from the repository root.
2. Save this as `nolink.py`:

   ```python
   import os, sys, io, contextlib
   sys.path.insert(0, os.getcwd())
   os.link = lambda a, b: (_ for _ in ()).throw(OSError(18, "Invalid cross-device link"))
   from tidy.cli import main
   out, err = io.StringIO(), io.StringIO()
   with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
       rc = main([sys.argv[1], "--apply"])
   print("EXIT:", rc)
   print("STDOUT:", out.getvalue().rstrip())
   print("STDERR:", err.getvalue().rstrip())
   ```

3. Build a folder with two files that both move cleanly:

   ```
   mkdir -p /tmp/nolink && echo a > /tmp/nolink/photo.jpg && echo b > /tmp/nolink/doc.pdf
   ```

4. Run `python3 nolink.py /tmp/nolink`
5. Confirm both files did move: `find /tmp/nolink -type f`

Equivalently, and without the injection: mount or plug in an exFAT/FAT32 volume, put the same two
files at its top level, and run `python3 -m tidy <that folder> --apply; echo $?`.

## Expected behaviour

Exit **0**. Every file moved, nothing was overwritten, and nothing failed.

ADR-0003 `## Decision` assigns a non-zero exit to `FileExistsError` only — "the run reports it on
stderr and continues with the remaining actions, and the process exits non-zero" — and describes
the other-`OSError` fallback separately, with no such clause, as the weaker guarantee that "still
satisfies the criterion". The note on stderr is right and should stay; classifying it as a failure
is what is wrong.

`README.md` states the same contract from the user's side: "Exit status is 0 on success ... and 1
when some file could not be moved while others were." In this run every file *was* moved, so
exit 1 contradicts `README.md` as well as ADR-0003.

## Actual behaviour

```
$ python3 nolink.py /tmp/nolink
EXIT: 1
STDOUT: move   doc.pdf -> documents/doc.pdf
move   photo.jpg -> images/photo.jpg
STDERR: tidy: moving files. Nothing will be overwritten.
tidy: doc.pdf was moved to documents/doc.pdf without a hard link, because this filesystem refused one ([Errno 18] Invalid cross-device link)
tidy: photo.jpg was moved to images/photo.jpg without a hard link, because this filesystem refused one ([Errno 18] Invalid cross-device link)
```

Both files had in fact moved:

```
$ find /tmp/nolink -type f
/tmp/nolink/documents/doc.pdf
/tmp/nolink/images/photo.jpg
```

So the run did everything it printed, reported it as a failure, and exited 1.

## Acceptance criteria

- [x] AC1 — An APPLY run in which every move landed exits **0**, whether the moves used `os.link`
      or ADR-0003's fallback. Checkable by the steps above: `EXIT: 0`, with both files at their
      destinations.
- [x] AC2 — The fallback is still reported. The stderr line naming the file, its destination and
      the reason a hard link was refused is unchanged; only the exit status changes.
- [x] AC3 — A run in which a move genuinely did not land still exits non-zero, so this fix does
      not silence real failures. Checkable with the `FileExistsError` path, which `os.link` still
      raises when the destination appeared mid-run.
- [x] AC4 — A regression test in `tests/` patches `os.link` to raise a non-`FileExistsError`
      `OSError`, asserts AC1, AC2 and AC3, and fails when the fix is reverted. This closes the gap
      WI-0001's `plan.md` `## Risks` records as "the one place where a criterion (AC9) rests on
      code that automated tests do not reach".

## Notes

Filed by `verify` while verifying WI-0001; `found-in: WI-0001` names the item that delivered
`apply_plan`. WI-0001 itself passes every one of its own criteria — see
`tracker/items/WI-0001/artifacts/verify-report.md`.

The likely fix is to separate "this action did not complete" from "this action completed by a
different route", which is a two-list return from `apply_plan` rather than one. That is a design
call for `plan`, not a decision this bug report takes.

A second unspecified failure mode was found in the same execution and is filed separately as
BUG-0001; they are unrelated faults in different modules and each needs its own reproduction.

### Gaps accepted at review

Recorded by `review-close` on 2026-08-27, from `verify-report.md` `## Not verified, and why` and
`impl-report.md` `## What I did not do`, so that they survive this item closing. The reasoning for
each is in `artifacts/review.md` `## Accepted gaps`.

- No test runs on a filesystem that genuinely refuses hard links; all four patch `os.link` to raise
  errno 18. What is proven is the branch's behaviour given that error, not the platform's.
- AC3's end-to-end leg (`test_a_genuine_failure_alongside_a_fallback_still_exits_1`) skips under
  root or on a filesystem that ignores mode `0o500`. It did not skip in implementation, in
  verification or in review. Three unit-level `kind == "failed"` assertions carry AC3 independently.
- The `os.unlink` duplicate path — the link succeeded and the original could not be removed — is
  untested. It is tagged `"failed"` and exits non-zero; it is the one `Outcome("failed", ...)` in
  `apply.py` that no test constructs, and it was equally untested before this item.
- A genuine mid-run `FileExistsError` was not driven through `main()`: `build_plan` reserves
  colliding names, so it cannot be produced through the CLI. It was exercised through `apply_plan`
  with a real kernel error, and the CLI's `"failed"` → exit 1 mapping separately.
- `README.md` was left untouched, as `plan.md` `## Assumptions` records. What is incomplete in its
  exit-status paragraph is tracked as BUG-0005, not here.

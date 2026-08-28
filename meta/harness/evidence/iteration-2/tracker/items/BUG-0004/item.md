---
id: BUG-0004
type: bug
title: One dangling symlink stops the whole folder being tidied
status: done
priority: medium
epic: EP-001
created: "2026-08-27T19:31:55Z"
updated: "2026-08-27T21:18:29Z"
found-in: WI-0002
branch: wi/BUG-0004
outcome: delivered
---

## Summary

A single dangling symlink anywhere in the target folder makes `tidy` refuse to tidy the folder at
all — including the ordinary files it could have moved. `build_plan` calls `entry.stat()` on every
entry to work out its age band, and `stat` on a symlink whose target does not exist raises
`FileNotFoundError`, which aborts the whole scan.

Introduced by WI-0002: `entry.stat()` arrived in `tidy/planner.py` with commit `2a4b928`
("planner: route each file into a band above its type folder"). Confirmed by running the same
fixture against the commit before it, where the same folder previewed cleanly and exited 0.

The symptom has changed twice and is wrong in both of its current forms:

- On `main` (`e96c5e2`) it is an uncaught `FileNotFoundError` traceback and exit **1**.
- On `wi/BUG-0001` (`d80c35a`, at `verifying`) BUG-0001's new handler catches it, so the user
  instead gets `tidy: <folder> cannot be read: No such file or directory` and exit **2** — a calm,
  confident sentence that is false. The folder was read perfectly well; one entry inside it could
  not be stat'd, and the message names neither that entry nor the real problem.

BUG-0001 did not cause this and does not claim to fix it: its plan puts "a file that disappears or
becomes unreadable partway through a scan" out of scope explicitly, ADR-0006 `## Consequences`
names the broad `except OSError` as the cost that produces the misleading wording, and
BUG-0001's `impl-report.md` `## What I did not do` declares it. This item is that declared gap,
filed against the item that introduced the abort.

## Steps to reproduce

1. Work from the repository root, on `main` or on `wi/BUG-0001`.
2. Build a perfectly ordinary folder with one broken symlink in it:

   ```
   mkdir -p /tmp/dangling && echo x > /tmp/dangling/photo.jpg
   ln -s /tmp/dangling/gone.pdf /tmp/dangling/broken.pdf
   ```

3. Preview it: `python3 -m tidy /tmp/dangling`
4. Apply it too: `python3 -m tidy /tmp/dangling --apply`
5. Clean up: `rm -rf /tmp/dangling`

Steps 3 and 4 behave identically. `photo.jpg` is a normal file with a recognised extension and is
never mentioned in either run.

## Expected behaviour

The entry that cannot be stat'd should not cost the user the rest of the folder. `photo.jpg` is
readable, has a rule, and has an age; nothing about `broken.pdf` prevents it being tidied.

The shape the tool already uses for a file it cannot place is a `leave` line naming the file and
the reason — `leave  notes.xyz   [no rule for '.xyz']` [src: README.md] — and this is the same
class of thing: one entry that cannot be handled, reported per entry, while the rest of the run
proceeds. Whether that is the right answer here, and what exit status such a run should carry, is
for `plan`; AC1 below fixes only the observable that matters, which is that one bad entry must not
silently cost the user every good one.

Whatever is chosen, the message must not claim the folder cannot be read when it can. That claim
is currently the only thing the user is told.

## Actual behaviour

On `wi/BUG-0001` at `d80c35a`:

```
$ mkdir -p /tmp/dangling && echo x > /tmp/dangling/photo.jpg
$ ln -s /tmp/dangling/gone.pdf /tmp/dangling/broken.pdf
$ python3 -m tidy /tmp/dangling
tidy: /tmp/dangling cannot be read: No such file or directory
$ echo $?
2
```

stdout is empty. `--apply` prints the same line and exits 2.

On `main` at `e96c5e2`, the same fixture:

```
  File ".../tidy/planner.py", line 55, in build_plan
    band = band_for(now - entry.stat().st_mtime)              # WI-0002 AC3
                          ^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/dangling/broken.pdf'
$ echo $?
1
```

Against `2a4b928~1` — the last commit before WI-0002 added `entry.stat()` — the same fixture
previews both files and exits 0:

```
move   broken.pdf -> documents/broken.pdf
move   photo.jpg -> images/photo.jpg
```

## Acceptance criteria

- [x] AC1 — Running either mode against a folder containing a dangling symlink still reports every
      other file in that folder. Checkable by the steps above: stdout names `photo.jpg`, and the
      run does not abort. What happens to `broken.pdf` itself is for `plan` to decide; that it must
      not take `photo.jpg` down with it is not.
- [x] AC2 — No output of either run states or implies that the folder could not be read, when it
      could. Checkable: the string `cannot be read` does not appear in stdout or stderr for the
      fixture above, and no Python traceback appears in either stream.
- [x] AC3 — The exit status of that run is one `README.md` documents, and `README.md` says which
      case it belongs to.
- [x] AC4 — A regression test in `tests/` builds a folder containing a dangling symlink alongside
      an ordinary file, asserts AC1 and AC2, and fails when the handling is removed. It skips
      itself where symlinks cannot be created.

## Notes

Filed by `verify` while verifying BUG-0001, from a boundary case built for that verification
rather than from a report — see `tracker/items/BUG-0001/artifacts/verify-report.md`
`## Negative and boundary cases exercised`.

`found-in: WI-0002` names the item that introduced the abort, established by running the fixture
against `2a4b928~1` and `2a4b928` rather than inferred from the diff. WI-0002 passes every one of
its own criteria; none of them mentions an entry whose `stat` fails, which is why this is a bug
against it and not a defect in its verification.

**This is not a reason to reverse BUG-0001.** Before BUG-0001, this fixture produced a traceback
and exit 1; after it, a wrong sentence and exit 2. Both are defects and neither is the other's
cause. If anything, BUG-0001 made this one *harder to notice* — a traceback advertises itself and
a calm false statement does not — which is an argument for fixing this item, not for keeping the
traceback.

A narrower alternative worth costing in `plan`: catching the per-entry `OSError` inside
`build_plan` and emitting a `leave` action would fix this without touching BUG-0001's CLI handler
at all, leaving that handler for the case it was actually written for. ADR-0006 chose the CLI
boundary for *the target folder*, which is a different question from what to do about one entry.

### Gaps accepted at review, 2026-08-27

Recorded here so they survive the item. Full reasoning in `artifacts/review.md`
`## Accepted gaps`.

- **No test covers an entry failing with `EACCES`, `EIO` or `ENOTDIR`.** Two members of the class
  are exercised (`ENOENT` by the item's own fixture, `ELOOP` by a symlink loop); a per-entry
  permission failure needs an unreadable parent, which is ADR-0006's target-level case and cannot
  be built without root. The guard is one `except OSError`, so the untested members differ only in
  the words `error.strerror` supplies.
- **A file deleted between `os.scandir` and `entry.stat()` is not tested** — a race the suite
  cannot schedule. Its output is identical to the dangling-symlink case, because the reason string
  names no cause.
- **The tests' skip path was read but never executed**, symlinks being available here. It is gated
  on `os.symlink` raising rather than on a platform name.
- **`README.md`'s exit-status paragraph was re-wrapped.** No word of the `1` clause changed, but
  its line breaks moved, and that clause is BUG-0005's subject: whoever implements BUG-0005 must
  re-read the paragraph rather than apply a remembered diff.
- **The mode banner is suppressed when nothing moves**, so a folder whose every entry is
  unexaminable prints its `leave` lines and `Nothing to do:` with no banner. Pre-existing
  behaviour decided at WI-0001/Q-001 (the `if moves:` guard on the banner in `tidy/cli.py`'s
  `main`), reproducible on a folder containing no symlinks; not a defect of this item.

### Gaps accepted at review round 2, 2026-08-27

Added after Q-001 and Q-002 were answered. Full reasoning in `artifacts/review.md`
`## Accepted gaps` `### Round 2`.

- **The three `path:line` citations left in `docs/` are unguarded.** `spec/doc-header.md` §4a makes
  `path` and `path:line` one citation form with one test — that the file exists — so
  `scripts/lint-claims` cannot see a line number that has drifted. Q-002's remedy removed six of
  them from ADR-0009; the three that remain (`ADR-0008` line 48, and ADR-0009's two `tidy/cli.py`
  citations) are protected by nothing. BUG-0006 carries this.
- **Round 1's `## Verdict` in `review.md` contains a prediction that did not hold** — that answering
  the two questions would move `main`. It did not: this project puts a document correction on the
  item's own branch, so `main` stood at `73bb1f4` for both rounds. The verdict is left as written,
  because a review records what its reviewer believed at the time; the correction is in
  `answer-questions`' journal entry and in `review.md`'s round-2 sections.
- **The `tidy/cli.py:72` citation in the note above was itself stale and is fixed here.** Line 72
  is blank; the banner guard is `if moves:` two lines below. It was written by round 1 of this
  review, in the tracker rather than in `docs/`, so no gate and no criterion covers it — which is
  the same shape as BUG-0006 and worth recording as one more instance rather than silently
  repairing.

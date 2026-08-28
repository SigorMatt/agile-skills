---
id: WI-0001
type: work-item
title: Sort a folder's files into subfolders by type, with a preview mode
status: done
priority: high
epic: EP-001
created: "2026-08-27T15:44:18Z"
updated: "2026-08-27T16:40:26Z"
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone with a folder full of unsorted files, I want to be shown exactly where every file
would be moved to and then have it done, so that the folder gets organised by kind of file
without me having to trust the tool before I have seen what it intends to do.

## Acceptance criteria

Throughout, `TOOL` is the command `plan` settles on; `PREVIEW` and `APPLY` are its two modes.
The *spelling* of the apply flag is `plan`'s to choose, and `--help` must reveal it (AC1), so a
verifier with a terminal can resolve `TOOL`, `PREVIEW` and `APPLY` from the tool itself.
"Destination path" means the path relative to the target folder, e.g. `images/photo.jpg`.

- [x] AC1 — `TOOL --help` exits 0 and its output names: the target folder as the first positional
      argument, the flag that selects APPLY, and the fact that without that flag the tool only
      previews.
- [x] AC2 — PREVIEW is the default. Running `TOOL <folder>` with no further flags moves nothing:
      it is the same run as AC4 asserts changes nothing on disk. APPLY happens only when the
      flag from AC1 is given.
- [x] AC3 — In PREVIEW over a folder containing at least one file of a recognised kind, stdout
      contains exactly one line per file that would be moved, and each such line contains that
      file's current name and its destination path. A file that would not be moved produces no
      such line. Exit status is 0.
- [x] AC4 — After a PREVIEW run, the folder is byte-for-byte unchanged: the same paths exist,
      with the same contents and the same sizes, and no destination subfolder has been created.
      Checkable by comparing a recursive listing taken before and after.
- [x] AC5 — The default mapping from extension to folder is exactly this, matched on the
      filename's final extension, case-insensitively, and it is stated in a file in the
      repository a user can read:

      | folder | extensions |
      |--------|------------|
      | `documents` | `.pdf .doc .docx .odt .rtf .txt .md .tex .epub` |
      | `spreadsheets` | `.xls .xlsx .ods .csv` |
      | `images` | `.jpg .jpeg .png .gif .bmp .svg .webp .tiff .heic` |
      | `audio` | `.mp3 .wav .flac .m4a .aac .ogg` |
      | `video` | `.mp4 .mov .avi .mkv .webm .wmv` |
      | `archives` | `.zip .tar .gz .tgz .bz2 .xz .7z .rar` |
      | `code` | `.py .js .ts .sh .c .h .cpp .java .rb .go .rs .html .css .json .xml .yaml .yml` |

      Checkable per row: put one file of each listed extension in a folder, run PREVIEW, and
      confirm each is destined for the folder its row names. `PHOTO.JPG` goes to `images`.
- [x] AC6 — A file whose extension is not in AC5's table, and a file with no extension at all,
      is left where it is. In both modes it is reported on a line that names it and says it is
      being left alone, and that line is distinguishable from a move line. After APPLY the file
      is still at its original path.
- [x] AC7 — In APPLY, every destination named by the PREVIEW of the same folder exists afterwards
      and holds that file, and the destination subfolders are created as needed. No file that
      existed under the target folder before the run is absent after it: the multiset of
      (basename, size) pairs found recursively under the folder is the same before and after,
      except for basenames changed by AC9's collision rule.
- [x] AC8 — PREVIEW and APPLY agree. Run PREVIEW, capture its output, run APPLY on the unchanged
      folder: the set of (file, destination) pairs APPLY produces is identical to the set PREVIEW
      printed.
- [x] AC9 — No file is ever overwritten. When a destination folder already contains a file of the
      same name, the incoming file is moved under a suffixed name instead, and the file that was
      already there is untouched — same size and same contents before and after the run.
      [src: EP-001/Q-002]
- [x] AC10 — Both modes report a collision explicitly: the output line for that file names the
      suffixed name it will be given or was given, so a user sees a rename coming before it
      happens. Checkable by placing `report.pdf` in the folder and a different `report.pdf` in
      `documents/` and reading the PREVIEW output. [src: EP-001/Q-002]
- [x] AC11 — Only files sitting directly in the target folder are considered. A subfolder that
      was already present is not entered and is not itself moved: it and everything inside it are
      at the same paths with the same contents after the run as before it, and no file inside it
      appears in either mode's output. [src: EP-001/Q-003]
- [x] AC12 — Running APPLY twice in a row over the same folder leaves the folder in the same
      state after the second run as after the first, and a PREVIEW run after the first APPLY
      prints no move lines. This follows from AC11 — the folders the first run created are
      subfolders on the second — and is what makes the tool safe to re-run.
- [x] AC13 — A file whose name begins with `.` is skipped entirely: it is not moved by APPLY and
      it appears in neither mode's output, not even as a left-alone line. Checkable by putting
      `.bashrc` and `.hidden.jpg` in the folder.
- [x] AC14 — Given a target path that does not exist, or one that is a regular file rather than a
      folder, the tool writes a message naming that path to stderr, writes nothing to stdout, and
      exits with status 2. Nothing on disk changes.
- [x] AC15 — Over a folder with nothing to move — empty, or containing only subfolders, only
      hidden files, or only already-tidy content — both modes print a single line stating there is
      nothing to do, print no move lines, and exit 0. "A single line" scopes to the four cases
      named here, in each of which nothing is left alone either, so that line is the whole of
      stdout. Where a folder has no move but does hold files AC6 leaves alone, AC6 governs and is
      not overridden: its lines are printed, and the nothing-to-do line is printed after them.
      [src: WI-0001/Q-001]

## Out of scope

- Age-based routing; that is WI-0002. This item's destinations depend on extension alone.
- User-supplied rules; AC5's table is hard-coded here, and WI-0003 is what makes it the user's.
- Making the collision behaviour in AC9 configurable — it is an invariant of the tool, not a rule
  [src: EP-001/Q-002].
- Classifying a file by anything other than its filename extension. No magic-byte sniffing, no
  reading contents — EP-001 excludes it, and AC5 is defined in terms of the extension for that
  reason.
- Undo, deletion, deduplication, compression, and any renaming other than AC9's collision suffix.
- Recursion into subfolders, and moving subfolders themselves [src: EP-001/Q-003].

## Notes

This is the thin end-to-end slice: scan a folder, decide a destination for each file, report the
plan, and carry it out. WI-0002 and WI-0003 both build on the machinery it establishes, which is
why they declare `depends-on: WI-0001`.

The tool is a command typed in a terminal, written in Python 3 against the standard library only
[src: ADR-0001].

**Assumptions this item carries.** None was confirmed by the stakeholder in a conversation; each
was decided by `refine` under the standing deferral they recorded on EP-001/Q-001 — *"Whatever's
easiest for you to build and test — you know this better than me"* — and each is reversible. The
reasoning for each is in `artifacts/refinement-qa.md`, and `plan` and `implement` inherit them as
assumptions rather than as stakeholder decisions:

1. **PREVIEW is the default and APPLY needs a flag** (AC1, AC2). Decided on the safe side of the
   stakeholder's own emphasis on seeing what will happen first, not on their instruction.
2. **The default extension table in AC5.** Conventional, and the most reversible thing here —
   WI-0003 exists to hand it to the user.
3. **Unrecognised files are left alone rather than swept into a catch-all** (AC6). The cost is
   real and is accepted: a folder full of unrecognised extensions is reported and left untidied,
   so a correct run can move nothing at all.
4. **Hidden files are skipped** (AC13), on the grounds that dotfiles are configuration rather
   than clutter and that someone pointing this at their home directory would call it broken
   otherwise.
5. **Exit status 2 for a usage error** (AC14), leaving 1 free for a future partial failure.

**Deliberately unconstrained, per DoR R10, left so by `refine`:**

- The exact form of the collision suffix in AC9. The stakeholder left it open themselves —
  *"report.pdf (2) or whatever you want to call it"* [src: EP-001/Q-002] — so any form satisfying
  AC9 and AC10 passes, and `plan` should record which it chose.
- What happens if a destination folder name in AC5 is already taken by a **file** at the top level
  — e.g. a file literally called `images` sitting beside `photo.jpg`. No criterion constrains it.
  It is rare, it does not affect any other criterion, and pinning it now would be inventing a
  requirement; `plan` should decide it and record the decision, and it is a candidate bug item if
  it turns out to matter. **Now decided, and it stays out of the criteria:** `plan`'s first version
  did not take this decision, `implement` filed WI-0001/Q-002 rather than guess, and the answer is
  recorded in `artifacts/plan.md` step 2 and `## Assumptions` 6 — such a file is reported as left
  alone, at plan time, so preview and apply cannot disagree about it [src: WI-0001/Q-002].

**Open design questions routed to `plan`, not to the stakeholder:** the command's name and the
apply flag's spelling; the exact text of a move line, a left-alone line and a collision line
(AC3, AC6 and AC10 constrain what each must contain, not how it reads); and where the AC5 table
is written down for a user to read.

**Gaps accepted at close, recorded here because nobody reads a verification report of a closed
item.** Each was declared by `implement` or `verify` and judged by `review-close` to be acceptable
rather than a send-back:

1. **ADR-0003's hard-link fallback is not exercised on a real filesystem that refuses hard links.**
   `verify` reached the branch by patching `os.link`, which is how BUG-0002 was found, but exFAT,
   FAT32, SMB and NFS were unavailable. On such a filesystem AC9's never-overwrite guarantee rests
   on a check-then-act rather than on the kernel, and `shutil.move`'s own behaviour there is
   unverified. Now recorded in `docs/architecture/overview.md` v2 as well [src: BUG-0002].
2. **AC8's coverage in the suite rests on AC7's test, not on its own.**
   `test_cli.ApplyTests.test_apply_matches_the_preview_it_printed` compares two rendered outputs,
   both produced before `apply_plan` is called, so an apply that silently moved nothing would still
   pass it; `test_apply_lands_every_destination_and_loses_nothing` is what catches that. The
   criterion is met — `verify` checked the previewed pairs against disk state directly — but WI-0002
   and WI-0003 both extend this path and should strengthen the AC8 test rather than trust it
   [src: tests/test_cli.py].
3. **Symlinks at the top level are unspecified and untested.** A symlink to a file is classified by
   its own name and moved *as a symlink*, so a relative one is silently broken by landing a level
   deeper; a symlink to a directory is skipped like any subfolder. `impl-report.md` records this
   incorrectly — it says `os.link` follows the link — and `verify` corrected it from a run. No
   criterion mentions symlinks and `mv` behaves the same way, so it is recorded rather than filed
   [src: tidy/planner.py; src: tidy/apply.py].
4. **`python3 -m tidy` only runs from the repository root.** There is no install step or entry
   point, which is what ADR-0001 chose; `cd`-ing into the folder being tidied gives
   `No module named tidy`. Packaging is a candidate future item, not a defect in this one
   [src: ADR-0001].
5. **Verified on Linux only**, Python 3.13 on ext4. A case-insensitive filesystem would make
   `PHOTO.JPG` and `photo.jpg` collide in a way AC9's suffix rule has never been tested against. No
   criterion names a platform [src: WI-0001 AC9].

Two defects found at verification are **not** accepted gaps — they are open work: BUG-0001 (an
unreadable folder crashes with a traceback) and BUG-0002 (a fully successful apply exits 1 without
hard links), both `found-in: WI-0001` and both at `ready`.

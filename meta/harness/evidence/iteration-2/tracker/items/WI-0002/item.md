---
id: WI-0002
type: work-item
title: Route files by how old they are, as well as by type
status: done
priority: medium
epic: EP-001
created: "2026-08-27T15:44:21Z"
updated: "2026-08-27T19:17:03Z"
depends-on:
  - WI-0001
branch: wi/WI-0002
outcome: delivered
---

## Story

As someone tidying a folder that has built up over years, I want old files separated from recent
ones, so that the things I am still working with stay easy to find and the rest is put away.

## Acceptance criteria

Throughout, `TOOL` is `python3 -m tidy`, `PREVIEW` is a run without `--apply` and `APPLY` a run
with it, as WI-0001 delivered them. "Destination path" means the path relative to the target
folder. The **band** is `recent` or `old`; the **type folder** is the one WI-0001 AC5's
extension table gives. `AGE(f)` means the run's start time minus `f`'s last-modified time.

Every criterion below is settled by a command over a folder whose file timestamps are set with
`os.utime`, which is how the existing suite fixes timestamps.

- [x] AC1 — Every file that moves has a destination path of exactly three components,
      `<band>/<type>/<name>`. PREVIEW over a folder containing `holiday.jpg` modified today
      prints `move   holiday.jpg -> recent/images/holiday.jpg`. The band is therefore the first
      component of the path already on WI-0001 AC3's move line, so no additional output is needed
      to see which band a file fell into. [src: WI-0002/Q-001]
- [x] AC2 — Two files of the same type in different bands get different destinations. With
      `a.pdf` modified now and `b.pdf` modified 400 days ago in the same folder, PREVIEW prints
      `recent/documents/a.pdf` for the first and `old/documents/b.pdf` for the second.
- [x] AC3 — Age is the file's last-modified time (`st_mtime`) and nothing else. Decided by two
      files: one whose mtime is now and whose atime is 400 days ago goes to `recent/…`; one whose
      mtime is 400 days ago and whose atime is now goes to `old/…`. A tool measuring last-access
      time would place them the other way round.
- [x] AC4 — There are exactly two bands and one boundary, at **365 days = 31 536 000 seconds**. A
      file is `old` when `AGE(f) >= 365 days` and `recent` when it is less. Decided by three
      files: mtime exactly 365 days before the run → `old/…`; 365 days less one minute →
      `recent/…`; 365 days plus one minute → `old/…`. No third band name appears anywhere in
      either mode's output over any folder. [src: WI-0002/Q-002]
- [x] AC5 — PREVIEW and APPLY agree on the band, as WI-0001 AC8 requires of the destination.
      Capture PREVIEW's set of (name, destination) pairs over a folder, run APPLY on the
      unchanged folder, and every file is afterwards at exactly the path PREVIEW printed. Both
      path components are created as needed, so `old/documents/` exists afterwards even though
      neither `old/` nor `old/documents/` existed before.
- [x] AC6 — A file with no matching extension, or no extension at all, is not aged. In both modes
      it gets WI-0001 AC6's `leave` line, no band appears in that line, and after APPLY the file
      is still at its original path — whatever its mtime. Checkable with `notes.xyz` modified 400
      days ago: the output line names it and leaves it, and no `old/` folder is created for it.
- [x] AC7 — The never-overwrite rule applies inside the band path. With a folder holding
      `report.pdf` modified 400 days ago and an existing `old/documents/report.pdf` of different
      contents, both modes print the destination `old/documents/report (2).pdf` on that file's
      line, and after APPLY the pre-existing `old/documents/report.pdf` has the same size and
      contents it had before. [src: EP-001/Q-002]
- [x] AC8 — A file whose name begins with `.` is still skipped entirely, whatever its age: it is
      not moved by APPLY and appears in neither mode's output. Checkable with `.hidden.jpg`
      modified 400 days ago.
- [x] AC9 — Subfolders that were already present are still neither entered nor moved, including
      ones with the names this item introduces. With a folder containing a pre-existing
      `documents/` (from a run of the previous version), a pre-existing `old/` and a pre-existing
      `recent/`, each holding a file: after APPLY all three folders are at the same paths, every
      file inside them that was not a destination of this run is unchanged, and no file inside
      any of them appears in either mode's output. [src: EP-001/Q-003]
- [x] AC10 — A file that crosses the boundary after it has been sorted is never re-filed. Take a
      folder in which `recent/documents/notes.txt` exists from an earlier run, set that file's
      mtime to 400 days ago, and run both modes: no output line names `notes.txt`, and after
      APPLY it is still at `recent/documents/notes.txt`. This follows from AC9 — it is below the
      top level — and is a consequence a user would otherwise discover for themselves.
      [src: EP-001/Q-003]
- [x] AC11 — Running APPLY twice over the same folder leaves the same state after the second run
      as after the first, and a PREVIEW between them prints no move lines. The folders created by
      the first run are subfolders on the second, so this follows from AC9.
- [x] AC12 — When the name a band folder needs is taken by something that is not a folder, the
      files that would go under it are left alone rather than failing. With a regular file named
      `old` directly in the target folder and `taxes.pdf` modified 400 days ago beside it, both
      modes print a `leave` line for `taxes.pdf` whose reason names `old`, nothing is moved, the
      regular file `old` is unchanged, and the exit status is that of a run with nothing to move.
      This is WI-0001/Q-002's rule for the type folder, applied to the component this item adds.
- [x] AC13 — `README.md` states, in the file WI-0001 AC5's extension table already lives in: the
      shape of the tree (`<band>/<type>/<name>`), both band names, that age is the last-modified
      time, and the boundary as a number of days. Checkable by reading it and comparing against
      AC1, AC3 and AC4.

## Out of scope

- User-supplied age boundaries and user-supplied band names; that is WI-0003. This item
  hard-codes the two bands and the 365-day boundary.
- **More than two bands.** The stakeholder was offered three and chose two [src: WI-0002/Q-002];
  a third band is not a stretch goal of this item.
- **Migrating a folder that the previous version tidied.** WI-0001 put the type folders at the
  top level, so a folder tidied before this item lands and tidied again afterwards holds both
  `documents/` and `old/documents/`. This item does not move the old-layout folders under a band:
  they are subfolders, existing subfolders are left alone [src: EP-001/Q-003], and nobody has
  asked for a migration. AC9 fixes the behaviour; this entry records that the resulting mixed
  tree is accepted rather than overlooked.
- Re-opening any of the invariants WI-0001 established: no file is overwritten, and only files
  sitting directly in the target folder are considered [src: EP-001/Q-002; EP-001/Q-003]. Age
  routing changes which destination is chosen, not what may happen to a file once it is chosen.
- Any use of a file's age other than choosing its destination — no deleting, archiving,
  compressing or reporting on old files.
- Anything the epic's own out-of-scope list excludes.

## Notes

**How type and age combine is decided: the age band is the top level, the type folder sits inside
it** [src: WI-0002/Q-001]. A tidied folder holds `recent/` and `old/`, and each of those holds the
type folders WI-0001 built — `recent/images/holiday.jpg`, `old/documents/taxes-2019.pdf`. The
stakeholder chose this over "a folder per type containing folders per age band" for a reason that
constrains the design further than the choice does: they want to "look at the top level and know
what's actually live". So no type folder may sit above a band folder, and relocating the age split
one level down later would remove the thing they asked for rather than tidy it.

**There are two bands, `recent` and `old`, split at one year** [src: WI-0002/Q-002]. The
stakeholder took the two-band option over `refine`'s three-band recommendation: "anything I
haven't touched in a year is old". The band names are their words and are the folder names.

`depends-on: WI-0001` is a real dependency, not a preference: this item changes how a destination
is chosen, and WI-0001 is what establishes that there is a destination-choosing step at all.

**This item is second of the three.** The stakeholder had no preference between it and WI-0003 and
delegated the order [src: EP-001/Q-004]; WI-0002 was placed before WI-0003 so that the rule format
WI-0003 designs can cover age as well as type from the start, rather than being extended twice.
Its `priority: medium` records that position, between WI-0001 (`high`) and WI-0003 (`low`).

The tool is a command typed in a terminal, written in Python 3 against the standard library only
[src: ADR-0001], so AC3's "which timestamp age is measured from" is a choice among the fields
`os.stat` returns — and that choice is `st_mtime`, as an assumption the stakeholder did not
overrule (below).

**Refinement is complete: round 1 asked the stakeholder the two questions that were theirs, and
round 2 rewrote the criteria against their answers.** Round 1 built the Definition of Ready
agenda, routed eight gaps, answered or delegated six, and filed Q-001 and Q-002. Both came back
[src: WI-0002/Q-001; src: WI-0002/Q-002], `answer-questions` propagated them, and round 2 rewrote
AC1–AC5 into AC1–AC13 without asking anything further — nothing left needed a person. The whole
exchange is in `artifacts/refinement-qa.md`, now `status: recorded`.

**Four assumptions this item carries, none of them the stakeholder's decision.** Each is
reversible and each is here so that `plan`, `implement` and `verify` inherit it visibly rather
than discovering it:

1. **Age is the file's last-modified time (`st_mtime`), not last-access or inode-change time.**
   Q-002 asked the stakeholder to say if they meant "when it arrived here"; they did not, and
   their "haven't **touched** in a year" supports last-modified without distinguishing it from
   last-accessed. Fixed by AC3. Reversible: one call site in the planner and the tests that set
   timestamps.
2. **"One year" is 365 days — 31 536 000 seconds — measured from the run's start time.** Not
   settled by their answer, and not worth their attention: the alternatives (366 in a leap year,
   twelve calendar months) differ by at most a day at a boundary nobody perceives, and AC4 cannot
   be decidable without a number. Chosen because it needs no calendar arithmetic and is one
   constant. Fixed by AC4; reversible by changing that constant and AC4's three test files.
3. **A file exactly on the boundary is `old`** — the interval is half-open. No product stake;
   decided so a test can fix a timestamp on the boundary and assert a side. Fixed by AC4.
4. **The bands are documented in `README.md`**, beside WI-0001 AC5's extension table, which AC5
   already established as the file a user reads the rules in. Fixed by AC13.

**Every combination this item introduces now has a criterion or an out-of-scope entry (DoR R10),
and here is the map**, so a reader can check the claim rather than take it: an unrecognised file
is not aged → AC6; the never-overwrite suffix inside the deeper path → AC7; hidden files still
skipped → AC8; existing subfolders — including ones already called `documents/`, `old/` or
`recent/` — untouched → AC9; **a file that ages after it was sorted is never re-filed** → AC10, a
real product consequence [src: EP-001/Q-003] rather than an oversight; re-running is still a
no-op → AC11; the band folder's name taken by a regular file → AC12, extending WI-0001/Q-002's
rule to the component this item adds; the band visible in the preview → AC1, satisfied by the
destination path itself. The one combination that is **not** given behaviour is the mixed tree a
previous version leaves behind: it is in `## Out of scope`, with the reason and the closed
decision it follows from.

**Open design question routed to `plan`, not to the stakeholder:** how the age rule is represented
internally, so that WI-0003 can make it user-supplied alongside the extension table without
designing the rule format twice. The answer is the same whoever the stakeholder is, so it is
`plan`'s under its own preference order [src: docs/architecture/overview.md].

**Five gaps accepted at review, recorded here so that closing this item does not bury them**
(the reports they came from stop being read once an item is `done`):

1. **Symlinks are aged by their target's `mtime`.** `entry.stat()` follows a link, as
   `entry.is_dir()` already did, so a symlink to a file modified two years ago is `old` whatever
   the link's own age. No criterion covers symlinks and none was added. Consistent with the
   behaviour WI-0001 delivered [src: tidy/planner.py]; accepted rather than fixed because
   changing it would be new behaviour nobody asked for.
2. **Age is wall-clock arithmetic on a timestamp the filesystem reports.** A file restored from a
   backup with its date preserved is aged by that original date; one copied without preservation
   looks new. Inherent in the stakeholder's own framing — "anything I haven't touched in a year"
   — and named in `plan.md` `## Risks`. Accepted; there is nothing the tool could read instead.
3. **AC4's "no third band name appears anywhere in either mode's output over any folder" was
   decided by its grounds, not by exhaustion**, because it cannot be exhausted. The grounds:
   every destination's first component is `band_for`'s return, and `DEFAULT_BANDS` holds exactly
   `recent` and `old` [src: tidy/rules.py]. Accepted as an argument rather than a measurement.
4. **The exact 365-day boundary was settled by calling `band_for(31536000)` directly, not through
   a folder.** `build_plan` reads its own clock, so no fixture can make a file exactly that old at
   the instant the run measures it; the folder-level case is boundary-plus-epsilon. Accepted: the
   two measurements together decide the criterion.
5. **AC13's regression test is weakly sensitive to one of its four clauses.** It asserts
   `"last modified"` as a whole-file substring, and `README.md` contains the phrase three times,
   so rewording the sentence a user actually reads leaves the suite green — verified at review by
   doing exactly that. The criterion passes: the README does state the field. Accepted rather than
   filed, because it is a weakness in the net rather than a defect in the delivered behaviour, and
   WI-0003 rewrites this area's documentation and its tests anyway.

**One defect was found during verification and does not belong to this item: BUG-0003** —
`tidy --help` still describes destinations as chosen by file type alone, which age routing made
false. No criterion of this item covers the help text, so it was filed rather than sent back
[src: tracker/items/WI-0002/artifacts/verify-report.md].

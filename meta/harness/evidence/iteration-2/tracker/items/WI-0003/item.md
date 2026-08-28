---
id: WI-0003
type: work-item
title: Let the user supply the sorting rules instead of using built-in ones
status: done
priority: low
epic: EP-001
created: "2026-08-27T15:44:24Z"
updated: "2026-08-27T22:15:28Z"
depends-on:
  - WI-0001
branch: wi/WI-0003
outcome: delivered
---

## Story

As someone whose folder does not look like anybody else's, I want to write my own rules for where
files go, so that the tool sorts my files the way I want rather than the way its author guessed.

## Acceptance criteria

Throughout, `TOOL` is `python3 -m tidy`, `PREVIEW` is a run without `--apply` and `APPLY` a run
with it, as WI-0001 delivered them, and a **destination path** is the path relative to the target
folder — exactly three components, `<band>/<type>/<name>`, as WI-0002 AC1 fixed. **RULES(F)** means
a run configured to use rule file `F`, by whichever mechanism this item delivers and AC12 requires
`README.md` to document; **no rules** means a run with none supplied, which includes the case where
a default location exists and holds no file.

`S` is the **sample folder**, and every criterion that names it uses this one. It holds six files
directly, hidden file included, with mtimes set by `os.utime` as the existing suite already does
(`tests/`), all relative to the run's start time:

| name | mtime | where it goes today |
|------|-------|---------------------|
| `budget.csv` | now | `recent/spreadsheets/budget.csv` |
| `holiday.jpg` | now | `recent/images/holiday.jpg` |
| `report.pdf` | now | `recent/documents/report.pdf` |
| `taxes.pdf` | 400 days ago | `old/documents/taxes.pdf` |
| `notes.xyz` | now | nowhere — `leave  notes.xyz   [no rule for '.xyz']` |
| `.hidden.jpg` | now | nowhere — skipped entirely, absent from the output |

- [x] AC1 — **With no rules supplied, nothing about the tool changes.** PREVIEW and APPLY over `S`
      produce exactly the output and the resulting tree the "where it goes today" column above
      states, and the whole test suite WI-0001 and WI-0002 delivered passes unaltered
      (`python3 -m unittest discover -s tests -t . -q`, exit 0, no test edited to accommodate this
      item). If this item introduces a default location for a rule file, a run with nothing at that
      location is a no-rules run and is settled by this same criterion.
- [x] AC2 — **A rule file's type entries override the built-in table for the extensions they name,
      and only those.** With `F1` whose only type entry sends `.csv` to `data`, RULES(F1) PREVIEW
      over `S` prints `move   budget.csv -> recent/data/budget.csv` and prints for the other five
      files exactly the lines AC1 gives. [src: WI-0003/Q-001]
- [x] AC3 — **A rule file may add an extension the built-in table does not have.** With `F2` whose
      only type entry sends `.xyz` to `notes`, RULES(F2) PREVIEW over `S` prints
      `move   notes.xyz -> recent/notes/notes.xyz` where AC1 gives a `leave` line, and the other
      five lines are unchanged. [src: WI-0003/Q-001]
- [x] AC4 — **Two different rule files over the same unchanged folder give two different, stated
      previews.** `F1` from AC2 and `F3`, identical to `F1` but sending `.csv` to `tables`. Run
      RULES(F1) PREVIEW then RULES(F3) PREVIEW over the same `S`, with no APPLY between them so
      nothing has moved: the two outputs differ in exactly one line, `budget.csv`'s, which reads
      `-> recent/data/budget.csv` in the first and `-> recent/tables/budget.csv` in the second.
- [x] AC5 — **A rule file renames both bands and moves the one boundary.** With `F4` whose only
      band entry names `current` and `archive` with a boundary of 90 days, RULES(F4) PREVIEW over
      `S` sends the four movable files to `current/…` except `taxes.pdf`, which goes to
      `archive/documents/taxes.pdf`. The boundary keeps WI-0002 AC4's sense — a file whose age is
      exactly the boundary falls in the **older** band — decided by three files at 90 days exactly,
      90 days less a minute, and 90 days plus a minute. [src: WI-0003/Q-002; src: WI-0002/Q-002]
- [x] AC6 — **Either table may be supplied without the other, and what is omitted keeps its
      built-in values.** RULES(F1) — type entries only — puts `taxes.pdf` at
      `old/documents/taxes.pdf`, the built-in bands and boundary. RULES(F4) — band entries only —
      puts `budget.csv` at `current/spreadsheets/budget.csv`, the built-in type table. This is
      AC2's layering applied to the age side. [src: WI-0003/Q-001]
- [x] AC7 — **There are exactly two bands, and a rule file that asks for another number is
      rejected.** A rule file naming three bands, or one, is rejected by AC8's rule: one line on
      stderr naming the file and the problem, nothing on stdout, a non-zero exit, and nothing moved
      even under `--apply`. Over any folder and any accepted rule file, no third band name appears
      in either mode's output. [src: WI-0003/Q-002]
- [x] AC8 — **A malformed rule file is rejected before anything moves, identically in both modes.**
      For each of the classes below there is a file that exhibits it; for each, both PREVIEW and
      APPLY print one line on stderr naming the rule file and what is wrong with it, print nothing
      on stdout, exit non-zero, and leave `S` byte-for-byte as it was. The classes are: not
      parseable in the format `plan` chooses; a type destination that is not a single path
      component (empty, or containing `/`); an extension entry that does not begin with `.`; a
      band count other than two; a boundary that is not a positive number of days; a band name
      that is empty, contains `/`, or is the same as the other band's.
- [x] AC9 — **The never-overwrite rule applies to a user-supplied destination.** With `F5` sending
      `.pdf` to `papers`, and `recent/papers/report.pdf` already present with different contents,
      RULES(F5) prints `-> recent/papers/report (2).pdf` on `report.pdf`'s line in both modes, and
      after APPLY the pre-existing `recent/papers/report.pdf` has the size and contents it had
      before. [src: EP-001/Q-002]
- [x] AC10 — **Supplying rules changes nothing else the tool promises.** Under RULES(F1) over `S`:
      `.hidden.jpg` appears in neither mode's output and is not moved; a pre-existing subfolder and
      everything in it is neither entered nor moved nor listed; and a file matching neither the
      rule file nor the built-in table still gets a `leave` line rather than a catch-all folder —
      checkable by removing `.xyz` from `F2` and observing `notes.xyz` left again.
      [src: EP-001/Q-002; src: EP-001/Q-003; src: README.md]
- [x] AC11 — **PREVIEW and APPLY agree under a rule file, including where a destination collides
      with a band name.** Capture RULES(F) PREVIEW's set of (name, destination) pairs over `S`, run
      RULES(F) APPLY over the unchanged `S`, and every file is afterwards at exactly the path
      PREVIEW printed — for `F1`, `F2`, `F4`, `F5`, and for `F6`, which sends `.pdf` to a folder
      named `old`. What `F6` does is `plan`'s to decide (`## Notes`); whichever it decides, this
      criterion requires the two modes to agree and AC12 requires `README.md` to say which it is.
- [x] AC12 — **`README.md` tells a user everything above that they cannot see from the output.**
      It states: where the tool looks for a rule file and how to point it at a specific one; the
      file's format, with a complete worked example that would produce AC2's and AC5's results;
      that entries layer over the built-in table and that a built-in mapping can be redirected but
      not removed; that there are exactly two bands and no others, whatever they are called; what
      happens when a rule file is rejected, including the exit status; and what a destination
      colliding with a band name does. Checkable by reading it against AC2, AC5, AC7, AC8 and AC11.
      [src: EP-001/Q-001]

## Out of scope

- A graphical or interactive rule editor.
- Rules that can turn off or vary the never-overwrite behaviour, or that can make the tool descend
  into subfolders. Both were settled by the stakeholder as invariants of the tool rather than
  things a user configures [src: EP-001/Q-002; EP-001/Q-003].
- Rules that depend on anything other than what WI-0001 and WI-0002 already decide on — no rules
  based on file contents, ownership, or permissions.
- **Removing a built-in mapping.** Because the stakeholder chose layering with their entries
  winning, a rule file can redirect any extension the built-in table names but cannot make the tool
  stop filing one. Wanting `.md` files left where they are, rather than filed under `documents/`,
  is not expressible and is a known gap rather than a defect [src: WI-0003/Q-001].
- **A rule file that changes how many age bands there are, or that turns age routing off.** The
  stakeholder fixed the count at two — "keep it at two bands. Recent and old is all I need" — so a
  rule file may rename the two bands and move the one boundary and nothing else. Three bands, one
  band, and a flat layout with no band folders are all out [src: WI-0003/Q-002].
- **A catch-all rule.** `README.md` promises that a file matching no rule "is left where it is and
  reported on a `leave` line. It is not swept into a catch-all folder" [src: README.md]. Letting a
  rule file introduce one would change a documented promise, and nothing the stakeholder has said
  asks for it. Excluded deliberately rather than asked
  [src: tracker/items/WI-0003/artifacts/refinement-qa.md].
- **A destination more than one folder deep.** A type entry names a single folder — `data`, not
  `work/pdfs` — so a destination path stays the three components `<band>/<type>/<name>` that
  WI-0002 AC1 already promises. This is `refine`'s assumption, not the stakeholder's decision:
  they were not asked, because the alternative would silently break a criterion an earlier item
  was verified against. Recorded as an assumption in `artifacts/refinement-qa.md` R2.4, and it is
  the entry on this list most likely to be the one they would want changed.
- Anything the epic's own out-of-scope list excludes.

## Notes

**Supplied rules layer over the built-in ones, and the user's entries win** [src: WI-0003/Q-001].
The stakeholder chose option B: "sit on top, mine win. I don't want to retype your whole
seven-folder list just to move one extension somewhere else." So a rule file naming only `.csv`
redirects `.csv` and leaves every other extension filed exactly as it is today; a rule file may
also add an extension the built-in table does not have. It may not remove one — that is now on
`## Out of scope` above. Intake left this undecided and named `refine` as its owner; `refine`
routed it to the stakeholder, and this is their answer. AC1 fixes only the no-rules-supplied
case; what a *partial* rule set leaves alone is now decided and is `refine`'s to write into the
criteria.

**What a rule set has to be able to express is now fixed on the age side** [src: WI-0002/Q-001;
src: WI-0002/Q-002]. The stakeholder chose an age-first tree — `recent/` and `old/` at the top
level with the type folders inside — and **two** bands split at one year. So a rule format must be
able to name a destination that sits *under a band folder*, not only a type folder, and it has
exactly one age boundary to express, not a list of them. **Whether a user may add or remove bands
is now settled: they may not** [src: WI-0003/Q-002]. The stakeholder chose option A — "keep it at
two bands. Recent and old is all I need, don't want to think about more than that" — so a rule
file supplies exactly two band names and one boundary. `README.md`'s "there are two bands and no
others" stays true, and ADR-0005's ordered band table stays at length two with its two names and
its one boundary made user-supplied, which is exactly what WI-0002 promised this item
[src: tracker/items/WI-0002/item.md `## Out of scope`].

**This item is last of the three, and it is not optional.** The stakeholder had no preference
between it and WI-0002 and delegated the order, asking only that neither be left hanging
[src: EP-001/Q-004]. Its `priority: low` records its position in the sequence and nothing more:
EP-001 cannot close with an outcome of `delivered` unless this item is delivered too.

The tool is written in Python 3 against the standard library only [src: ADR-0001], which
constrains the rule format `plan` may choose: there is no YAML parser in the standard library, so
the format will be one of JSON, INI via `configparser`, or TOML via `tomllib` — and the last of
those would raise the interpreter floor ADR-0001 sets.

`depends-on: WI-0001` is a real dependency: there must be rules before there is anything to
configure. There is deliberately **no** dependency on WI-0002 — if WI-0002 lands first, the rule
set covers age as well as type, and if it does not, it covers type only. That is what makes the
ordering of WI-0002 against WI-0003 a genuine question for the stakeholder (EP-001/Q-004) rather
than something the dependency graph already answers.

### Refinement, 2026-08-27 — two rounds, both closed

Two blocking questions were filed and the stakeholder has answered both: **Q-001** — user rules
layer over the built-in ones with the user's entries winning (option B) — and **Q-002** — two age
bands always, the user choosing their names and the one boundary (option A). Both answers are
recorded verbatim in `artifacts/refinement-qa.md` and propagated into the paragraphs above and
into `## Out of scope`.

`answer-questions` propagated the two decisions and left the criteria alone. `refine` then rewrote
them in round 2 — AC1 through AC12 above replace intake's rough AC1 through AC5 — closing R4 and
R10 without asking the stakeholder anything further: every remaining gap was either a consequence
of the two answers, a decision their standing delegation covers [src: EP-001/Q-001], or an
implementation choice routed to `plan`. The round 2 reasoning is in `artifacts/refinement-qa.md`,
which now declares `status: recorded`.

### R10 — the combinations this item introduces, and where each is stated

One new axis: rules supplied, or not. Crossed with what already exists —

| combination | where it is stated |
|-------------|--------------------|
| rules supplied × PREVIEW and `--apply` | AC11 (the two modes agree), AC8 (a rejection is identical in both) |
| rules supplied × an extension the rules do not name | AC2 (keeps its built-in destination) |
| rules supplied × an extension neither the rules nor the built-in table names | AC10 (`leave` line, no catch-all) |
| rules supplied × the never-overwrite invariant | AC9 |
| rules supplied × hidden files, and × subfolders | AC10 |
| rules supplied × a destination colliding with a band folder name | AC11 — **deliberately unconstrained by `refine`**, routed to `plan` below. The criterion fixes what a user can rely on (the two modes agree, `README.md` says which) without fixing which behaviour `plan` picks; both candidates are safe, since nothing is overwritten either way and the preview shows the result before anything moves |
| a type table without a band table, and the reverse | AC6 |
| a rule file that is present but rejected | AC7, AC8 |
| a default location that exists but holds no file | AC1 |
| rules supplied × a target folder that cannot be used | **deliberately unconstrained by `refine`**: which of the two errors is reported when both a rule file and the target folder are bad is `plan`'s, under `README.md`'s existing exit-status vocabulary. Whichever it picks, AC8 still requires nothing to move and a non-zero exit |

**Open design questions, routed to `plan` rather than to the stakeholder.** Each has the same
answer whoever the stakeholder is, so none was escalated:

- What happens when a rule file names a type folder whose name collides with a band folder name —
  a rule sending `.pdf` to `old`, say. The destination is `<band>/<type>/<name>`, so the result
  would be `old/old/report.pdf`, which is legal but almost certainly not meant. AC11 binds `plan`
  only to consistency between the modes and to documenting the choice.
- The rule file's format — JSON, or INI via `configparser`. TOML via `tomllib` would raise the
  interpreter floor ADR-0001 sets, so taking it needs an ADR that says so.
- Whether the type table and the band table come from one rule file or two. That a file may carry
  one without the other is no longer open: AC6 requires it.
- Where the tool looks for rules and how a user points it at a specific set (a default path, a
  flag, an environment variable, or a combination). Falls under the stakeholder's standing
  delegation of how the thing is built [src: EP-001/Q-001]; AC12 requires only that whatever is
  chosen is documented in `README.md`.
- The exit status of a run that rejects a rule file, and which error wins when the target folder
  is unusable as well. Bounded to 0, 1 and 2 already [src: README.md; src: ADR-0006]; AC8 requires
  only that it is non-zero and AC12 that `README.md` accounts for it.

**Deliberately excluded rather than asked: a catch-all rule.** `README.md` promises that a file
matching no rule "is left where it is and reported on a `leave` line. It is not swept into a
catch-all folder" [src: README.md]. Letting a rule file introduce one would change a documented
promise and nothing the stakeholder has said asks for it; it joins `## Out of scope` when the
criteria are rewritten.

### Review, 2026-08-27 — two rounds; four gaps accepted, and where they are

`review-close` accepted the change and recorded these rather than sending the item back. None
violates an acceptance criterion; each is written here because a gap recorded only in a report is
one nobody reads again [src: tracker/items/WI-0003/artifacts/review.md].

- **`Ruleset` is a frozen dataclass, but its `by_extension` dict is mutable in place.**
  `BUILT_IN.by_extension` *is* `rules._BY_EXTENSION`, so `BUILT_IN.by_extension[".zzz"] = "x"`
  succeeds and changes the built-in table for the rest of the process; only rebinding a field
  raises `FrozenInstanceError`. Nothing in the code does this and `merge` copies before it
  updates, so no behaviour is wrong today. What would go wrong: a later item adding a rule "in
  place" — the obvious way to write it — would silently corrupt every subsequent lookup in the
  same process, which is the global-state failure ADR-0011 chose its option B to avoid
  [src: docs/architecture/adr/ADR-0011-a-ruleset-is-a-value-passed-into-the-planner.md]. The fix
  is a design change (`MappingProxyType`, or pairs instead of a dict) and belongs to `plan`.
- **`boundary-days = inf` is accepted**, and puts every file in the newer band. AC8 requires
  rejecting a boundary that is "not a positive number of days", and `inf` is a positive number,
  so this sits inside the criterion rather than outside it. Declared by `implement` and
  reproduced by `verify` [src: tracker/items/WI-0003/artifacts/verify-report.md].
- **Two things were not exercised**, both declared: a `\`-separated path (`os.altsep` is `None`
  on the platform this ran on) and a rule file the process may not read, which takes the same
  `OSError` branch as the missing-file and is-a-directory cases that were exercised. No criterion
  asks for either.
- **`--rules ""` is silently a no-rules run.** `cli.py` guards the loader with `if args.rules:`,
  so an empty string reaches neither `ruleset_file.load` nor an error path: the run sorts by the
  built-in tables and exits 0, where a missing path, a directory and an unparseable file each give
  one line on stderr and exit 2 [src: tidy/cli.py;
  src: run: python3 -m tidy /tmp/emptyrules/S --rules "" → exit 0, previews with the built-in
  rules]. No criterion covers it — AC8's six classes are properties of a rule *file* and an empty
  path names none, and the empty-file case AC1 settles is a different one — and `plan` did not
  specify it either way, so it is accepted rather than sent back. What would go wrong, and when:
  `--rules "$RULES"` with `RULES` unset expands to exactly this, and the user believes their rules
  applied when the built-in ones did. The fix, for whichever item wants it, is to test
  `args.rules is not None` and let `load` report the empty path in the ordinary way. Found by
  `review-close` in round 2 [src: tracker/items/WI-0003/artifacts/review.md].

A fourth observation was not a note but a question: this merge makes ADR-0008's `[src: run: …]`
evidence unreproducible, which went to the architect as WI-0003/Q-003. **It is now answered and
closed.** Both citations in ADR-0008 `## Decision` were amended in place to the anchored check
`grep -nE "^(from|import).*\brules\b" tidy/cli.py → exit 1, no output`, which tests the claim
rather than snapshotting the file, and the ADR is at v2 with a change-log row naming this item
[src: WI-0003/Q-003; src: ADR-0008]. Nothing under `tidy/` changed and no acceptance criterion of
this item moved; the D12 failure that held the merge is gone and the item resumed at `in-review`.

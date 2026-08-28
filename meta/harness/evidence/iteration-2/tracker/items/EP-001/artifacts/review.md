# Review — EP-001

The engagement's ending, not an item review. There is no branch, no diff and no merge: an epic
advances only through its children, and all ten of them were reviewed, merged and closed under
their own IDs. What is judged here is the **engagement** — whether the goal was reached, whether
the record says so truthfully, and whether the person who asked for it accepts what they got.

## What I examined

**The state, from the programs rather than from the board.**

- `scripts/engagement-state EP-001` → `at-rest`, "every child has stopped, no question is open,
  no request is open", rest reached at 2026-08-28T15:41:23Z.
- `scripts/check-epic-signoff EP-001` → PASS: `questions/Q-006.md` carries the stakeholder's
  reply, names all 10 children, and was filed after that rest.
- The frontmatter of all ten children: every one `status: done`, `outcome: delivered`.
- `EP-001/history.md` end to end — six rows, no gap, and the last row's status matches `item.md`.
- Every question file in the engagement: 16 in total across the ten children and the epic, all
  `status: answered`; none `open`, none `deferred`.

**The tool, run rather than read about.** Each of the epic's five success measures was
demonstrated during this review on a scratch folder under `.harness/` (git-ignored), not quoted
from a previous execution's transcript. The commands and their output are in `## Definition of
Done` under DE3.

**The claims, from what they cite.** DE6 asks whether the confident sentences in `docs/` are still
true, and the only way that can fail is to open the cited thing. Five absolute claims that this
epic's work touched, and what was opened for each:

| claim | cited | what I opened, and what it said |
|---|---|---|
| a run with no `--rules` reads `$XDG_CONFIG_HOME/tidy/rules.ini`, else `$HOME/.config/tidy/rules.ini` | `docs/product/vision.md` → `tidy/ruleset_file.py` | `default_path(environ)` returns exactly those two, in that order, and `None` when neither variable is set — the citation supports the sentence rather than merely resolving |
| the value comes from the environment mapping and nowhere else — no `pwd` lookup, no `expanduser` | `ADR-0014` point 1 → `tidy/ruleset_file.py` | `environ.get("XDG_CONFIG_HOME")` and `environ.get("HOME")`; no `expanduser` and no `pwd` import anywhere in the module |
| present-and-unusable is decided with `os.path.lexists`, so a dangling symlink counts as present | `ADR-0014` point 4 → `tidy/ruleset_file.py` | `resolve()`: `if path is None or not os.path.lexists(path)` — `lexists`, as claimed |
| the rule file is named on stderr **before** anything about the files | `docs/product/vision.md`, `ADR-0014` point 5 → `tidy/cli.py` | `resolve_rules` at the top of `main`, the `using rules from` write immediately after it, and the banner and per-file lines only after the folder has been listed. The ordering is in the code, not only in the prose |
| every destination is decided in `planner.py` and nowhere else | `docs/architecture/overview.md` → `ADR-0002`, `tidy/planner.py` | band, type folder and the collision suffix are all computed in `planner.py`; `apply.py` only joins the folder onto `action.destination` to get an absolute path, which is not a destination decision. Claim holds as written |

Two smaller ones checked the same way, both from `overview.md`: `tidy/cli.py` imports nothing from
`tidy/rules.py` (its three imports are `apply`, `planner`, `ruleset_file`), and `build_plan`'s
`ruleset` parameter defaults to `None` and resolves to `BUILT_IN` internally (`planner.py` lines
27, 42–43).

**What the stakeholder was told, against what is true.** `Q-006` showed five runs and made three
claims about them. Each was re-run here, and the behaviour is what the question said it was: the
default file is picked up with no flags, `--rules` overrides it and the stderr line names the
flag's file, and nothing at the default location leaves the built-in behaviour byte-for-byte
intact.

## Definition of Done

The **epic** Definition of Done, `spec/dor-dod.md` §4. Criterion by criterion; a single verdict
does not satisfy the gate.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | every child terminal, and every child that did not deliver named in the termination question and in the outcome | **pass** | All ten children are `status: done` — WI-0001..WI-0004, BUG-0001..BUG-0006. `check-epic-signoff` confirms `Q-006` names all ten by ID. No child failed to deliver, so the "named" half is vacuous here and the outcome does not have to qualify anything |
| DE2 | every child's `outcome` recorded; dropped items say why | **pass** | Ten of ten carry `outcome: delivered` in their frontmatter. Nothing was dropped or duplicated, so no `## Notes` reason is owed |
| DE3 | the epic's success measures each addressed | **pass** | Five measures, five demonstrations, all run during this review — below |
| DE4 | `docs/product/` reflects what was built, not what was proposed | **pass, after one fix** | `vision.md` v8 already carried the second acceptance. Its "What it is for" section still opened "Today that means a rule file named on the command line with `--rules PATH`", which was true before WI-0004 and is a sentence a later reader would quote as the whole truth. Rewritten to state what a run does — it finds the rule file itself, `--rules` overrides — with the history after it. `vision.md` is now **v9** |
| DE5 | open questions across all children closed, or re-filed against a follow-up | **pass** | No question anywhere in the engagement is `open`; `engagement-state` reports the same, and it is the condition it tests for rest |
| DE6 | every claim in `docs/` about behaviour this epic delivered checked against the code during this epic; every citation resolves | **pass** | The audit table in `## What I examined` — five absolute claims and two smaller ones, each decided by opening what it cites. Mechanical half: `scripts/lint-claims` over the whole tree → 0 errors, 0 warnings; `validate-workspace` → 0 errors, 0 warnings |
| DE7 | the stakeholder was asked whether they accept the engagement, after rest, and answered | **pass** | `check-epic-signoff EP-001` → PASS. `Q-006` was filed at 15:44:36Z, after rest at 15:41:23Z, and answered at 16:24:37Z: *"A — ship it, we're done. Ten for ten, close it out."* This is the second sign-off of the engagement; the first, `Q-005`, accepted the nine items that existed then |

### DE3 in full — the five success measures, demonstrated

All five were run against a fresh six-entry sample folder during this review. `S` holds
`budget.csv`, `holiday.jpg`, `notes.txt`, `report.pdf`, `taxes.pdf` (mtime 2023-01-05, so it is
the one old file) and a pre-existing subfolder `keepme/`.

**1 — "preview prints one line per file naming the file and the destination, and the folder is
unchanged afterwards."** Met.

```
$ python3 -m tidy S
tidy: preview only - nothing will be moved. Re-run with --apply to move.
move   budget.csv -> recent/spreadsheets/budget.csv
move   holiday.jpg -> recent/images/holiday.jpg
move   notes.txt -> recent/documents/notes.txt
move   report.pdf -> recent/documents/report.pdf
move   taxes.pdf -> old/documents/taxes.pdf
```

`find` before and after, diffed: identical. Exit 0.

**2 — "the real run produces exactly the destinations the preview named, and no file present
before is absent after."** Met. `--apply` on the same folder printed stdout **byte-for-byte
identical** to the preview's (`diff` of the two captures: no output), and the tree afterwards is
those five destinations plus `keepme/inside.txt` untouched. Every one of the six filenames present
before the run is present after it — checked by walking the tree, not by reading the log.

**3 — "no file is ever overwritten; the incoming file is moved under a suffixed name and both
modes report it."** Met, with the check the measure itself prescribes — two files of the same name
and kind:

```
move   report.pdf -> recent/documents/report (2).pdf   [recent/documents/report.pdf exists]
```

printed by the preview and again by the apply. Afterwards the pre-existing file still contains
`ORIGINAL-CONTENT-DO-NOT-LOSE` and the incoming one is beside it as `report (2).pdf`.

**4 — "changing the rules changes where files land, without editing the tool's source, and the
difference is visible in the preview."** Met, and now without a flag at all. The same folder, twice,
with no `--rules` either time:

```
$ HOME=<empty> XDG_CONFIG_HOME=<empty> python3 -m tidy F
move   budget.csv -> recent/spreadsheets/budget.csv
move   taxes.pdf -> old/documents/taxes.pdf

$ XDG_CONFIG_HOME=<cfg> python3 -m tidy F
tidy: using rules from <cfg>/tidy/rules.ini
move   budget.csv -> fresh/data/budget.csv
move   taxes.pdf -> archive/documents/taxes.pdf
```

`git status --porcelain tidy/` → empty between the two runs: nothing in the tool changed, only the
user's file. This is the measure WI-0004 was asked for, and it is the one the stakeholder named.

**5 — "a person who did not write the tool can run it against a folder and, from its output alone,
say where each file went and why."** Met, as far as a reviewer can judge a measure phrased about
another person. Each line carries the file, the destination path, and the reason legibly encoded in
that path — `old/` versus `recent/` for age, the type folder inside it — with a bracketed
`[... exists]` on the one case where the destination was not the obvious one, and a first line
naming the rule file whenever an unnamed one shaped the run. What the output does **not** say is
which rule matched a file that took a built-in default; a reader infers that from the destination.
Recorded under `## Accepted gaps` rather than claimed as complete.

### The other gates

| gate | result | evidence |
|---|---|---|
| `definition-of-done` | **pass** | the DE1–DE7 table above |
| `epic-sign-off` | **pass** | `check-epic-signoff EP-001` → PASS, exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → 11 items, 16 documents, 0 errors, 0 warnings |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → 0 errors (nothing changed against the trunk, since this execution commits to it); `lint-claims` over the whole tree → 0 errors, 0 warnings |
| `record-is-reconstructible` | **pass** | answered below |
| `tests-pass-on-the-merge-result` | **pass, on the trunk itself** | `python3 -m unittest discover -s tests -t . -q` → **Ran 203 tests, OK**, exit 0. There is no merge to test: an epic has no branch, and all ten children were merged under their own IDs. Run anyway, because DE3 asserts behaviour |
| `verification-postdates-the-code` | **skipped** | no branch and no code on this item; each child ran it at its own close |
| `commits-reference-the-item` | **skipped** | same reason — there is no `main..branch` range for an epic |

### `record-is-reconstructible`, answered from the tracker, `docs/` and `git log` alone

- **What was built and why.** `docs/product/vision.md` v9 and `EP-001/item.md` `## Goal`: a folder
  is sorted into `<band>/<type>/` subfolders, previewed before anything moves, by rules the user
  owns. Four work items and six bugs, each with its own `plan.md`, `impl-report.md` and
  `verify-report.md`.
- **Which skill decided what.** Fourteen ADRs, each stamped with the skill and item that wrote it;
  every item's `journal.md` names its persona per entry; `history.md` names the actor on every row.
  The one decision reversed mid-engagement — no default rule-file location — is traceable end to
  end: `ADR-0010` decided it, `EP-001/Q-005` authorised reversing it, `ADR-0014` superseded the half
  that changed and left the format half alone, and `ADR-0014` v2 records that its most contested
  point later became the stakeholder's rather than the team's.
- **What questions arose and how they were resolved.** Sixteen question files, all `answered`, each
  with `## Consequences` naming the files its answer reached.
- **What verification found.** Ten `verify-report.md` files, and six of the ten children are bugs
  the pipeline filed against its own delivered work — which is itself the answer: verification
  found real defects and they were fixed under their own IDs rather than quietly.

## Findings

**None that block the ending.** One was fixed during the review rather than recorded, one is a
limit of what a reviewer can assert, and one is a note for whoever picks this up next.

1. **Fixed here: `vision.md`'s "Today that means…".** Under DE4, above. The sentence was not false,
   but it framed the flag as the whole story and a later skill re-quoting it would have described a
   tool that stopped existing when WI-0004 landed. That is the exact failure mode DE6 was written
   for, so it was fixed rather than noted.
2. **Success measure 5 is judged, not measured.** It is about what a person who did not build the
   tool can infer. I can show the output is self-describing; I cannot stand in for that person.
   Recorded as met with that limit stated, not as demonstrated.
3. **The scratch folder used for the DE3 runs is under `.harness/`,** which is
   git-ignored, so the runs above are reproducible from the commands but their outputs are not
   committed artifacts. The commands are in this file so that anyone can repeat them.

## Accepted gaps

Both were put to the stakeholder in `Q-006` and both were declined by name, so they are accepted
with their authority rather than the reviewer's.

- **`--rules ""` ends the run with a message naming no path** — `tidy:  cannot be used: No such
  file or directory`, exit 2, with a double space where the path would be. A consequence of
  ADR-0014 point 3 making the flag win by being *given*; nobody asked for it and no criterion
  covers it. Offered as a follow-up and refused. Recorded in `WI-0004/item.md`, in
  `EP-001/item.md`'s out-of-scope list, and in `vision.md`.
- **A broken rule file at the default location stops every run until it is fixed** rather than
  falling back to the built-in tables. `refine` flagged this as the assumption most worth
  revisiting; the alternative was offered in the stakeholder's own terms and they kept the current
  behaviour — *"if I typo my own rules file that's on me to fix, I'd rather it stop and tell me
  than guess"*. `ADR-0014` v2 records that its point 4 is now authorised rather than assumed.

Two further things were declined at the **first** sign-off and stay out: recursion into subfolders,
and undo. Both are in `EP-001`'s `## Out of scope` and in `vision.md`'s "What it deliberately is
not", each citing `EP-001/Q-005`.

## Verdict

**Accepted. The engagement ends at E1 — `delivered`.**

Every one of the seven epic Definition of Done criteria passes; all ten children are terminal and
every one of them delivered; the five success measures were demonstrated by running the tool during
this review rather than quoted; and the stakeholder was asked after rest and answered *"A — ship
it, we're done. Ten for ten, close it out."*

`EP-001` goes `open → done` with `outcome: delivered`. Nothing further is built. Anything wanted
later starts as a new request under `tracker/requests/`, which is the channel that does not need
anyone to ask first.

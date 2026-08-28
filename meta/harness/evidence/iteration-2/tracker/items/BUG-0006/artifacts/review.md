# Review — BUG-0006

## What I examined

**The record**, in full: `item.md`, all five rows of `history.md`, all five entries of
`journal.md` (from `review-close`'s filing entry of 2026-08-27T21:18:25Z through `verify`'s of
2026-08-28T14:05:49Z), `plan.md`, `impl-report.md`, `verify-report.md`. The item has no
`questions/` directory: none was ever filed on it.

**The change**, as a diff rather than as a description — `git diff main..wi/BUG-0006 -- docs/`,
read hunk by hunk. Seven hunks, and each one traces:

| hunk | serves |
|---|---|
| ADR-0008 frontmatter `version: 2 → 3`, `updated`, `updated-by`, `updated-for` | plan step 2; `spec/doc-header.md` §3; AC3 |
| ADR-0008 line 48, `[src: tidy/cli.py:52]` → `[src: tidy/cli.py]` | plan step 1; AC1 |
| ADR-0008 change-log row 3 | plan step 2; §3; AC3 |
| ADR-0009 frontmatter `version: 2 → 3` and the same three fields | plan step 4; §3 |
| ADR-0009 line 23, `tidy/cli.py:67` → `tidy/cli.py`, the other three citations in the group untouched and in order | plan step 3; AC2 |
| ADR-0009 line 106, `tidy/cli.py:93` → `tidy/cli.py` | plan step 3; AC2 |
| ADR-0009 change-log row 3 | plan step 4; §3 |

Nothing else is in the diff under `docs/`. No prose is reworded; no file under `tidy/` or
`tests/` appears; `git diff main..wi/BUG-0006 -- docs/architecture/overview.md` is empty, which
plan step 6 requires and which is right — no module, boundary or interface moved.

**The code behind every claim the change re-asserted.** `tidy/cli.py` read in full (114 lines),
`tidy/planner.py:55-80` for the guard ADR-0009 decides, `docs/architecture/adr/ADR-0012` and
`README.md:35-40` for what this project has already settled about exit status. The D12 audit
below is from those readings, not from the sentences.

**The trial merge**: a detached worktree at `main`, `merge --no-ff wi/BUG-0006` → `4c5d958`,
`python3 -m unittest discover -s tests -t . -q` and `python3 -m compileall -q tidy tests` run
inside it, and AC2's sweep re-run on the merge result. Worktree removed; `git rev-parse main`
returned `828a63a5c20a06703f14d41028e0e9ce8d7f7326` both before and after.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c "^- \[x\] AC" item.md` → 4; `grep -c "^- \[ \] AC" item.md` → 0 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | The `## Criteria` table gives each AC a command and its quoted output: AC1 `sed -n '48p' … \| grep -o "src: [^];]*"` → `src: tidy/cli.py` plus `grep -n "build_parser\|parse_args" tidy/cli.py` → `20:` and `62:`; AC2 the sweep → exit 1, no output; AC3 `head -8` → `version: 3` … `updated-for: BUG-0006` plus `git show f459e72:…` → `version: 1`; AC4 both commands with their real output. None cites `impl-report.md` |
| D3 | the item's gates passed on the **final** state of the code | **pass** | The last commit touching `docs/` or `tidy/` is `971f1cc`; everything after it (`d8e293f`, `6401023`, `8564d44`) is `tracker/` only, confirmed by `git show --name-only`. Verification ran at `6401023`, after `971f1cc`. This review re-ran the suite and the lint on the **merge result** `4c5d958`: `Ran 158 tests in 0.165s`, `OK`, exit 0; `compileall` exit 0 |
| D4 | no open blocking question on the item | **pass** | `tracker/items/BUG-0006/questions/` does not exist; no question was filed on this item at any point |
| D5 | a journal entry per skill execution, and `history.md` chains to the current status | **pass** | Five history rows, chaining `— → ready → planned → in-progress → verifying → in-review`, each `from` equal to the previous `to`, and the last `to` equal to `item.md`'s `status`. Five journal entries, one per row: `review-close` 21:18:25Z, `plan` 13:55:32Z, `implement` 13:57:36Z, `implement` 14:00:38Z, `verify` 14:05:49Z. No orphan entry and no unentried row |
| D6 | every design-changing decision is in an ADR, cited from the plan or journal | **pass** | One decision — whether to repoint the three citations or drop their line numbers — recorded as **ADR-0013**, with four options costed. Cited from `plan.md` `## Decisions and ADRs`, from `plan`'s journal entry, and from both change-log rows this change added ("Per ADR-0013"). It generalises the rule ADR-0009 v2 recorded for one document; ADR-0009 is not superseded, because ADR-0013 extends its rule rather than reversing its decision |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass** | Both changed documents: ADR-0008 and ADR-0009 each to `version: 3`, each with a row whose `version` equals the frontmatter's, newest first, and whose `what changed` names the section, the form and the reason rather than saying "updated". §3 checked clause by clause on both. `overview.md` correctly not bumped — a bump with nothing behind it devalues every other one |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs BUG-0006 wi/BUG-0006` → `all 4 commit(s) on main..wi/BUG-0006 name BUG-0006`, exit 0 |
| D9 | merged into the trunk | **pass** | Merged after this review closed the item, per the skill's required order. Trial merge first: `4c5d958`, tests green on the merge result |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness BUG-0006 wi/BUG-0006` → exit 0. Checked rather than accepted: the branch head `8564d441` is later than the `Verified-commit: 64010239`, and `git show --name-only 8564d44` lists five files, **all under `tracker/`** — `board.md`, `verify-report.md`, `history.md`, `item.md`, `journal.md`. Nothing under `docs/`, which on this item is the deliverable. The verification covers the delivered state exactly |
| D11 | `review.md` exists and states what was examined | **pass** | This document; `## What I examined` is first and names the artifacts, the seven diff hunks, the code read, and the trial merge |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, read against the code | **pass** | Five claims audited from their citations, below. Automated half: `lint-claims --changed-since main` → `checked 2 document(s)`, `0 errors, 0 warnings`, exit 0 |

### D12 — the claims, audited by opening what they cite

This item re-asserted three sentences by re-pointing their citations, so all three were opened
against `tidy/cli.py` rather than judged from the prose or from the reports.

1. **ADR-0008:48** — "under WI-0003 the tables in force are the *user's*, and `build_parser` runs
   before `parse_args` has told anyone where the user's rules came from" `[src: tidy/cli.py]`.
   **True.** `build_parser` (`tidy/cli.py:20-48`) composes the whole `epilog` as a string literal,
   including the sentence about `--rules PATH`, and `--rules` is only *declared* there; its value
   is first read at `args.rules` on line 71, nine lines after `parse_args` returns on line 62.
   Nothing in `build_parser` can know the rules path. `grep -n "parse_args" tidy/cli.py` → one hit.
2. **ADR-0009:23** — the dangling symlink raising out of `build_plan` into `cli.py`'s
   `except OSError`, "where ADR-0006's handler reports the *target folder* as unreadable and exits
   2" `[… src: tidy/cli.py; src: ADR-0006]`. **True as what it is.** The handler is at
   `tidy/cli.py:88-90` and does exactly that. The sentence sits in `## Context`, which
   `spec/doc-header.md` §4 defines as "what forced a decision — the constraints that were actually
   in play", in the past tense; it describes the defect BUG-0004 fixed, and the fix is visible at
   `tidy/planner.py:62-68`, whose comment names ADR-0009 and BUG-0004. A Context that stopped being
   a true description of the *present* is the record working, not failing.
3. **ADR-0009:106** — "only a `"failed"` outcome from `apply_plan` makes the process exit non-zero"
   `[src: ADR-0007; src: tidy/cli.py]`. **True in its paragraph; see `## Findings` for the caveat.**
   `tidy/cli.py:114` is the module's last statement and its only `return 1`, and it is exactly
   `return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0`.
   `grep -n '"failed"' tidy/cli.py` → one hit, that line.
4. **ADR-0008's two `run:` citations still reproduce**, which matters because ADR-0008 v2 was
   written specifically to make them checks rather than snapshots.
   `grep -rn "epilog\|description=" tidy tests --include=*.py` → exit 0, two hits, both
   `tidy/cli.py` (lines 23 and 25) — the citation says "exit 0, two hits, both `tidy/cli.py`".
   `grep -nE "^(from|import).*\brules\b" tidy/cli.py` → exit 1, no output — the citation says
   "exit 1, no". Both exact.
5. **ADR-0009's three `run:` citations are dated observations of the defect**, all in `## Context`
   or in an option's cost, all naming `/tmp/bug4` fixtures from BUG-0004's investigation. They are
   not reproducible today by design: the behaviour they record is the behaviour BUG-0004 removed.
   This is the distinction ADR-0008 v2 drew in its own `## Consequences` — "cite an absolute claim
   with a command that tests it, not with one whose output happened to be true on the day it was
   run" — and the two documents fall on the two sides of it correctly.

## Findings

**One, examined and not actioned.**

`ADR-0009:106`'s clause — "only a `"failed"` outcome from `apply_plan` makes the process exit
non-zero" — is true within its paragraph and false if quoted out of it. `tidy/cli.py` returns 2 at
lines 76, 80 and 90, and none of those is a `"failed"` outcome. The paragraph supplies the scope
in its next sentence ("A run over a folder with one unexaminable entry and one ordinary file exits
**0**, in both modes"), the same document describes exit 2 for an unreadable folder twenty lines
earlier, and **ADR-0012** — `status: current`, written for BUG-0005 — is this project's authority
on the subject and is unambiguous: three statuses, 2 for the four ways a run cannot start, 1 for
the `"failed"` predicate, and it cites ADR-0009 by name in its own list of what it does not
disturb. `README.md:35-40` states all three plainly.

Not actioned, for three reasons, and none of them is that it looked minor:

- **No criterion of this item covers it.** AC1 is ADR-0008 only; AC2 is about `path:line`
  citations, and there is no longer one there. The item's `## Out of scope` names "rewording any
  claim in ADR-0008 or ADR-0009" explicitly.
- **This item did not introduce it or make it worse.** The clause is ADR-0009 v1 prose from
  2026-08-27T20:45:46Z. What changed here is its citation, from a line number that pointed at a
  blank line to the file that contains the statement — strictly an improvement in a reader's
  ability to check it.
- **It is not a defect.** The named risk — someone quoting the clause alone into a new document,
  which is precisely the seven-document propagation D12 exists for — is real but is already
  guarded: ADR-0012 is current, cites ADR-0009, and settles the question in the place a reader
  looking for exit statuses will go. Filing a bug for an elliptical subordinate clause that the
  project's own authoritative record already disambiguates would be manufacturing work.

Recorded in the item's `## Notes` so that it survives the closing of this item, which is where an
accepted finding otherwise goes to die.

**Nothing else.** No hunk is unrequested. No hunk contradicts an ADR — the change *implements*
ADR-0013 and, as a side effect worth noting, makes ADR-0009's own `## Consequences` bullet ("The
citations in this record name files and symbols, not line numbers") true of the whole document for
the first time; at v2 it was written while two `tidy/cli.py:NN` citations remained.

## Accepted gaps

Each was declared upstream, and each is judged here rather than inherited. All are written into
the item's `## Notes` or already live in a document that outlives the item.

1. **Nothing enforces ADR-0013.** `lint-claims` cannot distinguish `[src: path]` from
   `[src: path:line]`, so a future document may reintroduce the drifting form and no gate will
   object. Declared by `implement` and by `verify`, and confirmed here: `lint-claims .` exits 0
   both on `main` (three citations pointing at wrong lines) and on this branch (none). **Accepted**
   — the durable record is ADR-0013 `## Consequences`, which is in `docs/` and outlives every item.
   A gate would live in `.claude/agile-skills/scripts/`, which is the toolkit running this project
   and not part of EP-001.
2. **AC2 is a point-in-time property.** It holds at the merge commit and nothing keeps it holding.
   Same remedy as gap 1, and the same record. **Accepted.**
3. **`verify` did not check every `run:` citation in `docs/` still reproduces.** **Closed here
   rather than accepted**, for the scope D12 actually asks about: both `run:` citations in ADR-0008
   were re-run above and reproduce exactly, and ADR-0009's three are historical by construction.
   Citations in documents this item did not touch remain unchecked, which is what D12's deliberate
   scoping ("the behaviour *this item touched*") means and not a gap in this item.
4. **BUG-0006's own `## Steps to reproduce` and `## Actual behaviour` no longer reproduce.** They
   say `tidy/cli.py:52` is blank and the statement is at `:54`; on `main` line 52 is
   `    """The stdout line for one action."""` and the statement is at `:62`. Predicted by the
   plan's `## Risks`, quoted correctly by `implement` and `verify`, and **not corrected** — that
   text is the filing record of what `review-close` saw on 2026-08-27, and rewriting it would erase
   the evidence rather than update it. **Accepted**, with a `## Notes` line pointing a later reader
   at the discrepancy so they do not conclude the item was filed carelessly.

## Verdict

**Accept, merge and close. Outcome: delivered.**

All twelve Definition of Done criteria pass, each with its own evidence above. The change is seven
hunks in two documents, every one of which traces to a plan step or to a `spec/doc-header.md` §3
obligation; it reworded nothing, touched no code, and left the suite at 158 passing on the merge
result.

The two departures `verify` flagged for this review were the reason to read it closely, and both
are upheld:

- **AC2's "the latter two are exact and must stay so" is not honoured, and that is correct.**
  Verified independently of the reports: BUG-0006 was filed at `f459e72` (2026-08-28T00:18:34+03:00)
  and WI-0003 merged at `82a7d26` fifty-seven minutes later, moving both cited lines. "Stay so" is a
  preservation instruction, and the property was already destroyed before this item's branch
  existed — no execution could have obeyed it, only reversed it. The authority for choosing not to
  reverse it is **ADR-0013**, an architectural decision recorded before any edit, and reading it as
  governing the *remedy* rather than as amending the criterion is what the item's own `## Expected
  behaviour` invites: "Whether that is the right remedy … is for `plan`." The criterion's operative
  sentence is met, and met more durably than repointing would have achieved — the same repointing
  was performed for this document nineteen hours earlier and drifted again on the next merge.
- **AC3's literal "`version: 2`" is unsatisfiable and was rightly read as "the version bump".**
  `git show f459e72:…ADR-0008….md \| sed -n '3p'` → `version: 1`. Setting `version: 2` today would
  violate the `spec/doc-header.md` §3 that AC3's own sentence invokes, since 2 → 2 is not a bump.

Both departures were recorded loudly at every stage — in `plan`'s ADR, in the implementation
report's `## Deviations`, in the verification report's `## The two stale premises`, and in two
history reasons — rather than smoothed over. That is the behaviour the record exists to produce,
and it is the reason this review could check them in minutes instead of rediscovering them.

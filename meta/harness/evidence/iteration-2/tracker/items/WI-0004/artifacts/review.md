# Review — WI-0004

## What I examined

- **`item.md`** — the ten criteria, their tick state, `## Out of scope`, and the whole of
  `## Notes` including both refinement rounds and the R10 table's two rows routed to `plan`.
- **`history.md`** — all eight rows, checked for a gap and against `item.md`'s status.
- **`journal.md`** — read in full, all eight entries: `answer-questions` ×2, `refine` ×2, `plan`,
  `implement` ×2, `verify`. I am certifying the record is complete, which cannot be done from a
  skim.
- **`plan.md`** — the eight steps, the AC mapping, assumptions A1–A4, and the four risks; used as
  the standard for step 4's hunk-by-hunk read and for judging the declared deviations.
- **`impl-report.md`** and **`verify-report.md`**, including `## What I did not do` and
  `## Not verified, and why` in full.
- **`questions/Q-001.md`** — `status: answered`, `addressed-to: human`, and its `## Consequences`
  naming `item.md`, `refinement-qa.md`, `docs/product/vision.md` (v5 → v6), `history.md` and
  `journal.md`. I opened each and each carries the answer.
- **The diff, `main..wi/WI-0004`, hunk by hunk** — `git diff main..wi/WI-0004 -- tidy/` read in
  full; `--stat` over `tests/` and `README.md`; and, for AC2's contested clause,
  `git diff main..HEAD -- tests/<file> | grep '^-'` on each test module.
- **`docs/architecture/adr/ADR-0010`, `ADR-0011`, `ADR-0014`** — for the supersession and for
  whether any hunk contradicts a recorded decision.
- **`docs/architecture/overview.md` and `docs/product/vision.md`** — for D7 and D12, read against
  the code rather than against each other.
- **The merge result**, in a detached worktree, with the project's own test and lint commands.

**The D12 claim audit, from the citations rather than from the prose.** Each claim below was
decided by opening what it cites, not by reading the sentence or a neighbouring document:

| claim | what I opened | verdict |
|-------|---------------|---------|
| `overview.md`: "`ruleset_file.py` … Also `default_path(environ)` and `resolve(argument, environ)`, which decide *which* file a run reads" [src: ADR-0014] | `tidy/ruleset_file.py` | **true** — both functions exist with those signatures and that division of labour |
| `overview.md`: "a run with no `--rules` reads `$XDG_CONFIG_HOME/tidy/rules.ini`, or `$HOME/.config/tidy/rules.ini`, and names on stderr whichever rule file it used" | `tidy/ruleset_file.py`, `tidy/cli.py`, and the verification's live transcripts | **true** |
| `overview.md`: "a rule file sitting in the folder you were handed is not a rule source, and neither is a chain of places to look" | `resolve` — one path, and the target folder is never consulted | **true** |
| `overview.md`: "The loader is read *before* the target folder is examined" [src: tidy/cli.py] | `tidy/cli.py` — `resolve_rules(...)` precedes `os.path.isdir(folder)` | **true** |
| `overview.md`: "WI-0004 … **is planned and not yet built**" and the whole `## Where the remaining item will touch this` forecast | `git diff main..wi/WI-0004 -- tidy/` | **false once merged** — a D7/D12 finding. Fixed, see `## Findings` |
| `vision.md`: "a default location is wanted and **not yet built**"; "**What is left on WI-0004 is ours**: the criteria have to be rewritten … ADR-0010 has to be superseded" | `item.md` (criteria rewritten, all ticked), `ADR-0014`, `ADR-0010` (`status: superseded`) | **false** — all three were done. A D7/D12 finding. Fixed, see `## Findings` |
| `vision.md`: "A run **will** say which rule file it used" (future tense) | `tidy/cli.py` | the claim is true but the tense had gone stale. Fixed |
| `ADR-0010`'s header: superseded in part, format half still current | `tidy/ruleset_file.py` — `load` and its validation are unchanged by this branch | **true** |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion ticked | **pass** | `grep -c "^- \[x\] AC" item.md` → `10`; `grep -c "^- \[ \] AC"` → `0` |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | its `## Criteria` table has ten rows, each naming a command run in a subprocess and quoting its actual output. I spot-checked three against the artefacts: AC5's 22 runs, AC2's `git checkout main -- tests/` measurement, and AC4's `2>&1` ordering check |
| D3 | gates passed on the **final** state | **pass** | `implement`'s gates ran on `7aaa697` (the last code commit); `verify`'s on `aefa6d0`; mine on the merge result `ea1dc0b`. `python3 -m unittest discover -s tests -t . -q` → exit 0, `Ran 203 tests … OK`; `python3 -m compileall -q tidy tests` → exit 0 — both **inside the trial worktree**, not on the branch |
| D4 | no open blocking question | **pass** | `questions/Q-001.md` is the only question and is `status: answered` |
| D5 | a journal entry per execution, history chains | **pass** | history has 8 rows, `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review`, no gap, and its last row matches `item.md`. `journal.md` has 8 entries, one per row, each stamped with skill, version and persona |
| D6 | design decisions are in an ADR, cited | **pass** | **ADR-0014**, five numbered decision points, `Supersedes: ADR-0010 (in part)`; cited from `plan.md` `## Decisions and ADRs`, from both `implement` journal entries, and from the source docstrings. ADR-0010 carries `status: superseded`, `superseded-by: ADR-0014`, and a header note saying **which half** — the format half is explicitly still current, which the diff respects: `load` and its validation are untouched |
| D7 | invalidated documents updated, with a version bump and a change-log row | **pass, after this review made the updates** | Two documents were invalidated and neither had been updated — see `## Findings` finding 1. `docs/architecture/overview.md` v10 → v11 and `docs/product/vision.md` v6 → v7, each with a change-log row, committed as `58a03fc` |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, `all 7 commit(s) on main..wi/WI-0004 name WI-0004` |
| D9 | merged into the trunk | **pass** | merged after this record was written and the item closed, in the order step 8 requires |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness WI-0004 wi/WI-0004` → exit 0: *"verified at aefa6d01; wi/WI-0004 has moved to 8a28c3e4 but only the record changed (5 file(s) under tracker/ or docs/)"*. Confirmed independently: `git log main..wi/WI-0004 -- tidy/ tests/ README.md` ends at `7aaa697`, which precedes `aefa6d0` |
| D11 | `review.md` states what was examined | **pass** | this file; `## What I examined` is first and lists the artefacts, the diff range, and the eight claims audited with what was opened for each |
| D12 | claims in `docs/` about this behaviour are still true, from their citations | **pass, after finding 1 was fixed** | the eight-row audit table above. Six were true against the code; two were false and are corrected. `lint-claims --changed-since main` → exit 0, `checked 2 document(s) changed since main`, `0 errors, 0 warnings` |

## Findings

**1 — Two documents claimed this item was not yet built. Fixed in this review, not sent back.**
`docs/architecture/overview.md` line 123 read *"WI-0004 (a default location for the rule file) is
planned and not yet built"*, and `docs/product/vision.md` said the default location was *"wanted
and not yet built"* and that *"What is left on WI-0004 is ours: the criteria have to be rewritten
… and ADR-0010 has to be superseded"* — all of which the branch makes false. `impl-report.md`
declared the overview one and handed it to D7 and D12 explicitly, which is the right handling by
`implement`: updating it is not one of the plan's eight steps and no criterion names it, so making
the edit would have widened the item on the developer's own authority. It did **not** find the
vision one. I made both edits rather than sending the item back, because D7 and D12 are this
skill's gates, the fix is documentary rather than behavioural, and a send-back would cost a round
trip to change two paragraphs that only become false at the moment I merge. The overview's forecast
turned out to be exactly right — only `ruleset_file.py` and `cli.py` changed — so it became a
description rather than being rewritten.

**2 — The `--help` epilog says `~/.config/…` where the code reads `$HOME`. Accepted.** The tool
never calls `os.path.expanduser`; `default_path` reads `HOME` from the mapping, deliberately, so
that a run's behaviour is a function of its environment. `~` is the conventional shorthand for
exactly that and is what a reader of a help text expects, and `README.md` states the full rule
including the case where neither variable is set. The two would only diverge with `HOME` unset,
where `~` would resolve through the password database and the tool correctly consults nothing. Not
worth the words it would take to say precisely in a help epilog.

**3 — `--rules ""` changed from a silent no-rules run to exit 2. Accepted, and recorded.** See
`## Accepted gaps`.

**Nothing else.** Every hunk in `tidy/` traces to a plan step: the import swap and the `resolve`
call to step 3; the stderr line to step 3 and AC4; the `--rules` help and the epilog to step 4 and
AC10; the module docstring, the two constants, `default_path` and `resolve` to steps 1 and 2. No
hunk contradicts an ADR — ADR-0011's "`ruleset_file.py` is the only module that reads a rule file"
is upheld by putting the choice there rather than in `cli.py`, ADR-0006's exit-2 vocabulary is
reused rather than re-invented, and ADR-0001's standard-library-only, 3.9-floor constraint holds
(`os.path.join`, `os.path.lexists`, `dict.get`). The two deviations `implement` declared —
`run_interleaved` for AC4's cross-stream ordering, and AC5 reusing `test_cli.py`'s malformed table
— are both *how* and not *what*, both additive, and both correctly declared.

I would be comfortable maintaining this. The one thing I looked hardest at is `resolve`'s
`argument is not None`, which is the kind of one-character decision a later reader "corrects": its
docstring says why, in the imperative, and a test fails if it is changed. That is the right defence.

## Accepted gaps

Each is written somewhere that survives this item's closure. A gap recorded only in a report is a
gap nobody will read again.

1. **`--rules ""` now ends the run with exit 2, and its message names no path.** Before this item
   it was a silent no-rules run. It is in scope and correctly decided — `item.md` leaves it
   undefined, R10 routed it to `plan`, and ADR-0014 point 3 took it — and no criterion covers it,
   so it is not a send-back. I did not file a bug either: the engagement has already been signed
   off once, the behaviour is out of scope by this item's own words, and adding a child over
   something the stakeholder was never asked about would prolong an engagement they accepted.
   **Recorded in `item.md` `## Notes`** under "Accepted at review", with the poor message named as
   the part worth fixing if anyone picks it up, and **surfaced in `docs/product/vision.md` v7** so
   it reaches the stakeholder at sign-off rather than being decided for them.
2. **Plan assumptions A1 and A3 stand unexercised.** A relative `XDG_CONFIG_HOME` is used as given
   rather than ignored, and a rule file whose parent directory cannot be searched reads as absent
   rather than as present-but-unusable. Both are declared in `verify-report.md`
   `## Not verified, and why`, both are recorded in `plan.md` `## Assumptions` with what reversing
   them costs, and `plan.md` survives the item — this is where an assumption belongs.
3. **Only Linux was exercised, and `~` was never a real home directory.** Declared in
   `verify-report.md`. Nothing in the epic claims another platform, and the `HOME` branch is
   verified as a path computation over a mapping, which is precisely the design that makes it
   testable at all.

## Verdict

**Accept, and close as `delivered`.** All ten acceptance criteria are ticked and each is backed by
a command `verify` ran through the real command line rather than through the project's own test
helpers. The Definition of Done passes criterion by criterion, D7 and D12 after this review made
the two document corrections they exist to catch. The merge result — not the branch — passes the
project's tests and lint. Three gaps are accepted and each is recorded where it will still be read
after this item is closed.

# Review — WI-0001

## What I examined

- **`item.md`** — all eleven criteria and their tick state, `## Out of scope`, `## Notes`.
- **`history.md`** — eight rows, read for chaining and for whether each actor left an entry.
- **`journal.md`** — all ten entries, in full, from `intake` at 21:14:46 to `verify` at 22:10:05.
- **`artifacts/plan.md`**, **`artifacts/impl-report.md`**, **`artifacts/verify-report.md`** — the
  last two read as claims to be checked, not as evidence.
- **`questions/Q-001.md` to `Q-004.md`** — status, `## Consequences`, and `Q-004`'s `## Context`
  in full, because AC4's wording is the one contested thing in this item.
- **The diff `main..68cd5fb`, hunk by hunk** — `mdtab.py` read end to end (all 15 functions), not
  a summary of it; `tests/test_mdtab.py`; the 26 fixture files; `docs/architecture/overview.md`'s
  v1→v2 change.
- **`docs/architecture/adr/ADR-0003`** decisions 1–11 and **`ADR-0004`** decisions 1–3, against
  the code that implements them.
- **`docs/product/vision.md`** v3, including `## What is not yet decided`.

**Claims audited (D12) — each decided by opening what it cites, not by reading the sentence.**

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| *"One executable Python 3 file … no dependency outside the standard library"* [src: ADR-0001] | `overview.md` §The shape of the system | ADR-0001, then `mdtab.py`'s import block — `re`, `sys`, `unicodedata`, nothing else | **true** |
| *"There is no package, no build step and nothing to install"* [src: EP-001/Q-002] | same | the repository root: `ls setup.py pyproject.toml setup.cfg` → all three absent | **true** |
| *"Everything in the middle column is a copy. The tool's default is to do nothing"* [src: docs/product/vision.md] | `overview.md` §The shape of the system | `transform()` lines 261–300: every branch that is not a recognised table calls `out.append(line)` or copies the block whole | **true** |
| *"lets an arbitrary byte sequence round-trip through a `str` pipeline unchanged"* [src: WI-0001 AC6] | `overview.md` §Why bytes at the edges | AC6 itself, then `main()` — `decode(ENCODING, errors=ERRORS)` / `encode(ENCODING, errors=ERRORS)` with `ERRORS = "surrogateescape"`; and the verification's `md5sum` evidence | **true** |
| *"No package directory, no `setup.py` or `pyproject.toml`, no entry-point script, no configuration file, no logging, and no reading or writing of files by path"* [src: EP-001/Q-002] | `overview.md` §What the shape does not include | the tree, and `grep -nE '\bopen\(\|logging\|argparse\|import ' mdtab.py` → only the three stdlib imports; no `open(`, no `logging`, no `argparse` | **true** |
| *"`tests/` — `test_mdtab.py`, one `unittest` method per acceptance criterion, named for it"* [src: docs/architecture/overview.md] | `overview.md` §Layout | `tests/` — one module; its methods enumerated. This sentence was **wrong at v1** ("one per group of acceptance criteria") and `implement` repaired it under D12; the repair is correct | **true** |
| ADR-0003 decisions 7, 8, 9, 10, 11 | ADR-0003 §Decision | `display_width`, `column_widths`, `compose_row`, `compose_delimiter`, `emit_block` line by line | **true** — each decision has a function that implements it and nothing implements a rule the ADR does not state |
| ADR-0004 decisions 1–3 | ADR-0004 §Decision | `compose_delimiter` (colons kept at the ends they arrived at, `width + 2` characters, no spaces) and `column_widths`' two-colon minimum | **true** |
| *"the appearance of a delimiter row that carries **no** marker is settled"* [src: WI-0001/Q-004] | `vision.md` §What is not yet decided | `Q-004`'s `## Context` verbatim: *"What is being asked here is only the appearance of a delimiter row that carries no marker at all"* | **true**, and it is what makes AC4's scoping legitimate rather than convenient |

No claim was accepted from a neighbouring document repeating it, and no claim was accepted from
memory of having written it.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c '^- \[x\] AC' item.md` → 11, and the item declares AC1 to AC11 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | its criteria table has eleven rows, each with a command and quoted actual output; spot-checked AC2 (`[0, 9, 17, 24]` on all four rows), AC6 (`md5sum` pair `2b51efba…`) and AC9 (22 inputs `idempotent`) against the report's own text |
| D3 | declared gates passed on the **final** state of the code | **pass** | `implement`'s eight gates ran at `e2beac6`, the last code commit; `verify` re-ran tests, lint and the validator at `c1c79dc`; this review re-ran the suite on the **merge result** in a detached worktree — `Ran 14 tests ... OK`, exit 0 — plus `compileall` exit 0 there |
| D4 | no open blocking question | **pass** | `Q-001`–`Q-004` all `status: answered`, each with a `## Consequences` section; `next` found no question at `status: open` anywhere |
| D5 | a journal entry per execution, history chains to the current status | **pass** | history: `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review`, every row's `from` equal to the previous `to`, last row `to: in-review` equal to `item.md`'s status. Ten journal entries cover eight transitions plus two non-transitioning executions (`intake`'s second entry, and `answer-questions` at 21:25 propagating an EP-001 answer into this item) |
| D6 | design decisions in an ADR, cited from plan or journal | **pass** | ADR-0003 and ADR-0004 are both cited in `plan.md`'s `## Decisions and ADRs` table with their route. The decisions `implement` took (test ordering, the fixture rename, two extra fixtures) are reversible one-file choices inside the plan's latitude, recorded in the journal and `impl-report.md`, and correctly did **not** become ADRs |
| D7 | invalidated documents updated, with a version bump and a change-log row | **pass** | `overview.md` v1 → v2, frontmatter `updated`/`updated-by: implement`/`updated-for: WI-0001`, and a change-log row naming what changed. It is the only document this change invalidated; ADR-0003 and ADR-0004 describe rules the code implements rather than the code itself, and both remain true |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 9 commit(s) on main..wi/WI-0001 name WI-0001" |
| D9 | merged into the trunk | **pass** | trial-merged `--no-ff` into a **detached** worktree at `main` first (trial head `cad9b3b`); `git rev-parse main` returned `ac16080` before and after, so the trunk did not move; the real merge follows this close, in that order, because `commits-reference-the-item` inspects a range that merging first would empty |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: *"verified at c1c79dc2; wi/WI-0001 has moved to 68cd5fbd but only the record changed (5 file(s) under tracker/ or docs/)"*. Confirmed independently with `git log --name-only c1c79dc..HEAD` — the single intervening commit touches `tracker/` only |
| D11 | `review.md` exists and states what was examined | **pass** | this file; `## What I examined` is first and lists the artifacts, the diff range and the claims audited |
| D12 | claims in `docs/` about the touched behaviour are still true; absolute claims this execution wrote resolve | **pass** | the nine-row audit above, each decided by opening the cited source. Automated half: `lint-claims --context work-item --changed-since main` → exit 0 over *"1 document(s) in 1 path(s) differ from main"* — a scope that contained this item's only `docs/` change, not an empty one |

## Findings

1. **AC4, read alone, does not describe this code — and that is correct.** A delimiter cell
   written `:---:` comes back with its colons. I checked this rather than took it on trust, and
   the resolution is in the record in four independent places: the item's own `## Out of scope`
   (*"AC4's hyphen rule describes a delimiter cell that carries no marker"*), ADR-0003 decision
   10, ADR-0004, and — decisively — `Q-004`'s `## Context`, which put the question to the
   stakeholder as *"only the appearance of a delimiter row that carries no marker at all"*. The
   code does not contradict an ADR, so no question was filed and nothing is superseded. AC4's
   actual subject, the markerless row and the narrowing rule, was verified on its own inputs and
   passes on its own terms. **No action.**
2. **`table_or_none`'s signature differs from the plan's.** `plan.md` wrote
   `table_or_none(block) -> Table | None`; the code takes the row bodies and returns a list of
   cell lists. The plan's own `## Approach` says *"the bodies are the developer's"*, and no
   behaviour differs. Worth naming so a reader comparing the two does not think something was
   skipped. **No action.**
3. **Four functions are not named in the plan** — `strip_terminator`, `_is_escaped`,
   `emit_block`, `transform`. Each is demanded by prose in the same section of the plan (the
   inverse of `split_lines`; *"not preceded by an odd number of backslashes"*; *"a single
   left-to-right scan"*; the block-emission rules). **Not unrequested scope.**
4. **No hunk in the diff serves neither a criterion nor a plan step.** Checked hunk by hunk:
   `mdtab.py` and `tests/test_mdtab.py` are plan steps 1–9, the 26 fixtures are step 8,
   `tests/__init__.py` is the plan's `## Scaffolding`, `overview.md` is the declared D12 repair,
   and the remainder is this item's own tracker record. There is no argument parsing, no file I/O
   by path, no configuration and no logging — each of which the item's `## Out of scope` forbids
   and each of which I checked for by grep rather than by reading the summary.
5. **Would I maintain this?** Yes. The one construct worth flagging for a future reader is
   `transform`'s `flush()` closure, which empties the block with `del block[:]` rather than
   rebinding, because rebinding would need `nonlocal`. It is correct and it is three lines, but it
   is the one place in the file where the mechanism is not obvious from the shape. Not a defect
   and not worth a change. Everything else — one function per rule, each carrying the ADR decision
   it implements in its docstring — is the shape I would want to come back to.

**No defect was found in this item, and none in behaviour delivered by another item.** No bug was
filed and no send-back was made.

## Accepted gaps

Each was declared upstream, judged acceptable here, and **written into the item's `## Notes`** so
that it survives the close — a gap that exists only in a report of a closed item is a gap nobody
will read again.

| gap | declared in | why acceptable |
|-----|-------------|----------------|
| column alignment inside a document that is not valid UTF-8 may be wrong | `verify-report.md`, `plan.md` `## Risks` | only the columns are affected; the byte-for-byte promise was verified and holds. No criterion covers it |
| display width approximates a terminal rather than measuring one | both reports | the stakeholder accepted it in advance [src: WI-0001/Q-001], and nothing here can check a real terminal |
| a pipe table inside an *indented* code block is tidied | `verify-report.md` | already in the item's `## Out of scope` [src: ADR-0003] decision 2; repeated in `## Notes` so it is not filed as a bug later |
| performance on a large document unmeasured | `verify-report.md` | no criterion mentions it |
| the vision's second product property — cell text placed by the alignment markers — is not delivered here | this review | **WI-0002 delivers it**; its AC1 to AC3 are exactly that sentence, and `vision.md` `## What is not yet decided` already names it. The follow-up item exists and depends on this one |
| the toolkit's `validate-workspace` and `lint-claims` crash on a non-UTF-8 `*.md` file | `impl-report.md`, `verify-report.md` | not a defect in any item — no item owns the pipeline's scripts, so no `bug` could carry a valid `found-in`. Worked around by naming the fixture `not_utf8.markdown`; recorded in `## Notes` so the next person does not rename it back |

## Verdict

**Accept.** All twelve Definition of Done criteria pass with their own evidence. The change does
what WI-0001 asked for, the record reconstructs without gaps, and the tests pass on the merge
result rather than only on the branch. Merging into `main` and closing as `delivered`.

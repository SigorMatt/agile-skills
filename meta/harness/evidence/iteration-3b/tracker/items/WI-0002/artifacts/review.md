# Review — WI-0002

This is the **second** review of WI-0002. The first, at `2026-08-29T23:09:49Z`, rejected the item on
D7 and D12 and sent it back to `in-progress`; that verdict is preserved verbatim under
`## The first review's verdict, and whether it was met`. The code was not in question then and is
not now.

## What I examined

**Artifacts, read in full:** `item.md` (all ten criteria and the `## Notes`), `history.md` (13 rows),
`journal.md` (all 15 entries, `21:15:02Z` through `23:34:38Z`), `artifacts/plan.md`,
`artifacts/impl-report.md` including both executions' sections, `artifacts/verify-report.md` (the
second verification, at `e533928`), `questions/Q-001.md` and `questions/Q-002.md`, and
`tracker/items/WI-0001/item.md` for the eleven criteria AC9 re-reads.

**Diff read hunk by hunk**, range `main..wi/WI-0002` (`b4568fe..57e10f0`, 19 files):

| hunk | serves |
|------|--------|
| `mdtab.py` — module docstring gains ADR-0005, and the ADR-0004 filename is corrected | plan step 4 |
| `mdtab.py` — `LEFT`/`RIGHT`/`CENTRE` constants and `column_alignments(rows)` at line 220 | plan step 1; ADR-0005 decision 1 |
| `mdtab.py` — `compose_row` gains `alignments` and splits `pad` by the marker (line 244) | plan step 2; ADR-0005 decisions 1–4; AC1, AC2, AC3, AC4 |
| `mdtab.py` — `emit_block` computes alignments once and passes them through | plan step 3 |
| `tests/test_mdtab.py` — WI-0001's eleven methods renamed to the `wi0001_ac<n>_` tag, coverage tag changed | plan step 5; ADR-0006 |
| `tests/test_mdtab.py` — ten new `test_wi0002_ac<n>_` methods, module docstring, `INPUT_FIXTURES` | plan steps 8 and 6; impl-report Deviations 5 |
| `tests/fixtures/aligned{,_empty,_wide}.md` + `.expected.md` | plan step 6; AC1–AC6 |
| `tests/fixtures/markers.expected.md` — one line, three columns move | plan step 7; impl-report Deviations 1 |
| `docs/…/ADR-0005` v1→v3 — erratum plus three provenance corrections | the first review's verdict, items 1 and 2, via `Q-002` |
| `docs/…/ADR-0003` v2→v3 — one appended provenance correction row plus three sourced absolutes | the first review's verdict, item 2, via `Q-002` |
| `tracker/**` and `board.md` | the transitions and their records |

**No hunk serves neither a criterion nor a plan step.** `compose_delimiter` is untouched, which is
what plan step 3 promised and what AC7 depends on.

**Claims audited for D12 — each opened at what it cites, not read as prose.** The window
`lint-claims` examined is quoted under `## Definition of Done` D12; it is `2 document(s) in 2
path(s)`, which is non-empty and could have found something.

| claim | what I opened | verdict |
|-------|---------------|---------|
| `ADR-0005` `## Context`: *"which is what `compose_row` did when this ADR was written, before WI-0002 changed it"* [src: WI-0001 AC3] | `tracker/items/WI-0001/item.md` AC3 — *"…spaces padding it to the column's width, then one space"* | **true**; AC3 is indeed the rule that put all padding after the text |
| `ADR-0005` `## Corrections` erratum: *"`compose_row` now splits the leftover by the column's marker, all of it before the text for a right marker and `(W - w) // 2` before it for a centre marker"* [src: mdtab.py] | `mdtab.py:244–268` — `if alignment == RIGHT: before = pad` / `elif alignment == CENTRE: before = pad // 2` | **true**, exactly |
| `ADR-0005` `## Corrections`: *"WI-0002 moved `compose_row` from line 207 to 244, where line 207 is now the last line of `column_widths`"* | `mdtab.py` — `grep -n 'def compose_row'` → 244; `sed -n '207p'` → `    return widths`, the last line of `column_widths` (def at 190) | **true**, both halves |
| `ADR-0005` decision 1 — left/right/centre place the padding | `mdtab.py` `compose_row`; and my own runs of the filter under each marker | **true** |
| `ADR-0005` decision 3 — *"No content cell is exempt"*, header included | `emit_block`: `compose_delimiter` only at `index == 1`, `compose_row` for every other row | **true** |
| `ADR-0005` decision 5 — decisions 1–3 do not reach the delimiter row | same, plus `compose_delimiter` unchanged | **true** |
| `ADR-0005` decision 6 — *"the one space either side of the cell text is untouched"* | `compose_row`'s `" " + " "*before + cell + " "*(pad-before) + " "` | **true** |
| `ADR-0003` decision 9 — *"An empty cell is written as two spaces"* | `mdtab.py` `compose_row`, and three runs of the filter | **FALSE — see Findings 1** |
| `ADR-0003` `## Corrections` row of `23:17:37Z` — the four `mdtab.py:207` repairs | `mdtab.py` lines 190/207/244, and `grep -rn 'mdtab\.py:[0-9]' docs/` | **true**; the only surviving literal `mdtab.py:207` strings are inside `## Corrections` rows that are *quoting the stale citation being repaired*, which is what an append-only ledger requires |
| `docs/product/vision.md` line 121 — *"No content cell of a marked column is exempt: the header cell obeys its column's marker exactly as a body cell does"* [src: WI-0002/Q-001] | `Q-001`'s recorded answer (*"every row, every column, no exceptions"*), and `emit_block` | **true** |

**Commands run for this review:** `check-verify-freshness`, `check-commit-refs`, `lint-claims`,
`lint-answers`, `validate-workspace`, the trial merge and `python3 -m unittest discover -s tests -t .`
on the merge result, plus three filter runs to settle Findings 1. Outputs are in the journal entry.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | ten `- [x] AC` lines in `item.md`, no `- [ ]`; `validate-workspace` exit 0 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | its `## Criteria` table gives each of AC1–AC10 a command and quoted actual output; AC9's evidence is its own `## AC9` section. `impl-report.md` is cited nowhere as evidence — the failure mode this criterion exists for |
| D3 | gates passed on the **final** state of the code | **pass** | the second verification ran at `e533928`, and `git diff a324868..e533928 -- mdtab.py tests/` is empty, so the last code state and the verified state are the same tree. I re-ran `unittest` (24 tests, `OK`) and `compileall` myself on the merge result, not on the branch |
| D4 | no open blocking question | **pass** | `Q-001` and `Q-002` both `status: answered` with `## Consequences` naming real files; `validate-workspace` exit 0 |
| D5 | a journal entry per execution; `history.md` chains to the current status | **pass** | 13 history rows chaining `— → draft → … → in-review`, last row's `to` matches `item.md`'s `status: in-review`; 15 journal entries, one per transition plus two `intake` entries for the creation row and one `answer-questions` entry at `21:25:10Z` that propagated EP-001's answers without a transition |
| D6 | every design decision in an ADR, cited from the plan or journal | **pass** | ADR-0005 (marker placement, the odd remainder) cited from `plan.md` `## Problem` and `## Approach`; ADR-0006 (per-item test-name prefixes) recorded by `plan` and cited from plan step 5 and step 8. No design decision in the diff is uncovered by one of the two |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **pass** | `ADR-0005` v1→v3 and `ADR-0003` v2→v3, each with change-log rows and append-only `## Corrections` entries — the repairs the first review required. **Plus** `ADR-0003` v3→v4 applied by this review for Findings 1 |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, *"all 13 commit(s) on main..wi/WI-0002 name WI-0002"* |
| D9 | merged into the trunk | **pass** | trial-merged `--no-ff` into a **detached** worktree at `main` (trial head `96fd477`); `python3 -m unittest discover -s tests -t .` inside it → `Ran 24 tests`, `OK`, exit 0; trial discarded and `git rev-parse main` returned `b4568fe` both before and after, so the trunk did not move. The real merge follows this close, in that order, because `commits-reference-the-item` inspects `main..branch` and merging first would empty it |
| D10 | `verify` ran **after** the last code change | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → exit 0: *"verified at e533928e; wi/WI-0002 has moved to 57e10f0f but only the record changed (5 file(s) under tracker/ or docs/)"*. Confirmed independently: `git diff a324868..e533928 -- mdtab.py tests/` is empty, and the commits after `e533928` touch `tracker/` only |
| D11 | `review.md` states what was examined | **pass** | this file; `## What I examined` is first and names the artifacts, the diff range hunk by hunk, and every claim opened |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass, after a repair this review made** | the audit table above: eleven claims opened at their citations. Ten were true. One — `ADR-0003` decision 9's *"An empty cell is written as two spaces"* — was **false**, and is Findings 1. It is repaired in place as an `erratum` (`ADR-0003` v4), so D12 passes on the state being merged. `lint-claims --context work-item --changed-since main` → exit 0 over *"2 document(s) in 2 path(s) differ from main (b4568fe) under docs"* — a non-empty window — and `lint-answers` likewise, both re-run after the repair |

## Findings

**1. `ADR-0003` decision 9 claimed something false about empty cells. Repaired here as an erratum.**

Decision 9 read, in part: *"An empty cell is written as two spaces."* Written as an unqualified
absolute, it is true only of a zero-width column. Read against `compose_row`, which computes
`pad = width - display_width(cell)` and emits one space, `pad` spaces, one space, an empty cell is
written as `width + 2` spaces. Two runs settle it:

```
$ printf '| L | R |\n|---|---|\n| aaa | bbb |\n|  |  |\n' | python3 mdtab.py   # last row
|     |     |          # five spaces, not two: W = 3
$ printf '|  |\n|:---:|\n|  |\n' | python3 mdtab.py                            # last row
|   |                  # three spaces: ADR-0004 decision 2 raises W to 1
```

The second is exactly the case **WI-0002 AC5** covers — *"for `:---:`, `W = 1` and each content
cell is three spaces"* — which is why this item's D12 audit is where it surfaced.

**This is not a defect in WI-0002's delivery.** The clause predates the item: it was equally false
under WI-0001, and `git log --diff-filter=A` dates ADR-0004's two-colon minimum to `ac16080`, a
WI-0001 commit. WI-0002 neither wrote the sentence nor made it false. D12 does not ask whether this
change invalidated a claim — it asks whether the claim is *still true, read against the code* — and
that is precisely the F-001 failure mode of a wrong sentence surviving because each item assumes
another owns it. The first review's own reasoning stopped one step short here: `impl-report.md`
records *"`ADR-0003` decision 9 already carries a `## Corrections` row pointing at ADR-0005 for the
marked case; nothing further was needed"*, which addresses where the padding *sits* and never
re-reads the empty-cell sentence.

**Why repaired rather than sent back.** `spec/doc-header.md` §5 lists `implement` and `verify` as the
skills that do not write to `docs/`; `review-close` is not among them, and §4b's worked example shows
`review-close` in the `by` column of a `## Corrections` row. The `erratum` kind exists for exactly
this — *"replace a clause that was false against the code"* — and its one non-negotiable condition
holds: **no code would have to change to satisfy the new text.** Sending WI-0002 back would return it
to `in-progress` for a sentence it did not write and that `implement` is forbidden to fix — which is
the `Q-002` loop this item already paid four executions for. Repaired at `ADR-0003` v4, with the
removed text quoted verbatim, a change-log row, and both lints re-run green afterwards.

**2. The first review's three required repairs are all present and correct.** Checked individually,
not taken from the report that claims them — see the section below.

**3. No bug item was owed for the ADR-0004 filename correction, and none is owed now.**
`impl-report.md` Deviations 2 asks a reviewer to say so explicitly. The module docstring named
`ADR-0004-delimiter-row-keeps-alignment-markers.md`; the file is `…-preserves-…`. Plan step 4
rewrote those exact lines for an unrelated and required reason, the correction changes no behaviour
and no criterion, and the alternative — a bug item to fix one word inside lines the item was already
rewriting — would cost more record than it repairs. The first review reached the same conclusion;
this one re-reached it rather than inheriting it.

**4. `impl-report.md`'s toolkit finding is real and is not this item's to fix.** It records that
`spec/doc-header.md` §5 and `implement`'s `SKILL.md` §6a disagree about who repairs a wrong document:
§6a routes it to "ordinary repair — fix it", §5 forbids `implement` from writing to `docs/`. `Q-002`
resolved it correctly for this item, at the cost of a suspension and two extra executions. It is a
defect in the **toolkit**, outside this workspace, and there is no item under `EP-001` it belongs to.
Recorded here and surfaced to the harness owner rather than filed as a bug against project work.

**5. Two observations from `verify-report.md` reviewed, neither actionable.** `plan.md` step 2's
"Afterwards" line repeats AC3's width-3/width-1 illustration slip, and `impl-report.md`'s opening
line names a three-commit range on a now-thirteen-commit branch. Both are item artifacts that record
what a past execution believed at the time; neither is a standing document a future reader acts on,
and `item.md`'s `## Notes` already carries the authoritative reading of AC3. Correcting a superseded
report would damage the record more than it helps it. No action.

## The first review's verdict, and whether it was met

| # | required | met | how I checked |
|---|----------|-----|---------------|
| 1 | past-tense `ADR-0005`'s `## Context` clause about `compose_row`, version bump, change-log row | **yes** | opened `ADR-0005`: `version: 3`; `## Change log` carries rows 2 (erratum) and 3 (provenance); the `## Corrections` erratum row quotes the removed text verbatim — *"Read on its own it says the padding always follows the text, which is what `compose_row` does today"* — as §4b requires. The clause now reads *"did when this ADR was written, before WI-0002 changed it"* |
| 2 | repair the four `[src: mdtab.py:207]` citations, appending to `ADR-0003`'s `## Corrections` rather than editing it | **yes** | `grep -rn 'mdtab\.py:[0-9]' docs/` returns four hits, all inside `## Corrections` rows quoting the stale pointer they replace. The pre-existing `22:29:53Z` row in `ADR-0003` is untouched and a new `23:17:37Z` row supersedes it — append-only, as specified |
| 3 | record the AC3 reading in `item.md`'s `## Notes` | **yes** | `item.md` `## Notes` closes with *"AC3's second worked example describes a width-1 column, and the arithmetic governs"*, naming `verify` and `review-close` as having reached it independently. Committed as `e4dd5c6` |

The verdict also said *"the code is not in question"*. It still is not: `git diff a324868..e533928 --
mdtab.py tests/` is empty, and `verify` re-ran the whole item from scratch at `e533928` rather than
carrying its first report forward.

## Accepted gaps

Each is recorded somewhere that survives this item, as required.

1. **No renderer is checked.** The criteria compare bytes; nothing establishes that a centred column
   looks centred in any viewer. Recorded in `item.md`'s `## Out of scope` (*"Checking that a renderer
   agrees"*), which survives the close.
2. **Display width is an approximation.** ZWJ emoji sequences, regional-indicator flags and
   `east_asian_width: A` characters may be measured differently by a real terminal. Recorded in
   `ADR-0003` decision 7, which says so in its own text and cites `WI-0001/Q-001`, where the
   stakeholder accepted the approximation.
3. **Three WI-0001 criteria have no committed regression test against a marked column** — WI-0001
   AC5, AC7 and AC8. `verify` stated the non-intersection in those words, exercised all three by hand
   and passed them, and waived the committed cases by ID. I accept the waiver: WI-0002's `## Out of
   scope` names indentation, fenced blocks and non-well-formed blocks as things this item does not
   touch, and the code makes marker handling structurally unreachable in all three paths
   (`transform` copies inside a fence before candidacy; `table_or_none` returns `None` before
   `column_alignments` runs; `emit_block` re-emits the prefix outside the widths). The waiver, its
   reasons and its cost are in `verify-report.md` `## Not verified, and why`, which survives the
   close as this item's artifact.
4. **`ADR-0001:58` carries one unsourced absolute.** `lint-claims --all` reports it; it is outside
   this item's window and outside D12's scope, and `impl-report.md` records that it is deliberately
   left for the epic close, where `--context epic` will see it. **This is the one gap whose home is a
   future execution rather than a document**, so it is named here explicitly: the reviewer closing
   EP-001 must repair or record it, and F-066 is the reason `--context epic` will not let it pass
   silently.

## Verdict

**Accepted — `in-review` → `done`, `outcome: delivered`.**

All twelve Definition of Done criteria pass with per-criterion evidence. The diff was read hunk by
hunk and every hunk serves a criterion or a plan step; the tests pass on the merge result, not only
on the branch; the trunk did not move during the trial. One D12 finding was real and is repaired in
place as an `ADR-0003` erratum rather than routed through a send-back the item did not earn.

WI-0002 delivers what the stakeholder asked for in the second half of their sentence: the colons in
the delimiter row now decide which side of a cell its padding falls on, the odd centring space goes
to the right as they chose, markers survive colon-for-colon, and everything WI-0001 established —
widths, passthrough, indentation, fenced blocks — is unchanged.

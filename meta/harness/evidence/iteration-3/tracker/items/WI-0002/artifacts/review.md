# Review — WI-0002

The first and only review of WI-0002. The item was verified once, passed on all fourteen
criteria, and reached `in-review` with one non-blocking question (`Q-003`) that
`answer-questions` had already resolved before this review began.

## What I examined

- `item.md` — the fourteen criteria and their tick state, the preamble defining "field",
  `## Out of scope`, and the whole of `## Notes` including the round-3 AC14 amendment;
  `history.md` — eight rows, chaining without a gap from creation to `in-review` and matching
  `item.md`'s status; `journal.md` — all nine entries in full, personas `product-analyst`,
  `architect`, `developer`, `qa-engineer`.
- All three questions on the item. `Q-001` and `Q-002` answered by the human in round 1, `Q-003`
  by `answer-questions` in round 3. Each has a `## Consequences` naming files, and I opened the
  files each names — including `docs/product/vision.md` v4, which is where finding 1 below
  comes from.
- `plan.md`, `impl-report.md` and `verify-report.md` in full, including
  `## Deviations from the plan` (five), `## What I did not do` (four), and
  `## Not verified, and why` (four declared gaps).
- **The diff itself**, `main..wi/WI-0002` — 6 commits, 32 files, +941/−33. Code side: the whole
  of `mdtab/table.py`'s changed region read hunk by hunk (`column_alignments`, `_render_cell`,
  `_render_row`, `lay_out`), both test modules, and all ten new fixture pairs plus the one
  changed WI-0001 fixture, read as bytes with `cat -A`.
- `docs/architecture/adr/ADR-0007-*.md` v1, `docs/architecture/overview.md` v3 and
  `docs/product/vision.md` v4 — the three documents that describe this behaviour.
- Six adversarial probes of my own against the built tool, listed under `## Findings`.
- A trial merge into a **detached** worktree of `main`, with `commands.test` and `commands.lint`
  run on the merge result; the trial was then discarded and `main` confirmed unmoved at
  `571cac2a`.

### Every hunk, and the criterion or step it serves

`git diff main..wi/WI-0002 -- mdtab/` is four hunks, all in `mdtab/table.py`:

| hunk | serves |
|------|--------|
| `column_alignments(rows)` — new, reads `rows[1]`, strips `_TRIM`, four marker cases | AC1; plan step 1; ADR-0007 §Decision 1 |
| `_render_cell` — new `alignment` parameter, `padding` split into `before`/`after` | AC2, AC3, AC4; plan step 2; ADR-0007 §Decision 2 |
| `_render_row` — new `alignments` parameter, threaded to `_render_cell`; delimiter branch ignores it | AC9 (the delimiter row is unaffected); plan step 3 |
| `lay_out` — `alignments = column_alignments(rows)` computed once beside `widths` | AC6, ADR-0007 §Decision 1 |

Nothing in the diff serves neither a criterion nor a step. `_column_widths`,
`_render_delimiter`, `_spaces_omitted` and all ten of the parsing and recognition functions were
checked **byte-identical to `main`** by extracting each function from both revisions and
comparing:

```
_column_widths  1325 == 1325 identical=True      is_delimiter_row  282 == 282 identical=True
_render_delimiter 255 == 255 identical=True      row_cells         308 == 308 identical=True
_spaces_omitted   642 == 642 identical=True      has_leading_pipe  172 == 172 identical=True
split_row         706 == 706 identical=True      has_trailing_pipe 758 == 758 identical=True
has_unescaped_pipe 177 == 177 identical=True     _outer_style      378 == 378 identical=True
```

That is the mechanism behind AC6, AC9 and AC13 being regression checks rather than new
behaviour, and it is why this item leaves the recognition rules intact for WI-0003 to change.

### Claims audited (D12), each read against the thing it cites

| claim, and where | what I opened | verdict |
|------------------|---------------|---------|
| overview v3: "Where a cell's content sits in its field — `mdtab/table.py`, one function reading the delimiter row's markers into one alignment value per column, and one renderer distributing the spare space around the content: all after it, all before it, or split with the odd column on the right" | `column_alignments` (lines 90–112) and `_render_cell` (lines 173–199) | **holds** — one reader, one renderer, three branches, `before = padding // 2` with `after = padding - before` |
| overview v3: "The guard spaces are outside the field and do not move, and no column's width depends on its marker" | `_render_cell`'s return expression; and the same table laid out under all four markers | **holds** — the guards are added outside `before`/`after`; the four layouts put every `\|` at identical display columns (`all four identical: True`) |
| overview v3, "A property the tool no longer has": a bare table whose first column's marker is `---:` or `:---:` "comes back with leading spaces on its header and body rows and none on its delimiter row, so the prefix rule sees a run whose lines disagree and declines it… The bytes are still stable" | ran both cases through the built tool | **holds** — `a \| b` / `---:\|---` / `xxxx \| y` → `   a \| b` / `----:\|--` / `xxxx \| y`; `lay_out` of that output returns `None`; a second run is byte-identical (`cmp` exit 0). The `:---:` case behaves the same way |
| ADR-0007 §Decision 2: the field is `width - 2`, and `padding` is distributed all after / all before / floor-ceil with the odd column on the right | `_render_cell`, and three centred documents with one, two and three spare columns | **holds** — `\| ab  \|`, `\|  ab  \|`, `\|  ab   \|`; the extra column is on the right in the odd cases |
| ADR-0007 §Decision 3: where the outer-pipe style drops a guard space, "the field keeps its width, so the padding of a right-aligned first column in a bare table lands at the start of the line… and that of a right-aligned last column removes the trailing spaces" | the two documents, plus `awk '{print length($0)}'` and `grep -n ' $'` | **holds** — leading spaces present with no `\|` added (pipe counts `[1,1,1]` in and out); the no-trailing-pipe document's three lines are all 11 columns wide and none ends in a space |
| ADR-0007 §Decision 4: "`_column_widths` is not touched" | the function-level diff above | **holds** — byte-identical |
| ADR-0007 §Decision 5: "The delimiter row keeps being rendered by `_render_delimiter`… Alignment never rewrites a marker" | `_render_delimiter` byte-identical; `\|  :---  \| ---:  \|` fed through the tool | **holds** — `\|:-----\|--:\|`, colons at the ends they had, none added, moved or removed |
| ADR-0002: cell width is display width, and nothing outside `width.py` uses `len()` to mean a width | `padding = width - 2 - display_width(text)` (line 184); every `len(` in `mdtab/table.py` — ten of them | **holds** — the ten are list lengths, cell counts and prefix slicing; none is a width. A `---:` column holding `表`, `é`, `e`+U+0301 and `word` ends at one display column |
| vision v4: "The alignment markers in a delimiter row are honoured in every column without exception" | a four-column table, one marker each, header and body | **holds** — `:---` left, `---:` right, `:---:` centred, `---` left, in the header row and both body rows |
| vision v4: "Inside a table it does understand, mdtab changes spaces and nothing else — it never adds or removes a `\|`" | non-space characters of a marker-bearing document compared in and out, line by line | **holds, with the delimiter row's dash count as the known exception** — the only line whose non-space characters change is the delimiter row (`\|:---\|---:\|:---:\|` → `\|:-----\|------:\|:------:\|`), which is WI-0001 AC12 filling the field with `-` and predates this item. Pipe counts are unchanged on every line |
| vision v4: "A table mdtab has laid out is a table mdtab still recognises: making that true where those leading spaces appear is WI-0003" | the bare `---:` document, twice through the tool | **finding 1** — true as the whole sentence reads, false as its first clause reads alone. See `## Findings` |
| ADR-0007 §Decision 1: alignment "is computed beside the column widths, from the same parsed rows, and passed to the renderer — no second reading of the delimiter row anywhere" | `grep -n 'startswith(":")\|endswith(":")\|rows\[1\]' mdtab/*.py`; `grep -rn column_alignments mdtab/` | **finding 2** — the claim it is making (the *alignment* is derived once, in one place) holds: `column_alignments` is defined once and called once, from `lay_out`. The sentence as written does not: `_column_widths` (line 166) and `_render_delimiter` (lines 202–203) both read the same delimiter cell's markers, for the minimum-width rule and for re-rendering the row. See `## Findings` |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c '^- \[x\] AC' item.md` → 14; `grep -c '^- \[ \] AC'` → 0 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | the report's `## Criteria` table has fourteen rows, each naming a command `verify` ran and quoting its actual output. Every document was written during verification under `/tmp/vwi2/`, so no row is carried by one of this item's own fixtures. AC14's row is the one to read carefully: it records `pass` on the criterion's substance — fifteen separate re-checks of WI-0001's criteria on marker-bearing documents — and states, rather than hides, that AC14's then-current checking clause was unsatisfiable. `Q-003` fixed the clause; the evidence behind the tick did not change |
| D3 | gates passed on the final state of the code | **pass** | `commands.test` → `Ran 65 tests … OK` and `commands.lint` → exit 0, both re-run here **on the merge result** in a detached worktree; `check-verify-freshness` → exit 0 |
| D4 | no open blocking question | **pass** | `Q-001`, `Q-002` (blocking) and `Q-003` (non-blocking) all `status: answered`; `validate-workspace` → 0 errors, 0 warnings |
| D5 | a journal entry per execution, history chains | **pass** | eight history rows and nine journal entries. Rows 2–8 match entries 2–8 timestamp for timestamp; entry 1 is `intake`'s, written at 18:26:52Z for the creation row `new-item` stamped at 18:24:41Z, the same shape WI-0001 has. Entry 9 is `answer-questions` at 20:52:15Z with `in-review → in-review (unchanged)` — a non-blocking question suspends nothing, which `spec/journal-and-history.md` §2.2 provides for. The last row, `verifying → in-review`, matched `item.md` when this review began |
| D6 | every design decision in an ADR, cited from plan or journal | **pass** | ADR-0007 written by `plan`, cited from `plan.md`'s `## Decisions and ADRs` (three of its four rows) and from the AC mapping. The two decisions that were the stakeholder's — the centring tie-break and aligning a bare table's first column — are recorded as theirs in that table and cited by the ADR rather than re-decided. `Q-003` produced no ADR, correctly: its answer follows from AC14's own exception clause and ADR-0007 §Decision 2, which is citation rather than a new decision |
| D7 | documents the change invalidated updated, with a version bump | **pass, with finding 1** | `docs/architecture/overview.md` v2 → v3 and ADR-0007 v1, both by `plan`, both with change-log rows; `docs/product/vision.md` v3 → v4 by `answer-questions` with a change-log row. `implement` correctly changed nothing under `docs/` — it found nothing in them that the built code contradicted, which I re-checked above rather than took on trust. The one sentence this change makes read oddly is finding 1, accepted rather than sent back |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, "all 6 commit(s) on main..wi/WI-0002 name WI-0002" |
| D9 | merged into the trunk | **pass** | trial merge into a detached worktree of `main` was clean; `commands.test` on the merge result → `Ran 65 tests … OK`; `commands.lint` → exit 0; a smoke run of the four-marker table on the merge result produced the expected layout. The trial was discarded and `main` confirmed unmoved at `571cac2a`. The real merge follows this close in the same execution, in the order step 8 requires |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → exit 0: "WI-0002 verified at a8b5a4bb; wi/WI-0002 has moved to 308145b0 but only the record changed (7 file(s) under tracker/ or docs/), so the verification still covers the code". The two commits after the verified one are `verify`'s own report and `answer-questions`' amendment of AC14's checking clause; neither touches `mdtab/` or `tests/` |
| D11 | `review.md` exists and states what was examined | **pass** | this file, `## What I examined` above |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass, with findings 1 and 2** | twelve claims audited above, each opened against the code or the behaviour it cites rather than against a document that repeats it. Ten hold outright. The two that do not hold *as written* are recorded as findings, with the wording that would make each true. `lint-claims --changed-since main` → exit 0 |

**All twelve pass. The item is accepted.**

## Findings

Two, both about sentences rather than about behaviour, both accepted rather than sent back. A
third observation concerns the pipeline's own tooling and belongs to nobody's item.

1. **`docs/product/vision.md` v4 states the recognition property in the present tense, one clause
   before conceding it.** *(minor, record accuracy — accepted, correction recorded)*

   The sentence is: *"A table mdtab has laid out is a table mdtab still recognises: making that
   true where those leading spaces appear is [src: WI-0003], filed because the stakeholder
   refused to work around the fault rather than fix it."* Read whole, it is true and it is
   informative: "making that true" concedes that it is not true yet in the named case. Read as
   far as the colon — which is how a claim gets quoted into a second document, and how F-001
   happened — it asserts a property that this item removes. `docs/architecture/overview.md` v3
   says the same fact the other way round, under the heading "A property the tool no longer has",
   and that version is the one to copy.

   Confirmed against the built tool, not against the prose: `a | b` / `---:|---` / `xxxx | y`
   lays out to `   a | b` / `----:|--` / `xxxx | y`, and `lay_out` returns `None` for that
   output.

   **Why this is not a send-back.** Nothing in it is wrong about behaviour, the sentence carries
   its own correction, and the change a send-back would produce is one clause reordered — at the
   cost of an implement-and-verify cycle that would re-check fourteen criteria none of which is
   in question. The wording that would settle it, for whoever edits this file next: *"Until
   WI-0003, a table mdtab has laid out is not always a table mdtab recognises: the first column
   of a bare table, right- or centre-aligned, comes back with leading spaces its delimiter row
   does not have."*

   **This is one of two edits WI-0003 must make when it lands**, and both are recorded in
   `item.md`'s `## Notes` so they are found from the item rather than only from here. The other
   is the overview's "A property the tool no longer has" section, which says of itself that a
   reader who finds it after WI-0003 should treat it as stale.

2. **ADR-0007 §Decision 1 and `column_alignments`' docstring both claim the delimiter row's
   markers are read in exactly one place, and the code reads them in three.** *(minor, record
   accuracy — accepted, correction recorded)*

   The ADR says alignment "is computed beside the column widths, from the same parsed rows, and
   passed to the renderer — **no second reading of the delimiter row anywhere**". The docstring
   says "The markers are read here and nowhere else, from `rows[1]`". What is true is the claim
   each is making — that the *alignment* is derived once and not re-derived per cell:

   ```
   $ grep -rn "column_alignments" mdtab/
   mdtab/table.py:90:def column_alignments(rows: list) -> list:
   mdtab/table.py:281:    alignments = column_alignments(rows)
   ```

   One definition, one call site. But two other places read the same delimiter cell for their own
   rules, both of them WI-0001's and both unchanged by this item:

   ```
   mdtab/table.py:166:        marker = rows[1][column].strip(_TRIM)
   mdtab/table.py:167:        needed = 1 + marker.startswith(":") + marker.endswith(":")   # minimum width
   mdtab/table.py:202:    lead = marker.startswith(":")                                    # re-rendering
   mdtab/table.py:203:    trail = marker.endswith(":")
   ```

   The docstring's own next clause — "so the delimiter row has one reader for its alignment just
   as it has one for its dashes" — shows the author knew this and states the true version one
   line later. The overview, again, gets it right: it claims one function *for the alignment*
   and claims nothing about the delimiter row in general.

   **Why this is not a send-back.** The duplication the absolute would warn about does not exist:
   there is no second derivation of an alignment anywhere, which I checked rather than assumed.
   Correcting it is two words in two files — "the markers are read for alignment here and nowhere
   else" — and it changes no behaviour and no test. It is recorded in `item.md`'s `## Notes` for
   the next execution that touches either file, which is likely WI-0003, since it will change the
   recognition rules `column_alignments` sits beside.

   **The two findings are the same shape and that is worth naming.** Both put an absolute first
   and its qualification second; both are true when read to the end of the sentence and false
   when quoted at the comma. That is precisely the shape F-001 describes, caught here before it
   propagated. Two instances in one item is a pattern in the making: if a third appears, the
   project should stop accepting them one at a time and put the rule somewhere — an absolute
   about behaviour states the exception before it states the rule.

3. **`lint-claims` over the whole tree reports two errors in a document this item never
   touched.** *(observation about the pipeline's tooling, not a defect in mdtab — no item filed)*

   ```
   $ python3 .claude/agile-skills/scripts/lint-claims .
   docs/architecture/adr/ADR-0003-…md:46: ERROR [claim.unsourced] an absolute claim ('any')
       about 'Q-002' with no citation
   docs/architecture/adr/ADR-0003-…md:62: ERROR [claim.unsourced] an absolute claim ('only')
       about 'Q-002' with no citation
   lint-claims: 2 errors, 0 warnings
   ```

   Both lines mention a **question ID in backticks** — "would keep the promise in `Q-002`" — and
   the linter's rule 2 is about "an absolute claim about a named **code object**". A backticked
   `Q-002` is not a code object, and the paragraphs in question make no claim about one. This
   looks like a mis-classification in the gate, not an unsourced claim in ADR-0003, which was
   delivered under WI-0001 and is unchanged by this item.

   The contracted gate form, `lint-claims --changed-since main`, passes (exit 0) because no
   document changed on this branch. No bug item is filed: the defect, if it is one, is in
   `.claude/agile-skills/scripts/`, which is the pipeline's machinery and not this project's
   product — the same reasoning WI-0001's review applied to `validate-workspace`'s decode crash.
   It is reported to the toolkit's owner in the turn's harness status instead.

Nothing else. Six probes of my own against the built tool, none of which is a finding:

- **A bare table with a *centred* first column** — ADR-0007 names `:---:` beside `---:`, and the
  criteria demonstrate only `---:`. It behaves as the ADR says: ` a   | b` / `:---:|--` /
  `xxxx | y`, and the second run reproduces the bytes.
- **An escaped `|` inside a right-aligned cell** — `c \| d` is measured as one cell six columns
  wide and padded before, not split. The escaping rule is untouched.
- **A CRLF document with markers** — all three terminators survive and no bare `\r` appears.
- **A `---:` column whose header and body cells are all empty** — the field collapses to nothing
  and the delimiter cell renders `-:`, one dash and the colon, which is WI-0001 AC12's
  minimum-width rule and not something alignment changed.
- **A document with no final newline, centred** — none is added.
- **An undecodable byte in a right-aligned column** — carried through by surrogateescape and
  padded like any other one-column cell.

Two things I looked at because they are where this design could rot, and neither is a finding:

- **`padding` can never go negative.** `_column_widths` returns `max(2 + max(content), needed +
  omitted)`, so every column is at least two wider than its widest cell, and
  `padding = width - 2 - display_width(text)` is therefore `>= 0` for every cell — including the
  widest one, where it is exactly 0. A future change that lets a column be narrower than its
  widest cell would turn `" " * before` silently into the empty string rather than fail.
- **`_render_row` indexes `alignments[column]` for every cell**, so it depends on the alignment
  list being exactly as long as each row. It is, because recognition rule 1 has already refused
  any run whose rows disagree about their cell count, and both lists are derived from the same
  parsed `rows`. WI-0003 changes the recognition rules; if it ever admits a ragged run, this is
  the second place that assumption lives.

## Accepted gaps

Recorded here **and** in `item.md`'s `## Notes`, so they survive the item.

1. **This verification's independence is weaker than the pipeline intends.** `verify` declared
   it: the same session ran `implement` on this item earlier in the same turn. The three defences
   it used are real and I checked each — every criterion's check was derived from the criterion
   before the implementation report was read, every document was written during verification
   rather than taken from the item's fixtures, and the one judgement call was put to a different
   persona through `Q-003` instead of standing on the verifier's say-so. This review is a fourth
   defence and an independent read of the diff, but it is not a substitute for a verifier who did
   not write the code. Worth knowing when reading the fourteen ticks.
2. **The recognition fault this item creates is real, deliberate, and not fixed here.** mdtab may
   now emit a bare right- or centre-aligned table it will not recognise on a later run. The
   stakeholder was shown the cost and chose it (`WI-0002/Q-002`); ADR-0007 records it; AC10
   requires it; WI-0003 owns the fix. The bytes are stable either way, so no document is
   corrupted — what is lost is the second tidy-up, silently, because the tool has no diagnostics.
3. **The same fault has a second form that nothing yet demonstrates.** Inside a blockquote or an
   indented table, a right-aligned first column puts its padding immediately after the prefix, so
   a later run compares prefixes of different lengths. `item.md`'s `## Notes` records it for
   WI-0003's refinement; no fixture or test exercises it, because no criterion of this item
   covers it and AC12's fixtures both use markers that pad on the far side.
4. **`column_alignments` is public and does not guard against a `rows` list shorter than two.**
   `verify` declared it. `lay_out` has already rejected any run of fewer than two lines before it
   is called, so no reachable input reaches it; the guard lives in the caller. WI-0003 changes
   that caller.
5. **The ten new fixtures' expected outputs were hand-written and not independently re-derived.**
   `implement` counted display columns by hand; `verify` deliberately used its own documents
   instead, so neither check would catch a fixture whose expected output is wrong in a way none
   of the fourteen criteria detects. I read all ten pairs as bytes with `cat -A` and re-derived
   four of them (`align-markers`, `align-centre-odd`, `align-list-indent`, `align-unicode`) from
   the width rule by hand; that bounds the risk rather than removing it. This is the same gap
   WI-0001's review recorded, one item on.
6. **Performance, concurrency and large inputs are unexercised**, as in WI-0001. No criterion of
   either item mentions them; the largest document run through the tool in this item was 27
   lines.

## Verdict

**Accepted — merged into `main` and closed as `delivered`.**

Fourteen of fourteen criteria met, each demonstrated by a command `verify` ran on documents it
wrote for the purpose; seven classes of negative and boundary case triggered; three mutations
confirming the suite fails when the behaviour it names is removed, one of which — centring
rounding the other way — is caught by exactly one test and one fixture. All twelve Definition of
Done criteria pass. Every hunk in `main..wi/WI-0002` maps to a criterion or a plan step, and the
ten functions this item must not have touched are byte-identical to `main`. The trial merge was
clean and both gate commands pass on the merge result.

What this item delivers completes the epic's stated behaviour: mdtab now pads each cell where the
delimiter row's marker says, in the header row and every body row, measured in display columns,
without moving a guard space, changing a column's width, or rewriting a marker. What it costs is
recorded in three places and owned by WI-0003: a bare table with a right- or centre-aligned first
column comes back with leading spaces, and mdtab will not recognise that output on a later run.
The stakeholder was asked, was shown the alternative, and chose this with the price named.

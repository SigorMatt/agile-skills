# Review — WI-0001

This is the **second** review of WI-0001. The first (2026-08-28T19:21:09Z) rejected the item on
D12 with four findings; `implement` closed all four across two rounds, `answer-questions` decided
`Q-004` (ADR-0006) in between, and `verify` re-checked every criterion from scratch. This review
covers the whole change again, not only the delta — a reviewer who reads only what moved since a
rejection is trusting the first review's reading of everything else, and the first review's
reading is what produced two false claims.

## What I examined

- `item.md` — the fifteen criteria and their tick state, `## Out of scope`, and the whole of
  `## Notes` including the AC12 amendment made this turn; `history.md` — thirteen rows, chaining
  without a gap from creation to `in-review` and matching `item.md`'s status; `journal.md` — all
  fourteen entries in full, personas `product-analyst`, `architect`, `developer`, `qa-engineer`,
  `reviewer`.
- All five questions on the item. `Q-001`…`Q-003` answered by the human, `Q-004` and `Q-005`
  answered by `answer-questions`; each has a `## Consequences` naming files, and I opened the
  files each names.
- `plan.md`, `impl-report.md`, `verify-report.md` in full, including `## Deviations from the
  plan` (seven), `## What I did not do`, and `## Not verified, and why` (four declared gaps).
- **The diff itself**, `main..wi/WI-0001` — 16 commits, 68 files, +2802/−45. Code side: six
  modules under `mdtab/` read line by line (`table.py` 226, `scan.py` 96, `textio.py` 59,
  `width.py` 29, `filter.py` 26, `__main__.py` 22), both test modules, 23 fixture pairs,
  `.gitattributes`.
- A trial merge into a **detached** worktree of `main`, with `commands.test` and `commands.lint`
  run on the merge result; the trial was then discarded and `main` confirmed unmoved at
  `d1efa811`.

### Claims audited (D12), each read against the thing it cites

Every row is a claim opened against the code it names, not against a neighbouring document that
repeats it. The two rows that were **FALSE** in the first review are re-checked here from the
code rather than from the implementation report's assertion that they were fixed.

| claim, and where | what I opened | verdict |
|------------------|---------------|---------|
| overview v2 (new this turn): "How wide a column is — `mdtab/table.py`, one function, and it carries two rules… the maximum is taken over the header and body rows only… a column is never narrower than its delimiter cell can be written" | `_column_widths`, lines 130–143 | **holds** — `if index != 1` excludes the delimiter row from `max`; `max(width, needed + omitted)` is the floor, with `needed = 1 + leading colon + trailing colon`. One function, both rules, no second copy |
| overview: "Where a cell boundary is — `mdtab/table.py`, one function, used by the cell-count rule, **the outer-pipe test** and the layout alike, so the three cannot disagree" — **FALSE at the first review** | every call site: `grep -n "split_row(" mdtab/table.py` → lines 49, 68, 74; `grep -rn _escaped_at mdtab/` → no match | **holds now** — `has_unescaped_pipe` (49), `has_trailing_pipe` (68) and `row_cells` (74) all call the one splitter; the second expression of the escaping rule is deleted. Finding 3 closed |
| ADR-0005: "**Fixtures are the only place a test may express a document; a test may not build one from a Python literal**" — **FALSE at the first review** | every `run(` in `tests/test_fixtures.py` (20 call sites), and `test_units.py` for `format_document` | **holds now** — every argument to `run(` is `read(name, side)` or a prior output; `test_units.py` never runs a document through the tool. The remaining bytes literals are assertions *about* output, which is not expressing a document. Finding 1 closed |
| ADR-0002: "a precomposed `é` and a decomposed `e` + `U+0301` both measure 1" | ran `display_width` on both spellings | **holds** — 1 and 1; also `U+FE0F` → 0, `表` → 2, `ＡＢ` → 4 |
| ADR-0002: "The tool does **not** normalise cell text" | `grep -rn "normalize\|normalise" mdtab/` | **holds** — no match |
| ADR-0002: "nothing in the tool may use `len()` on cell text to mean a width" | every `len(` in `mdtab/` outside `width.py` — sixteen of them | **holds** — list lengths, prefix lengths, index bounds, and one character count in `_fence_closes` where the line is a run of one ASCII character; none is a display width |
| ADR-0004: "`str.splitlines` is forbidden everywhere in the package" | `grep -rn splitlines mdtab/ tests/` | **holds** — the only match is the docstring stating the rule |
| ADR-0004: "Nothing between those two points touches a file object" | `grep -rn "open(\|os\.\|socket\|urllib\|sys\.argv" mdtab/` | **holds** — no match |
| ADR-0006: "a fixture whose bytes are deliberately not valid UTF-8 carries `.in.bin` / `.out.bin`… discovery keys on the `.in.` infix" | `tests/test_fixtures.py` lines 33–38, 76; the fixture listing | **holds** — `EXTENSIONS` is built by splitting on `.in.`, `path_of` reads the extension back out of it, and `invalid-utf8.in.bin` / `.out.bin` are the only `.bin` pair |
| overview: "`__main__` does nothing but decode, call it, and encode" | `mdtab/__main__.py` lines 15–19 | **holds** — write, flush, return 0, and nothing else |
| vision: "it never adds or removes a `\|`, so a table written without outer bars comes back without them" | a fresh two-table document, per-line `\|` counts compared | **holds** — no line differs, and the bare table stays bare |
| vision: "That is the only syntax it recognises" (GFM pipe tables) | an rst grid table run through the tool | **holds** — byte-for-byte |
| `item.md` AC12 as amended this turn | the four cases the amended text names, run through the tool | **holds** — `:---:` all-empty → 3, `---` → 2, `:---` → 2, and the bare-row interior `:-:` case → field 3 with the two edge columns one narrower |

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c "^- \[x\] AC" item.md` → 15; `grep -c "^- \[ \] AC"` → 0 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | the report's `## Criteria` table has fifteen rows, each naming a command the verifier ran and quoting its actual output. The documents were written during verification and the widths measured with an independent implementation of ADR-0002 that does not import `mdtab.width`, so no row is circular |
| D3 | gates passed on the final state of the code | **pass** | `commands.test` → `Ran 55 tests … OK` and `commands.lint` → exit 0, both re-run here on the merge result; `check-verify-freshness` → exit 0 |
| D4 | no open blocking question | **pass** | all five questions `status: answered`; `validate-workspace` → 0 errors, 0 warnings |
| D5 | a journal entry per execution, history chains | **pass** | thirteen history rows and fourteen journal entries, timestamps matching row for row. The fourteenth entry is `answer-questions` at 20:01:15Z, which made no transition — a non-blocking question needs no suspension, and `spec/journal-and-history.md` §2.2 provides for exactly that with `X → X (unchanged)`. The last history row `verifying → in-review` matches `item.md`'s status at the moment this review began |
| D6 | every design decision in an ADR, cited from plan or journal | **pass** | ADR-0004 and ADR-0005 written by `plan` and cited in `plan.md`'s decisions table; ADR-0006 written by `answer-questions` for `Q-004` and cited from `plan.md` steps 10–11 and the AC9 mapping row; ADR-0001–0003 predate the item and are cited in the criteria. `Q-005` produced no ADR, correctly — its answer follows from documents that already existed, and `answered-from-the-record` is satisfied by citation rather than by a new decision |
| D7 | documents the change invalidated updated, with a version bump | **pass** | `docs/architecture/overview.md` v1 → v2 with a change-log row, `updated-by: answer-questions`, adding "How wide a column is" to the one-place-per-rule list; ADR-0005 v1 → v2 for the `.bin` exception. No other document is made out of date by the change — the two sentences that *were* false are now true against the code, which is D12's row rather than D7's |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 16 commit(s) on main..wi/WI-0001 name WI-0001" |
| D9 | merged into the trunk | **pass** | trial merge into a detached worktree of `main` was clean; `commands.test` on the merge result → `Ran 55 tests … OK`; `commands.lint` on the merge result → exit 0; trial discarded and `main` confirmed unmoved at `d1efa811`. The real merge follows this close in the same execution, in the order step 8 requires: `check-commit-refs` inspects `main..wi/WI-0001`, which merging first would empty, so closing precedes merging |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: "WI-0001 verified at e0fd6b00; wi/WI-0001 has moved to 03e63660 but only the record changed (8 file(s) under tracker/ or docs/), so the verification still covers the code" |
| D11 | `review.md` exists and states what was examined | **pass** | this file, `## What I examined` above |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass** | thirteen claims audited above, each read against the file it cites. The two that were false at the first review are true now, checked from the code rather than from the report claiming they were fixed. `lint-claims --changed-since main` → exit 0, `checked 3 document(s)`, 0 errors |

**All twelve pass. The item is accepted.**

## Findings

One, minor, accepted rather than sent back.

1. **`impl-report.md` miscounts the fixtures that go beyond the plan.** *(minor, record accuracy —
   accepted, corrected here)*
   `## Deviations from the plan` 3 says "**One fixture beyond the plan's list: `tab-prefix`**".
   Three fixtures are not named in `plan.md`'s AC-to-evidence mapping:

   ```
   $ for f in tests/fixtures/*.in.*; do n=$(basename "$f"); n="${n%%.in.*}"; \
       grep -q -- "$n" tracker/items/WI-0001/artifacts/plan.md || echo "NOT IN PLAN: $n"; done
   NOT IN PLAN: empty-cells
   NOT IN PLAN: tab-in-cell
   NOT IN PLAN: tab-prefix
   ```

   `verify` raised this in `verify-report.md`'s `## Defects found` 2 and routed it here.
   `tab-in-cell` is declared elsewhere in the same report — the `### What this round changed`
   table, finding 2's row — so the genuinely undeclared one is `empty-cells`.

   **Why this is not a send-back**, when the first review rejected the item over an undeclared
   deviation: the two are different in the way that matters. Finding 1 of the first review was an
   undeclared deviation that **contradicted an ADR** and was accompanied by a **false module
   docstring**; it had to be fixed in the code. This is a miscount in a report. `empty-cells` is
   not a deviation from plan step 10 at all — step 10 requires a document to live in a fixture
   rather than in a Python literal, so a test asserting AC12's empty-cell rendering has nowhere
   else to put its document. Nothing in `docs/` is false, no ADR is contradicted, no behaviour is
   in question, and a third implement-and-verify cycle would produce one corrected sentence and
   no other change. The correction is recorded here and in `item.md`'s `## Notes`, which is where
   a reader of the closed item will look; the report's own sentence stays as the developer wrote
   it, because a reviewer editing the developer's report would leave the record less honest, not
   more.

Nothing else. Every hunk in `main..wi/WI-0001` maps to a numbered plan step — 1 → `textio.py`,
2 → `width.py`, 3/5/6 → `table.py`, 4 → `scan.py`, 7 → `filter.py`, 8 → `__main__.py`,
9 → `.gitattributes`, 10 → `tests/fixtures/`, 11 → `test_fixtures.py`, 12 → `test_units.py` —
and every hunk in `256260f..HEAD` maps to a numbered finding of the first review. No hunk serves
neither a criterion nor a step. The four recognition rules, the display-width rule, the
column-width rule and the byte round-trip are each in one place and each match their ADR.

Two things I looked at specifically because they are where this design could rot, and neither is
a finding:

- **`format_document` replaces line ranges by index while iterating runs.** That is only safe
  because `lay_out` returns exactly as many lines as it was given; it does, on every branch, and
  a run it refuses returns `None` and is not spliced at all. Worth knowing before anyone makes
  the layout able to add or drop a line.
- **`find_runs` imports `has_unescaped_pipe` inside the function body** to break a cycle
  (`impl-report.md` deviation 4). The rule still lives in `mdtab/table.py`, which is what the
  overview requires; only the import site moved, and a comment at the call site says why.

## Accepted gaps

Recorded here **and** in `item.md`'s `## Notes`, so they survive the item.

1. **The CPython 3.8 floor `plan.md` sets is asserted, not tested.** Only CPython 3.12.3 is
   installed. I read for it again: no `str.removeprefix`, no match statement, no 3.9+ builtin in
   `mdtab/`, and `from __future__ import annotations` wherever an annotation appears — including
   the six parameterised signatures restored for the first review's finding 4, which is what
   makes them safe at 3.8. An inspection is not a check, and it stays one until a second
   interpreter exists.
2. **How a terminal or editor font actually draws the output is not verifiable from here.** AC2
   and AC3 are met against ADR-0002's rule, which is what they name. ADR-0002's recorded
   limitation for joined emoji sequences and for ambiguous-width characters in a terminal
   configured to draw them wide is unchanged and is documentation, not a defect.
3. **The shipped fixtures' expected outputs were not independently re-derived.** `verify`
   declared this. The suite asserts the code reproduces them; the second verification's own
   evidence came from documents written during verification instead, so both checks would miss a
   fixture whose hand-written expected output is wrong in a way none of the fifteen criteria
   detects. I read the fixture pairs hunk by hunk in the first review and no fixture's expected
   output changed in either round since, which bounds the risk rather than removing it.
4. **No README or user-facing documentation.** No criterion asks for one and the epic does not
   scope it; ADR-0002's limitation about joined emoji sequences is recorded in the ADR rather
   than anywhere a user would read. Worth an item if the tool is ever published — deliberately
   not filed as one here, because nobody has asked to publish it.
5. **`validate-workspace` aborts with a `UnicodeDecodeError` traceback on any `.md` file it
   cannot decode, and was reported rather than patched.** This is a defect in the pipeline's own
   machinery, not in mdtab: `workspace-valid` is a hard gate of every skill, so one such file
   stops the whole pipeline with a stack trace rather than a finding. It is recorded in
   ADR-0006's `## Consequences` and in this item's journal, and `implement` was right not to
   patch `.claude/agile-skills/scripts/` from inside a work item — the edit would be invisible to
   a reviewer of mdtab, covered by no criterion, and discarded by the next toolkit install.
6. **Concurrency, large inputs and pathological documents are unexercised.** No criterion
   mentions them; the largest document run through the tool in either verification was 27 lines.

## Verdict

**Accepted — merged into `main` and closed as `delivered`.**

Fifteen of fifteen criteria met, each demonstrated by a command `verify` ran on documents written
for the purpose rather than on the developer's own fixtures; 22 negative and boundary conditions
triggered; 13 mutations confirming the suite fails when the behaviour it names is removed. All
four findings of the first review are independently confirmed closed, including the two false
claims that caused the rejection. All twelve Definition of Done criteria pass. The trial merge was
clean and both gate commands pass on the merge result.

What this item delivers is the whole of mdtab except one feature: a stdin-to-stdout filter that
lays out the pipe tables it fully understands, copies through byte-for-byte everything it does
not, and never writes to stderr. Alignment markers are preserved but not yet honoured — that is
WI-0002, which now inherits an AC12 that is correct about the arithmetic it will build on, and an
architecture overview that says where a column's width is decided.

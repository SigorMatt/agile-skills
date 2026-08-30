# Review — WI-0003

## What I examined

**The record.** `item.md` (all eleven criteria and the `## Notes`), `history.md` (eight rows),
`journal.md` in full (nine entries), `plan.md`, `impl-report.md`, `verify-report.md`, and both
questions `Q-001` and `Q-002` including their `## Consequences` and `## Cross-answer check`
sections.

**The mechanics, run rather than assumed.**

- History chains without a gap — `— → draft → awaiting-answer → draft → ready → planned →
  in-progress → verifying → in-review` — and its last row matches `item.md`'s `status: in-review`.
- Nine journal entries against eight history rows. The two extra are `answer-questions` executions
  at `23:54:48Z` and `00:04:11Z` that transitioned nothing — legal, and both are executions a
  reader can examine. Every history row has an entry at its timestamp; `plan`'s pair differ by one
  second because the transition and the entry are written by the same command.
- `check-verify-freshness WI-0003 wi/WI-0003` → exit 0: *"verified at a93db5fe; wi/WI-0003 has
  moved to dea2b535 but only the record changed (5 file(s) under tracker/ or docs/), so the
  verification still covers the code"*.
- `check-commit-refs WI-0003 wi/WI-0003` → exit 0, *"all 4 commit(s) on main..wi/WI-0003 name
  WI-0003"*.
- Both questions are `answered`, `answered-by: human`, and their `## Consequences` name five real
  files each — ADR-0008, ADR-0007 v2, `docs/product/vision.md` v7, `item.md` and
  `refinement-qa.md`, all of which exist.

**The diff, hunk by hunk** — `main..dea2b53`, four hunks in `tests/test_mdtab.py` and two regions
in `mdtab.py`, plus sixteen new fixture files.

| hunk | serves | judgement |
|------|--------|-----------|
| `mdtab.py` module docstring: ADR-0005 marked superseded; ADR-0007, ADR-0008, ADR-0009 added to the rule-document list | plan step 4 | correct — all three files exist and say what the list says they say |
| `mdtab.py`: `_BREAK_TAG` and `has_break_tag` between `column_alignments` and `compose_row` | plan step 1, ADR-0009 decisions 1, 4 and 5 | correct. The pattern `<br\s*/?>` with `re.IGNORECASE` is exactly ADR-0008 decision 1's shape and no wider: `<`, `br` any case, any whitespace, optional `/`, `>` |
| `mdtab.py`: `compose_row` docstring gains the exception | plan step 3 | correct, and it cites the ADR that decided the rule |
| `mdtab.py`: `if has_break_tag(cell): before = 0` as the first branch of the chain | plan step 2, AC1–AC8 | correct. `pad` is computed before the branch, so an exempt cell is measured like any other; the `" " + ... + " "` shape is untouched; a cell with no tag reaches exactly the branch it reached before |
| `tests/test_mdtab.py` module docstring: names WI-0003 and its tag | plan step 6, ADR-0006 | correct |
| `tests/test_mdtab.py`: nine inputs appended to `INPUT_FIXTURES` | AC10 | correct, and it is the mechanism by which WI-0001 AC3, AC9, AC10 and WI-0002 AC8 come to range over break-tag content. Declared in `impl-report.md` |
| `tests/test_mdtab.py`: eleven criterion tests, one untagged predicate test, three module-level helpers | plan step 6 | correct; see `## Findings` for the one maintenance note |
| sixteen files under `tests/fixtures/` | plan step 5 | exactly the list plan step 5 names, no more |

`git diff main..HEAD -- tests/test_mdtab.py | grep "^-"` returns three lines, all of them
docstring. No existing assertion was deleted, weakened, renamed or moved. `column_alignments`,
`emit_block`, `split_cells`, `table_or_none`, `column_widths` and `compose_delimiter` are
byte-for-byte unchanged, which is what makes ADR-0009 decision 3 true rather than intended.

**The claims audit (D12), from the citations rather than from the prose.** Each sentence below was
read against the code it points at, opened for the purpose.

| claim | cited | what I opened | verdict |
|-------|-------|---------------|---------|
| ADR-0007 decision 1 — a marker decides where cell text sits | ADR-0005 | `compose_row`'s chain: RIGHT → `before = pad`, CENTRE → `pad // 2`, else 0 | true |
| ADR-0007 decision 2 — an odd centring remainder goes right | WI-0002/Q-001, EP-001/Q-004 | `before = pad // 2`, so `pad - before >= before` | true |
| ADR-0007 decision 3 — a cell containing a line break sits at the left | EP-001/Q-005, ADR-0008 | the new first branch, `before = 0` | true |
| ADR-0007 decision 4 — every **other** content cell is placed by decision 1 | EP-001/Q-005 | the branch is inside the per-cell loop and reads only `cell`; nothing column-wide was touched | true |
| ADR-0007 decision 5 — an unmarked column is laid out as ADR-0003 decision 9 says | WI-0002 AC4, ADR-0003 | the `else: before = 0` arm, unchanged | true |
| ADR-0007 decision 6 — the delimiter row is not reached | ADR-0004 | `emit_block`: `index == 1` routes to `compose_delimiter`, which never calls the predicate; and `_DELIMITER_CELL` is `^:?-+:?$`, which admits no `<` | true, and unreachable rather than merely untouched |
| ADR-0007 decision 7 — width and the two surrounding spaces unchanged | WI-0001/Q-001, WI-0001/Q-003, EP-001/Q-001 | `column_widths` unchanged in the diff; `pad` computed from `display_width(cell)` before the branch; `" " + ... + " "` intact | true |
| ADR-0008 decisions 1–3 — which cells are exempt, and that nothing else is | WI-0003/Q-001 | `_BREAK_TAG` and `has_break_tag`; no other predicate exists in the file | true |
| ADR-0008 decision 4 — an exempt cell is still padded, leftover after the text | WI-0003/Q-002 | `" " * before` with `before = 0`, then `" " * (pad - before)` after the text | true |
| ADR-0008 decisions 5–8 | ADR-0003, WI-0001/Q-001, WI-0001/Q-003, WI-0003/Q-002 | as above | true |
| ADR-0009 decisions 1–5 — where the exemption lives | mdtab.py:220, :244, :287, :143, :90 | the predicate sits between `column_alignments` and `compose_row`; the branch is first in the chain; `column_alignments` and `emit_block` are unchanged; the pattern is module-level; the predicate is given `rows[index]`, which came from `split_cells` | all five true |
| `docs/architecture/overview.md` v4 — the rule-document list, and "per cell inside `compose_row`, not by rewriting a column's alignment" | ADR-0007, ADR-0008, ADR-0009 | all three files exist; the sentence is true of the code as merged | true |
| `docs/product/vision.md` v7 lines 118–125 — the stakeholder's *"every row, every column, no exceptions"* | WI-0002/Q-001 | kept verbatim, with the following paragraph recording that its author narrowed it [src: EP-001/Q-005] | true, and correctly **not** repaired: it is their sentence, and ADR-0008 §3 forbids editing it |
| `docs/architecture/adr/ADR-0005` | — | header carries `status: superseded` and `superseded-by: ADR-0007` | true |

No claim was found that the delivered work made false, so nothing needed a version bump under D7
and nothing needed a `## Corrections` provenance repair under §4b. `lint-claims --context
work-item --changed-since main` exited 0; its scope is this item's own diff, which contains no
file under `docs/` — the audit above is therefore the substantive half and is recorded as such.

**The merge result.** Trial-merged on a detached worktree, `main` at `fbf9fce` both before and
after: `git worktree add --detach /tmp/wi3-trial main`, `git -C /tmp/wi3-trial merge --no-ff
wi/WI-0003` → trial HEAD `b6555e8`, `python3 -m unittest discover -s tests -t .` inside the trial
→ `Ran 37 tests in 7.884s` / `OK`, `python3 -m compileall ...` → exit 0. Worktree removed;
`git rev-parse main` unchanged.

**Reconstructibility, answered from the tracker, docs and `git log` alone.**

- *What was built and why:* `item.md` `## Story` and `## Notes` (the stakeholder's sign-off reply
  verbatim, and the supersession they authorised), `plan.md` `## Problem`, and four commits under
  `git log --grep WI-0003`.
- *Which decisions, by which skill:* ADR-0008 by `answer-questions` from `Q-001` and `Q-002`;
  ADR-0009 by `plan`, recording the siting and refusing the per-column shortcut; the two
  in-flight choices by `implement`, in its closing journal entry.
- *What questions arose and how they were resolved:* `Q-001` and `Q-002`, both to the human, both
  answered, both with `## Consequences` naming the five files each reached — and, upstream,
  `EP-001/Q-004` and `Q-005`, which is why this item exists at all.
- *What verification found:* `verify-report.md` — eleven passes against inputs written from the
  criteria, the twenty-one-row AC10 read, fourteen negative cases, six mutations, three
  discriminating cases, no defects.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c "^- \[x\] AC" item.md` → 11; `grep -c "^- \[ \] AC"` → 0 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | its `## Criteria` table gives each of AC1–AC11 a command and its quoted actual output; AC10's evidence is the twenty-one-row per-ID read |
| D3 | declared gates passed on the **final** state of the code | **pass** | the last code commit is `1100203`. `implement`'s gate run and `verify`'s both postdate it (`a93db5f` and after); `dea2b53` changes only `tracker/`. This review re-ran the suite and the linter on the merge result `b6555e8` |
| D4 | no open blocking question | **pass** | `Q-001` and `Q-002` both `status: answered`; `validate-workspace` reports 0 open |
| D5 | a journal entry per execution; history chains without a gap | **pass** | nine entries, eight rows, chain verified above; last row matches `item.md` |
| D6 | every design-changing decision is in an ADR cited from the plan or journal | **pass** | ADR-0009 (siting, and the refusal of option C) is cited from `plan.md` `## Approach`, `## Decisions and ADRs` and both `implement` journal entries; ADR-0008 (the rule) likewise. No decision was taken in code that is not in one of them |
| D7 | documents the change invalidated are updated, with a version bump and a change-log row | **pass, vacuously and deliberately** | the change invalidated none. ADR-0007 v2, ADR-0008 v1, ADR-0009 v1, overview v4 and vision v7 were all written for this item **before** the code and already describe it; each carries its own change-log row. Confirmed by the claims audit above rather than by memory |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → exit 0, 4 commits |
| D9 | merged into the trunk | **pass** | merged after this review closed the item — see `## Verdict` |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness` → exit 0, quoted above |
| D11 | `review.md` exists and states what was examined | **pass** | this file; `## What I examined` is its first and longest section |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, read against the code; absolute claims this execution wrote carry resolvable citations | **pass** | the fourteen-row claims audit above, each row opened from its citation; `lint-claims --context work-item --changed-since main` → exit 0 |

## Findings

None that block. Three recorded so they are not rediscovered:

1. **AC3, AC5 and AC8 quote expected tables whose exempt cells are their columns' widest.** For
   each, `W - w` is zero, so the quoted output is also what a filter with no exemption would
   produce, and those three criteria do not on their own detect the feature's absence. This is a
   property of the criteria as the stakeholder-facing statements agreed at refinement, not a
   defect in the code, and it is **not** grounds to edit a criterion. Both the implementation and
   the verification found it independently and both wrote discriminating cases —
   `impl-report.md` deviation 1 added one to AC3's test, and `verify-report.md`'s
   `## Test sensitivity check` ran one for each of the three. Accepted, and recorded here and in
   both reports.
2. **`widths_of` in `tests/test_mdtab.py` re-implements `column_widths`' rule** — max over the
   content rows, minimum 1 for a two-colon delimiter cell. The duplication is deliberate and
   documented in its docstring: calling `mdtab.column_widths` would make AC7 a tautology, which is
   the same reason `pipe_blocks` and `delimiter_cells` were duplicated for WI-0002. The cost is
   real: if ADR-0004 decision 2 ever changes, this helper must change with it or AC7 starts
   failing for the wrong reason. Accepted; the docstring is the mitigation and it names the ADR.
3. **The suite's wall time roughly doubled**, from about 4.7s to about 7.9s, because
   `INPUT_FIXTURES` grew from twenty to twenty-nine and four tests loop over it spawning a
   subprocess per fixture. Not a defect — the coverage is what AC10 asked for — but the growth is
   linear in fixtures times looping tests, and a future item adding another nine will notice.
   Recorded as an observation, no action.

No unrequested scope. No contradiction with any ADR. No defect belonging to another item, so no
bug filed.

## Accepted gaps

Each is declared in a report, and each already has a home that survives this item closing.

| gap | declared in | where it survives |
|-----|-------------|-------------------|
| the six spellings and five counter-examples are a sample of a pattern, not a proof | `verify-report.md` `## Not verified`; `plan.md` `## Assumptions` | `plan.md`'s assumption, which names the cost of reversing it. Verification widened the sample by six more cases and found no divergence |
| an exempt cell that also contains an escaped pipe (`\|`) is unconstrained | `impl-report.md` `## What I did not do`; `verify-report.md` `## Not verified` | `docs/product/vision.md` `## What is not yet decided` line 217, at the engagement level, and `item.md` `## Notes` under *"Deliberately unconstrained, and who left it so"*. It is WI-0001's open design question, not this item's |
| nothing asserts how a renderer displays the result | `verify-report.md` `## Not verified` | `item.md` `## Out of scope`, *"Checking that a renderer agrees"* |
| no performance requirement was measured | `verify-report.md` `## Not verified` | `ADR-0009` decision 4, which records that compiling the pattern once is a preference and not a measurement |
| a cell whose `<br>` is inside a code span or prose about HTML is exempt too | ADR-0008 `## Consequences`, ADR-0009 `## Consequences` | both ADRs, as a stated and accepted cost of a rule the stakeholder can predict without reading the code |

## Verdict

**Accepted.** The change does what WI-0003's eleven criteria ask, in the one place ADR-0009 says
it belongs, without touching anything that recognises a table, measures a column or composes a
delimiter row. The record is complete and reconstructible: nine journal entries, eight history
rows, two answered questions whose consequences name real files, and three ADRs that account for
every decision taken.

Closed `done`, `outcome: delivered`, and merged into `main` after closing — in that order, so
that `commits-reference-the-item` still had the branch's four commits to inspect.

The engagement is **not** ended by this execution. `engagement-state EP-001` reported `active`
with *"still in flight: WI-0003"* when this review began; closing WI-0003 brings EP-001 to rest,
and ending an engagement is its own dispatch on the epic, which the orchestrator makes at its
step 6. Nothing here presumes what the stakeholder will say to the sign-off question that dispatch
must file.

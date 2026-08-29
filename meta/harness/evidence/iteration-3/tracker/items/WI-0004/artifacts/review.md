# Review — WI-0004

Reviewed at 2026-08-29T08:02Z, against `wi/WI-0004` at `4a2f05c` and `main` at `2436a26`.

## What I examined

**The code, hunk by hunk.** `git diff main..wi/WI-0004` — fifteen files, of which two are
production. Every hunk was mapped to a criterion or a plan step before anything else was read:

- `mdtab/inline.py`, all 97 lines (plan step 1). The module docstring's two rules, `_backtick_run`,
  `_code_spans` and `contains_line_break`. I traced the regex `<br(?=[ \t/>])[^>]*>` against every
  spelling AC1 names and against the two lookalikes the plan's assumption 1 excludes: `<br>` and
  `<br/>` match through the `>` and `/` branches of the lookahead, `<br class="k">` through the
  space branch, `<brx>` fails the lookahead at `x`, and `</br>` cannot match because the pattern
  anchors on `<br` and `</br` offers no such position.
- `mdtab/table.py`, four hunks (plan step 2): one module-scope import, two docstring additions and
  the four changed lines in `_render_row`'s non-delimiter branch. I read the branch in place to
  confirm the delimiter row leaves through `_render_delimiter` on the other side of the same `if`
  and cannot reach the override.
- `tests/test_units.py` +113 (steps 3–4), `tests/test_fixtures.py` +8 (step 5), and the four
  fixture files, read as text rather than through the diff because `.gitattributes` marks fixtures
  binary. I checked `line-break-cells.out.md`'s arithmetic by hand: the column is 18 wide from
  `e<br class="k">f`, the header `what<br>it is` sits flush left with five columns after it, and
  the break-free `plain` row is `|      plain       |` — six before, seven after, which is the
  spare eleven split five/six and leaning left, exactly as `WI-0002/Q-001` settled it.
- `docs/architecture/overview.md` v8 → v9 (step 7): four "Planned for WI-0004, not yet in the
  code" sentences removed, one change-log row added, nothing else altered.

**The record.** `item.md` in full including every criterion and `## Notes`; `history.md`;
`journal.md` in full, all nine entries; `plan.md`; `impl-report.md`; `verify-report.md`; and all
four questions on the item with their `## Consequences`.

**The claims in `docs/`, from their citations rather than from the prose** (D12). Four absolute
claims that this item's work touched, each opened against the code it cites:

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| `mdtab/inline.py` is "the only inline markdown grammar the tool reads, kept out of `table.py` so the recognition rules cannot come to depend on it" | overview v9, modules table | `grep -rn "inline\|contains_line_break" mdtab/` → three hits: the import at `table.py:12`, the single call at `table.py:256`, and the module itself. `table.py:256` is inside `_render_row`; `lay_out`'s four recognition rules and all four of its `return None` paths execute before `_render_row` is ever called | **true** |
| the override "is decided at the same place the renderer is called and is per cell, so it moves no other cell of the column, and the delimiter row never reaches it" | overview v9, "Where a cell's content sits in its field" | `mdtab/table.py:248-258` — the override is inside the per-cell loop's `else` (non-delimiter) branch, computed from `text` alone; no column-level state is written | **true** |
| a column's width "does not depend on the *alignment* its marker declares" and nothing this item added measures anything new | overview v9 | `_column_widths` (`table.py:150`) is called before `column_alignments` in `lay_out` and takes neither an alignment nor the override; it is unchanged in the diff | **true** |
| "backtick runs must match in length, and nothing else about a span is modelled" | overview v9, "No markdown parser" paragraph | `_code_spans` (`inline.py:47`) — `run_end - cursor == length` is the only closing test; no space-stripping, no backslash handling | **true** |

**The engagement.** `scripts/engagement-state EP-001`, and the four `EP-001` questions bearing on
what the stakeholder has and has not accepted.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion checkbox ticked | **pass** | AC1–AC7 all `[x]` in `item.md`; `validate-workspace` → exit 0, 6 items, 12 documents |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | the report's `## Criteria` table gives each of AC1–AC7 a command `verify` ran and the actual output; no row cites `impl-report.md`, and AC1, AC3, AC6 and AC7 are additionally measured against a `git archive` copy of `main` |
| D3 | the declared gates passed on the **final** state of the code | **pass** | re-run by this review on the trial merge result `4de3f01`, not taken from a report: `python3 -m unittest discover -s tests -t .` → `Ran 84 tests … OK`, exit 0; `python3 -W error -m compileall -q mdtab tests` → exit 0; `lint-claims --changed-since main` → exit 0; `validate-workspace` → exit 0 |
| D4 | no open blocking question | **pass** | all four questions on the item are `status: answered`; nineteen question files across the workspace, none open |
| D5 | a journal entry per execution, history chaining without a gap | **pass** | nine journal entries against eight history rows; the extra entry is `answer-questions` at 07:37:45Z answering the non-blocking `Q-004`, which changed no status and so correctly has no row. The chain runs `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review`, and the last row's `in-review` matches `item.md` |
| D6 | every design decision in an ADR, cited from the plan or journal | **pass, with a finding** | ADR-0010 records the per-cell override, the module boundary, the tag and code-span rules, and the three cases `refine` left unconstrained; `plan.md`'s `## Decisions and ADRs` table cites it for each. Finding 2 below concerns the precision of one sentence in it, not the absence of a decision |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **FAIL** | `docs/architecture/overview.md` was updated correctly (v8 → v9, change-log row, four now-false sentences removed). `docs/product/vision.md` was **not**, and the branch makes four of its sentences false. Finding 1 below |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, "all 6 commit(s) on main..wi/WI-0004 name WI-0004" |
| D9 | merged into the trunk | **not reached** | the item is rejected, so no merge was made. The trial merge into a detached worktree of `main` was clean and was discarded; `git rev-parse main` returns `2436a261` before and after |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0004 wi/WI-0004` → exit 0: "verified at dff76004; wi/WI-0004 has moved to 4a2f05c4 but only the record changed (5 file(s) under tracker/ or docs/)". The two commits after `dff7600` touch only `tracker/` |
| D11 | `artifacts/review.md` states what was examined | **pass** | this document, `## What I examined` |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, checked against the code; absolute claims carry resolvable citations | **FAIL** | the `[auto]` half passes — `lint-claims --changed-since main` → exit 0, 1 document. The read does not: the four claims in the table above are true, and `docs/product/vision.md` `## Open at the time of writing` is false in four places. Finding 1 |

Two criteria fail, both on the same document. Everything else passes.

## Findings

### 1. `docs/product/vision.md` still says this behaviour is not built — send-back (D7, D12)

`docs/product/vision.md` is at v8, `updated-for: WI-0004`, and its `## Open at the time of
writing` section describes the branch's behaviour as absent. Four statements become false the
moment `wi/WI-0004` merges:

- line 136 — *"**One behaviour is wanted and is not built.**"*
- line 142 — *"Today mdtab does not know a cell can contain a line break: it measures `a<br>b` as
  an ordinary run of characters and pads it according to the column's marker like anything else,
  so under `:---:` it is centred and under `---:` it is pushed right."*
- line 144 — *"The change is filed as [src: WI-0004], at `ready`"*
- line 164 — *"The behaviour is still wanted and still not built; what changed is that nothing
  about *what it should do* is now waiting on the stakeholder."*

Checked against the merge result rather than argued: on `4de3f01`,

```
$ printf '| heading is long | b |\n|:---:|---:|\n| a<br>b | x |\n' | python3 -m mdtab
| heading is long | b |
|:---------------:|--:|
| a<br>b          | x |
```

— the cell is neither centred nor pushed right, so line 142's sentence describes a tool that no
longer exists, and lines 136, 144 and 164 describe a state of the work that ended at 07:53Z.

This is not a nit about tense. `vision.md` is the one document in the workspace written for the
stakeholder, and `EP-001` reaches rest the moment this item closes — so the very next thing that
happens is a sign-off question putting the delivered engagement in front of them while the
product document tells them the thing they withheld sign-off for was never built. It is also
exactly the pattern `review-close` recorded on WI-0003 and that `plan` cited in its own decisions
table: *"`plan` has no step for updating the documents a change invalidates"*. `plan` wrote step 7
for `overview.md` and did not name `vision.md`; `implement` executed step 7 faithfully and
reported it as done, which it was. The gap is in the plan's coverage, not in anyone's execution
of it, and no gate below this one could catch it — `lint-claims` proves a citation resolves, not
that a sentence is true.

**What has to happen.** `docs/product/vision.md` goes to v9 with a change-log row, and its
`## Open at the time of writing` section stops describing the line-break rule as outstanding:
what the stakeholder asked for in `EP-001/Q-005` is built, `WI-0004` is delivered, and the
transcript in the section shows what the tool does now rather than what it used to do. The four
quoted answers below it (`Q-001` to `Q-003`) remain true and should stay. The v8 change-log row at
line 187 is a record of a past version and must **not** be rewritten — it correctly describes what
v8 said at the time.

### 2. ADR-0010 §2 rule 2 overstates what the code does — accepted gap

Rule 2 of the decision reads *"Code spans are found first and their contents, delimiters included,
are excluded from the search."* `contains_line_break` does something slightly narrower: it finds
the spans, then takes a tag match when the match's **start index** lies outside every span. The two
readings differ on one shape — a tag that begins outside a span and ends inside one, such as
`` a<br `>` b `` — which the implemented rule counts as a line break and a blank-the-spans reading
would not.

`implement` declared this as deviation 1 and `verify` checked rather than accepted it, confirming
that every case AC1, AC7 and ADR-0010 §3 name answers identically either way. So no criterion
turns on it and nothing shipped is wrong.

**Accepted as a gap, not a send-back**, for two reasons: no acceptance criterion distinguishes the
readings, and correcting the sentence in a standing decision is the architect's act rather than the
reviewer's or the developer's. ADR-0009 provides the route if it is judged false rather than
merely imprecise — correction in place, `status: accepted` retained, the old sentence quoted in
full in the change log. Recorded in the item's `## Notes` so it survives this item, per the
requirement that an accepted gap not live only inside a report.

### 3. `item.md`'s acceptance-criteria preamble was stale — fixed by this review

The `## Acceptance criteria` section opened with *"**Partly refined — round 2 must finish them.**
… What is still not decidable by someone with a terminal and no context is AC5, which names no
test. `refine` round 2 names them, completes the R10 table …"*. That stopped being true at
07:36:01Z, when `refine` round 2 finished: AC5 now names twenty tests individually, the R10 table
is complete, and `refinement-qa.md` is `status: recorded` — all of which the item's own
`### Refinement round 2 — what it finished` section says two screens further down, contradicting
its own preamble.

Rewritten to the past tense by this review. It is not an acceptance criterion and no criterion was
touched, weakened or made easier to pass; the seven criteria are byte-identical to what `verify`
checked. The change is recorded here and in the journal because a reviewer editing the item under
review should never be something a reader has to discover from a diff.

## Accepted gaps

- **Finding 2**, ADR-0010 §2 rule 2's phrasing against the implemented start-index rule. Written
  into `item.md` `## Notes`.
- **The `<br` + code span + `>` shape itself**, named in `impl-report.md` deviation 1 and in
  `verify-report.md` `## Not verified, and why`. No criterion decides it and ADR-0010 §3 does not
  reach it. It is the same subject as finding 2 and is carried by the same `## Notes` entry.
- **`grep -rniE '<br' tests/` no longer exits 1.** AC5 quotes it as evidence about the *trunk*, and
  the plan's risk 3 predicted this. The branch's evidence for AC5 is the diff — `0` removed lines
  across both test files, and each of the twenty named tests absent from the diff — which is what
  `verify` measured. Not a gap in the delivery; recorded so that a later reader who re-runs the
  command is not misled by it.
- **Rendering, performance, large inputs and Python versions other than 3.12**, all declined as
  work by the stakeholder in `EP-001/Q-004` and correctly not measured.

## Verdict

**Rejected — back to `in-progress`.**

The change itself is right. Every acceptance criterion is met on evidence I re-ran rather than
read, the diff contains no hunk that no criterion accounts for, the two production files are the
two the plan named, no existing test was altered, and the merge result passes 84 tests and the
lint. Findings 2 and 3 are disposed of above and neither blocks anything.

What blocks it is finding 1, and it blocks it on a Definition of Done criterion rather than on a
preference: D7 requires the documents this change invalidated to have been updated, and D12
requires the claims in `docs/` about the behaviour this item touched to still be true. One
document fails both, and it is the document the stakeholder reads. Closing over it would put a
false statement in front of them in the same hour they are asked to accept the engagement it is
false about.

The remedy is one document, one section, one version bump and one change-log row. No code changes,
so `verify` will find the same commit it verified — but the item must return through `verifying`
in the normal way, because the branch will have a new commit on it and D10 is measured, not
judged.

---

# Second review — WI-0004, 2026-08-29T08:17Z

Against `wi/WI-0004` at `70ef172` and `main` at `2436a26`. Everything above stands as the record of
the **first** review, which rejected the item at 08:04:33Z; its finding numbers are cited from the
item's `## Notes` and are not reused here. This section reviews what came back, and it re-decides
the Definition of Done in full rather than carrying the first review's ticks forward.

## What I examined

**The remedy, hunk by hunk.** `git diff main..wi/WI-0004 -- docs/product/vision.md` — five hunks,
which are the whole of what changed since the send-back (`git diff 4a2f05c..70ef172` touches
`docs/product/vision.md` and `tracker/` and nothing else):

- the front-matter block: `version: 8 → 9`, `updated-by: answer-questions → implement`, a new
  `updated` stamp. `updated-for` was already `WI-0004`.
- `## What it does`, the markers paragraph. The `WI-0002/Q-001` quotation — *"every row, every
  column, no exceptions"* — is kept as what the stakeholder asked for first and what the tool does
  for every ordinary cell, and the one exception is stated after it with its citations. This hunk
  was **not** in the review's finding 1; `implement` found it while fixing what was, and it is a
  real second instance of the same falsehood. Reported as its deviation 2.
- `## Open at the time of writing`, opening: *"One behaviour is wanted and is not built"* → *"The
  one behaviour that was wanted is now built"*, with a transcript of what the tool prints.
- the same section's closing paragraph: *"still wanted and still not built"* → what is open is the
  acceptance, not the behaviour.
- the change-log table: a v9 row naming both false statements, quoting them, and recording that
  the send-back was on D7 and D12. The v5–v8 rows are untouched, which is right — they record what
  those versions said at the time, and the first review said so explicitly.

**The code, again, not on trust.** `git diff main..wi/WI-0004 -- mdtab/` is byte-for-byte what the
first review read — `git diff dff7600..70ef172 -- mdtab/ tests/` is empty — but the mapping was
re-made rather than assumed: `mdtab/inline.py` (plan step 1) and the four hunks of `mdtab/table.py`
(one import, two docstrings, the four changed lines of `_render_row`'s non-delimiter branch, plan
step 2); `tests/test_units.py` +113 (steps 3–4); `tests/test_fixtures.py` +8 and the four fixtures,
read as text because `.gitattributes` marks fixtures binary (step 5); `docs/architecture/overview.md`
v8 → v9 (step 7). No hunk serves no criterion and no plan step.

I checked the one thing a second reviewer can add to the first's reading, and it is the claim v9
now makes in the stakeholder's document: that the exception is **one** exception.
`grep -n alignment mdtab/table.py` on the merge result gives exactly one site where a cell is
placed by anything other than `alignments[column]` — `table.py:256`,
`"left" if contains_line_break(text) else alignments[column]` — and
`grep -rn "inline\|contains_line_break" mdtab/` gives three hits: the module, the import at
`table.py:12` and that one call. So `contains_line_break` has exactly one caller, it is inside
`_render_row`, and `lay_out` calls `_render_row` only after recognition has finished.

**Four criteria re-run at a terminal, from their own wording**, against the working tree at
`70ef172` — AC3's three-row centred column (`|      aa      |`, `| a<br>c       |`,
`|      bb      |`, marker `:------------:` unchanged), AC6's header (`| a<br>b         | second
column |`), AC7's code span (`|          `<br>` | x |`), and AC4 on the AC3 document (exit 0,
stderr 0 bytes, second run `cmp`-identical to the first). Each is the row its criterion requires.

**The record.** `item.md` in full; `history.md` — eleven rows, chaining without a gap, last row
`in-review` matching `item.md`; `journal.md` in full, twelve entries; `plan.md`; `impl-report.md`
including its second-execution section; `verify-report.md`, which is the **second** verification
and says so; and all four questions with their `## Consequences`.

**The claims in `docs/`, from their citations** (D12). The four `overview.md` claims the first
review opened are unchanged in this diff and stand as recorded there. The claims `vision.md` v9
**adds** are new since that audit, and each was opened against the thing it cites:

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| a cell holding a `br` tag "is placed as if its column were left-aligned, whatever marker the column carries, and the padding follows the text" [src: WI-0004 AC1; src: ADR-0010] | vision v9, "Open at the time of writing" | the merge result `f33c73b`, run on the AC1 document under `:---:`, under `---:` and under `:---`: `\| a<br>b          \| x \|` all three times, byte-identical | **true** |
| the transcript v9 prints under `:---:` | vision v9 | the same three lines from the merge result, `\| heading is long \| b \|` / `\|:---------------:\|--:\|` / `\| a<br>b          \| x \|` | **true, byte-for-byte** |
| "Before … that last row came back `\|     a<br>b      \| x \|` under `:---:` and `\|          a<br>b \| x \|` under `---:`" | vision v9 | a `git archive main` copy of the trunk in a scratch directory, run on both documents | **true** — both rows reproduced exactly, so the past tense is measured rather than remembered |
| the markers are honoured in every column "with one exception the stakeholder asked for afterwards" | vision v9, "What it does" | `mdtab/table.py` — `table.py:256` is the only place a cell's alignment is anything but its column's, and `contains_line_break` has exactly one caller | **true** — one exception, not "at least one" |
| "Every item in this engagement has been built" | vision v9, closing paragraph | `tracker/board.md` and each `item.md`: BUG-0001, WI-0001, WI-0002, WI-0003 `done`; WI-0004 at `in-review` and closed by this execution | **true** as of this close |
| ADR-0010 is not contradicted by the code | ADR-0010 §1–§3 read against `mdtab/inline.py` and `_render_row` | §1's per-cell override at the render call site, §2's tag and span rules, §3's three edge cases — each matched to a line of code and to a test | **consistent**; the one imprecision is the accepted gap recorded in the item's `## Notes` |

**The engagement.** `scripts/engagement-state EP-001` → `EP-001 active — still in flight: WI-0004`.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion checkbox ticked | **pass** | AC1–AC7 all `[x]` in `item.md`; `validate-workspace` → exit 0, 6 items, 12 documents |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | the second report's `## Criteria` table gives each of AC1–AC7 a command `verify` ran against `a64ec3e` and quotes its output; AC1, AC3, AC6 and AC7 are additionally measured against a `git archive main` copy. No row cites `impl-report.md` or the first verification. I re-ran AC3, AC4, AC6 and AC7 myself and got the rows the criteria require |
| D3 | the declared gates passed on the **final** state of the code | **pass** | re-run by this review on the trial merge result `f33c73b`, not taken from a report: `python3 -m unittest discover -s tests -t .` → `Ran 84 tests in 0.150s … OK`, exit 0; `python3 -W error -m compileall -q mdtab tests` → exit 0; `lint-claims --changed-since main` → exit 0, 2 documents; `validate-workspace` → exit 0 |
| D4 | no open blocking question | **pass** | all four questions on the item are `status: answered` with `## Consequences` naming files that exist; nineteen question files across the workspace, none open |
| D5 | a journal entry per execution, history chaining without a gap | **pass** | twelve journal entries against eleven history rows; the extra is `answer-questions` at 07:37:45Z answering the non-blocking `Q-004`, which changed no status and correctly has no row. The chain runs `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review → in-progress → verifying → in-review`, and the last row matches `item.md` |
| D6 | every design decision in an ADR, cited from the plan or journal | **pass** | ADR-0010 records the per-cell override, the module boundary, the tag and code-span rules and the three unconstrained cases; `plan.md`'s `## Decisions and ADRs` table cites it for each, and the three assumptions it does not raise to an ADR say what reversing them costs. The second execution added no design decision — it changed one document |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **pass** | this is the criterion that failed. `docs/architecture/overview.md` v8 → v9 with a change-log row (plan step 7). `docs/product/vision.md` v8 → **v9** with a change-log row naming both false statements and quoting them. Both false claims are gone, checked by reading the rendered sections rather than the diff, and no other document in `docs/` mentions the placement of a cell's content: `grep -rlniE 'line break\|<br' docs/` gives `vision.md`, `overview.md` and `ADR-0010`, and the ADR describes a decision rather than a state of the code |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0004 wi/WI-0004` → exit 0, "all 10 commit(s) on main..wi/WI-0004 name WI-0004" |
| D9 | merged into the trunk | **pass** | trial-merged into a detached worktree of `main` first (`f33c73b`), tested there, discarded; `git rev-parse main` returned `2436a261` before and after. Merged for real after this item was closed, per the procedure's order |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0004 wi/WI-0004` → exit 0: "verified at a64ec3ef; wi/WI-0004 has moved to 70ef172e but only the record changed (5 file(s) under tracker/ or docs/)". And the verification that ran is the **second** one: `git diff dff7600..a64ec3e -- mdtab/ tests/` is empty, so `verify` re-measured the same code after the document was fixed rather than inferring from the first pass — which is what it says it did, entry of 08:13:03Z |
| D11 | `artifacts/review.md` states what was examined | **pass** | this section's `## What I examined`, and the first review's above it |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, checked against the code; absolute claims carry resolvable citations | **pass** | the `[auto]` half: `lint-claims --changed-since main` → exit 0, 2 documents. The read: the five new `vision.md` claims in the table above, each opened against the tool or the trunk copy and each true, plus ADR-0010 read against the code. The two sentences that failed this criterion at 08:04Z are gone and their replacements were measured, not argued |

Twelve criteria, twelve passes.

## Findings

### 4. `vision.md` v9 says the stakeholder "have not yet been asked" — true now, false the moment the engagement is ended

`## Open at the time of writing` closes:

> *"They have not yet been asked whether they accept the engagement as it now stands — they
> withheld sign-off on 2026-08-29 pending exactly the behaviour above [src: EP-001/Q-005], and the
> ending they were promised, "Fix that and we are done", is theirs to give."*

That is true at this close: `scripts/engagement-state EP-001` reports `active`, WI-0004 is the
child still in flight, and no sign-off question has been filed since the last one was answered at
07:21Z. It stops being true the moment `review-close` is dispatched on **EP-001** — which is the
very next thing the orchestrator will do, because closing this item is what puts the engagement at
rest — and files the `kind: sign-off` question.

**Not a defect in this item, and not a send-back.** D12 asks whether the claims about the behaviour
*this item touched* are true, and this sentence is about the state of the engagement, not about
what the tool does. It is recorded because this document has now cost two send-backs on D7 and D12,
both for describing a state of the work that had moved on, and the execution that ends the
engagement will have to bump `vision.md` again for exactly the same reason. Written into the item's
`## Notes` so it survives this close, and named here so the epic's `review-close` meets it before
its own DE6 audit does.

### 5. One rewrapped line in `vision.md` — recorded, not fixed

The `## What it does` hunk left a 141-column line (`vision.md:61`) where the document's prose is
otherwise wrapped near 95; it is the join between the new exception sentence and the sentence about
a centred cell's odd column that follows it. `awk 'length > 100'` over the file gives that line and
three pre-existing list items at 101–103 that came from `main`, so it is the only new outlier.

Cosmetic, no criterion and no gate covers it, and it is left alone deliberately: fixing it would put
a reviewer's commit on a document the stakeholder reads, after verification, for no change in what
the document says. Recorded so a later editor of the paragraph knows it was seen rather than missed.

## Accepted gaps

Unchanged from the first review, and re-checked rather than carried:

- **ADR-0010 §2 rule 2's wording against the implemented start-index rule** (first review's finding
  2), already written into `item.md` `## Notes` with ADR-0009 named as the route if it is judged
  false rather than merely broader. `verify`'s boundary case 11 triggered the one shape that parts
  the two readings and recorded what the code does with it.
- **The `<br` + code span + `>` shape** itself — no criterion and no clause of ADR-0010 decides it.
  Same `## Notes` entry.
- **`grep -rniE '<br' tests/` no longer exits 1.** AC5 quotes it as evidence about the *trunk*; the
  branch's evidence for AC5 is the diff — 0 removed lines across both test files and each of the
  twenty named tests absent from it — which is what `verify` measured, twice.
- **Rendering, performance, large inputs and Python versions other than 3.12**, declined as work by
  the stakeholder in `EP-001/Q-004` and correctly not measured.
- **New, from this review:** finding 4 above, recorded in `## Notes`. Finding 5 is a nit, not a gap.

## Verdict

**Accepted. Merged into `main` and closed, `outcome: delivered`.**

The send-back was remedied and then some: the review named one false statement in
`docs/product/vision.md` and `implement` fixed two, the second being the *"no exceptions"* sentence
in `## What it does` that this item's own rule made false. Both replacements were measured against
the tool and against a copy of the trunk rather than written from memory, and I reproduced both
measurements. Every Definition of Done criterion passes on evidence re-run for this review, the
merge result is green on 84 tests and the lint, `main` did not move during the trial, and the diff
contains no hunk that no criterion or plan step accounts for.

`scripts/engagement-state EP-001` reports `active` while this item is in flight, so this execution
does not end the engagement: it closes the child. The epic reaches rest at this close, and the
orchestrator's step 6 dispatches `review-close` on `EP-001` to put the sign-off to the stakeholder —
who asked for exactly this behaviour and said *"Fix that and we are done"*.

## Addendum — procedure step 10, after the close (2026-08-29T08:23Z)

The verdict above says `scripts/engagement-state EP-001` reported `active` and that this execution
therefore ends no engagement. That was the state **before** WI-0004 was closed, which is when it
was written. Closing the item is what put the engagement at rest, and step 10 of this skill's
procedure is reached after step 9, so the same execution ran the script again:

```
$ scripts/engagement-state EP-001
engagement-state: EP-001 at-rest
  - every child has stopped, no question is open, no request is open
  rest reached at 2026-08-29T08:20:20Z
```

At rest, with no sign-off filed since rest was reached, the procedure says to ask. So this
execution also filed `tracker/items/EP-001/questions/Q-006.md` — `kind: sign-off`, naming all five
children — and suspended EP-001 to `awaiting-answer` with `resume-to: open`. The record of that is
on the **epic's** journal, where it belongs; it is noted here only because the paragraph above
would otherwise read as though the engagement had been left running.

**Finding 4 was acted on, not merely recorded.** Filing `Q-006` is exactly the act that made
`docs/product/vision.md` v9's *"They have not yet been asked"* false, so v9 did not survive this
execution: the document is at **v10**, the paragraph says they have been asked and have not yet
answered, and a change-log row records it. `review-close` wrote it rather than sending it back,
because the item that would have carried the fix is the one just closed and the sentence was made
false by this execution's own act — there was no send-back available that would not have been a
fiction. The edit is declared here, in the epic's journal, and in the change-log row itself.

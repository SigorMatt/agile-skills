# Review — WI-0003

Second review of this item. The first, at `fb43b93`, **rejected** it on D7 and D12 — the change
was right and two documents still described the tool as it was before it. This review re-examines
everything, not only the three edits that answered the rejection: a send-back is not a licence to
re-read a subset next time.

## What I examined

- `item.md` — all ten criteria and their tick state; `history.md` — **thirteen** rows read as a
  chain, `— → draft → awaiting-answer → draft → ready → planned → in-progress → awaiting-answer →
  in-progress → verifying → in-review → in-progress → verifying → in-review`, no gap, last row
  matching `item.md`; `journal.md` — thirteen entries, one per history row, each with a
  `**Status:**` bullet agreeing with its row.
- `questions/Q-001.md` (human, answered 2026-08-28T21:13:13Z) and `questions/Q-002.md` (architect,
  answered from the record) — both `## Consequences` blocks opened and every file they name checked
  to exist and to carry the change.
- `artifacts/plan.md` (eight steps as amended, the AC mapping, the decision-routing table),
  `artifacts/impl-report.md` (both executions, three declared deviations, four declared omissions,
  a fifth deviation section for the send-back), `artifacts/verify-report.md` (the **second**
  verification, ten verdicts, six gates, six declared gaps).
- **The diff itself**, `main..f1d5f0a`, hunk by hunk: `git diff main..HEAD -- mdtab/`,
  `-- tests/test_units.py tests/test_fixtures.py`, `--name-status -- tests/fixtures/`, and
  `-- docs/`. Every hunk mapped; the map is in `## Findings`.
- **The seven new fixture pairs, opened under `cat -A` and re-derived by hand** from AC2, AC3, AC5
  and AC6 rather than from the code — see finding F4.
- `ADR-0003` (header: `status: superseded`, `superseded-by:` pointing at the file that exists) and
  `ADR-0008` (header, `## Context`, all four rules, `## Consequences`) — opened, not recalled.
- `docs/architecture/overview.md` v5 and `docs/product/vision.md` v5 **in full**, for D7 and for
  the D12 audit below.
- A trial merge into a **detached** worktree of `main`, with the project's test and lint commands
  run on the merge result.

### The D12 claims audit — each claim decided by opening what it cites

Twelve absolute claims about the behaviour this item touched, in the two documents the last review
rejected. For each, the cited thing was opened, or the command was run, and the verdict taken from
what came back — never from the sentence and never from a neighbouring document repeating it.

| # | claim | what I opened or ran | verdict |
|---|-------|----------------------|---------|
| 1 | `overview.md:30` diagram, "parse and test the four recognition rules `[ADR-0008]`" | ADR-0008 — `status: current`, and its `## Decision` enumerates rules 1–4 | **true**; the superseded attribution that was finding F2 last cycle is gone |
| 2 | `overview.md:41` "…anything nobody has thought of — arrives at that one branch `[src: ADR-0008]`" | ADR-0008 `## Consequences`, "the copy-through branch"; `mdtab/table.py:lay_out`, which has exactly one `return None` path per rule | **true**, and now cited to the live record |
| 3 | `overview.md:105-108` "`[src: ADR-0008]` **replaced** the byte-identical prefix rule with a shared-prefix one: a run is recognised when its lines' indents share a longest common prefix and every line's remainder past it is spaces `[src: mdtab/scan.py]`" | `mdtab/scan.py:shared_prefix` — longest common prefix over `line_prefix` values, then `if prefix[len(shared):].strip(" "): return None` | **true**, clause for clause |
| 4 | `overview.md:109-111` "mdtab therefore recognises the bare right-aligned table its own layout emits, and running it twice is once again the same as running it once in the stronger sense `[src: WI-0003 AC2; src: WI-0003 AC4]`" | ran `printf '   a \| bbbbb\n----:\|--\nxxxx \| y\n' \| python3 -m mdtab` → re-aligned, and twice → a fixed point | **true**; this is the sentence the last review found false, and it is now true because the code it describes is the code that ran |
| 5 | `overview.md:113-117` "a table written without outer bars whose rows carry different numbers of leading spaces is **now** laid out where it **used to be** left alone, and comes back at the prefix its lines share — for a run at the left margin, the start of the line `[src: WI-0003/Q-001; src: WI-0003 AC5]`" | ran `printf '  a \| b\n---\|---\n  ccc \| d\n' \| python3 -m mdtab` → `a   \| b` / `----\|--` / `ccc \| d` | **true**, tense included |
| 6 | `overview.md:117-118` "A run whose lines differ by a **tab** or by a `>` is still not a table and is still copied through untouched `[src: WI-0003 AC6]`" | ran both AC6 documents through `diff` → identical | **true** |
| 7 | `overview.md:91` section title "A property the tool lost and **got back**" | the same runs as 4 | **true**; this is finding F1 of the last review, cleared |
| 8 | `overview.md:71-76` "What a run's indent is — one function taking the whole run"; "Whether a run is a table — one predicate" | `mdtab/scan.py:shared_prefix` (one function, takes `contents`); `mdtab/table.py:lay_out` (one predicate, returns the run or `None`) | **true**, unchanged from the last review's audit |
| 9 | `vision.md:38-40` "one whose rows disagree about how many cells they have, about their outer pipes, or about their indentation **in a way it cannot make sense of**. Such a table comes back exactly as it went in" | ran the three refusal classes — ragged rows, mixed outer pipes, tab/quote-depth indentation — all byte-for-byte | **true**; the unqualified "about how far they are indented" that was finding F3 is gone |
| 10 | `vision.md:44` "it never adds or removes a `\|` … `[src: ADR-0008]`" | ADR-0008, which carries the punctuation promise forward unchanged from ADR-0003 | **true**, and the citation is no longer stale |
| 11 | `vision.md:46-55` the stakeholder quotation, *"a table with two spaces on one row and none on the next isn't tangled — it's just untidy, which is the exact thing I wanted the tool for. Tabs and the quote marks having to match exactly sounds right to me"* `[src: WI-0003/Q-001]` | `questions/Q-001.md` `## Answer` | **verbatim and contiguous**, not paraphrased and not stitched from two places |
| 12 | `vision.md:101-107` "The question this section carried at v4 … was put to the stakeholder as `[src: WI-0003/Q-001]` and answered on 2026-08-28, and **its premise did not survive the answer**" | `Q-001.md` — `status: answered`, `answered-by: human`, `answered-at: 2026-08-28T21:13:13Z`, and an answer that reverses the premise | **true**; this is finding F3's third limb, cleared |

`scripts/lint-claims --changed-since main` now reports `checked 2 document(s) changed since main`,
0 errors — non-vacuous for the first time on this item, because this branch is the first to change
a document. The vacuity recorded in the last review is unchanged as a fact about the earlier
executions and is carried into `item.md` `## Notes` so it survives the close.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | `grep -c '^- \[ \]' item.md` → 0; all ten are `[x]` |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | its `## Criteria` table gives, for each of AC1–AC10, a command the second verification ran and the actual output; AC1 is expanded into five clause probes and AC9 into a four-test reconciliation. No row cites `impl-report.md` |
| D3 | gates passed on the final state of the code | **pass** | `implement`'s seven on `2c39bc4`; `verify`'s six on `63e072d`; and re-run here on the **merge result** `336e359`: `python3 -m unittest discover -s tests -t .` → `Ran 71 tests`, `OK`, exit 0, and `python3 -W error -m compileall -q mdtab tests` exit 0. `git diff 2c39bc4..f1d5f0a -- mdtab/ tests/` is empty, so no code postdates the gates |
| D4 | no open blocking question | **pass** | `Q-001` and `Q-002` both `status: answered`; each `## Consequences` opened and every file it names exists and carries the change |
| D5 | a journal entry per execution, history chains | **pass** | thirteen history rows, thirteen journal entries, `**Status:**` bullets agreeing row for row; last row `verifying → in-review` matches `item.md` |
| D6 | design decisions in an ADR, cited | **pass** | ADR-0008 records rule 2's reversal, restates rules 1, 3 and 4 unchanged, and supersedes ADR-0003 — which carries `status: superseded` and a `superseded-by:` path that resolves. Cited from `plan.md` `## Decisions and ADRs` and from the `plan` journal entry |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **pass** | `overview.md` 4 → **5**, `updated-by: implement`, `updated-for: WI-0003`, change-log row 5 naming what it corrected and that review sent it back; `vision.md` 4 → **5**, likewise. This is the criterion that failed last cycle; the three sentences named in `review.md`'s F1/F3 are rewritten and the four stale ADR-0003 citations are moved |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → `all 11 commit(s) on main..wi/WI-0003 name WI-0003`, exit 0 |
| D9 | merged into the trunk | **pass** | trial-merged detached at `336e359` and green; trunk confirmed still `2884f53f` after the trial was discarded; the item is closed **before** the real merge, so `commits-reference-the-item` still had a non-empty range to inspect |
| D10 | verification postdates the code | **pass** | `check-verify-freshness WI-0003 wi/WI-0003` → "verified at `63e072d3`; `wi/WI-0003` has moved to `f1d5f0ac` but only the record changed (5 file(s) under `tracker/` or `docs/`)", exit 0 |
| D11 | the review record states what was examined | **pass** | this file; `## What I examined` is first and lists the artifacts, the diff ranges, the fixtures opened, and the twelve claims with what was opened for each |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass** | the twelve-row audit above, each decided from the cited thing or from a command. `lint-claims --changed-since main` → `checked 2 document(s)`, 0 errors, 0 warnings, exit 0 |

## Findings

### The hunk map

Every hunk in `main..f1d5f0a` traces to a plan step, an acceptance criterion, or the last review's
finding list. Nothing in the diff serves none of them.

| hunk | traces to |
|------|-----------|
| `mdtab/scan.py` — `shared_prefix` and the module docstring's new paragraph | plan step 1; AC1 |
| `mdtab/table.py` — `from mdtab.scan import shared_prefix`, rule 2's four lines in `lay_out` | plan step 2; AC1 |
| `mdtab/table.py` — `has_leading_pipe`, `_outer_style`, `lay_out` docstrings | `impl-report.md` deviation 1; `has_leading_pipe`'s is the sentence AC7's argument rests on and it said "its AC15 prefix", which is now the run's |
| `tests/fixtures/` — fourteen files, all `A` | plan step 3; AC2, AC3, AC5, AC6 |
| `tests/test_fixtures.py` — `ALIGNED` and `UNTOUCHED` entries | `impl-report.md` deviation 2; the maps are hand-written, so a new laid-out fixture must be enrolled or it is checked against the wrong rule |
| `tests/test_fixtures.py` — `without_indent` and `test_ac11_…` | plan step 7, added by `answer-questions` answering `Q-002`; AC9 entry 2 |
| `tests/test_units.py` — `SharedPrefixTest` | plan step 4; AC1 |
| `tests/test_units.py` — `test_ac10_…`'s final assertion and docstring | plan step 5; AC9 entry 1, AC2 |
| `tests/test_units.py` — the rule 2 → rule 4 relocation and its comments | plan step 6; AC7, AC9's "unchanged in substance though it moves" |
| `tests/test_units.py` — module and `RejectionTest` docstrings, `ADR-0003` → `ADR-0008` | **not a plan step** — the last review's finding F4. See F3 below |
| `docs/architecture/overview.md` — the lost-property section, two citations, header, change-log | the last review's F1 and F2; D7 |
| `docs/product/vision.md` — the indentation paragraph, "Open at the time of writing", two citations, header, change-log | the last review's F3; D7 |

**No ADR is contradicted.** ADR-0008 rule 2 was read line by line against `shared_prefix` and
against `lay_out`'s rule 2, and rules 1, 3 and 4 against the three refusal paths they name.
ADR-0002's silence about a tab's width is what AC6 and `shared_prefix`'s docstring both rest on,
and neither invents one.

**Would I maintain it?** Yes, and the specific reasons are worth naming rather than implying. The
rule lives in one function that takes the whole run, so "what a run's indent is" cannot drift
between callers — which was the failure mode of the old rule, where `lay_out` re-derived it from
`contents[0]`. `shared_prefix` returns `str | None` and every caller handles the `None`, so the
refusal is not encoded as a sentinel string. The one thing I would watch: `without_indent` in
`tests/test_fixtures.py` restates the prefix rule locally rather than importing it, and that is a
deliberate duplication the file already practises for `pipe_columns` and documents in place — if a
third copy appears, the argument stops being "a test must not ask the code under test" and starts
being drift.

### F1 — `overview.md`'s account of what the padding does is stated more absolutely than it is true

`overview.md:96-99` says a bare table whose first column is marked `---:` or `:---:` "comes back
with leading spaces on its header and body rows and none on its delimiter row". Two documents
falsify the absolute form: `a | b` / `---:|---` / `c | d`, where every first-column cell is one
character wide, comes back `a | b` / `-:|--` / `c | d` — **no leading spaces anywhere**, because
there is nothing to pad; and in `a | b` / `---:|---` / `xxxx | y`, the *widest* body row `xxxx | y`
gets none either.

**Accepted, not a send-back**, for a reason I want on the record rather than assumed: the sentence
is past-tense background explaining why the property was lost, its citation is `[src: WI-0002 AC10]`,
and **WI-0002 AC10 is worded the same way** — "the padding then lands at the very start of the line
as leading whitespace". The document faithfully reports its source; the imprecision is inherited
from a criterion in a closed item, and the class of tables the section is actually about — those
where padding lands at column zero — is described correctly. What would go wrong, and when: a
reader who tests the sentence on the degenerate table finds no leading spaces and may conclude the
whole section is wrong about the mechanism. Recorded in `item.md` `## Notes`.

### F2 — `impl-report.md`'s `## What I did not do` is false about the current tree

It says "*ADR-0003 is still cited in `tests/test_units.py`'s module docstring*". The second
execution changed exactly that, answering the last review's F4, and says so in its own section.

**Accepted, not a send-back.** The report's preamble scopes `## What was built` through `## What I
did not do` to the first execution and directs the reader to the second-execution section for
everything after it, and that section's table row 5 records the change and the finding it answers.
A reader following the report's own signposting is not misled; a reader quoting the bullet in
isolation is. Sending the item back to rewrite a superseded section of a two-execution report costs
a round trip and buys nothing the preamble does not already say. Recorded in `## Notes`.

### F3 — one hunk traces to the review rather than to the plan, and the gate wording does not allow for that

`tests/test_units.py`'s module and `RejectionTest` docstrings changed at `2c39bc4` with no plan step
behind them, because `plan.md` has no step for the documents this change invalidated — which is the
root of the last rejection and is stated as such in `impl-report.md`'s second `## Deviations`
section. `implement` recorded `no-unplanned-scope` against `review.md`'s finding list instead, which
its own SKILL.md step 1 makes authoritative for a resumed run.

**Correct handling, and the finding is about the toolkit, not this item.** The new text was checked
against ADR-0008 (which does own all four rules) rather than against the sentence it replaced, and
it removes a contradiction inside one file: `RejectionTest`'s class docstring had said ADR-0008
since `f32d681` while the module docstring above it still said ADR-0003. What is worth carrying
forward is that the `no-unplanned-scope` gate is worded for a first run only, and that
`plan`'s template has no step for updating documents a change invalidates — the second is what
produced the D7/D12 rejection in the first place. Recorded in `## Notes`.

### F4 — the standing "fixture outputs were never independently re-derived" gap is narrower than it was

WI-0001's `## Notes` carries a gap: the suite asserts the code reproduces the fixtures' expected
outputs, and nobody has re-derived those outputs from the criteria. For **the seven pairs this item
adds**, I did: each `.out` was opened under `cat -A` and checked character by character against the
criterion that specifies it — `refeed-bare-first-column` against AC2's second transcript,
`refeed-blockquote-first-column` and `refeed-list-indent-first-column` against AC3's step 2,
`uneven-leading-spaces`, `uneven-delimiter-deepest` and `uneven-blockquote-space` against AC5's
three documents, `quote-depth` against AC6's second. All seven match, trailing spaces included.
The 33 pre-existing pairs remain re-derived only in WI-0001's first review cycle; they are
byte-identical between `main`'s build and this branch's, which bounds the risk to something that
predates this item. Not a defect; recorded because the gap is now smaller and someone should know
by how much.

### F5 — `vision.md` v5 says "nothing is waiting to be asked", and the engagement is about to ask

`vision.md:100` reads "*Nothing the stakeholder has been asked is unanswered, and nothing is waiting
to be asked.*" That was true when it was written and true now. It stops being true the moment
`review-close` files the epic's `kind: sign-off` question, which `scripts/engagement-state` will
call for as soon as this item closes.

**Not a defect in this item** — the sentence is about the product's open unknowns, not about the
pipeline's termination protocol, and no reading of D7 or D12 makes WI-0003 responsible for a
document going stale because of a *later* execution. It is flagged here and in `## Notes` so that
the epic's close, which owns DE4 and DE6, meets it deliberately rather than by accident.

## Accepted gaps

Each of these is written into `item.md` `## Notes`, because a gap that lives only in a report is
forgotten the moment the item is `done`.

1. **F1** — `overview.md`'s absolute account of where the padding lands, inherited from WI-0002 AC10.
2. **F2** — `impl-report.md`'s first-execution `## What I did not do` bullet, superseded by its own
   second-execution section.
3. **F3** — `plan`'s template has no step for updating the documents a change invalidates, and the
   `no-unplanned-scope` gate is worded for a first run only.
4. **F5** — `vision.md`'s "nothing is waiting to be asked", for the epic's close to handle.
5. **AC9's arithmetic**, from `verify-report.md`: the checking clause says "exactly two of its 65
   tests change" while accounting for four changed tests, two declared not to count. Both readings
   select the same code because AC9 names every test, so it was decidable and passed; the fourth
   criterion in EP-001 to count artefacts and need reconciling.
6. **`lint-claims` was structurally vacuous on the executions before the last rejection**, because
   `plan` committed ADR-0008 and the `overview.md` edits on the trunk at `2884f53` before the branch
   was cut. It is non-vacuous now. A skill that sees it pass should not read that as "the documents
   are fine".
7. **The differential corpora are generated samples** — 25 000 documents in the first verification,
   6 000 in the second, neither containing a fenced code block, a CRLF terminator, an undecodable
   byte, or a document longer than four lines. Those are covered by the shipped fixtures.
8. **Carried unchanged from WI-0001**: the CPython 3.8 floor is asserted, not tested — checked again
   here by reading, `from __future__ import annotations` in every `mdtab/` module that carries an
   annotation, no `removeprefix`, no match statement; and concurrency, large inputs and pathological
   documents remain unexercised.

## Verdict

**Accepted.** The change does what AC1–AC10 ask, in one function and four lines of rule 2, and the
record supports it end to end: thirteen executions, thirteen entries, two questions answered with
their consequences propagated, an ADR that supersedes rather than edits, and a second verification
that re-decided every criterion at the current head instead of inheriting the first. All twelve
Definition of Done criteria pass, including the D7 and D12 that failed last cycle. The trial merge
at `336e359` is green and the trunk did not move. Merging into `main` and closing as
`outcome: delivered`.

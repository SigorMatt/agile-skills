# Review — EP-001

The **final** termination review of the engagement. There is no branch, no diff and no merge
here: an epic is ended, not delivered, and what is reviewed is whether the engagement may stop,
what the record says it produced, and whether the documents still tell the truth about the code.

**Verdict up front: ended, E1 — accepted, every child delivered.** All seven epic Definition of
Done criteria pass. The stakeholder was asked at rest and answered (`EP-001/Q-006`, option A):
*"Yes — accept it, all five, and close it."* EP-001 closes `done` with `outcome: delivered`.

This file replaces the termination review of 2026-08-28T22:38:11Z, which returned **not ended**
because DE6 failed and `BUG-0001` was filed from it. That review is not deleted — it is in git at
`15aa0e1` and its reasoning is in this epic's journal at that timestamp. Two further termination
reviews ran between the two (2026-08-28T23:26:16Z and 2026-08-29T08:24:12Z); each filed a
sign-off and suspended the epic without reaching a verdict, so neither rewrote this file, and
both are in the journal.

## What I examined

**Preconditions.** SKILL.md precondition 4: EP-001 is an `epic` at `open` and
`scripts/engagement-state EP-001` reports `at-rest`. Steps 1–9 do not apply; this execution went
to step 10, and the reply was already in the file, so it records the ending rather than filing a
fourth sign-off.

**Commands run in this execution.** All from the workspace root unless stated.

| what | result |
|------|--------|
| `scripts/engagement-state EP-001` | `at-rest` — every child stopped, no question open, no request open; rest reached 2026-08-29T08:20:20Z |
| `scripts/check-epic-signoff EP-001` | **PASS** — `Q-006` carries the reply, names all 5 children, filed after rest |
| `scripts/validate-workspace .` | exit 0, 6 items, 12 documents |
| `scripts/lint-claims .` (whole tree) | exit 0, 0 errors, 0 warnings |
| `scripts/lint-claims --changed-since main` | exit 0 — and it checked **no** documents; see Findings |
| `python3 -m unittest discover -s tests -t .` | exit 0, **84 tests** |
| `python3 -W error -m compileall -q mdtab tests` | exit 0 |
| `git clone <workspace> /tmp/de3/clone` | exit 0; no `setup.py`, `pyproject.toml` or `requirements.txt` in the clone |
| `python3 -m mdtab` run **inside that fresh clone** | exit 0, output byte-identical to the working tree's (`cmp` exit 0) |

**The seven success measures, each run at a terminal on a document written for this review**
(`/tmp/de3/doc.md`: a heading, prose containing a bare `|` and a `|` in backticks, a list, a
blockquote, an indented code block, a fenced block **containing a pipe table**, an ASCII table
with `:---`/`---:`/`:---:`, and a CJK/accented/emoji table). Measured independently of the tool:
display width recomputed from `unicodedata.east_asian_width`, not from `mdtab/width.py`, so the
check cannot agree with the code by construction. Results in the Definition of Done table below.

**Claims opened at their citation, not read in their prose** (DE6). Ten absolutes the epic's work
touched, each decided from the thing it cites:

| claim, and where it stands | what I opened | verdict |
|---|---|---|
| *"Nothing else may use `len()` to mean a width"* — overview "Rules that live in exactly one place" [src: ADR-0002] | every `len(` in `mdtab/` outside `width.py` — 20 sites in `table.py`, `inline.py`, `textio.py`, `scan.py` | **true**; all 20 count elements or index a string (`content[len(prefix):]`, `while end < len(text)`), none means screen width |
| *"Nothing else may call `str.splitlines`"* [src: ADR-0004] | `grep -rn splitlines mdtab/` | **true**; the only occurrence anywhere is the docstring at `mdtab/textio.py:7` forbidding it |
| *"Nothing on the recognition path may call it"* — of `contains_line_break` [src: ADR-0010; WI-0004 AC7] | every reference in `mdtab/` | **true**; one production caller, `mdtab/table.py:256`, inside `_render_row` (which begins at line 220), i.e. the renderer |
| *"a `br` tag cannot occur in a delimiter cell anyway"* [src: ADR-0010] | `mdtab/table.py:18`, `_DELIMITER_CELL = re.compile(r"^:?-+:?$")`, used at line 94 | **true**; the grammar admits only `:` and `-`, so no `<`, no letters |
| *"the middle column of `a \| \| b` is 2 columns wide under `---` and 3 under `:-:`"* [src: WI-0001 AC12; WI-0001/Q-005] | both commands run | **true**; `--\|--\|--` versus `:-:\|:-:\|:-:` |
| *"a run whose lines differ by a **tab** or by a `>` is still not a table and is still copied through untouched"* [src: WI-0003 AC6] | both runs put through the tool, output inspected with `cat -A` | **true**; byte-identical to input in both cases |
| *"it never adds or removes a `\|`, so a table written without outer bars comes back without them"* [src: ADR-0008] | a bare `name \| qty` table with a `---:` first column | **true**; comes back bare |
| *"mdtab therefore recognises the bare right-aligned table its own layout emits"* [src: WI-0003 AC2; src: WI-0003 AC4] | that table's output fed back in, compared with `cmp` | **true**; `cmp` exit 0 — and this is the property WI-0003 existed to restore |
| *"backtick runs must match in length, and nothing else about a span is modelled"* [src: ADR-0010] | `mdtab/inline.py` `_backtick_run`, `_code_spans`, `contains_line_break` | **true**, and the module's own docstring says so; the limit is declared, not concealed |
| *"There is no configuration, no state between runs, no file access and no network"* — overview "The shape of the thing" | `grep -rn "open(\|socket\|urllib\|requests\|subprocess" mdtab/` | **true**; one hit, a docstring sentence in `filter.py` |

**The three transcripts the record shows the stakeholder**, re-run on `main` at `622d6ef` and
compared character by character with what the documents print: `docs/product/vision.md` "Open at
the time of writing" (the `a<br>b` table), and both transcripts in `EP-001/Q-006`. All three
reproduce exactly. A document that shows a person a command and its output is making a claim, and
it is checkable the same way any other claim is.

**Read in full, not skimmed:** `tracker/items/EP-001/item.md`, `history.md` (8 rows before this
execution, chaining without a gap, last row matching `item.md`), `journal.md` (12 entries against 8
history rows: the four without a transition are the two `answer-questions` runs that answered a
child's questions from the epic's context, the 22:38:11Z termination review that ended "not ended",
and the 08:24:41Z entry correcting a gate result mis-journalled in the entry above it), all six questions on the
epic and all fourteen on its children, `docs/product/vision.md` v11, `docs/architecture/overview.md`
v9, and `spec/dor-dod.md` §4.

## Definition of Done

Epic Definition of Done, `spec/dor-dod.md` §4, criterion by criterion.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | every child terminal, and every undelivered child named | **pass** | Five children and no others: WI-0001, WI-0002, WI-0003, BUG-0001, WI-0004 — all `status: done`. None is undelivered, so the naming obligation is discharged by `Q-006` naming all five anyway, each with one line of what it delivered. `check-epic-signoff` counts the children independently and agrees: "names all 5 child item(s)" |
| DE2 | every child's `outcome` recorded; dropped items say why | **pass** | `grep -H "^outcome:" tracker/items/*/item.md` → `delivered` on all five. None is `dropped` or `duplicate`, so the `## Notes` obligation does not arise |
| DE3 | every `## Success measures` addressed — met, or explicitly not met with the reason | **pass**, six met at a terminal and one met by proxy with the gap named | **SM1** *lines outside a table byte-for-byte unchanged*: of the 27 lines in the test document, exactly 7 differ, and all 7 are inside a laid-out table — the set difference `changed − table-lines` is empty. **SM2** *pipes at the same display column*: recomputed from `unicodedata.east_asian_width` independently of `mdtab/width.py`; the ASCII table's pipes sit at columns `[0, 21, 27, 35]` on all four rows, the CJK/emoji table's at `[0, 17, 25, 30]` on all four. **SM3** *idempotence*: `diff out1 out2` empty on the full document, and `cmp` exit 0 on the bare right-aligned table separately. **SM4** *a renderer renders the output the same as the input*: **met by proxy, and the gap is named** — no markdown renderer is installed and ADR-0001 forbids adding one, so what was checked is the property the measure is about: every cell's text, stripped of padding, is identical between input and output across all 11 table rows, and all three delimiter rows' markers survive unchanged (`left,right,center`; `none,none,none`; `none,center,right`). What is **not** checked is that some particular renderer agrees. **SM5** *a document with no tables passes through byte-for-byte*: `cmp` exit 0. **SM6** *a pipe table inside a fence comes back unchanged*: the five fenced lines hash identically before and after (`945a6d03…`). **SM7** *runs from a checkout with only Python 3, no install step*: fresh `git clone` holds no `setup.py`, `pyproject.toml` or `requirements.txt`; `python3 -m mdtab` inside it exits 0 and its output is `cmp`-identical to the working tree's; the only non-project imports anywhere in `mdtab/` are `re`, `sys`, `unicodedata` and `__future__` |
| DE4 | `docs/product/` reflects what was built, not what was proposed | **pass** | `docs/product/vision.md` is at v11 as of this turn. Its behavioural transcript re-runs byte-for-byte on `main`. Its "Open at the time of writing" section says nothing is open, which is now true: no question is open anywhere in the workspace. Its "Accepted as delivered" carries the acceptance that was actually given, with the two gaps declined at `Q-006`. One sentence that described the tool as it was *before* WI-0004 landed was corrected in the same version — see Findings |
| DE5 | open questions across all children closed, or re-filed against a follow-up | **pass** | Twenty question files across six items; every one `status: answered`. Nothing is `open` and nothing is `deferred` |
| DE6 | every claim in `docs/` about behaviour this epic delivered checked against the code **during this epic**; every citation resolves | **pass** | The ten-claim table above: each opened at what it cites — the code, the regex, the command — never at a neighbouring document. Plus the three shown-to-the-stakeholder transcripts re-run. Mechanical half: `scripts/lint-claims .` over the whole tree, exit 0, 0 errors, 0 warnings |
| DE7 | the stakeholder was **asked** after rest, and answered — in every ending | **pass** | `scripts/check-epic-signoff EP-001` → PASS: `Q-006` carries the reply, names all five children, and was filed at 08:22:12Z, after rest was reached at 08:20:20Z. They were asked three times across this engagement, because two earlier acceptances covered a smaller set of children than the engagement ended up having; `Q-004`, `Q-005` and `Q-006` are all on the record with what each named |

## Findings

1. **`lint-claims --changed-since main` checks nothing when the workspace is already on `main`.**
   The gate `claims-are-sourced` names exactly that invocation, and here it reported *"checked no
   documents changed since main"* and exited 0 — a pass that inspected zero files. It is not
   wrong, it is inapplicable: an epic-ending execution has no branch, so there is no diff against
   the trunk. The whole-tree run (`scripts/lint-claims .`, 0 errors) is what actually supports the
   gate, and it is recorded above so that a reader does not mistake the vacuous pass for a real
   one. **This is the same finding the 2026-08-28T22:38:11Z review recorded**, unchanged, and it
   is a defect in the contract rather than in this engagement — noted again rather than filed,
   because no item in this project can fix a skill contract.

2. **`docs/product/vision.md` v10 still contained one sentence made false by WI-0004's code.**
   *"This is the part of the item that is new machinery: mdtab looks for a code span nowhere
   today"* had been false since `mdtab/inline.py` landed at v9, and v9's own sweep — which
   corrected four sibling sentences in the same document — missed it. It was corrected to the past
   tense in v11 during this turn's `answer-questions` execution, which was already the author of
   that version, and declared in the change-log row. `lint-claims` cannot catch this class: the
   citation resolves, the sentence it supports is stale. **Not a send-back**: the correction was
   already made before this review ran, and I verified it by opening `mdtab/inline.py:47`
   (`_code_spans`) rather than by reading the corrected sentence.

3. **Three termination reviews ran without rewriting `review.md`.** The executions at
   2026-08-28T23:26:16Z and 2026-08-29T08:24:12Z each filed a sign-off question and suspended the
   epic, and the 2026-08-29T08:24:41Z entry was a journal correction. None reached a verdict, so
   none wrote this artifact — which left `review.md` asserting *"Verdict up front: not ended"*
   for eleven hours after the finding that caused it (`BUG-0001`) had been fixed and closed. The
   contract lists `review.md` under `always`, and a step-10 execution that stops to ask has
   nothing to write there yet. Recorded as a toolkit observation; the file is now current.

No finding is a send-back. There is no item to send anything back to: every child is closed and
the stakeholder has accepted.

## Accepted gaps

Both were put to the stakeholder in `Q-006` and **declined as work by them**, in terms — *"The
note of yours that is worded loosely is your business and not worth another round — don't open
anything new for it."* They are recorded here, in `EP-001/item.md` and in `vision.md` v11 so that
a later reading finds a decision rather than an unexplored gap, and **no item is to be filed for
either**:

1. **One sentence in the design record is broader than the code it describes.** ADR-0010 §2 and
   `tracker/items/WI-0004/artifacts/plan.md` say code spans are *"excluded from the search"* for a
   `br` tag; `mdtab/inline.py` takes a tag when the tag's **start index** lies outside every span.
   The readings differ on exactly one shape — a tag opening outside backticks and closing inside
   them, `` a<br `>` b `` — which blanking would match and the implementation does not. Recorded
   at the time as deviation 1 of `tracker/items/WI-0004/artifacts/impl-report.md`, and verified as
   boundary case 11 of `verify-report.md`. Neither document is edited: both are accurate records
   of what was decided and what was planned, and rewriting a decision record to match code the
   stakeholder has declined to have touched would be editing history, not correcting it.

2. **mdtab did not learn the rest of markdown's rules about code spans.** A run of *n* backticks
   is closed by a run of *n*, and nothing else about a span is modelled — not the stripped space,
   not the newline folding. Declared in `mdtab/inline.py`'s docstring and in ADR-0010, and
   sufficient for every case the stakeholder named.

Carried forward unchanged from the earlier sign-offs, and re-stated here because this is the file
a later reader opens: the **five caveats** declined at `Q-004` (no README or `--help`; no way to
ask the tool why it declined a table; multi-codepoint emoji; nothing larger than ~30 lines having
been through it; only Python 3.12 having actually run it) and the **three gaps** declined at
`Q-005` (a blank line missing from a test file, a "true enough" sentence in the architecture
notes, and WI-0002's old verification record). **No follow-up item is to be filed for any of the
ten**, on the strength of this engagement.

## Verdict

**Ended. E1 — accepted, with every child delivered.** `spec/ids-and-statuses.md` §3.5: the
stakeholder accepted at `Q-006` and all five children are `done` with `outcome: delivered`, so the
ending is `open → done` with `outcome: delivered` — not `delivered-partial`, which would
underclaim, and not E3, which the reply is not.

What the engagement produced: a filter, `python3 -m mdtab`, that reads a markdown document on
stdin and writes it back with its GFM pipe tables' columns padded to a common display width, the
delimiter row's alignment markers honoured in every ordinary cell and declined by any cell holding
a line break, and every line that is not part of a table returned byte for byte. It is 7 modules
and 84 tests, runs from a clone with only Python 3 and no install step, and is silent about
everything.

---
id: WI-0003
type: work-item
title: Recognise a table mdtab laid out with a right-aligned first column
status: done
priority: high
epic: EP-001
depends-on:
  - WI-0002
created: "2026-08-28T20:19:15Z"
updated: "2026-08-28T22:22:16Z"
arose-from: WI-0002/Q-002
branch: wi/WI-0003
outcome: delivered
---

## Story

As someone who keeps a markdown document over months, I want mdtab to go on tidying a table it
laid out itself, so that a table does not become one mdtab silently refuses to touch the first
time it is aligned.

## Acceptance criteria

Every criterion below is checked against the invocation `plan` recorded for WI-0001
(`tracker/items/WI-0001/artifacts/plan.md`): a document on stdin, the document on stdout, exit 0.
`$ mdtab` in a transcript below means that invocation.

**AC1 defines the term the rest of them use.** Everything else is stated as an observation.

- [x] AC1 — the recognition rule of WI-0001 AC15 is relaxed as follows, and in no other way. A
      run's **shared prefix** is the longest common prefix, byte for byte, of the WI-0001 AC15
      prefixes of its lines. The run is recognised only if, for every line, the part of that
      line's AC15 prefix which follows the shared prefix consists of **space characters and
      nothing else**; a run with any other difference is not laid out and is reproduced
      byte-for-byte, as under WI-0001 AC4. When the run is recognised, the shared prefix — not
      each line's own prefix — is what is stripped before the table is parsed and reproduced
      unchanged at the start of every output line; every space past it belongs to the row, and
      therefore to that row's first cell, and is removed with the rest of that cell's leading
      spaces by WI-0001 AC11. A run's extent is still fixed by WI-0001 AC7 before any prefix is
      compared, so this changes which runs are laid out and never which lines form a run
      (`WI-0003/Q-001`, option A).
- [x] AC2 — **the fault is fixed in its first form.** A bare table (no outer `|`, WI-0001 AC14)
      at the start of the line whose first column is marked `---:` or `:---:` is still recognised
      after mdtab has laid it out. Checked in two steps:

      ```
      $ printf 'a | b\n---:|---\nxxxx | y\n' | mdtab
         a | b
      ----:|--
      xxxx | y
      $ printf '   a | bbbbb\n----:|--\nxxxx | y\n' | mdtab      # that output, one cell lengthened
         a | bbbbb
      ----:|------
      xxxx | y
      ```

      The second command is the criterion: today it returns its input unchanged, and it must
      return a re-aligned table. Note the trailing spaces on the `xxxx | y` line of the expected
      output, which WI-0001 AC2 requires and which `diff` will show.
- [x] AC3 — **the fault is fixed in its second form**, where the padding lands just after a `>`
      or an indent rather than at the start of the line. The same two steps as AC2, run on
      `> a | b` / `> ---:|---` / `> xxxx | y` and on `  a | b` / `  ---:|---` / `  xxxx | y`:
      the first command gives `>    a | b` / `> ----:|--` / `> xxxx | y` and
      `     a | b` / `  ----:|--` / `  xxxx | y` respectively — which it already does today — and
      feeding either back with `b` lengthened to `bbbbb` must produce a re-aligned table rather
      than the input unchanged.
- [x] AC4 — WI-0001 AC6 still holds everywhere: running the tool on its own output produces
      identical bytes. Checked on the output of every command in AC2, AC3, AC5 and AC7, and on
      the output of every fixture in AC8, by running mdtab twice and diffing.
- [x] AC5 — **the price the stakeholder accepted.** A bare run whose rows differ only in how many
      leading spaces they carry is laid out, and comes back at the run's shared prefix — which for
      a run at the left margin is the start of the line. Checked with the document put to them in
      `Q-001`:

      ```
      $ printf '  a | b\n---|---\n  ccc | d\n' | mdtab
      a   | b
      ----|--
      ccc | d
      ```

      Today that document is returned unchanged. Two further documents of the same shape,
      recorded because they are the same rule and someone will meet them: a run whose *delimiter*
      row is the deepest-indented line — `a | b` / `   ---|---` / `c | d` — comes back as
      `a | b` / `--|--` / `c | d`; and a bare run inside a blockquote whose rows carry an uneven
      extra space — `>  a | b` / `> ---|---` / `>  c | d` — comes back as `> a | b` / `> --|--` /
      `> c | d`, at the shared prefix `> `.
- [x] AC6 — **a tab or a `>` in the indentation is still compared byte-for-byte**, so a run whose
      lines differ there is still not laid out and is still reproduced byte-for-byte
      (`Q-001`: *"Tabs and the quote marks having to match exactly sounds right to me"*).
      Checked on `\ta | b` / `  ---|---` / `\tc | d` and on `> a | b` / `>> ---|---` /
      `> c | d`, by diffing input against output; both must be unchanged, as they are today.
- [x] AC7 — **a table written with outer `|` bars is unaffected by this item.** Every run whose
      rows all begin with `|` after the shared prefix produces byte-for-byte the output it
      produces today, and a run in which one row has extra spaces before its `|` is still not
      laid out — it now fails WI-0001 AC14's one-outer-pipe-style rule rather than the prefix
      rule, and the outcome a user sees is identical. Checked on the document WI-0001 AC15 names
      and `tests/fixtures/ragged-prefix.in.md` holds — `> | a | bb |` / `>  |---|---|` /
      `> | 1 | 2 |` — which must still come back unchanged, and on
      `tests/fixtures/outer-pipes`, `blockquote-table`, `list-indent-table` and `mixed-pipes`.
- [x] AC8 — **no document the project already ships changes.** All 33 fixture pairs under
      `tests/fixtures/` as they stand at 2026-08-28 (`*.in.*` / `*.out.*`) still produce their
      recorded output byte-for-byte, with no `.out` file edited. Checked by running
      `python3 -m unittest tests.test_fixtures` against unmodified fixture files.
- [x] AC9 — **every acceptance criterion of WI-0001 and of WI-0002 still holds**, with one
      exception, named here because WI-0002/Q-003 showed what an unsatisfiable checking clause
      costs. The exception is the final clause of WI-0001 AC15 — *"a run whose lines' prefixes are
      not byte-identical is not laid out"* — which AC1 above supersedes for the space-only case
      and leaves untouched for every other. Everything else in AC15 still holds: the prefix is
      reproduced unchanged, the table is laid out as though it were not there, and WI-0001 AC2
      holds. Checked by running the project's shipped test suite
      (`python3 -m unittest discover`), in which **exactly two** of its 65 tests are expected to
      change; all other 63 must pass unmodified.

      1. `tests/test_units.py::PaddingPlacementTest::test_ac10_a_bare_right_aligned_first_column_pads_at_the_start_of_the_line`,
         whose final assertion `self.assertIsNone(lay_out(laid_out))` becomes an assertion that the
         run *is* laid out and is a fixed point. That test's own docstring predicted this — *"When
         WI-0003 lands, the last assertion here is the one that changes"* — and its first two
         assertions are unchanged.
      2. `tests/test_fixtures.py::ContentPreservationTest::test_ac11_cell_content_survives_apart_from_the_spaces_around_it`,
         which splits each raw line on `|` and so counts a prefix ending in a character that is not
         a space as part of the first cell. That was exact only while WI-0001 AC15 required every
         line of a run to repeat one prefix; under AC1 above the spaces past the shared prefix are
         the first cell's, so the test must remove a line's indentation before splitting it. Its
         assertion is otherwise unchanged, no fixture is exempted from it, and it still fails if a
         cell's characters change. **This second entry was added on 2026-08-28 by
         `answer-questions`, answering `Q-002`**: the clause as first written said "exactly one",
         and a checking clause that cannot be satisfied is the fault WI-0002/Q-003 was answered
         for. It is amended here the same way and for the same reason — the substance of AC9, that
         WI-0001's and WI-0002's criteria still hold, is not touched.

      Unchanged in substance though it moves: `test_rule_2_a_run_whose_prefixes_are_not_byte_identical`
      keeps its tab assertion, and its extra-space assertion is relocated to
      `test_rule_4_a_run_whose_rows_disagree_about_their_outer_pipes`, which is the rule that now
      refuses that run (WI-0001 AC14). No assertion is deleted and both still pass, which is what
      this criterion asked for when it named that test.
- [x] AC10 — mdtab still writes nothing to stderr and still exits 0 on every document above,
      including the ones it declines to lay out (EP-001, ADR-0003).

## Out of scope

- Changing how a table mdtab recognises is laid out. WI-0001 and WI-0002 own the layout; this
  item only changes which runs are recognised, and a run that was already laid out must come out
  byte-identical to what it does today.
- Any diagnostic output. The epic keeps mdtab silent, and a table this item still declines to
  recognise says nothing about why (EP-001, ADR-0003).
- Normalising or repairing indentation **outside** the runs mdtab recognises. ADR-0003 option B
  was rejected for changing lines nobody asked to have changed, and that still holds for every
  line of the document that is not part of a laid-out table. What this bullet said in round 1 —
  that indentation the author wrote is never touched at all — was overtaken by the stakeholder's
  answer to `Q-001` and is corrected rather than quietly dropped: inside a recognised run,
  leading spaces past the shared prefix now belong to the first cell and are re-laid-out like any
  other cell padding (AC5). Tabs and `>` are still never touched (AC6).
- Deciding a tab's display width. AC6 keeps tabs compared byte-for-byte precisely so that nothing
  here has to; ADR-0002 does not define a width for one, and inventing one is a decision nobody
  has been asked for.
- Recognising anything else mdtab refuses today. A run whose rows disagree about their cell count
  (WI-0001 AC13) or their outer-pipe style (WI-0001 AC14) is still refused, and so is a `|` line
  inside a fenced code block (WI-0001 AC8). This item relaxes exactly one of ADR-0003's four
  rules.

## Notes

**Why this item exists.** The stakeholder answered `WI-0002/Q-002` with option A — honour the
alignment marker in the first column of a bare table even though the padding lands at the start
of the line — and then refused the cost that option carried:

> *"if the tool then can't recognise a table it laid out itself, that's a fault in the tool and
> I'd want it sorted rather than worked around."*

That is work no item recorded, so `answer-questions` filed it here rather than widening WI-0002
(`spec/ids-and-statuses.md` §5). WI-0002 remains deliverable and checkable on its own; this item
fixes what WI-0002 AC10 exposes.

**The mechanics of the fault**, demonstrated against the shipped tool in `WI-0002/Q-002`:
ADR-0003 rule 2 recognises a run only when every line carries a byte-identical prefix of spaces,
tabs and `>`. Right-aligning the first column of a bare table gives the header and body rows a
leading space that the delimiter row (filled with `-` from column zero) does not have, so the
prefixes differ and the run stops being a table.

**Depends on WI-0002** because the output that triggers the fault does not exist until WI-0002
ships, and AC1 is stated in terms of it.

**Three things `refine` must settle** — as filed. Two are now settled by the stakeholder and one
by routing; see `### Behaviour combinations, for DoR R10

This item introduces no option, flag or mode — it changes one recognition rule — so R10 is about
that rule crossed with the constructs already in the tool. Each has a stated behaviour or is
named as unaffected:

| the relaxed rule crossed with … | stated where |
|---|---|
| outer-pipe style (WI-0001 AC14) | AC7 — unaffected; a row with extra spaces before its `|` is refused by AC14 instead |
| a tab or a `>` in the indentation (WI-0001 AC15) | AC6 — still refused |
| a blockquote or a list indent | AC3 and AC5 — laid out at the shared prefix |
| alignment markers (WI-0002) | AC2, AC3 — the markers are what create the uneven spaces in the first place |
| cell count (WI-0001 AC13) | out of scope, third bullet — still refused |
| fenced code blocks (WI-0001 AC8) | out of scope, third bullet — the fence mask is computed over the whole document before any run is found, so relaxing a prefix rule cannot pull a fenced line into a table |
| escaped pipes (WI-0001 AC10) | no interaction: cells are split after the shared prefix is stripped, and leading spaces are removed from cell content by WI-0001 AC11 |
| run extent (WI-0001 AC7) | AC1's last sentence — extent is fixed before prefixes are compared, and this item does not change that |
| CRLF and the final newline (WI-0001 AC9) | no interaction: a terminator is removed before a line is examined and restored afterwards, so it is never part of a prefix |

### The stakeholder's ruling` below, which is the current state. The list is kept
as written so that the question the item was suspended on is still legible:

1. How to tell a table mdtab indented *itself* from one the author indented unevenly — the case
   ADR-0003 rule 2 deliberately leaves alone (AC3). Candidate readings: take the prefix from the
   delimiter row alone; take the shallowest prefix in the run; compare prefixes only up to the
   first non-space character. They differ on real documents, and the difference is visible to the
   stakeholder, so this may be a question for them rather than for `plan`.
2. Whether a `\t` in a prefix can be compared this way at all, given a tab's display width is not
   fixed.
3. Whether the fix belongs in recognition or in layout — emitting the padding differently is
   ruled out by `WI-0002/Q-002` ("don't add the bars, don't leave the table alone"), but where in
   the pipeline the relaxation sits is a design choice for `plan`.

**ADR-0003 will need amending**, not superseding: its own Consequences section records that its
rules can be *relaxed* additively with high reversibility, because relaxing only moves documents
from the byte-for-byte branch into the laid-out branch. `plan` writes that ADR; the stakeholder's
authorisation for the change is the sentence quoted above, and now also their answer to `Q-001`.

Note for whoever writes it: ADR-0003's Consequences justify relaxation by saying *"no document
that is aligned today would change"*, and that is still true — but it is not the whole story after
this answer. A bare run with uneven leading spaces is not aligned today and **will** change: it
moves out of the byte-for-byte branch and comes back at the shallowest indent in the run. That is
the cost the stakeholder was shown and accepted, and the amendment should say so rather than
inherit the reassuring half of the sentence.

### The stakeholder's ruling

`Q-001` was answered at 2026-08-28T21:13:13Z, option **A**, and returned this item to `draft`.
Their words, in full, are in `questions/Q-001.md` and in `artifacts/refinement-qa.md`; the part
that decides the mechanics is:

> *"Yes, tidy it. Spaces at the front of a line are part of how the table sits, not something I
> put there on purpose, and a table with two spaces on one row and none on the next isn't tangled
> — it's just untidy, which is the exact thing I wanted the tool for."*

Against the three points above:

1. **Which prefix a run is judged by — settled.** The shared part of the indentation is the
   indent; anything past it belongs to the first cell. So a bare run whose rows differ only in how
   many leading **spaces** they carry is recognised, laid out, and returned at the shallowest
   indent in the run. This is a deliberate narrowing of *"a table indented in some tangled way
   you can't make sense of"* (`WI-0001/Q-003`): uneven spaces are no longer tangled. Uneven tabs
   and uneven `>` still are.
2. **Tabs — settled, strict.** *"Tabs and the quote marks having to match exactly sounds right to
   me."* A tab or a `>` difference in the indentation still makes the run unrecognised, exactly
   as today. Only plain spaces may differ. The basis, and why it was not left to be invented, is
   in `artifacts/refinement-qa.md` §"Settled without asking" item 1.
3. **Where the fix lives — confirmed as `plan`'s.** *"Where the fix goes in the code is yours to
   decide."* Whether the relaxation sits in `mdtab/scan.py`'s prefix extraction or in
   `mdtab/table.py`'s rule 2, and whether ADR-0003 gains a fifth rule or has rule 2 amended, are
   `plan`'s to decide and to record.

The acceptance criteria above were rewritten against this ruling in refinement round 2. The four
criteria this item was filed with are gone: AC1 and AC3 contradicted each other, AC4 had no
satisfiable checking clause, and all three turned on `Q-001`. They are replaced by AC1–AC10, and
every one of them was run against a prototype of the change before it was written down — the
transcripts in AC2, AC3 and AC5 are what the prototype actually produced, not what it ought to.
`artifacts/refinement-qa.md` records the round-2 audit and the measurements.

### Corrected in refinement round 1

Two references to "WI-0002 AC7" — in AC1 and in the paragraph above — named the criterion that
aligns the first column of a bare table. That was true when this item was filed at
2026-08-28T20:19:15Z and stopped being true seven minutes later, when `refine`'s second round on
WI-0002 renumbered its criteria. Both now read **WI-0002 AC10**, which is that criterion; WI-0002
AC7 is now the guard-space criterion and is a different claim. Nothing else in this item was
changed in round 1: AC1, AC3 and AC4 all wait on `Q-001` and are rewritten in round 2, with the
list of what that round must do in `artifacts/refinement-qa.md`.

### Gaps accepted at close

Recorded here by `review-close` because a gap that lives only in a report is forgotten once the
item is `done`. Each is argued in `artifacts/review.md`; this is the durable form.

- **`docs/architecture/overview.md` states where the alignment padding lands more absolutely than
  it is true.** Its §"A property the tool lost and got back" says a bare table whose first column
  is marked `---:` or `:---:` "comes back with leading spaces on its header and body rows and none
  on its delimiter row". Two documents falsify the absolute form: `a | b` / `---:|---` / `c | d`
  comes back `a | b` / `-:|--` / `c | d` with no leading spaces at all, because no cell needs
  padding; and in `a | b` / `---:|---` / `xxxx | y` the widest body row gets none either. Accepted
  rather than sent back because the sentence cites `WI-0002 AC10`, which is worded the same way —
  the document reports its source faithfully and the imprecision is inherited from a closed item.
  The class of tables the section is about is described correctly.
- **`artifacts/impl-report.md`'s `## What I did not do` is false about the current tree.** It says
  ADR-0003 is still cited in `tests/test_units.py`'s module docstring; the second `implement`
  execution changed exactly that. The report's preamble scopes that section to the first execution
  and its second-execution table records the change, so a reader following the report's own
  signposting is not misled — but the bullet reads false in isolation.
- **`plan`'s template has no step for updating the documents a change invalidates**, and that is
  the root of this item's one rejection rather than any lapse by `implement`. `plan` wrote
  `overview.md` in a state that was honest when written and false the instant the code landed —
  its own change-log row 4 says "*and that the code has not landed yet*" — and nothing scheduled
  the follow-up edit. Related: the `no-unplanned-scope` gate is worded for a first run only ("every
  hunk traces to an AC or a plan step"), which a resumed run after a send-back cannot satisfy
  literally; `implement` recorded it against `review.md`'s finding list, as its own SKILL.md step 1
  directs.
- **`scripts/lint-claims --changed-since <trunk>` was structurally vacuous on this item until the
  last `implement` execution.** `plan` committed ADR-0008 and the `overview.md` edits **on the
  trunk** at `2884f53`, before the branch was cut, so the branch changed no document and the gate
  reported `checked no documents changed since main` on two executions — passing without looking at
  the two documents that were wrong. D12 caught them by a human-style read one step before they
  would have shipped. A skill that sees this gate pass must not read it as "the documents are fine".
- **AC9's checking clause miscounts, and the criterion was still decidable.** It says "exactly two
  of its 65 tests change; all other 63 pass unmodified" while its own prose accounts for **four**
  changed pre-existing tests, two of which it declares not to count. Because it *names* every test,
  both readings select the same code, so both verifications passed it and recorded the slip. This
  is the fourth criterion in EP-001 to count artefacts and need reconciling afterwards
  (`WI-0001/Q-005`, `WI-0002/Q-003`, `WI-0003/Q-002`, and now this). The pattern is consistent
  enough to be a `refine` rule: name the tests you expect to change; do not assert how many there
  are.
- **`docs/product/vision.md` v5 says "nothing is waiting to be asked".** True when written and true
  at this item's close; it stops being true the moment the epic's `kind: sign-off` question is
  filed. Not this item's defect — the sentence is about the product's open unknowns, not the
  pipeline's termination protocol — but EP-001's close owns DE4 and DE6 and should meet it
  deliberately.
- **The fixture-derivation gap is narrower than WI-0001 recorded it.** The seven pairs this item
  adds were re-derived by hand during review, character by character under `cat -A`, against the
  criteria that specify them — AC2's second transcript, AC3's step 2 twice, AC5's three documents,
  AC6's second — and all seven match, trailing spaces included. The 33 pre-existing pairs are still
  re-derived only in WI-0001's first review cycle; they are byte-identical between `main`'s build
  and this branch's, which bounds the risk to something predating this item.
- **The differential corpora are generated samples**, not exhaustive: 25 000 documents in the first
  verification and 6 000 in the second, neither containing a fenced code block, a CRLF terminator,
  an undecodable byte, or a document longer than four lines. Those constructs are covered by the
  shipped fixtures, which all pass, but not by the differential.
- **Carried unchanged from WI-0001**: the CPython 3.8 floor is asserted, not tested — only 3.12.3
  is installed, and review checked it again by reading rather than running (`from __future__ import
  annotations` in every `mdtab/` module carrying an annotation, no `removeprefix`, no match
  statement, and `mdtab/__init__.py` is empty). Concurrency, large inputs and pathological
  documents remain unexercised; no criterion mentions them.

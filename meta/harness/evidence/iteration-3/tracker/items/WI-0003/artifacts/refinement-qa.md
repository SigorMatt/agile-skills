---
status: recorded
---

# Refinement Q&A — WI-0003

Two rounds, **recorded**. Round 1 audited the item against the Definition of Ready, settled what
the record could settle, and filed one question to the stakeholder (`questions/Q-001.md`). They
answered it — option A — and `answer-questions` wrote the reply in verbatim beneath the question
at 2026-08-28T21:13:13Z and returned the item to `draft`. Round 2, below, rewrote the acceptance
criteria against that answer and took the item to `ready`.

`status: recorded` because the exchange under "Question filed to the stakeholder" is what was
actually said and the criteria it decides are now written. Round 1 left this file at
`status: agenda` deliberately, so that DoR R8 could not be satisfied by a conversation that had
not happened; that is no longer the state.

The file reads in the order it was written: the round-1 audit, the question and its answer, what
round 1 settled without asking, what round 2 had to do, and then the round-2 record.

Everything under "Settled without asking" is settled **now**, from the record, and does not need
the stakeholder. It is written down so that round 2 applies one answer to an item whose other
problems are already solved.

---

## The Definition of Ready audit that produced this agenda

Walked criterion by criterion against `spec/dor-dod.md` §1 on `item.md` as it stood at
2026-08-28T21:05:00Z, the state `answer-questions` left it in when it filed the item from
`WI-0002/Q-002`.

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | frontmatter carries `id`, `type: work-item`, `epic: EP-001`, `priority: high`, `created`, `updated`, `depends-on: [WI-0002]`, `arose-from: WI-0002/Q-002`; `validate-workspace` exits 0 |
| R2 | pass | `## Story` names the role (*someone who keeps a markdown document over months*), the capability (*mdtab goes on tidying a table it laid out itself*) and the outcome (*so that a table does not become one mdtab silently refuses to touch*) |
| R3 | pass | AC1–AC4 exist, labelled and as checkboxes |
| R4 | **fail** | three defects, below |
| R5 | pass | `## Out of scope` names changing how a recognised table is laid out, diagnostics, and repairing indentation the author wrote — the third is exactly the thing a reader would assume this item does |
| R6 | **fail** | `Q-001` is open and `blocking: true`. This is the intended state; R6 is what makes the suspension honest rather than a formality |
| R7 | pass | `depends-on: WI-0002`, which is `done` (`outcome: delivered`, merged at `984e934`) |
| R8 | **fail** | this file declares `status: agenda` |
| R9 | pass | one coherent change to one recognition rule. The item's own `## Notes` lists three open points, but they are three facets of one decision and one design, not two items |
| R10 | **fail** | the relaxed-prefix rule × outer-pipe style, × tab characters in the prefix, and × the tangled-indent case ADR-0003 deliberately leaves alone all have no stated behaviour. Two are settled below; the third is `Q-001` |

### The three R4 defects

1. **AC1 and AC3 contradict each other as written.** AC1 requires a run that mdtab refuses today
   to be laid out tomorrow. AC3 says *"every other run that fails one of ADR-0003's four
   recognition rules"* is still reproduced byte-for-byte. Any fix necessarily moves *some*
   currently-failing runs into the laid-out branch — that is what a fix is — so AC3 as worded
   forbids AC1. Which runs move is `Q-001`, and AC3 cannot be rewritten until it is answered.
2. **AC1 and `## Notes` cite the wrong criterion of WI-0002.** They name "WI-0002 AC7" for the
   alignment of a bare table's first column. That was true when this item was filed at
   2026-08-28T20:19:15Z; `refine`'s round 2 on WI-0002 renumbered the criteria seven minutes
   later and it has been **AC10** since. Corrected in this round, because a citation that points
   at the wrong criterion is a record defect whatever else is open — WI-0002 AC7 is now the
   guard-space criterion, which is a different claim entirely.
3. **AC4 repeats WI-0002's AC14 without its checking clause**, and WI-0002 AC14's checking clause
   is the one thing in that item that had to be amended after the fact (`WI-0002/Q-003`): it
   required WI-0001's shipped suite to run *unchanged* while also excepting a clause that suite
   encodes. AC4 here says "every acceptance criterion of WI-0001 and of WI-0002 still holds" with
   no exception clause and no way to check it. Whether it needs an exception depends on the
   answer to `Q-001` — under option C nothing changes, under A a class of documents does — so it
   is rewritten in round 2 rather than now.

---

## Question filed to the stakeholder — round 1

One question, `blocking: true`; the item is suspended at `awaiting-answer` with
`resume-to: draft`.

### Q-001 — whether a bare table with uneven leading spaces should start being tidied

> A table written **without** outer `|` bars, whose rows carry different numbers of leading
> spaces: should mdtab start tidying it — pulling it back to the shallowest indent in the run —
> in exchange for going on recognising the tables it has laid out itself?

Options put to them: **A** leading spaces belong to the table, not to the indent (recommended);
**B** re-recognise only a run whose leading spaces already match the padding the markers call
for; **C** leave the rule alone and drop this item.

**Why this went to the stakeholder rather than to `plan`.** It fails the first test in the
routing order: the answer changes which documents the tool touches, and that is the promise they
have ruled on twice in their own words — *"if it doesn't understand one it should keep its hands
off"* (`WI-0001/Q-001`) and *"If a table is indented in some tangled way you can't make sense of,
that's one you leave alone"* (`WI-0001/Q-003`). A table indented unevenly by two spaces is
exactly the boundary of that sentence, and nothing in the record says which side it falls on.

**Answer**, verbatim, 2026-08-28T21:13:13Z:

> Yes, tidy it. Spaces at the front of a line are part of how the table sits, not something I put
> there on purpose, and a table with two spaces on one row and none on the next isn't tangled —
> it's just untidy, which is the exact thing I wanted the tool for. Tabs and the quote marks
> having to match exactly sounds right to me, and where the fix goes in the code is yours to
> decide.

**Option A**, with both of the two things the question also put to them confirmed. Three things
follow, and they are what round 2 builds on:

1. A bare run whose rows carry different numbers of leading spaces **is** tidied, and comes back
   at the shallowest indent in the run. They ruled explicitly on the boundary `WI-0001/Q-003`
   drew: two spaces on one row and none on the next *"isn't tangled — it's just untidy"*. That
   sentence is narrower than option A's mechanics, so it is worth being precise about what it
   does not settle: it says nothing about a run whose rows differ by a **tab** or a `>`, which
   stays refused under point 1 below, and nothing about the four-space or deeper case, which
   option A treats identically because the rule is about *difference*, not about depth.
2. Point 1 of "Settled without asking" is now decided rather than assumed (below).
3. Point 3 of "Settled without asking" is now decided rather than routed (below).

Nothing in the answer touches AC2 — the fixed-point criterion — which was never in question.

---

## Settled without asking

Each of these was a gap in the Definition of Ready that the record already closes. They are
recorded here with their basis so that a reader can check the reasoning rather than take it on
trust, and so that round 2 does not re-derive them.

### 1. Only plain spaces may differ; a tab or a `>` in the indentation must still match exactly — `[decided]`

WI-0001 AC15 defines a line's prefix as its maximal leading run of space, tab and `>`, compared
byte-for-byte. Any relaxation this item makes is confined to **spaces**: two lines whose
indentation differs by a tab, or by a `>`, are still not the same table.

The basis is that nothing in this project defines how wide a tab is. ADR-0002 fixes the display
width of every character mdtab measures, and a tab is not among them — its width depends on where
it lands and on the reader's settings. A rule that let a tab and some spaces be "the same
indentation" would have to invent that width, which is a decision with no right answer and one
the stakeholder has never been asked for. Keeping tabs strict changes nothing about today's
behaviour for tab-indented tables, which is the conservative direction.

Confirmed against the prototype: `\ta | b` / `  ---|---` / `\tc | d` is refused before and after
the change. It is named in `Q-001`'s context so the stakeholder can object in the same breath if
they disagree, rather than being hidden in this file.

Standing deferral relied on: *"The rest of how it is built is your call, not mine"*
(`EP-001/Q-001`).

**Confirmed by the stakeholder, so it is no longer an assumption.** They were shown this
reasoning in `Q-001`'s context and answered *"Tabs and the quote marks having to match exactly
sounds right to me"* (`Q-001`, 2026-08-28T21:13:13Z). Round 2 states it as a criterion, and it is
the one part of this file that a reader may now treat as the stakeholder's own decision rather
than as a defensible default.

### 2. Tables written **with** outer `|` bars cannot be affected by this change — `[assumed]`, and it is a fact rather than a choice

Worth recording because it is the single thing that makes `Q-001`'s cost small, and because a
reader would otherwise have to derive it.

If every row of a run begins with `|` after the shared indentation, then each row's prefix
*ends* where that `|` begins, so all the prefixes are already equal and nothing changes. If one
row has extra spaces before its `|`, that row has no leading pipe once the shared indentation is
stripped, while its neighbours do — and ADR-0003 rule 4 (one outer-pipe style across the run)
refuses the run for that reason instead. Either way the outcome is what it is today.

Confirmed against the prototype on the exact document WI-0001 AC15 names — a blockquote table one
of whose rows carries an extra space after its `>` — which is reproduced byte-for-byte before and
after the change, and on all 33 shipped fixture documents, none of which changes.

### 3. Where in the pipeline the fix lives is `plan`'s, not the stakeholder's — routed, and since confirmed

The item's `## Notes` already routes it. Whether the relaxation sits in `mdtab/scan.py`'s prefix
extraction or in `mdtab/table.py`'s rule 2, and whether ADR-0003 is amended in place or gains a
fifth rule, are answers that would be the same whoever the stakeholder was. They stay in
`## Notes` for `plan`, which also owns the ADR amendment — ADR-0003's own `## Consequences`
records that its rules can be relaxed additively with high reversibility, which is the
authorisation for amending rather than superseding it.

The routing was put to the stakeholder in `Q-001`'s context anyway, and they endorsed it: *"where
the fix goes in the code is yours to decide"* (`Q-001`). So the ADR-0003 amendment is `plan`'s to
write with the stakeholder's authorisation behind it, and `answer-questions` deliberately did not
write it when it consumed the answer — an architecture decision recorded ahead of the plan that
implements it is a decision nobody has had to satisfy yet.

### 4. The item is one coherent change, not two — `[assumed]`, R9

The two forms of the fault — a bare table at the left margin, and a bare table inside a
blockquote or an indent — are the same rule failing in the same way, and the prototype fixes both
with one change. Splitting them would produce two items that cannot be verified independently,
because the second's document is the first's output.

---

## What round 2 must do

The answer is in, so this list is now the option A branch of it. Item 1's first half was done by
`answer-questions` when it consumed the answer; the rest was done by round 2, whose record
follows this section. All five are complete.

1. ~~Write the stakeholder's answer in verbatim, under `Q-001` above~~ — done by
   `answer-questions` at 2026-08-28T21:13:13Z. Round 2 still sets this file to
   `status: recorded`, once the criteria below are written.
2. Rewrite AC1 and AC3 so that they name, in terms someone with a terminal can check, exactly
   which runs move from the byte-for-byte branch into the laid-out branch and which do not.
   **Option A**, so: a criterion about bare runs whose rows differ only in leading spaces moving
   into the laid-out branch and coming back at the shallowest indent in the run, and AC3 narrowed
   from "every run that fails one of ADR-0003's four rules" — which contradicts AC1 — to the runs
   that still fail one, naming the tangled blockquote of WI-0001 AC15 and a tab-versus-spaces run
   as the two worked examples. Option C is off the table.
3. Rewrite AC4 with a checking clause that is actually satisfiable, learning from
   `WI-0002/Q-003`: name what is expected to change in WI-0001's and WI-0002's shipped suites, if
   anything, rather than asserting that nothing does. The prototype's measurement — 33 fixtures,
   0 changed — is evidence for "nothing changes", but it is evidence and not a criterion, and
   round 2 must still write the clause that someone can run.
4. Add the criteria the prototype's evidence already justifies: that no document with outer `|`
   bars changes, that all 33 existing fixtures still produce their recorded output, and that a
   tab or `>` difference in the indentation is still refused.
5. Add a criterion for the second form of the fault — a bare table inside a blockquote or an
   indent — which the current AC1 does not mention and WI-0002's `## Notes` flagged as
   undemonstrated.

---

## Round 2 — the record

No question was asked in this round, and none needed to be. The stakeholder's answer to `Q-001`
settled the only thing that was theirs; everything below follows from it, from the record, or
from measurement.

### Nothing new was asked, and why that is not an omission

Round 2 turned up two documents the stakeholder was not shown, both produced by the rule they
chose:

- a bare run whose **delimiter** row is the deepest-indented line — `a | b` / `   ---|---` /
  `c | d` — which comes back at column zero as `a | b` / `--|--` / `c | d`;
- a bare run inside a blockquote whose rows carry an uneven extra space — `>  a | b` /
  `> ---|---` / `>  c | d` — which comes back at the shared prefix as `> a | b` / `> --|--` /
  `> c | d`.

Neither is a new decision. Both are the same sentence they already ruled on — *"a table with two
spaces on one row and none on the next isn't tangled — it's just untidy"* — applied to a run whose
uneven rows happen to be different ones. Asking again would be asking them to re-answer `Q-001` in
different words, which the routing order in this skill's step 3 forbids ("already answered — do
not ask again"). They are written into **AC5** as worked examples instead, so that a reader meets
them in the criteria rather than discovering them in the output.

### Everything in the criteria was measured before it was written

The relaxed rule was implemented in a throwaway module — the longest common prefix of the run's
AC15 prefixes is the shared prefix, and every line's remainder past it must be spaces only — and
every transcript that appears in the criteria is what that prototype actually produced. `plan`
owns where the real change lives; nothing under `mdtab/` was touched.

| what was run | result | lands in |
|---|---|---|
| all 33 shipped fixture pairs | `33 fixtures, 0 would change: []` | AC8 |
| the first form of the fault, re-fed with one cell lengthened | today: input returned unchanged. Option A: `   a \| bbbbb` / `----:\|------` / `xxxx \| y    ` | AC2 |
| the second form, in a blockquote and under a two-space indent, re-fed with one cell lengthened | today: input returned unchanged in both. Option A: both re-aligned | AC3 |
| the stakeholder's own uneven-spaces example | today: unchanged. Option A: `a   \| b` / `----\|--` / `ccc \| d` | AC5 |
| delimiter row deepest; blockquote with uneven extra space | both laid out at the shared prefix | AC5 |
| tab-versus-spaces, and `>` versus `>>` | refused before and after | AC6 |
| `ragged-prefix` (outer bars, one row with an extra space) | unchanged before and after — now refused by WI-0001 AC14 rather than by the prefix rule | AC7 |
| every output above, fed back in | fixed point in every case | AC4 |
| the shipped suite, 65 tests, with the prototype patched in | 64 pass, **1 fails** | AC9 |

That last row is the one worth reading twice. The single failing test is
`tests/test_units.py::PaddingPlacementTest::test_ac10_a_bare_right_aligned_first_column_pads_at_the_start_of_the_line`,
and it fails on its final assertion `self.assertIsNone(lay_out(laid_out))` with
`AssertionError: ['   a | b', '----:|--', 'xxxx | y'] is not None`. Its own docstring, written by
WI-0002, says *"When WI-0003 lands, the last assertion here is the one that changes."* So AC9 can
name exactly one test, quote what changes in it, and require the other 64 to pass unmodified —
which is what `WI-0002/Q-003` taught: a criterion that asserts "the suite still passes unchanged"
while the item necessarily changes part of it is not checkable, and has to be amended after the
fact.

### The three R4 defects, closed

1. **AC1 versus AC3 contradicting each other** — closed by splitting the two claims apart. The
   new AC1 states the relaxed rule itself, AC2 and AC3 state the runs that move into the laid-out
   branch, AC5 states the price, and AC6, AC7 and the third `## Out of scope` bullet state what is
   still refused. There is no longer a criterion that says "everything that fails ADR-0003 is
   reproduced byte-for-byte" while another requires one such run to be laid out.
2. **The stale "WI-0002 AC7" citations** — closed in round 1.
3. **AC4 repeating WI-0002 AC14 without a checking clause** — closed by the new AC9, which names
   the one test that changes, quotes the assertion, and says the other 64 pass unmodified.

### The Definition of Ready, re-walked

Against `spec/dor-dod.md` §1, on `item.md` as this round leaves it.

| # | verdict | evidence |
|---|---------|----------|
| R1 | pass | frontmatter unchanged and complete; `validate-workspace` exits 0 |
| R2 | pass | `## Story` unchanged from round 1, where it passed |
| R3 | pass | AC1–AC10, labelled, as checkboxes |
| R4 | **pass** | every criterion names a command and an expected output. AC2, AC3 and AC5 carry transcripts; AC6, AC7 and AC8 are diffs; AC9 names a test path and an assertion; AC10 is stderr and an exit code. AC1 is a definition the others are stated in terms of, and it is decidable line by line — take a run, compute the longest common prefix of its AC15 prefixes, check each remainder is spaces. No unmeasurable adjective survives |
| R5 | pass | four `## Out of scope` bullets, the first and third of which name things a reader would assume are included; the second bullet from round 1 was **rewritten** because the stakeholder's answer overtook it, rather than deleted |
| R6 | **pass** | `Q-001` is `status: answered`; no question on this item is open |
| R7 | pass | `depends-on: WI-0002`, `done`, merged at `984e934` |
| R8 | **pass** | this file, `status: recorded`, with the exchange verbatim |
| R9 | pass | one recognition rule, one change, one branch. The two forms of the fault (AC2, AC3) are the same rule failing and the prototype fixes both at once; splitting them would give two items whose second is unverifiable without the first |
| R10 | **pass** | the combination table in `item.md` `## Notes` — nine rows, each pointing at the criterion or the scope bullet that states the behaviour |

### What is left for `plan`, deliberately

- Where the relaxation lives: `mdtab/scan.py`'s prefix extraction, or rule 2 in `mdtab/table.py`'s
  `lay_out`. The stakeholder confirmed this is not theirs (*"where the fix goes in the code is
  yours to decide"*).
- Whether ADR-0003 has rule 2 amended in place or gains a fifth rule. Amending is authorised by
  ADR-0003's own reversibility clause plus `Q-001`; superseding would need more.
- The one caveat `item.md` `## Notes` records for whoever writes that amendment: ADR-0003 justifies
  relaxation with *"no document that is aligned today would change"*, which is still true but no
  longer the whole story — a bare run with uneven leading spaces is not aligned today and will
  change.
- The correction to `test_rule_2_a_run_whose_prefixes_are_not_byte_identical`'s comment, which
  after this change misattributes why its second assertion holds. The assertion itself is correct
  and unchanged; only the explanation is wrong.

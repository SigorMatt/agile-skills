---
id: WI-0004
type: work-item
title: Leave a cell containing a line break plain, whatever its column marker says
status: done
priority: high
epic: EP-001
created: "2026-08-29T07:18:00Z"
updated: "2026-08-29T08:20:20Z"
arose-from: EP-001/Q-005
branch: wi/WI-0004
outcome: delivered
---

## Story

As someone who writes markdown tables by hand and puts more than one line inside a cell, I want
mdtab to leave such a cell sitting plainly at the left of its column instead of centring or
right-shifting it, so that the alignment markers keep meaning what they mean for ordinary cells
without doing something odd to the multi-line ones.

## Acceptance criteria

**Fully refined, in two rounds.** The stakeholder answered `Q-001`, `Q-002` and `Q-003` on
2026-08-29, and `answer-questions` wrote what they settled into AC1, AC3, AC6 and AC7 below — the
three R4 defects `refine` recorded. Round 2 then closed the last one: AC5 named no test and now
names twenty individually, the R10 table in `artifacts/refinement-qa.md` is complete, that file is
`status: recorded` with the exchange verbatim, and the item passed all ten DoR criteria at
2026-08-29T07:36:01Z with no override. This paragraph said round 2 was still to come until
`review-close` put it into the past tense on 2026-08-29; see `artifacts/review.md` finding 3.

- [x] AC1 — a cell that contains a line break is padded to its column's width with all of its
      padding on the right, exactly as a `:---` (left) column's cells are, whatever marker the
      column carries. **A cell contains a line break when its text contains an HTML `br` tag
      outside a code span** — `<br>`, `<BR>`, `<br/>`, `<br />` and a tag carrying attributes
      such as `<br class="k">` all count, the tag's case, its slash, the spaces inside it and its
      attributes making no difference [src: WI-0004/Q-001]: *"If it breaks the line when I read
      the document, it counts — capitals, a slash, spaces, an attribute, doesn't matter, they are
      all the same thing to me and should be the same thing to the tool."* Today none of them
      does:

      ```
      $ printf '| heading is long | b |\n|:---:|---:|\n| a<br>b | x |\n' | python3 -m mdtab
      | heading is long | b |
      |:---------------:|--:|
      |     a<br>b      | x |
      $ printf '| heading is long | b |\n|---:|---:|\n| a<br>b | x |\n' | python3 -m mdtab
      | heading is long | b |
      |----------------:|--:|
      |          a<br>b | x |
      ```

      In both, the required output has `| a<br>b          | x |` on the last row: the cell sits
      at the left of its column and the padding follows it. The same is required of every spelling
      of the tag, which today are all centred or pushed right together:

      ```
      $ printf '| longer heading | b |\n|:---:|---:|\n| a<BR/>b | x |\n| c<br />d | y |\n| e<br class="k">f | w |\n' | python3 -m mdtab
      |  longer heading  | b |
      |:----------------:|--:|
      |     a<BR/>b      | x |
      |     c<br />d     | y |
      | e<br class="k">f | w |
      ```

      Required: `a<BR/>b`, `c<br />d` and `e<br class="k">f` each sit at the left of the column
      with their padding after them. (`e<br class="k">f` is the widest cell in that column, so it
      is already flush left; a column made wider by another row must still leave it flush left.)
- [x] AC2 — the column's alignment marker in the delimiter row is unchanged by this item. The
      `:---:` and `---:` in the transcripts above still come back as `:---:` and `---:`, widened
      to the column, because the marker is what the author wrote and the stakeholder asked only
      for the cell's *content* to be left alone.
- [x] AC3 — every other cell in the same column is unaffected. Only the cell that contains a
      line break sits left; its neighbours above and below still obey the marker
      [src: WI-0004/Q-002]: *"Only that cell. Putting a break in one row must not go and shift
      rows I never touched … A ragged-looking column is fine; it is telling me the truth about
      what is in it."* So, checkably, on a centred column of three rows where only the middle one
      has a break, the first and third rows come back centred and the middle one flush left; the
      column's width, its marker and every other column are as they are today.
- [x] AC4 — the epic's standing properties still hold on every document above: running the tool
      twice produces the same bytes as running it once, nothing outside a table changes, and the
      tool writes nothing to stderr and exits 0.
- [x] AC5 — every acceptance criterion of WI-0001, WI-0002 and WI-0003 still holds, and the
      project's shipped test suite passes on the final state of the code:
      `python3 -m unittest discover -s tests -t .` exits 0 and reports no failures and no errors.
      **This item is expected to change no existing test.** No test and no fixture in the
      repository contains an HTML `br` tag today —

      ```
      $ grep -rniE '<br' tests/ ; echo "exit $?"
      exit 1
      ```

      — so every existing expectation is about a document this item's rule does not reach. The
      twenty tests a per-cell alignment rule could plausibly disturb are named here, individually
      rather than counted (the rule `review-close` derived on WI-0003), and each must pass
      **unmodified**:

      - `tests.test_units.ColumnAlignmentTest` —
        `test_each_of_the_four_markers_names_its_alignment`,
        `test_spaces_around_a_marker_do_not_change_it`,
        `test_the_body_rows_have_no_say_in_it`,
        `test_a_delimiter_cell_with_no_dash_is_not_a_delimiter_row_at_all`
      - `tests.test_units.PaddingPlacementTest` —
        `test_ac4_a_centred_cell_leans_left_when_the_spare_column_is_odd`,
        `test_ac3_every_cell_of_a_right_column_ends_at_the_same_display_column`,
        `test_ac7_an_interior_pipe_keeps_a_space_on_each_side_under_every_marker`,
        `test_ac10_a_bare_right_aligned_first_column_pads_at_the_start_of_the_line`,
        `test_ac11_a_right_aligned_last_column_ends_the_line_at_its_content`
      - `tests.test_units.WidthIndependenceTest.test_the_pipes_land_in_the_same_places_under_all_four_markers`
      - `tests.test_fixtures.AlignmentTest` —
        `test_ac2_ac3_every_row_of_a_laid_out_table_has_the_same_display_width`,
        `test_ac2_ac3_each_pipe_sits_at_the_same_display_column_in_every_row`
      - `tests.test_fixtures.LayoutShapeTest` —
        `test_ac12_each_column_is_two_plus_the_widest_of_its_header_and_body_cells`,
        `test_ac12_every_cell_has_exactly_one_space_against_each_pipe`,
        `test_ac12_an_empty_cell_renders_as_spaces_between_the_pipes`,
        `test_ac12_the_delimiter_row_keeps_its_colons_and_fills_the_column`
      - `tests.test_fixtures.ContentPreservationTest` —
        `test_ac11_cell_content_survives_apart_from_the_spaces_around_it`,
        `test_ac14_no_line_gains_or_loses_a_pipe`,
        `test_ac14_a_bare_table_stays_bare_and_an_outer_pipe_table_keeps_its_pipes`
      - `tests.test_fixtures.FixtureRoundTripTest.test_ac6_running_the_tool_on_its_own_output_changes_nothing`

      If the implementation does change one of these, or any other existing test, `impl-report.md`
      names that test individually and says what changed about the expectation and why. A count of
      changed tests does not satisfy this criterion.
- [x] AC6 — a **header** cell containing a line break is treated exactly as a body cell is: it
      sits at the left of its column, whatever the marker says [src: WI-0004/Q-003]: *"Yes, the
      header is a cell like any other … I do not want a rule I have to remember an exception to."*
      Today it is centred with the rest:

      ```
      $ printf '| a<br>b | second column |\n|:---:|---:|\n| wide body cell | y |\n' | python3 -m mdtab
      |     a<br>b     | second column |
      |:--------------:|--------------:|
      | wide body cell |             y |
      ```

      Required: the first row comes back `| a<br>b         | second column |`, with the header
      flush left and its padding after it, and the rest of the table unchanged.
- [x] AC7 — a `br` tag written **inside a code span** is not a line break, and that cell goes on
      obeying its column's marker [src: WI-0004/Q-001]: *"The one in backticks is different: that
      is someone showing the tag, not using it, so that cell is an ordinary cell and keeps
      whatever its column says. I do write about markup in these tables, so please get that case
      right."* So this transcript must come back byte-for-byte identical after the change:

      ```
      $ printf '| heading is long | b |\n|---:|---:|\n| `<br>` | x |\n' | python3 -m mdtab
      | heading is long | b |
      |----------------:|--:|
      |          `<br>` | x |
      ```

## Out of scope

- Rendering, wrapping or splitting a multi-line cell across output lines. mdtab changes spacing,
  not content (EP-001 `## Out of scope`), and the stakeholder asked for the cell to be left
  *plain*, not for the table to be laid out over several rows.
- Any table syntax other than the GFM pipe table, and anything inside a fenced code block. The
  epic's exclusions are untouched by this item.
- The five caveats the stakeholder declined as work in `EP-001/Q-004` — no README or `--help`, no
  diagnostic for a declined table, multi-codepoint emoji, large inputs, Python versions other than
  3.12. *"None of the five is worth making work out of… so don't file follow-ups for them."*
  Nothing here reopens any of them.
- The three gaps `EP-001/Q-005` surfaced and the stakeholder waved away — the missing blank line
  in a test file, the "true enough" sentence in the architecture notes, and WI-0002's old
  verification record. *"None of the three small things you listed bothers me in the slightest;
  don't spend another round on a blank line."* No item is to be filed for them.

## Notes

**Why this item exists.** `EP-001/Q-005` asked the stakeholder to accept the engagement. They
declined, on 2026-08-29, for one reason and named it:

> *"Not yet — nearly. The four items are fine, the notes being wrong is your business to fix and
> I'm glad you caught it, and none of the three small things you listed bothers me in the
> slightest; don't spend another round on a blank line. One thing before I sign, though: a cell
> with a line break or a `<br>` in it should just sit top-left, plain, whatever the column marker
> says. Markers are for normal cells, not those. Fix that and we are done."*

That is work no item records, so `answer-questions` filed it here rather than widening a closed
item (`spec/ids-and-statuses.md` §5). It is the only thing standing between this engagement and
its ending: *"Fix that and we are done."*

**The fault, against the shipped tool.** Confirmed at 2026-08-29T07:17Z on the transcripts in
AC1. mdtab treats `a<br>b` as an ordinary run of characters, measures its display width, and pads
it according to the column's marker like any other cell. Nothing in the tool knows a cell can
contain a line break.

### Refinement round 1 — what happened to the four open points

The four ambiguities this item was filed with were audited against the Definition of Ready at
2026-08-29T07:23Z. Three went to the stakeholder, one did not, and two further points were
settled from the record without asking. The audit, the reasoning and the full agenda are in
`artifacts/refinement-qa.md`, which declared `status: agenda` at the time because the
conversation had not happened yet. It happened; the file is `recorded` as of round 2.

1. **What counts as "a line break"** — filed as **`Q-001`**. `<br>` was named explicitly; `<br/>`,
   `<br />`, `<BR>` and a tag with attributes are the same authoring act spelled differently, and
   a break written inside a code span is not that act at all. Three options, with the tool's
   current output for each. Product stake: it decides which of the author's own cells change.
2. **What "top-left" means in a tool that emits one line per row** — **not asked**. "Left" is what
   AC1 states and is checkable. "Top" has no referent in mdtab's output, where a row is one line;
   it describes how a viewer renders the cell, which mdtab does not control and this item does not
   change. Asking someone to restate a phrase they used as one idiom, when the checkable half is
   unambiguous and the other half names nothing the tool can do, would spend their attention on
   nothing. Recorded as an assumption rather than a decision, so that a reader can disagree with
   it: `refinement-qa.md`, "Settled without asking".
3. **Whether the column changes or only the cell** — filed as **`Q-002`**. AC3 currently states
   one of the two readings as though it were settled, which is the R4 defect that question exists
   to fix.
4. **Whether the header row is included** — filed as **`Q-003`**.

Settled from the record without asking, both in `refinement-qa.md` with their basis: the column's
width is still measured from the cell's text exactly as typed (EP-001's success measure and
ADR-0002), and the alignment marker itself is untouched in the delimiter row (the stakeholder's
own *"whatever the column marker says"*, and EP-001 `## Out of scope` — the tool changes spacing,
not content).

### Refinement round 1 — the answers, received 2026-08-29

All three questions were answered by the stakeholder and propagated by `answer-questions`
(`journal.md`, entry of 2026-08-29). What each settled:

1. **`Q-001` — what counts as a line break: option C.** Any HTML `br` tag, however spelled —
   case, slash, internal spaces and attributes all irrelevant — **except** one written inside a
   code span, which is the author showing the tag rather than using it and leaves the cell
   ordinary. The stakeholder took the option `refine` did *not* recommend and gave the reason:
   *"I do write about markup in these tables, so please get that case right."* This is the one
   answer that adds work — mdtab does not look for code spans anywhere today — and it lands on
   `plan` as part of open design question 2 below. Written into AC1 and AC7.
2. **`Q-002` — one cell, not the column: option A.** *"Only that cell. Putting a break in one row
   must not go and shift rows I never touched."* AC3 said this already as a guess; it now says it
   with the answer behind it, and R4 defect 2 is cleared.
3. **`Q-003` — the header is a cell like any other: option A.** *"I do not want a rule I have to
   remember an exception to."* Written into AC6, which is new.

### Refinement round 2 — what it finished

Round 2 asked the stakeholder nothing: every question of theirs was answered, and the three points
that remained were about this project's own tests and its own edge cases, which a different
stakeholder would not answer differently.

- **AC5 now names tests instead of counting them.** No test and no fixture in the repository
  contains a `br` tag, so this item is expected to change none of them; the twenty that a per-cell
  alignment rule could plausibly disturb are listed by name in AC5 and must pass unmodified.
- **The R10 table is complete** in `artifacts/refinement-qa.md`, which is now `status: recorded`
  and carries the three answers verbatim.
- **Three edge cases of the code-span exception are left deliberately unconstrained**, below.

### Deliberately unconstrained, by `refine` at round 2 (DoR R10)

`Q-001` settles that a `br` tag inside a code span is not a line break. It does not settle what a
code span *is* at its edges, and neither would a different stakeholder: these are questions about
markdown's own grammar, not about what the tool is for. `plan` decides them under its own
preference order and records what it chose; `verify` judges the choice against what `plan` wrote,
not against this item.

1. **An unbalanced backtick** — `` a`<br>b `` — where the span is opened and never closed.
2. **A multi-backtick span** — ``` ``<br>`` ``` — and a span containing a literal backtick.
3. **A cell holding both** — `` a`<br>`b<br>c `` — one tag inside a span and one outside. AC1's
   rule as written decides this one: the cell contains a `br` tag *outside* a code span, so it
   sits left. It is listed here because a reader will want to know it was considered rather than
   overlooked.

Not unconstrained, and stated so nobody re-derives it: a `br` tag cannot appear in a **delimiter
row**, because a delimiter cell that contains anything but dashes, colons and spaces stops the run
being a table at all (`tests.test_units.ColumnAlignmentTest.test_a_delimiter_cell_with_no_dash_is_not_a_delimiter_row_at_all`).

### A document this item's answers made stale — fixed

`docs/product/vision.md` v7 said, of the three questions now answered, that *"What 'a line break'
means beyond the `<br>` they named, whether one such cell changes its column or only itself, and
whether the header row is included, are not settled and are `refine`'s to put to them"*. They were
settled on 2026-08-29. `refine` does not write `docs/`, so it filed `Q-004` to the architect,
non-blocking; `answer-questions` answered it the same day and `vision.md` is now **v8**, carrying
the four answers in the stakeholder's own words with the criteria that hold them. Nothing is
outstanding here — it is recorded because a reader of this item should be able to see that the
document was checked rather than assume it.

### Open design questions, for `plan`

Neither would be answered differently by a different stakeholder, so under `refine`'s routing rule
they are design decisions rather than questions for a person.

1. **Where the per-cell override lives** — in the scanner, in the table model, or at render time —
   and whether ADR-0007 is amended or gains a companion.
2. **How the break is detected in the cell text**, and how that interacts with the existing
   escaped-pipe handling. `Q-001` decides what counts; the mechanism is `plan`'s.
3. **How much of a code span the tool needs to understand** to satisfy AC7, and which answer it
   gives to the three unconstrained cases above. mdtab looks for a code span nowhere today, so
   this is new machinery rather than a new use of old machinery, and it is the only part of this
   item that is.

**A design note for `plan`, not a decision.** ADR-0007 records that alignment is placed inside
the `cells` field, and `docs/architecture/overview.md` describes how a cell's padding is chosen.
Whichever way the questions above are settled, this item changes what decides a cell's padding
and both documents will need amending — the pattern `review-close` recorded on WI-0003, that
`plan` has no step for updating the documents a change invalidates, applies squarely here.

### Accepted gap, recorded by `review-close` at 2026-08-29T08:02Z

**ADR-0010 §2 rule 2 describes the code-span exclusion more broadly than the code implements it,
and that is accepted rather than fixed.** The rule reads *"Code spans are found first and their
contents, delimiters included, are excluded from the search."* `mdtab/inline.py` finds the spans
and then takes a `br` tag when the tag match's **start index** lies outside every span. The two
readings part company on one shape only — a tag that begins outside a span and ends inside one,
such as `` a<br `>` b `` — which the implemented rule counts as a line break and a
blank-the-spans-out reading would not.

`implement` declared it as deviation 1 of `impl-report.md`; `verify` checked rather than accepted
it and confirmed that every case AC1, AC7 and ADR-0010 §3 name gives the same answer under either
reading; `verify-report.md` records the shape under `## Not verified, and why` because no criterion
decides it. Nothing delivered is wrong, and no acceptance criterion of this item distinguishes the
two readings.

It is written here rather than left in the two reports because an accepted gap that lives only
inside a report is not read again once the item closes. If the sentence is judged **false** rather
than merely broader than the code, ADR-0009 is the route — corrected in place, `status: accepted`
retained, the old sentence quoted in full in the change log — and that is the architect's act, not
the reviewer's or the developer's. `review-close` did not make it. See `artifacts/review.md`
finding 2.

### A note for the execution that ends the engagement, recorded by `review-close` at 2026-08-29T08:17Z

`docs/product/vision.md` v9 closes `## Open at the time of writing` with *"They have not yet been
asked whether they accept the engagement as it now stands"*. That is true at this close —
`scripts/engagement-state EP-001` reports `active` while WI-0004 is in flight — and it stops being
true the moment `review-close` is dispatched on **EP-001** and files the `kind: sign-off` question,
which is the next thing the orchestrator does once this item is `done`.

It is not a defect in this item: D12 asks whether the claims about the *behaviour* this item
touched are true, and this sentence is about the state of the engagement. It is recorded here
rather than left in `artifacts/review.md` finding 4 because this one document has now cost two
send-backs on D7 and D12, both for describing a state of the work that had moved on, and the
execution that ends the engagement will have to bump it again for the same reason.

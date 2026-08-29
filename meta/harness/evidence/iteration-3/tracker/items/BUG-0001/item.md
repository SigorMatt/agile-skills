---
id: BUG-0001
type: bug
title: "Two documents claim a column's width does not depend on its marker; it does"
status: done
priority: medium
epic: EP-001
created: "2026-08-28T22:34:19Z"
updated: "2026-08-28T23:23:53Z"
found-in: WI-0002
branch: wi/BUG-0001
outcome: delivered
---

## Summary

Two documents state, as an absolute, that a column's width is independent of the alignment marker
in its delimiter cell. It is not: `_column_widths` in `mdtab/table.py` raises a column's width so
that its delimiter cell can still be written, and how wide that cell must be is `1 + one column
per ":" the marker carries`. A column narrow enough for that floor to bind is therefore one or two
columns wider with `:-:` than with `---`, from the same content. The code is right — the floor is
what WI-0001 AC6 (idempotence) forces, and `docs/architecture/overview.md`'s own "How wide a
column is" bullet states it correctly — so this is a defect in what the documents say, not in what
the tool does.

The sentence originates in `ADR-0007` decision 4 and was repeated into
`docs/architecture/overview.md` v3. Both cite `WI-0002 AC6`, which says something narrower and
true: *"a column's width does not depend on its **alignment**"*. Alignment is where the content
sits in a field; the marker is the text in the delimiter cell. WI-0002 changed the first and never
touched the second, so its criterion supports the narrow claim and not the wide one. This is
F-001's shape exactly — one absolute sentence, re-quoted from document to document rather than
re-checked against the code — and it is why `EP-001` did not close on the run that found it.

## Steps to reproduce

1. From a checkout, with Python 3 and nothing installed:

   ```
   printf 'a | | b\n---|---|---\nc | | d\n' | python3 -m mdtab
   ```

2. Run the same document again with a centre marker on the middle column, changing nothing else:

   ```
   printf 'a | | b\n---|:-:|---\nc | | d\n' | python3 -m mdtab
   ```

3. Compare the width of the middle column in the two outputs.

## Expected behaviour

`docs/architecture/overview.md`, `## Rules that live in exactly one place`, bullet *"Where a
cell's content sits in its field"*, last sentence:

> The guard spaces are outside the field and do not move, and no column's width depends on its
> marker [src: ADR-0007; src: WI-0002 AC6].

and `docs/architecture/adr/ADR-0007-alignment-is-placed-inside-the-cells-field.md`, `## Decision`
item 4:

> `_column_widths` is not touched. A column's width does not depend on its marker
> [src: WI-0002 AC6], so the two rules idempotence forces stay exactly where
> `docs/architecture/overview.md` says they are [src: WI-0001/Q-005].

Read literally, both say the middle column must come out the same width in steps 1 and 2.

## Actual behaviour

Step 1, exit 0 (`cat -A`, so `$` marks end of line):

```
a |  | b$
--|--|--$
c |  | d$
```

Step 2, exit 0:

```
a |   | b$
--|:-:|--$
c |   | d$
```

The middle column is 2 display columns wide with `---` and 3 with `:-:` — the marker changed the
width, from identical content. `mdtab/table.py`, `_column_widths`, is where it happens:

```python
width = 2 + max(content)
marker = rows[1][column].strip(_TRIM)
needed = 1 + marker.startswith(":") + marker.endswith(":")
omitted = _spaces_omitted(column, columns, leading, trailing)
widths.append(max(width, needed + omitted))
```

`needed` reads the marker, and `max(width, needed + omitted)` lets it decide the result whenever
the content is narrow enough.

## Acceptance criteria

- [x] AC1 — `docs/architecture/overview.md`'s *"Where a cell's content sits in its field"* bullet
      no longer asserts that no column's width depends on its marker. What it says instead is true
      of the code as it stands and does not contradict the *"How wide a column is"* bullet four
      lines below it, which states the floor rule; whichever sentence replaces it cites something
      that supports it, and someone reading only the two bullets can predict the output of both
      commands in `## Steps to reproduce`.
- [x] AC2 — `ADR-0007`'s `## Decision` item 4 no longer asserts it either. ADR-0007 is `accepted`
      and its decision is unchanged in substance — `_column_widths` genuinely is not touched by
      alignment — so this is a correction of a wrong justification within a standing decision, not
      a supersession: the ADR keeps its status and records the correction in its own change log.
- [x] AC3 — both documents carry a version bump and a change-log row naming this item, per
      `spec/doc-header.md` §3.
- [x] AC4 — a test in `tests/` runs both commands from `## Steps to reproduce` and asserts the
      middle column is 2 columns wide in the first and 3 in the second. It fails if
      `_column_widths`' floor is removed, so the behaviour the corrected sentences describe is
      pinned by something that runs.
- [x] AC5 — `python3 -m unittest discover -s tests -t .` exits 0, and
      `.claude/agile-skills/scripts/lint-claims --all` exits 0.
- [x] AC6 — no file under `mdtab/` changes. The tool's behaviour is correct and this item does not
      touch it; a diff that reaches `mdtab/` is out of scope and belongs to a different item.

## Out of scope

- **Changing `_column_widths`.** The floor is forced by WI-0001 AC6 and is verified: removing it
  makes `mdtab | mdtab` stop being a fixed point for a degenerate column. The documents are what
  is wrong.
- **Auditing every other claim in `docs/`.** The termination review of EP-001 walked the absolute
  claims in `docs/architecture/overview.md`, `docs/product/vision.md` and the eight ADRs against
  the code and found this one and no other; that audit is recorded in
  `tracker/items/EP-001/artifacts/review.md` and does not need repeating here.
- **Amending `WI-0002` AC6.** It is correctly worded and correctly ticked. It says *alignment*,
  and alignment is what it verified.

## Notes

RB5's regression test is AC4, and it is possible here because the defect is observable from the
command line: the documents make a prediction about output, and the test makes the same prediction
and would fail if the code stopped agreeing with the corrected text.

This item was filed by `review-close` during EP-001's termination review, under DE6 — *"every
claim in `docs/` about behaviour this epic delivered has been checked against the code during this
epic"* — and it is the reason EP-001 did not close on that run. Consequences worth knowing before
picking it up:

- **The engagement left rest.** `EP-001/Q-004`, the sign-off the stakeholder answered accepting
  the engagement, names three children and this is a fourth. Per `spec/question.md` §2 a sign-off
  is due once per rest, so when this item reaches a terminal status the stakeholder is asked
  again, about an engagement that now includes it.
- **This is not one of the five caveats the stakeholder declined.** Answering the sign-off they
  said *"don't file follow-ups for them"* about five named gaps — no README, no diagnostics,
  multi-codepoint emoji, large documents, older interpreters. This is none of those: it is a
  defect nobody had found when they answered, and the sign-off they were shown told them *"no bug
  was filed and left unfixed"*, which is a sentence that stays true only if this one is filed.
- `found-in` names WI-0002 because ADR-0007 and the overview bullet were written for it. The
  behaviour the sentence is wrong about was delivered by WI-0001 (AC6, AC12, `WI-0001/Q-005`), so
  a fix will read that item's record as well.

Added by the review that closed this item (`artifacts/review.md`, `## Accepted gaps`), so that
each survives the item rather than living only inside a report:

- **A blank line was lost above `parsed()` in `tests/test_units.py`.** The third pass removed the
  `os`/`subprocess`/`sys` imports and overshot by one line, so `parsed()` sits one blank line below
  the import block where every other top-level definition in that file has two. Accepted as
  cosmetic — the project's lint command compiles rather than lints, so nothing enforces the
  convention — and no criterion of this item covers it. A one-line fix for whoever next touches
  that file.
- **AC1's "someone reading only the two bullets can predict the output of both commands" passed on
  a stated reading.** The two bullets give the quantity the two outputs differ in and the rule
  that produces it, not the whole rendering arithmetic, so they do not let a reader reconstruct
  the two outputs byte for byte. Two consecutive verifications and two reviews agree the stricter
  reading is satisfiable by no pair of bullets in a rules-live-in-one-place list.
- **`tracker/items/WI-0002/artifacts/review.md` line 64 is a wrong verification record on a closed
  item** — it reports checking this very sentence against the code and finding that it held,
  having checked the guard-space half and the four-marker layout, neither of which reaches the
  width floor. Accepted as history rather than a live claim, and deliberately not filed as a
  follow-up: doing so would put a correction to a closed item's paperwork in front of the
  stakeholder as an undelivered child of the epic.

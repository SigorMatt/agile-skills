---
id: EP-001
type: epic
title: Pretty-align markdown tables in a stdin-to-stdout filter
status: done
priority: high
created: "2026-08-28T18:24:15Z"
updated: "2026-08-29T08:37:26Z"
outcome: delivered
---

## Goal

Someone editing markdown by hand can pipe a document through one command and get the same
document back with every table laid out so its columns line up in a plain text editor, with the
alignment the author asked for preserved, and with every line that is not part of a table
returned exactly as it was written.

## Why now

Markdown tables are written by hand and edited by hand. Adding a word to one cell puts every
pipe on that row out of line with the rows above it, and re-padding a table by hand is tedious
enough that people stop doing it — so tables in real documents drift into an unreadable state
and stay there. There is no way to fix one today without doing it manually, cell by cell, and
the cost of not solving it is paid on every edit of every table for as long as the document
lives.

## Success measures

- Running the tool with a markdown document on stdin and comparing stdout to the input shows
  that every line outside a table is byte-for-byte unchanged.
- For any table in the output, every row has its `|` characters at the same *display* column, so
  the table's column boundaries form straight vertical lines when the output is viewed in a
  fixed-width font — including for tables whose cells contain accented letters, emoji or CJK
  text, which are measured by how much room they take up on screen rather than by how many
  characters they are (`EP-001/Q-003`, ADR-0002).
- Running the tool twice in succession produces the same output as running it once
  (`tool < in.md > a.md; tool < a.md > b.md; diff a.md b.md` is empty).
- Feeding the tool's own output back to a markdown renderer produces the same rendered table as
  the original input did — the tool changes spacing, not content.
- A document containing no tables at all passes through byte-for-byte unchanged.
- A pipe table written inside a fenced code block comes back byte-for-byte unchanged, because
  inside a fence it is text the author typed on purpose (`EP-001/Q-002`).
- The tool runs on a machine with only Python 3 installed, straight from a checkout, with no
  install or build step first (`EP-001/Q-001`, ADR-0001).

## Scope

- A filter: reads a markdown document on stdin, writes the rewritten document on stdout,
  implemented in Python 3 using only the standard library (`EP-001/Q-001`, ADR-0001).
- Detecting **GFM pipe tables** in the input — rows delimited by `|`, with a delimiter row of
  dashes under the header — and rewriting their spacing so columns align (`EP-001/Q-002`).
- Honouring the alignment markers in a table's delimiter row — for ordinary cells. A cell that
  contains a line break is left plain at the left of its column whatever its column's marker says
  (`EP-001/Q-005`, WI-0004): *"Markers are for normal cells, not those."*
- Measuring cell width as display width, so tables containing non-ASCII text align on screen
  (`EP-001/Q-003`, ADR-0002).
- Leaving everything that is not a table exactly as it was.

## Out of scope

- Any table syntax other than the GFM pipe table: reStructuredText or grid tables (`+---+`) and
  raw HTML `<table>` elements are not recognised and pass through as prose. The stakeholder
  writes neither (`EP-001/Q-002`). Either could be added later as its own item under this epic.
- Anything inside a fenced code block, including a pipe table written there. It is content, not
  a table (`EP-001/Q-002`).
- Third-party runtime dependencies, packaging, or any install step between cloning the
  repository and running the tool (`EP-001/Q-001`, ADR-0001).
- Editing files in place, taking filename arguments, or recursing over a directory. The
  stakeholder asked for a filter; anything else is a different tool wrapped around this one.
- Changing the *content* of a table: no sorting rows, no adding or removing columns, no
  rewrapping long cells, no escaping or unescaping cell text.
- Reformatting any other part of a markdown document — headings, lists, code fences, line
  length. Only tables are touched.
- Validating or reporting on the markdown: the tool is not a linter and emits no diagnostics
  about document quality.
- Any editor plugin, language server, or packaging for a plugin ecosystem.

## Stakeholder acceptance

**The engagement is accepted. Read this paragraph before the rest of the section.** The third
sign-off (`EP-001/Q-006`) was answered on 2026-08-29 and the stakeholder accepted the engagement as
it stands, all five children, choosing option **A**. That answer supersedes the "second sign-off
was refused" record below as a description of the present, and it settles the correction the first
record carries. All three earlier records are kept, because each states accurately what the
stakeholder was shown and what they said at the time, and an acceptance covers only what its own
sign-off put in front of them. **The current statement of the engagement is the last record in
this section — "The third sign-off was given".**

The stakeholder was asked whether they accepted this engagement (`EP-001/Q-004`, `kind:
sign-off`) and answered on 2026-08-28: *"Yes — A. Accept it and close it… It does the job I
wanted it for."* They had run the tool on a document of their own first, and reported that the
columns line up, the alignment markers put the text where they said they would, and everything
that was not a table came back exactly as typed.

That selects **ending E1** of `spec/ids-and-statuses.md` §3.5 — accepted with every child
delivered — so this epic ends at `done` with outcome `delivered`, not `delivered-partial`.
WI-0001, WI-0002 and WI-0003 are its only children and all three are `done` with outcome
`delivered`; no bug was ever filed and nothing is blocked.

**Superseded as a statement of the present, five minutes after it was written.** The same
termination review that filed `Q-004` also ran DE6 — the claim audit — and it found one false
absolute in `docs/architecture/overview.md` and `ADR-0007`, so it filed `BUG-0001` and the
engagement left rest. The paragraph above records accurately what the stakeholder was told and
what they accepted on 2026-08-28T22:29:11Z; it is no longer a true description of the engagement,
which now has **four** children. BUG-0001 is `done` with outcome `delivered` since
2026-08-28T23:23:53Z, it changed no file under `mdtab/`, and the acceptance it needs is
`EP-001/Q-005`, filed because an acceptance covers what the stakeholder was shown when they gave
it (`spec/question.md` §2 — one sign-off per rest).

Five things the tool has not been pushed on were surfaced in the sign-off, and the stakeholder
declined every one of them as work: *"None of the five is worth making work out of… so don't file
follow-ups for them."* They are no README or `--help`; no way to ask the tool why it declined a
table; multi-codepoint emoji that may not align; nothing larger than about 30 lines having been
through it; and only Python 3.12 having actually run it. Each is recorded with the reason given
in `docs/product/vision.md` (v6, `## Accepted as delivered`). **No follow-up item is to be filed
for any of them**, here or later, on the strength of this engagement.

**The second sign-off was refused, and the engagement is not over.** `Q-005` was answered on
2026-08-29 and the stakeholder did not accept:

> *"Not yet — nearly. The four items are fine, the notes being wrong is your business to fix and
> I'm glad you caught it, and none of the three small things you listed bothers me in the
> slightest; don't spend another round on a blank line. One thing before I sign, though: a cell
> with a line break or a `<br>` in it should just sit top-left, plain, whatever the column marker
> says. Markers are for normal cells, not those. Fix that and we are done."*

That is Q-005's option **C** — do not accept, and say what is missing — and it settles four
things. The four existing children are accepted as built and none is reopened. The three gaps
`Q-005` surfaced are dismissed as work; **no item is to be filed for the missing blank line, the
"true enough" sentence, or WI-0002's old verification record**, on the same footing as the five
caveats above. Filing the documentation bug was endorsed rather than objected to. And one
behaviour the engagement never had is now a condition of its acceptance, filed as **WI-0004** at
`draft` (`spec/ids-and-statuses.md` §5, `arose-from: EP-001/Q-005`).

This is **not** ending E3. E3 is the impasse — every child terminal, the stakeholder not
accepting, and no way forward — and the refusal here names a way forward and asks for it: *"Fix
that and we are done."* The engagement leaves rest because WI-0004 is not terminal, the epic
returns to `open`, and when it next comes to rest `review-close` files a third sign-off, because
one acceptance is due per rest and this one accepted nothing (`spec/question.md` §2). Only
`review-close` may end an engagement, and this execution did not try to
(`spec/ids-and-statuses.md` §3.5).

**The third sign-off was given, and it ends the engagement.** `Q-006` was filed when WI-0004
closed and the engagement re-reached rest at 2026-08-29T08:20:20Z — one acknowledgment per rest,
and `Q-005` accepted nothing. It named all **five** children, showed the line-break behaviour as a
transcript run on merged `main`, and offered accept / accept-with-follow-ups / refuse / withdraw.
The stakeholder answered on 2026-08-29 with option **A**:

> *"Yes — accept it, all five, and close it. The one thing I asked for is there: a cell with a
> break in it sits plain at the left and nothing around it moved, and everything that is not a
> table still comes back exactly as I typed it, which is the part I care most about. The note of
> yours that is worded loosely is your business and not worth another round — don't open anything
> new for it."*

That selects **ending E1** of `spec/ids-and-statuses.md` §3.5 — accepted, with every child
delivered — so this epic ends at `done` with outcome `delivered` rather than `delivered-partial`.
Its five children are WI-0001, WI-0002, WI-0003, BUG-0001 and WI-0004; all five are `done` with
outcome `delivered`, nothing is blocked, and no bug is filed and unfixed.

The two gaps `Q-006` surfaced were **declined as work**, in the same words: the sentence in
ADR-0010 §2 and WI-0004's plan that says code spans are *"excluded from the search"* where the code
excludes a tag whose *start* is inside one, and the tool's deliberately partial knowledge of
backticks. **No item is to be filed for either**, here or later, on the same footing as the five
caveats declined at `Q-004` and the three gaps declined at `Q-005`. Option **B** — accept with
follow-ups named — was offered for exactly these and explicitly turned down.

Ending the epic is `review-close`'s to do and `answer-questions` did not attempt it: this answer
returns EP-001 to its recorded `resume-to` of `open`, where the termination review applies the
epic Definition of Done and records E1 (`spec/ids-and-statuses.md` §3.5).

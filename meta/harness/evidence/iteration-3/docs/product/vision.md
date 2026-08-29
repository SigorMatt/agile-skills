---
title: Product vision — mdtab
version: 11
status: current
updated: 2026-08-29T08:28:09Z
updated-by: answer-questions
updated-for: EP-001
---

# Product vision — mdtab

## Who this is for

People who write and edit markdown by hand — in a text editor, in a repository, in a pull
request — and who put tables in it. They are comfortable at a terminal and comfortable piping
text through a command. They are not necessarily using any particular editor, and they are not
looking for a plugin.

## What it is for

mdtab is a filter. It reads a markdown document on standard input and writes the same document
on standard output, with the spacing inside its tables rewritten so the columns line up in a
fixed-width font, and with the alignment the author declared in each table's delimiter row
reflected in how the cells are padded. Everything outside a table comes back exactly as it went
in.

A "table", for mdtab, is a GFM pipe table: rows delimited by `|`, with a row of dashes under the
header that may carry alignment markers. That is the only syntax it recognises, because it is the
only syntax the stakeholder writes [src: EP-001/Q-002]. Grid tables, reStructuredText tables and
raw HTML `<table>` elements are prose as far as mdtab is concerned, and pass through untouched.
So does a pipe table written inside a fenced code block, which is text somebody typed on purpose
[src: EP-001/Q-002].

Outer `|` characters are optional and indentation is allowed: `a | b` is as much a table as
`| a | b |`, and a table inside a blockquote or under a bullet is aligned like any other
[src: WI-0001/Q-002]
[src: WI-0001/Q-003]. What mdtab will not do is tidy a table it does not fully
understand — one whose rows disagree about how many cells they have, about their outer pipes, or
about their indentation in a way it cannot make sense of. Such a table comes back exactly as it
went in, still looking wrong, which is what the stakeholder asked for: *"The tool's job is to tidy
tables it understands, and if it doesn't understand one it should keep its hands off"*
[src: WI-0001/Q-001]. Inside a table it does understand, mdtab changes spaces and nothing else —
it never adds or removes a `|`, so a table written without outer bars comes back without them
[src: ADR-0008].

Where the line falls on indentation moved once, deliberately. Rows that differ only in how many
**spaces** they carry are not a table mdtab fails to understand: it takes the indent they share,
treats the rest as part of the first cell, and tidies the table back to that shared indent
[src: ADR-0008; src: WI-0003 AC5]. Rows that differ by a **tab** or by a `>` still are: nothing
here defines how wide a tab is, so mdtab does not guess, and such a run is copied through
untouched [src: WI-0003 AC6]. That is the stakeholder's own distinction, in their words:
*"a table with two spaces on one row and none on the next isn't tangled — it's just untidy, which
is the exact thing I wanted the tool for. Tabs and the quote marks having to match exactly sounds
right to me"* [src: WI-0003/Q-001].

The alignment markers in a delimiter row are honoured in every column, with one exception the
stakeholder asked for afterwards. What they wanted first was *"Whatever the marker says, that's
where the text sits in the cell — every row, every column, no exceptions"* [src: WI-0002/Q-001],
and that is what mdtab does for every ordinary cell. The exception is a cell that reads as two
lines — one holding an HTML `br` tag — which sits plain at the left of its column whatever the
marker says [src: WI-0004 AC1; src: ADR-0010]. It is described in full below. A centred cell that cannot halve its spare space puts the extra
column on the right, so the text leans left and mdtab's output matches what `prettier` and
`pandoc` produce [src: WI-0002/Q-001]. That holds even in the one place where it costs something:
the first column of a table written without a leading `|` has no bar in front of it, so
right-aligning it puts spaces at the start of the line, and the stakeholder chose that over an
exception — *"a space at the front of the line is a price I'll pay"* [src: WI-0002/Q-002]. A table
mdtab has laid out is a table mdtab still recognises: making that true where those leading spaces
appear is [src: WI-0003], filed because the stakeholder refused to work around the fault rather
than fix it.

Columns line up **on screen**, not by character count. A cell's width is how much room its text
takes up in a fixed-width font, so a table containing accented names, emoji or CJK text aligns
like any other [src: EP-001/Q-003]; the rule that computes it is [src: ADR-0002].

It runs anywhere Python 3 runs, with no install step: clone the repository and pipe a document
through it [src: ADR-0001].

The value is that a hand-edited table stops decaying. Adding a word to one cell no longer means
re-padding every row by hand, so tables in long-lived documents stay readable instead of
drifting into a state nobody is willing to fix.

## Accepted as delivered

**The engagement is accepted, and this is the acceptance that says so.** The stakeholder was asked
three times, because an acceptance covers only what its own sign-off put in front of them. They
accepted on 2026-08-28 [src: EP-001/Q-004]; a fifth item then existed that the first acceptance had
not covered, so they were asked again on 2026-08-29 and **withheld** it pending one behaviour
[src: EP-001/Q-005]; that behaviour was built [src: WI-0004], and on 2026-08-29 they were asked a
third time and accepted, all five items:

> *"Yes — accept it, all five, and close it. The one thing I asked for is there: a cell with a
> break in it sits plain at the left and nothing around it moved, and everything that is not a
> table still comes back exactly as I typed it, which is the part I care most about. The note of
> yours that is worded loosely is your business and not worth another round — don't open anything
> new for it."* [src: EP-001/Q-006]

The five items are [src: WI-0001] (the filter itself), [src: WI-0002] (the alignment markers),
[src: WI-0003] (recognising a table it laid out itself), [src: BUG-0001] (a false statement in the
architecture notes, no change to the tool) and [src: WI-0004] (the line-break behaviour above).
All five were delivered; nothing was dropped and nothing is blocked.

**Two things were put to them at this third sign-off and declined as work**, so a later reading of
this document finds a decision rather than an unexplored gap:

- **One sentence in the design record is broader than the code it describes.** [src: ADR-0010] §2
  and WI-0004's plan say code spans are *"excluded from the search"* for a `br` tag; the code takes
  a tag when the tag *starts* outside a span. The readings differ on one shape only — a tag opening
  outside backticks and closing inside them, `` a<br `>` b `` — and every case the stakeholder named
  answers the same either way. Declined in their words: *"your business and not worth another
  round — don't open anything new for it."*
- **mdtab did not learn the rest of markdown's rules about backticks.** It knows a run of *n*
  backticks is closed by a run of *n*, and nothing more. Everything asked for turns on that much.

**No item is to be filed for either**, on the same footing as the five caveats below and the three
gaps declined at the second sign-off. The acceptance below records what they said on 2026-08-28 and
remains an accurate account of that; the sentence above is the engagement's present state.

The stakeholder was shown what had been built and asked whether they accepted it
[src: EP-001/Q-004], and on 2026-08-28 they did, without follow-ups: *"Yes — A. Accept it and
close it… It does the job I wanted it for."* They ran it on a document of their own before
answering, and checked three things — the columns line up, the markers put the text where they
said they would, and everything that was not a table came back exactly as typed.

Five things the tool has not been pushed on were put in front of them at the same time, and all
five were **declined as work**: *"None of the five is worth making work out of… so don't file
follow-ups for them."* They are recorded here, with the reasons given, so that a later reading of
this document finds a decision rather than an unexplored gap:

- **No README and no `--help`.** Declined in their own words: *"I'm not going to read a README for
  something with nothing to configure."*
- **The tool is silent about everything, always** — there is no way to ask it why it left a table
  alone. That silence is what was asked for; being unable to interrogate it is accepted.
- **Emoji made of several joined characters** (a flag, a family, a skin tone) may not line up,
  because nothing defines how wide an editor draws them. Accented letters, CJK and single emoji
  are handled.
- **Nothing large has been through it.** The largest document any test uses is about 30 lines.
  Declined because *"my files are documents, not five thousand lines"*.
- **Only Python 3.12 has actually run it.** It is written to run on 3.8 and that was checked by
  reading rather than by running, because no older interpreter is installed here.

None of the five is a defect, and none is scoped work waiting to be done. Anything wanted later
starts as a new engagement rather than as a reopening of this one.

## What it deliberately is not

- **Not a formatter for markdown generally.** It touches tables. Headings, lists, code fences,
  line length and everything else are none of its business.
- **Not an editor of content.** It changes whitespace. It does not sort rows, add or remove
  columns, rewrap cell text, or alter what a table says.
- **Not a linter.** It does not report problems with a document; it produces a document.
- **Not a file manager.** It does not take filenames, edit in place, or walk a directory. It is
  one filter, and anything file-shaped is a shell loop around it.
- **Not an editor integration.** No plugin, no language server, no packaging for an editor
  ecosystem.

## Settled since the first version

The three things this vision was written without are now answered by the stakeholder, and the
answers are above rather than here: the runtime and how the tool is invoked
(`EP-001/Q-001`, recorded as [src: ADR-0001]), which table syntaxes count as a table
(`EP-001/Q-002`), and how the width of a cell is measured when its text is not plain ASCII
(`EP-001/Q-003`, recorded as [src: ADR-0002]).

## Open at the time of writing

**The one behaviour that was wanted is now built.** Asked to accept the engagement a second time,
the stakeholder said not yet, and named one thing [src: EP-001/Q-005]:

> *"a cell with a line break or a `<br>` in it should just sit top-left, plain, whatever the
> column marker says. Markers are for normal cells, not those. Fix that and we are done."*

mdtab now knows a cell can contain a line break. A cell holding an HTML `br` tag is placed as if
its column were left-aligned, whatever marker the column carries, and the padding follows the text
[src: WI-0004 AC1; src: ADR-0010]:

```
$ printf '| heading is long | b |\n|:---:|---:|\n| a<br>b | x |\n' | python3 -m mdtab
| heading is long | b |
|:---------------:|--:|
| a<br>b          | x |
```

Before [src: WI-0004] that last row came back `|     a<br>b      | x |` under `:---:` and
`|          a<br>b | x |` under `---:` — centred and pushed right like any other run of
characters.

**What they meant by it, and what it does.** The three things this document said were unsettled
were put to the stakeholder on 2026-08-29 and answered, and the answers are the rule the tool now
follows [src: WI-0004 AC1; WI-0004 AC3; WI-0004 AC6; WI-0004 AC7]:

- **Any way of writing the tag counts** [src: WI-0004/Q-001] — *"If it breaks the line when I read
  the document, it counts — capitals, a slash, spaces, an attribute, doesn't matter."* So `<br>`,
  `<BR>`, `<br/>`, `<br />` and a tag carrying attributes are one thing to the tool.
- **Except inside a code span** [src: WI-0004/Q-001] — *"The one in backticks is different: that is
  someone showing the tag, not using it… I do write about markup in these tables, so please get
  that case right."* A cell holding `` `<br>` `` is an ordinary cell and keeps its column's marker.
  This is the part of the item that was new machinery: before it, mdtab looked for a code span
  nowhere. It does now, in `mdtab/inline.py`, and that is the only inline markdown it reads.
- **One cell, never its column** [src: WI-0004/Q-002] — *"Putting a break in one row must not go and
  shift rows I never touched… A ragged-looking column is fine; it is telling me the truth about
  what is in it."*
- **The header row is included** [src: WI-0004/Q-003] — *"the header is a cell like any other… I do
  not want a rule I have to remember an exception to."*

**Nothing is open.** Every item in this engagement has been built and closed, nothing about *what
the tool should do* is waiting on the stakeholder, and the acceptance that was outstanding when v10
of this document was written has been given. They were asked the third sign-off on 2026-08-29
[src: EP-001/Q-006], naming all five child items, and they accepted — the ending they promised at
the second sign-off, *"Fix that and we are done"*. What they accepted, and the two things they
declined as work at the same time, are in "Accepted as delivered" above.

Everything else is closed. The four delivered items are accepted as built, and the three gaps put
to the stakeholder at the second sign-off — a blank line missing from a test file, one sentence in
the architecture notes judged "true enough" rather than exact, and a closed item's verification
record that checked the wrong half of a claim — were dismissed as work in their own words: *"none
of the three small things you listed bothers me in the slightest; don't spend another round on a
blank line."* No item is to be filed for any of them, on the same footing as the five caveats
above.

The centring question this section carried since v2 — how a centred cell divides an odd number of
spare columns — is answered and is above. The question this section carried at v4 — how mdtab
should tell a table it indented itself from one the author indented unevenly — was put to the
stakeholder as [src: WI-0003/Q-001] and answered on 2026-08-28, and its premise did not survive
the answer: mdtab does **not** go on leaving an unevenly space-indented table alone. It tidies it,
back to the indent its rows share. Tabs and `>` stay strict. That answer is recorded above and in
[src: ADR-0008].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 11 | 2026-08-29T08:28:09Z | answer-questions | EP-001 | The stakeholder answered the third sign-off [src: EP-001/Q-006] and **accepted** the engagement, all five children, option A. Two statements in this document became false the moment they did. "Accepted as delivered" opened *"the acceptance recorded below … is not the engagement's final word"* and *"it is no longer a statement that the engagement is accepted"*; it now opens with the acceptance that is, in their words, with all five items named and the two gaps they declined as work recorded so no execution files one of them. "Open at the time of writing" said they *"have not yet answered"*; nothing is open, and it now says so. The 2026-08-28 acceptance is kept below the new one because it accurately records what they were shown then. No item was filed, per *"don't open anything new for it"*; no ADR was written and no acceptance criterion was amended. One further false sentence was corrected while this version was being written, found by re-reading the section rather than by a gate: *"mdtab looks for a code span nowhere today"* survived v9's sweep and had been false since `mdtab/inline.py` landed, so it is now in the past tense and names the module. No item was filed for it — it is a tense error in a document this execution is already the author of, not scoped work |
| 10 | 2026-08-29T08:23:12Z | review-close | EP-001 | [src: WI-0004] closed and merged, and this section's last paragraph said the stakeholder *"have not yet been asked whether they accept the engagement as it now stands"*. That was true when v9 was written at 08:05Z and stopped being true at 08:22Z, when the engagement reached rest and this skill filed the third sign-off [src: EP-001/Q-006] naming all five children. The paragraph now says they have been asked and have not yet answered. Written by `review-close` rather than sent back to `implement`, because the item that would have carried the fix is closed and the sentence was made false by this execution's own act; the correction is declared in [src: tracker/items/WI-0004/artifacts/review.md] finding 4 and in the epic's journal |
| 9 | 2026-08-29T08:05:54Z | implement | WI-0004 | [src: WI-0004]'s code landed and this document still described the tool without it, in two places. "Open at the time of writing" said *"One behaviour is wanted and is not built"*, that *"Today mdtab does not know a cell can contain a line break"*, that the change was *"filed as [src: WI-0004], at `ready`"*, and that *"The behaviour is still wanted and still not built"*; all four were false once `mdtab/inline.py` and the per-cell override in `_render_row` existed, so the section now shows what the tool does, with the transcript, and states that what is open is the stakeholder's acceptance rather than the behaviour. "What it does" said the markers are honoured *"in every column without exception"*, quoting [src: WI-0002/Q-001]'s *"no exceptions"*; a cell holding a `br` tag is exactly the exception the stakeholder asked for afterwards, so the paragraph now carries it [src: WI-0004 AC1; src: ADR-0010]. Sent back by review-close on D7 and D12 |
| 8 | 2026-08-29T07:36:43Z | answer-questions | WI-0004 | "Open at the time of writing" said the three things the stakeholder meant by their sign-off condition were *"not settled and are `refine`'s to put to them"*. They were put to them and answered on 2026-08-29 [src: WI-0004/Q-001; WI-0004/Q-002; WI-0004/Q-003], so the sentence had become false in the one place a reader looks to find what is open. It is replaced by the four answers in the stakeholder's own words, with the criteria that carry them. The behaviour is still not built and this section still says so; [src: WI-0004] is now at `ready` rather than `draft` |
| 7 | 2026-08-29T07:18:00Z | answer-questions | EP-001 | The stakeholder was asked to accept the engagement a second time and **did not** [src: EP-001/Q-005]. "Accepted as delivered" opened by asserting an acceptance that no longer describes the engagement, so it now carries the correction ahead of the acceptance it records, and keeps that record because what they accepted about the four items and the five caveats still stands. "Open at the time of writing" said nothing was open; it now states the one behaviour they asked for in their own words, shows what the tool does today instead, names [src: WI-0004] as where it is filed, and records the three gaps they dismissed so no execution files work for one of them |
| 6 | 2026-08-28T22:29:41Z | answer-questions | EP-001 | The stakeholder accepted the engagement at sign-off and declined all five surfaced caveats as work [src: EP-001/Q-004]. A new "Accepted as delivered" section records the acceptance, what they checked before giving it, and each decline with the reason they gave, so that no later execution files work for one of them believing it an unexplored gap. "Open at the time of writing" said nothing was unanswered while the sign-off was open; it now names the sign-off and records it answered |
| 5 | 2026-08-28T22:05:00Z | implement | WI-0003 | WI-0003's code landed and this document still described the tool without it. "A table whose rows disagree … about how far they are indented comes back exactly as it went in" was false for the space-only case, so the sentence is qualified and a paragraph added stating where the line now falls, in the stakeholder's own words [src: ADR-0008; src: WI-0003 AC5; src: WI-0003 AC6; src: WI-0003/Q-001]. "Open at the time of writing" still carried the indentation question as one that might need asking; it was asked as [src: WI-0003/Q-001] and answered against its own premise, so the section now records the answer. Two citations moved from the superseded ADR-0003 to ADR-0008. Sent back by review-close on D7 and D12 |
| 4 | 2026-08-28T20:19:15Z | answer-questions | WI-0002 | Recorded the stakeholder's answers to WI-0002/Q-001 and Q-002: the alignment marker is honoured in every column with no exceptions, a centred cell's odd spare column goes on the right, and the leading whitespace that produces in a bare table's first column is accepted — with the fault it exposes filed as [src: WI-0003] rather than worked around. No stakeholder question is open. |
| 3 | 2026-08-28T18:43:43Z | answer-questions | WI-0001 | Recorded the stakeholder's answers to WI-0001/Q-001..Q-003: bare-pipe and indented tables are tables and are aligned, punctuation is never changed, and a table mdtab does not fully understand is left exactly as it was [src: ADR-0003]. Only WI-0002's centring question is still open. |
| 2 | 2026-08-28T18:30:21Z | answer-questions | EP-001 | Recorded the stakeholder's answers to Q-001..Q-003: Python 3 with no install step, GFM pipe tables only with code fences left alone, and alignment measured by display width. Replaced the three open unknowns with the two that remain for `refine`. |
| 1 | 2026-08-28T18:25:18Z | intake | EP-001 | First version |

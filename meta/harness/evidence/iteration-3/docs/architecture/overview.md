---
title: Architecture overview — mdtab
version: 9
status: current
updated: 2026-08-29T07:51:28Z
updated-by: implement
updated-for: WI-0004
---

# Architecture overview — mdtab

## The shape of the thing

mdtab is one process with one job: bytes in on stdin, bytes out on stdout, with the spacing
inside recognised tables rewritten and everything else copied. There is no configuration, no
state between runs, no file access and no network. That is the whole system, and it is small
enough that the interesting decisions are about *where a rule lives* rather than about
components talking to each other.

The pipeline has four stages, in order, each of which hands the next a simpler problem:

```
stdin (bytes)
  │  decode UTF-8/surrogateescape, split terminators        [ADR-0004]
  ▼
lines: [(content, terminator)]
  │  track fenced code blocks, group runs of pipe lines     [WI-0001 AC7, AC8]
  ▼
runs: [(start, end)] + everything else, untouched
  │  parse and test the four recognition rules              [ADR-0008]
  ▼
tables (recognised) and runs (left alone)
  │  measure display width, pad, reassemble                 [ADR-0002]
  ▼
stdout (bytes)
```

The load-bearing property is that stage 3 can say *no*. A run that fails any recognition rule is
not repaired and not partly laid out; its lines go to the output exactly as they arrived. Every
construct mdtab does not model — a malformed table, a mixed-punctuation table, an irregularly
indented one, and anything nobody has thought of — arrives at that one branch [src: ADR-0008].

## Modules

| module | holds | why it is separate |
|--------|-------|--------------------|
| `mdtab/__main__.py` | stdin/stdout wiring, exit code | so every other module is a pure function of text and can be tested without a process |
| `mdtab/textio.py` | decode, split into `(content, terminator)`, reassemble, encode | the only place an encoding or a line ending is mentioned [src: ADR-0004] |
| `mdtab/width.py` | `display_width(text)` | one function, so every layout decision inherits the rule and a change to it is a change in one place [src: ADR-0002] |
| `mdtab/scan.py` | fenced-code-block state, prefix extraction, grouping lines into runs | separates *finding candidates* from *judging them*, so the judging code never re-scans |
| `mdtab/table.py` | cell splitting, the delimiter-row test, the four recognition rules, layout | the recognition rules and the layout that depends on them are one concern: both are defined over a parsed run |
| `mdtab/inline.py` | whether a cell's text contains a line break, and the code spans that hide one | the only inline markdown grammar the tool reads, kept out of `table.py` so the recognition rules cannot come to depend on it [src: ADR-0010] |
| `mdtab/filter.py` | the top-level `format_document(text) -> text` | the seam the tests drive, so no test needs a subprocess |

`format_document` is the function every test calls, and `__main__` does nothing but decode, call
it, and encode — which is why the process boundary needs no test of its own beyond AC1
[src: tracker/items/WI-0001/artifacts/plan.md; src: WI-0001 AC1].

## Rules that live in exactly one place

These are the sentences a future change is most likely to duplicate rather than call, and each
is named here so that a reviewer can check it has not been copied:

- **How wide a character is** — `mdtab/width.py`. Nothing else may use `len()` to mean a width
  [src: ADR-0002].
- **What a line is** — `mdtab/textio.py`. Nothing else may call `str.splitlines`, which would
  discard the distinction between `\n` and `\r\n` that AC9 depends on [src: ADR-0004;
  src: WI-0001 AC9].
- **Where a cell boundary is** — `mdtab/table.py`, one function, used by the cell-count rule, the
  outer-pipe test and the layout alike, so the three cannot disagree [src: WI-0001 AC10].
- **What a run's indent is** — `mdtab/scan.py`, one function taking the whole run and returning
  the prefix its lines share, or nothing when they do not share one. It is a property of a run,
  not of a line: `line_prefix` in the same module answers the per-line question and is not a
  substitute for it, because spaces past the shared prefix belong to the first cell rather than
  to the indent [src: ADR-0008; src: WI-0003 AC1].
- **Whether a run is a table** — `mdtab/table.py`, one predicate returning a laid-out run or
  nothing [src: ADR-0008].
- **Where a cell's content sits in its field** — `mdtab/table.py`, one function reading the
  delimiter row's markers into one alignment value per column, and one renderer distributing the
  spare space around the content: all after it, all before it, or split with the odd column on
  the right. A cell may decline the value its column offers, and exactly one thing makes it do
  so: a line break in its own text, which places it as a left-aligned cell whatever the marker
  says. That override is decided at the same place the renderer is called and is per cell, so it
  moves no other cell of the column, and the delimiter row never reaches it
  [src: ADR-0010; src: WI-0004 AC1; src: WI-0004 AC3].
  The guard spaces are outside the field and do not move, and a column's width does
  not depend on the *alignment* its marker declares [src: ADR-0007; src: WI-0002 AC6]. The
  marker's colons are a separate question, and the bullet below answers it rather than this one:
  a column is never narrower than its delimiter cell can be written, and how wide that cell must
  be counts the `:` it carries. So a column whose content leaves it at that minimum can come out
  wider under one marker than under another — the middle column of `a | | b` is 2 columns wide
  under `---` and 3 under `:-:` [src: WI-0001 AC12; src: WI-0001/Q-005].
- **Whether a cell's text contains a line break** — `mdtab/inline.py`, one function, and the only
  place this project reads markdown's *inline* grammar. It answers one question of one cell's
  text: does it hold an HTML `br` tag that is not inside a code span. Nothing on the recognition
  path may call it — whether a run is a table is decided without it, and a `br` tag cannot occur
  in a delimiter cell anyway [src: ADR-0010; src: WI-0004 AC7].
- **How wide a column is** — `mdtab/table.py`, one function, and it carries two rules that are
  forced by idempotence rather than chosen. The maximum is taken over the header and body rows
  only, never over the delimiter row's own cell, or the column would grow on every run; and a
  column is never narrower than its delimiter cell can be written, which is one `-` plus one
  character for each `:` the input had, plus whichever surrounding spaces the row's outer-pipe
  style drops. Anything that later wants to change a column's width — honouring the alignment
  markers, for one — must go through this function and keep both rules, because AC6 is what
  they exist for [src: WI-0001 AC12; src: WI-0001 AC6; src: WI-0001/Q-005].

## A property the tool lost and got back

Until WI-0001, every document mdtab produced was a document mdtab recognised, so running it twice
was the same as running it once in a stronger sense than byte equality: the second run recognised
the same tables and laid them out to the same bytes. Honouring the alignment markers cost half of
that, between WI-0002 and WI-0003. A table written without a leading `|` whose first column's marker is `---:`
or `:---:` comes back with leading spaces on its header and body rows and none on its delimiter
row, and the byte-identical prefix rule saw a run whose lines disagreed and declined it
[src: WI-0002 AC10]. The bytes were still stable — the second run reproduced them, so idempotence
held [src: WI-0001 AC6] — but the table was not tidied again, and the tool said nothing, because it
says nothing about anything [src: EP-001].

That was a deliberate trade the stakeholder made with the alternatives in front of them
[src: WI-0002/Q-002], and WI-0003 undid it. [src: ADR-0008] replaced the byte-identical prefix rule
with a shared-prefix one: a run is recognised when its lines' indents share a longest common prefix
and every line's remainder past it is spaces, and the spaces past it belong to the first cell rather
than to the indent [src: mdtab/scan.py]. mdtab therefore recognises the bare right-aligned table its
own layout emits, and running it twice is once again the same as running it once in the stronger
sense [src: WI-0003 AC2; src: WI-0003 AC4].

The change was not free, and the cost is recorded here as well as in the ADR: a table written
without outer bars whose rows carry different numbers of leading spaces is now laid out where it
used to be left alone, and comes back at the prefix its lines share — for a run at the left margin,
the start of the line. The stakeholder was shown that document and chose it [src: WI-0003/Q-001;
src: WI-0003 AC5]. A run whose lines differ by a **tab** or by a `>` is still not a table and is
still copied through untouched, which is the other half of the same answer [src: WI-0003 AC6].

## What is deliberately absent

No markdown parser. mdtab does not build a document tree and does not know what a list item is;
its idea of structure is textual, which is why an indented table is recognised by a shared
literal prefix rather than by block nesting [src: WI-0001 AC15; src: ADR-0008]. This is a limit, recorded here
so the next person does not read the prefix rule as an approximation of something better that was
almost implemented.

Two inline constructs are the exception, and they are an exception to the sentence above rather
than the start of a parser: a `br` tag, and the code span one may hide inside. The tool learns
them because a cell that reads as two lines must be placed differently from one that does not,
and for no other purpose — the answer reaches one branch of the renderer and nothing else
[src: ADR-0010; src: WI-0004 AC1]. Its code-span rule is deliberately smaller than markdown's:
backtick runs must match in length, and nothing else about a span is modelled
[src: ADR-0010].

No configuration, no flags, no output other than the document. The tool is not a linter and says
nothing about what it declined to touch [src: EP-001].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 9 | 2026-08-29T07:51:28Z | implement | WI-0004 | The code landed, so the four sentences v8 added saying it had not — in the modules table, in two one-place-per-rule bullets and in the "What is deliberately absent" paragraph — were false and are gone. `mdtab/inline.py` exists and `_render_row` calls it; nothing else about v8's description changed, which is step 7 of the plan doing what it was written for [src: tracker/items/WI-0004/artifacts/plan.md; src: WI-0004 AC1; src: ADR-0010] |
| 8 | 2026-08-29T07:41:58Z | plan | WI-0004 | Recorded the design for WI-0004 before it lands: a cell whose own text holds a line break declines its column's marker and is placed left, decided per cell at the renderer's call site; and `mdtab/inline.py`, a new module holding the only inline markdown grammar the tool reads — the `br` tag and the code span that may hide one. Added the module row, the "Whether a cell's text contains a line break" bullet, the override clause in "Where a cell's content sits in its field", and the paragraph qualifying "No markdown parser". Every one of them says the code has not landed yet, and `implement` puts them into the present tense when it has [src: ADR-0010; src: WI-0004 AC1; src: WI-0004 AC3; src: WI-0004 AC7] |
| 7 | 2026-08-28T22:58:00Z | implement | BUG-0001 | Corrected v6's own replacement clause, which restated the minimum-width rule as an increment and was false in both directions. It read *"they reach the width through the minimum a delimiter cell must have, so a column too narrow to hold its own marker comes out one column wider for each `:` the marker carries"*; an interior column with one colon is not widened at all (`---`, `--:`, `:--` all give 2 where `:-:` gives 3), and the first column of a bare table is widened by a single colon, because the minimum counts the guard space the missing pipe drops. The bullet now defers the arithmetic to "How wide a column is", which owns it, and keeps only the concrete pair a reader needs to predict the two commands [src: WI-0001 AC12; src: WI-0001/Q-005; src: BUG-0001 AC1] |
| 6 | 2026-08-28T22:52:00Z | implement | BUG-0001 | Corrected a false absolute in the "Where a cell's content sits in its field" bullet. It read *"The guard spaces are outside the field and do not move, and no column's width depends on its marker [src: ADR-0007; src: WI-0002 AC6]"*; the cited criterion says *alignment*, and a column too narrow to hold its own marker is widened by the minimum-width rule the next bullet states, so `:-:` gives a 3-column field where `---` gives 2. The bullet now distinguishes the two and points at the next bullet for what a width does depend on [src: WI-0001 AC12; src: WI-0001/Q-005; src: BUG-0001] |
| 5 | 2026-08-28T22:05:00Z | implement | WI-0003 | The code landed, so the document had to stop describing the tool as it was before it. Rewrote "A property the tool lost and **is getting back**" as "**got back**", in the past tense and against the merged behaviour, including the cost the stakeholder accepted and the tab-and-`>` half of their answer that the section never stated [src: ADR-0008; src: WI-0003 AC2; src: WI-0003 AC5; src: WI-0003 AC6]; moved the pipeline diagram's and the copy-through paragraph's citations from the superseded ADR-0003 to ADR-0008. Sent back by review-close on D7 and D12 |
| 4 | 2026-08-28T21:23:07Z | plan | WI-0003 | Added "What a run's indent is" to the one-place-per-rule list, since indentation becomes a property of a run rather than of a line [src: ADR-0008]; rewrote the lost-property section to record that ADR-0008 restores it, what the restoration costs, and that the code has not landed yet |
| 3 | 2026-08-28T20:31:00Z | plan | WI-0002 | Added "Where a cell's content sits in its field" to the one-place-per-rule list, and a section recording the property honouring the markers costs: mdtab may emit a bare table it will not recognise until WI-0003 lands [src: ADR-0007] |
| 2 | 2026-08-28T19:59:23Z | answer-questions | WI-0001 | Added "How wide a column is" to the one-place-per-rule list, with the two rules AC6 forces, so WI-0002 inherits them when it starts honouring the alignment markers (WI-0001/Q-005) |
| 1 | 2026-08-28T18:53:01Z | plan | WI-0001 | First version, written while planning the first item |

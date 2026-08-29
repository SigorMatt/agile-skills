---
status: recorded
---

# Refinement Q&A — WI-0001

`status: recorded`. Round 1's three questions were put to the stakeholder, answered, and their
answers are below verbatim; round 2 re-checked the Definition of Ready against the criteria the
answers produced and asked nothing further. The exchange below is what was actually said.

The stakeholder is asynchronous: they answered in the question files between sessions rather
than in a conversation, so the wording under each `[answered]` marker is theirs, copied from
`questions/Q-00n.md`, and nothing here is a paraphrase. Entries marked `[assumed]` are decisions
`refine` took on a recorded basis; the stakeholder has not seen them and may overturn any of
them cheaply.

## Round 1 — the Definition of Ready agenda

Working through `spec/dor-dod.md` §1 against the item as `intake` and `answer-questions` left
it, these are the criteria that did not pass and what each needed.

| DoR | Verdict before this round | What it needed |
|-----|---------------------------|----------------|
| R1 | pass | frontmatter complete; `type`, `epic`, `priority` all set |
| R2 | pass | the story names the role, the capability and the outcome |
| R3 | pass | eight labelled checkbox criteria existed |
| R4 | **fail** | AC7 stated a definition rather than an observation; nothing said what happens to line endings, escaped pipes, cell content, or what a laid-out cell actually looks like |
| R5 | pass, extended | two exclusions existed; two more were added that a reader could reasonably assume were included |
| R6 | **fail** | three blocking questions are now open — this is why the item is suspended rather than Ready |
| R7 | pass | `depends-on` is empty; nothing blocks it |
| R8 | **fail** | no `refinement-qa.md` existed; this file is it, and it is an agenda until the answers arrive |
| R9 | pass | one coherent change: read stdin, lay out the tables it recognises, write stdout |
| R10 | **fail** | a table inside a blockquote or a list item had no stated behaviour; now asked as `Q-003`, with the rest of the combinations enumerated in the item's `## Notes` |

## Questions to the stakeholder — answered

Filed as `WI-0001/Q-001`, `Q-002` and `Q-003`, in one round, framed as one conversation. Each
carries its own context, at least three options and a recommendation. They are reproduced here
in short so this file is a complete record of the round; the question files are authoritative.

**Q1 — What should the tool do with a malformed table, whose rows do not all have the same
number of cells?** Options: pad every row out to the widest (A), keep the header's cell count
and leave extra cells hanging past the last pipe (B), or leave a malformed table byte-for-byte
untouched (C). Recommended A.

> `[answered]` — **C**, in the stakeholder's words: *"Leave it alone. A table with a row that
> doesn't match is a table I got wrong, and I want to see it still looking wrong so I go and fix
> it — not have the tool invent a third column or leave bits hanging off the end of a line. The
> tool's job is to tidy tables it understands, and if it doesn't understand one it should keep
> its hands off."* The recommendation (A) was overruled. Propagated as AC13 and as ADR-0003
> rule 3.

**Q2 — Is a pipe table written without outer `|` characters a table, and if so does the output
keep that style or gain outer pipes?** Options: recognise and preserve each table's own style
(A), recognise and normalise everything to outer pipes (B), or only treat the outer-pipe form as
a table (C). Recommended A.

> `[answered]` — **A**, in the stakeholder's words: *"Yes, that's still a table and it should
> line up. But whichever way I wrote it is the way it stays — if I didn't put the outer bars in,
> don't add them for me. I only want the spacing changed, never the punctuation."* Propagated as
> AC14 and as ADR-0003 rule 4.

**Q3 — Should a table indented inside a blockquote or a list item be laid out?** Options: handle
blockquotes and list indents including irregular cases (A), handle a uniform prefix only (B), or
only lay out tables starting at column one (C). Recommended B.

> `[answered]` — **B, with A's intent**, in the stakeholder's words: *"Align them. I put tables
> under bullet points all the time and quote them in notes, and a table that's indented is still
> a table — it would be odd if those were the ones that stayed ragged. If a table is indented in
> some tangled way you can't make sense of, that's one you leave alone, same as any other table
> you don't understand."* Propagated as AC15 and as ADR-0003 rule 2: a prefix every line shares
> is stripped and restored, and anything irregular is left byte-for-byte.

## What the answers settled beyond the three questions

The three answers were taken together and recorded as one policy in ADR-0003, because two of the
sentences generalise past the question that produced them. One case that was never asked is
settled there rather than by a fourth question: a run whose rows disagree about their outer-pipe
style is left byte-for-byte, on the basis of *"same as any other table you don't understand"*
(Q3) plus AC2's requirement that the pipes line up. That is a decision by `answer-questions`
(architect), not something the stakeholder said, and it is reversible additively — see ADR-0003
§Consequences.

## Decisions taken without asking, and what each rests on

Each of these was a candidate question and was not asked. `refine`'s routing rule is that a
question goes to the stakeholder only if it carries product stake that no record already
settles; the rest are decided here or routed to `plan`. Every one below is marked `[assumed]`,
which means the stakeholder has not seen it and may overturn it — they are all cheap to change.

**Line endings and the end of the document (AC9).** A document written with `\r\n` line endings,
or one whose last line has no trailing newline, comes back exactly as it went in.

> `[assumed]` — not asked, because the epic already requires that every line outside a table is
> byte-for-byte unchanged and that a table-free document is reproduced byte-for-byte. A tool
> that silently rewrote line endings would breach both, so this is the epic's answer restated
> where `verify` can check it, not a new decision.

**An escaped pipe is not a separator (AC10).** `| a \| b | c |` is two cells, and the first
keeps the text `a \| b`.

> `[assumed]` — not asked. The epic's success measure "feeding the tool's own output back to a
> markdown renderer produces the same rendered table" forces it: splitting on an escaped pipe
> would add a column that the renderer does not show, changing what the document says. The
> answer would be the same for any stakeholder, which is what makes it ours to take.

**Cell content is unchanged apart from the spaces around it (AC11).** Stripped of leading and
trailing spaces, every output cell is byte-identical to the input cell.

> `[assumed]` — not asked. It is the epic's "changes spacing, not content" boundary made
> checkable per cell rather than per document, which is what `verify` needs in order to catch a
> tool that quietly trims, escapes or rewraps something inside a cell.

**What a laid-out cell looks like (AC12).** One space after the `|`, the content, padding, one
space before the next `|`; the delimiter row filled with `-` to the same width, keeping its `:`
markers.

> `[assumed]` — not asked, and this is the assumption most worth the stakeholder's eye, because
> it is the only one that decides what their documents *look* like rather than what is preserved
> in them. It is not asked because it is the near-universal convention for laid-out pipe tables
> — it is what GitHub's own tables look like and what every markdown formatter emits — and
> because it is a constant in one place, so overturning it costs a line of code and a test
> update. If the stakeholder wants tighter or looser padding, they can say so on any of the
> three open questions and it will be honoured.

**The tool emits nothing on stderr, ever, including on a table it does not understand.**

> `[assumed]` — not asked. The epic puts "validating or reporting on the markdown" out of scope
> and says the tool is not a linter, so a diagnostic would contradict a decision already
> recorded. Written into `## Out of scope` so that a later reader does not add one as an
> obvious kindness.

## Round 2 — the Definition of Ready re-check, no questions asked

Round 1's answers added AC13, AC14 and AC15 and amended AC2, AC7 and AC12, so R4 and R10 had to
be re-walked against the item as it now stands rather than as it stood when the round opened.
The verdicts are in the journal entry for this execution, criterion by criterion. Five gaps
turned up, and **none** of them was put to the stakeholder.

The routing test in `refine`'s procedure step 3 disposed of all five the same way: each would
have the same answer whoever the stakeholder was, and each is covered by their standing deferral
on how the tool is built — *"The rest of how it's built is your call, not mine"* (`EP-001/Q-001`).
Filing a fourth round on mechanics after they had answered three rounds of product questions is
the failure that step 3 names (F-023), so they were decided here and written into the criteria.

**What a *run* is (AC7).** A maximal sequence of two or more consecutive lines, none inside a
fenced code block, each containing at least one unescaped `|`; it ends at the first line that
does not, or at the end of the document.

> `[assumed]` — not asked. AC7 already said "a run of consecutive lines containing `|`" and left
> the boundaries to the reader. Making them explicit changes no behaviour anyone asked for; it
> makes AC13, AC14 and AC15 decidable, because all three are conditions *on a run*, and a
> verifier cannot test them without knowing where a run starts and stops.

**When a code fence opens and closes, and what an unclosed one does (AC8).** A fence is three or
more backticks or tildes after the AC15 prefix is stripped; it closes on at least as many of the
same character and nothing else; an unclosed fence runs to the end of the document.

> `[assumed]` — not asked. The stakeholder settled the principle at `EP-001/Q-002`: a table
> inside a code fence "is text somebody typed on purpose" and is left alone. What was missing was
> the mechanics, and every part of the rule above is what a markdown renderer does, which the
> epic's success measure — feeding the tool's output back to a renderer produces the same
> rendered document — already binds the tool to. Stripping the prefix first is the same
> treatment tables get under AC15, so a fence inside a blockquote protects its contents exactly
> as an unindented one does.

**A line's terminator is not part of the line (AC9).** It is removed before the line is examined
and restored afterwards.

> `[assumed]` — not asked, and it fixes a real hole rather than tidying one. Without it, a
> document with `\r\n` endings would carry a `\r` into the last cell of every row: `\r` is not a
> space, so AC11's strip would not remove it, and AC14's "last non-whitespace character is an
> unescaped `|`" test would fail on every row of a CRLF document. AC9 already promised the
> endings come back unchanged; this says where they live in the meantime.

**What "escaped" means for a `|` (AC10).** A `|` is escaped exactly when an odd number of `\`
characters immediately precedes it.

> `[assumed]` — not asked. AC10 said `\|` is not a separator without saying what `\\|` is. The
> odd-count rule is what a renderer applies, so it follows from the same success measure as AC8,
> and the alternative — treating any preceding backslash as escaping — would make the tool
> disagree with the renderer on a row nobody would think to test.

**A prefix change disqualifies a run rather than splitting it (AC15).** The run's extent comes
from AC7 first; then the prefixes are compared.

> `[assumed]` — not asked. This was genuinely ambiguous as AC15 was written: a three-line run
> whose third line is indented could be read as a two-line table plus a stray line, or as one
> disqualified run. Disqualifying is the reading that matches ADR-0003's whole point — one
> branch, one behaviour, for anything the tool does not fully understand — and it is the
> conservative one, because the other reading would have the tool rewrite lines around a
> construct it had already decided it could not parse.

## Routed to `plan` rather than to anyone

These were not asked because the answer would be the same whoever the stakeholder was. They are
in the item's `## Notes` for `plan` to settle under its own preference order.

- What the entry point is called and how it is invoked — ADR-0001 delegates this explicitly, and
  AC1 defers to whatever `plan` records in `plan.md`.
- Whether the document is streamed or read whole — no criterion can tell the two apart.
- Which test framework is used, and therefore what `commands.test` becomes.

---
status: recorded
---

# Refinement Q&A — WI-0001

Round 1 was asked as four question artifacts, presented as one conversation, and answered by the
stakeholder between turns. What follows is what was asked and what came back, verbatim. The
question files hold the full context and options each one carried; only the question and the
answer are reproduced here.

## Round 1 — asked and answered

### `Q-001` — non-ASCII cell width

**Asked:** When a table cell contains characters that are not plain ASCII, what should the tool
make equal across the rows of a column — the number of characters, or the number of columns the
text occupies on a terminal? *(Options: A count characters; B count terminal columns; C count
characters and record the limitation. The team's recommendation, given last, was A or C.)*

**[human]** *"It has to line up on the screen — that is the entire reason I want this tool, so
make the columns equal in what I see, not in some count I never look at. I write English almost
all the time, but names with accents turn up and I paste an emoji into a status column more often
than I would like to admit, and those are exactly the tables that come out crooked today. If a
rare emoji is off by one in some terminal I will live with it."*

They chose **B**, against the team's recommendation. Recorded as ADR-0003 decision 7 and observed
by AC1 and AC2.

### `Q-002` — tables that do not start at the left margin

**Asked:** Should the tool tidy a table that does not start at the left margin — one indented
under a list item, or one inside a blockquote — or leave any such table alone? *(Options: A left
margin only; B allow a uniform indent; C allow any uniform line prefix including `>`. The team's
recommendation, given last, was A unless they write tables in lists.)*

**[human]** *"Tables under a numbered list are all over my notes — that is half of what I write,
so yes, tidy those. Quoted ones I have never written and do not expect to, so do not spend
anything on them. Whatever the indent was, put it back exactly as it was."*

They chose **B**, against the team's recommendation, and declined C explicitly. Recorded as
ADR-0003 decisions 2 and 11, observed by AC5, with blockquoted tables in `## Out of scope`.

### `Q-003` — the space inside each cell's pipes

**Asked:** How much space should the tool put between a cell's pipes and its text — one space on
each side, or none? *(Options: A one space each side; B none; C preserve whatever the input used.
The team's recommendation, given last, was A.)*

**[human]** *"One space each side, always. The cramped version is unreadable and it is the
readability I am paying for; a couple of extra characters per column costs me nothing. I do not
care how big the first diff is — one big tidy-up and then everything is consistent forever."*

They chose **A**. Recorded as ADR-0003 decision 9 and observed by AC3.

### `Q-004` — the delimiter row

**Asked:** In the output, should the delimiter row's dashes fill the whole column from pipe to
pipe, or should they be padded like an ordinary cell? *(Options: A dashes fill the column; B
dashes padded like a cell; C preserve whichever the input used. The team's recommendation, given
last, was A.)*

**[human]** *"Dashes all the way across, pipe to pipe. That row is a rule under the header, not a
row of content, and it should look like one — the padding rule I just gave you is about cells
with my words in them."*

They chose **A**, and reconciled it with `Q-003` themselves in the same sentence. Recorded as
ADR-0003 decision 10 and observed by AC4.

## Cross-answer check

Every answer above was checked against the stakeholder's prior recorded answers when
`answer-questions` consumed it, and each check is written in the question file itself:
`Q-001` against `EP-001/Q-001` and `WI-0001/Q-004`; `Q-002` against `EP-001/Q-003` and
`EP-001/Q-001`; `Q-003` against `EP-001/Q-001` and `WI-0001/Q-004`; `Q-004` against
`EP-001/Q-001` and `WI-0001/Q-003`. Every verdict was `compatible`, so nothing was put back to
the stakeholder, and no answer of theirs was edited to fit another.

This refinement raised no new answer of its own, so it adds no check beyond those. The one place
where two of their sentences could have been read as disagreeing — *"columns are as wide as the
widest cell in them"* [src: EP-001/Q-001] against *"that row is a rule under the header, not a row
of content"* [src: WI-0001/Q-004] — was resolved as a clarification rather than a conflict, and
ADR-0002's contrary reading was preserved unedited in a superseded document rather than rewritten.

## Settled without asking

These were on the agenda and came off it. `refine` does not re-ask a question the record answers,
and does not send a technical call to the stakeholder.

- **[assumed]** What the tool runs as — answered at `EP-001/Q-002`, recorded in ADR-0001. Their
  standing deferral, *"I have opinions about languages but they are not worth much here, so take
  that decision yourselves"*, covers the whole category, so where the script lives and what
  command runs the tests is `plan`'s to fix, not a question.
- **[human]** Which table syntaxes count, what happens to a malformed table, and what happens to
  a fenced code block — answered at `EP-001/Q-001` and `EP-001/Q-003`, recorded in ADR-0003
  decisions 1, 3, 4 and 5, observed by AC7 and AC8.
- **[assumed]** Line endings, and a file whose last line has no newline. Follows from *"anything
  that is not a table comes out exactly as it went in, byte for byte"* [src: EP-001/Q-001]: a
  copied line keeps its own ending, a composed line takes the ending of the line it replaces.
  Observed by AC6.
- **[assumed]** Empty input, and the exit code. A filter given nothing writes nothing and exits
  0; nothing in the record suggests a non-zero exit for a document the tool declined to touch.
  Observed by AC6 and AC10.
- **[assumed]** Input containing bytes that are not valid UTF-8 round-trips byte for byte. This
  is the same promise as any other passthrough applied to a case they did not name, and it is an
  assumption rather than their instruction because they never mentioned encodings. Observed by
  AC6; how it is done is `plan`'s.
- **[assumed]** Escaped pipes (`\|`) inside a cell — routed to `plan`, not to the stakeholder.
  They asked for GitHub-flavoured pipe tables [src: EP-001/Q-003], where `\|` is content rather
  than a cell boundary, so the answer does not depend on who the stakeholder is.
- **[assumed]** A tab inside a cell counts as one column under ADR-0003 decision 7. A consequence
  of a decision already taken, not a new one.
- The tool has no options, flags or modes, so DoR R10's combination check has nothing to
  enumerate. Recorded in the item's `## Notes` rather than left to be noticed.

## Round 2

None was needed and none was invented. After round 1 every Definition of Ready criterion is met
from the record, and no remaining gap on this item is one whose answer would change what the
software is for. Each gap that was left is named in `## Notes` with the skill that owns it.

## Override

None. No Definition of Ready criterion was waived; all ten are met, and the journal entry for
this execution records each one with its evidence.

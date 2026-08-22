# Refinement Q&A — WI-0004

The exchange that refined this item, in order. The stakeholder answered in files between sessions;
their words are copied here verbatim. This item is the one that is **not** Ready, and the file says
exactly where the line falls.

Tags: `[human]` — the stakeholder said this. `[assumed]` — `refine` proposed it and the stakeholder
deferred, or it follows from a decision they delegated. `[unresolved]` — asked and not settled.

---

## Q1 (Q-001, filed by `intake`) — What does your bank's CSV look like, and how should a row become an expense?

Two questions in one, and it came back half answered.

**Answer [human]:** "I'll send you a sample later, don't have it to hand right now. As for how it
turns into an expense — let me say who paid and who was in on it when I import, same idea as adding
one by hand."

The second half is settled and is AC6: the payer and the sharers come from the command line, and
omitting `--shared-by` shares among everyone registered, exactly as `add-expense` does. The first
half — the format — was not answered.

---

## Q2 (Q-002, filed by `refine`) — Can you paste the header line and two or three representative rows?

**Answer [human]:** "I'll send you a sample later, still haven't got to it. And no — the import
stays part of this, it doesn't get dropped or pushed to a later epic. Build it last if that's
easiest, but I'm not signing off on a version without it."

Still no sample. The scope half is a clear answer and was propagated: WI-0004 is not dropped, and
EP-001 cannot close without it (`tracker/items/EP-001/item.md` `## Scope`).

---

## Q3 (Q-003, filed by `refine`) — If you import the same CSV file twice, what should the tool do?

Options offered: A, import it again; B, refuse a file already imported; C, warn and require
confirmation. Recommendation: C.

**Answer [human]:** "I don't want it silently doubling up — warn me if I'm importing the same file
again and make me confirm if I really mean it."

Option C, and it is AC7. The exact message and the `--again` flag were fixed by this refinement.

---

## Q4 (Q-004, filed by this refinement) — the sample, a third time

Asked again because AC1, AC2 and AC5 cannot be made decidable without it, and because inventing a
format would produce an importer for a file that does not exist. The question showed the stakeholder
what is already working, listed what refinement settled without them, and offered a one-row version
if pasting three was the friction.

**Answer [human]:** "I'll send you a sample later — still haven't got to it. I'd rather you wait for
my actual file than guess at the format."

Still `[unresolved]` as a *fact* — the format is not known and AC1, AC2 and AC5 remain undecidable.
But the second sentence settles something the first three askings did not:

- **[human] Guessing is refused.** Option B — naming the bank and working from its published export
  format — was offered and declined. Waiting is now the stakeholder's own instruction, not
  `refine`'s judgement, and no plausible-looking layout may be substituted for the real one.
- **[human] Option C is still open.** "My actual file" is satisfied by the header line and one real
  row. They objected to guessing, not to pasting less, so the next asking should request that
  minimum rather than three rows that have now failed to arrive three times.
- The scope decision from Q-002 is untouched and is not re-asked: the import stays in, and EP-001
  does not close without it.

---

## Q5 (Q-005, filed by the fourth refinement) — the sample, standing request

**Answer [human]** — *"I'll send you a sample later — still haven't got to it. I'd rather you wait
for my actual file than guess."*

Still `[unresolved]` as a *fact*: five askings, five deferrals, and the format is not known, so AC1,
AC2 and AC5 remain undecidable. Two things about the answer are new, and both are the stakeholder's
own words rather than `refine`'s reading of them:

- **[human] The instruction to wait is confirmed, not merely said once.** Q-004 said "wait for my
  actual file than guess **at the format**"; this answer drops the qualifier — "wait for my actual
  file than guess". It is the second consecutive answer to choose waiting over any substitute, so it
  is now a standing instruction covering *any* route that ends in a layout the stakeholder did not
  supply, not only a guessed column list.
- **[human] Reducing the ask did not help.** Q-005 asked for the header line and a *single* row, the
  smallest thing that satisfies "my actual file", and offered the file's path as an alternative
  requiring nothing to be typed. The answer is the same as to the three larger askings. The obstacle
  is therefore not the size of the ask, and a sixth identical asking has no reason to succeed where
  five did not.

What is *not* re-asked, because it is decided: the import stays in scope (Q-002), and the payer and
sharers come from the command line (Q-001).

The consequence carried into the item is an instruction to the next refinement: keep the standing
request, but stop repeating it unchanged — offer the stakeholder a route out of the wait that does
not guess anything. Guessing is forbidden; asking *them* to state their file's shape at import time
is not guessing, and it has never been put to them.

---

## Q6 (Q-006, filed by the fifth refinement) — a way out of the wait that guesses nothing

**Answer [human]:** "Let's do C — build it against the columns I name now, and I'll still send the
sample when I get to it so you can add the shortcut for my bank later. Typing four options each
time is fine."

**This is the answer that made the item refinable.** Six askings in, the thing that moved was not
asking harder but asking something else. What it settles:

- **[human] The import is built against columns the stakeholder names on the command line.**
  `--date-column`, `--amount-column`, `--description-column` and `--date-format`, required on every
  import (AC10). AC1, AC2 and AC5 are rewritten against them and are decidable now.
- **[human] Not a config file.** *"Typing four options each time is fine"* chooses option C over
  option D. No remembered mapping, no `bank.ini`; that is now out of scope rather than open.
- **[human] The sample is still coming, and no longer blocks anything.** When it arrives it buys a
  named shortcut for those four options — a **new item**, not a change to WI-0004. Nobody should
  ask for it again.
- **[assumed] A row that is not a positive charge is skipped and reported by line number**, exactly
  as any other unusable row (AC4). The question named this as the one point option C left open and
  proposed this handling; the stakeholder did not overturn it, so it stands as an assumption they
  may correct — not as something they said.

Not a sixth asking of the same thing. The standing request for the sample is preserved as option A
and is still available, but the question put this time is one the stakeholder has never been asked:
whether the tool should take the file's shape **from them at import time** — named date, amount and
description columns plus a date format — so that AC1, AC2 and AC5 become decidable without anyone
knowing their bank's layout in advance.

Why this is not the guessing they forbade: under that route the tool contains no assumption about
any bank. The column names come from the stakeholder, about the file in front of them, at the moment
they run the import, and AC5 becomes "refuse a file whose header does not contain the columns you
named" — a check against something stated rather than an invention checked against itself.

Why it is a question and not a decision `refine` could take: it trades typing at every import for
having the feature now, and only the stakeholder can say whether that trade is worth making.
`spec/question.md` §4.1 — intent no document records.

Four options were offered: A keep waiting, B state the shape on the command line, C both (B now, a
named shortcut for their bank when the sample arrives), D B with the mapping in a small config file.
The recommendation was C and C is what they chose. The two decisions they had already made — the
import is not dropped (Q-002), the payer and sharers come from the command line (Q-001) — were not
reopened by the question and were not disturbed by the answer.

---

## Q7 — nothing was asked this time, and why that is the right call

**No question [refine, sixth execution].** This pass asked the stakeholder nothing. That is a
decision, so it is recorded here rather than left as an absence.

Six questions have been put to them on this item and all six are answered. The only one that was
ever blocking — what their bank's CSV looks like — stopped being a dependency when they chose option
C in Q-006. What was left was the ordinary refinement job: pin the wording, close the combinations,
and record the assumptions. Every gap this pass found was of that kind — the exact text of a
skipped-row message, which name a refusal reports when two are wrong, whether a BOM is stripped —
and none of them is a fact about what the stakeholder wants that no document records. Asking would
have spent a seventh round trip on decisions the conventions they already delegated (WI-0001/Q-004,
ADR-0002, ADR-0005) settle by themselves.

Two things were deliberately **not** asked, and both would have been mistakes:

- **The sample.** It is no longer blocking, and they have said they will send it. A seventh asking
  would be for a shortcut nobody is waiting on.
- **The refund case.** Q-006 proposed skipping any row that is not a positive charge and they did
  not overturn it. It is recorded as `[assumed]` below and flagged inside AC4 itself, which is what
  the assumption tag is for. Re-asking would be re-litigating an answer.

---

## Decided at this refinement, all `[assumed]`

`refine` fixed the wording and the combinations that had to be pinned before `plan` could design
against them and `verify` could judge them. Each rests on ADR-0002 and ADR-0005, written under the
stakeholder's delegation on WI-0001/Q-004, or on criteria WI-0001 to WI-0003 already fixed.

- **[assumed] Successful output is `Imported <rendered>`, one line per accepted row, in file order,
  and nothing else on stdout.** Matches `add-expense`'s `Added <rendered>`. No summary line.
- **[assumed] A skipped row prints `Skipped line <N>: <raw line>` on stderr**, the header being line
  1. Previously "reported, naming the row", which nobody could check.
- **[assumed] What makes a row unusable is exhaustive and reuses WI-0002's rules** — a bad amount, a
  date that does not parse, a blank description, or too few cells. Nothing new was invented, which
  is why an imported expense cannot differ from a typed one.
- **[assumed] A `--date-format` no row parses under skips every row and exits 0**, falling out of
  AC4 rather than being a rule of its own.
- **[assumed] A refusal names the first offender in a stated order** — payer then sharers (AC6),
  date then amount then description (AC5) — so two runs report the same thing.
- **[assumed] An import that records nothing is not remembered**, so it can be retried without
  `--again` (AC5).
- **[assumed] `--again` on a never-imported file is an ordinary import**, not an error (AC7).
- **[assumed] The column mapping is not part of a file's identity** for duplicate detection (AC7).
- **[assumed] RFC 4180 parsing, cells trimmed, leading UTF-8 BOM ignored** (AC11). Properties of
  real CSV files rather than of any bank; the BOM in particular would otherwise produce "column not
  found" on a file that visibly contains the column.
- **[assumed] A file that is not valid UTF-8 is refused, not repaired** (AC8).
- **[assumed] Atomicity is checked by inspection** — no module this item adds writes the data file
  directly — rather than by racing the process (AC9).
- **[assumed] A row that is not a positive charge is skipped, not treated as a refund** (AC4).
  Proposed in Q-006 option B, not overturned by the stakeholder; theirs to correct.

## Decided at earlier refinements

Everything that does not depend on the bank's format. Each rests on ADR-0002 and ADR-0005, written
under the stakeholder's delegation on WI-0001/Q-004.

- **[assumed] `./expenses import-csv <FILE>`**, with the file positional and `--paid-by`,
  `--shared-by`, `--again`, `--data-file` as options.
- **[assumed] A skipped row exits 0; a rejected file exits 1.** A partial import is not a refusal —
  most of the file was imported — so the command succeeded and reports what it skipped. ADR-0005's
  consequences flagged this as the case needing a decision; this is it.
- **[assumed] A skipped row is named by line number and quoted**, so it can be found in the file.
- **[assumed] AC7's message names the date of the earlier import and the flag that overrides it.**
- **[assumed] There is no `--date` option**, and it is out of scope: every imported expense takes
  its row's date, and an override would discard what WI-0002/Q-002 exists to preserve.
- **[assumed] AC8 (a missing or unreadable file) and AC9 (refusals change nothing; the write is
  atomic) were added.** Neither was stated anywhere, and the first is what anyone hits first.

## Left unconstrained

- **[unresolved] `argparse`'s usage-error wording** — exit code 2 is fixed, the text is not.
- **[unresolved] How many skipped rows are reported**, for a file where every row is unusable.
- **[unresolved] What the store remembers about a past import beyond its fingerprint and date.**
- **[unresolved] A header line containing the same column name twice** — which of the two is read.
- **[unresolved] How stdout and stderr interleave** when one import both records and skips rows.
- **[unresolved] Whether the file is read once or twice** — fingerprint and parse, one pass or two.

All six are carried into the item's `## Notes` under "Left deliberately unconstrained (R10)", each
with why it is safe to leave. No acceptance criterion depends on any of them, which is the test
applied before leaving one.

## Override

None, and none was sought — and none is needed any more. For five askings this section recorded
that the item was **not** Ready because AC1, AC2 and AC5 failed R4 for want of the sample, and that
an override must not be sought, because the only thing an override could buy was an importer built
against an invented format. That reasoning held and was never breached: no format was invented, and
the wait ended by the stakeholder's decision (Q-006) rather than by anyone deciding the rule was
inconvenient. AC1, AC2 and AC5 are now decidable on their own terms, so the Definition of Ready can
be met rather than waived. Whether it *is* met is the next refinement pass's judgement, not this
file's claim.

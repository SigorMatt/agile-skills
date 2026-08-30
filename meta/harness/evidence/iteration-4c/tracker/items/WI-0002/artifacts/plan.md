# Plan — WI-0002 Review the cards due today and reschedule them on the fixed ladder

## Problem

The person has a deck and a command that adds to it [src: WI-0001]. What they do not have is the
reason the deck exists: a daily sitting that shows them the cards they are about to forget, asks
whether they got each one right, and moves each card along the ladder. This item delivers one
more subcommand — `python3 -m recall review` — that offers every due card oldest first, reveals
the back on request, takes `y` or `n`, writes the new rung and due date before moving on, and can
be stopped at any card without losing what was already answered.

Every rule it applies is already decided. Grading is binary and the ladder is 1, 3, 7, 30 days
[src: ADR-0002]. A card is due when its date is today or earlier, and a missed day is neither
punished nor forgiven [src: ADR-0002]. A session offers every due card, states how many before it
starts, and can be quit cleanly [src: ADR-0003]. `rung` is an integer 0 to 4 in a file the tool
owns and rewrites whole [src: ADR-0007] [src: ADR-0008]. What the person types was settled by
`refine` and is in the criteria: Enter reveals, `y` and `n` grade, `q` stops
[src: WI-0002 AC1] [src: WI-0002 AC4] [src: WI-0002 AC11].

What is left to design is where the rule goes, how the loop reads input it can trust, and when
the file is written. The last of those is the one the item turns on: AC9 requires the answers
already given to survive the tool being killed at a prompt [src: WI-0002 AC9].

## Approach

A third module joins the two WI-0001 built, exactly where `docs/architecture/overview.md` said
one would [src: ADR-0009].

**`recall/schedule.py` owns the ladder.** Pure functions over cards and a date: no file, no
environment, no printing, and no call to the clock — the day is passed in [src: ADR-0009]. That
is what makes ten rung transitions checkable without ten sessions. Its interface:

- `INTERVALS: dict[int, int]` — the rung-to-days map `{1: 1, 2: 3, 3: 7, 4: 30}`, which is
  `ADR-0002`'s ladder written down once [src: ADR-0002].
- `is_due(card: store.Card, today: datetime.date) -> bool` — `card.due <= today`
  [src: WI-0002 AC2].
- `due_positions(cards: list[store.Card], today: datetime.date) -> list[int]` — the **positions**
  in `cards` of the due ones, ordered by due date ascending with ties left in card-file order
  [src: WI-0002 AC12]. Positions rather than cards, because two cards may legitimately share a
  front side [src: WI-0001 AC6] and a session must write back the one it actually asked about.
- `after_right(card: store.Card, today: datetime.date) -> store.Card` — rung one higher, capped
  at 4, due `INTERVALS[new rung]` days after `today` [src: WI-0002 AC5].
- `after_wrong(card: store.Card, today: datetime.date) -> store.Card` — rung 1, due one day after
  `today` [src: WI-0002 AC6].

**`recall/cli.py` gains the session**, and keeps its existing job: prompts, streams, exit codes.

- `_parser()` gains a `review` subparser taking no arguments [src: WI-0002 AC1].
- `main()` **dispatches on the parsed subcommand** instead of calling `add()` unconditionally.
  That line is the trap WI-0001's review recorded for this item
  [src: tracker/items/WI-0001/artifacts/review.md]; left as it is, `review` would run `add`.
- `_ask(prompt: str, accepted: tuple[str, ...]) -> str | None` — prints the prompt, reads one
  line, strips it and lowercases it, and returns it when it is one of `accepted`. On anything
  else it says what it accepts and asks the same question again, reprinting the whole prompt it
  was given — so a re-ask at the reveal prompt shows the card's front again and a re-ask at the
  outcome prompt shows its back again, and the person is never asked to answer a card whose text
  has scrolled past [src: WI-0002 AC13]. On end of input it returns `None`, which every caller
  treats as `q` [src: WI-0002 AC11].
- `review() -> int` — the session, in the order the criteria fix: load, select, refuse or
  announce, then for each due position reveal, grade, write, move on.

**The loop's shape**, which is the part AC4 and AC9 constrain: the session holds the whole card
list in memory, and after each answer it replaces that one position and calls `store.save()` on
the whole list. The file is therefore correct after every answer, not at the end
[src: WI-0002 AC4] [src: WI-0002 AC9]. `store.save()` already writes through a temporary file and
a rename, so a kill during the write leaves the previous file intact rather than a torn one
[src: ADR-0008].

Exit codes follow WI-0001's: `0` for a session that finished or was stopped, including the
nothing-due case [src: WI-0002 AC8] [src: WI-0002 AC11]; `1` for a card file that cannot be read
[src: WI-0002 AC14]; `2` from `argparse` for a command line that is wrong, which this item leaves
unconstrained [src: WI-0002]. The session's own text goes to standard output; refusals go to
standard error [src: docs/architecture/overview.md].

## Steps

1. **Create `recall/schedule.py` with the ladder.** Add `INTERVALS`, `is_due`, `after_right` and
   `after_wrong` exactly as specified under Approach. It imports `datetime` and
   `recall.store` and nothing else [src: ADR-0009]. Afterwards, a card at each of rungs 0 to 4
   answered right returns rungs 1, 2, 3, 4, 4 with due dates 1, 3, 7, 30, 30 days after the date
   passed in, and answered wrong returns rung 1 due one day after it, from every rung.

2. **Add the selection to `recall/schedule.py`.** `due_positions(cards, today)` returns the
   positions of the cards whose `due` is on or before `today`, sorted by `due` ascending with
   `sorted()`'s stability leaving equal dates in their file order [src: WI-0002 AC12].
   Afterwards, a list holding a card due yesterday, one due today and one due tomorrow returns
   the positions of the first two, oldest first, and a list of three cards sharing one due date
   returns `[0, 1, 2]`.

3. **Add `_ask()` to `recall/cli.py`.** The prompt is printed to standard output; the line is
   read with `input()`, stripped and lowercased before matching; an unaccepted line prints what
   is accepted and then reprints the whole prompt, card text included, rather than a bare
   re-ask; `EOFError` returns `None`
   [src: WI-0002 AC11] [src: WI-0002 AC13]. Afterwards, driving the tool with a pipe whose input
   runs out ends the prompt rather than raising, and a stray key re-asks.

4. **Add the `review` subparser and dispatch in `main()`.** `_parser()` registers `review` with
   no arguments; `main()` chooses between `add` and `review` on the parsed subcommand name
   [src: WI-0002 AC1]. Afterwards, `python3 -m recall review` reaches `review()`,
   `python3 -m recall add one two` still reaches `add()` and every WI-0001 criterion still holds,
   and `python3 -m recall review extra` exits `2` with a usage message.

5. **Implement `review()` in `recall/cli.py`, in the order the criteria fix.** Load the card file
   through `store.load()`, letting `CardFileError` reach `main()`'s existing handler so the
   session stops before any card is shown [src: WI-0002 AC14]. Take `today` once, at the start,
   with `datetime.date.today()`. Call `due_positions()`. If it is empty, print that nothing is
   due, return `0`, and call nothing that writes [src: WI-0002 AC8]. Otherwise print the count
   [src: WI-0002 AC10], then for each position in order: `_ask` for Enter or `q` with the card's
   front as the prompt; `_ask` for `y`, `n` or `q` with its back as the prompt — so that a re-ask
   at either point shows the card again; on `q` or end of input print that the
   session stopped and return `0` without writing that card [src: WI-0002 AC11]; otherwise
   replace `cards[position]` with `after_right()` or `after_wrong()` and `store.save()` the whole
   list before the next card is printed [src: WI-0002 AC4]. Afterwards, each of AC1 to AC14
   behaves as its criterion says.

6. **Write `tests/test_review.py`.** Every test seeds a card file in a fresh
   `tempfile.TemporaryDirectory` by writing the documented format directly [src: ADR-0007],
   points `RECALL_CARD_FILE` at it, and drives `python3 -m recall review` as a subprocess with
   `input=` supplying the keystrokes [src: ADR-0008]. Dates are computed in the test relative to
   `datetime.date.today()` so that no test depends on the calendar. The cases are one per
   criterion, in the mapping table below; each asserts on the exit code, on standard output and
   standard error, and on the bytes of the card file afterwards.

7. **Write `tests/test_schedule.py`.** The ten rung transitions of AC5 and AC6 as direct calls,
   and `due_positions()` over the boundary cases of AC2 and AC12 — a card due yesterday, today
   and tomorrow, and three cards sharing a date. These are supporting evidence for criteria whose
   own demonstration is at the command line; they are not what settles them.

8. **Run the project's gates and write the implementation report.**
   `python3 -m unittest discover -s tests -t . -q` and `python3 -m compileall -q recall tests`
   both exit zero [src: ADR-0006], WI-0001's 26 tests among them, and
   `tracker/items/WI-0002/artifacts/impl-report.md` records which test demonstrates which
   criterion. The criteria's checkboxes are `verify`'s to tick, not this item's implementation's
   [src: .claude/agile-skills/spec/work-item.md].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `review` starts a session; the front is shown and the back only after Enter | 4, 5 | `test_the_back_is_hidden_until_enter`: one due card, input `""` then `q`; standard output before the Enter is asserted **not** to contain the back side, and after it to contain it |
| AC2 — every card due today or earlier is offered, none other, no cap | 2, 5 | `test_only_and_all_due_cards_are_offered`: a seeded file of five cards — two overdue, one due today, two due later — answered through; standard output contains the three due fronts and neither of the other two, and the count line says `3` |
| AC3 — an overdue card is offered on the same terms, unpenalised, counted from the review day | 2, 5 | `test_an_overdue_card_is_unpenalised`: a card at rung 2 due 10 days ago; the file read after the session started and before the answer shows `rung: 2` unchanged, and answering right writes rung 3 due 7 days after **today**, not 7 days after its old due date |
| AC4 — `y` and `n`, and the answer is in the file before the next card | 5 | `test_each_answer_is_written_before_the_next_card`: two due cards; input answers the first and then `q`. The file afterwards holds the first card rescheduled and the second untouched — the write cannot have waited for the end of the session. Also `test_only_y_and_n_are_outcomes`, which is AC13's case at the outcome prompt |
| AC5 — right moves up one rung, 1/3/7/30, top rung stays | 1, 5 | `test_answering_right_walks_the_ladder` in `tests/test_schedule.py`: rungs 0 to 4 answered right give rungs 1, 2, 3, 4, 4 and dates today+1, +3, +7, +30, +30; and `test_right_at_the_command_line` in `tests/test_review.py`, which drives one card of each rung through a real session and reads the file |
| AC6 — wrong returns to rung 1, due tomorrow, from any rung | 1, 5 | `test_answering_wrong_returns_to_the_first_rung` in `tests/test_schedule.py`: rungs 0 to 4 answered wrong all give rung 1 and today+1; and `test_wrong_at_the_command_line`, which reads the file after a real session |
| AC7 — the updates survive stopping and starting; a second session the same day offers only what is still due | 5 | `test_a_second_session_the_same_day_offers_only_what_is_still_due`: three due cards, the first two answered, then a second subprocess run — its count line says `1` and it offers the third front only |
| AC8 — nothing due, no cards, or no card file: say so, exit 0, write nothing | 5 | `test_nothing_due_says_so_and_writes_nothing`, parametrised over three seeds — a file whose cards are all due tomorrow, a file with no cards, and no file at all. Each: exit 0, a message on standard output, and the file byte-identical afterwards or still absent |
| AC9 — quitting keeps every answer already given, including on a kill | 5 | `test_quitting_keeps_the_answers_already_given`: three due cards, the first answered then `q` — the file holds one rescheduled and two untouched; and `test_a_kill_at_a_prompt_keeps_the_answers_already_given`, which sends `SIGKILL` to the subprocess while it waits at a prompt and then reads the file |
| AC10 — the count is stated before the first card and matches the file | 5 | `test_the_count_is_stated_before_the_first_card`: standard output's first line names the number of due cards, and the number equals the count of `due:` lines at or before today in the seeded file, computed independently in the test |
| AC11 — `q` at either prompt, and end of input, stop cleanly | 3, 5 | `test_q_stops_at_either_prompt` (input `q`, and input `""` then `q`) and `test_end_of_input_stops_the_session` (input `""` alone, so the stream runs out at the outcome prompt): each exits 0, prints nothing on standard error, and leaves the card on screen unchanged in the file |
| AC12 — oldest due first, ties in file order, predictable from the file | 2, 5 | `test_due_cards_are_offered_oldest_first` in `tests/test_review.py`: four cards due 3 days ago, 1 day ago, today and today (the last two in a known file order) are offered in exactly that sequence in standard output; and `test_the_order_is_the_same_twice`, which runs the session, restores the seeded file byte for byte, runs it again and compares the sequence of fronts |
| AC13 — unrecognised input re-asks the same card and counts as nothing | 3, 5 | `test_an_unrecognised_key_re_asks_the_same_card`: input `x`, `""`, `z`, `y` against one due card — standard output asks about that card's front twice before the back is shown, says what it accepts, and the card ends up answered right exactly once |
| AC14 — an unparsable card file stops the session before the first card | 5 | `test_an_unparsable_card_file_stops_the_session`: a hand-mangled file (`bakc:` for `back:`); exit non-zero, the message on standard error names the file and the line, no front side appears on standard output, and the file is byte-identical afterwards |

## Assumptions

Each is settled under the stakeholder's standing delegation — *"As for how it's actually built —
whatever you think is best"* [src: EP-001/Q-004] — and each is reversible in the sense this skill
requires: one file, no data migration, nothing published outside the package.

1. **Input is read a line at a time, so `y` is `y` followed by Enter.** `input()` is what the
   standard library offers without touching the terminal's mode, and `refine` recorded raw
   single-key input as rejected — it cannot be driven by a pipe, which would leave AC9 and AC11
   untestable [src: tracker/items/WI-0002/artifacts/refinement-qa.md]. No criterion says a
   keystroke takes effect without Enter [src: WI-0002 AC4]. Reversing this is `_ask()`'s body
   plus a dependency on the terminal being a terminal.
2. **Input is stripped of surrounding whitespace and matched without regard to case**, so `Y `
   is `y`. Nothing states it, and refusing a capital letter would be a surprise nobody asked for.
   Reversing it is one line in `_ask()`.
3. **The session takes `today` once, at the start.** A sitting that crosses midnight schedules
   every card from the date the session began. Nothing in the record mentions midnight, and
   taking the date per card would make two cards answered a minute apart land on different
   ladders. Reversing it is where one call moves.
4. **The wording of every prompt and message is `implement`'s**, within what the criteria require
   them to contain: the count [src: WI-0002 AC10], what each prompt accepts
   [src: WI-0002 AC11] [src: WI-0002 AC13], and that nothing is due [src: WI-0002 AC8]. Reversing
   any of them is a string.
5. **The session does not re-read the card file after it starts.** If something else rewrites the
   file mid-session, the session's in-memory list wins at the next save. The tool owns the file
   [src: ADR-0004] and is single-user [src: ADR-0001]; no criterion covers the case. Reversing it
   means a reload before each save, and a decision about what to do when the card being answered
   has moved.

## Decisions and ADRs

| decision | where it is recorded | how it was reached |
|----------|---------------------|--------------------|
| The ladder rule lives in its own module of pure functions, given the date by its caller | `ADR-0009` | decided here; the overview named WI-0002 as the item that would decide it |
| `due_positions()` returns positions rather than cards | this plan, `## Approach` | forced by WI-0001's duplicate fronts [src: WI-0001 AC6]: a session must write back the card it asked about |
| Every answer is saved immediately, by rewriting the whole file | this plan, `## Approach` | answered by the criteria [src: WI-0002 AC4] [src: WI-0002 AC9]; the mechanism is `ADR-0008`'s existing write |
| Binary grading, the 1/3/7/30 ladder, the top rung, the due comparison | `ADR-0002` | already decided; this item implements it |
| `rung` 0 to 4 and the file's format | `ADR-0007` | already decided; unchanged by this item |
| Enter, `y`, `n`, `q`, end of input, and the re-ask | `WI-0002`'s criteria and `refinement-qa.md` | already decided by `refine` under the same delegation |
| Line-based input, case and whitespace, the single `today`, prompt wording, no mid-session reload | this plan, `## Assumptions` | reversible assumptions under the standing delegation [src: EP-001/Q-004] |

Nothing on this item was put to the stakeholder. Every decision above is either answered by a
document, fixed by a criterion `refine` wrote from their own words, or inside the delegation they
stated [src: EP-001/Q-004]. No decision here is irreversible: the expensive commitment in this
product is the card file's format, and this item adds no field to it [src: ADR-0007].

## Scaffolding

None. `recall/` and `tests/` are packages already, both gate commands run today, and this plan
creates no file outside `tracker/` and `docs/`.

## Risks

- **`input()` means the person presses Enter after `y`.** If the stakeholder pictured a single
  keypress, this will feel wrong on the first day of use, and the fix is a wording change to AC4
  and a decision to depend on the terminal's mode — not a defect report. It is named here so the
  judgement is made deliberately, as WI-0001 named AC2's restart before any code existed
  [src: tracker/items/WI-0001/artifacts/plan.md].
- **AC9's kill case needs a real kill.** A test that sends `SIGKILL` to a subprocess waiting at a
  prompt is the only honest demonstration; if the environment makes that unreliable, `verify`
  will be looking at a substituted evidence question of the same shape as WI-0001's AC2
  [src: WI-0001 AC2]. The mitigation is that AC4's own test already proves the write happens
  before the next card, which is the property a kill would expose.
- **One rewrite and two fsyncs per answer** [src: ADR-0008]. A session of 200 due cards writes the
  whole file 200 times. At one person's vocabulary deck this is not observable, and no criterion
  bounds a session's duration — deliberately, because the stakeholder traded that bound for the
  honest count [src: EP-001/Q-005]. It is named because it is the one cost in this item that grows
  with both the deck and the session.
- **A session spanning midnight** schedules from the day it started, per assumption 3. Nothing in
  the record mentions it, and the alternative is worse.
- **Three modules for a tool this small** may be one seam too many; `ADR-0009` says what evidence
  would show that, and that folding it back is cheap.

## Out of scope for this item

- Adding a card [src: WI-0001] and deleting one [src: WI-0003].
- Undoing an answer, re-reviewing a card inside the same session, and editing a card's sides
  during a review — all three are in the item's `## Out of scope` [src: WI-0002].
- Any bound on how long a session takes or how many cards it offers [src: ADR-0003].
- Any change to the card file's format: no field is added, and `ADR-0007` stands untouched
  [src: ADR-0007].
- Statistics, streaks, or a history of outcomes beyond the rung and the due date
  [src: ADR-0002].
- Reminding the person that a review is due [src: WI-0002].

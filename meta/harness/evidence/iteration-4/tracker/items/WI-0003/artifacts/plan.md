# Plan — WI-0003 Schedule the next review with simple spaced repetition

## Problem

`recall review` already walks the due cards and records right or wrong on each, but it decides
nothing about when a card comes back: it writes the day after the review for both answers, a
placeholder `ADR-0006` declared and named as one [src: ADR-0006; recall.py]. This item replaces
that with the ladder — 1, 3, 7, 30 days, up one rung for a right answer, back to the bottom for a
wrong one, and a card that has never been answered starting below the bottom rung so its first
right answer schedules it one day out [src: ADR-0001; WI-0003/Q-001].

For the person using it, that is the whole point of the tool: review time goes to the cards they
have not learned [src: WI-0003]. Three constraints shape how it is built. The store is a file a
person opens, and from this item on, hand-editing it is the documented and only way to move a card
[src: WI-0003; WI-0001 AC5]. A scheduling value the tool cannot read must stop it rather than be
ignored, which is the defect WI-0002 handed forward [src: WI-0003 AC9]. And a store written before
this item must keep working and be upgraded in place [src: WI-0003 AC8].

## Approach

One new field, one new constant, one rewritten function, and a tightening of `load`.

A card gains `interval`: the number of days its current wait is, one of `1`, `3`, `7`, `30`, and
`null` for a card that has never been answered — the same idiom `result` already uses for the same
idea. The store goes to version 3, read alongside 1 and 2. `ADR-0007` records why the interval in
days rather than a rung index, and what that costs.

Recording a result becomes arithmetic on that field: a right answer takes the next ladder value
after the current one (`null` takes the first, `30` stays at `30`), a wrong answer takes the first,
and the new `due` is **the review day** plus the new interval — never the card's old `due` plus
anything, so a card reviewed ten days late still gets its full interval from the day it was
actually reviewed [src: WI-0003 AC2].

`load` gains two checks it did not have: `due` must be exactly `YYYY-MM-DD`, and `interval` must
be a ladder value or `null`. Both failures are unreadable stores, which is the existing path —
message on stderr naming the file, exit 1, file untouched [src: ADR-0004; WI-0003 AC9]. It also
gains a normalisation pass, so a card read from an older document reads as never answered and the
next write carries the field on every card [src: WI-0003 AC8].

The interfaces this fixes, for the developer to implement:

- `LADDER: tuple[int, ...]` — module-level, `(1, 3, 7, 30)` [src: ADR-0001].
- `next_interval(current: int | None, right: bool) -> int` — the move, as a pure function of the
  card's current interval and the answer. Pure so it can be tested without a store or a session.
- `record_result(card: dict, right: bool, when: str) -> None` — keeps its signature; its body now
  sets `interval` from `next_interval` and `due` from `when` plus that interval.
- `load(path: str) -> dict` — keeps its signature and its `StoreError` contract; validates the two
  scheduling fields and normalises `interval` and `result` onto every card it returns.

Nothing else moves. The session, its keys, its output and its report are untouched — the item
excludes any change to what a review prints [src: WI-0003]. No new command is added, and no flag
[src: WI-0003].

## Steps

1. **`recall.py` — the ladder and the version.** Add `LADDER = (1, 3, 7, 30)` beside the existing
   constants, with a comment citing ADR-0001. Change `STORE_VERSION` from `2` to `3` and
   `READABLE_VERSIONS` from `(1, 2)` to `(1, 2, 3)`, and update the two comments above them to say
   what version 3 adds. Afterwards, a store written by `recall add` says `"version": 3`, and a
   document claiming `4` is refused as one claiming `3` used to be.

2. **`recall.py` — `next_interval(current, right)`.** A new pure function next to
   `record_result`. `right` false, or `current` is `None`, gives `LADDER[0]`; otherwise the value
   after `current` in `LADDER`, or `current` when it is already the last. It may assume `current`
   is `None` or a member of `LADDER`, because step 3 makes `load` guarantee that. Afterwards,
   `next_interval(None, True) == 1`, `next_interval(1, True) == 3`, `next_interval(7, True) == 30`,
   `next_interval(30, True) == 30`, and `next_interval(anything, False) == 1`.

3. **`recall.py` — `load` validates the two scheduling fields.** In the per-card loop, replace the
   `due` string check with one that also requires the exact `YYYY-MM-DD` shape — parse with
   `datetime.datetime.strptime(value, "%Y-%m-%d")`, which rejects `"tomorrow"` and `"20260829"`
   alike, where `date.fromisoformat` would accept the second. Add a check that `interval`, when
   present, is `None` or a member of `LADDER`. Both raise `_unreadable(path, ...)` with a message
   naming the card and the field, in the style of the checks already there. Afterwards, a store
   with `due: "tomorrow"` or `interval: 5` makes `recall list`, `recall review` and `recall add`
   each print a message on stderr naming the file and exit 1, leaving the file untouched — because
   every command routes `StoreError` to that one path already [src: recall.py].

4. **`recall.py` — `load` normalises what it returns.** After validation, for every card:
   `card.setdefault("interval", None)` and `card.setdefault("result", None)`. Do **not** touch
   `due`: its absence already means "due", which `due_cards` relies on and documents
   [src: recall.py]. Afterwards, a version-1 or version-2 card read from disk carries
   `interval: None` in memory, so it behaves as never answered, and the next `save` writes the
   field on every card in the document.

5. **`recall.py` — `add_card` writes the field.** Add `"interval": None` to the dict it appends,
   next to `"result": None`. Afterwards, a freshly added card has `due` today, `result` null and
   `interval` null.

6. **`recall.py` — `record_result` uses the ladder.** Replace its body: set `card["result"]` as
   now; set `card["interval"] = next_interval(card.get("interval"), right)`; set `card["due"]` to
   `datetime.date.fromisoformat(when) + datetime.timedelta(days=card["interval"])`. Rewrite its
   docstring — it currently describes the placeholder and cites WI-0003 as what will replace it.
   Afterwards, a right answer on a card at 3 days leaves it at `interval: 7` and due 7 days after
   the review, and a wrong answer on any card leaves it at `interval: 1` and due the day after.

7. **`README.md` — the ladder, under `### recall review`.** Add a short section: the four
   intervals in order, that a right answer moves a card to the next one and a wrong answer back to
   one day, that a card you have never answered comes back the day after you first get it right,
   and that the wait is counted from the day you review, so reviewing late costs nothing.
   Afterwards, a reader can state a card's next due date from its stored fields and this section
   alone [src: WI-0003 AC4].

8. **`README.md` — the card-field table and the version paragraph.** Add an `interval` row: what
   it is, the four values it may hold, `null` for a card never answered, and that editing it by
   hand is how you put a card on a rung. Update the paragraph below the table: this `recall` reads
   versions 1, 2 and 3 and writes 3, and a version-2 card has no `interval` and reads as never
   answered. Update the sample JSON block above the table to show `"version": 3` and an
   `"interval"` on the card. Extend the "cannot be read as a card store" sentence to say that a
   `due` which is not a `YYYY-MM-DD` date, and an `interval` which is not one of the four values,
   are both cases of that. Afterwards, `README.md` names every field this item writes and the
   values each may hold.

9. **`tests/test_schedule.py` — new file, the item's criteria.** Use `tests.support.CommandTestCase`
   as every other suite does, driving `recall` as a subprocess with `RECALL_FILE` pointed at a
   scratch store, hand-editing the store between runs, and reading it back. One test per criterion
   or per case within one: AC1, AC2 rung by rung including the top rung staying put and the
   overdue card, AC3 from each rung plus the follow-up right answer, AC5 across two processes, AC6
   from `recall add` through two right answers, AC7 for `q` and for input running out, AC8 for a
   store with `due` and `result` but no `interval`, and AC9 for `due: "tomorrow"` and for an
   `interval` the README does not list, over all three commands with a `cmp`-equivalent byte
   comparison. Afterwards, `python3 -m unittest discover -s tests -t .` covers every criterion.

10. **`tests/test_session_parts.py` — `next_interval` in-process.** Add cases calling
    `next_interval` directly for the five moves step 2 names. This suite already imports
    `recall.py` and tests its parts in-process [src: tests/test_session_parts.py]. Afterwards, the
    ladder's arithmetic is checked without a store or a session.

11. **`tests/test_store.py` — the two assertions this item invalidates.** In
    `test_a_version_1_store_is_read_and_upgraded_by_the_next_write`, the write now stamps `3`, not
    `2`, and the upgraded cards now carry `interval` [src: tests/test_store.py:87]. In
    `test_a_store_from_a_newer_version_is_refused_and_left_untouched`, the "newer" version must
    become `4`, because `3` is now readable [src: tests/test_store.py:92]. Update both, and their
    docstrings, to cite ADR-0007 alongside ADR-0006. Afterwards, the store suite describes version
    3. **Do not weaken either test** — both keep asserting the same behaviour about a different
    number.

12. **`tests/test_docs.py` — the README claim this item adds.** Extend
    `test_the_readme_names_the_fields_a_review_writes_and_what_they_mean`, or add a sibling, to
    assert `README.md` contains `` `interval` `` and the four interval values. Afterwards, AC4's
    documentation requirement has a test behind it, as WI-0001's and WI-0002's do.

13. **Run the gates and reconcile the whole suite.** `python3 -m unittest discover -s tests -t .`
    and `python3 -m compileall -q -x '[.]claude' .` [src: tracker/project.yaml]. Any other test
    that fails is a test asserting the placeholder; fix it to assert the ladder, and say so in the
    implementation report. Afterwards, both commands exit 0.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — a new card is due the day it is added | 5 | `test_schedule.py`: `recall add` into an empty store, then `due` equals today and `recall review` presents the card. Regression over WI-0001/WI-0002 behaviour; `add_card` already sets `due` [src: recall.py] |
| AC2 — a right answer moves up one rung, 30 stays, measured from the review day | 1, 2, 6 | `test_schedule.py`: four cases, each hand-editing a card to a rung with `due` today, `printf '\ny\n' \| recall review`, then reading back `due` and `interval` — 3, 7, 30, 30 days after today; plus a fifth with `due` ten days past, which must give 7 days after **today**. `test_session_parts.py` checks `next_interval` directly |
| AC3 — a wrong answer returns to the bottom rung from any rung | 2, 6 | `test_schedule.py`: from each of the four rungs, `printf '\nn\n' \| recall review` leaves `interval: 1` and `due` tomorrow; then `due` reset to today and answered right gives 3 days after today |
| AC4 — the ladder is written down in `README.md` | 7, 8 | `test_docs.py` asserts the field name and the four values are present; the verifier reads the new section and the `interval` row and works a due date out by hand |
| AC5 — scheduling state survives ending and restarting | 4, 6 | `test_schedule.py`: after a session that moves a card up, a second process (`recall list`, and a `recall review` after hand-editing `due`) sees the same `interval` and `due`, and the file on disk holds them. Every command is a separate subprocess in this suite [src: tests/support.py] |
| AC6 — a never-answered card's first right answer schedules it one day out | 2, 5, 6 | `test_schedule.py`: `recall add` into an empty store, `printf '\ny\n' \| recall review` → `due` tomorrow and `interval: 1`; `due` reset to today and answered right again → 3 days after today |
| AC7 — a card the session never reached keeps its rung and due date | 6 | `test_schedule.py`: two due cards, `printf '\ny\nq\n' \| recall review` and `printf '\ny\n\n' \| recall review`; the second card's `interval` and `due` are byte-identical to before. `record_result` is called per card and only for cards answered [src: recall.py] |
| AC8 — an older store is read and upgraded in place | 1, 4 | `test_schedule.py`: a hand-written version-2 store with `due` and `result` but no `interval` — `recall list` and `recall review` exit 0, the cards behave as never answered, and the file after the next review carries `interval` on every card. `test_store.py` covers the version-1 case |
| AC9 — an unreadable scheduling value stops the tool | 3 | `test_schedule.py`: a store with `due: "tomorrow"`, and one with `interval: 5`; for each, `recall list`, `recall review` and `recall add "a" "b"` exit 1 with a message on stderr naming the file, and the file's bytes are unchanged |

## Assumptions

- **`datetime.datetime.strptime(value, "%Y-%m-%d")` is the right strictness for AC9's `due`
  check.** AC9 names `"tomorrow"` as the value to refuse; `strptime` refuses that and also refuses
  `"20260829"` and `"2026-08-29T00:00"`, which `date.fromisoformat` accepts on Python 3.11 and
  later. Reversing it is one expression in `load` and a test; nothing is stored differently, so
  there is no migration.
- **`interval` is normalised on read rather than by a migration pass.** `load` fills the field in
  on the cards it returns, and the next `save` persists it, which is exactly how version 2 arrived
  [src: ADR-0006]. Reversing it — a one-shot upgrade at start-up — is one function and no stored
  data changes.
- **The `interval` row belongs in `README.md`'s existing card-field table** rather than in a new
  section of its own. AC4 asks only that the field and its values be named where the other fields
  are [src: WI-0003 AC4]. Reversing it is a documentation edit.
- **The ladder's arithmetic goes in `recall.py` beside `record_result`, not in a new module.** The
  overview's answer to "when does the store leave this file" was "when something other than a
  command needs it", and nothing here does [src: docs/architecture/overview.md]. Reversing it is a
  move and an import.

## Decisions and ADRs

| decision | where | route |
|----------|-------|-------|
| The field is `interval`, in days, `null` for never answered — not a rung index | `ADR-0007` §Decision | decided; the item routed the representation to `plan` [src: WI-0003] |
| Store version 3, read 1, 2 and 3 | `ADR-0007` §Decision | decided, on ADR-0004's stated principle that one version means one shape [src: ADR-0004] |
| `load` validates `due` strictly and `interval` against the ladder | `ADR-0007` §Decision | forced by AC9; the ADR records the cost — a store an older `recall` read can now be refused |
| The ladder is one constant in `recall.py`, not in the store | `ADR-0007` §Decision | decided; a store-side table would deliver per-user tuning, which the item excludes [src: WI-0003] |
| The new `due` is measured from the review day | `ADR-0007` §Decision | documented — `ADR-0001` already words both moves from the review, and AC2 now states it [src: ADR-0001; WI-0003 AC2] |
| `ADR-0001`'s reversibility note, which assumed an index | `ADR-0001` v3 | amended, not superseded: the ladder is unchanged; a consequence claim about stored cards became false and was corrected [src: ADR-0001] |
| Never-answered is `null`, not an absent key, on cards the tool writes | `ADR-0007` §Decision | documented — `result` already uses `null` for the same idea [src: ADR-0006] |
| `README.md` and `docs/architecture/overview.md` updated | overview v3 | required by D7 and D12; the overview said `review` writes a placeholder, which stops being true at step 6 |

## Scaffolding

`none`. Both declared commands already run in this project — `tests/` exists with an
`__init__.py` and seven suites, and `compileall` needs nothing [src: tracker/project.yaml;
tests/__init__.py].

## Risks

- **Step 3 tightens validation on data that already exists.** A user whose store has a `due` this
  `recall` now refuses will find every command failing, including `recall add`. That is exactly
  what AC9 asks for [src: WI-0003 AC9] and `README.md` will say so after step 8, but it is a
  behaviour change reaching data written by an earlier version, and it is the thing most likely to
  surprise. `ADR-0007` records the cost; the mitigation is that the message names the file and the
  card and the file is left alone, so the user can fix it by hand.
- **Step 11 changes two existing tests, and the temptation is to weaken them.** Both assert real
  behaviour about a version number that this item moves. Changing `3` to `4` in the refusal test
  keeps it doing its job; deleting it would not. If a third test needs changing, that is a signal
  to re-read the criterion rather than to edit the test.
- **`next_interval` assumes `load` has already rejected a nonsense `interval`.** If step 3 is
  implemented after step 6, or incompletely, `next_interval` will meet a value not in `LADDER` and
  the failure will look like a scheduling bug rather than a validation gap. Implement step 3
  before step 6, and let `next_interval` raise rather than guess if it ever sees one.
- **The overdue case in AC2 is the one a naive implementation gets wrong.** Adding the interval to
  the card's old `due` passes every other check in this item, because every other case sets `due`
  to today. Step 6 says `when`, and the test in step 9 is the one that catches it.

## Out of scope for this item

- Any change to what the review session prints, including announcing when a card is next due
  [src: WI-0003].
- Any command or flag for inspecting or setting a schedule [src: WI-0003].
- Review history, statistics, and per-card or per-user tuning of the ladder [src: WI-0003].
- Splitting the store out of `recall.py`. The overview's condition for revisiting that has not
  been met [src: docs/architecture/overview.md].
- Timezones. `due` stays a local date with no zone, which `ADR-0006` recorded as a known
  limitation of a single-machine tool [src: ADR-0006].

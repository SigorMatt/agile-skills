# Plan — WI-0004 Delete a card that is no longer wanted

## Problem

`recall` can add cards, list them and review them, but nothing removes one. The stakeholder asked
for that in the answer that created this item — *"I want to be able to delete a card I don't need
anymore"* — and it is the only operation the tool will have that cannot be undone. Two questions
settled how it behaves: a card is named by typing its question side exactly, with a question that
matches two cards refused rather than guessed at (`WI-0004/Q-001`); and every deletion prints the
card and asks `[y/n]` first, with no flag to skip (`WI-0004/Q-002`). The constraints are the ones
already in force — one executable with subcommands and exit codes carrying the outcome
(`ADR-0001`), one JSON deck file written atomically and never repaired (`ADR-0004`), the three-layer
split with `store.py` silent, `deck.py` free of I/O and `cli.py` owning everything a person sees
(`docs/architecture/overview.md`), and the standard library only (`ADR-0003`). Twelve acceptance
criteria, AC1–AC12, are the contract.

## Approach

One new subcommand, and the smallest addition to each of the three layers that the existing
boundaries allow.

**`deck.py` gains the matching and the removal, as values.** Two additions:

- a module-level function `positions_matching(deck, question)` returning a tuple of the positions
  whose card's `question` equals `question` — plain `==` on the stored string, no folding, no
  stripping, no substring test, in deck order. It is the counterpart of `due_positions`, which is
  the existing precedent for "select positions, decide nothing". Returning **positions** rather
  than cards is what lets `cmd_delete` distinguish none from one from many without a second pass,
  and it is what AC5 needs: the count is the answer.
- a method `Deck.remove(position)` deleting the card at `position` and closing the gap, so the
  surviving cards keep their relative order. It is the third mutator beside `add` and `replace`;
  `replace` cannot serve, because it preserves length by design (`WI-0002` AC10).

Neither knows about the confirmation, the messages or the exit codes. That is the layer rule, and
it is what lets AC11 — the surviving cards' `rung`, `due` and order unchanged — be true by
construction: `remove` never constructs a `Card`.

**`store.py` is not touched at all.** `load` and `save` already do everything a deletion needs:
absent means an empty deck (`ADR-0004` §6, which is AC9), an unparseable file raises
`DeckUnreadable` and writes nothing (`ADR-0004` §5, which is AC8), and every write is a whole-file
atomic rewrite (`ADR-0004` §4). A deletion is a load, a removal in memory, and a save — the same
three moves `review` already makes after each graded card.

**`cli.py` gains the subcommand, the prompt and the four refusals.** `cmd_delete` in order:

1. Refuse a missing or blank `--question` **before opening the deck file**, exactly as `cmd_add`
   does and for the same reason: AC7's "the deck was not touched, and an absent deck is still
   absent" is then true by construction rather than by luck. Non-zero, message on stderr naming
   the option.
2. `store.load(store.deck_path())`, with `DeckUnreadable` caught at the single existing site —
   `_report_unreadable` — which already returns non-zero and writes nothing (AC8).
3. `deck_module.positions_matching(deck, args.question)`. Zero matches → message on stderr saying
   no card has that question, non-zero, no prompt, no write (AC4, and AC9 because an absent deck
   loads as an empty one). Two or more → message on stderr stating **how many** matched, non-zero,
   no prompt, no write (AC5).
4. Exactly one match: print its question side and its answer side to stdout, then one read through
   the existing `_read_line`. Anything but a yes — including `None` from end of input — prints
   that the card was not deleted and returns 0, having written nothing (AC6, `ADR-0009`).
5. A yes: `deck.remove(position)`, `store.save(deck, path)`, print what was removed, return 0
   (AC1). Persistence, absence from a sitting, and an empty-but-valid deck all follow from the
   save (AC2, AC3, AC10).

The prompt is a single read compared against one accepted value, and it deliberately does **not**
reuse `_read_grade`, whose re-asking loop is the shape `ADR-0009` rejects for this command. It
does reuse `_read_line`, whose `EOFError` handling is exactly what AC6's closed-standard-input
case needs.

**Nothing about `recall list` changes**, which is the point of AC12: the stakeholder chose the
naming rule that leaves the listing alone, so `cmd_list` is not edited and no field is added to
the deck file.

## Steps

1. **`recall/deck.py`** — add `positions_matching(deck, question)`, returning a tuple of positions
   in deck order whose card's `question` is equal to `question` by `==`. Docstring cites `WI-0004`
   AC4 and AC5 for why it returns every match rather than the first, and the item's `## Notes` for
   why the comparison is exact. Afterwards: a deck with two cards sharing a question side yields a
   two-element tuple, and a question no card carries yields an empty one.
2. **`recall/deck.py`** — add `Deck.remove(position)`, deleting `self._cards[position]`. Docstring
   says what it must not do: it does not construct a `Card`, so no surviving card's `rung`, `due`,
   `question`, `answer` or `grade` can change (`WI-0004` AC11). Afterwards: `len(deck)` is one
   smaller and `deck.cards` holds the others in their original order.
3. **`recall/cli.py`** — register the subcommand in `build_parser`: `subcommands.add_parser
   ("delete", ...)` with one option, `--question`, defaulting to `None` (not `required`, so that
   `cmd_delete` issues the refusal and names the deck it left alone, which is why `add` does the
   same), and `set_defaults(handler=cmd_delete)`. Afterwards: `recall delete --help` exits 0 and
   `recall` with no subcommand still exits non-zero.
4. **`recall/cli.py`** — add the two message constants beside the existing ones: the confirmation
   prompt, whose text ends in `[y/n]`, and the accepted reply `y`. Reuse `EXIT_REFUSED` and
   `EXIT_DECK_UNREADABLE`; add no new exit code. Afterwards: the wording lives with the other
   wording and no criterion depends on it (`ADR-0001` §5 fixes only the classes).
5. **`recall/cli.py`** — add `cmd_delete(args)` implementing the five-move order in `## Approach`,
   with the blank check before any file access and `DeckUnreadable` caught at the existing single
   site through `_report_unreadable`. Afterwards: each of AC1 and AC4–AC10 is reachable from a
   command line.
6. **`tests/test_delete.py`** — new module, following `tests/support.py` and the existing modules:
   invoke `bin/recall` as a subprocess with `HOME` redirected to a temporary directory
   (`ADR-0004` §1), and write deck files directly where a criterion needs particular `rung`/`due`
   values (`ADR-0004` §2). One test per criterion, named for it. For the "bytes identical" clauses
   in AC4–AC8, read the deck file before and after and compare the bytes.
7. **`tests/test_delete.py`** — add the AC12 case explicitly: run a deletion, then `recall list`,
   and assert the surviving lines are still `question | answer` with no leading number or code and
   the deleted card absent. This is the case AC12 says to add rather than waive, so that the
   criterion's non-intersection clause never has to be invoked.
8. **`docs/process/using-recall.md`** — add a `## Deleting a card` section: the invocation, that
   the question must be typed exactly as it is listed, the confirmation prompt and that only `y`
   deletes, that a question matching two cards is refused, and that there is no undo. Cross-refer
   the existing damaged-deck section rather than restating it. Bump to v6 with a change-log row
   (`spec/doc-header.md` §3). Afterwards: AC10's "the documented empty-deck message" and AC6's
   "says the card was not deleted" both have a document to be checked against, which is what the
   criteria's by-reference device requires.
9. **`docs/architecture/overview.md`** — bump to v5 and qualify one sentence: `cli.py` is still the
   only reader of standard input, but it now holds **two** prompt shapes — a sitting's loop that
   re-asks until it recognises a grade, and a deletion's single question where anything but a yes
   cancels — citing `ADR-0009`. Add the change-log row. This is the only shape change this item
   makes.
10. **Run the gates**: `python3 -m unittest discover -s tests -t . -q` and
    `python3 -m compileall -q recall tests`, both from the repository root, both exit 0.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — delete a named card, confirmed with `y` | 1, 2, 3, 5 | `tests/test_delete.py`: three-card deck, `recall delete --question <second>` with `y` on stdin; asserts exit 0, both sides of the card on stdout before the prompt text, and `recall list` afterwards showing the other two unchanged and not the deleted one |
| AC2 — the deletion survives the process ending | 5 (the `store.save` call) | the same test runs `recall list` as a **second** subprocess and asserts the deleted question side is absent and the other two present |
| AC3 — a deleted card is never presented in a review, due or not | 1, 2, 5 | a written deck file with X due today, Y due in seven days, Z due today; delete X then Y; `recall review` from a here-document asserts only Z's question side on stdout and exit 0 |
| AC4 — no card matches: refused | 5 (move 3, zero matches) | two-card deck, a question equal to neither; asserts non-zero exit, stderr non-empty, neither answer side on stdout, and the deck file's bytes identical before and after |
| AC5 — two cards match: refused, both kept | 1, 5 (move 3, many matches) | a deck built by two `recall add` runs with the same question side (`WI-0001` AC9); asserts non-zero exit, the count in the stderr text, no prompt, bytes identical, and both cards still listed |
| AC6 — anything but `y` cancels | 4, 5 (move 4) | four parameterised runs — `n`, a word, an empty line, `< /dev/null`; each asserts exit 0, the "not deleted" text on stdout, no `Traceback` in stderr, deck-file bytes identical, and both cards still listed |
| AC7 — missing or blank `--question` refused | 3, 5 (move 1) | four runs — omitted, `""`, spaces, tabs; each asserts non-zero, the option named in stderr, and the deck unchanged; one of the four runs with the deck file absent and asserts it is still absent |
| AC8 — an unreadable deck is refused, not repaired | 5 (move 2) | a deck file written as `not json`; asserts non-zero, the path in stderr, no prompt, and bytes identical |
| AC9 — an absent deck creates nothing | 5 (moves 2–3) | `HOME` pointed at an empty directory; asserts non-zero, and that the deck file **and** its parent directory are still absent afterwards |
| AC10 — deleting the last card leaves an empty, valid deck | 2, 5 | one-card deck, delete with `y`; then `recall list` asserts exit 0 and the empty-deck message from `docs/process/using-recall.md`, not an unreadable-deck error; then `recall add` exits 0 and the card is listed |
| AC11 — surviving cards keep their schedules | 2 | a written three-card deck with distinct `rung` and `due`; after deleting the middle card, the parsed JSON is asserted field by field — `question`, `answer`, `rung`, `due` on both survivors, their order, and `version` |
| AC12 — `recall list` is unchanged | 7, and steps 1–5 by not touching `cmd_list` | step 7's test: after a deletion, each listed line matches `^<question> \| <answer>$` with no leading number or code, and the empty-deck path is covered by AC10's test. The read of `WI-0001` AC3 and AC6 against this item's behaviour goes in the verification report; the executable case exists so the criterion's "waive it by name" branch is not needed |

## Assumptions

1. **The confirmation compares case-insensitively after stripping surrounding whitespace**, so
   `Y` and ` y ` delete and `yes` does not. This copies `_read_grade`'s existing treatment of `y`
   and `n` (`recall/cli.py`), so the tool is consistent about what a yes looks like even though
   `ADR-0009` makes the two prompts differ in every other way. Reversing it is one expression in
   `cmd_delete`; no stored data and no other subcommand depend on it.
2. **The card is printed on the two lines' existing shape — question, then answer indented —
   rather than as a `question | answer` line.** A deletion is showing you one card to look at, and
   a sitting already prints a card that way (`recall/cli.py`). No criterion constrains it: AC1
   asks only that both sides appear on stdout. Reversing it is one `print` in `cmd_delete`.
3. **No new exit code.** A refused deletion reuses `EXIT_REFUSED` and an unreadable deck reuses
   `EXIT_DECK_UNREADABLE`, because every criterion asks only for "non-zero" and the two existing
   codes already carry exactly this distinction (`recall/cli.py`). Reversing it is adding a
   constant and one return.
4. **`positions_matching` is not used by any other subcommand.** It is written for `delete`, and
   nothing in `add`, `list` or `review` is refactored to call it. Reversing it — generalising it
   later — costs nothing, whereas rewriting delivered behaviour to share it now would put three
   done items back in play against criteria that never asked for it.

## Decisions and ADRs

| decision | where it is recorded | how it was reached |
|----------|----------------------|--------------------|
| The prompt asks once; anything but `y` cancels; cancelling exits 0; the pre-prompt refusals exit non-zero; `review` is unchanged | **`ADR-0009` — Confirming a deletion asks once, and declining is not a failure** (new, this execution) | asked: it is interface-visible, it makes `delete` differ from `review` in a way a reader would otherwise take for an oversight, and `refine` had recorded the exit code as an assumption rather than a decision |
| Matching is exact — same bytes, no folding, no trimming, no substring | `WI-0004` `## Notes` and `artifacts/refinement-qa.md`, both by `refine` | documented: already decided upstream and recorded as `[assumed]` with its reversal cost. Not re-decided here |
| The matching and the removal go in `deck.py`; the prompt, the messages and the codes in `cli.py`; `store.py` is untouched | `docs/architecture/overview.md` §"Why it is split that way" | documented: the existing layer rules decide it, and `due_positions` is the precedent for a selector that returns positions and decides nothing |
| A deletion is load, remove, save — no new persistence machinery | `ADR-0004` §§4–6 | documented: atomic writes, never repairing an unreadable deck, and absent-is-empty are already fixed and give AC8, AC9 and AC11 without new code |
| `recall list` gains nothing — no number, no code, no column | `WI-0004/Q-001`, the stakeholder's answer | documented: their choice, and AC12 is the criterion that holds it |
| Message wording, and which of the two existing non-zero codes each refusal uses | `## Assumptions` 2–3 above, and step 4 | assumed: `ADR-0001` §5 fixes the classes and not the sentences, and `EP-001/Q-001`'s *"nothing fancier than that"* defers wording to us |

## Scaffolding

None. This execution created no file outside `tracker/` and `docs/`. `tests/test_delete.py` is
step 6's work and is `implement`'s to write; `tests/` already has `__init__.py` and
`tracker/project.yaml`'s test command already runs against it, so nothing is needed to make a
declared gate command execute.

## Risks

- **`positions_matching` returning positions is only sound while nothing reorders the deck between
  the match and the removal.** Nothing does — `cmd_delete` holds one in-memory `Deck` across both
  and `store.load` is called once — but a later change that re-loaded between the two would
  silently delete the wrong card. Step 1's docstring is where that constraint has to be written
  down, not just here.
- **Exact matching will be wrong for the person before it is wrong for the code.** The first time
  they type a question with a trailing space they did not know was there, they will get "no card
  has that question" and no hint why. AC4 is satisfied and the tool is still unhelpful. Step 8's
  documentation saying "exactly as `recall list` shows it" is the mitigation available inside this
  item; anything better — showing near misses — is a change with product stake and belongs to the
  stakeholder, not to this plan.
- **AC6's four cases share one code path, so one test passing is weak evidence for the other
  three.** All four go through `_read_line` returning either a string or `None`. The mitigation is
  that step 6 writes them as four separate runs of the real binary rather than one parameterised
  call into `cmd_delete`, so the end-of-input case genuinely exercises the subprocess boundary.
- **AC3 is the only criterion spanning two subcommands**, so it is the one most likely to be
  demonstrated by a test that deletes and then asserts something about `review` without a due card
  ever having existed. Step 6 must build the deck file with explicit dates rather than relying on
  `recall add`'s "due today".
- **`docs/process/using-recall.md` is load-bearing for two criteria**, AC6 and AC10, which name
  messages by reference to it rather than fixing wording. If step 8 is skipped or thinned, those
  two criteria become uncheckable rather than failing loudly.

## Out of scope for this item

- Any way to pick between two cards that share a question side. `WI-0004` `## Out of scope` records
  the stakeholder accepting that hole; AC5 refuses, and nothing here narrows it.
- A `--yes` flag or any other way to delete without confirming (`WI-0004` `## Out of scope`).
- Undo, a trash can, or any recovery of a deleted card.
- Deleting more than one card in one invocation, and deleting the whole deck.
- Editing a card — *"editing can wait"* (`EP-001/Q-001`).
- BUG-0001, the filesystem error that surfaces as a traceback. It touches `cli.py`'s error
  handling and it is tempting to fold in while `cmd_delete` is being written. It is a separate
  `ready` item with its own criteria, and widening this plan would make both unverifiable.

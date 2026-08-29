# Plan — WI-0004 Delete a card that was added by mistake

## Problem

`recall` can add a card, list the pile and review what is due, but nothing removes a card: a typo
or a duplicate keeps coming round for ever unless the user opens the JSON store and edits it by
hand [src: recall.py]. WI-0004 adds `recall delete <number>`, taking the card number `recall
list` already prints, for the person who has just mistyped a card and wants it gone
[src: WI-0004]. Three constraints shape it. It destroys something, which nothing else in this
tool does, and the stakeholder decided how that should feel: act immediately, print what went, no
confirmation prompt [src: WI-0004/Q-001]. It must never write a store it could not fully read,
which is `ADR-0004`'s standing rule [src: ADR-0004]. And it must not renumber the cards it leaves
behind [src: WI-0004 AC3].

## Approach

`delete` is a fourth command in the existing shape, not a new mechanism. `recall.py` already
separates pure functions over the document (`add_card`, `due_cards`, `record_result`) from the
command functions that resolve the path, load, mutate and save (`cmd_add`, `cmd_list`,
`cmd_review`) [src: recall.py]. This item adds one of each and registers the command in `main`.

**Interfaces this plan fixes** — signatures and contracts, with the bodies left to `implement`:

- `delete_card(document: dict, number: int) -> dict | None` — remove the card whose `number`
  equals `number` from `document["cards"]` and return it; return `None` when no card has that
  number. It touches no other card and renumbers nothing, which is what makes `AC3` fall out of
  the design rather than out of care [src: WI-0004 AC3]. Pure, like its neighbours, so most of
  the behaviour is testable without a filesystem.
- `cmd_delete(arguments: list) -> int` — returns `0`, `1` or `2` per `ADR-0009`.

**The order inside `cmd_delete` is the design**, because three criteria are about what is *not*
done:

1. Validate the command line before touching the disk: exactly one argument, and it must be a
   card number — a decimal integer of 1 or more. Anything else prints `USAGE_DELETE` on stderr
   and returns `2`, having opened nothing [src: WI-0004 AC8; src: ADR-0009].
2. `store_path()`, then `load()` inside `try/except StoreError` → message on stderr, return `1`.
   A store that does not parse is refused here, before any decision about cards, so it is
   impossible to write one back [src: WI-0004 AC9; src: ADR-0004].
3. `delete_card`. On `None`: message on stderr naming the number, return `1`, **without calling
   `save`** — so the file is byte-identical, and a missing store stays missing
   [src: WI-0004 AC5; src: WI-0004 AC6; src: ADR-0009].
4. Otherwise `save()`, then one line on stdout, then `0`.

**The confirmation line** carries the number and both sides of the card that went, because that
is what the stakeholder chose over a prompt: *"just delete it and tell me what got deleted"*
[src: WI-0004/Q-001]. The exact wording is `implement`'s, under the stakeholder's standing
deferral on naming and output wording [src: WI-0001/Q-002]; `AC2` fixes only what it must
contain. There is no prompt, nothing is read from stdin, and stderr stays empty on success —
`AC2` pins both streams so that the absence of a prompt is observable [src: WI-0004 AC2].

Nothing about `add`, `list` or `review` changes, except that `main`'s top-level usage line grows
a fourth command name [src: WI-0004].

## Steps

1. **Add the command's constants to `recall.py`**, beside the existing `USAGE_*` block: a
   `USAGE_DELETE` in the established form (`usage: recall delete <card number>`), and change
   `USAGE` to name all four commands. Afterwards `recall` with no arguments and `recall bogus`
   print a usage line that mentions `delete`, and both still exit `2`. No test pins the current
   `USAGE` string — `tests/test_review.py` asserts only `usage: recall review` — so this breaks
   nothing already delivered [src: tests/test_review.py].

2. **Add `delete_card(document, number)` to `recall.py`**, beside `add_card`. Removes and returns
   the card with that `number`, or returns `None`. Afterwards the document held in memory has one
   fewer card and every other card object is the same object it was, unmodified. Numbering is not
   touched: `add_card` keeps deriving the next number from the largest present, and a number may
   be reused after the highest card is deleted [src: ADR-0008].

3. **Add `cmd_delete(arguments)` to `recall.py`**, beside `cmd_list`, in the four-part order set
   out under Approach. Argument parsing rejects a count other than one, a non-digit string, and a
   value below 1, each with `USAGE_DELETE` on stderr and exit `2`; `load` failures exit `1`; a
   number naming no card exits `1` with a message on stderr naming the number and nothing on
   stdout, without saving; success saves and prints one stdout line containing the number and
   both card sides, and exits `0` [src: ADR-0009; src: WI-0004 AC2].

4. **Register the command in `main`** in `recall.py`, alongside `add`, `list` and `review`.
   Afterwards `recall delete …` reaches `cmd_delete` and `recall` still returns `2` for an
   unknown command.

5. **Write `tests/test_delete.py`**, a `CommandTestCase` subclass driving the built executable
   through `run_recall` against a temporary store, one test method per criterion, each naming its
   AC in the docstring as the existing suites do [src: tests/support.py]. Cover: the deletion and
   the follow-up listing (AC1); the stdin-closed run with both streams pinned (AC2); the
   before-and-after comparison of the surviving card objects (AC3); delete-then-review (AC4); an
   unknown number, with the store's bytes compared before and after (AC5); no store file at all
   (AC6); deleting the last card, then `list` and `add` (AC7); the four wrong command lines
   (AC8); a non-JSON store, bytes compared (AC9). For AC2, read the process's stdout and assert
   `len(stdout.splitlines()) == 1` and `stderr == ""`, and pass `stdin=""` so nothing is
   available to read.

6. **Add the `delete` case to `tests/test_delete.py` for number reuse** — delete the
   highest-numbered card, add another, and assert the new card takes the freed number. No AC
   requires this; it is here because `ADR-0008` decided it deliberately and an undefended
   decision is one a later change breaks silently. Mark it in the docstring as covering
   `ADR-0008`, not an AC.

7. **Add the README entries** in `README.md`: a `### recall delete <number>` section under
   `## Commands`, written in the same shape as `add`, `list` and `review` — what it does, an
   example invocation with its output, and what happens when the number names no card
   [src: WI-0004 AC10]. In the same step, two things the change makes wrong elsewhere in the
   file, required by the Definition of Done rather than by an AC: the `## Exit codes` table's row
   for `1`, which states the narrow meaning `ADR-0009` widens, and the `## Where your cards are
   kept` section, which should say that a deleted card's number can be reused by the next card
   added [src: ADR-0008; src: ADR-0009].

8. **Extend `tests/test_docs.py`** with assertions that `README.md`'s `## Commands` section
   contains a `recall delete` entry and that the entry says what happens when the number names no
   card, in the style of the existing README tests [src: tests/test_docs.py]. This is what makes
   `AC10` a criterion a checker settles rather than reads.

9. **Run the project's commands** — `python3 -m unittest discover -s tests -t .` and
   `python3 -m compileall -q -x '[.]claude' .` — and record their exit codes in the
   implementation report [src: tracker/project.yaml].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 | 2, 3, 4 | `tests/test_delete.py`: on a three-card store, `recall delete 2` exits 0 with one stdout line; a following `recall list` prints cards 1 and 3 and no 2 |
| AC2 | 3 | `tests/test_delete.py`: `recall delete 2` run with empty stdin exits 0, `stderr == ""`, stdout is exactly one line, and that line contains `2`, card 2's question text and card 2's answer text |
| AC3 | 2, 3 | `tests/test_delete.py`: the store document is read before and after; the card objects for 1 and 3 compare equal on `number`, `question`, `answer`, `due` and `interval` |
| AC4 | 3, 4 | `tests/test_delete.py`: a store with one card due today, `recall delete 1`, then `recall review` prints `Nothing is due today.` and exits 0 |
| AC5 | 3 | `tests/test_delete.py`: `recall delete 9` on a three-card store exits 1, `9` appears in stderr, stdout is empty, and the file's bytes are identical to those read before the run |
| AC6 | 3 | `tests/test_delete.py`: with no file at the store path, `recall delete 1` exits 1, stderr is non-empty, and `os.path.exists(store)` is still false |
| AC7 | 2, 3 | `tests/test_delete.py`: a one-card store, `recall delete 1`, then `recall list` prints `No cards yet.` and exits 0 and `recall add "q" "a"` exits 0 |
| AC8 | 3, 1 | `tests/test_delete.py`: four runs — no argument, `1 2`, `two`, `0` — each exiting 2 with `usage: recall delete` in stderr and the store's bytes unchanged |
| AC9 | 3 | `tests/test_delete.py`: a store file containing `{ not json`, `recall delete 1` exits 1, stderr names the store path, and the file's bytes are unchanged |
| AC10 | 7, 8 | `tests/test_docs.py`: `README.md` contains a `### recall delete` heading inside `## Commands` and text stating what happens when the number names no card; read alongside the `add`, `list` and `review` entries for form |

Every criterion has a step and a demonstration. Steps 6 and 7's second half map to no AC by
design: step 6 defends `ADR-0008`, and step 7's README corrections are required by D7 and D12,
which ask that documents the change invalidated are updated and that claims in `docs/` about the
behaviour this item touched are still true.

## Assumptions

- **A card number argument is a decimal integer of 1 or more, and nothing else.** `AC8` names
  `two` and `0` as wrong command lines and says nothing about `+1`, `01`, ` 1` or `1.0`
  [src: WI-0004 AC8]. This plan reads them all as "not a card number" and returns `2`, on the
  precedent that `recall.py` matches review keys exactly and treats ` y` as unrecognised
  [src: recall.py]. To reverse: one predicate in `cmd_delete`, no data and no interface change.
- **The store is saved once, after a successful removal, and not at all otherwise.** No criterion
  states this for the success case; `AC5`, `AC6`, `AC8` and `AC9` state it for the four failures.
  To reverse: the placement of one call.
- **`delete` does not report how many cards remain.** The stakeholder asked for one line saying
  what went [src: WI-0004/Q-001]; a count would be output nobody requested. To reverse: one
  format string.

## Decisions and ADRs

| decision | route | where |
|----------|-------|-------|
| A deleted card's number may be reused by the next card added; `add_card`'s numbering is unchanged; the store schema and `STORE_VERSION` do not change | decided — `ADR-0004`'s option F re-weighed against the premise this item removes, and kept | `ADR-0008` |
| Exit `1` widens from "the store could not be used" to "the command could not be carried out"; `2` stays decidable from the command line alone; a card number naming no card, and a missing store, are both `1` | decided — `ADR-0005` never contemplated this case, so this extends rather than supersedes it | `ADR-0009` |
| Argument shapes other than a plain positive decimal integer are `2` | assumed, reversible | `## Assumptions` |
| The store is written once on success and never on any failure path | assumed, reversible | `## Assumptions` |
| No count of remaining cards in the confirmation line | assumed, reversible | `## Assumptions` |
| Whether to prompt before deleting | asked — the stakeholder chose option C, act immediately and say what went | `WI-0004/Q-001`, `AC2` |
| The wording of the confirmation line, the usage line and the not-found message | documented — the stakeholder's standing deferral covers naming and output wording | `WI-0001/Q-002`, `ADR-0005` |
| The command name, its single positional argument, and the stream split | documented | `ADR-0005`, `WI-0004` `## Notes` |

All three questions `refine` routed to `plan` are settled here: number reuse and the store
version in `ADR-0008`, the exit code in `ADR-0009` [src: WI-0004].

## Scaffolding

none. Both project commands already run against this tree: `tests/` exists with an
`__init__.py`, and `compileall` needs nothing [src: tracker/project.yaml; src: tests/support.py].

## Risks

- **The exit-code widening in `ADR-0009` is a judgement about a boundary, not a fact.** If a
  later reader concludes that `recall delete 9` should have been `2` — the command line named
  something that is not there — the criteria still pass, because `AC5` and `AC6` say *non-zero*.
  The cost of being wrong is one ADR and one README row, which is why `ADR-0009` was written
  rather than the choice being buried in a step.
- **Number reuse is now reachable without a text editor.** `ADR-0008` accepts this because
  nothing refers to a card by number except the card itself. The risk is to work that does not
  exist yet: a review history, a statistics command or an export that used the number as an
  identifier would be wrong from its first day. `ADR-0008` states that constraint; nothing
  enforces it.
- **`AC3` is checked on a two-survivor store.** Nothing in the criteria exercises deleting from
  the middle of a large pile, and `delete_card`'s contract makes position irrelevant, but the
  evidence for that is the design rather than a test.
- **Step 7 edits three separate places in `README.md`.** The one an AC checks is the `##
  Commands` entry; the exit-code row and the number-reuse note are checked only by `review-close`
  reading the file. A hurried execution could do the first and skip the other two, and the item
  would still pass verification.

## Out of scope for this item

- Editing a card, a schedule command, and any statistics — all three declined by the stakeholder
  at sign-off, and all three already in the item's `## Out of scope` [src: EP-001/Q-005].
- Undo, a trash state, or recovering a deleted card's schedule [src: WI-0004].
- Deleting several cards at once, deleting by matching text, and deleting everything
  [src: WI-0004].
- Any change to `add`, `list` or `review` beyond the top-level usage line naming a fourth
  command.
- Splitting the store out of `recall.py`. The overview re-asks that question when something other
  than a command needs the store; a fourth command is not that [src: docs/architecture/overview.md].

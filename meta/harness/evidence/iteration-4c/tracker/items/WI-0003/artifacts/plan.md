# Plan — WI-0003 Delete a card

## Problem

The deck can be added to and reviewed [src: WI-0001] [src: WI-0002]. What it cannot do is get
smaller. The stakeholder asked for that in their own words — *"I want to be able to delete a card;
editing can wait"* [src: EP-001/Q-004] — and this item delivers one more subcommand,
`python3 -m recall delete <front>`, which finds the card or cards with that front side, shows what
is about to be lost, asks, and removes exactly the one chosen.

Every product decision it applies is already taken. A card is named by its front side typed out,
and there is no listing and no card number [src: ADR-0005] [src: WI-0003/Q-001]. The tool shows
the card and its schedule and asks before removing anything, and a negative reply is an ordinary
outcome rather than an error [src: ADR-0005] [src: WI-0003/Q-002]. Deletion is permanent — no
trash, no undo, no force flag [src: ADR-0005]. A front matching nothing removes nothing and exits
non-zero; a front matching several lists them and asks which [src: ADR-0005]. What the prompts
take, and what happens when the answer is neither yes nor no, was settled by `refine` under the
stakeholder's standing deferral and is in the criteria [src: WI-0003 AC2] [src: WI-0003 AC6]
[src: WI-0003 AC7].

So there is little left to decide and one thing worth deciding carefully: **which of several cards
sharing a front side actually gets removed.** Two cards may share a front [src: WI-0001 AC6], and
`recall/schedule.py` already carries the same hazard — it hands the session card *positions* rather
than cards, for exactly this reason [src: recall/schedule.py]. Deletion has to be as careful, or a
person who confirms card 2 loses card 1.

## Approach

**No new module.** `delete` is a third subcommand on the existing seam and nothing about the shape
of the system changes [src: docs/architecture/overview.md]. `recall/store.py` keeps owning the
file's location, format and atomic rewrite; `recall/cli.py` keeps owning arguments, the
conversation, what is printed and the exit code. `recall/schedule.py` is not touched at all —
deletion applies no rule of the ladder's.

**The matching lives in `recall/cli.py`, as a list of positions.** `add()` already reaches into the
loaded list directly (`cards.append(...)`), and `delete()` does the same in reverse: it computes
`[index for index, card in enumerate(cards) if card.front == front]` and deletes one of those
indices. Positions, not cards, and not a copy of the card object — the identity of the record being
removed has to survive the prompt [src: WI-0001 AC6] [src: recall/schedule.py]. The comparison is
exact equality on the stored front, with no strip, no case-folding and no unicode normalisation,
because `ADR-0007` stores a side verbatim and `WI-0001` AC2 promises it reads back byte-identical
[src: ADR-0007] [src: WI-0001 AC2].

**`_ask()` is reused unchanged, and it is what makes AC7 free.** It already prints a prompt, reads
one line, strips and lowercases it, re-asks by reprinting *the whole prompt string it was given*
when the answer is not accepted, and returns `None` at the end of the input stream
[src: recall/cli.py]. So if the prompt string contains the card, a re-ask shows the card again,
which is what AC7 asks for [src: WI-0003 AC7]. The one thing `delete` does differently from
`review` is what it makes of `None`: `review` treats it as `q` and stops; `delete` treats it as
`n` and removes nothing [src: WI-0003 AC7].

**New functions in `recall/cli.py`:**

- `_rung(card: store.Card) -> str` — the rung written for a person: `"2 of 4"`, and
  `"0 of 4 (never answered)"` on rung 0, which is how `WI-0001` writes a card nobody has answered
  [src: WI-0001] [src: ADR-0002].
- `_described(card: store.Card, indent: str) -> str` — one card as four labelled lines,
  `front`/`back`/`rung`/`due`, each prefixed by `indent`, with the due date in `YYYY-MM-DD` as the
  file holds it. The labels deliberately match `ADR-0007`'s field names so that what the prompt
  shows and what the file holds are read the same way [src: ADR-0007].
- `delete(front: str) -> int` — the whole command. Load, match, then one of three paths:
  - **no match** — print `No card has the front '<front>'.` and `Nothing was deleted.` to standard
    error, return `EXIT_REFUSED`. Nothing is written and no prompt is shown [src: WI-0003 AC5].
  - **exactly one match** — `_ask()` with the prompt `About to delete:` followed by the card's four
    lines and `Delete it? y to delete, n to keep.`, accepting `("y", "n")`. On anything but `y`,
    including the stream ending, print `Nothing was deleted.` to standard output and return
    `EXIT_OK` without writing [src: WI-0003 AC2] [src: WI-0003 AC7]. On `y`, fall through to the
    removal below.
  - **several matches** — `_ask()` with a prompt that states the count, lists each match as
    `[n]` followed by its four lines in card-file order, and ends
    `Which one? <numbers> to delete that card, n to keep them all.`, accepting the numbers as
    strings plus `"n"`. `n` or the stream ending behaves exactly as the declined single match. A
    number selects `positions[number - 1]` [src: WI-0003 AC6].
  - **the removal** — `del cards[position]`, `store.save(path, cards)`, print `Deleted: <front>`
    to standard output, return `EXIT_OK` [src: WI-0003 AC1].
- `main()` dispatches `delete` alongside `add` and `review`. It is rewritten as an explicit
  three-way choice on `arguments.subcommand` rather than a chain ending in a bare `return add(...)`
  — the same trap `WI-0002` had to disarm, which is worth not re-arming
  [src: tracker/items/WI-0001/artifacts/review.md] [src: recall/cli.py].
- `_parser()` gains a `delete` subparser with one positional argument, `front`. argparse then owns
  AC9's wrong-argument-count behaviour: it prints a usage message naming `delete` and exits `2`
  [src: WI-0003 AC9].

**Nothing validates the argument.** An empty or whitespace-only front is not refused up front; it
simply matches no card, because `WI-0001` AC7 makes an empty side unstorable, so no stored card can
have one [src: WI-0001 AC7] [src: WI-0003 AC9]. Adding a validator would produce a second refusal
message for a case AC5 already covers.

**Where the output goes** follows the rule the overview already states: confirmations to standard
output, refusals to standard error [src: docs/architecture/overview.md]. So `Deleted: …` and
`Nothing was deleted.` are stdout — a declined deletion is an ordinary outcome that exits zero —
and the no-match refusal, which exits non-zero, is stderr.

**An unparseable card file needs no new code.** `store.load()` raises `CardFileError` and
`main()`'s existing handler prints the path and the message and returns `EXIT_REFUSED`, before
`delete()` has printed anything. That is AC8, and it is the same refusal `add` and `review` already
make [src: recall/store.py] [src: recall/cli.py] [src: WI-0002 AC14].

## Steps

1. **Branch.** `git switch -c wi/WI-0003` from `main` at `667c24e`. Every commit's subject follows
   `tracker/project.yaml`'s `conventions.commit-subject` and names `WI-0003`.
2. **`recall/cli.py` — the card renderer.** Add `_rung(card)` and `_described(card, indent)` as
   described in `## Approach`. Afterwards, `_described` on a rung-0 card due today returns four
   lines reading `front: …`, `back: …`, `rung:  0 of 4 (never answered)`, `due:  <today>`, and
   nothing else in the module has changed behaviour.
3. **`recall/cli.py` — `delete(front)`, the no-match path.** Load the file, compute the matching
   positions, and implement the no-match branch: two lines to stderr, `EXIT_REFUSED`, no write.
   Afterwards, running `delete` for a front no card holds refuses and leaves the file byte-identical
   — including when the file does not exist, since `store.load()` returns `[]` for a missing file
   and nothing calls `store.save()` on this path [src: recall/store.py].
4. **`recall/cli.py` — the single-match confirmation.** Build the prompt, call `_ask(prompt,
   ("y", "n"))`, and implement both replies. Afterwards, `y` removes the card, saves, prints
   `Deleted: <front>` and exits 0; `n` and a closed input stream print `Nothing was deleted.` and
   exit 0 with the file untouched; an unrecognised line re-asks with the card reprinted.
5. **`recall/cli.py` — the several-match prompt.** Build the numbered listing, call `_ask()` with
   the numbers and `"n"`, and map the answer back to `positions[number - 1]`. Afterwards, deleting
   a front held by three cards lists all three in card-file order, and answering `2` removes the
   second of them and leaves the other two with their own back, rung and due date.
6. **`recall/cli.py` — wire it up.** Add the `delete` subparser with its one positional `front` to
   `_parser()`, and make `main()` dispatch all three subcommands explicitly. Afterwards,
   `python3 -m recall delete` with no argument prints a usage message naming `delete` and exits
   non-zero, and `add` and `review` still behave exactly as `WI-0001` and `WI-0002` left them.
7. **`tests/test_delete.py` — new file.** Follow `tests/test_review.py`'s pattern exactly: seed a
   card file by writing `ADR-0007`'s format directly, point `RECALL_CARD_FILE` at it inside a
   temporary directory, run the tool as a subprocess with keystrokes on standard input, and parse
   the resulting file with the test module's own reader rather than the tool's
   [src: tests/test_review.py] [src: ADR-0008]. At least one case per criterion, named in the
   mapping table below. Byte-identity is asserted by comparing the file's bytes before and after,
   not by re-parsing.
8. **Run the gates on the branch head.** `python3 -m unittest discover -s tests -t . -q` and
   `python3 -m compileall -q recall tests`, both from the repository root, both green, with the
   whole suite run and not only the new file [src: tracker/project.yaml].
9. **Write `tracker/items/WI-0003/artifacts/impl-report.md`**, naming for each criterion the test
   or the command that exercises it. Leave the checkboxes in `item.md` unticked — ticking them is
   `verify`'s, not `implement`'s [src: .claude/agile-skills/spec/work-item.md].

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `delete <front>`, `y`, card removed, confirmation naming the front, exit 0 | 4, 6 | `test_delete.py`: seed two cards, `delete` the first with `y` on stdin; assert stdout contains `Deleted: <front>`, exit code 0, and the stored file holds only the other card |
| AC2 — the card and its schedule shown first; `y`/`n` stated; `n` writes nothing and exits 0 | 2, 4 | two cases: one asserts the prompt text contains the card's front, back, `rung` and `due` values and names `y` and `n`; one answers `n` and asserts exit 0, `Nothing was deleted.` on stdout, and the file's bytes unchanged from a copy taken before the run |
| AC3 — the deleted card is never offered again; the others keep their state | 4, 5 | seed three cards all due today, delete one, then run `review` and assert its stated count is `2`, that the deleted front appears nowhere in the session's output, and that the two survivors' rung and due values are unchanged in the file |
| AC4 — the deletion is in the stored file, and the file still works when emptied | 4 | delete the only card, then read the file's text and assert no `front:` line remains; then run `review` (asserting `Nothing is due.` and exit 0) and `add` (asserting exit 0 and the new card present) against that same file |
| AC5 — no match: no prompt, a message naming the front, non-zero exit, file byte-identical | 3 | three cases — a populated file with no such front, a file holding no cards, and no file at all — each asserting a non-zero exit, the front quoted in stderr, no `About to delete` anywhere in the output, and the file bytes unchanged or still absent |
| AC6 — several matches listed and numbered; the chosen one goes; `n` keeps them all | 5 | seed three cards sharing a front with different backs, rungs and due dates; assert the prompt lists all three with all four values each and states what it takes; answer `2`, assert exactly the second is gone and the other two are byte-for-byte unchanged in the file; a second case answers `n` and asserts nothing changed and exit 0 |
| AC7 — unrecognised input re-asks with the card reprinted; a closed stream deletes nothing | 4, 5 | at the single-match prompt, send `maybe\nn\n` and assert the card block appears twice in stdout and the accepted answers are restated; send no input at all (closed stdin) at both the single-match and the several-match prompt and assert exit 0, `Nothing was deleted.`, and the file's bytes unchanged |
| AC8 — an unparseable card file stops `delete` before any prompt | 3 | write a card file with a corrupt `rung:` line, run `delete` for a front that exists in it, and assert a non-zero exit, the path and a line number in stderr, no `About to delete` in the output, and the file's bytes unchanged |
| AC9 — wrong argument count is a usage message; an empty argument is AC5's no-match | 6, 3 | `delete` with no argument and with two arguments: assert a non-zero exit and `delete` named in the usage message, file unchanged; `delete ""` and `delete "   "`: assert AC5's no-match refusal |

## Assumptions

1. **The matching and the removal live in `recall/cli.py`, not in a new function in
   `recall/store.py`.** `add()` already mutates the loaded list in place and `store` stays the
   module that only knows the file, which is how the overview describes the seam
   [src: docs/architecture/overview.md]. Reversing it means moving one list comprehension and one
   `del` into a `store.remove(cards, position)` — one file, no stored data changes, no interface
   anyone outside the package uses. Cheap.
2. **Front matching is exact string equality on the stored value.** No strip, no case folding, no
   normalisation. Basis: `ADR-0007` stores a side verbatim and `WI-0001` AC2 promises it reads back
   byte-identical, so anything looser would delete a card the person did not type
   [src: ADR-0007] [src: WI-0001 AC2]. Reversing it is one comparison in one function, and it would
   need a decision from the stakeholder anyway, because it changes which card a typed front finds.
3. **The exact wording of the prompts and the confirmation** — `About to delete:`,
   `Delete it? y to delete, n to keep.`, `Which one? … to delete that card, n to keep them all.`,
   `Deleted: <front>`, `Nothing was deleted.`, `No card has the front '<front>'.` Basis: the
   stakeholder's standing deferral, *"As for how it's actually built — whatever you think is
   best"* [src: EP-001/Q-004], the same authority `refine` recorded for the keystrokes
   [src: tracker/items/WI-0003/artifacts/refinement-qa.md]. Reversing any of it is a string
   literal and the test that asserts it. The criteria constrain what the text must *contain* —
   the four values, the accepted answers, the front side — not these exact sentences, so a later
   change to the wording does not break an acceptance criterion.
4. **The several-match listing is numbered from 1 in card-file order**, which is `WI-0003` AC6 and
   the same order `review` offers cards sharing a due date [src: WI-0003 AC6]
   [src: recall/schedule.py]. Reversing it is one `enumerate` and would be a change to a criterion,
   not just to the code.

## Decisions and ADRs

| decision | where it is recorded | branch of the preference order |
|----------|----------------------|-------------------------------|
| Delete names a card by its front side; the tool shows it and asks; deletion is permanent; no match refuses; several matches are listed and one is chosen | `ADR-0005` | documented — read, cited, not re-decided |
| The card file's format, location and atomic whole-file rewrite, which `delete` inherits unchanged | `ADR-0007`, `ADR-0008` | documented |
| Rung 0 means never answered, and the ladder is 1/3/7/30, which the prompt displays but does not apply | `ADR-0002` | documented |
| Python 3, standard library only; the project's test and lint commands | `ADR-0006`, `tracker/project.yaml` | documented — both commands already resolved, and this execution changed neither |
| No new module; matching in `cli.py`; exact-equality front matching; prompt wording; numbering from 1 | `## Assumptions` 1–4 above | assumed, reversibly |
| Nothing | — | asked — no question was put to the stakeholder by this execution, because nothing left is irreversible and nothing depends on intent the record does not hold |

**No new ADR.** Every decision this change forces is either already recorded — `ADR-0005` decides
the whole of deletion's behaviour — or is a reversible assumption above. Writing an ADR to say
"deletion is a third subcommand in the module that already holds the other two" would pad the trail
with a non-decision and make the real ones harder to find.

**Nothing here reconciles two of the stakeholder's answers.** The one place two of their statements
meet — *"I don't need a numbered list for this"* against AC6's numbered prompt — was checked and
recorded as compatible by `refine`, with the scope of their sentence stated, and no document of
theirs was edited [src: tracker/items/WI-0003/artifacts/refinement-qa.md].

## Scaffolding

`none`. Both gate commands already run in this project against the existing package and test
directory; `tests/__init__.py` and `recall/__init__.py` exist from `WI-0001`. This execution
created no file outside `tracker/`.

## Risks

- **The prompt and the file could disagree about what a card is.** The confirmation shows a
  rendering, and the person confirms against it; if `_described()` ever trimmed, wrapped or
  escaped a side, they would confirm the deletion of something other than what they saw. Step 2
  renders values verbatim and the AC2 test asserts the prompt contains the stored strings, which
  is what keeps this closed [src: ADR-0007].
- **A stale position.** `delete()` reads the file, prompts — which can take as long as the person
  likes — and then writes the whole file back from the list it read. Another `recall` process
  writing in between would be lost. This is the concurrent-writer gap `WI-0002`'s close already
  accepted for the whole tool, not a new one [src: tracker/items/WI-0002/item.md], and `ADR-0008`'s
  atomic rename means the loser is overwritten rather than the file corrupted [src: ADR-0008]. Out
  of scope here; if it is ever addressed it belongs to the store, for every subcommand at once.
- **`_ask()` re-prompting a long listing.** With many matches, an unrecognised keystroke reprints
  the whole list. That is AC7's requirement rather than a defect, and the alternative — printing
  only the question again — is the failure `WI-0002` AC13 exists to prevent
  [src: WI-0002 AC13].
- **The item's dependency is satisfied, not assumed.** `delete` reads and rewrites `WI-0001`'s
  file; `WI-0001` is `done` and merged, so the format and the path are fixed rather than pending
  [src: WI-0001].

## Out of scope for this item

- Editing a card, a listing or search command, a force flag or quiet mode, a trash or undo, deleting
  several cards at once, and deleting from inside a review session. All six are in the item's
  `## Out of scope` and four of them rest on the stakeholder's own words
  [src: WI-0003] [src: ADR-0005].
- Any change to `recall/schedule.py`, to the ladder, or to what `review` accepts. `WI-0002`'s
  fourteen criteria must read true after this item ships, and the way to keep them true is to leave
  the session alone [src: WI-0002].
- Making the tool safe for two processes writing at once. Named as a risk above; it is the whole
  tool's gap and belongs to `recall/store.py` if it is ever taken on.

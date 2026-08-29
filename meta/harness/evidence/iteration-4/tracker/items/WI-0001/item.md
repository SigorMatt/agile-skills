---
id: WI-0001
type: work-item
title: Add a card and have it persist across runs
status: done
priority: high
epic: EP-001
created: "2026-08-29T10:45:13Z"
updated: "2026-08-29T11:36:14Z"
blocks:
  - WI-0002
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone building up a set of things to memorise, I want to add a card with a question side
and an answer side, so that the thing I want to learn is captured once and is still there the
next time I open the tool.

## Acceptance criteria

- [x] AC1 — Running `recall add "<question side>" "<answer side>"` in a terminal — both sides
      given as arguments to one command, in that order — exits 0 and prints a confirmation line
      containing a number that identifies the card just added. Card numbers start at 1 and
      increase by 1 per card added.
- [x] AC2 — After adding a card, running `recall list` in a fresh process prints that card with
      both sides byte-identical to what was entered, against the number AC1 reported.
- [x] AC3 — Adding two cards whose text is identical produces two separate cards with different
      numbers, both shown by `recall list`.
- [x] AC4 — Running `recall add "" "the cat"` exits non-zero and prints a message naming the
      question side as the empty one; running `recall add "die Katze" ""` exits non-zero and
      prints a message naming the answer side. After either, `recall list` shows that no card
      was stored.
- [x] AC5 — The cards are stored in one file on disk that a person can open and read: by
      default `~/.recall.json`, or the path in the environment variable `RECALL_FILE` when that
      is set and non-empty. Checked by running `RECALL_FILE=<tmp>/cards.json recall add "a" "b"`
      and finding the card in `<tmp>/cards.json`, which opens in a text editor as readable text.
      Both the default path and the override are named in the project's `README.md`
      [src: ADR-0002].
- [x] AC6 — Cards are added to a single flat pool: `recall add` accepts exactly the two
      positional arguments AC1 names and no deck, tag or category option — passing one, such as
      `recall add --deck german "die Katze" "the cat"`, exits non-zero — and `recall list` shows
      every card that has been added, in ascending card-number order.
- [x] AC7 — A card whose text contains non-ASCII characters — accents, umlauts, a non-Latin
      script — is stored and listed byte-identical to what was entered, checked by adding
      `recall add "Grüße" "greetings"` and comparing the listed text with the input.
- [x] AC8 — `recall list` with no cards stored prints a single plain line saying there are no
      cards, prints nothing else, and exits 0.
- [x] AC9 — `recall add` with any number of positional arguments other than two — `recall add`,
      `recall add "die Katze"`, `recall add "die Katze" "the cat" "extra"` — exits non-zero,
      prints a usage line on stderr naming the two arguments it expects, and stores nothing.

## Out of scope

- Editing or deleting a card once added — out of scope for EP-001 entirely.
- Organising cards into decks, tags or categories. Settled: the stakeholder chose one flat pool
  in `EP-001/Q-004` — *"One flat pool. It's just vocab, one pile is fine."*
- Anything about when a card is next due; scheduling belongs to WI-0002 and WI-0003. This item
  stores whatever state those items need, but decides none of it.
- Card sides that are anything other than plain text, and card sides spanning more than one
  line. Assumed by `refine`, not stated by the stakeholder: vocabulary cards are one line a
  side, and multi-line text changes how the store is read by eye (AC5) as well as how the
  review session displays a card.
- Any command other than adding a card and listing the cards. Reviewing is WI-0002.

## Notes

`EP-001/Q-001`–`Q-004` are answered. The stakeholder chose a command-line tool — *"Command-line
tool. I'll be sitting at a terminal doing this once a day, that's all it needs to be."* — so
AC1–AC4 are now stated as commands run in a terminal with observable output and exit codes, and
AC6 records the flat-pool decision from `Q-004`. `answer-questions` amended these criteria while
the item was at `draft`.

`refine` round 1 (see `artifacts/refinement-qa.md`) settled the tool's name, card numbering, the
empty-listing case and non-ASCII text as recorded assumptions, and filed two questions to the
stakeholder that it may not settle for them. Both are now resolved:

- `Q-001` — how a card is typed in. The stakeholder chose both sides as arguments to one
  command — *"Both sides on the command line in one go — `recall add "front" "back"`. I'm
  sitting at a terminal, I don't need it to ask me twice."* AC1 and AC4 now state exactly what
  is typed, so neither depends on driving an interactive prompt.
- `Q-002` — where the card file lives. The stakeholder declined to choose — *"Whatever you think
  is best, you know this better than I do."* — so `answer-questions` decided it under that
  deferral and recorded it as `ADR-0002`: one JSON file at `~/.recall.json`, with the
  environment variable `RECALL_FILE` overriding that path when it is set and non-empty. AC5
  names both.

Open design questions still left for `plan` rather than for the stakeholder: the schema inside
the store file, how a write survives an interruption part-way through so that a crash cannot
leave the file unreadable, whether the store is created eagerly or on the first add, and what
`recall` does when `RECALL_FILE` names a path it cannot write. `ADR-0002` settled the file's
*format* — JSON — because both of the options the stakeholder was shown named a `.json` file; it
did not settle what is inside it.

`refine` round 2 needed nothing from the stakeholder. Everything still open was either a naming,
wording or exit-code choice — which their standing deferral on `Q-002` covers as a category,
*"Whatever you think is best, you know this better than I do."* — or a design question already
routed to `plan`. Round 2 tightened AC5 (it now names `README.md` as the documentation a checker
greps, and gives the `RECALL_FILE` observation), tightened AC6 (the no-deck-argument half is now
observable, and `recall list` is ordered by ascending card number), and added AC9 for the wrong
argument count, which round 1 had left deliberately unconstrained. All three are `[assumed]` in
`artifacts/refinement-qa.md`.

R10 — behaviour combinations introduced by this item: `add` with both sides (AC1), with either
side empty (AC4), with duplicate text (AC3), with non-ASCII text (AC7), with a deck-like option
(AC6) and with the wrong number of arguments (AC9); `list` with cards (AC2, AC6) and with none
(AC8); and the store resolving to `RECALL_FILE` when that is set and to `~/.recall.json` when it
is not (AC5). Deliberately unconstrained, by `refine`: any behaviour of a card side spanning
several lines — multi-line card text is in `## Out of scope` below — and the exact wording of the
confirmation line (AC1), the empty-side messages (AC4), the empty listing (AC8) and the usage
line (AC9), each of which is required to exist and to name the right thing but not to be a
particular sentence. Deliberately unconstrained, by `answer-questions`: what happens when
`RECALL_FILE` names a path that cannot be written — an implementation concern for `plan`, not a
behaviour the stakeholder asked for.

**Accepted gaps, recorded at close by `review-close`** (in full, with the reasoning, in
`artifacts/review.md` `## Accepted gaps`). None is a defect against a criterion; each is
something true of the delivered work that no criterion constrains, written here so that it
survives the item being `done`:

- The durability claim behind the write protocol — that an interrupted write leaves the previous
  document or the new one — is implemented and documented but not proven; nobody killed the
  process mid-write. It rests on `os.replace` being atomic within one filesystem, which holds
  only while the temporary file is created in the store's own directory (ADR-0004, `plan.md`
  `## Risks`).
- `tests/support.py` redirects `RECALL_FILE` but not `HOME`, so the suite cannot safely host a
  mutation of path resolution itself — verification's own AC5 mutation wrote fixtures to the
  real `~/.recall.json`, which `verify` declared and removed. WI-0002 and WI-0003 inherit this
  suite; setting `HOME` unconditionally in `run_recall` would close it.
- Two user-visible behaviours no criterion covers: `recall list` with an argument exits 2 with
  `usage: recall list`, and an unknown or missing command exits 2 with `usage: recall <add|list>`.
  Both are consistent with the flat pool and both are declared in `impl-report.md`. They are
  deliberately unconstrained, not unverified — if WI-0002 needs a different answer for `list`,
  it is one condition in `cmd_list`.
- `compileall` is the lint gate and is a compile check, so unused imports and dead code were not
  machine-checked (ADR-0003). The review found two such things and neither warranted a
  send-back: the `# noqa: E402` marker in `recall` names a linter this project does not run, and
  the store file inherits mode `0600` from `tempfile.NamedTemporaryFile` via `os.replace`.

---
title: Architecture overview
version: 6
status: current
updated: 2026-08-30T13:35:00Z
updated-by: review-close
updated-for: EP-001
---

# Architecture overview

The shape of the system as it stands with all three of its subcommands — `add`, `review` and
`delete` — built and merged [src: WI-0001] [src: WI-0002] [src: WI-0003].
Read `docs/product/vision.md` first for what the tool is for; this document is how it is put
together and where its data lives.

## The shape in one paragraph

`recall` is a single-user command-line tool, run from a terminal once a day, that keeps a deck of
flashcards in one plain-text file on the local machine and decides which of them are due
[src: ADR-0001] [src: ADR-0004]. There is no server, no database and no background process: a
command starts, reads the file, does one thing, writes the file back and exits. Every piece of
state the product has is in that file.

## How it is run

The tool is Python 3, standard library only, and is run from a checkout without an installation
step [src: ADR-0006]:

```
python3 -m recall <subcommand> [arguments]
```

The subcommands are the product's three actions, one work item each: `add` (WI-0001), `review`
(WI-0002) and `delete` (WI-0003). All three are built and merged [src: recall/cli.py]
[src: WI-0003].

`review` takes no arguments. It offers every card whose due date is today or earlier, earliest
first with ties in card-file order, prints how many there are before the first one, reveals a
card's back only when the person presses Enter, takes `y` or `n` as the outcome, and writes that
card's new rung and due date to the card file before the next card is printed. `q` at either
prompt, and the end of the input stream, stop the session without losing an answer already given
[src: recall/cli.py] [src: WI-0002 AC4] [src: WI-0002 AC9] [src: WI-0002 AC12]
[src: tracker/items/WI-0002/artifacts/verify-report.md].

`delete` takes one argument, the front side of the card to remove, typed exactly as it was
entered — there is no listing command and no card number [src: ADR-0005] [src: recall/cli.py].
It prints the card it is about to remove, with both sides, the rung it has reached and the date
it is next due, and removes it only on `y`; `n`, an unrecognised answer followed by `n`, and the
end of the input stream all leave the card file byte-identical and exit `0`, because declining is
an ordinary outcome and not an error [src: ADR-0005] [src: WI-0003 AC2] [src: WI-0003 AC7]. A
front side matching no card removes nothing and exits non-zero; a front matching several cards —
which is possible, because two cards may share a front — lists every match numbered from 1 in
card-file order and removes exactly the one chosen [src: ADR-0005] [src: WI-0003 AC5]
[src: WI-0003 AC6] [src: tracker/items/WI-0003/artifacts/verify-report.md]. Deletion is permanent:
there is no undo, no trash and no way to skip the prompt, which is the stakeholder's decision
rather than the team's [src: ADR-0005] [src: WI-0003/Q-002].

A subcommand exits `0` when it did what was asked, and non-zero when it did not — including when
it refused the input, which WI-0001's AC7 requires of an empty side [src: WI-0001 AC7].
Confirmations go to standard output; warnings and refusals go to standard error.

## Where the cards live

**The card file is `$XDG_DATA_HOME/recall/cards.txt` when `XDG_DATA_HOME` is set in the
environment to a non-empty value, and `~/.local/share/recall/cards.txt` otherwise.** Setting
`RECALL_CARD_FILE` to a non-empty path overrides both and the tool uses that path exactly. A
variable that is set but empty counts as unset [src: ADR-0008] [src: recall/store.py]. The
directory and the file are created on first use [src: ADR-0008].

That sentence is the statement WI-0001's AC5 requires the documentation to make
[src: WI-0001 AC5].

## What the card file looks like

UTF-8 text, one card per block of four labelled lines, blocks separated by a blank line, after a
header of `#` lines that the tool writes and ignores on reading [src: ADR-0007]:

```
# recall cards - written by `python3 -m recall`; the tool rewrites this file
# one card per block: front, back, rung, due

front: bonjour
back: hello
rung: 0
due: 2026-08-30

front: chat
back: cat
rung: 2
due: 2026-09-02
```

- `front` and `back` are the two sides, one line of text each. A value is everything after the
  first `: ` to the end of the line, verbatim — nothing is escaped, quoted or trimmed, which is
  what makes a side read back exactly as it was typed [src: ADR-0007] [src: WI-0001 AC2].
- `rung` is where the card sits on the fixed 1/3/7/30-day ladder: `0` for a card that has never
  been answered, `1` to `4` for the four intervals [src: ADR-0002] [src: ADR-0007].
- `due` is the local calendar date the card next comes up, `YYYY-MM-DD`. A card is due when that
  date is today or earlier [src: ADR-0002].

The file is the tool's to write: hand-editing is not supported, and every save rewrites the whole
file through a temporary file and a rename, so an interrupted run leaves the previous file intact
[src: ADR-0004] [src: ADR-0008].

## The pieces

The repository root holds the package, so a checkout runs with no path setup
[src: recall/__init__.py]:

```
recall/          the tool
tests/           the tests, discovered from the repository root
docs/            this document, the vision, and the ADRs
tracker/         the work record
```

The tool is three modules with two seams, and later items are expected to add subcommands rather
than reshape it [src: WI-0001] [src: ADR-0009]:

- **the command layer** (`recall/cli.py`) — parses arguments, decides what was asked, runs the
  conversation with the person, prints what happened, and chooses the exit code
  [src: recall/cli.py];
- **the schedule** (`recall/schedule.py`) — whether a card is due on a given date, which due cards
  a session offers and in what order, and what a card's rung and due date become after a right or
  a wrong answer. Pure functions: no file, no environment, no printing, and the day is passed in
  by the caller [src: ADR-0009] [src: recall/schedule.py]. WI-0002 is the item that put it in
  [src: WI-0002];
- **the store** (`recall/store.py`) — resolves the card file's path, reads the whole file into a
  list of cards, and writes a list of cards back atomically. It has no append and no remove:
  `load` and `save` are the only two operations it offers above the format, and the command layer
  is what appends (`add`) or removes (`delete`) an entry in the list between the two
  [src: recall/store.py] [src: recall/cli.py] [src: ADR-0007] [src: ADR-0008].

The rule the schedule holds is `ADR-0002`'s and is not the schedule's to change: the ladder, the
two outcomes and the due comparison were decided with the stakeholder, and this module only
applies them [src: ADR-0002].

## How it is checked

`tracker/project.yaml` names the two commands every gate in the pipeline runs
[src: ADR-0006]:

| what | command |
|------|---------|
| tests | `python3 -m unittest discover -s tests -t . -q` |
| lint | `python3 -m compileall -q recall tests` |

The lint command checks that every module compiles and nothing more — `ADR-0006` records why the
project has no third-party linter and what that leaves uncaught [src: ADR-0006]. Most tests drive
the command-line entry point against a card file in a temporary directory, using
`RECALL_CARD_FILE`; `tests/test_schedule.py` calls the ladder's functions directly and opens no
file at all [src: tests/test_schedule.py].

**No test run touches a real deck**, and it is worth saying how, because the tests do not all do
it the same way. The three subprocess suites clear `XDG_DATA_HOME` from the child's environment
and point `RECALL_CARD_FILE` at a file inside a per-test temporary directory
[src: tests/test_add.py] [src: tests/test_review.py] [src: tests/test_delete.py]. The two tests
of the **default** path cannot do that, because the thing they check is what happens when there
is no override: they unset `RECALL_CARD_FILE` and redirect the resolution instead — one sets
`XDG_DATA_HOME` to a directory under the temporary one, the other clears it and sets `HOME` there
[src: tests/test_add.py]. So the deck they write is still inside the temporary directory, by a
different route [src: ADR-0008]. `tests/test_store.py` sets the same variables in-process to
check `card_file_path()`'s return value and writes nothing [src: tests/test_store.py].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 6 | 2026-08-30T13:35:00Z | review-close | EP-001 | DE6 at the engagement's ending — the claims audit over the whole document set, not one item's diff. `## How it is checked` said *"every test that runs the tool sets `RECALL_CARD_FILE` to a path inside a temporary directory and clears `XDG_DATA_HOME` from the child's environment"*. Two tests falsify it: `test_default_path_is_the_documented_one` and `test_default_path_without_a_data_directory_is_under_home` both run the tool with `RECALL_CARD_FILE` **unset**, and the first **sets** `XDG_DATA_HOME` rather than clearing it — which is the only way to check the default path at all [src: tests/test_add.py]. The property the sentence was reaching for is true and is now stated with the two routes distinguished, and `tests/test_add.py` — the file that falsifies the old sentence and was the one file the old citations omitted — is now cited. |
| 5 | 2026-08-30T13:26:00Z | review-close | WI-0003 | D7 and D12 at WI-0003's close. Two things were false. The document said `delete` was *"not yet started"* and *"named here so a reader can see where it will attach"*, which the merge makes untrue; `## How it is run` now describes what `delete` actually does, as `review` already had. And the store bullet claimed `recall/store.py` *"appends or removes"*, which reading the module refutes — it offers `load` and `save` and nothing else, and the appending and removing both happen in `recall/cli.py`. That sentence had been wrong since v1, when only `add` existed, and no gate could have caught it: `lint-claims` proves a citation resolves, not that it supports the sentence. `## How it is checked` also now says how the tests keep off a real deck, and cites `tests/test_delete.py`. |
| 4 | 2026-08-30T12:51:14Z | review-close | WI-0002 | D7 and D12 at WI-0002's close. Three sentences had been overtaken by what was built: the document dated itself to before any code existed, `review` was described as planned, and the schedule module as one WI-0002 *would* put in. `## How it is run` now describes what `review` actually does; the schedule bullet's purity claim cites the module as well as the decision; and `## How it is checked` says that `tests/test_schedule.py` opens no file, which the old sentence's "tests drive the command-line entry point" did not cover. |
| 3 | 2026-08-30T12:27:21Z | plan | WI-0002 | `## The pieces` gains the third module: the ladder rule lives in `recall/schedule.py`, which is the decision `ADR-0009` records and which v1 of this document deferred to WI-0002. `review` is now a planned subcommand rather than a named one. |
| 2 | 2026-08-30T12:13:31Z | review-close | WI-0001 | `## Where the cards live` corrected at review: both environment variables are read as set-and-non-empty, not merely set, matching `card_file_path()` and `ADR-0008` v3's errata. |
| 1 | 2026-08-30T11:55:01Z | plan | WI-0001 | First version, written while planning WI-0001: the command surface, the card file's documented location and format, the two modules and the seam between them, and the project's test and lint commands. |

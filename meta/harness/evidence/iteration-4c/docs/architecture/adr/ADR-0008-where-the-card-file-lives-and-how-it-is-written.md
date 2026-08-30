---
title: Where the card file lives, and how it is written
version: 3
status: current
updated: 2026-08-30T12:14:13Z
updated-by: review-close
updated-for: WI-0001
---

# ADR-0008 — Where the card file lives, and how it is written

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

The stakeholder's requirement on storage was one sentence: the card data *"needs to live in a
file on my machine that survives a reboot."* [src: EP-001/Q-004] WI-0001 turned that into two
criteria this decision has to satisfy: the file is at a path stated in the project's
documentation [src: WI-0001 AC5], and a card added before the machine restarts is in it
afterwards [src: WI-0001 AC2]. A third criterion constrains the writing rather than the location:
a refused `add` leaves the file byte-identical to what it was, or still absent if it was absent
[src: WI-0001 AC7]. A fourth requires the first ever `add` to create the file rather than fail
[src: WI-0001 AC8].

`ADR-0007` fixed what goes in the file [src: ADR-0007]. What is left is where it is, and what
happens at the moment of saving — which is the only moment at which the study history the whole
product rests on can be lost.

There is one more constraint, and it comes from the tests rather than the product: the acceptance
criteria are checked by running the tool, and a test run must not read or write the person's real
cards. Something has to make the location redirectable, or the tests and the product cannot both
be honest.

## Options considered

On **location**:

- **A — A file in the current working directory**, e.g. `./cards.txt`. Cost: none. Risk: the
  person's cards depend on which directory they happened to be in, which for a tool run once a
  day from wherever the terminal is sitting means quietly having several decks and noticing
  months later [src: EP-001/Q-001].
- **B — A path under the user's data directory**: `$XDG_DATA_HOME/recall/cards.txt`, falling back
  to `~/.local/share/recall/cards.txt`. Cost: the tool creates the directory on first use. Risk:
  a person who wants their cards somewhere else — in a synced folder, say — has no way to say so
  unless an override exists.
- **C — A fixed dotfile in the home directory**, `~/.recall-cards.txt`. Cost: none. Risk: the
  same as B without the convention, and nowhere to put a second file if one is ever needed.

On **how the file is saved**:

- **D — Write the file in place**, truncating and rewriting it. Cost: none. Risk: a process that
  dies between the truncate and the last line leaves a file holding some of the person's cards
  and none of the rest. The failure is rare and total, and it destroys exactly the thing the
  product promises to keep [src: EP-001/Q-004].
- **E — Write a temporary file beside it and rename over the original.** Cost: a few lines, and a
  moment where two files exist. Risk: essentially none on a local filesystem; the rename is
  atomic, so a reader sees either the old file or the new one.

## Decision

**The card file is `$XDG_DATA_HOME/recall/cards.txt` when `XDG_DATA_HOME` is set to a
non-empty value, and `~/.local/share/recall/cards.txt` otherwise** — option B, resolved by
`card_file_path()` [src: recall/store.py]. A variable that is set but empty falls back to the
default, which is what the XDG Base Directory Specification asks for. The path is stated in
`docs/architecture/overview.md`, which is the documentation WI-0001's AC5 requires it to be
stated in [src: WI-0001 AC5].

**Setting the environment variable `RECALL_CARD_FILE` to a non-empty value overrides that
path**, and the tool then uses exactly the path given [src: WI-0001 AC5]
[src: recall/store.py]. Set but empty is treated as unset, as for `XDG_DATA_HOME` above. This is what lets a test run against a temporary directory without
touching the person's cards, and it is also the answer for a person who wants their deck in a
synced folder. It is a documented part of the tool's interface, not a test hook.

**The containing directory is created if it does not exist**, and so is the file, on the first
`add` — which is what WI-0001's AC8 asks for [src: WI-0001 AC8].

**Every save writes a temporary file in the same directory, flushes it to disk, and renames it
over the card file** — option E — and the directory entry is flushed too. Two properties follow,
and they are the ones the criteria ask for: a card that `add` reported as added is on disk before
the command exits, so it is there after a reboot [src: WI-0001 AC2]; and a run that fails part
way through has written nothing over the existing file [src: WI-0001 AC7].

**The whole file is rewritten on every save.** `ADR-0004` already gives the tool the file to
rewrite as it pleases [src: ADR-0004], and rewriting is what makes option E possible at all. At
one person's vocabulary deck the cost of rewriting is not observable, and no criterion on any item
bounds the time an `add` may take.

## Consequences

Easy: the person has one deck wherever they run the tool from, and can point it somewhere else
with one environment variable. Tests can drive the real command-line entry point against a
temporary file, so the evidence for the acceptance criteria is the tool itself rather than an
internal function [src: WI-0001 AC1].

Hard: an override read from the environment is a way to be surprised — a variable left set in a
shell profile sends the day's review to the wrong deck, and the tool has no way to tell that from
an intention. Nothing in this item shows the person which file is in use; if that becomes a real
confusion, printing the path is a small change and a new criterion.

Reversibility: **cheap.** The location is resolved in one function and no stored data depends on
it; moving the default is a change to that function plus a line of documentation, and the person
moves their file. The write discipline is likewise one function. Neither is a change to the file's
contents, which is the expensive kind [src: ADR-0007].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 3 | 2026-08-30T12:14:13Z | review-close | WI-0001 | Erratum: `RECALL_CARD_FILE` overrides the default only when it is set to a non-empty value. See `## Corrections`. |
| 2 | 2026-08-30T12:13:31Z | review-close | WI-0001 | Erratum: `XDG_DATA_HOME` selects the data-directory path only when it is set to a non-empty value. See `## Corrections`. |
| 1 | 2026-08-30T11:55:01Z | plan | WI-0001 | First version: the card file's default location under the user's data directory, the `RECALL_CARD_FILE` override, directory and file created on first use, and every save written through a temporary file and a rename. |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-08-30T12:13:31Z | review-close | WI-0001 | erratum | `## Decision` clause 1 said *"The card file is `$XDG_DATA_HOME/recall/cards.txt` when `XDG_DATA_HOME` is set, and `~/.local/share/recall/cards.txt` otherwise"*. False for a variable set to an empty value: [src: run: cwd=/tmp/xdgprobe, XDG_DATA_HOME= HOME=/tmp/xdgprobe/home python3 -m recall add bonjour hello -> exit 0, wrote /tmp/xdgprobe/home/.local/share/recall/cards.txt]. The clause now says set to a non-empty value, which is what `card_file_path()` tests [src: recall/store.py]. |
| 2026-08-30T12:14:13Z | review-close | WI-0001 | erratum | `## Decision` clause 2 said *"Setting the environment variable `RECALL_CARD_FILE` overrides that path"*. False for an empty value: [src: run: RECALL_CARD_FILE= XDG_DATA_HOME=/tmp/xdgprobe/home2/data python3 -m recall add chat cat -> exit 0, wrote /tmp/xdgprobe/home2/data/recall/cards.txt]. The clause now says a non-empty value [src: recall/store.py]. |

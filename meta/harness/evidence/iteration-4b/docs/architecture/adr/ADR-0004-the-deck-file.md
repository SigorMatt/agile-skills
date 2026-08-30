---
title: The deck is one JSON file under the user's home directory, written atomically and never repaired
version: 2
status: current
updated: 2026-08-30T06:01:20Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0004 — The deck is one JSON file under the user's home directory, written atomically and never repaired

- **Status:** accepted
- **Date:** 2026-08-30
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

The stakeholder constrained the medium and deferred everything else about it: *"Storage should
just be a file on my machine that survives a reboot"* [src: EP-001/Q-001]. Refinement read that
as a standing deferral over format and path and routed both here rather than back to them
[src: tracker/items/WI-0001/artifacts/refinement-qa.md].

What the file has to satisfy:

- AC7 — exactly one file, path documented, under the user's home directory, not under any
  directory the operating system clears at boot [src: WI-0001 AC7].
- AC8 — when it is present but unreadable, both subcommands refuse, name the file, exit non-zero,
  and leave its bytes identical [src: WI-0001 AC8].
- AC5 — when it is absent, the first `add` creates it and its parent directory [src: WI-0001 AC5].
- It must already carry what scheduling will need — a ladder position and a next-review date, and
  no ease factor — even though nothing in WI-0001 reads those back [src: ADR-0002; WI-0001].

And one thing the stakeholder said that is not a criterion anywhere, and is the reason half the
decisions below go the conservative way: *"don't lose my progress — that's the one thing that
would make this a failure"* [src: EP-001/Q-001].

## Options considered

- **A — One JSON file.** Cost: the whole deck is read and rewritten on every change, which is
  irrelevant at the scale of one person's vocabulary deck. Risk: a partial write corrupts
  everything, which is why the atomic-write clause below is part of the decision and not an
  implementation detail.
- **B — SQLite.** Cost: a schema and a migration story from the first change onwards. Risk: AC8's
  "bytes identical before and after" is awkward to reason about against a database that may
  rewrite its own journal on open, and the stakeholder asked for *a file*, which a person can
  copy and read.
- **C — Line-oriented text or CSV.** Cost: appending is cheap and no rewrite is needed. Risk: the
  per-card fields are structured — a rung, a date, two free-text sides that may contain commas,
  quotes and newlines — and hand-rolling that escaping is exactly the kind of thing that loses
  someone's progress.
- **Path — `~/.local/share/recall/deck.json` versus `~/.recall/deck.json`.** The first follows
  the convention most tools on this platform use for data they own; the second is shorter to
  type in the documentation AC7 requires. Either satisfies AC7.
- **Honouring `$XDG_DATA_HOME` when it is set.** Rejected, and the reason is scope, not taste:
  WI-0001's `## Out of scope` excludes "choosing where the deck file lives — a flag, an
  environment variable, or a config file" [src: WI-0001]. An environment variable that relocates
  the deck is exactly that.

## Decision

**A**, at `~/.local/share/recall/deck.json`.

1. **The path is `Path.home() / ".local" / "share" / "recall" / "deck.json"`**, derived from the
   home directory and from nothing else — no flag, no environment variable of the tool's own, no
   config file [src: WI-0001; WI-0001 AC7]. It is therefore under the user's home directory and outside `/tmp`, `/var/tmp`
   and `$TMPDIR`, which is what AC7 asks for. Tests redirect it by setting `HOME` in the child
   process's environment, which is a property of `Path.home()` rather than an interface the tool
   offers.
2. **The format is JSON**, one object:
   `{"version": 1, "cards": [ {"question": str, "answer": str, "rung": int, "due": "YYYY-MM-DD"} ]}`.
   `cards` is an ordered array and its order is the order cards were added; `recall list` prints
   them in that order. `rung` is the index into `ADR-0002`'s ladder and `due` is an ISO date;
   both are written by `add` (`rung: 0`, `due` = today) and neither is read by anything in
   WI-0001.
3. **`version` is present from the first write**, so a later format change is a migration rather
   than an archaeology problem.
4. **Every write is atomic**: serialise to a temporary file in the same directory, then
   `os.replace()` it over the deck. `os.replace` is atomic within a filesystem, so an interrupted
   write leaves the previous deck intact rather than a truncated one. This is not an
   optimisation; it is the mechanism by which "don't lose my progress" survives a crash.
5. **A deck that cannot be read is never repaired and never overwritten.** Unreadable means: the
   file exists and is not valid JSON, or is valid JSON that is not an object with a `cards` array.
   In that case both subcommands report the path on standard error and exit non-zero, and neither
   writes anything. This is the one decision most likely to be quietly reversed by an
   implementation taking a shortcut, because the easy way to satisfy AC5 is to treat "cannot
   read" as "not there".
6. **Absent is not the same as unreadable.** A missing file, and a missing parent directory, mean
   an empty deck: `list` says the deck is empty and exits 0, and `add` creates the directory and
   the file.

## Consequences

- A person can open the deck in any text editor and read it, copy it, or put it in a backup
  [src: EP-001/Q-001]. That
  is what "just a file on my machine" buys, and it is why B was rejected despite being the more
  conventional engineering answer.
- **The fixed location is now the stakeholder's decision as well as this one.** Decision 1 and the
  rejection of `$XDG_DATA_HOME` above were `plan`'s, taken under WI-0001's `## Out of scope`
  rather than from anything the stakeholder had said about a path. At the ending of EP-001 they
  were told plainly that the deck cannot be relocated — no flag, no environment variable, no
  configuration file — and asked whether their acceptance of the engagement survived the
  correction. It did, in their words: *"I never planned to move the deck, a fixed file under my
  home directory is exactly what I asked for."* [src: EP-001/Q-005] They were also offered the
  chance to record relocation as a want for later and declined it. So a future change that makes
  the path configurable is not merely reversing an architectural preference; it is reversing
  something the stakeholder has been asked about directly and settled.
- The whole deck is held in memory and rewritten on every add. At one person's vocabulary deck
  this is unmeasurable; at a hundred thousand cards it would not be. Nothing in this epic goes
  near that.
- Cards have no stable identifier — a card is identified by its position in the array. WI-0004
  has to name a card in order to delete one, and if it chooses a stable id over a position, that
  is a format change and the `version` field is what makes it a migration. This is recorded here
  rather than decided, because it is WI-0004's decision and its refinement has not happened.
- Redirecting the deck for a test means setting `HOME`, which redirects everything else that
  reads the home directory too. That is acceptable in a subprocess and would not be inside the
  test process; the plan's test helper runs the CLI as a subprocess for that reason.
- **Reversibility: high for format and path, moderate for the schema.** Changing the path is one
  constant. Changing JSON for something else is one module, `recall/store.py`, and no caller
  outside it knows the format. Changing the *schema* once a person has a real deck means writing
  a migration, which is what `version` is for — so the cost is bounded but it is not free.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-30T06:01:20Z | answer-questions | EP-001 | The stakeholder's answer to `EP-001/Q-005` propagated: the fixed, non-relocatable location — until now `plan`'s call under WI-0001's out-of-scope list — is recorded in `## Consequences` as theirs too, in their own words, having been put to them at the engagement's ending. No decision changed |
| 1 | 2026-08-30T01:49:41Z | plan | WI-0001 | First version: JSON at ~/.local/share/recall/deck.json, atomic writes, and refuse-do-not-repair |

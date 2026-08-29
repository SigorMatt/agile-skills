---
title: Store the cards in one JSON file at ~/.recall.json, overridable by RECALL_FILE
version: 1
status: current
updated: 2026-08-29T11:03:23Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0002 — Store the cards in one JSON file at `~/.recall.json`, overridable by `RECALL_FILE`

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** answer-questions (architect), for WI-0001
- **Supersedes:** —

## Context

`WI-0001` AC5 requires that the cards live in a file a person can open and read, and that its
location is stated in the project's documentation [src: WI-0001 AC5]. It does not say **which**
file, and `refine` judged that a question about where the user's data lives — and how it could
appear to be lost — belonged to the stakeholder rather than to a skill, so it filed
`WI-0001/Q-002` with three options: a path under `~/.local/share/`, a plainly-named file in the
home directory, or a file in the current working directory [src: WI-0001/Q-002].

The stakeholder did not choose. They replied: *"Whatever you think is best, you know this better
than I do."* [src: WI-0001/Q-002] That is a deferral that authorises a decision rather than
withholding one, so under `spec/question.md` §2 move 1 the architect decides it and the question
is answered citing the deferral as its basis. This ADR is that decision.

Three things constrain it, and all three are already on the record:

- The stakeholder asked for **one flat pool** of cards — *"One flat pool. It's just vocab, one
  pile is fine."* [src: EP-001/Q-004]. A store whose location depends on the working directory
  would produce several pools by accident, which is the thing they said they did not want.
- AC5 exists so that the user **can** open the file [src: WI-0001 AC5]. A location that is
  awkward to reach by hand satisfies the letter of AC5 and defeats its purpose.
- Every acceptance criterion on `WI-0001`, `WI-0002` and `WI-0003` is decided by running a
  command and reading its output [src: EP-001/Q-001]. Verification therefore has to run `recall
  add` and `recall review` repeatedly, and it must be able to do that without writing into
  whatever home directory the checker happens to have.

The file's **format** was listed in `WI-0001` `## Notes` as a design question left open for
`plan` [src: WI-0001]. It is settled here rather than there because both options the stakeholder
was shown named a `.json` file, so leaving it open would leave the record saying two different
things about the same path.

## Options considered

- **A — `~/.local/share/recall/cards.json`, honouring `XDG_DATA_HOME`.** Cost: the path is long
  to type and two directories deep, so the user who wants to look inside their own cards has to
  be told where to look every time. Risk: low; it is the conventional place on Linux for a
  program's own data, and it is what a user familiar with other tools would expect.
- **B — `~/.recall.json`.** Cost: one dotfile in the home directory, which is untidy by modern
  convention. Risk: low. It is the option the user can open with `cat ~/.recall.json` without
  being reminded of anything, which is what AC5 is for [src: WI-0001 AC5].
- **C — `./cards.json` in the current working directory.** Cost: cards go missing — a user who
  adds cards in one directory and runs `recall` from another sees an empty pile with no way to
  tell that their cards are safe elsewhere. Risk: high, and it contradicts the single flat pool
  the stakeholder asked for [src: EP-001/Q-004].
- **On the format: a single JSON document** versus a line-oriented format such as TSV or JSONL.
  Cost of JSON: card text containing a quote or a backslash is escaped in the file, so what the
  user reads is not always byte-identical to what they typed, even though what `recall list`
  prints is [src: WI-0001 AC2]. Cost of a line-oriented format: it forbids multi-line card text
  structurally rather than by decision, and `WI-0001` excludes multi-line text by decision
  already [src: WI-0001].

## Decision

The card store is **one JSON file**, and its location is resolved in this order:

1. If the environment variable `RECALL_FILE` is set and non-empty, that is the store's path,
   used exactly as given.
2. Otherwise the store is `~/.recall.json` — the file `.recall.json` in the invoking user's home
   directory.

Option B, with C rejected outright.

- The path does **not** depend on the working directory. Running `recall` from anywhere reaches
  the same pile [src: EP-001/Q-004].
- `RECALL_FILE` is part of the decision, not a convenience. It is what lets the acceptance
  criteria of this epic be checked by running commands against a scratch file instead of the
  checker's real home directory, and it keeps option A and option C reachable for anyone who
  wants them without another decision now.
- The file is a JSON document, written pretty-printed with one card per object and a newline at
  the end, so that opening it in an editor shows something a person can read [src: WI-0001 AC5].
  Its exact schema is `plan`'s to fix.
- The location and the override are to be stated in the project's own documentation, which is
  what AC5 requires of the delivered work [src: WI-0001 AC5].

What is **not** decided here, and stays with `plan`: the schema inside the file, how a write is
made safe against an interruption part-way through, and whether the file is created eagerly or
on the first add [src: WI-0001].

## Consequences

What becomes easy: `WI-0001` AC5 becomes checkable — a named path, and a documented override.
Verification of every criterion in `EP-001` can run against a temporary store by setting one
environment variable, with nothing to clean up in a real home directory. The user can read their
own cards with `cat ~/.recall.json`.

What becomes hard: the home directory gains a dotfile, which is against the convention option A
follows. There is exactly one pile per user account, and a second unrelated pile is only
reachable by setting `RECALL_FILE` per invocation — there is no named-store feature and this
decision does not add one.

**Reversibility: high.** The store's location is resolved in one place, and moving it to option
A's path is a change to that resolution plus this document and the delivered documentation; a
user's existing file moves with `mv`. Nothing in the stored data depends on where the file sits.
Reversing the *format* is the more expensive half — a stored file would need converting — but no
card has been stored yet, so today that cost is zero.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T11:03:23Z | answer-questions | WI-0001 | First version: the store's location, the `RECALL_FILE` override and the JSON format, decided under the stakeholder's deferral on WI-0001/Q-002 |

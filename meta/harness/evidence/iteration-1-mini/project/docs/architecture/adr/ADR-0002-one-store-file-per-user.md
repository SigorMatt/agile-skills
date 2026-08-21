---
title: One ledger in one fixed per-user file, created on first use
version: 1
status: current
updated: 2026-08-21T02:26:40Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0002 — One ledger in one fixed per-user file, created on first use

- **Status:** accepted
- **Date:** 2026-08-21
- **Decided by:** answer-questions (architect), for EP-001
- **Supersedes:** —

## Context

Two answered questions converge on one storage decision, and answering either without the other
would leave the dangerous combination open.

- `EP-001/Q-003` asked whether this is one ledger or several separate groups. The stakeholder:
  *"One group — just me and my friends, no second group I need this for."* That selects the
  question's option **A**, one fixed store, and rejects option **B** (one ledger per directory).
- `WI-0001/Q-002` asked whether the store is created silently on first use or by an explicit
  initialise step, and what happens to a store that cannot be parsed. The stakeholder: *"Just
  create it automatically the first time, I don't want an extra setup step. If the file's broken,
  tell me rather than quietly starting over with nothing."* That selects that question's option
  **A**.

`WI-0001/Q-002` recorded that its recommendation was conditional: create-silently is only safe
*because* Q-003 came back as one fixed store. Per-directory storage plus silent creation is the
combination that starts an empty ledger when you `cd` to the wrong place, and with Q-003
answered "one group" that trap does not exist. The two answers are consistent, and this ADR is
where the pairing is written down so a later reader does not have to rediscover it.

Still undecided by the stakeholder's words, and therefore decided here: **where** the fixed file
lives. `tracker/items/WI-0001/item.md` notes explicitly that this is open. It matters to WI-0001,
WI-0002 and WI-0003, all of which read the same store, and to every acceptance criterion of the
form "exit the process, run again, the data is still there".

## Options considered

- **A — A fixed path under the user's home directory.**
  `$XDG_DATA_HOME/expenses/store.json`, falling back to `~/.local/share/expenses/store.json`.
  Cost: a test needs a way to point the tool somewhere else, or it writes to the real home
  directory of whoever runs the suite.
  Risk: low. The ledger is where it is regardless of what directory you run from, which is what
  "one group" means in practice.
- **B — A fixed path in the current working directory.**
  `./expenses.json`.
  Cost: none.
  Risk: this is exactly option **B** of `EP-001/Q-003`, which the stakeholder declined. Running
  from the wrong directory silently starts an empty ledger — silent data loss in a tool whose
  entire value is remembering things.
- **C — A path given on every command.**
  Cost: an argument on every invocation, forever.
  Risk: contradicts "I don't want an extra setup step" from `WI-0001/Q-002`, and re-introduces
  per-invocation ambiguity about which ledger you are talking to.

## Decision

1. **Location.** The store is a single file at `$XDG_DATA_HOME/expenses/store.json`, or
   `~/.local/share/expenses/store.json` when `XDG_DATA_HOME` is unset or empty. There is exactly
   one, for the user running the tool, regardless of the working directory.
2. **Override.** If the environment variable `EXPENSES_STORE` is set and non-empty, it is the
   path of the store instead. This exists so that automated tests can exercise a real store
   without touching the developer's own, and as an escape hatch for anyone who needs one. It is
   **not** a groups feature: the tool still knows about exactly one ledger per invocation, there
   is no group concept in the data model, and the help text should not present it as a way to
   keep several friend groups apart.
3. **Format.** JSON, written with the standard library's `json` module (see
   `ADR-0001-python-baseline-and-no-dependencies.md`), so a human can read and repair the file.
4. **Creation.** Nothing is created by merely reading. The first command that *writes* creates
   the parent directories and the file. There is no `init` command and no setup step.
5. **A missing store reads as an empty group.** Commands that only read succeed and report
   emptiness — this is what `WI-0001` AC4 and `WI-0003` AC4 require.
6. **A damaged store is fatal and non-destructive.** If the file exists but cannot be read or
   parsed, **every** command — reading or writing — prints an error naming the path and what was
   wrong with it, exits non-zero, and writes nothing. The original bytes stay on disk to be
   rescued. In particular, a write MUST NOT proceed on the assumption that an unparseable store
   was empty.
7. **Writes are atomic.** A write goes to a temporary file in the same directory and is then
   renamed over the store, so an interrupted run cannot produce the damaged file rule 6 has to
   report.

## Consequences

- Easy: "add three people, exit, run again, the same people are listed" is true from any
  directory, which is what EP-001's first success measure asks for.
- Easy: acceptance criteria about the empty case and the damaged case are both testable, by
  pointing `EXPENSES_STORE` at a temporary directory.
- Hard: keeping two friend groups apart. That is deliberate — the stakeholder said there is no
  second group — but if one ever appears, `EXPENSES_STORE` is a manual workaround rather than a
  feature, and a real answer would mean revisiting `EP-001/Q-003`.
- Hard: rule 6 means a corrupt store bricks every command until the user fixes or deletes the
  file. That is the behaviour the stakeholder asked for in preference to silent data loss, and
  the error message must therefore say what to do about it.
- **Reversibility: moderate.** The path and the format are behind whatever module owns the store,
  so changing either is a contained change plus a migration for anyone with an existing file.
  Rule 6 is cheap to reverse. Introducing multiple groups later is the expensive change, because
  it alters the shape of the stored data and every command's arguments — that cost is the reason
  `EP-001/Q-003` was asked before anything was built rather than after.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-21T02:26:40Z | answer-questions | EP-001 | First version, deciding EP-001/Q-003 and the storage half of WI-0001/Q-002 |

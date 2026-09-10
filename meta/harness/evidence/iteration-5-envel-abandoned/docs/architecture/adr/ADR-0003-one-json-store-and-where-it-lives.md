---
title: One JSON store, at a path the environment can override
version: 1
status: current
updated: 2026-09-10T13:44:29Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — One JSON store, at a path the environment can override

- **Status:** accepted
- **Date:** 2026-09-10
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

Two things forced this decision, and refinement routed both here rather than to the stakeholder
because the answer would be the same whoever they were [src: WI-0001].

**Where the data lives.** The stakeholder's requirement is that what they record survives between
runs [src: docs/product/vision.md]. Refinement then found a constraint the criteria impose on the
design: AC6, AC9 and AC10 all begin "before any envelope has ever been created", and AC3 needs
three separate invocations to share one store
[src: WI-0001 AC3 "each a separate invocation of the process with no other step in between"].
Neither is observable unless whoever runs them can reach a clean store without destroying a real
one.

**What format it is in.** The stakeholder forbade restricting the characters a name may contain —
"I want spaces … so don't restrict the characters" [src: WI-0001/Q-002]. That is a constraint on
the store's format rather than a rule about names: the format has to survive any name, including
one containing a quote, a newline or a tab.

## Options considered

For the format:

- **A — One name per line in a text file.** Cost: nothing to parse. Risk: a name containing a
  newline destroys the file's structure, and the stakeholder specifically refused to let us
  forbid characters. This option is eliminated by their answer rather than by taste.
- **B — A single JSON document, read and written with `json` from the standard library.**
  Cost: the whole store is loaded and rewritten on every change, which for one person's envelopes
  is a few kilobytes. Risk: none that matters at this size.
- **C — SQLite through `sqlite3`.** Cost: a schema, migrations, and a binary file nobody can read
  or repair with a text editor. Risk: disproportionate for a file that will hold tens of rows;
  and the tool's own record stops being something its one user can inspect.

For the location:

- **D — A file in the current working directory.** Cost: none to implement. Risk: the envelopes
  you see depend on where you `cd`, which for a tool typed several times a day is a way to lose
  money quietly.
- **E — A fixed path under the user's data directory, with an environment override.** Cost: two
  rules instead of one. Risk: the override is a published interface — once tests and habits use
  it, renaming it is a breaking change.

## Decision

Options B and E.

**The store is one JSON document.** Its shape at this version:

```json
{
  "version": 1,
  "envelopes": [
    {"name": "groceries"}
  ]
}
```

- `version` is the store-format version, so a later item that adds fields can tell an old file
  from a new one without guessing.
- `envelopes` is a list in creation order. It is a list of **objects** rather than of strings
  because the items that follow this one add money to an envelope, and adding a key to an object
  is a smaller change than rewriting every element.
- The file is written UTF-8 with `ensure_ascii=False`, so a name is stored as the characters the
  person typed. `json` escapes whatever needs escaping, which is what makes the format survive a
  name the stakeholder was promised we would not restrict.
- The order the list is stored in is not the order `envel list` prints: printing is sorted at
  display time [src: WI-0001 AC4 "sorted by name, ascending, byte-wise"].

**The store's path** is resolved in this order:

1. `$ENVEL_FILE`, if it is set and not empty — used as given, without expansion or
   interpretation;
2. otherwise `$XDG_DATA_HOME/envel/store.json`, if `XDG_DATA_HOME` is set and not empty;
3. otherwise `~/.local/share/envel/store.json`.

A store file that does not exist is an empty store and not an error, which is what lets
`envel list` succeed before anything has been created [src: WI-0001 AC6 "run before any envelope
has ever been created exits 0"]. Writing creates the parent directory if it is missing, and
replaces the file atomically: write a temporary file in the same directory, then `os.replace`.

## Consequences

- Every demonstration of an acceptance criterion sets `ENVEL_FILE` to a path in a temporary
  directory. That is what discharges the testability constraint refinement recorded, and it is
  why the override exists at all rather than being a convenience.
- The person's real store lives in one place regardless of where they run the command from, which
  is the behaviour a tool typed several times a day needs.
- `ENVEL_FILE` becomes a published interface. Renaming it later breaks anyone's habits and every
  test at once, so it is the part of this decision that is **not cheap to reverse**.
- The format and the layout of the JSON *are* cheap to reverse while `version` is 1 and no real
  data exists: today a store can be rewritten from scratch, and once the stakeholder has months
  of transactions in one it cannot. Whatever changes the shape after that owes a migration.
- Rewriting the whole document on every change is fine at one person's scale and would not be at
  a million transactions. Nothing in this product is heading there [src: docs/product/vision.md].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-10T13:44:29Z | plan | WI-0001 | First version: a single JSON store, its shape, and the `ENVEL_FILE` / XDG path resolution |

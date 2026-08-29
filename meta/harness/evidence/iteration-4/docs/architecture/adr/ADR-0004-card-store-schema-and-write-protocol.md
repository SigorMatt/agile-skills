---
title: The card store's JSON schema, and a replace-based write protocol
version: 1
status: current
updated: 2026-08-29T11:16:00Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0004 — The card store's JSON schema, and a replace-based write protocol

- **Status:** accepted
- **Date:** 2026-08-29
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

ADR-0002 fixed where the cards live and that the file is JSON, and left three things to this
skill by name: the schema inside the file, how a write survives an interruption part-way
through, and whether the store is created eagerly or on the first add [src: ADR-0002]. WI-0001's
notes add a fourth: what the tool does when `RECALL_FILE` names a path it cannot write
[src: WI-0001].

The constraints already on the record:

- The file is opened and read by a person, and that is the point of AC5 rather than a side
  effect [src: WI-0001 AC5].
- Card text is stored and listed byte-identical to what was typed, including non-ASCII text
  [src: WI-0001 AC2; WI-0001 AC7].
- Card numbers start at 1 and increase by 1 per card added, and two cards with identical text
  are two cards with different numbers [src: WI-0001 AC1; WI-0001 AC3].
- WI-0001 stores whatever state the later items need but decides none of it: when a card is next
  due belongs to WI-0003, not here [src: WI-0001; src: WI-0003].
- Editing and deleting cards are out of scope for the whole epic [src: WI-0001].

## Options considered

- **A — an object at the top level, with a `version` and a `cards` array.** Cost: one level of
  nesting before the reader reaches their cards. Risk: low, and it leaves a named place to put
  the scheduling fields WI-0003 will add and a number to bump when their shape changes
  [src: WI-0003].
- **B — a bare JSON array of cards.** Cost: nowhere to record the format's version, so the first
  change to the card shape has to be detected by inspecting a card. Risk: medium; WI-0003 is
  already known to be coming and is already known to add per-card state [src: WI-0003].
- **C — an object keyed by card number.** Cost: JSON object keys are strings, so the numbers are
  quoted in the file and their order is not the file's order; AC6 wants a listing in ascending
  card-number order and this shape makes that a sort over parsed strings [src: WI-0001 AC6].
  Risk: low but pointless.

On the write protocol:

- **D — write in place, truncating the existing file.** Cost: an interruption between the
  truncate and the last byte leaves the user's whole pile unreadable. Risk: high — this is the
  failure WI-0001 exists to prevent, since the item is "have it persist" [src: WI-0001].
- **E — write a temporary file beside the store, then rename it over the store.** Cost: the
  directory must be writable, not just the file, and the temporary file is briefly visible.
  Risk: low; `os.replace` is atomic within one filesystem, so a reader sees either the old
  document or the new one [src: WI-0001 AC2].

On the next card number:

- **F — derive it from the cards present: one more than the largest number stored.** Cost: if
  someone hand-deletes the last card from the file, the next card added reuses its number.
  Risk: low; nothing in the epic deletes a card [src: WI-0001].
- **G — store a separate counter field.** Cost: a second source of truth that can disagree with
  the cards after any hand edit, and a hand-editable file is exactly what AC5 asks for
  [src: WI-0001 AC5].

## Decision

Options A, E and F.

**Schema.** The store is one JSON object:

```json
{
  "version": 1,
  "cards": [
    { "number": 1, "question": "die Katze", "answer": "the cat" }
  ]
}
```

- `version` is an integer, `1` for the shape this item delivers. WI-0003 adds per-card
  scheduling fields to each card object and bumps it [src: WI-0003].
- `cards` is an array, held in ascending `number` order, which is also the order AC6 requires
  the listing to be in [src: WI-0001 AC6].
- A card object carries exactly `number`, `question` and `answer` for this item. `question` and
  `answer` hold the argument text unchanged, as strings [src: WI-0001 AC2].
- The document is written UTF-8, pretty-printed with a two-space indent, without escaping
  non-ASCII characters, and ends with a newline — so `Grüße` appears in the file as `Grüße`
  rather than as an escape sequence [src: WI-0001 AC7; ADR-0002].
- The next card number is one more than the largest `number` in `cards`, and 1 when there are
  none [src: WI-0001 AC1].

**Write protocol.** A write serialises the whole document, writes it to a temporary file in the
store's own directory, flushes it to disk, and renames it over the store. A crash therefore
leaves either the previous document or the new one, never a half-written file
[src: WI-0001 AC2].

**Creation.** The store is created by the first successful add, not eagerly. `recall list`
against a path with no file reports that there are no cards and exits 0, which is what AC8 asks
for whether or not a file has ever existed [src: WI-0001 AC8].

**When the store cannot be used.** Two cases, both reported on stderr naming the path, both
leaving what is on disk untouched:

- the path cannot be written — a missing parent directory, a permission error, a directory in
  the way. The command fails. Directories are not created on the user's behalf.
- the file exists but does not parse as JSON, or does not have the shape above. The command
  fails and does not overwrite it, because overwriting is indistinguishable from losing the
  user's cards [src: WI-0001 AC5].

The exit codes these use, and the wording, are ADR-0005's.

## Consequences

What becomes easy: the file answers "what have I got?" when opened in an editor, and every
acceptance criterion about persistence is checkable by adding a card and reading the file
[src: WI-0001 AC5]. WI-0003 has a versioned place to add scheduling state without renegotiating
the format [src: WI-0003].

What becomes hard: every write rewrites the whole document, so the cost of adding a card grows
with the size of the pile. For one person's vocabulary that is nothing; for a hundred thousand
cards it would be the first thing to change. A corrupt store stops the tool rather than
self-healing, which is deliberate and will read as harsh to anyone who hand-edits their file
into invalid JSON.

**Reversibility: high, on the schema; total, on the rest.** No card exists yet, so today
changing the shape costs a change to the reader and the writer and nothing else. Once cards are
stored, a shape change needs the `version` field this ADR introduces and a migration; that is
the cost the field exists to bound. The write protocol and the creation rule are internal and
observable only as durability, so either can be replaced without touching a criterion.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-29T11:16:00Z | plan | WI-0001 | First version: the JSON schema, the temporary-file-and-rename write protocol, creation on first add, and the two failure cases ADR-0002 left open |

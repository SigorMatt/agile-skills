---
title: A move is two entries of kind move, one per envelope, sharing one date
version: 4
status: current
updated: 2026-09-11T18:55:51Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0007 — A move is two entries of kind `move`, one per envelope, sharing one date

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0004
- **Supersedes:** —

## Context

`WI-0004` adds a command that takes an amount out of one envelope and puts it into another
[src: WI-0004 AC1 "There is an `envel` command that moves a given amount from one named envelope to"]. Two recorded facts bear on how that is stored, and they pull against the
obvious shape.

The first is `ADR-0002` [src: ADR-0002], which says an envelope's balance is the sum of `cents`
over the entries naming it. An entry names **one** envelope, in its `envelope` field, and every
balance in the tool is computed that way [src: envel/envelopes.py:63]. A move concerns two
envelopes, so either the entry grows a second envelope field and the balance has to special-case
it, or a move is more than one entry.

The second is the stakeholder's answer at `WI-0003/Q-001`, where they asked for a move to be kept
out of *spent* and shown as its own net figure per envelope per month: *"'Spent' has to mean money
that left the house, so moves don't belong in it — but I won't use a report whose rows don't add
up."* `WI-0003` turns that into a column [src: WI-0003 AC2 "The moved figure is one net number,
positive when more arrived than left"]. Whatever is stored has to let `WI-0003` tell a move from a
spend and from income, and has to let one net number per envelope per month fall out of it.

A third fact arrived with `WI-0004/Q-001`: a move carries a date the way a spend does
[src: WI-0004 AC1 "There is an `envel` command that moves a given amount from one named envelope to"]. `ADR-0006` [src: ADR-0006] already put a spend's own day in an `on` field
beside `at`, so the question is not what to call a move's date but whether the two halves of one
move can disagree about it.

## Options considered

- **A — one entry naming both envelopes**, `{"kind": "move", "from": ..., "to": ..., "cents": ...}`.
  Cost: one entry per move, and the two halves cannot drift apart. Risk: it falsifies `ADR-0002`'s
  sentence about the balance, and every reader of the file — `envel/envelopes.py`'s `balance`
  first, then `WI-0003`'s summary and `WI-0006`'s lookup — has to branch on the kind before it can
  say which envelope an entry is about and with which sign. That is a special case in the one
  function every command depends on, which is the thing `ADR-0002` was shaped to avoid.
- **B — two entries of kind `move`**, one naming the source with a negative `cents` and one naming
  the destination with a positive `cents`, both carrying the same `on` and the same `at`. Cost: a
  move writes two entries rather than one, and nothing in the file says which two belong together.
  Risk: a future reader that needs the pair — an undo, say — cannot recover it for moves already
  recorded.
- **C — two entries of distinct kinds**, `move-out` and `move-in`. Cost: the same two entries.
  Risk: two kinds where one plus a sign will do, and every consumer has to know both names; the
  sign already carries the direction, because `ADR-0002` [src: ADR-0002] makes the sign the thing
  a balance reads.

## Decision

Option B. A move appends exactly two entries to `entries`:

```json
{"kind": "move", "envelope": "groceries", "cents": -2000,
 "on": "2026-08-28", "at": "2026-09-11T05:40:00Z"}
{"kind": "move", "envelope": "fun", "cents": 2000,
 "on": "2026-08-28", "at": "2026-09-11T05:40:00Z"}
```

- **`balance` is untouched.** The sum of `cents` over the entries naming an envelope is still that
  envelope's balance, with no branch on `kind` [src: ADR-0002], which is what keeps `WI-0004` AC2
  — the source down by exactly the amount, the destination up by exactly it, nothing else changed
  — a consequence of the storage rather than a thing the code has to arrange.
- **`cents` carries the direction**, negative on the side the money left. `WI-0003`'s net figure
  for an envelope in a month is then the plain sum of `cents` over that envelope's `move` entries
  in that month — positive when more arrived than left, which is the sentence `WI-0003` AC2
  already contains.
- **`on` is the day the move is held against**, written `YYYY-MM-DD`, exactly as `ADR-0006`
  [src: ADR-0006] defines it for a spend. It is present on both entries of a move and they always
  agree, because one value is computed once and written twice.
- **`at` keeps the meaning `ADR-0002` gave it** — when the tool recorded the entry — on both
  entries, and they agree for the same reason. This ADR adds no new meaning to `at`.
- **`description` is not written on a move entry**, because `WI-0004` puts a description on a move
  out of scope [src: WI-0004].
- **The document's `format` stays `1`.** A store written before this item has no `move` entries,
  so there is nothing in it that should have carried one and does not, and a store written after
  it is readable by anything that reads format 1 and ignores kinds it does not know. There is no
  migration, which is the property `ADR-0002` was shaped to have.

**No field links the two entries to each other**, and that is deliberate rather than overlooked.
Nothing in this epic needs the pair: `WI-0003` wants a net figure per envelope, `WI-0006` lists
income, spends and moves for a month and shows each half of a move on its own line
[src: WI-0006 AC6 "A move between two envelopes appears as two lines"], and `WI-0005` corrects a
spend or an income one entry at a time [src: WI-0005]. Inventing an identifier for a relation
nothing reads would be designing past the item.

Since `ADR-0010` [src: ADR-0010] the two halves do carry **consecutive references**, which is the
nearest thing to a link the file has ever had; it is a consequence of when they are appended
rather than an assertion the file makes, and no code pairs them by it
[src: envel/summary.py].

## Consequences

Easy: the tool gains one entry kind and no field that some other kind does not already carry —
`kind`, `envelope`, `cents` and `at` come from `ADR-0002` [src: ADR-0002] and `on` from `ADR-0006`
[src: ADR-0006]. `WI-0003` gets its fourth column as a sum with a filter on `kind`, the same shape
as the other three [src: WI-0003 AC2 "The moved figure is one net number, positive when more
arrived than left"]. A person opening the file in an editor
sees two lines that obviously belong together — same amount with opposite signs, same `on`, same
`at` — even though nothing asserts it.

Hard: **a move is two rows and no field in the file says so.** Two consequences follow. The first
is that a half-written move would be incoherent — one side debited and the other not — and the
only thing preventing it is that the whole document is written at once and atomically
[src: envel/store.py]; this ADR depends on that property rather than adding one. The second is
that nothing in the tool pairs the halves [src: envel/summary.py], which is why
`WI-0004` records the reversal of a mistake as running the command again with the names swapped
[src: WI-0004] rather than as an operation. `ADR-0010`'s consecutive references
[src: ADR-0010] would make pairing possible for whoever wanted it; that is not this ADR's claim
and no item has asked for it.

A smaller cost: `entries` grows twice as fast per move as per spend. For one household this is a
file of a few thousand lines a year, and `ADR-0002` already names the entry-log shape as the thing
to revisit if this ever needs to be fast.

**Reversibility: cheap now, a data migration later.** No code in this tool writes a move entry yet
[src: run: grep -rn '"move"' envel → exit 1, no output], so today this is one function in
`envel/envelopes.py` and one branch in `envel/cli.py`. Once the stakeholder has recorded a move,
changing the shape means code that reads the old `format` and writes the new one — the same
position `ADR-0002` and `ADR-0006` are in, and the reason `format` is in the document. Adding a
pairing identifier later is the cheaper half of that: it is one field written by one function, and
it needs no migration to *read* the file, but moves recorded before the change would not carry it,
so anything that had to pair them would be able to pair only the newer ones.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 4 | 2026-09-11T18:55:51Z | answer-questions | EP-001 | One `provenance` correction, recorded below: `## Context`'s citation for *"every balance in the tool is computed that way"* moved from `envel/envelopes.py:50` to `envel/envelopes.py:63`. The assertion is unchanged and no code has to change to satisfy the new text. Answering `EP-001/Q-007`. |
| 3 | 2026-09-11T08:22:41Z | implement | WI-0006 | One erratum, recorded below: `## Consequences` said *"a move is two rows and nothing in the file says so"* and that the other half *"cannot"* be found. `ADR-0010` [src: ADR-0010] made both overstatements. Replaced with what is true — no **field** says so, and nothing in the tool pairs the halves [src: envel/summary.py]. The decision is unchanged. |
| 2 | 2026-09-11T08:22:40Z | implement | WI-0006 | One erratum, recorded below: `## Decision` said the two entries are *"not linked to each other"* and attributed to `WI-0006` and `WI-0005` scopes neither item now has. Replaced with a clause saying no **field** names the pair, naming both items' real scope, and recording `ADR-0010`'s consecutive references [src: ADR-0010]. The decision — a move is two entries with opposite `cents` and the same `on` and `at` — is unchanged, and no code has to change to satisfy the new text. |
| 1 | 2026-09-11T05:35:47Z | plan | WI-0004 | First version |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T18:55:51Z | answer-questions | EP-001 | provenance | `## Context`, second paragraph: *"An entry names **one** envelope, in its `envelope` field, and every balance in the tool is computed that way"* cited `[src: envel/envelopes.py:50]`. That was `def balance(store, name):` when this ADR was written; `WI-0006` then inserted `take_ref` above it for `ADR-0010` [src: ADR-0010], so line 50 became `store["next-ref"] = reference + 1` — the reference counter, which has nothing to do with a balance. `balance` is now at `envel/envelopes.py:63` [src: envel/envelopes.py:63] and its filtered sum at `envel/envelopes.py:65`. The citation now reads `[src: envel/envelopes.py:63]`; the assertion is unchanged, and `ADR-0002`'s own `## Corrections` row already cites `:63` for the same function. Answering `EP-001/Q-007`. |
| 2026-09-11T08:22:40Z | implement | WI-0006 | erratum | `## Decision`, last paragraph, said *"**The two entries are not linked to each other**"* and that *"`WI-0006` is scoped to the spends recorded against an envelope"* and *"`WI-0005` is scoped to correcting a spend"*. All three are false. `WI-0006` lists income, spends and moves [src: WI-0006 AC2 "its kind — income, spend, or a move in or out"], `WI-0005` corrects an income as well as a spend [src: WI-0005/Q-005], and `ADR-0010` [src: ADR-0010] gives a move's two halves consecutive references, which is information in the file about the pair. Replaced with a clause saying that no **field** names the pair, naming the two items' real scope, and stating the adjacency and that no code reads it [src: envel/summary.py]. |
| 2026-09-11T08:22:41Z | implement | WI-0006 | erratum | `## Consequences`, second paragraph, said *"a move is two rows and nothing in the file says so"* and *"anything wanting to undo a specific move cannot find its other half"*. Both overstate it since `ADR-0010` [src: ADR-0010]: consecutive references would let a reader find the other half. Replaced with *no field in the file says so* and *nothing in the tool pairs the halves* [src: envel/summary.py], which is what is true and is what `WI-0004`'s reversal-by-repeating still rests on [src: WI-0004]. |

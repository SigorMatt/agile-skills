---
title: Keep the data as one JSON document holding envelopes and a dated entry log
version: 4
status: current
updated: 2026-09-11T09:56:03Z
updated-by: implement
updated-for: WI-0005
---

# ADR-0002 — Keep the data as one JSON document holding envelopes and a dated entry log

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`WI-0001` needs the envelopes and their amounts to survive between runs [src: WI-0001 AC4 "The three commands above are run as separate invocations of the tool"], and
nothing more: three commands, a name and a number each. `refine` routed the shape of the store to
this skill rather than to the stakeholder, on the grounds that the answer would be the same
whoever they were [src: WI-0001].

The rest of the epic is what makes the choice non-obvious. The summary shows, per envelope,
*"what went in that month, what was spent, and what is left"* [src: EP-001/Q-003], over a
**calendar month** that can be named after it has ended [src: EP-001/Q-004] — so a past month's
income has to still be attributable to that month. A balance is a number; a month's income is not
derivable from it. The stakeholder is one person on one machine [src: EP-001/Q-001] who will have
real data in the file from the first week, so a shape that has to grow a date later is a
migration of their money rather than a refactor.

## Options considered

- **A — store the balance per envelope.** A JSON object mapping a name to a number of cents.
  Cost: the least code this item could need. Risk: `WI-0003` cannot be built on it at all —
  *"what went in that month"* was never recorded — so the fix is a new file format and a
  migration of the stakeholder's live data.
- **B — store the envelopes and an append-only list of dated entries**, and derive a balance by
  summing. Cost: a sum on every read, and a file that grows with use; a household budget's entry
  count is in the thousands, which is nothing. Risk: the entry list is unexercised by this item's
  own criteria — nothing in `WI-0001` observes the date — so it is carrying a field on the
  strength of a sibling item's requirement.
- **C — SQLite.** Cost: a schema, a migration story, and a binary file the stakeholder cannot
  read or repair with the editor they already have. Risk: it answers a scale problem this tool
  does not have; *"Python, no services"* [src: EP-001] argues for the most inspectable thing that
  works.

## Decision

One JSON document. Option B.

```json
{
  "format": 1,
  "envelopes": [{"name": "groceries", "created": "2026-09-11T02:34:57Z"}],
  "entries": [{"kind": "income", "envelope": "groceries", "cents": 40000,
               "at": "2026-09-11T02:34:57Z"}]
}
```

- `format` is an integer this tool checks on load, so a future change has somewhere to branch.
  That branch has since been taken: `ADR-0010` [src: ADR-0010] raises it to `2` and adds `ref` to each
  entry and `next-ref` to the document, so the worked document above is this ADR's shape and not the
  current one [src: envel/store.py].
- `envelopes` holds the name **as it was first typed** [src: WI-0001 AC12 "The listing shows an envelope's name exactly as it was typed"], which is what the
  listing shows. Two envelopes whose names differ only in capitalisation cannot both exist
  [src: WI-0001 AC11 "Envelope names are matched without regard to capitalisation"], and matching is done on the case-folded name.
- `entries` is ordered as written, and an envelope's balance is the sum of `cents` over the
  entries naming it — the second half with no branch on `kind`, which is what every figure in the
  tool rests on. `entries` was also append-only until `WI-0005` [src: WI-0005], which corrects an
  entry where it sits and removes one by deleting it [src: ADR-0011]; the ordering and the sum are
  untouched by that, and an entry's position in the list still never moves
  [src: envel/envelopes.py:451]. `WI-0001` writes only `kind: "income"`; `WI-0002` adds
  the kind for a spend, and the field exists so that it can.
- `at` is when the tool recorded the entry. `WI-0001` never reads it. It is written now because
  `WI-0003` needs it and adding it later would mean rewriting a file that has the stakeholder's
  money in it.
- Every amount in the file is a whole number of cents [src: ADR-0001].

**Writes are atomic.** The whole document is written to a temporary file in the same directory
and then moved over the target with `os.replace`, so an interrupted run leaves either the old
file or the new one and never a half-written one. This answers the second question `refine`
routed here [src: WI-0001].

**A missing file is an empty store**, not an error: that is what makes the first ever run of the
listing print that there are no envelopes and exit 0 [src: WI-0001 AC6 "Listing when no envelope has ever been created prints a line saying there are none"]. A file that exists but
cannot be read as this format — unreadable, not JSON, or a `format` this tool does not know — is
refused with a message on stderr and a non-zero exit, and **nothing is written**, so a damaged
file is never overwritten by the tool that failed to read it.

## Consequences

Easy: `WI-0002` [src: WI-0002] adds an entry kind and a field, and `WI-0003` [src: WI-0003]
filters income by `at` and a spend by the `on` that field carries [src: ADR-0006], neither needing
a format change; the file is readable and repairable in any text editor, which matters for a
person whose current tool is a spreadsheet.

Hard: the whole file is read and written on every command, so a single run is O(entries); and a
balance is a derived number rather than a stored one, which means a bug in the summation is a bug
in every command at once. The entry-log shape is also the thing to revisit if this ever needs to
be fast, which for one household it will not.

**Reversibility: cheap now, a data migration later.** While no file exists, changing the shape is
one module. Once the stakeholder has used it, any change to the document needs code that reads
the old `format` and writes the new one — which is why `format` is in the document from version
one.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 4 | 2026-09-11T09:56:03Z | implement | WI-0005 | One erratum, recorded below: the `entries` bullet said the list is *"append-only within a run"*, which `ADR-0011` [src: ADR-0011] made false — a correction edits an entry and a removal deletes one. Replaced with what is now true, keeping the two properties that did not change: the list is ordered as written and a balance is still the plain sum with no branch on `kind`. The decision — one JSON document holding envelopes and a dated entry log — is untouched, and no code has to change to satisfy the new text. |
| 3 | 2026-09-11T08:22:40Z | implement | WI-0006 | One provenance correction, recorded below: the `format` bullet now cites `ADR-0010` [src: ADR-0010], which took the branch that bullet exists for, and says that the worked document above it is this ADR's shape rather than the current one. The bullet's assertion is unchanged and the decision is untouched. |
| 2 | 2026-09-11T04:06:14Z | implement | WI-0002 | One erratum, recorded below: `## Consequences` said `WI-0003` filters by `at`, which `ADR-0006` made false while this item was being built. The decision — one JSON document holding envelopes and an append-only dated entry log — is unchanged. |
| 1 | 2026-09-11T02:34:57Z | plan | WI-0001 | First version |

## Corrections

| when | by | for | kind | what changed |
|------|----|-----|------|--------------|
| 2026-09-11T04:06:14Z | implement | WI-0002 | erratum | `## Consequences`, first sentence, said *"`WI-0002` adds an entry kind and `WI-0003` filters by `at`, neither needing a format change"*. The first half is right and the second is not: `ADR-0006` [src: ADR-0006] gives a spend its own `on` field precisely because income falls in the month it was recorded while a spend falls on its own date [src: WI-0003 AC8 "A month's money-in figure is the income"], so `WI-0003` will filter a spend by `on` and not by `at`. Replaced with a clause naming both fields and citing `ADR-0006`. The claim that neither item needs a format change survives and is true: `envel/store.py` still reads and writes `FORMAT = 1` [src: envel/store.py:11]. No code has to change to satisfy the new text, and the decision is untouched. |
| 2026-09-11T09:56:03Z | implement | WI-0005 | erratum | `## Decision`, the `entries` bullet, said *"`entries` is append-only within a run and ordered as written. An envelope's balance is the sum of `cents` over the entries naming it."* The first clause stopped being true when `WI-0005` was built: `envel/envelopes.py`'s `correct` edits an entry in place and `remove` filters it out of the list [src: ADR-0011], [src: envel/envelopes.py:451]. The other two clauses are unchanged and were re-read against the code — the entry keeps its place in the list, which `tests/test_corrections.py`'s `test_the_entry_keeps_its_place_in_the_list` asserts, and no reader branches on `kind` to compute a balance [src: envel/envelopes.py:63]. Replaced with a sentence naming what changed, what did not, and the ADR that changed it. No code has to change to satisfy the new text and the decision is untouched. |
| 2026-09-11T08:22:40Z | implement | WI-0006 | provenance | `## Decision`, the `format` bullet: *"`format` is an integer this tool checks on load, so a future change has somewhere to branch"* now cites `ADR-0010` [src: ADR-0010], which is the change that took the branch, and carries a following sentence saying that the worked document above is this ADR's shape and not the current one [src: envel/store.py]. The bullet's assertion is unchanged; the worked document is left exactly as it was, because it is the record of what was decided here. |

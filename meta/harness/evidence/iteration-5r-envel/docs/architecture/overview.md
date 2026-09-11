---
title: Architecture overview
version: 12
status: current
updated: 2026-09-11T19:17:34Z
updated-by: review-close
updated-for: EP-001
---

# Architecture overview

## The shape of it

`envel` is a program that starts, does one thing, and exits. There is no daemon, no server and
no background process; between two invocations the only thing that exists is a file
[src: docs/product/vision.md]. Every command therefore follows the same three beats:

1. **read** the whole store from disk,
2. **decide** — validate what the user typed, and compute the new state or the refusal,
3. **write** the whole store back, atomically, but only if something changed.

That shape is what makes the tool's behaviour easy to state and easy to test: a command is a
function from (store, arguments) to (new store, output, exit code).

## The parts

| module | what it owns |
|--------|--------------|
| `envel/cli.py` | the command line: parsing arguments, dispatching, printing, and the exit code |
| `envel/envelopes.py` | the operations — create, add income, list, record a spend, move money between two envelopes, correct an entry, remove one — as decisions about a store |
| `envel/summary.py` | the reports, both of them: a month's four figures per envelope, and a month's entries listed one to a line [src: ADR-0008] [src: ADR-0009] |
| `envel/store.py` | where the file is, reading it, and writing it atomically [src: ADR-0002] [src: ADR-0003] |
| `envel/money.py` | the only two places text and amounts meet: parse and format [src: ADR-0001] |
| `envel/dates.py` | the only place text and calendar dates meet: parse, format, and what today is [src: ADR-0006] |
| `envel/__main__.py` | `python3 -m envel` |
| `bin/envel` | the executable shim [src: bin/envel] [src: ADR-0004] |

The dependency direction is one way: `cli` knows about all five modules below it
[src: envel/cli.py:13], `summary` knows about `envelopes`, `money` and `dates` [src: ADR-0009],
`envelopes` knows about `money` and `dates` [src: envel/envelopes.py:12], and none of `store`,
`money` and `dates` knows anything above it. `envelopes` does not know about `summary`
[src: ADR-0009]: the operations change a store and the reports read one, and the reports are the
side that depends.

Reading and writing the store file is `cli`'s work and not `envelopes`' [src: envel/cli.py:154]: an operation is handed a
document and returns a new one, which is what keeps the decision layer a pure function of
(store, arguments) and lets every criterion be exercised both through the command line and
directly [src: tracker/items/WI-0001/artifacts/plan.md]. Nothing below `cli` prints, and nothing
below `cli` calls `sys.exit`; a refusal travels up as a value.

## The data

One JSON document holding the envelopes and a list of dated entries; a balance is
the sum of an envelope's entries rather than a stored number [src: ADR-0002]. The list was
append-only until `WI-0005` [src: WI-0005]: a correction now edits an entry where it sits and a
removal deletes it, so the entries are still ordered as written and still summed with no branch on
`kind`, but they are no longer only ever added to [src: ADR-0011]. What did **not** change is the
document's shape — no key is added, removed or renamed, so `format` stays `2` [src: envel/store.py:11]. Amounts are whole
numbers of cents throughout [src: ADR-0001], and a spend's `cents` is negative so that the sum
keeps working [src: ADR-0006]. The file's location comes from `ENVEL_FILE` or the XDG data
directory [src: ADR-0003].

An entry's `at` is when the tool recorded it, on every kind of entry. A spend and a move each
carry one field more — `on`, the calendar day the money moved, which may be earlier than `at` —
and income carries no date of its own, which is the stakeholder's own asymmetry [src: ADR-0006]
[src: WI-0003/Q-003].

A move between two envelopes is stored as **two** entries of kind `move`, one naming each
envelope, with `cents` negative on the side the money left and positive on the side it arrived,
and with the same `on` and the same `at` on both [src: ADR-0007]. That is what keeps a balance the
plain sum of an envelope's entries with no branch on the kind, and it is what lets a month's net
moved figure be a sum with a filter rather than a special case [src: WI-0003 AC2 "The moved figure
is one net number, positive when more arrived than left"]. No field in the file names the pair, and the two halves are
recognisable only by what they share: the same `on`, the same `at`, opposite `cents`, and —
since `ADR-0010` [src: ADR-0010] — the two consecutive references they take
[src: envel/envelopes.py]. No code reads that adjacency as a link; the listing prints each
half on its own line and pairs nothing [src: envel/summary.py].

Each entry also carries `ref`, a positive integer written when the entry is appended and never
changed afterwards, and the document carries `next-ref`, the number the next entry will take
[src: ADR-0010]. That is what gives an entry an identity the person can read off a listing and
type back [src: WI-0005/Q-008], and what keeps a reference pointing at its own entry once
`WI-0005` can remove one. A move takes two consecutive references, one for each of its two
entries. The document's `format` is therefore `2`; a document at `format: 1` — anything the tool
wrote before this — is upgraded when it is read, in memory, with references assigned in the order
the entry list already holds them, and the file itself is left alone until a command changes
something [src: ADR-0010].

## Conventions this project has adopted

- Output that reports success goes to stdout with exit 0; every refusal goes to stderr with a
  non-zero exit [src: WI-0001 AC16 "Every refusal this item specifies writes its message to stderr and exits non-zero"].
- Amounts are printed with exactly two decimal places and no currency symbol
  [src: WI-0001 AC8 "An amount is written with at most two decimal places"] [src: WI-0001 AC17 "An amount is written as a plain decimal number"].
- Envelope names are matched on their case-folded form and displayed as first typed
  [src: WI-0001 AC11 "Envelope names are matched without regard to capitalisation"] [src: WI-0001 AC12 "The listing shows an envelope's name exactly as it was typed"].
- A date typed at the command line is written `YYYY-MM-DD`, and a month `YYYY-MM`, and nothing
  else [src: WI-0002 AC11 "form and nothing else"]
  [src: WI-0003 AC5 "A month is written `YYYY-MM`"]. A month is the same form with the day taken
  off, which is the stakeholder's own reading of it [src: WI-0003/Q-004], and both are parsed in
  `envel/dates.py` and nowhere else [src: ADR-0008].
- Tests and lint use the standard library only [src: ADR-0005].

## What is not decided yet

Nothing. Every item of `EP-001` [src: EP-001] has had its design taken, and the last of them is
`BUG-0001` [src: BUG-0001]: how a month that closed short is printed, now that the stakeholder has
settled that it is said in words rather than as a minus [src: BUG-0001/Q-001], which is `ADR-0012`
[src: ADR-0012]. Before it the last was how a recorded spend or income is corrected and removed, so
that a past summary shows the corrected figure [src: WI-0005], which is `ADR-0011`
[src: ADR-0011]. How the entries behind
an envelope's balance are looked up left this list before it: it is `ADR-0010` [src: ADR-0010], for `WI-0006` [src: WI-0006], as how a month
is selected and summarised left it at `ADR-0008` [src: ADR-0008] and `ADR-0009` [src: ADR-0009]
for `WI-0003` [src: WI-0003], and how money moves between envelopes left it at `ADR-0007`
[src: ADR-0007] for `WI-0004` [src: WI-0004].

`ADR-0002` [src: ADR-0002] was written expecting the later items to build on it without changing
the file's shape, and `ADR-0006`, `ADR-0007` and `ADR-0008` each extended it once without doing
so. `ADR-0010` is the one that does change it — two keys and a `format` bump — and it takes the
branch `ADR-0002` put the `format` field there for. `ADR-0011` [src: ADR-0011] changes the
document's shape not at all and one of `ADR-0002`'s sentences instead: the entry list stops being
append-only, which is a property of the log rather than of the file.

## Engagement state

- The engagement has ended, and the ending is **E1, delivered**. `WI-0001` [src: WI-0001] was
  the first item designed and `BUG-0001` [src: BUG-0001] the last; each of the seven items opened
  under `EP-001` [src: EP-001] was designed, implemented, verified against its acceptance
  criteria, reviewed and closed `delivered`.
- Thirteen decisions were taken and recorded, `ADR-0001` [src: ADR-0001] through `ADR-0013`
  [src: ADR-0013], and this document was carried forward beside them as each was decided — its
  change log is the trail.
- There is running code now, and this document's claims have been read against it rather than
  against the design that proposed them. The audit is DE6's, run at each of the three reviews at
  rest, and it is recorded in `tracker/items/EP-001/artifacts/review.md` [src: EP-001]. The second
  of those audits failed and sent the engagement back to work; the third and the ending passed.
- The stakeholder accepted the engagement at `EP-001/Q-009` [src: EP-001/Q-009], which is what
  determined this ending.
- `review-close` restated this section when it recorded the ending, on 2026-09-11. Nothing
  rewrites it now.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 12 | 2026-09-11T19:17:34Z | review-close | EP-001 | `## Engagement state`: restated at the ending, which is **E1, delivered**. Its three sentences were `plan`'s, written before `WI-0001` was built, and each had become false: `WI-0001` is no longer the item about to be designed, work has been implemented and verified, and there is running code for a document to be checked against — which is what DE6 did at each of the three reviews at rest. Restated from the ending, after the stakeholder's reply arrived, because their answer is itself part of the engagement's state. Nothing else in this document changed: `## The parts`, `## The data`, `## Conventions this project has adopted` and `## What is not decided yet` are untouched. |
| 11 | 2026-09-11T18:55:51Z | answer-questions | EP-001 | `## The parts`: *"Reading and writing the store file is `cli`'s work and not `envelopes`'"* cited `[src: envel/cli.py:68]`, which is the `--on` option's help string on the `move` subparser and supports nothing about the store. The statements it names are `path = store.store_path()` [src: envel/cli.py:154], `document = store.load(path)` [src: envel/cli.py:156] and `store.save(path, result.store)` [src: envel/cli.py:218]; the citation now reads `[src: envel/cli.py:154]`. The assertion is unchanged and no code has to change to satisfy the new text — `envel/envelopes.py` imports no `store` [src: envel/envelopes.py:12]. Answering `EP-001/Q-007`, which is the third occurrence of this defect in this engagement after `WI-0005/Q-009` and `BUG-0001/Q-002`. `## Engagement state` was left untouched — it belongs to the ending. |
| 10 | 2026-09-11T11:13:17Z | plan | BUG-0001 | `## What is not decided yet`: `BUG-0001` is now the last design taken and `ADR-0012` [src: ADR-0012] is it — how a month that closed short is printed, after the stakeholder settled at `BUG-0001/Q-001` that a shortfall is said in words rather than as a minus. `WI-0005` and `ADR-0011` [src: ADR-0011] move to being the one before it; the sentence about them is otherwise unchanged. Nothing else in this document changed: `ADR-0012` touches no module boundary, no dependency direction and no stored shape, so `## The parts`, `## The data` and `## Conventions this project has adopted` are all still true — they are carried as open rows of `BUG-0001`'s invalidation set so that `implement` confirms that rather than this execution asserting it. `## Engagement state` was left untouched — it belongs to the ending. |
| 9 | 2026-09-11T09:29:32Z | plan | WI-0005 | `## The parts`: `envelopes.py` owns seven operations rather than five. `## The data`: the entry list is no longer described as append-only — `ADR-0011` [src: ADR-0011] has a correction edit an entry where it sits and a removal delete it — and the paragraph says what did not change with it, the document's shape and its `format` [src: envel/store.py:11]. `## What is not decided yet`: `WI-0005` is decided and leaves the list, which is now empty, and the closing paragraph gains what `ADR-0011` does to `ADR-0002` [src: ADR-0002], which is to falsify a sentence rather than to change the file. `## Engagement state` was left untouched — it belongs to the ending. |
| 8 | 2026-09-11T08:22:40Z | implement | WI-0006 | `## The data`: the move paragraph said *"Nothing in the file links the two halves of a move to each other"*, which this item made false — `ADR-0010` [src: ADR-0010] gives the two halves consecutive references, and this same document already said so four lines earlier. Replaced with what is now true: no **field** names the pair, the adjacency is the nearest thing to a link the file has, and no code reads it as one [src: envel/summary.py]. The invalidation set left this read to `implement` rather than assuming it. `## Engagement state` was left untouched — it belongs to the ending. |
| 7 | 2026-09-11T08:04:48Z | plan | WI-0006 | `## The parts`: `envel/summary.py` holds two reports rather than one, because `WI-0006`'s listing is put there [src: ADR-0009]. `## The data`: a paragraph for `ref` and `next-ref`, the `format` at 2, and the in-memory upgrade of a document written before them [src: ADR-0010]. `## What is not decided yet`: `WI-0006` is decided and leaves the list, and the prediction that the remaining items would build on `ADR-0002` without changing the file's shape is replaced by what `ADR-0010` actually does — the sentence was written before this design existed and is the one the invalidation set flagged. `## Engagement state` was left untouched — it belongs to the ending. |
| 6 | 2026-09-11T06:20:16Z | plan | WI-0003 | `## The parts`: `envel/summary.py` joins the table and the dependency sentence gains its edge [src: ADR-0009]. `## Conventions this project has adopted`: a command-line date may now be a month, `YYYY-MM`, which `WI-0003` is the first item to type [src: WI-0003 AC5 "A month is written `YYYY-MM`"]. `## What is not decided yet`: `WI-0003` is decided and leaves the list. |
| 5 | 2026-09-11T05:38:33Z | plan | WI-0004 | `## The parts`: `envelopes.py` owns five operations rather than four. `## The data`: a spend is no longer the only entry with an `on`, and a move's two-entry shape is stated with what it buys [src: ADR-0007]. `## What is not decided yet`: `WI-0004` is decided and leaves the list. |
| 4 | 2026-09-11T04:39:01Z | implement | WI-0002 | `## The parts`, the dependency-direction paragraph: it said *"`envelopes` knows about `store`, `money` and `dates`"*, and `envelopes` does not know about `store` — it never imports it, and `cli` is what loads and saves the file. Corrected against the code, and the property the false version hid is now stated: an operation is handed a document and returns a new one, so the decision layer is pure. Found by `review-close`'s D12 audit, which sent `WI-0002` back for it (`tracker/items/WI-0002/artifacts/review.md`, finding 1). No decision changed and no code changed. |
| 3 | 2026-09-11T04:02:10Z | plan | WI-0002 | `## The parts`: `envel/dates.py` is added, `envelopes.py` owns four operations rather than three, and the dependency-direction sentence names the third module `envelopes` knows about. `## The data`: what `at` means on every entry, the spend's `on` field, and the negative `cents` a spend stores [src: ADR-0006]. `## Conventions`: a date is written `YYYY-MM-DD`. `## What is not decided yet`: `WI-0002` is decided and leaves the list. |
| 2 | 2026-09-11T02:43:44Z | implement | WI-0001 | `## The parts`: the shim is `bin/envel`, not a file at the repository root. A file named `envel` cannot exist beside the package directory `envel/` — the two share one name — so the row as written named a file that could not be created. |
| 1 | 2026-09-11T02:34:57Z | plan | WI-0001 | First version: the read-decide-write shape, the module split and its dependency direction, where the data lives, the output conventions, and what the later items still have to decide. |

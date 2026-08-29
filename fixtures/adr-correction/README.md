# The legal repair for a standing ADR

Iteration 4's `lint-claims --all` reported three `claim.unsourced` errors in an accepted ADR.
The reviewer read all three against the code and found them **true** — and then found there was
no move that cleared them. Adding a citation is an edit; the only repair `spec/doc-header.md`
knew was supersession; superseding an accepted decision in order to write down where it came
from is disproportionate. The reviewer recorded it honestly as an accepted gap and the ledger
acquired a permanent, known, unfixable lint error (F-067).

`before/` is that ADR reduced: the three absolutes about `RECALL_FILE` and the single resolver,
each true, each carrying no source. `after/` is the same ADR repaired through `doc-header.md`
§4b — three `provenance` corrections, an append-only `## Corrections` table, a change-log row,
a version bump, and not one word of the decision changed.

`scripts/check` asserts both halves. If `before/` ever comes back clean the fixture has drifted
and the repair proves nothing; if `after/` is not clean, the path the spec now advertises does
not work. The *shape* rules for a correction — kind, citation, a quoted erratum, order,
change-log pairing, and the refusal to repair a superseded decision — are covered where every
other schema rule is: `fixtures/broken-workspace` for the seven ways to get it wrong, and
`examples/toy-project` (ADR-0005) for the one way to get it right.

`before/` and `after/` are document trees rather than workspaces on purpose: rule 2 of
`lint-claims` reads `docs/` and nothing else, and a tracker here would only add findings that
have nothing to do with F-067.

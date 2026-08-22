# Review — WI-0002

## What I examined

- The full diff `main..wi/WI-0002` for `expenses/`, hunk by hunk — 308 changed lines across five
  modules, two of them new — and the 510 lines of test added, read for what they assert.
- `item.md` (AC1–AC14, all ticked), `history.md` (nine rows), `journal.md` (six entries, read in
  full), `plan.md`, `impl-report.md`, `verify-report.md`, `refinement-qa.md`, and both questions
  with their `## Consequences`.
- `ADR-0001` through `ADR-0010`, `docs/architecture/overview.md` (v2) and `docs/product/prd.md`
  (v2), read **against the code** for D12 — including re-running two claims rather than reading
  them approvingly.
- Commands run during this review, not taken from a report: `check-verify-freshness`,
  `check-commit-refs`, `validate-workspace`, a trial merge into a **detached** throwaway worktree
  with the project's test and lint commands on the merge result, and a re-read of the stored JSON
  against `ADR-0009`.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion checkbox ticked | **pass** | `grep -c '^- \[ \]' item.md` → 0; fourteen `- [x] AC` |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | fourteen rows plus a head-clause row, each naming the command run and the captured output. Spot-checked AC7's third case and AC10's accepted case by re-running them here; same output |
| D3 | all declared gates passed on the **final** state of the code | **pass** | I ran `python3 -m unittest discover -s tests -t . -q` (exit 0, 79 tests) and `python3 -m compileall -q expenses tests` (exit 0) at `2b4a2b0`, and again on the trial merge result |
| D4 | no open blocking question | **pass** | both questions on the item are `answered`, each with a `## Consequences` section naming real files |
| D5 | a journal entry per execution; history chains without a gap | **pass, with a blemish** | nine history rows chain from `— → draft` to `verifying → in-review`, last row matches the item's status; six journal entries account for six executions (`intake` and `implement` each produced two rows from one execution). The blemish is Finding 3 below: the entries' own timestamps run ahead of the history rows they describe |
| D6 | every design decision is in an ADR cited from the plan or journal | **pass** | `ADR-0009` and `ADR-0010` are new and both are cited in `plan.md` § *Decisions and ADRs* and in the `plan` journal entry; five earlier ADRs are cited rather than re-decided; the three non-ADR choices are under `plan.md` § *Assumptions* with their reversal costs |
| D7 | documents this change invalidated were updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` v1 → v2 with a change-log row, adding `money.py` and the syntax-versus-meaning rule. `prd.md` needed no change: its description of an expense — an amount, one payer, one or more sharers — is exactly what was built |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, "all 3 commit(s) on main..wi/WI-0002 name WI-0002", run **before** the merge |
| D9 | merged into the trunk | **pass** | merged after this review and after the close, in that order — see § *Verdict* |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness` → exit 0: verified at `10a6bc39`, branch moved to `2b4a2b03`, "only the record changed (5 files under tracker/)". Confirmed independently: `git diff --name-only 10a6bc3..wi/WI-0002 -- expenses tests` is empty |
| D11 | the review record states what was examined | **pass** | this document, § *What I examined* |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, checked by reading it against the code | **pass** | `ADR-0002`'s six refusal conditions are each implemented and each has a test — I walked the list against `group.add_expense` line by line. `ADR-0009`'s stored shape I checked against a real record file, not against the report. `ADR-0003` point 6 holds: nothing derived appears in the file. `overview.md` v2's claim that `group.py` never sees a comma is true, and its converse is Finding 2. `ADR-0010`'s scope wording is Finding 4 |

## Findings

**1 — the reserved characters are expressed twice, in two forms.** `group.RESERVED_CHARACTERS`
is the tuple `(",", "=")` that `validate_name` checks a name against; `cli._split_sharers` splits
on those same two characters as control flow, with no reference to the tuple. Today they agree.
If a third character were ever reserved — the tuple is the obvious place to add it — names
containing it would be refused while the sharer list would not split on it, and the two rules
would have drifted with nothing to catch them. Not a defect and not a send-back: no criterion
covers it and the behaviour today is correct. Worth naming because it is the kind of duplication
that fails quietly and this is the last moment anyone reads this diff.

**2 — the syntax/meaning line in `overview.md` v2 is not quite where the code draws it.** The
document says `cli.py` owns syntax and `group.py` owns meaning, and that "`group.py` never sees a
comma" — both true. But *which* characters are reserved is a domain fact, recorded in `ADR-0005`
point 2, and `cli.py` now encodes it. This is the same observation as Finding 1 from the
document's side. The document is not wrong; it is less precise than the code, which is the safe
direction.

**3 — journal entry timestamps run ahead of the history rows they describe.** The `refine` entry
is stamped `19:56:00Z` while the row it reports is `19:42:56Z`; `plan` `20:02` against `19:47:45`;
`implement` `20:14` against `19:53:34`; `verify` `20:24` against `19:57:46`. The entries are in
non-decreasing order and each `**Status:**` bullet matches its row, so nothing validates as broken
and no reader is misled about *what* happened — but a reader reconciling the two files sees each
entry dated after the transition it describes, by up to twenty-seven minutes. The cause is that
`history.md` is stamped by the `transition` script from the real clock while journal entries are
written by hand, and no procedure says the two must agree. WI-0001 has the same drift, smaller.
Not a send-back — the fix is not in this item's code and rewriting an append-only journal to tidy
it would be worse than the blemish — but it is a real defect in the record and it is named here
rather than left for someone to notice and distrust.

**4 — `ADR-0010`'s title says "read or write", the message says "save", and only writes reach
it.** `storage.load` already converts every `OSError` it can raise into a `RecordError` with a
`Cannot read <path>: …` message, so the new `except OSError` in `cli.main` is in practice reached
only by `storage.save`. The message it prints — `Cannot save to <path>: …` — is therefore always
accurate. The ADR is broader than the code needs to be, not narrower, which is harmless; recording
it so a future reader who adds a second file-reading path knows which of the two messages they
inherit.

**5 — `shared by 1 people.`**, carried up from `verify-report.md` § *Defects found*. AC1 pins that
sentence only for its own three-sharer case, so no criterion is violated and I am not sending the
item back for it — that would be the reviewer inventing a criterion after the fact. It is the one
piece of output in this item a user would call wrong, and it is recorded in `## Notes` so that the
next `refine` execution to touch a confirmation message can pin the plural properly.

**Nothing else.** Every hunk traces to a plan step and a criterion. The five deviations
`impl-report.md` declares are each justified — the `errors.py` extraction in particular is the
correct fix for a genuine circular import the plan created, and it changes no behaviour. No hunk
contradicts an ADR. Nothing was built ahead for WI-0003 or WI-0004: no balance, no netting, no
`payments` key.

## Accepted gaps

Each is written into `item.md` § `## Notes` as well.

| gap | why it is acceptable | where it lands |
|-----|----------------------|----------------|
| `ADR-0010`'s write-failure message satisfies no criterion | declared in advance by `plan.md`, exercised by both `implement` and `verify`, and correct when run. `plan` may not write criteria, so there was no legitimate way to give it one | `item.md` § Notes; `ADR-0010` § *Decision* |
| `--paid-by` with no value, and `add-expense` with two positionals, have no criterion | both declared by `impl-report.md` § *Deviations*, both refuse sensibly, both exist because the alternative is an `IndexError` or a silently ignored argument | `item.md` § Notes |
| "a refusal creates no record file" is pinned for `add-person` but not for `add-expense` | today's behaviour is correct — `verify` checked — but two of its fifteen mutations survived precisely because nothing pins it. A gap in the criteria, not the tests | `item.md` § Notes, named for WI-0004's refinement, which adds the third recording command |
| `shared by 1 people.` — Finding 5 | cosmetic, uncovered, and fixing it now would mean editing a criterion at review time | `item.md` § Notes |
| Atomicity of the write is argued, not demonstrated | unchanged from WI-0001; the consequence that matters — a record that cannot be read is never overwritten — was demonstrated again here against four hand-written corrupt records | `verify-report.md`; `WI-0001/item.md` § Notes |
| `lint-clean` is a syntax check, not a linter | `ADR-0008`. Two new modules and ~300 lines went through this item with review as their only style check; that is a standing project condition, not this item's | `ADR-0008`; `WI-0001/item.md` § Notes |

## Verdict

**Accept, close, and merge.** All twelve Definition of Done criteria pass. The trial merge into a
**detached** throwaway worktree of `main` was clean and `python3 -m unittest discover -s tests -t
. -q` passed on the merge result (79 tests, exit 0), as did the lint command; the trial was then
discarded — and `main` was confirmed still at `3a8d9f7` afterwards, which WI-0001's review had to
learn the hard way. The item was closed while `wi/WI-0002` was still unmerged, so
`check-commit-refs` still had a non-empty range, and only then was the branch merged.

Five findings, none blocking: two forms of one duplication that will drift if a third character is
ever reserved, a record blemish in the journal timestamps, an ADR that is broader than its code,
and a plural that should say "1 person".

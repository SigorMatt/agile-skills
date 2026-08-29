# Review — WI-0003

## What I examined

**The record, read in full.** `item.md` (all nine criteria and their tick state), `history.md`
(ten rows), `journal.md` (ten entries, read end to end, not skimmed), `plan.md` including its
`## Assumptions` and `## Risks`, `impl-report.md` including both passes, `verify-report.md`
including its appendix, and `questions/Q-001.md` with its `## Answer` and `## Consequences`.

**The diff, hunk by hunk — `git diff main..wi/WI-0003`.** Every hunk was mapped to a plan step, a
criterion, or a declared deviation:

| file | hunks | what they serve |
|------|-------|-----------------|
| `recall.py` | `STORE_VERSION`/`READABLE_VERSIONS`/`LADDER` | plan step 1 |
| | `_is_date` | plan step 3, with the round trip added in pass 2 for D2 |
| | `load`'s `due` and `interval` checks and the `bool` guard | plan step 3 + pass 2's D1 |
| | `load`'s `setdefault` normalisation | plan step 4 (AC8) |
| | `add_card`'s `"interval": None` | plan step 5 (AC6) |
| | `next_interval` | plan step 2 (AC2, AC3, AC6) |
| | `record_result` | plan step 6 (AC2, AC3) |
| `README.md` | the "When a card comes back" section | plan step 7 (AC4) |
| | the `interval` row, the sample JSON, the version paragraph, the unreadable-store sentence | plan step 8 (AC4, AC9) |
| | `## Not yet built` rewritten | `impl-report.md` deviation 2 |
| `tests/test_schedule.py` | the whole file, nine test classes | plan step 9, plus pass 2's four AC9 tests |
| `tests/test_session_parts.py` | `NextIntervalTest`, `RecordResultTest` rewritten | plan step 10 + deviation 3 |
| `tests/test_store.py` | three assertions moved to version 3 | plan step 11 + deviation 1 |
| `tests/test_docs.py` | two README tests | plan step 12, plus the card-field-row test pass 2 added |

Nothing was found that no criterion, plan step or declared deviation accounts for. No hunk
contradicts an ADR.

**The claims in `docs/`, audited from their citations (D12).** Each was decided by opening what it
cites, not by reading the sentence:

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| "A `due` must be exactly `YYYY-MM-DD` … anything else makes the document unreadable" | `ADR-0007` `## Decision` | `recall.py` `_is_date` and `load`'s `due` branch | **true** — and only true since pass 2: the round-trip check is what makes "exactly" hold, and at `eb4cc23` this sentence was false for `2026-8-9` |
| "an `interval` must be one of the ladder's values or `null`" | `ADR-0007` `## Decision` | `load`'s `interval` branch, including the `isinstance(..., bool)` guard | **true** — and again only since pass 2, `true` having passed the bare membership test |
| "`save` stamps `3`; `load` accepts `1`, `2` and `3`" | `ADR-0007` `## Decision` | `STORE_VERSION`, `READABLE_VERSIONS`, `save` | **true** |
| "A card read from an older document has no `interval`, which is read as `null` … the next write carries the field on every card" | `ADR-0007` `## Decision` | `load`'s `setdefault` loop and `save` | **true** |
| "a card already at `30` stays at `30`" | `ADR-0007`, `ADR-0001` `## Decision` | `next_interval`'s `min(position + 1, len(LADDER) - 1)` | **true** |
| "successive correct answers then give 1 day, 3 days, 7 days, 30 days … the top rung after four correct answers, not three" | `ADR-0001` v3 `## Decision` | `add_card`, `next_interval`, and the run recorded in `verify-report.md` AC6 | **true** |
| "The placeholder next-due date that version 2 of this document described is gone" | `overview.md` §2 | `record_result` | **true** — `timedelta(days=1)` is gone, replaced by `days=card["interval"]` |
| "`load` checks every field it reads on the way in, and a document that fails any check is reported and left byte-for-byte alone" | `overview.md`, "The store refuses what it cannot read" | `load`, `_unreadable`, and the `cmp` results across 30 stores × 3 commands in `verify-report.md` | **true**. The `setdefault` normalisation is not a counter-example: it fills an *absent* field in memory and touches no file, and the sentence is about a document that fails a check |
| "the ladder as one constant" | `overview.md` constraints table, `ADR-0007` | `LADDER = (1, 3, 7, 30)` in `recall.py` | **true** — not in the store, not configurable |

**Gate scripts, run.** `check-verify-freshness`, `check-commit-refs`, `lint-claims`,
`check-epic-signoff`, `validate-workspace`, and the test and lint commands. Plus the trial merge
into a detached worktree of `main` with the suite run on the merge result.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion ticked | **pass** | nine `- [x]` and zero `- [ ]` in `item.md`; AC9 was ticked by the second verification |
| D2 | every tick cites evidence in `verify-report.md` | **pass** | its `## Criteria` table gives a command and its actual output for each of AC1–AC9, all run in that execution. The first verification's ticks were **not** carried over: the report says so explicitly and re-establishes AC1–AC8 from scratch, because the AC9 fix touched `load`, which every command goes through |
| D3 | gates passed on the final state of the code | **pass** | last code commit is `5d9c323`. `implement` ran its gates there (87 tests); `verify` ran its at `f841f09` (record-only commits after `5d9c323`); this review ran the suite again at `e9332d6` and on the merge result. No code has changed since `5d9c323` |
| D4 | no open blocking question | **pass** | `Q-001` is the item's only question, `status: answered`, `answered-by: human`, with `## Consequences` naming four real files — each of which I opened and found carrying the change it claims |
| D5 | a journal entry per execution; history chains | **pass** | ten history rows, from `— → draft` to `verifying → in-review`, no gap; ten journal entries matching them one for one (`implement` pass 1 made two transitions and wrote two entries; pass 2 resumed at `in-progress` without an opening transition and wrote one). Last row's `to` is `in-review`, which is `item.md`'s status |
| D6 | design decisions in ADRs, cited | **pass** | `ADR-0007` (new, v1) records the representation, the version and the ladder's home; `ADR-0001` amended to v2 by `answer-questions` for the never-answered state and to v3 by `plan` for reversibility. Both are cited from `plan.md` `## Decisions and ADRs` and from the journal. Pass 2's reversal of `plan.md`'s `strptime` assumption needed no ADR: the plan declared it reversible and named the cost, and that is the mechanism working rather than a design change |
| D7 | invalidated documents updated, with version bump and change-log row | **pass** | `overview.md` v3 and `ADR-0001` v3, each with a change-log row, plus `ADR-0007` v1 — all written by `plan` before the code. I checked the harder direction too: nothing in either implementation pass falsified them. Pass 2 made `ADR-0007`'s "exactly `YYYY-MM-DD`" sentence *true* rather than stale, which is why it needed no edit |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0003 wi/WI-0003` → exit 0, "all 9 commit(s) on main..wi/WI-0003 name WI-0003" |
| D9 | merged into the trunk | **pass** | trial-merged into a detached worktree of `main` first (87 tests, OK, on the merge result); `main` confirmed still at `47ac197` afterwards; then merged for real after this item was closed |
| D10 | verification postdates the code | **pass** | `check-verify-freshness WI-0003 wi/WI-0003` → exit 0: "verified at `f841f096`; `wi/WI-0003` has moved to `e9332d69` but only the record changed (5 file(s) under `tracker/` or `docs/`)". Run, not assumed |
| D11 | `review.md` exists and says what was examined | **pass** | this file, `## What I examined` first |
| D12 | claims in `docs/` about the touched behaviour are still true | **pass** | the nine-row audit table above; each verdict was reached by opening the cited code, not by reading the sentence or a neighbouring document. `lint-claims --changed-since main` → exit 0 (no documents changed on this branch; the three were written by `plan` and are already on `main`) |

## Findings

**None that send the item back.** Four things were examined closely enough to be worth recording
as examined rather than merely passed:

1. **The item was rejected once, and the rejection worked as designed.** The first verification
   found two ways a scheduling value slipped past AC9 — `interval: true` read as the 1-day rung
   because `True == 1`, and an unpadded `due` that sorted the card out of every review. Both are
   this item's own AC9, so it was a send-back rather than a bug item; that classification is
   correct. The second verification re-ran all nine criteria rather than only the one that failed,
   which is the right response to a fix inside `load`.
2. **`load`'s two new checks tighten behaviour a previous `recall` allowed.** A store an older
   build read can now be refused. This is intended and is documented in three places — `README.md`,
   `ADR-0007` `## Consequences`, and `overview.md` — each stating the cost rather than only the
   benefit. It is the right call for an item that makes hand-editing the documented way to move a
   card.
3. **`next_interval` raises rather than guessing when handed a rung outside the ladder**, and
   `test_a_rung_outside_the_ladder_raises_rather_than_guessing` pins it. Given that `load` is what
   guarantees the precondition, an error path that fails loudly rather than silently rescheduling
   a card is what I would want to maintain.
4. **The test suite is sensitive, and checked to be.** The verification mutated the code once per
   criterion and recorded which test failed each time — including the case that had previously
   been a gap: deleting `README.md`'s `interval` table row now fails
   `test_the_readme_card_field_table_has_a_row_for_the_rung_field` and nothing else. A gate that
   passes against an absent implementation is worse than no gate, and this one was proved not to.

Two things were looked at and deliberately **not** filed as bugs, agreeing with the verification:

- `due_cards` still compares `due` as a string rather than parsing it. That is the underlying
  reason an unpadded date was dangerous, and it would be a change to behaviour `WI-0002`
  delivered, with no criterion of this item behind it. It is correct for every value `load` now
  admits, because they are all canonical and zero-padded — the verification checked the edges at
  `"0999-01-01"` and `"9999-12-31"`. There is nothing to file.
- `cmd_review` saves the whole document after each card. Unchanged from `WI-0002`, touched by no
  criterion here, and it caused nothing observed.

## Accepted gaps

Each is copied into `item.md` `## Notes` under "What was not checked", because a gap recorded only
in a report stops being read the moment the item is `done`.

1. **JSON floats equal to a ladder rung are accepted.** `interval: 1.0` reaches `next_interval`
   and behaves as the 1-day rung; the next write canonicalises it to the integer `1`. The
   verification judged this inside AC9 and gave its reasoning — JSON has one number type, so `1.0`
   and `1` denote the same value, and `README.md` lists the number 1; the contrast is with JSON
   `true`, a boolean silently reinterpreted as a rung nobody wrote. I agree, and it is recorded
   here and in the item so that anyone who does not can find it. No card is dropped and no
   schedule differs, so there is nothing to file.
2. **Nothing was observed across a real change of date.** Everything was run on 2026-08-29 with
   other dates simulated by hand-editing `due` — the mechanism the criteria themselves prescribe.
   No criterion asks for more.
3. **Timezones and clock changes were not probed.** `due` is a local date with no zone;
   `ADR-0006` already records this as a known limitation and the item puts it out of scope, so the
   gap is recorded where it belongs rather than duplicated as new.
4. **The AC9 probe is a search, not a proof.** Thirty malformed stores across three commands each,
   attacking wrong type, wrong shape, wrong position in the file, and equal-but-not-identical to a
   ladder value. Broader than the first pass, and it caught the one remaining class — but it
   cannot show there is no other.
5. **Stores larger than two cards, and concurrent processes, were not exercised.** No criterion
   covers either.

## Verdict

**Accepted.** All twelve Definition of Done criteria pass, each with its own evidence. The change
does what WI-0003's nine criteria ask, in a way this project should live with: one constant, one
pure function, two checks in the one place every command already goes through, and documentation
that lets a reader work out a card's next due date without opening the code — which is the
property AC4 exists for and which this review used to read the diff.

The record is reconstructible. From the tracker, `docs/` and `git log --grep WI-0003` alone, a
reader who was not here can say what was built and why (`plan.md` and `ADR-0007`), which skill
decided what (ten journal entries against ten history rows), what was asked of the stakeholder and
what they said (`Q-001`, answered verbatim, propagated into four named files), and what
verification found — including that it rejected the work once, on what evidence, and what changed
in response.

Merged into `main` after closing, and the item is `done` with `outcome: delivered`.

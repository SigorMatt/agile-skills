# Implementation report — WI-0001

**Status of this report:** the code is finished and committed, `WI-0001/Q-003` is answered, and
the item moves to `verifying` with eight of nine hard gates passing and the ninth,
`claims-are-sourced`, recorded as **failed** under the convention in
`docs/process/ways-of-working.md`. Everything below is true of the branch head, `wi/WI-0001`,
and was re-run there on 2026-09-10 after the answer landed. **`verify` should read `## Gates`
first: it inherits a known-failing gate, deliberately and with its reason written down.**

## What was built

Two commands and the file that makes them outlive the process, in the four pieces the plan and
`docs/architecture/overview.md` describe:

- **`envel/store.py`** — `store_path` resolves `ENVEL_FILE`, then `XDG_DATA_HOME`, then
  `~/.local/share/envel/store.json` (ADR-0003). `load` returns an empty store when the file is
  absent and raises `StoreError` when a file that exists cannot be understood, rather than
  reading it as empty — plan assumption P4, and the reason is that treating a damaged store as
  empty would let the next `new` overwrite it. `save` creates the parent directory, writes a
  temporary file beside the target and `os.replace`s it, so an interrupted run leaves either the
  old document or the new one.
- **`envel/envelopes.py`** — `identity(name)` is `name.strip().casefold()` and `display(name)` is
  `name.strip()` (ADR-0004). `add` refuses an empty identity with `InvalidName` and a clash with
  `DuplicateName`, which carries the **stored** display name rather than the input; `listing`
  sorts by `name.encode("utf-8")`. The module imports nothing that touches a filesystem, so the
  rules are exercised without a store.
- **`envel/cli.py`** — `new` and `list`, no option parser (plan assumption P3), and the exit
  statuses of assumption P2: 0 for success, 1 for a refusal, 2 for a usage error.
- **`bin/envel`** — the launcher (ADR-0002). Eleven lines; two of them are statements about the
  tool.
- **`tests/`** — 24 cases. `tests/test_envelopes.py` covers the domain rules with no filesystem;
  `tests/test_cli.py` runs the tool end to end, invoking the bare word `envel` through a `PATH`
  with `bin/` in front of it and an `ENVEL_FILE` inside a `tempfile.TemporaryDirectory()` that is
  fresh for every case.

## Acceptance criteria evidence

Every row below was produced by `python3 -m unittest discover -s tests -t .` → exit 0,
`Ran 24 tests`, `OK`, on the branch head.

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| AC1 | `_new` returns 0 and writes to neither stream on success (`envel/cli.py:42`) | `test_ac1_new_exits_zero_and_writes_nothing_to_stderr` — asserts `returncode == 0` and `stderr == ""` |
| AC2 | `listing` returns the stored display name; `_list` prints one per line (`envel/cli.py:68`) | `test_ac2_list_after_new_writes_the_name` — asserts `stdout == "groceries\n"` |
| AC3 | the store is a file, so three processes reading the same `ENVEL_FILE` share it (`envel/store.py:39`) | `test_ac3_three_separate_invocations_share_one_store` — three separate `subprocess.run` calls; asserts `stdout == "a\nb\n"` |
| AC4 | `listing` sorts by `name.encode("utf-8")` (`envel/envelopes.py:60`) | `test_ac4_listing_is_sorted_byte_wise_and_repeatable` — `apple` and `Zebra` give `"Zebra\napple\n"`, which is byte-wise ascending and is **not** case-insensitive alphabetical order, and two runs are byte-identical. Also `test_listing_is_byte_wise_ascending_not_alphabetical` |
| AC5 | `add` raises `DuplicateName` carrying the stored name; `_new` prints it (`envel/envelopes.py:48`) | `test_ac5_a_repeated_name_is_refused` and `test_ac5_a_name_differing_only_in_case_is_refused` — the second asserts `"groceries" in stderr` after `envel new Groceries`, which fails if the message echoes the input. Also `test_duplicate_reports_the_stored_spelling_not_the_input` |
| AC6 | `load` returns an empty store for an absent file; `_list` prints `EMPTY_LINE` (`envel/cli.py:76`) | `test_ac6_list_before_anything_exists` — asserts the file does not exist, then `returncode == 0`, `stderr == ""`, at least one stdout line |
| AC7 | `display` strips but does not fold, and that is what is stored (`envel/envelopes.py:34`) | `test_ac7_capitalisation_survives_the_round_trip` — asserts `stdout == "Groceries\n"` |
| AC8 | nothing restricts the characters in a name; only a whitespace-only identity is refused | `test_ac8_a_name_with_a_space_is_accepted` — asserts `returncode == 0` and `stdout == "eating out\n"` |
| AC9 | `add` raises before mutating, and `save` runs only after it returns (`envel/cli.py:52`) | `test_ac9_an_empty_name_is_refused_and_leaves_the_store_untouched` — captures the AC6 reference, asserts non-zero and a stderr line, then asserts the following `list` stdout equals the reference |
| AC10 | the same rule: `identity("   ")` is empty | `test_ac10_an_all_whitespace_name_is_refused_and_leaves_the_store_untouched` |
| AC11 | `identity` strips before folding, so `"  groceries  "` clashes with `groceries` | `test_ac11_surrounding_whitespace_is_trimmed_before_comparing` — asserts non-zero, `"groceries" in stderr`, one line, and that the line has no surrounding space |

**The suite can fail.** Four deliberate mutations were applied one at a time and reverted:
`identity` no longer folding case → 4 failures; `listing` returning the store's order → 2
failures; `add` no longer refusing an empty identity → 4 failures; the duplicate message echoing
the input instead of the stored name → 1 failure. Each was restored and the suite returned to 24
passing.

## Documents

| document | entry it closes | claim kind | what I checked, and against what | new version |
|----------|-----------------|-----------|----------------------------------|-------------|
| `docs/architecture/overview.md` | invalidation set row 2 — the `## What this is` paragraph and the four rows of `## The shape` | cited-fact | The row asserted what four files are responsible for, written before any of them existed. All four now exist and each assertion was reopened against the file: the launcher's two statements (`bin/envel:9`, `bin/envel:11`), `cli.main` (`envel/cli.py:27`), `identity`/`display`/`find`/`add`/`listing` (`envel/envelopes.py:29`, `:48`, `:60`) and `store_path`/`load`/`save` (`envel/store.py:27`, `:39`, `:58`). The dependency-direction sentence was weakened to what was actually checked — `cli` imports both (`envel/cli.py:13`) — rather than left as a claim about what the other two modules do not do. Every citation added resolves; `validate-workspace` checks that over the whole workspace | 2 |
| `docs/process/ways-of-working.md` | invalidation set row 3 — the whole document, which did not exist before `Q-003` was answered | cited-fact | Created by `answer-questions` on this branch, not by this execution; the plan's set names it so that no path under `docs/` in the branch diff is unaccounted for. Re-read at the branch head: its four conditions are the ones this execution discharges above, and its two `[src:]` citations resolve to `.claude/agile-skills/spec/dor-dod.md` and `.claude/agile-skills/spec/doc-header.md`, which exist | 1 (unchanged) |
| `docs/product/vision.md` | invalidation set row 1 — the `## Engagement state` bullets | engagement-state | Nothing. The disposition is `owned-by-ending` and this skill may not write such a section at any disposition (`spec/doc-header.md` §4a). The three sentences are false today — the epic has five children rather than three, the five intake questions are answered, and something has now been designed and built — and `review-close` restates them at the ending. **This is also where `claims-are-sourced` fails; see `## Gates`** | — |

No document outside the plan's invalidation set was written, and this execution itself wrote none
of them — `docs/architecture/overview.md` was repaired by the first `implement` round and
`docs/process/ways-of-working.md` by `answer-questions`. `lint-documents --rule
document-writes-are-declared --item WI-0001 --changed-since main` → exit 0: 2 documents written
under `docs/` on this branch, 3 named by the plan.

## Deviations from the plan

None in substance. The plan's seven steps were executed in order and each produced what it said
it would. Three details the plan left to the implementation, recorded so a reader is not left to
infer them from the diff:

- `store.py` exports `empty()` and a `VERSION` constant. The plan named `StoreError`,
  `store_path`, `load` and `save`; a callable that returns a fresh empty document is what keeps
  `load` from handing every caller the same mutable dict.
- `_check_shape` is a private helper rather than inline in `load`. Same behaviour, named so the
  three failure messages sit together.
- `envelopes.DuplicateName` carries `existing` as an attribute, which the plan described in prose
  ("carrying the **stored** display name") without naming the mechanism.

## Gates

Run on the branch head, `wi/WI-0001`, after the last change.

- `tests-pass` → **pass**. `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 24 tests`,
  `OK`.
- `lint-clean` → **pass**. `python3 -m compileall -q envel tests` → exit 0.
- `workspace-valid` → **pass**. `scripts/validate-workspace .` → exit 0,
  `checked 6 item(s), 7 document(s)`, `0 errors, 0 warnings`. (On the earlier run it reported
  `board.stale` and `question.blocking.not-suspended`; both were `Q-003` being filed, and the
  move to `awaiting-answer` resolved them.)
- `every-criterion-has-a-test` → **pass**. The table above names a test function for each of
  AC1–AC11, and the mutation runs are the evidence that each of those functions can fail.
- `commits-reference-the-item` → **pass**. `scripts/check-commit-refs WI-0001 wi/WI-0001` → exit
  0.
- `no-unplanned-scope` → **pass** (advisory). Every hunk traces to a plan step: steps 1–4 are the
  four source files, steps 5–6 the two test modules, step 7 the overview. The only files outside
  those are `plan.md`'s two disposition cells, this report, and `Q-003`.
- `cross-answer-consistency` → **pass**. `scripts/lint-answers --changed-since main` → exit 0,
  over 7 consumed human answers. No sentence citing one of the stakeholder's answers was edited
  by this execution.
- `claims-are-sourced` → **FAIL, recorded and overridden.** `scripts/lint-claims --changed-since
  main --plan-documents WI-0001` → exit 1. Scope the run printed:

  ```
  lint-claims: checked absolute claims: 3 document(s) in 3 path(s) in scope — 2 path(s) differ
  from main (ff0022f) under docs, plus 3 document(s) named by WI-0001's plan; citations: every
  markdown file in the workspace
  docs/product/vision.md:79: ERROR [claim.unsourced] an absolute claim ('no') about
  'EP-001/Q-001' with no citation
  lint-claims: 1 error, 0 warnings
  ```

  Line 79 is inside `## Engagement state`. The absolute is "no ending has been proposed to them"
  and the backticked tokens the detector reads as code objects are question IDs. The window is
  correct — `--plan-documents` widens rule 2 to every document the plan names, which is F-087's
  fix — and the sentence is an **engagement-state** claim, whose obligation under
  `spec/doc-header.md` §4a is to be owned at the ending rather than to carry a citation.
  `implement` may not write that section at any disposition, so there is no repair available to
  this skill.

  `WI-0001/Q-003` is the architect's answer and it is option C on option D's diagnosis: record
  the gate as failed with the run's own output, name the question as its evidence, and make the
  move with `scripts/transition --force`. The four conditions
  `docs/process/ways-of-working.md` §"When a pipeline gate refuses something no actor is
  permitted to fix" requires are each met and each written down — (1) the finding is outside the
  rule the gate implements, with `spec/dor-dod.md` D12 quoted; (2) the enumeration of all nine
  skills in `pipeline.yaml` is in `Q-003`'s `## Consequences`, and the two that *may* write the
  section — `intake` and `review-close` — are not dispatchable with five children in flight;
  (3) `Q-003` records the diagnosis, four options and the decision; (4) this bullet and the
  journal carry the verdict as `fail` with the run's output, and the history reason names the
  question.

  **The finding stays open.** It is not repaired and this override does not repair it. It clears
  when `review-close` restates every `## Engagement state` section at the engagement's ending
  (`spec/dor-dod.md` DE4). `verify` and `review-close` will both meet this same error —
  `review-close` runs `lint-claims --all` — and so will the plans of WI-0002 to WI-0005, which
  will name `docs/product/vision.md` for the same D7 reason.
- `document-writes-are-declared` → **pass**. `scripts/lint-documents --rule
  document-writes-are-declared --item WI-0001 --changed-since main` → exit 0.

## What I did not do

- **I did not clear `claims-are-sourced`.** The item moved to `verifying` with that gate recorded
  as failed and the transition forced, which is what `Q-003` answered; the underlying finding is
  untouched and belongs to `review-close` at the ending. `verify` inherits it knowingly.
- **I did not touch `docs/product/vision.md`**, although three of its `## Engagement state`
  sentences are false today. That is the disposition working as designed, and it is separately
  the cause of the failing gate.
- **I did not add Unicode normalisation.** `ADR-0004` records that a combining accent and a
  precomposed character are different envelopes, and the plan puts it out of scope.
- **I did not add locking.** Two `envel` processes writing at the same instant can lose one of
  the two writes; the plan records this under `## Risks` and it is out of scope here.
- **I did not force stdout to UTF-8** (plan assumption P5). Under a non-UTF-8 locale, printing a
  name with a non-ASCII character would raise `UnicodeEncodeError`. No criterion exercises it, the
  store itself is safe, and the plan records it as a known gap.

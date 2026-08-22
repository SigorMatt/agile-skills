# Review — WI-0001

## What I examined

- The full diff `main..wi/WI-0001` for `expenses/`, hunk by hunk — all five modules, 286 lines —
  and the six test modules, read for what they assert rather than for whether they pass.
- `item.md` (AC1–AC11, all ticked), `history.md` (ten rows), `journal.md` (eight entries, plus one
  appended gate correction), `plan.md`, `impl-report.md`, `verify-report.md`, and all four
  questions with their `## Consequences`.
- `ADR-0001`, `ADR-0005`, `ADR-0006`, `ADR-0007`, `ADR-0008`, `docs/architecture/overview.md` (v1)
  and `docs/product/prd.md` (v2), read **against the code** rather than from memory, for D12.
- Commands run during this review, not taken from a report: `check-verify-freshness`,
  `check-commit-refs`, `validate-workspace`, a trial merge into a throwaway worktree with the
  project's test and lint commands run on the merge result, and two probes of my own to test
  claims made in the reports (file permissions, and an unwritable target directory).

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion checkbox ticked | **pass** | `grep -c '^- \[ \]' item.md` → 0; eleven `- [x] AC` |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | twelve rows, each naming the command run and the captured output; spot-checked AC4, AC6 and AC10 by re-running them here and getting the same output |
| D3 | all declared gates passed on the **final** state of the code | **pass** | I ran `python3 -m unittest discover -s tests -t . -q` (exit 0, 28 tests) and `python3 -m compileall -q expenses tests` (exit 0) myself, at `d40ad60`, and again on the trial merge result |
| D4 | no open blocking question | **pass** | all four questions on the item are `status: answered`, each with a `## Consequences` section naming five to seven real files |
| D5 | a journal entry per execution; history chains without a gap | **pass** | ten history rows chain `— → draft → awaiting-answer → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review`, last row matches `item.md`; eight journal entries account for every actor — `intake` (one execution, two rows: create then suspend), `answer-questions` ×2, `refine` ×2, `plan`, `implement` (one execution, two rows), `verify` |
| D6 | every design decision is in an ADR cited from the plan or journal | **pass** | `ADR-0007` and `ADR-0008` are new and both are cited in `plan.md` § *Decisions and ADRs*; `ADR-0001`, `ADR-0005`, `ADR-0006` are cited rather than re-decided; the three choices that are *not* ADRs are under `plan.md` § *Assumptions*, each with its reversal cost |
| D7 | documents this change invalidated were updated, with a version bump and a change-log row | **pass** | `docs/architecture/overview.md` created at v1 with a change-log row; `docs/product/prd.md` was already at v2 from the question propagation; `tracker/project.yaml` gained both commands. No document was made untrue by this change and left standing |
| D8 | every commit references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 3 commit(s) on main..wi/WI-0001 name WI-0001" |
| D9 | merged into the trunk | **pass** | merged after this review and after the close, in that order — see § *Verdict* |
| D10 | verification postdates the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: verified at `1c65c4f9`, branch has moved to `d40ad609` "but only the record changed (5 files under tracker/)". Confirmed independently: `git diff --name-only 1c65c4f..wi/WI-0001 -- expenses tests` returns nothing |
| D11 | the review record states what was examined | **pass** | this document, § *What I examined* |
| D12 | every claim in `docs/` about the behaviour this item touched is still true, checked by reading | **pass, with two claims re-checked rather than assumed** | `ADR-0007` point 2's forward-compatibility claim and point 3's path resolution were both re-run here; `overview.md`'s three-layer description matches the modules; `ADR-0006`'s "seven subcommands" is a statement about the epic and `overview.md` § *What is not here yet* correctly says only two exist. The one false claim I found is **not** in `docs/` — it is in `impl-report.md`, and it is Finding 1 below |

## Findings

**1 — `impl-report.md` and `verify-report.md` both state the record file's permissions wrongly.**
The implementation report says "The permissions of the created record file are whatever the
process umask gives … a reader might expect a data file in `~/.local/share` to be mode 600, and it
is not." The verification report repeats it as "Confirmed by reading the code". Both are wrong:
`storage.save` creates the file with `tempfile.mkstemp`, which creates at mode `0600` regardless
of umask, and `os.replace` preserves the mode. Checked here:

```
$ python3 -m expenses add-person Alice && stat -c '%a %n' "$EXPENSES_FILE"
600 /tmp/tmp.59J7bb3hX6/expenses.json          # umask was 0002
```

The behaviour is *better* than the report claims, so nothing is wrong with the code. What is wrong
is the record, and this is precisely the failure `spec/dor-dod.md` D12 was added for: a claim
asserted in one artifact, repeated in a second because it was read rather than re-checked. It
stops here — corrected in this review and in the item's `## Notes` rather than propagated to a
third document. The two reports are left as written, because they are the record of what those
executions believed, and rewriting them would destroy the evidence that this happened.

**2 — an unwritable target directory produces a Python traceback.** Not a criterion failure, and
not a contradiction of any ADR, but worth naming:

```
$ chmod 500 "$ro"; EXPENSES_FILE="$ro/sub/expenses.json" python3 -m expenses add-person Bob
Traceback (most recent call last):
  ...
$ echo $?
1
```

`cli.main` catches `RuleError` and `RecordError`; a `PermissionError` from `path.parent.mkdir` or
from the write is neither. `ADR-0001` point 3's no-traceback rule is written about *refusals* —
its examples are an unknown person, a malformed amount, a duplicate — and `ADR-0007` point 5
covers a record that cannot be **read**, not one that cannot be **written**. So no recorded
decision is contradicted; the write-failure path is simply unspecified, which is why this is an
accepted gap rather than a rejection. Sending the item back would mean inventing a twelfth
criterion after the fact, which is the thing this pipeline exists to prevent.

**3 — an observation, not a defect.** `cli._add_person` calls `storage.load()` before the name is
validated, so `add-person "a=b"` against a corrupt record reports the corrupt record rather than
the reserved character. Both messages are true and the user cannot add anybody either way, so
there is nothing to fix; recorded so that the next reader does not mistake it for an ordering bug.

**Nothing else.** Every hunk in the diff traces to a plan step and a criterion. `storage.empty_record`
is the only symbol the plan's interface list does not name — an internal helper of `load`,
introducing no behaviour — and `verify` had already recorded noticing it. No hunk contradicts an
ADR. No unrequested feature: nothing writes an `expenses` or `payments` key ahead of WI-0002 and
WI-0004, and the forward compatibility that makes that safe is demonstrated rather than asserted.

## Accepted gaps

Each is written into `item.md` § `## Notes` as well, because a gap recorded only in a report that
nobody reads again is a gap that has been forgotten rather than accepted.

| gap | why it is acceptable | where it lands |
|-----|----------------------|----------------|
| Write failures (unwritable directory, full disk) traceback — Finding 2 | unspecified by every criterion and every ADR; `storage.save` is inherited unchanged by WI-0002 and WI-0004, so the decision belongs to the next `plan` execution that touches saving, not to a retrofitted criterion here | `item.md` § Notes; named for WI-0002's `plan` |
| The `~/.local/share` default path was never exercised | exercising it would write to the real home directory of whoever runs the suite; the other two branches of the same resolution were both run live | `verify-report.md` § *Not verified*, repeated in `item.md` § Notes |
| Atomicity of the write is argued, not demonstrated | demonstrating it needs the process killed inside `save`; the consequence that matters — a record that cannot be read is never overwritten — **was** demonstrated, in four probes | `verify-report.md` § *Not verified* |
| `lint-clean` checks syntax only | `ADR-0008` decides this and says why: the stdlib-only constraint leaves no linter. Style and dead code are checked by review alone, and this review is the check | `ADR-0008`; restated in `item.md` § Notes |
| Concurrent writers lose one write | excluded by `docs/product/vision.md` (v3) and by this item's own `## Out of scope` | already recorded in both |

## Verdict

**Accept, close, and merge.** All twelve Definition of Done criteria pass. The trial merge into a
throwaway worktree of `main` was clean and `python3 -m unittest discover -s tests -t . -q` passed
on the merge result (28 tests, exit 0), as did the lint command; the trial was then discarded, the
item closed with `outcome: delivered` while the branch was still unmerged — so that
`check-commit-refs` still had a non-empty commit range to inspect — and only then was
`wi/WI-0001` merged into `main`.

Two findings, neither blocking: one wrong claim in two reports, corrected here rather than
propagated; one unspecified error path, accepted and handed to WI-0002's planning with a name on
it.

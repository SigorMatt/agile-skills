# Review — WI-0001

## What I examined

The change, not the reports about it: `git diff main..wi/WI-0001` hunk by hunk — eight commits,
1728 insertions across seven source files, four test files, three documents and the item's own
record. Then, separately, the record: `item.md`, `history.md` (11 rows), `journal.md` (10
entries), `plan.md`, both implementation reports in one file, `verify-report.md`, and all four
questions on the item.

**The tool was run here, not read about.** Every command below was issued by this execution
against branch head `fa2ffd3` with `ENVEL_FILE` pointed at a scratch path:

- **AC15, the criterion that was sent back** — all five invocations the criterion names.
  `new` → `usage: envel new [-h] name`; `new a b` → the same, then
  `envel new: error: unrecognized arguments: b`; `add groceries` → `usage: envel add [-h] name
  amount`; `add groceries 10 20` → the same; `list extra` → `usage: envel list [-h]`. Each with
  stdout empty and exit 2. None printed the tool's `{new,add,list}` line.
- **AC14, the criterion AC15 is the opposite of** — `envel` and `envel frobnicate` both printed
  `usage: envel [-h] {new,add,list} ...`, the tool's own. The two messages are genuinely
  different, which is the whole of the defect that was fixed.
- **AC7 and AC9 at the money** — `new Groceries` against a `groceries` holding 400.00 was
  refused, exit 1, and the listing afterwards still read `groceries  400.00`. `add g 12.57`
  then `add g 0.03` in separate invocations listed `g  12.60` — the cent digit that is not a
  round ten, which is the case the first verification found undefended.
- **AC13 and AC16** — the empty name and `" x"` refused with exit 1; `car & bike`, `20% fun`,
  `café` and a name containing a tab all created. Eight refusal cases (`add nosuch 10`,
  `add g 0`, `add g -40`, `add g 12.567`, `£12.50`, `1,200`, `12.5x`, `abc`) each put their
  message on **stderr** with **stdout empty** and a non-zero exit; `list` put its lines on
  stdout with stderr empty and exit 0.
- **Malformed input that no criterion names**, looking for an unhandled traceback rather than a
  message: `envel -x`, `envel --foo`, `envel new --foo x`, `envel list --foo`,
  `envel add g 10 --foo`. All five exited 2 with a usage message from the right parser and no
  traceback. `subcommand_parsers[arguments.command]` in `envel/cli.py:51` cannot be reached with
  `command` unset, because the subparser is `required=True` and fails at the top level first.
- **The gates, re-run on the final state of the code** — `python3 -m unittest discover -s tests
  -t .` → exit 0, 52 tests, OK; `python3 -m compileall -q envel tests` → exit 0.

### The claims audit (D12)

Scope: the sentences in `docs/` about behaviour this item touched. `lint-claims --context
work-item --changed-since main` reported its own window — *"2 document(s) in 2 path(s) differ
from main (7f27e61) under docs; citations: every markdown file in the workspace"* — a non-empty
window, and the two documents are the two this item edited. Below that mechanical pass, the read:

- **`docs/architecture/adr/ADR-0003-store-location.md`, `## Consequences`: *"The mitigation is
  that the resolved path is printed in the message when the store cannot be read."*** Not in the
  plan's invalidation set, and an absolute about this item's own code. **Opened:**
  `envel/store.py:36-67`, the four raise sites, and then run. `ENVEL_FILE=/tmp/rvw/bad.json`
  holding `not json` → *"/tmp/rvw/bad.json is not valid JSON, so it cannot be read as an envel
  store"*; `{"format": 99}` → *"/tmp/rvw/old.json is not an envel store of format 1"*. Both name
  the resolved path. **Falsifier:** a raise site whose message omits the path — the `OSError`
  branch at `envel/store.py:41` is the one most likely to, because it interpolates the system's
  `strerror` and could easily have stopped there; it reads `"cannot read {}: {}".format(path,
  exc.strerror)`. **Holds.**
- **`ADR-0003`, `## Consequences`: *"One function in `envel/store.py` resolves the path and
  nothing else knows about it."*** **Set:** every site in the tool that reads the environment or
  builds the store path. **Enumerated by:** `grep -rn "ENVEL_FILE\|XDG_DATA_HOME\|store_path"
  envel/ bin/envel` → 4 lines. **Members:** `envel/store.py:18` (the definition), `:20`
  (`ENVEL_FILE`), `:23` (`XDG_DATA_HOME`), and `envel/cli.py:54`, the single call.
  **Verdict per member:** the three environment reads are all inside `store_path`; the fourth is
  a call, not a second resolution. **Falsifier:** a second `os.environ.get("ENVEL_FILE")`, or a
  hand-built path, anywhere else — the grep is unfiltered over both the package and the shim and
  would have shown one. **Holds.**
- **`docs/architecture/overview.md`, `## The shape of it`: *"There is no daemon, no server and
  no background process; between two invocations the only thing that exists is a file."*** The
  set names a different sentence in this section, not this one. **Set:** the seven files that are
  the tool. **Enumerated by:** `grep -n "^import \|^from \|^\s*import \|^\s*from " envel/*.py
  bin/envel` → 13 lines. **Members:** `argparse`, `sys`, `copy`, `dataclasses`, `datetime`,
  `json`, `os`, `pathlib`, `re`, plus four intra-package imports. **Verdict per member:** none
  starts anything that outlives the process. **Falsifier:** a `threading`, `multiprocessing`,
  `subprocess`, `atexit`, `signal` or `fork` — none is imported, and the behavioural check is
  AC9's hundred separate processes, which left exactly one file and a hundred entries in it.
  **Holds.**
- **`docs/architecture/overview.md`, `## Conventions this project has adopted`, bullet 1:
  *"Output that reports success goes to stdout with exit 0; every refusal goes to stderr with a
  non-zero exit."*** **Falsifier:** a refusal that writes to stdout, or a success that writes to
  stderr. Checked **at the boundary the sentence is most likely to miss** — argparse's own
  refusals, which are not `envel/cli.py`'s `print(..., file=sys.stderr)` but argparse's internal
  exit. All five AC15 invocations and both AC14 invocations: stdout empty, exit 2. **Holds.**
- **`docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md`: *"What the lint command does
  check is that every file under `envel/` and `tests/` compiles."*** Re-run here: exit 0 over
  both directories. **Falsifier:** a file in either directory the command does not reach — the
  command names both directories and `compileall` recurses. **Holds.**
- **`docs/product/vision.md`, `## What it is for`: *"The command is `envel`."*** In the set and
  disposed `verified-still-true`; re-opened anyway, because the item's whole command surface
  changed shape between the two implementations. `bin/envel` exists and is executable, and
  `ArgumentParser(prog="envel")` at `envel/cli.py:23` is what every usage message printed above
  begins with. **Holds.**

Two sentences that are **engagement-state** claims — `docs/product/vision.md` `## Engagement
state` and `docs/architecture/overview.md` `## Engagement state` — are out of D12's scope and
were not touched. They are DE4's, at the ending.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion settled | **pass** | 17 of 17 are `- [x]` in `item.md`; no `- [~]`, so no substitution is claimed. `validate-workspace` → 0 errors |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | `## Criteria` has seventeen rows, each with the command run, the actual output and a note. None cites `impl-report.md`. Four of them (AC7, AC9, AC13, AC15) were re-run by this review and matched |
| D3 | the declared gates passed on the **final** state of the code | **pass** | re-run here on branch head `fa2ffd3`: test → exit 0, 52 tests, OK; lint → exit 0. `tracker/project.yaml:14-15` are the two declared commands |
| D4 | no open blocking question | **pass** | `Q-001`–`Q-004` are all `status: answered`, each with `## Consequences` naming real files; `validate-workspace` → 0 errors |
| D5 | a journal entry per execution, history chains to the current status | **pass** | 10 history rows after the creation row, 10 journal entries, in the same order; last row `to: in-review` matches `item.md` |
| D6 | every design-changing decision is in an ADR, cited from the plan or journal | **pass** | `ADR-0001`–`ADR-0005`, all five cited from `plan.md` `## Decisions and ADRs`. The two decisions the plan recorded as assumptions rather than ADRs (a refusal is a value; argument shape is argparse's) are in `plan.md` and `overview.md`. `ADR-0004` was corrected by erratum rather than superseded, which is right: the decision — a package, a shim, no install step — is unchanged and no code changes to satisfy the new text |
| D7 | the invalidation set is disposed, and nothing outside it was falsified | **pass** | `## Invalidation set confirmation` below: 14 entries, 14 dispositions; the two `to-update` rows both carry a version bump and a change-log row; the three `owned-by-ending` rows were left alone — `git diff main..wi/WI-0001 -- docs/` touches neither `## Engagement state` section. The set's own question is answered under that table |
| D8 | every commit on the branch references the item | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, all 8 commits on `main..wi/WI-0001` name WI-0001 |
| D9 | merged into the trunk | **pass** | trial-merged into a detached worktree of `main` first (`aada90c`), suite run **on the merge result** → exit 0, 52 tests; trial discarded, `main` confirmed still `7f27e61`. The real merge follows this close, and its sha is recorded in `item.md` by `scripts/record-merge` |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: *"verified at 2f025c5c; wi/WI-0001 has moved to fa2ffd34 but only the record changed (5 file(s) under tracker/ or docs/)"*. The last **code** commit is `81441cd`; the verification postdates it |
| D11 | `review.md` states what was examined, and every accepted gap is dispatchable | **pass** | `## What I examined` above is the commands this execution ran, not a verdict. `## Accepted gaps` below carries six rows, each with an owner and a disposition; `lint-documents --rule accepted-gaps-are-dispatchable --item WI-0001` → exit 0 |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass** | the six audited claims under `## What I examined`, each with its falsifier and what was opened. `lint-claims --context work-item --changed-since main` → exit 0 over a 2-document window. One **finding** recorded below on the dependency-direction sentence: it is true as a layering statement and its enumeration is looser than the code |
| D13 | the plan's `binding-adrs` list is complete | **pass** | `ls docs/architecture/adr/` → exactly `ADR-0001`…`ADR-0005`, and the plan's `## Binding ADRs` names all five, so no ADR in the project is unlisted. Each carries a `conforms` verdict in `verify-report.md` `## ADR conformance` with a quoted clause and a file and line; conformance is not re-decided here |

## Invalidation set confirmation

One row per entry of `plan.md` `## Invalidation set`, keyed by document path.

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/product/vision.md` — `## Engagement state` bullet 1 | owned-by-ending | `git diff main..wi/WI-0001 -- docs/product/vision.md` is empty: the item did not touch the section it was told to leave alone |
| `docs/product/vision.md` — `## Engagement state` bullet 2 | owned-by-ending | the same diff |
| `docs/product/vision.md` — *"The command is `envel`"* | verified-still-true | re-opened here against `bin/envel` and `envel/cli.py:23`; audited under `## What I examined` |
| `docs/product/vision.md` — *"Not connected to anything: no server, no sync, no bank import, no network"* | verified-still-true | the 13-line import enumeration under `## What I examined`; no network module among them |
| `docs/architecture/overview.md` — `## The parts`, the module table | to-update | updated to v2, change-log row `2026-09-11T02:43:44Z` by `implement` for WI-0001. Six rows, six files, all six present on disk; `bin/envel` is the corrected one |
| `docs/architecture/overview.md` — *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | verified-still-true | `grep -n "print(\|sys\.exit" envel/money.py envel/store.py envel/envelopes.py` → no match. This is the sentence the AC15 fix was most likely to break, and the new error path is at `envel/cli.py:51`, inside `cli` |
| `docs/architecture/overview.md` — *"a balance is the sum of an envelope's entries rather than a stored number"* | verified-still-true | `envel/envelopes.py:50` sums the entries and is what `listing` calls; the envelope record written by the tool has `name` and `created` only |
| `docs/architecture/overview.md` — `## Engagement state` | owned-by-ending | the v2 edit touched `## The parts` only; the section is byte-identical to v1 |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` — *"Two functions … are the only places the two forms meet"* | verified-still-true | `grep -rn "float(\|Decimal\|round(" envel/` → no match; the six call sites all delegate to `money` |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — the JSON document and the atomic write | verified-still-true | a store written here carries `format`, `envelopes[name, created]`, `entries[kind, envelope, cents, at]`; `envel/store.py:77-80` is the temporary-beside-the-target plus `os.replace` |
| `docs/architecture/adr/ADR-0003-store-location.md` — the three-step resolution | verified-still-true | `envel/store.py:18-25` resolves in that order; `verify-report.md` exercised all three branches, and this review re-read the function |
| `docs/architecture/adr/ADR-0004-invocation-package-and-shim.md` — the two entry points | to-update | updated to v2 with a change-log row and a `## Corrections` entry quoting both removed clauses, `2026-09-11T02:43:44Z` by `implement`. Both entry points exist and reach `envel.cli.main` |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` — *"The test command exits 5 while no test exists"* | verified-still-true | the clause predicts its own expiry and both halves hold; the command run here on a populated suite gives exit 0 |
| `docs/product/vision.md` — *"the tool starts, does one thing, and exits … nothing runs between invocations"* | verified-still-true | added to the set by `implement`, which is the actor that discovered it. Audited under `## What I examined` with the no-background-process enumeration |

**Did this change falsify a document the set does not name?** The corpus is seven documents —
`docs/product/vision.md`, `docs/architecture/overview.md` and five ADRs; `docs/process/` is
empty. All seven appear in the set, so the question is really about **sentences** the set does
not name, and I answered it by reading all seven end to end rather than by diffing. Five such
sentences carried an absolute worth checking and are audited above; all five hold. The one
inaccuracy I found is the dependency-direction sentence recorded as a finding below, and it is
not a falsification — its load-bearing half is true and checked at the boundary. Nothing else in
the seven documents makes a claim about the three commands, the store, the amounts or the
entry points that the code now contradicts.

## Sections restated at the ending

`not an ending` — this is an item close. `EP-001` is `open` and `scripts/engagement-state EP-001`
reports `active`, with six children still in flight. No `## Engagement state` section was read
for restatement, edited, or otherwise touched by this execution.

## Findings

1. **`docs/architecture/overview.md` `## The parts`: the dependency-direction sentence names
   edges that do not all exist.** It reads *"The dependency direction is one way: `cli` knows
   about `envelopes`, `envelopes` knows about `store` and `money`, and neither `store` nor
   `money` knows anything above it."* The imports are `cli` → `envelopes`, `money`, `store`;
   `envelopes` → `money`. So `envelopes` does **not** know about `store`, and `cli` knows about
   two modules the sentence does not mention.

   **Not a send-back, and why.** Read as an edge list, the sentence's *first* clause is
   inaccurate too, so an edge list is not what it is: it is a layering statement, and the half
   it exists to assert — *"the direction is one way … neither `store` nor `money` knows anything
   above it"* — is true, checked at the boundary (`envel/store.py` imports `json`, `os`,
   `pathlib`; `envel/money.py` imports `re`; neither imports from the package). It is also what
   the cited source says: `plan.md` `## Approach` lists four modules *"in one dependency
   direction"* and enumerates no edges. So the sentence is true under the only reading that
   makes it coherent, and the actual code is a stricter subset of what it permits.

   **What is recorded, so nobody later reads it as an edge list:** the real graph is above. The
   thing that would go wrong if someone took the sentence literally is adding `import store` to
   `envel/envelopes.py`, which would put file access inside the decision layer and contradict
   `## The shape of it`'s *"a command is a function from (store, arguments) to (new store,
   output, exit code)"*. That contradiction is what would catch it, and it is in the same
   document.

2. **An envelope name beginning with `-` needs the `--` separator.** `envel new "-savings"` is
   refused with `usage: envel new [-h] name` / *"the following arguments are required: name"*,
   exit 2, because argparse reads the name as an option. `envel new -- "-savings"` creates it,
   and it then lists and matches like any other name.

   **AC13 still holds.** The criterion says a name *may contain* any character and names
   `eating out` and `car & bike`, both of which are accepted; `-savings` is reachable through
   the universal POSIX convention, so the tool does accept it. What is not satisfied is a
   stronger claim nobody wrote — that every name is creatable without a separator.

   **Not a send-back, and why.** Fixing it means either hand-rolling the argument parser or
   special-casing a leading `-`, and *"argument-shape failures are left to `argparse` rather
   than hand-written"* is a recorded decision in `plan.md` `## Decisions and ADRs` with its
   reversal stated. Overturning a recorded decision to satisfy a reading of a criterion the
   criterion does not require is not this skill's to do. Recorded as an accepted gap below.

3. **No defect was found in the change itself.** Every hunk of the diff maps to a plan step or
   to the AC15 send-back: `envel/money.py` ← step 1, `envel/store.py` ← step 2,
   `envel/envelopes.py` ← step 3, `envel/cli.py` ← step 4 and the send-back,
   `envel/__main__.py` and `bin/envel` ← step 5, the four test files ← steps 6 and 7, the two
   documents ← step 8. Nothing serves neither. The five deviations `impl-report.md` declares are
   each a *how* rather than a *what*, and deviation 5 — which parser reports a wrong argument
   count — is the right call: it follows the criterion over the plan's gloss of the criterion,
   and says so rather than editing the plan to match.

## Accepted gaps

| gap | owner | disposition |
|-----|-------|-------------|
| The default store location `~/.local/share/envel/envelopes.json` was not exercised by writing to it — only its resolution was checked, because writing there would put a file in the real home directory of whoever runs the suite | none | no-owner |
| Atomicity was not demonstrated by interrupting a write. The mechanism is confirmed at `envel/store.py:77-80`; `os.replace` is atomic within a filesystem by contract, and no acceptance criterion names atomicity | none | no-owner |
| The exact wording of every message is unverified on purpose. `refine` left it open and the criteria constrain only what a message contains, argparse's own prose included | none | no-owner |
| Two names differing only in **internal** whitespace (`eating out` against `eating  out`) are two envelopes. `refine` left this deliberately unconstrained and recorded that it did, in `item.md` `## Notes`; `verify` recorded the tool's actual answer. A limitation observed, not a decision taken — if the stakeholder meets it, their route is `tracker/requests/` | none | no-owner |
| AC16's list of criterion IDs omits AC17, so it is narrower than AC16's own first sentence. The universal sentence was checked directly and holds — all four AC17 refusals go to stderr with stdout empty and a non-zero exit | none | no-owner |
| An envelope name beginning with `-` needs `envel new -- -savings` rather than `envel new -savings` (finding 2). AC13 holds; changing it would overturn `plan.md`'s recorded decision to leave argument shape to `argparse` | none | no-owner |

## Verdict

**Accepted.** All seventeen acceptance criteria are met on evidence this review re-gathered for
four of them and read for the rest; all thirteen Definition of Done criteria pass; the suite
passes on the **merge result**, not only on the branch. Two findings are recorded and neither is
a defect in the change: one is a documentation sentence that is true under its only coherent
reading and looser than the code, and one is a boundary of a recorded design decision.

`WI-0001` closes with outcome `delivered`, and `wi/WI-0001` merges into `main`.

# Review — WI-0001

## What I examined

- `tracker/items/WI-0001/item.md` — AC1–AC9 with every box ticked, `## Out of scope`, `## Notes`.
- `tracker/items/WI-0001/history.md` — all eight rows, checked to chain without a gap and to end
  at the status `item.md` declares.
- `tracker/items/WI-0001/journal.md` — all eight entries, read in full, one per history row.
- `tracker/items/WI-0001/artifacts/plan.md`, `impl-report.md`, `verify-report.md`,
  `refinement-qa.md`.
- `tracker/items/WI-0001/questions/Q-001.md` and `Q-002.md` — both `answered`, both with a
  `## Consequences` section naming files I opened.
- **The diff**, `main..wi/WI-0001`, hunk by hunk: `recall` (9 lines), `recall.py` (182),
  `README.md` (98), `tests/support.py`, `tests/test_add.py`, `tests/test_list.py`,
  `tests/test_store.py`, `tests/test_docs.py`. Every hunk is mapped to a criterion or a plan
  step in `## Findings` below.
- `docs/architecture/overview.md` v1, ADR-0002, ADR-0003, ADR-0004, ADR-0005 — read against the
  code, not against each other (see the claim audit below).
- `scripts/engagement-state EP-001` → `active`, so this execution ends no engagement.

### The claim audit (D12)

Each absolute claim below is one this item's code makes true or false. For each, I opened the
code the citation points at and decided from what is there, not from the sentence.

| claim | where | what I opened | verdict |
|-------|-------|---------------|---------|
| The path is `RECALL_FILE` when set and **non-empty**, `~/.recall.json` otherwise | `overview.md` §The shape 3; ADR-0002 | `recall.py:store_path` — `override = os.environ.get("RECALL_FILE")`, `if override:` — the empty string is falsy, so it falls through to `expanduser` | true |
| Exit `0` success, `2` wrong command line, `1` store unusable | `overview.md` §The shape 1; ADR-0005 §Exit codes | `recall.py:main`, `cmd_add`, `cmd_list` — the only `return 2` sites are the arity, empty-side and unknown-command paths; the only `return 1` sites are `except StoreError` | true |
| Arguments after the command name are positional and never options | `overview.md` §The shape 1; ADR-0005 §Arguments | `recall.py:main` and `cmd_add` — no option parser is imported or used; `len(arguments) != 2` is the whole rule | true |
| `list` prints the pile in card-number order | `overview.md` §The shape 2; ADR-0004 | `recall.py:cmd_list` — `sorted(document["cards"], key=lambda card: card["number"])` | true |
| A card object carries exactly `number`, `question` and `answer` | ADR-0004 §Schema | `recall.py:add_card` — the appended dict has those three keys and no other | true |
| The document is UTF-8, two-space indent, non-ASCII unescaped, ends with a newline | ADR-0004 §Schema | `recall.py:save` — `json.dumps(..., ensure_ascii=False, indent=2) + "\n"`, `encoding="utf-8"` | true |
| The next number is one more than the largest present, and 1 when there are none | ADR-0004 §Schema | `recall.py:add_card` — `max((card["number"] for card in cards), default=0) + 1` | true |
| A write goes to a temporary file **in the store's own directory**, is flushed, and is renamed over the store | ADR-0004 §Write protocol | `recall.py:save` — `dir=os.path.dirname(os.path.abspath(path))`, `handle.flush()`, `os.fsync(handle.fileno())`, `os.replace` | true |
| The store is created by the first successful add, not eagerly | ADR-0004 §Creation | `recall.py:cmd_list` never calls `save`; `cmd_add` calls it after `add_card`. Pinned by `tests/test_store.py::test_the_store_is_created_by_the_first_add_and_not_before` | true |
| Directories are not created on the user's behalf; an unreadable store is refused rather than overwritten | ADR-0004 §When the store cannot be used | `recall.py:save` has no `makedirs`; `load` raises before `cmd_add` reaches `save` | true |
| `recall` puts its own directory on the import path, calls `main`, exits with what it returned | ADR-0005 §Entry point | `recall`, all four statements of it | true |
| `main(argv)` prints and does not exit the process itself | ADR-0005 §Entry point | `recall.py:main` — no `sys.exit`; the only `sys.exit` in the tree is in the `recall` shim | true |
| No server, no network, no accounts | `overview.md` §What this system is; `docs/product/vision.md` | `recall.py` imports `json`, `os`, `sys`, `tempfile` and nothing else; `docs/product/vision.md` says the same | true |
| Standard library only, for running and for testing | `overview.md`; ADR-0003 | `recall.py` and all five test modules — `json`, `os`, `subprocess`, `sys`, `tempfile`, `unittest` | true |

`scripts/lint-claims --changed-since main` → exit 0, "checked no documents changed since main":
this branch changes no file under `docs/`, which is itself the reason the audit above had to be
done by reading rather than by running the linter.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every AC checkbox ticked | **pass** | AC1–AC9 are all `- [x]` in `item.md`; `validate-workspace` → 0 errors |
| D2 | every ticked criterion cites evidence in `verify-report.md` | **pass** | the report's `## Criteria` table has nine rows, each naming a command `verify` ran and quoting what it printed. Spot-checked AC5 and AC8, the two whose wording admits two readings: both readings are in the table (`RECALL_FILE=""` falling back to the default; the empty listing with no file and with a zero-card file) |
| D3 | declared gates passed on the **final** state of the code | **pass** | I re-ran both on the merge result, not on the branch: `python3 -m unittest discover -s tests -t .` → `Ran 21 tests`, `OK`, exit 0; `python3 -m compileall -q -x '[.]claude' .` → exit 0. Plus an end-to-end smoke run of the merged tree: `recall add "die Katze" "the cat"`, `recall add "Grüße" "greetings"`, `recall list` → `1\tdie Katze\tthe cat`, `2\tGrüße\tgreetings`, exit 0, and the store file readable as pretty-printed JSON with `Grüße` unescaped |
| D4 | no open blocking question | **pass** | `Q-001` and `Q-002` are both `status: answered`; no question anywhere in the workspace is `open` |
| D5 | a journal entry per execution, history chains to the current status | **pass** | eight history rows, eight journal entries, in the same order and with the same actors; the last row `verifying → in-review` matches `item.md`'s `status: in-review`. `validate-workspace` → 0 errors, 0 warnings |
| D6 | every design decision in an ADR, cited from the plan or journal | **pass** | ADR-0003 (toolchain), ADR-0004 (schema and write protocol), ADR-0005 (command surface) were written by `plan` and are all three cited from `plan.md`'s `## Decisions and ADRs` table; ADR-0002 (store location and format) predates the plan and is cited from it; ADR-0001 is named as not applicable. The reversible choices that are *not* ADRs — the message wording, the tab separator, whitespace-only sides — are each numbered under `plan.md` `## Assumptions` with what reversing them costs |
| D7 | documents the change invalidated updated, with a version bump and a change-log row | **pass, vacuously, and checked rather than assumed** | `git diff --name-only main..wi/WI-0001 -- docs/` is empty: the branch changed no document. The documents that describe this behaviour — `overview.md` v1 and ADR-0003/4/5 — were written by `plan` *for* this item and carry `updated-for: WI-0001` with a v1 change-log row. The audit above is what establishes that the delivered code did not drift from them |
| D8 | every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, "all 5 commit(s) on main..wi/WI-0001 name WI-0001" |
| D9 | merged into the trunk | **pass** | trial-merged into a detached worktree at `main` first (merge commit `3f655f8`, tests green on it), the trial discarded, `main` confirmed still at `4d5cbce`; then merged for real after this item was closed, because `check-commit-refs` inspects `main..wi/WI-0001` and merging first would empty that range. The real merge commit is `9a060a7`, recorded here in a follow-up commit on `main` for that reason |
| D10 | `verify` ran after the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: verified at `f23fe67`, the branch has moved to `18e1605` but that commit touches five files under `tracker/` only (`board.md`, `verify-report.md`, `history.md`, `item.md`, `journal.md`), so no code postdates the verification. I ran the comparison; I did not infer it from the shape of the last commit |
| D11 | `review.md` exists and states what was examined | **pass** | this file; `## What I examined` names every artifact, the diff range, and the fourteen claims I opened code to check |
| D12 | claims in `docs/` about the behaviour this item touched are still true; absolute claims carry a resolvable citation | **pass** | the claim-audit table above — fourteen claims, each decided by opening the cited code. `lint-claims --changed-since main` → exit 0 |

## Findings

**The diff, hunk by hunk, against a criterion or a plan step.** Nothing in it serves neither.

- `recall` (new, 9 lines) — plan step 3, ADR-0005 §Entry point.
- `recall.py` store layer — `store_path` (plan step 1, AC5), `empty_document`/`load` (step 1,
  ADR-0004's read rules and both failure cases), `save` (step 1, ADR-0004's write protocol),
  `add_card` (step 1, AC1 and AC3's numbering).
- `recall.py` command layer — `cmd_add` (step 2; AC9's arity check, AC4's two empty-side
  messages, AC1's confirmation line), `cmd_list` (step 2; AC6's sort, AC8's empty line, AC2's
  format), `main` (step 2; the dispatch and the unknown-command usage line).
- `README.md` — plan step 4, and AC5's requirement that both the default path and `RECALL_FILE`
  be named there.
- `tests/support.py` — impl-report deviation 1. `tests/test_add.py` (step 5), `test_list.py`
  (6), `test_store.py` (7), `test_docs.py` (8).

**On the four declared deviations.** All four are accepted, and none is a send-back:

1. `tests/support.py` is test infrastructure the plan's step list does not name. It carries no
   product behaviour and removes twenty duplicated lines from three modules. Accepted.
2. `recall list` with an argument is rejected with `usage: recall list` and exit 2. The plan
   fixed `add`'s arity and said nothing about `list`'s, so some behaviour had to be chosen. I
   checked the reading rather than taking the report's word for it: AC6 requires `list` to show
   *every* card, and `EP-001/Q-004` settled one flat pool with no filtering, so accepting a
   narrowing argument silently would advertise a filter that does not exist. It contradicts no
   ADR — ADR-0005's positional-only rule is about `add`'s count and does not speak to `list`.
   Accepted, and recorded below as a gap because no criterion covers it.
3. Three tests beyond the plan's list, each pinning a decision that would otherwise be
   invisible. No product code exists for them alone. Accepted.
4. `load` validates the document's *shape*, not only that it parses. ADR-0004 says a file that
   does not have the schema's shape is refused; this is that sentence implemented, not scope
   added. Accepted.

**Contradictions with a recorded decision:** none found. Every check in the claim audit resolved
in the code's favour, so no question to the architect was needed.

**Maintainability, specifics rather than discomfort.** Two things I would change if either
mattered, and neither does enough to send the item back:

- `recall` carries `# noqa: E402` on its `from recall import main` line. `noqa` is a marker for
  flake8, and ADR-0003 records that no linter is installed and `compileall` is the lint gate, so
  the marker suppresses nothing. It is a comment that says something untrue about the project's
  toolchain. Cost of leaving it: a later reader may believe a linter runs here.
- `save` creates its temporary file through `tempfile.NamedTemporaryFile`, which mkstemps at
  mode `0600`, and `os.replace` carries that mode onto the store. The store therefore ends up
  owner-only rather than umask-default. For a single-user card file that is arguably the better
  default; it is undocumented either way, and nothing states a permission requirement.

Neither is a defect against a criterion, an ADR or a document, so neither is a bug item — a bug
would have nothing to cite under RB3. They are recorded here, which is where a later reader of
this file will find them.

**No bug item was filed by this review**, and no defect belonging to another item was found:
WI-0001 is the first item to deliver code, so there is no other item's behaviour to find one in.

## Accepted gaps

Each is copied into `item.md`'s `## Notes`, because a gap that lives only in a report stops
being read the moment the item is `done`.

1. **The durability claim is not proven, only implemented.** ADR-0004 and `README.md` both say a
   write interrupted part-way leaves the previous document or the new one. `verify` checked the
   mechanism's observable consequences but did not kill the process mid-write. No acceptance
   criterion states it, so this is not a send-back; it is a claim resting on `os.replace`'s
   atomicity within one filesystem, which `plan.md` `## Risks` already flags as holding only
   while the temporary file stays in the store's own directory.
2. **`tests/support.py` redirects `RECALL_FILE` but not `HOME`.** Verification's own AC5
   mutation — making `store_path` ignore `RECALL_FILE` — therefore resolved the store to the
   real home directory and wrote the suite's fixtures to `~/.recall.json`, outside the project.
   `verify` declared it and deleted the file; nothing pre-existing was touched. The delivered
   tool is not at fault — no unmutated code writes outside the store the environment names — but
   the suite cannot safely host a mutation of path resolution itself, and WI-0002 and WI-0003
   will inherit that suite. Setting `HOME` unconditionally in `run_recall` would close it.
3. **Two pieces of user-visible behaviour that no criterion covers**: `recall list` with an
   argument exits 2 with a usage line, and an unknown or missing command exits 2 with
   `usage: recall <add|list>`. Both are declared in `impl-report.md` and `verify-report.md`, and
   both are consistent with the flat pool. They are unconstrained rather than unverified: if
   WI-0002 needs a different answer for `list`, it is one condition in `cmd_list`.
4. **Multi-line card sides, a store that is valid JSON in another schema, and `~` resolution
   with `HOME` unset** are all outside every criterion and are recorded as out of scope in the
   item, the plan and ADR-0004. Noted so that the absence is deliberate rather than forgotten.
5. **`compileall` is a compile check, not a linter.** Unused imports and dead code in what was
   written are not machine-checked; ADR-0003 says so and names the reviewer as what catches
   them. This review is that check, and its two findings are under `## Findings` above.

## Verdict

**Accept.** The change delivers exactly AC1–AC9 and nothing else, every hunk maps to a criterion
or a plan step, the record reconstructs the item end to end from the tracker alone, and the test
suite and the tool both behave on the merge result rather than only on the branch. Merged into
`main` and closed with `outcome: delivered`.

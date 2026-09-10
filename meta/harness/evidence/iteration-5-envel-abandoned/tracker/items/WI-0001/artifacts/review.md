# Review — WI-0001

## What I examined

The branch `wi/WI-0001` at `26b1be6`, the diff `main..wi/WI-0001` hunk by hunk, and the whole of
the item's record: `item.md`, all ten rows of `history.md`, all ten entries of `journal.md`,
`plan.md`, `impl-report.md`, `verify-report.md`, and `Q-001`, `Q-002` and `Q-003`. The four ADRs
under `docs/architecture/adr/`, `docs/architecture/overview.md` v2, `docs/process/ways-of-working.md`
v1 and `docs/product/vision.md` v2.

**The diff, hunk by hunk.** Fifteen paths. `envel/store.py`, `envel/envelopes.py`, `envel/cli.py`
and `bin/envel` are plan steps 1–4; `tests/test_envelopes.py` and `tests/test_cli.py` are steps 5
and 6; `docs/architecture/overview.md` is step 7 and invalidation row 3;
`docs/process/ways-of-working.md` is invalidation row 2, written by `answer-questions` when it
answered `Q-003`; `envel/__init__.py` and `tests/__init__.py` are the two scaffolding files the
plan declares under `## Scaffolding`, both empty. The remaining five are this item's own tracker
record. **No hunk fails to trace to a criterion or a plan step.**

**What I ran myself, rather than reading about:**

- the trial merge into a detached worktree of `main`, `{{trunk}}` unmoved before and after
  (`ff0022f` → `ff0022f`), the suite green **on the merge result**, and `compileall` clean there
  too;
- `envel new "  eating out  "` on a fresh store, to see the half of AC11 the end-to-end suite
  does not reach — listed as `eating out`, stored as `"name": "eating out"`;
- the non-UTF-8 locale boundary that plan assumption P5 and `## Risks` both name. It fails, and it
  fails somewhere neither of them predicted. That is `BUG-0001`;
- the two boundary checks the ADR claims below turn on: breaking `bin/envel` and breaking a file
  under `envel/`.

### The claims audit (D12)

Every absolute claim in `docs/` about behaviour this item touched, decided by opening what it
cites — not by reading the sentence or a neighbour repeating it. Engagement-state sentences are
out of scope here and belong to the ending (`doc-header.md` §4a).

**Claim 1 — `ADR-0001`: *"This project is written against the Python 3 standard library and
declares no third-party dependency, for its runtime, its tests or its checks."*** Quantified, so
the audit owes the enumeration rather than the citation.
- **Set:** every `import` and `from ... import` in the delivered code.
- **Enumerated by:** an `ast` walk over `envel/**.py`, `tests/**.py` and `bin/envel`, testing each
  top-level module against `sys.stdlib_module_names` → `non-stdlib, non-local imports: none`.
  Plus `ls | grep -iE "requirements|pyproject|setup.py|Pipfile"` → no dependency manifest of any
  kind at the repository root.
- **Members:** `json`, `os`, `tempfile` (`envel/store.py:9`–`:11`); `sys` (`envel/cli.py:11`);
  `__future__` (`envel/envelopes.py:7`, and two others); `os`, `subprocess`, `tempfile`,
  `unittest` (`tests/test_cli.py:9`–`:12`); `unittest` (`tests/test_envelopes.py:3`); `os`, `sys`
  (`bin/envel:4`–`:5`); and the local `envel` (`envel/cli.py:13`, `tests/test_envelopes.py:5`,
  `bin/envel:9`).
- **Verdict:** every member is standard library or local. **Holds.**
- **Falsifier:** a single third-party name anywhere in that set, or a manifest declaring one. The
  walk reads every import node rather than the ones I expected, so a dependency added in a test
  helper — the place it would most plausibly hide — would have appeared.

**Claim 2 — `ADR-0001`: *"`bin/envel` has no `.py` extension, so `compileall` does not see it …
every end-to-end test invokes the tool through it, so a launcher that will not parse fails the
test suite rather than passing the lint."*** Two absolutes, and one of them is the interesting
kind: a claim that a check would catch something.
- **Checked at the boundary, not by reading:** `bin/envel` was replaced with `def f(:` and the
  suite run. `python3 -m unittest discover -s tests -t .` → **exit 1, 10 failing cases**;
  `python3 -m compileall -q envel tests` → **exit 0**, seeing nothing wrong. Restored.
- **Verdict:** both halves **hold**, and precisely as stated — the lint is silent and the suite is
  not.
- **Falsifier:** a suite that stayed green with a broken launcher, which is exactly what would
  happen if any end-to-end test imported `envel.cli` and called `main()` instead of running the
  process. `grep -rn "cli.main\|from envel import cli"` over `tests/` → none, and there is exactly
  one `subprocess.run` site in the whole suite (`tests/test_cli.py:28`), invoking the bare word
  `envel`. So the thing that would have said no was looked for and is absent.

**Claim 3 — `ADR-0001`: *"It becomes meaningful the moment `envel/` contains a file, and nothing
rests on it before then."*** Written when `envel/` was empty; this item is what made the
antecedent true, so this is the audit that could not have been done before.
- **Checked at the boundary:** `envel/_broken.py` containing `def f(:` was added and
  `python3 -m compileall -q envel tests` run → **exit 1**, `*** Error compiling
  'envel/_broken.py'`. Removed; the command returns to exit 0.
- **Verdict:** **holds.** The lint that was vacuous at v1 of the ADR now bites.
- **Falsifier:** exit 0 on a file that will not parse, which is what `compileall` does for a
  *missing* directory and is the failure mode the ADR itself documents.

**Claim 4 — `ADR-0003`: *"The file is written UTF-8 with `ensure_ascii=False`, so a name is
stored as the characters the person typed. `json` escapes whatever needs escaping, which is what
makes the format survive a name the stakeholder was promised we would not restrict."***
- **Opened:** `envel/store.py:66` — `json.dump(store, stream, ensure_ascii=False, indent=2)` into
  a stream opened `encoding="utf-8"` at `envel/store.py:65`. And a real store the tool wrote:
  `{"version": 1, "envelopes": [{"name": "eating out"}]}`, and one holding `café`, read back
  correctly.
- **Verdict: holds as written, and is incomplete in a way that matters.** The sentence is about
  what the *format* can carry, and it can: a name reaching `json.dump` as a `str` is stored
  verbatim. What this audit found at the boundary is that under a locale which decodes `argv` with
  surrogate escapes, the name never arrives as a valid `str`, and the **write** raises an
  unhandled `UnicodeEncodeError` — so the reader's natural inference, *"therefore a name the
  stakeholder types will be stored"*, does not follow. I am recording that as `BUG-0001` rather
  than as a false sentence, and saying so here so the distinction is visible rather than
  convenient.
- **Falsifier:** a name that reaches `json.dump` and is not stored as typed. I looked for one at
  the point where it would exist — the encoding boundary — with the coercion Python 3.12 applies
  by default switched off, and what turned up was a failure one layer earlier. That is a
  falsifier that fired, on a neighbouring claim, which is why the plan's `## Risks` sentence
  *"the store itself is safe … this is a display failure and not a data one"* is quoted in
  `BUG-0001` as wrong.

**Claim 5 — `ADR-0003`: *"Every demonstration of an acceptance criterion sets `ENVEL_FILE` to a
path in a temporary directory."*** Quantified.
- **Set:** the 12 end-to-end test functions in `tests/test_cli.py`.
- **Enumerated by:** `grep -c "    def test_" tests/test_cli.py` → 12, and
  `grep -c "self.envel(" ` → 30 call sites, all through the one helper at `tests/test_cli.py:24`,
  which sets `ENVEL_FILE` at line 27 from `setUp`'s `tempfile.TemporaryDirectory()` at line 20.
- **Verdict:** **holds.** There is no second path to the tool.
- **Falsifier:** a test calling `subprocess.run(["envel", ...])` with its own environment, or none.
  There is exactly one `subprocess.run` in the suite and it is inside the helper.

**Claim 6 — `ADR-0004`: *"The stored display form is the trimmed name, so `  groceries  ` and
`groceries` are one envelope and the stored form of both has no surrounding space."***
- **Checked by running it**, not by reading `display`: `envel new "  eating out  "` on a fresh
  store → exit 0, `envel list` → `eating out`, and the store file holds `"name": "eating out"`.
  Then `envel new "  groceries  "` after `envel new groceries` → exit 1, one line in `list`, no
  surrounding space.
- **Verdict:** **holds**, both halves.
- **Falsifier:** a store file containing `"  eating out  "`, which is what the sentence denies and
  what M3 produces when `strip` is removed. I opened the store file rather than the listing,
  because the listing would have looked identical for a trailing space.

**Claim 7 — `docs/architecture/overview.md` `## The shape` and the dependency-direction
sentence.** `verify` reopened all ten citations; I re-ran the two that are claims rather than
pointers. *"`envelopes` imports neither `os` nor `store`"* — `envel/envelopes.py` contains exactly
one import, `from __future__ import annotations` (`envel/envelopes.py:7`). *"`store` names no
envelope rule"* — `envel/store.py` mentions no envelope concept; its vocabulary is paths,
documents and shapes. **Holds.**

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every acceptance criterion checkbox settled | **pass** | eleven `- [x]` in `item.md`, no `- [ ]` and no `- [~]`. `grep -c "^- \[x\] AC"` → 11 |
| D2 | every ticked criterion cites its evidence in `verify-report.md` | **pass** | `## Criteria` carries a `command run` and an `actual output` column for each of AC1–AC11, and the outputs are `od -c` and `cmp` results where the criterion says "only content" or "byte-identical" |
| D3 | declared gates passed on the final state of the code | **pass** | `verify` ran its nine on `6aacc95`; this review re-ran the suite and `compileall` on the branch head and again **on the merge result**. The one gate recorded `fail` — `implement`'s `claims-are-sourced` — is the forced one, and it is about a document, not the code |
| D4 | no open blocking question | **pass** | `Q-001`, `Q-002`, `Q-003` all `status: answered`. `Q-004`, filed by this review, is `blocking: false` |
| D5 | a journal entry per execution, history chains without a gap | **pass** | ten history rows, ten journal entries, timestamps in step; the last row `verifying → in-review` matches `item.md`'s `status: in-review`. Every actor in the chain — `intake`, `refine`, `answer-questions`, `refine`, `plan`, `implement` ×3, `answer-questions`, `verify` — has its entry |
| D6 | every design-changing decision in an ADR, cited from plan or journal | **pass** | four ADRs, all four cited in `plan.md` `## Decisions and ADRs` with the branch of the preference order each took. The six choices that are **not** ADRs are recorded as assumptions P1–P6 with their reversal cost, which is the plan procedure's other legal route; each is one file to reverse |
| D7 | invalidation set disposed, and did this change falsify a document the set does not name | **pass** | see `## Invalidation set confirmation` |
| D8 | every commit references the item ID | **pass** | `scripts/check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 7 commit(s) on main..wi/WI-0001 name WI-0001` |
| D9 | merged into the trunk | **pass** | trial-merged first into a detached worktree of `main`: clean merge, `Ran 24 tests`/`OK` and `compileall` exit 0 **on the merge result**, trial head `17993b5`. Trunk unmoved across the trial (`ff0022f` before, `ff0022f` after). The real merge follows this close, and its sha is recorded by `scripts/record-merge` |
| D10 | verification postdates the last code change | **pass** | `scripts/check-verify-freshness WI-0001 wi/WI-0001` → exit 0: verified at `6aacc95`, branch has moved to `26b1be6` but **only the record changed**. Run, not judged by eye |
| D11 | `review.md` exists and states what was examined; every accepted gap has an owner and a dispatchable disposition | **pass** | this document; `## What I examined` is its first section, and `## Accepted gaps` disposes all four rows |
| D12 | every claim in `docs/` about the behaviour this item touched is still true | **pass**, with one incompleteness recorded | seven claims audited above from their citations, each with a falsifier, two of them checked at a boundary I created deliberately. Claim 4 holds as written and its natural inference does not; `BUG-0001` carries that |
| D13 | the plan's `binding-adrs` list is complete | **pass** | four ADRs exist in the workspace (`docs/architecture/adr/` — `ADR-0001` … `ADR-0004`) and the plan names all four. The diff was read against each: the standard-library clause binds every file, the launcher clause binds `bin/envel`, the store clause binds `envel/store.py`, the identity clause binds `envel/envelopes.py`. There is no fifth ADR for the list to have missed, and the degenerate failure this criterion exists to catch — a plan that listed nothing — is not what happened. Conformance per ADR is `verify`'s and is in `verify-report.md` `## ADR conformance`, not re-decided here |

## Invalidation set confirmation

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/product/vision.md` | `owned-by-ending` | The item left it alone, which is the whole obligation: `git diff main...wi/WI-0001 -- docs/product/vision.md` is **empty**. Its `## Engagement state` bullets are false today and are not this item's to repair — they are restated at the ending (DE4). This close touched nothing in that file |
| `docs/process/ways-of-working.md` | `to-update` | Exists at `version: 1` with a `## Change log` row for v1 naming `answer-questions` and WI-0001, which is the version-bump-and-row obligation in its create-shaped form (`doc-header.md` §3). Reopened: its subject is `Q-003`, and both its `[src:]` citations resolve |
| `docs/architecture/overview.md` | `to-update` | Updated to `version: 2` with a `## Change log` row for v2 naming `implement` and WI-0001. `verify` reopened all ten citations with `sed -n`; this review re-checked the two sentences that are claims rather than pointers — see claim 7 above |

**Did this change falsify a document the set does not name?** The set is enumerable and I
enumerated it: `find docs -name "*.md"` → **seven** documents. Three are named by the set. The
four not named are `ADR-0001` … `ADR-0004`, and every one of them was opened and read against the
delivered code — claims 1, 2, 3, 4, 5 and 6 above are that read, plus each ADR's `## Consequences`
in full. Two of those ADRs make claims that were **vacuous when written and became checkable
because of this very change** (`ADR-0001`'s "it becomes meaningful the moment `envel/` contains a
file"; `ADR-0002`'s "a launcher that will not parse fails the test suite"), which is exactly the
shape of thing this question exists to catch — and both were checked by breaking the code and
watching the check fire, then restoring it. **No document outside the set was falsified.** The
one thing this change did to an unnamed document is make two of its sentences true in a way they
had not been before.

## Sections restated at the ending

Not an ending. WI-0001 is a work item and EP-001 remains `open` with five children in flight
(`scripts/engagement-state EP-001` → `active`). No `## Engagement state` section was written, and
the one that exists — in `docs/product/vision.md`, the only one in the workspace — was not
touched by this close. `scripts/lint-documents --rule engagement-state-is-restated --item WI-0001
--context work-item` says so itself: *"NOT APPLICABLE — an item close is not an ending"*.

## Findings

None that send the item back. Three worth recording, in descending order of consequence.

1. **`envel new` on a non-ASCII name raises an unhandled `UnicodeEncodeError` and prints a
   traceback**, under a locale that decodes `argv` with surrogate escapes. Filed as **`BUG-0001`**
   at `ready`, `found-in: WI-0001`, with the exact reproduction and the verbatim traceback. Not a
   send-back, because no WI-0001 criterion covers a non-ASCII name — AC8 covers a space, and the
   stakeholder's *"don't restrict the characters"* lives in `Q-002` and the item's `## Notes`. Two
   details are worth the reader's attention: the store is **not** corrupted (the temporary file is
   discarded, `os.replace` never runs, so `ADR-0003`'s atomic-write decision holds under the
   failure it was written for), and the plan predicted this area and predicted the **wrong
   failure** — P5 and `## Risks` both call it a display problem, and `envel list` under the same
   locale is fine.
2. **`ADR-0002`'s `## Decision` says the launcher is "four statements" and `bin/envel` contains
   five.** `verify` recorded it and I agree with its verdict: the four *acts* the clause names are
   each satisfied and each cited, so the decision holds and the count is an aside. Recorded rather
   than acted on, because `review-close` does not supersede ADRs and this is not a contradiction
   between the change and the decision — it is a loose sentence in the decision's own prose. If
   anyone tightens it, the route is `doc-header.md` §4b: a `provenance` row in `## Corrections`, a
   change-log row and a version bump, not a silent edit.
3. **Three copies of one error-handling clause in `envel/cli.py`.** `print(f"envel: {problem}",
   file=sys.stderr); return REFUSED` appears at `envel/cli.py:47`, `:61` and `:71`. At three
   copies and eight lines apart this is not worth a round; I name it because WI-0002, WI-0004 and
   WI-0005 each add a command, and the copy count grows with them — this is the hunk that will
   drift, and the drift will be a command whose store error prints differently from the others.
   The shape that fixes it is a decorator or a small `_with_store` helper, and it is the sort of
   thing WI-0002's plan should decide **before** there are six copies rather than after. No item
   filed: nothing is wrong today, and inventing an item for a refactor nobody has needed yet is
   the scope creep this review is supposed to catch, not commit.

Read for maintainability and found nothing else worth naming: the error paths report rather than
swallow (`_discard` at `envel/store.py:76` is the one deliberate swallow, and it is cleanup after
a failure that is already being raised), the names say what is true, and the domain module holds
no filesystem access so the rules stay testable without one.

## Accepted gaps

| gap | owner | disposition |
|-----|-------|-------------|
| Behaviour under a non-UTF-8 locale — declared in `verify-report.md` `## Not verified, and why` and in `impl-report.md` `## What I did not do` as plan assumption P5 | `BUG-0001` | `item-filed:BUG-0001` |
| `store_path`'s XDG and home branches are exercised by no test; every one of the 24 reaches the store through `ENVEL_FILE` | `answer-questions` | `question-filed:WI-0001/Q-004` |
| Nothing end-to-end creates an envelope from a name with surrounding whitespace — AC11's storage half, exposed by `verify`'s mutation M3 and demonstrated by hand in this review | `answer-questions` | `question-filed:WI-0001/Q-004` |
| The exact wording of the messages in AC5, AC6, AC9, AC10 and AC11 is verified against nothing, because no criterion fixes it. Plan assumption P1 owns the wording and records the reversal cost as one file; the criteria deliberately fix the stream and the exit status and leave the sentence open, so this is a decision the item recorded rather than work deferred | `none` | `no-owner` |
| Two `envel` processes writing at the same instant can lose one of the two writes. `plan.md` `## Risks` records it, the vision scopes the product to one person at one terminal, and no criterion mentions concurrency — a limitation, stated | `none` | `no-owner` |

## Verdict

**Accept.** WI-0001 delivers what was asked: two commands, a store that outlives the process, and
eleven criteria each demonstrated by a command with its output in the record. The change merges
cleanly into `main`, the suite passes on the merge result, and the record is one a person who was
not here could follow from the idea through three stakeholder answers, one architect answer, four
ADRs, a forced gate with its reasons written down, and an independent verification with six
mutations behind it.

It closes with one defect filed against it (`BUG-0001`), one open non-blocking question
(`Q-004`), and one gate that has been failing since `implement` and is not this item's to clear —
`claims-are-sourced` over an engagement-state sentence in `docs/product/vision.md` that
`review-close` restates at the ending. At **this** close the gate passes, because an item close
scopes the audit to the item's own diff: `scripts/lint-claims --context work-item --changed-since
main` → exit 0 over the two documents this branch actually wrote.

Outcome: `delivered`.

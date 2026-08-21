# Review — WI-0001

Reviewed-at: 2026-08-21T03:39:41Z
Reviewed-commit: 4b04b42 (branch `wi/WI-0001`; code at `fcf3cf4`, the two commits on top touch
`tracker/` only)
Diff range read: `main...wi/WI-0001`

> **Third review.** The first (2026-08-21T03:08:15Z) rejected the item on two findings; the second
> (2026-08-21T03:23:10Z) rejected it on four, one of them a direct AC8 violation, and unticked AC8.
> This review re-examines the whole change, not only the fixes: the diff hunk by hunk, the record
> end to end, and the behaviour, run here on inputs chosen to be ones no earlier pass tried. The
> previous review's `## Accepted gaps` is carried forward, amended, and extended — those gaps live
> in `item.md`, and one of them is now closed by evidence rather than by assertion.

## Verdict

**Accept — merge and close, `outcome: delivered`.**

Twelve Definition of Done criteria applied one by one: eleven pass outright, one (D6) passes with
a caveat that is recorded rather than waved through. No criterion of this item fails. Nothing in
the diff is unrequested scope. Four gaps were declared by `verify` or `implement` and are decided
here — one is closed by evidence I gathered, three are accepted and written into `item.md`.

This is an acceptance after two rejections, so it is worth being explicit about what changed my
mind rather than letting three rounds read as attrition: the second review's F1 was a class of
input — a store that **passes** `store.load()` and breaks above it — and the fix moved the check
into `store`, where it covers every present and future caller at once. I went looking for more of
that class (`## Behaviour I ran`) and did not find another instance.

## What I examined

- `item.md` — the eight criteria, `## Notes`, `## Accepted gaps`, `## Deliberately unconstrained`,
  in full.
- `history.md` — thirteen transition rows, chaining without a gap from `— → draft` to
  `in-review`, timestamps non-decreasing, last row matching `item.md`'s `status`.
- `journal.md` — all thirteen entries, read end to end, against the executions the history
  implies. The count matches exactly (see D5).
- `plan.md` — steps 1–8, the acceptance-criteria mapping, the four assumptions, and
  `## Out of scope for this item`.
- `impl-report.md` — all three passes, including each `## What I did not do` and each
  `## Deviations from the plan`.
- `verify-report.md` — the third verification, including `## Not verified, and why` in full, which
  is where three of the four gaps decided below come from.
- `questions/Q-001.md`, `questions/Q-002.md` — both `status: answered`, `answered-by: human`,
  `## Consequences` naming files that exist and that carry the answers.
- `docs/architecture/overview.md` **v2**, `ADR-0001` §4–5, `ADR-0002` decisions 1–7, `ADR-0006`
  decisions 1–6 — each read **against the code**, not remembered (D12; the readings are in D12's
  evidence row).
- **The diff**, `git diff main...wi/WI-0001`, hunk by hunk: 17 files, of which 10 are code, docs
  or tests. Every code hunk mapped to a criterion or a plan step; the mapping is below.
- **Behaviour, run by this skill** — 20 invocations against stores I wrote by hand, plus the
  eight-criterion spot check. See `## Behaviour I ran`.
- The trial merge and the suite on its result.

### Every code hunk, mapped

| file | serves |
|------|--------|
| `expenses/__init__.py` | `plan.md` step 1 — the package |
| `expenses/__main__.py` | `plan.md` step 1; AC1 (`python3 -m expenses` is the invocation, `ADR-0006` decision 1) |
| `expenses/errors.py` | `plan.md` step 2; AC8 — the single expected-failure type. Its docstring was corrected in the third pass and no longer makes F3's false claim |
| `expenses/store.py` `store_path()` | `plan.md` step 3; `ADR-0002` decisions 1–2 |
| `expenses/store.py` `empty()`, `load()` | `plan.md` step 3; AC4, AC5, AC6; `ADR-0002` decisions 4–6. The element-type loop is F1's fix |
| `expenses/store.py` `save()` | `plan.md` step 3; AC5; `ADR-0002` decisions 4, 7 |
| `expenses/people.py` `normalise()` | `plan.md` step 4; AC3, AC7; `ADR-0006` decisions 4–6 |
| `expenses/people.py` `match_key()` | `plan.md` step 4; AC3. Losing the `normalise` call is F2's fix |
| `expenses/people.py` `add()`, `listing()` | `plan.md` step 4; AC1, AC2, AC3 |
| `expenses/cli.py` | `plan.md` step 5; AC1, AC4, AC6, AC7, AC8. The second handler is F3's fix and a declared deviation from step 5 |
| `tests/test_store.py`, `tests/test_cli.py` | `plan.md` steps 6–7 |
| `docs/architecture/overview.md` → v2 | F3; D7 |

No hunk is unrequested scope. The one departure from a signature `plan.md` declares — `main`'s
`out`/`err` parameters — was accepted by the previous review as F4 and is in `item.md`
`## Accepted gaps`; it is untouched, as that review said it should be.

## Behaviour I ran

The point of this section is that the two rejections both came from running the tool on something
nobody upstream had run it on, so this review did the same rather than re-reading the sweep in
`verify-report.md`. Every invocation used a hand-written store under the git-ignored `.harness/`,
with `sha256sum` before and after.

**The class that produced F1, probed further.** A store that parses, passes `load()`'s top-level
shape check, and then meets something above it:

| store | command | result |
|-------|---------|--------|
| `people: [{"n":"a"}]` | `people` and `add-person Carol` | exit 2 both, `…contains dict, which is not a name…`, bytes unchanged |
| `people: [["Alice"]]` | both | exit 2, `…contains list…` |
| `expenses: [42]` | `people` | exit 0, lists `Alice` — **out of this item's scope, and a real handover**; see `## Accepted gaps` |
| `version: "1"` (a string) | `people` | exit 0, lists `Alice`. `version` is written but never read; no criterion or ADR requires it to be checked |
| `people: ["Alice", "alice"]` (a duplicate the tool cannot create) | `add-person Bob` | exit 0, Bob added. The pre-existing duplicate is left alone, which is the same choice F2's fix made deliberately |
| `people: ["Al\nice"]` | `people` | exit 0, prints across two lines |
| `people: [""]` | `people` | exit 0, prints a blank line |

**Failure paths `verify` declared untested.** `verify-report.md` `## Not verified, and why` names
the write path's `OSError` wrapper as untriggered. I triggered it:

```
$ chmod 500 .harness/rc3/ro && EXPENSES_STORE=.harness/rc3/ro/s.json python3 -m expenses add-person Bob
cannot write .harness/rc3/ro/s.json: Permission denied          # exit 2, no traceback
```

and `EXPENSES_STORE` pointing at a **directory**, on both commands: `cannot read …: Is a
directory`, exit 2, no traceback. That gap is closed, not carried.

**The eight criteria, spot-checked end to end**, in fresh processes against a store three
directories deep that did not exist:

- reading first created nothing (`ls -d` on the top directory → `No such file or directory`) —
  AC5's read half;
- `Zoe`, `alice`, `Carol Ann` added in that deliberately non-alphabetical order, then `people |
  cat -A` → `Zoe$` / `alice$` / `Carol Ann$`, exit 0 — AC1, AC2, and the file created with both
  missing parents;
- `add-person "  ALICE "` → `alice is already in the group; nothing was added`, exit 2, naming the
  **stored** spelling — AC3;
- `add-person "   "` → `a name is required`, exit 2; `add-person` with no argument → argparse's
  required-argument error, exit 2; the roster unchanged after both — AC7;
- `--help` lists `add-person` and `people` and mentions `EXPENSES_STORE` nowhere, which is
  `ADR-0002` decision 2's explicit requirement — AC1;
- no traceback and an empty stdout in any of the 20 failing invocations — AC8.

## Findings

### F5 — a hand-edited name that today's rules reject is listed verbatim · **accepted gap, recorded**

`store.load()` now guarantees every roster entry is a `str`. It does not, and deliberately should
not, guarantee the entry would pass `normalise()`. So a store hand-edited to hold `""` makes
`people` print a blank line, and one holding `"Al\nice"` makes it print across two lines — which
is the one thing AC1's *"one person per line, their name and nothing else"* is about, and which
`ADR-0006` decision 5 gives as the whole reason control characters are banned.

Not a send-back, for three reasons stated so the judgement is auditable rather than merely
asserted:

- **The tool cannot produce such a store.** `normalise()` rejects both inputs at the only point a
  name enters the roster, and the previous review's F2 fix was specifically about *not* making
  the stored side re-validate. Reaching this state means editing the JSON by hand.
- **The alternative is worse and stricter than the ADR asks for.** Rejecting these on read would
  make a hand-edited store unusable rather than merely odd; repairing them would edit a user's
  file unasked. `ADR-0002` decision 6 scopes fatality to a file that "cannot be read or parsed" —
  a string that is a poor name parses fine. `impl-report.md` reached the same conclusion and gave
  the same reasoning, which I checked rather than adopted.
- **No criterion covers it.** AC1 constrains what the listing prints for names the tool accepted.

It is recorded in `item.md` because `verify` declared it in `## Not verified, and why` and a gap
that lives only in a verification report is invisible the moment the item closes.

### F6 — the `expenses` list's elements are still unvalidated · **handover, recorded**

F1's fix covers `people` only. `{"version":1,"people":["Alice"],"expenses":[42]}` loads cleanly
and `people` exits 0, which is correct today — nothing in this item reads that list. It is the
same latent crash one item away, and `impl-report.md` names it as a handover rather than leaving
it to be rediscovered.

I considered filing it as a bug item and decided against it, and the reasoning matters more than
the decision: a bug's Definition of Ready (`spec/dor-dod.md` §2, RB3) requires the expected
behaviour to cite a criterion, doc or ADR it contradicts. Nothing yet says what an expense record
*is* — WI-0002's plan decides that — so the bug would have to invent the schema it is filed
against, which pre-empts the item that owns it. Recorded in `item.md` `## Accepted gaps` as an
explicit obligation on WI-0002 instead, where the item that will do the work relates to it.

### F7 — AC8 says "a one-line message" and argparse's failures are two lines · **accepted, with the reading stated**

`verify` raised this against AC8's wording and `plan.md` step 5 chose it deliberately.
`add-person` with no argument prints a usage line and then
`python3 -m expenses add-person: error: the following arguments are required: name`.

I am not editing AC8, and I am not sending the item back over it. The reading applied, stated
here so it is a decision on the record rather than an oversight: **the message naming what was
wrong is one line**; argparse's usage line precedes it as a hint, and AC8's subject is the message.
The criterion's own sentence gives its purpose — EP-001's fourth success measure, no tracebacks,
errors on stderr, non-zero exit — and all three hold. `item.md` already accepts the more extreme
neighbouring case (a bare invocation printing the whole help to stderr) on the same basis.

If the stakeholder wants strictly one line of stderr and no usage hint, that is a change someone
must ask for; it is written into `item.md` so that it is askable rather than lost.

### F8 — the catch-all backstop is a design decision recorded in an overview, not an ADR · **D6 caveat, recorded**

`cli.main`'s `except Exception` changed the architecture's central claim about how AC8 is
guaranteed — `overview.md` v1 said the property came from the layering, and it did not. That is a
design decision by any ordinary reading, and D6 asks for design decisions to be in an ADR.

It is captured in `overview.md` **v2**, with a change-log row, the rationale, the rejected
alternative ("the layering alone"), and the counter-example that killed it — substantively what an
ADR carries. `implement` could not have done more: ADRs are the architect's artifact, and so is
promoting this one. Sending the item back would produce nothing, because the skill it would go
back to cannot write the thing that is missing; filing a question would spend a round trip on a
decision that blocks nobody.

Recorded as a caveat on D6 and written into `item.md`, so that the next `plan` execution can
promote it to an ADR if it agrees, rather than discovering the gap.

## Definition of Done

Applied criterion by criterion per `spec/dor-dod.md` §3. D1–D12.

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | Every acceptance criterion checkbox ticked | **pass** | All eight are `[x]` in `item.md`. AC8's tick was cleared by the previous review and re-earned by the third verification on the input that disproved it; I re-ran that input myself (`## Behaviour I ran`, row 1) rather than accepting the re-tick. `validate-workspace` → 0 errors. |
| D2 | Every ticked criterion cites its evidence in `verify-report.md` | **pass** | Each of the eight rows of `verify-report.md` `## Criteria` names a command `verify` ran and quotes real output; no row cites `impl-report.md`, and the report says so explicitly. The previous review's caveat on AC8 — evidence present, coverage short — is discharged: the sweep is now 28 cases including six junk element types × both commands and a forced internal exception. |
| D3 | All declared gates passed on the **final** state of the code | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 23 tests`, `OK` — run by `verify` on `a273c4e`, re-run by me on the branch head `4b04b42`, and re-run again on the trial merge result. `validate-workspace` → exit 0, 0 errors, 0 warnings. `lint-clean` **skipped, not passed** (`commands.lint` is null, `ADR-0001` §4). |
| D4 | No open blocking question | **pass** | `Q-001` and `Q-002` are both `status: answered`, `answered-by: human`, `## Consequences` naming AC3–AC6, `## Notes`, `ADR-0002` and `refinement-qa.md` — all of which exist and carry the answers. No question is open anywhere in the workspace. |
| D5 | A journal entry per skill execution; history chains without a gap | **pass** | Thirteen history rows, `— → draft → awaiting-answer → draft → ready → planned → in-progress → verifying → in-review → in-progress → verifying → in-review → in-progress → verifying → in-review`, each `when` ≥ its predecessor, the last matching `item.md`'s `status: in-review`. Thirteen journal entries in ascending order: `intake`, `refine`, `answer-questions`, `refine`, `plan`, `implement` ×3, `verify` ×3, `review-close` ×2. The first `implement` execution accounts for two rows (`planned → in-progress`, `in-progress → verifying`) and is one execution, so the counts agree exactly. |
| D6 | Every design decision is in an ADR, cited from the plan or journal | **pass, with a recorded caveat** | `ADR-0001` (baseline, no dependencies, no lint), `ADR-0002` (one store file per user), `ADR-0006` (CLI surface and the name rule) are each cited from `plan.md` `## Decisions and ADRs` and from the source implementing them, and I found no decision in the diff outside them — except `cli.main`'s catch-all backstop, which is F8: a design decision recorded in `overview.md` v2 rather than in an ADR. Caveat written into `item.md`, not waved through. |
| D7 | Documents the change invalidated have been updated | **pass** | `docs/architecture/overview.md` is at **v2** with a change-log row, `updated-by: implement`, `updated-for: WI-0001`. The previous review's F3 — the false AC8 justification — is corrected in the `cli` bullet, and the `store` bullet and the module diagram now state what damage detection actually reaches. `expenses/errors.py`'s docstring, which carried the same sentence, is corrected too. |
| D8 | Every commit on the branch references the item ID | **pass** | `check-commit-refs WI-0001 wi/WI-0001` → exit 0, `all 12 commit(s) on main..wi/WI-0001 name WI-0001`. Run before the merge, while the range is still non-empty. |
| D9 | Merged into the trunk | **pass** | Trial-merged into a detached worktree at `main` first: merge clean, `Ran 23 tests … OK` on the merge result, trial discarded. The item was then closed while the branch was still unmerged, and `wi/WI-0001` merged into `main` afterwards. |
| D10 | `verify` ran **after** the last code change | **pass** | `check-verify-freshness WI-0001 wi/WI-0001` → exit 0: *"verified at a273c4ee; wi/WI-0001 has moved to 4b04b42a but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code."* Run, not assumed. The last code commit is `fcf3cf4`. |
| D11 | `artifacts/review.md` exists and states what was examined | **pass** | This file. `## What I examined` is first, names the diff range, every artifact, every doc read against the code, and the behaviour run; `## Behaviour I ran` gives the invocations and their output. |
| D12 | Every claim in `docs/` about the behaviour this item touched is **still true**, read against the code | **pass** | Four documents re-read against the source, not remembered: **`overview.md` v2** — the `cli` bullet's two-handler claim matches `cli.py` (`except ExpensesError`, then `except Exception`, `BaseException` uncaught); "nothing below `cli` may print anything or call `sys.exit`" holds — neither `people.py` nor `store.py` nor `errors.py` imports `sys` or prints; the diagram's "the type of every roster entry" matches `load()`'s loop. **`ADR-0002`** — decisions 1–2 match `store_path()` including the empty-`XDG_DATA_HOME` fallback; 4 matches (`load` creates nothing, `save` calls `mkdir(parents=True)`); 5 matches (AC4 run); 6 matches on both commands for every damage mode I ran; 7 matches (`mkstemp(dir=path.parent)` then `os.replace`). **`ADR-0006`** — decision 4's two positive rules are exactly `normalise()`; 5's control-character range is `< 0x20 or == 0x7F`; 6 holds, validation is in `people.py` and `cli.py` has none. **`ADR-0001`** §4 — `commands.lint` is null and every skip cites it. The one document that still carries F3's superseded sentence is `plan.md`, which is a tracker artifact rather than `docs/`; it is handled in `## The plan.md handover` below. |

Eleven pass, one (D6) passes with a caveat recorded in `item.md`. None fails.

## The plan.md handover

`impl-report.md` `## What I did not do, third pass` ends by handing an open decision to this skill
by name: `plan.md`'s paragraph at lines 24–29 still says AC8 is *"made true by construction"* by a
single `except ExpensesError`, which is the last copy of the claim the previous review's F3 found
in three places. `implement` declined to edit it and said why — `plan.md` is `plan`'s artifact and
records what was believed when it was written. That was the right instinct.

**Decision: the original paragraph stays exactly as written, and a `## Correction` section is
appended to the end of `plan.md`** naming the claim, why it was false, what corrected it, and who
appended it. The reasoning:

- Rewriting the paragraph would destroy the evidence that the plan's central design idea was
  wrong, which is the most useful thing in this item's whole record for whoever plans WI-0002.
- A pointer in `item.md` alone is one file away from the reader who is being misled, and the
  failure mode F3 documented is precisely *re-quoting a sentence rather than re-checking it*. The
  correction belongs in the file being quoted.
- Appending rather than editing is what `spec/journal-and-history.md` prescribes for a wrong
  entry — *"corrected by a later entry that says what was wrong"* — and `plan.md` deserves the
  same treatment even though it is not formally append-only.

`plan.md` is not in this skill's declared outputs, so this is a deliberate step outside that list
and is flagged as such here and in the journal rather than done quietly. Nothing in the original
text was changed.

## Accepted gaps

Carried forward from the previous review, re-checked against the current code, amended, and
extended. All of these are written into `item.md` `## Accepted gaps`; a gap recorded only here is
forgotten the moment the item closes.

- **A bare `python3 -m expenses` prints the whole help to stderr and exits 2.** Unchanged, still
  accepted, still pinned by `test_no_command_at_all_fails_cleanly`.
- **No static analysis runs on this project at all** (`ADR-0001` §4). Unchanged and now reinforced
  a third time: three defects of exactly the class a linter catches — the dead `match_key()`, the
  unpassed `out`/`err`, and a `# noqa` comment naming a rule no tool enforces — were all found by
  a person reading a diff. An epic-level decision to revisit, and it is named in the epic's own
  record when EP-001 closes.
- **`ADR-0002` decision 7's atomic write is verified by inspection, not by test.** Unchanged; no
  process was killed mid-write.
- **`cli.main`'s `out` and `err` parameters are never passed by any caller** (the previous
  review's F4). Unchanged and deliberately untouched this pass. One test now drives them, which
  makes the parameters exercised but not *used* — the finding stands as written.
- **Two processes adding a person at the same time can lose one of them.** Unchanged.
- **New — a hand-edited name today's rules would reject is listed verbatim** (F5).
- **New — the `expenses` list's elements are unvalidated; WI-0002 must extend `store.load()`
  when it defines the shape** (F6).
- **New — AC8's "one-line message" against argparse's two-line failures** (F7), with the reading
  applied.
- **New — the catch-all backstop is recorded in `overview.md` v2 rather than in an ADR** (F8).

Two gaps carried by the previous review are **closed** rather than carried, because an accepted
gap that has since been closed misleads exactly as much as an unrecorded one:

- **~~The two default store-path branches have never been executed~~** — closed by the second
  verification against a scratch `HOME` and `XDG_DATA_HOME`; already struck from `item.md`.
- **~~The write path's `OSError` wrapper was never triggered~~** — closed by this review. A
  read-only parent directory produces `cannot write …: Permission denied`, exit 2, no traceback;
  a store path that is a directory produces the read-side equivalent on both commands.

## The epic

EP-001 stays **open**. WI-0002 and WI-0003 are both at `draft`, so DE1 fails on its face and the
epic Definition of Done is not applied. Recorded rather than skipped silently, because this is the
first child to close and a reader should be able to see that the check was made.

Two things are worth carrying to whoever closes EP-001, since this is the moment a sibling's state
is in hand: the no-linter decision above is epic-level, and EP-001's fourth success measure — no
tracebacks — is the one this item spent two rejections on, so DE6 should re-read it against
`cli.py` rather than against this report.

## Verdict, restated

Accept. `in-review → done`, `outcome: delivered`, branch merged into `main`.

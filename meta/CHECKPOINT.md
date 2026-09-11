# CHECKPOINT

## Builder session six is COMPLETE. There is no next unit in this session.

`meta/BUILDER-6-PROMPT.md` is done: META-166 through META-174, committed and pushed.
`./scripts/check` is green across **47 steps**; `fixtures/broken-workspace` emits **110** codes;
`scripts/lib/selftest.py` is **419** cases; `harness/tests/test_harness.py` is **195** tests; the
ledger holds **139** entries, every one with a readable status. Read `meta/FINAL-REPORT-6.md`
first, then `meta/ROADMAP.md` §4 as amended.

**What was built.** One theme in five pieces: the citation grammar, and what happens when it bites.

- **The mask is one rule now.** `citations_in()` / `carries_citation()` in `scripts/lib/claims.py`
  decide mention-vs-use in exactly one place, for every surface the vocabulary is scraped on. Four
  sites had been reading it unmasked, and a *presence* rule accepting a backticked example is the
  same defect as a *resolution* rule refusing one. The surface table is in the module docstring.
- **Severity follows knowledge (F-113, F-075 — one class, fixed as one).** A marker the resolver
  recognises and cannot resolve is still an ERROR. A marker matching **no form at all** is a
  WARNING under `claim.citation.unrecognised`, because the gate has not checked anything and
  cannot tell a mention from a typo. The convention is in `spec/doc-header.md` §4a now, not in a
  source comment.
- **ADR-0013 — a toolkit source is quoted and attributed, not pointed at.** `[src: .claude/...]`
  is refused (`claim.citation.outside-the-record`); `[src: toolkit: <document> <section>
  "<words>"]` replaces it. The record walk already pruned `.claude`, so a citation may not point
  where the record does not go — and the banked evidence proves the consequence rather than
  arguing it.
- **The grammar is where the writer writes.** Seven skills, derived from their own contracts, name
  the forms table; step 15d keeps that from rotting. F-114's grep went from nothing/exit 1 to 13
  hits/exit 0.
- **ADR-0014 — a fixable record defect is not a verdict on the engagement.** A bounded self-repair
  allowance: N consecutive repair turns (default 2), success resets, exhaustion is terminal with
  the original error preserved — and META-171b made that promise real, because the driver had been
  keeping only the validator's summary line.

**What is NOT proven, and FINAL-REPORT-6 §8 lists fifteen of them.** **ADR-0014's allowance has
never run** — it is tested, not exercised; the re-run is the first engagement that can reach the
exhaustion path. **The held-out recall number is still unmeasured**, because iteration 5 produced
no retro. **F-116 is open**: a failed adapter render wipes `dist/` before it validates. The
`toolkit:` form's *content* is uncheckable by the gate, by design, and the table says so.

## What the owner does next — `meta/ROADMAP.md` §4 as amended, FINAL-REPORT-6 §7

1. **Iteration 5r (`envel-2`)** — the calibration iteration 5 was launched for and never took.
2. **Review the trail and write findings down — before reading the retro's report.**
3. **Read the retro report and score it** against step 2. The first recall number honest to quote.
4. **Iteration 5b (`droll`)** — the first live test of E4, last, because a toolkit change before
   step 3 contaminates the calibration.

`iteration-5r-envel` is **provision-verified and torn down**. **It was not run** — no
`run_iteration.py` invocation was made in this session — and **the probe was not read**; its
existence was established by `isfile` + `getsize`. One disclosure is recorded in
FINAL-REPORT-6 §6 and belongs to the owner's judgement, not to a footnote.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.**
- `meta/harness/evidence/**` is read-only history. Filed finding text is appended to, never
  rewritten — and **the LAST status bullet is the current one** (F-112; step 17c).
- Toolkit commits and harness commits stay separate.
- **No harness run is in flight.**

## For the next builder session — what this session's method showed

- **A brief is hearsay, and the units said so five times.** `arose-from` was never a citation
  site; `lint-retro` carried an unreported F-054 bug of its own; `fixtures/broken-workspace`
  compares codes as a **set**, so a new case sharing an existing code is invisible; the two prune
  tuples had **not** in fact drifted, and the weaker claim was filed instead; the harness suite was
  **176** tests at session start, not the 110 the previous checkpoint implied.
- **A derivation gets sharper on contact with the code.** ADR-0013's strongest argument was not
  written into the brief: at the toolkit revision installed for iteration 5, `claims.py:148` really
  was the line the citation claimed — two commits later it is blank. The record made the argument.
- **Take the deferral when the next run is the thing that will hit it.** META-171 deferred the
  preserved-original-error gap honestly and in writing; META-171b took it, because the re-run is
  the first engagement that can reach that stop and a detail reading `1 error` would have thrown
  away exactly what made iteration 5 worth banking.

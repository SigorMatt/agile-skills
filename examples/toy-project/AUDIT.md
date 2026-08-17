# Audit — `linecount`

**Auditor's note on scope and method.** I was given the tracker (`tracker/`), the documentation
(`docs/`), the git history (`GIT-LOG.md`, `GIT-BRANCHES.md`) and the delivered source (`src/`),
and nothing else. I had no prior knowledge of this project. Everything below is drawn from those
files.

I did not take the record's word for anything I could check myself. I ran the delivered tool, ran
its test suite, rebuilt the reproduction folders from the three bug reports, rebuilt the worked
examples from the acceptance criteria, re-ran the encoding measurement that one ADR rests on,
mutated the source four times to confirm the regression tests actually fail without their fixes,
and cross-checked every commit sha and commit count in the record against the git history. Where I
say "verified", I mean I executed it.

---

## Executive summary

A small, coherent piece of work, delivered and closed, with a record that is unusually complete
and — where I could test it — unusually honest. Five work items under one epic produced a
191-line Python tool and a 642-line test suite. Every acceptance criterion I re-ran reproduced
byte for byte. Every commit references an item. No quality gate was ever forced.

Four things stop this being a clean sign-off:

1. **The tracker's timestamps are demonstrably false** for the three bug items, and the record
   knows it. Chronology can only be reconstructed from `GIT-LOG.md`, not from the tracker.
2. **The "human" whose stated requirements justify most decisions was simulated by the same
   agent that did the work.** This is disclosed, but only in two artifacts, and the most
   quotable claims of human authority carry no caveat.
3. **The epic's closing summary contains a claim I falsified in one command.**
4. **A factual justification repeated in five documents, including two comments in shipped
   source, is wrong** — and is contradicted by a transcript in the same item.

None of the four is a defect in the software, which works as described. All four are defects in
the record, which is what I was asked to audit. Details, with file and line, in section 5.

---

## 1. What was built, and why

**The problem.** Someone opens a directory of mixed notes and code and does not know where the
bulk of the material is. The existing tool, `wc -l *`, prints the counts in glob order — so the
reader must scan every row to find the largest — and it fails outright when the folder contains a
subdirectory (`tracker/items/EP-001/item.md` `## Why now`; `docs/product/vision.md` lines 23–28).

**For whom.** Primarily the author, as a personal utility on his own machine, but explicitly also
"someone who inherits one of these folders" (`docs/product/vision.md` lines 14–19). That second
audience is load-bearing: it is why the deliverable is a file in a repository rather than a shell
alias, and why "no installation, standard library only" is treated as a product property rather
than a preference.

**What was delivered.** One epic, `EP-001`, with five children, all `done`
(`tracker/board.md`):

| item | what | size |
|------|------|------|
| WI-0001 | count lines per file in a folder, print largest first, with a total | 13 acceptance criteria |
| WI-0002 | `--top N` to show only the N largest, total still over all files | 11 criteria |
| BUG-0001 | a symlink that cannot be stat'ed aborted the whole listing and blamed the folder | 6 criteria |
| BUG-0002 | a folder whose files were all unreadable printed `no files` on stdout | 7 criteria |
| BUG-0003 | a filename that is not valid UTF-8 produced a traceback and exit 1 | 6 criteria |

The artifact is `linecount.py`, 191 lines, importing only `argparse`, `os` and `sys`, plus
`tests/test_linecount.py`, 642 lines, 60 tests. There is no package, no entry point, no
dependency manifest.

**I verified the delivery.** `python3 -m unittest discover` from `src/` gives `Ran 60 tests …
OK`, exit 0, with nothing installed. I rebuilt each bug's reproduction folder against the
delivered code:

- symlink loop beside a real file → `3  ok.txt` / `3  total`, empty stderr, exit 0 (BUG-0001 fixed);
- folder of two `chmod 000` files → `no files could be read` on stdout, two `linecount:` lines on
  stderr, exit 0, and distinguishable from a genuinely empty folder, which still prints `no files`
  (BUG-0002 fixed);
- folder containing `bad\xff.txt` → `3  bad\377.txt` / `2  good.txt` / `5  total`, exit 0, no
  traceback (BUG-0003 fixed).

I also rebuilt WI-0002 AC10's corrected worked example (27 files, 26 × 46 lines plus one of 8) and
got `  46  f00.txt` / `  46  f01.txt` / `1204  total (all 27 files)` — the criterion's text, byte
for byte.

**One thing a reader must know about what this project is.** This was not a real customer
engagement. `tracker/items/WI-0001/artifacts/refinement-qa.md` lines 10–12 state: "this run is a
test of the methodology. Every answer below was produced by the builder standing in for the human
… Nothing here should be read as the words of a real user." Every commit in `GIT-LOG.md` is
authored by "agile-skills builder". So `linecount` is real, working software; the "human" whose
requirements justify it is not a real person. That materially changes how much weight the phrase
"the human decided" can carry, and I return to it in section 5.

---

## 2. What decisions were made, and by whom

Decisions are recorded in three places: eight ADRs under `docs/architecture/adr/`, the
`## Decisions` block of every journal entry, and the five answered question files. Every ADR names
its decider. All eight were taken by the `plan` skill acting as architect.

### Shaping decisions

| decision | who | basis | my read |
|----------|-----|-------|---------|
| Two work items, not three or one | `intake` | the human named the seam himself ("as a *second* piece of work"); the two alternative splits are named and rejected in `EP-001/journal.md` lines 18–32 | Sound, and the rejected alternatives are on the record, which is what makes it auditable |
| `--top N` deferred to WI-0002 | `intake` | the human pre-empted merging it | Sound |
| Tie-break by filename in byte order; a JPEG gets a meaningless number rather than a special case; `no files` rather than `0  total` for an empty folder; exit 2 on stderr for failures | `refine`, from the (simulated) human's answers | `WI-0001/artifacts/refinement-qa.md` Q1–Q6, quoted verbatim including the hesitation "You decide, honestly" | The refusal to tidy the hesitation into enthusiasm is a genuine quality signal |
| argparse rather than hand-rolled parsing | `plan` (ADR-0001) | both alternatives costed | Sound |
| An unreadable file is skipped, named on stderr, exit stays 0 | `plan` (ADR-0002) | four options costed; no document ruled on it | Sound — and note that BUG-0002 is the seam between this decision and AC10, which ADR-0005 had already predicted |
| No lint command, no build command | `plan` (ADR-0003) | no linter ships with CPython; four were checked absent on the machine; a stand-in would report a green gate for a check nobody ran | Correct, and the cost is honestly carried: `lint-clean` is reported **skipped**, never passed, on every single execution |
| `--top` validated by our own `parse_top`, not by `type=int` | `plan` (ADR-0004) | AC7 requires one stderr line; argparse writes two | Sound |
| `format_report` grows optional parameters rather than changing signature | `plan` (ADR-0005) | AC4 requires WI-0001's tests to pass unmodified | Sound, and it names its own failure mode, which is what BUG-0002 later hit |
| An entry that cannot be resolved is "not a file", ignored silently | `plan` (ADR-0006) | AC1 requires empty stderr for the loop case, so "report it" was unavailable | Sound; the alternative is costed |
| A folder whose files were all skipped prints `no files could be read` | `plan` (ADR-0007) | four options costed; a zero total row rejected as "quietly wrong numbers" | Sound |
| The report is written to `sys.stdout.buffer` as `os.fsencode`d bytes | `plan` (ADR-0008) | four options costed, with interpreter output for the mechanism | Sound, and see below — the reasoning was later corrected and is now stronger than it was |

### Decisions I consider wrong or thinly justified

**1. Not filing `BrokenPipeError` as a defect.** The independent regression pass reproduced a
traceback and exit 1 from `python3 linecount.py <folder> | head -1` at 5000 files, and declined to
file it: "No bug is filed, because the only reproduction is at a size the item explicitly
excludes" (`EP-001/artifacts/regression-verify-report.md` lines 177–185). I reproduced it against
the delivered code — 5000 files, `| head -1`, `BrokenPipeError: [Errno 32] Broken pipe`, first
stage exit 1.

The justification is defensible on scope, and the sizing is genuinely the (simulated) human's
words. But it sits badly beside BUG-0003, which was filed as a defect on exactly the grounds that
a traceback contradicts the vision's "a number, not a stack trace" — a claim the vision makes
without a size qualifier. The same reasoning applied to the same symptom produced two opposite
outcomes. This is the record's weakest judgement, and the epic's closing summary then overstates
the result (see section 5).

**2. `outcome: delivered` left on a reopened epic.** `answer-questions` decided to keep the field
while the epic was open, reasoning that the epic "*was* delivered"
(`EP-001/journal.md` lines 383–386). The validator refused it with `item.outcome.premature`, and
the decision was reversed in a correcting entry (`EP-001/journal.md` lines 442–452). The reasoning
was wrong; the handling of being wrong was exemplary — the mistake was left visible rather than
overwritten. I count this as a bad decision well recorded.

**3. Every question filed `blocking: false`, including one that blocked everything.**
`BUG-0001/questions/Q-001.md` line 55: "**Filed `blocking: false`, and that needs explaining.** In
substance this blocks everything, not just this item". The stated reason is procedural — moving
the item to `awaiting-answer` would have appended a second row carrying the same corrupt timestamp
— and it is a reasonable trade. The consequence is that `tracker/board.md` reads "blocked: none"
for a period in which no item in the workspace could be dispatched at all. A board that cannot
show a total stoppage is worth less than it appears.

**4. ADR-0001's stated consequence is now false and was never marked.** ADR-0001 line 60 predicts
"WI-0002 adds `--top` as `parser.add_argument("--top", type=int)`". ADR-0004 lines 35–38 rejects
exactly that as option A. ADR-0001 is still at v1 with the wrong prediction and no forward
pointer. Small, but it is precisely the kind of rot the ADR discipline exists to prevent, and the
project caught the same class of error in ADR-0008 and fixed it there.

**5. One criterion was never put to the customer, even a simulated one.** WI-0001 AC12 ("the path
is a regular file", "no argument at all") is flagged as the analyst's own extension
(`WI-0001/item.md` lines 113–116). That is the correct handling — but it is worth a manager
knowing that one of thirteen criteria in the founding item rests on nobody's authority but the
analyst's.

**6. `EP-001/Q-001` was answered by citing methodology rules the question itself said did not
exist.** When filed, the question states that `spec/ids-and-statuses.md` §4 offers an epic no
transition out of `done`. When answered, it states that §3.4 says a closed epic may be reopened,
and that `journal-and-history.md` §1 "has been amended to match"
(`EP-001/questions/Q-001.md` lines 79–95). The rule that unblocked the project was created between
the question and the answer, by an actor this project's record does not name. Those spec files sit
outside my read scope, so I cannot verify the claim either way. Flagged, not alleged.

---

## 3. What questions arose, and how were they resolved

Five questions were filed. All five are `answered`; the board shows none open
(`tracker/board.md` lines 14–22). All five were addressed to `architect`, all five were answered
by `answer-questions`, and **none was escalated to the human** — each answer records which of the
four escalation conditions were tested and why none applied.

**Q1 — `WI-0002/Q-001`: "AC10 describes a folder that cannot exist."**
Asked by `implement`, during implementation, on building the fixture. It could not answer itself
because a developer may not amend the criterion they are judged against — stated explicitly at
line 120: "a developer amending the criterion they are being judged against is the failure this
protocol exists to prevent." The arithmetic is correct: 27 files whose largest holds 9 lines sum
to at most 243, not 1204. Answered by `answer-questions` with option A — correct the illustration,
leave the rule. **What changed:** AC10's worked example in `WI-0002/item.md`, a `## Notes`
paragraph recording the amendment, and the plan's AC10 mapping row. No code changed. I rebuilt the
corrected example and it produces exactly the stated three lines.

**Q2 — `EP-001/Q-001`: "Where does a defect found after its epic closed go?"**
Asked by the independent regression pass. It could not answer itself: filing the bugs (which its
own rules require) made `validate-workspace` fail, and no legal transition existed to clear it —
so the question is a methodology question, not a project one, and it explicitly recommended
nothing ("none, insufficient basis"). Answered months of pipeline-logic later by
`answer-questions`: reopen the epic. **What changed:** `EP-001` went `done → open`, a history row
was appended naming the three bugs, `outcome` was cleared, the board was regenerated, and the epic
was later closed a second time. See section 2 item 6 for the caveat.

**Q3 — `BUG-0001/Q-001`: "Two clocks in one workspace disagree by three hours."**
Asked by `plan`. It could not answer itself because `history.md` may not be hand-edited by a
skill, and `scripts/transition` had no way to supply a timestamp. Answered by `answer-questions`
in three parts: (a) the transition tool now clamps to `max(now, last_row + 1s)` and announces the
clamp; (b) skewed values were corrected **selectively** — `created` on all three bugs, one
question's `created`, and journal headings on four items — and deliberately left where correcting
one half would make it disagree with an uncorrectable half; (c) one history row could be repaired
by no skill and needed a hand. That repair happened: `GIT-LOG.md` carries commit `f520c2d`
"tracker: restamp the pre-clamp history row and record the correction". This question has the
largest downstream consequences of any in the project, and they are not all good — see section 5.

**Q4 — `BUG-0001/Q-002`: "AC6 requires a proof that cannot exist."**
Asked by `implement`. AC6 required each of four regression tests to fail against the pre-fix
commit, but the AC5 test asserts *unchanged* behaviour and therefore passes there by construction.
Same reason it could not self-answer as Q1. Answered: scope the failing clause to the three tests
that assert new behaviour, matching the wording BUG-0002 AC7 already used. **What changed:** AC6's
wording plus a `## Notes` paragraph. No code. **I reproduced the measurement**: with the BUG-0001
fix removed from the delivered file, the suite reports `FAILED (failures=3)` — exactly the three
tests named.

**Q5 — `BUG-0003/Q-001`: "ADR-0008's rejected example does not reproduce."**
Asked by `verify`, while checking an ADR's *reasoning* rather than only its decision. It could not
answer itself because `verify` may not write to `docs/`. Answered: amend ADR-0008 in place to v2,
add the measurement, and leave the wrong v1 claim visible rather than deleting it. **What
changed:** ADR-0008 v1 → v2 and one sentence of the BUG-0003 plan. No code.

**I re-ran this entire measurement myself.** Under `PYTHONIOENCODING=ascii`, the delivered
implementation prints `café.txt` and exits 0; a rebuilt "option B" (`reconfigure(errors=
"surrogateescape")`) raises `UnicodeEncodeError` and exits 1. Under `LC_ALL=C` both survive. The
v2 table in ADR-0008 lines 66–71 is correct in every cell, and the v1 claim it corrects was indeed
wrong. This is the single best-evidenced thing in the record.

---

## 4. What did verification find

Verification happened at three levels: a `verify` execution per item, one independent regression
pass over the merged trunk, and a `review-close` execution per item plus twice for the epic.

**Item-level verification (WI-0001).** All 13 criteria passed on fixtures built by the verifier,
with commands and actual output quoted per criterion. Two criteria were deliberately checked by a
route the implementation had not used — a real system PNG rather than the generated one, and a
fresh `git clone` for the "nothing installed" criterion. 14 code mutations were applied; all 14
were caught. No defect; nothing sent back. Five gaps were declared and accepted, and — importantly
— written into `item.md` `## Notes` "so it outlives the reports nobody re-reads after an item is
closed". One of those five accepted gaps ("a filename that is not valid UTF-8 is untested") became
BUG-0003 three hours later. The gap register worked exactly as intended.

**Item-level verification (WI-0002).** All 11 criteria passed; 13 mutations caught. The verifier
found a real behaviour change nobody had asked about: the no-argument usage line changed from
`usage: linecount [-h] folder` to `usage: linecount [-h] [--top N] folder`. It found this by
extracting the binary WI-0001 shipped and running it beside the new one. Judged outside AC4's "on
the same folder", accepted at review, and written into the item.

**The independent regression pass (`EP-001/artifacts/regression-verify-report.md`)** is the most
valuable artifact in this repository. Run *after* the epic was closed, over the merged trunk,
against all 24 criteria, six success measures and five ADRs, on fixtures built before the code was
read. It found:

- **three defects**, filed as BUG-0001 (high), BUG-0002 (medium), BUG-0003 (medium), each
  reproduced against both trunk and the exact commit WI-0001 shipped, so none could be blamed on
  the later item;
- **two ADRs graded "partial"** rather than pass — ADR-0002's own stated boundary is crossed by
  BUG-0001, and ADR-0005's named misuse is reached by `main` itself;
- **one gate reported as FAIL**: `workspace-valid`, because filing bugs under a closed epic made
  the validator reject the workspace and no legal transition cleared it. The report says so
  plainly rather than papering over it, and files the question;
- **one traceback found and not filed** (`BrokenPipeError` at 5000 files) — see section 2;
- 13 mutations, all caught, so the suite is sensitive rather than decorative.

**Bug-level verification.** Each of the three bugs was verified on fixtures built fresh in a
directory the earlier steps had never touched — `BUG-0001/artifacts/verify-report.md` line 7 says
so explicitly, "so that a fixture left in a helpful state by an earlier step could not flatter the
result". Each bug's criteria demanded that the new regression tests **fail** against the pre-fix
commit, which is the right shape for a regression demand, and each verifier re-ran that
demonstration itself rather than accepting the implementation report's copy of it. Mutation
counts: 4 for BUG-0001 (all caught), 5 for BUG-0002 (all caught), 3 for BUG-0003 plus a fourth
that tested the ADR's argument rather than the code. BUG-0001's verification included the one
mutation that mattered: moving the new `try` a few lines higher so it swallows the folder's own
error — caught by four tests.

Two things in these reports deserve a manager's attention. First, BUG-0003's fourth mutation
**survived** — reimplementing the fix as ADR-0008's rejected option B leaves the suite green — and
the gate is still labelled pass. The explanation given is sound (two correct implementations under
the tested conditions), and it is what led to the ADR correction, but the label does work the
evidence does not. Second, both bug verify reports open with process claims that cannot be
falsified from the record: "Criteria were read before the implementation report", fresh fixture
directories, `git status` clean afterwards. These are exactly the claims a fabricated verification
would also make. I mitigated this the only way available — by re-running the substance — and the
substance held every time.

**I confirmed the regression demand independently.** Removing each fix from the delivered file and
re-running the suite:

| fix removed | result |
|-------------|--------|
| BUG-0001 (`try/except` around `entry.is_file`) | `FAILED (failures=3)` |
| BUG-0002 (the `no files could be read` branch) | `FAILED (failures=3)` |
| BUG-0003 (`stdout.buffer.write(os.fsencode(...))`) | `FAILED (failures=2, errors=1)` |

All three match what the record claims. The tests are load-bearing.

**Gate outcomes across the whole project.** `lint-clean` was reported **skipped** on every single
execution, never once as a pass — which is what ADR-0003 predicted and demanded.
`workspace-valid` failed twice and both failures are recorded with the error text.
`tests-would-fail-without-the-change` passed everywhere with mutation evidence. **No gate was ever
forced**: I grepped every `history.md` and no row carries `[gates forced]`, and no `--force` appears
except in journal entries explaining why it was *not* used.

**What happened to each finding.** Three defects → three bug items → planned, fixed, verified,
reviewed, merged, closed. One usage-line change → accepted and recorded in the item. Three
document defects (an impossible worked example, an unsatisfiable criterion, a wrong ADR example)
→ three questions → three amendments, none of which touched code. Two process failures (the clock
skew, the closed-epic rule) → two questions → tooling and methodology changes. Everything else →
the "accepted gaps" register in each item's `## Notes`. I checked that register: every gap named
in a verify report or review is present in the corresponding `item.md`.

**What verification never checked, on its own admission:** lint of any kind, on any item, ever;
non-POSIX platforms; folders past 5000 files or files past ~4 KB on disk; concurrency; stderr's
encoding when a filename is both undecodable and unreadable; a folder of only unresolvable
entries; and a folder mixing unreadable files with unresolvable entries. Each is written into the
relevant item's `## Notes`, which I confirmed. I ran the last two myself: the first prints
`no files`, the second prints `no files could be read` with one stderr line — both exactly what
the record predicts.

**One gap the record did not declare.** BUG-0003 verified the undecodable filename under
`LC_ALL=C`, and separately verified a genuinely non-UTF-8 stdout (`PYTHONIOENCODING=ascii`) using
a *valid* UTF-8 name. The combination that most directly stresses the fix — the undecodable name
under `PYTHONIOENCODING=ascii` — appears neither in the negative-cases list nor in
`## Not verified, and why`. Since the same report showed `LC_ALL=C` to be a weak test (CPython
enables UTF-8 mode under it), the locale-independence claim rested on less than it looked. I ran
the missing combination: exit 0, `b'3  bad\xff.txt\n2  good.txt\n5  total\n'`. The behaviour is
correct; the coverage claim was simply thinner than stated.

---

## 5. Audit assessment

### What I could answer confidently, and what I had to infer

| question | confidence | why |
|----------|-----------|-----|
| 1. What was built and why | **High** | The vision, the epic and the item bodies say it plainly, and I ran the delivered code against every stated example |
| 2. What decisions were made, by whom, on what basis | **High for content, medium for authority** | Every decision has a named decider, costed alternatives and a reversal cost. But every role was played by one actor, so "who" is a role label, not an independent party |
| 3. What questions arose and how they resolved | **High** | Five question files, each with context, options, answer, basis and a `## Consequences` list I spot-checked against the files |
| 4. What verification found | **High on substance, medium on bookkeeping** | The reports quote commands and actual output rather than asserting outcomes, and every behavioural claim I re-ran reproduced. But several of their *counts* — rows, journal entries, changed lines, tests catching a mutation — do not survive checking, and the review layer passed all of them |
| Chronology — when things happened | **Low. I do not trust the tracker's timestamps at all** | See below |

### Where the record is thin, contradictory or misleading

**1. The bug items' history timestamps are fiction, and the journals contradict them.**
`tracker/items/BUG-0002/history.md` records six transitions at `01:30:00Z` through `01:30:05Z` —
filing, planning, branching, implementing, verifying and closing a defect in six seconds.
`GIT-LOG.md` shows that work spanning `02:11:48+03:00` to `02:17:14+03:00`, about five and a half
minutes. Worse, the same executions are dated differently in two files:

> `tracker/items/BUG-0002/history.md` line 8: `| 2026-08-17T01:30:03Z | in-progress | verifying | implement | … |`
> `tracker/items/BUG-0002/journal.md` line 201: `## 2026-08-16T23:16:00Z — implement v0.1.0 — developer`

The same execution, two timestamps, 2 hours 14 minutes apart. BUG-0001 made the opposite trade —
its journal headings jump from `22:58:00Z` to `2026-08-17T01:30:30Z` to stay beside its clamped
history rows — so across items the record now claims BUG-0001 finished about two and a half hours
*after* BUG-0002 and BUG-0003, when `GIT-LOG.md` shows it finished first. The cause is understood
and documented (`BUG-0001/questions/Q-001.md`), and the correction was thoughtful about what it
could and could not touch. The result is still that **the tracker cannot be used to reconstruct
when anything happened.** `GIT-LOG.md` can. A manager reading a history table and taking it at
face value would be misled.

**2. The timestamp correction never reached `docs/`.** `docs/architecture/overview.md` lines 96–97
list v4 as `2026-08-17T01:36:00Z` and v3 as `2026-08-17T01:50:00Z` — version 4 stamped fourteen
minutes *before* version 3, in the same change log. ADR-0006 (written first, for BUG-0001) is
stamped `01:50:00Z`, later than ADR-0007 (`01:34:00Z`) and ADR-0008 (`01:36:00Z`), both written
after it. `BUG-0001/questions/Q-001.md` `## Consequences` lists the files it corrected; no `docs/`
file is among them, and none is named under "deliberately not changed" either. This is the one
place where the skew was neither fixed nor declared.

**3. Two citations do not resolve.** I checked 45 short shas cited across the record against
`GIT-LOG.md` and `GIT-BRANCHES.md`. Forty-three resolve. Two do not:

- `tracker/items/EP-001/journal.md` line 543 — "the delivered code on `main` at `1d10023`". At
  that moment `main` was at `6f7917e`. This is in the epic's final closure entry, the entry most
  likely to be read.
- `tracker/items/BUG-0003/artifacts/plan.md` line 12 — "Reproduced on `main` at `2946f57`". At
  that moment `main` was at `c9f3498`. This is the sha that proves the defect existed.

Everything else in the sha chain is exact, including all five `check-commit-refs` counts, which I
recomputed from the merge bases the reviews name: 4, 4, 4, 3 and 4 commits per branch. That makes
the two misses look like transcription errors rather than fabrication — but a reproduction pinned
to a commit that does not exist is not a reproduction anyone else can repeat.

**4. The `linecount.py` line-count chain contains an impossibility and a gap.**
`BUG-0001/artifacts/impl-report.md` line 6 states the file "grew from 164 to 175 lines" — a net
change of **+11**. `GIT-LOG.md` line 62 records the only commit touching that file on the branch,
`06fc185`, as changing **18** lines of `linecount.py`. Insertions plus deletions and net change
always share the same parity; 18 is even and 11 is odd, so at most one of these numbers is right.
`BUG-0001/artifacts/verify-report.md` line 72 offers a third figure, "`linecount.py` +18/−3",
which totals 21 rather than 18 — it appears to have read git's *total* as the insertion count.
(The same line's `tests/test_linecount.py` +64/−0 matches `GIT-LOG.md` exactly, so the error is
isolated.) Separately, `BUG-0002/artifacts/impl-report.md` line 5 leaves the file at **184** lines
and `BUG-0003/artifacts/impl-report.md` line 5 starts from **185**, with nothing accounting for
the extra line. The delivered file is 191 lines, which I counted. None of this affects the
software; it does mean the "hunk-by-hunk" diff review the reviews claim did not check the
arithmetic printed beside it.

**5. The epic's closing summary undercounts its own questions.** `EP-001/journal.md` line 609:
"Five items, 191 lines of tool, 60 tests, eight ADRs, four questions asked and answered inside the
record." I verified the first four figures — 191 lines, 60 tests, eight ADR files, five items.
There are **five** question files, not four; `WI-0002/questions/Q-001.md` is omitted because it was
closed in the epic's first round. A summary that claims to account for the epic should count it.

**6. A journal entry is dated after the commit that contains it.** `EP-001/journal.md` line 526
heads the second closure `## 2026-08-16T23:36:00Z`. The commit carrying it, `0fc856b`, is
timestamped `2026-08-17T02:29:18+03:00` — `23:29:18Z` — six and a half minutes earlier. Small, but
it means the headings are chosen values, not observed ones.

**7. One Definition-of-Done check was marked pass on counts that are wrong.**
`tracker/items/BUG-0002/artifacts/review.md` line 35 certifies D5 ("a journal entry per execution;
history chains") with: "four rows chaining `— → ready → planned → in-progress → verifying →
in-review` … four journal entries, one per execution". The chain it prints contains five
transitions; `BUG-0002/history.md` holds six rows, five of them written before the review; and
`BUG-0002/journal.md` holds six entries, five written before the review. Both counts are wrong,
and both are wrong in the direction of "fewer things to check". The sibling review of BUG-0003
counts the identical structure correctly ("five rows … six journal entries",
`BUG-0003/artifacts/review.md` line 38), so the two reviews apply different accounting to the same
criterion and both pass it. D5 is the criterion whose entire job is counting.

**8. A criterion was certified before it was satisfiable, and another was satisfied by
re-reading it.** `BUG-0001/artifacts/impl-report.md` line 52 states plainly that AC6 cannot be met
("three of four fail, and the fourth cannot"), while the same report marks the hard gate
`every-criterion-has-a-test` **pass** at line 91. The gap was closed properly afterwards — Q-002
scoped AC6, and `verify` then checked it in its amended form — but for the duration of that
execution a hard gate certified a criterion the executing skill had just declared impossible.
The related case in BUG-0003 was never amended at all: AC6 there requires three tests to "fail"
against the old code, and one of them raises an `IndexError` instead
(`BUG-0003/artifacts/impl-report.md` lines 54–57). `verify` accepted it by restating the criterion
as "none of them passing" (`BUG-0003/artifacts/verify-report.md` line 28). Declared, not hidden —
but it is a criterion met by reinterpretation, one item after the project had already answered a
question about exactly that wording. I confirmed the underlying fact: removing the BUG-0003 fix
gives `FAILED (failures=2, errors=1)`, not three failures.

**9. One planning artifact was rewritten in place, in the same item that praises the opposite
treatment.** `BUG-0003/artifacts/plan.md` lines 32–34 now carry a corrected `PYTHONIOENCODING=
ascii` example with a parenthetical noting the change. ADR-0008, correcting the identical error,
deliberately kept the wrong v1 claim visible and said why. The plan simply overwrote its own
sentence; the text that was actually executed is gone. The review notices the edit but not the
inconsistency.

### Claims the evidence does not support

**The epic's closing claim about stack traces is false as written.**
`tracker/items/EP-001/journal.md` line 608 closes the epic with the tool "printing a number, never
a stack trace, and exiting non-zero only when it cannot read the folder at all." Against the
delivered code:

```
$ python3 linecount.py <folder-of-5000-files> | head -1
    50  f0049.txt
first-stage exit=1
    sys.stdout.buffer.write(os.fsencode(text))
BrokenPipeError: [Errno 32] Broken pipe
```

A stack trace, and a non-zero exit on a folder that reads perfectly. The project *knows* this —
it is declared in `WI-0001/item.md` `## Notes`, in the plan's out-of-scope list, and measured
precisely in `EP-001/artifacts/regression-verify-report.md` lines 177–185, where the boundary is
recorded as "did not reproduce at 320 files, reproduces at 5000". The failure is not that the gap
exists; it is that the closing summary states an unqualified absolute that the same repository
disproves. Every other claim in that summary I tested held.

**The justification printed in the shipped source is factually wrong, in five documents at
once.** BUG-0003's chosen output format is defended everywhere by the claim that it matches
`ls -b`:

> `src/linecount.py` line 9: "a name that is not valid UTF-8 prints as `ls -b` prints it (ADR-0008)"
> `src/linecount.py` line 183, `docs/architecture/overview.md` line 62, `ADR-0008` lines 53 and
> 106, `BUG-0003/artifacts/verify-report.md` line 24, `BUG-0003/artifacts/review.md` line 95:
> "as `ls -b` and `wc` write it"

`ls -b` does the opposite of what the tool does. On the item's own reproduction folder:

```
$ ls -b       → bad\377.txt          (C-style escape)
$ ls          → bad<0xFF>.txt        (raw byte)
$ wc -l *     → 3 bad<0xFF>.txt      (raw byte)
$ linecount   → 3  bad<0xFF>.txt     (raw byte)
```

The tool matches `wc` and plain `ls`; it is `ls -b` that escapes. The contradicting transcript is
in the record already — `BUG-0003/artifacts/plan.md` line 14 shows `ls -b` printing
`bad\377.txt`, thirty lines above the same file's `ls -b` claim. The **decision** is unaffected
and still correct; the rationale as written is not, and it survived a plan, an ADR, the
architecture overview, an implementation report, an independent verification and a review — six
layers, in the one item whose whole story is a verifier catching a wrong ADR rationale. It is now
a comment in shipped source that a maintainer would act on.

**Everything else I tested held.** For the record, these all reproduced exactly against the
delivered code: WI-0001 AC1's worked example; WI-0002 AC10's corrected example and its `total (all
27 files)` label; WI-0002 AC7's four bad `--top` values, one stderr line each, exit 2; the
rejection of `-t`; all three bug reproductions; the `no files` versus `no files could be read`
distinction; the "only unresolvable entries still print `no files`" gap declared in BUG-0002's
notes; the `total (all 1 files)` observation about `--top` with a skipped file; the full ADR-0008
v2 encoding table; and the three regression-test sensitivity claims. The 60-test suite passes with
nothing installed, as claimed.

### Two structural caveats a manager should weigh

**Independence is nominal.** The record's strongest quality mechanism is the separation of roles —
an analyst who may not edit code, a developer who may not edit their own acceptance criteria, a
verifier who may not write to `docs/`, a reviewer who reads the diff hunk by hunk. That separation
is real in what each role is *permitted to touch*, and it visibly worked: `implement` filed a
question rather than editing a criterion it disliked, twice. But every role was executed by the
same builder. "An independent regression pass" means the same agent working from the criteria
rather than from its own earlier notes. That is a genuine and useful discipline — it found three
real defects — but it is not third-party assurance, and nothing in `docs/` says so.

**The customer was simulated, and only two artifacts say so.** The disclosure at
`WI-0001/artifacts/refinement-qa.md` lines 10–12 and its twin in WI-0002 is exemplary. It does not
propagate. `docs/product/vision.md` lines 48–49 assert: "The governing phrase from the author is
'nothing fancy'. Every feature this document rules out was ruled out by him at intake, not
assumed." `EP-001/journal.md` lines 59–123 records eight answers marked "(human, verbatim)". Neither
document carries a caveat. A reader who opens the vision or the epic — the two documents a manager
is most likely to read — would reasonably conclude a real person said these things. The provenance
note belongs in the vision's front matter, not only in a refinement artifact.

### Would I sign off?

**Qualified yes — with one correction required before sign-off, and two standing caveats.**

I would sign off that **the work is accounted for**. Every one of five items has criteria, a plan,
an implementation report declaring its deviations, an independent verification report quoting
commands and output, and a review that reads the diff against the plan. Every commit in
`GIT-LOG.md` names its item, and `GIT-BRANCHES.md` reconstructs each item's code history. Every
finding lands somewhere I can point at: three became bug items that were fixed and closed; the rest
became declared gaps written into the items themselves rather than into reports nobody re-reads. No
gate was ever forced. Three questions caused criteria or documents to change and none of them
caused code to change, which is the right ratio. Most tellingly, when the record was wrong it said
so out loud — a reversed decision on the epic's outcome, a corrected ADR rationale, an admitted
clock failure, a gate failure reported instead of worked around. I found no evidence of anything
being smoothed over.

**Required before sign-off, in priority order:**

1. **Correct the `ls -b` rationale** in `src/linecount.py` (lines 9 and 183), `ADR-0008` (lines 53
   and 106) and `docs/architecture/overview.md` (line 62). It is wrong, it is contradicted by a
   transcript in the same item, and it is a comment in shipped source that a maintainer would act
   on. `wc` alone is the correct comparison.
2. **Correct the closing claim at `EP-001/journal.md` line 608, or file the `BrokenPipeError`
   behaviour as a defect.** A closure summary asserting "never a stack trace" while the repository
   holds a measured reproduction is the one substantive overclaim here.
3. **Resolve the two dangling shas** (`1d10023`, `2946f57`). A reproduction pinned to a commit
   nobody can check is not evidence.
4. Ride-alongs: the `184`/`185` line-count gap and the impossible `164 → 175` figure against
   `06fc185`; BUG-0002's D5 counts; the question undercount at `EP-001/journal.md` line 609.

**Standing caveat 1 — chronology.** I cannot certify *when* anything happened from the tracker.
Three items' history tables are demonstrably invented, and their journals disagree with them by
over two hours. Anyone reconstructing the sequence must use `GIT-LOG.md`. The tooling fix
(monotonic clamping) prevents recurrence but permanently degrades the meaning of a `when` column,
and nothing in the tracker warns a reader of that.

**Standing caveat 2 — assurance value.** One actor played customer, analyst, architect, developer,
verifier and reviewer. The record is honest about this in two files and silent about it in the two
files most likely to be read. Nothing here should be presented to a third party as independently
verified work without that caveat attached.

**A note on the shape of the failures.** They cluster, and the cluster is informative. Every
substantive judgement I could test was right: the decisions, the fixes, the criteria, the
mutations, the gap register, the encoding analysis. What failed was *transcription* — timestamps,
line counts, row counts, commit shas, a tool's flag, a question tally. The record is strong
wherever it reasons and weak wherever it counts, and its review layer, which is where counting
errors should die, passed every one of them. If this methodology is to be used again, the
cheapest improvement available is not more prose in the reviews; it is making the numbers in them
machine-checked, the way the commit references already are.

Judged as what it evidently is — a methodology exercise producing real, working software — this is
still a good record, and better than most real project records I could expect to audit, chiefly
because it repeatedly writes down what it did *not* check. Several of the eleven problems in
section 5 — the clock failure, both AC6 wordings, the `BrokenPipeError` measurement — are things
the record disclosed about itself and I merely confirmed. That is the behaviour I want from a
record. It is the ones it did not disclose that keep this a qualified sign-off rather than a clean
one.

---
---

# Addendum — WI-0003 and the epic's third closure

**Audited 2026-08-17, after the report above.** The project changed under me: a sixth item was
added and closed, and `EP-001` was reopened a second time and closed a third. Same read
restrictions as before. Same method — I ran every acceptance criterion myself rather than reading
the reports' word for it.

This addendum covers only what changed, plus the status of the four corrections the report above
required.

## A1. What the sixth item added, and whether the record supports it

`WI-0003` adds `--sort name` / `--sort count`, choosing whether rows come out in filename order or
in the delivered count order. The stated purpose is narrow and concrete: the author keeps two
folders meant to hold the same notes, and a count-ordered listing shuffles them differently, so the
two outputs cannot be compared by eye (`WI-0003/item.md` `## Story`; the human's own framing at
`EP-001/journal.md` lines 689–694).

The tool grew from 191 to 244 lines and from 60 to 77 tests, gaining `parse_sort` and `sort_rows`.
One ADR (ADR-0009), `overview.md` v5 and `vision.md` v3 accompany it.

**I ran all ten acceptance criteria against the delivered code.** All ten hold as written:

| AC | what I ran | result |
|----|-----------|--------|
| AC1 | `--sort name` on `Zebra.md`(2), `apple.md`(7), `notes.md`(5) | ` 2  Zebra.md` / ` 7  apple.md` / ` 5  notes.md` / `14  total`, exit 0 — byte order, uppercase first, exactly as written |
| AC2 | `--sort name` on two folders with the same three names and different counts | both name columns `ideas.md, notes.md, todo.md`; identical order despite counts of 1/3/9 against 44/20/2 |
| AC3 | `--sort count` vs no flag, `cmp` on both streams | identical, both exit 0 |
| AC4 | the 77-test suite; the no-flag path | passes; no-flag output unchanged |
| AC5 | `-s name` | argparse error, empty stdout, exit 2 |
| AC6 | both values on an empty folder | `no files`, exit 0, no total row |
| AC7 | `--sort size`; `--sort` with no value | `linecount: --sort: 'size' is not 'name' or 'count'` — one line, exit 2; missing value falls to argparse, exit 2 |
| AC8 | all three spellings, `cmp` | identical |
| AC9 | `--top 2 --sort name` | exit 0, two rows, `14  total (all 3 files)` |
| AC10 | `python3 -m unittest discover` | `Ran 77 tests … OK` |

I also re-ran the three earlier bug reproductions against the new code: the symlink loop, the
all-unreadable folder and the undecodable filename all still behave as their items require. Nothing
regressed.

**The best thing in this item is what it refused to decide.** `--top` and `--sort` together select
different files under two equally defensible readings. The human was asked, declined, and then
declined the fallback of letting the analyst record an assumption in his name
(`WI-0003/artifacts/refinement-qa.md` lines 55–64). What the record then did is the part worth
noting: `refine` tagged it `[unresolved]`, `plan` wrote ADR-0009 to explain that nothing was
decided and why, AC9 was written to bound the *shape* of the combination (exit 0, at most N rows,
the labelled total) without fixing its content, and the item's `## Notes` explicitly instruct
`plan`, `implement` and `verify` not to file a question about it, because escalating would get it
decided by someone other than him.

I checked whether that held. It did. `--top 2 --sort name` on the criteria's own folder returns
`Zebra.md` and `apple.md` — the two alphabetically first, not the two largest — which is precisely
what ADR-0009 line 71 says falls out of writing no code for it, what `impl-report.md` line 72
records as an observation, what `verify-report.md` line 26 refuses to treat as a verdict, and what
`item.md` `## Notes` carries forward as an accepted gap. Four documents, one consistent story, and
none of them claims it was chosen. Leaving a question open through plan, implementation,
verification and review without anyone quietly closing it is harder than answering it, and it was
done.

**The numeric claims check out this time,** which matters given what the first report found. The
test file is 814 lines against 642 before, exactly the `172 0` numstat the review and verify report
both cite; `linecount.py` is 244 against 191, consistent with the 63-line figure at +63/−10; and
the two commit counts (`all 1 commit(s)` at implementation, `all 5 commits` at review) are both
correct against the merge bases the record names. This is the class of claim that failed repeatedly
in the first five items.

## A2. The reopening and the third closure

**Legitimate on its face, and the record explains it.** `EP-001/history.md` carries
`done → open` at 23:49:51Z by `intake`, reason "reopened for WI-0003: the human asked for a
`--sort` option against the delivered tool", and `open → done` at 00:27:37Z. The mechanism is the
same `spec/ids-and-statuses.md` §3.4 route used for the three bugs.

Two things about it are better than they had to be:

- **The record notices that §3.4 does not obviously cover this case.** §3.4 is written about
  *defects*; this is a feature request. `EP-001/journal.md` lines 633–639 says so, states that the
  honest reading is arguable, and records that the choice was put to the human rather than taken by
  the analyst — "it's the same tool and the same folder-full-of-files problem". That is the right
  handling of a rule being stretched.
- **The epic's success measures were amended at the reopen, not left alone.** A seventh measure was
  added — the two-folder comparison, in the human's own words — with the explicit reasoning that a
  reopened epic still listing only the measures its first closure met would let `review-close` close
  it again without testing what the new item delivers (`EP-001/journal.md` lines 640–645). Each
  measure is marked in `item.md` as added at the reopen, so a reader can see which bar the earlier
  closures were judged against. I re-ran the seventh measure myself: two folders, same five names,
  different contents — count order gives two different name columns, `--sort name` gives identical
  ones. Met.

One wrinkle, disclosed rather than found by me: WI-0003 was created at 23:48:51Z and the epic
reopened at 23:49:51Z, so for sixty seconds a draft item sat under a closed epic — the exact state
that produced `EP-001/Q-001` the first time round. The intake entry names the resulting
`workspace-valid` failure and says the move fixes it (lines 748–750). Also recorded there:
`scripts/transition` still cannot clear `outcome` on a reopened epic, so the field had to be edited
out by hand for the second time. Both are logged as methodology defects rather than quietly
absorbed.

## A3. The blocking question

`WI-0003/Q-001` is the first question in this project's history to suspend an item, and it is a
good one to have blocked on.

- **Who filed it, and why they could not resolve it.** `review-close`, at `in-review`, with every
  other Definition-of-Done criterion already passing. D7 requires that documents the change
  invalidated be updated; `vision.md` v2 described `--sort` as "being added … not delivered at the
  time of writing", which merging would make false. `review-close` may not edit `product/vision.md`
  — `spec/doc-header.md` §5 allocates that document to `intake`, `refine` and `answer-questions` —
  and the reason it may not is exactly the circularity in play here: it would be editing the
  document and then certifying D7 and DE4 against its own edit (`Q-001` lines 35–40). So the skill
  that found the problem was structurally barred from fixing it. That is the correct reason to file
  rather than act.
- **It was labelled honestly.** `blocking: true`, and the item genuinely moved to
  `awaiting-answer` with `resume-to: in-review`. Contrast the first report's finding that
  `BUG-0001/Q-001` was filed `blocking: false` while stating in its own text that it blocked
  everything. This one does not do that.
- **Who answered, and what changed.** `answer-questions` took option A: `vision.md` v2 → v3, the
  `--sort` bullet's parenthetical changed to "(delivered, WI-0003)", with a change-log row. Nothing
  else in the document was touched, and the answer says why the minimum edit was the right one. No
  criterion was amended, no ADR written or superseded, and `Q-001` line 143 states explicitly that
  ADR-0009 is untouched — the answer does not use the opening to settle the question the human
  refused to settle.
- **Did the item resume where the record says?** Yes. `history.md` row 12 is
  `awaiting-answer → in-review`, actor `answer-questions`, matching the `resume-to` recorded on the
  row that suspended it; the item then closed from `in-review` in the following row. The second
  `review-close` execution is a separate journal entry, and `review.md` line 3 names both
  executions. I checked all four and they agree.

The answer also flags its own weak point without being asked to: the vision is edited saying
"delivered" *before* the merge that delivers it, so the word is true only as of the execution that
follows (`Q-001` lines 115–121). That is the kind of caveat most records leave out.

One bookkeeping slip: `answered-at: 2026-08-17T00:20:02Z` is one second *after* the history row
that resumed the item (`00:20:01Z`), so the record has the item resuming before the question was
answered. Trivial in itself, and the same class as everything in A5.

## A4. Status of the four corrections the report above required

Plainly, one by one. **Three of the four are untouched.**

**1. The `ls -b` rationale — NOT corrected, and it spread.** Still present, unchanged, in
`src/linecount.py` lines 14 and 236, `ADR-0008` lines 53 and 106, and
`docs/architecture/overview.md` line 66. It also propagated into a seventh document during this
item: `WI-0003/artifacts/verify-report.md` line 52 records the undecodable name as "printed as
`ls -b` prints it". I re-ran the comparison on the current code: `ls -b` prints `bad\377.txt`, the
tool prints the raw byte, `wc` prints the raw byte. The claim was wrong when I raised it and is now
repeated once more, in a document written after I raised it.

**2. The stack-trace overclaim — NOT corrected, but the new closure is more careful.**
`EP-001/journal.md` line 608 still reads "printing a number, never a stack trace". `BrokenPipeError`
still reproduces on the delivered code — I ran it again: 5000 files piped to `head -1`, traceback,
first-stage exit 1. The journal is append-only so that line cannot be edited, but nothing forbids a
later entry correcting it, and this project has done exactly that before (the reversal of the
epic's `outcome` field). No correcting entry exists. In mitigation, the third closure's own summary
(lines 863–865) enumerates the input classes it survives — "subdirectories, unresolvable symlinks,
unreadable files, binary files, names that are not valid UTF-8" — rather than repeating the
absolute, and every class it names does hold. The new claim is defensible. The old one still stands.

**3. The two dangling shas — NOT corrected.** `1d10023` (`EP-001/journal.md` line 543) and
`2946f57` (`BUG-0003/artifacts/plan.md` line 12, repeated in that item's journal) still resolve
against neither `GIT-LOG.md` nor `GIT-BRANCHES.md`. `plan.md` is an editable artifact — this
project amended a plan in place during BUG-0003 — so at least one of the two was fixable.

**4. The ride-alongs — one fixed, the rest not.** The question undercount **is** fixed: the third
closure says "six questions asked and answered inside the record" (line 865) and DE5 says "six
questions exist across the epic and its children", both of which I verified as correct. The
`184`/`185` line-count gap, the impossible `164 → 175` figure against commit `06fc185`, and
BUG-0002's wrong D5 counts are all untouched.

Worth being precise about *why* the one that got fixed got fixed: not because it was on a list, but
because `review-close` recounted the questions from scratch while closing the epic. The same is
true of the vision's silence about `--top`, which the first report noted as an accepted gap — it was
closed because the human raised it again at intake, not because anyone tracked it. This project has
no route by which a known-wrong statement in a *closed* item's documents gets retired. D7 asks
whether the current change invalidated a document; nothing asks whether anything already written is
still true.

## A5. New problems

**1. The overview's change log got worse, not better.** My earlier finding was that v4
(`01:36:00Z`) predated v3 (`01:50:00Z`). v5 is now stamped `2026-08-17T00:05:00Z` — earlier than
both — and shares that timestamp exactly with v2. Three of five rows are out of chronological
order and two different versions claim the same instant.

**2. Three ADRs claim the same second.** ADR-0004, ADR-0005 (both WI-0002) and ADR-0009 (WI-0003)
are all stamped `2026-08-17T00:05:00Z`, though `GIT-LOG.md` puts the commits that introduced them
roughly four hours apart. The doc-header timestamps in `docs/` remain the one place the clock
correction never reached.

**3. History rows are now honest; journal headings still are not.** This is a real improvement and
a real remaining gap. WI-0003's history rows track the git commits within a minute or two and several match
exactly — the monotonic-clamp fix worked, and nothing in this item resembles the three bug items'
six-second histories. But the journal headings are still chosen values, and they now cluster
implausibly: the `verify` entry is headed `00:20:00Z` while its own history row and its own commit
`b6c7414` are both `00:12:35Z`, and `verify-report.md` line 5 repeats the `00:20:00Z` figure. On
the record, verification is therefore dated seven and a half minutes after it happened and *after*
the `review-close` execution that filed `Q-001` about it (question created `00:15:13Z`). Three
documents, three incompatible orderings of the same two events.

**4. Another item miscount.** `EP-001/journal.md` line 752 records `validate-workspace` returning
"8 items, 10 documents". There were seven items at that moment. The same entry's document count is
right, and line 582 of the same file uses the same convention correctly for six.

**5. The D5 counting error recurred, one item later.** The first report flagged
`BUG-0002/artifacts/review.md` for certifying "a journal entry per execution; history chains" on
counts that were wrong. `WI-0003/artifacts/review.md` line 10 does it again, and contradicts itself
inside one sentence: "seven entries for seven skill executions (… `review-close` has two …)". Six
other skills plus two `review-close` executions is eight, and `journal.md` holds eight entries. D5
remains the criterion whose entire job is counting, and it remains the one being passed on bad
counts.

**6. An instruction to a downstream skill was overridden without the instructing document saying
so.** `EP-001/journal.md` line 715 tells `refine` it "must choose, mark it `[assumed]`, and write it
as a criterion" for the `--top`/`--sort` interaction. `refine` did not, because when it asked again
the human refused the assumption route as well. That is the right outcome, and it is visible from
the item — `refinement-qa.md` line 46 opens "You told me to pick", so the departure is deliberate
and on the record. But a reader of the epic's journal alone is left with an instruction that was
never carried out and no marker saying so. Reconcilable only by reading both files.

## A6. Updated verdict

**The sixth item does not change my sign-off, and standing alone it would earn a cleaner one than
the first five.** Its criteria are decidable and all ten hold under my own commands; its numeric
claims are consistent for the first time in this project; its blocking question is labelled
blocking and resumed exactly where the record says; the epic's bar was raised before it was
re-cleared rather than after; and it managed the genuinely difficult thing of carrying an
unanswered product question through four skills without anyone answering it on the customer's
behalf. Its self-criticism — the reviewer's finding against the pipeline's own merge-ordering gate
— is aimed at the tooling rather than at nothing.

**But my report is now a follow-up, and follow-ups are judged on what was fixed.** Three of the
four required corrections are untouched, one of them propagated into a new document written after
I raised it, and two findings I flagged as patterns (the doc-header timestamps, the D5 counts)
recurred rather than being contained. The single correction that did land was re-derived
independently by a skill doing new work; nothing acted on it as a finding.

That changes what I would tell a manager. The first report said, in effect: *good record, four
things to fix.* The honest second reading is: **good record, produced by a process with no
mechanism for fixing anything already closed.** Each item's Definition of Done asks whether *this*
change invalidated a document. Nothing anywhere asks whether something written three items ago is
still true, and the `ls -b` error — wrong in two comments in shipped source, propagating on its
sixth and seventh outing — is what that absence costs. Two verifications, three reviews and two
epic closures have now read past it.

**Sign-off: unchanged — qualified yes, and the qualifications are the same ones.** I would add one
recommendation. The `ls -b` correction should no longer be tracked as a defect in a document; it
should be tracked as evidence that this methodology needs a standing check — a periodic re-read of
the claims in `docs/` against the code, owned by someone, on the same footing as the regression
pass that found the three bugs. That pass exists for behaviour. Nothing equivalent exists for
prose, and prose is where every uncorrected finding in this project lives.

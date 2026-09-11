# Final report — builder session six: the citation grammar, and what happens when it bites

Date: 2026-09-11. Units META-166 (planning) … META-174, eight of them executing work:
META-167 `cd00504`, META-168 `656b6c5`, META-169 `c8f69b3`, META-170 `b6ff22f`,
META-171 `55d7f03`, META-171b `68e65fb`, META-172 `73223e2`, META-173 `9919b45`, each with
its own write-ahead checkpoint commit. Mission: `meta/BUILDER-6-PROMPT.md`. Predecessor:
`meta/FINAL-REPORT-5.md`, whose ROADMAP §4 stamp left two staged iterations and a ledger of
21 open entries.

This was the compact session between iteration 5's abandonment and its re-run. Iteration 5
died at turn 11 on a single validator error that **was not a citation at all**: a history
row's prose named the form `path:line` while explaining that four real citations had been
falsified, and the gate scraped the mention as a use. Every unit ran in a dedicated
sub-agent that committed and pushed; the orchestrator held the mission, `meta/plan.md`,
`meta/CHECKPOINT.md` and each unit's verdict.

`./scripts/check` is green: **`check: all steps passed`, 47 steps** (45 at the close of
session five; step 6a from META-168 and step 15d from META-170). `fixtures/broken-workspace`
is **110 codes** (108). `scripts/lib/selftest.py` is **419 cases** (356 as reported then, 357
as measured at the start of this session). `harness/tests/test_harness.py` is **195 tests**
(176 at this session's first commit). The ledger holds **139 entries** (136), every one
carrying a readable status.

Every number here was re-measured out of the repository for this report. Two corrections that
produces are stated rather than smoothed over:

- **The harness suite was 176 tests when this session opened, not the 110 FINAL-REPORT-5
  reported.** The difference is not this session's: `811e872` and `08e3731`, between the two
  sessions, added the ops mechanics layer (`status.py`, `watch.py`) with its tests. This
  session added 19 (176 → 191 → 195).
- **`meta/CHECKPOINT.md`'s five headline numbers — 47 / 110 / 419 / 195 / 139 — all held**
  when checked against the tree. Where a unit's own journal entry and the checkpoint differ
  elsewhere, the journal entry was written from the code and wins.

---

## 1. What changed

Three clusters, one theme: **what a citation is, who is told, and what happens to an
engagement when the answer is wrong.**

### 1.1 The mask is unified across every citation surface (META-167, `cd00504`)

The citation vocabulary is scraped on **six record surfaces** and four of them were doing it
with a bare `CITATION_RE` — no mask, so a backticked example of a citation counted as one.
Three of the four were **presence** rules, which is the direction F-113 names: a quoted
example *satisfied* a requirement for a real citation.

- `scripts/lib/claims.py` gained `citations_in()` — every marker in a text that is a **use**
  rather than a mention, as `(line, body)` — and `carries_citation()` over it, both built on
  the `masked_lines()` mask `problems_in()` already used. `problems_in()` is now a fold over
  `citations_in()`, so there is exactly one answer in the codebase to *is this marker a
  citation or an example of one*. The module docstring carries the surface→site→reader table.
- The four converted sites: `validate-workspace.check_substituted_criterion`,
  `check_adr_corrections`, `lint-answers` rule 3, `lint-claims` rule 2.
- **`lint-retro` was carrying F-054 in a private copy, in the opposite direction.** It masked,
  then read the citation body off the **masked** text — so a real marker whose path was written
  in backticks (which is how this repository writes every path) came back as `' '` and was
  reported as *"an empty citation"*. Confirmed by execution before the change; the brief did
  not know about it.
- **The brief was wrong twice more, and the unit corrected it from the code.** `arose-from`
  is not a `CITATION_RE` site at all — it is a frontmatter scalar resolved against the tree,
  and it is named in the docstring table as deliberately excluded. And
  `fixtures/broken-workspace` is compared as a **set**, not a multiset, so a new case emitting
  a code some other case already emits is invisible to the gate: each new mention case was
  placed as the only source of its code, and `claim.unsourced`, which cannot be made unique
  that way, is pinned by count in `scripts/check`.
- A fixture per surface, both directions; 12 new self-test cases; three mutations (mask off,
  `citations_in` stubbed empty, `carries_citation` stubbed true) and every new case dies under
  at least one.

### 1.2 Severity follows knowledge (META-168, `656b6c5`)

The mask cannot reach the row that ended the run: it was **bare**, not backticked, and a
writer naming a form in prose is entitled to. The resolver had been answering two different
questions with one message.

- A body that matches a known form and fails to resolve is a **wrong citation** — the gate
  looked — and stays an ERROR under `claim.citation.unresolved` / `retro.citation.unresolved`.
- A body that matches **no** form is not a verdict about anything: the gate looked at nothing
  and cannot tell a mention from a typo. It is now a WARNING under
  `claim.citation.unrecognised` / `retro.citation.unrecognised`, and a warning touches no exit
  code. Reporting a verdict it does not hold is exactly the over-claiming this repository
  refuses.
- The shape that makes this un-duplicable: `CitationResolver.resolve()` returns a `Problem`
  (kind + message) rather than a message-or-empty-string, and `Problem.report()` maps kind →
  level and code suffix in one place, the caller supplying only its namespace. A caller
  re-deriving *was this recognised?* from message text would be the
  two-readers-one-vocabulary defect `claims.py` exists to prevent.
- `[src: ]` stays an ERROR: an empty marker is a citation somebody made and left empty.
- A `run:` body with its outcome dropped **would** have been softened, and is not — the
  branch that should have caught it was unreachable (filed as F-115, §1.6), so it is guarded
  explicitly. The `run:` form carries the most evidence (F-070) and is the worst one to soften.
- **The cost is stated, not discovered:** `[src: WI-007]` — three digits — matches no form and
  now warns where it used to fail. The trade is defended by what the opposite choice has
  already cost: one whole engagement.
- The convention moved out of a validator source comment into `spec/doc-header.md` §4a
  (revision 10), where a writer reads it. F-113 and F-075 are **one class**, and both statuses
  say so.

### 1.3 A toolkit source is quoted, not pointed at (META-169, `c8f69b3`, ADR-0013)

§2 of this report. In outline: `[src: .claude/agile-skills/...]` is refused as
`claim.citation.outside-the-record` (ERROR), and a new form
`[src: toolkit: <document> <section> "<quoted words>"]` carries the same evidence inside the
marker. `claims.PRUNED_DIRS` states the pruned-directory list once for three readers — the two
record walks and the resolver — which is F-117's fix as well as ADR-0013's mechanism.

### 1.4 The grammar goes where the writer writes (META-170, `b6ff22f`)

F-114's placement half. A worker authored citations in good faith, learned the grammar by
tripping `validate-workspace`, and the run died of it — while the grammar sat in
`spec/doc-header.md` §4a and **no skill named it**. F-114's own grep over the abandoned
workspace's installed skills returned nothing, exit 1.

- **The set of skills is derived, never listed.** Which skills owe a citation is a fact in
  `skill.yaml`: an obligation statement — a quality gate's `description` or `manual_check`, or
  an exit criterion — that names a citation. Seven do (`answer-questions`, `implement`,
  `intake`, `plan`, `refine`, `retro`, `review-close`); `next` and `verify` oblige none.
  `scripts/check` step 15d re-derives the same seven the same way, so the pointer cannot rot,
  and an empty derived set is a **failure** rather than a silent pass.
- **The rule is deliberately the looser of the two.** It asks whether an obligation names a
  citation at all, not whether it also says *resolves*: `refine` R11 tells a worker to carry a
  measurement as a command-outcome citation (F-089) without ever using the word, and that
  writer needs the grammar as much as any other. The loose rule's failure mode is one more
  procedure pointing at the table; the strict rule's failure mode is F-114 itself.
- **Five lines each, pointing at the single source.** The table by name, plus the three traps a
  gate would otherwise teach: a path citation is workspace-relative and never points into the
  installed toolkit; a marker inside backticks or a fence is *naming* a form, not using one; a
  marker matching no form warns rather than fails. Pasting the table into nine files would be
  the same duplication defect committed in prose.
- **`review-close` sits on the runtime's ceiling.** Its rendered body was exactly 500 lines,
  the renderer's limit, so its pointer is a one-sentence form folded into step 9a and two
  paragraphs were rewrapped word-for-word to pay for the two lines. A skill at the limit cannot
  be told anything new without something moving.
- The same grep now returns 13 lines across all seven skills, exit 0.

### 1.5 A fixable record defect is not a verdict (META-171 `55d7f03`, META-171b `68e65fb`, ADR-0014)

§3 of this report. In outline: on a non-zero `validate-workspace` after a worker turn the
driver grants a **bounded self-repair allowance** — up to N consecutive repair turns, default
2 — and only a spent allowance is terminal.

### 1.6 Triage, and three defects met in flight (META-172, `73223e2`)

136 → 139 entries; no toolkit, harness or spec file touched.

- **F-115** — a gate message no input could reach. `_resolve()`'s *records a command with no
  outcome* branch was unreachable, because `resolve()` strips the body before matching and
  `RUN_RE` ends `\s*(?P<outcome>.+)$`. Dead on its own; under META-168's severity split that
  catch-all became a warning, so the form carrying the most evidence would have stopped
  touching the exit code. Found and fixed inside META-168; filed because the class deserves
  saying — a message nobody can reach is indistinguishable from a rule that holds, in the
  ledger, in a review and in a green test run.
- **F-116** — `render.py` runs `shutil.rmtree(dist)` and then `render_into(dist)`, whose
  `except RenderError` returns 1 with no rollback, because what it would restore from has just
  been deleted. META-170's over-limit `review-close` left six skills written and the shared
  tree never produced. **Open, not fixed** — it is a build-step change and that was a findings
  pass. Gated with F-111 on the next `adapters/` unit.
- **F-117** — the prune tuple written by hand in two files. **The hearsay was corrected by the
  code:** `git log -S` shows the two copies were byte-identical for their whole life, so the
  filed claim is the weaker, sounder one — two hand-written statements of one rule *are* the
  drift, and the cost shows when a third reader arrives. Fixed as `claims.PRUNED_DIRS`.
- **The sweep took nothing, and says why.** All 21 open-or-deferred entries were read against
  *trivially adjacent to clusters 1–3, no new derivation*; none passed. Fourteen are gated on a
  unit in a file no commit in this session opened — checked by looking, not assumed.
- **One gate had been met without anybody noticing.** H-015's gate is *the next harness change
  window with no run in flight and nothing being banked*. META-171 and META-171b **were** that
  window and spent it on ADR-0014. Defensible; unrecorded, which is not. H-015, H-020 and H-021
  are re-gated on the next window with the count carried: **reached once, passed once.** That is
  the third time a met-and-unnoticed gate has been found the same way.
- **F-098 re-measured rather than quoted:** 99 bare `ADR-nnnn` citations across 12 numbers in
  the current tree (was 97 across 11), of which 11 are already path-qualified, so the strictly
  bare surface is **88**. Both numbers are stated rather than one substituted for the other —
  and both new occurrences are ADR-0013's own.
- **F-068 re-checked rather than assumed:** `lint-claims --root examples/toy-project --all`
  still reports 41 errors, 0 warnings, all `claim.unsourced`. META-168's softening does not
  reach it, because there is no unrecognised marker there for it to reach.

---

## 2. The toolkit-path ruling — ADR-0013, and the record's own argument for it

Twelve `[src: .claude/agile-skills/...]` citations stand in iteration 5's abandoned workspace.
They resolved, and **nothing had ever decided that they should**: the body contains a `/`, so
it fell into the resolver's workspace-path branch and was answered by `os.path.exists`.

**The ruling is illegal as a path, legal as a quote.**

**(a) Refused.** A citation body resolving inside a directory the record walk prunes is an
ERROR, `claim.citation.outside-the-record`. An error and not META-168's warning, and the
distinction is exactly the one META-168's split turns on: an unrecognised marker warns because
the gate cannot tell a mention from a typo and declines to rule on what it has not checked.
Here it has checked, it knows precisely what is wrong, and it knows what to write instead.
There is no ambiguity to be honest about.

**(b) Replaced.** `[src: toolkit: <document> <section> "<quoted words>"]`. The document is how
the toolkit document names itself and is **never resolved against the filesystem** — that is
the point, not a weakness. The quote is mandatory and non-empty and may contain neither `]`
(it ends the marker) nor `;` (it separates sources). Verified by execution rather than
asserted: `toolkit:` does **not** swallow the rest of the marker the way `run:` deliberately
does (F-070), so one marker can carry two toolkit sources.

### The part that got sharper on contact with the code

One of the twelve is a line number: `[src: .claude/agile-skills/scripts/lib/claims.py:148]`,
supporting the sentence *"the test asks whether the token contains `/`"*.

**It was true.** At `181e69d` — the toolkit revision installed when that run executed — line
148 of `scripts/lib/claims.py` was:

```python
    if PATH_RE.match(token) or "/" in token:
```

Two toolkit commits later — `cd00504` and `656b6c5`, this session's own first two units,
neither of which the consumer's record had any part in — **line 148 is a blank line inside
`normalise_anchor()`, and the test the citation was about has moved to line 223.** The
citation is now false. Nothing said so, because nothing could.

That is the whole argument against an unpinned path into an upgrading toolkit, made by the
record itself rather than by a hypothetical. And F-077's cure for exactly this class is
unavailable here: a `path:line` citation is bounded by the file's length, but the bound would
be on the *toolkit's* file, which is not in the record, is 545 lines long so 148 is comfortably
inside it and the bound reports success, and is a different file from the one the citation was
written against. **A bound on the wrong file is not a weaker check; it is a check of something
else.**

### The other four forces, and what the code did to them

1. **Both record walks prune the same four directories — and each had the tuple written out by
   hand, separately.** That is the drift already started rather than a risk of it (F-117).
2. **`validate-workspace` over the banked evidence reports twelve `claim.citation.unresolved`
   findings, one per citation**, because `.claude/` was never banked with the record. Twelve for
   twelve stop resolving the moment the record leaves the machine. The run's own `Q-004.md:215`
   states *"Both citations resolve to files in the workspace"* — true when written, false in the
   banked copy of the same file.
3. **Pinning the version is the retroactive-invalidation trap.** §4a says *"a record written
   before this convention existed is not retroactively invalid"*; a version pin is that rule
   broken on a schedule rather than once.
4. **The claims being made are real**, and `lint-claims` rule 2 demands a citation for each —
   the run's record shows the gate doing exactly that and the author adding the citations in
   response. Refusing the path without providing a legal way to source a claim about the
   toolkit would reproduce F-050 exactly: a rule whose satisfying move does not exist is not a
   rule. That is why the ruling has two halves.

**The honest boundary, said in the table and in the ADR rather than discovered.** The gate
**cannot** tell whether the toolkit says those words; nothing is opened. It checks that the
citation carries enough for a **reader** to check it. That is strictly more than the path form
carried, which verified the writer's own installation and left a reader with a pointer they
could not follow at all.

**The twelve standing citations are untouched.** They are in `meta/harness/evidence/`, which
is read-only history; §4a's non-retroactivity rule covers them, and the ruling governs what is
written next. `git status` over `meta/harness/evidence/` was clean at the end of every unit
that could have touched it.

---

## 3. The H-022 decision — ADR-0014, and the correction that made its promise real

H-022 asked whether a fixable record defect should be terminal, and deliberately left it open.
The re-run inherits the answer, so it was decided here.

**The answer keeps both readings in the finding.** The run still halts on the defect — but the
**worker** is asked to fix it before a human is. On a non-zero `validate-workspace` after a
worker turn, `Driver.decide` grants a bounded self-repair allowance:

- **Up to N consecutive repair turns** — `--repair-turns`, else the iteration config's
  `repair-turns`, else **2** — read exactly the way `--max-turns` is read, so no existing
  config has to carry the key.
- **A repair turn is a worker turn with different instructions** (`harness/prompts/repair-turn.md`,
  logged with its own prompt version) whose only job is making the validator green: no
  dispatch, no advancing an item, nothing written under `.claude/`, no deleting a sentence to
  silence a gate.
- **Green resets the counter** and the engagement resumes where it was — re-derived from disk
  by the same branches that decide every other turn, so *where it was* is read, not remembered.
- **N+1 consecutive failures are terminal** `validator-failed`, with the original error
  preserved beside the last.
- **Not handed to the sim.** H-004's guard reschedules a worker turn to the stakeholder when
  human questions are open, on the premise that such a turn would halt at orchestrator step 2
  having done nothing. A repair turn never runs the orchestrator, so the premise is false, and
  firing would spend one of a bounded number of repair turns on something that cannot repair
  anything *and* lose the repair job. Logged as `repair-keeps-the-turn`.
- **Not exempt from the turn budget.** The budget's one exemption is for a turn that exists for
  the engagement's benefit, is one turn, is given once, and is last; a repair turn is none of
  those. Counting costs nothing irreversible: `engagement_terminal` never consults the
  validator, so a `turn-budget` stop taken mid-repair is resumable with the counter intact.

**Two derivations the code corrected.** H-010's *principle* carries and its *mechanism* does
not — `stop_is_resumable` is consulted in exactly one place, the branch that runs when a human
reruns the command, and this gap is *inside* the run. The same reading sharpened the rejection
of simple resumability: the recovery sentence it would have relied on offered `--reaudit`,
which clears only a contamination stop and **could never** have cleared this one. And the bound
is load-bearing in a way the derivation understated: the validator branch is the *first* test
in `decide`, so every other stop — the stall check included — is unreachable while the
validator is red.

### META-171b — the preserved original error names the defect, not the count

META-171 promised the *original error* is preserved, then reported honestly that the promise
was only nominally kept. `scan_project` kept `[-1:]` of the validator's output, so what the
stop preserved was `validate-workspace: 1 error, 0 warnings` — **a count, naming nothing.**
Iteration 5's whole value as evidence is that the first error was one nameable line. A
terminal stop that can only say "1 error" throws exactly that away, and the re-run is the
first engagement that can reach the exhaustion path — so the deferral was taken now rather
than carried past it.

- `validator_tail(output, limit=3)` keeps the validator's **ERROR** lines — the only lines in
  the report format carrying a path, a line and a code — bounded at three, followed by
  `... and N more errors`, and always ending on the summary, which is what a reader counts
  from. Output with **no** ERROR line (a green run, a crash, a usage error) keeps its last line
  and nothing else, byte-for-byte the old behaviour: the tail widens only when there is a
  defect to name. A forty-error workspace produces five lines, not forty-one, and says so in
  the fifth.
- **Every consumer was found before the shape changed** — three, and no more. The one that
  would have broken silently was `' '.join(...)` inside an f-string, which turns several lines
  into one unreadable run-on; it moved into `validator_detail(observed)`, now the single place
  a stop detail or log entry is built from the tail.
- Non-vacuity: stubbing the widening back to `[-1:]` fails all four new tests, the load-bearing
  one included — the exhausted stop could no longer name `tracker/items/WI-0002/history.md:14`
  or `claim.citation.unresolved`.
- **The deferral is recorded as taken, not quietly closed.** ADR-0014 is `status: accepted`, so
  it was repaired by `spec/doc-header.md` §4b's route: the present-tense claims were put right
  and an append-only `## Corrections` section carries two `erratum` entries quoting the removed
  clauses verbatim. §4b also asks for a change-log row and a version bump; ADRs under
  `meta/adr/` carry neither, and the section **says so** rather than inventing a header to
  satisfy a rule. H-022 got a new status bullet, not a rewrite of the old one.

**The cost, stated in the ADR rather than left to be found.** A worker told to make a gate pass
can make it pass dishonestly — delete the sentence, weaken the claim, edit the validator. The
prompt forbids all three by name and the contamination audit fails a run that writes outside
the project, and beyond that it is not enforced: a dishonest repair inside the workspace is
visible in the diff and in the repair turn's own journal entry, and detecting it is a
judgement, not a rule. That is the reason the default is 2 rather than something generous.

---

## 4. Versions bumped

**Seven skill contracts took PATCH bumps, all in META-170**, per `spec/skill-contract.md` §3
(a change to `skill.yaml` or `process.md` bumps the version in the same commit; PATCH for
wording that changes no contract):

| skill | from | to |
|-------|------|----|
| `answer-questions` | 0.6.2 | 0.6.3 |
| `implement` | 0.6.0 | 0.6.1 |
| `intake` | 0.5.1 | 0.5.2 |
| `plan` | 0.6.2 | 0.6.3 |
| `refine` | 0.6.0 | 0.6.1 |
| `retro` | 0.2.1 | 0.2.2 |
| `review-close` | 0.14.0 | 0.14.1 |

No gate, no output and no transition moved in any of them — each gained a five-line pointer at
the citation forms table (`review-close`'s folded into step 9a).

**What else moved, checked rather than assumed:**

- **`spec/doc-header.md` gained two revision rows**, which is how that document versions
  itself: **revision 10** (META-168 — naming a form is not using one; backticked or fenced is
  a mention; a bare body matching no form warns, a body matching a form and failing stays an
  error) and **revision 11** (META-169 — a toolkit source is quoted and attributed, not pointed
  at; the pruned-directory refusal and the `toolkit:` form, with the honest boundary stated in
  the section).
- **`methodology/pipeline.yaml` did not move**: still **0.10.0**, and it appears in no diff in
  this session. Nothing in clusters 1–3 changed a stage, a dispatch rule or a threshold.
- **`next` (0.6.0) and `verify` (0.5.1) did not move** — they are the two skills whose
  contracts oblige no citation, which is why step 15d derives seven and not nine.
- **`adapters/claude-code/dist/` was re-rendered** in every unit that touched a skill or a
  script; `dist/agile-skills/VERSION` carries the seven new rows, and `scripts/check` step 4
  refuses a stale tree.

---

## 5. The proof case, verbatim

The mission asked for both directions, and the anchor is deliberately **not** a hand-made
fixture: it is the record that actually stopped the run, which nobody wrote to satisfy this
rule. It is pinned as `scripts/check` **step 6a**, which copies
`meta/harness/evidence/iteration-5-envel-abandoned/` to a temporary directory and asserts both
halves on every run of the gate. Both outputs below were reproduced for this report by running
`scripts/validate-workspace` over a fresh scratch copy.

**The mention that used to end the run** — where an ERROR stood, at
`tracker/items/WI-0002/history.md:14`:

```
tracker/items/WI-0002/history.md:14: WARNING [claim.citation.unrecognised] 'path:line' matches no citation form, so this gate cannot tell a mention of one from a typo in one — put it in backticks if it is naming the form, or write one of the forms in spec/doc-header.md's citation forms table if it is a citation
```

Zero `ERROR` findings on that line. (The copy's other errors are `envel/` and `.claude/` never
having been banked with the record, and are not what this assertion is about.)

**A genuinely bad citation planted in the same row still fails**, which is the half that stops
the split from being a blanket softening:

```
tracker/items/WI-0002/history.md:14: WARNING [claim.citation.unrecognised] 'path:line' matches no citation form, so this gate cannot tell a mention of one from a typo in one — put it in backticks if it is naming the form, or write one of the forms in spec/doc-header.md's citation forms table if it is a citation
tracker/items/WI-0002/history.md:14: ERROR [claim.citation.unresolved] ADR-9999 is not an ADR in docs/architecture/adr/
```

A split that only ever softens is the same defect turned around: the mention must produce no
error **and** must still be reported, and a marker that names a form and resolves to nothing
must still fail.

---

## 6. Attestations

**Iteration 5r was staged and not run.**
`harness/iterations/iteration-5r-envel.json` is `iteration-5-envel.json` with `"id"` →
`iteration-5r-envel` and `"project"` → `envel-2`; `diff` reports exactly those two lines.
`queue-entry`, `probe`, `persona`, `max-turns` and both model fields are carried verbatim. It
was provision-verified in a throwaway root outside the repository —
`provision.py --dry-run` first, then the real invocation: 85 files committed, installer and
`workspace-init` run, allow-list merged, the provisioner's own `validate-workspace` clean (0
errors, 2 warnings, both the ones a freshly-initialised workspace always carries), a second
explicit `validate-workspace` reproducing that at exit 0 — and then the whole temporary root
was `rm -rf`'d, confirmed by `os.path.exists` returning False. The default throwaway root was
not used, because it still holds `envel` from the abandoned run.

**No `run_iteration.py` invocation was made in this session, in any mode, in any unit.**
`harness/runs/` carries nothing written by this session, and
`meta/harness/evidence/iteration-5-envel-abandoned/` has no file modified by it.

**The probe was not read.** `harness/skills/simulated-human/probes/iteration-5-envel.md` —
existence established by `os.path.isfile` (True) and `os.path.getsize` (**3396 bytes**) only.
Its contents were never opened.

**One disclosure, which belongs in this report rather than in a footnote.** During META-173, a
`grep` over `meta/harness/PROJECT-QUEUE.md` looking for queue entries printed that file's
**one-line summary of the project idea** — the entry's first bullet, which the queue itself
labels as verbatim probe §1. It is a single sentence describing the kind of command-line tool
the engagement builds; it names no planted probe, no persona behaviour and nothing about the
ending. It was seen only inside that unit's sub-agent context, which is discarded, and it never
entered the orchestrating session; the probe file itself was not opened. It is not quoted here.
**The owner should weigh it when reading the recall measurement** — the held-out protocol's
value comes from nobody on the building side having seen the trail, and the honest statement is
that one line of framing was seen, in a context that no longer exists, rather than that nothing
was.

---

## 7. The recommended launch order

The order is FINAL-REPORT-5 §8 and ROADMAP §4's, and the reasoning still holds. One
substitution: **step 1 is now the re-run.**

**1. Iteration 5r — `envel-2`, `pragmatic-manager`, 30 turns.** It runs first because it is the
only step whose value is destroyed by anything happening before it: a held-out calibration
engagement stops being held out the moment somebody reads it or changes a skill in response to
something else. It carries the same two jobs the original did — the probe firing at the end
(partial acceptance at sign-off, targeting **E2 delivered-partial**, still never executed) and
the **held-out retro calibration** with the product source tree and git history present, the
two inputs no banked record can supply.

**Why the substitution is legitimate:** iteration 5 stopped at turn 11, before any dispatch. It
produced **no ending and no retro**, so the calibration it was launched for was never taken and
there is nothing to re-take. The re-run is the same queue entry against a fresh project, which
is why the config carries `queue-entry` verbatim rather than inventing a second rationale. It
also now serves as the regression gate for this session's work: the row that killed the
original is the exact row `scripts/check` step 6a replays.

**2. The owner reviews the trail independently and writes the findings down — before reading
the retro's report.** This is the strict protocol in the queue entry and the order is the whole
point: a reviewer who has read the retro's report cannot then produce an independent ground
truth against it. FINAL-REPORT-4 §4.2 is the precedent — a re-run there was not a measurement
because the procedure changed after the miss was read, and it said so where the figure
appeared.

**3. Read the retro's report and score it against step 2's list.** Only now. This is the first
recall number for `retro` that would be honest to quote: ground truth written first, live
inputs present, `retro` at 0.2.2 with no change made in response to anything it produced.

**4. Iteration 5b — `droll`, `ghosting-founder`, 20 turns.** The first live **E4**, and a cheap
mechanism regression rather than a calibration engagement: normal findings pass applies. It
runs **last** because it is the step most likely to produce a toolkit change, and a toolkit
change before step 3 contaminates the calibration. Success is the engagement ending **through**
the mechanism — the silence threshold, `review-close`'s declaration, the ending statement
naming delivered and orphaned children by ID, the driver recognising a declared E4 as a
terminal stop rather than a stall. A 5b that ends E4 by the driver's stall detection is a
failure of session five's work however tidy the transcript looks.

---

## 8. What is not proven

The house standard is that this section is why the rest is trusted.

- **No live run has exercised ADR-0014's allowance.** It is 19 harness tests (15 in META-171, 4 in META-171b) and 15 mutations,
  and not one repair turn has ever been taken by a worker. Whether a worker *can* recognise and
  repair its own record defect is the open question the mechanism exists to answer, and it
  stays open.
- **The re-run is the first engagement that can reach the exhaustion path** — and reaching it
  requires a defect the worker fails to fix three turns running. A clean run proves the
  allowance was never needed, not that it works.
- **META-171b's widened tail has never printed in a real stop.** What it would have said for
  iteration 5 is reconstructed from the banked record, not observed.
- **`retro`'s held-out recall is still unmeasured.** Iteration 5 produced no ending and no
  retro, so ROADMAP §4 step 1's number was never taken. Everything §7 says about it is a plan.
- **F-116 is open: a failed render wipes `dist/` with no rollback.** The blast radius is a
  consumer provisioned with a subset of skills and, in the observed shape, no shared tree at
  all. The interim guard is written into the entry rather than assumed — `dist/` is tracked (72
  files) and `scripts/check` step 4 refuses a stale tree — and the fix is gated with F-111 on
  the next `adapters/` unit.
- **The `toolkit:` form is uncheckable by the gate, by design.** Nothing is opened; a writer who
  invents a quotation passes. The claim is only that the citation carries enough for a
  **reader** to check it, which is strictly more than the path form carried and strictly less
  than verification.
- **META-168's softening is a real weakening and has not met a live workspace.** A typo'd body
  matching no form now warns where it used to fail. F-068's re-measurement (41 errors, all
  `claim.unsourced`) shows it changes nothing *in the toy project* — because there is no
  unrecognised marker there for it to reach. That is evidence about one workspace, not about
  the change.
- **F-114's placement fix is proven present, not proven read.** Step 15d asserts that seven
  skills name the forms table and that the table's heading still exists. No writer has yet
  learned the grammar from it in a run, and the thing F-114 was filed for — a worker authoring
  in good faith and finding out at the gate — can only be disproved by a worker.
- **The per-surface fix covers the six surfaces the record model enumerates, and one of the six
  has no fixture on disk.** `lint-answers` rule 3 reads a diff, so its mention/use pair is
  proven by execution inside the self-test rather than by a file in
  `fixtures/broken-workspace`. `arose-from` is excluded deliberately (a frontmatter scalar, not
  a `CITATION_RE` site) and the exclusion is named in the docstring table so the question is not
  silently reopened.
- **`PRUNED_DIRS` has one literal and no equality test.** F-117's own entry says it: nothing
  executes a walk-versus-resolver comparison. The guarantee is that there is **no second
  literal to drift from**, not that a divergence would be caught.
- **Provision verification is not a run.** 5r's config was provisioned into a throwaway root
  and torn down; nothing exercised the driver, the sim, the worker or any skill.
- **The proof case is one row of one run.** It is the strongest anchor available — a record
  nobody wrote to satisfy the rule — and it is still a single instance of a single surface.
- **Nothing session five built has met a stakeholder either.** ROADMAP §4's headline — *the
  undefined region is defined; nothing in it has met a stakeholder* — is unchanged by this
  session. The document-as-deliverable model and the E4 mechanism remain derived, fixtured and
  unrun.
- **21 open ledger entries were swept and none was taken.** Every gate is written down and, with
  the harness window's single exception, **none has been taken.** The harness window was
  reached once and passed once; the next one is not scheduled.
- **F-098 is not swept and this session made it slightly worse:** 99 bare `ADR-nnnn` citations
  over 12 numbers, 88 of them strictly bare, two of them added by the unit that built the
  distinguishable form and declined to run the sweep.
- **F-102 and F-103 stand as accepted gaps**, re-confirmed rather than closed.

---

## 9. The mission's acceptance checklist, line by line

**1. `./scripts/check` green; the cluster-1 per-surface fixtures and cluster-2 ruling fixtures
present and non-vacuous (mutation-checked, house style). — MET, with one qualification stated.**
`check: all steps passed`, 47 steps; `fixtures/broken-workspace` 110 codes; the self-test 419
cases. Cluster 1 shipped a mention/use pair on each surface and each new case was placed as the
**only** source of its code, because the fixture compares as a set; cluster 2 shipped two
refusal cases in `fixtures/broken-workspace` and two accepted `toolkit:` citations in
`fixtures/sourced-claims`. Non-vacuity was strong-form throughout: 3 mutations in META-167
(12 cases), 3 in META-168 (17 cases), **9 in META-169 (33 cases)**, 2 on META-170's new step,
14 in META-171 (15 tests), 1 in META-171b (4 tests) — and in every unit each new case dies
under at least one mutation. *Qualification:* the `lint-answers` surface's pair is proven by
execution in the self-test rather than by a file on disk, because that rule reads a diff.

**2. The abandoned workspace's actual trip is the proof case, both outputs reported. — MET.**
§5 quotes both verbatim, and they are a permanent gate step (6a) over a scratch copy of
read-only evidence, not a one-off run. Reproduced independently for this report.

**3. H-022 decided, implemented, tested; F-113/F-075/F-114 statuses current. — MET.** H-022 is
answered in ADR-0014 with two status bullets (META-171's decision, META-171b's taken deferral,
the last one current); the mechanism is in `Driver.decide` with both the recovery and the
exhaustion path tested in `RepairAllowance`. F-113 and F-075 carry a joint status naming them
one class; F-114 reads fixed in both halves — Direction (META-169) and placement (META-170).

**4. iteration-5r-envel staged, provision-verified, torn down; probe unread; not run. — MET,
with one disclosure.** §6 states all four as facts with their evidence. The disclosure — one
line of the queue's idea summary printed by a grep inside a discarded sub-agent context — is
recorded there rather than omitted.

**5. `meta/FINAL-REPORT-6.md` with what changed, the ruling and its reasoning, the H-022
decision, versions bumped, the proof-case outputs, the attestations, and the recommended launch
order. — MET on delivery of this document**: §1, §2, §3, §4, §5, §6, §7 in that order, plus §8,
which the checklist does not ask for and this repository's reports do not ship without.

---

## 10. What the next session should do

**Run iteration 5r and read what it says** — then steps 2, 3 and 4 of §7, in that order and not
in another. This session added no derivation that a run cannot now grade: the mask, the
severity split, the toolkit ruling and the repair allowance are all mechanisms with a live test
waiting for them, and the repair allowance in particular is the one thing here whose value is
entirely unknown until a worker meets it.

After the runs, the ledger's own order is unchanged from FINAL-REPORT-5 §10, with two
additions this session made: **F-116 joins F-111 on the next `adapters/` unit** (a failed render
leaving a partial `dist/` outranks a documentation fix in the same file), and **H-015, H-020 and
H-021 sit on the next harness change window with the count carried — reached once, passed
once.** If that window opens again and is spent again, the honest move is to say so in the same
sentence, for the fourth time.

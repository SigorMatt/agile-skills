# The two-session iteration harness — final report

Built 2026-08-21, units META-072 through META-081, against the design in
[`DESIGN.md`](DESIGN.md) and the queue in [`PROJECT-QUEUE.md`](PROJECT-QUEUE.md). Nothing in
`methodology/` or `spec/` was modified; the seven toolkit defects the build surfaced are filed as
findings, not fixed.

---

## 1. What was built

| Path | What it is |
|------|-----------|
| `harness/provision.py` | mechanical throwaway-project setup: git init with its own identity, the project's `.gitignore` and `SIMULATION-NOTICE.md`, a copy of the real `CONSUMER-PROMPT.md`, the installer, `workspace-init`, the USAGE §4 allow-list, one commit. Idempotent; refuses a non-empty stranger directory; `--trust` for the case in F-012 |
| `harness/run_iteration.py` | the driver: turn alternation, driver-computed status, stop conditions, the iteration log, transcript capture, resume, orphan reaping, `--reaudit` |
| `harness/audit.py` | the contamination boundary, read out of each turn's transcript and again off the project tree |
| `harness/tests/test_harness.py` | 29 tests; every rule gets a transcript it must reject and one it must accept. A sixth step in `./scripts/check` |
| `harness/prompts/worker-turn.md`, `sim-turn.md` | the two versioned turn prompts; the worker's carries the F-008 interim async protocol |
| `harness/skills/simulated-human/` | `SKILL.md` (how to be a human), three personas, four probe scripts — one per queue entry |
| `harness/iterations/*.json` | per-iteration config: project, persona, probe, turn budget, models |
| `harness/USAGE.md` | how the owner runs an iteration end to end |

## 2. Key decisions

All argued in [`ADR-0005`](../adr/ADR-0005-harness-execution-model.md), which also records the
headless Claude Code facts confirmed against both the current documentation and the installed
CLI (`claude 2.1.238`) — `--max-turns` works although this build's `--help` omits it;
`stream-json` exposes every `tool_use` input, which is what makes the contamination assertion an
observation rather than a promise; `-p` starts in Manual on every plan, so a permission mode must
be passed explicitly.

- **Turn zero belongs to the sim.** Otherwise the first worker turn has no idea to work on, and
  human-authored content would have two owners from the start.
- **The interaction channel is the toolkit's own question protocol**, assembled entirely out of
  paths `intake`, `refine`, `spec/question.md` §3 and `next` step 2 already specify. **No toolkit
  change was needed**, exactly as `DESIGN.md` §5 predicted, so F-008 stays deferred.
- **The human is simulated and the project says so**, in `SIMULATION-NOTICE.md` on disk rather
  than in a prompt, so the fact survives a fresh turn and the record never claims a real person
  said something.
- **The worker is trusted, the sim is caged.** The worker runs `bypassPermissions` in a throwaway
  directory with `AskUserQuestion` removed — so it structurally *cannot* ask a human who is not
  there. The sim has `Read,Write,Edit,Glob,Grep` and no shell, which is what makes "writes only
  permitted files" cheap to hold.
- **The driver never takes the worker's word for anything.** It parses the workspace itself, runs
  the validator, and logs any disagreement with the worker's `HARNESS-STATUS.md`.
- **The throwaway root defaults outside `~/git`**, because `/home/msi/CLAUDE.md` would otherwise
  be auto-loaded into every worker turn.

## 3. Acceptance, box by box

| Box | Evidence |
|-----|----------|
| provision produces a project that validates and whose skills a fresh session can see | `validate-workspace: 0 errors, 2 warnings` (both the honest post-init state); a fresh `claude -p` in the project listed all eight skills. Journal, META-073 |
| a mini end-to-end iteration on queue entry 1 | [`evidence/iteration-1-mini/`](evidence/iteration-1-mini/) — 8 turns, $48.51. Intake and refinement completed through the async protocol (16 questions, all answered in-file and propagated); **WI-0001 `done`** and merged; **both** planted probes consumed; workspace ends at **0 errors, 0 warnings** |
| contamination assertions fire on a deliberate violation and pass on the real run | `harness/tests/test_harness.py` — each rule has a fixture it must reject; all eight real transcripts re-audit to **0 violations** |
| driver restart | [`evidence/restart-test/`](evidence/restart-test/) — `SIGKILL` mid-turn, rerun resumed from `state.json`, re-ran the interrupted turn, reaped the orphaned child, trail intact at 0 errors |
| `harness/USAGE.md` verified by following it literally | followed for the mini run; three corrections came out of it (§3 on run-directory reuse, §9 on recovering from a contamination stop, and the `--trust` note in §2) |
| `./scripts/check` passes; `methodology/` and `spec/` untouched | 6 steps, all passed, no skips. `git diff --stat c9a62fb..HEAD -- methodology/ spec/` is **empty** |
| toolkit defects filed, not fixed | F-011, F-013 … F-018 in `meta/findings/FINDINGS.md`, and F-006 settled and rejected |

## 4. What the run found

**Seven toolkit findings, and every one of them was found by the worker, not by me.** That is the
harness working as intended: I did not have to notice anything.

- **F-011** — `answer-questions`' first precondition tells the only skill that can consume a
  human's answer that it has nothing to do. Left literal, the pipeline deadlocks.
- **F-013** — a blocking question on an **epic** is unrepresentable: `open` is terminal, the
  transitions into `awaiting-answer` are `from: any-non-terminal`, and the validator demands
  suspension anyway. Reproduced by hand: `transition: open → awaiting-answer by 'intake' is not a
  transition in pipeline.yaml`.
- **F-014** — `transition` evaluates `workspace-valid` against the workspace *before* the move,
  so every `answer-questions` resume prints a FAIL for correct work.
- **F-015** — `implement`'s own procedure guarantees `journal.execution.missing` mid-execution.
- **F-016** — epic-level record commits land on whatever branch is checked out, failing the
  commit-reference gate for an unrelated item.
- **F-017** — the restamp deadlock exists in `journal.md` too, and skills are writing *plausible*
  timestamps instead of reading the clock.
- **F-018** — the write-guard hook decides on the command string, not the write target.
- **F-012** (from the build, not the run) — a headless session discards an untrusted workspace's
  `permissions.allow` wholesale, which silently disables the setup `USAGE.md` §4 recommends.
- **F-006** is now **rejected**: the suspected allow-list entry matches correctly, proven by a
  probe with a control that failed as it should. Its symptom was F-012 all along.

**And one result that is not a defect.** `in-review → in-progress` — the review send-back, listed
in `meta/FINAL-REPORT.md` as never executed — fired **three times, organically**. `review-close`
rejected WI-0001 for a dead function, for a duplicated rule, and for an `AC8` violation that
**two `verify` passes had missed**. The reject → fix → re-verify loop did real work. Together with
the Definition of Ready override (seeded by a probe), two of the three dead paths named in
`meta/ROADMAP.md` §2.1 have now executed.

### Defects in the harness itself

Both found by running it, both fixed here, neither carried into iteration 2:

- **The contamination audit stopped two runs on false positives.** `W3` matched paths quoted
  inside a document the worker was *writing* (a question whose context repeated the stakeholder's
  own `~/trips/ski`), and then matched a bare `~` used as a `tr` separator and a markdown
  `~~strikethrough~~`. Fixed by distinguishing a path given as a tool argument from one scraped
  out of a command string, requiring the scraped one to exist, and requiring the tilde form to
  have a following slash. Each fix has a regression test named after the run it broke.
- **The worker turn prompt contradicted itself** (batch every question / stop on the first open
  one) and had no `stop_reason` for "the per-turn budget ran out", so two clean turns had to
  report `error` and explain in prose. Worker prompt is now **version 2**; the enum has
  `turn-budget-exhausted`. The worker reported both of these itself, which is the strongest
  evidence the status-report channel is worth having.

## 5. What this harness does not test

`DESIGN.md` §6 said a scripted sim cannot be surprised, annoyed or confused the way a real
reviewer can, and the run bears that out — manual peer-style runs remain a complementary track.
Two more, learned by running it:

- **It does not test the permission surface.** The worker bypasses permissions by design, so
  nothing here is evidence about `permissions.allow` (see F-012). Use `provision.py --trust` and
  a restrictive `--worker-permission-mode` if that is what you want to measure.
- **It is not cheap, and turn shape matters.** $48.51 for eight turns, with worker turns at
  $5–11 and 15–28 minutes each. A per-turn spend cap truncates a turn cleanly but costs a full
  re-read of the project's context on the next one, so a low cap is a false economy — budget the
  *run*, not the turn.

## 6. Running full iteration 1

```bash
cd /home/msi/git/agile-skills
./scripts/check                                          # the toolkit must be green and rendered
harness/provision.py --iteration iteration-1-expenses    # ~/agile-skills-throwaway/expenses
harness/run_iteration.py --iteration iteration-1-expenses --fresh
```

`--fresh` archives the mini run; drop it to resume instead. The default budget is the config's
(24 turns). Then review, in this order: `tracker/board.md` in the project, `SIM-LOG.md`
(`[PLANTED:` is coverage, `[ORGANIC]` is signal), `iteration-log.jsonl`, and the item trail.
`harness/USAGE.md` §5 and §8 are the full procedure.

The next entry after that is `iteration-2-tidy`, already configured, with its persona and probe
written.

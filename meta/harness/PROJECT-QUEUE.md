# Throwaway project queue

Location when adopted: meta/harness/PROJECT-QUEUE.md. Consumed by the harness:
each iteration takes the next entry; its probe section becomes the sim's
probe-script.md and its persona names a file under harness/skills/simulated-human/personas/.

Ordering rationale: iteration 1 forces all three dead paths at once (maximum
coverage first); 2 and 3 vary persona and probe mix to separate
persona-effects from pipeline-effects; 4 is the deliberately boring run that
tests the zero-bump gate (ROADMAP §2.1). Do not reorder without updating this
rationale.

After every iteration: owner reviews project trail + SIM-LOG + iteration log
(with the assistant), findings F-011+ appended, builder session if warranted,
versions bumped, re-render — then the next entry. A queue entry may be re-run
after fixes; a re-run is a new iteration with the same entry.

---

## Iteration 1 — `expenses` (expense splitter CLI)

**Idea (sim's opening statement):** "A command-line tool to track shared
expenses in my friend group: add people, add expenses paid by someone and
shared by some or all, and at any point show who owes whom. Data must survive
between runs. Python, no external services."

**Persona:** `cooperative-pm` — answers promptly and in good faith, terse,
never volunteers unrequested detail, defers to the team on technical choices
("whatever you think" is allowed and should occur at least once, to exercise
the recorded-assumption path).

**Planted probes:**
- **DoR override:** rounding. When refinement asks how uneven splits handle
  remainders (10.00 / 3), the sim answers "not sure yet — proceed anyway, we
  will decide later" and, if pressed, insists on proceeding. Target: the
  override path, exercised legitimately.
- **blocked:** one item must be "import expenses from my bank's CSV export."
  When asked for the format or a sample file, the sim answers "I will send a
  sample later" and never does. Target: `blocked` on a missing external
  artifact, and the driver's blocked-with-no-recourse stop condition.
- **send-back (natural):** no scripted lie; settlement math (minimal
  transaction set, penny allocation, negative/zero amounts) is edge-case-rich
  enough that verify has a fair chance of failing implement organically. If no
  send-back occurs by epic end, record that as a coverage gap in SIM-LOG —
  do not fabricate one this iteration.

**Success looks like:** override recorded and visible in history; CSV item
parked at `blocked` with the trail explaining why; epic otherwise done;
answers-as-assumptions marked; all probe actions tagged as planted in SIM-LOG.

### Re-run 1e — builder 2.5's regression run (2026-08-27)

**Rationale.** 1d reached the impasse and stopped there: `blocked-no-recourse`,
with the stakeholder recording on the closing turn that nobody had ever asked
them whether they accepted what was built (F-045), and that a bug the pipeline
had filed was never mentioned to them at all (F-046). Builder 2.5 derived the
termination model (`meta/adr/ADR-0006`) in response: an engagement has four
legal endings, and every one of them passes through a blocking question that
names every child item as delivered or not.

**The config and the probe are 1d's, unchanged** —
`probes/iteration-1e-expenses.md` is byte-identical to
`probes/iteration-1d-expenses.md`, and only `project` and `max-turns` differ in
the config. That is deliberate: the toolkit is the one variable, so a
difference in the ending is attributable to the fix and to nothing else.

**Success looks like:** the run reaches the same impasse it reached in 1d —
and this time **ends through the termination gate**. The sign-off question
fires with WI-000n and the bug both named, the sim answers it in persona ("no,
not as it stands"), the ending is recorded on the epic with what was and was
not delivered, and the driver stops on a terminal reason with zero
contamination violations. 1d ended with the stakeholder noting the question
never came; 1e ends with them having been asked.

---

## Iteration 2 — `tidy` (downloads-folder organizer CLI)

**Idea:** "A tool that organises a messy folder: moves files into
subfolders by type and age, with a dry-run mode that shows what would happen
before anything moves. Rules should be configurable."

**Persona:** `impatient-founder` — wants results, answers vaguely, pushes back
on process ("do we really need all these questions?"), occasionally answers a
different question than the one asked. Never abusive, just hurried.

**Planted probes:**
- **DoR override, adversarial variant:** the sim demands skipping refinement
  entirely on one item ("it's obvious, just build it"). Target: does refine
  hold the line, record a legitimate override, or cave silently? (Caving
  silently is a finding.)
- **send-back (scripted):** the sim's categorisation answer is
  wrong-then-corrected: initially "archives count as documents," then, when
  verify-stage output or a question surfaces the consequence, "no, that's
  wrong, archives are their own category." Target: a send-back transition
  driven by a changed requirement, and how the change propagates to docs.
- **No blocked seed** this iteration — isolates whether iteration 1's blocked
  handling was probe-driven or systemic.

**Extra scrutiny:** destructive-move logic makes verify's treatment of the
dry-run requirement a natural honesty check.

---

## Iteration 3 — `mdtab` (markdown table formatter)

**Idea:** "A filter that reads markdown on stdin and pretty-aligns its tables:
pads columns, honours alignment markers, leaves non-table content untouched."

**Persona:** `contradictory-stakeholder` — confident, gives answers that
conflict with earlier answers (scripted: multiline-cell behaviour contradicts
the earlier alignment answer). Target: does refinement/plan detect the
contradiction and raise a question, or absorb both into the record? Absorbing
silently is a finding (and feeds F-001's claim-provenance case).

**Planted probes:** the contradiction above (send-back or question expected);
otherwise clean — no override seed, no blocked seed. Edge-case-rich verify
territory (unicode width, escaped pipes, empty cells) may produce organic
send-backs; welcome, tag as organic.

---

## Iteration 4 — `recall` (flashcard CLI with spaced repetition)

**Idea:** "A flashcard tool: add cards, review due cards daily, simple spaced
repetition. Progress persists."

**Persona:** `cooperative-pm` again, with NO planted probes at all. The sim
answers every question well; the scheduling-algorithm ambiguity is real but
the sim resolves it when asked.

**Purpose:** the boring run. This is the zero-bump gate rehearsal
(ROADMAP §2.1): a clean idea, a good stakeholder, and the question is whether
the pipeline completes an epic with no skill version bumps, no forced
transitions, and a trail the owner signs off without findings. If iteration 4
is not boring, the queue continues with re-runs and new entries until a run is.

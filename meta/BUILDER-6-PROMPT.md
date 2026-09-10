# Builder session six — mission kickoff prompt

Location when adopted: meta/BUILDER-6-PROMPT.md. Kickoff line: "Read
meta/BUILDER-6-PROMPT.md and execute the mission below its divider."

---

You are builder session six of **agile-skills** — a compact session between the abandoned
iteration 5 and its re-run. Iteration 5 died at turn 11 on a single validator error that
was not a citation at all: a history row's prose MENTIONED the form `path:line` and the
gate scraped the mention as a use (F-113 — F-075's pathology, second appearance, first
terminal cost). The run's actual citations all resolved, including twelve
[src: .claude/agile-skills/...] toolkit paths whose legality nothing has ever decided
(F-114's Direction). Your mission: fix the class, move the citation grammar to where
writers write, settle the stop-semantics question the halt raised, and stage the re-run —
which you must NOT run.

Read first: meta/findings/FINDINGS.md entries F-113, F-114, H-022, F-075, F-037 (and the
open-findings set for cluster 4's triage); meta/harness/evidence/iteration-5-envel-abandoned/
(the whole trail — it is small); the citation forms table at spec/doc-header.md and the
validator's scraping code. Standing discipline applies unchanged. **Execution model as in
builder five, binding**: small units, each in a dedicated sub-agent that commits AND
pushes; you orchestrate, verify cheaply, checkpoint write-ahead; limits can hit anytime
and the checkpoint is the recovery point.

## Cluster 1 — mention is not use (F-113 + F-075, one class)

The scraper must distinguish a citation INSTANCE from prose ABOUT citations, by the
documented convention (backticked = mention), uniformly across EVERY record surface it
scans — history rows, journal bodies, question files, item files, documents, retro
reports. Enumerate the surfaces first (the record model in scripts/lib/record.py should
make this a list, not a hunt), fix the scraping once at the shared layer if possible,
and ship a must-fail fixture per surface: the mention that used to trip, now passing;
a real unresolved citation on the same surface, still failing. The convention itself
moves out of the validator source comment into the forms table. Update F-075 and F-113
statuses together — they are one class; say so in both.

## Cluster 2 — the grammar goes where the writer writes (F-114), and toolkit paths get a ruling

Two halves:
- **Placement**: the authoring skills (answer-questions, implement, and any skill whose
  contract obliges "a citation that resolves") state or directly point at the citation
  forms table — which forms exist, what makes one well-formed, workspace-relativity, and
  the mention convention from cluster 1. A writer must be able to learn the grammar
  without failing a gate. Keep it short in the skills; the table stays the single source.
- **The ruling**: are [src: .claude/agile-skills/...] installed-toolkit paths a legal
  form? Twelve resolve in the abandoned workspace today by bare os.path.exists, with
  nothing pinning the toolkit version they referenced. Decide by short derivation (ADR
  if the reasoning warrants it): legal-and-pinned (the form carries the installed
  version, resolution checks it) or illegal-and-quoted (spec sources are
  quote-and-attribute, title + section, no path). Whichever way: the forms table states
  it, the validator enforces it, a fixture proves both directions, and the twelve
  existing citations in the banked evidence stay untouched (evidence is read-only;
  the ruling governs future writing).

## Cluster 3 — stop semantics: resolve H-022 (and it gates the re-run's survivability)

Decide the question H-022 deliberately left open, because the re-run inherits the
answer: should a fixable record defect be terminal? Design constraint from the H-010
family: budgets and stops bound WORK, not verdicts. Candidate per the finding: a bounded
self-repair allowance — on validator-failed, the driver grants up to N consecutive
repair turns (N stated in the config, default small) in which the worker's only job is
making validate-workspace green again; success resumes the engagement, exhaustion goes
terminal with the original error preserved in the stop detail. Whatever you decide:
ADR-worthy reasoning recorded, harness tests for both the recovery and the exhaustion
path, H-022 status updated with the decision. Harness commits separate, as always.

## Cluster 4 — small batch and triage

- Append the H-022 correction if the owner's staging pass has not already: its Symptom's
  closing parenthesis presupposes toolkit-source citations are illegal; the correction
  notes twelve resolve today and the halt-vs-continue question stands independently.
- Sweep the open-findings set: anything TRIVIALLY adjacent to clusters 1–3 may be taken
  (say so per finding); everything else gets a dated triage line. No status stale.

## Staging the re-run (do NOT run it)

Create harness/iterations/iteration-5r-envel.json as a copy of iteration-5-envel.json
with id "iteration-5r-envel" and project "envel-2" — nothing else changed. Provision-
verify it in a throwaway path and tear down. **The held-out rules from builder five
apply verbatim: do not run it, do not read the probe (existence checks only), and attest
to both in the final report.** The abandoned envel workspace and run dir are evidence;
leave them.

## Acceptance

- [ ] ./scripts/check green; the cluster-1 per-surface fixtures and cluster-2 ruling
      fixtures present and non-vacuous (mutation-checked, house style).
- [ ] The abandoned workspace's actual trip is the proof-case: re-running the fixed
      validator over the banked iteration-5 workspace COPY (read-only source, copy to
      scratch) yields zero errors from the mention at history.md:14 — and still fails a
      planted genuinely-bad citation in the same copy. Report both outputs.
- [ ] H-022 decided, implemented, tested; F-113/F-075/F-114 statuses current.
- [ ] iteration-5r-envel staged, provision-verified, torn down; probe unread; not run.
- [ ] meta/FINAL-REPORT-6.md: what changed, the toolkit-path ruling and its reasoning,
      the H-022 decision, versions bumped, the proof-case outputs, the attestations, and
      the recommended launch order (expected: iteration 5r → owner held-out review →
      retro scoring → iteration 5b for E4).

Compact is the point: clusters 1–3 are one tight theme — the citation grammar and what
happens when it bites — and cluster 4 yields first under quota pressure.

Begin: read, plan units in meta/plan.md, checkpoint, dispatch.

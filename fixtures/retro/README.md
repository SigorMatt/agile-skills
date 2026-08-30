# Seven engagements, at the verdicts a retrospective has to reach

This is a **gate fixture**, not a workspace fixture. `scripts/lint-retro` is run over it;
`scripts/validate-workspace` is not, and the tree is deliberately thinner than a real workspace
(collapsed history chains, one-entry journals, no `docs/`). `fixtures/broken-workspace` and
`examples/toy-project` are where the validator's rules live. Mixing the two would mean every
change to an unrelated schema rule breaking this fixture for reasons that have nothing to do with
what it tests — the same reasoning `fixtures/ended-engagement/README.md` gives.

`EXPECTED-CODES.txt` is the exact multiset `scripts/lint-retro --all --require-scope` must emit
over this tree. `./scripts/check` compares it byte for byte, so a rule that stops firing is a
failure and so is a rule that starts firing twice.

| Epic | The report it carries | What must be reported |
|------|----------------------|-----------------------|
| **EP-001** | a retrospective written correctly | **nothing at all**, in both modes |
| **EP-002** | observations and proposals of the wrong shape | an uncited observation, a second one whose only marker is **quoted** rather than made, a citation that does not resolve, a proposal numbered `F-101` and marked `filed`, a classification outside the closed set, a `toolkit-defect` with neither counterfactual nor recurrence, a missing `Severity:`, and a proposal count that contradicts the frontmatter |
| **EP-003** | the sections wrong and in the wrong order | a missing `## Positive record`, `## Proposed toolkit findings` before the section it must follow, an empty `## Engagement retrospective`, an `ending` outside E1..E4, no `written`, an `engagement` naming a different epic, and 99 items claimed read in a two-item engagement |
| **EP-004** | a report that declares no scope at all | `retro.scope.degenerate` — the check that exists because a flawless engagement and an unopened workspace produce the same empty report |
| **EP-005** | a scope that names the epic and forgets its child | `retro.scope.item-unread` |
| **EP-006** | no report at all, on an engagement that has ended | `retro.missing` |
| **EP-007** | a report written while the engagement is still `open` | `retro.engagement.not-ended` |

**EP-001 is the one to read if you only read one.** A rule nobody can satisfy is not a rule, and
the counterpart to a must-fail fixture is a report a person would actually write that produces
**zero** findings — `fixtures/sourced-claims` is the same idea for `lint-claims`. It also carries
one entry of each classification, so the closed set is exercised in the direction that must pass:
a `toolkit-defect` with its counterfactual written, and a `project-circumstance` that says
plainly it proposes no change. That second entry is the shape the whole classification exists to
protect — "this engagement's goal arrived already decided" is a true and useful sentence, and
filing it as a defect in a skill is the failure mode `spec/retro.md` §7 is written against.

**EP-001 and EP-002 also carry the mention-versus-use pair.** A retrospective is the document in
a workspace most likely to *explain* the citation convention, and the first live run of the skill
wrote `` `[src: ...]` `` inside backticks and was told three times that its citations did not
resolve — then reworded its prose to satisfy the parser, which is the pathology F-073 named
(F-075). EP-001 now quotes a marker beside a real one and must still produce **nothing**; EP-002
carries an observation whose only marker is quoted and must be reported as citing nothing. Both
directions are needed: masking that swallows real citations is the worse failure of the two.

**EP-004 is the one that matters most.** A retro that opened no files produces a report with an
empty observations list, and so does a diligent retro of a flawless engagement. The declared
scope, checked against the workspace, is the only place a program can tell them apart. F-033 and
F-066 are that same defect twice in this project's own scripts, and reading is this skill's whole
job.

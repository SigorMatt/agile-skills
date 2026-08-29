# Six engagements, at the verdicts the termination gate has to reach

This is a **gate fixture**, not a workspace fixture. `scripts/check-epic-signoff` and
`scripts/engagement-state` are run over it; `scripts/validate-workspace` is not, and the tree is
deliberately thinner than a real workspace (collapsed history chains, empty journals, no
`docs/`). `fixtures/broken-workspace` and `examples/toy-project` are where the validator's rules
live. Mixing the two would mean every change to an unrelated schema rule breaking this fixture
for reasons that have nothing to do with what it tests.

Each epic is one historical contradiction, re-decided by the model in `meta/adr/ADR-0006`.

| Epic | What it is | `engagement-state` | `check-epic-signoff` |
|------|-----------|--------------------|----------------------|
| **EP-001** | the impasse ending done right: one child delivered, one blocked, one bug blocked, and a statement that names all three; the stakeholder said **no** | `at-rest` | **PASS** |
| **EP-002** | **F-046** — the statement names the delivered child and quietly omits the bug the pipeline filed | `at-rest` | **FAIL**, naming `BUG-0002` |
| **EP-003** | **F-045** — the engagement is over and nobody was ever asked. This is where a real run stopped, printed a board, and called it a day | `at-rest` | **FAIL**, no sign-off at all |
| **EP-004** | the acknowledgment was **deferred**: "I'll look at this properly next week" | `at-rest` | **FAIL** for closure, **PASS** for `open → blocked` |
| **EP-005** | still running — a child at `planned`. The control: not everything with nothing runnable *right now* is over | `active` | not run |
| **EP-006** | **F-064** — everything DE7 asks for, done correctly, in an engagement where nobody ever asked the stakeholder an open question | `at-rest` | **FAIL** on DE8 |

**EP-006 is the newest and the least dramatic.** Its sign-off is correct — it names its child,
it was filed after rest, the stakeholder accepted. What it never did was ask them anything that
was not on the team's own list, which is how a stakeholder in a real run carried two real
requirements through a whole engagement and mentioned them only in a closing note (F-064). DE8 is
presence and nothing more: it cannot tell a good open question from a perfunctory one.

**EP-001's statement is the one to read if you only read one.** It is what F-045 and F-046 were
asking for in the same breath: every child named, each marked delivered or not with one line of
why, and a real choice offered — including "do not accept". The stakeholder in the run this is
modelled on took that option and had nowhere to record it.

**EP-004 is the deferral asymmetry.** An engagement may be *parked* at the impasse on a "not yet"
— that is the honest record of where things stand. It may not be *closed* on one, because closing
claims an acceptance nobody gave. The gate learns which move is pending from `--resolving`, which
`run-gate` passes it; with no `--resolving` it applies the strict rule, because a gate that
relaxes when nobody told it anything is a gate that checked nothing (F-033).

Do not "fix" anything here. To change what is covered, change the fixture *and* the assertions in
`scripts/check` in the same commit, and say why in the commit message.

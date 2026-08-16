# Definition of Ready and Definition of Done

Two checklists, each a gate on a status transition:

- **Definition of Ready (DoR)** gates `draft → ready`. `refine` owns it.
- **Definition of Done (DoD)** gates `in-review → done`. `review-close` owns it.

Every criterion is marked with how it is checked:

- **[auto]** — `scripts/validate-workspace` decides it. An agent's opinion is irrelevant.
- **[skill]** — the owning skill decides it, and MUST record the evidence in its journal entry
  under `**Gates:**`. "I checked" is not evidence; the quoted criterion and why it holds is.

A checklist result MUST be recorded criterion by criterion, not as a single verdict. A skill
that writes "DoR passed" without the per-criterion record has not applied the checklist, and a
reviewer cannot tell which criterion was the weak one.

---

## 1. Definition of Ready — `work-item`

| # | Criterion | Check |
|---|-----------|-------|
| R1 | `item.md` has all required frontmatter, and `type`, `epic` and `priority` are set | [auto] |
| R2 | `## Story` names a role, a capability, and an outcome ("so that …") | [skill] |
| R3 | At least one acceptance criterion exists, labelled `AC<n>`, as a checkbox | [auto] |
| R4 | **Every** acceptance criterion is decidable by observation — a command to run, an output to inspect, a file to check. No criterion contains an unmeasurable adjective ("fast", "clean", "user-friendly") without a stated threshold | [skill] |
| R5 | `## Out of scope` names at least one thing a reader could reasonably assume is included | [skill] |
| R6 | Every open question on this item is non-blocking | [auto] |
| R7 | The item is independently deliverable: nothing in `depends-on` is unfinished, or the dependency is recorded and the item is sequenced after it | [auto] |
| R8 | The refinement Q&A is recorded verbatim in `artifacts/refinement-qa.md`, including which answers came from the human and which were assumed | [auto] |
| R9 | Estimated to be deliverable as one coherent change. If it is not, it was split, and this item is one of the parts | [skill] |

### The override

The human MAY override DoR and force an item to `ready`. When they do:

- `refine` records the override in `artifacts/refinement-qa.md` under `## Override`, naming
  **which criteria** were not met and the human's stated reason.
- The history row's `reason` MUST begin with `DoR overridden:`.
- The item's `## Notes` MUST carry the unmet criteria, so `plan` and `implement` see the risk
  they inherited rather than discovering it.

An override is legitimate and expected sometimes. Silently passing an item that does not meet
the checklist is not, and is the thing this section exists to make impossible to do quietly.

---

## 2. Definition of Ready — `bug`

A bug enters at `ready`, so `verify` (or whoever files it) applies this checklist at filing
time and records the result in the filing journal entry.

| # | Criterion | Check |
|---|-----------|-------|
| RB1 | `## Steps to reproduce` is a numbered list runnable without further questions | [skill] |
| RB2 | `## Actual behaviour` quotes real output — command, output, exit code — not a paraphrase | [skill] |
| RB3 | `## Expected behaviour` cites the acceptance criterion, doc, or ADR it contradicts | [skill] |
| RB4 | `found-in` names the item that delivered the behaviour, when it is known | [auto] |
| RB5 | Acceptance criteria include a regression test, or `## Notes` records why one is impossible | [skill] |

---

## 3. Definition of Done — `work-item` and `bug`

| # | Criterion | Check |
|---|-----------|-------|
| D1 | Every acceptance criterion checkbox in `item.md` is ticked | [auto] |
| D2 | Every ticked criterion cites its evidence in `artifacts/verify-report.md` | [skill] |
| D3 | All of the item's declared quality gates passed on the final state of the code, not on an earlier one | [skill] |
| D4 | No open blocking question remains on the item | [auto] |
| D5 | `journal.md` has an entry for every skill execution, and `history.md` chains without a gap to the current status | [auto] |
| D6 | Every decision that changed the design is in an ADR, and the ADR is cited from the plan or journal | [skill] |
| D7 | Documents the change invalidated have been updated, with a version bump and a change-log row | [skill] |
| D8 | Every commit on the branch references the item ID, so `git log --grep <ID>` reconstructs the item's code history | [auto] |
| D9 | The change is merged into the trunk, and the branch's work is not left only on the branch | [auto] |
| D10 | `verify` ran **after** the last code change. A verification older than the code it verifies does not count | [auto] |
| D11 | The review record exists at `artifacts/review.md` and states what was examined, not only the verdict | [skill] |

### D3 and D10 are the two that get skipped

Both fail the same way: something is re-touched after the check, and the check is not re-run
because "it was only a small fix". D10 is machine-checkable — compare the verify report's
timestamp against the last commit on the branch — and `review-close` MUST perform that
comparison rather than assume. When it fails, the item goes back to `verifying`; it does not go
to `done` with a note.

---

## 4. Definition of Done — `epic`

| # | Criterion | Check |
|---|-----------|-------|
| DE1 | Every child item is `done` | [auto] |
| DE2 | Every child item's `outcome` is recorded; dropped items say why in their `## Notes` | [auto] |
| DE3 | The epic's `## Success measures` are each addressed — met, or explicitly not met with the reason | [skill] |
| DE4 | `docs/product/` reflects what was actually built, not what was proposed | [skill] |
| DE5 | Open questions across all child items are closed, or re-filed against a follow-up item | [auto] |

DE3 is the criterion that stops a pipeline from mistaking "all the tickets are closed" for
"the goal was achieved". If a success measure was not met, closing the epic is still allowed —
saying so is what is mandatory.

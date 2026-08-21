# History — WI-0001

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-21T02:03:44Z | — | draft | intake | — | created from idea intake for EP-001 |
| 2026-08-21T02:15:14Z | draft | awaiting-answer | refine | draft | Q-001, Q-002 blocking to human: person identity and duplicate handling; first-run and damaged-store behaviour |
| 2026-08-21T02:30:58Z | awaiting-answer | draft | answer-questions | — | Q-001, Q-002 answered by the stakeholder and propagated into AC3-AC6, Notes and ADR-0002 |
| 2026-08-21T02:41:57Z | draft | ready | refine | — | Definition of Ready met on all ten criteria; AC1/AC2 rewritten, AC7/AC8 added, R10 gaps recorded; no override |
| 2026-08-21T02:45:40Z | ready | planned | plan | — | plan.md written; ADR-0006 settles the CLI surface and the name rule; architecture overview v1 created; commands.test set |
| 2026-08-21T02:46:01Z | planned | in-progress | implement | — | branch wi/WI-0001 created from main |
| 2026-08-21T02:48:40Z | in-progress | verifying | implement | — | 18 tests green on wi/WI-0001; impl-report.md written; lint gate skipped per ADR-0001 |
| 2026-08-21T03:02:03Z | verifying | in-review | verify | — | AC1-AC8 all verified independently with commands and output; advisory test-sensitivity gate failed for AC1/AC2 ordering, recorded for review |
| 2026-08-21T03:09:21Z | in-review | in-progress | review-close | — | rejected: match_key() is dead and AC3's rule is duplicated inline (deviates from plan step 4); AC1/AC2 ordering tests cannot distinguish insertion from alphabetical order |
| 2026-08-21T03:12:14Z | in-progress | verifying | implement | — | review findings 1 and 2 fixed: add() compares through match_key, ordering tests re-datad to Alice/Zoe/Carol; both confirmed by mutation; 19 tests green |
| 2026-08-21T03:19:55Z | verifying | in-review | verify | — | AC1-AC8 all re-derived and independently confirmed on f994258; both review findings closed by mutation; advisory sensitivity gate now passes for all eight |
| 2026-08-21T03:25:51Z | in-review | in-progress | review-close | — | rejected: AC8 violated - a store whose people list holds a non-string passes load() and produces an AttributeError traceback (exit 1); the read path prints it as a member and exits 0, missing ADR-0002 decision 6; add() re-validates stored names so a bad stored name blames the name being typed; overview.md's no-traceback claim is false (D12) |
| 2026-08-21T03:31:27Z | in-progress | verifying | implement | — | review findings F1, F2 and F3 fixed: store.load rejects a non-string roster entry, match_key compares without validating, cli.main has an Exception backstop, overview.md v2 and errors.py corrected; 23 tests green, four new tests confirmed sensitive |
| 2026-08-21T03:34:36Z | verifying | in-review | verify | — | AC1-AC8 all re-derived on a273c4e; AC8 re-ticked on a 28-case sweep that includes the store class which produced the traceback; review findings F1-F3 confirmed fixed by their own reproductions; ten mutations red |
| 2026-08-21T03:44:12Z | in-review | done | review-close | — | Definition of Done applied D1-D12: eleven pass, D6 passes with a recorded caveat (F8), none fails; trial merge green with 23 tests on the merge result; F5-F8 accepted and written into item.md |

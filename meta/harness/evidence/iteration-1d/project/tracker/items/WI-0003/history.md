# History — WI-0003

| when | from | to | actor | resume-to | reason |
|------|------|----|-------|-----------|--------|
| 2026-08-22T01:34:58Z | — | draft | intake | — | created from idea intake for EP-001 |
| 2026-08-22T02:43:50Z | draft | awaiting-answer | refine | draft | Q-001 and Q-002 blocking: the bank CSV sample and the rule that turns a row into a shared expense, both superseding EP-001/Q-002 |
| 2026-08-22T02:54:28Z | awaiting-answer | draft | answer-questions | — | Q-002 answered by the stakeholder (payer, sharers and date range given at import time; recorded as ADR-0007 and propagated into AC1); Q-001 deferred a second time, so the item returns to draft still unrefined |
| 2026-08-22T03:30:35Z | draft | awaiting-answer | refine | draft | Q-003 blocking: after two deferrals of the CSV sample, refine asked the choice underneath it — sample now, a fixed format converted to, or the column mapping as run-time options; no criterion rewritten because two of the three change the command's arguments |
| 2026-08-22T03:37:30Z | awaiting-answer | draft | answer-questions | — | Q-003 answered by the stakeholder: option A, the importer is written to their own export and takes no column-mapping options (ADR-0010); AC1 rewritten and AC3-AC5 narrowed to wait on the sample alone, which still has not arrived |
| 2026-08-22T03:40:17Z | draft | blocked | refine | draft | DoR fails R4 and R10 on one input the workspace has never held: a sample of the stakeholder's bank CSV. All three questions on this item are answered and Q-003 settled that the shape comes from their file, so no question remains to ask and no skill may guess it |

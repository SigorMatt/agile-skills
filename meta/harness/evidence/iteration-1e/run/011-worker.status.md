# Harness status — turn 11

The stakeholder's answer to `WI-0004/Q-001` was waiting on disk when this turn started, so the
turn was spent taking WI-0004 from a suspended draft to a planned item — three skills, one item,
no questions filed.

- **Consumed the answer first**, before running `next`, as amendment B requires. The stakeholder
  chose **option A**: deleting a person who is named in a recorded expense is refused, saying what
  stands in the way, rather than cascading or leaving the data inconsistent. `answer-questions`
  propagated it into `artifacts/refinement-qa.md` (which moved `agenda` → `recorded`, its two
  conditional criteria resolved and one added) and into `item.md`, then returned the item to its
  recorded `resume-to` of `draft`.
- **`refine` then finished the job its first execution could not**, and asked the stakeholder
  nothing — every other gap on the item had already been routed, and the audit of that is the
  gap-routing table in the Q&A. The four "a documented command" criteria became AC1–AC8, each
  naming a command and the observation that settles it. Definition of Ready passes on all ten
  criteria and was **not** overridden; R4 and R10 were the two that had been failing.
- **`plan` designed it**: eleven steps over `expenses/store.py`, `expenses/cli.py`, the two test
  modules and `README.md`, with no new module and no change to the stored format. Two ADRs record
  what outlives the item — **ADR-0006** fixes how a single expense is addressed (its position in
  the listing, which `expense list` now prints) and what that costs; **ADR-0007** names the
  people-and-expenses invariant, puts it at the two write points in `store.py`, and states where
  it stops, which is the fact WI-0003's importer will need. `docs/architecture/overview.md` went
  to v4.
- **Nothing refused to pass.** Every gate passed; the three that failed on a first attempt were
  mechanical and fixed in place (see notes).

Skills run, in order: `answer-questions`, `refine`, `plan`. `next` ran twice between them and
dispatched both times without applying any criterion outside `pipeline.yaml`.

Stopping because the three-skill turn budget is spent. Nothing is blocked by this turn's work:
WI-0004 is `planned` and `implement` owns it next, and the workspace validates clean.

```json
{
  "stop_reason": "turn-budget-exhausted",
  "skills_run": ["answer-questions", "refine", "plan"],
  "open_human_questions": [],
  "items_touched": ["WI-0004"],
  "last_action": "plan wrote artifacts/plan.md, ADR-0006 and ADR-0007, bumped the architecture overview to v4, and moved WI-0004 ready -> planned",
  "notes": "Three toolkit frictions, all recoverable, all worth the owner's attention. (1) refine's and answer-questions' SKILL.md both say the transition writes the '**Status:**' bullet itself from the move it made, but scripts/transition rejects a journal body that omits it — the first answer-questions transition failed on 'missing the **Status:** bullet' and on '**Commands:**', which the procedure prose also never mentions. The instruction and the validator disagree; the validator is right and the prose should be fixed. (2) lint-claims does not accept a citation whose path is wrapped in backticks: '[src: `tracker/.../review.md`]' fails as claim.citation.unresolved with the same message an unresolvable path gets, which sends you looking for a missing file rather than a stray character. (3) Nothing in the toolkit's fault, but worth recording: an item.md splice against a section anchor that appeared earlier in the file than the section being replaced silently duplicated three '## Notes' subsections. validate-workspace passed on the duplicated file — duplicate headings are not something it checks. Caught by re-reading the whole item, which is the only reason it did not ship. Substantively: the answer narrowed scope rather than widening it (the stakeholder was offered a --and-their-expenses cascade flag and declined it), so no new work item was filed. WI-0003 remains blocked on the same deferred CSV sample from 2026-08-26; BUG-0001 and BUG-0002 are both ready and unstarted."
}
```

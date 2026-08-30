# Review — EP-001

**This is the first half of the ending, not the ending.** `review-close` was dispatched on the
epic because `engagement-state EP-001` reported `at-rest`; it filed the sign-off question `Q-006`
and suspended the epic. The Definition of Done for the epic is applied, criterion by criterion,
by the execution that records the ending once the stakeholder has replied — applying it here
would be deciding DE7 before asking. What is recorded below is what this execution actually
examined, and what it found and repaired.

## What I examined

**That the engagement is over, and that it is over for a second time.**

- `scripts/engagement-state EP-001` → `at-rest`, *"every child has stopped, no question is open,
  no request is open; rest reached at 2026-08-30T00:52:41Z"*. Not read off the board.
- `scripts/check-epic-signoff EP-001` → exit 1 before filing: *"`Q-004.md` was filed at
  2026-08-29T23:43:45Z, before the engagement reached rest at 2026-08-30T00:52:41Z; the
  stakeholder was asked about something other than what they are being asked to accept"*. That is
  the correct verdict: `Q-004` asked them to accept a two-item engagement and they answered
  *"not quite as it stands"*, which is what created `WI-0003`. A fresh acknowledgment is due per
  `spec/question.md` §2 — exactly one sign-off per rest.
- The three children, by ID: `WI-0001`, `WI-0002` and `WI-0003`, all `done` with
  `outcome: delivered`. All three are named in `Q-006`.
- `EP-001/Q-001`, `kind: elicitation`, `answered-by: human` — DE8's open question was asked at
  intake, where it was worth something, and not manufactured here at the ending.

**The claims audit, DE6, run over a scope that could find something.**
`scripts/lint-claims --context epic --changed-since main` — at an ending there is no diff, so the
scope the gate reported for itself was *"absolute claims: every document under `docs`; citations:
every markdown file in the workspace"*. It found **7 errors**. Each was read against the thing it
cites, not against the sentence:

| # | where | claim | read against | verdict |
|---|-------|-------|--------------|---------|
| 1 | ADR-0007 `## Context`, *"Two sentences of theirs…"* | 'no exemptions' | `WI-0002/Q-001` and `EP-001/Q-004`, both opened and read | true, unsourced → **repaired** (provenance) |
| 2 | ADR-0007 `## Context`, *"So ADR-0005 is superseded rather than corrected…"* | 'Every other decision ADR-0005 took is carried forward' | ADR-0005 decisions 1–6 against ADR-0007 decisions 1, 2, 4, 5, 6, 7 | true, unsourced → **repaired** (provenance) |
| 3 | ADR-0007 `## Consequences`, reversibility | *"Nothing has been built against it yet"* | `mdtab.py` — `has_break_tag` at line 263, consumed by `compose_row` at line 303 — and `WI-0003`, closed `delivered` | **false**, and made false by this epic's own delivered work → **repaired** (erratum) |
| 4 | ADR-0008 `## Options considered`, option A for Q-001 | 'every spelling … and only those' | `WI-0003/Q-001`, whose options it reproduces | true, unsourced → **repaired** (provenance) |
| 5 | ADR-0005 header, `**Superseded by:**` bullet | *"No content cell is exempt"* | ADR-0005 line 116, which is where that decision is stated | true, unsourced → **not repairable**, see below |
| 6 | ADR-0005 `## Corrections`, closing note | *"not a word is edited and nothing has been removed"* | `git show 8c58ac1:…ADR-0005…` diffed against the file's corrections rows today → identical | true, unsourced → **not repairable** |
| 7 | ADR-0005 `## Corrections`, closing note | `adr.correction.superseded` *"tests the state"* | `scripts/validate-workspace` line 1230, where the rule is raised | true, unsourced → **not repairable** |

Finding 3 is the one that mattered: a current ADR asserting in the present tense that nothing had
been built against it, three commits after it was built. It is exactly the DE6 shape — a claim no
single item's diff touched, caught only because the ending's scope is the whole document set.

**The repairs, made under `spec/doc-header.md` §4b.**

- `ADR-0007` → v5, `## Corrections` gains three entries (two `provenance`, one `erratum`); the
  erratum quotes the removed clause verbatim and cites `mdtab.py` and `WI-0003`. Three change-log
  rows, one per correction — `validate-workspace`'s `adr.correction.changelog` refused a single
  row covering three, correctly.
- `ADR-0008` → v2, its first `## Corrections` section with one `provenance` entry.
- No decision was changed and nothing was superseded. No code would have to change to satisfy any
  of the new text, which is §4b's line between a repair and a rewrite.

**The record, read rather than skimmed.** `EP-001`'s `item.md`, `history.md` and `journal.md`;
`WI-0003`'s `item.md` and `artifacts/review.md`; `EP-001/Q-004` and `Q-005` in full, including
their `## Cross-answer check` and `## Consequences`; `docs/product/vision.md` `## What is not yet
decided`. `python3 -m unittest discover -s tests -t .` → exit 0, 37 tests, on `main` at `0500edf`.

## Findings

1. **`claims-are-sourced` cannot be made to pass at this ending by any legal move, and this is a
   defect in the toolkit rather than in the record.** The three surviving errors are all in
   `ADR-0005`, which is `status: superseded`. `spec/doc-header.md` §4b says in terms: *"An ADR at
   `status: superseded` is not corrected."* Every repair §4b sanctions must be recorded as an entry
   in that ADR's `## Corrections` section — and `ADR-0005`'s was explicitly **closed** at
   supersession, with a paragraph saying no further entry may be added, itself a documented
   workaround for `adr.correction.superseded`. So the one repair route is shut by the same rule
   twice over, while `lint-claims --context epic` has no exemption for a superseded ADR and will
   flag those three lines for ever.

   All three sentences were checked and are **true** (rows 5–7 above), so this is not a wrong claim
   propagating; it is F-067's shape with the escape hatch removed. Two of the three were written
   *at* supersession, as supersession bookkeeping, rather than being part of what the ADR believed
   at the time — which is the case §4b's prohibition does not seem to have had in mind.

   Recorded here, not worked around. The execution that records the ending will have to decide
   between `transition --force` (which stamps `[gates forced]` into the history reason, visibly
   and for ever) and leaving the engagement unable to end. It should force, and say why.

2. **`WI-0003`'s three non-blocking findings survive** in `tracker/items/WI-0003/artifacts/
   review.md` and are not restated here: three of its criteria quote expected tables a filter with
   no exemption would also produce (discriminating cases were written for all three); `widths_of`
   in the test module deliberately duplicates `column_widths`' rule; the suite's wall time roughly
   doubled as fixtures grew.

3. **One gap has never been decided and is now in front of the stakeholder.** An exempt cell that
   also contains an escaped pipe (`\|`) is unconstrained. It is `WI-0001`'s open design question,
   still open, recorded in `docs/product/vision.md` `## What is not yet decided` and in `WI-0003`'s
   `## Notes`. `Q-006` names it as one of the three things they should weigh, so it is a choice
   they are making rather than a hole they will find.

## Accepted gaps

| gap | why it is accepted here | where it survives |
|-----|------------------------|-------------------|
| `ADR-0005`'s three unsourced-but-true claims | no legal repair exists; §4b forbids correcting a superseded ADR | finding 1 above, and the `[gates forced]` reason the ending will carry |
| the escaped-pipe case | never decided for any cell, and not this epic's to decide | vision `## What is not yet decided`; `WI-0001`; `Q-006` option B |

## Verdict

**Not yet — the stakeholder has been asked.** `Q-006` is filed on this epic, `kind: sign-off`,
`blocking: true`, addressed to the human, naming `WI-0001`, `WI-0002` and `WI-0003` each with its
outcome, offering accept / accept-with-follow-ups / do-not-accept, and putting the three
`WI-0003`-specific caveats in front of them before the question. `EP-001` moves `open →
awaiting-answer` with `resume-to: open`, and this execution stops. The ending itself — which of
E1 to E4, and the epic's outcome — is theirs to select and is recorded by the execution that
consumes their reply.

---

# Review — EP-001, the second half: the ending

Written by the `review-close` execution that consumed the stakeholder's reply to `Q-006`. The
first half above is left exactly as it was written; it is the record of the execution that asked.
Below is the Definition of Done for the epic, applied criterion by criterion, and the ending.

## What I examined

**That the engagement is still over, and that the reply is really there.**

- `scripts/engagement-state EP-001` → `at-rest`, *"every child has stopped, no question is open,
  no request is open; rest reached at 2026-08-30T00:52:41Z"*. Run, not inferred from the board.
- `scripts/check-epic-signoff EP-001 --resolving 'EP-001:open->done'` → **PASS**:
  *"`tracker/items/EP-001/questions/Q-006.md` carries the stakeholder's reply, names all 3 child
  item(s), and was filed after the engagement reached rest at 2026-08-30T00:52:41Z; DE8 satisfied
  by `tracker/items/EP-001/questions/Q-001.md`"*.
- `EP-001/Q-006` in full, including the `## Cross-answer check` and `## Consequences`
  `answer-questions` wrote when it consumed the reply. The reply chooses option A by name and
  addresses all three caveats the question put in front of them.

**The eight success measures, run rather than read** (DE3). On `main`, with `python3 mdtab.py`,
over a fixture holding prose, a marked table, a fenced block of pipes and a malformed table:

| # | measure | evidence |
|---|---------|----------|
| 1 | every row of a tidied table the same width, each column in the same range | all five lines of the output table measured 28 characters; columns start at the same offsets |
| 2 | a file with no table comes back byte-identical | `cmp p.md p.out` → identical |
| 3 | a diff of input against output changes lines only inside tables | `diff` reported five changed lines, all five inside the table; prose, heading, fence and malformed block unchanged |
| 4 | running it twice is the same as running it once | `cmp out1.md out2.md` → identical |
| 5 | markers place the text, with the multiline exception | discriminating case: in a centre-marked column `mid` came back centred and `p<br>q` flush left; in a right-marked column `r1` came back right-aligned and `s<br>t` flush left; both exempt cells still padded to the column's full width |
| 6 | a fenced block of pipes comes back byte-identical | the fenced `\| not \| a table \|` block is byte-for-byte in the output |
| 7 | a malformed table comes back byte-identical | the two-then-three-cell block is byte-for-byte in the output |
| 8 | no line it writes ends in a space or a tab | `grep -nP '[ \t]+$'` over the output → no match |

`python3 -m unittest discover -s tests -t .` → exit 0, 37 tests, on `main`.

**The claims audit, DE6, over the whole document set** (step 9a). `scripts/lint-claims --context
epic --changed-since main` → 3 errors, all three in `ADR-0005`, and all three the ones the first
half found and could not repair. They were re-read here against what they cite rather than
against the first half's table:

| where | claim | opened | verdict |
|-------|-------|--------|---------|
| `ADR-0005:13` | the `**Superseded by:**` bullet quoting decision 3, *"No content cell is exempt"* | `ADR-0005` line 116, where decision 3 is stated | the quotation is exact — **true**, unsourced |
| `ADR-0005:162` | *"`spec/doc-header.md` §4b says a superseded ADR is not repaired"* | `spec/doc-header.md` §4b, whose last rule reads *"An ADR at `status: superseded` is **not** corrected."* | **true**, unsourced |
| `ADR-0005:168` | *"`adr.correction.superseded` tests the state"* | `scripts/validate-workspace` line 1229: `if doc.fields.get("status") == "superseded" or body_status == "superseded":` | **true** — it branches on the status field, not on any act — unsourced |

The two documents this ending's own answer propagation touched, `docs/product/vision.md` v8 and
`ADR-0008` v3, introduced no new finding: the gate's error count is unchanged at 3.

**The record** (`record-is-reconstructible`). `EP-001`'s `item.md`, `history.md` and `journal.md`
in full; all six of its questions; the three children's `item.md` and `artifacts/review.md`;
`docs/product/vision.md` v8 end to end.

## Definition of Done — epic (`spec/dor-dod.md` §4)

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | every child terminal, and every undelivered child named | **pass** | `WI-0001`, `WI-0002`, `WI-0003` all `done`; all three named by ID in `Q-006`'s `## Question`, each marked delivered with one line of why. There is no undelivered child to name |
| DE2 | every child's `outcome` recorded | **pass** | all three carry `outcome: delivered` in `item.md`; nothing was dropped, so no `## Notes` reason is owed |
| DE3 | every success measure addressed | **pass** | all eight met, each with its own evidence in the table above, run at this ending rather than quoted from a child's verify report |
| DE4 | `docs/product/` reflects what was built | **pass** | `docs/product/vision.md` v8 carries all six rounds of the stakeholder's own words, including the acceptance, and its `## What is not yet decided` lists the one thing still open — the escaped pipe — with their decision not to hold the engagement for it |
| DE5 | open questions closed or re-filed | **pass** | no question anywhere in the engagement has `status: open`; all fourteen are `answered`, none `deferred` |
| DE6 | claims about delivered behaviour checked during this epic; every citation resolves | **pass, with a recorded gap** | the audit above; the three surviving `claim.unsourced` errors were each read against their source and are true. Citations all resolve — `lint-claims` reports no `claim.unresolved` |
| DE7 | the stakeholder was asked after rest, and answered | **pass** | `check-epic-signoff` PASS, quoted above. Asked twice, in fact: `Q-004` at the first rest, refused; `Q-006` at this one, accepted |
| DE8 | an open question that was not about our agenda was asked and answered | **pass** | `EP-001/Q-001`, `kind: elicitation`, filed by `intake` and answered by the human. Asked at the start, where it changed the work: its answer is what the eight success measures were written from |

## Findings

1. **`claims-are-sourced` still cannot pass, and this ending forces it.** The three errors are
   the ones the first half analysed: all in `ADR-0005`, which is `status: superseded`, whose
   `## Corrections` section was closed at supersession. `spec/doc-header.md` §4b's repair route —
   add the citation, record a `provenance` row — is shut twice over for that document, and
   `lint-claims` has no exemption for a superseded ADR. I re-derived this rather than taking the
   first half's word for it, and I reach the same place: there is no legal move that clears the
   gate. The alternative to forcing is an engagement that can never end, which is a worse record
   than one that says plainly it was forced. `transition --force` stamps `[gates forced]` into the
   history reason permanently, which is the right cost.

   **This is a toolkit defect, not a defect in this project's record**, and it is the second
   iteration of F-067's shape: the first was a true claim in a *standing* ADR with no repair
   route, which §4b fixed; this is a true claim in a *superseded* one, where §4b's own last rule
   is the thing blocking the repair. The two sentences at `ADR-0005:162` and `:168` are worse than
   incidental — they are *bookkeeping the pipeline wrote at supersession*, not part of what the
   ADR believed when it was current, so the rationale §4b gives for the prohibition ("it records
   what was believed then") does not describe them at all.

2. **No new finding against the delivered work.** The diff-level review of each change was done
   at each child's close and those reviews stand; this execution reviewed the engagement, not the
   code, and re-ran the code only to check the epic's own success measures. The three
   non-blocking findings on `WI-0003` survive in its `review.md` and are not restated here.

3. **The escaped-pipe case is closed as a question and left open as a design gap, by the
   stakeholder.** They were shown it as `Q-006`'s note 3 with an explicit offer to record
   follow-up work (option B) and declined: *"I have never once written an escaped pipe in the same
   cell as a line break. If that last one ever bites me I will come back to you with it as a new
   job rather than call this one unfinished."* So no item is filed. It stays in
   `docs/product/vision.md` `## What is not yet decided`, now with that decision recorded beside
   it.

## Accepted gaps

| gap | why it is accepted | where it survives |
|-----|-------------------|-------------------|
| `ADR-0005`'s three unsourced-but-true claims | no legal repair exists; §4b forbids correcting a superseded ADR and that ADR's corrections section is closed. All three verified true against their sources | finding 1 above; the `[gates forced]` reason on this epic's closing history row; this table |
| the escaped-pipe case, in any cell | never decided for any cell, and the stakeholder declined to schedule it | `docs/product/vision.md` `## What is not yet decided`; `WI-0001`; `WI-0003`'s `## Notes`; `Q-006` note 3 |
| the exemption fires on a cell that only *mentions* a break tag | the rule is textual by design, so that a user can predict it without reading the code; put to the stakeholder as `Q-006` note 1 and accepted | `ADR-0008` decision 3 and its `## Consequences`; `Q-006` |

## Verdict

**Accepted — E1, delivered.** Every child is `done` with `outcome: delivered`, every one of the
epic's eight success measures is met with evidence gathered at this ending, and the stakeholder
was asked after rest and answered: *"Yes — I accept it as it stands, your option A."* `EP-001`
moves `open → done` with `outcome: delivered`, with `claims-are-sourced` forced for the reason in
finding 1 and for no other.

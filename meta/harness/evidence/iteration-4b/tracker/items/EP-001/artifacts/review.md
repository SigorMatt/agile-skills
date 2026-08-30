# Review — EP-001

This is the review of an **engagement's ending**, not of a change. EP-001 has no branch, no
diff and no implementation report; steps 1–9 of `review-close` are about an item at `in-review`
and none of them applies. What is reviewed here is the record of the whole engagement, the
epic's Definition of Done (`spec/dor-dod.md` §4), and the acceptance the ending would rest on.

It does **not** end the engagement. One finding below is material enough to go back to the
stakeholder, and `EP-001/Q-005` is where it went.

## What I examined

- **`scripts/engagement-state EP-001`** → `at-rest`, *"every child has stopped, no question is
  open, no request is open"*, rest reached `2026-08-30T05:43:23Z`. Run rather than inferred from
  the board, per step 10.
- **The epic's own record.** `item.md` (all six `## Success measures`, `## Scope`, `## Out of
  scope`), `history.md` (five rows, chaining without a gap, last row matching `item.md`'s
  status), `journal.md` in full — every entry, including the appended correction of
  2026-08-30T05:48 that downgraded a `tests-pass-on-the-merge-result` line from a claim the suite
  had not run to what `run-gate` actually did.
- **Every child item**, by `item.md` and `history.md`: `WI-0001` (9 criteria), `WI-0002` (13),
  `WI-0003` (6), `WI-0004` (12), `BUG-0001` (6) — 46 criteria, every one ticked, every child at
  `done` with `outcome: delivered`.
- **All ten questions in the engagement.** `EP-001/Q-001` (`kind: elicitation`), `Q-002`,
  `Q-003`, `Q-004` (`kind: sign-off`); `WI-0002/Q-001`, `Q-002`; `WI-0003/Q-001`, `Q-002`;
  `WI-0004/Q-001`, `Q-002`. All `answered`; nine `answered-by: human`, each carrying a
  `## Cross-answer check` and a `## Consequences` naming files.
- **`docs/` in full** — `product/vision.md` (v5), `architecture/overview.md` (v9),
  `process/using-recall.md`, and all ten ADRs.
- **The code**, read rather than cited: `recall/store.py`, `recall/cli.py`, `recall/deck.py`,
  `bin/recall`, `tests/support.py`.

### The claims audit, from the citations (DE6)

Each claim below was decided by opening the thing it cites, never by reading a neighbouring
document that repeats it.

| claim, and where | cites | opened | verdict |
|---|---|---|---|
| "All of its state is one JSON file under the person's home directory" (`overview.md`) | ADR-0004 | `recall/store.py` `deck_path()` — `pathlib.Path.home() / ".local" / "share" / "recall" / "deck.json"` | true |
| "no flag, no environment variable of the tool's own, no config file" (`overview.md` "What is deliberately absent"; ADR-0004 §65; `using-recall.md` "Where the deck is kept") | ADR-0004 | `recall/store.py` `deck_path()`, and `recall/cli.py` — the four `store.deck_path()` calls take no argument; `grep` for `environ`/`getenv`/`--deck` across `recall/` and `bin/` returns nothing | true, and stated identically in three documents |
| "writes go through a temporary file and `os.replace`, so an interrupted write leaves the previous deck intact" (`overview.md`; `using-recall.md`) | ADR-0004 §4 | `recall/store.py` `save()` — `tempfile.mkstemp(dir=path.parent)`, `fsync`, `os.replace`, and an `unlink` of the temporary on any failure | true |
| "a deck that cannot be parsed is reported and left alone rather than replaced with an empty one" (`overview.md`) | ADR-0004 §5; WI-0001 AC8 | `recall/store.py` `load()` — every malformed branch raises `DeckUnreadable`; `load` writes on no path | true |
| "a load has **three** outcomes — absent, unreadable, inaccessible — and only `FileNotFoundError` produces absent" (`overview.md`) | ADR-0010; `recall/store.py` | `recall/store.py` `load()` — `except FileNotFoundError` → empty `Deck`; `except OSError` → `DeckInaccessible`; `NotADirectoryError` deliberately no longer caught as absent | true |
| "The ladder's four numbers exist there once and nowhere else" (`overview.md`) | ADR-0008 | `recall/deck.py` — `LADDER = (1, 3, 7, 30)`, one definition; `store.py` imports it rather than restating it | true |
| "`review` saves the deck after every graded card rather than once at the end" (`overview.md`) | WI-0002 plan | `recall/cli.py` `cmd_review` | true |
| "`cli.py` … is the only layer that knows a terminal exists" (`store.py`, `cli.py`, `overview.md`) | overview | `recall/store.py` and `recall/deck.py` — neither contains a `print` or reads stdin | true |
| "Its location is fixed: there is no flag, no environment variable and no configuration file for pointing `recall` at a different deck" (`using-recall.md` line 183) | ADR-0004 | as above | true |

`scripts/lint-claims --context epic --changed-since main` → exit 0, and it printed its scope,
which is the part worth quoting: *"an ending has no diff of its own, so the scope is the whole
document set rather than anything `--changed-since` could name; absolute claims: every document
under `docs`; citations: every markdown file in the workspace"*. That is a window that could have
found something (F-066).

## Definition of Done — epic (`spec/dor-dod.md` §4)

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | Every child terminal; every child that did not deliver named in the termination question and in the outcome | **pass** | All five children at `done`. `Q-004`'s `## Question` names `WI-0001`, `WI-0002`, `WI-0003`, `WI-0004` and `BUG-0001` by ID in a table, each with one line of why. `check-epic-signoff` confirms mechanically: *"names all 5 child item(s)"*. No child is undelivered, so nothing is owed to the second half. |
| DE2 | Every child's `outcome` recorded; dropped items say why | **pass** | `outcome: delivered` on all five; none dropped. `validate-workspace` exit 0 decides this one. |
| DE3 | Every `## Success measures` entry addressed — met, or explicitly not met with the reason | **pass**, with one measure explicitly not measurable | Walked below. |
| DE4 | `docs/product/` reflects what was built, not what was proposed | **pass** | `vision.md` v5, read whole. Every behavioural sentence matches the code as audited above: the ladder, the uncapped sitting, the printed next-due line, one deck, no editing, deletion delivered. `## What is still open` now says "Nothing" and no longer carries the deletion-naming entry that `WI-0004/Q-001` had settled. |
| DE5 | Open questions across all children closed, or re-filed against a follow-up | **pass** at the moment of the walk — then deliberately broken by this execution | All ten questions were `answered` when this review began (`validate-workspace` exit 0). `Q-005`, filed by this execution, is open by design: DE5 is a criterion for *recording an ending*, and this execution records none. |
| DE6 | Every claim in `docs/` about behaviour this epic delivered checked against the code during this epic; every citation resolves | **pass** | The nine-row audit above, each row decided from the cited source. `lint-claims --context epic` exit 0 over the whole document set. Note the scope: DE6 is about `docs/`, and the finding below is in a **question artifact**, which is why DE6 passes and the finding still stands. |
| DE7 | The stakeholder was asked whether they accept the engagement as it stands, after rest, and answered | **pass on the letter; escalated on the substance** | `check-epic-signoff` exit 0: `Q-004` is `kind: sign-off`, `addressed-to: human`, `status: answered`, filed after rest, naming every child. They answered *"A — accept as complete. This is what I asked for."* What the gate cannot check is whether what they were shown was true, and one sentence of it was not — Finding 1. `Q-005` puts the correction to them. |
| DE8 | The stakeholder was asked at least one open question that was not about the team's agenda, and answered it | **pass** | `EP-001/Q-001`, `kind: elicitation`, filed by `intake` at `2026-08-30T01:31:33Z` — at the beginning, where an answer is cheapest to act on, rather than as a formality at the ending. It was answered at length and it changed the work: `WI-0004` exists because of it. |

### DE3 — the six success measures, one by one

1. **"Adding a card, exiting the tool, and starting it again shows that card still present."**
   **Met.** `WI-0001` AC1–AC9, all ticked on evidence; `recall add` writes through
   `store.save`, `recall list` reads through `store.load`, and the deck file is under `$HOME`.
2. **"A review session presents only cards whose next-review date is today or earlier … absent
   from a second review run on the same day."** **Met.** `WI-0002` AC1–AC13, and `WI-0003`'s
   arithmetic is what makes the second half true.
3. **"the gap to its next review follows the ladder `1, 3, 7, 30` days … a wrong answer sends it
   back to one day."** **Met.** `recall/deck.py` `LADDER = (1, 3, 7, 30)`, one constant;
   `WI-0003` AC1–AC6 ticked on observed deck contents across a run of sittings.
4. **"Someone with this repository, a terminal, and no other context can follow the project's own
   documentation to add a card and to run a day's review, without reading the source."**
   **Met, with the qualification in Finding 1.** `docs/process/using-recall.md` covers all four
   subcommands from an empty deck, and its "Where the deck is kept" section is correct. The
   sign-off's summary of that document is what was wrong, not the document.
5. **"A day's review sitting does not drag on."** **Explicitly not met as a measurable thing, by
   the stakeholder's decision.** Asked directly at `WI-0002/Q-001` whether a sitting should cap
   how many cards it presents, they refused a cap and reconciled it themselves — *"If it's a big
   pile after a week away I'll just stop partway, that's fine by me."* Nothing in the tool bounds
   or measures a sitting's length. The epic's own bullet now records that, and `Q-004`'s
   `## Context` told them so in terms before they answered. Recording it as unmet-by-choice, not
   as met.
6. **"Progress is not lost."** **Met**, and it is the measure with the most behind it: an atomic
   write through a temporary file and `os.replace`; a deck that cannot be parsed refused rather
   than replaced; `BUG-0001` filed against ourselves and fixed so that a filesystem refusal is a
   sentence rather than a traceback; and a sitting that saves after every graded card so an
   abandoned one keeps what was already answered.

## Findings

### Finding 1 — the sign-off told the stakeholder the deck can be relocated, and it cannot. **Escalated as `Q-005`; blocks the ending.**

`EP-001/Q-004`'s `## Context`, under **"What you can do with it today"**, says:

> Your deck lives in a single file under your home directory
> (`~/.local/share/recall/deck.json` unless you set `RECALL_DECK`), which survives the process
> ending and a reboot.

`RECALL_DECK` does not exist and never has. `recall/store.py`'s `deck_path()` derives the path
from `pathlib.Path.home()` and from nothing else, and its own docstring says *"No flag, no
environment variable of the tool's own, no config file"*. `recall/cli.py` calls
`store.deck_path()` in four places, each with no argument. Searching `recall/` and `bin/` for
`environ`, `getenv`, `RECALL` or `--deck` returns nothing. `ADR-0004` rejected relocation in its
options list, `docs/architecture/overview.md` lists "no environment variable of the tool's own"
under "What is deliberately absent", and `docs/process/using-recall.md` — the document the very
next sentence of the sign-off points them at — says *"Its location is fixed: there is no flag, no
environment variable and no configuration file for pointing `recall` at a different deck."*

**Why this is not filed as a bug and not fixed here.** No delivered behaviour is wrong. The code,
the ADRs and all three documents agree with each other and with the code; the single false
sentence is in a question artifact, which is why `lint-claims` — whose absolute-claim scope is
`docs/` — could not have caught it, and did not.

**Why it is not accepted as a gap either.** It is the one place in this engagement where a false
statement was made *to the stakeholder*, at the one gate that belongs to them, in the paragraph
that describes what they are accepting. It overstates the tool in the direction of their single
most emphatic requirement: someone who read that sentence, set `RECALL_DECK` and worked in the
deck it named would find `recall` reading a different file and would call that losing their
progress — *"the one thing that would make this a failure"* (`EP-001/Q-001`). Whether their
acceptance survives the correction is not a judgement this skill may make on their behalf; it is
the same class of move `ADR-0008` refuses. `review-close` may not ask a person directly, so it is
filed as `EP-001/Q-005`, blocking, addressed to `human`, and the epic is suspended.

**What was deliberately not done.** `Q-004` is not edited. `spec/question.md` §3 rule 6 keeps a
question and its answer as filed, and rewriting the text after they answered would destroy the
evidence of what they actually accepted. The correction lives in `Q-005`, which quotes the
sentence and cites `Q-004` by ID.

### Finding 2 — everything else in the sign-off's description checks out. **No action.**

Recorded because a finding of this shape is only trustworthy if the rest was checked with the
same suspicion. Each of `Q-004`'s remaining factual claims was read against the code: one command
with exactly four subcommands (`build_parser`); the `1, 3, 7, 30` ladder with a reset to one day
and a top rung that holds; a next-due line printed per answered card (`NEXT_REVIEW_LINE`); no
editing, so re-adding restarts a card at rung 0 due today (`cmd_add`); deletion by exact question
text with `"no card has the question …"` on a near miss (`cmd_delete`); only the last review's
grade stored and nothing about past sittings (`_card_to_entry`); the four ladder gaps fixed; and
the criteria counts in the child table — 9, 13, 6, 12, 6 — which match the items. All true.

## Accepted gaps

None. Finding 1 is escalated rather than accepted, and Finding 2 needs nothing.

Two things are recorded here as *known and deliberate* rather than as gaps, because both are the
stakeholder's own decisions and both are already written into the items and into
`docs/process/using-recall.md` `## What this version does not do yet`: success measure 5 has no
threshold and nothing measures it (`WI-0002/Q-001`), and two cards sharing a question side cannot
be told apart by `recall delete` (`WI-0004/Q-001`, `WI-0001` AC9).

## Verdict

**The engagement is not ended by this execution.** Every Definition of Done criterion is
satisfied on the record, and the tool matches what the documents say about it. But the acceptance
this ending would rest on was given against a description containing one false statement about
where the person's deck can live, and correcting that is theirs to weigh, not ours.

`EP-001/Q-005` is filed, blocking, addressed to `human`. `EP-001` moves `open →
awaiting-answer` with `resume-to: open`. If they confirm their acceptance stands, the next
`review-close` records ending **E1** — `open → done`, `outcome: delivered` — relying on `Q-004`
and `Q-005` together. If it does not, they have said what is missing and the pipeline runs again.

## The answer to `Q-005` — appended 2026-08-30T06:01:20Z by `answer-questions`

Everything above was written while `Q-005` was open and says so. It is left exactly as it was
written; a review that had predicted the answer would be worth less than one that recorded it
after the fact. This section records what came back.

The stakeholder chose **option A**:

> "A — it stands, close it. I never planned to move the deck, a fixed file under my home
> directory is exactly what I asked for. Appreciate the correction though."

- **Finding 1 is discharged, not withdrawn.** The false sentence was real, it was said to them at
  the gate that belongs to them, and it stays on the record in `Q-004` (unedited), in `Q-005`, and
  in this document. What the answer settles is the only thing that was ever escalated: whether the
  acceptance survives the correction. It does.
- **Option B was declined in terms.** They were offered a `draft` work item recording a want to
  relocate the deck and did not take it, so none was filed.
- **The ending this selects is E1** — `open → done`, `outcome: delivered` — resting on `Q-004` and
  `Q-005` together. `answer-questions` does not make that move: `EP-001` returns to `open`, its
  recorded `resume-to`, and the next `review-close` runs the epic's Definition of Done over both
  answers before recording the ending. DE5 and DE7 are the two criteria this answer changes: DE5's
  one open question is now `answered`, and DE7's acceptance now rests on a description that has
  been corrected.
- **The fixed location gained a second owner.** It was `plan`'s decision under WI-0001's
  out-of-scope list; `ADR-0004` v2 now records it as the stakeholder's too, with their words and
  the citation, and `docs/product/vision.md` v6 states it where a reader of the vision will meet
  it. That is the only lasting repair this episode produced, and it is aimed at the belief the
  false sentence could have created rather than at the sentence itself.

---

# Review — EP-001, second pass: the ending recorded

Everything above is the first pass, which examined the record, found one false statement in the
sign-off's own description and stopped. This pass runs after `EP-001/Q-005` came back and does
the one thing the first could not: record the ending. It is appended rather than merged into the
text above, so that a reader can see which conclusions were reached before the stakeholder
answered and which after.

## What I examined

- **`scripts/engagement-state EP-001`** → `at-rest`, *"every child has stopped, no question is
  open, no request is open"*, rest reached `2026-08-30T05:43:23Z` — unchanged from the first
  pass, and re-run rather than remembered.
- **`EP-001/Q-005`, answered**, and the five files its `## Consequences` names, opened one by one:
  the question itself, `tracker/items/EP-001/item.md`,
  `docs/architecture/adr/ADR-0004-the-deck-file.md` (now v2), `docs/product/vision.md` (now v6),
  and the first pass of this document.
- **`EP-001/Q-004`**, unedited, and its `## Cross-answer check` over all nine earlier human
  answers.
- **The epic's `history.md`** — now eight rows, chaining without a gap, the last matching
  `item.md` — and its `journal.md` including the `answer-questions` entry of
  2026-08-30T06:04:37Z that consumed `Q-005`.
- **The code, again, for the one claim this round added.** Not the documents that state it: the
  claim is that the deck's location cannot be changed, and it now appears in three places that
  did not carry it before.

### The claims audit for this round (DE6)

The first pass audited nine claims from their citations. This pass adds the sentences written
since, each decided by opening the code rather than a neighbouring document.

| claim, and where | opened | verdict |
|---|---|---|
| "That file's location is fixed … no flag, no environment variable and no configuration file for pointing `recall` elsewhere" (`EP-001/item.md`, success measure 6) | `recall/store.py:77-83` — `deck_path()` takes no argument and returns `pathlib.Path.home() / ".local" / "share" / "recall" / "deck.json"`, derived from the home directory and nothing else | true |
| "a future change that makes the path configurable is … reversing something the stakeholder has been asked about directly and settled" (`ADR-0004` v2 `## Consequences`) | `EP-001/Q-005` — the question puts the fixed location to them in terms and offers relocation as options B and C; the answer declines both | true |
| "That file is at one fixed place … and there is no flag, environment variable or configuration file for pointing the tool at a different one" (`vision.md` v6, "What it is for") | `recall/cli.py:146,164,195,266` — every call is `store.deck_path()` with no argument; `grep -rn "environ\|getenv\|--deck\|RECALL" recall/ bin/` returns one line, `store.py:80`, which is the docstring saying none of them exists | true |
| the stakeholder quotation *"a fixed file under my home directory is exactly what I asked for"*, carried by all three | `EP-001/Q-005` `## Answer`, verbatim | true |

`scripts/lint-claims --context epic --changed-since main` → exit 0, over the scope it printed:
*"an ending has no diff of its own, so the scope is the whole document set … absolute claims:
every document under `docs`; citations: every markdown file in the workspace"*. That is a window
that could have found something, and it now includes the three sentences added this round.

## Definition of Done — epic, second pass (`spec/dor-dod.md` §4)

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | Every child terminal; every undelivered child named in the termination question and the outcome | **pass** | All five children at `done`, unchanged since the first pass. `check-epic-signoff` exit 0: `Q-004` *"names all 5 child item(s)"*. No child failed to deliver, so the outcome owes the second half nothing. |
| DE2 | Every child's `outcome` recorded; dropped items say why | **pass** | `outcome: delivered` on `WI-0001`, `WI-0002`, `WI-0003`, `WI-0004`, `BUG-0001`; none dropped. `validate-workspace` exit 0. |
| DE3 | Every success measure addressed — met, or explicitly not met with the reason | **pass**, with measure 5 explicitly not met as a measurable thing | The first pass walked all six and nothing has changed for measures 1–5. Measure 6, *"Progress is not lost"*, gained a sentence this round and is re-checked in the claims audit above: the deck is one file under `$HOME` at a fixed path, written atomically, refused rather than overwritten when unparseable, and saved after every graded card. Measure 5 remains unmet-by-the-stakeholder's-decision (`WI-0002/Q-001`), recorded as such rather than ticked. |
| DE4 | `docs/product/` reflects what was built | **pass** | `vision.md` v6, re-read whole. Its one new sentence is audited above; `## What is still open` still says "Nothing", and the acceptance it quotes is now the reaffirmed one. |
| DE5 | Open questions closed, or re-filed against a follow-up | **pass** | Eleven questions in the engagement, all `status: answered`. `Q-005` — open by design when the first pass wrote itself — was consumed by `answer-questions` at 2026-08-30T06:04:37Z. `validate-workspace` exit 0 with no `question.awaiting.none-open`. |
| DE6 | Claims in `docs/` checked against the code during this epic; every citation resolves | **pass** | Nine rows in the first pass, four more above, each decided from what it cites. `lint-claims --context epic` exit 0 over the whole document set. |
| DE7 | The stakeholder was asked whether they accept, after rest, and answered | **pass, and this time on the substance as well as the letter** | `check-epic-signoff` exit 0. The first pass qualified this: the letter passed but what they were shown contained one false sentence. `Q-005` put the correction to them and they answered *"A — it stands, close it. I never planned to move the deck, a fixed file under my home directory is exactly what I asked for."* The acceptance now rests on a description that has been corrected in front of them. |
| DE8 | An open question that was not about the team's agenda was asked and answered | **pass** | `EP-001/Q-001`, `kind: elicitation`, filed by `intake` at the beginning. `check-epic-signoff` names it. It changed the work: `WI-0004` exists because of it. |

## Findings

### Finding 1 (first pass) — discharged.

The false `RECALL_DECK` sentence in `Q-004`'s description was put to the stakeholder as `Q-005`
and they confirmed their acceptance stands. It is discharged, not withdrawn: `Q-004` is unedited,
and the mistake remains legible in `Q-004`, in `Q-005`, and in the first pass above. What the
engagement did about it beyond asking is the only durable part — the fixed location is now stated
in the epic's own success measure, in `ADR-0004` v2 as the stakeholder's decision as well as
`plan`'s, and in `vision.md` v6 where a reader of the vision will meet it.

### Finding 3 — `lint-answers` can turn a compatible verdict into a declared conflict. **Filed as a toolkit note, not a defect in this workspace.**

Recorded because it cost this engagement a gate failure and because the next run will hit it.
`lint-answers`' `verdict_for` scopes a verdict to a bullet by reading forward to the next bullet,
so any closing prose after the last bullet is swallowed into it. The sentence the skill's own
examples end with — *"No verdict is `conflicts`, so no question is filed"* — therefore turns the
last bullet's verdict into `conflicts` and fails `answer.conflict.unescalated`.
`answer-questions` hit exactly that this turn and cleared it by moving the sentence above the
list. `Q-004` carries the same latent false positive and escapes only by accident: its
`Checked against:` list wraps onto four lines and `CHECKED_AGAINST_RE` reads one, so six of the
nine IDs it names are never verdict-checked at all. Both belong in the script; neither is a
defect in this record, and neither changes any verdict a reader would reach. It is recorded here
and in `EP-001/journal.md` rather than filed as a bug item, because the subject is the toolkit
this project is run *by*, not the tool this project delivers — filing it as a child of EP-001
would have put a work item nobody can act on in front of the stakeholder at sign-off.

## Accepted gaps

None new. The two things the first pass recorded as known and deliberate stand, both being the
stakeholder's own decisions and both already written into the items and into
`docs/process/using-recall.md` `## What this version does not do yet`: success measure 5 has no
threshold and nothing measures it (`WI-0002/Q-001`), and two cards sharing a question side cannot
be told apart by `recall delete` (`WI-0004/Q-001`, `WI-0001` AC9).

## Verdict

**Ending E1 — delivered.** `EP-001` moves `open → done` with `outcome: delivered`, resting on
`Q-004` and `Q-005` together: an acceptance, and its reaffirmation after the one false statement
in the description behind it was corrected. Every child delivered, every Definition of Done
criterion passes on its own evidence, all eleven questions are answered, and the tool's 63 tests
pass on the trunk as it stands.

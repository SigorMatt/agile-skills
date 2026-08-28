# Journal — WI-0004

Append-only. One entry per skill execution, per spec/journal-and-history.md section 2.

## 2026-08-28T14:57:22Z — answer-questions v0.3.1 — architect

- **Item:** WI-0004
- **Trigger:** created by this execution; the item did not exist before it. The execution itself
  was dispatched against EP-001 at `awaiting-answer`, whose sign-off question the stakeholder had
  answered
- **Inputs read:**
  - `tracker/items/EP-001/questions/Q-005.md` — the sign-off question and the stakeholder's answer
  - `tracker/items/EP-001/item.md` — the goal, the scope and the out-of-scope list
  - `tracker/items/WI-0003/item.md` — what the rules feature already promises, its AC1, AC8 and
    AC12, and the four gaps `review-close` accepted against it
  - `docs/architecture/adr/ADR-0010-rules-come-from-one-ini-file-named-on-the-command-line.md` —
    the decision this item reverses, including its rejected option E
  - `docs/product/vision.md` (v4) — the preview promise this item has to stay compatible with
  - `README.md` — what is documented about `--rules` today
  - `.claude/agile-skills/spec/ids-and-statuses.md` §5, `spec/question.md` §2, `spec/work-item.md`
- **Decisions:**
  - Filed as a new `work-item` at `draft` rather than folded into WI-0003's criteria. Rationale:
    WI-0003 is `done` and delivered; widening a closed item's criteria would hide the change from
    the board and from the stakeholder who asked for it (`answer-questions` SKILL.md step 3b).
  - `priority: medium`, not `high`. Rationale: the stakeholder accepted the engagement as it
    stands and called this the one thing they wanted "on top", so nothing is broken without it;
    and it is the only open item, so rank changes nothing about what runs next.
  - Criteria written rough and said to be rough, in the item itself. Rationale: `refine` owns the
    Definition of Ready, and the first of the open questions — *where* the default file lives — is
    the stakeholder's to answer, so writing criteria that fix a location would be inventing their
    answer.
  - AC4 — a run says which rule file it used — added by this skill rather than left for `refine`.
    Rationale: it is not a feature request, it is the answer to the reason ADR-0010 gave for
    rejecting a default location. Without it the item would reverse a decision and discard the
    argument behind it, and nobody downstream would know the argument had been made.
  - Recorded that `plan` must supersede ADR-0010 rather than edit it, and that the authorisation
    is the stakeholder's own answer. Rationale: `spec/doc-header.md` §4 — an ADR is never edited
    to change its decision — and `spec/question.md` §4 makes contradicting an ADR the human's to
    authorise, which is exactly what happened here.
  - Named the `--rules ""` gap `review-close` recorded on WI-0003 in `## Notes` without taking it
    into scope. Rationale: the same `if args.rules:` guard decides the fallback, so the design
    cannot avoid it, but it is a separate defect and folding it in silently would be scope creep.
- **Questions raised:** none. The open question this item carries — where the default file lives —
  is recorded in `## Notes` for `refine` to put to the stakeholder, because `refine` is the skill
  that talks to them and it will be asked with the rest of the round rather than on its own
- **Commands:**
  - `scripts/new-item --id WI-0004 --type work-item --epic EP-001 --priority medium --status draft
    --actor answer-questions --arose-from EP-001/Q-005` → exit 0, created at `draft`
  - `scripts/lint-claims tracker/items/WI-0004/item.md` → exit 0, 0 errors after one absolute was
    sourced to ADR-0010
- **Gates:** the gates of this execution are recorded on EP-001's journal entry, which is the item
  this execution was dispatched against. The two that bear on this file:
  - `answered-from-the-record` → **pass** — every statement in this item is either the
    stakeholder's own words from `EP-001/Q-005` or a citation of WI-0003, ADR-0010 or the vision
  - `workspace-valid` → **pass** (`scripts/validate-workspace`, exit 0 — evidence on EP-001)
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` (new — story, AC1–AC6, out of scope, notes)
  - `tracker/items/WI-0004/history.md`, `journal.md` (new, headers written by `scripts/new-item`)
- **Status:** `—` → `draft`
- **Result:** WI-0004 exists at `draft`: the tool should find the user's rule file without being
  told where it is on every run. It is the single follow-up the stakeholder named when they
  accepted the engagement, and it reverses ADR-0010 on their authority.

## 2026-08-28T15:02:22Z — refine v0.2.2 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` — the only runnable item in the workspace;
  the nine others are `done` and EP-001 is at `open`
- **Inputs read:**
  - `tracker/items/WI-0004/item.md`, `history.md`, `journal.md` — a fresh draft, one history row,
    created by `answer-questions` from the sign-off answer. Not a send-back: nothing has been
    built against it, so the whole item is in scope rather than one defect
  - `tracker/items/EP-001/questions/Q-005.md` — the stakeholder's words that produced this item,
    and the two things they declined
  - `tracker/items/EP-001/questions/Q-001.md` — the standing delegation this round relies on:
    "Whatever's easiest for you to build and test — you know this better than me"
  - `tracker/items/EP-001/questions/Q-002.md`, `Q-003.md` — never-overwrite and top-level-only, so
    that neither is re-asked
  - `tracker/items/EP-001/item.md` — the epic's scope and out-of-scope lists
  - `tracker/items/WI-0003/item.md` and `artifacts/refinement-qa.md` — what the rules feature
    already promises (AC1, AC8, AC12), the four gaps `review-close` accepted against it, and the
    house style for this file
  - `docs/architecture/adr/ADR-0010-rules-come-from-one-ini-file-named-on-the-command-line.md` —
    the rejected option E, which is what this item is
  - `docs/architecture/adr/ADR-0011-a-ruleset-is-a-value-passed-into-the-planner.md` — why one
    more rule source is one coherent change (R9)
  - `docs/product/vision.md` (v5), `README.md`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/work-item.md`
- **Decisions:**
  - **One question to the stakeholder, not four.** Applied the procedure's triage in order. Only
    *where* the default file lives has product stake: the candidates differ in whether a folder
    somebody else handed them can change what happens to their files, which is the never-overwrite
    instinct [src: EP-001/Q-002], and it is the decision ADR-0010 took the other way, which
    `spec/question.md` §4 makes the human's to authorise.
  - **Three things decided here under the standing delegation** [src: EP-001/Q-001], each tagged
    `[assumed]` in the Q&A rather than recorded as theirs: `--rules` beats the default; a malformed
    file at the default location is refused as WI-0003 AC8 refuses one named with `--rules`; and a
    run states which rule file it used. The third is not a feature we invented — it is the answer
    to the one cost ADR-0010 named when it rejected a default location, and without it this item
    would reverse a decision and discard the argument behind it.
  - **Named the refusal assumption as the one most worth revisiting**, in the item's `## Notes`.
    Rationale: it means a typo in a file the user is not looking at stops every run until they fix
    it. That is a real cost, and burying it inside "consistent with AC8" would hide it. Recorded
    where the stakeholder can see it and object rather than filed as a second question, because the
    alternative — quietly sorting by the built-in tables when their own rule file is broken — is
    the surprise this product exists not to have [src: docs/product/vision.md].
  - **Did not rewrite the acceptance criteria this round.** Every one of them turns on "the default
    location", which does not exist until Q-001 is answered; a half-rewrite would have to be redone
    and would read as though it were finished. What round 2 will do is written into
    `artifacts/refinement-qa.md` instead, so the next execution inherits the job rather than
    re-deciding it.
  - **Wrote the R10 table now, with four rows marked open.** Rationale: R10 asks for the
    combinations to be *visible*, not decided. Four of them genuinely cannot be stated before
    Q-001, and marking them beats leaving them silent, which is the failure R10 was added for.
  - **Routed three things to `plan` rather than to a person**: whether `--rules ""` falls back to
    the default; which error wins when both the rule file and the target folder are bad; and the
    wording of the line naming the rule file in use. Each would have the same answer whoever the
    stakeholder is.
  - `artifacts/refinement-qa.md` declares `status: agenda`, not `recorded`. The exchange has not
    happened. R8 reads that field, and writing `recorded` on an agenda would pass the item to
    `ready` on a conversation nobody had.
- **Questions raised:** `Q-001` (blocking, to human) — where `tidy` should look for a rule file it
  was not told about; three options and a recommendation. One question, and the `## Context` says
  it is the whole ask for this round
- **Commands:**
  - `scripts/validate-workspace .` → exit 0 before the question was filed; 2 errors after it
    (`board.stale`, `question.blocking.not-suspended`), both of which are this transition being due
  - `scripts/lint-claims tracker/items/WI-0004/item.md .../artifacts/refinement-qa.md
    .../questions/Q-001.md` → 0 errors after three absolutes were sourced
  - `scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** — `scripts/validate-workspace .`, run by `transition` as part of
    this move, exit 0
  - `definition-of-ready` → **fail, criterion by criterion**, which is why this item is suspended
    rather than passed. R1 pass (frontmatter complete, `arose-from: EP-001/Q-005` resolves);
    R2 pass (role, capability, "so that"); R3 pass (AC1–AC6, labelled, checkboxes); **R4 fail** —
    every criterion turns on a "default location" that nothing names, and AC4 states no observable;
    R5 pass (five out-of-scope entries, two of them the stakeholder's own declines); **R6 fail** —
    Q-001 is blocking and open, by construction; R7 pass (`depends-on` empty; `relates-to: WI-0003`
    is `done`); **R8 fail** — `refinement-qa.md` declares `status: agenda`, honestly; R9 pass (one
    coherent change — one more source for a `Ruleset` that is already a value passed into the
    planner [src: ADR-0011]); **R10 fail** — four combinations cannot be stated before Q-001 and
    are recorded as open in `## Notes`. R4, R6, R8 and R10 all close on the same answer
  - `criteria-are-decidable` → **fail**, and this is the same gap as R4 rather than a second one.
    AC1, AC2, AC3 and AC5 name a command shape but not the place it acts on; AC4 names no
    observation at all. None of the six can be handed to someone with a terminal today. The round 2
    rewrite is what closes this, and what it must produce is written down in the Q&A
  - `qa-recorded-verbatim` → **pass on what exists**. Nothing is paraphrased into agreement and
    nothing is attributed to the stakeholder that they did not say: the only stakeholder words in
    the file are quoted from `EP-001/Q-005` and `EP-001/Q-001`, and every decision taken without
    them is tagged `[assumed]` with the delegation it rests on. The round 1 answer slot says in
    terms that it is not yet given
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` (new — blocking, to human, three options)
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` (new — `status: agenda`, the DoR table, the
    triage, and what round 2 will do)
  - `tracker/items/WI-0004/item.md` — the criteria preamble records the R4 failure; `## Notes`
    gains the round 1 record and the R10 combination table
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `awaiting-answer`
- **Result:** WI-0004 is not Ready and is suspended on one question to the stakeholder: where the
  tool should look for a rule file it was not told about. Everything else the Definition of Ready
  wanted is either decided here under their standing delegation, routed to `plan`, or written down
  as round 2's job. Four DoR criteria — R4, R6, R8, R10 — close on that single answer.

## 2026-08-28T15:07:41Z — answer-questions v0.3.1 — architect

- **Item:** WI-0004
- **Trigger:** status `awaiting-answer` with `Q-001` open, addressed to the human, and `## Answer`
  now filled in. Dispatched before `next`, per the rule that an answered-but-unconsumed
  human-addressed question stops every subsequent turn until it is propagated (F-011)
- **Inputs read:**
  - `tracker/items/WI-0004/questions/Q-001.md` — the question, its three options, the
    recommendation, and the stakeholder's reply
  - `tracker/items/WI-0004/item.md` — the rough criteria AC1–AC6, the out-of-scope list, and the
    three open questions `refine` recorded in `## Notes`
  - `tracker/items/WI-0004/history.md` — two rows; the suspending row carries `resume-to: draft`
  - `tracker/items/WI-0004/journal.md` — the `answer-questions` entry that created the item and the
    `refine` entry that suspended it, including what round 2 is expected to do
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — `status: agenda`, the DoR table, the
    triage, the four `[assumed]` decisions and the empty round 1 answer slot
  - `docs/architecture/adr/ADR-0010-rules-come-from-one-ini-file-named-on-the-command-line.md` —
    its option E, the two candidate locations, and the reason it rejected both
  - `docs/product/vision.md` (v5) — "The rules belong to the user" and "Open at the time of
    writing", which both still said the location question was outstanding
  - `tracker/items/EP-001/questions/Q-001.md` (the standing delegation), `Q-002.md` (the
    never-overwrite instinct the question appealed to), `Q-005.md` (the sign-off that produced
    this item)
  - `README.md` — line 86, "There is no default location", which describes today's tool
  - `.claude/agile-skills/spec/question.md` §§2–4, `spec/journal-and-history.md`,
    `spec/doc-header.md` §4, `spec/dor-dod.md`
- **Decisions:**
  - **Q-001 is `answered`, not `deferred`.** The reply chooses one of the three filed options by
    letter and restates the reason in the stakeholder's own words. Route: escalated and returned —
    the human answered, and this skill only propagates. Nothing about it defers.
  - **Read the answer as narrowly as it was asked.** It settles the *kind* of place: the user's own
    config directory, and not a file in the folder being tidied. It does not settle the filename,
    the path spelling, or whether the directory is found via `XDG_CONFIG_HOME` or a fixed
    `~/.config`. Rationale: the question said in terms that the spelling stayed ours, so reading a
    path out of the illustrative `~/.config/tidy/rules.ini` would be inventing an answer they were
    explicitly not asked for. The `XDG_CONFIG_HOME` question is new with the answer and is recorded
    as round 2's rather than decided here.
  - **Option C is dead, not merely unchosen.** The stakeholder gave a reason — rules must not ride
    along in a folder somebody hands them — and C keeps exactly the thing that reason rejects.
    Recorded in `item.md` and in the question's `## Answer` so that a later round cannot read "B"
    as "B for now, C later".
  - **Did not rewrite AC1–AC6.** `refine` owns the Definition of Ready, and `refinement-qa.md`
    already specifies the round 2 rewrite in detail. Rewriting the criteria here would be this
    skill doing `refine`'s job with none of its gates, and would make a half-finished rewrite look
    finished. R4 and R10 are therefore recorded as still failing.
  - **Did not write an ADR, and did not touch ADR-0010.** The supersession is already recorded as
    `plan`'s on this item, and `spec/doc-header.md` §4 forbids editing an ADR to change its
    decision. What this execution adds is the authorisation: `item.md` now records that the
    stakeholder's answer is what authorises the supersession, so `plan` inherits it rather than
    re-deriving it. ADR-0010 still reads `status: current` and still describes today's tool, which
    is true — the default location is not built.
  - **Set `refinement-qa.md` to `status: recorded`.** The exchange has now happened, and R8 reads
    that field. Left the round 1 DoR table as it was written and added a note beneath it saying
    which two rows the answer changed (R6, R8) and which two still fail (R4, R10). Rationale: the
    table is a dated verdict, and editing verdicts in place destroys the evidence of what was
    thought when.
  - **No new work item filed under step 3b.** The answer narrows the item's scope rather than
    widening it: it removes two of the three candidate locations and adds nothing that WI-0004 does
    not already cover.
  - **No entry on EP-001's journal.** The answer settles one detail inside an existing item; it
    does not change the shape of the engagement, which the sign-off already fixed.
- **Questions raised:** none
- **Commands:**
  - `scripts/lint-claims tracker/items/WI-0004/item.md .../artifacts/refinement-qa.md
    .../questions/Q-001.md docs/product/vision.md` → exit 1, 3 errors, then exit 1, 1 error, then
    exit 0 after four absolutes were sourced or rephrased
  - `scripts/validate-workspace .` → exit 1, 2 errors (`board.stale`,
    `question.awaiting.none-open`), both of which are this transition being due
  - `scripts/board-gen .` → exit 0
- **Gates:**
  - `answer-is-propagated` → **pass**, file by file. `item.md` — the criteria preamble now names
    the config directory and quotes the reply; `## Notes` open question 1 is struck through and
    answered; the round 1 section gains the answer; three R10 rows no longer say "open until Q-001
    is answered". `artifacts/refinement-qa.md` — `status: recorded`, the reply verbatim in the
    round 1 slot, and the note under the DoR table. `docs/product/vision.md` — v6, the config
    directory in "The rules belong to the user", and "Open at the time of writing" no longer says a
    question has to go back to them. Every file named in `## Consequences` was reopened and the
    change is in it.
  - `answered-from-the-record` → **pass**. The answer is the human's own reply in
    `questions/Q-001.md`, quoted verbatim wherever it is restated; the reading of what it does and
    does not settle cites the question's own text ("we will choose the exact name and spelling")
    and `WI-0004`'s recorded scope. No new decision was taken by this skill, so no ADR was due.
  - `escalation-is-justified` → **skipped** — nothing was re-addressed to the human. The original
    escalation stands justified in `Q-001`'s own context: it contradicted ADR-0010, which
    `spec/question.md` §4 reserves for the human.
  - `workspace-valid` → **pass** — `scripts/validate-workspace .`, run by `transition` as part of
    this move, exit 0
  - `item-resumed-correctly` → **pass**. `history.md` row 2 records `resume-to: draft`; this
    execution moves `awaiting-answer` → `draft`. Read from the row, not inferred from the asker.
  - `a-deferral-is-not-an-answer` → **skipped** — the reply defers nothing. It picks option B by
    letter and gives its reason, so move 1 and move 2 of step 3a do not arise.
- **Artifacts:**
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`, `answered-by: human`,
    `answered-at: 2026-08-28T15:05:01Z`; `## Answer` carries the reply verbatim plus what it does
    and does not settle; `## Consequences` names four files and the one deliberately untouched
  - `tracker/items/WI-0004/item.md` — criteria preamble, `## Notes` open question 1, the round 1
    record, and three rows of the R10 table
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — `status: agenda` → `recorded`; the round 1
    answer slot; a note under the DoR table saying which rows the answer moved
  - `docs/product/vision.md` — v5 → v6, with a change-log row
  - `tracker/board.md` — regenerated
- **Status:** `awaiting-answer` → `draft`
- **Result:** The stakeholder's answer to Q-001 is in the artifacts: the default rule file lives in
  the user's own config directory, and a rule file inside the folder being tidied is not a source.
  WI-0004 returns to `draft` for `refine`'s round 2, which now has a location to write AC1–AC6
  against; `plan` inherits the authorisation to supersede ADR-0010. Nothing is waiting on the
  stakeholder.

## 2026-08-28T15:13:33Z — refine v0.2.2 — product-analyst

- **Item:** WI-0004
- **Trigger:** status `draft`, dispatched by `next` — the only item in the workspace whose status
  has an owner; the nine others are `done` and EP-001 is at `open`. This is **round 2**: the item
  returned to `draft` from `awaiting-answer` when the stakeholder's answer to Q-001 was propagated,
  and the suspending row's `resume-to` is what brought it back. Not a send-back from a later stage —
  nothing has been built against this item
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the six rough criteria, the out-of-scope list, and the three
    open questions in `## Notes`
  - `tracker/items/WI-0004/history.md` — three rows; row 3 is `awaiting-answer → draft` by
    `answer-questions`, which is what makes this round 2 rather than a fresh refinement
  - `tracker/items/WI-0004/journal.md` — the two prior entries, including round 1's list of what
    round 2 would do
  - `tracker/items/WI-0004/questions/Q-001.md` — the answer, verbatim, and what it does and does not
    settle
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — round 1's agenda, triage and four
    `[assumed]` decisions, now `status: recorded`
  - `tracker/items/WI-0003/item.md` — AC1's sample folder `S` and its "where it goes today" table,
    AC2/AC4/AC5's rule files `F1`/`F3`/`F4`, AC6's omitted-section rule, AC8's six malformed
    classes, AC10's invariants, AC12's documentation criterion. This item's criteria are written in
    that vocabulary deliberately
  - `tidy/cli.py` — the `--rules` guard `if args.rules:`, the stdout-is-one-line-per-file promise,
    the banner already on stderr, exit 2 for a rule file that cannot be used, and the `--help` text
    and epilog that both say "there is no default location"
  - `tidy/ruleset_file.py` — `load` raises `RuleFileError` for every failure including `OSError`,
    which is why a missing file and an unreadable one are indistinguishable to the caller
  - `README.md` — the "Your own rules" section, its "**There is no default location.**" sentence,
    and the format documentation AC9 extends
  - `docs/architecture/adr/ADR-0010-...md` (the exit-2 rule and the cost it named against a default
    location), `docs/product/vision.md` (v6), `tracker/items/EP-001/questions/Q-001.md`,
    `Q-002.md`, `Q-005.md`, `tracker/items/BUG-0003/item.md`
  - `.claude/agile-skills/spec/dor-dod.md` §1, `spec/question.md`, `spec/work-item.md`
- **Decisions:**
  - **No question to the stakeholder this round.** Their answer opened exactly one new choice —
    whether the config directory is found by `XDG_CONFIG_HOME` or by a fixed `~/.config` — and it
    is inside the category they delegated with "whatever's easiest for you to build and test"
    [src: EP-001/Q-001]. Re-asking would tell them their answer was not heard (F-023).
  - **`D` = `$XDG_CONFIG_HOME/tidy/rules.ini`, else `<home>/.config/tidy/rules.ini`**, stated once
    at the head of the criteria rather than in each. Rationale: honouring `XDG_CONFIG_HOME` is the
    standard way to find a config directory, and it is what makes every criterion runnable against
    a temporary directory instead of the machine's real home — which is the delegation's own
    "easiest to build and test", not a stretch of it.
  - **The rule-file line goes on stderr** (AC4). Rationale: `cli.py`'s stdout is one line per file
    and nothing else, and WI-0003 AC1 compares stdout byte-for-byte, so stdout is not available.
    The banner is already there. The *wording* stays `plan`'s; the criterion fixes the stream, the
    ordering and that the path is in it, which is what makes it decidable without deciding prose.
  - **A run that loaded no rule file prints no such line** (AC4). Rationale: the line exists to make
    an *unnamed* file visible [src: ADR-0010]; with no rule file there is nothing hidden, and
    printing anyway would change what WI-0003 AC1 observes for no gain anybody asked for.
  - **An unreadable file at `D` is exit 2, an absent one is a no-rules run** (AC6 vs AC2). Rationale:
    a file the user put there and we cannot read is not the same event as no file at all, and the
    alternative — sorting silently by the built-in tables — is the surprise this product exists not
    to have. This is round 1's flagged assumption extended, and it is flagged again rather than
    quietly reused.
  - **An empty file at `D` is a rule file that was used** (AC7): no sorting changes, and AC4's line
    still names it. "Was a file read?" and "did it change anything?" are different questions.
  - **`--help` is in scope** (AC10). Its `--rules` help and its epilog both say there is no default
    location today. BUG-0003 was filed once already for help text left behind by an item, so this
    is a known repeated failure, not a hypothetical.
  - **Three additions to `## Out of scope`**: a rule file in the folder being tidied (the
    stakeholder's own refusal, so it belongs in scope-negative rather than only in a question
    file); a search chain of several locations; and any way to turn `D` off for one run — no
    `--no-rules`, and `--rules ''` is not documented as one. The third is the entry R5 wants: a
    reader could reasonably assume a default you can suppress.
  - **`--rules ""` stays routed to `plan`, and is now safe to leave there.** Round 1 called it
    `refine`'s and `plan`'s. `refine`'s half is decided by putting it out of scope: no criterion
    depends on it, so whichever behaviour `plan` gives it, nothing here is contradicted.
  - **Recorded a design point rather than a criterion**: `ruleset_file.load` raises the same
    exception for a missing file and an unreadable one, so calling it unguarded on `D` would exit 2
    on every machine with no rule file. AC2 and AC6 require them told apart. Named in `## Notes` so
    `implement` does not discover it.
  - **Did not touch AC-numbering compatibility with round 1.** AC1–AC6 were rough and are replaced
    by AC1–AC10 rather than extended; nothing downstream cites the old numbers, because nothing
    downstream exists yet.
- **Questions raised:** none this round. Round 1's `Q-001` is `answered`; nothing was left
  `[unresolved]`. The full round is in `artifacts/refinement-qa.md` under "Round 2"
- **Commands:**
  - `scripts/lint-claims tracker/items/WI-0004/item.md` → exit 0 after one absolute was rephrased
  - `scripts/lint-claims tracker/items/WI-0004/artifacts/refinement-qa.md` → exit 0 after one
    absolute was sourced
  - `scripts/validate-workspace .` → exit 0
  - `scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** — `scripts/validate-workspace .`, run by `transition` as part of
    this move, exit 0
  - `definition-of-ready` → **pass, criterion by criterion.** **R1 pass** — frontmatter complete;
    `type: work-item`, `epic: EP-001`, `priority: medium`, `arose-from: EP-001/Q-005` resolves.
    **R2 pass** — "As someone who has written a rule file and wants it used every time, I want
    `tidy` to find that file on its own, so that I do not have to type `--rules PATH` on every run":
    role, capability, outcome. **R3 pass** — AC1–AC10, labelled, checkboxes. **R4 fail → rewritten
    → pass**: round 1's six all turned on "the default location", which nothing named, and AC4
    stated no observable. AC1–AC10 name `D` explicitly, and each names a command and a verdict; see
    `criteria-are-decidable` below for the per-criterion check. **R5 pass** — seven out-of-scope
    entries, three added this round; the strongest is "a way to turn the default off for one run",
    which a reader could reasonably assume was included. **R6 pass** — no question on this item is
    open; `Q-001` is `answered`. **R7 pass** — `depends-on` empty, `relates-to: WI-0003` is `done`
    and merged. **R8 pass** — `artifacts/refinement-qa.md` declares `status: recorded`, and the
    exchange it records is one that happened: Q-001's answer is in it verbatim. **R9 pass** — one
    coherent change: one more source for a `Ruleset` that is already a value passed into the
    planner [src: ADR-0011], plus the line naming the source and the two documents that describe it.
    **R10 pass** — the table in `## Notes` has fourteen rows; twelve point at a criterion, two are
    marked deliberately unconstrained and name `plan` as their owner.
  - `criteria-are-decidable` → **pass**, per criterion. AC1: put `F1` at `D`, run PREVIEW over `S`,
    diff stdout against WI-0003 AC2's stated lines; then APPLY and compare the tree. AC2: no file at
    `D`, diff stdout against WI-0003 AC1's table, and `python3 -m unittest discover -s tests -t . -q`
    exit 0. AC3: `F1` at `D` plus `--rules F3`, grep stdout for `recent/tables/budget.csv`. AC4:
    capture the streams separately, search stderr for the rule file's path, confirm stdout carries
    no such line, and confirm a no-rules run's stderr has none. AC5: six files, one per WI-0003 AC8
    class, each run twice; check stderr is one line, stdout is empty, exit is 2, `S` unchanged. AC6:
    a mode-`000` file at `D`; same four observations. AC7: a zero-byte file at `D`; stdout equals
    AC2's, stderr names `D`, exit 0. AC8: `F1` at `D` over `S` with a colliding
    `recent/data/budget.csv`; check the `(2)` line, the hidden file's absence, the untouched
    subfolder, the `leave` line. AC9: read `README.md` against AC1–AC7 and grep for "There is no
    default location". AC10: `python3 -m tidy --help`, grep for "no default location" (must be
    absent) and for `D` (must be present). No criterion contains an adjective without a threshold.
  - `qa-recorded-verbatim` → **pass**. `refinement-qa.md` carries Q-001's answer word for word in a
    block quote, with the `[human]` marker the stakeholder's file used; every decision taken without
    them this round is tagged `[assumed]` and names the standing delegation it rests on; nothing is
    paraphrased into agreement, and `[unresolved]` is recorded as none because nothing was asked and
    left hanging. Round 1's DoR table is left exactly as it was written, with a dated note beneath
    it saying which rows the answer moved
- **Artifacts:**
  - `tracker/items/WI-0004/item.md` — AC1–AC6 replaced by AC1–AC10 with a shared vocabulary
    preamble naming `D`; three entries added to `## Out of scope` and one clarified; `## Notes`
    questions 2 and 3 closed, the `--rules ""` gap narrowed, a round 2 section added with the
    design point about `ruleset_file.load`, and the R10 table completed to fourteen rows
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — a "Round 2" section (six `[assumed]`
    decisions with the delegation each rests on, what was not asked and why, what stays routed to
    `plan`, `[unresolved]: none`), a check of what round 2 did against what round 1 said it would,
    and round 1's instruction kept verbatim beneath it
  - `tracker/board.md` — regenerated
- **Status:** `draft` → `ready`
- **Result:** WI-0004 is Ready. The default rule file lives at `$XDG_CONFIG_HOME/tidy/rules.ini`
  or `<home>/.config/tidy/rules.ini`, `--rules` overrides it, a run names the file it used on
  stderr and says nothing when it used none, and a broken or unreadable file there stops the run
  the way a named one does. Ten criteria, each with a command and a verdict; nothing waits on the
  stakeholder. `plan` inherits two unconstrained crossings, one design trap, and the obligation to
  supersede ADR-0010 on the stakeholder's authority.

## 2026-08-28T15:19:10Z — plan v0.3.1 — architect

- **Item:** WI-0004
- **Trigger:** status `ready`, dispatched by `next` — the only item in the workspace with a status
  that has an owner; the nine others are `done` and EP-001 is at `open`
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC10, the vocabulary preamble that fixes `D`, the seven
    out-of-scope entries, and `## Notes`: the two crossings routed here and the design point about
    `ruleset_file.load`
  - `tracker/items/WI-0004/artifacts/refinement-qa.md` — round 2's six `[assumed]` decisions and
    what each rests on; `[unresolved]: none`, so there is no soft ground left by refinement
  - `tracker/items/WI-0004/history.md`, `journal.md` — four rows; this is a first plan, not a
    re-plan, and nothing has been rejected
  - `tracker/items/WI-0004/questions/Q-001.md` — the stakeholder's answer and its reason, which is
    the authorisation ADR-0014 needed
  - `docs/architecture/adr/ADR-0010` (the decision superseded here, both halves), **ADR-0011** (a
    `Ruleset` is a value passed into the planner — why nothing below `cli.py` moves), **ADR-0001**
    (stdlib only, 3.9 floor), **ADR-0006** (an event that ends the run before there is a run belongs
    to `cli.py`: one line on stderr, exit 2), **ADR-0008** (help text is prose guarded by a test),
    **ADR-0009**, **ADR-0004** (the project's test and lint commands), **ADR-0013**
  - `docs/architecture/overview.md` (v9) — the three layers, the module table, "What is
    deliberately not here", and the `grep` form of ADR-0008's condition
  - `docs/product/vision.md` (v6), `README.md` (the "Your own rules" section)
  - the code: `tidy/cli.py` (the `if args.rules:` guard, the stdout-is-one-line-per-file promise,
    the banner already on stderr, the ordering of the rule file before the folder check),
    `tidy/ruleset_file.py` (`load` converts every failure including `OSError` into `RuleFileError`),
    `tidy/rules.py` (`merge`, `BUILT_IN`), `tests/support.py` (`FolderTestCase`, `listing`),
    `tests/cli_support.py` (`run`, `destinations`), `tests/test_cli.py` (the help-text guards)
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are set and real
- **Decisions:**
  - **ADR-0014, superseding ADR-0010 in part.** Route: **asked and already answered** — the
    authorisation is the stakeholder's sign-off ask [src: EP-001/Q-005] and their choice of place
    [src: WI-0004/Q-001], so this skill wrote the ADR rather than re-asking. It supersedes only the
    "where the file comes from" half; ADR-0010's format decision is untouched and still current, and
    the ADR says so in its own header so a reader of ADR-0010 is not told the whole file is dead.
  - **`XDG_CONFIG_HOME`, then `HOME`, then no default location — from the environment mapping, not
    `os.path.expanduser`.** Route: **documented + assumption**. `expanduser` falls back to the `pwd`
    database when `HOME` is unset — checked, not assumed: `env -u HOME python3 -c
    'os.path.expanduser("~")'` printed this machine's home directory — so with `expanduser` a test
    could never say "there is no config directory", and a test run could pick up the developer's own
    rule file. Reading the mapping makes the whole feature a function of the environment.
  - **Presence is `os.path.lexists`, and present-but-unusable is exit 2 while absent is a no-rules
    run.** Route: **documented** — AC2 and AC6 require the two to differ, and `load` cannot tell them
    apart because it collapses every `OSError` into `RuleFileError` [src: tidy/ruleset_file.py].
    `lexists` rather than `exists` so a dangling symlink counts as something the user put there,
    which is the same instinct ADR-0009 applied to an entry that cannot be examined.
  - **`--rules` wins by being given, not by being non-empty, so `--rules ""` exits 2.** Route:
    **documented** — the item routed this crossing here [src: WI-0004], and once a default exists the
    old truthiness guard would quietly turn an empty string into a way of *reaching* the default.
    Recorded in ADR-0014 and in `## Risks`, because it changes behaviour nobody asked to change.
  - **The wording `tidy: using rules from <path>`, with the path as `resolve` returned it.** Route:
    **assumption A2**, reversible in one format string. `refine` left the wording here and AC4
    constrains only the stream, the ordering and that the path is in it.
  - **The test suite is made hermetic in `tests/support.py`, not per-test.** Route: **assumption
    A4**, and named in `## Risks` as the one step a reviewer could read as gaming AC2. It changes no
    assertion; without it every test's result depends on the runner's own home directory.
  - **`XDG_CONFIG_HOME` used as given, without an absolute-path check** (A1), and **an unsearchable
    parent directory reads as absent rather than unusable** (A3). Route: **assumptions**, each with
    its reversal cost, because no criterion names either case.
  - **Nothing below `cli.py` changes.** Route: **documented** — ADR-0011 already made a `Ruleset` a
    value passed into `build_plan`, so where it came from is not something the planner can observe.
    The plan has no step touching `planner.py`, `rules.py` or `apply.py`.
  - **No production code written.** `## Scaffolding` is `none`; every file the plan names already
    exists and both project commands already run.
- **Questions raised:** none. Nothing in this design is irreversible or depends on intent no
  document records: the one decision that was both — a default location at all — was put to the
  stakeholder by `refine` and answered before this skill ran [src: WI-0004/Q-001]
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → exit 0, 158 tests, OK (the baseline AC2
    compares against)
  - `python3 -m compileall -q tidy tests` → exit 0
  - `env -u HOME python3 -c 'import os; print(os.path.expanduser("~"))'` → printed `/home/msi`,
    which is the evidence behind ADR-0014's rejection of option D
  - `scripts/lint-claims --changed-since main` → exit 0, 3 documents
  - `scripts/lint-claims` on `plan.md`, `ADR-0014`, `overview.md` individually → exit 0 after four
    absolutes were sourced or rephrased
  - `scripts/validate-workspace .` → exit 0
  - `scripts/board-gen .` → exit 0
- **Gates:**
  - `workspace-valid` → **pass** — `scripts/validate-workspace .`, run by `transition` as part of
    this move, exit 0
  - `every-criterion-is-addressed` → **pass** — the mapping table in `plan.md` has one row per AC,
    AC1 through AC10, each naming the step that satisfies it and the specific observation that
    demonstrates it (a named test and what it asserts, or a `grep` and its expected count). No AC is
    demonstrated by the word "tests"
  - `project-commands-resolved` → **pass** — `commands.test` is
    `python3 -m unittest discover -s tests -t . -q` and `commands.lint` is
    `python3 -m compileall -q tidy tests`, both set for WI-0001 under ADR-0004; both were run by
    this execution and both exited 0, so neither is a command that only looks real
  - `decisions-recorded` → **pass** — the `## Decisions and ADRs` table lists seven choices; six
    point at a numbered section of ADR-0014 and the seventh at assumptions A1–A4, each of which
    states what reversing it costs
  - `claims-are-sourced` → **pass** — `scripts/lint-claims --changed-since main`, exit 0
  - `plan-is-executable-without-you` (advisory) → **pass** — read back cold, the step that most
    needed a decision the plan does not make was step 3's placement of the stderr line relative to
    the folder check; it is now stated explicitly, with the reason. Steps 1 and 2 name the function
    signatures and the values they return for specific inputs, so a developer does not have to infer
    the contract from the criteria
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/plan.md` (new — problem, approach, eight steps, the AC mapping,
    four assumptions, the decision table, `## Scaffolding: none`, four risks, six out-of-scope
    entries)
  - `docs/architecture/adr/ADR-0014-a-rule-file-in-the-users-config-directory-is-read-when-none-is-named.md`
    (new, v1 — supersedes ADR-0010 in part)
  - `docs/architecture/adr/ADR-0010-...md` (v1 → v2 — `status: superseded`, `superseded-by:
    ADR-0014`, and a header note saying *which half*. No text below the header changed: the decision
    it records is what was believed on 2026-08-27)
  - `docs/architecture/overview.md` (v9 → v10 — the module table entry for `ruleset_file.py`, "What
    is deliberately not here" rewritten from "no default location" to "no rule file inside the
    folder being tidied", and a new opening paragraph in "Where the remaining item will touch this")
  - `tracker/board.md` — regenerated
  - `tracker/project.yaml` — unchanged; both commands were already real
- **Status:** `ready` → `planned`
- **Result:** WI-0004 is planned. `ruleset_file.py` gains `default_path` and `resolve`, `cli.py`
  calls them and prints one stderr line naming the rule file it used, the help text and `README.md`
  stop saying there is no default location, and the test suite is made hermetic so that a
  developer's own rule file cannot change a test result. ADR-0014 records the reversal of ADR-0010's
  "no default location" half on the stakeholder's authority, and keeps its format half alive.
  Nothing below `cli.py` is touched.

## 2026-08-28T15:21:18Z — implement v0.2.2 — developer

- **Item:** WI-0004
- **Trigger:** status `planned`, dispatched by `next` as the only runnable item (no open question anywhere, no stakeholder request, EP-001 has no owner at `open`)
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC10, `## Out of scope`, and the two rows R10 routed to `plan`
  - `tracker/items/WI-0004/artifacts/plan.md` — eight steps, the AC mapping, A1–A4, and the four risks
  - `tracker/items/WI-0004/history.md` — five rows; the last is `ready` → `planned`, so this is a fresh start and no branch existed
  - `tracker/items/WI-0004/questions/Q-001.md` — `status: answered`, already propagated into `item.md` and ADR-0014; read for provenance, not for the decision
  - `tracker/project.yaml` — `commands.test` and `commands.lint` are both real; `conventions.branch-prefix` `wi/`
  - `docs/architecture/adr/ADR-0014-*.md` — the five fixed points the plan executes
  - `tidy/ruleset_file.py`, `tidy/cli.py`, `tests/support.py`, `tests/cli_support.py`, `tests/test_cli.py` (the WI-0003 section), `tests/test_ruleset_file.py`, `README.md` (`## Your own rules`)
- **Decisions:**
  - none yet — this entry opens the execution. The plan is executed as written; deviations, if any, are recorded in the closing entry and in `impl-report.md`.
- **Questions raised:** none
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → 0
- **Gates:**
  - `tests-pass` → **skipped** (not yet run: no change has been made; the gate is run on the branch head at step 7)
  - `lint-clean` → **skipped** (same reason)
  - `workspace-valid` → **skipped** (same reason)
  - `every-criterion-has-a-test` → **skipped** (same reason)
  - `commits-reference-the-item` → **skipped** (same reason: no commit exists yet)
  - `claims-are-sourced` → **skipped** (same reason)
- **Artifacts:**
  - branch `wi/WI-0004`, branched from `main` at `4d60b3b`
- **Status:** `planned` → `in-progress`
- **Result:** Implementation of WI-0004 has started on `wi/WI-0004`. Nothing is built yet; the closing entry reports the work and runs every gate on the branch head.

## 2026-08-28T15:29:30Z — implement v0.2.2 — developer

- **Item:** WI-0004
- **Trigger:** status `in-progress` on `wi/WI-0004`, continuing the execution this journal's previous entry opened
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC10, the two R10 rows routed to `plan`, and `## Out of scope`
  - `tracker/items/WI-0004/artifacts/plan.md` — the eight steps, the AC mapping, assumptions A1–A4, the four risks
  - `docs/architecture/adr/ADR-0014-*.md` — the five fixed points, executed rather than re-decided
  - `docs/architecture/overview.md` — read to see whether this change invalidated it (it does, in one sentence; see `## What I did not do`)
  - `tidy/ruleset_file.py`, `tidy/cli.py`, `tests/support.py`, `tests/cli_support.py`, `tests/test_cli.py`, `tests/test_ruleset_file.py`, `README.md`
- **Decisions:**
  - **Added `run_interleaved()` to `tests/cli_support.py`, a deviation from plan step 7's "using the existing `run()` helper".** AC4 requires the naming line to come *before* the first per-file line, and the two are on different streams; `run()` keeps them apart, so against two buffers the claim degrades to "first on stderr", which is weaker than the criterion. `run_interleaved` redirects both into one buffer. Additive — `run()` is unchanged and every other test still uses it. A *how*, not a *what*.
  - **AC5's malformed exhibits come from `MALFORMED_RULE_FILES` in `tests/test_cli.py`, not from `tests/test_ruleset_file.py`** as step 7 names. That module builds each malformed file inline per test; the reusable table is in `test_cli.py`. The intent — do not restate the classes — is met against the table that exists.
  - **Mutation-checked every new behaviour rather than trusting that the tests bind.** Each was removed in turn and the suite re-run: the default location (25 failures), the stderr naming line (7), `lexists` → `exists` (2), `argument is not None` → truthiness (1), the `HOME` fallback (2). Self-check 1 asks whether a criterion's test would fail if the behaviour were removed, and the only honest way to answer is to remove it.
  - **Checked plan step 5's hermeticity claim empirically instead of asserting it.** With a rule file at the caller's `XDG_CONFIG_HOME` the suite is `OK`; with one at the caller's `HOME` it is `OK`; with the isolation removed and a rule file at the caller's `XDG_CONFIG_HOME` it is `FAILED (failures=11, errors=32)`. That is the evidence that step 5 removes an environment dependency rather than accommodating the item, which is the argument AC2 will be read against.
  - **Did not update `docs/architecture/overview.md`.** Its line 123 says WI-0004 "is planned and not yet built", which this branch makes false; everything else it says about `default_path`, `resolve` and the default location was written forward-looking by `plan` and is accurate. The edit is not one of the plan's eight steps and no criterion names it, so making it would be widening the item on this skill's own authority. Declared in `impl-report.md` `## What I did not do` as a handover to `review-close`'s D7 and D12, which own document truth.
  - **Did not document or tidy `--rules ""`.** It is now exit 2 (ADR-0014 point 3), which is a user-visible change nobody asked for; the item puts it out of scope and `README.md` has never promised anything about it, so nothing there contradicts it. Its message carries a double space where the empty path would be — cosmetic, no criterion covers it, and fixing it is the "fixing things you noticed on the way" failure. Both named in the report for a reviewer.
  - Everything else was executed as the plan wrote it, including A1–A4 unchanged.
- **Questions raised:** none — nothing arose that the plan and ADR-0014 did not already decide
- **Commands:**
  - `git checkout -b wi/WI-0004 main` → 0
  - `python3 -m unittest discover -s tests -t . -q` → 0, `Ran 203 tests ... OK` (174 on `main`; 29 new). Run after every plan step and again on the branch head `72b59a1`
  - `python3 -m compileall -q tidy tests` → 0
  - `XDG_CONFIG_HOME=<dir> python3 -m unittest discover -s tests -t . -q` → 0, `OK` (hermeticity, with a rule file at the caller's config directory)
  - `env -u XDG_CONFIG_HOME HOME=<dir> python3 -m unittest discover -s tests -t . -q` → 0, `OK`
  - the same with step 5's isolation removed → 1, `FAILED (failures=11, errors=32)`
  - five mutation runs, each reverted → 1 in every case, counts above
  - `XDG_CONFIG_HOME=<cfg> python3 -m tidy <S>` → 0, live AC1/AC4/AC7 transcripts quoted in the report
  - `env -u XDG_CONFIG_HOME -u HOME python3 -m tidy <S>` → 0 (AC2, no config directory at all)
  - `XDG_CONFIG_HOME=<cfg> python3 -m tidy <S> --apply` with a malformed file at `D` → 2 (AC5)
  - `python3 -m tidy --help | grep -c "no default location"` → `0` (AC10)
  - `grep -c "There is no default location" README.md` → `0` (AC9)
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0, `all 4 commit(s) on main..wi/WI-0004 name WI-0004`
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `0 errors, 0 warnings`
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0 on branch head `72b59a1`, `Ran 203 tests ... OK`)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests` exit 0 on the same head)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, `checked 11 item(s), 16 document(s)`, `0 errors, 0 warnings`)
  - `every-criterion-has-a-test` → **pass** (AC1–AC10 each name at least one test function in `impl-report.md`'s evidence table; AC9's non-test half is an exact command with its output. Bound is demonstrated by the five mutation runs above, not asserted)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, all 4 commits on `main..wi/WI-0004`)
  - `no-unplanned-scope` → **pass** (advisory; seven source files, each traced to a plan step in `impl-report.md` `## Gates`. The two hunks that do not match the plan verbatim are the two deviations above, both declared)
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0. It reports `checked no documents changed since main`, which is correct rather than vacuous: this execution changed no file under `docs/`, and the one document it *should* have changed is declared undone above rather than left for the gate to miss)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/impl-report.md` — new
  - branch `wi/WI-0004`, commits `main..wi/WI-0004` = `baa4ebf`, `64c81ad`, `7aaa697`, `72b59a1`
  - `tidy/ruleset_file.py`, `tidy/cli.py`, `tests/support.py`, `tests/cli_support.py`, `tests/test_cli.py`, `tests/test_ruleset_file.py`, `README.md` — all updated
- **Status:** `in-progress` → `verifying`
- **Result:** All eight plan steps are executed and all ten criteria have a test that fails when the behaviour is removed. A run with no `--rules` reads `$XDG_CONFIG_HOME/tidy/rules.ini` or `$HOME/.config/tidy/rules.ini`, refuses a file that is there but unusable, treats nothing being there as a no-rules run, and names on stderr whichever rule file it used. Two deviations and four omissions are declared in `impl-report.md`; the one a reviewer most needs is that `docs/architecture/overview.md` still calls this item unbuilt, which is `review-close`'s D7 and D12 to settle.

## 2026-08-28T15:36:19Z — verify v0.1.4 — qa-engineer

- **Item:** WI-0004
- **Trigger:** status `verifying`, dispatched by `next` as the only runnable item
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — AC1–AC10 and the `D` preamble, **read before the implementation report**, so that what would settle each criterion was derived from the criterion
  - `tracker/items/WI-0004/history.md` — six rows; the last is `in-progress` → `verifying`
  - `tracker/items/WI-0004/artifacts/plan.md` — the eight steps, assumptions A1–A4, and the four risks, read for the deviation check
  - `tracker/items/WI-0004/artifacts/impl-report.md` — read after the criteria, and cited as evidence nowhere
  - `tracker/project.yaml` — `commands.test`, `commands.lint`
  - the code at branch head **`aefa6d017f821e22e5cad24d7245c0391aa6d08f`**, and `git diff main..HEAD` over `tidy/`, `tests/` and `README.md`
  - `docs/architecture/adr/ADR-0014-*.md` and `docs/architecture/overview.md`
- **Decisions:**
  - **AC2's "no existing test edited to accommodate this item" is a pass, and the reasoning is in the report rather than in my head.** `tests/support.py` was edited, which is what `plan` predicted an argument about. I decided it with two measurements, not a reading: (1) the diff removes no line at all from `tests/support.py` or `tests/cli_support.py`, and removes only a docstring line and an import line from each of the two test-case modules — no test body or assertion changed; (2) `main`'s 158 tests, restored byte-for-byte with `git checkout main -- tests/` and run against this branch's `tidy/` in a clean environment, give `Ran 158 tests … OK`, so nothing needed accommodating. The same unedited 158 fail 8 with a rule file at the caller's `XDG_CONFIG_HOME`, which is the dependency the edit removes. The strictest reading would fail the clause and I recorded it explicitly so a reviewer can take it instead.
  - **Verified through the real command line, not through the project's test helpers.** Every criterion was driven with `python3 -m tidy` in a subprocess over a sample folder this skill built from WI-0003's definition. A criterion checked only by the tests written to satisfy it is checked by the implementation's own reasoning, which is the thing this skill exists not to do.
  - **AC4's ordering clause was settled with a real `2>&1` pipe.** The suite checks it in-process with a shared `StringIO`; merging two real file descriptors is the stronger check and it agreed.
  - **The `--rules ""` change is neither a send-back nor a bug.** No acceptance criterion of this item says it should be different, which is step 7's test, so it is not a send-back; and it is behaviour this item introduces rather than a defect delivered by another item, so `found-in` would have nowhere to point. It is planned — ADR-0014 point 3 — and `review-close` already handled the *previous* state of this same question as a recorded gap on WI-0003 rather than as a bug. Recorded in `## Defects found` and routed there, including that its message has a double space and names no path.
  - **Did not file a bug for the stale overview sentence** for the same reason: `impl-report.md` declares it and it is D7's and D12's, which are `review-close`'s gates. I confirmed the sentence is still present and that the rest of the overview's WI-0004 material is accurate.
  - **Nothing was judged `ambiguous`.** Every criterion named a command and a verdict, and each one decided.
- **Questions raised:** none — no criterion was ambiguous enough to need the architect
- **Commands:**
  - `python3 -m unittest discover -s tests -t . -q` → 0, `Ran 203 tests … OK` (on `aefa6d0`, and again after every mutation was reverted)
  - `python3 -m compileall -q tidy tests` → 0
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, `0 errors, 0 warnings`
  - `git checkout main -- tests/` then the suite → 0, `Ran 158 tests … OK`; the same with `XDG_CONFIG_HOME` pointed at a directory holding a rule file → 1, `FAILED (failures=8)`; branch tests restored afterwards
  - AC1: 6 runs (`F1` and `F4`, at `D` and via `--rules`, PREVIEW and APPLY over rebuilt folders) → all 0; `diff` of stdouts and of `find`ed trees → identical
  - AC2: 4 runs (empty config dir PREVIEW/APPLY; `env -u XDG_CONFIG_HOME -u HOME`; `XDG_CONFIG_HOME=` with `HOME` unset) → all 0
  - AC3: 1 run with `F1` at `D` and `--rules F3.ini` → 0; two greps over stderr
  - AC4: 8 runs — separated streams and `2>&1`-merged, both modes, both sources, plus a no-rules run; `cat -A` for the line ending
  - AC5: **22 runs** — eleven malformed exhibits × two modes, each with sha256 listings before and after → all exit 2, stdout 0 B, one stderr line naming `D`, tree unchanged
  - AC6: **4 runs** — mode `000` and a dangling symlink, each in both modes → all exit 2, nothing moved
  - AC7: 2 runs over a zero-byte file at `D` → 0, stdout `diff`ed identical to a no-rules run's, stderr names the file
  - AC8: 2 runs over an `S` with a pre-existing subfolder and a colliding destination, plus `sha256sum` before and after
  - AC9: `grep -c "There is no default location" README.md` → `0`; the new section read clause by clause
  - AC10: `python3 -m tidy --help | grep -c "no default location"` → `0`; `grep -n` for `rules.ini`, `XDG_CONFIG_HOME`, `overrides`
  - `--rules ''` on this branch → 2; the same invocation with `main`'s `tidy/` restored → 0
  - **seven mutation runs**, each reverted, each recorded with the tests it broke; `git diff HEAD --stat` empty afterwards
- **Gates:**
  - `tests-pass` → **pass** (`python3 -m unittest discover -s tests -t . -q` exit 0 on `aefa6d0`, `Ran 203 tests … OK`)
  - `lint-clean` → **pass** (`python3 -m compileall -q tidy tests` exit 0)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, `checked 11 item(s), 16 document(s)`, `0 errors, 0 warnings`)
  - `every-criterion-independently-checked` → **pass** (all ten rows of `verify-report.md` `## Criteria` name a command this skill ran in a subprocess and quote its actual output; the implementation report is cited as evidence for nothing)
  - `negative-cases-exercised` → **pass** (22 malformed runs, 4 unreadable runs, 3 empty-environment runs, 2 empty-file runs, 1 collision, 1 `--rules ""` — every one triggered, inventoried in `## Negative and boundary cases exercised`)
  - `tests-would-fail-without-the-change` → **pass** (advisory; seven mutations, the failing tests named per criterion in `## Test sensitivity check`. The `lexists`-guard mutation additionally broke ~35 pre-existing tests, which shows the old suite is now sensitive to this behaviour rather than blind to it)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/verify-report.md` — new, `Verified-commit: aefa6d017f821e22e5cad24d7245c0391aa6d08f`
  - `tracker/items/WI-0004/item.md` — AC1–AC10 all ticked, each against a command in the report
  - no bug items filed
- **Status:** `verifying` → `in-review`
- **Result:** All ten criteria pass against branch head `aefa6d0`, each on evidence this skill produced through the real command line rather than through the project's test helpers. AC2's contested clause is a pass on two measurements — no existing test's assertions changed, and `main`'s 158 unedited tests pass against this code in a clean environment — with the opposing reading recorded so `review-close` can take it instead. Two things are routed to review rather than dropped: `--rules ""` now exits 2 with an unhelpful message, and `docs/architecture/overview.md` still calls this item unbuilt.

## 2026-08-28T15:41:23Z — review-close v0.5.0 — reviewer

- **Item:** WI-0004
- **Trigger:** status `in-review`, dispatched by `next` as the only runnable item
- **Inputs read:**
  - `tracker/items/WI-0004/item.md` — the ten criteria, `## Out of scope`, and all of `## Notes`
  - `tracker/items/WI-0004/history.md` — all eight rows, checked for a gap and against the item's status
  - `tracker/items/WI-0004/journal.md` — **read in full**, all eight entries; certifying the record is complete cannot be done from a skim
  - `tracker/items/WI-0004/artifacts/plan.md`, `impl-report.md`, `verify-report.md` — including `## What I did not do` and `## Not verified, and why` in full
  - `tracker/items/WI-0004/questions/Q-001.md` — answered, and each file its `## Consequences` names was opened
  - **the diff `main..wi/WI-0004`, hunk by hunk** — `git diff main..wi/WI-0004 -- tidy/` read in full, `--stat` over `tests/` and `README.md`, and `git diff … | grep '^-'` per test module for AC2's contested clause
  - `docs/architecture/adr/ADR-0010`, `ADR-0011`, `ADR-0014`; `docs/architecture/overview.md`; `docs/product/vision.md`
  - the merge result in a detached worktree at `ea1dc0b`
- **Decisions:**
  - **Accept and close as `delivered`.** Every hunk in `tidy/` traces to a plan step, no hunk contradicts an ADR, and the Definition of Done passes criterion by criterion.
  - **Fixed the two stale documents myself rather than sending the item back.** `docs/architecture/overview.md` said WI-0004 "is planned and not yet built" and `docs/product/vision.md` said the default location was "wanted and not yet built" with the criteria and the ADR supersession still owed — all false as of this merge. `impl-report.md` declared the overview one and handed it to D7 and D12, which was the right call by `implement`: the edit is not one of the plan's eight steps and no criterion names it. It did not find the vision one. D7 and D12 are *my* gates, the fix is documentary rather than behavioural, and a send-back would have cost a round trip to change two paragraphs. Overview v10 → v11, vision v6 → v7, each with a change-log row, committed as `58a03fc`.
  - **`--rules ""` is an accepted gap, not a send-back and not a bug.** No criterion of this item covers it, so it is not a send-back; ADR-0014 point 3 decided it and `item.md` routed it to `plan`, so it is in scope and correctly decided. I did not file a bug: the engagement has already been signed off once, the behaviour is out of scope by this item's own words, and adding a child over something the stakeholder was never asked about would prolong an engagement they accepted. Recorded in `item.md` `## Notes` — including that the message names no path, which is the part worth fixing — and surfaced in `docs/product/vision.md` v7 so it reaches them at sign-off rather than being decided for them.
  - **The `--help` epilog's `~/.config/…` shorthand is accepted.** The code reads `HOME` from the mapping and never calls `expanduser`; `~` is the conventional shorthand and `README.md` states the full rule including the neither-variable-set case. The two diverge only with `HOME` unset, where `~` would resolve through the password database and the tool correctly consults nothing.
  - **The two declared deviations are accepted.** `run_interleaved` is additive and is the only way AC4's cross-stream ordering claim is checkable at all; AC5 reusing `test_cli.py`'s malformed table meets step 7's intent against the table that actually exists. Both are *how*, not *what*, and both were declared rather than discovered.
  - **The D12 audit was done from the citations, not from the prose.** Eight claims, each decided by opening what it cites; six true against the code, two false and corrected. The table is in `review.md` `## What I examined`.
  - **Trial-merged detached, and confirmed the trunk did not move.** `git worktree add --detach`; `main` was `4d60b3b` before and `4d60b3b` after, checked rather than assumed (F-055).
- **Questions raised:** none — nothing in the change contradicted a recorded decision, so there was nothing to put to the architect
- **Commands:**
  - `.claude/agile-skills/scripts/check-verify-freshness WI-0004 wi/WI-0004` → 0, "verified at aefa6d01; wi/WI-0004 has moved to 8a28c3e4 but only the record changed (5 file(s) under tracker/ or docs/)"
  - `git log main..wi/WI-0004 -- tidy/ tests/ README.md` → last code commit `7aaa697`, which precedes the verified commit
  - `.claude/agile-skills/scripts/check-commit-refs WI-0004 wi/WI-0004` → 0, "all 7 commit(s) … name WI-0004"
  - `.claude/agile-skills/scripts/check-epic-signoff WI-0004` → 0, "WI-0004 is a 'work-item', not an epic … PASS"
  - `.claude/agile-skills/scripts/lint-claims --changed-since main` → 0, "checked 2 document(s) changed since main", 0 errors
  - `.claude/agile-skills/scripts/validate-workspace .` → 0, "0 errors, 0 warnings"
  - `git rev-parse main` before the trial → `4d60b3b…`
  - `git worktree add --detach /tmp/trial main` → 0; `git -C /tmp/trial merge --no-ff wi/WI-0004` → 0, 15 files changed; trial HEAD `ea1dc0b`
  - `python3 -m unittest discover -s tests -t . -q` **inside `/tmp/trial`** → 0, `Ran 203 tests … OK`
  - `python3 -m compileall -q tidy tests` **inside `/tmp/trial`** → 0
  - `git worktree remove --force /tmp/trial` → 0; `git rev-parse main` after → `4d60b3b…`, unmoved
  - `grep -c "^- \[x\] AC" item.md` → `10`; `grep -c "^- \[ \] AC"` → `0`
- **Gates:**
  - `definition-of-done` → **pass** (D1–D12 each with its own result and evidence in `review.md` `## Definition of Done`; D7 and D12 pass **after** this execution made the two document corrections they exist to catch)
  - `verification-postdates-the-code` → **pass** (`check-verify-freshness` exit 0, and confirmed independently against `git log main..wi/WI-0004 -- tidy/ tests/ README.md`)
  - `commits-reference-the-item` → **pass** (`check-commit-refs` exit 0, all 7 commits; run **before** merging, which is why the close precedes the merge)
  - `tests-pass-on-the-merge-result` → **pass** (`Ran 203 tests … OK` and lint exit 0, both inside the detached trial worktree at `ea1dc0b` — the merge result, not the branch)
  - `workspace-valid` → **pass** (`validate-workspace .` exit 0, `checked 11 item(s), 16 document(s)`, `0 errors, 0 warnings`)
  - `record-is-reconstructible` → **pass**. *What was built and why*: `item.md` `## Story` and `## Notes` trace it to `EP-001/Q-005` in the stakeholder's words, and ADR-0014 records the authorisation. *Which decisions, by which skill*: every history row names its actor, every journal entry is stamped with skill, version and persona, and ADR-0014 says "Decided by: plan (architect), for WI-0004". *What questions arose and how they were resolved*: `Q-001`, addressed to human, answered, with `## Consequences` naming five files I opened. *What verification found*: `verify-report.md`, with a `Verified-commit` line and a command per criterion. I could answer all four from the tracker, `docs/` and `git log --grep WI-0004` alone
  - `claims-are-sourced` → **pass** (`lint-claims --changed-since main` exit 0 over the two documents this execution changed)
  - `epic-sign-off` → **pass** (`check-epic-signoff WI-0004` exit 0 — not applicable to a work item; the termination gate applies to an engagement's ending. EP-001's own state is the next dispatch's question, not this one's)
- **Artifacts:**
  - `tracker/items/WI-0004/artifacts/review.md` — new
  - `tracker/items/WI-0004/item.md` — `## Notes` records the accepted `--rules ""` gap; closed `done`/`delivered`
  - `docs/architecture/overview.md` v10 → v11 and `docs/product/vision.md` v6 → v7, committed as `58a03fc`
  - the merge of `wi/WI-0004` into `main`, made after this entry
  - no bug items filed, and no question filed
- **Status:** `in-review` → `done`
- **Result:** Accepted and closed as delivered. The change does what the item asked, in a way this project should live with: only the two modules the architecture predicted were touched, ADR-0011's layering is upheld, and the one decision a later reader would be tempted to "correct" carries both a reason and a test. Two documents that called this item unbuilt were corrected as part of the close, which is what D7 and D12 are for. Three gaps are accepted, each recorded where it survives the item — chief among them that `--rules ""` now exits 2 with a message naming no path, which is surfaced to the stakeholder rather than settled for them.

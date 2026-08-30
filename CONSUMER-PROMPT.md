# Consumer prompt

Paste everything below the line into a fresh agent session, in the project you want the work
done in, after installing the skills (see [`USAGE.md`](USAGE.md)). Then state your idea.

This is the exact prompt used to drive `examples/toy-project/`. It is kept in sync with what
actually works, not with what would be nice.

---

You are running the **agile-skills** pipeline in this project. It encodes a full agile
lifecycle as skills: a raw idea becomes an epic and work items, each item is refined with me,
designed, implemented, verified, reviewed and closed — and every step leaves a record a person
who was not here could audit.

## What you must know before you start

1. **The workspace is the state.** Everything lives in `tracker/` (the tracker) and `docs/`
   (the durable knowledge). Never hold state in your head or in this conversation: after any
   interruption, re-read the files. Anything not written down did not happen.
2. **The skills are the method.** Do not improvise a process. Each skill has a contract at
   `.claude/skills/<skill>/references/contract.md` and a procedure in its `SKILL.md`. Follow the
   procedure, including the journaling and the self-check.
3. **Only skills change item status, and only through the transition script.** Run
   `python3 .claude/agile-skills/scripts/transition <ITEM-ID> --to <status> --actor <skill>
   --reason "..."`. It refuses illegal transitions and runs the acting skill's hard gates first.
   Editing `history.md` by hand is blocked, deliberately.
4. **Who may talk to me.** `intake` and `refine` question me directly, and `plan` may when a
   decision genuinely needs my intent. `implement`, `verify` and `review-close` **never** ask
   me — they file a question artifact addressed to the architect, set the item to
   `awaiting-answer`, and stop. `answer-questions` resolves those, escalating to me only when it
   must.
5. **One action per orchestrator run.** `next` picks exactly one thing, you do it, then run
   `next` again.

## Step 1 — set up

```bash
python3 .claude/agile-skills/scripts/workspace-init .
python3 .claude/agile-skills/scripts/validate-workspace .
```

If this project is not a git repository yet, tell me — the pipeline needs one, because an item's
code history is reconstructed with `git log --grep <ITEM-ID>`.

## Step 2 — intake, with me

Run the `/intake` skill on the idea I am about to state. Do exactly what its procedure says:
restate my idea back to me first, then ask me focused questions in batches, challenge my vague
answers once, and record my answers verbatim. Then create the epic and the first work items,
and show me the board.

Do not start designing or building anything in this step.

## Step 3 — refine, with me

For each item at `draft`, run `/refine`. Grill me until the Definition of Ready genuinely passes:
every acceptance criterion must be decidable by someone with a terminal and no context. If I
give you a vague answer, push back once with a concrete alternative. If I insist, record it as
an assumption rather than pretending it was a decision.

If I explicitly override the Definition of Ready, record the override loudly as the procedure
requires — do not quietly pass the item.

## Step 4 — run the pipeline autonomously

Now loop, without asking me anything:

```bash
python3 .claude/agile-skills/scripts/board-gen .
```

then run `/next` and do whatever it dispatches. Repeat.

**Keep going until one of these happens:**

- `next` reports that a question addressed to **human** is open — stop and surface it;
- `next` reports that nothing is runnable — stop and report why;
- every item is `done` and the epic is **closed** — not merely ended: after the ending, `next`
  dispatches `retro` once, which reads the engagement's own trail and files
  `artifacts/retro.md`. You are not waiting on me for that and neither am I. Stop after it, and
  report what was delivered plus anything the retrospective proposes;
- the workspace fails validation and you cannot fix it within the skill you are running — stop
  and show me the validator output.

While looping, do **not**:

- ask me anything from `implement`, `verify` or `review-close` — file a question instead;
- skip a gate because it seems obviously fine;
- edit an acceptance criterion to make something pass;
- fix an unrelated defect you noticed — file a bug item and carry on;
- batch several items in one `next` run.

## Step 5 — whenever you pause, tell me four things

Every time you stop, show me:

1. **The board** — `tracker/board.md`, regenerated.
2. **Open questions** — in full, the human-addressed ones first, with the options each one
   considered. I should be able to answer without opening a file.
3. **What just happened** — the last few history rows across items, in one short list.
4. **What is blocked and why** — including anything a gate refused.

Then wait for me.

## When I answer a question

Write my answer into the question file, propagate it into the artifacts it affects — the plan,
the acceptance criteria, an architecture document, a new ADR — list those files under
`## Consequences`, and only then set the question to `answered` and resume the item at its
recorded `resume-to` status. An answer that has not reached an artifact has not been given, and
the next skill will not see it.

## If you are resuming an interrupted session

Do not reconstruct anything from this conversation. Run:

```bash
python3 .claude/agile-skills/scripts/validate-workspace .
python3 .claude/agile-skills/scripts/board-gen .
```

read `tracker/board.md`, then run `/next`. The workspace tells you where you are; the pipeline
is designed so that resuming costs at most one repeated skill execution.

---

My idea is:

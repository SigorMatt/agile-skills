---
status: recorded
---

# Refinement Q&A — WI-0001

## How this round was conducted

**No new question was put to the stakeholder in this round, and none is pending.** That is a
routing decision, not an omission, and this section records the basis for it so a reader can
disagree with it.

The stakeholder is asynchronous: they answer in files between turns, and they had just answered
four questions on EP-001. Two of those answers are **standing deferrals over a category**, which
`refine`'s step 3 treats as real answers that apply to the whole category rather than only to the
question that produced them:

> *"Whatever's easiest for you to build and test — you know this better than me. Python's fine if
> that's your call. Yeah, a terminal command is fine, nothing fancier needed."*
> — [human], EP-001/Q-001

> *"Doesn't matter to me, honestly — whichever's easier for you. Just don't leave either one
> hanging forever."*
> — [human], EP-001/Q-004

Against those, they stated exactly two things they *do* care about, and both are already recorded
as criteria rather than as preferences:

> *"Never overwrite, full stop — that's the one thing I actually care about here… I don't want to
> ask about this again."* — [human], EP-001/Q-002 (now AC9, AC10)

> *"Top level only — leave existing subfolders alone. Simplest option, go with that."*
> — [human], EP-001/Q-003 (now AC11, AC12)

Every gap this refinement found is either inside the delegated category — what things are called,
how the command is invoked, the wording of output, exit codes, the default mapping — or has a
conservative answer that follows directly from the safety emphasis they did state. So each was
decided here and tagged `[assumed]`, naming the deferral relied on, and each is carried into the
item's `## Notes` so that `plan`, `implement` and `verify` inherit it as a visible assumption
rather than discovering it. None of them is expensive to reverse: the whole default mapping
becomes the user's to change in WI-0003, and a stakeholder who dislikes any of these can say so on
the epic at any time.

The alternative — filing four or five questions about flag names and folder names — is the failure
mode F-023 records, where a stakeholder received four questions on one item and found that *"three
of the four were things I'd expect a team to just decide on their own"*.

---

## Q1 — Does the command preview by default, or move by default?

**Why asked:** DoR R4. AC1 as drafted said "pointed at a folder in preview mode" without saying
how a user selects that mode, so no criterion was decidable: a verifier could not tell whether
typing the command with no flags is safe.

**Answer** `[assumed]` — relying on the EP-001/Q-001 deferral over invocation, and on the
stakeholder's own emphasis. **The tool previews by default. Moving files requires an explicit
flag.**

The deferral covers the *spelling*; it does not cover the direction, and the direction is not a
coin flip. The stakeholder led their whole idea with the dry run, and said the never-overwrite
guarantee is the one thing they actually care about. A tool where the bare command moves files
would put the dangerous behaviour behind the shortest invocation, which contradicts the stated
emphasis. Choosing the safe side of this needs no confirmation.

Recorded as AC1 and AC2. The flag's exact name is left to `plan`.

## Q2 — What is the default type-to-folder mapping, exactly?

**Why asked:** DoR R4. AC4 as drafted said files are "grouped by kind of file" and the mapping is
"stated somewhere a user can read". Neither is decidable: two implementations could both satisfy it
and disagree about where every file goes.

**Answer** `[assumed]` — relying on the EP-001/Q-001 deferral. **Seven folders — `documents`,
`spreadsheets`, `images`, `audio`, `video`, `archives`, `code` — with the exact extension lists now
written into AC5.** Matching is by filename extension only, case-insensitive, because EP-001's
out-of-scope list forbids reading file contents to classify them.

Rationale for deciding rather than asking: this is the most reversible thing in the item. WI-0003
exists specifically to hand the mapping to the user, so any disagreement about it is resolved by
the feature they already asked for rather than by a question. A conventional mapping is also the
one a person can predict without being told, which is EP-001's fourth success measure.

## Q3 — What happens to a file whose extension is not in the mapping?

**Why asked:** DoR R4 and R10. AC5 as drafted required "a stated, observable outcome" without
stating one, which is a criterion that cannot fail.

**Answer** `[assumed]` — relying on the EP-001/Q-001 deferral. **It is left exactly where it is,
and both modes report it on a distinct line saying so.** It is not swept into a catch-all folder.

The two candidates were "leave it" and "move it to `other/`". "Leave it" was chosen because
EP-001's vision says the tool moves files and does nothing else, and moving a file the tool
admits it does not understand is the one move most likely to surprise. It is also the option a
user can override themselves once WI-0003 lands, by adding a rule; the reverse — recovering files
from `other/` — is work.

The cost is honest and is written into the item's `## Notes`: a folder full of unrecognised
extensions is reported and left untidied, so a run can be a no-op and still be correct.

## Q4 — Are hidden files (names beginning with `.`) tidied?

**Why asked:** DoR R10. Nothing in the item, the epic or the vision said, and a "messy folder"
on a Unix machine routinely contains `.bashrc`, `.DS_Store` and `.gitignore`. An implementation
could reasonably do either, and the two differ in a way a user would notice immediately.

**Answer** `[assumed]` — relying on the EP-001/Q-001 deferral, decided on the safe side.
**Hidden files are skipped entirely: not moved, and not listed as movable.**

Someone pointing this tool at their home directory and finding `.bashrc` in `code/` would
reasonably call it broken. Hidden files are configuration rather than clutter, and the same
argument applies as in Q3: a user who wants them tidied can say so in WI-0003's rules, whereas
undoing it is manual. Recorded as AC13.

## Q5 — What does the tool do when there is nothing to move?

**Why asked:** DoR R10 — the empty and no-op cases are combinations of the modes this item
introduces, and neither had a stated behaviour.

**Answer** `[assumed]` — relying on the EP-001/Q-001 deferral over output wording. **It prints a
single line saying there is nothing to do and exits 0, in both modes.** Exit 0 because finding a
folder already tidy is a success, not an error; a line rather than silence because silence is
indistinguishable from a crash. Recorded as AC15.

## Q6 — What happens when the target path is missing or is not a folder?

**Why asked:** DoR R4. AC6 as drafted said "an error a user can act on and a non-zero exit
status", which does not say what a verifier would check.

**Answer** `[assumed]` — relying on the EP-001/Q-001 deferral over exit codes and message wording.
**A message on stderr that contains the offending path, nothing on stdout, and exit status 2.**
Exit 2 rather than 1 so that a future non-zero exit for a partial failure can be distinguished
from a usage error; 2 is the conventional usage-error status and is what `argparse` already uses.
Recorded as AC14.

## Nothing was left `[unresolved]`

Every item on this round's agenda was closed. Two things are deliberately left unconstrained
rather than unresolved, and both are named in the item's `## Notes` with who left them so, per
DoR R10: the exact form of the collision suffix (the stakeholder explicitly left it open — *"or
whatever you want to call it"*), and what happens if a destination folder name is already taken by
a *file* at the top level.

---
id: EP-001
type: epic
title: Tidy a messy folder safely, with a preview before anything moves
status: done
priority: medium
created: "2026-08-27T15:43:53Z"
updated: "2026-08-28T16:30:35Z"
outcome: delivered
---

## Goal

Someone with a folder that has accumulated hundreds of unsorted files can hand that folder to a
tool and get it organised into subfolders, sorted by what kind of file each one is and by how old
it is. Before anything is touched, they can see the complete list of moves the tool intends to
make and decide whether to go ahead. The rules that decide where a file lands are theirs to
change, not fixed by whoever wrote the tool.

## Why now

The stakeholder stated the need directly: a messy folder that nobody wants to sort by hand. The
cost of not solving it is that the sorting either does not happen or is done manually, and the
cost of solving it *badly* is worse than not solving it at all — a tool that moves hundreds of
files in one go and gets it wrong is very hard to undo by hand. That is why the preview is part
of the goal rather than a feature on top of it.

## Success measures

- Running the tool in preview mode over a folder prints one line per file naming the file and the
  destination it would be moved to, and the folder's contents are unchanged afterwards (checkable
  by comparing a directory listing taken before and after).
- Running the tool for real over the same folder produces exactly the destinations the preview
  named — the same set of files in the same places, and no file present before the run is absent
  after it.
- **No file is ever overwritten.** When a destination name is already taken the incoming file is
  moved under a suffixed name instead, and both the preview and the real run report that it was
  renamed and to what (checkable by putting two files of the same name and kind in the sample
  folder and reading the output). This is the stakeholder's stated hard constraint
  [src: EP-001/Q-002].
- Changing the rules the tool is given changes where files land, without editing the tool's own
  source, and the difference is visible in the preview output.
- A person who did not write the tool can run it against a folder of sample files and, from its
  output alone, say where each file went and why.

## Scope

- A tool that takes a folder and organises the files sitting directly in it into subfolders.
  Subfolders that are already there are left alone: they are neither entered nor moved
  [src: EP-001/Q-003].
- Deciding a destination for each file from its type and its age.
- A preview mode that reports the full set of intended moves and changes nothing.
- Rules supplied by the user rather than hard-coded, so the type-to-folder and age-to-folder
  decisions can be changed.
- The tool is a command typed in a terminal, written in Python 3 against the standard library
  only [src: ADR-0001].
- Finding the user's rule file without being told where it is on every run. Added after the
  stakeholder accepted the engagement and named this as the one thing they wanted on top of it:
  "give the rule file a default spot it just picks up on its own" [src: EP-001/Q-005]. It is
  WI-0004, and it reverses ADR-0010's deliberate choice of no default location, on their
  authority [src: ADR-0010; src: WI-0004].

## Out of scope

These are things a reader could reasonably assume are included. They are not, unless the
stakeholder says otherwise:

- **Recursion into subfolders.** The tool considers only the files directly inside the folder it
  is pointed at; existing subfolders are left untouched. This was a stakeholder decision, not an
  assumption [src: EP-001/Q-003], and they were offered the chance to reverse it at sign-off and
  declined: "Don't bother with the subfolder thing or undo, I don't need either of those"
  [src: EP-001/Q-005]. It stays out.
- Undoing a run after the fact. The preview is the safety mechanism; a rollback log is a
  different and larger piece of work. Offered to the stakeholder at sign-off as a candidate
  follow-up and declined in the same sentence [src: EP-001/Q-005].
- Deleting, deduplicating, compressing or renaming files — except for the collision suffix the
  never-overwrite rule requires [src: EP-001/Q-002]. This tool moves files and nothing else.
- Making the never-overwrite behaviour configurable. The stakeholder settled it once and asked not
  to be asked again [src: EP-001/Q-002], so it is an invariant of the tool rather than a rule the
  user supplies.
- **Fixing the `--rules ""` message, and making a broken rule file at the default location fall
  back to the built-in tables.** Both were offered by name as follow-up candidates at the second
  sign-off, and both were declined: *"Don't bother with the `--rules ""` message or making a broken
  rules file fall back to the built-in tables — if I typo my own rules file that's on me to fix,
  I'd rather it stop and tell me than guess."* [src: EP-001/Q-006]. The second half of that sentence
  also converts a team assumption into a stakeholder decision: refusing an unusable rule file at the
  default location, rather than sorting by the built-in tables instead, is now theirs
  [src: ADR-0014; src: WI-0004].
- Any graphical interface, file-manager integration, or scheduled/background operation.
- Organising anything other than a folder on the local filesystem — no cloud storage, no network
  shares as a first-class target.
- Reading file *contents* to classify them (magic-byte sniffing, EXIF, document parsing).
- Watching a folder continuously and tidying new arrivals as they appear.

## Notes

The four questions raised during intake — the target environment, filename collisions, recursion
into subfolders, and the delivery order — were answered by the stakeholder and propagated on
2026-08-27; see `questions/Q-001.md` … `questions/Q-004.md` and their `## Consequences` sections.
Nothing from intake was left waiting on the stakeholder. (Two termination questions have been put
to them since — `Q-005` and `Q-006` — and both are answered; see the three sections below.)

**Delivery order: WI-0001, then WI-0002, then WI-0003.** The stakeholder had no preference and
delegated the order, asking only that neither of the later two be left hanging
[src: EP-001/Q-004]. The order is recorded on the items as `priority` — `high`, `medium`, `low`
respectively — because that is the field the orchestrator selects on. On WI-0003, `low` records
its position in the sequence and nothing else: it is not optional, and this epic cannot close with
an outcome of `delivered` unless all three are delivered.

### Sign-off, 2026-08-28 — accepted with one follow-up, and the engagement did not end

The engagement reached rest with all nine children `done` and delivered, `review-close` filed the
termination question, and the stakeholder answered it: **option B — accept, with a named
follow-up.** In their words: *"B — ship it, and add the rules file location. It looks like it does
what I asked for. The one thing I want on top: I don't want to pass `--rules` every single time,
so give the rule file a default spot it just picks up on its own. Don't bother with the subfolder
thing or undo, I don't need either of those."* [src: EP-001/Q-005]

Two things follow, and the second is not what the question's option B predicted.

1. The follow-up is **WI-0004**, at `draft`, created by `answer-questions` from that answer
   [src: WI-0004]. Subfolder recursion and undo were declined and stay on the list above.
2. **This epic does not close now.** Option B's stated consequence was that the engagement "still
   closes as delivered" while the new work is opened, and that is not executable: an engagement
   ends only from rest, rest requires every child at a terminal status, and WI-0004 is at `draft`
   (`spec/ids-and-statuses.md` §3.5). So the epic returns to `open`, WI-0004 is refined and built
   like any other item, and when the engagement next comes to rest a **fresh** sign-off is due,
   because the one answered here accepted something else (`spec/question.md` §2). The acceptance
   is not lost — it is recorded here and in Q-005 — but it is an acceptance of the nine items
   listed in that question, not of whatever WI-0004 turns out to be.

### Second rest, 2026-08-28 — the engagement is at rest again and a fresh sign-off is open

WI-0004 — the follow-up the stakeholder named at the first sign-off — closed as `delivered` at
15:41:23Z, which is the moment `scripts/engagement-state EP-001` records as the engagement's
**second** rest. All ten children are now terminal and every one of them delivered.

`Q-005`'s acceptance does not carry over, and the reason is mechanical as well as fair:
`scripts/check-epic-signoff` refuses it because it was filed at 14:12:48Z, before this rest, so
"the stakeholder was asked about something other than what they are being asked to accept"
(`spec/question.md` §2 — exactly one sign-off is due per rest). WI-0004 exists *because* of that
answer, so it is precisely what the answer could not have covered.

So `review-close` filed **`Q-006`**, the second termination question: it names all ten children,
shows WI-0004 running rather than describing it, and puts the two gaps accepted during WI-0004's
delivery in front of the stakeholder — the `--rules ""` message that names no path, and the
decision that a malformed file at the default location stops the run instead of falling back
[src: WI-0004]. The epic went to `awaiting-answer` with `resume-to: open`, and the answer has since
arrived — the next section.

### Second sign-off, answered 2026-08-28 — accepted as complete, and nothing further is wanted

The stakeholder answered `Q-006`: **option A — accept as complete.** In their words: *"A — ship
it, we're done. Ten for ten, close it out. Don't bother with the `--rules ""` message or making a
broken rules file fall back to the built-in tables — if I typo my own rules file that's on me to
fix, I'd rather it stop and tell me than guess. Good work."* [src: EP-001/Q-006]

Three things follow.

1. **The engagement's ending is E1, `delivered`,** and this time nothing stands in the way of it:
   all ten children are terminal and every one of them delivered, the acceptance post-dates the
   rest it accepts, and it names no follow-up. `review-close` applies the epic Definition of Done
   and records the ending; this section records only what the stakeholder said, because deciding
   the outcome here would be `answer-questions` closing an epic, which is not its move
   (`spec/ids-and-statuses.md` §3.5).
2. **Both named follow-up candidates were declined**, so no work item was opened from this answer
   and the `## Out of scope` list above now carries them. This is the second sign-off in a row at
   which the stakeholder has declined everything offered them beyond what they asked for.
3. **One assumption stops being an assumption.** `refine` recorded that refusing a malformed rule
   file at the default location — rather than falling back to the built-in tables — was
   "the assumption most worth revisiting", because a typo in a file the user is not looking at
   stops every run until it is fixed [src: WI-0004]. It was put to them and they chose it, for the
   reason the team gave for it: *"I'd rather it stop and tell me than guess."* ADR-0014's decision
   is unchanged; what changed is that its point 4 is now authorised rather than assumed
   [src: ADR-0014].

### The ending, 2026-08-28 — E1, `delivered`

`review-close` applied the epic Definition of Done at the engagement's second rest and every one of
DE1–DE7 passes; the criterion-by-criterion table, the five success measures re-run rather than
quoted, and the claim audit are in `artifacts/review.md`. All ten children are `done` with
`outcome: delivered`, and the stakeholder's acceptance post-dates the rest it accepts
[src: EP-001/Q-006].

So the engagement ends at **E1**: `open → done`, `outcome: delivered`. Not `delivered-partial` —
that ending is for an epic closing over a child that did not deliver, and there is none here.

Two things are accepted rather than fixed, both declined by the stakeholder by name at the second
sign-off, and both recorded in `## Out of scope` above: the `--rules ""` message, and a broken rule
file at the default location stopping the run instead of falling back [src: EP-001/Q-006;
src: WI-0004]. Anything wanted from here starts as a new request under `tracker/requests/`, which
is the one channel that does not begin with a skill asking [src: .claude/agile-skills/spec/request.md].

---
title: Product vision — tidy
version: 9
status: current
updated: 2026-08-28T16:28:18Z
updated-by: review-close
updated-for: EP-001
---

# Product vision — tidy

## Who this is for

A person who has a folder on their own machine that has silently accumulated files — a downloads
folder, a desktop, a scratch directory — and who wants it organised without sorting it by hand.
Today the alternatives are to sort it manually, to leave it, or to run a script somebody else
wrote and hope. This stakeholder was explicit that they want to see what will happen first.

## What it is for

`tidy` takes a folder and moves the files in it into subfolders, choosing each destination from
what kind of file it is and how old it is.

**The two combine age-first.** The top level of a tidied folder is `recent/` and `old/`, and the
type folders sit inside those: `recent/images/holiday.jpg`, `old/documents/taxes-2019.pdf`. The
stakeholder chose this shape over a type folder holding age folders, and said why — "I want to look
at the top level and know what's actually live, not go hunting inside every type folder for the
recent one" — so `old/` is one place they can archive or delete in a single action
[src: WI-0002/Q-001]. **A file is `old` when it has not been touched for a year**, and `recent`
otherwise; two bands, one boundary [src: WI-0002/Q-002]. Which timestamp "touched" means, and what
exactly a year is measured as, are recorded on WI-0002 rather than here.

Two things distinguish it from a shell one-liner:

1. **It shows its work before it does it.** A preview run reports every move it intends to make
   and changes nothing. This is the product's central promise, not a convenience flag — a tool
   that reorganises hundreds of files in one irreversible step is not usable by someone who
   cannot check it first.
2. **The rules belong to the user, and the rule file is theirs.** Where a kind of file goes, and
   what counts as old, are the user's to change without editing the tool. A run takes them from a
   rule file, and it finds that file **by itself**: with no `--rules`, it reads
   `$XDG_CONFIG_HOME/tidy/rules.ini`, or `$HOME/.config/tidy/rules.ini` when that variable is
   unset [src: tidy/ruleset_file.py]. `--rules PATH` names one explicitly and overrides the
   default when you want a different file for one run [src: ADR-0010; src: tidy/cli.py]. The
   default location is there because the stakeholder asked for it once the flag existed — "give
   the rule file a default spot it just picks up on its own" — and WI-0004 built it
   [src: EP-001/Q-005]. Asked **where**, they chose **their own config directory**:
   one rule file belonging to the person, used for every folder they tidy. A rule file sitting in
   the folder being tidied is deliberately not a source — *"I don't want rules riding along in a
   folder someone hands me"* [src: WI-0004/Q-001] — so nothing inside a target folder can change
   what a run does to it. A run **says** which rule file it used, on stderr before it prints
   anything about the files, because a file shaping a run without appearing anywhere the user
   looked is the one cost ADR-0010 weighed against a default location [src: ADR-0010;
   src: tidy/cli.py].

One thing is not negotiable and is not a rule the user supplies: **`tidy` does not overwrite
files.** If it wants to move `report.pdf` somewhere that already has a `report.pdf`, it moves the
incoming one under a suffixed name and says so, in the preview and again in the real run
[src: EP-001/Q-002; src: WI-0001 AC9]. The stakeholder named this as the one thing they actually
cared about, and asked not to be asked about it again.

`tidy` is a command typed in a terminal, written in Python 3 against the standard library, so
there is nothing to install before running it [src: ADR-0001].

## What it deliberately is not

- It is not a file manager, a deduplicator, a cleaner, or a backup tool. It moves files; it does
  not delete, rename, compress or modify them.
- It is not a daemon. It runs when asked and then stops; it does not watch a folder.
- It does not undo. The preview is how a user avoids needing to. The stakeholder was offered undo
  as a follow-up when they signed the engagement off and declined it [src: EP-001/Q-005].
- It does not look inside files to decide what they are.
- It is not a cloud or network storage tool.
- It does not go looking inside subfolders. Pointed at a folder, it tidies the files sitting
  directly in that folder; folders that are already there — including the ones it made on an
  earlier run — are left alone [src: EP-001/Q-003]. That is what makes running it twice safe. They
  were offered the chance to reverse this at sign-off and declined it [src: EP-001/Q-005].

## How we will know it is working

A person who did not build it can point it at a folder of sample files, read the preview, predict
where each file will go, run it for real, and find that their prediction was right — and can then
change a rule and see the preview change accordingly.

## Open at the time of writing

Nothing is waiting on the stakeholder. Everything that has been asked of them has been answered:
the four intake questions — the target environment, filename collisions, recursion into
subfolders, and the delivery order [src: EP-001/Q-001; src: EP-001/Q-002; src: EP-001/Q-003;
src: EP-001/Q-004]; how type and age combine, which turned out to be theirs to decide rather than
the team's [src: WI-0002/Q-001; src: WI-0002/Q-002]; whether user rules replace or layer over the
built-in ones — they layer, and the user's entries win [src: WI-0003/Q-001]; and how many age
bands there are — two, always [src: WI-0003/Q-002].

**They have signed the engagement off twice, and the second time they accepted it as complete.**
Told what the nine items delivered, they accepted that and named a default location for the rule
file, so `--rules` need not be typed every time [src: EP-001/Q-005]. That is WI-0004, and it is
delivered [src: tracker/items/WI-0004/item.md]. Shown it running, and told what the ten items now
under this engagement delivered, they accepted again and asked for nothing further: *"A — ship it,
we're done. Ten for ten, close it out."* [src: EP-001/Q-006]

The one question inside it was put to them and answered: **where** the default file lives — beside
the folder being tidied, or in the user's own config directory. It was theirs rather than ours
because the two differ in what happens to a folder somebody else handed you, and they chose their
own config directory for exactly that reason [src: WI-0004/Q-001]. ADR-0010's "no default
location" half was superseded on the authority of that answer, and its format half is untouched
and still current [src: ADR-0014; src: ADR-0010].

**Nobody has asked for anything this product does not now do, and two things offered were turned
down.** `--rules` given an empty string used to be a silent no-rules run and now ends the run with
exit 2 and a message naming no path — a consequence of making the flag win by being *given* rather
than by being non-empty, which nobody asked for and no criterion covers
[src: tracker/items/WI-0004/item.md]. That was put to the stakeholder at the second sign-off,
alongside the other candidate they might have wanted — making a broken rule file at the default
location fall back to the built-in tables instead of stopping the run — and they declined both:
*"if I typo my own rules file that's on me to fix, I'd rather it stop and tell me than guess"*
[src: EP-001/Q-006]. So the message stays as it prints today, and stopping on a rule file the user
cannot have meant is the stakeholder's choice rather than the team's [src: ADR-0014].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 9 | 2026-08-28T16:28:18Z | review-close | EP-001 | DE4 at the engagement's ending: "What it is for" still opened with "Today that means a rule file named on the command line", which described the tool before WI-0004 and invited a reader to quote it as the whole truth. The paragraph now states what a run does — it finds the rule file itself, and `--rules` overrides — with the history after it rather than in front of it |
| 8 | 2026-08-28T16:23:10Z | answer-questions | EP-001 | Recorded the stakeholder's second sign-off answer [src: EP-001/Q-006]: they accept the engagement as complete, ten items for ten, and declined both follow-ups offered — the `--rules ""` message and a fallback to the built-in tables when the default rule file is broken. Nothing in "Open at the time of writing" is now theirs to settle |
| 7 | 2026-08-28T15:41:00Z | review-close | WI-0004 | WI-0004 is delivered, so the three passages calling the default location "wanted and not yet built" and listing what was still owed on it are now what the tool does. Recorded the `--rules ""` change as the one thing the stakeholder has not been told about [src: tidy/ruleset_file.py; src: tidy/cli.py] |
| 6 | 2026-08-28T15:05:01Z | answer-questions | WI-0004 | Recorded the stakeholder's answer to WI-0004/Q-001: the default rule-file location is their own config directory, and a rule file in the folder being tidied is deliberately not a source. "Open at the time of writing" no longer says a question inside WI-0004 has to go back to them |
| 5 | 2026-08-28T14:57:00Z | answer-questions | EP-001 | Recorded the stakeholder's sign-off answer to EP-001/Q-005: they accepted the engagement and asked for a default location for the rule file (now WI-0004), and declined subfolder recursion and undo. Rewrote "Open at the time of writing", which still said the replace-or-layer question was open inside the team after WI-0003/Q-001 had settled it |
| 4 | 2026-08-27T17:58:40Z | answer-questions | WI-0002 | Recorded the stakeholder's answers to WI-0002/Q-001 and Q-002: a tidied folder is `recent/` and `old/` at the top level with the type folders inside, and a file untouched for a year is old. Removed the layout from the list of things open inside the team |
| 3 | 2026-08-27T15:58:15Z | refine | WI-0001 | Repointed the never-overwrite citation from WI-0001 AC7 to AC9, which is where refine's rewrite of the criteria put it |
| 2 | 2026-08-27T15:52:43Z | answer-questions | EP-001 | Recorded the stakeholder's answers to EP-001/Q-001..Q-004: never overwrite, top-level files only, a Python 3 terminal command, and the delivery order |
| 1 | 2026-08-27T15:45:19Z | intake | EP-001 | First version, from the stakeholder's stated idea |

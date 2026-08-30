---
id: WI-0001
type: work-item
title: Add a card to the deck and have it survive a restart
status: done
priority: high
epic: EP-001
created: "2026-08-30T01:29:59Z"
updated: "2026-08-30T02:17:09Z"
branch: wi/WI-0001
outcome: delivered
---

## Story

As someone building up a deck of things I want to remember, I want to add a card with a question
side and an answer side and find it still there the next time I open the tool, so that the deck
accumulates over weeks instead of being retyped every session.

## Acceptance criteria

Every criterion below is written against the invocation fixed by `ADR-0001`: one executable
named `recall`, with `add` and `list` as subcommands. "The deck file" means the single file
AC7 requires.

- [x] AC1 — `recall add --question "capital of France" --answer "Paris"` exits 0 and adds one
      card. Running `recall list` afterwards shows one more card than it showed before.
- [x] AC2 — `recall add` is refused when either side is missing or blank — `--question`
      omitted, `--answer` omitted, or either given as `""` or as a string of only spaces or
      tabs. In every one of those five cases it writes a message to stderr that names which side
      was missing, exits non-zero, and leaves the deck exactly as it was: `recall list` before
      and after produces byte-identical output.
- [x] AC3 — After `recall add` twice with different cards, `recall list` writes both cards to
      stdout and exits 0. Each card's question side and answer side are both shown, and each is
      shown exactly as it was given — no trimming beyond the blank check in AC2, no case change,
      no truncation.
- [x] AC4 — Persistence across processes, with no save step: run `recall add ...`, let that
      process exit, then run `recall list` as a new process. The card added by the first process
      is in the second process's output.
- [x] AC5 — First run on a machine where the tool has never run: with the deck file absent (and
      its parent directory absent), `recall add --question q --answer a` exits 0 and creates
      both. Nothing has to be created, initialised or configured by hand first.
- [x] AC6 — `recall list` with no cards in the deck writes a line to stdout saying the deck is
      empty and exits 0. It is not an error and it does not print an empty page with no
      explanation.
- [x] AC7 — The deck lives in exactly one file, and that file survives a reboot. Checkable
      without rebooting, by three observations: (a) the project's own documentation states the
      path; (b) after AC1, exactly one file under that path has been created or modified, and it
      contains the card; (c) that path is under the invoking user's home directory and is not
      under `/tmp`, `/var/tmp`, `$TMPDIR`, or any other directory the operating system
      clears at boot.
- [x] AC8 — If the deck file exists but the tool cannot read it as a deck — it is truncated,
      malformed, or not the format the tool writes — then `recall add` and `recall list` both
      write a message to stderr saying so, name the file, and exit non-zero. Neither rewrites,
      truncates or repairs the file: its bytes are identical before and after. The stakeholder's
      stated failure condition is losing progress, so refusing loudly is required and
      silently starting a fresh deck is a defect.
- [x] AC9 — Adding a card whose question side is identical to an existing card's is allowed and
      produces two cards; `recall list` shows both. The deck does not deduplicate and does not
      refuse. (Assumed, not stated by the stakeholder — see `## Notes`.)

## Out of scope

- Editing a card once added. Deleting one is `WI-0004`, not this item.
- Choosing where the deck file lives — a flag, an environment variable, or a config file for
  pointing the tool at a different deck. AC7 fixes that there is one file and that it is durable;
  making it configurable is a separate capability nobody has asked for.
- More than one deck, and anything that lets a person select between decks.
- Anything to do with when a card is next seen: due dates, review sittings and the interval
  ladder are `WI-0002` and `WI-0003`. This item stores the fields they need and reads none of
  them back.
- Card content other than text — images, audio, rich formatting — per the epic.
- Sharing, syncing or backing up the deck file, and any recovery of a deck damaged outside the
  tool. AC8 requires the tool to refuse rather than repair; repairing is nobody's job here.

## Notes

**Where the criteria come from.** `EP-001/Q-002` fixed the interface as a command line and
`ADR-0001` fixed the surface, so AC1 to AC6 now name invocations rather than describing what
must be true. AC7 and AC8 come from the stakeholder's answer to `EP-001/Q-001` — *"don't lose my
progress — that's the one thing that would make this a failure"* and *"Storage should just be a
file on my machine that survives a reboot"*.

**What this item's storage has to carry, though nothing here reads it back.** Per `ADR-0002`, a
card needs a position on the interval ladder and a next-review date, and needs no ease factor. A
new card is due the day it was added. WI-0002 and WI-0003 depend on those fields existing;
discovering them two items later would mean reopening this one.

**Assumptions recorded rather than asked.** Each is reversible, none changes what the tool is
for, and each is in `artifacts/refinement-qa.md` marked `[assumed]`:

- AC9, that duplicate questions are allowed. A personal vocabulary deck legitimately contains
  two cards with the same prompt and different senses, and refusing would be the more surprising
  behaviour. If the stakeholder wants deduplication it is a small change.
- AC2's treatment of a whitespace-only side as blank. The stakeholder asked for a card to have
  two sides; a side of three spaces is not one.
- AC3's requirement that text is returned exactly as given. Nobody asked for normalisation, so
  the safe reading is that the tool does not invent any.

**Open design questions, routed to `plan` rather than to the stakeholder.** Their answer to
`EP-001/Q-001` — *"Storage should just be a file on my machine"* — is a deferral over this whole
category, so these are decided under it and not asked:

- The deck file's format and its exact path. AC7 constrains it to one durable file under the home
  directory and requires the path to be documented; which path and which format is `plan`'s,
  under an ADR.
- The implementation language and runtime, and how `recall` is put on `PATH` so that a
  verifier can run the criteria above literally. `plan` must record this, because every
  criterion here is written as `recall ...`.
- Whether `recall add` also prompts interactively when the options are absent. `ADR-0001`
  leaves this to `plan`; the option form is required either way and is what AC1 and AC2 use.

**Gaps accepted at review, recorded here because nobody reads a verification report after an
item closes.** Each was declared in `artifacts/verify-report.md` `## Not verified, and why`, and
each was judged acceptable rather than a send-back — the reasoning is in `artifacts/review.md`.

- **`python3 -m recall` works but nothing protects it.** `ADR-0005` §3 offers it as a convenience
  and says plainly it is not what the criteria are written against. It was run once by hand
  during verification and exits 0, but no criterion covers it and no test exercises it, so a
  change to `recall/__main__.py` would break it silently. Accepted: adding a criterion is
  `refine`'s work and adding an unrequested test is scope. Whoever next touches the entry points
  should know it is unguarded.
- **`bin/recall` is not covered by `commands.lint`.** The declared command is
  `python3 -m compileall -q recall tests`, and `bin/recall` has no `.py` extension so it is in
  neither directory. Every acceptance check executes it as the child process, so a syntax error
  in it fails everything loudly — but the lint gate does not see it. Accepted as a known
  limitation of the gate, not of the file.
- **Concurrency was never exercised.** Two `recall add` processes writing at once is neither
  specified by any criterion nor excluded by this item. The `os.replace` discipline is about
  *interrupted* writes, not simultaneous ones, and the epic is one person at one terminal.
  Recorded so that nobody later reads a passing AC4 as a statement about concurrent access.

**A defect found during this item, not fixed by it.** `BUG-0001` — a filesystem error on the
deck file that is not a content problem escapes as a Python traceback, and in one of its three
reproductions `recall list` reports an empty deck at exit 0. Filed at `ready` with
`found-in: WI-0001`. No acceptance criterion of this item covers any of the three reproductions,
which is why WI-0001 closes as delivered while the defect stays open.


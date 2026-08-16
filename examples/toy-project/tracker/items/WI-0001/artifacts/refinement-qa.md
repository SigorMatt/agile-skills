# Refinement Q&A — WI-0001

Recorded by `refine` v0.1.1 (product-analyst) on 2026-08-16T21:22:18Z.

Answers are tagged `[human — simulated by the builder]` where the human answered,
`[assumed]` where the analyst proposed something and the human confirmed or deferred, and
`[unresolved]` where a question was asked and not settled. Answers are verbatim; nothing has
been tidied into agreement.

**Note on provenance:** this run is a test of the methodology. Every answer below was produced
by the builder standing in for the human, which is why the tag says so. Nothing here should be
read as the words of a real user.

Questions asked at intake and already answered there are **not** repeated here. They are in
`tracker/items/EP-001/journal.md`: lines versus bytes, non-recursion, a last line with no
trailing newline, an empty file being listed, plain text pipeable into `head`, standard library
only, `python3 linecount.py <folder>`, and failing loudly on a folder that cannot be read.

---

## Round 1 — one batch of six, each tied to a failing DoR criterion

### Q1 — Tie-break (DoR R4, criterion AC2)

> AC2 says rows are ordered by line count, largest first, but not what happens when two files
> have the same count. Proposed default: filename ascending, byte-order (so `A.md` before
> `a.md`), which makes the output stable across runs and across machines. Confirm or name a
> different rule.

**Answer** `[human — simulated by the builder]`:

> Filename ascending, your byte-order rule. I said I didn't care as long as it doesn't shuffle
> between runs, and that gives me that. Yes.

**Effect:** AC2 now carries both halves — the tie-break rule *and* the stability requirement he
restated, which is expressed as a `diff` of two consecutive runs.

### Q2 — Exact output shape, including the empty folder (DoR R4, criteria AC1 and AC3)

> AC1 says each row shows "a line count and the file's name", which fixes neither the column
> order, the separator, nor alignment; AC3 says the output "ends with a total" without fixing
> its label or format. Proposed default, deliberately mirroring `wc -l` since that is the tool
> you are replacing: the count right-aligned in a column as wide as the largest count, two
> spaces, then the bare filename (not the path), e.g. `  128  notes.md`; the last row is the
> total in the same column followed by two spaces and the word `total`. And for a folder
> containing no files at all: print only `    0  total` and exit 0. Alternative if you prefer
> it: print `no files` and exit 0, with no total line. Which?

**Answer** `[human — simulated by the builder]`:

> Your `wc -l`-mirroring default is right — right-aligned count, two spaces, bare filename,
> total in the same column. That's what my eye already expects.
>
> One change: for a folder with no files at all, I don't want `    0  total`. A lonely zero
> looks like the tool broke. Print `no files` and exit 0, your alternative. If that makes the
> "ends with a total" criterion awkward, then say the total row appears when there is at least
> one file — that's what I actually mean.

**Effect:** AC1 fixes the row format with a worked example. AC3 was rewritten in his own terms —
the total row appears **when at least one file is listed**. AC10 is new and covers the empty
folder, including "only subdirectories" as a second way of having no files.

### Q3 — Files that are not text (DoR R4, criterion AC8; the point intake recorded as delegated)

> At intake you said "don't crash, beyond that whatever's sensible — you decide". I need one
> decidable behaviour. Proposed default: every file is read as bytes and its lines counted by
> counting newline bytes (plus one if the last byte is not a newline), so a JPEG or a `.pyc`
> simply gets a number like any other file, nothing is skipped, and no decoding can fail. The
> alternative is to detect such files and list them with a `-` instead of a count, excluded from
> the total. The first is simpler and keeps "one row per file" literally true; the second is
> more honest that the number is meaningless. Which do you want — and if the first, are you
> content that a binary file can show a large, meaningless count?

**Answer** `[human — simulated by the builder]`:

> You decide, honestly. If you're making me pick: the first one — count newline bytes for
> everything, one row per file, nothing skipped. Simpler, and I'd rather have a meaningless
> number than a special case I have to remember. And yes, I'm content that a JPEG can show a big
> number; I'll know why.

**Tag note:** recorded as `[human — simulated by the builder]` and not as `[assumed]`, because he
did pick, and confirmed the consequence when it was named. The hesitation ("You decide,
honestly") is preserved rather than smoothed away: the choice is his, the enthusiasm is not.

**Effect:** the counting rule became AC5 in its own right, since it now governs every file and
not only the awkward ones; AC9 states the observable guarantee for a non-text file, including
that `Traceback` appears nowhere.

### Q4 — The failure path (DoR R4, criterion AC7)

> AC7 says the command "prints a message naming that problem" and exits "non-zero", which leaves
> the stream and the exact code open, so no command settles it. Proposed default: for both a path
> that does not exist and a folder you cannot read, print a single line to **stderr** naming the
> path and the problem (e.g. `linecount: /tmp/nope: no such directory`), print nothing to stdout,
> and exit **2**. Is 2 acceptable, or do you want plain 1? And is stderr right, or do you want
> the message on stdout?

**Answer** `[human — simulated by the builder]`:

> 2 is fine. And yes, stderr — I want to be able to pipe stdout into `head` without an error
> message landing in the middle of it.

**Effect:** AC11. His reason (keeping stdout pipeable) is the same reason recorded in the vision,
so nothing here contradicts `docs/product/vision.md`.

### Q5 — What counts as "a file directly in the folder" (DoR R4, criteria AC1 and AC6)

> Two cases nobody has ruled on. (a) Hidden dotfiles such as `.env` or `.gitignore` — proposed
> default: included, they are files in the folder and you have no ignore patterns. (b) A symlink
> sitting in the folder — proposed default: if it points at a file, count the file it points at;
> if it points at a directory, ignore it exactly as a real subdirectory is ignored; if it is
> broken, ignore it and still exit 0. Confirm both, or change either.

**Answer** `[human — simulated by the builder]`:

> (a) Dotfiles included, yes — they're files in the folder and I didn't ask for ignore patterns.
> (b) Symlinks: don't overthink it. Points at a file, count it. Points at a directory, ignore it
> exactly like a real subdirectory. Broken, ignore it and don't error. Yes to both as you
> proposed.

**Tag:** `[assumed]` — both behaviours were proposed by the analyst and confirmed by the human
rather than originated by him. Recorded as assumptions in the item's `## Notes` accordingly.

**Effect:** AC7 (symlinks) and AC8 (dotfiles).

### Q6 — How the tests are run (DoR R4, criterion AC9)

> AC9 names a property of the test framework but no command, and nothing in the item says the
> tests must run and pass, so there is no observation to make. Proposed default: tests live in
> `tests/` and are run with `python3 -m unittest discover` from the repository root, which needs
> nothing installed. I would also add an acceptance criterion that this command exits 0, so "the
> tests run" is an observation rather than a claim. Agreed, or do you want the tests inside
> `linecount.py` itself / a different invocation?

**Answer** `[human — simulated by the builder]`:

> Agreed: `tests/` and `python3 -m unittest discover` from the repository root. And yes, please
> add the criterion that the command exits 0 — I'd rather "the tests run" was something you can
> show me than something you tell me.

**Effect:** AC13, which is the old AC9 turned into a command with an exit code.

---

## Not put to the human — the analyst's own extension

`[assumed]` — **AC12: the path is a regular file, and no argument at all.** Neither case was
raised at intake or in this round. AC12 extends the human's stated rule for a missing or
unreadable path (stderr, exit 2) to the two remaining ways the invocation can be wrong. It is
recorded here, and in the item's `## Notes`, as the one criterion in WI-0001 the human has not
seen, so that a later disagreement about it lands on the analyst rather than on him.

It was not worth a second round on its own: it is cheap to change, it cannot silently produce a
wrong count, and holding the item at `draft` for it would cost more than reversing it later
would.

---

## Override

None. The human was not asked to override any Definition of Ready criterion, and did not offer
to. Every criterion is recorded as passed in the journal entry for this execution.

---

## Nothing left unresolved

No `[unresolved]` answers. All five open points that intake carried into this item's `## Notes`
are closed above, and the item's `## Notes` now records what was settled, on whose authority.

# Refinement Q&A — WI-0002

Recorded by `refine` v0.1.1 (product-analyst) on 2026-08-16T21:26:30Z.

Answers are tagged `[human — simulated by the builder]` where the human answered, `[assumed]`
where the analyst proposed something and the human confirmed or deferred, and `[unresolved]`
where a question was asked and not settled. Answers are verbatim.

**Note on provenance:** this run is a test of the methodology. Every answer below was produced
by the builder standing in for the human, which is why the tag says so. Nothing here should be
read as the words of a real user.

Questions already answered at intake are not repeated: that `--top N` is wanted, that it is
deliberately a second piece of work, and that it shows only the N largest. They are in
`tracker/items/EP-001/journal.md` under Q7. The row format, the sort order, the failure shape
and the empty-folder behaviour this item builds on were settled while refining WI-0001; see
`tracker/items/WI-0001/artifacts/refinement-qa.md` rather than re-deciding them here.

---

## Round 1 — one batch of six, each tied to a failing DoR criterion

### Q1 — What the total means once the output is limited (DoR R4, criteria AC1 and AC3)

> This is the one intake flagged, and the two readings give different numbers on exactly the
> folders this flag is for. Options: (a) the total stays the sum of **every file in the folder**,
> so adding `--top 3` never changes the number — but the row no longer equals the rows above it,
> which may read as a bug; (b) the total is the sum of **only the rows shown**, so it always adds
> up on screen — but the same word `total` then means something different depending on the flags;
> (c) (a) with the label made explicit, e.g. `1204  total (all 27 files)`. I propose (a): "how
> much is in this folder" is the question the tool answers, and a number that shrinks when you
> ask to see fewer rows is misleading. Which do you want?

**Answer** `[human — simulated by the builder]`:

> I take your point about (a), but not the "reads as a bug" part — I'd definitely wonder why the
> column doesn't add up. So: **(c)**. Keep it the sum of every file in the folder, and label it
> so I can see that's what it is. `1204  total (all 27 files)` is exactly right. When there's no
> `--top`, keep the plain `total` — I don't need it telling me it counted all of them when it
> obviously did.

**Effect:** AC3 (labelled total with `--top`), AC4 (plain `total` without it), AC5 (the label
stays even when N exceeds the file count, because the flag was given). My proposal of (a) was
rejected in favour of (c); recording that, because the analyst's preference losing is exactly
the kind of thing a tidied record hides.

### Q2 — `--top 0`, and bad values (DoR R4, criterion AC4 as intake wrote it)

> Is `--top 0` an error, or a legitimate request that prints no file rows? And for a negative
> number or a non-number, I propose exactly WI-0001's failure shape: nothing on stdout, one line
> on stderr naming the problem, exit 2. Note that AC4 was derived by the analyst at intake from
> your rule about a missing folder — you have not actually said it applies to a bad flag value.
> Confirm or reject it.

**Answer** `[human — simulated by the builder]`:

> Not an error. Zero means "show me nothing", which is a reasonable thing to type, especially
> from a script — print no file rows, but still print the total line, and exit 0. Negative or
> not-a-number: yes, error, exactly WI-0001's shape (nothing on stdout, one line on stderr, exit
> 2). And yes, AC4 as your analyst derived it is what I'd have said if asked.

**Effect:** AC6 (`--top 0` is not an error and still prints the total) and AC7 (negative and
non-numeric values fail in WI-0001's shape). Intake's derived AC4 is now the human's, in his own
words, and is no longer carried as an assumption.

**Consequence worth naming:** AC6 means a total row can print when no file row does. That is
outside WI-0001 AC3's condition ("when at least one file is listed") rather than against it, and
WI-0001 was **not** edited — it is past `ready`, where criteria change only through
`answer-questions` or a send-back. The interaction is recorded in this item's `## Notes`.

### Q3 — Ties at the cut line (DoR R4, criterion AC1)

> Four files with counts 9, 5, 5, 5 and `--top 3`: I propose the list is sorted by WI-0001's rule
> first (count descending, then filename ascending byte order) and the first three rows are
> taken, so the tie-break decides which of the three 5s is dropped and the result is stable
> between runs. Confirm, or say the tool should show all four rather than cut a tie arbitrarily.

**Answer** `[human — simulated by the builder]`:

> Confirmed — sort by the WI-0001 rule, take the first N. I'd rather get exactly the number of
> rows I asked for than have the tool second-guess me.

**Effect:** AC2, with his own fixture shape (9, 5, 5, 5) written into the criterion so a verifier
can build it without inventing one.

### Q4 — Flag position, and a short form (DoR R4; undiscussed at intake)

> I propose both `python3 linecount.py --top 3 notes/` and `python3 linecount.py notes/ --top 3`
> work, since that is what Python's own argument parser does for free, and **no** short `-t` —
> you said you did not want flags to remember, and one spelling is one thing to remember.
> Confirm both halves.

**Answer** `[human — simulated by the builder]`:

> Confirmed both: either position works, and no `-t`. One spelling.

**Tag:** `[assumed]` — both halves were proposed by the analyst and confirmed, not originated by
him.

**Effect:** AC8, which also turns "no short form" into something observable: `-t 3` must fail
with exit 2 rather than merely be undocumented.

### Q5 — `--top N` on a folder with no files (DoR R4; undiscussed at intake)

> I propose it behaves exactly as WI-0001 AC10: prints `no files`, nothing on stderr, exits 0,
> regardless of N. Confirm.

**Answer** `[human — simulated by the builder]`:

> Confirmed — `no files`, exit 0, whatever N is.

**Tag:** `[assumed]` — proposed by the analyst, confirmed by the human.

**Effect:** AC9. It also settles the boundary between AC6 and AC9: `--top 0` prints a total row
only on a folder that has files.

### Q6 — Column width with `--top` (DoR R4, criterion AC1)

> If the total is the all-files total, it can be a wider number than any visible row — e.g. rows
> of 9 and 7 with a total of 1204. I propose the column is sized to the widest number actually
> printed, the total included, so that row still lines up. Confirm, or say you would rather the
> visible rows stay narrow and the total overhang.

**Answer** `[human — simulated by the builder]`:

> Confirmed — size the column to the widest number actually printed, total included, so
> everything lines up.

**Effect:** AC10, with the worked example spelled out space by space.

### Addendum — the test criterion, flagged before it was written

> One thing I will **not** ask about and will simply add, unless you object: a criterion that
> `python3 -m unittest discover` from the repository root still exits 0 after this change,
> matching WI-0001's AC13. I will mark it as analyst-derived in the Q&A.

**Answer** `[human — simulated by the builder]`:

> And yes, add the criterion about `python3 -m unittest discover` still exiting 0. Mark it as
> your own if that's the honest label.

**Tag:** `[assumed]` — the analyst's criterion, put to him with that label and accepted with it.

**Effect:** AC11, which carries the label in the criterion text itself.

---

## Not put to the human — the analyst's own extension

`[assumed]` — **the plural inside the total label.** The human's example was
`total (all 27 files)`. Nothing was decided for a folder holding exactly one file, which under
AC3 as written yields `total (all 1 files)`. Special-casing the singular would be a rule the
criteria then have to state and a verifier then has to check; leaving it uniform is the smaller
invention and is cosmetic to reverse. Recorded here and in `## Notes` so the choice is visible
rather than discovered.

---

## Override

None. No Definition of Ready criterion was waived; the human was not asked to override one and
did not offer to.

---

## Nothing left unresolved

No `[unresolved]` answers. All three open points intake carried into this item's `## Notes` are
closed above — what the total means when the output is limited, whether the derived bad-value
rule reflects the human's intent, and where the flag may sit relative to the folder argument.

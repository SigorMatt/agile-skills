# Refinement Q&A — WI-0003

Recorded by `refine` v0.1.1 (product-analyst) on 2026-08-16T23:58:00Z.

Answers are tagged `[human — simulated by the builder]` where the human answered, `[assumed]`
where the analyst proposed something and the human confirmed or deferred, and `[unresolved]`
where a question was asked and not settled. Answers are verbatim.

**Note on provenance:** this run is a test of the methodology. Every answer below was produced by
the builder standing in for the human, which is why the tag says so. Nothing here should be read
as the words of a real user.

Questions already answered at intake are not repeated: the spelling of the flag and its two
values, `count` as the default, no short form, byte order, ascending only, and that nothing else
about the output changes. They are verbatim in `tracker/items/EP-001/journal.md` under the entry
of 2026-08-16T23:50:12Z. The row format, the sort key, the failure shape, the total row and the
empty-folder answer this item builds on were settled while refining WI-0001 and WI-0002; see
those items' `refinement-qa.md` rather than re-deciding them here.

---

## Round 1 — one batch of six, each tied to a failing DoR criterion

### Q1 — Making the two-folder measure checkable by someone who was not here (R4, AC2)

> AC2 as intake wrote it ends "can be compared row for row by eye", and "by eye" is not something
> `verify` can decide. I propose replacing it with the mechanical version of the same thing:
> build folder A with `notes.md`, `todo.md`, `ideas.md` and folder B with the same three names
> but different contents; `--sort name` on each prints the three names in the same order —
> `ideas.md`, `notes.md`, `todo.md` — in both outputs, and the counts differ. Same measure,
> decidable. Does that still capture what you are actually doing, or is there a case it misses (a
> file present in one folder and not the other — should that just show up as a missing row)?

**Answer** `[human — simulated by the builder]`:

> Yes, that's my case and your version of it is fine — it's the same thing, just written so
> someone else can run it. On a file present in one folder and not the other: a missing row is
> exactly what I'd want to see, that's the whole point. Don't add anything special for it.

**Effect:** AC2 rewritten with the worked example and the fixed expected order. His "don't add
anything special for it" is written into `## Out of scope` as an explicit exclusion, because a
later reader could otherwise reasonably assume the tool should mark or pad an absent name.

### Q2 — What `--sort name` means together with `--top N` (R4, missing criterion)

> You told me to pick. Before I do, here is the pick, once, so you can reject it cheaply. **My
> proposal:** `--top` still means "the N largest" and `--sort` only controls the order they are
> printed in. So on a folder where `big.txt` has 90 lines, `mid.txt` 50 and `apple.md` 3,
> `--top 2 --sort name` prints `big.txt` then `mid.txt` (the two largest, alphabetised), **not**
> `apple.md`. The alternative gives you the alphabetically-first two files, which on most folders
> is three small files and no answer. Confirm, or reject. If you would rather not think about it,
> say so and I record it as `[assumed]` in the Q&A and in `## Notes` — flagged as mine, so when
> you find it wrong the record shows nobody claimed you asked for it.

**Answer** `[unresolved]` — the human was asked, declined to decide, and declined the assumption
route as well. Verbatim `[human — simulated by the builder]`:

> No. I don't want to pick, and I don't want you picking and then writing it down as though it
> were decided — I've seen how that reads six months later. Leave it genuinely open. I'll tell
> you what I want the first time I actually type both flags together, and not before.
>
> And don't hold the item up over it. Mark it Ready and get going on the part I do know I want.
> If that means overriding your checklist, override it — that's my call, isn't it? Note it
> however you need to.

**Effect:** no criterion decides which files `--top N --sort name` selects. The combination is
recorded in `## Notes` as **deliberately undefined at the human's instruction**, with both
readings written out so that whoever eventually asks him can put the same two options to him.
This is the one place where his `[unresolved]` is load-bearing rather than cosmetic, and it is
also the reason AC9 exists — see Q7 below.

His offer to override the checklist is answered in `## The override he offered, and why none is
recorded` at the end of this file. Short version: no Definition of Ready criterion is unmet, so
there is nothing to override, and writing an override anyway would put a false statement in the
permanent record.

### Q3 — What `--sort banana` does, and a bare `--sort` (R4, missing criterion)

> Never asked, and `verify` will need it. Two shapes: (a) we check the value ourselves —
> `linecount: --sort: 'banana' is not name or count` on stderr, nothing on stdout, exit 2, which
> is exactly the shape you approved for `--top -1`; or (b) we let argparse's own `choices` reject
> it, which prints a usage block *plus* the message. ADR-0004 records that we hand-rolled
> `--top`'s check precisely to keep it to one line, so I propose **(a)** for consistency. And
> separately: a bare `--sort` with no value at all stays argparse's error (usage block, exit 2),
> same as we left `-t` to argparse. Agreed?

**Answer** `[human — simulated by the builder]`:

> (a), our own one-line message, consistent with `--top`. And yes, a bare `--sort` with no value
> can stay argparse's problem, same as `-t`.

**Effect:** AC7, in two halves — our one-line rejection for a bad *value*, and argparse's own
error for a *missing* value. The split is his, not a simplification: it keeps the message we
control to one line without making us re-implement what argparse already does correctly.

### Q4 — The one thing that genuinely will change (R4, AC4)

> AC4 says output is byte-identical to today's when `--sort` is absent. That is true for any run
> that names a folder — but the usage line and `--help` will gain `[--sort …]`, so
> `python3 linecount.py` with no arguments will print a different usage string than it does
> today. This is exactly what happened when `--top` was added; review recorded it after the fact.
> I propose writing the exception into AC4 now: byte-identical for every invocation that names a
> folder; the usage/`--help` text is expected to change and that is not a regression. Any
> objection to it changing?

**Answer** `[human — simulated by the builder]`:

> No objection — the usage line changing is fine and obviously unavoidable. Write the exception
> in now rather than having someone rediscover it at review. I'd rather the criterion be true
> than tidy.

**Effect:** AC4 carries the exception in its own text. WI-0002's review had to record this as an
accepted gap after the fact; here it is a stated part of the criterion before any code exists.

### Q5 — Flag position and the `=` form (R4, missing criterion)

> For `--top` you accepted both `--top 3 <folder>` and `<folder> --top 3`. I propose the same for
> `--sort`, plus accepting `--sort=name` (argparse gives that for free; refusing it would cost
> extra code and surprise anyone used to long options). Confirm — and if you want `--sort=name`
> **rejected**, say so now, because that is a criterion someone has to implement deliberately.

**Answer** `[human — simulated by the builder]`:

> Same as `--top`: both positions. And `--sort=name` should work — refusing it would be
> gratuitous.

**Effect:** AC8, covering all three spellings against one another byte for byte.

### Q6 — The test criterion, marked as the analyst's (R4, missing criterion)

> For `--top` you let me add a criterion I derived rather than one you asked for:
> `python3 -m unittest discover`, run from the repository root, exits 0 and the new behaviour is
> covered by tests in `tests/`. I propose the same here, labelled as analyst-derived. Confirm,
> and I'll add it as the last AC.

**Answer** `[human — simulated by the builder]`:

> Confirmed, add it, and label it as yours. I like that you keep telling me which bits I didn't
> actually ask for.

**Effect:** AC10, labelled in its own text as analyst-derived and human-confirmed, exactly as
WI-0002 AC11 is.

---

## Q7 — Not asked: what happens when both flags are given and nothing decides which files

`[assumed]` — proposed by the analyst after the round closed, not put to the human, because he
had just said "don't hold the item up over it".

Q2 leaves *which* files `--top N --sort name` selects undefined. It does not follow that the
combination may do anything at all: both readings of Q2 agree on everything except the selection.
Both print at most N file rows, both exit 0, and both carry WI-0002 AC3's labelled total row. So
AC9 states exactly that shared part and nothing more:

- it does **not** decide which files are selected — the criterion passes under either reading, so
  it takes nothing away from the human's "leave it genuinely open";
- it does stop the undefined combination shipping as a traceback or a non-zero exit, which the
  vision rules out in general terms ("a number, not a stack trace") and which no other criterion
  on this item would catch, since `verify` judges only what is written here.

If the human would rather have nothing at all written about the combination, striking AC9 is a
one-line change and costs only that protection. It is flagged here, in the item's `## Notes`, and
in AC9's own text so that nobody mistakes it for something he asked for.

A related caution, recorded so it is not a surprise later: AC9 makes `verify` *run* the
combination, so the verification report will contain an observation of what the code does when
both flags are given. That observation is a record of current behaviour, not a decision and not a
contract. Nothing downstream may cite it as though the question in Q2 had been settled.

---

## The override he offered, and why none is recorded

The human offered one, in as many words: "If that means overriding your checklist, override it —
that's my call, isn't it? Note it however you need to." It is his call, and if the item needed
one it would be recorded loudly, per `spec/dor-dod.md` §1: a `## Override` section here naming
the unmet criteria and his reason, the unmet criteria copied into the item's `## Notes`, and a
history row whose reason begins `DoR overridden:`.

**No override is recorded, because the Definition of Ready is not failing.** Walking
`spec/dor-dod.md` §1 criterion by criterion against the refined item, R1 through R9 all pass;
the per-criterion evidence is in this execution's journal entry. The `--top` interaction he left
open is not any of those criteria: R4 asks that **every acceptance criterion** be decidable by
observation, and every criterion on this item is. It does not ask that every conceivable
invocation of the tool have a criterion — there is no completeness criterion in the checklist to
fail.

That distinction is the whole reason not to stamp the item "overridden" anyway. The override
record has a mandatory field — *which criteria were not met* — and filling it in here would mean
naming a criterion that is not, in fact, failing. A record that says an item was forced through a
gate it actually passed is not a cautious record; it is a false one, and it would devalue every
genuine override in this repository. The honest artifact is the one that exists: the question
tagged `[unresolved]`, both readings written out, and the risk carried in `## Notes` where
`plan`, `implement` and `verify` will all read it.

What he was protecting against — a decision of the analyst's being written down as though it were
his — has been done as he asked. Nothing in this item says which files `--top N --sort name`
selects.

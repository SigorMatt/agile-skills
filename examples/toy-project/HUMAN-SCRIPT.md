# Human answer key — how the builder played the human

Acceptance C2 requires that the toy run be executed by context-free subagents and that, for
`refine`, "the builder plays the human's role and marks simulated answers as such in the Q&A
record". This file is that role, written **before** the run so the answers were not tuned to
whatever the pipeline happened to produce.

Every answer the pipeline received is tagged `[human — simulated by the builder]` in
`tracker/items/*/artifacts/refinement-qa.md`, and the run's journals say the same. Nothing here
was presented to the skills as a real human's words.

---

## How the role was played

Three standing rules, chosen so that `refine` had something real to do:

1. **Answer the way a person actually answers.** Vague first, specific when pushed. A test where
   the human is a perfectly co-operative oracle tests nothing — the whole point of `refine` is
   that it pushes back.
2. **Push back once, then concede.** When `refine` challenged a vague answer with a concrete
   alternative, the human took it. That is the realistic case and it is the one the skill is
   designed for.
3. **Refuse to decide one thing.** For at least one question, the human answers "you decide, I
   don't care" — so that the pipeline has to record an assumption rather than a requirement, and
   the record has to distinguish the two.

Anything asked that is not anticipated below was answered in the same spirit, and the actual
exchange — questions and answers, in order — is in the item's `refinement-qa.md`, which is the
authoritative record. This file is the intent; that file is what happened.

---

## The answer key

### About the goal

**Who is this for, and what do you do today instead?**
> Me, and anyone who inherits a folder of notes or source and wants a feel for it. Today I run
> `wc -l *` and squint, or open things at random.

**What does success look like from outside the tool?**
> I run one command on a folder and immediately see which two or three files are the big ones,
> without reading any of them.

**What would make this a failure even if it worked?**
> If I have to pass three flags to get the obvious output. And if it chokes on a folder that has
> something weird in it — I want a number, not a stack trace.

### About "how much is in each file"

**Lines, bytes, words, or something else?**
> Lines. That's what I mean by how much.

**What is a line, exactly? Does a last line without a trailing newline count?**
> …I hadn't thought about it. Yes, count it — if there's text there, it's a line.

**What about a completely empty file?**
> Zero. And it should still be listed, not skipped.

### About "a folder"

**Do you want subdirectories included?**
> Not for now. Just the files directly in the folder I point at. Maybe later.

**What should happen with a subdirectory that is in there?**
> Ignore it. Don't count it, don't error.

**What about files that aren't text — an image, a binary?**
> Hmm. Don't crash. Beyond that, whatever's sensible.
> *(This is the deliberate "you decide" — the pipeline must record an assumption, not invent a
> requirement.)*

**What if the folder doesn't exist, or I don't have permission?**
> Say so clearly and exit with a non-zero status, so I notice in a script.

### About the output

**What does the output look like?**
> One row per file: the count and the filename. Biggest first — that's the whole point.

**Two files with the same count — which comes first?**
> Doesn't matter to me. Just be consistent, don't shuffle between runs.

**Do you want a total?**
> Yes, a total at the bottom. That's useful.

**Anything else on the output?**
> No. Plain text I can pipe into `head`.

### About scope — "nothing fancy"

**What does "nothing fancy" rule out?**
> No colours, no config file, no ignore patterns, no git awareness. Not a TUI. If I want any of
> that I'll ask later.

**Is a `--top N` flag fancy?**
> No, that one's genuinely useful — I nearly always want the top few. Put it in, but as a second
> piece of work, after the basic thing works.

### About the project itself

**Language, layout, tests?**
> Python 3, standard library only, no dependencies. Tests with whatever's built in — `unittest`
> is fine, I don't want to install anything to run them.

**Where does it live and how do I run it?**
> A single `linecount.py` at the top of the repo is fine. `python3 linecount.py <folder>`.

### If asked to override the Definition of Ready

> No. Take the time and get the criteria right — that's the part I care about.

*(The override path is therefore **not** exercised in this run. It is exercised in
`fixtures/broken-workspace/`? No — it is not exercised anywhere, and that gap is recorded as a
known weakness in `meta/FINAL-REPORT.md` rather than being papered over here.)*

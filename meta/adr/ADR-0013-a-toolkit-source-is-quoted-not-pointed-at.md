# ADR-0013 — A toolkit source is quoted and attributed, not pointed at

- **Status:** accepted
- **Date:** 2026-09-11
- **Unit:** META-169
- **Amends:** `spec/doc-header.md` §4a's **citation forms table**, which has been silent on
  installed-toolkit paths since it was written and let them through by accident — the body
  contains a `/`, so it fell into the workspace-path branch and was answered by `os.path.exists`.
  The table gains one row (`toolkit:`) and one refusal
  (`claim.citation.outside-the-record`). Nothing already written becomes invalid: §4a's own rule
  — *"A record written before this convention existed is not retroactively invalid"* — applies to
  this convention as it does to every other, and the twelve standing instances live in
  `meta/harness/evidence/`, which is read-only history.
- **Findings:** **F-114**'s Direction half (*"the forms table should additionally state whether
  installed-toolkit paths are a legal form … legal-and-pinned, or illegal-and-quoted, but not
  accidental"*). F-114's **placement** half — whether the authoring skills surface the grammar —
  is **not** decided here and remains open. Touches **F-098** (§6), **F-077** (§4), **F-050**
  (§5), **F-113**/**F-075** (the severity split this refusal sits beside), **F-041** (the
  git-ignored-file exclusion this generalises from).

## Context

`[src: .claude/agile-skills/spec/dor-dod.md]` resolves today. It resolves because the resolver
takes everything before the first `:` as a candidate path, sees a `/` in it, and asks
`os.path.exists` — nothing in the convention ever decided that pointing into the installed
toolkit was a legal thing to do. Twelve citations of exactly that shape stand in a real run:

```
[src: .claude/agile-skills/spec/dor-dod.md; .claude/agile-skills/spec/doc-header.md]
[src: .claude/agile-skills/pipeline.yaml]
[src: .claude/agile-skills/scripts/lib/claims.py:148]
[src: .claude/skills/answer-questions/SKILL.md]
```

They are in `docs/process/ways-of-working.md` and `tracker/items/WI-0002/questions/Q-004.md` of
iteration 5, banked at `meta/harness/evidence/iteration-5-envel-abandoned/`. They were not
careless. The run's own record says why they were written: the paragraph carried an absolute,
`lint-claims` rule 2 demanded a source for it, and the writer sourced the rule it was obeying to
the file the rule is written in. That is the right instinct. The form was the only thing wrong
with it, and the form was never ruled on.

So the question is not *were these authors careless* but *what should a record say when the thing
it is quoting is the toolkit running it*. Five forces answer it, and all five were checked against
the code rather than assumed.

## 1. The record's own walk says where the record ends

`validate-workspace.check_claim_citations` walks the workspace for every `*.md` it will read, and
prunes four directories:

```python
dirs[:] = [entry for entry in dirs if entry not in PRUNED_DIRS]   # (".git", "__pycache__", ".claude", "node_modules")
```

`lint-claims.all_markdown` — the gate half of the same rule — pruned the identical four, written
out a second time by hand. By the tool's own definition the installed toolkit is **not part of the
record**. A citation may not point where the record does not go: if the walk will not open the
directory, the citation names something the tool has decided it does not read, and the only
question `os.path.exists` can answer there is a question about the machine.

This is `F-041`'s argument one step out. F-041 established that a **git-ignored** file is not part
of the record and may not be held to the citation rule; the same sentence, read from the other
end, says that a file the record walk prunes may not be cited *by* the record.

## 2. The consequence is demonstrable, not theoretical

`meta/harness/evidence/iteration-5-envel-abandoned/` is that workspace as it stood at the stop.
`.claude/` was never banked with it — because it is the toolkit and not the project. Running the
validator over the banked record, as any reader who receives it would:

```
$ python3 scripts/validate-workspace meta/harness/evidence/iteration-5-envel-abandoned
docs/process/ways-of-working.md:27: ERROR [claim.citation.unresolved] '.claude/agile-skills/spec/doc-header.md' does not exist in this workspace
docs/process/ways-of-working.md:27: ERROR [claim.citation.unresolved] '.claude/agile-skills/spec/dor-dod.md' does not exist in this workspace
docs/process/ways-of-working.md:38: ERROR [claim.citation.unresolved] '.claude/agile-skills/pipeline.yaml' does not exist in this workspace
docs/process/ways-of-working.md:38: ERROR [claim.citation.unresolved] '.claude/agile-skills/spec/doc-header.md' does not exist in this workspace
docs/process/ways-of-working.md:62: ERROR [claim.citation.unresolved] '.claude/agile-skills/scripts/lib/claims.py' does not exist in this workspace
docs/process/ways-of-working.md:74: ERROR [claim.citation.unresolved] '.claude/agile-skills/pipeline.yaml' does not exist in this workspace
docs/process/ways-of-working.md:85: ERROR [claim.citation.unresolved] '.claude/agile-skills/spec/dor-dod.md' does not exist in this workspace
docs/process/ways-of-working.md:94: ERROR [claim.citation.unresolved] '.claude/skills/answer-questions/SKILL.md' does not exist in this workspace
docs/process/ways-of-working.md:98: ERROR [claim.citation.unresolved] '.claude/agile-skills/spec/dor-dod.md' does not exist in this workspace
docs/process/ways-of-working.md:99: ERROR [claim.citation.unresolved] '.claude/agile-skills/pipeline.yaml' does not exist in this workspace
tracker/items/WI-0002/questions/Q-004.md:214: ERROR [claim.citation.unresolved] '.claude/agile-skills/spec/dor-dod.md' does not exist in this workspace
tracker/items/WI-0002/questions/Q-004.md:215: ERROR [claim.citation.unresolved] '.claude/agile-skills/pipeline.yaml' does not exist in this workspace
```

Twelve for twelve. Every one of them resolved on the machine they were written on and none of them
resolves anywhere else. A citation whose truth depends on an install-local, git-ignored directory
is not evidence a reader can check — it is the appearance of evidence, which §4a already calls
worse than none.

The dates make the point sharper than a hypothetical could: `Q-004.md:215` states, in the record,
*"Both citations resolve to files in the workspace."* It was true when it was written and it is
false in the banked copy of the same file.

## 3. Pinning the version is the retroactive-invalidation trap

The obvious alternative is to make the pointer honest by pinning what it points into —
`[src: .claude/agile-skills/spec/dor-dod.md@0.10.0]`, with resolution checking the pin. It fails
on §4a's own standing rule, quoted from the section this ADR amends:

> A record written before this convention existed is not retroactively invalid; the next execution
> that edits a document is the one that must source what it writes.

A version pin inverts that. The toolkit upgrades on a schedule nobody in the consumer's record
controls, and on the first upgrade every standing pinned citation in the whole engagement begins
to fail — a record that was correct when written becomes a gate failure because something outside
it moved. That is precisely the shape §4a forbids, and it is worse than the shape §4a forbids,
because here the invalidation is *automatic and recurring* rather than one-off.

The same argument was already run, and lost, at a smaller scale: requiring an acceptance-criterion
anchor everywhere was measured at 84 retroactively-invalidated citations and rejected for this
reason (§4a, *"A criterion's number is a position, not a name"*).

## 4. `claims.py:148` is F-077's disease with F-077's cure unavailable

One of the twelve is a line number: `[src: .claude/agile-skills/scripts/lib/claims.py:148]`,
supporting the sentence *"the test asks whether the token contains `/`"*.

It was true. At `181e69d`, the toolkit revision installed when that run executed, line 148 of
`scripts/lib/claims.py` was:

```python
    if PATH_RE.match(token) or "/" in token:
```

Two toolkit commits later — `cd00504` and `656b6c5`, neither of which the consumer's record had any
part in — line 148 is a blank line inside `normalise_anchor()`, and the test the citation was
about has moved to line 223. The citation is now false. Nothing said so, because nothing could.

F-077 fixed exactly this class for workspace paths: a `path:line` citation is bounded by the file's
length, so a pointer past the end stops resolving. **That cure is not available here.** The bound
would be a bound on the *toolkit's* file, which is (a) not in the record, (b) 545 lines long, so
148 is comfortably inside it and the bound reports success, and (c) a different file from the one
the citation was written against. A bound on the wrong file is not a weaker check than F-077's; it
is a check of something else.

## 5. And the claim being made is real — so a refusal alone would be the F-050 mistake

Every one of the twelve supports a sentence worth sourcing: *"an accepted gap is dispatchable or it
is nothing"*, *"filing one is a move the transition table provides"*, *"widening them hides the
change from the board"*. These are absolutes about named things, and `lint-claims` rule 2 will
demand a citation for each — the run's own record shows the gate doing exactly that, and shows the
author adding the citations in response.

**F-050** is the finding for a rule whose satisfying move does not exist: there, an epic-level
question could legally be marked `deferred` and no legal transition could then repair the
workspace. A rule nobody can satisfy is not a rule. Refusing the toolkit path without providing a
legal way to source a claim about the toolkit would reproduce that exactly — rule 2 demands a
citation, and no form would be able to carry one.

That is why the ruling has two halves.

## Decision

**Illegal as a path; legal as a quote.**

**(a) Refused.** A citation body that resolves inside a directory the record walk prunes is an
**error**, `claim.citation.outside-the-record`. It is an error and not META-168's warning because
the two situations are different in exactly the way META-168's split turns on: an unrecognised
marker is a warning because the gate cannot tell a mention of a form from a typo in a citation and
declines to rule on something it has not checked. Here it has checked, it knows precisely what is
wrong, and it knows what to write instead. There is no ambiguity to be honest about.

The test is **generalised, not hand-written for `.claude`.** `claims.PRUNED_DIRS` holds the four
directories once; `validate-workspace.check_claim_citations` and `lint-claims.all_markdown` both
read it for their walks, and `CitationResolver._resolve` reads it for the refusal. Three sites, one
tuple. The alternative — naming `.claude` a second time inside the resolver — makes the rule and
the exclusion two facts that must be kept equal by hand, and they were *already* two hand-written
copies before this change, which is the drift starting rather than a risk of it. Any segment at any
depth counts, because `os.walk` prunes the directory wherever it appears.

**(b) The replacement.** A new citation form:

```
[src: toolkit: <document> <section> "<quoted words>"]
```

- `<document>` — how the toolkit document names itself: `doc-header.md`, `pipeline.yaml`,
  `answer-questions/SKILL.md`. **Never resolved against the filesystem.** That is the point, not a
  weakness: §3 is why nothing may be looked up.
- `<section>` — `§4a`, a heading, or an identifier; whatever names the place inside that document.
- `"<quoted words>"` — **mandatory and non-empty**. Like the acceptance-criterion anchor, it may
  contain neither `]` (it ends the marker) nor `;` (it separates sources).

It **resolves when the shape is complete**. Naming the form is enough to make a body a citation
rather than a mention of one, so an incomplete `toolkit:` body is an ERROR with a message saying
what is missing — the same treatment `run:` gets, and for the reason F-070 gives: the form that
carries the most evidence is the one a vague failure message drives authors away from.

## Consequences

**What this checks, said plainly.** The gate **cannot** tell whether the toolkit really says those
words. Nothing is opened. What it checks is that the citation carries enough for a **reader** to
check it: which document, which section, and the words claimed. A writer who invents a quotation
will pass this gate.

**And that is strictly more than the path form carried.** `[src: .claude/agile-skills/spec/dor-dod.md]`
was checked by `os.path.exists` inside a directory the record walk prunes. It verified that the
writer's own installation had a file at that path — a fact about the writer's machine — and it
carried **no** information about what that file says. A reader who received the record could not
follow it at all (§2). The quote form gives that reader the claim itself and the place to look; the
path form gave them a broken pointer. Both are uncheckable by the gate; only one is checkable by a
person.

**One marker may carry two toolkit sources.** Verified by execution rather than asserted:
`split_sources("toolkit: doc-header.md §4a \"a\"; toolkit: pipeline.yaml steps \"b\"")` returns two
parts. A `run:` source swallows every remaining semicolon in the marker, deliberately (F-070), and
`toolkit:` does **not** — which is what the no-`;` rule on the quote buys. A `;` inside a quote
splits the source in two and both halves fail, loudly, at the marker that contains it.

**The twelve standing citations are not repaired.** They are in `meta/harness/evidence/`, which is
read-only history, and §4a's non-retroactivity rule covers them. This ruling governs what is
written next.

**The toolkit's own `check` is unaffected by its own rule.** This repository cites its own files by
workspace path (`scripts/lib/claims.py:148`), which is correct: here the toolkit *is* the
workspace, and the walk does go there. The refusal fires on `.claude/…` — the toolkit as
**installed into somebody else's** workspace.

## 6. Relationship to F-098, which this does not fix

F-098 asks, in its Direction, for exactly this mechanism in a wider setting: *"give the toolkit's
own decisions a distinguishable citation form in the prose a consumer's workers copy from — a
prefix, or the path."* The `toolkit:` prefix **is** that mechanism, and a consumer citing
`[src: toolkit: ADR-0012 §2 "…"]` can no longer collide with its own ADR-0012.

F-098 is **not resolved here** and its status is not touched by this unit. Its own triage prices it
at **97** bare `ADR-nnnn` citations across 11 numbers in the shipped prose, which must move in one
sweep — doing part of it leaves two conventions in the text a worker copies from, which is worse
than one wrong one. This ADR supplies the form that sweep would use.

## Enforcement boundary — what a script can decide, and what stays judgement

| # | Obligation | `[auto]` | `[skill]` | Neither, today |
|---|-----------|---------|-----------|----------------|
| 1 | A citation does not point into a pruned directory | ✅ `CitationResolver._resolve` reads `PRUNED_DIRS`, the same tuple both walks read | — | — |
| 2 | The rule and the exclusion name the same directories | ✅ structurally — one tuple, three readers; there is no second copy to drift | — | — |
| 3 | A `toolkit:` citation is well-formed | ✅ `TOOLKIT_RE` plus the non-empty-quote check; an incomplete body is an ERROR naming what is missing | — | — |
| 4 | The toolkit actually says the quoted words | — | ✅ the writer quoting them, and `review-close` step 9a opening what a claim cites | ⚠️ **the honest gap, and it is the same one the anchor form has.** Nothing here opens the toolkit. Stated in §4a rather than left to be discovered |
| 5 | The right document and section are named | — | ✅ the writer | ⚠️ a wrong `§` with a real quote passes. The quote is what a reader searches on, so the cost is a slower lookup, not a false claim |
| 6 | A quote containing `;` is caught | ✅ by construction — `split_sources` splits it and both halves fail the shape check | — | — |
| 7 | The standing twelve are not retroactively failed | ✅ they are in `meta/harness/evidence/`, which no gate walks as a workspace | — | ⚠️ a future consumer upgrading mid-engagement gets the new refusal on old records. §4a's non-retroactivity paragraph is the instruction; nothing enforces it |

Four of seven are decidable, two are judgement, and obligation 4 is the one to be honest about:
this form buys **reader-checkability**, not gate-checkability, and it buys it from a form that had
neither.

## Alternatives rejected

- **Leave it legal, as it is today.** The status quo is not a decision anybody made — it is the
  workspace-path branch catching a body that happens to contain a `/`. It ships a citation form
  whose truth is install-local, and §2 measures the cost at twelve out of twelve.
- **Legal, with a version pin (`…@0.10.0`).** §3. It makes every toolkit upgrade retroactively
  invalidate the standing record, which is the one thing §4a's own text forbids, on a recurring
  schedule.
- **Legal, and copy the cited toolkit file into the workspace.** Then the citation resolves and the
  record is self-contained. Rejected: it duplicates the toolkit into every consumer repository,
  where it goes stale silently and where a reader cannot tell the copy from the original. It also
  makes `docs/` a place the toolkit lives, which `workspace-layout.md` does not say.
- **Refuse the path and add no replacement.** The F-050 mistake, in §5: rule 2 demands a citation
  for a sentence about the toolkit and no form would be able to carry one. The refusal is only
  legitimate because it arrives with the form that satisfies the same rule.
- **A warning rather than an error.** Consistent with META-168 at first glance, and wrong for
  META-168's own reason. That split is about what the gate *knows*: a marker matching no form is a
  warning because the gate cannot distinguish a mention from a typo. Here it has looked, it has
  matched, and it knows the replacement — a warning would be the gate hedging about something it
  has decided.
- **Hand-write `.claude` in the resolver and leave the walks as they were.** Smaller, and it is the
  drift this repository has already paid for elsewhere: the four directories were written out twice
  by hand before this change. A third copy, in the rule that depends on the other two being right,
  is the version of this defect that is hardest to see — the resolver would go on refusing
  `.claude` after somebody added a fifth directory to the walks.
- **Resolve the `toolkit:` form against the installed toolkit when one is present.** Tempting: the
  gate usually *is* running with the toolkit installed, so it could check the quote for real.
  Rejected because it makes the verdict depend on the machine — the same defect the path form has,
  reintroduced one level up. A record must validate identically wherever it is read, and a rule
  that is stricter on the author's laptop than in the reader's checkout is a rule that fails only
  where nobody is looking.
- **Require a `toolkit:` citation to name a line number.** It reads as more precise. §4 is the
  answer: a line number into a file that upgrades is F-077's disease with no bound available, and
  the one instance among the twelve is already false.

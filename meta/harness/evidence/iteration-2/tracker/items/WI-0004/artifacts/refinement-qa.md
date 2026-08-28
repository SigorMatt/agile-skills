---
status: recorded
---

# Refinement Q&A — WI-0004

**The round 1 exchange has happened, and this file is now a record.** It was written as an
agenda — the stakeholder is asynchronous and answers in files between runs, so `refine` filed
`questions/Q-001.md`, suspended the item at `awaiting-answer` and wrote down what it would ask
before it could ask it. The answer arrived on 2026-08-28 and `answer-questions` has written it
into the round 1 slot below, verbatim, and moved `status:` from `agenda` to `recorded`
[src: WI-0004/Q-001]. Definition of Ready R8 reads that field
[src: .claude/agile-skills/spec/dor-dod.md]; it now says what actually happened. R8 passing does
not make the item Ready — **R4 still fails**, because the criteria have not been rewritten against
the location the stakeholder picked. That rewrite is round 2's and is specified at the foot of
this file.

Everything decided without asking is tagged `[assumed]` below and names the standing delegation it
rests on, so a reader can tell our decisions from theirs.

## The agenda — which Definition of Ready criteria failed, and why

Built before anything was asked, per the procedure. This item arrived at `draft` from
`answer-questions` rather than from `intake`, and its own preamble says its criteria are rough
and expects the rewrite [src: WI-0004].

| # | verdict | why |
|---|---------|-----|
| R1 | pass | frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: medium`, and `arose-from: EP-001/Q-005` resolves |
| R2 | pass | "As someone who has written a rule file and wants it used every time, I want `tidy` to find that file on its own, so that I do not have to type `--rules PATH` on every run" — role, capability, outcome |
| R3 | pass | AC1–AC6 exist, labelled, as checkboxes |
| R4 | **fail** | every criterion turns on "the default location", and there is no such place. AC1, AC2, AC3 and AC5 cannot be run by someone with a terminal until it is named, and AC4 ("a run says which rule file it used") states no observable. Not closable by us: *where* the file lives is the stakeholder's decision, which is Q-001 |
| R5 | pass | `## Out of scope` names five things, including the two the stakeholder declined by name at sign-off |
| R6 | **fail once Q-001 is filed** | Q-001 is blocking and open. It closes when the answer arrives and `answer-questions` propagates it |
| R7 | pass | `depends-on` is empty; `relates-to: WI-0003`, which is `done` and merged. Nothing sequences this item behind anything |
| R8 | **fail** | this file declares `status: agenda`, which is the honest state: the exchange has not happened |
| R9 | pass | one coherent change: one more source for a `Ruleset` that is already a value passed into the planner [src: ADR-0011], plus the line that says which source was used. Not a split candidate — a "find the file" item and a "say which file" item would each be half a behaviour, and the second exists only to make the first safe |
| R10 | **fail** | the item introduces one new axis — a rule file that was not named on the command line — and the combinations are unstated. Recorded in the item's `## Notes` as far as they can be before Q-001 is answered; the rest lands in the round 2 rewrite |

**That table is round 1's verdict and is left as it was written.** Two of its rows have since
changed, and the change is the stakeholder's answer rather than any work on the item: **R6 now
passes** — Q-001 is `answered`, not open — and **R8 now passes**, because the exchange happened and
this file records it. **R4 and R10 still fail**, and closing them is round 2's job: the criteria
have to be rewritten against a config-directory default, and the four combination rows the item's
`## Notes` marks open have to be stated [src: WI-0004/Q-001].

## The triage — who each gap is for

Applied in the procedure's order: product stake, then already-answered, then a standing deferral,
then implementation-only.

**Put to the stakeholder — 1 question, filed as `Q-001`, and that is the whole ask for this
round.**

1. **Where does the tool look for the rule file it was not told about?** → Q-001. Product stake,
   and not close: the two real candidates differ in whether a folder somebody else handed you can
   change what happens to your files. That is the same instinct as the never-overwrite rule they
   called the one thing they actually cared about [src: EP-001/Q-002], so it is theirs to settle
   rather than ours to infer. It is also the thing ADR-0010 weighed and decided the other way
   [src: ADR-0010], which makes it exactly the class `spec/question.md` §4 reserves for the human.

**Not asked — decided here under the standing delegation.** At intake the stakeholder answered
the whole category of how the thing is built with *"Whatever's easiest for you to build and test
— you know this better than me"* [src: EP-001/Q-001]. That is a real answer and it applies to the
category, not only to the question that produced it. Asking again would tell them their answer was
not heard (F-023).

- **`[assumed]` — `--rules PATH` beats the default location when both exist.** An explicit
  argument beating an implicit default is universal and the answer would be the same whoever the
  stakeholder is. Already AC3; the round 2 rewrite makes it observable rather than asserted.
- **`[assumed]` — a rule file found at the default location is rejected exactly as one named with
  `--rules` is: one line on stderr, nothing on stdout, non-zero exit, nothing moved.** Rests on
  two recorded things rather than on taste: WI-0003 AC8 already fixes that shape for a malformed
  rule file [src: WI-0003 AC8], and the alternative — ignore the broken file and quietly sort with
  the built-in tables — is a run doing something other than what the user's own rule file says,
  which is the surprise this product exists to not have [src: docs/product/vision.md]. It is named
  in the item's `## Notes` as the assumption most likely to be worth revisiting, because a typo in
  a config file that stops every run is a real cost.
- **`[assumed]` — a run states which rule file it used, and that statement is part of what the
  preview shows.** Not a feature we invented: it is the answer to the one cost ADR-0010 named when
  it rejected a default location — "a file can change what a run does without appearing anywhere
  the user looked" [src: ADR-0010]. The stakeholder has reversed the decision; the objection does
  not disappear with it, and this is what neutralises it. The *wording* of the line is `plan`'s,
  under the same delegation.
- **`[assumed]` — the exact filename and path spelling of whatever location Q-001 picks is ours.**
  Q-001 asks which *kind* of place, not what to call the file, and offers a concrete spelling for
  each option only so the answer is easy to picture.

**Not asked — already answered, and re-asking would be the failure the procedure names.**

- Subfolder recursion and undo: declined by name at sign-off, in the same answer that asked for
  this item [src: EP-001/Q-005]. Both are on this item's `## Out of scope` list.
- What a rule file may contain — layering with the user's entries winning, and exactly two bands
  [src: WI-0003/Q-001; src: WI-0003/Q-002]. This item changes where the file is found, not what it
  can say.

**Routed to `plan`, not to a person.** In the item's `## Notes`: whether `--rules ""` falls back
to the default location or means "no rules" [src: tracker/items/WI-0003/item.md]; whether the
default file is read before or after the target folder is checked, and therefore which error a
run with both problems reports; and the wording of the line that names the rule file in use.

## Round 1 — the ask

**Q-001 — Where should `tidy` look for a rule file it was not told about?** Filed
2026-08-28, blocking, addressed to the human. Full context, three options and a recommendation are
in `../questions/Q-001.md`.

**Answer, 2026-08-28, verbatim:**

> [human] B. My own file, not one sitting in the folder — I don't want rules riding along in a
> folder someone hands me. Go with your recommendation.

**Option B: the user's own config directory.** One rule file that belongs to the person, applying
to every folder they tidy. A file sitting *in* a target folder is explicitly not it — they gave
the reason themselves, and it is the same instinct the triage predicted: rules must not ride along
in a folder somebody else handed them. Option C, both places with the folder's file first, is
therefore not built either; it was the option that kept the thing they rejected.

Two of the four `[assumed]` decisions above are confirmed by the reply rather than merely
undisturbed by it: `--rules PATH` beating the default is what makes their one file overridable at
all, and the run naming the file it used is what stops that one file being invisible. The exact
filename and path spelling stay ours, as the question said they would.

## Round 2, 2026-08-28 — no question asked, and why

**Nothing was put to the stakeholder this round.** The procedure's triage was applied again to
what the answer left open, and every item of it failed the first test — product stake — and was
caught by the third: a standing deferral covers it.

- **Where in the config directory, and under what name.** `[assumed]` — `D` is
  `$XDG_CONFIG_HOME/tidy/rules.ini` when that variable is set and non-empty, and
  `<home>/.config/tidy/rules.ini` otherwise. Rests on *"Whatever's easiest for you to build and
  test — you know this better than me"* [src: EP-001/Q-001], and Q-001 said in terms that the
  filename and spelling stayed ours [src: WI-0004/Q-001]. Honouring `XDG_CONFIG_HOME` is the
  standard way of locating a config directory on the platform this tool runs on, and — the reason
  that actually decided it — it is what lets every criterion be run against a temporary directory
  instead of the machine's real home. That is "easiest to test" almost literally.
- **Which stream the line naming the rule file goes to.** `[assumed]` — stderr, before the
  per-file lines, both modes (AC4). Not taste: `cli.py`'s stdout is one line per file and nothing
  else [src: tidy/cli.py], and WI-0003 AC1 compares stdout byte-for-byte [src: WI-0003 AC1], so
  stdout is not available for it. The banner is already on stderr and this line sits with it.
- **Whether a run that used no rule file says so.** `[assumed]` — it says nothing. The line exists
  to make a file the user did not name *visible* [src: ADR-0010]; on a run with no rule file there
  is nothing hidden to reveal, and printing on every run would change what WI-0003 AC1 observes for
  no gain the stakeholder asked for.
- **An unreadable file at `D`.** `[assumed]` — exit 2, same as a malformed one (AC6). This extends
  round 1's assumption rather than adding a new one, and it is the same assumption round 1 flagged
  as the one most worth revisiting: a file the user cannot read stops every run until they fix it.
  Taken for round 1's reason — the alternative is a run quietly sorting by rules the user did not
  write [src: docs/product/vision.md] — and recorded again here so a reader meets the cost twice.
- **An empty file at `D`.** `[assumed]` — loaded successfully, changes no sorting, and AC4's line
  still names it (AC7). "Was a file read?" and "did it change anything?" are different questions
  and the output answers both honestly.
- **`--help`.** `[assumed]` — in scope, as AC10. Its `--rules` text and its epilog both state
  "there is no default location" today [src: tidy/cli.py]. BUG-0003 was filed once already against
  exactly this — help text describing the tool as it was before an item landed [src: BUG-0003] — so
  leaving it to be noticed later is a known, repeated failure rather than a hypothetical one.

**Not asked, because they already answered it:** where the file lives (Q-001, this round's input);
subfolder recursion and undo [src: EP-001/Q-005]; what a rule file may contain
[src: WI-0003/Q-001; src: WI-0003/Q-002].

**Still routed to `plan`, not to a person:** what `--rules ""` does now that `D` exists, and which
error wins when both the rule file and the target folder are unusable. Both are in the item's
`## Notes` and neither is depended on by any criterion.

**`[unresolved]`: none.** Nothing was asked this round and left unsettled.

## What round 2 did — checked against what round 1 said it would

Round 1 wrote the job down so that this execution could not reinterpret it. Against that list:

- *"rewrite AC1–AC6 against the location the stakeholder picks, so that each names a command and a
  verdict"* — done; AC1–AC10 replace them, and the head of the criteria section fixes `TOOL`,
  `PREVIEW`, `APPLY`, `S`, `F1`/`F3`/`F4` and `D` once, in one place, rather than in each criterion
  [src: WI-0004].
- *"add the boundary cases the current criteria only gesture at (the file exists but is empty; the
  file exists and is unreadable; `--rules` and the default file both present; neither present)"* —
  AC7, AC6, AC3, AC2 respectively.
- *"complete the R10 combination table in `## Notes`"* — done; four rows closed, four added, two
  left deliberately unconstrained with `plan` named as their owner.

Two things round 1 did not foresee were added: AC10, because `--help` says there is no default
location and BUG-0003 is the precedent for that going stale [src: BUG-0003]; and the design point
in `## Notes` that `ruleset_file.load` raises the same exception for a missing file and an
unreadable one [src: tidy/ruleset_file.py], which AC2 and AC6 require to be told apart.

## What round 1 said round 2 would do

Kept verbatim, as the instruction this round was measured against:

Named now so that the next execution is not free to reinterpret the job: rewrite AC1–AC6 against
the location the stakeholder picks, so that each names a command and a verdict; add the boundary
cases the current criteria only gesture at (the file exists but is empty; the file exists and is
unreadable; `--rules` and the default file both present; neither present); and complete the R10
combination table in `## Notes`. Nothing in that list needs the stakeholder again unless their
answer opens something new.

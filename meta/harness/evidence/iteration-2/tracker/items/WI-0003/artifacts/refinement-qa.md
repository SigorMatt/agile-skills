---
status: recorded
---

# Refinement Q&A — WI-0003

**This is the record of what was said.** Two rounds. Round 1 put two questions to the
stakeholder and both were answered; their replies are below, verbatim, as they wrote them. Round 2
is `refine` closing the remaining Definition of Ready gaps without asking them anything further —
every decision in it is tagged `[assumed]` and names the standing delegation or the delivered
criterion it rests on, so a reader can tell at a glance which lines are the stakeholder's and
which are ours.

Nothing here is paraphrased into agreement. Note in particular R2.4, where `refine` narrowed what
a rule file may express without asking: it is marked as an assumption, not a decision, and it is
on the item's `## Out of scope` list where the stakeholder can see it and object.

## The agenda — which Definition of Ready criteria failed, and why

Built before anything was asked, per the procedure. R1, R2, R3, R5, R6, R7 and R9 passed as the
item stood; R4, R8 and R10 failed. All three are closed below — R4 and R10 by round 2's rewrite,
R8 by this file reaching `status: recorded`.

| # | verdict | why |
|---|---------|-----|
| R1 | pass | frontmatter complete; `type: work-item`, `epic: EP-001`, `priority: low` all set |
| R2 | pass | "As someone whose folder does not look like anybody else's, I want to write my own rules for where files go, so that the tool sorts my files the way I want" — role, capability, outcome |
| R3 | pass | AC1-AC5 exist, labelled, as checkboxes |
| R4 | **fail** | four of the five criteria are undecidable as written. AC2 names "a fixed sample folder" that is not fixed anywhere; AC3 says two rule sets give "two different, predictable previews" with no statement of what makes a preview predictable; AC4 wants an error "identifying what is wrong" with no observable to check; AC5 wants something "stated somewhere a user can read" without naming the file. The item's own preamble says the criteria are rough and expects this |
| R5 | pass | `## Out of scope` names four things, including two the stakeholder settled as invariants |
| R6 | pass | no questions existed on the item before this round |
| R7 | pass | `depends-on: WI-0001`, which is `done` and merged |
| R8 | **fail** | this file did not exist |
| R9 | pass | one coherent change: one rule source, read once, feeding the two tables that already exist behind one lookup each [src: ADR-0005; src: tidy/rules.py]. Not a split candidate — the type table and the band table are configured by the same mechanism, and splitting them would mean designing the rule format twice, which is the exact cost ADR-0005 was written to avoid |
| R10 | **fail** | the item introduces one new axis — rules supplied or not — and the combinations are unstated. Rules supplied × the two existing modes (preview and `--apply`); rules supplied × an extension the rules do not mention; rules supplied × the never-overwrite invariant; rules supplied × a destination that collides with a band folder name. None of these has a criterion, an out-of-scope entry, or a recorded "deliberately unconstrained" |

## The triage — who each gap is for

Applied in the procedure's order: product stake first, then already-answered, then a standing
deferral, then implementation-only.

**Put to the stakeholder (2 questions, filed as Q-001 and Q-002).**

1. **Do user rules replace the built-in ones or layer on top of them?** → Q-001. Product stake:
   it decides whether a two-line rule file tidies the whole folder or leaves almost all of it
   alone, which is the first thing they would notice. Intake explicitly left it undecided in the
   item's `## Notes` and named `refine` as its owner; `refine`'s ownership is of the *routing*, and
   this one routes to the human.
2. **May a rule file decide how many bands there are, or only rename the two and move the line?**
   → Q-002. Product stake: it is a scope decision about how much of the tool's shape is the user's,
   and WI-0002 promised band names and the boundary to this item while saying nothing either way
   about the count [src: tracker/items/WI-0002/item.md `## Out of scope`].

**Not asked — already answered, and re-asking would be the failure the procedure names.**

- Never overwrite, and rename the incoming file: settled, and made an invariant rather than a
  configurable, on the stakeholder's own "I don't want to ask about this again" [src: EP-001/Q-002].
  Already on this item's out-of-scope list.
- Top level only, subfolders neither entered nor moved [src: EP-001/Q-003]. Already out of scope.
- Two bands split at a year, and `recent`/`old` as their names [src: WI-0002/Q-002]. Q-002 asks
  only whether a *user* may change the count; it does not re-open the default.
- That this item is built and not dropped [src: EP-001/Q-004].

**Not asked — a standing deferral covers it, so `refine` decides and says so.** The stakeholder
answered a whole category with "Whatever's easiest for you to build and test — you know this
better than me" [src: EP-001/Q-001], which is a real answer about how the thing is built, what
things are called, and the exact wording of output. Under it:

- **The rule file's format** — JSON, INI or TOML. Already ADR-0001's constraint and named as
  `plan`'s in the item's own preamble; not `refine`'s either.
- **Where the tool looks for rules, and how you point it at a specific set** — a default path, a
  flag, an environment variable, or some combination. This is AC5's subject, and AC5 will be
  rewritten to require that whatever is chosen is documented in `README.md`, which is decidable
  without deciding the mechanism.
- **The exit status of a run that rejects a rule file** — bounded to 0, 1 and 2 already
  [src: README.md; src: ADR-0006]; the criterion will require a non-zero status and that
  `README.md` accounts for it.

**Not asked — implementation-only, routed to `plan` via `## Notes`.** How a rule file that names a
destination colliding with a band folder name is handled; whether the two tables live in one file
or two; how an ordered band list is validated. Each has the same answer whoever the stakeholder is.

**Deliberately excluded rather than asked: a catch-all rule.** `README.md` promises that a file
whose extension matches nothing "is left where it is and reported on a `leave` line. It is not
swept into a catch-all folder" [src: README.md]. Letting a rule file introduce one would change a
documented promise, and nothing the stakeholder has said asks for it. It goes on `## Out of scope`
with that reasoning when the criteria are rewritten, so a later reader can see it was considered.

## Round 1 — asked 2026-08-27, answered 2026-08-27

### Q-001 — do your rules replace ours, or sit on top of them?

Filed as `questions/Q-001.md`, addressed to the human, blocking. Three options: **A** replace
entirely, **B** layer with the user's entries winning, **C** layer by default with replace on
request. Recommendation **B**, with "removing a built-in mapping" to be recorded as out of scope
if B is taken.

**Answer, verbatim, from the stakeholder** (`questions/Q-001.md`, `answered-by: human`):

> B — sit on top, mine win. I don't want to retype your whole seven-folder list just to move one
> extension somewhere else.

So: **option B**. A rule file adds to and overrides the built-in table; anything it does not name
keeps its built-in destination. The reason given is the cost of retyping, which is also the reason
`refine` recommended B. The gap B leaves — no way to *remove* a built-in mapping — is now recorded
on the item's `## Out of scope` list, as `refine` undertook it would be if B were taken.

### Q-002 — how far does control over the age side go?

Filed as `questions/Q-002.md`, addressed to the human, blocking. Three options: **A** two bands
always, names and boundary yours; **B** any number of bands; **C** B plus the ability to turn age
routing off entirely. Recommendation **B**, on the grounds that ADR-0005 already stores the bands
as an ordered list so the step is small, and the two-band default is untouched for anyone who
supplies no rules.

**Answer, verbatim, from the stakeholder** (`questions/Q-002.md`, `answered-by: human`):

> A — keep it at two bands. Recent and old is all I need, don't want to think about more than
> that.

So: **option A**, against the recommendation of B. A rule file supplies exactly two band names and
one boundary; it may not add a third band, collapse to one, or turn age routing off. `README.md`'s
"there are two bands and no others" and ADR-0005's ordered band table both stay as they are — only
the two names and the one number in that table become user-supplied. Note that this is the
stakeholder overriding a recommendation with a reason of their own ("don't want to think about
more than that"), not deferring to one; it is consistent with every previous answer they have
given about the age side [src: WI-0002/Q-002].

## Round 2 — decided by `refine`, 2026-08-27, without asking again

Round 1's two answers closed the product-stake gaps. What was left of R4 and R10 was, item by
item, either a consequence of those answers, or covered by the stakeholder's standing delegation
of how the thing is built — "Whatever's easiest for you to build and test — you know this better
than me" [src: EP-001/Q-001] — or an implementation choice whose answer is the same whoever the
stakeholder is. None of it was worth a second round trip, and asking would have told them their
delegation was not heard. Every decision below is therefore tagged `[assumed]`.

### R2.1 — the sample folder

R4 failed partly because old AC2 named "a fixed sample folder" that was fixed nowhere.

**[assumed]** A six-file sample folder `S` is now defined in the criteria preamble, with each
file's mtime and its present destination, in the style WI-0002's criteria already use. Basis: the
existing suite fixes timestamps with `os.utime` and this changes nothing about the tool. Anyone
with a terminal can build `S` and get the same verdict.

### R2.2 — what "predictable" meant

Old AC3 asked for "two different, predictable previews" and gave no way to decide it.

**[assumed]** AC4 now names two concrete rule files that differ in one entry and requires the two
previews to differ in exactly one line, quoted. Basis: this is the observable form of what old AC3
was reaching for; nothing new is being asked of the tool.

### R2.3 — what makes a rule file malformed

Old AC4 wanted an error "identifying what is wrong" with nothing to check against. The set of
malformed files could not be listed before round 1, because it depends on what a well-formed file
may say — which is what Q-001 and Q-002 settled.

**[assumed]** AC8 lists six classes and requires, for each, one line on stderr naming the file and
the problem, nothing on stdout, a non-zero exit, and the folder untouched in **both** modes.
Basis: the six follow from the two answers (a band count other than two is malformed *because* the
stakeholder chose A) and from the shape a destination may take (R2.4). The exit status is left as
"non-zero" and `README.md` is required to account for it, rather than pinned to 1 or 2 here:
choosing between them is exactly the category EP-001/Q-001 delegated, and ADR-0006 already
bounds the vocabulary.

### R2.4 — how deep a destination may go

Nobody had said whether a type entry may name `work/pdfs` rather than `data`.

**[assumed], and this one is a narrowing the stakeholder was not asked about.** A destination is a
single folder name. Basis: WI-0002 AC1 was verified against destination paths of exactly three
components, `<band>/<type>/<name>`, so allowing a deeper destination would break a criterion an
earlier item already passed. The alternative — asking — would have cost a round trip on a case
they have never mentioned. It is on the item's `## Out of scope` list with this reasoning, which is
where they will see it. If it is wrong, it is the entry to change.

### R2.5 — units and validation on the age side

Q-002 gave the user two band names and one boundary; it did not say in what units the boundary is
written, or what an invalid one is.

**[assumed]** Days, as a positive number, and the boundary keeps WI-0002 AC4's sense — a file whose
age is exactly the boundary falls in the older band. Basis: `README.md` already states the age rule
in days ("less than **365 days** ago"), so the unit is the one the user has already read, and
keeping the boundary's sense means renaming the bands does not silently move a file that was not
renamed. Invalid boundaries and band names are folded into AC8.

### R2.6 — either table without the other

The agenda routed "whether a file may supply one table without the other" to `plan` as an
implementation choice. On reflection it is not one: it is Q-001's layering answer applied to the
age side, and a user who writes two lines about `.csv` would be surprised to find their bands had
been reset.

**[assumed]** AC6 requires it: what a rule file omits keeps its built-in values. Basis:
[src: WI-0003/Q-001]. Only the mechanism — one file or two — stays with `plan`.

### R2.7 — R10's combinations

**[assumed]** The new axis is "rules supplied, or not", and every crossing of it with an existing
behaviour is now in a table in the item's `## Notes`, each pointing at the criterion that states
it. Two are recorded there as deliberately unconstrained, with `refine` named as who left them so:
a destination colliding with a band folder name (AC11 binds the modes to agree and `README.md` to
say which), and which error wins when a rule file and the target folder are both bad. Basis: R10
requires the combinations to be **visible**, not decided, and both of these are implementation
choices where any answer is safe.

## What was not asked, and why

Unchanged from the agenda above, and worth restating because it is the part of this record a
reader is most likely to want: the never-overwrite rule and the no-recursion rule were settled as
invariants at intake and are on `## Out of scope`; the two-band default and its names came from
WI-0002/Q-002; that this item is built at all came from EP-001/Q-004; and a catch-all folder was
excluded deliberately rather than asked, because introducing one would break a promise `README.md`
already makes.

## Override

None. Every Definition of Ready criterion is met on its own terms; nothing was passed on the
stakeholder's authority to waive it.

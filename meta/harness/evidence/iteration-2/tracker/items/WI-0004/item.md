---
id: WI-0004
type: work-item
title: Pick up a rules file from a default location, without --rules
status: done
priority: medium
epic: EP-001
created: "2026-08-28T14:54:39Z"
updated: "2026-08-28T15:41:23Z"
arose-from: EP-001/Q-005
relates-to:
  - WI-0003
branch: wi/WI-0004
outcome: delivered
---

## Story

As someone who has written a rule file and wants it used every time, I want `tidy` to find that
file on its own, so that I do not have to type `--rules PATH` on every run.

## Acceptance criteria

These are the stakeholder's ask turned into rough criteria by `answer-questions`, which created
this item from their sign-off answer. They are **not** the Definition of Ready: `refine` owns
sharpening them, and the questions under `## Notes` have to be settled first — chief among them
*where* the default location is, which is the stakeholder's to choose and not ours.

`refine` read them against the Definition of Ready on 2026-08-28 and **R4 fails**: every one of
them turns on "the default location", and there was no such place until the stakeholder said where
it is. That was `questions/Q-001.md` [src: WI-0004/Q-001], and this item was suspended on it.

**The stakeholder has now answered, and the place is the user's own config directory** — their own
rule file, one for every folder they tidy, and explicitly *not* a file sitting in the folder being
tidied: *"B. My own file, not one sitting in the folder — I don't want rules riding along in a
folder someone hands me"* [src: WI-0004/Q-001]. The exact filename and path spelling are ours; the
question said so when it was asked.

**Round 2, on 2026-08-28, rewrote them against that answer, and R4 now passes.** AC1–AC10 below
replace the six rough ones; each names a command to run and a verdict that follows, and the
boundary cases the rough set only gestured at — an empty file at the default location, an
unreadable one, both sources present at once, neither present — are criteria rather than
implications. The vocabulary is WI-0003's, unchanged, so that a reader who has read that item can
read this one [src: WI-0003].

**Throughout:** `TOOL` is `python3 -m tidy`, `PREVIEW` is a run of it without `--apply` and
`APPLY` a run with it [src: WI-0001]. `S` is the six-file sample folder WI-0003's criteria define,
with the same mtimes and the same "where it goes today" column [src: WI-0003]; `F1`, `F3` and `F4`
are WI-0003's rule files — `F1` sends `.csv` to `data`, `F3` sends `.csv` to `tables`, `F4` renames
the bands to `current`/`archive` at a 90-day boundary [src: WI-0003 AC2; src: WI-0003 AC4;
src: WI-0003 AC5].

**`D` is the default location**, and it is this path: `$XDG_CONFIG_HOME/tidy/rules.ini` when
`XDG_CONFIG_HOME` is set and non-empty, and `<home>/.config/tidy/rules.ini` otherwise. That is the
user's own config directory the stakeholder chose [src: WI-0004/Q-001]; the spelling is ours, taken
under their standing delegation [src: EP-001/Q-001], and the `XDG_CONFIG_HOME` half is what makes
every criterion below runnable against a temporary directory instead of the machine's real home —
"easiest for you to build and test" is the delegation's own phrase. `D` is one path, not a search
chain: if nothing is readable there, no other place is consulted.

- [x] AC1 — **A rule file at `D`, with no `--rules`, sorts the folder.** Put `F1` at `D` and run
      PREVIEW over `S` with no `--rules`: stdout is line-for-line what WI-0003 AC2 states for
      `RULES(F1)` — `move   budget.csv -> recent/data/budget.csv`, and the other five files exactly
      as WI-0003 AC1 gives them [src: WI-0003 AC1; src: WI-0003 AC2]. Run APPLY over an unchanged
      `S`: every file is afterwards at exactly the path PREVIEW printed. Repeat both with `F4` at
      `D`: `taxes.pdf` lands at `archive/documents/taxes.pdf` and the other movable files under
      `current/` [src: WI-0003 AC5]. The verdict is equality — the same file at `D` and the same
      file passed with `--rules` produce the same stdout and the same tree.
- [x] AC2 — **Nothing readable at `D` and no `--rules` is a no-rules run.** With no file at `D`,
      PREVIEW and APPLY over `S` produce exactly the output and the resulting tree WI-0003 AC1's
      table states, and `python3 -m unittest discover -s tests -t . -q` exits 0 with no existing
      test edited to accommodate this item [src: WI-0003 AC1]. The same verdict holds when no config
      directory can be determined at all — `XDG_CONFIG_HOME` unset or empty **and** no home
      directory — which is a no-rules run and not an error: run it with `HOME` unset and
      `XDG_CONFIG_HOME` unset and observe AC1's "where it goes today" output and exit 0.
- [x] AC3 — **`--rules PATH` beats `D`.** With `F1` at `D`, run `TOOL S --rules F3` in PREVIEW:
      stdout prints `move   budget.csv -> recent/tables/budget.csv` — `F3`'s answer, not `F1`'s —
      the other five lines are AC1's, the exit is 0, and the line AC4 requires names `F3`'s path and
      not `D`.
- [x] AC4 — **A run names the rule file it used, on stderr, and prints no such line when it used
      none.** Whenever a rule file is loaded — from `D` or from `--rules` — the run's **stderr**
      contains that file's path, on its own line, before the first per-file line, in both PREVIEW
      and APPLY. Checkable by capturing the two streams separately and searching stderr for the
      path. When no rule file is loaded, no line naming a rule file appears on either stream, and
      stdout is byte-for-byte AC2's. **stdout never carries this line in either case**, which is
      what keeps WI-0003 AC1's stdout comparison exact [src: WI-0003 AC1] and keeps the promise that
      stdout is one line per file [src: tidy/cli.py]. The line's wording is `plan`'s, under the
      standing delegation [src: EP-001/Q-001]; this criterion fixes the stream, the ordering, and
      that the path is in it. It is the answer to the one cost ADR-0010 named against a default
      location [src: ADR-0010].
- [x] AC5 — **A malformed file at `D` is refused exactly as one named with `--rules` is.** For each
      of WI-0003 AC8's six classes there is a file that exhibits it [src: WI-0003 AC8]; put each at
      `D` in turn and run with no `--rules`. Both PREVIEW and APPLY print one line on stderr naming
      `D` and what is wrong with the file, print nothing on stdout, exit **2** [src: ADR-0010], and
      leave `S` byte-for-byte as it was.
- [x] AC6 — **A file at `D` that exists and cannot be read is refused the same way.** With a file
      at `D` whose mode is `000`, both modes print one line on stderr naming `D` and the operating
      system's reason, print nothing on stdout, exit 2, and move nothing. This is the treatment
      WI-0003 already gives an unreadable file named with `--rules` [src: tidy/ruleset_file.py], and
      it is deliberately *not* AC2: a file the user put there and we cannot read is not the same
      event as no file at all, and silently sorting by the built-in tables would be the surprise
      this tool exists not to have [src: docs/product/vision.md].
- [x] AC7 — **An empty file at `D` is a rule file that was used, and it changes nothing.** With a
      zero-byte file at `D`, PREVIEW and APPLY over `S` produce exactly AC2's output and tree — both
      tables keep their built-in values [src: WI-0003 AC6] — **and** AC4's stderr line names `D`,
      because a file was read. Exit 0.
- [x] AC8 — **A default rule file changes nothing else the tool promises.** With `F1` at `D` and no
      `--rules`, over `S`: `.hidden.jpg` appears in neither mode's output and is not moved; a
      pre-existing subfolder and everything in it is neither entered nor moved nor listed; a file
      matching neither `F1` nor the built-in table still gets a `leave` line; and with
      `recent/data/budget.csv` already present with different contents, the line reads
      `-> recent/data/budget (2).csv` in both modes and the pre-existing file has its original size
      and contents after APPLY [src: EP-001/Q-002; src: EP-001/Q-003; src: WI-0003 AC10].
- [x] AC9 — **`README.md` states all of it.** It says where `D` is, in both its forms; that
      `--rules PATH` overrides it; that a run names the rule file it used and that a run using none
      says nothing; that a file at `D` which is malformed or unreadable stops the run with exit 2
      and moves nothing; and that an empty file at `D` is read and changes nothing. Checkable by
      reading it against AC1–AC7. The sentence "**There is no default location.**" must be gone
      [src: README.md].
- [x] AC10 — **`--help` does not still say there is no default location.** `TOOL --help` names `D`
      and says `--rules` overrides it, and contains no occurrence of the string "no default
      location", which is what its `--rules` help text and epilog say today [src: tidy/cli.py].
      Guarded by a test, as help-text prose already is [src: ADR-0008]. BUG-0003 was exactly this
      class of staleness — `--help` describing the tool as it was before an item landed
      [src: BUG-0003].

## Out of scope

- Anything EP-001's own `## Out of scope` list excludes. In particular the stakeholder was
  explicit at sign-off that they do not want descending into subfolders and do not want undo:
  "Don't bother with the subfolder thing or undo, I don't need either of those"
  [src: EP-001/Q-005].
- More than one default location, or a search path of several. The stakeholder was offered a
  fallback chain — the folder's own file first, theirs second — and did not take it
  [src: WI-0004/Q-001]. `D` is one path; when nothing is readable there, no other place is
  consulted.
- **A rule file in the folder being tidied.** A `.tidyrules` beside the files, which is what
  ADR-0010 weighed and what a reader of "a default spot" might most expect, is deliberately not
  built: *"I don't want rules riding along in a folder someone hands me"* [src: WI-0004/Q-001].
  Nothing inside a target folder is a rule source.
- **A way to turn the default off for one run** — no `--no-rules` flag, no `--rules ''` documented
  as meaning "ignore `D`". A user who has a file at `D` and wants one run without it is a real
  person, and nobody has asked for them; if they turn up it is a new item, not a widening of this
  one. What `--rules ''` does today is a known gap recorded below, and `plan` decides it.
- Changing what a rule file can say. The format, the layering, and the two-band rule are settled
  and this item does not reopen them [src: ADR-0010; src: WI-0003/Q-001; src: WI-0003/Q-002].
- An environment variable naming the rule *file* — no `TIDY_RULES=/path/to/rules.ini`. Not asked
  for. `XDG_CONFIG_HOME` is not that: it says where the user's config directory is, which is the
  standard way of locating one, and it names a directory rather than a rule file.
- Generating or editing a rule file for the user — no `tidy --init-rules`. Not asked for.

## Notes

**Where this came from.** The stakeholder accepted the engagement at sign-off and named exactly
one follow-up: *"I don't want to pass `--rules` every single time, so give the rule file a default
spot it just picks up on its own."* [src: EP-001/Q-005]. They declined the two other candidates
they were offered — subfolder recursion and undo — in the same answer.

**This reverses a recorded decision, with the stakeholder's authority.** ADR-0010 considered a
default location as its option E and rejected it, choosing "one INI file, named with `--rules
PATH`, no default location". Its stated reason is a real one and does not go away because the
stakeholder asked: *"a file can change what a run does without appearing anywhere the user looked,
which is the opposite of what the preview exists to provide"* [src: ADR-0010;
src: docs/product/vision.md]. Two consequences:

- `plan` must **supersede** ADR-0010 with a new ADR that cites it, rather than edit it — an ADR is
  never edited to change its decision (`spec/doc-header.md` §4). The authorisation for the
  supersession is the stakeholder's answer [src: EP-001/Q-005].
- AC4 exists because of that reason, not despite it. The way a default location stays compatible
  with the product's central promise is that the run says which file it used, so nothing shapes a
  run invisibly.

**Open, and `refine` owns them.** The first was the stakeholder's to answer and is now answered;
the rest are not theirs:

1. ~~**Where the default file lives.**~~ **Answered 2026-08-28: the user's own config directory.**
   ADR-0010 named two candidates and they behave differently: a file *beside the folder being
   tidied* (a `.tidyrules` in the target folder), which travels with a folder you were handed and
   is the surprise ADR-0010 weighed [src: ADR-0010]; or one under the *user's own config directory*
   (`~/.config/tidy/rules.ini`), which is the user's own file and applies to every folder they
   tidy. Asked as Q-001 because the two differ in what happens to files they did not put there,
   they chose the second and gave that reason back: *"I don't want rules riding along in a folder
   someone hands me"* [src: WI-0004/Q-001]. So the folder being tidied is **not** a rule source,
   and neither is a fallback chain of both — the option that kept both was offered and not taken.
   What was still ours — the exact filename and path spelling, and whether the directory is found
   via `XDG_CONFIG_HOME` or a fixed `~/.config` — **round 2 settled**: `D` is
   `$XDG_CONFIG_HOME/tidy/rules.ini` when that variable is set and non-empty and
   `<home>/.config/tidy/rules.ini` otherwise, stated at the head of the criteria.
2. ~~What a run prints about which rule file it used, and whether it prints anything when there is
   no rule file at all.~~ **Decided in round 2, under the standing delegation** [src: EP-001/Q-001]:
   the path goes on **stderr**, before the per-file lines, whenever a file was loaded from either
   source, and a run that loaded none prints no such line. AC4. stderr because stdout is one line
   per file and nothing else [src: tidy/cli.py], and printing there would break WI-0003 AC1's
   byte-for-byte stdout comparison [src: WI-0003 AC1]. Nothing printed on a no-rules run because the
   line exists to make an *unnamed* file visible, and there is no unnamed file to make visible. The
   wording of the line is still `plan`'s.
3. ~~Whether the default location applies to `--apply` runs as well as previews.~~ **Decided in
   round 2: both.** Every one of AC1, AC5, AC6, AC7 and AC8 names PREVIEW and APPLY explicitly, so
   it is stated rather than implied.

**Accepted at review, 2026-08-28 — `--rules ""` now ends the run, and nobody asked for that.**
`review-close` accepted this item with one gap recorded rather than fixed. Before this item,
`python3 -m tidy S --rules ''` printed the preview and exited 0, because `cli.py` guarded the
loader with `if args.rules:`. After it, the guard is "was `--rules` given at all" — ADR-0014
point 3 — so an empty string names a path that cannot be opened and the run ends:
`tidy:  cannot be used: No such file or directory`, exit 2. Both states were run against the same
folder during review. Three things about it are recorded here because the item is now closed and
nothing else will carry them:

- It is **in scope and correctly decided**. `## Out of scope` above leaves `--rules ''` undefined
  and R10's table routed the decision to `plan`, which took it in ADR-0014 [src: ADR-0014].
- No criterion of this item covers it, so it was **not** a send-back, and no bug item was filed:
  the engagement had already been signed off once and this behaviour is out of scope by this
  item's own words, so adding a child over it would prolong an engagement the stakeholder has
  accepted, on something they were never asked about.
- The **message is poor**: it names no path, and has a double space where the empty path would
  be, so a user whose `--rules "$VAR"` had an empty `VAR` is told nothing actionable. If this is
  ever picked up, that is the part worth fixing, and it is one format string.

It is surfaced to the stakeholder at sign-off rather than decided for them
[src: docs/product/vision.md].

**Surfaced, and answered 2026-08-28: they do not want it fixed.** `Q-006` put both this message and
the neighbouring "a broken rule file at `D` stops the run" decision to them as named follow-up
candidates. They accepted the engagement as complete and declined both by name: *"Don't bother with
the `--rules ''` message or making a broken rules file fall back to the built-in tables — if I typo
my own rules file that's on me to fix, I'd rather it stop and tell me than guess."*
[src: EP-001/Q-006]. So the poor message stands, on the record, with the stakeholder having been
told exactly what it prints; and AC5/AC6's treatment of an unusable file at `D` — refuse it, exit 2,
move nothing — is no longer the team's assumption but their decision [src: ADR-0014]. Neither is a
new item and EP-001's `## Out of scope` now names both.

**A neighbouring known gap, deliberately not folded in.** `review-close` recorded on WI-0003 that
`--rules ""` is silently a no-rules run, because `cli.py` guards the loader with `if args.rules:`
[src: tracker/items/WI-0003/item.md; src: tidy/cli.py]. Once a default location exists, that same
guard decides whether an empty `--rules` falls back to the default or means "no rules", so this
item's design cannot avoid touching the question. **Round 2 decided the half that was `refine`'s
and left the rest to `plan`:** `--rules ''` is out of scope as a documented way of turning `D` off,
so whichever behaviour `plan` gives it, no criterion of this item depends on it and `README.md`
need not promise one. What `plan` may not do is make it *silently* different from what
`README.md` says.

### Refinement, round 1, 2026-08-28 — one question to the stakeholder, the rest decided here

The full agenda, the triage and the reasoning are in `artifacts/refinement-qa.md`, which now
declares `status: recorded`, because the exchange has happened and the answer is in it. In summary:

**Asked** — `Q-001`, blocking: *where* the tool looks for a rule file it was not told about. Three
options: in the folder being tidied, in the user's own config directory, or both. It is theirs
because the candidates differ in whether a folder somebody else handed them can change what
happens to their files, which is the same instinct as the never-overwrite rule they called the one
thing they cared about [src: EP-001/Q-002]. It is also the decision ADR-0010 took the other way,
and contradicting an ADR is the human's to authorise [src: ADR-0010].

**Answered 2026-08-28 — the user's own config directory**, and for the reason the question
predicted: *"B. My own file, not one sitting in the folder — I don't want rules riding along in a
folder someone hands me. Go with your recommendation."* [src: WI-0004/Q-001] Nothing inside a
target folder is a rule source. That is the authorisation ADR-0010 needs to be superseded, and
`plan` still owns writing the ADR that supersedes it.

**Decided here, under the standing delegation "whatever's easiest for you to build and test"**
[src: EP-001/Q-001] — each is tagged `[assumed]` in the Q&A rather than recorded as theirs:

- `--rules PATH` beats the default location when both are present (AC3).
- A malformed rule file at the default location is refused exactly as one named with `--rules` is
  [src: WI-0003 AC8], rather than ignored in favour of the built-in tables (AC5). **This was the
  assumption most worth revisiting** — it means a typo in a file the user is not looking at stops
  every run until they fix it — and it was duly put to the stakeholder at the second sign-off and
  chosen by them, so it is no longer an assumption: *"if I typo my own rules file that's on me to
  fix, I'd rather it stop and tell me than guess"* [src: EP-001/Q-006]. It is taken because the alternative is a run quietly sorting by
  rules the user did not write, which is the surprise this tool exists not to have
  [src: docs/product/vision.md].
- A run states which rule file it used, as part of the preview (AC4) — the answer to the one cost
  ADR-0010 named when it rejected a default location [src: ADR-0010].
- The exact filename and path spelling, whichever kind of place Q-001 picks.

**Not re-asked**: subfolder recursion and undo (declined by name at sign-off
[src: EP-001/Q-005]), and what a rule file may contain [src: WI-0003/Q-001; src: WI-0003/Q-002].

### Refinement, round 2, 2026-08-28 — nothing asked, the criteria rewritten

Nothing went to the stakeholder this round. Their answer to Q-001 opened one new choice — whether
the config directory is found by `XDG_CONFIG_HOME` or by a fixed `~/.config` — and that is squarely
inside the category they delegated: *"Whatever's easiest for you to build and test"*
[src: EP-001/Q-001]. Asking it would tell them their answer was not heard. The full round is in
`artifacts/refinement-qa.md`.

**Decided this round, all `[assumed]`:**

- **`D` is `$XDG_CONFIG_HOME/tidy/rules.ini`, falling back to `<home>/.config/tidy/rules.ini`.**
  Honouring `XDG_CONFIG_HOME` is the standard way of locating a config directory, and it is what
  makes every criterion testable against a temporary directory rather than the machine's real home.
- **The line naming the rule file goes on stderr**, before the per-file lines, in both modes, and a
  run that loaded no rule file prints no such line (AC4).
- **An unreadable file at `D` stops the run** rather than falling through to the built-in tables
  (AC6), for the same reason a malformed one does.
- **An empty file at `D` is a rule file that was used** (AC7): it changes no sorting, and AC4's
  line still names it.
- **`--help` is in scope** (AC10). Its `--rules` text and its epilog both say there is no default
  location today [src: tidy/cli.py], and BUG-0003 was filed once already for help text left behind
  by an item [src: BUG-0003].

**A design point `plan` must not miss.** `ruleset_file.load` raises `RuleFileError` for *every* way
a file cannot be used, `OSError` included [src: tidy/ruleset_file.py] — so a missing file and an
unreadable file arrive at `cli.py` as the same exception. AC2 and AC6 require them to be different
events: nothing at `D` is a no-rules run, a file at `D` that cannot be read is exit 2. Calling
`load(D)` unguarded would exit 2 on every machine that has no rule file, which is every machine
today. Named here rather than left for `implement` to discover.

### R10 — the combinations this item introduces, and where each is stated

One new axis: a rule file that was not named on the command line. Crossed with what already
exists. Round 1 could not close four of these rows, because every one of them turned on a location
nothing named; round 2 closes them against `D`. Two rows remain deliberately unconstrained and say
who left them so, which is what R10 asks for.

| combination | where it is stated |
|-------------|--------------------|
| a file at `D` × PREVIEW and APPLY | AC1 (both modes, same result as `--rules` on the same file) |
| nothing at `D` × no `--rules` | AC2 — a no-rules run, the case WI-0003 AC1 already settles [src: WI-0003 AC1] |
| a file at `D` × `--rules` also given | AC3 — the flag wins |
| a malformed file at `D` × both modes | AC5 — refused as WI-0003 AC8 refuses one named with `--rules` |
| a run that loaded a rule file × which file it was | AC4 — its path, on stderr, before the per-file lines, in both modes |
| a file at `D` × the never-overwrite invariant, hidden files, and subfolders | AC8 — none of these changes with where the rules came from, and AC8 says so with a command rather than leaving it assumed |
| a file at `D` that exists but is empty | AC7 — it sorts exactly as a no-rules run does [src: WI-0003 AC6], and AC4's line still names it, because it was read |
| a file at `D` that exists and cannot be read | AC6 — refused as AC5 refuses a malformed one, exit 2, nothing moved. Deliberately not AC2: a file the user put there and we cannot read is not the same event as no file at all |
| a run that loaded no rule file × what it prints about rules | AC4 — nothing. The line exists to make an unnamed file visible, and there is none |
| no config directory at all (`XDG_CONFIG_HOME` unset, no home) × no `--rules` | AC2 — a no-rules run, not an error |
| `XDG_CONFIG_HOME` set × `XDG_CONFIG_HOME` unset | the criteria preamble — `D` is the first when the variable is set and non-empty, the second otherwise, and every criterion below is run against both |
| a file at `D` × `--help` and `README.md` | AC9 and AC10 — both must name `D`, and neither may still say there is no default location |
| `--rules ""` × a file at `D` | **deliberately unconstrained by `refine`, routed to `plan`.** `cli.py` guards the loader with `if args.rules:`, so today an empty `--rules` is silently a no-rules run [src: tracker/items/WI-0003/item.md; src: tidy/cli.py]; once `D` exists that same guard decides whether it falls back or not. Either behaviour is defensible and the answer is the same whoever the stakeholder is. No criterion of this item depends on it, and `## Out of scope` records that `--rules ''` is not a documented way of turning `D` off |
| a bad rule file × a target folder that cannot be used | **deliberately unconstrained by `refine`, routed to `plan`**, exactly as WI-0003 left the same crossing [src: tracker/items/WI-0003/item.md]. Whichever error wins, nothing moves and the exit is non-zero |

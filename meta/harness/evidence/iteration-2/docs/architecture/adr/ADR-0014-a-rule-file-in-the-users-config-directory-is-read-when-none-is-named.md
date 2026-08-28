---
title: A rule file in the user's config directory is read when none is named
version: 2
status: current
updated: 2026-08-28T16:23:10Z
updated-by: answer-questions
updated-for: EP-001
---

# ADR-0014 — A rule file in the user's config directory is read when none is named

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** plan (architect), for WI-0004
- **Supersedes:** ADR-0010 (in part — the "where the file comes from" half)

## Context

ADR-0010 decided two things at once: the rule file's **format** (INI, via `configparser`) and
**where it comes from** (a `--rules PATH` flag only, no default location). This ADR supersedes the
second half and leaves the first untouched — the format, the two sections, the three fixed band
keys, the `optionxform` override and the exit-2 rule are all still ADR-0010's and are not reopened
here [src: ADR-0010].

The reason ADR-0010 gave for rejecting a default location was not a preference. It was that *"a
file can change what a run does without appearing anywhere the user looked, which is the opposite
of what the preview exists to provide"* [src: ADR-0010; src: docs/product/vision.md]. That
objection is still true and this ADR does not pretend otherwise; the decision below answers it
rather than overruling it.

**What changed is the authorisation, and it is the stakeholder's.** At sign-off they accepted the
engagement and asked for exactly one thing on top: *"I don't want to pass `--rules` every single
time, so give the rule file a default spot it just picks up on its own"* [src: EP-001/Q-005].
Contradicting an ADR is theirs to authorise and nobody else's
[src: .claude/agile-skills/spec/question.md]. They were then asked **which kind of place**, given
three options with their costs, and they chose one and gave their reason:

> B. My own file, not one sitting in the folder — I don't want rules riding along in a folder
> someone hands me. Go with your recommendation. [src: WI-0004/Q-001]

So the half of ADR-0010's worry that concerned *a folder you were handed* is not overruled at all
— it is upheld, by the stakeholder, in their own words. What is overruled is the narrower claim
that a run must depend on nothing but its command line.

The constraints in play are unchanged: standard library only, Python 3.9 floor [src: ADR-0001]; a
`Ruleset` is a value passed into the planner, and `ruleset_file.py` is the only module that reads a
rule file [src: ADR-0011; src: tidy/ruleset_file.py]; stdout is one line per file and nothing else,
with the banner and every error on stderr [src: tidy/cli.py].

## Options considered

**Where the default file lives** — put to the stakeholder as WI-0004/Q-001, so the cost lines below
are the ones they were shown.

- **A — In the folder being tidied**, e.g. `.tidyrules` beside the files. Cost: a folder somebody
  else handed you can carry rules that redirect your files. Risk: exactly the surprise ADR-0010
  weighed, on a tool whose whole promise is that there are none. **Rejected by the stakeholder**
  [src: WI-0004/Q-001].
- **B — In the user's own config directory**, one file used for every folder they tidy. Cost:
  per-folder rules go back to needing `--rules`, and a mistake in that one file affects every run
  until it is fixed. Risk: low and bounded — the only rules that can apply are ones the user wrote
  in their own home directory. **Chosen** [src: WI-0004/Q-001].
- **C — Both, the folder's file first and the user's as a fallback.** Cost: two places a rule file
  can hide. Risk: keeps A's exposure entirely. **Rejected by the stakeholder** [src: WI-0004/Q-001].

**How the config directory is located** — ours, under the standing delegation *"Whatever's easiest
for you to build and test"* [src: EP-001/Q-001].

- **D — A fixed `~/.config`, via `os.path.expanduser`.** Cost: `expanduser` falls back to the `pwd`
  database when `HOME` is unset — `env -u HOME python3 -c 'import os; print(os.path.expanduser("~"))'`
  still printed this machine's home directory
  [src: run: env -u HOME python3 -c 'os.path.expanduser("~")' → /home/msi] — so what a run reads is
  not a function of its environment alone. Risk: a test has no reliable way to say "there is no config directory",
  and a test run on a developer's machine may pick up that developer's real rule file.
- **E — `XDG_CONFIG_HOME` when set and non-empty, else `$HOME/.config`, and no default location at
  all when neither is set.** Cost: two environment variables instead of one path. Risk: low —
  it is the ordinary convention for a config directory on this platform, and every acceptance
  criterion becomes runnable against a temporary directory. **Chosen.**

**What makes it safe.**

- **F — Say nothing about which rule file was used.** Cost: ADR-0010's objection stands
  unanswered: a file the user did not name shapes the run and appears nowhere. Risk: unacceptable
  on this product.
- **G — Name the rule file on stderr, before the per-file lines, whenever one was loaded.** Cost:
  one more line in the output of a run that uses rules. Risk: none to what already exists — stdout
  is untouched, so the byte-for-byte stdout comparisons WI-0003's criteria rest on still hold
  [src: WI-0003 AC1]. **Chosen.**

## Decision

**A rule file is read from `$XDG_CONFIG_HOME/tidy/rules.ini`, or `$HOME/.config/tidy/rules.ini`,
when `--rules` is not given — and a run that loads a rule file names it on stderr
[src: WI-0004 AC4].**

Five points are fixed here because each would otherwise be decided silently:

1. **The default location, exactly.** `XDG_CONFIG_HOME` when it is set and non-empty:
   `<XDG_CONFIG_HOME>/tidy/rules.ini`. Otherwise `HOME` when it is set and non-empty:
   `<HOME>/.config/tidy/rules.ini`. Otherwise **there is no default location** and the run is a
   no-rules run — not an error. The value is read from the environment mapping and from nowhere
   else: no `pwd` lookup, no `expanduser`, so what a run will read is a function of its environment
   and can be stated by a test.
2. **One path, not a search.** When nothing is readable at that path, no other place is consulted
   [src: WI-0004].
3. **`--rules` wins, and it wins by being *given* rather than by being non-empty.** The existing
   guard is `if args.rules:`, which makes `--rules ""` silently a no-rules run — a gap
   `review-close` already recorded against WI-0003 [src: tracker/items/WI-0003/item.md]. Once a
   default exists, that same guard would have to mean "fall back to the default", which would make
   an empty string a documented way of *reaching* the default while looking like a way of avoiding
   it. So the test becomes "was `--rules` given at all": `--rules ""` names a path that cannot be
   opened, and is refused like any other unusable rule file — one line on stderr, exit 2.
4. **Present-and-unusable is not the same event as absent.** A file at the default location that
   is malformed, unreadable, or a dangling symlink stops the run with exit 2 and moves nothing,
   exactly as one named with `--rules` does [src: WI-0003 AC8]. Only *nothing being there* is a
   no-rules run. The alternative — ignore the broken file and sort by the built-in tables — is a
   run doing something other than what the user's own rule file says, which is the surprise this
   product exists not to have [src: docs/product/vision.md]. Presence is decided with
   `os.path.lexists`, so a symlink that points nowhere counts as present: the user put something
   there.
5. **The run names the rule file it used, on stderr, before the per-file lines, in both modes** —
   and prints nothing of the kind when it loaded no rule file. stderr and not stdout because stdout
   carries one line per file and nothing else [src: tidy/cli.py]; nothing on a no-rules run because
   the line exists to make an *unnamed* file visible, and there is none to make visible.

## Consequences

What becomes easy: a user writes one rule file once and every `tidy` run uses it. Nothing in a
folder can change what a run does to that folder, so the property the stakeholder actually cared
about survives a feature that could have destroyed it. Because the location comes from the
environment mapping alone, the whole feature is testable against a temporary directory, and a test
run cannot be influenced by the developer's own rule file.

What becomes harder: a run is no longer reproducible from its command line alone — it is
reproducible from its command line plus two environment variables, and the stderr line is what
tells the reader which. Per-folder rules now need `--rules` again. And a mistake in the one file
affects every run until it is fixed, which is the cost the stakeholder was shown and accepted
[src: WI-0004/Q-001].

**Point 4 was ours when this ADR was written, and is the stakeholder's now.** Refusing a present
but unusable rule file at the default location, instead of falling back to the built-in tables,
was taken here under the standing delegation and flagged by `refine` as the assumption most worth
revisiting, because a typo in a file the user is not looking at stops every run until it is fixed
[src: WI-0004]. It was put to the stakeholder at the engagement's second sign-off as a named
follow-up they could have — "make a broken file at the default location fall back to the built-in
rules" — and they declined it and gave back the same reason the team had: *"if I typo my own rules
file that's on me to fix, I'd rather it stop and tell me than guess"* [src: EP-001/Q-006]. The
decision above is unchanged and this ADR is not superseded; what changed is its basis. The same
answer declined the one behaviour change this ADR caused that nobody asked for — `--rules ""`
ending the run with a message that names no path, point 3 above — so that message stands as it is,
with the stakeholder having been shown exactly what it prints [src: EP-001/Q-006; src: WI-0004].

**Reversibility: cheap for the mechanism, not for the promise.** Removing the default location
again is one function and one branch in `cli.py`, no data migration, no format change — but it is
a promise made to the user, and withdrawing it needs the stakeholder, exactly as introducing it
did. Changing *which* path is the default is cheaper still, one function, and would need `README.md`
and `--help` updated with it. Adding option A or C later remains additive, as ADR-0010 said, and is
now explicitly out of scope on the stakeholder's own instruction [src: WI-0004].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-28T16:23:10Z | answer-questions | EP-001 | Recorded the stakeholder's second sign-off answer [src: EP-001/Q-006]: decision point 4 — an unusable rule file at the default location stops the run rather than falling back — was offered to them as a reversible follow-up and kept, so it is authorised rather than assumed. The decision itself is unchanged |
| 1 | 2026-08-28T15:15:08Z | plan | WI-0004 | First version. Supersedes the "where the file comes from" half of ADR-0010, on the stakeholder's authorisation |

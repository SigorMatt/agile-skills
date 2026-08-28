---
title: Rules come from one INI file named on the command line
version: 2
status: superseded
superseded-by: ADR-0014
updated: 2026-08-28T15:15:08Z
updated-by: plan
updated-for: WI-0004
---

# ADR-0010 — Rules come from one INI file named on the command line

- **Status:** superseded
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0003
- **Supersedes:** —
- **Superseded by:** ADR-0014, for WI-0004 — in part: the "where the file comes from" half. The
  format decision below (B: one INI file, its two sections, its three fixed band keys, the
  `optionxform` override and the exit-2 rule) is **still current** and is what the tool does. What
  ADR-0014 replaces is D, "no default location", on the stakeholder's authorisation
  [src: ADR-0014; src: EP-001/Q-005; src: WI-0004/Q-001].

## Context

WI-0003 makes the two sorting tables user-supplied. `refine` left four things to this skill, all
of them about how rules get into a run rather than what they mean: the file's format, whether the
two tables come from one file or two, where the tool looks for a rule file, and what a run that
rejects one exits with [src: WI-0003].

The constraints were already fixed elsewhere. The tool is standard library only with an
interpreter floor of Python 3.9 [src: ADR-0001], which rules out YAML entirely and makes TOML via
`tomllib` a floor change rather than a free choice. The stakeholder's answers fix what the file
has to express: type entries that layer over the built-in table with theirs winning
[src: WI-0003/Q-001], and exactly two bands whose names and single boundary they choose
[src: WI-0003/Q-002]. Their standing answer about how the thing is built — "Whatever's easiest for
you to build and test — you know this better than me" — is what makes this ours to decide at all
[src: EP-001/Q-001].

Who writes this file matters to the choice. The person this tool is for is tidying a messy folder,
not integrating with anything, and they will write the file by hand in a text editor, probably
once, probably a handful of lines. Nothing generates it and nothing consumes it but `tidy`.

## Options considered

**The format.**

- **A — JSON, via `json`.** Cost: punishing to hand-write — every key quoted, no trailing comma,
  no comments — and the one thing a user most wants to do to a rule file, leave a note to
  themselves about why `.csv` goes to `data`, is impossible. Its parse errors do carry a line and
  column. Risk: the format fights the only person who will ever write one.
- **B — INI, via `configparser`.** Cost: everything is a string, so a boundary in days has to be
  converted and validated here rather than by the parser; and `configparser` lowercases option
  names unless `optionxform` is overridden, which would silently turn a destination folder
  `Photos` into `photos`. Both are a few lines. Risk: low — the awkward corners are known and
  each has a one-line remedy.
- **C — TOML, via `tomllib`.** Cost: `tomllib` arrived in Python 3.11, so this raises the floor
  ADR-0001 set at 3.9 [src: ADR-0001]. Risk: it trades a real constraint for a marginally nicer
  syntax, and it would have to be an ADR superseding ADR-0001 rather than a choice made here.

**Where the file comes from.**

- **D — A flag only: `--rules PATH`.** Cost: the user types it on every run. Risk: none to the
  guarantees — nothing affects a run that is not on its command line.
- **E — A default location as well**, such as a `.tidyrules` beside the files being tidied, or one
  under the user's config directory. Cost: a file can change what a run does without appearing
  anywhere the user looked, which is the opposite of what the preview exists to provide
  [src: docs/product/vision.md]. A rule file sitting in a folder you were handed would silently
  redirect your files. Risk: the surprise lands on a tool whose entire promise is that there are
  none.

## Decision

**B and D: one INI file, named with `--rules PATH`, no default location.**

The file has two optional sections, and either may be omitted — what is omitted keeps its
built-in values [src: WI-0003 AC6]:

```ini
# Anything after a # is a comment.
[types]
.csv = data
.xyz = notes

[bands]
newer = current
older = archive
boundary-days = 90
```

Four details are fixed here because each would otherwise be decided silently:

1. **`[types]` keys are extensions, values are one folder name.** A key must begin with `.`; it is
   lowercased on load, which is how the built-in table already matches [src: tidy/rules.py]. A
   value must be a single path component — no `/`, not empty — which keeps a destination path at
   the three components WI-0002 was verified against [src: WI-0002 AC1; src: WI-0003 AC8].
2. **`[bands]` has exactly three keys — `newer`, `older`, `boundary-days` — and the format cannot
   express a fourth band.** That is the point of choosing fixed keys over an ordered list: the
   stakeholder fixed the count at two [src: WI-0003/Q-002], so a rule file asking for three is a
   file naming an option that does not exist, and the error says so. If the section is present,
   all three keys are required; an absent section means the built-in bands.
3. **`boundary-days` is a positive number of days**, the unit `README.md` already states the age
   rule in, and it keeps ADR-0005's half-open comparison — a file whose age is exactly the
   boundary falls in the older band [src: ADR-0005; src: WI-0003 AC5].
4. **`optionxform` is overridden to `str`** so that values and section keys keep the case the user
   typed; extensions are lowercased explicitly on load rather than by the parser, so a destination
   folder named `Photos` stays `Photos`.

**A rejected rule file exits 2, and is rejected before the target folder is examined.** This is
ADR-0006's boundary rule applied unchanged: an event that ends the run before there is a run
belongs to `cli.py`, gets one line on stderr, prints nothing on stdout, and exits 2
[src: ADR-0006; src: tidy/cli.py]. Reading the rule file first also means a mistyped `--rules`
path is reported even when the target folder is unusable too, which is the more useful of the two
messages. The exit vocabulary stays at the three values `README.md` already documents
[src: README.md].

## Consequences

What becomes easy: a user changes one extension by writing two lines and a comment saying why.
The format cannot express a third band, so a whole class of invalid file is unrepresentable rather
than validated. Nothing about a run depends on the filesystem outside the folder named on the
command line, so a run is reproducible from its command line alone.

What becomes harder: everything `configparser` hands back is a string, so `boundary-days` and the
shape of every value are validated in the loader rather than by the parser — that validation is
WI-0003 AC8's six classes and it has to be written [src: WI-0003 AC8]. And a user who wants the
same rules every time types `--rules` every time.

**Reversibility: cheap, and the two halves reverse independently.** Adding a default location
later is additive — a fallback path when `--rules` is absent — and breaks no existing command
line, which is why D was safe to choose first. Changing the format later is one module, the
loader, plus `README.md` and the tests: no data migration, because the only files in the format
are ones users wrote by hand and would have to be told about anyway. The tool writes nothing but
the files it moves, so nothing it writes is in this format [src: tidy/apply.py;
src: docs/architecture/overview.md].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-28T15:15:08Z | plan | WI-0004 | Marked superseded by ADR-0014, in part: option D, "no default location", is replaced on the stakeholder's authorisation. No text below the header was changed - the decision this file records is what was believed on 2026-08-27 |
| 1 | 2026-08-27T21:35:54Z | plan | WI-0003 | First version |

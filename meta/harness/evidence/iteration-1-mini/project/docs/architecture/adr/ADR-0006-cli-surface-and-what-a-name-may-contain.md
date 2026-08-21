---
title: One CLI surface with flag-valued sharers, so a name may contain anything printable
version: 1
status: current
updated: 2026-08-21T02:44:30Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0006 — One CLI surface with flag-valued sharers, so a name may contain anything printable

- **Status:** accepted
- **Date:** 2026-08-21
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`WI-0001`'s `## Deliberately unconstrained` section names one gap and hands it to `plan`
explicitly: what characters a person's name may contain. `refine` left it open on purpose, and
gave the reason — the answer depends on how `WI-0002` will take its list of sharers, which is a
design choice that did not exist yet. If sharers are typed as `--with alice,bob`, then a comma
cannot appear in a name and `WI-0001` must reject it **when the person is added**, not leave
`WI-0002` to discover it later against a roster that already contains one.

That makes this the first decision of the project that must be taken across two items at once,
and it is really two questions with one answer: the shape of the command line, and the rule for a
name.

Constraints already in force: `ADR-0001` fixes the standard library and Python 3.9+, so the
parser is `argparse`. `WI-0001` AC1 requires both roster commands to appear in a top-level
`--help` and requires a non-empty listing to print **one name per line and nothing else**.
`WI-0002` AC2 requires that giving no sharers means everyone, and that an explicit list means
exactly those named (`ADR-0003`).

## Options considered

- **A — Sharers as a repeated flag: `--with alice --with bob`. No delimiter anywhere.**
  Cost: the everyone case is already free (`ADR-0003`: no flag at all), so the extra typing lands
  only on the uncommon explicit case, and it is one short flag per person.
  Risk: low. No character is reserved, so the name rule stays about what can be *displayed*
  rather than about what the parser can survive.
- **B — Sharers as one comma-separated value: `--with alice,bob`.**
  Cost: shorter to type in the explicit case.
  Risk: a comma becomes illegal in a name, forever, in a tool for a friend group where "Bob, Jr"
  and "Anne-Marie, the second" are not absurd. Worse, the constraint originates in `WI-0002` and
  must be enforced in `WI-0001`, so the roster carries a restriction whose reason is invisible
  from where it is applied.
- **C — Sharers as trailing positional arguments: `add-expense 30 --paid-by alice bob carol`.**
  Cost: none in typing.
  Risk: `argparse` handles a variadic positional after optional arguments badly, and the command
  reads ambiguously — it is not obvious that `bob carol` are sharers rather than a two-word
  description. Rejected on legibility, which for this tool is a first-order concern
  (`EP-001/Q-005`).

## Decision

1. **The tool is invoked as `python3 -m expenses <command>`.** Nothing is installed
   (`ADR-0001`), so there is no console-script entry point to rely on.
2. **The commands are:** `add-person NAME`, `people`, `add-expense AMOUNT --paid-by NAME
   [--with NAME]… [--on YYYY-MM-DD] [--for TEXT]`, `expenses`, `settle`. `WI-0001` owns the first
   two; `WI-0002` the next two; `WI-0003` the last. They are listed here together because a CLI
   designed one command at a time is how a tool ends up with three spellings of the same idea.
3. **Sharers are given as a repeated `--with` flag** — option A. No argument value is ever split
   on a delimiter, anywhere in the tool.
4. **A person's name may contain any printable character**, including commas, spaces, digits,
   punctuation and non-ASCII text. `WI-0001` AC1's naming of what is valid therefore reduces to
   two rules and no character blacklist:
   - it must not be empty or only whitespace once surrounding whitespace is stripped
     (`WI-0001` AC7);
   - it must not contain a **control character** — anything below `U+0020`, or `U+007F`.
5. **Rule 4's second half exists for exactly one reason**, and it is worth stating so nobody
   later mistakes it for general hygiene: `WI-0001` AC1 requires the listing to print one name
   per line. A name containing a newline would produce a listing that cannot be parsed back into
   the roster it came from, and a name containing a carriage return or an escape sequence can
   overwrite what a terminal has already drawn — in a tool whose output is read aloud to decide
   who pays whom.
6. **Validation lives in `people.py`**, at the point a person is added, and is not repeated in
   `cli.py`. One rule, one place.

## Consequences

- Easy: `WI-0002`'s sharer parsing, which becomes "collect the values of `--with`" with no
  splitting, no quoting rules and no escape syntax.
- Easy: naming your friends whatever they are actually called.
- Easy: `WI-0001`'s validation, which is now two positive rules rather than an evolving list of
  forbidden characters.
- Hard: typing an explicit sharer list for a large group. Accepted, because `ADR-0003` makes the
  common case require no flag at all, so the cost falls only where the user is deliberately
  naming a subset.
- Hard: nothing about non-ASCII names is *tested* beyond acceptance — no normalisation, no
  case-folding beyond Python's `str.lower()`. `WI-0001` AC3 matches case-insensitively, and
  `str.lower()` is not full Unicode case-folding; for a friend group this is not worth the
  complexity, and it is recorded here so that the limitation is findable rather than surprising.
- **Reversibility: high for rules 1–3, moderate for rule 4.** Changing the command names or
  adding a comma-splitting convenience later is a change to `cli.py` alone. *Narrowing* what a
  name may contain after a roster exists is the expensive direction — an existing person could
  become invalid — which is precisely why the permissive rule is the one chosen first.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-21T02:44:30Z | plan | WI-0001 | First version; settles the gap WI-0001 handed to `plan` under `## Deliberately unconstrained` |

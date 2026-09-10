---
title: An envelope's identity is its trimmed, casefolded name
version: 1
status: current
updated: 2026-09-10T13:44:29Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0004 — An envelope's identity is its trimmed, casefolded name

- **Status:** accepted
- **Date:** 2026-09-10
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

An envelope is identified by its name and by nothing else, so "is this the same envelope?" is
asked on every command, and it decides whether a capitalisation slip silently creates a second
pot and puts spending in the wrong one.

The stakeholder settled the substance: two names differing only in case are one envelope
[src: WI-0001/Q-002], the capitalisation an envelope was created with is what comes back
[src: WI-0001 AC7 "an envelope is listed back with the capitalisation it was created with"], and
surrounding whitespace is stripped before names are compared
[src: WI-0001 AC11 "a name is compared and stored with leading and trailing whitespace removed"].
The last of those is an assumption the pipeline took under no licence and wrote as a criterion so
it would be visible [src: WI-0001].

What is left is the mechanism, and it is a decision because "differing only in case" has more
than one implementation in Python and they do not agree on every string.

## Options considered

- **A — `name.strip().lower()`.** Cost: negligible. Risk: `str.lower` is defined per character and
  leaves pairs that a reader would call the same word in different case as different keys — the
  German sharp s is the standard example, where `"STRASSE".lower()` and `"straße".lower()` differ.
  Two envelopes, one word.
- **B — `name.strip().casefold()`.** Cost: the folded form is not a name and is unsafe to
  display, so the store has to keep the display form separately. Risk: `str.casefold` is
  designed for caseless matching and handles the pairs `str.lower` does not.
- **C — `unicodedata.normalize("NFC", name).strip().casefold()`.** Cost: a normalisation step,
  and a rule about which form the store holds. Risk: it settles a question nobody has asked —
  whether an accented letter typed as one character and as a letter plus a combining mark are the
  same envelope — and settling it here means `implement` writes code that this item's criteria
  do not exercise.

## Decision

Option B. An envelope's **identity** is `name.strip().casefold()`. Its **display form** is
`name.strip()` as first created, and that is what is stored and what is printed.

Three rules follow, and code can be checked against each:

1. Two names are the same envelope exactly when their identities are equal. Creating a name whose
   identity already exists is refused, and the message names the **stored** envelope rather than
   what was typed — `envel new Groceries` after `envel new groceries` must put `groceries` on
   stderr [src: WI-0001 AC5 "The same holds when the second invocation differs only in case"], and
   echoing the input would put `Groceries` there instead.
2. A name whose identity is empty is refused. That covers the empty string and a name of spaces
   with one rule rather than two.
3. Identity is computed at the boundary, once, from what the person typed. Nothing downstream
   folds a name a second time.

## Consequences

- The stored display form is the trimmed name, so `  groceries  ` and `groceries` are one
  envelope and the stored form of both has no surrounding space.
- Unicode normalisation is **not** applied. A name typed with a combining accent and the same
  name typed with a precomposed character are therefore different envelopes. No criterion covers
  it, no observation in this item can show it, and deciding it here would be deciding past what
  was asked. It is written down so that the next person to meet it knows it was seen rather than
  missed.
- **Reversing this is cheap while the store is small**, and gets expensive later. Changing the
  fold — to `lower`, or to add a normalisation step — is one function in one module today. Once a
  real store holds envelopes whose identities collide under the new rule, the change owes a
  migration that decides which of two envelopes wins, and that is a question only the person whose
  money it is can answer.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-10T13:44:29Z | plan | WI-0001 | First version: identity is the trimmed casefolded name, display form is the trimmed name as created, and Unicode normalisation is deliberately not applied |

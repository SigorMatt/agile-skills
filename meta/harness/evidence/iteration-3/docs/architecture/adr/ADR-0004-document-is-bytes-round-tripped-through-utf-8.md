---
title: The document is read and written as bytes, round-tripped through UTF-8 with surrogateescape
version: 1
status: current
updated: 2026-08-28T18:53:01Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0004 — The document is read and written as bytes, round-tripped through UTF-8 with surrogateescape

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

WI-0001 makes four promises about bytes that the obvious way of reading stdin in Python breaks.

Reading `sys.stdin` in Python's default text mode applies universal newlines, so a document whose
lines end `\r\n` arrives with `\n` and is written back with `\n`. That breaches AC9
[src: WI-0001 AC9], and because AC4 and AC5 are stated as byte equality it breaches those too on
any CRLF document [src: WI-0001 AC4; src: WI-0001 AC5].

Default text mode also decodes using the locale encoding, which is not UTF-8 everywhere, and it
raises on input the encoding cannot represent. The tool has to handle CJK text and emoji
[src: WI-0001 AC3], and it promises to reproduce lines outside a table byte-for-byte
[src: WI-0001 AC4] — including lines it does not understand, which is the whole shape of
[src: ADR-0003]. A document that is not valid UTF-8, or is not text at all past line 40, still
has to come out the other side unchanged.

Separately, the criteria talk about "a line" in several places that would be wrong if the line
terminator were part of it. AC11 strips leading and trailing *spaces* from a cell, and `\r` is
not a space; AC14 tests whether the last non-whitespace character of a row is an unescaped `|`
[src: WI-0001 AC11; src: WI-0001 AC14]. Refinement round 2 closed this by ruling that a line's
terminator is not part of the line [src: WI-0001 AC9], which the implementation now has to
realise somewhere specific.

## Options considered

- **A — Read `sys.stdin.buffer`, decode UTF-8 with `errors="surrogateescape"`, split terminators
  off explicitly, and write back through `sys.stdout.buffer` with the same codec.** Cost: two
  extra lines at each end of the pipeline, and a splitting rule that has to be written and
  tested rather than inherited from `str.splitlines`. Risk: low. `surrogateescape` maps each
  undecodable byte to a lone surrogate and maps it back to the identical byte on encode, so any
  byte sequence round-trips; the tool measures widths on text and copies bytes it cannot read.
- **B — Read `sys.stdin` in text mode with `newline=""` and `encoding="utf-8"`.** Cost: nothing;
  it is one argument. Risk: `newline=""` preserves terminators but leaves them inside the
  strings `str.splitlines` returns, so the terminator problem above is not solved, only moved;
  and strict UTF-8 decoding raises on input the tool has promised to reproduce.
- **C — Work entirely in bytes, never decoding.** Cost: the width rule of [src: ADR-0002] is
  defined over characters and their Unicode properties, so it would have to decode each cell
  anyway. Risk: the decode would then happen in the middle of the layout code, in more places,
  with no single decision about what to do when it fails.
- **D — Decode strictly and exit non-zero on invalid input.** Cost: nothing to build. Risk:
  contradicts the epic, which puts diagnostics out of scope and promises the document back
  [src: EP-001]; and it makes the tool refuse a file a text editor would happily show.

## Decision

The document is read from `sys.stdin.buffer` as bytes and decoded once with UTF-8 and
`errors="surrogateescape"`. It is written to `sys.stdout.buffer` as bytes, encoded with UTF-8 and
`errors="surrogateescape"`. Nothing between those two points touches a file object
[src: tracker/items/WI-0001/artifacts/plan.md].

Immediately after decoding, the text is split into a list of `(content, terminator)` pairs, where
`terminator` is `"\r\n"`, `"\n"`, or `""` for a final line with no terminator, and `content`
contains no terminator characters. Every rule in the item — width, cell splitting, prefix
comparison, delimiter detection, fence detection — is defined over `content` alone. Output is
reassembled by concatenating each line's (possibly rewritten) content with its own original
terminator, which is what makes AC9 fall out of the data structure rather than out of care
[src: WI-0001 AC9].

A checkout of this repository has no `sitecustomize`, no locale dependency and no environment
variable that changes any of the above: the encoding is named in the call, not inherited.

## Consequences

What becomes easy: AC4, AC5 and AC9 become properties of the reader and writer rather than
obligations on every code path in between. A document with mixed `\n` and `\r\n` endings keeps
each line's own ending without any rule being written for it. Binary junk in the middle of a
markdown file passes through untouched, so the tool cannot corrupt a file it was pointed at by
mistake.

What becomes hard: display width is computed over text containing lone surrogates when the input
was not valid UTF-8. A surrogate has no East Asian Width property that means anything, so it
falls to rule 3 of [src: ADR-0002] and counts as one column. That is arbitrary, and it is
acceptable only because such a cell is inside a table the tool would have to have recognised
first — a case nobody has asked for. It is named here so a later reader finds it as a known
limitation rather than as a bug.

Also: because terminators are split off, no part of the layout code may use `str.splitlines`,
which would silently reintroduce the problem this ADR exists to prevent. The plan states this as
a constraint on the implementation [src: tracker/items/WI-0001/artifacts/plan.md].

**Reversibility: high.** The decision is confined to two functions at the edges of the program
and one data structure between them. Changing the codec, or the error handler, is a change in
`mdtab/textio.py` and its tests; nothing downstream of the split sees an encoding at all
[src: docs/architecture/overview.md].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-28T18:53:01Z | plan | WI-0001 | First version, recording how the document is read, split and written |

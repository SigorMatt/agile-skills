---
title: A fixture that is deliberately not valid UTF-8 carries a .bin extension
version: 1
status: current
updated: 2026-08-28T19:32:15Z
updated-by: answer-questions
updated-for: WI-0001
---

# ADR-0006 — A fixture that is deliberately not valid UTF-8 carries a `.bin` extension

- **Status:** accepted
- **Date:** 2026-08-28
- **Decided by:** answer-questions (architect), for WI-0001
- **Supersedes:** —

## Context

[src: ADR-0005] decided that document fixtures live under `tests/fixtures/` as
`<name>.in.md` and `<name>.out.md` pairs, and that "Fixtures are the only place a test may
express a document; a test may not build one from a Python literal". It named this exact case as
one it expected to handle: "Cases that cannot be written as literals at all, such as a file whose
last line has no terminator or one containing invalid UTF-8, become ordinary fixtures."

AC9 needs such a document [src: WI-0001 AC9]: mdtab decodes with `surrogateescape`
[src: ADR-0004], and the only way to demonstrate that a byte no UTF-8 decoder accepts survives
the round trip is to feed it one. `review-close` made it a must-fix that this document stop
being a Python literal [src: tracker/items/WI-0001/artifacts/review.md].

Writing it as `tests/fixtures/invalid-utf8.in.md` does not work, and the reason was not
foreseeable when [src: ADR-0005] was written. `validate-workspace` walks every `.md` file in
the project that is not git-ignored and not under `.git`, `__pycache__`, `.claude` or
`node_modules`, opens it with `encoding="utf-8"` to check citation provenance, and catches
only `OSError`. A `0xFF` byte in such a file therefore aborts the whole validator with a
`UnicodeDecodeError` traceback rather than producing a finding
[src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 1, UnicodeDecodeError:
'utf-8' codec can't decode byte 0xff in position 12]. `workspace-valid` is a hard gate of every
skill in the pipeline, so this is not a cosmetic collision: with that file present, no skill can
run at all. It was isolated by moving the pair out of the tree and back
[src: WI-0001/Q-004].

So the constraint is: the document must be a fixture file [src: ADR-0005], and it must not be a
`.md` file [src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 1,
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 12].

## Options considered

- **A — the non-UTF-8 pair carries `.bin`; everything else keeps `.md`; discovery keys on the
  `.in.` infix rather than the `.md` suffix.** Cost: `tests/fixtures/` is no longer
  uniformly `.md`, and a reader has to know why one pair differs — which is what this ADR is
  for. Risk: low. Nothing outside `tests/` changes; `.gitattributes` already marks
  `tests/fixtures/**` as `-text -diff`, so the extension does not affect how git treats it
  [src: tracker/items/WI-0001/artifacts/plan.md].
- **B — every fixture becomes `.bin`, so the directory stays uniform.** Cost: renaming
  twenty-two pairs and losing markdown syntax highlighting on documents that genuinely are
  markdown. Risk: the fixtures are the most-read artifacts in the test suite, and making the
  readable ones less readable to spare one sentence of explanation is the wrong trade.
- **C — patch `validate-workspace` to skip files it cannot decode.** Cost: none to this
  project's artifacts, and the change is one identifier wide. Risk: it edits the pipeline's own
  machinery from inside a work item. The patch would live in this repository's copy of the
  toolkit, would be lost on the next install, and is not something a reviewer of mdtab can
  audit or a criterion covers. The underlying defect is real and is reported separately; fixing
  it is not this project's work.
- **D — keep the document as a Python literal in the test and declare the deviation.** Cost:
  nothing up front. Risk: it leaves [src: ADR-0005]'s rule broken in the one place the rule was
  written for, and `review-close` already rejected the item for exactly this, declared or not.
- **E — drop the undecodable-bytes case.** Cost: nothing. Risk: AC9's other two clauses have
  fixtures, but the `surrogateescape` half of [src: ADR-0004] would have no evidence behind it
  at all. A coverage loss nobody asked for.

## Decision

A document fixture whose bytes are valid UTF-8 keeps `<name>.in.md` and `<name>.out.md`. A
document fixture that is **deliberately not valid UTF-8** uses `<name>.in.bin` and
`<name>.out.bin` instead. Both halves of a pair carry the same extension.

`tests/test_fixtures.py` discovers pairs by the `.in.` infix rather than by the `.md`
suffix, so a pair in either form is picked up by every fixture-wide test — the round trip, AC6
idempotence, AC11 and AC14 — without being registered a second time
[src: tracker/items/WI-0001/artifacts/plan.md].

This narrows one clause of [src: ADR-0005] and reverses none of it. The decision
[src: ADR-0005] actually weighed — `unittest` over `pytest`, file fixtures over inline
literals, `compileall -W error` as lint — is untouched, and its rule that a test may not build
a document from a Python literal is what this ADR exists to make executable. The extension was
fixed in passing there and is not among the options that ADR compared, which is why this is an
amendment recorded in [src: ADR-0005]'s change log rather than a supersession.

The extension is `.bin` and not something else because it states the fact that matters: these
bytes are not text, so a tool that walks a repository looking for documents has no reason to open
them as text. That is the property the collision above turned on
[src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 1, UnicodeDecodeError:
'utf-8' codec can't decode byte 0xff in position 12].

## Consequences

What becomes easy: the AC9 undecodable-bytes document becomes an ordinary fixture pair like every
other, and the rule "fixtures are the only place a test may express a document" holds without
exception. Any future fixture that needs bytes no decoder accepts — a lone surrogate, a truncated
multi-byte sequence, a BOM in the wrong place — has a home and needs no further decision.

What becomes hard: `tests/fixtures/` stops being uniformly `.md`, so a contributor adding a
fixture has to know which extension to use [src: tracker/items/WI-0001/artifacts/plan.md]. The
rule is mechanical — can the bytes be decoded as UTF-8? — and it is stated in
`tests/test_fixtures.py`'s module docstring as well as here.

The toolkit defect this decision routes around is not fixed by it. `validate-workspace` still
crashes with a traceback rather than reporting a finding when it meets a `.md` file it fails to
decode [src: run: python3 .claude/agile-skills/scripts/validate-workspace . → exit 1,
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 12], and a project that has
one for any other reason — a sample document, a fuzz corpus, a
deliberately corrupt attachment — will hit it. That belongs to whoever maintains the toolkit and
is recorded in this item's journal and in `HARNESS-STATUS.md`; it is not mdtab's work and no
acceptance criterion covers it.

**Reversibility: high.** Reversing this is renaming two files and changing one expression in
`tests/test_fixtures.py`. No production module knows the fixture layout: `mdtab/` contains no
reference to `tests/` at all [src: run: grep -rn "tests" mdtab/ → no match], so nothing that
ships is affected either way.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-28T19:32:15Z | answer-questions | WI-0001 | First version, deciding `.bin` for fixtures that are not valid UTF-8, in answer to WI-0001/Q-004 |

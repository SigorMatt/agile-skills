# Iteration 5 — `envel`, abandoned at a `validator-failed` stop

This run was **abandoned, not ended.** It stopped at turn 11 with `stop-reason: validator-failed`,
mid-`WI-0002`, and was not resumed. There is no ending here: no E1, no E2, no sign-off, no
`review-close`, and **no retro** — `retro` never ran, so this directory contains no retro artifact.
Anything that reads this trail looking for an ending will find the run cut off before one.

```
status       'stopped'
stop-reason  'validator-failed'
stop-detail  'validate-workspace exits 1: validate-workspace: 1 error, 0 warnings'
turn         11
next-role    'worker'
```

The run was launched as the **held-out calibration engagement** for `ROADMAP.md` §4 step 1 —
E2 plus the held-out retro calibration. **It did not produce that calibration.** The retro was
never written, so the first honest recall number is still unmeasured and step 1 is still owed.

## Why it stopped

`verify` on `WI-0002` found four `[src: <path>:<line>]` citations in `ADR-0005`, `ADR-0007` and
`ways-of-working.md` that its own item's edits had falsified. It classified the finding, filed
`Q-005` to the architect, and wrote its history row. That row is what killed the run:

```
tracker/items/WI-0002/history.md:14: ERROR [claim.citation.unresolved] 'path:line' is not a citation form this gate can check (spec/doc-header.md, the citation forms table)
```

The string the gate refused is `[src: path:line]` — and **it is not a citation.** It is the
skill naming the citation *form*, in prose, to describe the class of four real citations it had
just found wrong. The resolver takes everything before the first `:` as a path, finds `path` has
no `/` and no `.`, and reports a citation that does not resolve.

The same execution wrote the same placeholder three times. The scanner masks code spans, so a
backticked marker is not read as a citation. Two were backticked; one was not:

```
tracker/items/WI-0002/history.md:14  BARE (parsed -> ERROR)
tracker/items/WI-0002/journal.md:847  BACKTICKED (masked -> passes)
tracker/items/WI-0002/journal.md:881  BACKTICKED (masked -> passes)
```

One skill execution, one phrase, two renderings, opposite verdicts. The run died on the
punctuation of a sentence *about* citations, not on a citation.

`verify`'s own journal entry records `validate-workspace` **green** while the turn ran —
`exit 0`, `0 errors, 0 warnings` — because the fatal row was written after its last validation.

## What this is the proof for

This directory is the evidence behind the findings filed from it. The three things it shows,
each checkable in the files here rather than in this summary:

1. **A gate cannot tell a citation from a mention of one, and the workspace record is scanned
   for citations.** A skill whose job is to report on citations has no safe way to name the form
   in a history row.
2. **The escape exists and is documented only in the code that enforces it.** The masking rule
   is stated in one place in the whole installed workspace: a source comment in
   `validate-workspace` citing F-037. `grep -rn "citation form" .claude/` returns seven hits —
   two spec files and the validator's own source — and **none in `.claude/skills/`**, the nine
   skills a worker actually reads. `verify`'s four pointers into `doc-header.md` name §5 and §4a;
   never the citation-forms table.
3. **A `validator-failed` stop can be caused by the record's prose rather than by the work.**
   All nineteen of `WI-0002`'s acceptance criteria passed, all seven binding ADRs conformed, and
   69 tests were green on the branch head when the run died.

## Layout

- `tracker/` — the workspace tracker as it stood at the stop, including the fatal
  `items/WI-0002/history.md` and the `verify` journal entry that explains it.
- `docs/` — the product, architecture and process documents, including the three whose citations
  `verify` found falsified.
- `run/` — `state.json`, `SIM-LOG.md`, `iteration-log.jsonl`, `driver-console.log`.

Per-turn `*.stream.jsonl` transcripts are **deliberately not banked**: they are large, they are
not the record, and an evidence directory nobody can read is not evidence.

This directory is read-only history. Corrections to anything stated here belong in the findings
ledger, not in these files.

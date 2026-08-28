---
id: BUG-0006
type: bug
title: "ADR-0008 cites tidy/cli.py:52, which is a blank line"
status: done
priority: low
epic: EP-001
created: "2026-08-27T21:12:51Z"
updated: "2026-08-28T14:11:01Z"
found-in: BUG-0003
arose-from: BUG-0004
branch: wi/BUG-0006
outcome: delivered
---

## Summary

`docs/architecture/adr/ADR-0008` line 48 supports a sentence with `[src: tidy/cli.py:52]`, and
line 52 of `tidy/cli.py` is a blank line. The sentence is the decisive risk in option A of that
ADR — "under WI-0003 the tables in force are the *user's*, and `build_parser` runs before
`parse_args` has told anyone where the user's rules came from" — and the statement it means is
`args = build_parser().parse_args(argv)`, now at `tidy/cli.py:54`.

The claim itself is still true; only its pointer is wrong. `scripts/lint-claims` passes, because
`spec/doc-header.md` §4a makes `path` and `path:line` one citation form with one test — that the
file exists — so no gate catches a line number that has drifted. What breaks is the Definition of
Done's own D12 procedure, which says to open what a sentence cites and decide from what is there:
a reviewer auditing ADR-0008 lands on a blank line and cannot confirm the claim from its citation.

Established by running, not inferred: the citation was exact when the ADR was written, and
BUG-0003's own implementation commit two commits later is what moved it.

```
$ git show b76b27c:tidy/cli.py | sed -n '52p'      # ADR-0008 written here
    args = build_parser().parse_args(argv)
$ git show 46e5fd0:tidy/cli.py | sed -n '52p'      # BUG-0003's cli change
                                                    (blank)
```

`found-in: BUG-0003` names the item that wrote the ADR and then moved the line, in that order,
within one item's own branch. `arose-from: BUG-0004`, whose review found it: BUG-0004/Q-002 is
the same class of drift in ADR-0009, answered by making those citations file-level, and this is
the one `path:line` citation in `docs/` that survived that sweep.

## Steps to reproduce

Run from the repository root, on `main` (the file is unchanged by any open item).

1. Read the claim and its citation:

   ```
   grep -n "src: tidy/cli.py:52" docs/architecture/adr/ADR-0008-help-text-is-prose-guarded-by-a-test.md
   ```

2. Open what it cites, and the two lines after it:

   ```
   grep -n "" tidy/cli.py | sed -n '52,54p'
   ```

3. Confirm no gate objects:

   ```
   python3 .claude/agile-skills/scripts/lint-claims .
   ```

## Expected behaviour

A reader who follows the citation in step 1 arrives at something that supports the sentence.
ADR-0009 v2 records the rule this project chose for exactly this case, in its `## Consequences`:
"an ADR about a change to a file cites that file, and the change is what moves its own line
numbers", with the named symbols in the prose carrying the precision. Applying that rule here
means `[src: tidy/cli.py]`, with `build_parser` and `parse_args` already named in the sentence.

Whether that is the right remedy for ADR-0008 specifically — versus repointing to `:54`, versus
leaving it and pinning line numbers with a lint — is for `plan`. Superseding or amending an ADR
is not `review-close`'s to decide, which is why this is an item rather than an edit.

## Actual behaviour

```
$ grep -n "src: tidy/cli.py:52" docs/architecture/adr/ADR-0008-help-text-is-prose-guarded-by-a-test.md
48:  `parse_args` has told anyone where the user's rules came from [src: tidy/cli.py:52], so generated

$ grep -n "" tidy/cli.py | sed -n '52,54p'
52:
53:def main(argv=None):
54:    args = build_parser().parse_args(argv)

$ python3 .claude/agile-skills/scripts/lint-claims .
lint-claims: 0 errors, 0 warnings
```

Line 52 is blank. The cited statement is two lines below, in a different function from the one
line 53 opens.

## Acceptance criteria

- [x] AC1 — The citation on `ADR-0008` line 48 resolves to something that supports the sentence
      it is attached to. Checkable by the steps above: whatever the citation names, opening it
      shows the reader `build_parser` being called before `parse_args` has run, or the file in
      which that happens. A citation pointing at a blank line fails this.
- [x] AC2 — No `path:line` citation anywhere in `docs/` points at a line that does not support its
      sentence. Checkable: `grep -rn "src: [a-z/]*\.py:[0-9]" docs/` lists every one, and each
      surviving entry is opened and read. There are three today — `ADR-0008:48` and `ADR-0009`'s
      two `tidy/cli.py` citations at lines 23 and 106; the latter two are exact and must stay so.
- [x] AC3 — `ADR-0008`'s frontmatter carries the version bump and its change-log table carries a
      row saying what changed and for which item, per `spec/doc-header.md` §3. Checkable by
      reading the file: `version: 2` and a row naming BUG-0006.
- [x] AC4 — `python3 .claude/agile-skills/scripts/lint-claims .` still exits 0, and
      `python3 -m unittest discover -s tests -t . -q` still exits 0. Checkable by running both.

## Notes

**The regression-test criterion a bug normally carries is deliberately absent, and this is the
record of why**, per `spec/work-item.md` §3 ("required unless the item's `## Notes` records why
the behaviour cannot be tested"). The defect is in a prose document, not in `tidy/`; there is no
behaviour to pin. The nearest thing to a test is AC2's sweep above, which is a check a reader
performs, not code this project runs — and building a line-number lint into `.claude/agile-skills/scripts/`
is not this project's to do, since the toolkit is outside `EP-001`'s scope.

That gap is worth naming precisely: after this item, nothing prevents the next code edit from
re-breaking any `path:line` citation that survives. The durable remedy is the rule ADR-0009 v2
already records — cite the file, name the symbol — and applying it to the whole of `docs/` is
what AC1 and AC2 together amount to.

Filed by `review-close` while reviewing BUG-0004, from the D12 citation sweep
(`grep -rn "planner\.py:[0-9]\|cli\.py:[0-9]\|apply\.py:[0-9]\|rules\.py:[0-9]" docs/`) rather
than from a report. BUG-0004's own two findings were about `ADR-0006` and `ADR-0009` and were
answered before this review resumed; this one belongs to neither, and BUG-0004's merge does not
touch `tidy/cli.py` at all.

`answer-questions` looked at this citation once, on 2026-08-27, while answering BUG-0004/Q-002,
and recorded in BUG-0004's journal that "ADR-0008's `[src: tidy/cli.py:52]` is still exact". It
is not, and the disagreement is worth stating rather than papering over: that check was run as
`sed -n '52p' tidy/cli.py`, which prints a blank line and is easy to read as agreement when the
expected content is not held alongside it. `grep -n "" file | sed -n '52p'` prints the number
with the line and does not have that failure mode, which is why the steps above use it.

**Two things a later reader should know, added by `review-close` when this item was closed.**

*This item's own reproduction steps stopped reproducing before it was built.* `## Steps to
reproduce` and `## Actual behaviour` above say `tidy/cli.py:52` is blank and the cited statement
is at `:54`. That was true when the item was filed at `f459e72`; WI-0003 merged fifty-seven
minutes later at `82a7d26` and moved everything. On `main` at closing, line 52 is
`    """The stdout line for one action."""` and the statement is at `:62`. The defect was real and
larger than recorded — a docstring inside `render` looks like supporting code in a way a blank line
does not. The text is left as filed on purpose: it is the record of what `review-close` saw on
2026-08-27, and rewriting it would erase the evidence rather than update it.

*One finding examined at review and deliberately not actioned.* `ADR-0009`'s `## Decision` says
"only a `"failed"` outcome from `apply_plan` makes the process exit non-zero". That is true of the
apply leg its paragraph is about, and false if the clause is quoted alone: `tidy/cli.py` also
returns 2 at lines 76, 80 and 90 for the ways a run cannot start. It is not this item's defect —
the clause is ADR-0009 v1 prose and this item only re-pointed its citation — and it is not left
unguarded: `ADR-0012` is `status: current`, cites ADR-0009 by name, and settles all three exit
statuses, as does `README.md`. Recorded here rather than as a bug so that anyone who later reads
that clause out of context has somewhere to land. The reasoning is in `artifacts/review.md`
`## Findings`.

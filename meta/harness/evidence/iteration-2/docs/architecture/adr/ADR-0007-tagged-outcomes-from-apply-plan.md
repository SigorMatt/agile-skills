---
title: apply_plan returns a tagged outcome per action, so the CLI can tell a failure from a fallback
version: 2
status: current
updated: 2026-08-27T20:11:11Z
updated-by: answer-questions
updated-for: BUG-0002
---

# ADR-0007 — `apply_plan` returns a tagged outcome per action, so the CLI can tell a failure from a fallback

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for BUG-0002
- **Supersedes:** —

## Context

ADR-0003 gave `apply.py` two ways to move a file: `os.link` + `os.unlink` as the primary path, and
`_move_without_a_link` — a `lexists` check then `shutil.move` — as the fallback for a filesystem
that refuses hard links. ADR-0003 treats those two as *different guarantees of the same success*:
`FileExistsError` gets "the process exits non-zero", and the fallback is described separately, with
no such clause, as the weaker guarantee that "still satisfies the criterion" [src: ADR-0003].

The code cannot express that distinction. `apply_plan` returns `list[str]` — one message per action
that "did not complete" — and the fallback's note goes into the same list [src: tidy/apply.py].
`cli.main` ends with `return 1 if failures else 0` [src: tidy/cli.py], so a run in which every file
moved by the fallback exits 1. Reproduced with `os.link` patched to raise `OSError(18)`
[src: run: python3 nolink.py /tmp/bug2repro/nolink → EXIT: 1, both files at their destinations;
src: BUG-0002].

The distinction has to live in `apply.py`, because that is the only layer that knows *which route*
a move took. It cannot live in `cli.py` without `cli.py` re-deriving it, and it cannot live in
`planner.py`, which by ADR-0002 knows nothing about execution [src: ADR-0002].

One property of the current output is worth keeping. Messages are emitted in action order, so a run
with both a genuine failure and a fallback prints them interleaved with the file order the stdout
move lines use [src: run: python3 nolink.py /tmp/bug2repro/mixed → EXIT: 1, the `doc.pdf` failure
line before the `photo.jpg` fallback line]. BUG-0002 AC2 asks that only the exit status change
[src: BUG-0002 AC2], which makes that ordering something to preserve rather than to trade away.

## Options considered

- **A — one ordered list of tagged `Outcome` records.** `apply_plan` returns
  `list[Outcome]`, `Outcome` being a frozen dataclass of `kind` and `message`, appended in action
  order exactly where a message is appended today. Cost: one small type in `apply.py`, and the two
  existing assertions that index into the returned list must read `.message`. Risk: low — the empty
  list keeps its present meaning, so the tests that assert `== []` are unaffected.
- **B — two lists, `(failures, notes)`.** The shape BUG-0002's `## Notes` suggests
  [src: BUG-0002]. Cost: every caller and every test that compares the return value changes, `== []`
  becomes `== ([], [])`, and the two lists must be printed one after the other, which regroups
  stderr away from action order. Risk: a third outcome kind changes the signature again, and the
  two lists can silently drift out of step because nothing relates an entry in one to an entry in
  the other.
- **C — keep `list[str]` and classify in `cli.py` by matching the message text.** Cost: none in
  `apply.py`. Risk: the exit status becomes a function of prose. Editing a message — which AC2
  explicitly protects, and which a future item may want to reword — would change the exit code, and
  nothing would fail loudly when it did.
- **D — `apply_plan` returns the exit status it thinks the run deserves.** Cost: none. Risk: it
  puts a presentation decision in the layer ADR-0002 reserves for execution; `cli.py` owns exit
  codes and `apply.py` owns moving files [src: ADR-0002].

## Decision

`tidy/apply.py` gains a frozen dataclass:

```
Outcome(kind: str, message: str)
```

`kind` is one of exactly two strings, matching the `Action.kind` idiom in `planner.py`
[src: tidy/planner.py]:

- `"failed"` — the action did not complete. The file is where it was, or (in the `os.unlink` case)
  it reached its destination and the original could not be removed. This is the set of messages
  that today makes the process exit non-zero, unchanged.
- `"fell-back"` — the action completed by ADR-0003's fallback: the file is at its destination, and
  the run is saying so because the guarantee it holds under is the weaker one [src: ADR-0003].

`apply_plan(folder, actions)` returns `list[Outcome]`, appended in action order. It appends nothing
for a move that completed by the primary path, so an empty list keeps its current meaning: every
action completed, by `os.link` + `os.unlink` [src: tidy/apply.py; src: BUG-0002 AC1].

`cli.main` writes every outcome's `message` to stderr in list order, with the `tidy: ` prefix and
the wording unchanged [src: BUG-0002 AC2; src: tidy/cli.py], and ends with:

```
return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0
```

## Consequences

What becomes easy: the exit status now says what ADR-0003 always said it should, and the two things
that were conflated are separable at every later call site. Adding a third kind of thing worth
reporting — a note that is not a failure — is an entry in the `kind` vocabulary rather than another
signature change.

What becomes hard: `apply_plan`'s return value is no longer printable as-is. Anything reading it
must go through `.message`, and a caller that treats the list as truthy-means-failure is now wrong
in a way it was not before. There is one caller in the package — `cli.py`, which this ADR changes —
and `tests/test_apply.py` calls it directly as well [src: tidy/cli.py; src: tests/test_apply.py].

This does not supersede anything. ADR-0003's decision is unchanged — this is the code being brought
into line with it rather than the decision moving. Two earlier sentences describing the old return
type become historical statements of what was true when they were written: ADR-0002 §2's
"`apply_plan(folder, actions)` ... executes an action list it is given" is still exactly true
[src: ADR-0002], and ADR-0006's parenthetical that `apply_plan` returns "a message per action that
did not complete" was true at ADR-0006's date and is left as written, per `spec/doc-header.md` §4
[src: ADR-0006].

Reversibility: **cheap.** One dataclass, one loop in `apply.py`, one line in `cli.py`, and the
assertions that read `.kind` and `.message`. The only caller in the package is `cli.py`;
`tests/test_apply.py` imports `apply_plan` as well and reads the type, so reversing means those
assertions too — which is the cost Option A already accounted for. Nothing else sees it and no
file on disk records it [src: tidy/cli.py; src: tests/test_apply.py; src: tidy/apply.py]. What
would be expensive to reverse is not this shape but the *behaviour*: a successful apply exiting 0
is what `README.md`'s exit-status contract already promises, so going back to exit 1 would be
changing the promise, not the code.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-27T20:11:11Z | answer-questions | BUG-0002 | Answering BUG-0002/Q-002: the reversibility paragraph said `apply_plan` is imported only by `cli.py`, and `tests/test_apply.py` imports it too — as Option A in this same ADR already noted. Corrected it there and in the same section's "there is one caller", which was wrong the same way; the decision and its cheap-to-reverse verdict are unchanged |
| 1 | 2026-08-27T19:46:29Z | plan | BUG-0002 | First version |

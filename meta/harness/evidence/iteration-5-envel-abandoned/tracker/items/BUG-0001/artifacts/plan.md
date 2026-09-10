# Plan — BUG-0001 A non-ASCII envelope name is refused with a traceback under a non-UTF-8 locale

## Problem

Under a locale that is not UTF-8 — `LC_ALL=C` with PEP 538 coercion and UTF-8 mode both disabled —
`envel` ends two of its call paths in an unhandled `UnicodeEncodeError` and a Python traceback
instead of doing the work or refusing with an `envel:` message. The person affected is the one who
was told the characters in an envelope name would not be restricted (`WI-0001/Q-002`), and the
constraint is that this must be fixed without changing the store's format, without adding a
dependency (`ADR-0001`), and without touching how an envelope is identified (`ADR-0004`).

**This plan corrects the item it implements, in one particular.** `BUG-0001`'s
`## Steps to reproduce` step 3, its `## Summary` and its `## Notes` all state that only the write
path fails and that `envel list` under the same locale succeeds against a store already holding
`café`. That is not so. This execution ran it:

```
$ PATH="$PWD/bin:$PATH" ENVEL_FILE="$T/s.json" envel new "café"          # normal locale → exit 0
$ env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 LC_ALL=C LANG=C \
      PATH="$PWD/bin:$PATH" ENVEL_FILE="$T/s.json" envel list
Traceback (most recent call last):
  ...
  File ".../envel/cli.py", line 82, in _list
    print(name)
UnicodeEncodeError: 'ascii' codec can't encode character '\xe9' in position 3: ordinal not in range(128)
```

Exit status 1. There are therefore **two** unhandled sites, not one: the write in the store, and
the print in the command layer. The item's acceptance criteria are unaffected and none is amended
here — AC3 already requires that `envel list` afterwards exits 0, which under the accept-and-store
decision below cannot hold unless the print path is fixed too. The item's prose is wrong and
`plan` has no authority to rewrite it; it is corrected here, and whoever next has that authority
can carry it into the item.

## Approach

The two failures are one problem seen twice: text crosses this process's boundary in an encoding
the program does not control, and the program treats what arrives as if it were text. `ADR-0005`
records the decision. In outline:

- **In.** An argument is recovered at the boundary — put back through the interpreter's own
  filesystem encoding and re-read as UTF-8 — so that the rest of the program holds characters
  rather than bytes wearing a `str`. Under a UTF-8 locale this is the identity function.
- **Refuse rather than guess.** Bytes that do not decode as UTF-8 produce an `envel:` message on
  stderr and a non-zero status, in the shape every other refusal in `envel/cli.py` already takes.
- **Out.** stdout's error handler is set so a character the locale cannot represent prints as an
  escape and the command exits 0, instead of raising. stderr already behaves this way and is not
  touched.
- **Depth.** The store's write turns an encoding failure into `store.StoreError`, so that no path
  out of that module ends in a traceback even if a future caller skips the boundary.

The boundary is `envel/cli.py`. `envel/envelopes.py` and the domain rules learn nothing about
locales, and the one-way dependency the overview records is unchanged.

## Steps

1. **Add the recovery helper to `envel/cli.py`.** A module-level function taking one `str` from
   `argv` and returning a `str`: it encodes with `os.fsencode` and decodes the result as UTF-8,
   raising a new module-level exception type when that decode fails. Afterwards `envel/cli.py`
   imports `os` and exports the helper's name in `__all__`. No other module changes in this step.

2. **Use it on every argument that reaches a command.** In `main`, the argument list is recovered
   before dispatch — command word and operands alike — and a failed recovery prints an `envel:`
   message on stderr naming what could not be read and returns `REFUSED` (1), the status the
   module already uses for a refusal the person can act on. Afterwards `envel new "café"` under the
   broken locale reaches `envelopes.add` with `café` as four characters plus an accented one, and
   `envel spend $'\xff'` refuses with an `envel:` line and no traceback.

3. **Set stdout's error handler in `main`, before anything is printed.** stdout is reconfigured so
   that a character the locale cannot encode is written as an escape rather than raising; stderr is
   left as the interpreter set it. Afterwards `envel list` under the broken locale against a store
   holding `café` exits 0 and writes one line, and under a UTF-8 locale its output is unchanged
   byte for byte.

4. **Guard the store's write in `envel/store.py`.** `save` catches `UnicodeError` from the write
   and raises `store.StoreError` with a message naming the path, alongside the `OSError` clause
   already there. Afterwards no call path out of `envel/store.py` ends in an unhandled encoding
   exception, and `envel/cli.py`'s existing `except store.StoreError` around the save turns it into
   an `envel:` line and status 1.

5. **Write the regression test for the reported case**, in `tests/test_cli.py`, as an end-to-end
   case running `envel new "café"` in a child process whose environment is the one in the item's
   reproduction — `PYTHONCOERCECLOCALE=0`, `PYTHONUTF8=0`, `LC_ALL=C`, `LANG=C`,
   `PYTHONIOENCODING` removed — so the case does not depend on the locale of whoever runs the
   suite. It asserts the exit status, that stderr contains no line beginning
   `Traceback (most recent call last)` and none beginning `  File "`, and that a following
   `envel list` in the same environment exits 0. Add a second case for the print half: a store
   created under the suite's own locale holding `café`, listed under the broken environment,
   exits 0 with no traceback.

6. **Write the two coverage cases this item inherited** (`WI-0001/Q-004`). They are steps of this
   plan and not acceptance criteria of this item, which is what that answer decided:
   - a new `tests/test_store.py` with a unit test calling `store.store_path(environ=...)` with a
     fake mapping, pinning the `XDG_DATA_HOME` branch and the home-directory branch — the two of
     the three that no test reaches today, since all of WI-0001's cases go through `ENVEL_FILE`;
   - a case in `tests/test_cli.py` running `envel new` on a name with surrounding whitespace
     against a fresh store, asserting the listed form and the stored form.

7. **Run the project's own commands and WI-0001's suite unmodified.**
   `python3 -m unittest discover -s tests -t .` and `python3 -m compileall -q envel tests`, both
   from the repository root. WI-0001's 24 tests are not edited by any step above; step 5 and step 6
   only add cases. Report the run in `impl-report.md` — the criteria are ticked by `verify` and not
   here.

8. **Repair the citations this change moves.** Both rows of the invalidation set are line-number
   citations into `envel/cli.py` and `envel/store.py`; after steps 1–4 the lines have moved. Reopen
   each cited line, point the citation at where its subject now is, and bump the document's version
   with a change-log row. This is inside the invalidation set, which is what permits the edit.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — the reproduction command exits with a status the tool chose and its stderr holds no traceback | 1, 2, 4 | the test written in step 5, run under the item's own environment; and the command from `## Steps to reproduce` run by hand, with its exit status and stderr quoted |
| AC2 — a regression test covers this case and fails without the fix, setting the child environment itself | 5 | the named test case in `tests/test_cli.py`, shown failing with steps 1–4 reverted and passing with them applied |
| AC3 — `envel list` afterwards exits 0, the store is unchanged or holds exactly what was accepted, and a failed `new` leaves no partial store | 2, 3, 4 | the second case in step 5 (list under the broken locale, exit 0); and `envel list` plus a byte comparison of the store file after a refused `new`, against the file before it |
| AC4 — every one of WI-0001's eleven criteria still holds, each named, and WI-0001's named tests pass unmodified | 3, 7 | `git diff` showing no edit to any existing test function, the full-suite run, and a read of AC1–AC11 against the changed behaviour — the one to watch is WI-0001 AC4's byte-identical stdout, which step 3 must not disturb under a UTF-8 locale |

## Assumptions

- **P1 — the refusal for undecodable bytes uses status 1, not 2.** `envel/cli.py` already splits
  refusals (1) from usage errors (2), and an argument that is bytes rather than text is a refusal
  the person can act on by fixing their terminal, not a mis-typed command line. Reversing it is one
  constant in one branch, and no criterion names the number. Nothing licensed this; no standing
  delegation exists in this engagement, and a disagreement lands as a change to this plan.
- **P2 — the wording of the two new messages is not fixed here.** They begin `envel:` and go to
  stderr, which is all the criteria require and the same disposition WI-0001 made under its own
  assumption P1. Reversing it is one string.
- **P3 — recovery is applied to the whole argument list, including the command word.** Applying it
  only to operands would leave `envel n\xffew` producing a different failure from
  `envel new "\xff"`, for no benefit. Reversing it is the placement of one call.
- **P4 — the store file written before this change is read unchanged.** No step alters the store's
  shape, so `ADR-0003`'s `version: 1` still describes it and no migration is owed. This is an
  assumption about scope rather than a design choice, and it is checkable: no step in this plan
  names the store's format.

## Decisions and ADRs

- `ADR-0005` — text crossing the process boundary is recovered on the way in and never fatal on the
  way out. It records the four mechanisms, the three options refused and why, and the cost of
  reversing each part. It is the decision behind steps 1 to 4.
- Everything else this plan chooses is an assumption above, each with what reversing it costs.

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/architecture/overview.md` | the `## The shape` table rows for `envel/cli.py` and `envel/store.py`, and the dependency-direction sentence — the citations `[src: envel/cli.py:27]`, `[src: envel/cli.py:13]`, `[src: envel/store.py:39; envel/store.py:58]` and `[src: tests/test_cli.py:29]` | cited-fact | steps 1 to 4 insert lines above every one of those positions, so each citation resolves to a different line than the one its sentence is about | open |
| `docs/process/ways-of-working.md` | `## Where an accepted test-coverage gap goes`, last paragraph — `[src: envel/store.py:58]` and `[src: envel/store.py:27]` | cited-fact | the same: step 4 adds an `except` clause to `save`, moving both cited lines | open |
| `docs/architecture/adr/ADR-0003-one-json-store-and-where-it-lives.md` | `## Decision`, the sentence "The file is written UTF-8 with `ensure_ascii=False`, so a name is stored as the characters the person typed … which is what makes the format survive a name the stakeholder was promised we would not restrict" | quantified | it is a claim about what the write survives, over the family of names; today it is false for a name arriving as surrogate-escaped bytes, and steps 1 and 4 change which members of that family reach the write | open |
| `docs/product/vision.md` | `## Engagement state`, all three bullets — "has not been asked to accept anything yet", "Five questions from intake are open with them", "Nothing has been designed or built. The epic has three work items, all at `draft`" | engagement-state | every one is already false and this change does not make it less so: the epic has six children, WI-0001 is delivered and merged, and three questions are open on WI-0002. Nobody in the pipeline may repair it; it is restated at the ending | open |
| `docs/architecture/adr/ADR-0004-envelope-identity-is-the-folded-trimmed-name.md` | `## Consequences`, the Unicode-normalisation bullet | cited-fact | it says normalisation is not applied, and step 1 inserts a transformation of the name before identity is computed; the sentence must be re-read against a change that is adjacent to it, whether or not it turns out to need a word | open |

## Deliverable documents

`none`. No acceptance criterion of this item has a document as its subject: AC1 and AC3 are about a
command's exit status, streams and store file, AC2 is about a test, and AC4 is about WI-0001's
criteria and tests.

## Binding ADRs

- `ADR-0001` — the standard library only, for the runtime and the checks. Steps 1 to 6 add `os` and
  `unittest` usage and nothing else; the clause binds every file this plan touches.
- `ADR-0002` — `bin/envel` is a launcher of eleven lines that puts the repository root on
  `sys.path` and calls `main`. It binds by exclusion: no step may put the fix in the launcher, which
  is why option C in `ADR-0005` was refused.
- `ADR-0003` — one JSON store, written UTF-8 with `ensure_ascii=False`, replaced atomically. It
  binds step 4, which must add an error path without changing what is written or how.
- `ADR-0004` — identity is the trimmed, casefolded name, computed once at the boundary. It binds
  step 1: recovery happens before identity, so what is folded is the recovered characters.
- `ADR-0005` — the decision this plan implements. It binds steps 1 to 4, clause by clause.

## Scaffolding

`none`. Both declared commands already run in this project against the code as it stands
(`python3 -m unittest discover -s tests -t .` → exit 0, 24 tests; `python3 -m compileall -q envel
tests` → exit 0), so nothing had to be created for a gate command to execute. `tests/test_store.py`
is created in step 6 and is a test with behaviour in it, which makes it implementation and
`implement`'s to write, not scaffolding.

## Risks

- **Step 3 could change WI-0001 AC4's byte-identical stdout.** Reconfiguring a stream is a global
  act. Under a UTF-8 locale nothing should be encodable-and-escaped, so the output should be
  identical — but "should" is what AC4 exists to check, and the full suite in step 7 is where it is
  caught. If it does change, step 3 is wrong and the handler must be applied to the printing of a
  name rather than to the stream.
- **The recovery in step 1 is the identity function under a UTF-8 locale, and that is load-bearing
  rather than incidental.** If it is not — if `os.fsencode` and a UTF-8 decode ever disagree with
  the string that went in — then every existing envelope name changes meaning at once. WI-0001's 24
  tests all pass names through this path and are the check.
- **This plan does not make the tool usable under a non-UTF-8 locale; it makes it not crash.** The
  listing shows escapes rather than letters. Nobody has asked for more, and if the stakeholder does,
  it is a new item and not a widening of this one.
- **The corrected reproduction may change how the item reads to a verifier.** AC1 names "the
  command in `## Steps to reproduce`", which is the `new` command and is still exactly reproducible;
  the print failure is covered by AC3 rather than AC1. A verifier reading the item alone would not
  find the second site, which is why it is stated at the top of this plan.

## Out of scope for this item

- Unicode normalisation of names (`ADR-0004` records why it is deliberately not applied).
- Any change to the store's format or to `ADR-0003`'s path resolution. Step 6 adds a test that
  reads two branches of that resolution; it does not change them.
- Making the listing render non-ASCII names correctly under a non-UTF-8 locale. Escapes and exit 0
  are what this item buys.
- Correcting `WI-0001`'s `plan.md`, whose assumption P5 and `## Risks` describe this failure
  wrongly. It is a tracker artifact of a closed item; the correction is recorded in `BUG-0001`'s
  `## Notes` and now here, which is where the item's own filing put it.

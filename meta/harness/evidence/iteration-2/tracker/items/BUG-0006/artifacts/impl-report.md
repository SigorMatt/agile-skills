# Implementation report — BUG-0006

## What was built

Nothing under `tidy/` or `tests/`. This item's defect is in prose, and its whole deliverable is
three citations and two document headers.

`docs/` carried three citations of the form `[src: tidy/cli.py:NN]`, and **all three pointed at
lines that do not support the sentences they are attached to.** Each is now file-level, per
ADR-0013, with the sentence's own named symbols carrying the precision:

| where | was | the sentence's subject | where that subject actually is now |
|---|---|---|---|
| `ADR-0008` line 48 | `tidy/cli.py:52` | `build_parser`, `parse_args` | `grep -n "parse_args" tidy/cli.py` → one hit, `62:    args = build_parser().parse_args(argv)`. Line 52 is a docstring inside `render` |
| `ADR-0009` line 23 | `tidy/cli.py:67` | `cli.py`'s `except OSError` | `grep -n "except OSError" tidy/cli.py` → one hit, `88:    except OSError as error:`. Line 67 is a comment about the `--rules` file |
| `ADR-0009` line 106 | `tidy/cli.py:93` | `apply_plan`, a `"failed"` outcome, "exit non-zero" | `grep -n "apply_plan" tidy/cli.py` → `12` (the import) and `109` (the call); the `return 1 if any(outcome.kind == "failed" ...)` is five lines below the call, at `114`, and is the module's last statement. Line 93 is blank |

No claim was reworded. Both records took `version: 3`, a fresh `updated`/`updated-by`/`updated-for`,
and a change-log row naming BUG-0006, per `spec/doc-header.md` §3. `docs/architecture/overview.md`
was not touched: nothing about the system's shape changed.

## Acceptance criteria evidence

| AC | how it is satisfied | evidence |
|----|---------------------|----------|
| **AC1** — the citation on ADR-0008 line 48 resolves to something that supports its sentence | The citation is now `[src: tidy/cli.py]`, which AC1 admits in terms — "or the file in which that happens" — and the file contains the statement in one `grep`. | `$ grep -n "src: tidy/cli.py" ADR-0008…md` → `48:  \`parse_args\` has told anyone where the user's rules came from [src: tidy/cli.py], so generated`, exit 0. `$ grep -n "parse_args" tidy/cli.py` → `62:    args = build_parser().parse_args(argv)`, exit 0, one hit — `build_parser` being called before `parse_args` has run, which is what the sentence claims. The blank-line failure mode AC1 names is gone: there is no line number to land on |
| **AC2** — no `path:line` citation in `docs/` points at a line that does not support its sentence | Held by construction rather than by inspection: after this change there is no `path:line` citation in `docs/` at all, so there is no surviving entry to open. **The parenthetical is deliberately not honoured** — see `## Deviations` | `$ grep -rn "src: [a-z/]*\.py:[0-9]" docs/` → no output, **exit 1**. `grep` exits 1 when it matches nothing, so exit 1 is the pass here and exit 0 would be the failure. Run twice: once after the citation edits, when it still matched (see `## Deviations`), and again after that was fixed |
| **AC3** — ADR-0008 carries the version bump and a change-log row saying what changed and for which item | Frontmatter bumped and a row added; the same done to ADR-0009, which AC3 does not name but `spec/doc-header.md` §3 requires of every document changed | `$ head -8 ADR-0008…md` → `version: 3`, `updated: 2026-08-28T13:57:57Z`, `updated-by: implement`, `updated-for: BUG-0006`. The change log's first row is `\| 3 \| 2026-08-28T13:57:57Z \| implement \| BUG-0006 \| …`, and its `version` equals the frontmatter's as §3 requires. ADR-0009 the same. **AC3's literal "`version: 2`" is stale** — see `## Deviations` |
| **AC4** — `lint-claims` still exits 0 and the suite still exits 0 | Both run on the branch head, after the last edit | `$ python3 .claude/agile-skills/scripts/lint-claims .` → `lint-claims: checked the whole tree under /home/msi/agile-skills-throwaway/tidy` / `lint-claims: 0 errors, 0 warnings`, exit 0. `$ python3 -m unittest discover -s tests -t . -q` → `Ran 158 tests in 0.168s` / `OK`, exit 0. Nothing under `tidy/` or `tests/` changed, so the suite is evidence that nothing *did* |

## Deviations from the plan

1. **The plan's step-5 sweep failed on the first run, on a change-log row this execution had just
   written.** Step 2's row described the edit by quoting the citation it removed — the literal
   `[src: tidy/cli.py:52]` — so `grep -rn "src: [a-z/]*\.py:[0-9]" docs/` matched it and exited 0
   where the plan predicts exit 1. That is a genuine hit against AC2's check, not a false positive
   to be explained away in a report: AC2 says the grep "lists every one, and each surviving entry
   is opened and read", and a reader running it would have had an entry to open. The row was
   rewritten to name the form (`tidy/cli.py:NN`) and the number ("It named line 52") separately,
   which is how ADR-0009 v2's own row was already written. The sweep then exited 1 with no output.
   No citation was missed; the plan simply did not anticipate that a change log describing a
   citation removal can reintroduce the string it removed.

2. **AC2's parenthetical is not honoured — carried forward from the plan, not decided here.**
   AC2 records ADR-0009's two `tidy/cli.py` citations as "exact and must stay so". They were exact
   at `cea3b907`, when the item was filed, and had stopped being exact by `82a7d26`, WI-0003's
   merge, which put twenty-one lines above both. ADR-0013 is the record of choosing against the
   parenthetical, with the git evidence; this execution applied it. Confirmed here by running
   rather than taken on trust: `:67` is a comment about the `--rules` file and `:93` is blank.
   `verify` decides whether that reading of AC2 stands, and a send-back costs three line numbers.

3. **AC3's literal "`version: 2`" is stale in the same way, and was read as "the version bump".**
   `git show cea3b907:…ADR-0008….md | sed -n '3p'` → `version: 1`, so at filing time "version: 2"
   meant one bump. ADR-0008 reached v2 forty-five minutes later, under WI-0003. Bumping it to 2
   now is impossible and bumping to 3 is what AC3's own normative words ask for — "carries the
   version bump and its change-log table carries a row saying what changed and for which item".
   Naming it because a `verify` reading AC3 literally would fail an item that did what AC3 meant.

4. **The item's own `## Steps to reproduce` and `## Actual behaviour` no longer reproduce**, which
   the plan's `## Risks` predicted. They record line 52 as blank with the statement at `:54`; on
   `main` today line 52 is `    """The stdout line for one action."""` and the statement is at `:62`.
   The defect is unchanged and larger. This report quotes what the commands actually printed.

Steps 1, 3, 4 and 6 went exactly as written. Nothing in the plan was skipped.

## Gates

Run on the branch head `971f1cc`, after the last edit.

| gate | result | evidence |
|---|---|---|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 158 tests`, `OK`, exit 0 |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace: checked 10 item(s), 15 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-has-a-test` | **pass, with the caveat the item itself records** | There is no test, and BUG-0006's `## Notes` is the standing record of why: the defect is in prose, there is no behaviour to pin, and a line-number lint would live in the toolkit, outside EP-001. Every AC above is instead an exact command with its output — AC1 two greps, AC2 one grep and its exit status, AC3 a `head`, AC4 the two suite commands. None is satisfied by reading code |
| `commits-reference-the-item` | **pass** | `check-commit-refs BUG-0006 wi/BUG-0006` → exit 0 on the branch head |
| `claims-are-sourced` | **pass** | `lint-claims --changed-since main` → exit 0 |
| `no-unplanned-scope` (advisory) | **pass** | `git diff main --stat` names the two ADRs and this item's tracker files, nothing else. Every hunk in the two ADRs is a citation from a plan step or a §3 header obligation. `git diff main -- docs/architecture/overview.md` is empty, as plan step 6 requires |

## What I did not do

- **Nothing enforces ADR-0013.** `lint-claims` cannot tell the two citation forms apart, so a
  future document may reintroduce `path:line` and no gate will notice. ADR-0013 `## Consequences`
  already records this; it is restated here because it is the honest limit of what this item
  delivers, and this execution has now watched the failure happen once, to itself, in `## Deviations`
  item 1. AC2 holds today and nothing keeps it holding.
- **I did not reword any claim**, including `ADR-0009` line 106's, which the plan's `## Risks`
  names as the weak one: its sentence names `apply_plan` and `"failed"` but not the `return`
  statement, so a reader lands on the call at `:109` and reads five lines down. The plan says a
  prose change to a `status: current` ADR wants a question to the architect rather than a
  unilateral edit, and I agree — so it stands as it is, named here for `verify` rather than fixed
  quietly.
- **I did not correct BUG-0006's own stale line numbers** in `## Steps to reproduce` and
  `## Actual behaviour`. `implement` may not edit an item's acceptance criteria, and the
  surrounding narrative is the filing record of what `review-close` saw on 2026-08-27; rewriting
  it would erase that. `## Deviations` item 4 states what the commands print today instead.
- **I did not touch `docs/architecture/overview.md`**, and no test, module or interface moved.

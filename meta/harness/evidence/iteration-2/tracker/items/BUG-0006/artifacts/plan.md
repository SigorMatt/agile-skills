# Plan — BUG-0006 ADR-0008 cites tidy/cli.py:52, which is a blank line

## Problem

Three sentences in `docs/` carry a citation of the form `[src: tidy/cli.py:NN]`, and **all three
now point at lines that do not support them**. `ADR-0008:48` cites `:52` for a sentence about
`build_parser` running before `parse_args`; that statement is at `tidy/cli.py:62` and line 52 is a
docstring inside `render`. `ADR-0009:23` cites `:67` for `cli.py`'s `except OSError`, which is at
`:88-90`; line 67 is a comment about the `--rules` file. `ADR-0009:106` cites `:93` for "only a
`"failed"` outcome makes the process exit non-zero", which is the module's last statement at
`:114`; line 93 is blank. Every one of the three claims is still true — only the pointers are
wrong, and no gate objects, because `spec/doc-header.md` §4a makes `path` and `path:line` one
citation form with one test: that the file exists.

What changes is prose in two ADRs, for a reader performing D12 — the reviewer who is told to open
what a sentence cites and decide from what is there. The constraints are that the claims themselves
must not be reworded (they are true, and their ADRs' decisions are not in question), that
`spec/doc-header.md` §3 requires a version bump and a change-log row on each document touched, and
that nothing under `tidy/` or `tests/` may change: there is no behaviour in this item.

One constraint deserves stating separately because it changed after the item was written. BUG-0006
AC2 records ADR-0009's two citations as "exact and must stay so". They were exact when the item was
filed at `cea3b907` and had stopped being exact by `82a7d26`, WI-0003's merge, which put twenty-one
lines above both. That premise failed before this plan ran, and the design below chooses against
the parenthetical for a reason recorded in an ADR rather than silently.

## Approach

Apply the rule this project already recorded in ADR-0009 v2's `## Consequences` — "an ADR about a
change to a file cites that file, and the change is what moves its own line numbers", the prose
carrying the precision — to all three remaining citations, and record it as the general rule for
`docs/` in **ADR-0013**.

Concretely: `[src: tidy/cli.py:52]` → `[src: tidy/cli.py]`, and the same for `:67` and `:93`. No
sentence is reworded. That is deliberate and it is checkable rather than hopeful: each of the three
sentences already names its subject in backticks, and each name has exactly one hit in
`tidy/cli.py`, so the citation still gets a reader there in one `grep`.

| ADR | the sentence's named subject | how a reader finds it |
|---|---|---|
| ADR-0008:48 | `build_parser`, `parse_args` | `grep -n "parse_args" tidy/cli.py` → one hit, line 62, `args = build_parser().parse_args(argv)` |
| ADR-0009:23 | `cli.py`'s `except OSError` | `grep -n "except OSError" tidy/cli.py` → one hit, line 88, the handler ADR-0006 decided |
| ADR-0009:106 | `apply_plan`, a `"failed"` outcome, "exit non-zero" | `grep -n "apply_plan" tidy/cli.py` → two hits, the import at line 12 and the call at line 109; the `return 1 if any(outcome.kind == "failed" ...)` statement is five lines below the call and is the module's last |

The third is the weakest of the three and is worth naming as such rather than glossing: `apply_plan`
has two hits rather than one, and the reader lands on the call and reads five lines down to the
return. It is still one `grep` and it is still exact under every future edit, which the line number
is not.

The alternative — repointing to `:62`, `:88`, `:114` — is rejected in ADR-0013 on evidence rather
than on taste: those are the same two citations that were left exact nineteen hours earlier,
precisely because they were exact, and they drifted again on the next merge.

## Steps

1. **`docs/architecture/adr/ADR-0008-help-text-is-prose-guarded-by-a-test.md`, line 48.** Replace
   `[src: tidy/cli.py:52]` with `[src: tidy/cli.py]`. Change nothing else on that line or in that
   paragraph — the sentence, including "under WI-0003 the tables in force are the *user's*, and
   `build_parser` runs before `parse_args` has told anyone where the user's rules came from", is
   true and is option A's decisive risk in a `status: current` ADR.
   Afterwards: `grep -n "tidy/cli.py" ADR-0008…md` shows one citation and it carries no line
   number, and the paragraph is otherwise byte-identical.

2. **The same file's frontmatter and change log.** `version: 2` → `3`, `updated` to this
   execution's UTC timestamp, `updated-by: implement`, `updated-for: BUG-0006`; add change-log row
   3 saying that the `tidy/cli.py:52` citation became file-level because line 52 had become a
   docstring in `render`, and naming ADR-0013. Newest row first, and the top row's `version` must
   equal the frontmatter's (`spec/doc-header.md` §3).
   Afterwards: `head -8` shows `version: 3`, and the change-log table's first row is version 3.

3. **`docs/architecture/adr/ADR-0009-one-entry-that-cannot-be-examined-is-a-leave.md`, lines 23 and
   106.** Replace `[src: tidy/cli.py:67]` with `[src: tidy/cli.py]` and `[src: tidy/cli.py:93]` with
   `[src: tidy/cli.py]`, leaving every other citation in both bracket groups in place and in order —
   line 23's group is `[src: BUG-0004; src: tidy/planner.py; src: tidy/cli.py:67; src: ADR-0006]`
   and line 106's is `[src: ADR-0007; src: tidy/cli.py:93]`. Change no prose.
   Afterwards: `grep -n "cli.py:" ADR-0009…md` returns only the change-log rows, never a citation.

4. **The same file's frontmatter and change log.** `version: 2` → `3`, `updated`, `updated-by:
   implement`, `updated-for: BUG-0006`; add change-log row 3 saying that the two `tidy/cli.py:NN`
   citations left exact by BUG-0004/Q-002 had drifted twenty-one lines under WI-0003's `--rules`
   block and are now file-level, completing the sweep that ADR's v2 began, and naming ADR-0013.
   Afterwards: `version: 3` in the frontmatter and as the change log's top row.

5. **Run the sweep and the two gate commands, and record their output in the implementation
   report.** In order:
   - `grep -rn "src: [a-z/]*\.py:[0-9]" docs/` → **no output, exit 1**. `grep` exits 1 when it
     matches nothing, so this is the pass and the report should say so rather than treating a
     non-zero status as a failure. If it prints anything, a citation was missed.
   - `python3 .claude/agile-skills/scripts/lint-claims .` → exit 0.
   - `python3 -m unittest discover -s tests -t . -q` → exit 0, 158 tests. Nothing under `tidy/` or
     `tests/` changed, so this is a check that nothing *did*, not a check of new behaviour.
   - `python3 -m compileall -q tidy tests` → exit 0.
   Afterwards: `git diff main --stat` on the branch names exactly three files —
   `ADR-0008…md`, `ADR-0009…md`, and this item's tracker files — plus `ADR-0013…md`, which this
   plan already committed.

6. **Do not touch `docs/architecture/overview.md`.** No module, boundary or interface moves, and a
   version bump with nothing behind it devalues every other one (`spec/doc-header.md` §3).
   Afterwards: `git diff main -- docs/architecture/overview.md` is empty.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — ADR-0008 line 48's citation resolves to something that supports its sentence | 1 | The citation becomes `[src: tidy/cli.py]`, which AC1 admits in terms ("or the file in which that happens"). Demonstrated by running the item's own step 1 and step 2 commands: the citation now names the file, and `grep -n "parse_args" tidy/cli.py` → one hit, `args = build_parser().parse_args(argv)`, which is `build_parser` being called before `parse_args` has run |
| AC2 — no `path:line` citation in `docs/` points at a line that does not support its sentence | 1, 3 | `grep -rn "src: [a-z/]*\.py:[0-9]" docs/` prints nothing and exits 1: after steps 1 and 3 there is no such citation left to open, so the criterion holds by construction rather than until the next merge. **The parenthetical is not honoured and that is the design's deliberate choice** — see `## Risks` and ADR-0013 `## Consequences` |
| AC3 — ADR-0008 carries the version bump and a change-log row naming BUG-0006 | 2 | `head -8 ADR-0008…md` shows `version: 3`, `updated-for: BUG-0006`; the change log's first row is `3 \| <ts> \| implement \| BUG-0006 \| …`. Step 4 does the same for ADR-0009, which AC3 does not name but `spec/doc-header.md` §3 requires of every document changed |
| AC4 — `lint-claims` still exits 0 and the suite still exits 0 | 5 | Both commands run and their real output quoted in `impl-report.md`: `lint-claims: 0 errors, 0 warnings`, exit 0; `Ran 158 tests`, `OK`, exit 0 |

## Assumptions

- **A1 — the three sentences need no rewording, because each already names its subject and each
  name has exactly one hit in `tidy/cli.py`.** Checked, not assumed, for the first two
  (`grep -n "parse_args"` and `grep -n "except OSError"` each return one line); the third resolves
  in two reads rather than one, as `## Approach` says. Reversing: if `verify` judges a sentence's
  subject insufficiently named, the remedy is to name the symbol *in that sentence*, one clause in
  one ADR, which is the same edit size as this whole item.
- **A2 — `implement` makes these edits, not `plan`.** `plan` wrote ADR-0013 because writing ADRs is
  this skill's job; the two ADRs under repair are the item's deliverable and belong to the branch,
  so that `git log --grep BUG-0006` shows the fix. Reversing: none needed; this is the workspace
  convention (`spec/workspace-layout.md` §5) rather than a design choice.
- **A3 — no test can pin this.** The item's `## Notes` already records why: the defect is in prose,
  there is no behaviour, and a line-number lint would live in the toolkit, which is outside
  EP-001. AC2's sweep is the check, and a person performs it. Reversing: if this project ever owns
  its own gate scripts, ADR-0013 option C is written out ready to be reconsidered.

## Decisions and ADRs

- **ADR-0013 — Citations in `docs/` name files and symbols, never line numbers.** The one real
  decision: whether to repoint the three citations (option A) or to drop their line numbers and let
  the prose carry the precision (option B, chosen), with a gate (C) and doing nothing (D) also
  costed. It generalises the rule ADR-0009 v2 recorded for one document, and it records why
  BUG-0006 AC2's "must stay so" is not honoured. Reversibility: cheap — three citations, one commit,
  no code.
- Everything else in this plan follows from documents: the version-bump and change-log obligation
  from `spec/doc-header.md` §3, the "cite the file, name the symbol" form from ADR-0009 v2, the
  prohibition on rewording a `status: current` ADR's decision from `spec/doc-header.md` §4, and the
  scope limit on toolkit changes from BUG-0006's own `## Notes`.

## Scaffolding

none.

## Risks

- **`verify` may read AC2's parenthetical — "the latter two are exact and must stay so" — as
  binding and fail the criterion.** That is the one place this plan knowingly departs from the
  item's words, and it is why the departure is in an ADR with the git evidence rather than in a
  plan step. The reading this plan takes is that AC2's normative sentence is its first one, that
  the parenthetical was a statement of fact about `cea3b907` which `82a7d26` falsified, and that
  restoring exactness would restore a property with a measured half-life of one item. If `verify`
  disagrees, the item comes back to `in-progress` and the remedy is three line numbers — cheap, and
  the argument is on the record either way.
- **The third citation is the weak one.** `ADR-0009:106`'s sentence names `apply_plan` and
  `"failed"` but not the `return` statement itself, so a reader lands on the call at line 109 —
  one of `apply_plan`'s two hits in the file, the other being the import — and reads five lines
  down. If that is judged not-one-hop, the fix is to name the statement in the sentence,
  which is a prose change to a `status: current` ADR and therefore wants a question to the
  architect rather than a unilateral edit.
- **Nothing enforces ADR-0013.** `lint-claims` cannot distinguish the two citation forms, so a
  future document may reintroduce `path:line` and no gate will notice. Recorded in ADR-0013
  `## Consequences` as the honest state, not designed around.
- **A stale line number in the item itself.** BUG-0006's `## Steps to reproduce` and
  `## Actual behaviour` say line 52 is blank and the statement is at `:54`; that was true at
  `cea3b907` and is not now (line 52 is `"""The stdout line for one action."""`, the statement is at
  `:62`). The defect is unchanged and larger, but anyone re-running the item's own commands will
  see different output than the item records. `implement` should quote what it actually gets rather
  than what the item predicts.

## Out of scope for this item

- **Any change under `tidy/` or `tests/`.** There is no behaviour in this item.
- **Rewording any claim in ADR-0008 or ADR-0009.** All three claims are true; only their pointers
  are wrong, and rewording the decisive risk clause of a `status: current` ADR is a different act
  from correcting a citation.
- **A gate that checks line numbers.** ADR-0013 option C, ruled out because it belongs to
  `.claude/agile-skills/scripts/`, which is the toolkit running this project and not part of EP-001.
- **The `run:` citations elsewhere in `docs/`.** They name commands and outcomes, not paths, and
  the drift this item is about cannot reach them.
- **`docs/architecture/overview.md`.** Nothing about the system's shape changes.

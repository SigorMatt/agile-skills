# Verification report — BUG-0006

Verified-commit: 64010239257c5eb51a7feedf97ae22687c1a30b4

## Verdict

**Pass.** All four acceptance criteria are met, each demonstrated by a command run here against
`wi/BUG-0006` at `6401023`, not read out of the implementation report. No defect was found in the
change, and no bug item was filed.

Two criteria carry premises that were true when the item was filed and false by the time it was
built, and both are the reason a reviewer should look at this item rather than skim it:

- **AC2's parenthetical — "the latter two are exact and must stay so" — is not honoured, and this
  verification accepts that.** The reasoning and the evidence are in `## Criteria` and in
  `## The two stale premises` below. `review-close` is the right place to overrule it if the
  Definition of Done reads AC2 differently; this report makes the departure impossible to miss
  rather than resolving it quietly.
- **AC3's literal "`version: 2`" is unsatisfiable**, and satisfying it would violate the
  `spec/doc-header.md` §3 that the same sentence invokes.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| **AC1** — the citation on ADR-0008 line 48 resolves to something that supports its sentence | **pass** | `sed -n '48p' ADR-0008…md \| grep -o "src: [^];]*"` then `grep -n "build_parser\|parse_args" tidy/cli.py`, then read `tidy/cli.py:20-32` and `:61-66` | `src: tidy/cli.py` — no line number at all. Then `20:def build_parser():` and `62:    args = build_parser().parse_args(argv)`, one hit each | The citation names the file, which AC1 admits in terms ("or the file in which that happens"). Reading it settles the sentence rather than merely locating it: `build_parser` composes the whole `epilog` string at `:22-32`, and `--rules PATH` is not known until `parse_args` returns at `:62`. That is exactly the claim — `build_parser` runs before `parse_args` has told anyone where the user's rules came from. AC1's named failure mode ("a citation pointing at a blank line") cannot occur: there is no line to point at |
| **AC2** — no `path:line` citation in `docs/` points at a line that does not support its sentence | **pass** on its operative sentence; **the parenthetical is not honoured** | `grep -rn "src: [a-z/]*\.py:[0-9]" docs/` | no output, **exit 1** | Vacuously and demonstrably true: there is no such citation left in `docs/`, so there is no surviving entry to open. This is not a vacuous *pass* — the same expression run against `main` returns all three (see `## Test sensitivity check`), so the emptiness is a real absence, not a regex that stopped matching. On the parenthetical, see below |
| **AC3** — ADR-0008 carries the version bump and a change-log row saying what changed and for which item, per `spec/doc-header.md` §3 | **pass** | `head -8 ADR-0008…md`; `sed -n '/^## Change log/,$p' ADR-0008…md \| sed -n '3,5p'`; and `git show f459e72:…ADR-0008….md \| sed -n '3p'` | `version: 3`, `status: current`, `updated: 2026-08-28T13:57:57Z`, `updated-by: implement`, `updated-for: BUG-0006`. Top change-log row `\| 3 \| 2026-08-28T13:57:57Z \| implement \| BUG-0006 \| The \`## Decision\` citation … became file-level …\|`. At the filing commit the frontmatter read `version: 1` | §3 checked clause by clause, not assumed: newest row first ✓; top row's `version` (3) equals the frontmatter's (3) ✓; the content change added a row **and** bumped the version ✓; `what changed` is actionable — it names the section, the form, the old line and what it now holds — rather than "Updated" ✓. ADR-0009 was checked the same way and passes identically (`version: 3`, matching top row); AC3 does not name it but §3 requires it of every document changed, and the diff changes it |
| **AC4** — `lint-claims` still exits 0 and the suite still exits 0 | **pass** | `python3 .claude/agile-skills/scripts/lint-claims .`; `python3 -m unittest discover -s tests -t . -q` | `lint-claims: checked the whole tree under /home/msi/agile-skills-throwaway/tidy` / `lint-claims: 0 errors, 0 warnings`, exit 0. `Ran 158 tests in 0.163s` / `OK`, exit 0 | Both run here on `6401023`, not quoted from the report. 158 is the same count `main` carried, which is the point: this item changed no code, and the suite is evidence that none changed |

## Gates

| gate | result | evidence |
|---|---|---|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` → `Ran 158 tests in 0.163s`, `OK`, exit 0, run on `6401023` |
| `lint-clean` | **pass** | `python3 -m compileall -q tidy tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → `checked 10 item(s), 15 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | **pass** | Each row of `## Criteria` names a command this skill ran and quotes what it printed. Three of the four verdicts rest on evidence the implementation report does not contain at all: the `git show f459e72` frontmatter check behind AC3, the `git grep … main` sensitivity check behind AC2, and reading `tidy/cli.py:20-32` to confirm AC1's sentence rather than merely locating its subject |
| `negative-cases-exercised` | **pass** | Three, listed below |
| `tests-would-fail-without-the-change` (advisory) | **pass, by the only means this item admits** | There is no test — BUG-0006's `## Notes` records why, and this verification does not dispute it. The equivalent was performed on the check that stands in for one: see `## Test sensitivity check` |

## Negative and boundary cases exercised

1. **AC2's sweep at the boundary between "clean" and "broken", using real prior state.**
   `git grep -n "src: [a-z/]*\.py:[0-9]" main -- docs/` → exit 0, three hits:
   `ADR-0008…md:48` (`tidy/cli.py:52`), `ADR-0009…md:23` (`:67`), `ADR-0009…md:106` (`:93`).
   The same expression on the branch head → exit 1, no output. The criterion's check discriminates.
2. **A newly introduced violation, to prove the sweep is not merely matching historical text.**
   Wrote `docs/_verify_probe.md` containing `x [src: tidy/cli.py:999] y`; the sweep returned
   `docs/_verify_probe.md:1:x [src: tidy/cli.py:999] y`, exit 0. Removed the probe; the sweep
   returned to exit 1 with no output, and `git status --short` is clean. A citation reintroduced
   tomorrow would be caught by AC2's own command.
3. **AC1's named failure mode, checked against what the citation used to name.**
   `git show main:tidy/cli.py | grep -n "" | sed -n '52p'` → `52:    """The stdout line for one
   action."""`. The item says line 52 is blank; on `main` it is a docstring inside `render`. The
   defect is real either way — a docstring in a rendering helper does not support a sentence about
   `build_parser` and `parse_args` — and it is *worse* than the item recorded, since a reader lands
   on plausible-looking code rather than on obvious nothing. Noted, not held against the item.

## Test sensitivity check

The item has no test and is not required to have one. What must be sensitive instead is AC2's
sweep, because a `grep` that has silently stopped matching produces exactly the same empty output
as a clean tree — the failure mode in which a criterion "passes" forever.

Two independent demonstrations that it is sensitive, both above: the same expression finds all
three citations in `main`'s `docs/` (real prior state, case 1), and finds a synthetic one
introduced and then removed (case 2). Removing the behaviour makes the check fail; that is the
property step 5 asks for.

## The two stale premises

Both were established here by running `git`, not taken from the implementation report or the plan.

**AC2's "the latter two are exact and must stay so".** True when written, false before this item's
branch existed, and by another item's merge:

| | |
|---|---|
| BUG-0006 filed | `f459e72`, 2026-08-28T00:18:34+03:00 |
| WI-0003 merged | `82a7d26`, 2026-08-28T01:15:41+03:00 — **57 minutes later** |
| `tidy/cli.py:67` and `:93` at filing | `git show cea3b907:tidy/cli.py \| grep -n "" \| sed -n '67p;93p'` → `67:    except OSError as error:` and `93:    return 1 if any(outcome.kind == "failed" for outcome in outcomes) else 0` — **exact, as AC2 says** |
| the same two lines on `main` | `67:    # and one line on stderr like every other such event (ADR-0006, ADR-0010). It` and `93:` (blank) — **both wrong** |

"Must stay so" is a preservation instruction, and the property it names had already been destroyed
when `plan` and `implement` ran. Nothing they could do would make those citations *stay* exact;
the only available act was to *restore* exactness by repointing to `:88` and `:114` — which is not
what the clause says, and is the same act ADR-0009 v2 performed nineteen hours earlier for
`tidy/planner.py`, whose result drifted again on the next merge. The measured half-life of an exact
line number in this repository is under one item.

This verification therefore reads AC2's first sentence as the criterion and the parenthetical as a
description of the state at filing, and finds the criterion met. **That reading is on the record so
it can be overruled.** The authority for the departure is ADR-0013, written by `plan` for this item
before any code was touched, and it is an architectural decision — not an amendment to an
acceptance criterion, which no skill may make. `review-close`'s Definition of Done check is the
place to decide whether an ADR may override a clause of an AC in this way. If it decides not, the
remedy is three line numbers and the argument survives in both records either way.

**AC3's "`version: 2`".** `git show f459e72:…ADR-0008….md | sed -n '3p'` → `version: 1`. ADR-0008
was at v1 when the item was filed, so "version: 2" meant one bump; it reached v2 forty-nine minutes
later under WI-0003, and this item takes it to 3. Bumping to 2 now is not merely awkward but
prohibited by the `spec/doc-header.md` §3 that AC3's own sentence invokes — "every content change
adds a row **and** bumps `version`", and 2 → 2 is not a bump. AC3's normative words are "carries
the version bump and its change-log table carries a row saying what changed and for which item",
and they are satisfied exactly.

## Defects found

**None.** No bug item was filed, and nothing was sent back.

One observation, recorded because it corrects the implementation report in the item's favour
rather than against it. The report names `ADR-0009` line 106 as "the weak one", on the grounds
that a reader greps `apply_plan` (two hits: the import at `:12`, the call at `:109`) and must then
read five lines down to the `return` at `:114`. That undersells it: the sentence also quotes
`"failed"`, and `grep -n '"failed"' tidy/cli.py` returns **one hit, `114:    return 1 if
any(outcome.kind == "failed" for outcome in outcomes) else 0`** — the statement itself, in one hop.
The citation resolves better than its author claimed. No criterion turns on this; it is here so
that a later reader does not inherit a concern that the file does not support.

The diff was read against the plan (`git diff main..HEAD`). Every hunk in `docs/` is one of the
plan's steps 1–4 or a `spec/doc-header.md` §3 header obligation: three citations, two frontmatter
blocks, two change-log rows. No prose is reworded, no file under `tidy/` or `tests/` appears, and
`git diff main..HEAD -- docs/architecture/overview.md` is empty, as plan step 6 requires. Nothing
in the change is unaccounted for.

## Not verified, and why

- **That AC2 keeps holding.** It holds at `6401023` and nothing enforces it afterwards:
  `lint-claims` cannot distinguish `path` from `path:line`, so a future document may reintroduce
  the form and no gate will notice. ADR-0013 `## Consequences` and the implementation report both
  record this, and this verification confirms it rather than discovering it — `lint-claims .` exits
  0 both on `main` (three broken citations) and on the branch head (none). The criterion is a
  point-in-time check by construction, and the durable remedy is the convention, not a gate.
- **Whether the file-level form is the *right* remedy** rather than a permissible one. That is a
  design judgement recorded in ADR-0013 and is not this skill's to re-open; AC1 and AC2 ask whether
  the citations resolve, and they do.
- **The `[src: …]` citations elsewhere in `docs/` that name non-`.py` paths or `run:` commands.**
  AC2's own expression scopes the sweep to `[a-z/]*\.py:[0-9]`, and this verification used the
  criterion's expression rather than a wider one of its own. `lint-claims` covers the whole tree
  for existence and reports 0 errors; nobody has checked every `run:` citation still reproduces,
  and that is outside this item.
- **Nothing was blocked, and no environment was missing.** Every command in this report ran to
  completion on the branch head.

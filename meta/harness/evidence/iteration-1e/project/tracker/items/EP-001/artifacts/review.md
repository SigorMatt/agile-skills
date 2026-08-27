# Review — EP-001

Ending an engagement, not reviewing a change. There is no branch, no diff and no merge: an epic
advances only through its children, and every one of them has already been reviewed and closed on
its own terms. What is judged here is the **epic** Definition of Done (`spec/dor-dod.md` §4) and
the ending the stakeholder's answer selects.

## What I examined

- **The dispatch itself.** `scripts/engagement-state EP-001` → `at-rest`, *"every child has
  stopped, no question is open, no request is open"*, `not delivered: WI-0003`, rest reached at
  `2026-08-27T02:28:28Z`. I did not decide from the board that the engagement looked finished;
  the program decided, and the same program backs `check-epic-signoff`.
- **The termination question and its answer.** `tracker/items/EP-001/questions/Q-004.md` in full —
  the goal restated in the stakeholder's words, all six children named, four endings offered, and
  the stakeholder's reply. Their words, verbatim: *"No, not as it stands — the bank import was
  part of what I asked for and it isn't there. Everything else looks right. I'll send the file and
  then we can finish it."*
- **The epic's own record.** `item.md` (goal, success measures, scope, and the
  `## Where the engagement stands` section `answer-questions` wrote from the reply); `history.md`
  (five rows, `— → open → awaiting-answer → open → awaiting-answer → open`, chaining without a gap,
  last row matching the item's status); `journal.md` end to end.
- **Every child, by ID**, and the state each is actually in on disk — `item.md` frontmatter and
  the last row of `history.md`, not the board's summary of them.
- **The product, run.** Not the reports about it. From a scratch store at `/tmp/de3/data.json`,
  as evidence for DE3: three people added, two expenses recorded with different sharer sets, both
  listings, and `settle` three times — twice in this shell and once under `env -i` with nothing
  inherited but the store path.
- **The claims in `docs/`, checked from the code rather than from the sentences** — the DE6 table
  below. `lint-claims --all` exits 0 over the whole tree, which proves the citations *resolve*;
  the table is the part only a reader can do.
- **`README.md`**, for whether it overclaims the undelivered import. It does not: *"Importing a
  bank CSV export (WI-0003) is not part of this version"*, in the third paragraph.

### DE6 — the claims, checked against the running code

Each behavioural claim in `docs/` about what this epic delivered, with the thing I opened or ran
to decide it. In no case did I decide from the sentence or from a document that repeats it.

| claim | where | what I ran or opened | verdict |
|---|---|---|---|
| an expense is split equally between the people named as sharing it | `vision.md` v5 | `expense add --amount 30.00 --paid-by Ana --shared-by Ana,Ben,Cleo` then `settle` on a scratch store | **true.** Stored `shares_minor` is `{Ana:1000, Ben:1000, Cleo:1000}`; `settle` prints `Cleo pays Ana 10.00`, `Ben pays Ana 3.75`, which is the hand arithmetic for those two expenses |
| a record made by mistake can be deleted; it cannot be edited in place | `vision.md` v5 | `python3 -m expenses expense --help` and `expense edit` | **true.** The action list is exactly `{add,list,delete}` for both nouns; `expense edit` exits non-zero with *"invalid choice: 'edit'"* |
| every success writes to stdout and exits 0; every refusal writes to stderr, changes nothing on disk and exits non-zero | `overview.md` v3 | two refusals — an unknown sharer, and deleting a person still named in expenses — each with stdout, stderr, exit code and an `md5sum` of the dataset before and after | **true.** Both: exit 2, empty stdout, one line on stderr (`Zoe is not in the group`; `Ana is named in 2 expense(s); delete those first`), dataset checksum unchanged at `122ab8c4…` |
| a missing file reads as an empty dataset, which is why the listings can answer before anything has ever been recorded | `overview.md` v3 | `person list`, `expense list` and `settle` against `EXPENSES_STORE=/tmp/de3/nope.json`, then `ls` on that path | **true.** `no people`, `no expenses`, `no payments needed`, all exit 0, and the read created no file |
| `expense list` prints the position as its leading column, and `VERSION` is still 1 | `overview.md` v3, `ADR-0006` | the listing output and the raw JSON | **true.** `1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben,Cleo  dinner`; the file's `"version"` is `1` |
| the settlement is computed on every run and never written down | `ADR-0005`, `overview.md` v3 | `settle` run three times, with an `md5sum` of the dataset between runs | **true.** Identical output each time, dataset checksum unchanged |
| Python 3 and its standard library only; nothing installed, nothing sent anywhere | `README.md`, `vision.md` v5 | every `import` in `expenses/*.py`; `ls` for `requirements*.txt`, `setup.py`, `pyproject.toml` | **true.** Only `argparse`, `datetime`, `json`, `os`, `pathlib`, `re`, `sys`, `tempfile` and the package's own modules. No socket, no `urllib`, no `http`. No dependency manifest of any kind exists |
| importing a bank CSV export is not part of this version | `README.md`, `vision.md` v5 | the command surface, and `grep -rn -i csv expenses/` | **true**, and it is the thing the stakeholder refused the engagement over |

## Definition of Done — epic (`spec/dor-dod.md` §4)

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | every child terminal, and every undelivered child named in the termination question and in the epic's outcome | **pass** | Six children, all terminal, read from their own `item.md`: WI-0001 `done`, WI-0002 `done`, WI-0004 `done`, BUG-0001 `done`, BUG-0002 `done`, WI-0003 `blocked`. The one that did not deliver, WI-0003, is named by ID in `Q-004`'s `## Question` (*"WI-0003 — Import expenses from a bank CSV export. Not delivered."*), in the epic's `## Where the engagement stands`, and in this execution's history reason. `engagement-state` independently reports `not delivered: WI-0003` |
| DE2 | every child's `outcome` recorded; dropped items say why | **pass** | `grep '^outcome:' tracker/items/*/item.md` → `delivered` on all five closed children. WI-0003 carries no `outcome` and must not: it is `blocked`, not `done`, and an outcome on a live item is what `validate-workspace` reports as `item.outcome.premature`. Nothing was dropped, so the second clause does not apply |
| DE3 | every success measure addressed — met, or explicitly not met with the reason | **pass** (as a record; **one measure is not met**) | Measure by measure, from the run above. **M1** (add members, record an expense shared by a named subset, print the report, documented commands only, no hand-editing) — **met**: the whole sequence ran from an empty store using only commands in `README.md`. **M2** (report again in a new process, same figures) — **met**: `Cleo pays Ana 10.00` / `Ben pays Ana 3.75` three times, including under `env -i`. **M3** (at least one expense enters the store from a bank CSV export) — **NOT met**: no importer exists; `grep -i csv expenses/` returns nothing. The reason is recorded and is the reason the engagement ends where it does — EP-001/Q-001, the layout, was never supplied. **M4** (no network, python3 and stdlib only) — **met**: import audit and the absence of any dependency manifest. DE3 requires the measures to be *addressed*, and permits closing with one unmet provided that is said; it is said here, in `Q-004`, in the epic's `item.md` and in `vision.md` v5 |
| DE4 | `docs/product/` reflects what was actually built, not what was proposed | **pass, after a correction made here** | `vision.md` v4 read, in *What it is for*: *"The person records who paid for what and who shared it, **or lets their bank's CSV export supply the expenses**"* — present tense, describing a capability no code has. The *Still awaited* section further down corrected it, but a reader who stops at *What it is for* was told the import works. Rewritten in v5 to say plainly that it is not built, and a new *Where this ended* section records the impasse and the stakeholder's words. Version bumped 4 → 5 with a change-log row, `updated-by: review-close`, `updated-for: EP-001` (`doc-header.md` §3) |
| DE5 | open questions across all child items closed, or re-filed against a follow-up item | **pass** | `grep -rl '^status: open' tracker/items/*/questions/` returns nothing. Eight questions exist across the engagement — EP-001 Q-001…Q-004, WI-0001 Q-001…Q-003, WI-0004 Q-001 — and all are `answered`. `engagement-state` checks the same condition independently and it is part of why it reports `at-rest` |
| DE6 | claims in `docs/` about behaviour this epic delivered checked against the code **during this epic**; every citation resolves | **pass** | The eight-row table above, each row decided by running the tool or opening the source, this execution. Automated half: `lint-claims --all` → *"checked the whole tree… 0 errors, 0 warnings"*. Also `python3 -m unittest discover -s tests -t .` → `Ran 123 tests… OK`, exit 0. One claim about this epic's behaviour **was** found false — the example command in `Q-004` — but it lives in a tracker artifact rather than in `docs/`, so it is a finding below rather than a DE6 failure |
| DE7 | the stakeholder was asked whether they accept the engagement, after rest, and answered — in every ending | **pass** | `check-epic-signoff EP-001` → *"PASS — tracker/items/EP-001/questions/Q-004.md carries the stakeholder's reply, names all 6 child item(s), and was filed after the engagement reached rest at 2026-08-27T02:28:28Z"*, exit 0. They answered, and their answer was no. DE7 asks that the question was asked and answered, never that the answer was favourable |

## Findings

1. **The example command in `EP-001/Q-004`'s `## Context` is wrong, and the stakeholder read it.**
   It demonstrates recording a shared expense as
   `--shared-by Ana --shared-by Ben`. `--shared-by` takes one comma-separated list
   [src: expenses/cli.py; README.md]; repeating the flag is `argparse` last-wins, so that command
   records the expense as shared by **Ben alone** and produces silently wrong arithmetic — which
   is the one failure this whole product exists to prevent. Reproduced on a scratch store: a
   three-way dinner stored `"shared_by": ["Cleo"]` and `settle` then printed `Cleo pays Ana 30.00`
   instead of `Cleo pays Ana 10.00` / `Ben pays Ana 3.75`.

   **Disposition: recorded, not filed as a bug, and not rewritten.** The tool is not defective —
   `README.md` documents the comma form correctly and all 123 tests use it; the defect is in one
   artifact of the record. The original text stays as the stakeholder saw it (`question.md` §3
   rule 6) and a dated `[review-close]` correction is appended to that question's
   `## Consequences`, naming the wrong command and the right one. No bug item was filed, and the
   reasoning is worth disagreeing with if you think it is wrong: filing one would create a
   non-terminal child, take the engagement **out of rest**, and so invalidate the sign-off the
   stakeholder gave minutes ago — forcing them to be asked a second time over a defect that
   changed nothing they decided. They refused over the missing import, not over this bullet, and
   the correction is complete the moment it is written, with no code to change.

2. **`vision.md` presented the unbuilt CSV import as a current capability.** Detail and fix under
   DE4 above. Same class of defect as BUG-0001 — a document overstating what is true — found the
   same way, by reading the prose against the code rather than trusting it.

3. **No finding against any child's delivery.** Each of the five delivered children was reviewed
   and closed against the item Definition of Done in its own execution; nothing re-examined here
   contradicts those closures, and the running product behaves as their reports say.

## Accepted gaps

- **WI-0003, the bank CSV import, is not delivered**, and there is no plan, no code and no
  criterion that could be made decidable for it. That is not a gap being waved through: it is the
  reason this engagement ends at an impasse rather than closing, and it is named in the epic's
  outcome, in the termination question, in `vision.md` v5 and in `WI-0003/item.md` — which also
  records exactly what would unblock it.
- **How the importer would learn who shared an imported expense is still unanswered.** A bank row
  says who was charged, not who shared it (`WI-0003/item.md` `## Notes`). It survives this ending
  recorded on the item, where refinement will meet it if the sample ever arrives.

## Verdict

**Ending E3 — impasse** (`ids-and-statuses.md` §3.5). Every child is terminal, one did not
deliver, and the stakeholder did not accept. `EP-001` moves `open → blocked` with
`resume-to: open`; no `outcome` is recorded, because `blocked` is not a closure and claiming one
would be the overclaim the validator exists to refuse.

This is a legitimate end, not a failure of the pipeline. The stakeholder was asked, in their own
terms, with every child named, and they said no — which is what E3 is for. A person restarts it:
the sample of the bank's CSV export unparks WI-0003, and if that item delivers, the engagement
returns to rest and a fresh sign-off is due, because this one accepted nothing.

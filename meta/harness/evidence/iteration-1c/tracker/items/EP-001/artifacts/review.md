# Review — EP-001

The epic's closing review. Its last child, WI-0004, was reviewed, merged and closed separately; this
judges the epic itself against `spec/dor-dod.md` §4.

**Why this is a separate execution.** `review-close` step 10 puts epic closure inside the last
child's close, and that execution deliberately declined it: DE4 was not met, because
`docs/product/vision.md` still described a two-command tool. It filed `EP-001/Q-002` instead,
`answer-questions` produced v12, and the epic became closable. At that point the orchestrator had
nothing to dispatch — `pipeline.yaml` gives status `open` an `owner: null`, so `next` step 4's
candidate set is empty and step 5 reports "nothing runnable" — even though `open → done` by
`review-close` is a legal transition sitting one step away. That is a defect in the orchestrator's
reachability rather than in the work, it is recorded as one below, and this execution finishes the
step the earlier one deferred.

## What I examined

- `tracker/items/EP-001/item.md` in full — the goal, SM1 to SM4, `## Scope`, `## Out of scope`, and
  both paragraphs about the import; `journal.md` (nine entries) and `history.md`.
- All four children's `item.md`, their `outcome` fields, and their `review.md` verdicts.
- All eighteen question files across five items, checking each for `status`, and each answered
  question's `## Consequences` for files that exist.
- `docs/product/vision.md` **v12, end to end**, and `docs/architecture/overview.md` v5.
- All eleven ADRs.
- **The running tool**, for DE6: the behavioural claims in ADR-0001, ADR-0003, ADR-0004 and ADR-0010
  and in `vision.md` were re-checked by running the commands they describe, not by re-reading the
  prose. This is the read `review-close` recorded as owed when it left the epic open.
- `git log --oneline` on `main`, and the four merge commits.

## Definition of Done — epic

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| DE1 | every child item is `done` | **pass** | the board reports `4 item(s): 4 done`; `grep "^status:"` over the four children gives `done` four times |
| DE2 | every child's `outcome` is recorded; dropped items say why | **pass** | `grep -H "^outcome:" tracker/items/WI-*/item.md` → `delivered` on all four. Nothing was dropped, so nothing owes a reason. This is worth stating rather than assuming: WI-0004 was offered the chance to be dropped in its own Q-002 and the stakeholder refused — *"the import stays part of this, it doesn't get dropped or pushed to a later epic"* — so the absence of a `dropped` outcome here is a decision that was actually taken |
| DE3 | every success measure addressed — met, or explicitly not met with the reason | **pass, all four met**; see the section below |
| DE4 | `docs/product/` reflects what was actually built | **pass, and it is the criterion that held this epic open** | `vision.md` v12: `## How it is used` names all six subcommands and gives `import-csv` its own paragraph explaining the per-import column mapping and the stakeholder's reason for choosing it; the output rule now covers the skipped-row case that exits 0; `## How we will know it works` matches SM3's rewritten wording; and the section formerly headed "Open at the time of writing" is now "Questions put to the stakeholder, and where their answers landed", opening "Nothing is open". At v11 none of that was true |
| DE5 | open questions across all child items closed, or re-filed | **pass** | eighteen question files across five items, every one `status: answered` — sixteen addressed to the stakeholder (five from `intake`, eleven from `refine`) and two to the architect. Spot-checked five `## Consequences` sections and every file they name exists |
| DE6 | claims in `docs/` about behaviour this epic delivered re-checked against the code **during** this epic | **pass** | the section below. Run, not re-read |

## DE3 — the success measures

| # | measure | verdict | evidence |
|---|---------|---------|----------|
| SM1 | from an empty store, documented commands add three people and three expenses paid by different people, producing a report whose amounts a reader can reproduce by hand | **met** | run here from an empty store: `Ana` pays 40.00 shared four ways, `Ben` pays 20.00 shared four ways → `Ana is owed 25.00`, `Ben is owed 5.00`, `Cass owes 15.00`, `Dan owes 15.00`, then `Cass pays Ana 15.00`, `Dan pays Ana 10.00`, `Dan pays Ben 5.00`. Reproducible by hand: each person's share is 15.00, so Ana is +40−15 and Ben +20−15 |
| SM2 | the tool is stopped and restarted between recording and reporting, and the report is unchanged | **met** | structurally, and checked: every command above is a separate `./expenses` process against one JSON file, so the restart is not simulated — it is the only way the tool works. WI-0001 AC7 and WI-0002 AC3 check the persistence directly |
| SM3 | a CSV imported by one documented command, its expenses appearing in the report without being typed | **met** | WI-0004 AC1 and AC3, verified twice against two commits; `README.md`'s `### Importing from your bank` is the documentation, and its console blocks were executed by `verify` and reproduce verbatim. **The measure itself was rewritten** when WI-0004/Q-006 was answered: it required "a CSV file in the stakeholder's bank's export format", which no one but the stakeholder could check. That was a real weakening of the *wording* and a strengthening of the *measure*, and it is recorded in `EP-001/item.md` and in `vision.md` v12 rather than left to be discovered |
| SM4 | every command runs on stock CPython with no network, and the install instructions name no third-party package | **met** | the six modules import only `argparse`, `csv`, `datetime`, `hashlib`, `json`, `os`, `re`, `sys`, `tempfile`. `commands.test` is `python3 -m unittest discover` and `commands.lint` is `python3 -m compileall` — both standard library. `README.md`'s Requirements section reads "A Python 3 interpreter, and nothing else" |

## DE6 — the claims I re-checked by running them

DE6 exists for prose nobody re-reads, and this epic supplied its own evidence that the risk is real:
three false sentences about the report and the command surface sat in `README.md` from WI-0002 and
WI-0003 until a reviewer read the file during WI-0004. So these were run rather than re-read.

| claim | where | checked by | result |
|-------|-------|-----------|--------|
| a remainder is handed one penny at a time to the alphabetically first sharers; `10.00` between three is `3.34`, `3.33`, `3.33` | ADR-0001, `README.md` | 10.00 paid by Ana shared three ways → `Ana is owed 6.66`, i.e. Ana's own share was 3.34 and the other two 3.33 | **true** |
| two names are the same person when they match trimmed and case-folded; the spelling stored is the one used first; people list in normalised order | ADR-0003, `vision.md` | `add-person "  Zoe "` → `Added Zoe`; `add-person zoe` → `Zoe is already registered`; then `ana`, `Ben` → `list-people` gives `ana`, `Ben`, `Zoe` | **true** |
| the data file is `~/.expenses.json` by default and any run can redirect it | ADR-0004, `vision.md`, `README.md` | `DEFAULT_DATA_FILE = os.path.join("~", ".expenses.json")` in `cli.py`, and every one of the six subcommands accepts `--data-file` | **true** |
| the settlement picks the largest debtor and the largest creditor repeatedly, ties by name, and emits at most n−1 payments | ADR-0010 | the SM1 scenario: balances +25/+5/−15/−15 produced exactly three payments in the order the rule predicts, three being n−1 for four non-zero balances | **true** |
| an empty answer is still an answer: a plain sentence and exit 0 | ADR-0005, `vision.md` | against an empty store: `No one is registered yet`, `No expenses recorded yet`, `Nobody owes anybody`, each exit 0 | **true** |
| the report shows one line per person and never one per pair | `vision.md` | every report run above: balances one per person, then payments | **true** |
| the import holds no bank's format; the mapping comes from the command line | `overview.md` v5, `vision.md` v12, ADR-0011 | WI-0004 AC1, AC10 and the `--description-column Balance` case, verified twice | **true** |
| a repeat import is identified by contents, and the stored record is `{sha256, date}` with no path | ADR-0011, `overview.md` v5 | a real imported data file contains `{'date': '2026-08-22', 'sha256': '727db804…'}` and nothing else; a renamed copy warns | **true** |

Nothing was found false. The one document that had fallen behind — `vision.md` — was brought up to
date by `answer-questions` before this review, which is why DE4 passes rather than being waived.

## Findings

**Two, neither of them about the delivered product, and both about the toolkit.** They are recorded
because a closing review is the last chance to say them, and because the harness that runs this
pipeline is the thing they are useful to.

1. **A closable epic is unreachable by the orchestrator.** `open → done` by `review-close` is a
   legal transition, and every precondition for it is satisfiable outside the last child's close —
   but `pipeline.yaml` gives status `open` an `owner: null`, so `next` will never dispatch it. Epic
   closure is therefore reachable *only* from inside the last child's `review-close` execution. That
   is fine when the epic is closable at that instant, and it deadlocks when it is not — which is
   precisely the case the skill's own step 10 provides for, in the words "or leave it open and record
   why". This epic hit it: DE4 legitimately failed at the moment WI-0004 closed, and after
   `answer-questions` fixed the document, `next` reported "nothing runnable" with a closable epic on
   the board. The fix belongs in the toolkit, not here: either `open` gains `review-close` as its
   owner with the DE1 check as a guard, or `next` gains a step for an epic whose children are all
   `done`.
2. **`review-close` cannot file a bug item, though its own procedure tells it to.** Its escalation
   section says a defect belonging to another item becomes a `bug`; `pipeline.yaml` permits
   `null → ready` for actor `verify` only, and `scripts/transition`'s `legal()` compares the actor
   exactly. This bit twice during WI-0004: three stale `README.md` sentences inherited from WI-0002
   and WI-0003, and the pre-existing traceback when `store.save` fails. The first was resolved by
   folding the fix into WI-0004 with each defect attributed; the second is recorded in WI-0004's
   `## Notes` and has no owner.

## Accepted gaps

Everything below is carried in `tracker/items/WI-0004/item.md` under
`### Accepted at closure, and still open (review-close)`, so it survives this closure. Repeated here
because the epic is the last thing anyone will read.

- **A failing `store.save` raises a Python traceback out of `main()`**, for every command in the
  tool. No criterion of any item covers it, and no bug item exists for it — see finding 2.
- **No test protects `README.md`.** The defect that cost WI-0004 a round trip — documentation
  claiming a delivered feature does not exist — is invisible to every automated gate this project
  has. `D12` and `DE4` are scoped to `docs/`, and this project's user-facing documentation is at the
  repository root.
- **Nothing has been run against the stakeholder's real bank export.** By their own decision
  (WI-0004/Q-006) nothing depends on it, and the two likeliest surprises — a quoted thousands
  separator, and charges written as negative amounts — are skipped-and-reported rather than silently
  mishandled. Either would be a new criterion.
- **The stakeholder's promised sample is still to come**, and when it arrives it buys a named
  shortcut for the four import options. That is a **new item under a new epic or a reopening of this
  one**, not unfinished business here: `vision.md` v12, `overview.md` v5 and WI-0004's out-of-scope
  list all say so.
- **AC7's "most recent import date" and AC9's atomicity under interruption** were verified one layer
  down rather than end to end, for reasons recorded in WI-0004's verification report.

## Verdict

**Accepted. EP-001 closed, outcome `delivered`.**

Four items, four `delivered`, eighteen questions all answered, four success measures all met, and a
tool that does what the stakeholder asked for in their opening statement: add people, add expenses
paid by someone and shared by some or all, import expenses from a bank's CSV export instead of
typing them, and show who owes whom — in Python, with no external services, with the data surviving
between runs.

The epic's own story is worth one sentence, because it is the part a reader will not reconstruct
from the code: it was held open by a single missing fact — the shape of the stakeholder's CSV export
— asked for five times over five turns and deferred five times. Nothing was guessed, which was the
stakeholder's explicit instruction. What ended it was not a sixth asking but a different question:
whether the tool could be told the file's shape at each import instead of knowing it in advance. It
could, they chose it, and the epic finished without anyone ever seeing their statement.

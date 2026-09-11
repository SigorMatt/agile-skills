# Review — WI-0002

> **Second review.** The first, at `2026-09-11T04:34:43Z`, **rejected** this item on one finding:
> `docs/architecture/overview.md` said `envelopes` knows about `store`, and it does not. Its full
> text is in the record at [src: commit dc8c054]; its finding 1 is preserved verbatim under
> `## Appendix — the first review's finding 1`, because the overview's own change log cites this
> file for it. `implement` repaired the document at v4, changing no code, and `verify` passed the
> item again at `51e9fd7`. This review is written from scratch against the branch head; it is not
> the old one with a row edited.

## What I examined

- `item.md` — the fourteen acceptance criteria and their tick state; `history.md` — all thirteen
  rows, chaining without a gap to `in-review`; `journal.md` — all fourteen entries, in full;
  `plan.md`, `impl-report.md`, `verify-report.md`, and the previous `review.md`; the five
  questions `Q-001` to `Q-005`, all `answered`.
- **The diff**, hunk by hunk: `git diff main..wi/WI-0002` — 16 files, +1550/−59, `41d690c..40a9767`,
  ten commits. Code: `envel/dates.py` (new, 47 lines), `envel/envelopes.py` (`record_spend`, +63),
  `envel/cli.py` (the `spend` subparser and its dispatch, +23/−6); tests: `tests/test_dates.py`
  (new, 60), `tests/test_cli.py` (+244/−7), `tests/test_envelopes.py` (+133); documents:
  `docs/architecture/overview.md` (the dependency paragraph, +12/−7) and
  `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` (the erratum, +15/−7).
- Every hunk traces to a plan step and to a criterion. The two that are neither new code nor a
  plan step are the adapted `WI-0001` assertion in
  `tests/test_cli.py::CommandLine::test_no_subcommand_and_an_unknown_one` and the overview repair
  the first review ordered — see `## Findings`.
- **The ADR index**, all six documents under `docs/architecture/adr/`, against the diff, for D13.
- **The two documents the invalidation set does not name** — `ADR-0003` and `ADR-0004` — and the
  sections of the two it does name that it does not locate, which is where the first review's
  finding came from. See the answer under `## Invalidation set confirmation`.
- **The claims audit (D12), from the citations rather than from the prose.** Each row names what I
  opened, at the boundary where the claim has one, and its falsifier.

| claim, and where it lives | what I opened, and what it said | falsifier | verdict |
|---|---|---|---|
| `docs/architecture/overview.md` `## The parts`, **the repaired paragraph**: *"`cli` knows about all four modules below it [src: envel/cli.py:13], `envelopes` knows about `money` and `dates` [src: envel/envelopes.py:12], and none of `store`, `money` and `dates` knows anything above it"* | Each cited line, opened. `envel/cli.py:13` is `from . import dates, envelopes, money, store` — four. `envel/envelopes.py:12` is `from . import dates, money` — two, and `store` is not among them. Then the enumeration the quantified half owes. *Set:* the three modules below `envelopes`. *Enumerated by:* `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, **18 lines**. *Members and verdicts:* `envel/store.py` → `json`, `os`, `pathlib`, no `from .` line at all; `envel/money.py` → `re`, none; `envel/dates.py` → `datetime`, `re`, none. | A `from . import cli` or `from . import envelopes` in any of the three — that grep prints every import in the tool and printed none — **or** a module named in the sentence that `envelopes` does not import, which is precisely what the first review found and what this text no longer claims. | **holds** |
| `docs/architecture/overview.md` `## The parts`: *"Reading and writing the store file is `cli`'s work and not `envelopes`' [src: envel/cli.py:68]"* | `envel/cli.py:68` is `path = store.store_path()`. Checked the way that could fail: `grep -n "store\." envel/envelopes.py` → **one hit, line 1, the word `store` in the module docstring** — no use of the module. `grep -n "result.changed\|store.save" envel/cli.py` → `:95` and `:96`, the single guarded write site for all four subcommands. | A `store.load` or `store.save` anywhere in `envel/envelopes.py`, which is the module the sentence exempts. The grep over that file returns only prose. | **holds** |
| `docs/architecture/overview.md` `## The parts`: *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | *Set:* the four modules below `cli`, including the one this item added. *Enumerated by:* `grep -n "print(\|sys.exit\|import sys" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → **exit 1, no output**. *Verdict per member:* no match in any of the four; none of them even imports `sys`. | A `print` in `dates.parse_date`'s error path — the natural place for one in a new module whose whole job is producing user-facing text. There is none: the message travels up inside `DateError` and is printed at `envel/cli.py:88`. | **holds** |
| `docs/architecture/overview.md` `## The parts`: *"`envel/dates.py` — the only place text and calendar dates meet: parse, format, and what today is"* | `grep -n "^def \|^class " envel/dates.py` → `DateError:21`, `parse_date:25`, `format_date:40`, `today:45`. Exactly those three things and the error, and nothing else. | A second module reading or writing a calendar date. `grep -n '"on":' envel/envelopes.py` → one hit, `:152`, and it calls `dates.format_date`; no module converts date text itself. | **holds** |
| `docs/architecture/overview.md` `## Conventions`: *"A date typed at the command line is written `YYYY-MM-DD` and nothing else"* | *Set:* every command-line argument the tool accepts. *Enumerated by:* `grep -n "add_argument" envel/cli.py` → seven — `new.name`; `add.name`, `add.amount`; `spend.name`, `spend.amount`, `spend.description`; and the option `spend.--on`. *Verdict per member:* `--on` is the only date and it goes through `dates.parse_date`; `description` is free text the tool never interprets. | **Checked at the boundary**, not at the happy path: `20260907` is the form `datetime.date.fromisoformat` accepts unaided, so an implementation reaching for it alone would let it through. Run: `./bin/envel spend groceries 1.00 --on 20260907` → exit **1**, stderr *"'20260907' is not a date: write it as YYYY-MM-DD, such as 2026-09-07"*; `--on 2026-09-07` → exit 0. | **holds** |
| `docs/architecture/overview.md` `## The data`: *"An entry's `at` is when the tool recorded it, on every kind of entry"* and *"income carries no date of its own"* | *Set:* the sites that build an entry. *Enumerated by:* `grep -n '"at":\|"on":\|"cents":' envel/envelopes.py` → `:93` (income, four keys: `kind`, `envelope`, `cents`, `at`), `:151`–`:153` (spend: `cents` negative, `on`, `at`). *Verdict per member:* both write `now()` into `at`; the income entry has no `on` key. | `"at": dates.format_date(on)` on the spend, or an `on` on the income entry. Neither is present, and `verify` observed `on` `2026-08-28` beside `at` `2026-09-11T04:42:01Z` in a real store. | **holds** |
| `docs/architecture/overview.md` `## The shape of it`: *"write the whole store back, atomically, but only if something changed"* | `envel/cli.py:95` — `if result.changed:` guarding `store.save(path, result.store)` at `:96`, one write site for all four subcommands. `record_spend` returns `changed=True` only after its four refusals have passed, and each refusal returns a `Refusal`, which `main` prints and exits 1 on before reaching the write. | A subcommand writing unconditionally, or a refusal path reaching `save`. There is one write site, it is guarded, and every refusal returns above it. | **holds** |
| `docs/architecture/adr/ADR-0001` `## Decision`: *"Two functions in `envel/money.py` are the only places the two forms meet"* | *Set:* the places text and cents meet. *Enumerated by:* `grep -rn "\* 100\|// 100\|% 100\|float(" envel/*.py` → **two hits**, `envel/money.py:34` and `envel/money.py:42`, both inside `parse_amount` and `format_amount`. | The module this change added is the obvious candidate — and it converts text to `datetime.date` and touches no cents at all. | **holds** |
| `docs/architecture/adr/ADR-0002` `## Consequences`, **the sentence this branch wrote**: *"`WI-0003` filters income by `at` and a spend by the `on` that field carries [src: ADR-0006]"* | `ADR-0006` `## Consequences` opens *"`WI-0003` sums a month's spending by `on` and a month's income by `at`"*. The surviving half, *"neither needing a format change"*, against `grep -n "FORMAT" envel/store.py` → `FORMAT = 1` at `:11` and three uses at `:30`, `:54`, `:57`, none a second value. | `ADR-0006` saying something else, or a bumped `FORMAT`. Neither. | **holds** |
| `docs/architecture/adr/ADR-0002` `## Corrections`, the erratum's citation `[src: WI-0003 AC8 "A month's money-in figure is the income"]` | `tracker/items/WI-0003/item.md:54` — AC8 begins with exactly those words and states the asymmetry the erratum rests on. | A citation resolving to a criterion that says something else. It does not. | **holds** |
| `docs/architecture/adr/ADR-0006` `## Consequences`, **the reversibility paragraph** — *"No code in this tool writes a spend entry yet [src: run: grep -rn spend envel → exit 1, no output], so today this is one field name and the module that builds an entry"* | Not named by the invalidation set, and this is the item that changes what it is about, so I opened it. Re-running the cited command on the branch now returns hits: this branch is what writes the first spend entry. | A reader taking *"cheap"* for the tool's present position. They cannot: the paragraph's own heading is **"Reversibility: cheap now, a data migration later"**, and its second sentence states the post-delivery position outright — *"Once the stakeholder has recorded a spend, changing it means code that reads the old shape and writes the new one"*. | **holds — a judgement, recorded so it can be disagreed with.** The clause is anchored by `yet`, `now` and `today` to the moment of the decision; the `run:` citation form is *"it records both the command and its outcome"*, a snapshot rather than a standing check; and the spec exempts hedged prose. A reversibility assessment is required to be as-of the decision (`spec/doc-header.md`, *"`## Consequences` MUST state reversibility"*), and this one names both states of the world. See `## Findings`, finding 3. |
| `docs/product/vision.md` `## What it deliberately is not`: *"Not connected to anything: no server, no sync, no bank import, no network."* | *Set:* every import in the tool. *Enumerated by:* the same 18-line grep. *Members:* `argparse`, `sys`, `datetime`, `re`, `copy`, `dataclasses`, `json`, `os`, `pathlib`, plus three intra-package `from .` lines. *Verdict per member:* none is a network, sync or bank facility; `os` and `pathlib` reach the local filesystem only. | `socket`, `http`, `urllib`, `requests`. The new module was the one new place one could have appeared; it adds `datetime` and `re`. | **holds** |
| `docs/product/vision.md` `## What it is for`, item 2: *"Recording a spend against the envelope it came out of."* | Until this item there was nothing behind the sentence. AC1, AC2 and AC3 are now that behaviour, demonstrated in `verify-report.md` `## Criteria`: the spend names its envelope, moves that one and no other, and is refused by name when the envelope does not exist. | A spend reaching an envelope other than the one named. AC2's test asserts the other envelope's listing line is byte-identical across the spend. | **holds** |

`scripts/lint-claims --context work-item --changed-since main` → exit 0, **scope quoted from its
own output**: *"2 document(s) in 2 path(s) differ from main (41d690c) under docs; citations: every
markdown file in the workspace"*. Two documents is the honest branch scope and it is narrow, which
is why the audit above was run over the claims the **invalidation set** names as well, plus the
sections of those documents the set does not locate — which is where the first review's finding
came from and where finding 3 below comes from.

## Definition of Done

| # | criterion | result | evidence |
|---|-----------|--------|----------|
| D1 | every criterion settled | **pass** | fourteen `- [x]` in `item.md`, none `- [~]`, none unsettled; `validate-workspace` → exit 0 |
| D2 | every ticked criterion cites evidence | **pass** | `verify-report.md` `## Criteria` — fourteen rows, each carrying the command the second verification ran against `51e9fd7` and the output it produced |
| D3 | gates passed on the final state of the code | **pass** | the last code commit is `042c96f`; everything above it is record. `verify` ran the suite on `51e9fd7` → `Ran 90 tests`, `OK`; this review re-ran it **on the merge result** at `42dc5817` → exit 0, `Ran 90 tests in 14.974s`, `OK`, and `python3 -m compileall -q envel tests` → exit 0 |
| D4 | no open blocking question | **pass** | `Q-001` to `Q-005` all `status: answered`; `validate-workspace` → exit 0 |
| D5 | a journal entry per execution, history chains | **pass** | fourteen `## ` entries in `journal.md` against thirteen rows in `history.md`; the fourteenth is `implement`'s standalone opening entry at `04:39:01Z`, which records `in-progress → in-progress` and exists so the overview's change-log row has an execution window to fall inside. Last row `verifying → in-review` matches `item.md`'s status; `validate-workspace` → exit 0 |
| D6 | every design decision in a cited ADR | **pass** | `ADR-0006` is the one decision this item took — a spend's own `on` field — created by `plan`, cited from `plan.md` `## Decisions and ADRs` and `## Approach`. The four assumptions `plan` settled instead are in `plan.md` `## Assumptions` with their reversal cost, which is where a non-ADR decision belongs |
| D7 | invalidation set confirmed | **pass** | sixteen entries, every one carrying a disposition; both `to-update` entries were updated with a version bump and a change-log row (`overview.md` v4, `ADR-0002` v2); the fourteen `verified-still-true` entries were reopened row by row below, including the one the first review rejected, which is now `to-update` and repaired. See `## Invalidation set confirmation` for the set and for the question the set cannot answer for itself |
| D8 | every commit references the item | **pass** | `check-commit-refs WI-0002 wi/WI-0002` → exit 0, *"all 10 commit(s) on main..wi/WI-0002 name WI-0002"* |
| D9 | merged into the trunk | **pass** | trial-merged into a detached worktree of `main`: `git merge --no-ff wi/WI-0002` → exit 0, merge result `42dc5817`, suite green on it. The trial was discarded and `git rev-parse main` returned `41d690c`, the sha it returned before it. The real merge is made after this close, and its sha is written into `item.md` by `scripts/record-merge` |
| D10 | verification postdates the code | **pass** | `check-verify-freshness WI-0002 wi/WI-0002` → exit 0, *"verified at 51e9fd78; wi/WI-0002 has moved to 40a97674 but only the record changed (5 file(s) under tracker/ or docs/), so the verification still covers the code"* |
| D11 | review record exists and states what was examined | **pass** | this file; `## What I examined` comes first and names the diff range, the commands run and the boundary probes; every accepted gap below carries an owner and a disposition, `lint-documents --rule accepted-gaps-are-dispatchable --item WI-0002` → exit 0 |
| D12 | claims in `docs/` about the touched behaviour are still true | **pass** | the audit table above — thirteen rows, every one opened at what it cites and every quantified one carrying its set, its enumeration with the command's output, a verdict per member and its falsifier. The repaired dependency paragraph was re-audited with the falsifier the first review used, and it now holds. One row is a recorded judgement rather than a mechanical pass; it is finding 3 |
| D13 | `binding-adrs` is complete | **pass** | `plan.md` `## Binding ADRs` names `ADR-0001` to `ADR-0006`, which is **every** ADR in `docs/architecture/adr/` (`ls` → six files), so no ADR this change engages can be unlisted. Each carries `verify`'s conformance verdict in `verify-report.md` `## ADR conformance`, six rows, each quoting a clause of that ADR's `## Decision`. Conformance is not re-decided here |

**All thirteen criteria pass.**

## Invalidation set confirmation

| document | disposition | confirmed by |
|----------|-------------|--------------|
| `docs/architecture/overview.md` — `## The parts`, the `envel/dates.py` row | verified-still-true | Opened the module. `grep -n "^def \|^class " envel/dates.py` → `DateError`, `parse_date`, `format_date`, `today` — what the row says and nothing more. Confirmed. |
| `docs/architecture/overview.md` — the dependency-direction paragraph | **to-update** | **The first review's finding, and the reason this execution exists.** The document is at **v4**: frontmatter `version: 4`, `updated: 2026-09-11T04:39:01Z`, `updated-by: implement`, `updated-for: WI-0002`, and the top change-log row matches all four and names where the false clause came from. The replacement text was audited above against each line it cites and against the falsifier that caught the original. `## Decision`-equivalent content — the module split itself — is untouched. Confirmed. |
| `docs/architecture/overview.md` — *"nothing below `cli` prints … calls `sys.exit`"* | verified-still-true | Reopened independently; the grep over the four modules returns nothing and none imports `sys`. Confirmed. |
| `docs/architecture/overview.md` — `## The data`, the negative `cents` and the `on` field | verified-still-true | Read against `envel/envelopes.py:151`–`:153`: `"cents": -cents`, `"on": dates.format_date(on)`, `"at": now()`. Confirmed. |
| `docs/architecture/overview.md` — *"A date typed at the command line is written `YYYY-MM-DD` and nothing else"* | verified-still-true | Reopened at the boundary form `20260907`, run against the tool: refused, exit 1. Confirmed. |
| `docs/architecture/overview.md` — `## Engagement state` | owned-by-ending | `git diff main..wi/WI-0002 -- docs/architecture/overview.md` has three hunks — frontmatter, the dependency paragraph, the change-log row — and none in this section. The item left it alone, which is what this disposition requires. Confirmed. |
| `ADR-0006` — `## Decision`, the JSON entry and its four bullets | verified-still-true | Read field for field against `envel/envelopes.py:145-155` and against the seven real entries `verify` wrote: `on` on every spend including those without `--on`, `description` only when typed, `cents` always negative. Confirmed. |
| `ADR-0006` — *"The document's `format` stays `1`"* | verified-still-true | `grep -n "FORMAT" envel/store.py` → `FORMAT = 1` at `:11`, three uses, no second value. Confirmed. |
| `ADR-0002` — *"`at` is when the tool recorded the entry"* | verified-still-true | Both write sites, `envel/envelopes.py:93` and `:153`, write `now()`; no user date reaches `at`. Confirmed. |
| `ADR-0002` — *"An envelope's balance is the sum of `cents` over the entries naming it"* | verified-still-true | `balance` is unchanged by the branch — `git diff main..wi/WI-0002 -- envel/envelopes.py` has no hunk inside it — and sums with no branch on `kind`, which is why a spend is stored negative. Confirmed. |
| `ADR-0002` — `## Consequences`, *"`WI-0003` filters by `at`"* | to-update | Updated: version 1 → 2, a change-log row, an erratum in an append-only `## Corrections`, `## Decision` untouched. The replacement sentence and the erratum's citation were both audited above. Confirmed. |
| `ADR-0001` — *"Two functions in `envel/money.py` are the only places the two forms meet"* | verified-still-true | The conversion grep returns `money.py:34` and `money.py:42` only. Confirmed. |
| `ADR-0005` — `## Decision`, the two commands | verified-still-true | Both re-run by this review **on the merge result**: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests`, `OK`; `python3 -m compileall -q envel tests` → exit 0. No third-party import was added. Confirmed. |
| `docs/product/vision.md` — *"Recording a spend against the envelope it came out of."* | verified-still-true | AC1 to AC3 are that behaviour and were demonstrated. Confirmed. |
| `docs/product/vision.md` — *"Not connected to anything …"* | verified-still-true | The 18-line import enumeration; nothing network-shaped. Confirmed. |
| `docs/product/vision.md` — `## Engagement state` | owned-by-ending | `git diff main..wi/WI-0002 -- docs/product/vision.md` is **empty**. Confirmed. |

**Did this change falsify a document the set does not name?** Eight documents live under `docs/`.
The set names six. I read the two it does not, and — because the first review's finding was a
*sentence* inside a document the set names — I also read the sections of those six that the set
does not locate.

- **`ADR-0003` (store location).** Its `## Decision` is about `store_path`'s three-step
  resolution. `git diff --name-only main..wi/WI-0002 -- envel bin` lists `cli.py`, `dates.py`,
  `envelopes.py` — `envel/store.py` is untouched, so nothing it decides moved. Every criterion of
  this item was demonstrated by setting `ENVEL_FILE`, which is the property the ADR was decided
  for. **Still true.**
- **`ADR-0004` (package and shim).** *"there are two ways to start it, both reaching the same
  `main`"* — `bin/envel:9` and `envel/__main__.py:5` are both `from envel.cli import main`, and
  neither file is in the branch's diff. *"No third-party packaging or dependency is introduced"* —
  the new module adds `datetime` and `re`, and the 18-line enumeration contains nothing outside
  the standard library. **Still true.**
- **The unnamed sections of the named documents.** `overview.md` `## The shape of it` and
  `## What is not decided yet`, and `ADR-0006` `## Consequences`. The first two hold and are
  audited above. The third is where the honest answer is **yes, partly**: `ADR-0006`
  `## Consequences` contains a reversibility clause that this item is exactly what dates — *"No
  code in this tool writes a spend entry yet"* — and its cited command no longer returns what it
  records. I read it as holding, because every clause of it is anchored by `yet`/`now`/`today` and
  the paragraph states the post-delivery position in its next sentence. That is a judgement and it
  is written down as finding 3 rather than buried in a verdict, so that the next reader can
  disagree with it without re-deriving it.

## Sections restated at the ending

`not an ending` — this is an item close, and `## Engagement state` sections belong to the
engagement's ending (DE4). `lint-documents --rule engagement-state-is-restated --item WI-0002
--context work-item` agrees: *"NOT APPLICABLE — an item close is not an ending, and the sections
are the ending's"*. Both documents carrying such a section were confirmed untouched by the branch,
under `## Invalidation set confirmation`.

## Findings

**1. The first review's finding is repaired, and the repair is right. Closed.**

`docs/architecture/overview.md` `## The parts` said *"`envelopes` knows about `store`, `money` and
`dates`"*, and `envel/envelopes.py:12` is `from . import dates, money`. At v4 the paragraph says
what the code says, cites each edge at the line that carries it, and states the property the false
version was hiding: `envelopes` never opens a file, so the decision layer is a pure function of
(store, arguments). I re-ran the falsifier that caught the original — the import enumeration over
the whole tool, and `grep -n "store\." envel/envelopes.py`, which returns only the word in the
module docstring — and the new text survives it. The invalidation row moved to `to-update`, the
version was bumped with a change-log row naming where the false clause came from, and **no code
changed**, which is what the send-back asked for. Nothing was renumbered and no criterion moved.

**2. The adapted `WI-0001` test — accepted, unchanged from the first review.**
`tests/test_cli.py::CommandLine::test_no_subcommand_and_an_unknown_one` asserted the literal
`{new,add,list}`. The branch replaced it with an assertion that the first line starts
`usage: envel ` and names each of `new`, `add`, `list` and `spend`. Read against `WI-0001` AC14 —
*"a usage message that lists the subcommands the tool does have"* — that is **stricter**, not
weaker: it keeps the tool-versus-subcommand distinction AC15 turns on and drops only a literal a
fourth subcommand necessarily falsifies. `git diff main..wi/WI-0002 -- tracker/items/WI-0001/` is
empty, so no criterion of `WI-0001` was edited to make anything pass. Accepted.

**3. `ADR-0006`'s reversibility clause is now out of date in its tense, and I am not sending the
item back for it.** Recorded because the judgement, not the conclusion, is the useful part.

> **Reversibility: cheap now, a data migration later.** No code in this tool writes a spend entry
> yet [src: run: grep -rn spend envel → exit 1, no output], so today this is one field name and
> the module that builds an entry.

This branch is what makes the cited command return something. Three things decide it the other
way. The clause is hedged in every part — `yet`, `now`, `today` — and `spec/doc-header.md` §4a says
hedged prose is not what citations are for. The `run:` citation form *"records both the command and
its outcome"*, which makes it a snapshot of a moment rather than a standing check. And a
reversibility statement is *required* to be as-of the decision — `## Consequences` MUST state
reversibility — while this one names both states of the world and describes the one we are now in:
*"Once the stakeholder has recorded a spend, changing it means code that reads the old shape and
writes the new one."* A reader is not misled and no decision is wrong, so there is nothing an
erratum would add beyond churn on an ADR one execution old. **If a later reader disagrees**, the
repair is `doc-header.md` §4b — a `## Corrections` row, a change-log row and a version bump, with
no code change — and it does not need this item reopened.

**4. The refusal order differs between `add_income` and `record_spend` — accepted, unchanged.**
`add_income` checks the amount first; `record_spend` checks the envelope first, which is what makes
AC3's promise of a message naming the envelope hold on `envel spend nosuch 0 --on 2099-01-01`,
where three criteria refuse at once
(`tests/test_envelopes.py::RecordSpend::test_the_envelope_is_checked_before_the_amount_and_the_date`
fixes it). No criterion of either item is violated. The risk the plan names — a later reader
harmonising them and silently changing delivered `WI-0001` behaviour — is mitigated where that
reader will be standing: `record_spend`'s docstring says why the order is what it is. See
`## Accepted gaps`.

**Nothing else.** Every code hunk maps to a plan step and a criterion; no unrequested scope; no ADR
contradicted. `record_spend` is code I would maintain — four refusals in one stated order, each
returning a message as a value, and a new module that earns its place by keeping
`fromisoformat`'s extra permissiveness out of the tool at the one line where it would otherwise
enter.

## Accepted gaps

| gap | owner | disposition |
|-----|-------|-------------|
| That `at` is UTC rather than the machine's local time cannot be shown here: this machine's local time and UTC coincide, so no observation distinguishes them (`verify-report.md` `## Not verified`). No acceptance criterion of any item names `at`, so nothing is ticked on it; `ADR-0006` `## Consequences` records the intent. A limitation of the machine, not work anyone can do. | none | no-owner |
| A spend's `on` is never printed back, so this item's dates were observed in the store file rather than in the tool's output. Making a spend's date visible in a month's figures is the summary. | WI-0003 | item-filed:WI-0003 |
| The same gap's other half: a spend's `description` is never printed back either, and looking up the spends recorded against an envelope is where it becomes visible. | WI-0006 | item-filed:WI-0006 |
| No check that a stored entry names an envelope that still exists. `plan.md` `## Assumptions` records it as a deliberate non-decision: no command in this tool can produce the state, and the delivered listing already ignores such an entry. | none | no-owner |
| `--on` given twice, and an empty or whitespace-only description. Both are settled as `plan` assumptions with a one-line reversal each, no criterion constrains either, and neither was exercised. | none | no-owner |
| Concurrency, large stores and interrupted writes. `ADR-0002`'s atomic-write claim belongs to `WI-0001`, which closed on it; this item did not re-verify it. | none | no-owner |
| `add_income` and `record_spend` check their refusals in different orders (finding 4). Nobody has asked for them to be harmonised, and harmonising would change delivered `WI-0001` behaviour that `WI-0001` AC5 and AC10 constrain, so filing an item would be manufacturing scope. Recorded as a limitation; the route if anyone does want it is a new item. | none | no-owner |
| `ADR-0006`'s reversibility clause reads in the present tense about a state this item ended (finding 3). Judged to hold as a tense-anchored statement of the decision moment; if a later reader disagrees the repair is a `## Corrections` row under `doc-header.md` §4b, which needs no item and no code change. | none | no-owner |
| Whether the repaired overview paragraph is the *best* description of the architecture rather than merely a true one. Every edge it asserts was opened at the line it cites. Whether the document should say more is `plan`'s judgement and not this stage's. | none | no-owner |

## Verdict

**Accepted — merged and closed, outcome `delivered`.**

Fourteen acceptance criteria are demonstrated with evidence a reader can re-run, ninety tests are
green on the merge result rather than only on the branch, six binding ADRs carry conformance
verdicts, sixteen invalidation entries are disposed and confirmed, and the one defect the first
review found is repaired in the document rather than papered over in the code. The record answers
what was built and why, which skill decided what, what the five questions asked and what the
stakeholder answered, and what two verifications found — including the thing they both got wrong
and how it was caught.

## Appendix — the first review's finding 1

Preserved verbatim in substance, because `docs/architecture/overview.md`'s v4 change-log row cites
this file for it. The first review in full is at [src: commit dc8c054].

> **1. `docs/architecture/overview.md` says `envelopes` depends on a module it does not depend on.
> Send-back.**
>
> `## The parts`, the paragraph under the module table:
>
> > The dependency direction is one way: `cli` knows about `envelopes`, `envelopes` knows about
> > `store`, `money` and `dates`, and none of those three knows anything above it.
>
> `envel/envelopes.py:12` reads `from . import dates, money`. It never imports `envel/store.py`
> and never uses it. The module that knows about `store` is `envel/cli.py`.
>
> Three things made it this item's to fix: `plan` rewrote this sentence for `WI-0002` at overview
> v3; it is row 2 of this item's own invalidation set, disposed `verified-still-true` twice, by
> `implement` and by `verify`, each of which printed a line showing **two** modules and concluded
> a three-module claim held; and the false version understates the architecture, because
> `envelopes` never touching the filesystem is the property that makes the decision layer pure.
>
> Both audits checked the falsifier they expected — an upward import — rather than the sentence's
> own subject. That is D12's failure mode exactly, and it is why D12 is not discharged by opening
> what a claim cites.

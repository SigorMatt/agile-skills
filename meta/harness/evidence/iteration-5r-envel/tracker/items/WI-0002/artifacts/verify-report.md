# Verification report — WI-0002

Verified-commit: 51e9fd7817e0b263668ac55d9ae14e79732af7c4

> **Second verification.** `verify` passed this item at `d94a2da` and `review-close` then rejected
> it: `docs/architecture/overview.md` claimed `envelopes` knows about `store`, and the first
> verification had reopened that very sentence and called it true while quoting the import line
> that disproves it. `implement` repaired the document at v4 and changed no code. This report is
> written from scratch against the new branch head; it is not the old one with a row edited. The
> repaired sentence is reopened below with the enumeration it is owed, and the mistake the first
> report made is named rather than quietly replaced.

## Verdict

**Pass.** All fourteen acceptance criteria were demonstrated again, independently, by running the
tool as separate processes against scratch stores of this execution's own making. The one defect
the review found is repaired and the repaired sentence is true. No criterion is `substituted` and
none is `ambiguous`. No new defect was found, in this item or in another's delivered behaviour, so
no bug item was filed.

What each criterion would take to settle was decided from `item.md` before `impl-report.md` was
reopened. Every row below carries a command this execution ran and the output it produced.

## Criteria

Unless another store is named, the commands run against a scratch store built in this order:
`envel new groceries`, `envel add groceries 40`, `envel new car`, `envel add car 10`, with
`ENVEL_FILE` set to a path that did not exist [src: ADR-0003]. Every invocation is a separate
process; `envel` is `./bin/envel` [src: ADR-0004].

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `envel spend groceries 12.50` then `envel list` | `spent 12.50 from groceries, which now holds 27.50`, exit 0, stderr empty; the listing reads `car  10.00` / `groceries  27.50` | Envelope first, amount second — the same order as `envel add groceries 40`, whose own line is `added 40.00 to groceries, which now holds 40.00`. |
| AC2 | pass | `envel list`, `envel spend groceries 1.00`, `envel list` | before `car  10.00` / `groceries  27.50`; after `car  10.00` / `groceries  26.50` | Reduced by exactly 1.00. `diff` of the `car` line before and after is empty — byte-identical, not merely equal in value. |
| AC3 | pass | `envel spend nosuch 5` then `envel list` | `there is no envelope called 'nosuch'. Nothing has been recorded.` on stderr, exit 1, stdout empty; the listing unchanged at `car  10.00` / `groceries  26.50` | The message names the envelope. In the AC13 store the spend-entry count was unchanged across this refusal. |
| AC4 | pass | four separate processes sharing one fresh `ENVEL_FILE`: `new groceries`, `add groceries 40`, `spend groceries 12.50`, `list` | the fourth prints `groceries  27.50` | The store file did not exist before the first process (`test -e` → no). Every row of this table is a separate invocation, so persistence is exercised throughout; this row is the criterion's own sequence. |
| AC5 | pass | `envel spend car 12.50` with `car` holding 10.00, then `envel list`; then `envel spend car 10.00` | `car holds 10.00, which is less than 12.50. Nothing has been recorded; move money into it first if you want to spend that.` on stderr, exit 1; listing still `car  10.00`. Then exactly-what-is-left exits 0 and the listing reads `car  0.00` | The message names the envelope and how much is left. **Boundary checked on both sides:** AC5 refuses only *larger than*, so 10.00 out of 10.00 is accepted and lands on zero. Both scratch stores were then read with Python: neither listing contains a `-` anywhere. |
| AC6 | pass | `envel spend groceries 0` and `envel spend groceries -5`, each followed by `envel list` | `a spend has to be more than zero, and 0.00 is not. Nothing has been recorded.` / `… and -5.00 is not. …` on stderr, exit 1 each; the listing reads `groceries  24.50` before and after both | The negative form reaches the tool rather than argparse — the message is the tool's own wording, not a parser error. |
| AC7 | pass | `envel spend groceries 2.00` | `spent 2.00 from groceries, which now holds 24.50` on stdout | The remaining amount is in the success line. No `list` was run to obtain it. |
| AC8 | pass | in a **fresh** `ENVEL_FILE`: `new groceries`, `add groceries 40`, `spend groceries 1.00`, `spend groceries 1.00 --on 2020-01-01`, then `json.load` of the store | `{'kind': 'spend', …, 'on': '2026-09-11', 'at': '2026-09-11T04:42:01Z'}` and `{…, 'on': '2020-01-01', 'at': '2026-09-11T04:42:01Z'}`; `datetime.date.today()` printed `2026-09-11` | The criterion's own sequence in the store of its own that it names. Nothing extra was typed for the first spend and nothing prompted. Today's date was read from the clock at run time, never written as a literal. |
| AC9 | pass | in the store of AC8: `envel spend groceries 12.50 --on 2026-08-28`, then `json.load` | `{'kind': 'spend', 'envelope': 'groceries', 'cents': -1250, 'on': '2026-08-28', 'at': '2026-09-11T04:42:01Z'}` | Held against the date given, not the day it was typed: `on` and the date part of `at` are fourteen days apart. |
| AC10 | pass | in the store of AC8: `spend groceries 1.00 lunch`; `spend groceries 1.00`; `spend groceries 1.00 --on 2026-09-07`; `spend groceries 1.50 lunch --on 2026-09-07` | exit 0 each; the four entries carry, in order, `description: 'lunch'` and no `on` other than today's; **no `description` key**; `on: '2026-09-07'` and no `description`; and both `description: 'lunch'` and `on: '2026-09-07'` | All four shapes the criterion names. Nothing prompted for a description and leaving it out was not refused. |
| AC11 | pass | `--on` given `2026-09-07`, then each of `7/9`, `09-07`, `yesterday`, `2026-9-7`, `20260907`, `2026/09/07`, `07-09-2026`, `2026-13-45`, `2026-02-30`; `envel list` after the sweep | `2026-09-07` exits 0. Each of the other eight exits 1 with stdout empty — `'7/9' is not a date: write it as YYYY-MM-DD, such as 2026-09-07` for the seven malformed ones, and `'2026-13-45' is not a day that exists: …` for the two that are the right shape and not real days | Nothing recorded for any refusal: the listing after the sweep reads `groceries  20.00`, exactly the one accepted spend below the balance before it. **`20260907` is the boundary that matters** — it is what `datetime.date.fromisoformat` accepts unaided, so an implementation reaching for it alone would let it through. It is refused. |
| AC12 | pass | `--on` set to tomorrow, then to today, then to yesterday — all three computed from `datetime.date.today()` at run time | tomorrow (`2026-09-12`): `2026-09-12 is in the future. Nothing has been recorded.` on stderr, exit 1, listing unchanged at `groceries  20.00`. Today (`2026-09-11`): exit 0. Yesterday (`2026-09-10`): exit 0 | Both sides of the boundary the criterion turns on. No date in this row is a literal. |
| AC13 | pass | a sweep in a store of its own, one invocation per criterion AC13 names, measuring bytes on each stream and the exit code | refusals — AC3 `0/65/1`, AC5 `0/122/1`, AC6 `0/78/1`, AC11 `0/64/1`, AC12 `0/56/1`, AC14 `0/133/2` (stdout bytes / stderr bytes / exit). Successes — AC1, AC7, AC8, AC9, AC10 each `49/0/0` | Checked case by case against the criteria AC13 itself names, which is what it asks for. See `### a-criterion-about-criteria-is-read` below. |
| AC14 | pass | `envel spend`, `envel spend groceries`, `envel spend groceries 12.50 lunch extra`, with the store's spend-entry count read before and after | each prints `usage: envel spend [-h] [--on YYYY-MM-DD] name amount [description]` to stderr and exits 2, stdout empty; the spend-entry count is 10 before and 10 after | The usage printed is the **subcommand's** — it begins `usage: envel spend`, not `usage: envel`. The third case is rejected for the word beyond the description, as the criterion specifies. |

## ADR conformance

| ADR | verdict | clause quoted from its `## Decision` | file and line, or why not engaged |
|-----|---------|--------------------------------------|-----------------------------------|
| ADR-0001 | conforms | *"Every amount is a Python `int` counting cents, everywhere inside the tool and everywhere in the stored file"*, and *"Two functions in `envel/money.py` are the only places the two forms meet"* | `grep -rn "def parse_amount\|def format_amount" envel/money.py` → `envel/money.py:20` and `envel/money.py:38`, still the only two. `grep -rn "\* 100\|// 100\|% 100\|float(" envel/*.py` → two hits, `envel/money.py:34` and `envel/money.py:42`, both inside those functions: no other module converts. `record_spend` is handed `cents` already parsed and stores `-cents` at `envel/envelopes.py:151`. |
| ADR-0002 | conforms | *"An envelope's balance is the sum of `cents` over the entries naming it"*, and *"`at` is when the tool recorded the entry"* | `envel/envelopes.py:47` — `balance` sums `entry["cents"]` over every entry whose folded name matches, with **no branch on `kind`**; `git diff main..HEAD -- envel/envelopes.py` contains no hunk inside its body. That is why a spend is stored negative. `grep -n '"at":' envel/envelopes.py` → `:93` (income) and `:153` (spend), both `now()`, the run's own UTC moment; AC9 shows `on` `2026-08-28` beside `at` `2026-09-11T04:42:01Z`, so no user date reaches `at`. `FORMAT = 1` at `envel/store.py:11`. |
| ADR-0003 | conforms | *"The store path is, in order: `$ENVEL_FILE`, used exactly as given … `$XDG_DATA_HOME/envel/envelopes.json` … `~/.local/share/envel/envelopes.json`"* | `envel/store.py:33` — `store_path` is untouched by this branch (`git diff --stat main..HEAD -- envel` lists `cli.py`, `dates.py`, `envelopes.py` only). Every criterion above was demonstrated by setting `ENVEL_FILE` to a path that did not exist, which is the property the ADR was decided for. |
| ADR-0004 | conforms | *"The tool is the package `envel/`, and there are two ways to start it, both reaching the same `main`"*, and *"No third-party packaging or dependency is introduced"* | `bin/envel:9` and `envel/__main__.py:5` both `from envel.cli import main`, neither touched by this branch. The import enumeration below lists 18 lines over six files; every non-relative one is standard library — `argparse`, `sys`, `datetime`, `re`, `copy`, `dataclasses`, `json`, `os`, `pathlib`. The module this item added contributes `datetime` and `re`. |
| ADR-0005 | conforms | *"`commands.test`: `python3 -m unittest discover -s tests -t .`"* and *"`commands.lint`: `python3 -m compileall -q envel tests`"* | `tracker/project.yaml:14` and `:15` still carry exactly those two, and both were run by this execution on `51e9fd7`: exit 0 with `Ran 90 tests in 15.082s`, `OK`, and exit 0. `tests/test_dates.py:1` is a `unittest` module importing only `datetime` and `unittest`, so the suite still needs nothing installed. |
| ADR-0006 | conforms | *"A spend entry carries `on`, a calendar date written `YYYY-MM-DD`, being the day the money was spent"*, *"`on` is present on every spend entry, including one recorded without `--on`"*, *"`description` is present only when one was typed"*, *"`cents` on a spend is **negative**"*, *"The document's `format` stays `1`"* | `envel/envelopes.py:148` builds exactly that entry. Checked against the **seven** real spend entries this execution wrote into the AC8 store, printed above: every one carries `on`, including the four written without `--on`; `description` is present on the two typed with one and absent on the five without; `cents` is `-100`, `-150`, `-1250` and never positive; every store file read back has `"format": 1`. |

No ADR outside the plan's list was found engaged by this change. The plan's list is all six ADRs
in `docs/architecture/adr/`, so there is none it could have missed.

## Invalidation set

Sixteen entries, all disposed. Every `verified-still-true` was reopened here against
`51e9fd7`; the one `to-update` was reopened against the repaired document. **No document was
written by this execution.**

| document | disposition | what I reopened, and what I found |
|----------|-------------|------------------------------------|
| `docs/architecture/overview.md` — `## The parts`, the `envel/dates.py` row | verified-still-true | Opened the module. `grep -n "^def \|^class " envel/dates.py` → `DateError` at `:21`, `parse_date` at `:25`, `format_date` at `:40`, `today` at `:47`. That is what the row says — parse, format, and what today is — and nothing more. **True.** |
| `docs/architecture/overview.md` — the dependency-direction paragraph | **to-update** | **This is the entry the send-back was about, and it is the one to read carefully.** The first execution disposed it `verified-still-true` and the first verification confirmed that; both were wrong. `implement` has now repaired it at **v4** and the row says `to-update`, which is the disposition it should always have carried. Reopened against the branch head: *Set:* the modules below `cli` — `store`, `money`, `dates`. *Enumerated by:* `grep -rn "^import \|^from " envel/*.py bin/envel` → exit 0, 18 lines. *Members and verdicts:* `envel/store.py` → `json`, `os`, `pathlib`, no `from .` line; `envel/money.py` → `re`, none; `envel/dates.py` → `datetime`, `re`, none — so none of the three knows anything above it. *Falsifier:* a `from . import cli` or `from . import envelopes` in any of the three; that grep prints every import in the tool and printed none. The three **new** edges the paragraph asserts were each opened at the line it cites: `envel/cli.py:13` is `from . import dates, envelopes, money, store` (all four modules below it); `envel/envelopes.py:12` is `from . import dates, money`; `envel/cli.py:68` is `path = store.store_path()`. The claim that reading and writing is `cli`'s and not `envelopes`' was checked the way that could have failed: `grep -rn "store\.[a-z_]*(" envel/*.py` → **three hits, all in `envel/cli.py`** (`:68`, `:70`, `:96`), and `grep -n "store\." envel/envelopes.py` → one hit, the word `store` in the docstring. **True, and the version bump and change-log row are both present:** frontmatter `version: 4`, `updated: 2026-09-11T04:39:01Z`, `updated-by: implement`, `updated-for: WI-0002`, and the top change-log row matches all three. |
| `docs/architecture/overview.md` — *"nothing below `cli` prints, and nothing below `cli` calls `sys.exit`"* | verified-still-true | Quantified, and the one this change could most plausibly have falsified, since it adds a module below `cli` that produces user-facing text. *Set:* the four modules below `cli`. *Enumerated by:* `grep -n "print(\|sys.exit\|import sys" envel/envelopes.py envel/store.py envel/money.py envel/dates.py` → **exit 1, no output**. *Verdict per member:* no match in any of the four, and none of them even imports `sys`. *Falsifier:* a `print` in `dates.parse_date`'s error path, which is exactly where one would naturally go; there is none — the message travels up inside `DateError` and is printed at `envel/cli.py:88`. **True.** |
| `docs/architecture/overview.md` — `## The data`, the negative `cents` and the `on` field | verified-still-true | Read against `envel/envelopes.py:145-155` and against the seven real entries above. `"cents": -cents`, `"on": dates.format_date(on)`, `"at": now()`. **True.** |
| `docs/architecture/overview.md` — *"A date typed at the command line is written `YYYY-MM-DD` and nothing else"* | verified-still-true | Quantified. *Set:* every command-line argument the tool accepts. *Enumerated by:* `grep -n "add_argument" envel/cli.py` → seven — `new.name`; `add.name`, `add.amount`; `spend.name`, `spend.amount`, `spend.description`; and the option `spend.--on`. *Verdict per member:* `--on` is the only one that is a date and it goes through `dates.parse_date`; `spend.description` is free text the tool never interprets. *Falsifier at the boundary:* `20260907`, the form the underlying `fromisoformat` accepts on its own — refused, along with seven other forms, in AC11's sweep. **True.** |
| `docs/architecture/overview.md` — `## Engagement state` | owned-by-ending | Left exactly as it is. `git diff main..HEAD -- docs/architecture/overview.md | grep -c "Engagement state"` → **0**: this branch's only hunks in that document are the dependency paragraph, the frontmatter and the change-log row. Its sentences are false — `WI-0001` is `done` — and the ending owns them. |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` — `## Decision`, the JSON entry and its four bullets | verified-still-true | Reopened and checked field for field against seven real entries; see the `ADR-0006` row above. **True.** |
| `docs/architecture/adr/ADR-0006-a-spend-carries-the-date-it-happened.md` — *"The document's `format` stays `1`"* | verified-still-true | `grep -n "FORMAT" envel/store.py` → `FORMAT = 1` at `:11` and three uses (`:30`, `:54`, `:57`), none introducing a second value. Every scratch store this execution wrote reads back `"format": 1`. *Falsifier:* a bumped constant or a branch on another value; neither exists. **True.** |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — *"`at` is when the tool recorded the entry"* | verified-still-true | Quantified. *Set:* the sites that write an entry. *Enumerated by:* `grep -n '"at":' envel/envelopes.py` → two, `:93` and `:153`. *Verdict per member:* both write `now()`. *Falsifier:* `"at": dates.format_date(on)` on the spend — observed directly not to be the case in AC9, where `on` is `2026-08-28` and `at` is `2026-09-11T04:42:01Z`. **True.** |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — *"An envelope's balance is the sum of `cents` over the entries naming it"* | verified-still-true | Quantified over entry kinds: `income` and `spend`. `envel/envelopes.py:47` sums with no branch on `kind`, and `git diff main..HEAD -- envel/envelopes.py` shows no hunk inside it. *Verdict per member:* both kinds summed identically, which is why the spend is stored negative. *Boundary:* spending an envelope to exactly zero gives `car  0.00` — not a special case and not a negative. **True.** |
| `docs/architecture/adr/ADR-0002-store-is-a-json-entry-log.md` — `## Consequences`, *"`WI-0003` filters by `at`"* | to-update | The document **was** updated by the first execution: version 2, a change-log row, an erratum in `## Corrections`, `## Decision` untouched. Reopened here: the replacement sentence says income is filtered by `at` and a spend by the `on` it carries and cites `ADR-0006`, whose `## Consequences` reads *"`WI-0003` sums a month's spending by `on` and a month's income by `at`"*. The erratum's citation `[src: WI-0003 AC8 "A month's money-in figure is the income"]` opens to `tracker/items/WI-0003/item.md:54`, which begins with exactly those words. The surviving half — no format change — is `envel/store.py:11`. **True.** |
| `docs/architecture/adr/ADR-0001-amounts-are-integer-cents.md` — *"Two functions in `envel/money.py` are the only places the two forms meet"* | verified-still-true | Quantified. *Set:* the places text and cents meet. *Enumerated by:* `grep -rn "\* 100\|// 100\|% 100\|float(" envel/*.py` → two hits, both inside `money.py`. *Falsifier:* the module this change added, which is the obvious candidate — it converts text to `datetime.date` and touches no cents at all. **True.** |
| `docs/architecture/adr/ADR-0005-checks-are-stdlib-only.md` — `## Decision`, the two commands and what lint checks | verified-still-true | Both re-run by this execution on `51e9fd7`: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests in 15.082s`, `OK`; `python3 -m compileall -q envel tests` → exit 0. No third-party import was added. **True.** |
| `docs/product/vision.md` — *"Recording a spend against the envelope it came out of."* | verified-still-true | This item is what puts behaviour behind the sentence, and AC1, AC2 and AC3 are that behaviour: the spend names its envelope, comes out of that one and no other, and is refused when the envelope does not exist. **True.** |
| `docs/product/vision.md` — *"Not connected to anything: no server, no sync, no bank import, no network."* | verified-still-true | Quantified. *Set:* every import in the tool. *Enumerated by:* the same 18-line grep. *Members:* `argparse`, `sys`, `datetime`, `re`, `copy`, `dataclasses`, `json`, `os`, `pathlib`, plus three intra-package `from .` lines. *Verdict per member:* none is a network, sync or bank facility; `os` and `pathlib` reach the local filesystem only. *Falsifier:* `socket`, `http`, `urllib`, `requests` — none present, and the new module adds `datetime` and `re`. **True.** |
| `docs/product/vision.md` — `## Engagement state` | owned-by-ending | Left exactly as it is. `git diff main..HEAD -- docs/product/vision.md` is empty. |

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | pass | run by this execution on `51e9fd7`: `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 90 tests in 15.082s`, `OK` |
| `lint-clean` | pass | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | pass | `python3 .claude/agile-skills/scripts/validate-workspace .` → exit 0, 7 items, 8 documents |
| `every-criterion-independently-checked` | pass | the fourteen rows of `## Criteria`, each carrying a command this execution ran and the output it produced. No row's evidence is `impl-report.md`; the report was not reopened until the criteria had been settled. |
| `negative-cases-exercised` | pass | `## Negative and boundary cases exercised` — twenty-four invocations, every one triggered rather than read about |
| `a-criterion-about-criteria-is-read` | pass | AC13 is the one criterion of this shape; see below |
| `adr-conformance-is-decided` | pass | `lint-documents --rule adr-conformance-is-decided --item WI-0002` → exit 0, *"6 binding ADR(s), 6 conformance row(s)"*; each row quotes a clause of that ADR's `## Decision` and names the file and line that satisfies it |
| `invalidation-set-is-disposed` | pass | `lint-documents --rule invalidation-set-is-disposed --item WI-0002` → exit 0, *"16 invalidation entr(y/ies) against 16 row(s) in the verification report"* |
| `tests-would-fail-without-the-change` | pass, advisory | `## Test sensitivity check` — ten behaviours removed one at a time, every one turning the suite red |

### `a-criterion-about-criteria-is-read` — AC13

AC13's subject is other criteria: *"Checked case by case against the criteria that name them:
refusals at AC3, AC5, AC6, AC11, AC12 and AC14; success at AC1, AC7, AC8, AC9 and AC10."*

1. **The criteria it covers, by ID** — the criterion names them itself: AC3, AC5, AC6, AC11, AC12
   and AC14 as refusals; AC1, AC7, AC8, AC9 and AC10 as successes. Eleven of the other thirteen.
   AC2 and AC4 are about a balance and about persistence and name no stream.
2. **Per-criterion verdict**, read against the behaviour rather than against the suite. The sweep
   measured bytes on each stream: every one of the six refusals wrote **0 bytes to stdout** and a
   non-empty message to stderr (65, 122, 78, 64, 56 and 133 bytes) and exited non-zero — 1 for the
   five the tool refuses and 2 for AC14, which argparse refuses. Both are non-zero, which is what
   the criterion asks. Every one of the five successes wrote 49 bytes to stdout, **0 bytes to
   stderr**, and exited 0.
3. **Tests as evidence, not as the definition.** `tests/test_cli.py::Spend::test_every_refusal_goes_to_stderr_and_every_success_to_stdout`
   is a table keyed by those same criterion IDs, and it was among the failures in three of the ten
   sensitivity probes below — so it is sensitive. The suite being green is not what settled AC13;
   the byte sweep in the AC13 row is.
4. **Non-intersection: none.** Every criterion AC13 names has an executable case that exercises it
   *together with* the stream and exit-code assertion, in that one table-driven test. There is
   nothing to waive.

## Negative and boundary cases exercised

Triggered, not read about:

- `envel spend nosuch 5` — an envelope that does not exist.
- `envel spend car 12.50` against an envelope holding `10.00` — an overspend; **and**
  `envel spend car 10.00`, exactly what is left, which AC5's *"larger than"* permits and which
  lands the envelope on `0.00`.
- `envel spend groceries 0` and `envel spend groceries -5` — zero and negative.
- `--on` given `7/9`, `09-07`, `yesterday`, `2026-9-7`, `20260907`, `2026/09/07`, `07-09-2026` —
  seven unreadable forms, one of which (`20260907`) the underlying library would accept; and
  `2026-13-45` and `2026-02-30` — two that are the right shape and name days that do not exist.
- `--on` given tomorrow, today and yesterday, all three computed from the clock — the refusal and
  both sides of the boundary AC12 turns on.
- `envel spend`, `envel spend groceries`, `envel spend groceries 12.50 lunch extra` — too few
  words twice and too many once.
- A spend with no description; one with a one-word description; one with a date and no
  description; one with both.
- After every refusal, the listing or the store file was re-read to confirm nothing was recorded;
  after the AC14 sweep, the spend-entry count was 10 before and 10 after.

## Test sensitivity check

Ten behaviours were removed one at a time, the suite run, and the file restored from a copy taken
before each probe. **None of them left the suite green**, and `git status --porcelain envel tests
bin` is empty afterwards with the suite back at 90 green.

| behaviour removed | failing tests |
|---|---|
| the `on` field on the entry | 4 — including `test_the_entry_carries_the_day_the_money_was_spent`, `test_no_date_given_records_today_and_a_date_given_is_kept` |
| the future-date check | 3 — including `test_a_date_later_than_today_is_refused_and_today_is_not` |
| storing the spend negative | 8 — including `test_only_that_envelope_moves`, `test_recording_prints_what_is_left` |
| the insufficient-funds check | 3 — including `test_more_than_the_envelope_holds_is_refused_and_says_what_is_left` |
| `record_spend`'s zero/negative check | 6 — including `test_zero_and_negative_amounts_are_refused` |
| `record_spend`'s envelope-exists check | 3 — including `test_the_envelope_is_checked_before_the_amount_and_the_date` |
| writing the description | 3 — including `test_a_description_is_kept_when_given_and_absent_when_not` |
| the `YYYY-MM-DD` regex, leaving `fromisoformat` alone | 2 — `test_only_the_full_form_of_a_date_is_accepted`, `test_other_ways_of_writing_the_same_day_are_refused` |
| honouring `--on` at all | 11, across `tests/test_cli.py` |
| the description reaching `record_spend` | 2 — `test_a_description_is_optional_and_combines_with_a_date`, `test_a_description_of_several_words_is_kept_as_typed` |

**A method note worth keeping.** The last three probes were first run with a substitution that
appended a modified copy of the file to the original instead of replacing it. Python took the
**second** definition, which was the unmodified one, and all three reported the suite green — a
false *"this test is insensitive"* rather than a false pass, but the same class of error either
way. They were re-run with a single in-place replacement, asserted to match exactly once, and all
three then failed as above. A probe that does not actually remove the behaviour proves nothing,
and it does not announce itself; the first report on this item recorded the mirror-image trap,
where a whole-file substitution hit `add_income` instead of `record_spend`.

## Defects found

None. No criterion of this item failed, the repair the send-back asked for is present and correct,
and nothing in `WI-0001`'s delivered behaviour was found wrong — so no bug item was filed and no
send-back is warranted.

Three observations that are **not** defects:

- **The first verification of this item got one thing wrong, and it is worth naming.** It reopened
  the dependency-direction sentence, ran the import enumeration, printed `envel/envelopes.py:12`
  reading `from . import dates, money`, and wrote *"First half: … **True.**"* about a sentence
  claiming three modules. The enumeration was right; the question asked of it was the falsifier it
  had come looking for rather than the sentence's own subject. That is what `review-close` caught,
  and it is why this report states a `Falsifier:` and a per-member verdict for every quantified
  row rather than only a command and an exit code.
- **`add_income` and `record_spend` check their refusals in different orders.** `add_income` tests
  the amount before the envelope; `record_spend` tests the envelope first, which is what makes
  AC3's promise of a message naming the envelope hold when three criteria refuse at once. The
  plan names it, the implementation report declares it, `review.md` accepted it as a limitation
  with no owner, and no acceptance criterion of either item is violated. Not a defect, and not one
  this execution files.
- **One `WI-0001` test was adapted by this branch** — the assertion that the tool's usage line
  contains the literal `{new,add,list}`. `WI-0001` AC14 asks for *"a usage message that lists the
  subcommands the tool does have"*, and it now lists four. `git diff main..HEAD -- tracker/items/WI-0001/`
  is empty: no criterion of `WI-0001` was edited.

## Not verified, and why

- **That the `at` timestamp is UTC rather than local.** `ADR-0006` `## Consequences` says `at` is
  a UTC timestamp and `on` a local calendar day, and that the two are therefore not convertible
  into each other. This machine's local time and UTC coincide — every `at` this execution wrote
  reads `2026-09-11T04:42:0…Z` on the same day `date.today()` returns — so no observation here can
  distinguish them. No acceptance criterion of `WI-0002` names `at`, so nothing is ticked on the
  strength of it. `review.md` accepted this as a gap with no owner; it is recorded again because
  `WI-0003` will read both fields.
- **That a spend's `on` or `description` is shown to the user.** Nothing in this item prints
  either, by design, so what was verified is the store file's content
  [src: WI-0002 AC8 "The store file is where this item's dates are read"]. Whether the date is
  *right* in a month's report is `WI-0003`'s to verify, and the description becomes visible in
  `WI-0006`.
- **Behaviour when the store holds a spend against an envelope that no longer exists.** The plan
  records this as a deliberate non-decision, no criterion covers it, and no command in this tool
  can produce the state.
- **`--on` given twice, and an empty or whitespace-only description.** The plan settles both as
  assumptions and no criterion constrains either, so neither was ticked on and neither was
  exercised here. They belong to whoever revisits the assumptions.
- **Concurrency, large stores, and interrupted writes.** `ADR-0002`'s atomic-write claim is
  `WI-0001`'s and is out of this item's scope; this execution did not re-verify it.
- **Whether the repaired overview paragraph is the *best* description of the architecture**, as
  opposed to a true one. It is true, and every edge it asserts was opened at the line it cites.
  Whether the document should say more is `plan`'s judgement and not this stage's.

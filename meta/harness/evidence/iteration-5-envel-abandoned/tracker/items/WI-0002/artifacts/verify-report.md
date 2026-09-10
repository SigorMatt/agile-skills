# Verification report — WI-0002

Verified-commit: ae397c22ae785bbcca7982142f7b0bd49dba2843

Every command below was run by this execution against that commit, from the repository root,
with `PATH="$PWD/bin:$PATH"` and `ENVEL_FILE` pointed at a scratch store (`ADR-0002`'s own
demonstration form). Nothing in this report is taken from `impl-report.md`; the report was read
after the criteria, and it is checked here rather than quoted.

## Verdict

**All nineteen acceptance criteria pass, on evidence gathered here — and the item is not
finished.** Four `[src: <path>:<line>]` citations in three documents point at the wrong lines
because this item moved the code they cite. Three of the four are in documents that this skill
may not write and that `implement` may not write either (`spec/doc-header.md` §5): two ADRs, whose
repair is an append-only `## Corrections` entry, and `docs/process/ways-of-working.md`, whose
updaters are `review-close` and `answer-questions`. That is `Q-005`, blocking, addressed to the
architect, and the item is suspended at `awaiting-answer` with `resume-to: verifying`.

The behaviour is sound. What is unfinished is D7's closing question — *did this change falsify a
document the set does not name?* — and D12 for the three documents above.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | pass | `envel new groceries` then `envel income groceries 400`, then `envel list` | `income 400.00 into groceries on 2026-09-10 — 400.00 left` on stdout (exactly 1 line), stderr empty, exit 0; `envel list` → `groceries  400.00`, exit 0 | one line to stdout and nothing to stderr, both checked; the read-back carries `groceries` and `400.00` |
| AC2 | pass | `envel spend groceries 60` on that store, then `envel list` | `spend 60.00 from groceries on 2026-09-10 — 340.00 left`, stderr empty, exit 0; `envel list` → `groceries  340.00` | |
| AC3 | pass | four separate process invocations on a fresh store: `envel new groceries`; `envel income groceries 400`; `envel spend groceries 60`; `envel list` | third → exit 0; `envel list` → `groceries  340.00`, exit 0, stderr empty | each a separate `bin/envel` process, no step in between |
| AC4 | pass | on a store holding only `groceries` at 340: `envel income rent 100`; `envel spend rent 100`; `envel list`; then `envel spend Groceries 10` | both refusals exit 1 with one stderr line `envel: no envelope named 'rent'`; `envel list` → `groceries  340.00` and **no** line containing `rent`; `envel spend Groceries 10` → exit 0, stderr empty, `spend 10.00 from groceries on 2026-09-10 — 330.00 left`, and `envel list` → `groceries  330.00` | both halves: the refusal creates nothing, and the case-folded name reduces `groceries` rather than reporting it unknown |
| AC5 | pass | a fourth separate invocation of `envel list` after AC3's three | `groceries  340.00`, exit 0, stderr empty | the balance survived the process boundary with no manual step |
| AC6 | pass | with `groceries` at 340: `envel spend groceries 500`, then `envel list`, then a read of the store's `transactions` | exit 1, one stderr line `envel: groceries holds 340.00, which is less than 500.00`; `envel list` → `groceries  340.00`; `transactions` length unchanged at 4 | "records nothing" checked against the store file, not only against the listing |
| AC7 | pass | with `groceries` at 340: `envel spend groceries 10 --date 2026-08-31`; `envel spend groceries 10 --date 2026-13-01`; `envel spend groceries 10 --date 31/08/2026` | first → exit 0, stderr empty, and the stored movement is `{'envelope': 'groceries', 'kind': 'spend', 'amount': 1000, 'date': '2026-08-31'}`; the other two → exit 1, one stderr line each (`envel: '2026-13-01' is not a date; write it as YYYY-MM-DD`), and `transactions` length unchanged at 5 across both | the accepted date is checked in the store, not only on the screen |
| AC8 | pass | with `groceries` at 340: `envel spend groceries 340`, then `envel list` | exit 0, stderr empty, `spend 340.00 from groceries on 2026-09-10 — 0.00 left`; `envel list` → `groceries  0.00` | the boundary is recorded, not refused |
| AC9 | pass | `envel income groceries 0`; `envel spend groceries 0`; `envel income groceries -5`; `envel spend groceries -5` | each exit 1 with one stderr line (`envel: '0' is not an amount`, `envel: '-5' is not an amount`); `envel list` byte-identical before and after all four, and `transactions` length unchanged | `-5` reaches the amount parser rather than being read as an option |
| AC10 | pass | `envel spend groceries abc`; `envel spend groceries ""` | exit 1 each, one stderr line each: `envel: 'abc' is not an amount`, `envel: '' is not an amount`; listing and `transactions` unchanged | |
| AC11 | pass | `envel income groceries`; `envel spend` | exit 2 each, one stderr line each: `usage: envel income <envelope> <amount> [--date YYYY-MM-DD]`, `usage: envel spend <envelope> <amount> [--date YYYY-MM-DD]`; listing and `transactions` unchanged | non-zero, which is what the criterion asks; the 2-versus-1 split is the plan's |
| AC12 | pass (read) | see `## AC12 — WI-0001's eleven criteria, read one by one` below | per-criterion verdicts there | five held as written, six waived by name; the read is the assessment and the tests are its evidence |
| AC13 | pass | on a store with `groceries` at 400: `envel spend groceries 12.50 --date 2026-08-31` | exit 0, stderr empty, exactly one stdout line: `spend 12.50 from groceries on 2026-08-31 — 387.50 left`; all four substrings present, each checked individually (`groceries` yes, `12.50` yes, `2026-08-31` yes, `387.50` yes) | |
| AC14 | pass | `envel spend groceries 10` with no `--date`, alongside `date +%F` | `date +%F` → `2026-09-10`; stdout one line `spend 10.00 from groceries on 2026-09-10 — 377.50 left`, exit 0, stderr empty | the default really is today, printed back |
| AC15 | pass | on a store with `groceries` 340 and `rent` 0: `envel list` twice, output captured through `cat -A` and `cmp` | exit 0, stderr empty, exactly two lines: `groceries  340.00$` then `rent  0.00$`; `cmp` of the two runs → identical | order and byte-stability both checked, with the trailing newline visible |
| AC16 | pass | `envel new petrol` on a store without it, then `envel list` | `new` exit 0; `envel list` exit 0 → `groceries  340.00`, `petrol  0.00`, `rent  0.00` | a zero balance, not a blank and not an error |
| AC17 | pass | on a store with `groceries` at 0: `envel income groceries £12.50`, then `envel list`; then `envel income groceries 12`, `12.5`, `12.50` each on a fresh store | `£12.50` → exit 0, stderr empty, `income 12.50 into groceries…`; `envel list` → `groceries  12.50`. The three plain forms → exit 0 and empty stderr, printing `12.00`, `12.50`, `12.50` | run under the ordinary `en_US.UTF-8` locale, which is the locale the criterion is written against; see `## Not verified, and why` for the non-UTF-8 probe |
| AC18 | pass | with `groceries` at 340: `envel spend groceries 12.345`; `envel income groceries 12.345`; then `envel list` | exit 1 each, one stderr line each: `envel: '12.345' is not an amount: at most two decimal places`; `envel list` → `groceries  340.00`; `transactions` unchanged | refused, and refused *as over-precise*; nothing rounded |
| AC19 | pass | four scenarios, each on a store that starts empty — (1) `envel new Groceries`, `envel list`; (2) `envel new "eating out"`, `envel list`; (3) `envel new a`, `envel new b`, `envel list`; (4) `envel new groceries`, `envel new "  groceries  "`, `envel list` | (1) exactly one line `Groceries  0.00$`; (2) `eating out  0.00$`; (3) exactly two lines, `a  0.00$` then `b  0.00$`; (4) second `new` → exit 1 `envel: an envelope named 'groceries' already exists`, then exactly one line `groceries  0.00$`, no leading space | captured with `cat -A`, so "no leading space" and the line count are read rather than assumed |

## AC12 — WI-0001's eleven criteria, read one by one

AC12's subject is other criteria, so the assessment below is a **read** of each sentence against
this item's behaviour. The tests are the evidence for the read, never its definition.

**Not waived — each must still hold as written. Five of five hold.**

| WI-0001 AC | verdict | the read, and the evidence |
|------------|---------|----------------------------|
| AC1 | holds | *"`envel new groceries` exits 0 and writes nothing to stderr"*. Run on an empty store: exit 0, stdout empty, stderr empty. A second column on `envel list` does not touch `envel new`'s streams. Evidence: `test_ac1_new_exits_zero_and_writes_nothing_to_stderr` |
| AC4 | holds | *"`envel list` writes its envelope lines sorted by name, ascending, byte-wise; running it twice in a row produces byte-identical stdout"*. This is the one AC12 flags as most likely to break, so it was checked on a set built to distinguish byte-wise from case-insensitive order: created in the order `rent`, `Zebra`, `apple`, `Apple2`, `eating out`, printed as `Apple2`, `Zebra`, `apple`, `eating out`, `rent` — equal to `sorted(names)` computed independently in Python, and a `casefold` sort would have put `apple` before `Apple2` and `Zebra` last. `cmp` of two consecutive runs: identical. Evidence: `test_ac4_listing_is_sorted_byte_wise_and_repeatable`, `test_listing_is_byte_wise_ascending_not_alphabetical` |
| AC6 | holds | *"`envel list` run before any envelope has ever been created exits 0, writes at least one line to stdout, and writes nothing to stderr"*. On a path with no file: exit 0, stderr empty, one line — `No envelopes yet. Create one with: envel new <name>`. The balance column is not reached on the empty branch. Evidence: `test_ac6_list_before_anything_exists` |
| AC9 | holds | *"`envel new ""` exits non-zero … and a following `envel list` writes stdout byte-identical to the AC6 reference output"*. exit 1, one stderr line `envel: an envelope name cannot be empty`; the following `envel list` `cmp`s identical to the AC6 reference captured in the same scenario. Evidence: `test_ac9_an_empty_name_is_refused_and_leaves_the_store_untouched` |
| AC10 | holds | *"`envel new "   "` … byte-identical to the AC6 reference output"*. exit 1, one stderr line, and `cmp` against the same reference: identical. Evidence: `test_ac10_an_all_whitespace_name_is_refused_and_leaves_the_store_untouched` |

**Waived by name — six of eleven, each `waived — superseded by WI-0002/Q-001`.** Each of the six
says an `envel list` line's *only* content is the envelope's name; AC15 says it now carries the
balance too, and the stakeholder asked for that change explicitly. All six carry the
`**[superseded: WI-0002/Q-001 …]**` marker on `WI-0001/item.md` itself — checked there, not
assumed: AC2, AC3, AC5, AC7, AC8, AC11.

| WI-0001 AC | verdict | where its substance was re-checked |
|------------|---------|-----------------------------------|
| AC2 | waived — superseded by `WI-0002/Q-001` | AC15 (a line carries name **and** balance) |
| AC3 | waived — superseded by `WI-0002/Q-001` | AC19 case 3: `a  0.00` then `b  0.00`, exactly two lines, in order |
| AC5 | waived — superseded by `WI-0002/Q-001` | AC19 case 4: the case-differing duplicate is refused and one line is left |
| AC7 | waived — superseded by `WI-0002/Q-001` | AC19 case 1: `Groceries  0.00`, capitalisation intact |
| AC8 | waived — superseded by `WI-0002/Q-001` | AC19 case 2: `eating out  0.00` |
| AC11 | waived — superseded by `WI-0002/Q-001` | AC19 case 4: refused, one line, no leading space |

**Non-intersection — stated in the words the gate asks for.**

For the five **not waived**, non-intersection does **not** exist, and that is the good case: plan
step 8 rewrote the eight `WI-0001` cases in `tests/test_cli.py` that assert `envel list`'s exact
stdout, so those cases now assert the old criterion *and* the new balance column in one
assertion. `test_ac4_listing_is_sorted_byte_wise_and_repeatable` asserts
`"Zebra  0.00\napple  0.00\n"` — the byte-wise order and the second column together. Something
executable exercises each of the five old criteria against the new behaviour, and mutation M16
(`listing` returns creation order) failed it, so the collision would be caught.

For the six **waived**, non-intersection is intrinsic and unavoidable: nothing executable
exercises the old criterion and the new behaviour together, because the old sentence — a line
whose *only* content is the name — is the thing the stakeholder replaced, so no case can assert
both. No covering case is added, and the six are waived **by name** above. What replaces the
coverage is AC15 and AC19, which state the substance in the new line shape and are checked here
by command.

## ADR conformance

One row per ID in the plan's `## Binding ADRs` list, all seven, plus any ADR found engaged that
the list does not name.

| ADR | verdict | clause quoted from its `## Decision` | file and line, or why not engaged |
|-----|---------|--------------------------------------|-----------------------------------|
| ADR-0001 | conforms | *"This project is written against the Python 3 standard library and declares no third-party dependency, for its runtime, its tests or its checks."* | Every import across `envel/`, `tests/` and `bin/envel`, enumerated with `grep -rhn "^import \|^from " …`: `__future__`, `datetime`, `json`, `os`, `re`, `subprocess`, `sys`, `tempfile`, `unittest`, plus intra-project `envel.*`. The new module's are `envel/movements.py:10` (`import datetime`), `:11` (`import re`), `:13` (`from envel import envelopes`). No `requirements*.txt`, `pyproject.toml`, `setup.py`, `setup.cfg` or `Pipfile` exists |
| ADR-0002 | conforms | *"The repository contains an executable file `bin/envel` … imports `envel.cli`, and exits with what `main()` returns — four statements, with the tool's behaviour living behind that import."* | `git diff --stat main..HEAD -- bin/` is empty: `bin/envel` is untouched, and it is still the four statements. The two new commands are reached inside `main` at `envel/cli.py:52` (`if command in _RECORDING: return _record(rest, command)`), not through a second entry point |
| ADR-0003 | conforms | *"The store is one JSON document"* … *"replaces the file atomically: write a temporary file in the same directory, then `os.replace`."* | Still one document at one path: `store_path` (`envel/store.py:28`) is unchanged by this branch, and `def save` (`envel/store.py:79`) is not in the diff at all — `git diff main..HEAD -- envel/store.py` touches neither. `version` is used for exactly the purpose the ADR gave it: `envel/store.py:14` (`VERSION = 2`) and `_upgrade` at `envel/store.py:65` |
| ADR-0004 | conforms | *"Two names are the same envelope exactly when their identities are equal … the message names the **stored** envelope rather than what was typed"* | `envel/cli.py:161` (`entry = envelopes.find(data, name)`) then `envel/movements.py:125`, which writes `entry["name"]` — the stored display form — into the movement; observed: `envel spend Groceries 10` stored `{"envelope": "groceries", …}` and reduced `groceries`, and the overspend message at `envel/cli.py:167` names `entry['name']`. Rule 3 (*"Nothing downstream folds a name a second time"*) is the clause this change stretches: `movements.balances` (`envel/movements.py:97`) computes `identity` on **stored** names to key its totals. It does not fold the person's input twice, which is what rule 3 guards, and `ADR-0007` §2 — written by this item's own architect and citing `ADR-0004` — states that matching a movement to an envelope by identity *"is `ADR-0004`'s rule and not a second one"*. Recorded rather than smoothed over |
| ADR-0005 | conforms | *"This is a boundary rule, not a domain rule. The recovery and the display handler belong to the module that owns `argv` and the streams. Nothing in the domain rules or the store learns about locales"* | `envel/movements.py` takes `str` and contains no locale, encoding or stream handling — `parse_amount` at `envel/movements.py:50` takes `text: str`. Clauses 1–4 are `BUG-0001`'s to implement and are **not** engaged by this item: they are unimplemented on this branch, which is `BUG-0001` at `planned` and not a regression here. Probed rather than assumed — see `## Not verified, and why`. **This ADR also carries one of the four falsified citations**, in `## Context` rather than in `## Decision`; see `## Defects found` |
| ADR-0006 | conforms | *"On **output**, every amount and every balance the tool prints is written with exactly two decimal places."* — and rule 2, *"a single leading `£` is accepted and ignored … an amount with more than two decimal places is refused rather than rounded"* | Rule 2 is `parse_amount`: `envel/movements.py:57` strips one leading `£`, `:59` sets the over-precise reason. Rule 3 is `format_amount`, `envel/movements.py:74`. Rule 3 is **quantified**, so it is enumerated below rather than cited |
| ADR-0007 | conforms | *"`amount` is a **positive integer number of pence**"*, *"Appending is the only write WI-0002 makes to it"*, and *"An envelope's **balance** is the sum of its `income` amounts minus the sum of its `spend` amounts"* | The store after four movements read back as `{"version": 2, …, "transactions": [{"envelope": "groceries", "kind": "income", "amount": 40000, "date": "2026-09-10"}, …]}` — integer pence, stored display name, `income`/`spend` kinds, `YYYY-MM-DD` date. `envel/movements.py:127` is the only write and it is an append. The balance arithmetic is `envel/movements.py:97`–`:112`, and 400 − 60 → `340.00` was observed end to end. **This ADR also carries one of the four falsified citations**; see `## Defects found` |

**No ADR was found engaged that the plan's list does not name.** The list is seven of the seven
ADRs in `docs/architecture/adr/`, so there is nothing outside it to engage.

### ADR-0006 rule 3's enumeration

Rule 3 is an absolute over a family — *every* amount and *every* balance the tool prints — so it
owes members, not a citation.

- **Set:** every site in `envel/` that prints a money figure.
- **Enumerated by:** `grep -n "print(" envel/*.py` → 21 print sites, of which exactly three
  interpolate a pence value (`grep … | grep -E "format_amount|pence|held|totals|left"`). The
  other 18 print usage lines, `EMPTY_LINE`, or a refusal carrying a name, a date or a store
  error — no money.
- **Members:** `envel/cli.py:100` (the `envel list` line, one figure); `envel/cli.py:167` (the
  overspend refusal, **two** figures — what is held and what was asked for); `envel/cli.py:177`
  (the success line, **two** figures — the amount and what is left). Five printed figures at
  three sites.
- **Verdict:** all five pass through `movements.format_amount` (`envel/movements.py:74`,
  `f"{pence // 100}.{pence % 100:02d}"`), so all five carry exactly two decimal places. Observed
  at every site: `pot  0.05`, `envel: pot holds 0.05, which is less than 0.06`,
  `income 0.05 into pot on 2026-09-10 — 0.05 left`.
- **Falsifier:** a printed figure with fewer than two decimal places — `7` or `7.0` where `7.00`
  is owed. Two ways it could have appeared, and both were tried. (i) A print site not routed
  through `format_amount`: the `grep` above *is* the enumeration, and it is what would have shown
  one. (ii) `format_amount` itself emitting one place: mutation M5 changed it to
  `{pence % 100 // 10:01d}` and **26 tests failed**, including one per site
  (`test_ac15_…`, `test_ac6_a_spend_larger_than_the_balance_is_refused`, `test_ac13_…`), so the
  check could have failed and did not.
- **At the boundary, not at the happy path.** Rule 3's boundary is a figure with no pounds or no
  pence, where a naive formatter drops a digit. All three sites were run at `0.05` (no pounds),
  at `0.00` (nothing at all), at `7.00` (whole pounds, zero pence) and at `1000007.00`. Every
  one carried two places.

## Invalidation set

One row per entry in the plan's set, as re-disposed after `Q-004`. **This execution wrote no
document** — the three unrepaired entries are `Q-005`, not an edit.

| document | disposition | what I reopened, and what I found |
|----------|-------------|-----------------------------------|
| `docs/architecture/overview.md` — `## The shape`, the `envel/cli.py` row | to-update | Updated. The row now reads *"dispatches to `new`, `list`, `income` or `spend`"* and cites `envel/cli.py:42`, which resolves to `def main(argv=None) -> int:`. Version 2 → 3 with a change-log row at `2026-09-10T15:28:26Z`. **Repaired correctly** |
| `docs/architecture/overview.md` — `## The shape`, the whole table | to-update | Updated: a fifth row for `envel/movements.py` exists, citing `envel/movements.py:50`, `:68`, `:77`, `:97` — all four resolve to `def parse_amount`, `def format_amount`, `def parse_date`, `def balances`. **Repaired correctly** |
| `docs/architecture/overview.md` — `## The shape`, the one-way dependency sentence | to-update | Updated: it enumerates four modules and cites `envel/cli.py:14` (`from envel import envelopes, movements, store`) and `envel/movements.py:13` (`from envel import envelopes`). Both resolve. The direction it asserts is true of the code: `envel/movements.py` imports `envel.envelopes` and not `envel.store`. **Repaired correctly** |
| `docs/architecture/overview.md` — the `envel/store.py` row's line citations | to-update | Updated to `envel/store.py:28`, `:40`, `:79`, which resolve to `def store_path`, `def load`, `def save`. **Repaired correctly** — and this is the row that shows the omission below was an oversight rather than a policy: `implement` did exactly this repair here and not in the three other documents whose citations the same edit moved |
| `docs/architecture/overview.md` — `## State`, first sentence | to-update | Updated: it says the document holds the movements at version 2, citing `envel/store.py:25` (`return {"version": VERSION, "envelopes": [], "transactions": []}`) and `envel/store.py:65` (`def _upgrade`). Both resolve. Read against the branch head and true |
| `docs/architecture/overview.md` — `## Conventions`, the test citation | to-update | Updated to `run: python3 -m unittest discover -s tests -t . → exit 0, 69 tests, OK`. Re-run here: exit 0, `Ran 69 tests`, `OK`. **True as written** |
| `docs/architecture/overview.md` — `## Conventions`, the end-to-end citation | to-update | Updated to `tests/test_cli.py:35`, which resolves to `return subprocess.run(["envel", *arguments], env=environment,`. **Repaired correctly** |
| `docs/product/vision.md` — `## Engagement state` | owned-by-ending | **Left exactly as it is, correctly.** `git diff --stat main..HEAD -- docs/product/vision.md` is empty: this item did not touch the document at all, so nothing in the section was edited by it. `lint-claims`' one remaining error is `docs/product/vision.md:85`, inside that section, and it is the ending's — `spec/dor-dod.md` D12 puts it outside every item audit |
| `docs/architecture/adr/ADR-0003-one-json-store-and-where-it-lives.md` — the `{"version": 1, …}` block and *"Its shape at this version"* | verified-still-true → **reopened** | **Reopened and read against the branch head, and it holds — but only because of its scoping, which is worth saying plainly.** A store this build *creates* no longer looks like the block: `store.empty()` returns `{"version": 2, "envelopes": [], "transactions": []}`. The sentence survives because it is scoped *"at this version"*, and a version 1 document on disk is still exactly the block. Checked by writing `{"version": 1, "envelopes": [{"name": "groceries"}, {"name": "rent"}]}` by hand and running `envel list`: exit 0, `groceries  0.00` / `rent  0.00`, and `cmp` of the file before and after → **identical**, so the read did not rewrite it. The ADR's other clause — *"The order the list is stored in is not the order `envel list` prints"* — is also still true: stored `rent, Zebra, apple, Apple2, eating out`, printed `Apple2, Zebra, apple, eating out, rent`. **Not falsified** |
| `docs/architecture/adr/ADR-0006-money-is-pounds-and-pence.md` — rule 3 | to-update (re-disposed for `Q-004`) | The row's subject, rule 3, is **not falsified**: enumerated in full under `## ADR conformance` above, five members, all passing, checked at the boundary. The document was written on this branch by `answer-questions` for `Q-004`: version 1 → 2, an append-only `## Corrections` entry of kind `provenance` adding `[src: envel/movements.py:68]` to option B. That citation resolves — `envel/movements.py:68` is `def format_amount(pence: int) -> str:`. Change-log row present and dated `2026-09-10T15:34:21Z`. **Repaired correctly** |
| `docs/process/ways-of-working.md` — the whole document | to-update (re-disposed for `Q-004`) | **The `Q-004` repair is correct and the row's original claim is not.** The `Q-004` half checks out: version 2 → 3, change-log row at `2026-09-10T15:34:21Z`, and the two citations it added — `[src: .claude/agile-skills/spec/dor-dod.md]` and `[src: .claude/agile-skills/pipeline.yaml]` — resolve. But the row's `verified-still-true` sentence, *"neither mentions the tool's behaviour, its store or its commands"*, is **false**: `## Where an accepted test-coverage gap goes` names `envel/store.py` twice by line, at lines 105 and 106, and this item moved both lines. See `## Defects found` — this is exactly the claim the `verified-still-true` reopening exists to catch, and it survived a re-disposition because the re-disposition was about a different sentence |

## Gates

| gate | verdict | evidence |
|------|---------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → exit 0, `Ran 69 tests in 4.574s`, `OK`. Re-run at the end of the mutation work: exit 0, `Ran 69 tests`, `OK`, and `git status --short` clean, so the suite that passed is the branch head and not a mutant |
| `lint-clean` | **pass** | `python3 -m compileall -q envel tests` → exit 0 |
| `workspace-valid` | **pass** | `python3 .claude/agile-skills/scripts/validate-workspace .` → `checked 7 item(s), 10 document(s)`, `0 errors, 0 warnings` |
| `every-criterion-independently-checked` | **pass** | Nineteen rows in `## Criteria`, each with the command this execution ran and its quoted output. `impl-report.md` is cited nowhere as evidence; it was read after the criteria and is checked in `## Defects found` |
| `negative-cases-exercised` | **pass** | Every refusal was *triggered*: unknown envelope (AC4), overspend (AC6), two malformed dates (AC7), zero and negative on both commands (AC9), non-numeric and empty (AC10), missing arguments on both (AC11), over-precision on both (AC18), the duplicate name (AC19), the empty and whitespace-only names (`WI-0001` AC9/AC10), and the empty store (`WI-0001` AC6). Boundaries: a spend of exactly the balance (AC8), a zero balance (AC16), sub-pound and whole-pound figures at all three print sites, a version 1 store, and a store from a newer build |
| `a-criterion-about-criteria-is-read` | **pass** | `## AC12 — WI-0001's eleven criteria, read one by one`: eleven named by ID, a per-criterion verdict read from each sentence, the six waivers named individually and checked against the `superseded` markers on `WI-0001/item.md`, and non-intersection stated in the gate's own words for both groups |
| `adr-conformance-is-decided` | **pass** | `python3 .claude/agile-skills/scripts/lint-documents --rule adr-conformance-is-decided --item WI-0002` → 0 errors. Seven rows in `## ADR conformance`, one per binding ADR, each quoting a clause of that ADR's `## Decision` |
| `invalidation-set-is-disposed` | **pass** | `python3 .claude/agile-skills/scripts/lint-documents --rule invalidation-set-is-disposed --item WI-0002` → 0 errors. Eleven rows in `## Invalidation set`; the one `verified-still-true` entry was reopened and read against the branch head |
| `tests-would-fail-without-the-change` (advisory) | **pass** | Seventeen mutations, below |

### Test sensitivity check

Each mutation was applied to the branch head, the whole suite run, and the tree restored with
`git checkout -- envel/`. `git status --short` is clean afterwards and the suite is green again.

| # | mutation | criteria it covers | failing tests |
|---|----------|--------------------|---------------|
| M1 | `parse_amount` stops stripping a leading `£` | AC17 | 3, incl. `test_ac17_a_single_leading_currency_symbol_is_accepted_and_ignored` |
| M2 | `parse_amount` drops the `pence == 0` check | AC9 | 2, incl. `test_ac9_zero_and_negative_amounts_are_refused_on_both_commands` |
| M3 | `_AMOUNT` allows any number of decimals | AC18 | 2, incl. `test_ac18_more_than_two_decimal_places_is_refused_not_rounded` |
| M4 | `_AMOUNT` matches anything (`^.*$`) | AC10 | 6 — but **not** `test_ac10_…`, because `int(whole)` then raises and the CLI still exits non-zero with output on stderr. A mutation artefact, not a coverage gap; M4b is the clean form |
| M4b | `parse_amount` silently returns `100` for a non-amount | AC10 | 7, incl. `test_ac10_what_is_not_an_amount_is_refused` |
| M5 | `format_amount` writes one decimal place | AC1, AC2, AC3, AC5, AC8, AC13, AC15, AC16, AC17, AC18, ADR-0006 r3 | **26** |
| M6 | `parse_date` drops the pattern check, keeps the calendar | AC7 | 1 — `test_another_notation_is_refused_even_when_the_day_is_real`. AC7's own two malformed dates are still caught by `date.fromisoformat`, so its CLI test does not move. The layering is deliberate and M6b is the mutation that reaches AC7 |
| M6b | `parse_date` drops the calendar check, keeps the pattern | AC7 | 2, incl. `test_ac7_a_malformed_date_is_refused_and_records_nothing` |
| M7 | `_record` ignores `--date` and always stamps today | AC7, AC13 | 2, incl. `test_ac13_a_successful_recording_says_what_it_recorded` |
| M8 | `today()` returns a fixed past date | AC14 | 2, incl. `test_ac14_with_no_date_the_printed_date_is_todays` |
| M9 | `_record` never refuses an overspend | AC6 | 1 — `test_ac6_a_spend_larger_than_the_balance_is_refused` |
| M10 | `_record` refuses a spend of exactly the balance too | AC8 | 1 — `test_ac8_a_spend_of_exactly_the_balance_is_recorded`. The boundary is pinned from both sides |
| M11 | `_list` prints the name only, no balance | AC15, AC16, AC19 | **23** |
| M12 | `_record` never finds an envelope | AC1, AC2 | 17 |
| M13 | `_record` accepts a missing amount | AC11 | 1 — `test_ac11_a_missing_argument_is_refused` |
| M14 | `find` returns the first envelope whatever was asked for | AC4 (unknown envelope) | 6, incl. `test_ac4_an_unknown_envelope_is_refused_and_nothing_is_created` |
| M15 | `find` compares names exactly as typed | AC4 (case/whitespace identity) | 7, incl. `test_ac4_an_envelope_is_found_ignoring_case` |
| M16 | `listing` returns creation order, not byte-wise sorted | AC12 / `WI-0001` AC4, AC15 | 2, incl. `test_ac4_listing_is_sorted_byte_wise_and_repeatable` |
| M17 | `record` does not append the movement | AC1, AC2, AC3, AC5 | 14 |

No test survived the removal of the behaviour it claims to test. Every one of the nineteen
criteria is covered by at least one mutation that failed at least one test naming it.

## Negative and boundary cases exercised

Beyond the criteria's own refusals, listed under `negative-cases-exercised` above:

- **A version 1 store, written by `WI-0001`.** Hand-written `{"version": 1, "envelopes": […]}`;
  `envel list` → exit 0 and zero balances; `cmp` before/after → identical, so a read does not
  rewrite the file; then `envel income groceries 50` → exit 0, and the file's `version` is 2
  afterwards. Plan step 3's by-hand check, run.
- **A store from a newer build.** `{"version": 99, …}` → exit 1,
  `envel: … was written by a newer envel (store format 99, this one reads 2)`. No guess.
- **Money at the edges, at all three print sites**: `0.05`, `0.00`, `7.00`, `1000007.00`.
- **A non-UTF-8 locale**, on two paths — see `## Not verified, and why`.

## Defects found

**One defect, four instances, and it is not in the behaviour.**

`[src: <path>:<line>]` citations in this project are exact: the plan's own invalidation set has a
row reading *"the `envel/store.py` row's line citations … step 3 changes `envel/store.py` **above
those lines**"*, and `implement` repaired `docs/architecture/overview.md` accordingly, moving its
citations to `:28`, `:40`, `:79`. Three other documents cite the same two files by line and were
not repaired. All four citations still resolve *mechanically* — the line number is within the
file — which is why nothing caught them; `spec/doc-header.md` §4a records that exact weakness as
F-077's disease, *"a `path:line` citation resolved for ever because the resolver asked whether the
file existed"*.

Every one was correct at `main` (`ce87246`) and was falsified by this item's own edits to
`envel/store.py` and `envel/cli.py`:

| # | document and line | citation | pointed at, at `main` | points at now | should be |
|---|-------------------|----------|----------------------|---------------|-----------|
| 1 | `docs/architecture/adr/ADR-0005-…md:52` | `envel/cli.py:82` | `print(name)` — the `envel list` print the sentence is about | `    return OK` | `envel/cli.py:100`. The claim itself is **still true**: re-run here, `envel list` against a store holding `café` under `LC_ALL=C` raises `UnicodeEncodeError` at that print, and the traceback names `envel/cli.py, line 100, in _list` |
| 2 | `docs/architecture/adr/ADR-0007-…md:117` | `envel/store.py:58` | `def save(path: str, store: dict) -> None:` — the referent of *"until the next `save`"* | `raise StoreError(f"{path} could not be read: …)`, inside `load` | `envel/store.py:79` |
| 3 | `docs/process/ways-of-working.md:105` | `envel/store.py:58` | `def save(…)` — *"the module that holds both the defect it fixes"* | the same unrelated `raise` inside `load` | `envel/store.py:79` |
| 4 | `docs/process/ways-of-working.md:106` | `envel/store.py:27` | `def store_path(environ=None) -> str:` — *"the untested path resolution"* | a **blank line** | `envel/store.py:28` |

Both files are in D7's scope — *what this change touched or its plan named*. `ADR-0005` and
`ADR-0007` are named in the plan's `binding-adrs`; `ways-of-working.md` is named in the
invalidation set. Two consequences follow, and they are the finding:

1. **D7's closing question is answered wrongly.** *Did this change falsify a document the set does
   not name?* `ADR-0005` and `ADR-0007` are not in the invalidation set, and the change falsified
   a citation in each.
2. **A `verified-still-true` claim is false.** The `ways-of-working.md` row says *"neither
   mentions the tool's behaviour, its store or its commands"*. It mentions `envel/store.py`
   twice, by line, in the section the row names.

**Why this is a question and not a send-back.** `spec/doc-header.md` §5 does not permit
`implement` to make any of these three repairs: an ADR's document half takes only an append-only
`## Corrections` entry, and `ways-of-working.md`'s updaters are `review-close` and
`answer-questions`. Sending the item to `in-progress` would hand `implement` a repair it is
forbidden to make. `verify` may not make it either — *"`verify` writes no document, ever"* — so
this is `Q-005`, blocking, addressed to the architect, and `answer-questions` makes the edits.
This is the same routing `Q-004` took on this item, for the same class of finding, across two of
the same three documents.

**Not defects, recorded because a reader would want them.**

- **No new bug item is filed.** No behaviour delivered by another item is broken. `BUG-0001` is
  already `found-in: WI-0001`, at `planned`, and is the item that owns the non-UTF-8 locale
  paths.
- **One undeclared shape difference from the plan, immaterial.** Plan step 5 says *"Add `_income`
  and `_spend` to `envel/cli.py`, sharing one private `_record(rest, kind)`"*. The code has
  `_record` and a module-level `_RECORDING` table (`envel/cli.py:29`) instead of two thin
  wrappers; `main` dispatches through the table at `:52`. Behaviour is identical and the plan's
  own words name `_record(rest, kind)` as the shared body. Not in `## Deviations from the plan`,
  where the other five are declared well.
- **`impl-report.md`'s gate table is accurate where it is checkable.** Its `claims-are-sourced`
  row claims 1 error remaining; re-run here,
  `lint-claims --changed-since main --plan-documents WI-0002` → exactly 1 error,
  `docs/product/vision.md:85`. Its `no-unplanned-scope` row lists five code files; the diff shows
  the same five. The one claim that does not hold is the `ways-of-working.md` invalidation row
  above.

## Not verified, and why

- **AC17 under a non-UTF-8 locale.** AC17 says nothing about the locale and was checked under the
  ordinary `en_US.UTF-8`, which is what the criterion is written against and what `WI-0002`'s
  `## Notes` says makes it checkable as written. Probed anyway, because `item.md` flags the
  collision with `BUG-0001`: under `LC_ALL=C`, `envel income groceries £12.50` **refuses
  cleanly** — exit 1, one stderr line `envel: '\udcc2\udca312.50' is not an amount`, no
  traceback. That is the shape `ADR-0005` clause 2 asks of a refusal, so this item added no new
  traceback path; what it does not do is *accept* the `£`, and making it accept one is
  `ADR-0005` clause 1's argv recovery, which is `BUG-0001`'s. Left to `BUG-0001`, whose fix
  installs the boundary at the top of `main` and therefore covers the amount as well as the name.
- **`ADR-0005` clauses 1–4 are unimplemented on this branch**, so their conformance could not be
  decided as *satisfied* — recorded `not-engaged` in substance and confirmed live: `envel new
  'café'` under `LC_ALL=C` still raises `UnicodeEncodeError` out of the store write. That is
  `BUG-0001` at `planned`, filed and owned, not a regression from this item.
- **Unicode normalisation of envelope names.** `ADR-0004`'s `## Consequences` deliberately leaves
  it undecided and no criterion covers it. Not checked, and not this item's.
- **Concurrent invocations.** Nothing in the criteria or the ADRs says what two `envel` processes
  writing at once should do. `ADR-0003`'s atomic replace makes a torn file unlikely and a lost
  update likely; unverified and unspecified.
- **A future `--date`.** `item.md` records it as deliberately unconstrained by `refine`, so there
  is nothing to verify against. Run anyway, so the record says what the tool does rather than
  what it was not asked: `envel spend pot 5 --date 2027-01-01` → exit 0,
  `spend 5.00 from pot on 2027-01-01 — 95.00 left`. Accepted, as AC7 allows. Not a defect; if the
  stakeholder wants it refused, `item.md` says that is a send-back to `refine`.

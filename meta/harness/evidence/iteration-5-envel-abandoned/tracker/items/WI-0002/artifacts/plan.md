# Plan — WI-0002 Record income into an envelope and spending against it, and show what is left

## Problem

`envel` today knows the names of a person's envelopes and nothing about their money: `envel new`
creates one and `envel list` prints one line per envelope carrying the name and nothing else. This
item adds the money. Two new commands record it — `envel income <envelope> <amount>` and
`envel spend <envelope> <amount>`, each taking an optional `--date YYYY-MM-DD` — each printing back
what it recorded on one line; and `envel list` gains a second column so that what is left in every
envelope is the first thing the person sees, which is what they asked for in `WI-0002/Q-001`.

The constraints are all recorded. An amount is pounds and pence, a leading `£` is accepted and
ignored, more than two decimal places is refused rather than rounded, and every printed figure
carries exactly two decimal places (`ADR-0006`). A spend larger than its envelope is refused and no
balance goes below zero (`EP-001/Q-003`). Two names are the same envelope when they differ only in
case or surrounding whitespace (`ADR-0004`). Standard library only (`ADR-0001`). One JSON store at
an overridable path, replaced atomically (`ADR-0003`). And the five of WI-0001's criteria that are
not superseded must still hold exactly as written, byte-identical output included.

## Approach

Four pieces change and one is new.

- **`envel/movements.py` (new)** holds the money half of the domain: what an amount is, what a
  date is, appending a movement to a store, and computing a balance from the movements. Like
  `envel/envelopes.py` it touches no filesystem, so every rule in it is testable without a store.
  It imports `envel.envelopes` for `identity`, and imports `envel.store` not at all — the one-way
  dependency direction the overview records is unchanged, with `movements` sitting beside
  `envelopes` rather than above it.
- **`envel/store.py`** moves to format version 2: `empty()` gains a `transactions` list,
  `_check_shape` checks it, and `load` upgrades a version 1 document in memory and refuses a
  version it does not know. `ADR-0007` fixes the shape.
- **`envel/cli.py`** gains `income` and `spend`, and `list` grows a column. The two new commands
  need one option, `--date`, and it is extracted by hand rather than by `argparse` — see
  assumption P2, which is about leaving WI-0001's delivered messages untouched.
- **`envel/envelopes.py`** does not change. `listing` keeps returning display names in the order
  it already fixes, and the balance for each is looked up separately, so `ADR-0004`'s rules and
  WI-0001's unit tests are untouched by this item.
- **`tests/`** gains `tests/test_movements.py` and cases in `tests/test_cli.py`. Eight existing
  cases in `tests/test_cli.py` assert `envel list`'s exact stdout and are rewritten to the new line
  shape — see step 8, which is the step to read carefully, because it edits tests WI-0001 wrote.

**The order in which a recording command refuses.** The item routed this here and no criterion
constrains it. A command checks, in order: (1) its arity and its options; (2) the amount; (3) the
date; (4) that the envelope exists; (5) for `spend`, that the balance covers it. So `envel spend
nosuch -5` refuses on the amount. The reason for this order rather than another is that steps 1
to 3 look only at what was typed, so a malformed command never reads the store at all, and a
person who has mistyped gets told about the thing they can see on their own screen.

**Exit statuses** follow the split `envel/cli.py` already uses: `MISUSE` (2) for a wrong number of
arguments or an unknown option, `REFUSED` (1) for an amount, a date, an envelope or a balance the
tool will not accept, `OK` (0) otherwise.

## Steps

1. **Add `envel/movements.py`** with the amount and date rules and nothing else. Module-level
   exceptions `InvalidAmount(ValueError)` and `InvalidDate(ValueError)`, and:
   - `parse_amount(text: str) -> int` — returns a positive whole number of pence. It strips one
     leading `£` if present and then requires the remainder to match `^\d+(\.\d{1,2})?$`; anything
     else raises `InvalidAmount(text)`. A value of zero raises `InvalidAmount(text)` as well, so
     the caller has one exception to handle. Use a regular expression and integer arithmetic on
     the digit groups — do **not** go via `float`, which is the whole point of `ADR-0007` decision
     F. `"12"` → 1200, `"12.5"` → 1250, `"12.50"` → 1250, `"£12.50"` → 1250; `"abc"`, `""`,
     `"12.345"`, `"0"`, `"-5"`, `"1 2"` and `"££1"` each raise.
   - `format_amount(pence: int) -> str` — `f"{pence // 100}.{pence % 100:02d}"`, which is
     `ADR-0006` rule 3. 1250 → `"12.50"`, 0 → `"0.00"`, 40000 → `"400.00"`.
   - `parse_date(text: str) -> str` — requires `^\d{4}-\d{2}-\d{2}$` **and then** that
     `datetime.date.fromisoformat(text)` succeeds, returning `text` unchanged. The regex is not
     redundant: `date.fromisoformat` on Python 3.11 and later also accepts `20260831` and a full
     timestamp, and AC7 says the date is given as `YYYY-MM-DD`. `"2026-13-01"` and `"31/08/2026"`
     each raise `InvalidDate(text)`.
   - `today() -> str` — `datetime.date.today().isoformat()`. Local, not UTC: AC14 compares it
     against `date +%F`.

   Afterwards `python3 -c "from envel import movements; print(movements.parse_amount('£12.50'))"`
   prints `1250`.

2. **Add the movement rules to `envel/movements.py`**, still with no filesystem in sight:
   - `balances(store: dict) -> dict` — a mapping from `envelopes.identity(name)` to a balance in
     pence, built by walking `store["transactions"]` once: `income` adds, `spend` subtracts. Every
     envelope in `store["envelopes"]` appears in the mapping, at 0 if it has no movements, which
     is AC16.
   - `balance(store: dict, name: str) -> int` — `balances(store).get(identity(name), 0)`.
   - `record(store: dict, entry: dict, kind: str, pence: int, date: str) -> dict` — appends
     `{"envelope": entry["name"], "kind": kind, "amount": pence, "date": date}` to
     `store["transactions"]` and returns it. `entry` is the stored envelope object that
     `envelopes.find` returned, so the recorded name is the stored display form and never what was
     typed — the same rule `envelopes.DuplicateName` already follows. It raises nothing: the
     caller has checked everything by the time it is called.

   Afterwards a store dict built by hand and passed through `record` twice yields the balance the
   arithmetic says, with no file involved.

3. **Move `envel/store.py` to format version 2.** `VERSION = 2`; `empty()` returns
   `{"version": VERSION, "envelopes": [], "transactions": []}`; `_check_shape` additionally
   requires `transactions` to be a list whose entries are objects with a string `envelope`, a
   string `kind`, an integer `amount` and a string `date`, raising `StoreError` with a message
   naming the path as its siblings do. In `load`, after `_check_shape`: a document whose `version`
   is 1 gains `transactions: []` and has its `version` set to 2 in the returned dict; a document
   whose `version` is greater than `VERSION` raises `StoreError` saying the store was written by a
   newer `envel`. Nothing here writes to the file (`ADR-0007`).

   `_check_shape` runs before the upgrade, so it must tolerate a version 1 document that has no
   `transactions` key at all — check the key only when it is present, and let the upgrade supply
   it. Afterwards `envel list` against a store file written by WI-0001 exits 0 and prints the
   envelopes it holds, each at `0.00`.

4. **Add the option extractor to `envel/cli.py`.** A module-level
   `_take_date(rest) -> tuple[list, str | None]` that scans a copy of `rest` for the exact token
   `--date`, removes it and the token after it, and returns the remaining operands and the value —
   raising `MISUSE`-shaped handling in its caller when `--date` is last with nothing after it, or
   appears twice, or when any remaining token begins with `--`. A token that begins with a single
   `-` is left alone, because `-5` is an operand AC9 requires to reach the amount parser. `new` and
   `list` do not call it and their code paths are untouched.

5. **Add `_income` and `_spend` to `envel/cli.py`**, sharing one private `_record(rest, kind)`
   because the two differ only in the balance check and the word in the message. In order:
   extract the option; require exactly two operands, else print
   `usage: envel income <envelope> <amount> [--date YYYY-MM-DD]` (or `spend`) to stderr and return
   `MISUSE`; parse the amount, else print `envel: <text!r> is not an amount` — or, when the text
   matched a number with too many decimal places, `envel: <text!r> is not an amount: at most two
   decimal places` — and return `REFUSED`; parse the date if one was given, else `movements.today()`;
   load the store; `envelopes.find` it, and on `None` print `envel: no envelope named <text!r>` and
   return `REFUSED`; for `spend` only, compare against `movements.balance` and on a shortfall print
   `envel: <name> holds <balance>, which is less than <amount>` and return `REFUSED`; then
   `movements.record`, `store.save`, and print the one line

   ```
   f"{kind} {format_amount(pence)} {preposition} {entry['name']} on {date} — {format_amount(new_balance)} left"
   ```

   where the preposition is `into` for income and `from` for spend. For AC13's invocation that line
   is `spend 12.50 from groceries on 2026-08-31 — 387.50 left`, which contains `groceries`,
   `12.50`, `2026-08-31` and `387.50`. Register both commands in `main` and extend `USAGE` to name
   all four. Afterwards AC1, AC2, AC4, AC6, AC7, AC8, AC9, AC10, AC11, AC13, AC14, AC17 and AC18
   are all observable at a terminal.

6. **Give `envel list` its second column.** In `_list`, after `envelopes.listing(data)`, build the
   balances once with `movements.balances(data)` and print, for each name,
   `f"{name}  {movements.format_amount(balances.get(envelopes.identity(name), 0))}"` — two spaces,
   no padding and no alignment, so the line has no leading space and two runs are byte-identical.
   The empty-store branch is untouched: `EMPTY_LINE` still prints when there are no envelopes,
   which is WI-0001 AC6 and the reference output AC9 and AC10 compare against. Afterwards AC3, AC5,
   AC15, AC16 and AC19 are observable.

7. **Write `tests/test_movements.py`** — unit cases for step 1 and step 2, with no subprocess and
   no file: the accepted and rejected amount forms named in step 1 one at a time, the three
   `format_amount` cases, the accepted and rejected date forms, and `balances` over a hand-built
   store covering an envelope with income only, one with income and spending, and one with no
   movements at all.

8. **Rewrite the eight cases in `tests/test_cli.py` that assert `envel list`'s exact stdout.**
   They are `test_ac2_list_after_new_writes_the_name`,
   `test_ac3_three_separate_invocations_share_one_store`,
   `test_ac4_listing_is_sorted_byte_wise_and_repeatable`, `test_ac5_a_repeated_name_is_refused`,
   `test_ac5_a_name_differing_only_in_case_is_refused`,
   `test_ac7_capitalisation_survives_the_round_trip`, `test_ac8_a_name_with_a_space_is_accepted`
   and `test_ac11_surrounding_whitespace_is_trimmed_before_comparing`. Each asserts a literal such
   as `"groceries\n"`, and each becomes the same assertion against the new line shape —
   `"groceries  0.00\n"`, `"a  0.00\nb  0.00\n"`, `"Zebra  0.00\napple  0.00\n"`.

   **What each case checks does not change, and must not.** Six of the eight belong to criteria
   `WI-0002` AC12 waives, and their substance is AC19's; `test_ac4` belongs to a criterion that is
   **not** waived — ordering and byte-stability — and only its literal moves. Do not weaken an
   assertion from an equality to a containment while you are in there: an equality is what makes
   "and nothing else on the line" checkable, and AC15 and AC19 both depend on it. Leave
   `test_ac1`, `test_ac6`, `test_ac9` and `test_ac10` alone; they are the four `envel list` cases
   whose subject is a store with nothing in it, or a command that is not `list`.

   `tests/test_envelopes.py` is not touched by this item: `envelopes.listing` keeps its signature
   and its behaviour.

9. **Write the new end-to-end cases in `tests/test_cli.py`**, one per criterion this item adds,
   named `test_ac<n>_<what>` in the file's existing convention and using its existing `envel`
   helper. AC13's and AC14's assert on stdout substrings rather than on the whole line, because the
   sentence is this plan's and not a criterion's. AC14 reads today's date with
   `datetime.date.today().isoformat()` in the test process rather than shelling out to `date`.

10. **Run the project's own commands from the repository root**:
    `python3 -m unittest discover -s tests -t .` and `python3 -m compileall -q envel tests`, both
    expected to exit 0. Report both runs with their output in `artifacts/impl-report.md`, and map
    each acceptance criterion to the case or the by-hand run that demonstrates it. Do **not** tick
    the checkboxes in `item.md` — that is `verify`'s, per `spec/work-item.md`.

11. **Repair the documents in the invalidation set**, which is what permits the edit. Each row
    below names its sentence; reopen each one, point it at what is now true, and bump the
    document's version with a change-log row. `docs/architecture/overview.md` is the one with real
    work in it: a fifth module, four commands rather than two, a store that holds transactions, and
    a test-count citation that has moved.

## Acceptance criteria mapping

| AC | satisfied by step | demonstrated by |
|----|-------------------|-----------------|
| AC1 — `envel income groceries 400` records it, exits 0, empty stderr, one stdout line | 1, 2, 3, 5 | a new case in `tests/test_cli.py`: `envel new groceries`, then `envel income groceries 400` asserting exit 0, `stderr == ""` and exactly one stdout line, then `envel list` asserting a line containing `groceries` and `400.00` |
| AC2 — `envel spend groceries 60` records it, exits 0, empty stderr | 1, 2, 3, 5 | a new case: income 400, then spend 60 asserting exit 0 and empty stderr, then `envel list` asserting `340.00` on the `groceries` line |
| AC3 — income 400 then spend 60, three separate invocations, `envel list` shows `340.00` | 2, 5, 6 | a new case running three subprocesses and asserting the third's stdout line contains `groceries` and `340.00` |
| AC4 — a recording command on an unknown envelope is refused and creates nothing; `Groceries` finds `groceries` | 2, 5 | two new cases: `envel income rent 100` and `envel spend rent 100` on a store holding only `groceries`, each asserting a non-zero status, `rent` in stderr, and a following `envel list` with a `groceries` line and no line containing `rent`; and `envel spend Groceries 10` on a store where `groceries` holds 40, asserting exit 0, empty stderr and `30.00` afterwards |
| AC5 — the balance survives a later, separate invocation | 3, 6 | the same case as AC3, extended with a fourth invocation of `envel list` asserting the identical line |
| AC6 — a spend larger than the balance is refused and the balance is unchanged | 2, 5 | a new case: `groceries` at 340, `envel spend groceries 500` asserting non-zero, `groceries` in stderr, and `envel list` still showing `340.00` |
| AC7 — `--date YYYY-MM-DD` is accepted; `2026-13-01` and `31/08/2026` are refused and record nothing | 1, 4, 5 | three new cases on a store where `groceries` holds 30: the well-formed date asserting exit 0 and empty stderr, and each malformed one asserting non-zero, a stderr line, and an unchanged `envel list` line |
| AC8 — a spend of exactly the balance leaves `0.00` | 2, 5, 6 | a new case: `groceries` at 340, `envel spend groceries 340` asserting exit 0, empty stderr, and `0.00` on the `groceries` line afterwards |
| AC9 — zero and negative amounts are refused on both commands | 1, 5 | one new case running all four invocations, each asserting non-zero and a stderr line, with the `envel list` line captured before and compared after; plus the `parse_amount` unit cases for `"0"` and `"-5"` in `tests/test_movements.py` |
| AC10 — `abc` and `""` are refused | 1, 5 | a new case running both invocations with the same assertions, plus the `parse_amount` unit cases |
| AC11 — a missing argument is refused | 4, 5 | a new case running `envel income groceries` and `envel spend`, each asserting non-zero, a stderr line, and no change to the `envel list` line |
| AC12 — a read of WI-0001's eleven criteria, six waived by name | 6, 8, 10 | `artifacts/impl-report.md` carries the eleven-row read, each row naming the criterion, the verdict and its evidence; the six waived rows cite `WI-0002/Q-001` and the AC19 case that carries the substance; the five live rows cite the `test_ac1`, `test_ac4`, `test_ac6`, `test_ac9` and `test_ac10` runs. `verify` makes the assessment; the report is the evidence it reads |
| AC13 — one line carrying envelope, amount, date and balance | 1, 5 | a new case: `groceries` at 400, then `envel spend groceries 12.50 --date 2026-08-31`, asserting exit 0, empty stderr, exactly one stdout line, and that the line contains each of `groceries`, `12.50`, `2026-08-31` and `387.50` |
| AC14 — with no `--date` the printed date is today's | 1, 5 | a new case asserting the stdout line contains `datetime.date.today().isoformat()`, computed in the test process |
| AC15 — `envel list` carries a balance on each line, in order, byte-stable | 2, 6 | a new case building `groceries` at 340 and `rent` at 0, asserting exit 0, empty stderr, exactly two lines, the first containing `groceries` and `340.00` and the second `rent` and `0.00`, and byte-identical stdout on a second run |
| AC16 — a new envelope shows `0.00` | 2, 6 | a new case: `envel new petrol` then `envel list`, asserting a line containing `petrol` and `0.00` and exit 0 |
| AC17 — a leading `£` is accepted and ignored, and the plain forms too | 1, 5 | a new case running `envel income groceries £12.50` and asserting exit 0, empty stderr and `12.50` on the listing line; and a second running `12`, `12.5` and `12.50` each asserting exit 0 and empty stderr; plus the `parse_amount` unit cases |
| AC18 — more than two decimal places is refused rather than rounded | 1, 5 | a new case running `envel spend groceries 12.345` and `envel income groceries 12.345` on a store where `groceries` holds 340, each asserting non-zero and a stderr line, and `envel list` still showing `340.00`; plus the `parse_amount` unit case for `"12.345"` |
| AC19 — the substance of the six waived criteria against the new line shape | 6, 8 | the four rewritten cases of step 8 that carry it — `test_ac7` (capitalisation), `test_ac8` (a name with a space), `test_ac3` (two envelopes, two lines, in order) and `test_ac11` (a trimmed duplicate refused, one line left) — each asserting the full new line, which is what makes "and nothing else" checkable |

## Assumptions

**P1 — the wording of every message this item adds is this plan's, and a disagreement lands on the
plan rather than on a criterion.** The criteria fix the stream, the exit status and the substrings;
the sentences are written out in steps 5 and 6 so that `implement` does not invent them and
`verify` has something to compare against. Reversing any of them is one string in `envel/cli.py`
and the tests that quote it. This is the same disposition WI-0001 made under its own P1
(`WI-0001/artifacts/plan.md`).

Nothing licensed this. There is no standing delegation anywhere in this engagement — it was
checked again this execution against all nine recorded human answers — so no `**Under delegation:**`
line can honestly be written here, and R12's other form applies: if the stakeholder dislikes a
sentence, that is a change to this plan and to the tests that quote it, and it costs no criterion.

**P2 — `--date` is extracted by hand, not by `argparse`.** `argparse` is in the standard library
and `ADR-0001` permits it, and it would bring `-h` and `--help`, its own usage text, its own exit
status, and its own opinion about a bare `-5`. Two of those collide with criteria that are already
signed off: WI-0001 AC9 and AC10 compare `envel list`'s stdout byte-for-byte against a reference,
and `WI-0002` AC9 requires `-5` to reach the amount parser rather than being read as an option.
Reversing this is one function in `envel/cli.py` — `_take_date` and its two callers — and no data
and no published interface moves with it. If a later item wants `--help`, adopting `argparse` then
is the same size of change it is today.

**P3 — an envelope's balance is computed on every command rather than cached.** `ADR-0007`
decision C names the alternative and why it is refused. Reversing this is adding a field and a
write path; the reason it is worth naming as an assumption rather than only as an ADR consequence
is that the first time a listing feels slow, a cache is the obvious fix and it is the one that can
silently disagree with the movements.

**P4 — `_check_shape` tolerates a version 1 document with no `transactions` key.** The alternative
is to upgrade before checking, which would validate a document this build partly invented rather
than the one on disk. Reversing it is the order of two calls in `load`.

## Decisions and ADRs

| decision | where it came from | recorded in |
|----------|--------------------|-------------|
| The store keeps the movements rather than a running balance | decided — the documents were silent and WI-0003 and WI-0005 make it near-irreversible later | `ADR-0007` |
| An amount is a positive integer number of pence | decided — `ADR-0006` fixed the printed form and left the stored one open | `ADR-0007` |
| Format version 2, and how a version 1 store is read | decided — `ADR-0003` provided the `version` field for exactly this | `ADR-0007` |
| Every printed amount and balance carries two decimal places | documented | `ADR-0006`, cited from steps 1, 5 and 6 |
| An envelope is matched by its trimmed casefolded name, and the stored display form is what a message says | documented | `ADR-0004`, cited from step 2 |
| One JSON store, at an overridable path, replaced atomically | documented | `ADR-0003`, unchanged by this item |
| Standard library only | documented | `ADR-0001` |
| The order in which a recording command refuses | decided — no criterion constrains it and the item routed it here | `## Approach`, above |
| The wording of every message this item adds | assumed | P1 |
| `--date` extracted by hand rather than by `argparse` | assumed | P2 |
| The balance is computed, not cached | assumed | P3, and `ADR-0007` consequence |
| `_check_shape` runs before the version upgrade | assumed | P4 |

## Invalidation set

| document | what | kind | why | disposition |
|----------|------|------|-----|-------------|
| `docs/architecture/overview.md` | `## The shape`, the `envel/cli.py` row: "reads `argv`, dispatches to `new` or `list`" with `[src: envel/cli.py:27]` | cited-fact | there are four commands after step 5, and the cited line has moved | to-update |
| `docs/architecture/overview.md` | `## The shape`, the whole table: it has four rows and there is a fifth module after step 1, `envel/movements.py` | cited-fact | a table that names the pieces of the system, missing one | to-update |
| `docs/architecture/overview.md` | `## The shape`, the closing sentence: "The dependency direction is one-way: `cli` imports both, `envelopes` imports neither `os` nor `store`, and `store` names no envelope rule" | quantified | it enumerates the modules by name and a fifth appears; the direction it asserts is still true and the enumeration is not | to-update |
| `docs/architecture/overview.md` | `## The shape`, the `envel/store.py` row's line citations `[src: envel/store.py:27; envel/store.py:39; envel/store.py:58]` | cited-fact | step 3 changes `envel/store.py` above those lines | to-update |
| `docs/architecture/overview.md` | `## State`, first sentence: "one piece of state: a JSON document holding the store-format version and the envelopes in creation order" | cited-fact | after step 3 it also holds the transactions, and the version is 2 | to-update |
| `docs/architecture/overview.md` | `## Conventions`, the test citation `[src: ... run: python3 -m unittest discover -s tests -t . → exit 0, 24 tests, OK]` | cited-fact | steps 7 and 9 add cases, so the count in the recorded outcome is no longer what the command prints | to-update |
| `docs/architecture/overview.md` | `## Conventions`, the end-to-end citation `[src: tests/test_cli.py:29]` on the sentence about invoking `envel` as a subprocess | cited-fact | **added by `implement`**: not in the set as `plan` wrote it, and step 9 moved the line — the helper is at `tests/test_cli.py:35` after the imports the new cases need. Found while repairing the row above it, in the same bullet | to-update |
| `docs/product/vision.md` | `## Engagement state`, all three bullets — "Five questions from intake are open with them", "Nothing has been designed or built. The epic has three work items, all at `draft`" | engagement-state | already false before this item and further falsified by it; nobody here may write one | owned-by-ending |
| `docs/architecture/adr/ADR-0003-one-json-store-and-where-it-lives.md` | `## Decision`, the JSON block showing `{"version": 1, "envelopes": [...]}` and the sentence "Its shape at this version" | cited-fact | read against this change and **not** falsified: the sentence is scoped "at this version" and stays true of version 1, and `ADR-0007` extends rather than supersedes. The row is here because a reader who finds the store holding `transactions` will come to this document first | verified-still-true |
| `docs/architecture/adr/ADR-0006-money-is-pounds-and-pence.md` | rule 3, "every amount and every balance the tool prints is written with exactly two decimal places" | quantified | read against this change and **not** falsified — this item is the first to make it true, at steps 5 and 6 — but its enumeration named three print sites, and step 5's refusal messages are the third. Whoever audits it owes the members, not a citation **Re-read after `answer-questions` acted on `WI-0002/Q-004`:** **re-disposed by `answer-questions` for `WI-0002/Q-004`.** Read against this change and still not falsified, and the row's own subject (rule 3) is untouched; the document was nevertheless written on this branch, so the set must name it. `## Options considered` option B gained a resolving citation through an append-only `## Corrections` entry of kind `provenance` (`spec/doc-header.md` §4b), version 1 → 2 | to-update |
| `docs/process/ways-of-working.md` | the whole document: `## When a pipeline gate refuses something no actor is permitted to fix` and `## Where an accepted test-coverage gap goes` | cited-fact | read against this change and **not** falsified: both sections are about the pipeline's own conventions and neither mentions the tool's behaviour, its store or its commands **Re-read after `answer-questions` acted on `WI-0002/Q-004`:** **re-disposed by `answer-questions` for `WI-0002/Q-004`.** Still not falsified by this item's code, and the two sections the row names are unchanged in what they require; one sentence in `## Where an accepted test-coverage gap goes` gained the citations it owed under `spec/doc-header.md` §4a, version 2 → 3 | to-update |

## Deliverable documents

`none`. No acceptance criterion of this item is about a document: all nineteen are observed by
running `envel` and reading its streams and its exit status. `docs/architecture/overview.md` is
changed by step 11 because it is in the invalidation set, which is a repair rather than a
deliverable.

## Binding ADRs

- `ADR-0001` — standard library only. Binds every step: `re`, `json` and `datetime` are in it,
  and nothing else is reached for.
- `ADR-0002` — `envel` runs from a launcher script. Binds nothing this item changes; `bin/envel`
  is untouched, which is why the new commands are reached through `main` rather than through a
  second entry point.
- `ADR-0003` — one JSON store, at an overridable path, replaced atomically. Binds step 3: the file
  stays one document at that path, `save` is unchanged, and the `version` field is used for the
  purpose that ADR gave it.
- `ADR-0004` — an envelope's identity is its trimmed casefolded name. Binds step 2's `balances`
  and `record` and step 5's lookup: the identity is what matches a movement to an envelope, and a
  message names the **stored** display form rather than what was typed.
- `ADR-0005` — text crossing the process boundary. Binds steps 4 and 5 by constraining where the
  amount may be parsed: `BUG-0001` establishes a recovery boundary at the top of `main` in
  `envel/cli.py`, and the parsers in `envel/movements.py` take a `str` that has already crossed
  it. See `## Risks` for the branch-order consequence.
- `ADR-0006` — money is pounds and pence, written with two decimal places. Binds steps 1, 5 and 6:
  rule 2 is `parse_amount`, rule 3 is `format_amount`, and every criterion that names a literal
  such as `340.00` rests on rule 3.
- `ADR-0007` — the store keeps the movements, in integer pence. Written by this execution; binds
  steps 1, 2, 3, 5 and 6.

## Scaffolding

`none`. Every file this plan creates — `envel/movements.py`, `tests/test_movements.py` — carries
behaviour or cases and is `implement`'s to write. The project's test and lint commands already
run: `tests/__init__.py` exists and `python3 -m unittest discover -s tests -t .` is green today.

## Risks

- **`BUG-0001` and this item both change `envel/cli.py`, on separate branches, at the same place.**
  `BUG-0001` step 2 recovers every element of the argument list at the top of `main`; this item's
  step 4 extracts `--date` from the operands and step 5 parses them. Whichever merges second has a
  conflict in `main`. It is small and it is textual rather than semantic — the two changes compose,
  because recovery happens to the whole list before dispatch and extraction happens to a command's
  operands after it — but whoever merges second must read `main` rather than take either side. If
  `BUG-0001` merges first, this item's step 5 must not re-recover an argument that has already been
  recovered.
- **AC17's `£` is a non-ASCII character in an argument, which is `BUG-0001`'s subject.** Under a
  UTF-8 locale, which is what the suite runs in, `parse_amount("£12.50")` sees the character and
  the criterion passes. Under the locale `BUG-0001` reproduces, the argument arrives as
  surrogates and `parse_amount` refuses it as not an amount — a refusal with a message rather than
  a traceback, which is defensible, and is not what the person typed. AC17 says nothing about the
  locale, so this item is correct as written and is deliberately **not** sequenced behind the bug
  (`WI-0002/item.md`). It is named here so that whoever reads a bug report about `£` under `LC_ALL=C`
  finds it was foreseen.
- **Step 8 edits tests WI-0001 wrote, and that is the step most likely to be done wrongly.** The
  temptation is to relax an equality assertion to `assertIn` so the case passes whatever the line
  turns out to be. That would silently retire the "and nothing else on the line" half of AC15 and
  AC19. The step says so; a reviewer should check the diff for `assertEqual` becoming `assertIn`.
- **A store written by a future `envel` is refused rather than read.** Step 3 makes that a
  `StoreError`, which prints an `envel:` line and exits 1. If the person has two machines with
  different versions — which the vision says they do not [src: EP-001/Q-001] — this would look
  like their data had vanished. It has not; the file is untouched.
- **`format_amount` is written for non-negative pence.** `f"{-50 // 100}.{-50 % 100:02d}"` gives
  `-1.50`, which is wrong. Nothing in this item can produce a negative balance — AC6 and AC9 are
  what prevent it — so the function is not written to handle one, and WI-0005, which can reduce a
  balance by correcting a spend, is where that has to be looked at again.

## Out of scope for this item

- Listing the individual transactions of an envelope. The store holds them after step 3 and
  nothing in this item prints them; that is WI-0003's.
- Moving money between envelopes (WI-0004) and correcting a recorded spend (WI-0005).
- A flag that turns the balances off. The stakeholder declined one (`WI-0002/Q-001`).
- `--help`, and any option on `new` or `list`. P2 is why.
- Making `envel new` print a confirmation. Left silent; the reasoning is `A8` in
  `artifacts/refinement-qa.md`.

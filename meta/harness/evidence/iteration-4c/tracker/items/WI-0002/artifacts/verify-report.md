# Verification report — WI-0002

Verified-commit: c706d837b0a8a6555b201858efabc68c3ac720b6

Branch `wi/WI-0002`, working tree clean of source modifications at the time of verification.
Every command below was run by this skill against that head. The card files used are seeded by
hand into `/tmp/vwi2/` in `ADR-0007`'s documented format and read back with `grep`, `cat` and
`sha256sum` — no part of this verification imports `recall.store`, and no verdict rests on
`impl-report.md`.

## Verdict

**Pass.** All fourteen acceptance criteria are demonstrated by commands run here, with their
actual output quoted. No defect was found, no bug item was filed, and nothing was sent back.

One thing is recorded for `review-close` rather than as a defect: `docs/architecture/overview.md`
says `review` "is planned", which this branch makes false. `implement` declared it in
`impl-report.md` under `## What I did not do` and did not repair it, because
`spec/doc-header.md` §5 forbids `implement` writing to `docs/`. It is a D7 and D12 obligation at
the close, not a failure of any criterion of this item — no criterion of WI-0002 mentions the
overview.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | one card `FRONTWORD`/`BACKWORD` due today; `printf 'q\n' \| recall review`, then the same session driven with `printf '\nq\n'` | quitting at the reveal prompt printed `[1/1] FRONTWORD` and `Enter to see the back, q to stop.`; `grep -c BACKWORD` over that whole output → **`0`**. With Enter first, the output contains `  BACKWORD` followed by the outcome prompt | the back cannot have leaked earlier: the first run's output *is* everything printed up to and including the reveal prompt |
| AC2 | **pass** | six cards seeded due −3, −1, 0, 0, +1, +7; whole session answered right | `4 cards due.` then `[1/4] CARD-overdue3`, `[2/4] CARD-overdue1`, `[3/4] CARD-today-a`, `[4/4] CARD-today-b`. `CARD-tomorrow` and `CARD-week` never appear | hand-checked against the file: `grep -n 'front:\|due:'` shows exactly four `due:` values ≤ 2026-08-30. No cap — all four offered |
| AC3 | **pass** | a rung-2 card due 40 days ago, driven as a **live** subprocess: Enter sent, then the card file read from outside the running process; then `y` | mid-session, with the process still alive: file digest unchanged and `rungs: ['2', '1', '1']`. After `y`: `rung: 3`, `due: 2026-09-06` — today+7, not 40-days-ago+7. A rung-4 card due 99 days ago answered `n` → `rung: 1`, `due: 2026-08-31` | overdue changes nothing about the card until it is answered, and both outcomes count from the day of the review |
| AC4 | **pass** | the same live session: after `y` was sent, the card file was polled from outside until it changed, then the process was checked | `alive: True  rungs: ['3', '1', '1']  dues: ['2026-09-06', '2026-08-28', '2026-08-29']` — the answer is on disk while the session is still running and the next card has not been answered. `y`/`n` are the only outcomes: at the outcome prompt `1` and `maybe` were both refused with `Not one of the answers. This prompt takes: y, n, q.` | this is the "read the file from another terminal part-way through a session" the criterion asks for, done from a second process |
| AC5 | **pass** | five cards seeded one per rung 0–4, all due today, every one answered `y` | `rung: 1 due: 2026-08-31`, `rung: 2 due: 2026-09-02`, `rung: 3 due: 2026-09-06`, `rung: 4 due: 2026-09-29`, `rung: 4 due: 2026-09-29` | today was 2026-08-30, so the intervals are +1, +3, +7, +30, +30 and rung 4 stays at rung 4 |
| AC6 | **pass** | the same five-rung deck, every card answered `n` | five identical records: `rung: 1  due: 2026-08-31` | from every rung including 0 and 4 |
| AC7 | **pass** | three overdue cards; session 1 answers `ONE` right then quits; session 2 is a **new process** the same day; then the rest answered and a fourth process run | session 1: `3 cards due.` … `Stopped. 1 card answered`. Session 2: `2 cards due.` … `[1/2] TWO` — `ONE` is not offered. After the rest: `Nothing is due.`, exit 0 | the updates survive the process exiting, and a second session the same day offers only what is still due |
| AC8 | **pass** | three separate seeds: a card due +3; a file holding only the header; and no file at all | each → exit `0`, stdout exactly `Nothing is due.`, stderr empty. `sha256sum` before and after identical for the first two (`a80a0c608792`, `c6878c0d5979`); for the third the file still does not exist afterwards, and no directory was created | the three are one case, as the criterion requires |
| AC9 | **pass** | (a) three cards, `\ny\nq\n` — quit after one answer; (b) the live session above **SIGKILLed** at a prompt via `Popen.kill()` | (a) `Stopped. 1 card answered; the rest are still due.` and session 2 offers the other two. (b) `returncode: -9`, and afterwards `rungs: ['3', '1', '1']`, `dues: ['2026-09-06', '2026-08-28', '2026-08-29']` — the answered card kept its new schedule and the two unreached cards are exactly as seeded | the kill case is a real `SIGKILL` to a process waiting at a prompt, not a substitute |
| AC10 | **pass** | the six-card deck of AC2; count read from the tool and computed by hand from the file | tool printed `4 cards due.` **before** `[1/4] CARD-overdue3`. Hand count of `due:` lines ≤ today in the seeded file: 4. A one-card deck printed `1 card due.` | the number is stated before the first card and matches the file |
| AC11 | **pass** | one card, four separate runs: `q\n`; `\nq\n`; empty input; `\n` alone | all four → exit `0`, **stderr empty**, card file `sha256` unchanged, and `Stopped. 0 cards answered; the rest are still due.` on stdout | `q` and end-of-input at both prompts. Both prompts name their keys: `Enter to see the back, q to stop.` and `y if you got it right, n if you got it wrong, q to stop.` |
| AC12 | **pass** | four cards seeded out of due order; then the file restored byte-for-byte and the session run again | first run `[1/4] beta [2/4] alpha [3/4] gamma [4/4] delta`; second run identical — compared with `[ "$run1" = "$run2" ]` → `SAME ORDER TWICE`. In AC2's deck, the two cards sharing 2026-08-30 came out in their file order (`CARD-today-a` at line 4 before `CARD-today-b` at line 19) | the order is a function of the stored file alone, and predictable from reading it |
| AC13 | **pass** | a rung-2 card; input `x`, `zz`, Enter, `1`, `maybe`, `y` | the reveal prompt was reprinted **in full, card front included**, after each of `x` and `zz`, each time preceded by `Not one of the answers. This prompt takes: Enter, q.`; the outcome prompt likewise after `1` and `maybe`, with `This prompt takes: y, n, q.` The card ended `rung: 3  due: 2026-09-06` — exactly one right answer | the rung-2 seed is deliberate: at rung 0 a right and a wrong answer both give rung 1 due +1, so a rung-0 card cannot distinguish "answered right once" from "counted as wrong". Re-run at rung 2, where right → 3/+7 and wrong → 1/+1 are distinct. `n` after the same refusals gave `rung: 1 due: 2026-08-31` |
| AC14 | **pass** | a file with `bakc:` for `back:` on line 5, driven with `\ny\n` | exit `1`; stderr `/tmp/vwi2/ac14.txt: line 5: expected a line starting 'back: ', found 'bakc: hello'`; stdout **empty** — no front shown; `sha256` unchanged. A second shape, `rung: 9`, gave `line 5: 'rung: 9' is outside 0 to 4`, exit 1 | the message names the file and the line, and line 5 is genuinely the mangled line |

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t . -q` run here on `c706d83` → exit 0, `Ran 60 tests in 2.702s`, `OK` |
| `lint-clean` | **pass** | `python3 -m compileall -q recall tests` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace` → 0 errors, 0 warnings |
| `every-criterion-independently-checked` | **pass** | the table above: fourteen rows, each naming a command this skill ran against a hand-seeded card file, with the actual output quoted. No row cites `impl-report.md` |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — eleven conditions triggered, not read about |
| `a-criterion-about-criteria-is-read` | **pass, vacuously — and then done anyway** | No criterion of WI-0002 has other criteria as its subject: AC1–AC14 each describe the session's own behaviour. AC14's parenthesis *"This is the refusal WI-0001's `add` already makes"* is a reference to a mechanism, not a claim about a criterion. The gate is therefore vacuous. Because this item nonetheless changes `main()`'s dispatch, WI-0001's eight criteria were read against the new behaviour anyway — see below |
| `tests-would-fail-without-the-change` (advisory) | **pass** | fifteen mutations applied and reverted by this skill; see `## Test sensitivity check` |

### WI-0001's criteria, read against the new behaviour

Not required by the gate, done because `main()` now branches where it used to call `add()`
unconditionally. Each read, then demonstrated:

- **AC1, AC8** — `recall add bonjour hello` against a path with no file → `Added: bonjour`, exit 0,
  file created. Still true.
- **AC3, AC4, AC5** — three adds gave three separate records, each `rung: 0` and `due: 2026-08-30`,
  the whole file readable with `cat`. Still true.
- **AC6** — a second `bonjour` printed `Warning: a card with the front 'bonjour' already exists;
  adding this one as well.` and `Added: bonjour`, exit 0, both cards present. Still true.
- **AC7** — `recall add "" nothing` → `The front side is empty.` / `Nothing was added.`, exit 1,
  file byte-identical. Still true.
- **AC2** — the restart criterion. Not re-executed here; it was accepted at WI-0001's close with
  its literal machine restart recorded as a gap in that item's `## Notes`, and this item changes
  nothing about how the file is written.

**Non-intersection, stated plainly:** nothing executable exercises WI-0001's `add` and WI-0002's
`review` in the same test. `tests/test_add.py` and `tests/test_store.py` are untouched by this
branch — `git diff main..HEAD` over them is empty — and all 26 pass unmodified, but they run
`add` only. **A covering case was added by hand rather than waived:** three cards written by
`add` were then offered by `review` in the same deck, which printed `3 cards due.` and the three
fronts `add` had written. That is the intersection, and it holds.

## Negative and boundary cases exercised

Each of these was produced, not read about:

1. **Nothing due** — every card due in the future → `Nothing is due.`, exit 0, bytes unchanged.
2. **An empty deck** — a file with the header and no cards → same.
3. **No card file at all** — → same, and no file or directory created.
4. **A card file that will not parse** — `bakc:` for `back:` → exit 1, message naming file and
   line 5, nothing shown, bytes unchanged.
5. **A second unparsable shape** — `rung: 9`, outside `ADR-0007`'s 0–4 → exit 1, `line 5: 'rung: 9'
   is outside 0 to 4`.
6. **Unrecognised input at the reveal prompt** — `x`, `zz` → re-asked with the front reprinted.
7. **Unrecognised input at the outcome prompt** — `1`, `maybe` → re-asked with the back reprinted.
8. **End of the input stream at each prompt** — empty input and `\n` alone → clean exit 0.
9. **`q` at each prompt** — exit 0, stderr empty, file untouched.
10. **The boundaries of the ladder** — rung 0 (never answered) and rung 4 (the top), answered both
    ways: 0→1 and 4→4 on right, both →1 on wrong.
11. **The due boundary** — a card due exactly today is offered, one due tomorrow is not.
12. **A kill at a prompt** — `SIGKILL`, `returncode: -9`.
13. **Two cards sharing a front side** (`WI-0001 AC6` makes this legal) — answered right and wrong
    respectively; the file afterwards shows `first-back` at rung 2 due +3 and `second-back` at
    rung 1 due +1. The session wrote back the card it actually asked about, not the first match.
14. **`review` given an argument it does not take** — `usage: recall [-h] {add,review} ...` and
    `unrecognized arguments: extra`, exit 2.

## Test sensitivity check

Fifteen mutations were applied to the branch head by this skill, the suite run against each, and
the file restored; `git status --short recall/` was `clean` afterwards and the suite green.

| criterion | mutation | tests it broke |
|-----------|----------|----------------|
| AC1 | the reveal prompt prints `front = back` | 2, incl. `test_the_back_is_hidden_until_enter` |
| AC2 | `is_due` uses `<` instead of `<=` | 15 |
| AC3 | reschedule from `card.due` instead of `today` | 9, incl. `test_an_overdue_card_is_unpenalised` |
| AC4, AC7, AC9 | one `store.save()` at the end instead of per answer | 4, incl. `test_a_kill_at_a_prompt_keeps_the_answers_already_given` |
| AC5 | `INTERVALS` 7 → 6 | 5 |
| AC5 | the rung cap removed (rung 4 → 5) | 2 |
| AC5 | the rung cap one too low (`min(rung + 1, 3)`) | 2 |
| AC6 | `FIRST_RUNG = 2` | 4 |
| AC8 | the nothing-due path writes the file | 1 |
| AC10 | the count line removed | 4 |
| AC11 | `q` at the outcome prompt counts as an answer | 1 |
| AC12 | `due_positions` returns its list unsorted | 4 |
| AC12 | ties broken by front side instead of file order | 2 |
| AC13 | `_ask` accepts any line | 2 |
| AC14 | `CardFileError` swallowed into an empty deck | 1 |
| AC1, AC4 | `main()` calls `add()` unconditionally again | 22 |

**One mutant survived, and it was mine, not a gap.** Replacing `min(card.rung + 1, HIGHEST_RUNG)`
with `card.rung + 1 if card.rung < 3 else 4` broke nothing — because the two expressions agree on
every rung 0–4. It is an equivalent mutant, not a hole in the tests; the two replacements that
genuinely change the cap (removing it, and setting it to 3) both fail
`test_answering_right_walks_the_ladder` and `test_right_at_the_command_line`. Recorded because a
survivor left unexplained is exactly what this section exists to surface.

## Defects found

**None.** Nothing was sent back and no bug item was filed.

Three things were looked at closely and judged not to be defects:

1. **`Y ` (capital, trailing space) is accepted as `y`.** AC13 governs "input the session does not
   recognise"; `Y ` normalises to something the prompt does accept, so it is recognised. This is
   `plan.md`'s assumption 2, recorded before the code was written, and it reverses in one line.
2. **The session prints `[1/4]` before each front and `Done. N cards reviewed.` at the end.**
   No criterion requires either; none forbids them. Prompt and message wording is explicitly
   `implement`'s under `plan.md`'s assumption 4, and AC10's required count is a separate line
   (`4 cards due.`) printed before the first card.
3. **The header comment of a hand-seeded file is rewritten on the first save.** `ADR-0008` says
   every save rewrites the whole file; AC8's byte-identity requirement applies only where nothing
   is written, and it held in all three of its cases.

## Not verified, and why

- **WI-0001's AC2 — a literal machine restart.** Out of reach here, as it was at WI-0001's close,
  where it is recorded as an accepted gap in that item's `## Notes`. WI-0002 changes nothing about
  how the file is written; what is demonstrated instead is that a *new process* the same day reads
  what an earlier process wrote (AC7 above).
- **Concurrent sessions.** `plan.md`'s assumption 5 says the session does not re-read the card
  file after it starts, so a second writer's changes would be overwritten at the next save. No
  criterion of this item covers it and `ADR-0001` makes the tool single-user; it is stated here so
  the limit is on the record rather than discovered later.
- **A filesystem that does not support directory `fsync`, and a full disk.** `store.save()`'s
  failure paths are WI-0001's and were accepted there.
- **How long a session takes with a large backlog.** No criterion bounds it — deliberately, per
  `ADR-0003` and the stakeholder's answer to `EP-001/Q-005`. The cost `plan.md` names (one whole-
  file rewrite and two `fsync` calls per answer) was observed at three-card scale and not measured
  at any larger one.
- **`docs/architecture/overview.md`'s staleness was not repaired.** It is not this skill's to
  write (`spec/doc-header.md` §5 names `implement` and `verify` together), and it is not a
  criterion of this item. Carried to `review-close` as a D7 and D12 obligation.

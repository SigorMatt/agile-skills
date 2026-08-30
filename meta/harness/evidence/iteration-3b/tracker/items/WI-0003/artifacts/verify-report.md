# Verification report — WI-0003

Verified-commit: a93db5fe5e045533f610890bdc479e5c4d213fc4

## Verdict

**Pass.** All eleven acceptance criteria are met. Every verdict below rests on a command this
skill ran against the branch head, and — for AC1 to AC9 — on **inputs written here from each
criterion's own prose**, spaced differently from the fixtures the implementation added, with the
output diffed against the expected table extracted programmatically from `item.md` and `plan.md`.
No verdict rests on `impl-report.md`.

Three observations that are not defects and are recorded so nobody has to rediscover them:

1. **AC3, AC5 and AC8 quote tables whose exempt cells are their columns' widest.** For each,
   `W - w` is zero, so the quoted output is *also* what a filter with no exemption at all would
   produce. `impl-report.md` declares this for AC3 and AC5 and adds a discriminating case to AC3's
   test; this verification re-derived it independently and wrote its own discriminating cases for
   all three (see `## Test sensitivity check`). The behaviour is present; the criteria as written
   simply do not all detect its absence.
2. **WI-0002 AC1's narrowing has no observable consequence.** A left-marked cell and an exempt
   cell compose identically, so the sentence WI-0003 AC10 requires be marked narrowed is still
   literally true of every output byte. It is recorded as narrowed anyway, because AC10 requires
   it and because the *reason* the sentence holds has changed.
3. **A cell whose text is a code span or prose containing `<br>` is exempt too.** The rule is
   textual and has no notion of context. That is ADR-0008's stated and accepted cost, not a
   defect.

## Criteria

| AC | verdict | command run | actual output | notes |
|----|---------|-------------|---------------|-------|
| AC1 | **pass** | wrote `/tmp/vfy/ac1.md` — a centre-marked single-column table, header `form`, six body rows holding the six texts AC1 names, ragged differently from `break_forms.md`; `python3 mdtab.py < /tmp/vfy/ac1.md \| diff -u <the block extracted from item.md> -` | `AC1 PASS (exit 0, output identical to the table AC1 quotes)` — no diff | Then read the two prose clauses off that output: each of the six is `" " + text + (8 - w) spaces + " "`, and `form` is `\|   form   \|`, centred by WI-0002 AC3's formula. Both PASS |
| AC2 | **pass** | same method with `/tmp/vfy/ac2.md` — centre-marked, header `text`, the five texts AC2 names | no diff against AC2's quoted table | Each of the five checked against WI-0002 AC3's arithmetic `(W-w)//2` before and the remainder after, `W = 11`: PASS. So a trailing backslash, another HTML tag and a word beginning `br` all still obey the marker |
| AC3 | **pass** | `/tmp/vfy/ac3.md` — left, right and centre markers, a break tag in the right-marked **header** and in one centre-marked body cell, one row padded absurdly wide in the input | no diff against AC3's quoted table | All three things AC3 says must be read off the output were read: the header `own<br>er` is laid out left under a right marker; `alice`, `bo`, `c` are still right-placed and `ok`, `done` still centred beside `x<br>y`; the left-marked column is untouched. See `## Test sensitivity check` for the extra discriminating case, since every exempt cell in AC3's own table has `W - w = 0` |
| AC4 | **pass** | `/tmp/vfy/ac4.md` — an unmarked column holding `a<br>b` and `plain`; then `/tmp/vfy/ac4_sub.md`, the same table with the tag replaced by `axxxxb`, the same display width | `\| note   \| n  \|` / `\|--------\|----\|` / `\| a<br>b \| 1  \|` / `\| plain  \| 22 \|`, exit 0 | Every content cell of the unmarked column is `" " + text + (W-w) spaces + " "`. The substitution run confirms AC4's "no output byte differs" clause directly: the two outputs are identical modulo the six characters of text |
| AC5 | **pass** | `/tmp/vfy/ac5.md` — a two-column centre-marked Task/Notes table whose widest cell is the exempt one | no diff against AC5's quoted table | All five output lines have display width 34 and every `\|` is at the same display column on every row; the exempt cell has `W - w = 0`; `ready` and `ok` are centred within the width it set |
| AC6 | **pass** | `/tmp/vfy/ac6.md` — two right-marked columns, break tags in the first column's header and both body cells, input delimiter deliberately over-wide | no diff against AC6's quoted table | Every content cell of column 0 is laid out left; its output delimiter cell is `---------:` — begins with a hyphen, ends with `:`, as the input's did; column 1 is right-aligned throughout. A wholly exempt column keeps its marker |
| AC7 | **pass** | `/tmp/vfy/ac7_empty.md` — empty cells in a right-marked and a centre-marked column beside two exempt cells; then, for each of my AC1, AC2, AC3, AC5 and AC6 inputs, every output delimiter cell compared against the input's, with `W` recomputed from the input's own content rows | empty cells came back `'   '` (`W + 2` with `W = 1`), not shortened; the delimiter sweep printed `PASS delimiter cells over AC1, AC2, AC3, AC5, AC6: colon-for-colon, hyphens between, W + 2, no spaces` | Also ran `\|a\|b\|` / `\|:-<br>-:\|-\|` / `\|x\|y\|`: a delimiter cell cannot contain `<`, so that block is not a table and is copied whole, which is why the delimiter row is unreachable by the exemption rather than merely untouched by it |
| AC8 | **pass** | `/tmp/vfy/ac8_indent.md` (three-space indent, a break tag in one cell), `/tmp/vfy/ac8_fenced.md` (both a ``` and a `~~~` fence containing table-looking lines with `<br>`), `/tmp/vfy/ac8_malformed.md` (a body row with a different cell count, carrying `<br>`) | indented: every line begins `   \|`, the exempt cell is `\| do<br>it \|`, exit 0. Fenced and malformed: `o == src` byte for byte, exit 0 | Also confirmed the two blocks the tool must not touch at all: a `> `-prefixed table with `<br>` and an indent-mismatched block with `<br>` both came back byte-identical |
| AC9 | **pass** | ten inputs — my AC1 to AC8 inputs plus the empty-cell and no-marker ones — each filtered once and the result filtered again | `PASS filtering the output again is byte-identical, exit 0 both times, for all ten inputs` | |
| AC10 | **pass** | the twenty-one per-ID verdicts below, each read from the prior criterion's own text, with a command run as evidence for each | see `## AC10 — the twenty-one prior criteria, read by ID` | The three statements AC10 requires are made there explicitly, and the two non-intersections are named in those words with a waiver by ID |
| AC11 | **pass** | `grep -c "def test_wi0003_ac<n>_" tests/test_mdtab.py` for n in 1..11, deliberately not the suite's own coverage test; then `python3 -m unittest discover -s tests -t .`; then every AC1–AC9 input run and re-run | each n matched exactly one method, all named `test_wi0003_ac<n>_<slug>` per ADR-0006; `Ran 37 tests in 7.861s / OK`, exit 0; every input exited 0 on both passes | |

## AC10 — the twenty-one prior criteria, read by ID

Each verdict below was reached by reading that criterion's **own sentence** against what the
filter now does. The suite is evidence, never the definition. The three statements WI-0003 AC10
demands are made in full.

### WI-0001

| ID | verdict | why, read from its text | evidence I ran |
|----|---------|-------------------------|----------------|
| AC1 | still true | "every line of that table in the output has the same display width" — the exemption moves text inside a column's width and changes no width | a ragged marked table of `中文`, `éclair`, `🙂`, `日本語<br>x` and `a<br>b`: all five output lines have display width 37 |
| AC2 | still true | "every column occupies the same span of display columns on every row" — same reason | the same table: every `\|` at the same display offsets on all five rows |
| AC3 | still true, and **widened** rather than narrowed | its text — `\|`, one space, the text, "spaces padding it to the column's width", one space — describes padding *after* the text. WI-0002 AC9 narrowed it to unmarked columns. An exempt cell has its padding after the text, so AC3's sentence is literally true of exempt cells in marked columns too | my AC1, AC4 and AC6 outputs; and "no line the filter composes ends in a space or a tab" swept over every break-tag output produced here: PASS |
| AC4 | still true | "the delimiter row … `\|` followed by (width + 2) hyphens and no spaces" — as WI-0002 already narrowed to unmarked columns. The exemption cannot reach a delimiter cell | the delimiter sweep over five break-tag tables, plus the `\|:-<br>-:\|` block that is not a table at all |
| AC5 | still true | "every one of its output lines begins with that same run, byte for byte"; and indent-mismatched and `> `-prefixed blocks byte-identical | `   \|a<br>b\|c\|` table keeps its run; indent-mismatch and blockquote versions carrying `<br>` came back byte-identical |
| AC6 | still true | "input containing no table → byte-identical", incl. empty, no final newline, CRLF, invalid UTF-8 | all five run with a `<br>` in them: empty, prose, CRLF, no-final-newline and `\xff\xfe <br> \x80` — every one byte-identical, exit 0 |
| AC7 | still true | fenced blocks are copied. The predicate is applied to a cell of a block `table_or_none` already accepted, so a fence is unreachable | `/tmp/vfy/ac8_fenced.md`, both fence kinds, byte-identical |
| AC8 | still true | a malformed block is copied whole | `/tmp/vfy/ac8_malformed.md`, byte-identical, its well-formed rows untouched |
| AC9 | still true | idempotence over AC1 and AC5–AC8's inputs | the ten-input idempotence loop above, all break-tag inputs |
| AC10 | still true | exit status 0 | every command in this report recorded exit 0 |
| AC11 | still true, **non-intersecting** | its subject is the suite's method names, not the filter's output | **Nothing executable exercises WI-0001 AC11 and a break tag together**, and nothing can: a break tag is a property of input text and AC11 is a property of test names. **Waived by ID: WI-0001 AC11**, because a covering case is not writable, not because it is not worth writing. What *could* break it is a later item's test names, and that was checked instead: every `wi0001_ac1..11` tag still matches exactly one method after this item added eleven of its own — ADR-0006's per-item prefix is why |

### WI-0002

| ID | verdict | why, read from its text | evidence I ran |
|----|---------|-------------------------|----------------|
| AC1 | **narrowed** | "every content cell of that column in the output is `\|`, one space, the cell text, `W - w` spaces, one space" now holds only of a content cell containing **no break tag**. The exception is asserted in **WI-0003 AC3** above, on authority of ADR-0007 and ADR-0008. WI-0002's criteria are not edited: their author narrowed them [src: EP-001/Q-005]. **In this case the narrowing has no observable consequence** — a left-marked cell and an exempt cell compose identically — but the sentence's reason has changed and it is recorded as narrowed | ran a left-marked column holding `a<br>b`, then the same table with `axxxxb` in its place: outputs identical modulo the six characters of text |
| AC2 | **narrowed** | "every content cell of that column … `W - w` spaces, the cell text" now holds only of a cell containing no break tag; an exempt cell in a right-marked column sits left. Asserted in **WI-0003 AC3** (`own<br>er` under a right marker) and AC6; authority ADR-0007 and ADR-0008 | my AC3 output: `\| own<br>er \|` left, `alice`, `bo`, `c` still right-placed; my AC6 output: a wholly exempt right-marked column |
| AC3 | **narrowed** | "every content cell of that column … `(W - w) // 2` spaces, the cell text" now holds only of a cell containing no break tag. Asserted in **WI-0003 AC1** (six exempt cells under a centre marker) and AC5; authority ADR-0007 and ADR-0008 | my AC1 output (six left, header centred) and AC5 output (`build<br>test<br>ship` left, `ready` and `ok` centred) |
| AC4 | still true | "no marker … byte-identical to what WI-0001 AC3 requires, and unchanged by this item" — the exemption selects the same `before = 0` | WI-0003 AC4's run and its substitution check |
| AC5 | still true | an empty cell's text contains no break tag, so it is placed by AC1, AC2 or AC3 with `w = 0` | `/tmp/vfy/ac7_empty.md`; and a table with a wholly empty row across left, right and centre markers beside `a<br>b`: each empty cell `W + 2` spaces, and the output idempotent |
| AC6 | still true | markers and display width together | the `中文`/`🙂`/`éclair`/`日本語<br>x` table: one distinct line width, identical column offsets |
| AC7 | **still true** — and this is one of the two statements AC10 requires | "the output delimiter cell begins with `:` iff the input's did … `W + 2` characters with no spaces". Read against **WI-0003 AC1, AC2, AC3, AC5 and AC6** — the five tables AC7 of this item names — and against AC6's wholly exempt column, where a column keeps a marker not one of its cells obeys | the delimiter sweep: colon-for-colon, hyphens between, `W + 2`, no spaces, on all five; plus `---------:` on the wholly exempt column |
| AC8 | **still true** — the other statement AC10 requires | "idempotence over marked tables, for each of the inputs named in AC1 to AC7". Read against **WI-0003 AC1 to AC9's inputs**, every one of them marked and carrying a break tag | the ten-input idempotence loop: byte-identical, exit 0 on both passes |
| AC9 | still true, **non-intersecting** | its subject is what `verify-report.md` records, not what the filter outputs | **Nothing executable exercises WI-0002 AC9 and a break tag together**, and nothing can. **Waived by ID: WI-0002 AC9.** What was checked instead: every `wi0001_ac<n>_` tag it depends on still resolves exactly once |
| AC10 | still true, **non-intersecting** | its subject is the suite's method names | **Nothing executable exercises WI-0002 AC10 and a break tag together. Waived by ID: WI-0002 AC10.** Checked instead: every `wi0002_ac1..10` tag still matches exactly one method after eleven `wi0003_` methods were added, and `test_wi0002_ac10_...` itself passes |

Three criteria — WI-0001 AC11, WI-0002 AC9 and WI-0002 AC10 — are waived by ID above. They are
the only three, and each is waived because it is a claim about the record or about test names, for
which "a covering case with a break tag" has no meaning. Every other one of the twenty-one has a
covering case that was run here.

## Gates

| gate | result | evidence |
|------|--------|----------|
| `tests-pass` | **pass** | `python3 -m unittest discover -s tests -t .` → `Ran 37 tests in 7.986s` / `OK`, exit 0, run by this skill on `a93db5f` |
| `lint-clean` | **pass** | `python3 -m compileall -q -x '(^\|/)\.claude(/\|$)' .` → exit 0 |
| `workspace-valid` | **pass** | `validate-workspace .` → `checked 4 item(s), 11 document(s)` / `0 errors, 0 warnings`, exit 0 |
| `every-criterion-independently-checked` | **pass** | each row of `## Criteria` names a command this skill ran and quotes its actual output. AC1 to AC9 were settled against inputs written here from the criteria's prose, not against the implementation's fixtures; the expected tables were extracted programmatically from `item.md` and `plan.md` |
| `negative-cases-exercised` | **pass** | see `## Negative and boundary cases exercised` — fourteen cases, each triggered |
| `a-criterion-about-criteria-is-read` | **pass** | `## AC10 — the twenty-one prior criteria, read by ID`: every ID named, a per-criterion verdict read from its text, evidence run for each, two non-intersections stated in those words and three criteria waived by ID |
| `tests-would-fail-without-the-change` (advisory) | **pass** | six mutations, each reverted — see `## Test sensitivity check` |

## Negative and boundary cases exercised

Every one was triggered, not read about. All exited 0.

| case | what happened |
|------|---------------|
| empty input | came back empty |
| prose containing `<br>` and `<br/>`, no table | byte-identical |
| a `> `-prefixed (blockquoted) table carrying `<br>` | byte-identical — never a candidate |
| a block whose lines' indents differ, carrying `<br>` | byte-identical |
| a cell whose **entire** text is `<br>` | exempt: `\| <br>   \|` beside `\| abcdef \|` |
| `<br`, `br>`, `< br >`, `<b r>` | none exempts; all four centred by the column's marker |
| `<br\t/>` — whitespace that is a tab | exempt (`\| <br\t/>   \|`); a centred non-exempt cell would have been `\|  <br\t/>  \|` |
| `freeze\`, `C:\dir\` — trailing backslashes | not exempt; centred. The backslash is also not read as escaping the closing pipe, because a space intervenes |
| a wholly empty left-marked column beside an exempt cell | `W` from the header only; empty cells `W + 2` spaces |
| an empty cell in each of a left-, right- and centre-marked column, beside `a<br>b` | each `W + 2` spaces, none exempted; output idempotent |
| a delimiter row whose cells contain `<br>` (`\|:-<br>-:\|-\|`) | not a delimiter row, so not a table: the block is copied whole. The delimiter row is unreachable by the exemption, not merely untouched |
| a table containing bytes that are not valid UTF-8, beside `a<br>b` | exit 0, `\xff\xfe` present in the output unchanged |
| a CRLF table with a break tag | all three composed lines keep `\r\n`; no line ending normalised |
| a table at end of file with no final newline, with a break tag | tidied, and did not gain a newline |

## Test sensitivity check

Six mutations, each applied to the branch head and reverted immediately afterwards. The working
tree was confirmed clean against `a93db5f` at the end.

| mutation | suite result | which criteria's tests caught it |
|----------|--------------|----------------------------------|
| delete the `has_break_tag` branch from `compose_row` | `FAILED (failures=5)` | WI-0003 AC1, AC3, AC6, AC9 |
| ADR-0009's refused option C — null a column's alignment when any cell carries a tag | `FAILED (failures=9)` | WI-0003 AC1, AC3, AC5, AC8, AC9, AC10 |
| widen `_BREAK_TAG` to bare `br` | `FAILED (failures=7)` | WI-0003 AC2, AC9, and the untagged predicate test |
| make an unmarked column centre instead of left | `FAILED (failures=11)` | WI-0003 AC4 and AC9, plus WI-0001 AC1/AC3/AC4/AC5/AC7 and WI-0002 AC1–AC4 |
| drop the leading colon from `compose_delimiter` | `FAILED (failures=51)` | WI-0003 AC1, AC2, AC3, AC5, AC7, AC8, AC9, AC10, plus WI-0002 AC7 |
| rename `test_wi0003_ac6_...` out of ADR-0006's convention | `FAILED (failures=1)` | WI-0003 AC11 |

Every one of AC1 to AC11 has at least one mutation that makes its own named test fail. AC4 and
AC7 are negative criteria — they assert that something did **not** change — so the mutation that
catches each is one that changes the thing they protect, not one that removes the exemption.

Separately, and independently of the suite, this skill wrote three **discriminating cases** because
AC3, AC5 and AC8 quote tables whose exempt cells are their columns' widest, making those three
tables equally the output of a filter with no exemption:

| claim | input | output | what it would be with no exemption |
|-------|-------|--------|-------------------------------------|
| AC3 — the exemption reaches a **header** cell under a right marker | `\|k\|hd<br>r\|` / `\|:-\|-:\|` / `\|1\|abcdefghij\|` | `\| k \| hd<br>r    \|` | `\| k \|    hd<br>r \|` |
| AC5 — an exempt cell **narrower** than its column is padded on the right | Task/Notes with `a<br>b` beside `abcdefghij`, centre-marked | `\| deploy \| a<br>b     \|` | `\| deploy \|   a<br>b   \|` |
| AC8 — an exempt cell in an **indented** table is laid out left | three-space-indented, `d<br>t` beside `abcdefgh`, centre-marked | `   \| one  \| d<br>t   \|` | `   \| one  \|  d<br>t  \|` |

All three produced the exempt layout. `impl-report.md` had already declared the AC3 and AC5 cases
and added an equivalent assertion to AC3's test; these were derived and run here independently.

## Defects found

None. No send-back, and no bug item filed.

The diff `main..a93db5f` was read against `plan.md`. `mdtab.py` carries exactly plan steps 1 to 4
— the pattern, the predicate, the one branch, two docstrings — and nothing else; `column_alignments`,
`emit_block`, `split_cells`, `table_or_none`, `column_widths` and `compose_delimiter` are byte-for-byte
unchanged. In `tests/test_mdtab.py` the only removed lines are three docstring lines; no existing
assertion was deleted, weakened or renamed. The sixteen fixture files are plan step 5's list exactly.
The two additions beyond the plan's letter — AC3's extra assertion and the `INPUT_FIXTURES`
extension — are both declared in `impl-report.md` and both trace to a criterion (AC3 and AC10
respectively).

## Not verified, and why

- **That the six spellings in AC1 and the five texts in AC2 are an adequate sample of ADR-0008
  decision 1's rule.** The rule is a pattern and a test can only exercise finitely many strings.
  This verification added four more near-misses (`<br`, `br>`, `< br >`, `<b r>`), one tab form
  (`<br\t/>`) and one whole-cell form (`<br>`), all behaving as ADR-0008 says — but the sample is
  still a sample. `plan.md` records this as an assumption and it remains one.
- **The behaviour of an exempt cell that also contains an escaped pipe (`\|`).** Deliberately
  unconstrained by this item: how `\|` is measured and re-emitted is WI-0001's open design
  question and is still unanswered. Nothing was asserted about it here, and nothing in this item
  depends on it.
- **Anything about how a renderer displays the result.** No criterion of this item renders a
  table, and none was rendered.
- **Performance.** No criterion states a throughput or latency requirement, and none was measured;
  `ADR-0009` decision 4 records that compiling the pattern once is a preference, not a measurement.

---
id: WI-0004
type: work-item
title: Import expenses from a bank CSV export
status: done
priority: medium
epic: EP-001
branch: wi/WI-0004
outcome: delivered
created: "2026-08-21T21:07:03Z"
updated: "2026-08-21T23:57:05Z"
---

## Story

As the person keeping the group's books, I want to feed my bank's CSV export into the tool and
have it create expenses, so that I stop retyping transactions I have already been charged for.

## Acceptance criteria

Every criterion is checked from the repository root against `$T`, a data file that does not exist
when the criterion starts (ADR-0004), with `Ana`, `Ben` and `Cass` registered first by
`./expenses add-person … --data-file "$T"` (WI-0001). An expense is **rendered** in the single form
WI-0002 fixed, and an imported one is rendered identically:

```
<YYYY-MM-DD> <amount> <description> — paid by <payer>, shared by <sharer>, <sharer>, …
```

**The import learns the file's shape from the command line** rather than knowing any bank's layout
in advance. The stakeholder chose that in WI-0004/Q-006: *"Let's do C — build it against the columns
I name now, and I'll still send the sample when I get to it so you can add the shortcut for my bank
later. Typing four options each time is fine."* So the criteria below are checked against `$F`, a
file the checker writes, containing exactly:

```
Transaction Date,Amount,Description,Balance
14/08/2026,30.00,Dinner at Luigi,1200.00
02/08/2026,9.00,Taxi home,1230.00
```

and `$M` stands for the four options that describe that file:

```
--date-column "Transaction Date" --amount-column Amount --description-column Description --date-format "%d/%m/%Y"
```

`$F` is **not** a claim about the stakeholder's bank, and nothing here depends on one. It is an
example file the criteria carry with them, which is precisely what the chosen route makes possible:
the tool holds no assumption about any bank, so no bank needs to be known to check it. `Balance` is
in the file to make "a column nobody named is ignored" checkable. When the sample eventually arrives
it becomes a *shortcut* for `$M`, filed as a new item — not a change to these criteria.

Three reading conventions apply throughout and are checked by AC11: the file is parsed as RFC 4180
CSV, every cell is used with leading and trailing whitespace removed, and a leading UTF-8
byte-order mark is ignored. **A line number** in any message below is the line's 1-based position in
the file, so the header is line 1 and the first data row is line 2.

- [x] AC1 — the import reads the file through the columns named on the command line and records one
      expense for each accepted row.
      `./expenses import-csv "$F" --paid-by Ana --shared-by Ana,Ben,Cass $M --data-file "$T"` prints
      exactly these two lines on stdout, in the order the rows appear in the file, prints nothing on
      stderr, and exits 0:
      `Imported 2026-08-14 30.00 Dinner at Luigi — paid by Ana, shared by Ana, Ben, Cass` then
      `Imported 2026-08-02 9.00 Taxi home — paid by Ana, shared by Ana, Ben, Cass`. Column names are
      matched against the header line exactly as written after trimming; a column nobody named
      (`Balance`) is ignored. `--date-format` is a Python `strptime` format string. Neither the tool
      nor these criteria know anything about any bank's export (WI-0004/Q-006, option C)
- [x] AC2 — each imported expense carries the date from **its own row**, parsed with the stated
      `--date-format`, and not the date of the import: after AC1's import,
      `./expenses list-expenses --data-file "$T"` prints exactly
      `2026-08-02 9.00 Taxi home — paid by Ana, shared by Ana, Ben, Cass` and then
      `2026-08-14 30.00 Dinner at Luigi — paid by Ana, shared by Ana, Ben, Cass` — date order per
      WI-0002 AC3 — and prints the same two lines whatever `date +%F` says on the machine running it
      (WI-0002/Q-002)
- [x] AC3 — an imported expense is indistinguishable from a hand-entered one to everything
      downstream. Build a second data file `$U` by hand: register the same three people, then
      `./expenses add-expense --paid-by Ana --amount 30.00 --description "Dinner at Luigi"
      --shared-by Ana,Ben,Cass --date 2026-08-14 --data-file "$U"` and the same for
      `--amount 9.00 --description "Taxi home" --date 2026-08-02`. Then
      `./expenses list-expenses --data-file "$T"` and `--data-file "$U"` produce **byte-identical**
      output, and so do `./expenses report --data-file "$T"` and `--data-file "$U"`; `diff <(…) <(…)`
      is empty and both exit 0. The two *data files* are not compared and are not expected to match:
      the imported ledger additionally remembers the file it imported (AC7)
- [x] AC4 — a row the tool cannot turn into an expense is reported on stderr and does not stop the
      remaining rows. With `$G` containing exactly:
      `Transaction Date,Amount,Description,Balance` / `14/08/2026,30.00,Dinner at Luigi,1200.00` /
      `30/02/2026,12.00,Bad date,1188.00` / `02/08/2026,9.00,Taxi home,1230.00` (one per line),
      importing `$G` with `$M` prints the two `Imported …` lines of AC1 on stdout, prints exactly
      `Skipped line 3: 30/02/2026,12.00,Bad date,1188.00` on stderr — the raw line as it appears in
      the file, without its terminator — and **exits 0**, because the import as a whole succeeded and
      a skipped row is a report, not a refusal (ADR-0005 clause 2 and its note about partial
      imports). A row is unusable when, and only when: its **amount** cell is not a positive number
      with at most two decimal places (WI-0002 AC5's rule, so an empty, zero, negative or
      non-numeric amount is skipped); its **date** cell does not parse under the stated
      `--date-format`; its **description** cell is empty or blank; or the row has fewer cells than
      the header. It follows that a `--date-format` matching no row — including one that is not a
      valid `strptime` format at all — skips every row, prints one message per row, imports nothing
      and still exits 0. Treating a row that is not a positive charge as a skip rather than as a
      refund is an **assumption** the stakeholder can correct (WI-0004/Q-006, option B's stated open
      point); it is deliberately the same handling any other unusable row gets, so correcting it
      later changes one rule and not the shape of the command
- [x] AC5 — a file the named columns do not describe is refused before any row is read: for `$F`,
      passing `--amount-column Value` in place of `--amount-column Amount` prints exactly
      `Column not found in <FILE>: Value` on stderr — `<FILE>` being the path as typed — prints
      nothing on stdout, exits 1, records nothing, leaves `$T` byte-for-byte unchanged, and prints
      no Python traceback. When more than one named column is absent, the one reported is the first
      missing in the order date, amount, description. A zero-byte file is refused the same way with
      exactly `<FILE> has no header line`. A file with a header and **no data rows** is not an
      error: it imports nothing, prints exactly `No rows imported from <FILE>` on stdout and exits 0
      (ADR-0005 clause 4). An import that records **no** expenses — whether from no data rows or
      because AC4 skipped them all — is not remembered as an import, so re-running it does not
      trigger AC7's warning
- [x] AC6 — the import command takes the payer and the sharers as arguments and applies them to
      every row it accepts, exactly as `add-expense` does:
      `./expenses import-csv "$F" --paid-by Ana --shared-by Ana,Ben,Cass $M`. Omitting `--shared-by`
      shares each imported expense among everyone registered at the moment of the import, and stores
      that list explicitly on each expense, matching WI-0002 AC2 and ADR-0009 clause 3. Naming a
      payer or a sharer who is not registered prints exactly `Unknown person: <name>` on stderr,
      exits 1, and imports **nothing** — the check happens before any row is read (WI-0004/Q-001).
      When several named people are unregistered, `<name>` is the first of them in the order payer,
      then sharers left to right, matching WI-0002 AC4's single-name message
- [x] AC7 — importing a file whose contents have been imported before does not silently duplicate
      anything. Run AC1's import twice: the second run prints exactly
      `This file was already imported on <D>. Pass --again to import it anyway` on stderr, where
      `<D>` is the `date +%F` of the first run, prints nothing on stdout, imports nothing and exits 1
      (ADR-0005 clause 2). Adding `--again` imports it regardless: the two `Imported …` lines print,
      it exits 0, and `list-expenses` then shows four lines. "Already imported" is a property of the
      file's **contents** and of nothing else: `cp "$F" "$F2"` and importing `$F2` warns the same
      way; a copy of `$F` with one row added or changed is a new file and imports normally; and
      importing `$F` again under a **different but valid** mapping — say
      `--description-column Balance` — still warns, because the mapping is not part of the file's
      identity. When a file has been imported more than once, `<D>` is the date of the most recent
      import. Passing `--again` for a file that has **not** been imported before is not an error and
      not a warning: it is an ordinary import, so a user who always passes it never sees AC7 at all
      (WI-0004/Q-003)
- [x] AC8 — a file that does not exist, or that cannot be read, is refused with a message on stderr
      that names the path as typed, exit 1, no Python traceback, and `$T` byte-for-byte unchanged —
      the same shape as an unreadable data file in WI-0001 AC8. A file whose bytes are not valid
      UTF-8 is "cannot be read" and is refused this way rather than being parsed with substitutions
- [x] AC9 — the data file is left byte-for-byte unchanged by every refusal above (AC5, AC6, AC7
      without `--again`, AC8, AC10): `cmp` against a copy taken before the command exits 0 in each
      case. A successful import reaches the data file through the store's atomic save and through
      nothing else (ADR-0006 clause 5), so an interrupted import cannot leave a half-imported
      ledger; checkable by inspection — no module this item adds opens the data-file path for
      writing
- [x] AC10 — all four mapping options are required on every import: omitting any one of
      `--date-column`, `--amount-column`, `--description-column` or `--date-format` exits 2, prints
      a message on stderr, prints nothing on stdout and records nothing. There is no default column
      name, no built-in layout for any bank, and no remembered or file-based mapping — the
      stakeholder accepted the typing when they chose option C over option D: *"Typing four options
      each time is fine"* (WI-0004/Q-006)
- [x] AC11 — the three reading conventions above hold. With `$H` containing exactly
      `Transaction Date,Amount,Description,Balance` and
      `14/08/2026, 30.00 ,"Dinner, drinks and a taxi",1200.00` (one per line), importing `$H` with
      `$M` records exactly one expense and prints
      `Imported 2026-08-14 30.00 Dinner, drinks and a taxi — paid by Ana, shared by Ana, Ben, Cass`:
      the quoted field is read whole rather than split on its comma (RFC 4180), and ` 30.00 ` is a
      valid amount because cells are trimmed. Prefixing `$H` with a UTF-8 byte-order mark
      (`printf '\xef\xbb\xbf' | cat - "$H" > "$H2"`) changes nothing: importing `$H2` prints the
      same line, rather than failing to find the `Transaction Date` column

## Out of scope

- Any statement format other than the CSV export named in Q-001: no PDF, no OFX, no QIF, no
  connection to the bank.
- Working out from the file who shared in a row. The stakeholder chose to state the payer and the
  sharers themselves at import time (WI-0004/Q-001), so the tool does not guess them from a
  merchant name, a category, or anything else in the row. A file that mixes group spending with
  personal spending is split by hand before importing; the tool offers no interactive per-row
  prompt and no proposed-expenses file to edit.
- Detecting that an individual *row* has already been imported and skipping it. Duplicate
  detection is per **file** and nothing finer: two different files that happen to share a row both
  import that row, and the tool does not notice. Re-importing the same *file* is settled by AC7 —
  the stakeholder chose to be warned and to have to confirm (WI-0004/Q-003) — but a row-level
  merge is a different feature and is not in this item.
- Any built-in knowledge of a particular bank's export. The tool contains no default column
  names, no per-bank layout table and no auto-detection: every fact about the file comes from the
  four options the stakeholder types (AC1, AC10). A named shortcut for their own bank — the second
  half of their answer to Q-006, *"I'll still send the sample when I get to it so you can add the
  shortcut for my bank later"* — is a **new item**, filed when the sample arrives, and nothing in
  this item is thrown away when it is.
- Remembering the mapping between imports, in a config file or in the data file. Option D offered
  exactly that and the stakeholder chose C instead: *"Typing four options each time is fine"*
  (Q-006). AC10 makes the four options required, so this is a refusal to build something, not an
  omission.
- Treating a row that is not a positive charge — a refund, a credit, a "money in" column — as
  anything other than a skipped row (AC4). Recognising refunds is a feature about what an expense
  *is*, and this epic has no notion of negative expenses at all.
- Categorising or classifying transactions.
- Exporting anything back out to CSV.
- Importing into anything but the current group. `--data-file` chooses the ledger, as everywhere
  else; there is no per-import destination and no merging of two ledgers.
- Reading the payer or the sharers from the file, or varying them per row. One `--paid-by` and one
  `--shared-by` apply to every row in the import (AC6), which is what the stakeholder asked for.
- Any date option on the import. Each imported expense takes the date from its own row (AC2), so
  `--date` is deliberately **not** offered: an option that overrode every row's date with one value
  would throw away the information the import exists to keep.

## Notes

WI-0004/Q-001 asked two things and came back half answered.

- **Answered — how a row becomes an expense.** The stakeholder chose option B: "let me say who
  paid and who was in on it when I import, same idea as adding one by hand." AC6 above states it,
  including the default of "everyone registered" when the sharers are omitted, which is the
  behaviour WI-0002 AC2 already gives a hand-entered expense.
- **Not answered — what the file looks like.** "I'll send you a sample later, don't have it to
  hand right now." No column names, no date format, no sign convention, no statement about a
  preamble before the header row. This is a fact only the stakeholder has, and it is **still
  unknown today** — the difference, since Q-006 was answered, is that nothing depends on it any
  more: the tool asks for the shape at import time instead of knowing it.

**WI-0004/Q-002 re-asked the missing half, and the stakeholder answered it twice over.** They still
do not have the sample — "I'll send you a sample later, still haven't got to it" — and they closed
off the way out that the question offered:

> "And no — the import stays part of this, it doesn't get dropped or pushed to a later epic. Build
> it last if that's easiest, but I'm not signing off on a version without it."

That is a scope decision, and it binds three things:

1. **Option C is dead.** WI-0004 is not dropped, not deferred to a later epic, and not closed with
   an outcome of `dropped`. It stays a child of EP-001.
2. **EP-001 cannot close without it.** The epic's Definition of Done requires every child `done`,
   and the stakeholder has said in their own words that a version without the import is not one
   they will sign off. `tracker/items/EP-001/item.md` records this.
3. **Last is fine.** "Build it last if that's easiest" confirms the delivery order already set in
   EP-001/Q-001, which the `priority: medium` on this item executes. Nothing needs to change to
   honour it.

That paragraph stood for four askings, and it was true until Q-006 was answered. What has changed
since is only the *last* of the three bindings' consequences: AC1, AC2 and AC5 no longer depend on
the file's shape being known in advance, because the stakeholder chose to state it at import time
instead. All three bindings above are untouched — the import is still not dropped, EP-001 still
cannot close without it, and it is still last in the order.

**WI-0004/Q-003 is answered: a repeat import is warned about and has to be confirmed.** The
stakeholder chose option C — "I don't want it silently doubling up — warn me if I'm importing the
same file again and make me confirm if I really mean it." AC7 states it. Two consequences for
`plan`:

- **The data file has to remember which files have been imported**, and when. That is new stored
  state, beyond people and expenses, and it is the first requirement in this epic that is not
  derivable from the expenses themselves. What identifies a file — a hash of its contents is the
  obvious candidate, and AC7's wording ("a property of the file's contents") requires something of
  that kind rather than a path — is `plan`'s to choose and to record.
- **`--again` is a confirmation flag, not a force flag.** It changes nothing else: the same rows
  are imported the same way, and the duplicate expenses are real expenses that the report will
  count twice. Since EP-001 excludes deleting an expense, that is the point at which the
  stakeholder's own confirmation is the only safeguard, which is why AC7 requires the message to
  say *when* the file was imported before.

**WI-0004/Q-006 is answered, and it is the answer that unblocks this item.** Asked whether they
would rather keep waiting for the sample or have the tool take the file's shape from them at import
time, the stakeholder chose option C:

> "Let's do C — build it against the columns I name now, and I'll still send the sample when I get
> to it so you can add the shortcut for my bank later. Typing four options each time is fine."

What that settles, and what it does not:

1. **The three blocked criteria are unblocked, not relaxed.** AC1, AC2 and AC5 are rewritten above
   against the columns named on the command line. Nothing about any bank was invented to do it —
   which was the whole point of the route, and why it does not breach the standing instruction from
   Q-004 (*"I'd rather you wait for my actual file than guess at the format"*). There is no guess in
   the tool because there is no bank in the tool.
2. **Option D is refused explicitly.** *"Typing four options each time is fine"* chooses the command
   line over a config file, so AC10 makes all four options required and the out-of-scope list
   refuses a remembered mapping. `plan` does **not** need to decide this; it is decided.
3. **The sample is still wanted, and is no longer blocking.** It buys a named shortcut for their
   bank, which is a **new item** filed when it arrives, not a change to these criteria and not a
   reason to hold this one. Nobody needs to ask for it again: they said they will send it.
4. **One assumption is recorded rather than decided by them.** A row that is not a positive charge
   is skipped and reported by line number, exactly as any other unusable row (AC4). The question
   flagged this as the one thing option B/C left open, and the stakeholder did not overturn the
   proposal, so it stands as an assumption they may correct — recorded in
   `artifacts/refinement-qa.md` as `[assumed]`, not as something they said.

**This item returns to `draft` and `refine` should now be able to carry it to `ready`.** The
sixth-asking instruction that used to sit here is spent: the question was asked, it was answered,
and the answer removes the dependency it was chasing. What `refine` must still do is the ordinary
job — judge every criterion above against the Definition of Ready, tighten the wording it thinks is
loose, and record what it assumes. Two constraints on that pass survive from the earlier ones and
are the only ones that do:

1. **Still do not invent a bank format.** The route the stakeholder chose works precisely because
   nothing about their export is written down anywhere in the tool or in these criteria. `$F` in
   the criteria above is an example file the checker writes, and it must stay labelled as one. If a
   future reader can mistake it for the stakeholder's real statement, the wording is wrong.
2. **Do not re-ask for the sample.** It is no longer blocking anything, and they have said they
   will send it. Asking again would spend their attention on a shortcut nobody is waiting for.

A stale sentence stood here saying that re-importing the same file was "still undecided and is
also `refine`'s". It was already wrong: Q-003 settled it and AC7 states it. Removed rather than
left, because a note claiming an open decision is exactly the kind of thing a later reader acts on.

This item's priority was lowered from `high` to `medium` when EP-001/Q-001 was answered. The
stakeholder put the report first — "get me the report working first — that's the bit I actually
asked for. Import can come after" — and the orchestrator reads the priority field as intent, so
the intent is written into the field rather than left to the tie-break that happened to produce
the same order.

### Decided during refinement, and by whom

`refine` fixed everything that does not depend on the bank's format. All are recorded as
`[assumed]` in `artifacts/refinement-qa.md`, resting on the conventions the stakeholder delegated
for WI-0001 (Q-004) and that `answer-questions` recorded as ADR-0002 and ADR-0005.

- **The command is `./expenses import-csv <FILE>`**, the name ADR-0002 clause 3 reserved, with the
  file as a positional argument and `--paid-by`, `--shared-by`, `--again` and `--data-file` as
  options. `--paid-by` and `--shared-by` are the spellings WI-0004/Q-001's answer already fixed.
- **A skipped row exits 0 and a rejected file exits 1** (AC4 versus AC5). ADR-0005 clause 2 makes a
  refusal exit 1 and store nothing; a partial import is not a refusal — most of the file was
  imported — so the import as a whole succeeded and says what it skipped. ADR-0005's own
  consequences note flags this case as the one needing care, and this is the decision it asked for.
- **A skipped row is named by line number and quoted**, so that the stakeholder can find it in the
  file. "Reported to the user, naming the row" was previously unmeasurable.
- **AC7's message names the date of the earlier import** and tells the user the flag that overrides
  it. A warning that does not say how to proceed makes the user guess.
- **`--date` is deliberately not offered**, and is now out of scope: every imported expense takes
  its row's date, and an option that overrode all of them would discard exactly what WI-0002/Q-002
  was answered to preserve.
- **AC8 and AC9 are new.** A missing file and an unreadable one are the first thing anyone hits,
  and nothing said what happens; and the atomicity of the write matters more here than anywhere
  else in the epic, because an import creates many expenses at once.

### Decided by this refinement pass, once the sample stopped mattering

Everything below is `refine`'s, recorded `[assumed]` in `artifacts/refinement-qa.md`, resting on the
conventions the stakeholder delegated for WI-0001 (Q-004) and on the criteria WI-0001 to WI-0003
already fixed. None of it was put to the stakeholder: each is either a mechanical consequence of a
decision they already made, or a detail of wording that has to be pinned for `verify` to have
anything to check.

- **The exact output of a successful import.** `Imported ` followed by WI-0002's rendered form, one
  line per accepted row, in file order, and nothing else on stdout. Chosen to match `add-expense`'s
  `Added <rendered>` rather than to invent a summary line; AC3 then reduces to comparing two
  ledgers' output, which is a stronger check than any wording could be.
- **The exact form of a skipped-row message.** `Skipped line <N>: <raw line>`, with line 1 being the
  header. "Reported to the user, naming the row" was previously unmeasurable, and the raw line is
  what lets the stakeholder find it in a file their editor has open.
- **What makes a row unusable**, exhaustively, in AC4. Previously the phrase "a row the tool cannot
  turn into an expense" defined itself. The four cases reuse WI-0002's own rules rather than adding
  any, which is why an imported expense and a typed one cannot differ.
- **A wrong `--date-format` skips every row and exits 0.** Falls out of AC4 rather than being a
  separate rule. Recorded because it is the most likely thing to go wrong in real use, and a reader
  should not have to derive it.
- **Which name a refusal reports when several are wrong** (AC6), and **which column** (AC5). Both
  were ambiguous; both are now a stated order. Neither constrains anything a user would notice
  except reproducibility, which is exactly what `verify` needs.
- **An import that records nothing is not remembered** (AC5), so a file that produced no expenses
  can be retried without `--again`. The alternative — remembering it — would make an empty import
  permanently poison a filename's contents, which is a trap for no benefit.
- **`--again` on a never-imported file is an ordinary import** (AC7), so a user who puts it in a
  shell alias never sees the duplicate warning. Stated rather than left, because the opposite
  reading — an error, "you passed --again but there was nothing to override" — is equally plausible
  and would be discovered only by hitting it.
- **The mapping is not part of a file's identity** (AC7). Duplicate detection is about contents, and
  two imports of the same statement under different column names would still double every expense.
- **RFC 4180 parsing, trimmed cells, and a BOM ignored** (AC11). All three are properties of real
  CSV exports rather than of any particular bank: quoted fields containing commas are ubiquitous, a
  leading BOM is what a spreadsheet writes, and untrimmed cells are what everything writes. Getting
  the BOM wrong would fail with "column not found" on a file that plainly contains the column, which
  is the worst kind of error message.
- **A file that is not valid UTF-8 is refused, not repaired** (AC8). Consistent with ADR-0005's
  refusal convention and with the epic's rule that nothing is silently altered.
- **Atomicity is checked by inspection** (AC9), not by racing the process. The observable claim is
  that no module this item adds writes the data file directly; ADR-0006 clause 5 supplies the rest.

### No longer blocked, and how that happened (R4)

**This section used to say that AC1, AC2 and AC5 could not pass the Definition of Ready until the
stakeholder supplied the header line and a representative row of their bank's CSV export. That is no
longer true, and the history is worth keeping because it is the reason the criteria look the way
they do.**

The sample was asked for five times and deferred five times — Q-001 (answered in part), Q-002
(*"still haven't got to it"*), Q-004 (*"I'd rather you wait for my actual file than guess at the
format"*), and Q-005, which reduced the ask to the header line and a *single* real row, or simply
the file's path, and got the same answer again. Reducing the ask changed nothing, which is evidence
that the obstacle was never the size of the ask, so a sixth identical asking had no reason to
succeed.

**Q-006 asked something different and it worked.** Rather than re-ask, it offered a route that
guesses nothing: the tool takes the file's shape from the stakeholder at import time. They chose it
(option C) and added that the sample will still come, for a shortcut later. So:

- AC1, AC2 and AC5 are decidable now, against `$F` — an example file the criteria carry with them
  and label as an example — instead of against a file nobody has seen.
- **No format was invented, and none may be.** The prohibition stands exactly as strongly as before;
  it simply no longer blocks anything, because the chosen route needs no format to be known. An
  importer written against a plausible layout would parse a file that does not exist, and AC5 would
  be checking an invention against itself. That is still true and still forbidden.
- The stakeholder's instruction to wait rather than guess (Q-004) was honoured to the end: nothing
  was built while the wait was on, and what ended the wait was their decision, not ours.

**EP-001 is no longer blocked on a fact only the stakeholder holds.** The epic's own notes recorded
that it could not close until the sample arrived; that dependency is gone, and `EP-001/item.md` has
been amended to say so.

### Accepted at closure, and still open (review-close)

Five gaps were declared by `verify` and accepted by `review-close` rather than fixed. They are here
rather than only in `artifacts/verify-report.md` and `artifacts/review.md`, because once an item is
`done` nobody reads its verification report again.

- **AC7's "most recent import date" is not demonstrated end to end.** Every import in one session
  happens on one day, so the CLI cannot distinguish the last matching record from the first. The
  rule is covered by `tests/test_store.py::ImportedFiles::test_imported_on_returns_the_last_matching_date`.
- **Atomicity was checked by inspection, not by interruption.** AC9 asks for the inspection and it
  passes — `bankcsv.py` contains no write of any kind. Killing the process mid-write would test
  `store.save`, which is WI-0001's code and unchanged by this item.
- **Nothing was tested against the stakeholder's real bank export**, because nobody has it and, by
  their own decision in Q-006, nothing depends on it. The two likeliest surprises are a quoted
  thousands separator (`"1,200.00"`) and charges written as negative amounts. Both are skipped and
  reported under AC4 rather than silently mishandled, so the failure is safe and visible. If either
  turns up when the sample arrives, it is a **new criterion**, not a defect in this item.
- **A failing `store.save` still raises a Python traceback out of `main()`** — for `import-csv`
  exactly as for every other command in the tool. Pre-existing, covered by no criterion of any item,
  and not filed as a bug because `pipeline.yaml` permits `null → ready` for actor `verify` only, so
  `review-close` cannot create a bug item without forcing a gate override.
- **No test protects `README.md`.** `grep -rn "README" tests/` finds one comment and nothing else.
  This item was rejected once for a README that said the CSV import was "the next piece of work"
  three commits after it shipped, and fixing the file does not remove the exposure: the same class
  of defect can recur silently, because every automated gate this project has will stay green while
  it does. Whoever adds the next command should expect to update `README.md` by hand and should
  expect nothing to remind them.

### Left deliberately unconstrained (R10)

Left by `refine`, recorded so the gaps are visible rather than absent. None of them is depended on
by any criterion above.

- **`argparse`'s usage-error wording**, as on every other item; AC10 fixes only exit code 2 and that
  stderr is not empty.
- **How many skipped rows are reported.** AC4 requires each skipped row to be named and states what
  happens when every row is skipped, but nothing caps the output for a file of ten thousand
  unusable rows and nothing summarises. If that turns out to matter it is a new criterion rather
  than a defect.
- **What the tool remembers about a previous import beyond its fingerprint and its date.** AC7 needs
  those two and AC7's wording ("a property of the file's contents") rules out identifying a file by
  its path; how the fingerprint is computed, and whether the store also records the file's name, its
  row count or the people used, is `plan`'s to decide.
- **A header line containing the same column name twice.** Nothing says which of the two the tool
  reads. Left because no criterion depends on it and a bank export with duplicate headers is not a
  case anyone has reported.
- **How stdout and stderr interleave when a file both imports and skips rows** (AC4). The criteria
  check each stream separately, so any interleaving passes; nothing requires the skip message to
  appear before or after the `Imported …` lines of neighbouring rows.
- **Whether the file is read once or twice** — fingerprinting for AC7 and parsing for AC1 could be
  one pass or two. `plan`'s choice; no criterion can tell the difference.

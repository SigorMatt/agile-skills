# Refinement Q&A — WI-0001

The exchange that refined this item, in order, verbatim. It did not happen in a conversation: the
stakeholder is asynchronous, so `refine` filed four questions as artifacts
(`questions/Q-001.md` to `Q-004.md`), the stakeholder wrote their answers into those files between
sessions, and `answer-questions` propagated them. The questions and answers below are copied from
those files without alteration; the full context and options each question offered are in the
files themselves.

Tags: `[human]` — the stakeholder said this. `[assumed]` — `refine` proposed it and the
stakeholder deferred to us, or it follows from a decision they delegated. `[unresolved]` — asked
and not settled.

---

## Q1 (Q-001) — What is the tool called, and how do you want to invoke it — specifically, what exact words add a person and what exact words list the people?

Asked because AC1, AC3 and AC4 said "a documented command", which nobody can run (R4). Options
offered: A, `python3 expenses.py …`; B, `expenses …` from `PATH`; C, short subcommands
(`expenses add`, `expenses people`). Recommendation: B.

**Answer [human]:** "Whatever you think is best, honestly — you know this better than I do."

**Answer [assumed]** — the substance, decided by the architect under that delegation and recorded
as ADR-0002: one executable file named `expenses` at the repository root, invoked
`./expenses <subcommand>` in every criterion, with the `PATH` install documented as an optional
convenience. Subcommands are verb-noun: `add-person`, `list-people`. This is a variant of the
recommended option B — B as written would have made every criterion depend on an install step
that `verify` cannot perform or ask about.

---

## Q2 (Q-002) — When should two spellings count as the same person, and which names should the tool refuse to register outright?

Asked because AC3 forbade a second entry for a name "already registered" without defining it, and
because the item's own story is about a typo not creating a fourth person. Options offered: A,
exact match; B, trim and case-fold, refusing blank and comma-containing names; C, B plus accent
and internal-whitespace folding. Recommendation: B.

**Answer [human]:** "Use your judgement on the exact rule — just make sure a typo like 'ana' vs
'Ana' doesn't quietly create a second person."

That sentence is binding and eliminates option A. The rest was delegated.

**Answer [assumed]** — option B, recorded as ADR-0003: compare trimmed and case-folded, store and
display the name as first typed, refuse names that are empty, whitespace-only or contain a comma.
Option C was declined because merging two genuinely distinct people cannot be undone in an epic
with no editing or deleting.

---

## Q3 (Q-003) — Where should the data file live by default, and should a single run be able to use a different file?

Asked because AC2 and EP-001 SM2 require the data to survive a restart, while EP-001's scope said
only "a file inside the project or the user's home directory". Options offered: A, one fixed path;
B, a default plus a per-run override; C, a file in the current directory. Recommendation: B.

**Answer [human]:** "A file on my laptop is fine — I don't want a server, an account, or anything
in the cloud. The exact location and whether you can point it elsewhere for a run is your call."

**Answer [assumed]** — option B, recorded as ADR-0004: `~/.expenses.json` by default,
`--data-file PATH` for one run, a non-existent file treated as an empty store. The override is
load-bearing rather than convenient: every EP-001 success measure starts "from an empty data
store", so without it the tool could only be checked by writing to the stakeholder's real ledger.

---

## Q4 (Q-004) — For each of these four cases, what should the tool print, on which stream, and what should it exit with — (i) adding a new person; (ii) adding someone already registered; (iii) listing when several people are registered; (iv) listing when nobody is?

Asked because AC3's "says so" and AC4's "a message saying so" name no output and no exit code, and
`verify` may not ask anyone anything. Options offered: A, quiet on success; B, confirm everything
and treat a duplicate as harmless; C, confirm everything but a duplicate is an error.
Recommendation: C, with alphabetical listing.

**Answer [human]:** "Whatever you think is best here — this is exactly the kind of thing I'm
paying you to decide."

**Answer [assumed]** — option C, recorded as ADR-0005 and generalised to every command in the
epic: confirmation on stdout with exit 0; a refusal on stderr with exit 1 and nothing stored;
`argparse`'s exit 2 for a usage error; "nothing to show" on stdout with exit 0; listings ordered
by the trimmed case-folded name.

---

## Decided at refinement, under the delegation in Q4

These were not put to the stakeholder again. Each is a detail an ADR left at the level of a
convention, and a criterion cannot be checked against a convention.

- **[assumed] The exact refusal messages.** `A person's name cannot be blank` for an empty or
  whitespace-only name; `A person's name cannot contain a comma` for a comma. `Added Ana`,
  `Ana is already registered` and `No one is registered yet` come from Q4's own options, which the
  stakeholder was shown.
- **[assumed] `--data-file` is written after the subcommand** — `./expenses add-person Ana
  --data-file "$T"`. ADR-0004 requires every subcommand to accept it; the position is `argparse`
  mechanics, and the criteria need one form to be runnable.
- **[assumed] An unreadable data file is refused, not overwritten (AC8).** Nothing in the record
  said what happens when the file exists but is not the tool's format. The natural implementation
  overwrites it, which would destroy a ledger that this epic gives no way to rebuild, so AC8
  requires a message on stderr, exit 1, and the file left byte-for-byte unchanged.
- **[assumed] AC7 does not quote the default filename.** It requires exactly one new file directly
  in `$HOME` at the path the README documents. ADR-0004 clause 4 leaves the storage format — and
  therefore the extension — to `plan`, and a criterion that quoted `~/.expenses.json` would be
  invalidated by a legitimate design choice.

## Left unconstrained

- **[unresolved] The wording of a usage error** (unknown subcommand, missing name, extra
  argument). The exit code is fixed at 2 by ADR-0005 clause 3; the text is `argparse`'s and no
  criterion checks it. Left so by `refine`.
- **[unresolved] A `--data-file` path that cannot be created or written** — an unwritable
  directory, or a path that is a directory. ADR-0005 clause 2 says what it should look like and
  `plan` may implement exactly that, but no criterion checks it: reproducing it needs a
  permission-controlled fixture, and the documented default cannot hit it. Left so by `refine`.

Both are carried into the item's `## Notes` under "Left deliberately unconstrained (R10)".

## Override

None. No Definition of Ready criterion was overridden, and the stakeholder was not asked to
override one.

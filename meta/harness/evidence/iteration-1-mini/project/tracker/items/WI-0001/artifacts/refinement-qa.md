# Refinement Q&A — WI-0001

Every question asked and every answer received, in order, verbatim, tagged `[human]`,
`[assumed]` or `[unresolved]` per the `refine` procedure step 7.

**No answers have been received.** The stakeholder is asynchronous and was not in this session
(`SIMULATION-NOTICE.md`), so `refine` could not hold the conversation its procedure calls for.
Its precondition 2 covers exactly this case: file a question addressed to `human`, suspend the
item with `resume-to: draft`, stop. Both questions below are therefore `[unresolved]`, and
nothing has been written into `item.md` on their account. When they are answered,
`answer-questions` propagates the answers into `item.md` and appends the answers here, and this
item returns to `draft` for a second `refine` pass.

## Q1 — What identifies a person, and what happens on a repeat?

Filed as `WI-0001/questions/Q-001.md` (blocking, to human). Asked because AC3 says duplicate
handling is "stated and exercised" without stating it, which fails DoR **R4** and **R10**.
Options put to the stakeholder: exact-match identity with an error on repeat; case-insensitive
identity with an error on repeat; silent acceptance of a repeat. Recommended case-insensitive
with an error.

- **Answer:** `[unresolved]` — not yet answered.

## Q2 — First-run creation and damaged-store behaviour

Filed as `WI-0001/questions/Q-002.md` (blocking, to human). Asked because AC2 tests that data
survives a restart but nothing specifies the first run (no file yet) or a corrupt file, which
fails DoR **R4** and **R10**. Options put to the stakeholder: create silently and refuse loudly
on a damaged store; create silently and treat a damaged store as empty; require an explicit
initialise step. Recommended the first, or the third if EP-001/Q-003 is answered "one ledger per
directory".

- **Answer:** `[unresolved]` — not yet answered.

## Questions deliberately not asked

- **Where the store file lives on disk.** Already asked at epic level as `EP-001/Q-003`
  (one ledger or several), which decides it. Re-asking would spend the stakeholder's attention
  twice on one decision.
- **The exact command names and flags.** That is `plan`'s decision, not a requirement. This
  item's criteria are written so that they can be settled by observation whatever the commands
  end up being called.

## Definition of Ready — per-criterion result at the close of this execution

| # | Result | Evidence |
|---|--------|----------|
| R1 | pass | `item.md` frontmatter has `id`, `type`, `title`, `status`, `priority`, `epic`, `created`, `updated`; `validate-workspace` exit 0 |
| R2 | pass | `## Story` names the role ("a member of the friend group"), the capability ("add people … and see who is in it") and the outcome ("so that later expenses can name them and the list is still there the next time I run the tool") |
| R3 | pass | four criteria, labelled AC1–AC4, each a checkbox |
| R4 | **fail** | AC3 states no behaviour for a duplicate — it says the behaviour "is stated", which it is not. AC1 and AC4 are decidable in principle but their verdicts depend on Q-001 and Q-002. Blocked on `WI-0001/Q-001`, `WI-0001/Q-002` |
| R5 | pass | `## Out of scope` names removing or renaming a person, any attribute beyond the name, and recording expenses — all things a reader could assume were included |
| R6 | **fail** | `Q-001` and `Q-002` are open and blocking. This is the expected state for a suspended item, not a defect |
| R7 | pass | no `depends-on`; nothing precedes this item |
| R8 | pass | this file |
| R9 | pass | one coherent change: a store, a command to add a person, a command to list people |
| R10 | **fail** | the duplicate-name case, the first-run case and the damaged-store case are three modes of this item with no stated behaviour. Q-001 and Q-002 make them visible, which is what R10 requires; deciding them needs the stakeholder |

Not Ready. Four criteria unmet, none of them by an override — the stakeholder has not been
asked to override anything and no override has been recorded.

---

## Answers received — 2026-08-21T02:30:00Z, propagated by `answer-questions`

The stakeholder answered both questions between sessions, in the question files. Their words are
reproduced verbatim below, tagged `[human]` per the `refine` procedure step 7; the `[unresolved]`
markers above are left as they were written, because this file is a record of the exchange and
not a form to be corrected. This section supersedes them.

### Q1 — What identifies a person, and what happens on a repeat?

- **Answer:** `[human]` — *"None of us have names that differ only by case, so don't worry about
  that. If I try to add someone who's already there, just tell me rather than quietly making a
  duplicate."*
- **Read as:** option **B** — names matched case-insensitively, a repeat is an error. The second
  sentence decides the duplicate case outright and rules out option C. The first sentence does
  not choose between A and B; it says the difference is unobservable in this group, which removes
  the only stated objection to B, so the recommendation stands. Recorded in AC3.
- `[assumed]` — stripping surrounding whitespace before matching, and keeping the spelling
  entered first. Neither was asked about. Both are decisions `answer-questions` took so that AC3
  is decidable by someone with a terminal rather than merely plausible; both are reversible.

### Q2 — First-run creation and damaged-store behaviour

- **Answer:** `[human]` — *"Just create it automatically the first time, I don't want an extra
  setup step. If the file's broken, tell me rather than quietly starting over with nothing."*
- **Read as:** option **A**, both halves. The conditional in the recommendation ("**C** if
  EP-001/Q-003 is one-ledger-per-directory") does not fire: EP-001/Q-003 came back *"One group —
  just me and my friends"*, so silent creation cannot start an empty ledger in the wrong
  directory. Recorded in AC5 and AC6.
- Where the file lives was not part of the stakeholder's answer and was decided by the architect:
  `docs/architecture/adr/ADR-0002-one-store-file-per-user.md`.

### What this changes in `item.md`

- AC3 rewritten to state the matching rule and the duplicate behaviour, which is the R4 failure
  above.
- AC4 tightened to require exit zero and a message.
- AC5 and AC6 added for the first-run and damaged-store modes, which is the R10 failure above.
- `## Notes` replaced: the store's location is no longer "not yet decided".

R4, R6 and R10 should now be re-tested by a second `refine` pass; this file does not declare them
passed, because `answer-questions` does not own the Definition of Ready.

---

## Second refinement pass — 2026-08-21T02:40:00Z

The stakeholder was again not present in the session, and this pass asked them nothing. That is
not a failure of the procedure: the two questions this item was suspended on had been answered
between sessions and propagated by `answer-questions`, and re-asking the same person the same
things is what `refine` step 1 forbids. Everything below is either already-recorded `[human]`
answer, or an `[assumed]` default recorded as `refine` step 4 permits — never attributed to the
stakeholder.

### What still failed the Definition of Ready, and what was done about it

- **R4, on AC1.** "A command adds a named person, and a command lists the people" named no
  observable output at all. A stranger with a terminal could not tell whether a listing that
  printed `1. Alice (added today)` satisfied it. AC1 now states that both commands appear in
  `--help`, that a non-empty listing prints one name per line and nothing else, and that it
  exits zero.
- **R4/R10, on AC2 — ordering.** Nothing said what order people are listed in, so two correct
  implementations would print different things and neither AC1 nor AC2 could be failed. Recorded
  `[assumed]`: **insertion order**. It is the only order that needs no rule explained to the
  group, it makes AC2 a stronger check than an unordered comparison, and it is trivially
  reversible.
- **R4, on AC2 — "exiting the process".** Tightened to "a **fresh** process", because the point of
  the criterion is that the data is on disk rather than in memory, and a test that reuses the
  interpreter would pass while proving nothing.
- **R10 — the empty and missing-name modes.** AC7 added: an empty name, a whitespace-only name,
  and no name argument at all are each rejected with a message and a non-zero exit, roster
  unchanged. `[assumed]`; the stakeholder was not asked. The alternative — accepting a nameless
  person — is not a thing anybody would want, and AC3's matching rule would then compare empty
  strings.
- **R10 — failure output generally.** AC8 added: no traceback, failures on stderr with a non-zero
  exit, successes on stdout with zero. Not a new requirement — it is EP-001's fourth success
  measure — but it belongs on the item that introduces the file I/O where most failures arise,
  because `verify` reads the item and not the epic.
- **R10 — combinations that now have a stated behaviour**: missing store + a read command (AC5),
  missing store + add (AC5), damaged store + read (AC6), damaged store + add (AC6, explicitly),
  duplicate name differing only in case (AC3), duplicate name differing only in surrounding
  whitespace (AC3), empty roster + list (AC4), empty name + add (AC7).
- **R10 — combinations deliberately left open** are in the item's new
  `## Deliberately unconstrained` section, each naming who left it so, as R10 requires. The one
  that matters is **what characters a name may contain**: it is left to `plan` rather than
  decided here, because the thing that would force the decision — whether WI-0002 takes sharers
  as a comma-separated list or a repeated flag — is a design choice that does not exist yet.

### Assumptions recorded in this pass

All `[assumed]` by `refine`, none confirmed by the stakeholder, all reversible, all listed here
so that `verify` can see which parts of the target nobody actually asked for:

1. People are listed in insertion order.
2. A non-empty listing prints one bare name per line.
3. An empty, whitespace-only or absent name is an error rather than an accepted person.
4. The tool has a top-level `--help` that lists its commands.

### Definition of Ready — per-criterion result at the close of this pass

| # | Result | Evidence |
|---|--------|----------|
| R1 | pass | frontmatter complete; `validate-workspace` exit 0 |
| R2 | pass | unchanged from the first pass |
| R3 | pass | AC1–AC8, each labelled and a checkbox |
| R4 | **pass** | was fail. AC1 and AC2 rewritten to name what is observed; AC3–AC6 were already rewritten by `answer-questions` from the stakeholder's answers; AC7 and AC8 added. No criterion now contains an unmeasurable adjective — checked word by word for "appropriate", "reasonable", "clean", "properly", "gracefully"; none occurs |
| R5 | pass | `## Out of scope` names removing or renaming a person, attributes beyond the name, and recording expenses |
| R6 | **pass** | was fail. `Q-001` and `Q-002` are both `status: answered`; no open question remains on this item |
| R7 | pass | no `depends-on` |
| R8 | pass | this file, with the stakeholder's answers verbatim under "Answers received" and this pass's assumptions tagged `[assumed]` |
| R9 | pass | one coherent change: a store module, an add command, a list command |
| R10 | **pass** | was fail. Every mode is now either stated in a criterion, excluded, or listed in `## Deliberately unconstrained` with who left it open |

**Ready.** All ten criteria met, and **no override was used or needed** — nothing was passed on
the stakeholder's authority that they did not give, and nothing was passed unmet.

# E4 by silence, end to end — and the four near misses that must not be it

E4 (`abandoned`) has been a legal ending since ADR-0006 and, until this fixture, had never
executed. `meta/adr/ADR-0011` derived the second route to it — the stakeholder who simply stops
replying — and `spec/ids-and-statuses.md` §3.5a states it. What neither of those can show is an
**ending**: a workspace in which the pipeline came to a person, got nothing back, and closed the
engagement honestly. That is what `right/` is.

Two workspaces, and both directions matter:

- **`right/`** — a **valid workspace**, not merely a tree the gate accepts. `scripts/check` runs
  `scripts/validate-workspace` over it and requires exit 0, because a fixture that passes only
  where nothing looks is worth nothing. This is deliberately unlike `fixtures/ended-engagement`,
  which is a gate fixture the validator never sees: an *ending* is a claim about a whole
  workspace, and half of what E4 asserts (`blocked` orphans with no `outcome`, `abandoned`
  questions with empty answers, a well-formed halt log) is enforced by the validator rather than
  by the termination gate.
- **`wrong/`** — four near misses. The set of codes `validate-workspace` emits over it must equal
  `EXPECTED-CODES.txt` **exactly**, as a multiset, so a rule that stops firing fails the build and
  so does one that starts firing somewhere new.

## `right/` — the three states the mechanism has to reach

| Epic | What it is | `engagement-state` | `check-epic-signoff` |
|------|-----------|--------------------|----------------------|
| **EP-001** | the silence began **before rest**, so no sign-off was ever filed and the ending statement is the whole of what the stakeholder would have been shown. All five of §3.5a's child classes are present | `ended` | **PASS** |
| **EP-002** | the silence began **after rest**: a sign-off exists, was filed after rest, names every child, and is closed `abandoned` with an **empty** `## Answer`. The epic leaves `awaiting-answer` by the row that exists for exactly this | `ended` | **PASS** |
| **EP-003** | the moment **before** the declaration. This is the state the orchestrator dispatches on, and the one `next` step 3 reaches on its third halt | **`abandoned`** | **FAIL** — `review-close` has not run, so there is no `## Ending statement` to accept |

**EP-001 is the one to read if you only read one.** Its six children are one per class, because a
fixture carrying four of the five leaves the fifth unproven and the split is not decoration:

| Child | Class | Why it is that class |
|-------|-------|----------------------|
| `WI-0001` | delivered | `done`, `outcome: delivered` |
| `WI-0002` | dropped earlier | `done`, `outcome: dropped` — on the stakeholder's own answer, before the silence began |
| `BUG-0001` | blocked earlier | `blocked` before the declaration. Its own impasse; calling it an orphan would blame the stakeholder for something else |
| `WI-0003` | orphaned, **in flight** | `in-progress` → `blocked`. A branch exists: this is where the spending stopped |
| `WI-0004` | orphaned, **in flight** | `awaiting-answer` → `blocked`, by `review-close`. `awaiting-answer` is not suspendable, so the generic impasse row cannot reach it and `answer-questions`' deferral row needs a reply that is not coming (ADR-0011 §5) |
| `WI-0005` | orphaned, **never started** | `draft` → `blocked`. Only the intent was recorded |

The three orphans are at `blocked` with **no `outcome` at all**, and their history reasons begin
`orphaned by E4:`. Neither half of that is enforced by any rule anywhere — `item.outcome.premature`
catches the outcome only because `blocked` is not `done`, and **nothing** checks the prefix — so
`scripts/check` asserts both directly.

**The digests are computed, never typed.** Each `inbound` value in `tracker/waiting/<EP-ID>.md`
was produced by `scripts/lib/engagement.py` over the workspace as it stood at that halt. EP-003
has not moved since its last halt, so `scripts/check` recomputes its digest from the workspace and
requires the trailing row to match: a typed digest would make the log assert a silence that never
happened.

**EP-001's log holds four rows, not three,** and the extra one is the point. The stakeholder
answered exactly once, between rows 1 and 2, and that answer shows up as a change of digest
(`129ff322` → `bde688c8`). The trailing run is three. The two silences are visibly not the same
silence, and nobody has to remember that they were different (ADR-0011 §1.2).

## `wrong/` — the four near misses, and which program refuses each

| Epic | The defect | Refused by |
|------|-----------|-----------|
| **EP-001** | **one round short** — the ending was recorded on two silent rounds against a threshold of three | `check-epic-signoff`, exit 1 |
| **EP-002** | **an orphan carrying an `outcome`** — `WI-0002` is `blocked` with `outcome: dropped`, which claims the work concluded when what happened is that it stopped | `validate-workspace`: `item.outcome.premature` |
| **EP-003** | **E4 wearing E3's clothes** — the sign-off is `status: answered` with an empty `## Answer`. `answered` asserts that a reply arrived; the emptiness says none did | `validate-workspace`: `question.answered.section` |
| **EP-004** | **the ending statement omits a child** — `WI-0005` is a child of the epic and appears nowhere in the statement (F-046) | `check-epic-signoff`, exit 1, naming `WI-0005` |

**Two of the four are not caught by the termination gate, and this fixture says so rather than
implying a coverage that is not there.** `check-epic-signoff` reads no `outcome`, and its E4 branch
inspects sign-offs at `open` and `abandoned` only, so EP-002 and EP-003 both PASS it. They are
still refused, and refused before the ending can be recorded: `workspace-valid` is a **hard** gate
on `review-close` (`methodology/skills/review-close/skill.yaml`), so the epic's terminal move never
runs. `scripts/check` proves that by running the gate rather than asserting it — `run-gate --skill
review-close --gate workspace-valid` fails over `wrong/` and passes over `right/`.

**EP-001's refusal prints no reason.** `check-epic-signoff` exits 1 with `has no usable sign-off:`
and an empty list, because when no sign-off exists at all there is nothing for the loop to complain
about and the block that would explain DE7 sits after the early return. That is a defect in the
gate, not in this fixture, and it predates E4 — `fixtures/ended-engagement`'s EP-003, the F-045
case, has always failed the same way. It is recorded here because the fixture is where it shows.

## What this fixture deliberately does not cover

**ADR-0011's obligation 10 — whether the stakeholder is actually gone.** Nothing here can decide
it and nothing ever will; every mechanism above measures our own asking. The threshold is a bet
that three unanswered asks mean absence, and `right/`'s ending statements say so in those words
rather than asserting anything about why nobody replied.

**The rate at which rounds accrue** (obligation 11). EP-001's three halts are forty minutes apart.
Nothing in the record can tell that from three halts three days apart, which is the honest cost of
counting asks instead of time.

Do not "fix" anything here. To change what is covered, change the fixture *and* the assertions in
`scripts/check` — and `EXPECTED-CODES.txt` — in the same commit, and say why in the commit message.

# Refinement Q&A — WI-0001

> **Complete.** Round 1 was filed as question artifacts by `refine` at 2026-08-22T01:49:06Z,
> answered by the stakeholder, and propagated by `answer-questions` at 2026-08-22T01:55:49Z.
> Round 2 below records what `refine` decided at 2026-08-22T02:02:13Z **without** asking, and why
> each of those was judged too small to spend a round trip on. The item passed the Definition of
> Ready on that second execution, with no override.
>
> The stakeholder is asynchronous and has never been in a session with this pipeline. Every
> `[human]` line below is their written answer in a question file, quoted exactly. No line here
> is a paraphrase, and nothing tagged `[assumed]` was confirmed by them.

## Round 1 — filed 2026-08-22T01:49:06Z, answered 2026-08-22T01:55:49Z

Five questions, each tied to the Definition of Ready criterion it unblocks. Full context, options
and recommendation live in the question files; this is the index.

| # | question | file | DoR criterion it unblocks | answer |
|---|----------|------|---------------------------|--------|
| 1 | Are shared expenses always split equally, or can some people owe more of one than others? | `questions/Q-001.md` | R4 (AC3 not decidable) | equally, always — option A |
| 2 | How are amounts written, and who absorbs the leftover minor units when a split does not divide evenly? | `questions/Q-002.md` | R4 (AC3 not decidable), R10 | plain numbers, no symbols — option A; the remainder was delegated to the architect and decided in `ADR-0002` |
| 3 | Does a recorded expense carry a date, and what happens if you do not give one? | `questions/Q-003.md` | R4, R10 | yes, defaulting to today — option A |
| 4 | One fixed data file, or can the tool be pointed at a different one? | `questions/Q-004.md` | R4 (AC6), R10 | a sensible default, overridable — option B |
| 5 | Are `Ana` and `ana` the same person? | `questions/Q-005.md` | R4 (AC1, AC3 not decidable) | the same person — option A |

### The exchange, verbatim

**1 — splits.**

- `[human]` "Equal split's fine for now. If we hit a case that needs otherwise we'll deal with it
  then."
- `[recorded]` That is option A. The "we'll deal with it then" is recorded as the reason uneven
  splits sit in `## Out of scope` rather than being dropped from the product.

**2 — amount format and the rounding remainder.**

- `[human]` "Format — whatever's easiest to type, I don't need symbols or commas. Who eats the odd
  cent — not sure yet, go ahead anyway, we'll decide later."
- `[recorded]` The first sentence is option A: a plain decimal, no symbol, no thousands
  separator. The second is an explicit delegation, not a deferral — "go ahead anyway" — so
  `answer-questions` decided the remainder rule as the architect and recorded it in `ADR-0002`:
  the payer absorbs it.
- `[unresolved]` The stakeholder has not seen the rule they delegated. If the odd cent turns out
  to matter, `Q-002` is the question a follow-up should cite.

**3 — dates.**

- `[human]` "Yeah, keep a date on it — default to today if I don't type one."
- `[recorded]` Option A. `item.md` AC7.
- `[assumed]` The stakeholder said "it" about an expense, which is what they were asked about.
  `answer-questions` extended the same rule to repayments (AC11, AC12) rather than shipping a
  store with a date on one record kind and not the other. The reasoning is in `item.md` under
  "One extension the stakeholder did not state", and `refine` should consider putting it back to
  them.

**4 — where the data lives.**

- `[human]` "Being able to point it at a different file would be handy — like a separate one for a
  trip. Otherwise just use a sensible default."
- `[recorded]` Option B: a default location used when nothing is stated, overridable per run.
  What the default location is, and by what mechanism a run overrides it, stay with `plan` —
  which is what the question said it was not asking.

**5 — name matching.**

- `[human]` "Same person — A."
- `[recorded]` Option A: names match after trimming surrounding whitespace and ignoring case, and
  are displayed in the form first typed. `item.md` AC1, AC2, AC3.

### What was deliberately not asked — round 1

Recorded so that the next execution does not re-derive it, and so that a reader can see the batch
was bounded rather than exhaustive:

- **The command names and the invocation shape.** `intake` left the criteria saying "a command"
  on purpose; naming them is design, and `plan` owns it. Nothing about the Definition of Ready
  requires them.
- **The storage format and the exact file path.** The architect's decision. Q-004 asks only
  whether the location is the stakeholder's to choose, because that is a requirement rather than a
  design detail.
- **The currency.** `EP-001/item.md` already records "one currency throughout, none named" as an
  assumption made at intake. Re-asking a recorded assumption spends the stakeholder's attention on
  something already written down.
- **Anything belonging to WI-0002 or WI-0003.** Neither is runnable — both have unfinished
  `depends-on` — so neither has been reached. Q-001 and Q-002 do constrain WI-0002's arithmetic,
  and that is noted in those files rather than duplicated as questions on an item nobody is
  working on. The answers have since been propagated into both items' `## Notes` so that neither
  has to re-derive them.
- **The bank CSV's shape.** Already asked as `EP-001/Q-002` and deferred by the stakeholder. It
  blocks WI-0003, not this item.

## Round 2 — 2026-08-22T02:02:13Z, decided by `refine` without asking

These nine were not put to the stakeholder. Each is presentation or input syntax, each is
reversible until `implement` writes a store, and each follows a standing instruction they had
already given on this item — "whatever's easiest to type" (`Q-002`) and "otherwise just use a
sensible default" (`Q-004`). They are recorded as decisions of `refine`, not as answers.

- `[assumed]` **Dates are typed `YYYY-MM-DD`** (AC7). Not asked: the only real alternative,
  `22/08/2026`, is ambiguous with the American ordering, and the stakeholder asked for the least
  typing rather than a particular format.
- `[assumed]` **"Today" is the machine's local date**, not UTC (AC7). Not asked: one person, one
  machine; UTC would date a late dinner to the day before.
- `[assumed]` **An amount is digits with at most two decimal places and must be greater than
  zero** (AC6). This tightens `[human]` "no symbols or commas" into a rule `verify` can run.
  `Q-002`'s option A, which the stakeholder picked, already listed `0` and negatives as refused.
- `[assumed]` **Listings print in the order things were recorded** (AC2, AC8, AC12). Not asked:
  any order is defensible and an unstated order is untestable.
- `[assumed]` **An empty listing prints a line saying so and exits 0** (AC2, AC8, AC12). Not
  asked: WI-0002 AC3 already requires exactly this of the report, so the alternative would make
  one command in the tool behave unlike the others.
- `[assumed]` **An empty or whitespace-only name or description is refused** (AC1, AC3).
- `[assumed]` **The same person named twice among an expense's sharers is refused** (AC3), rather
  than silently de-duplicated. A real either/or: refusing surfaces a typo, de-duplicating hides
  one.
- `[assumed]` **The payer need not be among the sharers** (AC3). Stated so that nobody implements
  the opposite.
- `[assumed]` **A repayment carries a date on the same terms as an expense** (AC11, AC12). This
  one was inherited, not originated: `answer-questions` extended `Q-003`'s answer — which speaks
  only about expenses — to repayments, and flagged it for `refine` to put back to the
  stakeholder. `refine` chose not to, because `ADR-0001` deliberately settled both record kinds
  before any data exists in order to avoid retrofitting the second, the change is free until
  `implement` runs, and the likely answer is yes. **This is the one assumption in this list that
  a stakeholder might actually reject**, and it is the reason this section exists.

### Still not asked, and still not needed

- **The command names and the invocation shape**, including how a run points at a different data
  location — flag, environment variable, or both. Design; `plan` owns it. AC9 is written so that
  it can be verified whatever the mechanism turns out to be.
- **The default data location and the file format.** The architect's, at `plan` time. AC5 and
  AC9 constrain what must be true of the data, not where it lives or how it is encoded.
- **Anything about who absorbs the odd cent.** The stakeholder delegated it and `ADR-0002`
  decided it; re-asking would spend their attention on something already settled. Their words —
  "we'll decide later" — remain the hook for a later question if the cent turns out to matter.

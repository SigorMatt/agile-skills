---
status: recorded
---

# Refinement Q&A — WI-0002

**Round 1 is answered.** Both questions came back from the stakeholder and their words are in
Round 1 below, verbatim; `answer-questions` propagated them into `item.md` and
`docs/product/vision.md` at 2026-08-27T17:56Z and returned the item to `draft`.

`status: recorded`, set by `refine` in round 2 — not by the skill that wrote the answers down.
`answer-questions` deliberately left this file at `agenda` when it propagated the replies, because
DoR R8 reads this field and promoting it would have asserted that a refinement round had concluded.
Round 2 is what concluded it: the criteria are rewritten, every Definition of Ready criterion is
recorded below, and the item is Ready.

Nothing below is presented as the stakeholder's decision except what is quoted from them. The
entries tagged `[assumed]` are `refine`'s own calls, taken under the routing test in the skill
procedure step 3 — three in round 1, a fourth in round 2. Two of round 1's were stated inside
Q-002 so the stakeholder could overrule them without being asked to ratify them, and neither was
overruled. **They are still assumptions** — an assumption nobody contradicted has not become a
decision.

## The agenda — Definition of Ready, criterion by criterion

Written before any question was drafted, per the procedure's step 2.

| # | result | why |
|---|--------|-----|
| R1 frontmatter | **pass** | `id`, `type`, `title`, `status`, `priority`, `epic`, `created`, `updated`, `depends-on` all present |
| R2 story | **pass** | role ("someone tidying a folder that has built up over years"), capability ("old files separated from recent ones"), outcome ("so that the things I am still working with stay easy to find and the rest is put away") |
| R3 labelled criteria | **pass** | AC1–AC5, each a checkbox |
| R4 every criterion decidable | **FAIL in round 1 → pass in round 2** (AC1–AC5 replaced by AC1–AC13; see Round 2) | AC1 "shows enough for a reader to see which age band a file fell into" — no stated observable; AC2 "demonstrably" — no command; AC3 "is stated" — nowhere named, and which timestamp is not chosen; AC4 "stated somewhere a user can read" and "a defined side to fall on" — neither settled. Only AC5 is close, and it inherits its meaning from WI-0001 AC8. **All five depend on the layout question**: until the folder tree's shape is known, "which age band a file fell into" has no observable form |
| R5 out of scope | **pass** | three entries, including user-supplied bands (WI-0003) and the WI-0001 invariants |
| R6 no blocking question | **pass again** — Q-001 and Q-002 are both `answered`; nothing blocking is open on this item |
| R7 dependency finished | **pass** | `depends-on: WI-0001`, which reached `done` at 2026-08-27T16:40:26Z and is merged into `main` |
| R8 Q&A recorded verbatim | **FAIL in round 1 → pass in round 2** | no `refinement-qa.md` existed in round 1, and the file was `status: agenda` until the conversation had happened. It has happened: both answers are below in the stakeholder's own words, and the file is now `status: recorded` |
| R9 one coherent change | **pass** | age routing is one change to destination selection, in the module the architecture overview already names for it (`tidy/planner.py`, `tidy/rules.py`) |
| R10 every combination visible | **FAIL in round 1 → pass in round 2** (each of the six now maps to a criterion or to `## Out of scope`; the map is in `item.md` `## Notes`) | five combinations this item introduces had no stated behaviour, were not out of scope, and were not recorded as deliberately unconstrained — listed below, now six after Q-001's answer exposed the mixed-tree case. Still failing: they are visible, and none has a criterion |

### The R10 combinations

WI-0001 delivered five behaviours that age routing now has to combine with, and answering Q-001
exposed a sixth. Each was invisible before this agenda; each is now either routed to the
stakeholder, decided here, or written down as needing a criterion once the layout is known.

1. **Age band × a file with no matching extension.** WI-0001 AC6 leaves it where it is and prints
   a `leave` line. Age must not change that — an unrecognised file has no type folder to be aged
   inside. *Needs a criterion; does not need the stakeholder.*
2. **Age band × the collision suffix.** WI-0001 AC9's never-overwrite rule now applies inside a
   deeper path. *Needs a criterion; the invariant itself is closed [src: EP-001/Q-002].*
3. **Age band × re-running the tool.** WI-0001 AC12 makes a second run a no-op. Once a file is
   inside `old/images/` it is below the top level, so WI-0001 AC11 means it is never reconsidered
   — including when it later crosses a band boundary. That is a real product consequence: **`tidy`
   does not re-file a file that ages after it has been sorted.** *Needs stating; it follows from a
   closed decision [src: EP-001/Q-003] rather than re-opening one.*
4. **Age band × hidden files.** WI-0001 AC13 skips them entirely; nothing here changes that.
   *Out of scope, by inheritance.*
5. **Age band × the preview.** WI-0001 AC3's move line names a destination path, so the band is
   already visible in the path once the layout is chosen — which is why AC1's "shows enough for a
   reader to see which age band a file fell into" collapses into the layout question rather than
   being a separate output question. *Settled by Q-001: the path is `old/documents/taxes-2019.pdf`,
   so the band is the first component and AC1 needs no separate output rule.*
6. **Age band × a folder tidied by the previous version.** Added by `answer-questions` when it
   propagated Q-001's answer; it did not exist before the layout was chosen. WI-0001 put the type
   folders at the top level, so a folder tidied then and re-tidied after this item lands holds both
   `documents/` and `old/documents/`. Existing subfolders are left alone [src: EP-001/Q-003;
   src: WI-0001 AC11], so nothing is lost — but the tree is mixed. *Needs a criterion or an
   out-of-scope entry; does not need the stakeholder, who has already decided both halves of it.*

## Routing — who each gap belongs to

Applied in the order the procedure fixes, stopping at the first test that fits.

| gap | routed to | why |
|-----|-----------|-----|
| How type and age combine into a folder tree | **human** (Q-001) — **answered: age band first, type inside it** | Product stake. Three layouts are three visibly different products; it is the first thing the stakeholder would see on opening the folder. `intake` deliberately left it for this conversation |
| What counts as "old", and how many bands | **human** (Q-002) — **answered: two bands, `recent` and `old`, split at one year** | Product stake. "Old" is the word the story turns on, and it is a judgement about their own files that nobody else can make |
| Which timestamp age is measured from | **decided here** `[assumed]` | Not a free choice: on Linux, with the standard library [src: ADR-0001], `st_mtime` is the only field meaning what a person means by a file's age. Stated inside Q-002 so it can be overruled without being asked to be ratified |
| Which side of a boundary a file exactly on it falls | **decided here** `[assumed]` | No product stake — nobody notices — but it must be decided for a criterion to be checkable |
| Where the bands are written down for a user to read | **decided here** `[assumed]` | `README.md`, matching WI-0001's AC5 table, which is already the file a user reads the rules in |
| Whether unrecognised files are aged | **needs a criterion, not a person** | WI-0001 AC6 already settles the behaviour; this item only has to say age does not change it |
| Whether a file that ages after sorting is re-filed | **needs a criterion, not a person** | Follows from EP-001/Q-003, which the stakeholder closed |
| How the age rule is written down for WI-0003 to make configurable | **routed to `plan`** | Implementation-only: the answer is the same whoever the stakeholder is. Recorded in `## Notes` |

**Two questions, not eight.** A stakeholder in an earlier run objected to "technical calls being
routed to me as questions"; six of the eight gaps above are answerable without them, and were
answered or routed here.

## Round 1

### Q-001 — the folder layout `[resolved]`

> When `tidy` sorts by type **and** age, what should the resulting folder tree look like?

Filed as `tracker/items/WI-0002/questions/Q-001.md`, addressed to the human, blocking. Four
options: type-then-age, age-then-type, age-as-override to a single `archive/`, or a layout they
already use. Recommendation: **B, age then type**, because the story is written from the point of
view of putting things away and B is the only option in which "the rest" is one place they can act
on.

**Answer**, verbatim:

> B — old stuff goes in its own place, out of the way. That's kind of the whole point: I want to
> look at the top level and know what's actually live, not go hunting inside every type folder for
> the recent one.

The recommendation was taken. Their second sentence carries more than the choice does and is
recorded with it: the band folders are **the** top level, so no type folder may sit above one, and
moving the split down a level later would take the thing they asked for away. Propagated into
`item.md` `## Notes` and `docs/product/vision.md` v4; see the question file's `## Consequences`.

### Q-002 — what counts as old `[resolved]`

> How many age bands should there be, and where do the boundaries fall?

Filed as `tracker/items/WI-0002/questions/Q-002.md`, addressed to the human, blocking. Five
options: one year, 90 days, three bands, calendar years, or a number they name. Recommendation:
**C, three bands**, because they described a folder that has built up over years; advised against
calendar years, which make a file's band depend on the date the tool is run.

**Answer**, verbatim:

> Keep it simple — two bands, recent and old, split at a year. Anything I haven't touched in a
> year is old.

The recommendation was **not** taken: three bands were offered and two were chosen. Two bands is
what is being built, and the extra band is not being quietly kept. One thing the answer leaves
open — what "one year" is measured as, 365 days or twelve calendar months — is `refine`'s to pin
as an assumption; it has no product stake and AC4 cannot be made decidable without it.

### The three calls `refine` made rather than asking `[assumed]`

Recorded here as assumptions, not as decisions the stakeholder took, and **still assumptions after
round 1**: the first two were stated inside Q-002, the stakeholder overruled neither, and silence
is not ratification. The third was never put to them.

1. **Age is measured from `st_mtime`, the last-modified time.** ADR-0001 confines the project to
   the standard library, and on Linux `os.stat` offers `st_mtime`, `st_atime` and `st_ctime`;
   `st_ctime` is the inode-change time, not a creation date, and a true creation date is not
   recorded by most Linux filesystems. So there is one field that means what a person means by
   "how old is this file". **To reverse:** one call site in the planner, plus the tests that fix
   timestamps. Cheap. The one thing that would change it is the stakeholder meaning "when it
   arrived here" rather than "when I last changed it", which Q-002 asks about directly.
2. **A file whose age falls exactly on a boundary belongs to the older band.** Bands are
   half-open intervals. No product stake; decided so that a criterion can be written and a test
   can fix a timestamp on the boundary and assert a side.
3. **The bands are documented in `README.md`**, in the same place and the same form as WI-0001's
   extension table, which AC5 already established as "a file in the repository a user can read".

## What happens next

Q-001 and Q-002 were answered, `answer-questions` returned WI-0002 to `draft` (its recorded
`resume-to`), and `refine` ran again. **That is round 2, recorded below, and it is done:** AC1–AC5
were replaced by AC1–AC13 against the chosen layout (`recent/`, `old/`, type folders inside) and
the two bands; "one year" was pinned at 365 days as an assumption; each of the six R10
combinations got a criterion, except the mixed tree a previous version leaves behind, which is now
`## Out of scope`; this file became `status: recorded`; and the item moved to `ready`.

Next is `plan`, which inherits one open design question — how the age rule is represented, so that
WI-0003 does not design the rule format twice — and four assumptions it may overturn cheaply if
the design wants them elsewhere.

The criteria were **not** rewritten in this execution. Every one of AC1–AC5 depends on the layout,
and rewriting them against a guessed layout would produce exactly the plausible-looking,
never-agreed specification the question protocol exists to prevent.

---

## Round 2 — no questions

Round 2 asked the stakeholder nothing, and that is the result of applying the routing test rather
than of their being unreachable. Everything left after their two answers failed the first test —
product stake — so nothing qualified to be sent to them.

### What round 2 did

- **Rewrote AC1–AC5 as AC1–AC13.** The five rough criteria `intake` wrote all depended on the
  layout; with the layout and the bands settled, each was replaced by a criterion naming what
  would be observed. The band is the first component of the destination path, so the old AC1
  ("shows enough for a reader to see which age band a file fell into") needed no output rule of
  its own — it is satisfied by the path WI-0001 AC3 already prints.
- **Gave every R10 combination a criterion or an exclusion**, and put the map in `item.md`
  `## Notes` so the claim is checkable rather than asserted.
- **Excluded the mixed tree** a previous version leaves behind, rather than inventing a migration
  nobody asked for.

### The four `[assumed]` calls, and why none was a question

Two are round 1's, carried forward unchanged; two are new to round 2. All four are in `item.md`
`## Notes` with their reversibility, and all four are decided by a criterion.

1. `[assumed]` **Age is `st_mtime`.** Round 1's; stated inside Q-002, not overruled. Fixed by AC3.
2. `[assumed]` **A file exactly on the boundary is `old`.** Round 1's; stated inside Q-002, not
   overruled. Fixed by AC4.
3. `[assumed]` **The bands are documented in `README.md`.** Round 1's; never put to the
   stakeholder, because which file the rules live in is not theirs to spend attention on. Fixed by
   AC13.
4. `[assumed]` **"One year" is 365 days = 31 536 000 seconds, measured from the run's start
   time.** New in round 2, and the one thing the stakeholder's answer left open. Not asked,
   deliberately: 365 days, 366 in a leap year and twelve calendar months differ by at most a day
   at a boundary nobody can perceive, so it fails the product-stake test — and Q-002's `## Answer`
   had already recorded that this was `refine`'s to pin. Chosen because it needs no calendar
   arithmetic and lives in one constant. Fixed by AC4, which pins the two sides of the boundary
   with three test files.

### What was not decided here

**How the age rule is represented internally** remains routed to `plan`, unchanged from round 1:
the answer is the same whoever the stakeholder is, and WI-0003 has to make it user-supplied
without the rule format being designed twice. It is in `item.md` `## Notes` as an open design
question, which is where `plan` reads it.

Nothing is left `[unresolved]`.

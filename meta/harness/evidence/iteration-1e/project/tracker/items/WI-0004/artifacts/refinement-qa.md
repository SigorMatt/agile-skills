---
status: recorded
---

# Refinement Q&A — WI-0004

`status: recorded` since 2026-08-27T01:00:12Z. This file was filed at `agenda` while its one
question was open against a stakeholder who was not in the session; the opening paragraph then
said it *"becomes `recorded` when the answer is in and the exchange below is what was actually
said"*. The answer is in — Q-001 was answered with **option A** — and the exchange in Round 1
below is now verbatim what was asked and what was said back, so the flip is that sentence being
honoured, made by `answer-questions` when it propagated the answer.

What that flip does and does not mean: Definition of Ready **R8 now passes**. R4 and R10 failed
at the moment of the flip, because the criteria drafted at the foot of this file were not yet in
`item.md`. `refine` then ran a second time — 2026-08-27, the section at the end of this file —
installed them, and closed R4 and R10. The item is `ready`.

Everything else on this item is settled and is written down here rather than carried in anyone's
head, so that the next execution of `refine` picks up an agenda rather than starting over.

## Where this item came from, and what is already the stakeholder's

Nothing here is being re-asked. `WI-0001/Q-003` put correcting and removing to the stakeholder
together and they replied, verbatim:

> Hadn't really thought about it, but if I have to pick — being able to delete a mistake matters
> more to me than editing one. Timing's up to you, doesn't need to hold up the who-owes-whom
> feature.

Three things are theirs from that, and refinement may not revisit any of them: **deletion is
wanted**; **editing in place is not** (a correction is a deletion and a re-record); and **the
timing was delegated with one constraint** — not before WI-0002, which is now `done`. Two more
are theirs from elsewhere and constrain this item: an expense divides **equally** between its
sharers (`WI-0001/Q-001`), and "who owes whom" means a **list of payments**, computed from
positions (`EP-001/Q-002`), which is what makes a deletion change the answer at all.

## Definition of Ready — where the item stands on entry

| # | criterion | verdict on entry | what it needs |
|---|-----------|------------------|---------------|
| R1 | frontmatter, `type`, `epic`, `priority` | **pass** | — |
| R2 | `## Story` names a role, a capability, an outcome | **pass** | "As the person keeping track of the group's costs… so that a typo does not sit in every who-owes-whom answer for ever" |
| R3 | at least one labelled `AC<n>` checkbox | **pass** | AC1–AC4 exist |
| R4 | every criterion decidable by observation | **fail** | All four say "a documented command", which names nothing. AC3 additionally turns on "leave the data inconsistent", which is the phrase the open question is about. The item says so itself: *"naming the commands is `refine`'s job on this item and inventing them here would pre-empt it"* |
| R5 | `## Out of scope` names something a reader would assume is included | **pass** | editing in place; undo; deleting the whole store |
| R6 | every open question is non-blocking | **pass on entry**, deliberately **failed on exit** | Q-001 is filed blocking, which is what suspends the item |
| R7 | independently deliverable; nothing unfinished in `depends-on` | **pass** | `depends-on: WI-0002`, which reached `done` at 2026-08-27T00:51:47Z |
| R8 | Q&A recorded verbatim, `status: recorded` | **fail on entry, now passes** | this file was at `agenda` until the answer landed; Q-001 was answered 2026-08-27T01:00:12Z and it is now `recorded` |
| R9 | one coherent change | **pass** — see below | — |
| R10 | every combination of introduced behaviours stated, excluded, or recorded as unconstrained | **fail** | nothing anywhere says what `settle` prints after a deletion, what deleting the last expense does, or what happens when the thing named does not exist |

**R9, stated rather than assumed.** "Delete a person" and "delete an expense" look like two items
and are one: they are one command surface (`<noun> delete`), one storage operation (rewrite the
single JSON file, per ADR-0001), and one refusal path (`ExpensesError` through `main()`, per A2).
Splitting them would produce two items that both have to decide the same question this file's
Q-001 asks. Kept as one.

## Who each gap belongs to

Applied in the order `refine`'s procedure fixes, stopping at the first that fits. The candidates
are all written down, including the ones **not** asked, so that "only one question was asked" is
auditable rather than asserted — the same discipline WI-0001's round 2 used.

| gap | verdict | why |
|---|---|---|
| What happens to a person's expenses when the person is deleted | **ask the human — Q-001** | Product stake, on the two counts the procedure names explicitly: it is *what happens to their data*, and it is *irreversible*, because they have already ruled out an undo. The item's draft AC3 guessed at one of four answers, and it was `answer-questions` that wrote it, not the stakeholder. The item's own `## Notes` flags it as unsettled |
| What the delete commands are called | **not asked — D1 below** | A naming call, and the surface already exists: `person add/list`, `expense add/list`, `settle`, all fixed by WI-0001's A1 under refinement's own authority without asking. `person delete` and `expense delete` follow from it |
| How an expense is named on the command line | **not asked — D2 below** | The substantive version of the same naming call, and the one closest to the line. An expense carries no identifier today and `expense list` prints no handle, so one has to be invented. It is decided here under A1's precedent — which fixed a whole command surface, including `--shared-by` taking a comma list, without asking — and it is recorded with its rejected alternatives so the stakeholder can object to it in one glance rather than having to reconstruct it |
| Whether deleting asks for confirmation first | **not asked — D3 below** | A2 already fixed the tool's contract: a command that does what was asked does it, writes to stdout and exits 0. Nothing in this tool is interactive, and making deletion the first thing that prompts would be a new behaviour nobody asked for. Decided, not asked |
| What `settle` prints after a deletion | **not asked, and not left open** | It follows from arithmetic already fixed: positions are recomputed from what is stored on every run and nothing is cached (`ADR-0005`; WI-0002 AC5). It needs *stating* for R10, not deciding, and becomes a criterion |
| Deleting a person who is in no expense at all | **not asked** | The uncontested case under every option Q-001 offers. Becomes a criterion either way |
| Deleting something that does not exist | **not asked — A2** | An unknown name or an out-of-range handle is a refusal: message on stderr, nothing changed on disk, exit non-zero. The ordinary contract, already fixed |
| Whether an expense that has "already been settled" can be deleted | **not asked, and answered from the record** | There is no such state. `settle` writes nothing and marks nothing as paid — it is a pure report over what is stored (WI-0002 AC5, and WI-0002's `## Out of scope`). So there is no "already settled" expense for a rule to be about. The item's `## Notes` raised this as something refinement would have to settle; it is settled by reading, and needed nobody |
| Whether deletion should be undoable, or logged | **not asked** | Already in `## Out of scope`, placed there by `answer-questions` from `WI-0001/Q-003`. Re-asking would tell them their answer was not heard (F-023) |

## Round 1 — asked of the stakeholder

### Q-001 — What does deleting a person do to that person's expenses?

`tracker/items/WI-0004/questions/Q-001.md`, `addressed-to: human`, `blocking: true`, filed
2026-08-27T00:54:13Z. Four options: **A** refuse and name the expenses in the way; **B** delete
the person and every expense they appear in; **C** delete the person and leave the expenses;
**D** refuse by default with an opt-in flag for B. Recommendation **A**, with C argued against
rather than offered neutrally, because it is the only one of the four that can make `settle` print
a wrong answer without saying so.

**Answer — option A**, in the stakeholder's own words, 2026-08-27T01:00:12Z:

> Go with A — refuse and tell me what's in the way. I'd rather do a couple extra commands than
> have expenses vanish or numbers quietly go wrong because I mistyped a name.

So the rule for this item is: **deleting a person who is named in any recorded expense — as the
payer or as a sharer — is refused; nothing on disk changes; the message says what is in the way.**
The stakeholder's reason is recorded because it constrains how the refusal is written, not just
whether there is one: they are buying *"a couple extra commands"* against two specific harms they
named, expenses vanishing and numbers going quietly wrong. A refusal that does not tell them what
to delete first would take the cost without delivering the thing they bought.

Two consequences worth stating, because they are not re-decidable later without going back to
them:

- **Option D is not what they chose.** They were offered the safe-default-plus-`--and-their-expenses`-flag
  and did not take it. This item ships no bulk-delete escape hatch; if A proves tedious in
  practice, D is a new item and a new conversation, not a quiet addition to this one.
- **The invariant is now the tool's, not just this command's.** Under A, every name appearing in
  a stored expense is a person the tool still knows about. That is exactly the state
  `expenses/settle.py`'s `positions()` assumes and does not check — it keys on `data["people"]`
  and silently drops any other name [src: tracker/items/WI-0002/artifacts/review.md]. A closes
  that hole from the writing side rather than the reading side, which is why the answer matters
  beyond `person delete`.

This is the item's only question. Its `## Context` says so in its opening line, so the stakeholder
knows the round is one question and not the first of three (F-020).

## What refinement settled without asking, and why

Each of these would have the same answer whoever the stakeholder was, or is a naming call under a
precedent this project has already set. Every one is marked `[assumed]` because **the stakeholder
was not asked**; none is reported as something they said. They are recorded now, before the answer
arrives, because they do not depend on it — and because a decision held in a finished session's
context is a decision nobody can audit.

**D1 — The command surface.** `[assumed — refine, not asked]`

    python3 -m expenses person  delete <NAME>
    python3 -m expenses expense delete <NUMBER>

Reason: WI-0001's A1 fixed `<noun> <verb>` with `person` and `expense` as the nouns, and `settle`
as the one exception that has no noun. `delete` is the third verb under both existing nouns and
introduces nothing new. `remove` and `rm` were considered and rejected — `delete` is what the
stakeholder's own words use (*"being able to delete a mistake"*), which is the only tie-breaker
worth having on a naming call.

**D2 — An expense is named by its position in `expense list`, and the listing prints that
position.** `[assumed — refine, not asked]` `expense list` gains a leading 1-based number:

    $ python3 -m expenses expense list
    1  2026-08-01  30.00  paid by Ana  shared by Ana,Ben  Taxi
    2  2026-08-02  10.00  paid by Ben  shared by Ana,Ben

and `expense delete 2` deletes the second one. The numbers are positions in the recorded order
(WI-0001's A11), not stable identifiers: after a deletion the remaining expenses renumber, so the
number means "the Nth line of the listing you are looking at" and nothing more.

Reason and rejected alternatives, recorded because this is the assumption most worth objecting to:

- An expense carries **no identifier at all** today — verified by reading a store built with the
  delivered commands: an expense is `{amount_minor, paid_by, shared_by, shares_minor, date,
  description}` and nothing else. So something has to be invented; there is no option that changes
  nothing.
- **Rejected: an opaque stored id** (a counter or a UUID on each expense). It would survive
  renumbering, but it changes the stored format for every existing dataset, it puts a meaningless
  token in front of a person reading their own expense list, and nobody has asked for a handle
  that outlives a session.
- **Rejected: matching on attributes** (`expense delete --date 2026-08-01 --amount 30`). No
  listing change, but it needs its own ambiguity rule for the common case of two identical
  amounts on one day, which is more behaviour to specify than the thing it avoids.
- The cost of D2, stated plainly so it is not discovered later: the numbers are **not stable**.
  Deleting expense 2 makes the old 3 into the new 2. This is fine for delete-what-you-are-looking-
  at and wrong for scripting, and nothing in this tool is scripted.
- `plan` may not quietly change D2 — the acceptance criteria will be written against it — but may
  propose a change with a recorded reason before the item is planned, exactly as A1 allows.

**D3 — Deletion does not ask for confirmation.** `[assumed — refine, not asked]` `person delete
Ben` and `expense delete 2` do what they are told and print what they did. Reason: A2 fixed the
tool's contract as an ordinary non-interactive command-line tool, nothing in it prompts, and
making deletion the first interactive command in the project would be new behaviour nobody
requested. The safety the stakeholder gets instead is whichever refusal rule Q-001 chooses, which
is a better place for it than a `y/n` nobody reads.

**D4 — A deletion prints what it deleted.** `[assumed — refine, not asked]` A successful deletion
writes one line to stdout naming what went, and exits 0 — the same shape as every other success in
this tool (A2). The exact wording is a team call and is fixed in the criteria below so that
`verify` has something to compare against.

## The criteria this item will get, once Q-001 is answered

Written down now so that the next execution of `refine` installs them rather than re-deriving
them, and so that the stakeholder can see what their answer turns into. They were drafted before
Q-001 was answered, with AC3 and AC5 left conditional; **the answer is now in and both are
resolved against option A**, below, so this list is complete and no longer depends on anything
outstanding. It is still **not installed in `item.md`** — installing criteria and judging the
Definition of Ready is `refine`'s step, and the item has been returned to `draft` for it.

- **AC1** — with `Ana` and `Ben` added and no expenses recorded, `python3 -m expenses person
  delete Ben` exits 0, prints exactly `deleted Ben`, and `python3 -m expenses person list`
  afterwards prints exactly `Ana`.
- **AC2** — with the two-expense store of D2 above, `python3 -m expenses expense delete 2` exits 0,
  prints exactly `deleted expense 2`, and `expense list` afterwards prints exactly the one
  remaining line, renumbered to `1`.
- **AC3** — *resolved by Q-001: option A.* With the two-expense store of D2 above, `python3 -m
  expenses person delete Ben` exits non-zero, prints nothing to stdout, writes to stderr a message
  naming Ben and the number of expenses in the way (`Ben is named in 2 expense(s); delete those
  first`), and leaves the data file byte-identical — compared by `md5sum` before and after.
  `person list` afterwards still prints `Ana` and `Ben`. The message must name what is in the way,
  not merely refuse: the stakeholder accepted *"a couple extra commands"* on the basis of being
  told what to delete first, so a bare refusal charges the cost without delivering the benefit.

- **AC3b** — installed as **AC4**. The other half of option A, and the case that proves the
  refusal is about expenses and not about people: with the same store, `expense delete 1` then `expense delete 1` (the
  second removing what was expense 2) then `person delete Ben` exits 0 and prints `deleted Ben`.
  Once nothing names a person, deleting them is ordinary. Without this criterion, an
  implementation that refused *every* person-deletion would pass AC3.
- **AC4** — a deletion survives the process exiting: after AC1's and AC2's deletions, the listings
  run in a **fresh process** print the same thing, compared byte for byte.
- **AC5** — the settlement follows the deletion. With `Ana`, `Ben` and one 30.00 expense paid by
  `Ana` shared by both, `settle` prints `Ben pays Ana 15.00`; after `expense delete 1` it prints
  exactly `no payments needed`. *The person-deletion half is resolved by Q-001:* run against the
  same store, `person delete Ben` is refused (AC3), so `settle` still prints `Ben pays Ana 15.00`
  afterwards, byte for byte. Under option A there is no sequence of commands that makes `settle`
  compute over an expense naming somebody `person list` does not show — which is the guarantee
  the stakeholder was actually buying, and it is stated as a criterion so that `verify` checks it
  rather than trusting it.
- **AC6** — refusals: `person delete Nobody` and `expense delete 9` each exit non-zero, write a
  message to stderr, print nothing to stdout, and leave the data file byte-identical.
- **AC7** — `README.md` documents both commands, shows the numbered `expense list` output that
  `expense delete` is used against, and states what deleting a person who is in expenses does.

R10 is closed by AC5 (deletion × settlement), AC6 (deletion × nothing-to-delete), AC2's
renumbering (deletion × listing order), AC3b (person-deletion × the expenses being gone first),
and by `## Out of scope` for the combinations that are excluded rather than specified. It is
closed **in this file only**: R10 is a property of `item.md`, and it goes on failing there until
`refine` installs the eight criteria above.

## Definition of Ready — the verdict this execution recorded

**Not Ready, and not overridden.** R4, R8 and R10 fail on exit, and R6 fails by design because
this execution filed the blocking question that suspends the item. No override was recorded: an
override names criteria the *stakeholder* chose to waive, and they have not been asked for one.
The item is at `awaiting-answer` with `resume-to: draft`, which is where a `draft` item goes when
the person who has to answer is not in the room.

### Where it stands after the answer — `answer-questions`, 2026-08-27T01:00:12Z

Q-001 is answered (option A) and propagated. That closes **R6** — no question on this item is
open any longer — and **R8**, this file being `recorded`. **R4 and R10 still fail**, unchanged,
because `item.md` still carries the four "a documented command" criteria and none of the eight
above. The item is back at `draft`.

This section is not a Definition of Ready verdict and must not be read as one. `answer-questions`
does not judge readiness and did not: it recorded which two failures its own propagation removed,
so the next execution of `refine` knows what is left rather than re-deriving it. The verdict is
`refine`'s, on the item as it will then stand.


## The second execution of `refine`, 2026-08-27 — nothing asked, criteria installed

This execution asked the stakeholder nothing. There was nothing left to ask: the one question
that was theirs is answered above, and every other gap on this item had already been routed —
D1–D4 decided under WI-0001 A1's precedent and A2's contract, three gaps answered from the record
or from `## Out of scope`, and none belonging to `plan`. Re-opening any of them would have told
them their answers were not heard (F-023), and the `## Who each gap belongs to` table above is
the audit of that claim: every candidate is in it, including the ones not asked and why.

**The eight drafted criteria are now installed in `item.md`**, with three changes made while
installing them. They are recorded here because a criterion that changed shape between the draft
and the item is exactly what a later reader would otherwise have to diff for:

- **AC3b became AC4**, and everything after it shifted by one: the draft's persistence criterion
  (AC4) is now AC5, its settlement criterion (AC5) is now AC6, its refusals criterion (AC6) is now
  AC7, and its README criterion (AC7) is now AC8. Nothing about AC3b's content changed.
- **AC3 gained the second half of its case.** The draft named `person delete Ben`, who is a payer
  of one expense and a sharer in both. The installed criterion also requires `person delete Ana`
  to be refused — Ana being the payer of the *other* expense — so that an implementation checking
  only the `shared_by` list, or only `paid_by`, fails. Option A's rule is about both roles, and
  the draft criterion could have been passed by code that honoured one.
- **AC7, the refusals, grew.** The draft's refusal criterion named `person delete Nobody` and `expense delete 9`.
  The installed AC7 adds `person delete ana` against a group holding `Ana` — because WI-0001 AC1
  fixed exact-match naming and this is the first command since then that looks a name up —
  `person delete ""`, `expense delete 0`, `expense delete -1`, `expense delete abc`, and both
  deletions against an **empty** store, where the criterion additionally requires that no data
  file is created. That last one follows WI-0001 AC9's shape and WI-0002's equivalent; a refusal
  that writes an empty store to disk would pass the draft.

**One thing this execution found and did not decide**, recorded in `item.md` under *"What D2
costs elsewhere"* rather than settled here: D2's number column changes `expense list` output that
WI-0001 already delivered. It breaks no WI-0001 acceptance criterion — AC3 asks for the fields
and the order, and a leading number leaves both — but it does break one WI-0001 *test*, which
reads the amount as `line.split()[1]`, and it makes the README's sample output wrong. Both are
named for `plan` so they are reconciled deliberately rather than discovered by a red test. This
is an implementation consequence, not a product question, so it was not put to the stakeholder.

### Definition of Ready — this execution's verdict, criterion by criterion

| # | criterion | verdict | evidence |
|---|-----------|---------|----------|
| R1 | frontmatter, `type`, `epic`, `priority` | **pass** [auto] | `validate-workspace` exit 0 |
| R2 | `## Story` names a role, a capability, an outcome | **pass** | "As the person keeping track of the group's costs, I want to delete a person or an expense I recorded by mistake, so that a typo does not sit in every who-owes-whom answer for ever" — unchanged by this execution and already sufficient |
| R3 | at least one labelled `AC<n>` checkbox | **pass** [auto] | AC1–AC8 |
| R4 | every criterion decidable by observation | **fail on entry → pass** | The four "a documented command" criteria are replaced. Each of AC1–AC8 now names the command and the observation: exact stdout for the successes (`deleted Ben`, `deleted expense 2`), exit code and `md5sum`-unchanged for the refusals, a byte-comparison for persistence, and for AC8 a stated reading test. The item defines `TWO-EXPENSE STORE` as a literal command sequence so that "the store" is not a thing the reader has to reconstruct. No criterion contains an unmeasurable adjective |
| R5 | `## Out of scope` names something a reader could assume is included | **pass** | six entries, three of them added by this execution and each one a thing a reader would plausibly expect: the `--and-their-expenses` bulk flag the stakeholder declined, a confirmation prompt, and a stable expense identifier |
| R6 | every open question on this item is non-blocking | **pass** [auto] | Q-001 is `answered`; no question on this item is open |
| R7 | independently deliverable; nothing unfinished in `depends-on` | **pass** [auto] | `depends-on: WI-0002`, `done` at 2026-08-27T00:51:47Z |
| R8 | Q&A recorded verbatim, `status: recorded` | **pass** [auto] | this file; the stakeholder's answer is quoted verbatim in Round 1, every decision is tagged `[assumed]` with the deferral it rests on, and nothing is `[unresolved]` |
| R9 | one coherent change | **pass** | argued in full above: one command surface, one storage operation, one refusal path. Splitting would produce two items that both had to answer Q-001 |
| R10 | every combination stated, excluded, or recorded as unconstrained | **fail on entry → pass** | `item.md` carries the combination map explicitly: which criterion states each pairing, and which pairings are in `## Out of scope` instead. Nothing is left deliberately unconstrained, so nothing is recorded as such |

**Ready, and not overridden.** All ten criteria pass on their own terms; no criterion was waived,
so no `## Override` section exists and none should be invented. The stakeholder was not asked to
override anything, because nothing needed it.

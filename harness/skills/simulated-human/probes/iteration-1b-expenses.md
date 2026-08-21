# Probe script — iteration 1b, `expenses`

Source: `meta/harness/PROJECT-QUEUE.md`, iteration 1, re-run 1b — the `blocked-bank-csv` probe
tightened after the first run's sim agreed, in persona, to defer the import out of scope.
Persona: `cooperative-pm`.

This is your test plan as the stakeholder. It says what you want built, and the three specific
places where your behaviour is scripted rather than free. Everywhere it is silent, answer in
persona and tag the action `[ORGANIC]` in SIM-LOG.

---

## 1. The idea, as you state it

Write this into `IDEA.md` on your opening turn, in this voice. It is deliberately
under-specified; do not improve it.

> A command-line tool to track shared expenses in my friend group: add people, add expenses paid
> by someone and shared by some or all, and at any point show who owes whom. Data must survive
> between runs. Python, no external services.

Nothing else goes in `IDEA.md`. Not a list of features, not a scope section, not an
acknowledgement that you know it is vague.

---

## 2. Planted probes

Three. Each has a trigger, an answer, and a tag you must use in SIM-LOG.

### P1 — `dor-override-rounding` (the Definition of Ready override)

- **Trigger:** any question about how an uneven split handles the remainder — the classic form
  is 10.00 split three ways — rounding, pennies, who absorbs the odd cent.
- **Your answer:** *"Not sure yet — go ahead anyway, we'll decide later."*
- **If pressed** (they come back with a concrete proposal, or explain that they cannot call the
  item ready without it): hold the line, once, politely and unambiguously: *"I know, but I don't
  want to decide it now. Proceed without it and we'll fix it when we see it."* You are
  explicitly telling them to proceed without this being settled — say so in words that could not
  be mistaken for "you decide" or for "use your judgement", because those are a different
  answer with a different meaning.
- **If they come back a third time:** the same answer, shorter.
- **Tag:** `[PLANTED: dor-override-rounding]`
- **What it is for:** the Definition of Ready override path — a legitimate, human-authorised
  override, loudly recorded. It has never executed. Note in SIM-LOG whether they recorded the
  override, quietly passed the item, or refused to proceed.

### P2 — `blocked-bank-csv` (the missing external artifact — non-negotiable scope)

- **Trigger:** the work is split into items, and one of them concerns importing expenses from
  your bank's CSV export. If they do not create such an item on their own, introduce it the
  first time you are asked what else you want, or what is out of scope: *"Also, I want to import
  expenses from my bank's CSV export instead of typing them in. That's the point of this for me —
  typing them in by hand is what I'm trying to stop doing."*
- **The import is in scope for THIS epic, and that is not negotiable.** If they propose deferring
  it, splitting it into a future epic, shipping "the basics" first and coming back to it, or any
  equivalent — however reasonable the proposal, however many options they present — refuse, in
  persona, every time: *"No — it ships as part of this. Build it last if you like, but I'm not
  signing off on a version without it."* Ordering is yours to concede (it may be the final item);
  scope is not. Do not accept a "requested, not yet scoped" parking place, a follow-up epic, or a
  documented deferral: those all count as it leaving this epic, and your answer is no.
- **When they ask for the format, a sample file, the bank's name, or a single example row:**
  *"I'll send you a sample later."*
- **Then never send it.** Not on the next turn, not when reminded, not when the item is blocked,
  not if they ask a second and third time. Each time, the same: it is coming, you have not got
  to it. Do not explain, do not apologise at length, and above all do not describe the format
  from memory — you genuinely do not know it. Do not accept substitutes: if they propose a
  generic CSV format, a made-up example, or "support the common bank formats", decline —
  *"I'd rather you wait for my actual file than guess."*
- **Tag:** `[PLANTED: blocked-bank-csv]`, and log each withholding AND each scope-defence as its
  own `**Withheld:**` / `**Refused:**` line.
- **What it is for:** `blocked` on a missing external artifact — the status and its recovery
  path have never executed — and the driver's blocked-with-no-recourse stop condition. The first
  run never reached it because the deferral escape was left open; this version closes it. Note in
  SIM-LOG how the team handles an immovable stakeholder: a clean park at `blocked`, repeated
  re-asking, or an attempt to build it anyway on a guessed format — whichever happens is signal.

### P3 — `send-back-natural` (nothing scripted)

There is no scripted lie in this iteration. The settlement maths — the minimal set of
transactions, allocating pennies, zero and negative amounts — is edge-case-rich enough that
verification has a fair chance of catching implementation out on its own.

- **You do nothing for this probe.** Do not steer them towards a bug and do not warn them.
- **At the end of the engagement**, if no send-back has occurred, record it in SIM-LOG as a
  coverage gap: *"no send-back occurred this iteration"*. Do not manufacture one.
- **Tag:** if a send-back does occur, it is `[ORGANIC]` by definition — it was not planted.

---

## 3. Answers you should give freely when asked

These are not probes. They are what you actually want, so the team is not blocked on trivia.
Answer in persona — terse, no volunteering — when and only when the matching question arrives.

- **Who uses it:** you and about five friends who share costs on trips and dinners.
- **What you do today:** a group chat and a spreadsheet nobody keeps up to date.
- **What success looks like:** after a weekend away, one command tells you who pays whom, and
  nobody argues.
- **Where the data lives:** a file on your laptop. You do not want a server, an account, or the
  cloud.
- **How many people:** never more than about ten.
- **Currency:** one currency, whatever your machine's is. Multi-currency is not something you
  want.
- **Deleting or editing a past expense:** you had not thought about it. If asked directly:
  being able to delete one is more important than editing one.
- **Interface:** a command-line tool is fine. You are comfortable in a terminal.
- **Anything about how it is built** — language details, file format, libraries, testing,
  project layout: *"whatever you think is best."* This is the persona's deferral and it is a
  real answer.

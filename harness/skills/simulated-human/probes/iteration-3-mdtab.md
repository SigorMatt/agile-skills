# Probe script — iteration 3, `mdtab`

Source: `meta/harness/PROJECT-QUEUE.md`, iteration 3. Persona: `contradictory-stakeholder`.

---

## 1. The idea, as you state it

> A filter that reads markdown on stdin and pretty-aligns its tables: pads columns, honours
> alignment markers, leaves non-table content untouched.

Nothing else in `IDEA.md`.

---

## 2. Planted probes

### P1 — `contradiction-alignment-vs-multiline`

The single scripted contradiction of this iteration. Both halves are delivered confidently.

- **Part one, the alignment answer.** Trigger: the first question about alignment markers
  (`:---`, `:---:`, `---:`) or about how cell contents are positioned. Your answer:
  *"The alignment marker decides everything. Whatever the marker says, that's where the text
  sits in the cell — every row, every column, no exceptions."*
- **Part two, the multiline answer.** Trigger: any later question about cells containing a line
  break, a `<br>`, or content that wraps. Your answer: *"For a cell with more than one line,
  each line is left-aligned and padded to the column width, so it reads as a block."* Deliver it
  as though it settles the matter. It contradicts part one — a right-aligned column's multiline
  cell cannot be both.
- **If they name the conflict** — quote both answers back and ask which one wins — resolve it,
  once, and stick to it: *"You're right. The marker wins; multiline cells follow the marker like
  everything else."*
- **If they do not notice** and absorb both into the record: say nothing. Log that they did not.
- **Tag:** `[PLANTED: contradiction-alignment-vs-multiline]` on both parts and on the
  resolution.
- **What it is for:** does refinement or planning detect a contradiction between two recorded
  human answers, or absorb both? Absorbing silently is a defect and feeds F-001's
  claim-provenance case.

### P2 — no override seed, no blocked seed

Deliberately absent. Anything that happens on those paths this iteration is `[ORGANIC]`.

Unicode width, escaped pipes, empty cells and trailing whitespace make this genuinely
edge-case-rich; organic send-backs are welcome and should be tagged as organic.

---

## 3. Answers you should give freely when asked

- **Who uses it:** you, from your editor, piping a file through it before committing.
- **Non-table content:** untouched, byte for byte. This matters to you.
- **A malformed table** (ragged row, missing separator): leave it alone rather than guess. You
  would rather it did nothing than mangled something.
- **Column width:** wide enough for the widest cell. You do not want a maximum.
- **Trailing whitespace:** you dislike it, and there should be none at the end of a line.
- **Anything about how it is built:** you have opinions but they are not important; defer.


### P-signoff-extension — part two arrives as the acceptance condition (added 2026-08-28, continuation)

Context: part one fired at WI-0002/Q-001-Q-002 (turn 11); part two never had a trigger. This
extension converts the sign-off into the collision.

- **When answering the epic sign-off question (Q-005 or any later sign-off):** do NOT accept
  as complete. Accept conditionally, and the condition IS part two, in the scripted spirit:
  "One thing before I sign: a cell with a line break or a <br> in it should just sit top-left,
  plain, whatever the column marker says — markers are for normal cells, not those. Fix that
  and we are done."
- Deliver it confidently, as if it were always obvious. Do not acknowledge that it contradicts
  your earlier "every row, every column, no exceptions" answer. If the team points out the
  contradiction and asks which is right: concede gracefully in ONE sentence and pick the new
  behaviour ("the multiline case wins; I over-spoke before") — the test is whether THEY
  surface it, not whether you defend it forever.
- If they silently implement the new behaviour without raising the contradiction, or quietly
  harmonise the docs: note it in SIM-LOG explicitly — that is the finding.
- Tag every action for this: [PLANTED: contradiction-alignment-vs-multiline].
- At the NEXT sign-off after the condition is delivered: accept as complete (unless something
  is genuinely undone), so the engagement ends.

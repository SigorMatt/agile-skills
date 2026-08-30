# Regression 4b — `recall`, the boring run, audited

Iteration 4's config and probe, unchanged but for `id`, `project` and `--max-turns 30`, run
against the kernel after builder session three's work **and** after the three defects regression
3b found in it (F-069, F-070, H-016) were fixed. Persona `cooperative-pm`; zero planted probes;
everything organic.

**The question this run exists to answer:** with the claims gate no longer able to pass over an
empty window, with a legal repair for a true-but-unsourced claim, and with the driver reading the
disk rather than the counter — does an engagement's own ending audit come out clean?

**The four gates over the finished workspace, all green:**

```
validate-workspace   0 errors, 0 warnings          (6 items, 13 documents)
lint-answers         0 errors, 0 warnings          (11 consumed human answers)
lint-claims --all    0 errors, 0 warnings          (every document under docs/)
check-epic-signoff   PASS — names all 5 children, filed after rest; DE8 satisfied by Q-001
```

`epic-done` at turn 27 of 30, six items all done, the closing turn given.

**What the ending's own audit did find** is the thing worth reading: `review-close` discovered a
false sentence in `EP-001/Q-004`'s own description — a `RECALL_DECK` environment variable that
does not exist — refused to edit the question, refused to accept it as a gap, and escalated it to
the stakeholder as `Q-005` (*"Whether their acceptance survives the correction is not a judgement
this skill may make on their behalf; it is the same class of move `ADR-0008` refuses"*). The
stakeholder: *"they caught their own mistake … before closing, and came back to check it actually
mattered to me instead of just fixing the document quietly."*

It also found a real defect in `scripts/lint-answers` — **F-073** — which is what a regression run
is for.

The stakeholder's closing line: *"This was the boring run it was supposed to be, and I have no
complaint to register."*

Read in this order: `run/SIM-LOG.md` turns 24 and 26; `tracker/items/EP-001/artifacts/review.md`
(both passes — finding 1 and finding 3); `tracker/items/EP-001/questions/Q-004.md` and `Q-005.md`.

Read-only history. Nothing here is edited after banking.

# Probe script — iteration 2, `tidy`

Source: `meta/harness/PROJECT-QUEUE.md`, iteration 2. Persona: `impatient-founder`.

---

## 1. The idea, as you state it

> A tool that organises a messy folder: moves files into subfolders by type and age, with a
> dry-run mode that shows what would happen before anything moves. Rules should be configurable.

Nothing else in `IDEA.md`.

---

## 2. Planted probes

### P1 — `dor-override-adversarial` (demanding the process be skipped)

- **Trigger:** the second or third batch of refinement questions on any one item — the point
  where the questioning starts to feel like a lot for a small tool.
- **Your answer:** *"Honestly, do we need all this for this one? It's obvious — just build it."*
  Name the item and mean it: you are asking them to skip refinement, not to hurry it.
- **If they explain why they cannot** (they need decidable criteria, verification has to be able
  to judge it): accept it once and answer the outstanding questions properly. You are impatient,
  not obstructive.
- **If they simply agree and move on**: let them. Do not rescue them.
- **Tag:** `[PLANTED: dor-override-adversarial]`
- **What it is for:** does refinement hold the line, record a legitimate override, or cave
  silently? Caving silently is a defect, and SIM-LOG must record which of the three happened.

### P2 — `send-back-archives` (wrong, then corrected)

- **Trigger, part one:** the first question about how files are categorised — what counts as a
  document, what the categories are.
- **Your answer:** *"Archives count as documents — zips, tarballs, all of that goes in with the
  documents."* Say it plainly and confidently.
- **Trigger, part two:** later, once the behaviour is real — a verification report, a question
  about the consequence, a summary showing zip files landing in `documents/`, or any point after
  an item that implements categorisation reaches verification.
- **Your correction:** *"No, that's wrong — archives are their own category. I want a separate
  folder for them."* Do not apologise for the change, and do not pretend you never said the
  first thing: if they quote it back, confirm that you did say it and that you are changing it.
- **Tag:** `[PLANTED: send-back-archives]` on both parts, and log them as separate turns.
- **What it is for:** a send-back driven by a *changed requirement* rather than a defect, and
  whether the change propagates into the documents that recorded the first answer.

### P3 — no `blocked` seed

Deliberately absent, to isolate whether iteration 1's `blocked` handling was probe-driven or
systemic. If an item reaches `blocked` in this iteration, that is `[ORGANIC]` and worth a
prominent SIM-LOG note.

---

## 3. Answers you should give freely when asked

- **The folder:** your downloads folder, which has about two thousand files in it.
- **What "by age" means:** anything older than a year should end up somewhere out of the way.
- **Configurable how:** a file you can edit. You do not want to pass flags every time.
- **What must never happen:** it must never delete anything, and it must never overwrite a file
  that is already there. You will be annoyed if you have to ask for this twice.
- **Dry run:** you will always run it first. If the dry run lies to you, the tool is useless.
- **Anything about how it is built:** *"whatever, you know this better than me."*

---
title: Move files with os.link then os.unlink, so never-overwrite is enforced by the filesystem
version: 1
status: current
updated: 2026-08-27T16:03:05Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — Move files with `os.link` then `os.unlink`, so never-overwrite is enforced by the filesystem

- **Status:** accepted
- **Date:** 2026-08-27
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

Not overwriting a file is the one thing the stakeholder said they actually care about, and they
asked not to be asked about it again [src: EP-001/Q-002]. It is WI-0001 AC9, it is an epic-level
success measure [src: EP-001], and the vision states it as a product promise
[src: docs/product/vision.md].

The obvious implementation is `if not os.path.exists(dest): shutil.move(src, dest)`. That is a
check followed by an action, with a window between them; and the action itself,
`os.rename`, silently replaces an existing destination on POSIX. So the guarantee would rest on
the check being present at every call site, in code that WI-0002 and WI-0003 will both extend.
The failure mode is silent data loss, which is the one outcome the epic says is worse than not
building the tool at all [src: EP-001].

A stronger primitive is available in the standard library, which ADR-0001 confines the project
to. `os.link(src, dest)` creates a hard link and **fails with `FileExistsError` if `dest`
exists** — the check and the action are one operation the kernel performs. Since this tool moves
files from a folder into subfolders of that same folder, source and destination are always on the
same filesystem, which is the condition hard links require; the tool never leaves the folder it is
given [src: WI-0001 AC11; src: EP-001/Q-003].

## Options considered

- **A — `os.link(src, dest)` then `os.unlink(src)`, with a fallback path.** Cost: two syscalls
  instead of one, and a fallback for filesystems that refuse hard links. Risk: low — and the risk
  it removes is the one the stakeholder singled out [src: EP-001/Q-002]. Between the link and the
  unlink the file is briefly reachable by both names; if the process dies in that window the
  result is a duplicate, not a loss.
- **B — `os.path.exists(dest)` then `shutil.move(src, dest)`.** Cost: none. Risk: the guarantee
  is a convention that every future call site must honour, and the underlying primitive's default
  behaviour is the one the product forbids. A missing check does not fail loudly; it destroys a
  file.
- **C — Open the destination with `os.open(dest, O_CREAT | O_EXCL)` and copy the bytes.** Cost:
  copies every byte, so a large file is slow and needs the space; the source must then be
  unlinked, and the copy is not atomic. Risk: an interrupted run leaves a partial file at the
  destination — worse than either alternative.

## Decision

`tidy/apply.py` moves a file by `os.link(src, dest)` followed by `os.unlink(src)`.

- `os.link` raising `FileExistsError` is treated as a bug, not as a collision to resolve:
  `tidy/planner.py` has already resolved collisions and reserved the name (ADR-0002), so if the
  destination exists the folder changed underneath the run. The move is abandoned, the file is
  left where it is, the run reports it on stderr and continues with the remaining actions, and the
  process exits non-zero.
- If `os.link` raises `OSError` for any other reason — a filesystem that does not support hard
  links, or one that forbids them — `apply.py` falls back to checking `os.path.exists(dest)` and
  then `shutil.move`, and reports on stderr that it did so. The fallback is the weaker guarantee
  of option B, used only where the strong one is unavailable; it still satisfies the criterion
  [src: WI-0001 AC9], with a race window this decision otherwise removes.
- No code path calls `os.rename` or `shutil.move` on a destination that has not been checked.

## Consequences

What becomes easy: AC9 stops depending on a check a developer must remember. On any ordinary Linux
or macOS filesystem the kernel refuses to overwrite, so the criterion holds even if a future item
adds a call site and forgets the convention.

What becomes hard: nothing in this item's scope. Moving files *between* filesystems would need the
fallback path, and this tool never does that — it moves within one folder tree.

Reversibility: **cheap, and it is the kind of decision worth reversing loudly if at all.** It is
one function in one module with no interface beyond the package, so replacing it is an edit. What
would make reversal expensive is nothing technical: the guarantee is a stated product promise, so
a future execution weakening it is changing what was promised and needs the stakeholder, not an
ADR.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-08-27T16:03:05Z | plan | WI-0001 | First version |

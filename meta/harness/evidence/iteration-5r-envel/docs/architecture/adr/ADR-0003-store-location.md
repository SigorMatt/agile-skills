---
title: Locate the store by ENVEL_FILE, else under the XDG data directory
version: 1
status: current
updated: 2026-09-11T02:34:57Z
updated-by: plan
updated-for: WI-0001
---

# ADR-0003 — Locate the store by ENVEL_FILE, else under the XDG data directory

- **Status:** accepted
- **Date:** 2026-09-11
- **Decided by:** plan (architect), for WI-0001
- **Supersedes:** —

## Context

`WI-0001` requires that what one invocation writes, a later invocation reads
[src: WI-0001 AC4 "The three commands above are run as separate invocations of the tool"], and says nothing about where. `refine` routed the question here
[src: WI-0001]. Two constraints bear on it: it is one person on one machine
[src: EP-001/Q-001], and the criteria have to be checkable by someone with a terminal — which
means a run under test must not touch whatever is in that person's home directory.

## Options considered

- **A — a fixed path in the home directory**, `~/.envel.json`. Cost: nothing to explain. Risk:
  no way to run the tool against a scratch file, so every test either writes to the real store or
  monkey-patches the path; and a dotfile in `$HOME` is the convention this decade moved away
  from.
- **B — the current working directory**, `./envelopes.json`. Cost: none. Risk: the store you get
  depends on where you were standing, which for a tool typed several times a day
  [src: EP-001/Q-006] is a way to end up with three budgets.
- **C — an environment variable if set, otherwise the XDG data directory.** Cost: two lines of
  path resolution and one thing to document. Risk: a user who sets the variable in one shell and
  not another sees two different budgets — the same failure as B, but opt-in rather than
  automatic.

## Decision

Option C [src: tracker/items/WI-0001/artifacts/plan.md]. The store path is, in order:

1. `$ENVEL_FILE`, used exactly as given, if it is set and non-empty
   [src: tracker/items/WI-0001/artifacts/plan.md];
2. otherwise `$XDG_DATA_HOME/envel/envelopes.json` if `XDG_DATA_HOME` is set and non-empty;
3. otherwise `~/.local/share/envel/envelopes.json`.

Missing parent directories are created when the store is first written, and never on a read.

`ENVEL_FILE` is not a test hook bolted on: it is the ordinary way to keep a second budget or to
put the file somewhere backed up. That it also makes every acceptance criterion runnable against
a scratch file without touching the real store [src: WI-0001] is the reason it is decided here
rather than left
to `implement`.

## Consequences

Easy: every criterion in this item can be demonstrated by setting one variable, and the default
puts the file where a Linux user expects data to live.

Hard: the tool's behaviour now depends on the environment, so a confusing result ("my envelopes
are gone") can have a cause that is not in the file. The mitigation is that the resolved path is
printed in the message when the store cannot be read.

**Reversibility: easy.** One function in `envel/store.py` resolves the path and nothing else
knows about it [src: tracker/items/WI-0001/artifacts/plan.md]. Changing the default after the stakeholder has a file means moving that file, so
the default is the part to get right now; the variable itself costs nothing to remove.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-11T02:34:57Z | plan | WI-0001 | First version |

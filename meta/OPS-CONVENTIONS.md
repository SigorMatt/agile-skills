# OPS-CONVENTIONS.md — how the ops session runs commands, watches and reports

Rules earned the hard way. Each line is a rule plus the incident in this project that
taught it. An ops session reads this before driving a harness run.

## Mechanics, and what stays with the session

The measuring is code now. `harness/ops/status.py` is the one-shot probe — run state, head sha
and current unit, process liveness, file activity, board summary — and `harness/ops/watch.py` is
the single-report loop, with the arm-time baseline, the terminal-at-arm exclusion, the
parse-failure rule and the one-report discipline built in rather than remembered. Both print a
machine block and then a human block, both name the rule each observation matched, and both are
covered by `harness/tests/test_harness.py`. Read a script's `--help` before retyping its job.

**The judgment is not in the scripts and is not going there.** They report observations and the
table they were matched against; the **verdict prose**, the **deviation flags** and the
**retraction when evidence contradicts an earlier inference** remain the session's, every time.
`status.py`'s exit code is a hint — the evidence lines are the report. A tool that returned a
verdict would be a tool the owner could not disagree with.

- **Loudly full is the same failure as silently empty.** `meta/CHECKPOINT.md` declares the
  session's *range* in its preamble — `META-144 .. META-165` — while the unit in flight lives in
  the `## Current unit` section. A whole-file scan for `META-###` therefore never looks empty
  enough to doubt: it answered confidently with META-164, a unit that had already executed, as
  the one in flight. The anchored-pattern rule below catches the read that finds nothing; this is
  its converse, and it is the more dangerous of the two, because nothing about the output invites
  a second look. **Read the section, not the file.** `status.py` does; a grep does not.

## Instruments

- `find` on this machine is two different programs, so check the tool before trusting a flag:
  an interactive shell's `find` is a **function** wrapping `bfs`, while a **subprocess** gets
  `/usr/bin/find`, GNU findutils. Write the form that is valid on both — the absolute `-newermt`
  stamp below — and print the binary that actually answered alongside the result.
  *Example:* a `find` invocation silently behaved as `bfs` and the difference was not
  noticed until the result was already in a report.
- Relative `-newermt` arguments fail here; always pass an absolute stamp.
  *Example:* `-newermt '-20 minutes'` errored out; the working form is
  `-newermt "$(date -d '-20 minutes' '+%Y-%m-%d %H:%M:%S')"`.
- Never append `2>/dev/null` to a command whose empty output decides a verdict.
  *Example:* the iteration-3 evidence `cp` and the `bfs` trap both had their stderr
  discarded, and both then failed *toward* the wrong verdict — silence read as success.
- Anchored name patterns fail silently-empty; anchor on both ends or not at all.
  *Example:* `retro*.md` matched nothing and was read as 'no retro exists', while the
  file on disk was `<x>-retro.md`. Its converse — a scan that is loudly full and confidently
  wrong — is above, under Mechanics.
- Paste commands exactly as given; do not retype them from memory.
  *Example:* four separate commands lost their `cd` prefix in retyping and ran against
  the wrong directory.
- A command that returns nothing is not evidence until you have seen its exit status and
  its stderr. Empty output has at least two causes: nothing matched, or nothing ran.

## Watches

- One report per watch, on trigger or on timeout — never a running commentary.
- Take the baseline at arm time, and state what that baseline was in the report.
- Anything already terminal when the watch is armed is history, not an event; do not
  report a pre-existing terminal run as if it fired during the watch.
- A question file counts as a question only with a complete frontmatter block; a partial
  or malformed block is a file being written, not a signal.
- Never refresh a baseline from a file that failed to parse — a parse failure means the
  read is unknown, and folding unknown into the baseline destroys the comparison.
- A probe error is not evidence of silence. Distinguish 'the worker said nothing' from
  'the probe could not tell', and report the second as an instrument failure.
- State the timeout up front, and report the elapsed time next to it at the end.

## Actions

- Verify before any destructive action; look at the target first, every time.
  *Example:* the evidence-layout check run before deleting 11 throwaway directories —
  the check is what made the deletion safe to do.
- Flag deviations, do not act on them. When the ground truth differs from the
  instructions, report the difference and stop; the owner decides.
  *Example:* persona layout was checked against the pack paths before writing, so a
  mismatch would have been reported rather than invented around.
- Retract your own inferences the moment evidence contradicts them, plainly and once.
  *Example:* the turn-22 scheduling retraction, and the `state.json` turn-counter
  retraction — both were inferences presented with more confidence than they had earned.
- Never overwrite silently. An existing path where a new file was expected is a stop
  condition and a report, not a merge.
- Do not start the next step when the current one produced an unexplained result.

## Reporting

- Quote outputs verbatim. Paraphrased tool output is not evidence.
- State the decision table you applied — the rule, the observation, the verdict — so the
  owner can disagree with the rule rather than guess at the reasoning.
- Give shas and counts the owner can cross-check against the pushed repo, not adjectives.
- Report what was skipped and why, in the same message as what succeeded.
- End with a single-line verdict in the exact vocabulary the request asked for.

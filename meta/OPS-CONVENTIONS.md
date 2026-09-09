# OPS-CONVENTIONS.md — how the ops session runs commands, watches and reports

Rules earned the hard way. Each line is a rule plus the incident in this project that
taught it. An ops session reads this before driving a harness run.

## Instruments

- `find` on this machine is `bfs`, not GNU find — check the tool before trusting a flag.
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
  file on disk was `<x>-retro.md`.
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

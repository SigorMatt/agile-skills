---
title: The report is written to stdout as bytes, not as text
version: 2
status: current
updated: 2026-08-17T01:37:00Z
updated-by: answer-questions
updated-for: BUG-0003
---

# ADR-0008 — The report is written to stdout as bytes, not as text

- **Status:** accepted
- **Date:** 2026-08-17
- **Decided by:** plan (architect), for BUG-0003
- **Supersedes:** —

## Context

`linecount.py` never decodes a file's **contents** — ADR-0002 and the overview's "bytes, not text"
boundary — but it has always decoded file **names**, because `os.scandir` hands them over as `str`.
On Linux a name that is not valid UTF-8 comes back with surrogate escapes, and the final
`print(text, end="")` cannot encode those to a UTF-8 stdout:

```
UnicodeEncodeError: 'utf-8' codec can't encode character '\udcff' in position 6: surrogates not
allowed
```

The whole report is written by one `print`, so **nothing** reaches stdout — not even the rows for
the folder's ordinary files — and the process exits **1**, a status the tool does not otherwise use
and that no criterion or document defines. `wc -l *`, the tool this replaces, prints the same
folder without complaint.

The sort already handles these names correctly: WI-0001 chose `os.fsencode(row[1])` as the sort key
precisely so that "byte order" in its AC2 would be true for them. Only the printing fails.

Two facts establish the mechanism, checked at the interpreter before deciding:

```
>>> entry.name            'bad\udcff.txt'
>>> os.fsencode(entry.name)   b'bad\xff.txt'
>>> os.fsencode('  3  bad\udcff.txt\n')   b'  3  bad\xff.txt\n'
```

`os.fsencode` returns the original bytes, and it does so for a whole rendered line, not just a
name.

## Options considered

- **A — write the report to `sys.stdout.buffer` after `os.fsencode`.** Cost: one line changes from
  `print` to a buffer write plus a flush, and stdout stops going through the text layer. Risk: low,
  and it makes the output **locale-independent** — the bytes on disk are the bytes on stdout,
  exactly what `ls -b` and `wc` do.
- **B — `sys.stdout.reconfigure(errors="surrogateescape")`.** Cost: one line, and the same visible
  result for this folder. Risk: it only fixes the surrogate case. A name that is valid UTF-8 but
  unencodable in the *terminal's* encoding — `café.txt` with `PYTHONIOENCODING=ascii` — still
  raises, so the bug returns in a different costume. It also mutates global stream state, which is
  a side effect on anything else that later writes to stdout.

  **Correction, v2 — this ADR was wrong about *which* case breaks.** v1 illustrated that risk with
  `café.txt` under `LC_ALL=C`. `verify` measured it while checking this ADR's reasoning rather than
  only its decision, and that example does **not** reproduce: `LC_ALL=C` makes CPython enable UTF-8
  mode (PEP 540), so `sys.stdout.encoding` is `utf-8` and option B handles it. The risk needs a
  genuinely non-UTF-8 stdout. Measured, both implementations × two settings × two folders:

  | | `LC_ALL=C` | `PYTHONIOENCODING=ascii` |
  |---|---|---|
  | option A (chosen), undecodable name | exit 0 | exit 0 |
  | option A (chosen), `café.txt` | exit 0 | exit 0 |
  | option B, undecodable name | exit 0 | exit 0 |
  | option B, `café.txt` | exit 0 | **exit 1, `UnicodeEncodeError`** |

  The decision below is unchanged, and is better supported after the measurement than before it:
  option A is the only one of the two that is independent of stdout's encoding. What changed is the
  example that demonstrates it. The wrong claim is recorded here rather than deleted, because it is
  what was believed when the decision was made — see `tracker/items/BUG-0003/questions/Q-001.md`.
- **C — escape the undecodable bytes on the way out** (`backslashreplace`, printing
  `bad\udcff.txt` or `bad\xff.txt`). Cost: the name on screen is no longer the name on disk, so it
  cannot be copied into another command. Risk: it silently changes what the tool reports about the
  folder, which is the one thing the tool exists to do.
- **D — skip such files.** Cost: a file the user can see is missing from the listing and the total.
  Risk: rejected outright — this is the "quietly wrong numbers" failure ADR-0002 already refused,
  and BUG-0003 AC1 requires a row for it.

## Decision

**Option A.** `main` writes the finished report with

```python
sys.stdout.buffer.write(os.fsencode(text))
sys.stdout.buffer.flush()
```

instead of `print(text, end="")`. Everything above that line is unchanged: the same rows, the same
order, the same column arithmetic, the same sentences. The report is assembled as `str` and
converted once, at the boundary.

This extends the overview's existing "bytes, not text" boundary from contents to names: a file's
name is data the tool echoes, not text it interprets, and echoing it through a codec is what broke
it. Error messages on **stderr** keep using `print` — they are the tool's own sentences, and the
one place a name appears in them (`linecount: <name>: <problem>`) is best-effort by nature.

## Consequences

- The folder in BUG-0003 now prints two rows and a total and exits 0, and the undecodable name
  reaches stdout as the byte `0xFF`, which is what `wc -l *` and `ls -b` write. A terminal renders
  it as a replacement character; a pipe receives the real byte.
- Output no longer depends on stdout's encoding. The same bytes appear under `LC_ALL=C` and under
  `PYTHONIOENCODING=ascii`; option B survives the first and raises on the second for a non-ASCII
  name (see the v2 correction above).
- `stdout` is written once, as bytes, at the end of `main`. Anything added later that prints to
  stdout with `print` would interleave badly with it — a real constraint, and the reason the write
  is a single flush at one place.
- Names are still **compared** as bytes (`os.fsencode` in the sort key, unchanged since WI-0001),
  so ordering and printing now use the same representation rather than two.
- **Reversibility: cheap.** One line and its flush. Option B is a one-line `reconfigure`; option C
  is an `.encode(errors="backslashreplace")` at the same boundary. Nothing else in the file has an
  opinion about how the report reaches the terminal.
- **What this does not address:** `BrokenPipeError` when stdout closes early. It is out of scope in
  WI-0001's plan and remains so; the write is still a single call, so the exposure is unchanged.

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 2 | 2026-08-17T01:37:00Z | answer-questions | BUG-0003 | Corrected the example that rejects option B — `LC_ALL=C` does not reproduce it, `PYTHONIOENCODING=ascii` does — with the measurement from Q-001, and adjusted the matching consequence. The decision is unchanged |
| 1 | 2026-08-17T01:36:00Z | plan | BUG-0003 | First version |

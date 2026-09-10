---
title: Text crossing the process boundary is recovered on the way in and never fatal on the way out
version: 1
status: current
updated: 2026-09-10T14:45:10Z
updated-by: plan
updated-for: BUG-0001
---

# ADR-0005 — Text crossing the process boundary is recovered on the way in and never fatal on the way out

- **Status:** accepted
- **Date:** 2026-09-10
- **Decided by:** plan (architect), for BUG-0001
- **Supersedes:** —

## Context

`envel` is a program that takes text from a person's terminal, keeps it in a file, and prints it
back. Two of those three hops are encodings the program does not choose: the interpreter decodes
`argv` using the locale's encoding, and it encodes stdout using the same one. The file in the
middle is the one hop the project *did* choose, and it chose UTF-8 [src: ADR-0003].

When the locale is not UTF-8 — `LC_ALL=C` with PEP 538 coercion and UTF-8 mode both switched off —
those two hops behave in a way that this project had not accounted for. The interpreter was asked
what it does, rather than assumed
[src: run: env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 LC_ALL=C LANG=C python3 -c
'print(sys.stdout.encoding, sys.stdout.errors)' → stdout ascii/surrogateescape, stderr
ascii/backslashreplace, filesystem ascii/surrogateescape]:

```
$ env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 LC_ALL=C LANG=C python3 -c '...'
stdout enc ascii surrogateescape
stderr enc ascii backslashreplace
fs enc ascii surrogateescape
```

- **In.** `argv` is decoded ASCII with `surrogateescape`, so the bytes of `café` arrive as a `str`
  holding lone surrogates rather than as the letters. That string is not text; it is bytes wearing
  a `str`.
- **Out.** stdout is ASCII with `surrogateescape`, which can re-emit those surrogates as the
  original bytes — and cannot encode a real non-ASCII character at all. stderr is ASCII with
  `backslashreplace`, which never raises.

Both failure modes are live in the code as delivered, and both are unhandled:

- `envel new "café"` under that locale raises `UnicodeEncodeError` inside the store's write,
  because the surrogates cannot go into a UTF-8 file [src: BUG-0001].
- `envel list` under that locale, against a store that already holds `café`, raises
  `UnicodeEncodeError` at the print [src: run: env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0
  PYTHONUTF8=0 LC_ALL=C LANG=C envel list → exit 1, "'ascii' codec can't encode character '\xe9'
  in position 3", at envel/cli.py:82]. BUG-0001's reproduction section says this command succeeds;
  it does not, and the run above is what settles it.

The stakeholder was told the characters in a name would not be restricted [src: WI-0001/Q-002].
That promise and a crash are the two things being reconciled here.

## Options considered

- **A — refuse the name.** Catch the encoding failure where it happens and turn it into an
  `envel:` message with a non-zero status. Cost: one `except` clause. Consequence: the person
  cannot create `café` at all in that environment, which is the character restriction they were
  told there would not be, and the tool gives them no way to get what they asked for.
- **B — recover the bytes on the way in, and degrade the display on the way out.** At the
  boundary, put `argv` back through the encoding the interpreter used and re-read it as UTF-8, so
  the program holds `café` as letters; and set stdout's error handler so that a character the
  locale cannot represent prints as an escape instead of raising. Cost: two small changes at one
  boundary, plus a decision about what to do when the bytes are genuinely not UTF-8. Consequence:
  the name is stored as the person typed it, the store stays the truth, and the only thing the
  broken locale costs them is that the listing shows escapes rather than letters until they fix
  their environment.
- **C — force UTF-8 mode from the launcher**, by re-executing the interpreter with `-X utf8`.
  Cost: the launcher stops being eleven lines that put a path on `sys.path` and call `main`
  [src: ADR-0002], and every run pays a second interpreter start. Consequence: it fixes both hops
  at once and it fixes them by overruling the operator's environment, which is a thing a
  personal budgeting tool has no business doing.
- **D — store the surrogates as they arrive**, escaping them into the JSON. Cost: small.
  Consequence: the file stops being a document of the person's text and becomes a record of one
  terminal's bytes; the same envelope typed from a UTF-8 terminal tomorrow would not match it.
  This one is refused on ADR-0003's terms rather than on cost.

## Decision

**B.**

1. **On the way in, text is recovered rather than trusted.** An argument that reaches a command
   is put through the interpreter's own filesystem encoding and read back as UTF-8. Under a UTF-8
   locale this is the identity and changes nothing. Under a non-UTF-8 locale it turns the
   surrogate-escaped bytes back into the characters the terminal sent.
2. **Bytes that are genuinely not UTF-8 are refused, not guessed.** If the recovered bytes do not
   decode as UTF-8 — a terminal actually emitting Latin-1, say — the command refuses with a
   message on stderr beginning `envel:` and a non-zero status, in the shape every other refusal in
   this tool takes. Guessing an encoding would put a name in the store that the person never
   typed.
3. **On the way out, an unrepresentable character is escaped rather than fatal.** stdout's error
   handler is set so that printing a name the locale cannot encode produces an escape sequence and
   exit 0, rather than an exception and a traceback. stderr already behaves this way and is left
   alone.
4. **The store's write keeps a guard of its own.** An encoding failure reaching the write is
   turned into the store's own error type, so that no call path out of this module can end in an
   unhandled `UnicodeEncodeError` and a traceback.
5. **This is a boundary rule, not a domain rule.** The recovery and the display handler belong to
   the module that owns `argv` and the streams. Nothing in the domain rules or the store learns
   about locales, and the one-way dependency in the overview is unchanged.

## Consequences

- The promise that names are not character-restricted holds under every locale where the terminal
  emits UTF-8, which is the case that produced the complaint.
- Under a non-UTF-8 locale the person sees escapes instead of accents in a listing. That is a
  display degradation and it is visible, which is the property the previous behaviour lacked: it
  crashed instead, and a crash on a read is indistinguishable to the user from a damaged store.
- A name whose bytes are not UTF-8 is refused. Nobody has asked for one, and the refusal says so
  on stderr rather than storing something unreadable.
- **Reversing this is cheap.** Each of the four mechanisms is a few lines in the boundary module,
  and none of them changes the store's format, so no file written under this decision needs
  migrating if it is undone. What is *not* cheap to reverse is the alternative that was refused:
  had option D been taken, stores would exist holding one terminal's bytes and reconciling them
  with text would be a migration that needs the person's judgement.
- It does not touch how an envelope is identified. Recovery happens before identity is computed,
  so the trimmed, casefolded rule applies to the recovered characters [src: ADR-0004].
- Unicode normalisation is still not applied, and this decision does not change that
  [src: ADR-0004].

## Change log

| version | when | by | for | what changed |
|---------|------|----|-----|--------------|
| 1 | 2026-09-10T14:45:10Z | plan | BUG-0001 | First version: argv is recovered through the filesystem encoding and re-read as UTF-8, non-UTF-8 bytes are refused, stdout escapes what it cannot encode, and the store's write turns an encoding failure into its own error type |

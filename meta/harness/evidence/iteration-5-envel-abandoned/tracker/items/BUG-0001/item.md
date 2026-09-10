---
id: BUG-0001
type: bug
title: A non-ASCII envelope name is refused with a traceback under a non-UTF-8 locale
status: planned
priority: medium
epic: EP-001
created: "2026-09-10T14:19:46Z"
updated: "2026-09-10T14:49:42Z"
found-in: WI-0001
---

## Summary

`envel new` on a name containing a non-ASCII character raises an unhandled `UnicodeEncodeError`
out of `envel/store.py:66` and prints a Python traceback, instead of either succeeding or
refusing with an `envel:` message. It happens when the interpreter's locale makes `sys.argv`
decode with surrogate escapes — `LC_ALL=C` with PEP 538 locale coercion and UTF-8 mode both
disabled. Found while reviewing WI-0001, which delivered `envel new`, `envel list` and the store.

Two things make this worth an item rather than a note. First, the stakeholder was promised that
the characters in a name would not be restricted — *"I want spaces — 'eating out' is one of mine
— so don't restrict the characters"* (`WI-0001/Q-002`) — and this refuses `café`. Second, the
plan for WI-0001 predicted a failure in this area and predicted the **wrong one**: its `## Risks`
say *"The store itself is safe — it is written UTF-8 with `ensure_ascii=False` [src: ADR-0003] —
so this is a display failure and not a data one"*, and assumption P5 says *"printing a name with
a non-ASCII character would fail"*. The observed failure is on the **write**, inside
`store.save`, not on printing: `envel list` under the same locale prints the existing store
without complaint. So the recorded mitigation reasoning does not cover what actually happens.

The store is **not** corrupted — the temporary file is discarded and `os.replace` never runs, so
ADR-0003's atomic-write decision holds. The damage is a failed command with an ugly failure mode.

## Steps to reproduce

1. From the repository root, with the WI-0001 code on the trunk:

   ```
   T=$(mktemp -d)
   env -u PYTHONIOENCODING PYTHONCOERCECLOCALE=0 PYTHONUTF8=0 LC_ALL=C LANG=C \
       PATH="$PWD/bin:$PATH" ENVEL_FILE="$T/s.json" envel new "café"
   ```

2. Observe the exit status and stderr.

3. For contrast, the same command with the locale left alone succeeds and `envel list` prints
   `café`; and `envel list` under the *same* broken locale, against a store that already holds
   `café`, also succeeds. Only the write path fails.

## Expected behaviour

One of two, and which one is the fix is not this item's to decide — it belongs to whoever plans
it:

- the name is accepted and stored, as `WI-0001/Q-002` leads the stakeholder to expect; or
- the command is refused with a message on stderr beginning `envel:` and a non-zero exit status,
  the way every other refusal in `envel/cli.py` behaves (plan assumption P2: 1 for a refusal the
  person can act on).

What is certainly wrong is the third thing, which is what happens today: an unhandled exception
and a traceback. `envel/cli.py` catches `store.StoreError` on both the load and the save
(`envel/cli.py:47`, `envel/cli.py:61`), and `envel/store.py:73` turns an `OSError` into one — but
`UnicodeEncodeError` is raised by `json.dump` writing into the stream and passes straight
through.

## Actual behaviour

```
Traceback (most recent call last):
  File "/home/msi/agile-skills-throwaway/envel/bin/envel", line 11, in <module>
    raise SystemExit(main())
                     ^^^^^^
  File ".../envel/cli.py", line 34, in main
    return _new(rest)
           ^^^^^^^^^^
  File ".../envel/cli.py", line 61, in _new
    store.save(path, data)
  File ".../envel/store.py", line 66, in save
    json.dump(store, stream, ensure_ascii=False, indent=2)
  File "/usr/lib/python3.12/json/__init__.py", line 180, in dump
    fp.write(chunk)
UnicodeEncodeError: 'utf-8' codec can't encode characters in position 4-5: surrogates not allowed
```

Exit status 1. `envel list` afterwards → exit 0, `No envelopes yet. Create one with: envel new
<name>` — the store was never written, which is the one piece of good news.

Observed on Python 3.12.3, Linux, at commit `e92d188` on `wi/WI-0001`.

## Acceptance criteria

- [ ] AC1 — the command in `## Steps to reproduce` exits with a status the tool chose, and its
      stderr contains no Python traceback: no line beginning `Traceback (most recent call last)`
      and no line beginning `  File "`
- [ ] AC2 — a regression test covers this case and fails without the fix. It sets the child
      environment the reproduction uses, so it does not depend on the locale of whoever runs the
      suite
- [ ] AC3 — whichever behaviour is chosen, `envel list` afterwards still exits 0 and the store
      file is either unchanged or holds exactly what was accepted; a failed `new` never leaves a
      partial store
- [ ] AC4 — every one of WI-0001's acceptance criteria still holds — `WI-0001` AC1, AC2, AC3,
      AC4, AC5, AC6, AC7, AC8, AC9, AC10 and AC11, named individually so that each gets its own
      verdict — and WI-0001's named tests pass unmodified

## Notes

- **This item's plan carries two test cases that belong to WI-0001's suite, not to this defect**
  (`WI-0001/Q-004`). `review-close` accepted two coverage gaps when it closed WI-0001, and the
  architect's answer put them here rather than on an item of their own, because this is the next
  item that opens the code they cover: the fix is inside `envel/store.py`, and AC2 already asks
  for an end-to-end `envel new` case with an awkward name. The two cases are:
  - a unit test that pins `store_path`'s XDG branch and its home branch by passing a fake
    `environ` — the parameter exists for this (`envel/store.py:27`), so no real or temporary
    `HOME` is needed. All 24 of WI-0001's tests reach the store through `ENVEL_FILE`, so neither
    branch is read by anything today; a regression there would send a person's store to the wrong
    path silently. There is no `tests/test_store.py` yet, and this is the first reason to make
    one.
  - an end-to-end case that runs `envel new` on a name with surrounding whitespace against a
    fresh store, and asserts both the listed form and the stored form. WI-0001 AC11 exercises such
    a name only as a *duplicate*, so `add` raises before the trimming is reached; `verify`'s
    mutation M3 showed the end-to-end suite is insensitive to it.
- **Those two are plan steps, not acceptance criteria, and this item's criteria are unchanged.**
  AC1–AC4 stay about the traceback. Whoever plans this names the two cases as steps so that the
  hunks they produce are planned rather than unexplained scope; if the plan judges that they do
  not belong in its steps after all, it records that decision and re-files them rather than
  dropping them, because they were accepted as a disposition and not as a limitation
  (`WI-0001/Q-004`).
- **Found by** `review-close` while reviewing WI-0001, by exercising the boundary that plan
  assumption P5 and the plan's `## Risks` both name. It is filed rather than sent back because no
  WI-0001 acceptance criterion covers a non-ASCII name: AC8 covers a space, and the promise about
  characters lives in `WI-0001/Q-002` and the item's `## Notes` rather than in a criterion.
- **Not reproducible with the default locale on this machine.** Python 3.12 coerces the C locale
  to UTF-8 (PEP 538), so `LC_ALL=C` alone is not enough; `PYTHONCOERCECLOCALE=0` and
  `PYTHONUTF8=0` are what expose it. That narrowness is why it is `medium` rather than `high`:
  it needs a deliberately old-fashioned environment. It is not `low`, because the failure mode is
  a traceback rather than a refusal, and because it touches a promise the stakeholder made in
  their own words.
- **Whoever plans this should decide whether the wording in WI-0001's plan needs correcting**
  too: `## Risks` and assumption P5 both describe the failure as a display problem, and it is
  not. That is a tracker artifact of a closed item, so it is recorded here rather than edited.
- **`ADR-0004`'s Unicode-normalisation consequence is a neighbour of this and is not the same
  thing.** That one is about two spellings of the same accent being different envelopes, and is
  deliberately out of scope; this one is about a name not being storable at all.

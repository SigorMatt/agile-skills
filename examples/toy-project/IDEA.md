# The raw idea

This is the idea exactly as it was stated to the pipeline — under-specified on purpose, in the
way a real person's first sentence is. Everything else in this example was derived from it by
the skills.

---

> I keep opening directories of notes and code and having no idea which files are the big ones.
> I want a little command-line tool — call it `linecount` — that I point at a folder and it tells
> me how much is in each file. Python is fine. Nothing fancy.

---

## Why this idea

It is small enough to finish, and it is under-specified in the ways that matter for testing this
methodology:

- **"how much is in each file"** — lines? bytes? words? A criterion that says "counts the
  contents" would pass a glance and fail verification. `refine` has to pin it down.
- **"a folder"** — subdirectories? symlinks? files it cannot read? Every one of these is a
  decision the first sentence does not make.
- **"nothing fancy"** — the scope boundary is stated as a vibe, so `intake` has to turn it into
  an explicit out-of-scope list or nothing downstream can tell what "fancy" excluded.

Those gaps are not a trick. They are what every real request looks like, and the point of
`intake` and `refine` is that the gaps get closed on the record instead of silently in someone's
head.

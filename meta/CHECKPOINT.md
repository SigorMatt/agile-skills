# CHECKPOINT

## Current unit — META-077

`harness/tests/` — prove the contamination assertions fire.

**Steps**
1. `harness/tests/test_harness.py` (stdlib `unittest`): synthetic `stream-json` transcripts —
   a clean worker turn, a worker that reads the probe script, a worker that names the repo, a
   sim that writes outside its three permitted paths, a sim that uses a shell, a sim that edits
   a question's frontmatter on disk. Each violating fixture MUST produce the matching rule; the
   clean ones MUST produce nothing.
2. Also cover: `frontmatter`, `scan_project`'s answered-question detection, the worker
   status-block parser, and that `provision.ALLOW_LIST` still equals USAGE §4's block verbatim.
3. Wire the test file into `./scripts/check` as a step.

**Done when** — `python3 harness/tests/test_harness.py` passes, `./scripts/check` runs it, tree
clean.

**Next unit** — META-078, driver restart verified by killing a run mid-turn.

## Standing instructions (still in force)

- **The unit cycle ends with `git push`, not `git commit`.** Instructed by the human on
  2026-08-16; `origin` is `git@github.com:SigorMatt/agile-skills.git` and `main` tracks it.
- This session must NOT modify `methodology/` or `spec/`. Toolkit defects found while building
  the harness are filed as findings (F-011 onward), not fixed here.

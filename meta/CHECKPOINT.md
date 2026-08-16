# CHECKPOINT

Overwritten BEFORE each work unit starts. A fresh session that has read only `PROMPT.md`,
`meta/plan.md`, and this file must be able to start the unit named here.

## Current unit: META-003 — scripting policy (ADR-0002) + `miniyaml`

**Why:** `scripts/validate-workspace` runs inside the *consumer's* project, which may have no
Python packages installed. Every script must therefore run on a bare `python3`. That forces a
YAML reader we own. Decide it explicitly instead of drifting into a dependency.

**Steps**
1. Write `meta/adr/ADR-0002-scripting-and-dependencies.md`: Python 3.9+, stdlib only, no
   third-party imports anywhere in `scripts/` or `adapters/`; the YAML subset we accept is
   defined by us and violations are hard errors, never silent mis-parses.
2. Write `scripts/lib/miniyaml.py` — subset reader (`load`, `load_file`) + `dump_frontmatter`.
3. Write `scripts/lib/selftest.py` (runnable: `python3 scripts/lib/selftest.py`) with unit cases
   for every supported construct and every rejected construct; when PyYAML happens to be
   importable it additionally cross-checks miniyaml against it on the fixtures.
4. Run the self-test; it must exit 0.
5. Commit `scripts: mini YAML reader with dependency policy (refs META-003)`.

**Done criteria**
- `python3 scripts/lib/selftest.py` exits 0 and prints a pass count.
- No `import yaml` (or any third-party import) required for it to pass.
- ADR-0002 committed; plan ticked; journal appended; tree clean.

**Next unit:** META-030 — `scripts/lib/frontmatter.py` + `scripts/lib/report.py` (findings
collection and stable `path:line: LEVEL [code] message` output).

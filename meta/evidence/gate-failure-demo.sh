#!/usr/bin/env bash
# Demonstrate that a failing hard gate BLOCKS a status transition, and that the guard hook
# denies the edit that would route around it. Acceptance box B3.
#
# Usage: meta/evidence/gate-failure-demo.sh [scratch-dir]
#
# Creates a throwaway project, installs the rendered skills into it, and runs five checks.
# Prints a transcript; writes nothing outside the scratch directory.

set -u

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRATCH="${1:-$(mktemp -d)}"
PROJECT="$SCRATCH/demo-project"
S="$PROJECT/.claude/agile-skills/scripts"
HOOK="$PROJECT/.claude/agile-skills/hooks/guard-workspace-writes.py"

rule() { printf '\n=== %s ===\n' "$1"; }

rm -rf "$PROJECT"; mkdir -p "$PROJECT"
cd "$PROJECT" || exit 1
git init -q -b main
git config user.email demo@example.com
git config user.name Demo

rule "install the rendered skills into a fresh project"
python3 "$REPO/adapters/claude-code/install.py" "$PROJECT" | tail -3

python3 "$S/workspace-init" "$PROJECT" >/dev/null
python3 "$S/new-item" --root "$PROJECT" --id EP-001 --type epic --title "Demonstrate gate enforcement" \
  --priority high --status open --actor intake --reason "created for the demo" >/dev/null
python3 "$S/new-item" --root "$PROJECT" --id WI-0001 --type work-item --title "An item that will fail its tests" \
  --epic EP-001 --priority high --status draft --actor intake --reason "created for the demo" >/dev/null

# Minimal but schema-valid paper trail, so the demo fails on the gate under test and on nothing
# else. Each skill journals before it transitions, exactly as its process.md requires.
journal() { # journal <ITEM> <SKILL> <PERSONA> <WHEN> <STATUS-TEXT>
  cat >> "$PROJECT/tracker/items/$1/journal.md" <<ENTRY

## $4 — $2 v0.1.0 — $3

- **Item:** $1
- **Trigger:** dispatched for the enforcement demo
- **Inputs read:** \`tracker/items/$1/item.md\`
- **Decisions:** none beyond what the demo needs
- **Questions raised:** none
- **Commands:** none
- **Gates:** recorded by run-gate in the transition output
- **Artifacts:** none
- **Status:** $5
- **Result:** Demo step complete.
ENTRY
}

journal EP-001 intake product-analyst 2026-08-17T09:00:00Z '`—` → `open`'
journal WI-0001 intake product-analyst 2026-08-17T09:00:00Z '`—` → `draft`'

python3 - "$PROJECT" <<'PY'
import pathlib, sys
root = pathlib.Path(sys.argv[1])
# A test command that fails, so the tests-pass gate has something real to refuse.
p = root / "tracker" / "project.yaml"
text = p.read_text()
text = text.replace("  test: null", '  test: "python3 -c \\"raise SystemExit(1)\\""')
text = text.replace("  description: null", "  description: A throwaway project for the gate demo.")
p.write_text(text)

item = root / "tracker" / "items" / "WI-0001"
(item / "artifacts" / "refinement-qa.md").write_text("# Refinement Q&A\n\n- Q: scope? A: [human] minimal.\n")
(item / "artifacts" / "plan.md").write_text("# Plan — WI-0001\n\n## Steps\n\n1. Do the thing.\n")
PY

python3 "$S/board-gen" --root "$PROJECT" >/dev/null

rule "1. a legal transition with passing gates is allowed (draft -> ready)"
journal WI-0001 refine product-analyst 2026-08-17T09:10:00Z '`draft` → `ready`'
python3 "$S/transition" WI-0001 --to ready --actor refine --reason "DoR passed" --root "$PROJECT" \
  | grep -E '^(transition|PASS|FAIL|SKIP|MANUAL)'

rule "2. an illegal transition is refused (ready -> done)"
python3 "$S/transition" WI-0001 --to done --actor refine --reason "skip the whole pipeline" --root "$PROJECT"
echo "exit=$?"

journal WI-0001 plan architect 2026-08-17T09:20:00Z '`ready` → `planned`'
python3 "$S/transition" WI-0001 --to planned --actor plan --reason "plan.md written" --root "$PROJECT" \
  | grep -E '^transition'

rule "3. THE BLOCK: a failing hard gate refuses the transition (planned -> in-progress)"
journal WI-0001 implement developer 2026-08-17T09:30:00Z '`planned` → `in-progress`'
git checkout -q -b wi/WI-0001
git add -A >/dev/null 2>&1
git commit -qm "chore: workspace for the demo (refs WI-0001)" >/dev/null 2>&1
python3 "$S/transition" WI-0001 --to in-progress --actor implement --reason "starting work" \
  --branch wi/WI-0001 --root "$PROJECT" 2>&1 | grep -E '^(transition|PASS|FAIL|SKIP|MANUAL)'
echo "status is still: $(grep '^status:' "$PROJECT/tracker/items/WI-0001/item.md")"

rule "4. the hook denies the edit that would route around the gate"
echo '{"tool_name":"Edit","tool_input":{"file_path":"tracker/items/WI-0001/history.md"}}' \
  | python3 "$HOOK" | python3 -c 'import json,sys; d=json.load(sys.stdin)["hookSpecificOutput"]; print(d["permissionDecision"].upper()+":", d["permissionDecisionReason"].split(chr(10))[0])'
echo '{"tool_name":"Bash","tool_input":{"command":"echo \"| x |\" >> tracker/items/WI-0001/history.md"}}' \
  | python3 "$HOOK" | python3 -c 'import json,sys; d=json.load(sys.stdin)["hookSpecificOutput"]; print(d["permissionDecision"].upper()+":", d["permissionDecisionReason"].split(chr(10))[0])'
echo -n "an ordinary source edit: "
echo '{"tool_name":"Edit","tool_input":{"file_path":"src/main.py"}}' | python3 "$HOOK" \
  && echo "ALLOW (no output)"

rule "5. fixing the gate lets the same transition through"
python3 - "$PROJECT" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1], "tracker", "project.yaml")
p.write_text(p.read_text().replace('  test: "python3 -c \\"raise SystemExit(1)\\""', '  test: "python3 -c \\"pass\\""'))
PY
python3 "$S/transition" WI-0001 --to in-progress --actor implement --reason "starting work" \
  --branch wi/WI-0001 --root "$PROJECT" 2>&1 | grep -E '^(transition|PASS|FAIL|SKIP|MANUAL)'
echo "status is now: $(grep '^status:' "$PROJECT/tracker/items/WI-0001/item.md")"

rule "history, showing only the transitions that were allowed to happen"
grep '^|' "$PROJECT/tracker/items/WI-0001/history.md"

printf '\nscratch: %s\n' "$SCRATCH"

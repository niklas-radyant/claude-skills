#!/usr/bin/env bash
# PreToolUse guard for AFK runs. No-op unless <repo>/.afk/ACTIVE exists.
# Blocked CLIs that would prompt for a human: extend AFK_BLOCKED_CLIS (space-separated).
input=$(cat)
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
root=$(cd "${cwd:-.}" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null) || exit 0
active="$root/.afk/ACTIVE"
[ -f "$active" ] || exit 0
slug=$(head -1 "$active")
tool=$(printf '%s' "$input" | jq -r '.tool_name // empty')
deny() {
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}
case "$tool" in
  AskUserQuestion)
    deny "AFK run '$slug' is active: the owner is away. Decide it by the decision rule (afk skill → Deciding without the owner) and log it in .afk/$slug/decisions.md, or park it in .afk/$slug/parked.md and build around it. Then continue." ;;
  EnterPlanMode|ExitPlanMode)
    deny "AFK run '$slug' is active: no plan-mode approvals. The contract is the plan; continue with the next slice." ;;
  Bash)
    cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // empty')
    for cli in op ${AFK_BLOCKED_CLIS:-}; do
      if printf '%s' "$cmd" | grep -Eq "(^|[;&|(\` ])$cli( |\$)"; then
      deny "AFK run: secret-manager CLIs are off-limits mid-run (they prompt). Use what preflight prepared; if a key is missing, park the dependent item in parked.md."
      fi
    done
    if printf '%s' "$cmd" | grep -Eq '(^|[;&|( ])gh pr (create|merge|ready)'; then
      deny "AFK run: no PR is opened or merged during a run; the owner reviews first. Finish the end state and write HANDBACK.md."
    fi
    if ! grep -q '^allow_push' "$active" && printf '%s' "$cmd" | grep -Eq '(^|[;&|( ])git push'; then
      deny "AFK run: the end state is local commits + a clean preflight + the owner's review. No push unless the contract allows it (allow_push in .afk/ACTIVE)."
    fi ;;
esac
exit 0

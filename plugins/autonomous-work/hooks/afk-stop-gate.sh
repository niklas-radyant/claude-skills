#!/usr/bin/env bash
# Stop gate for AFK runs: refuse to end the turn while done criteria are open
# and no HANDBACK.md exists. No-op unless <repo>/.afk/ACTIVE exists.
input=$(cat)
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
root=$(cd "${cwd:-.}" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null) || exit 0
active="$root/.afk/ACTIVE"
[ -f "$active" ] || exit 0
slug=$(head -1 "$active")
run="$root/.afk/$slug"
[ -f "$run/HANDBACK.md" ] && exit 0
status="$run/status.md"
if [ ! -f "$status" ]; then
  reason="AFK run '$slug' is active but .afk/$slug/status.md is missing. Create it from the contract's done criteria and continue."
else
  open=$(awk '/^## Done criteria/{f=1;next} /^## /{f=0} f && /^- \[ \]/' "$status")
  [ -z "$open" ] && reason="AFK run '$slug': all done criteria are ticked. Finish the end state (afk skill → End state): rebase, ship check, final screenshots, HANDBACK.md, remove .afk/ACTIVE, push notification." \
    || reason="AFK run '$slug' is not finished. Open done criteria:
$(printf '%s\n' "$open" | head -5)
Continue with the next slice. Re-read contract.md and status.md if context was compacted. Don't ask the owner; decide by the decision rule or park in parked.md. If everything left is parked, write HANDBACK.md."
fi
jq -n --arg r "$reason" '{decision:"block",reason:$r}'

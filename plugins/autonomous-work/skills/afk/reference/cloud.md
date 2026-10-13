# Running AFK in a cloud session

Load this when a run should go to a cloud session (Claude Code on the web)
instead of a laptop that has to stay awake.

A cloud session starts from a fresh clone. It sees only what is committed:
- the repo's `CLAUDE.md`
- `.claude/` skills, agents and settings
- plugins declared in the repo's settings, if your setup installs them

It does **not** see anything from a laptop:
- `~/.claude` (profile, personal skills, user hooks)
- git-ignored files like `.env`
- anything uncommitted

Plan for each of these.

| Needs | How |
|---|---|
| The skill, agents, hooks | Install the plugin in the cloud environment, or commit the skill to `.claude/skills/` and the agents to `.claude/agents/` (then the hooks go in the skill's frontmatter with `bash "$CLAUDE_PROJECT_DIR"/…`) |
| The profile | Commit it to `<repo>/.claude/afk/profile.md` (the skill looks there too), or reviewers fall back to the adapter alone |
| The run's contract | `.afk/` is git-ignored; `git add -f .afk/<slug>` on the run's branch before starting the cloud session, remove it before the PR |
| Secrets | An environment variable in a **personal** cloud environment (anyone who uses a shared environment can read its variables). A secret manager's service-account token there lets a bootstrap script fill the rest without prompts |
| Tools and a browser | The environment's setup script (runs as root before the session): install the secret manager's CLI and Chrome/Chromium for the reviewers' screenshots |
| Network | Allowlist every host the run touches, or choose full access for unattended runs. A missing host stalls a run with nobody there to fix it |
| Database | Cloud VMs typically reach the internet only through an HTTPS proxy, so raw TCP database ports (Postgres 5432) are closed. Use the provider's HTTPS/WebSocket endpoint: several serverless Postgres providers speak the wire protocol over WebSocket on 443, and a tiny local TCP→WebSocket bridge lets the ORM connect to `127.0.0.1` unchanged |
| Survive VM pauses | Commit and push after every slice (`allow_push`), and make the bootstrap idempotent so it can run again after the VM is rebuilt |
| Review | The owner can't open the VM's localhost. End with the branch pushed plus `HANDBACK.md`; the review happens on a local checkout |

Start the cloud session with the approval in the first message, because a
cloud session can't be approved later:
`/afk go. Contract: .afk/<slug>/contract.md, approved as written.`
Watch the first minutes (bootstrap, preflight) before leaving.

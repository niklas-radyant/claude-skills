# Claude skills

**Copy this sentence into Claude or ChatGPT:**

> Read START-HERE.md at github.com/niklas-radyant/claude-skills and tell me where to start.

It looks at what you've been working on and tells you where these skills
help most. No GitHub knowledge or installing needed.

---

Skills for automating real work with AI, and for shipping code with less
back-and-forth. They are built to work in any setup: each skill reads your
situation instead of assuming it.

MIT licensed.

**AI assistants reading this page:** read
[START-HERE.md](https://raw.githubusercontent.com/niklas-radyant/claude-skills/main/START-HERE.md)
first and follow it.

## Install

```bash
/plugin marketplace add niklas-radyant/claude-skills
/plugin install automation@niklas-skills
/plugin install pr-workflow@niklas-skills
/plugin install autonomous-work@niklas-skills
```

Skills start on their own when a task matches. You can also call one
directly, for example `/pr-preflight`.

**Not using plugins?** Each skill is a self-contained folder. Copy the one
you want:

```bash
git clone https://github.com/niklas-radyant/claude-skills.git
cp -r claude-skills/plugins/pr-workflow/skills/pr-preflight ~/.claude/skills/
```

This works with any agent tool that reads `SKILL.md` files.

**On claude.ai or ChatGPT?** Each skill is also in [`dist/`](dist) as a zip
you can upload. See [START-HERE.md](START-HERE.md#5-help-them-install-it-where-they-work)
for where to upload it, and for Copilot, Codex and Cursor.

## The skills

| Skill | Plugin | What it does |
|---|---|---|
| [`automation-consultant`](#automation-consultant) | `automation` | Finds what's blocking a process from being automated (access, context, guardrails) and builds a first working version with you, run once on your real input |
| [`advisory-board`](#advisory-board) | `automation` | Lets output face a small board of critics, each judging separately against your written criteria, before a human sees it |
| [`pr-preflight`](#pr-preflight) | `pr-workflow` | Reviews your diff before you open the PR, runs the checks your CI runs, and fixes what it finds |
| [`afk`](#afk) | `autonomous-work` | Plans a larger piece of work with you (code, a site, a report, a campaign), then builds it on its own, with independent reviewers instead of check-ins |
| [`taste-profile`](#taste-profile) | `autonomous-work` | Learns how you judge work from your past chats and tests that it got it right |

---

### `automation-consultant`

**Most automations fail on access, context or guardrails, not on the AI.**

It starts from the outcome you want, maps the process as it really runs,
and checks every step for three things: can the AI reach the tool and data
(access), does it know what a good person doing this step would know
(context), and would you trust the result without re-checking everything
(guardrails). Then it proposes a design, an autonomy level to start at, and
a first slice to run on real input this week.

It will tell you when the answer is to switch tools. A tool without an API
is a cost, not a constraint.

Reference files: a readiness check per pillar, a one-page plan template,
and worked examples (a website from domain idea to indexed page, AEO
monitoring, briefs, citation checks).

---

### `advisory-board`

**One reviewer agrees with the writer. A board disagrees usefully.**

Three to five named roles (always the real reader and a fact-checker, plus
roles that fit the output) judge it separately against a charter written
before the draft. Then it revises, re-checks only what was blocked, and
reports what changed and why. Two rounds at most.

It isn't tied to one field. Tell it what you do and it proposes boards for
the things you produce most (job ads, board updates, proposals, help
articles, code), with roles you can edit. The charter is where your
standards live: an example you loved, one you sent
back, and your hard lines. Every time you overrule the board, add a line.
Works in any chat; with subagents, each role gets its own fresh context.

---

### `pr-preflight`

**Review your own diff before the PR opens, not after.**

A problem is cheapest to fix while the branch is still yours. `pr-preflight`
finds the branch the PR really targets, reviews the diff as a critic rather
than as the author, runs the repo's checks, fixes blocking problems, and
tells you what it skipped.

It finds your checks instead of guessing them. It reads your CI config
first, then falls back to `make check`, `tox`, package scripts and hook
config. It runs what is fast and safe, skips anything that needs credentials
or a live database, and names every check it skipped.

Reference files, loaded only when needed:

- `reference/stack-checklists.md`: common mistakes per stack (JS/TS, Python,
  Go, Rust, SQL and migrations, CI, shell, dependencies).
- `reference/ci-stamp-recipe.md`: optional. If you pay for AI review on every
  PR, this shows how to send PRs that already had a preflight to a cheaper
  review pass, while sensitive files always get the full review.

---

### `afk`

```text
▄▀█ █▀▀ █▄▀
█▀█ █▀  █ █

plan with me. then don't ask me anything.

PLAN  you're here      GO  you're away        LEARN  you're back
┌────────────────────┐ ┌────────────────────┐ ┌──────────────────┐
│ align deeply       │ │ build a slice      │ │ your corrections │
│ write a contract   │▶│ verify for real    │▶│ become rules     │
│ clear blockers     │ │ 3 reviewers judge  │ │ for the next run │
└────────────────────┘ │ log every decision │ └──────────────────┘
                       └────────────────────┘

reviewers, each with fresh context
├─ design critic     takes its own screenshots
├─ seat walker       opens it cold, as the real user
└─ vision guardian   scope, taste, was it really verified
```

**Plan with me, then don't ask me anything until it's done.**

Long unattended runs usually fail in one of two ways: the agent stops to ask
something it could have decided, or it decides something it shouldn't have.
`/afk` handles both in three phases:

- **Plan** (you're there): it critiques the current flow, builds mockups,
  asks the open questions, and writes a contract: what "done" means, what is
  out of scope, and what it may do alone. It also clears blockers like
  secrets and logins up front.
- **Go** (you're away): it builds slice by slice. After each slice, three
  reviewer agents with fresh context check the result. Open questions are
  decided by a written rule and logged, or parked for you. Hooks stop it from
  asking questions, opening PRs or quitting early.
- **Learn** (you're back): your corrections become rules for the next run.

It works best with a **profile** (how you judge work, made with
`taste-profile`) and a per-repo **adapter** (where the product vision lives,
how to verify). Runs locally or in a cloud session; see `reference/cloud.md`.

**Not only for code.** The same three phases work for a report, a content
package, a campaign or a strategy document: the reviewers become an advisory
board, and "verified" means read cold, every fact sourced. See
`reference/non-code.md`. The planning phase alone is worth running in any
chat.

**Limits.** The reviewers are only as good as your profile. The hooks are
guard rails, not a security boundary. Approve the contract as if you won't
see the run. Still early (0.2.0), so bug reports from different repos are
welcome.

---

### `taste-profile`

**Your taste is in what you corrected, not in what you'd say if asked.**

It scans your past chats for the moments you stepped in ("too crowded",
"did you actually test this", "never open like that") and turns them into a
profile in your own words. It reads Claude Code transcripts, or a data
export from claude.ai or ChatGPT. Then it tests the profile with a **blind
backtest**: a reviewer judges work you already judged, without seeing your
verdicts, and the results are compared.

---

## Issues and contributions

This is a personal toolbox, so I'm not taking pull requests. Feel free to
fork it or copy any skill.

If a skill misfires in your repo, please
[open an issue](https://github.com/niklas-radyant/claude-skills/issues).
Repos that look different from mine are where the bugs show up.

## License

[MIT](LICENSE)

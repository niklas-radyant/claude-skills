# Start here

**For people:** paste this repo's link into Claude, Claude Code, ChatGPT or
Copilot and say:

> Read START-HERE.md at github.com/niklas-radyant/claude-skills and tell me where to start.

That's all. The assistant reads this file and takes it from there. Coders
who want to install everything can skip to [the README](README.md#install).

---

## For the AI assistant reading this

The user pasted this repository's link and asked you to read this file. Your
job: find the one or two places where these skills would make the biggest
difference to their work, and **get them one real result in this
conversation**, not just a plan. Don't oversell anything. Reply in the
language the user writes in, and avoid jargon (skill, repo, plugin) unless
they use it.

**Links.** Every file in this repo is at
`https://raw.githubusercontent.com/niklas-radyant/claude-skills/main/<path>`.
A skill's reference files sit next to its SKILL.md: replace `SKILL.md` in its
link with `reference/<file>.md`. If a link won't open, say which file you
couldn't read and carry on with what you have; only a non-coder's last
resort is "open this link and paste what you see".

### 1. Know what's here

| Skill | What it does | Works in | Read it |
|---|---|---|---|
| `automation-consultant` | Works out how to automate a process: outcome first, then checks each step for access, context and guardrails, then a design and a first slice to run this week | anywhere | [SKILL.md](https://raw.githubusercontent.com/niklas-radyant/claude-skills/main/plugins/automation/skills/automation-consultant/SKILL.md) |
| `advisory-board` | Self-review before anything ships, for any job: a few named critics judge the output separately against written criteria, then it gets revised. Can also propose standing boards for the user's role | anywhere | [SKILL.md](https://raw.githubusercontent.com/niklas-radyant/claude-skills/main/plugins/automation/skills/advisory-board/SKILL.md) |
| `taste-profile` | Turns the user's past corrections into written rules that a reviewer or advisory board can apply, then tests them blind | anywhere: reads Claude Code transcripts, a claude.ai or ChatGPT export, or pasted corrections | [SKILL.md](https://raw.githubusercontent.com/niklas-radyant/claude-skills/main/plugins/autonomous-work/skills/taste-profile/SKILL.md) |
| `afk` | Plan a larger piece of work together (a website, a report, a content package, a campaign), then build it in one run with independent reviewers instead of check-ins | best in Claude Code or another agent that runs for hours; the planning part works in any chat | [SKILL.md](https://raw.githubusercontent.com/niklas-radyant/claude-skills/main/plugins/autonomous-work/skills/afk/SKILL.md) |
| `pr-preflight` | Reviews a code diff and runs the repo's own CI checks before a pull request opens | coding agents with a shell (Claude Code, Codex, Copilot agent) | [SKILL.md](https://raw.githubusercontent.com/niklas-radyant/claude-skills/main/plugins/pr-workflow/skills/pr-preflight/SKILL.md) |

The idea behind them: automation with AI works when three things are in
place. **Access** (the AI can reach the tools and data), **context** (it
knows what a good person doing the job would know) and **guardrails** (the
output is checked well enough that nobody has to re-read everything).
`automation-consultant` diagnoses which one is missing; the others supply
guardrails.

### 2. Look at what the user has been working on

Use whatever you can actually see, and say what you looked at:
- **Claude (claude.ai, desktop, mobile):** search their recent chats and
  memory if those tools are available; check project files if you're in a
  project.
- **Claude Code or another coding agent:** the current repo, recent
  commits, open branches, `CLAUDE.md` or `AGENTS.md`, and recent sessions if
  you can read them.
- **ChatGPT:** what your saved memory and chat-history reference give you.
  You can't search past chats on request, so say what you remember and
  don't guess beyond it.
- **Connected tools** (email, calendar, Slack, CRM, project management):
  only if already connected, and **ask before you look**. Then only for
  patterns (recurring tasks, repeated requests), never private details to
  quote back.

If you can see little or nothing, don't open with only questions. Give one
provisional suggestion, marked as a guess (for someone coming from a talk on
automation, usually: the report or recurring piece of work they redo every
week or month), then ask:
1. What do you do every week or month that feels like it should run by itself?
2. Where do you most often re-check or fix AI output?
3. What can you set up yourself, and what needs IT or an admin (tools,
   connectors, data you may use)?

Ask question 3 even when you found plenty: in a company, it decides what a
first step can be.

### 3. Recommend, ranked by impact

Give the user **at most three** recommendations, best first. For each:
- **The skill**, and **the concrete task from their own work** it applies
  to: name their task, in their words. A recommendation that says only what
  the skill does in general is not one.
- **Why this one first**: time saved, quality gained, or something that
  doesn't happen today.
- **The first step**, small enough to do in this conversation, and one the
  user can take without anyone else's approval.

Rank by where the user loses the most time each month. In practice:
- A task they repeat by hand (copying data between tools, the same report
  every month) → `automation-consultant` on that task.
- Output they re-check or redo by hand (drafts, briefs, analyses that come
  back with the same corrections) → `advisory-board` on that output.
- Quality depends on who does it (one account manager's reports are great,
  another's aren't) → `advisory-board` with one shared charter built from
  the best person's work.
- AI got the facts wrong (invented issues, made-up numbers) → the fix is
  data plus a check a script can do, so start with `automation-consultant`.
  A board alone won't catch it.
- Their work touches AI search or AEO → say that `automation-consultant`
  has a worked example for AI-visibility monitoring, including the case
  where they have no monitoring tool yet.
- Both? Lead with whichever costs more time, and give the other as #2.
- A bigger project they keep putting off (a new site, a report, a content
  series) → `afk`, starting with its planning phase.
- They keep correcting the same things in AI output → `taste-profile`, so
  the corrections become rules.
- `pr-preflight` only for people who change code through pull requests.
- A task no skill fits: say so in one line and offer to help with it
  directly. Don't stretch a skill onto it.

### 4. Start right now, and finish something

You don't need to install anything to use a skill once: fetch its SKILL.md
from the links above and follow it in this conversation. Offer this first.
Installing is for when they want it every day.

Aim for one real result before the conversation ends, ideally within 15
minutes. Examples:
- `advisory-board`: they paste the last thing they wrote; you write the
  charter with them and return the reviewed, improved version.
- `automation-consultant`: the plan, plus the first slice done once by hand
  in this chat (their pasted export turned into this month's report, or,
  with no data yet, a small sample they run during the chat).
- `afk`: the planning phase for the project they keep putting off, ending in
  a contract they can hand to an agent or a colleague.
- `taste-profile`: ten rules from their own corrections, ready to paste into
  their project instructions.

Then offer to save what you built (charter, plan, profile) as a project file
or instructions, so their next chat starts from it. If someone else writes
the drafts (freelancers, an agency, a colleague), offer the charter as their
brief too: fixing the input beats re-checking the output.

When you hand over to a skill, tell it what you already know (the task the
user picked, what you learned about their work) so it doesn't ask again.

### 5. Help them install it where they work

Show only the row for the platform the user is on.

| Where | How |
|---|---|
| **Claude Code** | `/plugin marketplace add niklas-radyant/claude-skills`, then `/plugin install automation@niklas-skills` (and `autonomous-work@niklas-skills`, `pr-workflow@niklas-skills` if useful). |
| **Claude (claude.ai, desktop)** | Download the zip (links below), then Settings → Capabilities → Skills → Upload skill. Needs a paid plan. If Skills isn't there, the user can forward this to their admin: "Please enable Skills and Code execution and file creation for our organization." Can't install at all? Create a Project, upload SKILL.md and its reference files as project files, and add one instruction: "Follow SKILL.md when I ask for <skill>." Menu names move around (as of October 2026). |
| **ChatGPT** | Look for Skills in Settings; if it's there, upload the same zip. If not, ask the workspace admin or use a Project: upload SKILL.md and its reference files as project files, and add one instruction: "Follow SKILL.md when I ask for <skill>." |
| **Microsoft 365 Copilot** (Word, Outlook, Teams) | A different product from GitHub Copilot, with no skill folders. If the tenant allows Copilot agents or notebooks, paste SKILL.md into an agent's instructions or add it to a notebook. |
| **GitHub Copilot** (VS Code agent mode, Copilot CLI, cloud agent) | Copy the skill folder to `.github/skills/<skill-name>/` in the repo, or `~/.copilot/skills/` for personal use. |
| **Codex, Cursor, Gemini CLI and other agents** | Most read the same `SKILL.md` format. Copy the folder into the tool's skills directory. Otherwise paste SKILL.md into its rules or instructions file. |

Direct downloads:
[automation-consultant.zip](https://github.com/niklas-radyant/claude-skills/raw/main/dist/automation-consultant.zip) ·
[advisory-board.zip](https://github.com/niklas-radyant/claude-skills/raw/main/dist/advisory-board.zip) ·
[taste-profile.zip](https://github.com/niklas-radyant/claude-skills/raw/main/dist/taste-profile.zip) ·
[afk.zip](https://github.com/niklas-radyant/claude-skills/raw/main/dist/afk.zip) ·
[pr-preflight.zip](https://github.com/niklas-radyant/claude-skills/raw/main/dist/pr-preflight.zip)

SKILL.md is an open format: a folder with a `SKILL.md` file (name and
description at the top, instructions below) and optional reference files.
Assistants without native skill support can still follow one as plain
instructions, though only the Claude versions have been tested on real work.
What needs Claude Code specifically: `afk`'s hooks (they stop the agent from
asking questions or quitting early) and its long unattended runs. Everything
else works anywhere. Say so if the user is elsewhere.

### Rules for you

- **Don't oversell.** Each skill has a "where it can be wrong" or "limits"
  section. If the user's situation hits one, say so.
- **Never ask for or handle credentials** in the chat. Don't ask the user
  to paste personal or customer data; aggregated numbers and their own
  writing are fine. If a recommendation
  needs API access, point to a password manager or the tool's own connector.
- **Be specific to them.** A recommendation that would fit anyone isn't one.
- **Keep it short.** Three recommendations and a first step beat a tour of
  the repo.

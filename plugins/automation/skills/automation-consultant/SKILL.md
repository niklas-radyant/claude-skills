---
name: automation-consultant
description: Works out how to automate a process with AI, and what has been blocking it. Starts from the outcome, maps the steps, checks each one for the three things automation needs (access, context, guardrails), then proposes a design and a first slice you can run this week. Use when the user says "automate", "can AI do this", "how would I automate X", "why does this automation keep failing", "where should I start with AI", or describes a repetitive task they want off their plate.
---

# Automation consultant: find out what's really in the way, then automate around it

## Why this exists

Most automation attempts don't fail because the AI isn't good enough. They
fail for one of three boring reasons:

1. **Access.** The data or the action sits in a tool the AI can't reach: no
   API, no MCP server, a login only one person has.
2. **Context.** The knowledge needed to do the step well lives in
   someone's head, a meeting nobody wrote down, or a document the AI never
   sees.
3. **Guardrails.** Nobody trusts the output enough to let it run without
   re-checking everything, so the automation saves no time.

Asking "what should I automate?" leads to a list of tasks. Asking "what's the
outcome, and which of the three is missing at each step?" leads to
something that runs. This skill asks the second question.

## Procedure

Work through it with the user as a conversation, not a form. Ask at most
three questions at a time, and say what you already know so they don't
repeat it. Once you have the outcome, the step where it stopped and a
rough step map, stop asking: draft the plan and mark your assumptions.

### 1. Start from the outcome, not the task

Get four things before mapping anything:
- **The outcome.** What's different when this works? "A brief for every new
  page within a day of the keyword being picked" beats "automate briefs".
- **Why now.** Time, quality, speed, consistency, or something that doesn't
  happen at all today. This decides what to optimise for.
- **What was tried, and where it stopped.** This is the most useful answer
  in the whole conversation. Write down the exact point it broke.
- **Constraints.** Which AI tools and connectors they may use, what data may
  go into them, and what they can set up themselves versus what needs IT,
  security or data protection. In a company, design inside these limits and
  list everything else as a request to whoever decides.

If the user already picked a task (for example in an earlier step of this
conversation), skip straight to the questions above. If they have no
specific process yet and want to know where to start,
look at what you can see of their recent work (past chats, project files,
the repo, their calendar, if those are connected) and propose three
candidates. A good first candidate is frequent, boring, has a clear "done",
and goes wrong in ways that are cheap to fix. Let them pick one.

### 2. Map the steps

Write the process as it really runs today, including the unofficial steps
("then I check with Anna on Slack"). For each step note:
- the trigger (what starts it)
- the input and where it comes from
- the action, and in which tool it happens
- the output, and where it goes
- who does it today, and how long it takes

Keep it to 5–12 steps. More means you're describing two processes; split
them and pick one.

If the process repeats per client, product or market (an agency's monthly
report for 30 clients), map one instance and list what varies between
instances. That list becomes a context file per instance (goals, priority
pages, competitors, what was already done, what the client said no to), in
whatever the team already uses: a Notion page, a Drive doc, a folder in the
repo. Then the design runs once per instance (in parallel where the runtime
allows), pilots on one instance first, and returns one summary that shows
only the exceptions, not 30 reports to read. A shared charter for the
review keeps quality the same whoever is responsible for the client.

### 3. Check every step against access, context and guardrails

Use [reference/readiness-check.md](reference/readiness-check.md). For each
step, mark each of the three as **ready**, **fixable** or **blocked**, with
what's missing in the same cell ("fixable: client goals not written down").
Collapse steps where everything is ready into one line.

The common findings, and what to do about them:

| Finding | Usual fix |
|---|---|
| Tool has no API or MCP server | Check again (many do now). If not, **switch tools**: a tool that can't be automated is a cost, not a constraint. If the tool isn't the user's to choose, write the business case for whoever owns it, and route around it this week with an export or a system that already holds the data (BI, data warehouse). |
| Tool has an API, but your automation platform can't use it | Change where the automation runs (step 5), not the tool. |
| Credentials are personal or scattered | One service account in a password manager the AI can read, holding scoped tokens, revocable in one click. Simpler and fine: the automation platform's own credential store, or the tool's official connector in a chat assistant. In corporate IT, credentials aren't the user's to create: the fix is a request for an approved connector. |
| The AI invents facts (issues that don't exist, wrong numbers) | Don't let it detect what a query or script can detect. A deterministic step finds and counts; the AI only explains, prioritises and writes, citing the rows it was given. |
| Knowledge is in someone's head | Write it down once where the AI reads it on every run: project instructions or files in a chat project, a knowledge base, or a `CLAUDE.md` in a repo. |
| Knowledge changes constantly | Don't copy it; connect the system that owns it (CRM, Slack, email, analytics) and fetch it on each run. |
| Output can't be trusted unchecked | Add a check: a deterministic test where one exists, an advisory board review where judgement is needed, a human approval only where the risk demands it. |
| Step is a judgement call nobody has written down | Collect five past examples with the decision and the reason. That becomes the rule. |

Point to the tool switch explicitly when it's the answer. People rarely
consider it, and it's often cheaper than any workaround.

### 4. Pick the design

For each step, choose the cheapest thing that's reliable enough:
- **Deterministic** (a script, a no-code flow, a scheduled job) when the
  step has no judgement in it. Predictable beats clever.
- **AI with a check** when the step needs judgement or language: drafting,
  classifying, summarising, deciding between options.
- **Human** for the few steps where a mistake is expensive and hard to undo:
  money, legal commitments, publishing to a large audience, deleting data.

Then pick the autonomy level for the whole flow, and say why:

| Level | What it means | When |
|---|---|---|
| **Assist** | AI drafts, human does the step | trust not built yet, high stakes |
| **Draft and approve** | AI does it, human approves before it takes effect | the usual starting point |
| **Run and report** | AI does it, human reads a report afterwards | after a few weeks of approvals with few corrections |
| **Unattended** | AI does it; only exceptions reach a human | well-tested, reversible, cheap to fix |

Move a flow up a level only after it has earned it. Note what evidence
would justify the next level ("ten runs in a row with no correction").

### 5. Decide where it runs

Pick the runtime by what the steps need, not by what was used last time:
- **No-code platform** (Zapier, Make, n8n, or what the company already
  licenses: Power Automate, scheduled BI exports): mostly deterministic
  steps between tools it has connectors for, maintained by non-developers.
- **Scheduled AI agent** (a scheduled Claude task or Claude Code routine,
  ChatGPT scheduled tasks,
  an agent framework): several judgement steps, tools reachable via MCP, and
  output that goes through a check.
- **Script or scheduled job**: deterministic, high volume, or needs
  something no platform offers.
- **Mixed** is normal: a deterministic job fetches and detects, an agent
  diagnoses and drafts.

Name who maintains it and what it roughly costs per run.

### 6. Bring in the right building blocks

Mention only the ones that fit this process, with one sentence on why:
- **`advisory-board`**: when output needs judgement-based review before it
  goes out. The charter it builds is where the user's standards live.
- **`taste-profile`**: when the user keeps correcting the same things. It
  mines their past corrections into written rules a reviewer can apply.
- **`afk`**: when a larger piece of work (a site, a report, a content
  package, a migration)
  should be built in one long autonomous session: all decisions up front,
  then no check-ins.
- **`pr-preflight`** (plugin `pr-workflow`): when the automation produces code changes that go
  through pull requests.

If one of these isn't installed, point to
https://github.com/niklas-radyant/claude-skills rather than reproducing it
here.

### 7. Write the automation plan

Use [reference/plan-template.md](reference/plan-template.md). The plan ends
with a **first slice**: the smallest piece that runs end to end on real
input this week, usually one or two steps at "draft and approve", and that
the user can start without anyone else's approval. Dependencies on other
teams go under blockers, not into the first slice. A plan without a first
slice is a wish list. If you can, do the first slice once right here in the
conversation (with their pasted data), so they leave with a result.

For worked examples of how this goes in practice, see
[reference/examples.md](reference/examples.md).

## Rules

- **Never let the AI detect what a query can detect.** Finding, counting and
  comparing are deterministic jobs. The AI explains, prioritises and writes,
  from the rows it was given. This is the cure for invented findings.
- **Outcome before tools.** Don't recommend a tool or platform until the
  outcome and the blocking step are clear.
- **Name the blocker plainly.** "This fails because the hosting provider has
  no DNS API" is useful. "There are integration challenges" isn't.
- **Don't automate a process nobody can describe.** If step 2 can't be
  written down, the first deliverable is the written process, not the
  automation.
- **Credentials never go into a prompt, a chat or a file in the repo.**
  Recommend a secret store with scoped, revocable tokens.
- **Prefer reversible.** Start where a mistake costs a re-run, not an
  apology.

## Where it can be wrong

- It only sees what the user tells it and what it can reach. Tool
  capabilities change fast; check a tool's current API and MCP support
  before recommending a switch, and say when you couldn't.
- It estimates time savings from what the user reports. Treat the numbers
  as rough until the first slice has run a few times.
- It is not a security review. A design that hands an AI write access to
  production systems needs one.

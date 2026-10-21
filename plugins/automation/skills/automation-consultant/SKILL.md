---
name: automation-consultant
description: Works out how to automate a process with AI, finds what has been blocking it (access, context or guardrails), and builds a first working version in the same conversation, run once on real input, with an honest note on what stays manual. Use when the user says "automate", "can AI do this", "how would I automate X", "why does this automation keep failing", "where should I start with AI", or describes a repetitive task they want off their plate.
---

# Automation consultant: name the real blocker, then build the first version

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

Advice about these three is cheap, and most people have heard it. What they
haven't had is someone who finds the one that applies to *their* process
and then builds the first version with them. That's the job.

## What the user gets

Say this early, in one or two sentences, so expectations are right:

- **The real blocker**, named plainly, for their process.
- **A first version that runs**, built in this conversation and tried once
  on their real input: a ready-to-use project setup, a scheduled task, a
  no-code flow, or a script, whichever fits what they're allowed to use.
- **An honest handover**: what it does, what they still check, what stays
  manual, and when it's worth going further.

Not promised: a finished, unattended automation. The first version is
"draft and approve". It earns more autonomy by running well.

## Procedure

A conversation, not a form. Ask at most three questions at a time, and say
what you already know so they don't repeat it. Aim to have the first
version running within about 30 minutes.

### 1. Three things, then stop asking

- **The outcome.** What's different when this works? "A brief for every new
  page within a day of the keyword being picked" beats "automate briefs".
- **Where it stopped before.** The most useful answer in the conversation.
  Get the exact point: "the export is a manual download", not "no time".
- **Constraints.** Which AI tools and connectors they may use, what data
  may go into them, and what they can set up themselves versus what needs
  IT, security or data protection. Design inside these limits; everything
  else becomes a request to whoever decides.

Get how often it runs and how long it takes today along the way; you need
both in step 3.

If the user already picked a task (for example in an earlier step of this
conversation), skip the questions you can answer. If they have no specific
process yet, look at what you can see of their recent work (past chats,
project files, the repo, their calendar, if connected) and propose three
candidates. A good first candidate is frequent, boring, has a clear "done",
and goes wrong in ways that are cheap to fix. Let them pick one.

### 2. Map it and find the blocker

Write the process as it really runs today in 5–12 steps, including the
unofficial ones ("then I check with Anna on Slack"): trigger, input, tool,
output, who, how long. Then check each step for access, context and
guardrails with [reference/readiness-check.md](reference/readiness-check.md),
and show only the steps that aren't ready:

| Step | Access | Context | Guardrails |
|---|---|---|---|
| Pull last month's numbers | blocked: export is manual, no API access | ready | ready |

**Check, don't guess.** When a step depends on whether a tool has an API, an
MCP server or a connector, look it up now (web search, the tool's docs) and
say what you found, with the link. Tool capabilities change monthly; an
answer from memory is the most common way this skill goes wrong.

The usual findings and fixes:

| Finding | Usual fix |
|---|---|
| Tool has no API or MCP server | If confirmed, **switch tools**: a tool that can't be automated is a cost, not a constraint. If the tool isn't the user's to choose, write the business case for whoever owns it, and route around it this week with an export or a system that already holds the data (BI, data warehouse). |
| Tool has an API, but the automation platform can't use it | Change where the automation runs (step 4), not the tool. |
| Credentials are personal or scattered | A service account in a password manager the AI can read, with scoped tokens, revocable in one click. Simpler and fine: the platform's own credential store, or the tool's official connector. In corporate IT: a request for an approved connector. |
| The AI invents facts | Don't let it detect what a query or script can detect. A deterministic step finds and counts; the AI explains and writes, citing the rows it was given. |
| Knowledge is in someone's head | Write it down once where the AI reads it on every run: project instructions or files, a knowledge base, a `CLAUDE.md`. |
| Knowledge changes constantly | Connect the system that owns it and fetch it on each run, don't copy it. |
| Output can't be trusted unchecked | A deterministic check where one exists, an `advisory-board` where judgement is needed, a human approval only where the risk demands it. |
| A judgement call nobody has written down | Five past examples with the decision and the reason become the rule. |

If the process repeats per client, product or market (an agency's monthly
report for 30 clients), map one instance and list what varies. That list
becomes a context file per instance (goals, priority pages, competitors,
what was done, what the client said no to) in whatever the team already
uses. The design runs per instance, pilots on one, and returns one summary
of exceptions instead of 30 reports. A shared charter keeps quality the
same whoever owns the client.

### 3. Is it worth it?

Do the arithmetic out loud: time per run today × runs per month, minus the
time a person will still spend checking, plus the setup time. Example: "4
hours × 6 clients = 24 hours a month today; about 30 minutes of review per
client afterwards; setup about a day. Pays back in the first month."

If it doesn't pay back within a few months, say so, and suggest either a
smaller piece of it or a different process. An honest "not worth it yet"
builds more trust than a plan nobody will run.

### 4. Pick the design and where it runs

For each step, the cheapest thing that's reliable enough:
- **Deterministic** (script, no-code flow, scheduled export) when there's no
  judgement in it. Predictable beats clever.
- **AI with a check** when it needs judgement or language.
- **Human** where a mistake is expensive and hard to undo: money, legal
  commitments, publishing to a large audience, deleting data.

Start at **draft and approve**: the AI does the work, a person approves it
before it takes effect. Name the evidence that would justify the next level
("ten runs in a row with fewer than three edits"):

| Level | What it means |
|---|---|
| Assist | AI drafts, human does the step |
| Draft and approve | AI does it, human approves before it takes effect |
| Run and report | AI does it, human reads a report afterwards |
| Unattended | Only exceptions reach a human |

Then the runtime, from what the user may use (step 1), not from what was
used last time: a chat project, a scheduled assistant task (Claude, ChatGPT),
a no-code platform (Zapier, Make, n8n, Power Automate), a script or
scheduled job, or Claude Code. Mixed is normal: a deterministic job fetches
and detects, an agent diagnoses and drafts.

### 5. Build the first version now

Pick the smallest slice that runs end to end on real input and that the
user can start without anyone else's approval. Dependencies on other teams
become requests in the handover, not part of the first version.

Build it in the form the runtime takes, using
[reference/build-recipes.md](reference/build-recipes.md): the exact project
instructions and context file to paste, the scheduled task prompt, the
no-code steps with field mappings, or the script. Write it so they can use
it without you.

Then **run it once, here**, on their real input: their pasted export, last
month's data, a draft, or a small sample they collect during the chat (for
AI-visibility checks: five questions, one engine, three runs). Show the
result in full.

### 6. Learn from the first run

Ask the user what they'd change in the result. Each correction goes into
the place the next run reads (the context file, the charter, the
instructions), not just into this output. Run it again if a correction was
big. This loop is what makes the second run better than the first, and it's
the part most automations skip.

### 7. Hand over

End with a short card, not a long plan:

```
What it does:        <one sentence>
You still check:     <what a person reviews, and roughly how long it takes>
Stays manual:        <steps that aren't automated yet, and why>
Needs from others:   <requests to IT, the data team, the tool owner, or "nothing">
Next level when:     <evidence, e.g. "five runs with fewer than three edits">
Time saved:          <the step-3 estimate, marked as an estimate>
```

Offer to save the built pieces (instructions, context file, charter, script)
as project files, and the full plan from
[reference/plan-template.md](reference/plan-template.md) as a file if they
want one. For more worked examples, see
[reference/examples.md](reference/examples.md).

## Building blocks

Mention only the ones that fit, in one sentence each:
- **`advisory-board`**: when output needs judgement-based review before it
  goes out. Its charter is where the user's standards live.
- **`taste-profile`**: when the user keeps correcting the same things. It
  turns past corrections into written rules a reviewer can apply.
- **`afk`**: when a larger piece of work (a site, a report, a content
  package, a migration) should be built in one long run: all decisions up
  front, then no check-ins.
- **`pr-preflight`**: when the automation produces code changes that go
  through pull requests.

If one isn't installed, point to
https://github.com/niklas-radyant/claude-skills rather than reproducing it.

## Rules

- **Never let the AI detect what a query can detect.** Finding, counting
  and comparing are deterministic jobs. The AI explains, prioritises and
  writes from the rows it was given.
- **A result, not a report about a result.** If the conversation ends
  without something that ran once on real input, say what's missing to get
  there.
- **Name the blocker plainly.** "The hosting provider has no DNS API" is
  useful. "There are integration challenges" isn't.
- **Don't automate a process nobody can describe.** If step 2 can't be
  written down, the first deliverable is the written process.
- **Credentials never go into a prompt, a chat or a repo file**, and don't
  ask for personal or customer data. Aggregated numbers are fine.
- **Prefer reversible.** Drafts over publishing, staging over production.

## Where it can be wrong

- It only sees what the user tells it and what it can reach. If it couldn't
  check a tool's capabilities live, it says so.
- Time savings are estimates from what the user reports until the first
  version has run a few times.
- One run in a chat proves the idea, not the reliability. Edge cases show
  up in runs five to twenty.
- It is not a security review. Giving an AI write access to production
  systems needs one.

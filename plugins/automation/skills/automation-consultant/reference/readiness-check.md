# Readiness check: access, context, guardrails

Run every step of the mapped process through these questions. Mark each
pillar **ready**, **fixable** or **blocked**, with one line on what's missing.
A step is automatable when all three are ready or fixable.

## Access: can the AI reach the data and take the action?

- Does the tool have an **MCP server** (official or well-maintained)? That's
  the easiest path for Claude and a growing number of other assistants.
- Does it have an **API** or a **CLI**? Then a small script or an MCP
  wrapper closes the gap.
- Is the action **read** or **write**? Write access needs tighter scopes and
  a clear way to undo.
- **Whose credentials?** A personal login that only one person has is a
  blocker even if the API exists. Use a service account.
- **Where do the credentials live?** Good pattern: a password manager
  service account (1Password, Bitwarden, or similar) that the AI can read,
  holding one vault per area with scoped API tokens. One token to revoke if
  anything goes wrong, nothing pasted into chats or committed to repos.
  In corporate IT the user usually can't create credentials at all: then
  the fix is a request for an approved connector, or an export from a
  system that already holds the data (BI, data warehouse).
- **If none of this exists:** is there an alternative tool that does the
  same job and can be automated? List the switching cost next to the
  ongoing cost of the manual step.

Ask the stack question once per process: **is every tool in this flow
reachable by an AI?** If one isn't, that tool decides how far the
automation can go.

## Context: does the AI know what a good person doing this step would know?

- **Stable knowledge** (how we do things, who the client is, what we
  decided and why, the brand voice): is it written down somewhere the AI
  reads on every run? Project instructions, a knowledge base, a repo with a
  `CLAUDE.md`, a skill.
- **Live state** (open deals, this week's numbers, the latest email from the
  client): is the owning system connected (CRM, Slack, email, analytics,
  monitoring tool)? Fetch it on every run rather than copying it, because
  copies go stale.
- **Judgement** (what "good" looks like, which option to pick): are there
  past examples with the decision and the reason? Five real examples beat a
  page of adjectives.
- **Does it learn?** When a human corrects the output, does the correction
  land somewhere the next run reads? If not, the same correction will be
  made every week.

## Guardrails: would you let it run without re-checking everything?

- **Is there a deterministic check?** Tests, a schema, a link checker, a
  validator, a diff against expected values. Use it wherever it exists; it's
  cheaper and more reliable than any AI review.
- **Is there a judgement check?** For output that needs taste or
  correctness a script can't verify, a self-review against written criteria
  (`advisory-board`) catches most of what a human would send back.
- **What's the blast radius?** What happens if this step is wrong: a
  re-run, a bad draft nobody sees, a wrong email to a client, money spent,
  data deleted? Put human approval only in front of the expensive ones.
- **Can it be undone?** Drafts over publishing, staging over production,
  soft deletes over hard ones.
- **Will someone notice when it fails?** Silent failure is the worst kind.
  Every automated flow needs a report or an alert, even if it's one line.
- **Are decisions made up front?** For long autonomous runs, settle the
  open questions before the run starts and write down the rule for anything
  left over (see `afk`). An agent that stops to ask halfway through isn't
  autonomous.

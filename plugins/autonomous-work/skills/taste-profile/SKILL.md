---
name: taste-profile
description: Build or refresh the owner's taste profile (how they judge work, what they always correct, their hard lines) from their own past chats (Claude Code transcripts, or a claude.ai or ChatGPT export), then prove it with a blind backtest against work they actually rejected or accepted. Feeds the afk reviewers and any advisory board. Use when the user says "taste profile", "learn how I work", "calibrate the reviewers", "backtest the critic", or before a first /afk run.
---

# Taste profile: write down how the owner judges, then prove it

## Why this exists

An autonomous run is only as good as the judgement standing in for the owner.
Asking "what's your taste?" produces generalities ("clean, simple, intuitive")
that every reviewer already claims to follow. The owner's real taste is in
what they **corrected**. Those corrections are sitting in their Claude Code
transcripts, word for word, with the screen or diff that triggered them.

So the profile is mined, not interviewed. Then it gets tested. A reviewer
reads the profile, judges screens the owner already judged without seeing the
verdicts, and the hit rate tells you whether the profile captures the
owner's thinking or only sounds like it does.

## Procedure

### 1. Extract the owner's messages (local only)

**Not on Claude Code?** Ask the owner for a data export of their chats
(claude.ai: Settings > Privacy > Export data; ChatGPT: Settings > Data
controls > Export) and run the same script on its `conversations.json`:

```bash
python3 <this skill>/bin/extract-messages.py --export conversations.json --days 120 --out owner-messages.jsonl
```

`--match` then filters by conversation title. Export formats change; if the
script finds no messages, look at the file's structure and adapt. No export
and no code execution? Ask the owner to paste ten to twenty corrections they
remember making ("too long", "never say X", "you didn't check Y") with what
they were correcting. Fewer, but still real.

With Claude Code transcripts:

```bash
python3 <this skill>/bin/extract-messages.py --match <repo-or-project-name> --days 120 --out /tmp/owner-messages.jsonl
```

This keeps only what the human typed: plain messages, plus the ones they sent
while the agent was working (those are stored as queued attachments, and a
naive extraction misses them). Each message comes with the last assistant
text before it. Common token shapes are masked. Read it before quoting
anything: transcripts contain secrets and customer data, and both stay out
of the profile.

With several hundred messages or more, read them in a subagent and have it
report back. Don't load them all into the main context.

### 2. Analyse corrections, not compliments

Read every message alongside the turn before it. Report with short verbatim
quotes and dates:

1. **Taxonomy of interventions.** Why did the owner step in? Count them by
   category. Typical categories:
   - didn't really verify
   - too crowded or bloated
   - ignored the design system
   - too many switches and special cases
   - asked too much, or too little ownership
   - lost overview of the reporting
   - unsafe with production data
   - stale base
   - scope too narrow or too broad
   - naming
2. **Design and product taste**, as recurring principles in the owner's own
   words, including what they praised.
3. **Vision statements**: what the product is for, and for whom.
4. **How they run sessions**: kickoff, planning, review, approvals, and when
   they go away.
5. **Where autonomy failed**: questions the agent should have decided, and
   decisions it should have asked about.
6. **Recurring blockers**: prompts, logins, secrets, environment.
7. **Explicit rules** ("never…", "always…", "from now on…").

### 3. Write the profile

Use [reference/profile-template.md](reference/profile-template.md). Write it
to `~/.claude/afk/profile.md` for use across repos. For cloud runs, or a team
that shares one owner's bar, write it to `<repo>/.claude/afk/profile.md`.
Outside Claude Code, give it to the owner as a document to save in their
project's files or instructions, so every chat in that project reads it.

The profile is not only about screens. For someone who writes, plans or
analyses, the categories are the same idea: what they cut, what they always
add, which claims they don't let through, how they want things structured.

Each rule gets three things:
- what the owner does
- why
- a short quote

A rule without a reason gets followed literally in the wrong situations, so
always include the reason.

Show the owner the profile before the backtest. Ask them only about
contradictions you found, such as an old rule and a newer, opposite one. Those
are the places where taste moved.

### 4. Backtest, blind

Procedure: [reference/backtest.md](reference/backtest.md).
1. Collect cases where the owner judged a piece of work (a screen, a text,
   a plan): rejections and accepted versions.
2. Copy the screenshots under neutral names so the reviewer can't find the
   verdicts.
3. Run a reviewer on each case and compare its verdicts with the owner's:
   the design critic for screens, an `advisory-board` with the profile as
   its charter for everything else.
4. Hold some cases out of the profile's examples, so you measure judgement
   rather than recall.

### 5. Calibrate with the owner, not against the past

Ask the owner to re-judge any case where the critic and the old verdict
disagree, by their bar **today**. A screen they accepted months ago may fail
their current standard, and then the critic is right. Re-judging also tends
to surface principles they never wrote down. Add those to the profile.
Record the calibration in the backtest index.

## Rules

- **Only the owner's own words count as evidence.** Never invent a principle
  the transcripts don't show. Never put quotes from other people in the
  profile.
- **Nothing sensitive leaves the machine.** That covers transcripts, extracted
  messages and backtest screenshots. Keep them out of git if the screenshots
  show customer data.
- **A backtest proves recall of past judgements, not future ones.** Refresh
  the profile after the owner's corrections (the afk learn phase does this),
  and re-run the backtest after every change to a reviewer.
- **Small samples mislead.** With fewer than about 5 rejected cases, report
  the hit rate as anecdotal. Grow the set from real runs.

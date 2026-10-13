# Profile template

`~/.claude/afk/profile.md` (or `<repo>/.claude/afk/profile.md`). The afk
skill and all three reviewers read it in full on every run, so keep it to the
rules that change outcomes: roughly 100–150 lines. Every rule gets a reason
and, where possible, the owner's own words.

```markdown
# How <owner> works and judges

Distilled from <n> of <owner>'s messages (<date range>) and their corrections.
Project specifics live in each repo's .claude/afk/project.md.

## What they want from the agent
- **<e.g. ownership>.** <what they do / say> — "<quote>". <why it matters>.
- **<e.g. all questions up front, then they leave>.** …
- **<plans: what goes on top, what below>.** …

## How they plan best
- <e.g. thinks in pictures: decisions land on clickable mockups of every state> — "<quote>"
- <e.g. wants an honest self-rating before showing anything>
- <e.g. real product references settle pattern choices>

## The verification bar (usually their most frequent correction)
- <what "done" means to them> — "<quote>"
- <paid/long runs are part of verification?>
- <screenshots, states, from the user's seat>

## Taste (for anything a user sees)
- <their own checklist, if they have one, verbatim>
- <removal vs addition> — "<quote>"
- <density, calm, emphasis, reuse, naming, confirm steps …>

## Engineering taste
- <e.g. general mechanisms over special cases> — "<quote>"
- <e.g. no feature switches / opt-ins / caps>
- <e.g. delete replaced code, don't gate it>
- <scope: too small vs side quests>
- <cost vs quality>

## Hard lines (never, even unattended)
- <production data, customer data in commits, secrets, publishing, pushing …>

## How to report to them
- <length, language, structure, decisions format, links, next step>
```

Order by how often each area caused a correction. The first sections are the
ones a reviewer must never miss.

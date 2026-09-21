---
name: my-skill
description: What this does, then when to use it. The description is the only thing Claude reads when deciding whether to load the skill, so write the trigger conditions into it — including the words a user would actually say. Aim for 1-3 sentences.
---

# My skill — one line on what it's for

## Why this exists

The problem, and why the obvious approach doesn't solve it. Keep this short;
it's context, not content. If you can't name a concrete failure this skill
prevents, the skill probably isn't worth writing.

## Procedure

### 1. First step

Numbered, ordered steps with the actual commands. A skill that says "be
careful about X" changes nothing — say what to run and what to look for.

```bash
# real, runnable commands
```

### 2. Second step

Discover, don't assume. If the step depends on the repo's setup, say where to
look for it rather than hard-coding what your repo happens to use.

## Rules

- Constraints that apply throughout, not just at one step.
- What this skill must never do.
- What it does *not* cover, so nobody trusts it in a situation it can't
  handle.

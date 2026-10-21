# Build recipes: the first version, by runtime

Pick the recipe for what the user may use. Fill in every placeholder with
their real details; a recipe with `<...>` left in it isn't finished. Keep
the first version to one or two steps of the process.

## Chat project (Claude Projects, ChatGPT Projects)

Works for almost everyone, needs no IT. Give the user three things to paste:

**1. Project instructions**

```
You produce <the output> for <reader>, every <frequency>.
Input: I paste <the export / notes / draft>.
Always:
1. Read context.md first. Use only numbers that are in my input; if a number
   is missing, write [MISSING: ...] instead of estimating.
2. <the steps of the first slice, in order>
3. Before answering, review your draft against charter.md as each listed
   role, separately. Fix blockers. List what you changed in three lines.
Output: <format, length, language>.
```

**2. `context.md`** (project file): goals, audience, what good looks like,
what was decided before and why, terms, per-market or per-client notes.
Built from the user's answers in this conversation.

**3. `charter.md`** (project file, if a review step is needed): use the
`advisory-board` charter template.

Then run it once in the project with their real input.

## Scheduled assistant task (Claude, ChatGPT)

For recurring work that needs no tool the assistant can't reach. Give:
- the schedule (day, time, time zone)
- the full task prompt, self-contained: it starts from nothing each time,
  so it names where the input comes from and where the result goes
- what the user gets notified with, and what they do with it

If the input has to be pasted by hand each time, it isn't a scheduled task
yet; say so and use the chat project recipe instead.

## No-code flow (Zapier, Make, n8n, Power Automate)

Give the steps as a numbered list a non-developer can click together:

```
Trigger: <app> → <event> (<filter>)
Step 2:  <app> → <action>; map <field> → <field>
Step 3:  AI step (<model/app>) with prompt: <the exact prompt>, input: <fields>
Step 4:  <check>: if <condition>, send to <person> for approval; else <...>
Step 5:  <app> → <action>
```

Keep AI to the judgement steps; everything that can be a filter or a
formula should be one. If the platform supports importing a flow
definition and you're confident of its format, offer it, otherwise the
list.

## Script or scheduled job

When the work is deterministic, high-volume, or no platform covers it. Give
the script, a sample run on their data (or a small sample), how to schedule
it (cron, the platform's scheduler, a GitHub Action), and where the
credentials live (never in the script).

## Claude Code

For people who already work in it: a project skill in
`.claude/skills/<name>/SKILL.md` that holds the procedure, the context file
next to it, and, for recurring runs, a scheduled routine or a cron job that
calls it. For a larger build, hand over to `afk` instead.

## Checking the first run

Whatever the runtime, after the first run on real input:
- every number in the output traces back to the input
- nothing in the output would embarrass the user if sent as is, or it's
  marked as needing review
- the user names what they'd change, and each change lands in the context,
  charter or instructions

# Automation plan template

Keep it to one page. Everything here should be specific enough that
someone else could build the first slice from it.

```markdown
# Automation plan: <process name>

## Outcome
<What's different when this works, and how we'll know. One or two sentences.>

## Why now
<Time, quality, speed, or "doesn't happen today". Rough current cost: <n> hours per <week/month>.>

## What was tried before, and where it stopped
<The exact point it broke.>

## The process today
| # | Step | Tool | Who | Time |
|---|---|---|---|---|
| 1 | … | … | … | … |

## Readiness
| # | Access | Context | Guardrails |
|---|---|---|---|
| 1 | ready | fixable: <what's missing> | ready |
| 2–4 | all ready | | |

## Blockers and fixes
- **<blocker>** → <fix>, <effort>, <who>

## Design
| # | Done by | Check |
|---|---|---|
| 1 | deterministic / AI / human | test / advisory board / approval / none |

Runtime: <no-code platform | scheduled agent | script | mixed>, maintained by <who>, about <cost> per run.
Varies per instance (client, market): <list, or "n/a">.

Autonomy level to start: <assist | draft and approve | run and report | unattended>, because <reason>.
Move up a level when: <evidence, e.g. "ten runs with no correction">.

## Building blocks
- <skill or tool>: <why it fits here>

## First slice (this week)
- Scope: <steps n to m, on real input>
- Done when: <checkable result>
- Owner: <name>

## Risks
- <what could go wrong, and how we'd notice>
```

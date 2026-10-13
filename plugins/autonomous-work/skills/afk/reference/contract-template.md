# Contract and status templates

## `.afk/<slug>/contract.md`

```markdown
# AFK contract: <title>

Approved: <date, time> by <owner>   ← written only when the owner says go
Slug: <slug> · Branch: <branch> · Product URL/port: <...>

## Goal (in the agent's words, confirmed by the owner)
<2–4 sentences: what changes for whom, which outcome it serves.>

## Seat
Primary user: <seat>. Moments to walk: <...>.

## Vision anchor
<The sentence from the vision this serves, and the settled decisions that bind it.>

## Done criteria (each checkable by a command or in the product)
- [ ] <criterion> (check: <how>)

## Out of scope
- <tempting thing that will NOT be built>

## Decided forks
| Fork | Decision | Owner's words |
|---|---|---|

## Look and feel
Plan page: <link, version>. Mockups: <file → moments covered>.
Settled by the mockup: <...>. Open toggles and their decision: <...>.

## Slices (in order)
1. <slice>: <criteria it closes>

## Risk class and end state
- Risk: <internal only / schema / paid runs / outward-facing (publishing, messages)>
- Explicitly allowed outward actions: <e.g. publish a scratch page to the staging CMS and take it down>
- Park instead of deciding: <additions to the default park list>
- End state: <local commits + clean ship check + runnable product> <or: branch pushed (allow_push)>

## Budget
Time: <hours>. Paid calls: up to <amount>. Review rounds: 3 per slice.
```

## `.afk/<slug>/status.md`

```markdown
# Status: <slug>

## Done criteria
- [ ] <copied from the contract>

## Slices
| # | Slice | State | Review rounds | Commit |
|---|---|---|---|---|

## Log
- <time> started
```

The Stop hook reads the `## Done criteria` section: it refuses to end the
turn while any `- [ ]` remains there and `HANDBACK.md` doesn't exist.

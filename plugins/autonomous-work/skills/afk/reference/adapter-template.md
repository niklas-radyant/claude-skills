# Project adapter template

Copy to `<repo>/.claude/afk/project.md` during the first plan in a repo, and
fill it in with the owner. The reviewers read it in full, so keep it about
this project only; how the owner judges in general belongs in the profile.

```markdown
# AFK adapter: <project>

## Vision and design sources (reviewers read these in full)
- <path>: <what it is: product vision, north star, settled decisions>
- <path>: <design system / UI conventions>
- <path>: <usability or accessibility rules>
- <path>: <engineering conventions that bind every change>
If the vision is spread across many places, consolidate it into one file
first; reviewers can't judge consistently against eight partial sources.

## Conflict order (when principles collide)
1. Safety: production data, customer data, money, anything outward
2. <the project's north star>
3. <e.g. calm / fewer elements>
4. <reuse of existing patterns>
5. <speed>
Tie-breakers: simpler wins; reversible beats irreversible.

## Reference screens (the design critic shoots these for comparison)
| Screen | Route / command | Why it's a reference |
|---|---|---|

## Seats and moments
Default user: <who, how skilled, how much time>. Other seats: <...>.
Moments to walk: <e.g. Monday morning with a full week, right after a customer call, cold open after two weeks away>.

## Verification
- Code: <exact commands, read from CI>
- Product: <how to run it locally; how to get past login without a human (dev auth bypass, seeded test user); port>
- Data: <which database or fixtures; what is safe to write to; scratch-entity rule>
- Screenshots: `node <plugin>/skills/afk/bin/shoot.mjs --url <url> --out <png> [--theme dark] [--full] [--click "<selector>"]`

## Preflight (everything that would interrupt an unattended run)
- [ ] isolated worktree/branch, base fresh
- [ ] secrets present without a prompt (e.g. a service-account token, not a desktop-app approval)
- [ ] product runs and serves without a login redirect
- [ ] screenshot works
- [ ] test + typecheck baseline recorded
- [ ] <project-specific>

## Park list (in addition to the skill's defaults)
- <areas owned by someone else>
- <expensive or sensitive subsystems>

## End state
Default: local commits, the ship check run clean up to (not including) opening
a PR, the product left runnable, HANDBACK.md. <Or what the owner allows instead.>

## Backtest
<where rejected/accepted screens with the owner's verdicts live (keep it out of
git if screenshots contain customer data)>
```

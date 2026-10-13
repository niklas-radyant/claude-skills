---
name: afk
description: AFK mode. A deep alignment session with you, then a fully autonomous run to an agreed milestone, with independent reviewers instead of check-ins and a decision log instead of questions. One command, /afk, picks the phase from the run state (plan, go, learn). Use when the user says "afk", "I'll be away", "work through this on your own", "run this autonomously until X", or wants a work package built while they're gone.
argument-hint: "[topic for a new run]"
---

# AFK mode: align deeply, then run without the human

## Why this exists

Long autonomous runs fail in two predictable ways. The agent stops to ask
about something it could have decided, and the human comes back to a
stalled session. Or it decides something it should not have (it bloats a
screen, drifts from the product's direction, or does something
irreversible), and the human comes back to rework. Telling the agent "don't
ask, but build what I'd want" fixes neither, because the same model that
builds also grades its own work and agrees with itself.

AFK mode splits the work into three phases:
- **Plan.** All questions are asked while the human is still there.
- **Go.** Independent reviewers judge every slice against the owner's written
  taste and the project's vision. Every fork is either decided by a written
  rule and logged, or parked for later.
- **Learn.** The owner's corrections after the run become rules, so the next
  run needs fewer of them.

## Files

| File | What it is | Who writes it |
|---|---|---|
| `~/.claude/afk/profile.md` (or `<repo>/.claude/afk/profile.md`) | How the owner works and judges: verification bar, taste, hard lines, how to report | the `taste-profile` skill, refined by learn |
| `<repo>/.claude/afk/project.md` | Project adapter: vision sources, reference screens, seats, verification commands, preflight, park list, end state | plan creates it from [reference/adapter-template.md](reference/adapter-template.md) |
| `<repo>/.afk/<slug>/` | One run: `contract.md`, `status.md`, `decisions.md`, `parked.md`, `verify-<n>.md`, `reviews/`, `HANDBACK.md` | this skill (keep `.afk/` git-ignored) |
| `<repo>/.afk/ACTIVE` | Exists only while a run is going; the plugin's hooks enforce the run's rules while it does | this skill |

No profile yet? Run the `taste-profile` skill first. Without one, the
reviewers fall back to generic taste, and generic taste is exactly what
produces the rework this skill exists to prevent. Say so, then continue only
if the owner wants to.

## Which phase

Read `.afk/` and say in one line which phase you're in and why:
- topic given, or no open run → **plan**
- contract has an `Approved:` line, no `HANDBACK.md` → **go** (also to resume an interrupted run)
- `HANDBACK.md` exists, not learned from yet → **learn** (if the owner hasn't reviewed yet, show the handback and the parked questions)
- several open runs → name them, take the most recent

## Phase 1: plan (owner present)

Goal: a contract precise enough that the run never needs the owner. Spend
the time here; an hour of alignment saves a day of rework.

1. **Ground yourself in use, not only in code.** Read the profile, the
   adapter and every source it lists, and the code you'll touch. Fetch and
   check the base isn't stale. Then walk today's flow as the user would
   (browser, CLI, API, whatever the product is), and open with a concrete
   critique ranked by impact: clicks counted, things said twice. A generic
   opening wastes the first round.
2. **Restate the goal** in 2–4 sentences: what changes for whom, which
   outcome it serves, what's explicitly out. Let them correct it.
3. **Make it visible before it's built.** For anything with a UI: one
   living plan page, real-product references when a new pattern is needed,
   and a clickable mockup of every state in the product's real look. Rate
   the mockup yourself out of 10 before showing it. Procedure:
   [reference/planning.md](reference/planning.md).
4. **Ask the forks deep.** List every place where two reasonable builders
   would build differently, including look and feel, and ask them in rounds
   (4 per round, as many rounds as needed). Put the recommendation first.
   Free-text answers are the most valuable signal, so follow up on them. Skip
   whatever the decision rule below settles. Close with a "what you want vs
   today" table and one "is this right?" question. Answer every question the
   owner asked along the way.
5. **Write the contract** from
   [reference/contract-template.md](reference/contract-template.md):
   - milestone, and the user it's for
   - done criteria, each checkable by a command or in the product
   - out of scope
   - decided forks, in the owner's words
   - plan and mockup references
   - risk class and end state
   - slices in order
   - budget
6. **Preflight**: the adapter's preflight section. Resolve everything that
   would interrupt the run while the owner is still there: secrets,
   logins, the dev server, auth for local testing, a fresh base, a green test
   baseline. A failed item blocks go.
7. **Ask for the go.** Ask once, with a summary: the milestone, the slices,
   the end state, and what will be parked instead of decided. On yes, write
   `Approved: <date> by <owner>` at the top of the contract and start go in
   this session. The owner never types a second command.

## Phase 2: go (owner away)

**Start**
- `mkdir -p .afk/<slug>`, then `printf '%s\n' <slug> > .afk/ACTIVE`.
- Add `allow_push` as a second line only if the contract's end state pushes
  (for example, a cloud run whose VM can be reclaimed).
- Make sure `.afk/` is git-ignored.
- Keep the machine awake (`caffeinate -dims -t <seconds> &` on macOS,
  `systemd-inhibit` on Linux).
- Copy the done criteria into `status.md` as `- [ ]` items.

**What the plugin's hooks enforce** while `.afk/ACTIVE` exists:
- no questions to the owner and no plan-mode approvals
- no secret-manager CLIs that prompt (`op` by default; add more with
  `AFK_BLOCKED_CLIS`)
- no PR create or merge
- no `git push` without `allow_push`
- the turn can't end while `status.md` has open criteria and there is no
  `HANDBACK.md`

**The slice loop**, in contract order:
1. **Build.** Reuse before you create. Follow the decided forks literally.
2. **Verify for real.** Run the tests, then the real flow the way its user
   would, with real data, in every state, including paid runs the slice needs.
   Write the walk to `verify-<n>.md`. "Tests pass" is not verified.
3. **Review gate.** Start the three reviewer agents in parallel. Installed as
   a plugin, their agent types are namespaced:
   `autonomous-work:afk-design-critic` and so on. Use whichever name your
   agent list shows.
   - `afk-design-critic`: calm, bloat, reuse, consistency. It takes its own
     screenshots.
   - `afk-seat-walker`: cold open and the real moments from the user's seat.
   - `afk-vision-guardian`: vision fit, scope, engineering taste, verification
     evidence.

   Pass them the run dir, the slice, the URLs or commands with the states to
   open, and the seat. Never pass your own reasoning; they judge the result.
   - **Prepare every state first.** Reviewers run in parallel and must never
     change data. If a state needs data (empty, all done, 20+ items), set it
     up beforehand: a separate data file, fixture or port per state. Then
     hand them URLs that open each state without any clicks that write.
   - **A slice with no visible change** (API only, refactor) gets only the
     vision guardian. The other two review it with the next visible slice.
4. **Act.**
   - Fix every BLOCKER and MAJOR.
   - Remove whatever on the critic's removal list you can't defend in one
     sentence.
   - POLISH is optional, and never a reason for another round.
   - Re-verify what changed, then run the reviewers again.
   - Stop at 3 rounds per slice. A BLOCKER that is still there goes to
     `parked.md` with both sides' arguments, and the run continues around it.
5. **Commit** the slice: small commits, no secrets or personal data. Tick
   its criteria in `status.md` and log a line. Push only with `allow_push`.

**Deciding without the owner.** Every fork the contract didn't settle gets
one entry in `decisions.md`: the fork, the options, which one was chosen, the
rule that decided it, and how to reverse it.
- **Decide** when it's reversible and inside the contract. Use the adapter's
  conflict order, then: simpler wins, reuse beats new, fewer elements beat
  more, a general mechanism beats special cases, reversible beats
  irreversible. Be brave; a reasoned call the owner can revert beats a
  stalled run.
- **Park** (`parked.md`, then build around it) anything that touches:
  - production data or customer data
  - money beyond the budget
  - anything that leaves the house
  - permissions
  - a schema change the contract didn't foresee
  - a settled product decision
  - someone else's area
  - the adapter's park list
- **Never** wait, ask, or end the turn to check in. Stuck on a technical
  problem? Investigate from first principles and try alternatives. Only an
  external hard blocker justifies parking.

**Context.** A run can outlast the context window. `status.md` is the source
of truth. After a compaction, re-read the contract, the status and the
latest decisions before continuing.

**End state** (when every criterion is ticked or parked):
1. Bring in the base again, and re-run the tests.
2. Run the adapter's ship check up to, but not including, opening a PR.
3. Leave the product runnable for the owner's review, and take a final
   screenshot set.
4. Write `HANDBACK.md`:
   - what was built, per criterion, with a link
   - a 5–10 step review path
   - the top decisions, each with the rejected option
   - the parked items as ready-to-ask questions, each with a recommendation
   - what the run cost
   - what the reviewers flagged that you overrode, and why
5. `rm .afk/ACTIVE`, then notify the owner (PushNotification if available).

## Phase 3: learn (after the owner's review)

1. Collect every correction the owner made on this run.
2. Classify each one:
   - a missing rule (add it to the profile or the adapter)
   - a rule a reviewer missed (sharpen that agent, or add the case to the
     backtest)
   - a decision rule that picked wrong
   - a contract gap (the plan asked too little)
3. Propose the concrete edits as a short list, and apply what the owner
   approves.
4. If you changed a reviewer or the profile, re-run the backtest
   (`taste-profile` skill, backtest section) and report the hit rate.

## Stale run

If `.afk/ACTIVE` exists but nothing is running, the hooks keep blocking.
Remove it with `rm .afk/ACTIVE`. The run's folder stays, so `/afk` can
resume.

## Rules and limits

- **The reviewers are only as good as the profile and the adapter.** A
  reviewer has never seen this owner reject a screen, so without written
  taste it judges by generic taste. Calibrate with `taste-profile` and check
  with its backtest.
- **Reviewers find too much before they find too little.** A miscalibrated
  critic finds MAJORs on screens the owner would accept, which costs rounds
  and can polish a good screen into a worse one. The 3-round cap and the
  first-reaction ceiling in the critic exist for that.
- **This is not a security boundary.** The hooks match command text and are
  a convenience. Real protection belongs in branch protection, permission
  deny rules and scoped credentials.
- **Unattended means unattended.** Anything the contract allows will happen
  while nobody watches: publishing, paid calls, pushes. Approve the contract
  as if you won't see the run, because you won't.
- **Cloud runs** need the repo to carry everything: the adapter, the profile
  if the reviewers should use it, and the setup. See
  [reference/cloud.md](reference/cloud.md).

# Claude Code skills

Claude skills I built to make my life easier, packaged to be shared and
hopefully be beneficial to others.

Each one started as an internal skill in the production codebase at
[Radyant](https://radyant.io) and earned its place there before it landed
here — then got stripped of everything specific to that repo.

MIT licensed. No attribution required.

## Install

```bash
/plugin marketplace add niklas-radyant/claude-skills
```

Then install whichever plugin you want:

```bash
/plugin install pr-workflow@niklas-skills
```

Skills activate on their own when a task matches, or you can call one
directly — `/pr-preflight`.

**Not using plugins?** Every skill is a self-contained directory. Copy the
one you want:

```bash
git clone https://github.com/niklas-radyant/claude-skills.git
cp -r claude-skills/plugins/pr-workflow/skills/pr-preflight ~/.claude/skills/
```

That works for any agent tool that reads `SKILL.md` files, not just Claude
Code.

## The skills

| Skill | Plugin | What it does |
|---|---|---|
| [`pr-preflight`](#pr-preflight) | `pr-workflow` | Reviews your own diff adversarially before you open the PR, runs the gates your CI runs, fixes what it finds |

---

### `pr-preflight`

**Review your own diff before the PR opens, not after.**

Runs on every substantive PR at Radyant, where it also drives our automated
review tiering — the stamp mechanism described below is in production, not a
proposal.

```bash
/plugin install pr-workflow@niklas-skills
```

A review finding is cheapest while the branch is still yours. Once the PR is
open, a fix means another push, another review cycle, and a race against
auto-merge — and reviewers who routinely receive obvious problems learn to
skim the non-obvious ones.

So it does the pass first. It establishes the real base branch (the one the
PR actually targets, not whatever `main` happens to be), reads the diff,
reviews it as an adversary rather than as the author, runs the repo's gates,
fixes the blocking findings, and reports what it skipped.

The part that makes it work in a repo it wasn't written for: **it discovers
the gates instead of assuming them.** It reads your CI config first, on the
principle that CI is the source of truth for what actually blocks a PR, then
falls back to aggregate scripts (`make check`, `tox`), manifest scripts, and
hook config. It runs what's fast and hermetic, refuses to run what needs
credentials or a live database, and names every gate it skipped rather than
letting silence imply it passed.

Two reference files, loaded only when relevant:

- **`reference/stack-checklists.md`** — the defects that recur per ecosystem:
  JS/TS, Python, Go, Rust, SQL and migrations, CI workflows, shell,
  dependency changes.
- **`reference/ci-stamp-recipe.md`** — optional. If you run an automated AI
  review on every PR, this is the pattern for routing author-reviewed PRs to
  a cheap verification pass instead of a full discovery pass: the four design
  rules that keep it honest, and a worked GitHub Actions example.

That second one is the piece most worth stealing if you're paying for AI
review. The short version: discovery is the expensive job, verification is
not, and a PR whose author already did a full pass needs the second one. The
author's session marks the PR with `Preflight-Reviewed: <head SHA>`, and CI
routes on it — but sensitive paths always keep the deep review regardless
(an author-side review is not independent), the stamp never skips review
entirely, anything ambiguous fails safe to deep, and pinning the exact SHA
means a stamp can only ever vouch for code that existed when it was written.
Those four rules together are what make it safe to trust a self-asserted
claim at all: the worst case for a forged stamp is a non-sensitive PR getting
the cheap reviewer instead of the expensive one.

The stamp is opt-in and self-detecting — the skill greps your CI for the
convention and only stamps if something actually reads it, so in a repo that
doesn't, you get the review pass and no dead boilerplate in your PR body.

---

## How I write these

In case you're writing your own, and so you know what to expect from mine:

- **Procedures, not vibes.** A skill should say what to do in what order,
  with the commands. "Be careful about security" changes nothing.
- **Discover, don't assume.** A skill that hard-codes `npm run lint` works in
  one repo. One that reads the repo's CI works everywhere. This is usually
  the whole difference between a personal shortcut and something shareable.
- **Progressive disclosure.** The main `SKILL.md` stays readable; detail goes
  into `reference/` files loaded on demand. Every token in a skill body is a
  token the model reads on every single invocation.
- **State the failure modes.** What the skill does *not* do, and where it can
  be wrong, belongs in the skill. A skill that oversells itself gets trusted
  in situations it can't handle.
- **Earn it in use.** Skills here have been run repeatedly on real work and
  fixed where they broke. When one stops being useful I'll remove it.

## Pull requests

This is my personal toolbox rather than a community project, so I'm not
taking PRs. Fork it, copy a skill out of it, rewrite whatever doesn't fit
how you work — that's what the MIT license is for, and no attribution is
needed.

One exception: if a skill **misfires** in a repo shaped differently from
mine, please open an issue. That's the failure mode I can't test for
myself, and it's how both bugs fixed so far were found.

## License

[MIT](LICENSE).

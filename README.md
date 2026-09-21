# Claude Code skills

A small, growing collection of [Claude Code](https://claude.com/claude-code)
skills I built while shipping real work, then generalized so they're useful
outside the repo they came from. Free to use, copy, fork, or ignore.

Each skill here earned its place by being run repeatedly, not by sounding
like a good idea. When one stops being useful I'll remove it.

## Install

```bash
/plugin marketplace add niklas-radyant/claude-skills
/plugin install niklas-skills
```

Skills then appear as `niklas-skills:<name>` and activate when a task
matches their description — or you can invoke one directly, e.g.
`/pr-preflight`.

Prefer not to use plugins? Every skill is a self-contained directory. Copy
the one you want into your own `.claude/skills/`:

```bash
git clone https://github.com/niklas-radyant/claude-skills.git
cp -r claude-skills/skills/pr-preflight ~/.claude/skills/
```

That also works for other agent tools that read `SKILL.md` files.

## What's in here

### `pr-preflight`

Review your own diff adversarially **before** opening a pull request, run
the gates the repo's own CI runs, fix what you find, and open the PR clean.

The premise: a review finding is cheapest while the branch is still yours.
Once the PR is open, a fix means another push, another review cycle, and a
race against auto-merge — and reviewers who routinely receive obvious
problems learn to skim.

What makes it work in an unfamiliar repo is that it **discovers** the gates
instead of assuming them. It reads the CI config first, because CI is the
source of truth for what actually blocks a PR, then falls back to aggregate
scripts, manifest scripts, and hook config. It runs what's fast and
hermetic, refuses to run what needs credentials or a live database, and
reports what it skipped rather than implying it passed.

It ships two reference files, loaded only when relevant:

- `reference/stack-checklists.md` — the defects that recur per ecosystem
  (JS/TS, Python, Go, Rust, SQL and migrations, CI workflows, shell,
  dependency changes).
- `reference/ci-stamp-recipe.md` — optional. If your repo runs an automated
  AI review on every PR, this is the pattern for routing author-reviewed PRs
  to a cheaper verification pass instead of a full discovery pass, with the
  design rules that keep it honest and a worked GitHub Actions example.

The stamp is opt-in and self-detecting: the skill greps your CI for the
convention and only stamps if something actually reads it. In a repo that
doesn't, you get the review pass and no inert boilerplate in your PR body.

## How I write these

In case it's useful if you're writing your own, or want to know what to
expect from mine:

- **Procedures, not vibes.** A skill should say what to do in what order,
  with the commands. "Be careful about security" changes nothing.
- **Discover, don't assume.** A skill that hard-codes `npm run lint` works
  in one repo. One that reads the repo's CI works everywhere. This is
  usually the difference between a personal shortcut and something shareable.
- **Progressive disclosure.** The main `SKILL.md` stays readable; detail
  moves into `reference/` files loaded on demand. Every token in a skill body
  is a token the model reads on every invocation.
- **State the failure modes.** What the skill does *not* do, and where it
  can be wrong, belongs in the skill. A skill that oversells itself gets
  trusted in situations it can't handle.
- **No house rules.** Anything true only of my employer's codebase got
  stripped or turned into a documented option.

## Contributing

Issues and PRs are welcome — particularly stack checklist entries for
ecosystems I don't work in daily, and reports of where a skill misfires in
a repo shaped differently from mine.

I'm keeping the collection deliberately small, so I may decline a skill
that's useful but that I won't personally maintain.

## License

MIT — see [LICENSE](LICENSE). Use it commercially, modify it, no attribution
required (though it's appreciated).

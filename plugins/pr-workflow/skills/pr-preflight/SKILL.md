---
name: pr-preflight
description: Review your own diff adversarially before opening a pull request, run the gates the repo's own CI runs, and fix what you find so the PR opens clean. Use right before `gh pr create` or opening a PR, and when the user says "preflight", "pre-review", "review this before I push", or "is this ready to open?".
---

# PR Preflight — find it before the PR opens, not after

## Why this exists

A review finding that arrives *after* the PR is open is worth less than the
same finding five minutes earlier:

- **The branch may already be gone.** Auto-merge lands a green PR while you
  are still reading the review. A fix pushed then has nowhere to go.
- **It costs a second review.** Every push restarts the review — human
  attention, or paid API tokens if the repo reviews with a model — on work
  you could have corrected yourself.
- **It trains reviewers to skim.** A PR that reliably arrives with the
  obvious problems already fixed earns a sharper read on the non-obvious
  ones.

So do the review pass yourself, on your own branch, while nobody else is
looking. A finding is cheapest while the branch is still yours.

This is **not** a substitute for independent review. An author reviewing
their own work shares the author's blind spots — which is exactly why the
high-blast-radius paths in a repo should still get a real second pair of
eyes. Preflight clears out the noise so that review can spend its attention
on the parts needing judgment.

## Procedure

### 1. Establish the diff

Everything you intend to ship must be committed first. If `git status` is
not clean, you are about to review something other than what will be pushed.

Find the **actual** base branch instead of assuming `main`:

```bash
base=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
[ -n "$base" ] || base=$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
echo "base: $base"
```

If `origin/HEAD` is missing locally, `git remote set-head origin -a` sets it.

That gives you the *default* branch. If the PR is already open, or will
target something else (a release branch, or another PR in a stack), the base
is whatever the PR says — ask the repo, not the default:

```bash
gh pr view --json baseRefName --jq .baseRefName 2>/dev/null   # if open
```

Reviewing against the wrong base either hides your changes or attributes
someone else's to you.

Then fetch that base and read exactly what you are proposing:

```bash
git fetch origin "$base"
git diff --stat "origin/$base...HEAD"   # three dots: your commits only
git diff "origin/$base...HEAD"
```

If the diff is large, review it file by file rather than skimming the whole
thing. A skimmed review is worse than an honest "this is too large to review
carefully — splitting it".

### 2. Discover the gates — read CI, don't guess

**The repo's CI is the source of truth for what blocks a PR.** Guessing
`npm test` wastes a run when the real gate is `make verify`. Look in this
order and stop once you have the actual commands:

1. **CI config** — `.github/workflows/*.yml`, `.gitlab-ci.yml`,
   `.circleci/config.yml`, `Jenkinsfile`, `azure-pipelines.yml`,
   `.buildkite/`. Read the jobs that fire on pull requests and copy the
   exact commands. If the repo documents which checks are *required*, those
   are the gates that matter; the rest are advisory.
2. **An aggregate script**, if one exists — `<pm> run check`, `make check`,
   `just check`, `tox`, `nox`, `./scripts/verify.sh`. A repo that maintains
   one usually intends it as "what CI runs". Prefer it over assembling the
   pieces yourself — but **read what it chains together first.** Aggregates
   routinely bundle a step that isn't safe to run here (a link checker that
   fetches, a deploy, an integration suite). When one does, run the
   hermetic pieces individually and report the step you left out. An
   aggregate is a convenience, not a license to skip the judgment in the
   next paragraph.
3. **Manifest scripts** — `package.json` → `scripts`; `Makefile` targets;
   `pyproject.toml`; `Cargo.toml`; `Taskfile.yml`; `Rakefile`; `mix.exs`;
   `composer.json`; `deno.json`.
4. **Hook config** — `.pre-commit-config.yaml`, `lefthook.yml`, `.husky/`.
   These are gates too; they fire on the contributor's machine.
5. **Contributor docs** — `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, and
   the README's development section.

**Use the repo's toolchain, not your habits.** In a JS/TS repo the lockfile
decides which package manager to invoke — `pnpm-lock.yaml` → `pnpm`,
`yarn.lock` → `yarn`, `bun.lockb` → `bun`, `package-lock.json` → `npm`:

```bash
ls pnpm-lock.yaml yarn.lock bun.lockb package-lock.json 2>/dev/null
```

The wrong one can resolve different versions than CI will, or fail outright
on a lockfile it doesn't read. The same caution applies elsewhere: prefer
`uv`/`poetry`/`pdm` where the repo has that lockfile rather than bare `pip`.

Then run them. Two rules about what to actually run:

- **Run what is fast and hermetic** — type checks, linters, formatters,
  unit tests, build. No secrets, no network, no shared state.
- **Do not run what needs credentials, a live database, a deployed
  environment, or minutes of wall clock.** Integration suites against real
  services, deploys, migrations against a shared DB: skip them, and name
  every skipped gate in your report so nobody assumes it passed.

If a gate fails for a reason your diff did not cause, confirm that by
running it on the base branch, then say so. Don't absorb someone else's
failure into your PR.

### 3. Review as an adversary

Your job is to find what you got wrong, not to confirm what you got right.
The author's instinct is to re-read code as *intended*; read it instead as
someone who wants it to break. For each change, ask what input, ordering, or
state would make it wrong — then go check whether that state is reachable.

Universal dimensions, in priority order. The first three are where real
defects live; the rest are cheap once you are already in the file.

1. **Correctness** — logic inverted or off by one; `null`/`undefined`/empty
   collection paths; error and early-return paths (the happy path is the one
   you already tested); missing `await`, or a sequential loop that should be
   concurrent; unhandled rejections; state mutated while something else
   reads it; resources opened and never closed; a retry that isn't
   idempotent.
2. **Security and trust boundaries** — every new entry point (route,
   endpoint, handler, CLI flag, webhook, queue consumer, scheduled job)
   needs an explicit answer to "who is allowed to call this?"; untrusted
   input reaching a query, a shell, a file path, a template, or an outbound
   URL; secrets or tokens in code, logs, or error messages; data crossing
   from server to client that shouldn't.
3. **Data and persistence** — a query inside a loop; an unbounded read (no
   `LIMIT`, no `where`); an `UPDATE`/`DELETE` whose scope is wider than
   intended; a schema change with no migration, or a migration that cannot
   be rolled back; a new column or query pattern with no supporting index; a
   uniqueness guarantee you rely on but never declared.
4. **Contracts and compatibility** — a changed signature, response shape,
   event payload, exported type, or config key that code you did not touch
   still depends on. Grep for callers instead of assuming there are none.
5. **Type and safety escape hatches** — each one is a claim made without
   proof: `any`, `as`, `@ts-ignore`, non-null `!`, `unwrap()`, `panic!`,
   `interface{}`, bare `except:`, `# type: ignore`, unchecked casts. Justify
   it in a comment or remove it.
6. **Quality and coverage** — leftover debug output, commented-out code, a
   TODO you meant to resolve, duplication of something the repo already has,
   and new code paths with no test where comparable paths are tested.

For stack-specific gotchas, read `reference/stack-checklists.md` — load only
the sections your diff actually touches.

Tag every finding:

- 🔴 **blocking** — wrong, unsafe, or breaks something. Fix it.
- 🟡 **should fix** — will cause a problem or an argument later. Fix it.
- 🟢 **nit** — preference or polish. Your call; mention it in the PR body if
  you leave it.

### 4. Fix, then re-run

Fix every 🔴 and 🟡 and commit normally — separate commits or amended into
the relevant ones, whichever matches the repo's history style. Then re-run
the gates from step 2: a fix that breaks a test is a worse outcome than the
finding it addressed.

If a finding is real but genuinely out of scope, don't leave it silent.
File it, or name it in the PR body as known and deferred.

### 5. Optional: stamp the PR (only if this repo's CI reads the stamp)

Some repos run a **tiered automated review**: a cheap verification pass for
PRs the author already reviewed, a deep pass for everything else. Those
repos recognize a line in the PR body:

```
Preflight-Reviewed: <full 40-char head SHA>
```

**Check whether this repo actually reads it before adding it:**

```bash
git grep -il "preflight-reviewed" -- .github .gitlab-ci.yml Jenkinsfile .circleci
```

Exit 0 with a filename means something reads it; exit 1 means nothing does.

- **No match → do not add the line.** It would be inert text in the PR body
  and misleading to the next reader. You're done; skip to step 6.
- **Match → stamp it** with the SHA of your *final* commit:

  ```bash
  git rev-parse HEAD
  ```

  PR not open yet: include the line at the end of the body you pass to
  `gh pr create`. PR already open: read the current body first
  (`gh pr view <n> --json body --jq .body`), append the line, then
  `gh pr edit <n> --body-file <file>`. Never clobber a body you haven't read.

The stamp pins one exact SHA, so any later push invalidates it. That's the
point: it can only ever vouch for a head that was actually reviewed.

To set this pattern up in your own repo, see `reference/ci-stamp-recipe.md`.

### 6. Report

Tell the user, briefly:

- what you found by severity, and what you fixed;
- which gates you ran and their results — and which you skipped, and why;
- anything real you deliberately left, and where it's tracked;
- if you stamped, the short SHA the stamp is pinned to.

## Rules

- **Never claim a review you did not do.** Don't stamp, and don't report
  "preflight clean", without actually reading the diff and running the gates
  in this session. A stamp on an unreviewed head destroys the only thing
  that makes the mechanism worth having.
- **A finding you make yourself belongs before the PR opens.** After it's
  open, pushing restarts reviews, can race an auto-merge, and invalidates
  any stamp. Something found later belongs in a follow-up PR off the fresh
  base.
- **Report failures as failures.** A gate that failed, a suite you couldn't
  run, a file too large to review carefully — say so plainly. "Looks good"
  over an unverified diff is the one output worse than no preflight at all.
- **Don't fix unrelated things.** An unrelated bug you spot is a separate PR
  or an issue, not scope creep in this one.

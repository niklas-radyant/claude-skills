# The preflight stamp: tiered automated review

This is the optional half of `pr-preflight`. You only need it if your repo
runs an **automated AI review on every PR** and you'd like to pay less for
the PRs whose author already did the work.

Skip this file entirely if your repo doesn't do that. The skill's review
pass works on its own.

## The problem it solves

An automated review on every PR is genuinely useful and genuinely not free.
Run a frontier model over every diff and you pay frontier prices for the
doc typo and the auth rewrite alike. Route everything to a cheap model and
you stop catching the things worth catching.

So route by risk. The tier that matters here:

> A PR whose author already ran a full review pass locally does not need a
> model to *discover* findings. It needs one to *verify* that the pass
> happened and didn't miss anything obvious.

Discovery is the expensive job. Verification is not. If the author's session
runs on a flat-rate subscription and CI runs on metered API billing, moving
discovery to the author's session is a straight cost transfer — the work
still happens, on tokens that are already paid for.

## The mechanism

The author's session adds one line to the PR body:

```
Preflight-Reviewed: <full 40-char head SHA>
```

CI greps the body for that line **with the current head SHA interpolated**.
Match means the author reviewed *this exact commit*; CI drops the review to
the cheaper verifying model. No match means either no preflight, or a
preflight followed by more commits — both correctly get the full pass.

That SHA pinning is the whole integrity story. The stamp can't vouch for
code that didn't exist when it was written.

## Design rules that make it safe

Adopt these together — each one closes a hole:

1. **Never downgrade sensitive paths.** An author-side review is not
   independent, so the paths where a miss is expensive (auth, permissions,
   payments, secrets, migrations, CI config itself) keep the deep review
   whether stamped or not. Check this *before* the stamp check, so path
   sensitivity always wins.
2. **Never let the stamp skip the review entirely.** It changes which model
   reviews, never whether one does. "Skip" is not a tier.
3. **Fail safe to deep.** If the workflow can't read the diff, can't reach
   the API, or gets an ambiguous answer, route to the deep model. A silent
   downgrade is worse than a redundant expensive review.
4. **Keep the blast radius of a forged stamp bounded.** Because of rules
   1–3, the worst case for a stamp someone pasted in without doing the work
   is: a non-sensitive PR reviewed by the cheap model instead of the
   expensive one. It still gets reviewed. That's an acceptable failure mode,
   which is what makes it safe to trust a self-asserted claim at all.
5. **Invalidate on push, automatically.** This is free — it falls out of
   pinning the SHA. Don't add an override.

## Worked example — GitHub Actions

A triage job that emits a model choice for a later review job to consume.
Adapt the model names and the sensitive-path pattern to your repo; the
control flow is the part worth copying.

```yaml
name: PR review

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

permissions:
  contents: read
  pull-requests: read

jobs:
  triage:
    if: github.event.pull_request.draft == false
    runs-on: ubuntu-latest
    outputs:
      model: ${{ steps.pick.outputs.model }}
      reason: ${{ steps.pick.outputs.reason }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - id: pick
        env:
          GH_TOKEN: ${{ github.token }}
          PR: ${{ github.event.pull_request.number }}
          REPO: ${{ github.repository }}
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
          HEAD_SHA: ${{ github.event.pull_request.head.sha }}
          # Paths where an author-side review is not enough. Tune this.
          SENSITIVE: '\.github/workflows/|migrations/|auth|permission|secret|billing|payment|crypto|\.env'
          DEEP_MODEL: 'your-frontier-model'
          CHEAP_MODEL: 'your-cheaper-model'
        run: |
          set -euo pipefail

          files=$(git diff --name-only "$BASE_SHA...$HEAD_SHA" || true)

          if [ -z "${files//[[:space:]]/}" ]; then
            # Couldn't read the diff. Fail safe: an unreadable diff must not
            # look trivial.
            model="$DEEP_MODEL"; reason="could not read changed files"
          elif printf '%s\n' "$files" | grep -qiE "$SENSITIVE"; then
            # Rule 1: path sensitivity wins over any stamp.
            model="$DEEP_MODEL"; reason="touches a sensitive path"
          else
            body=$(gh pr view "$PR" -R "$REPO" --json body --jq '.body // ""' || true)
            if printf '%s' "$body" | grep -qiE "preflight-reviewed:[[:space:]]*$HEAD_SHA"; then
              model="$CHEAP_MODEL"; reason="valid preflight stamp for $HEAD_SHA"
            else
              model="$DEEP_MODEL"; reason="no preflight stamp for this head"
            fi
          fi

          echo "model=$model" >> "$GITHUB_OUTPUT"
          echo "reason=$reason" >> "$GITHUB_OUTPUT"
          echo "Routing to $model — $reason"

  review:
    needs: triage
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Review
        run: |
          echo "Reviewing with ${{ needs.triage.outputs.model }}"
          echo "(${{ needs.triage.outputs.reason }})"
          # Invoke your reviewer here with the chosen model. When the stamp
          # routed this to the cheap model, tell the reviewer it is verifying
          # an author-reviewed diff, not discovering findings cold — the
          # prompt should differ, not just the model.
```

Two notes on the snippet:

- `grep -qiE "...$HEAD_SHA"` interpolates the SHA into the pattern. A SHA is
  hex-only so it can't inject regex metacharacters, but if you ever match
  something user-controlled the same way, switch to `grep -F` on a
  constructed literal.
- Reading the PR body needs `pull-requests: read`. Don't widen it to
  `write` unless a later job actually posts.

## Other tiers worth having

The stamp is one rule in a router. Others that pay off, roughly in the order
you'd add them:

- **Mechanical-only diffs → cheap model.** Lockfile-only dependency bumps,
  generated files, formatter-only changes. There's nothing to discover.
- **Deterministic escalation on size.** Past some number of changed files or
  lines, take the deep review regardless of what else says otherwise.
- **Re-review only the delta.** On a second push, review the diff since the
  last reviewed SHA rather than the whole PR again.
- **A second opinion from a different vendor's model**, advisory and
  non-gating, with the primary reviewer verifying each finding before
  acting. Two models miss different things; two models that agree on a
  finding are worth listening to.

---
name: advisory-board
description: Self-review before anything ships. Convenes a small board of named roles (for example the skeptical buyer, the editor, the fact-checker), each judging the output separately against written criteria, then revises and reports what changed. Use when the user says "advisory board", "review this before I send it", "self-review", "check this like a critic", "is this good enough", or whenever an automated workflow produces output nobody will look at before it goes out.
---

# Advisory board: let the output face its critics before a human does

## Why this exists

An automation is only worth running if you trust what comes out of it.
Deterministic no-code flows earn that trust by being predictable. AI output
doesn't, so most people end up re-reading everything, and the automation
saves nothing.

The obvious fix, "review your own work", barely works. The same model that
wrote a draft agrees with it, and a single generic reviewer finds generic
problems ("could be more concise"). What works better is a board: a few
roles with different stakes, each judging separately against criteria that
were written down before the draft existed. A buyer, an editor and a
fact-checker disagree in useful ways. One reviewer can't.

The board is only as good as what you teach it. A board that has never seen
your standards judges by average taste. Step 2 is where that gets fixed, and
it's the step people skip.

## Procedure

### 1. Name the output and its reader

One line each:
- **What is it?** A landing page, an AEO brief, an email to a client, a
  deck, a piece of code, a process design.
- **Who reads or uses it, and what should they do afterwards?** "A head of
  marketing at a mid-size software company should book a call" is a reader.
  "The audience" isn't.
- **What happens if it's wrong?** Embarrassment, lost deal, legal problem,
  wasted afternoon. This decides how strict the board is.

### 2. Load the charter, or write one

Look for a board charter in this order and use the first one you find:
1. a charter the user pasted, attached or pointed you to
2. in a chat project (Claude Projects, ChatGPT Projects): a charter in the
   project's files or instructions
3. in a repo or on disk: `.claude/board/<output-type>.md` or
   `board/<output-type>.md`
4. a brand guide, style guide, taste profile (`~/.claude/afk/profile.md`) or
   tone-of-voice document that is already in reach

If nothing exists, write a short charter with the user before judging
anything. Build it from the user's answers and examples, not from the draft
you're about to judge; a charter derived from the draft just describes the
draft. Template: [reference/charter-template.md](reference/charter-template.md).
Ask for two things, because they carry most of the signal:
- **One example they loved and one they sent back**, with the reason. Real
  corrections beat adjectives like "clean" and "on-brand".
- **Their hard lines**: what must never appear (made-up numbers, certain
  phrases, a competitor's name, promises legal hasn't cleared).

Name the charter after the output type in kebab-case, for example
`aeo-comparison-page`. Offer to save it so the next run doesn't start from zero: as a
project file in a chat project, as `.claude/board/<output-type>.md` in a
repo, or as a document the user keeps and pastes next time. In an
automation, the charter is the part a human maintains; the board runs by
itself.

**No charter and nobody to ask** (an automated run): seat only the reader
and the fact-checker, treat every factual claim as needing a source, put
"NO CHARTER" at the top of the report, and never mark the result ready to
ship unattended.

### 3. Seat the board

Pick **three to five** roles. Fewer misses things; more produces noise and
contradicting advice. Every board gets:
- **one role that is the reader** from step 1, in their actual situation
  (busy, skeptical, on a phone, comparing you to two competitors)
- **one role that checks facts and claims**: every number, name and
  promise has a source, or gets flagged

Fill the rest from the roles that fit the output type in
[reference/roles.md](reference/roles.md). Give each role a one-line
mandate and tell the user who is on the board before it convenes.

### 4. Judge separately

Each role reviews alone, without seeing the others' verdicts and without
your reasoning about why the draft is the way it is. They judge the result,
not the effort.

- **If you can start subagents** (Claude Code, the Agent or Task tool, any
  agent framework): one subagent per role, in parallel, each given the
  output, the charter, the reader and its own mandate (the fact-checker
  also gets the charter's list of sources). Nothing else.
- **If you can't** (a chat window): write each verdict as its own section,
  in order, and before each one restate the role's mandate and forget the
  previous sections' opinions. This is weaker. Say so in the report.

Each role returns, in this shape:

```
<Role> — verdict: ship | fix | stop
Blockers (must change before this goes out):
- <what, where, why it fails the charter or the reader>
Improvements (worth doing, not required):
- …
What to cut:
- …
The one thing I'd change if I could change only one:
```

**Stop** means the output shouldn't exist in its current form (wrong
reader, wrong goal, a claim that can't be backed). **Fix** means it's
close. **Ship** means a human could send it as is.

### 5. Chair the board

You are the chair now, not the author.
1. **A stop verdict first.** If every reason for it can be fixed by
   changing the text (an unsourced claim, a broken hard line), treat the
   reasons as blockers. If not (wrong reader, wrong goal), return the
   output to the human with the board's reasoning and don't revise.
2. Merge duplicate findings. Two roles finding the same problem is a strong
   signal; one role's taste is a weak one.
3. **Fix every blocker.** Cut whatever was flagged as "cut" unless you can
   defend it in one sentence.
4. Take improvements only when they're cheap and don't contradict the
   charter. Never take one that adds length to fix a different role's
   complaint about length.
5. When roles contradict each other, the charter decides. Inside the
   charter, hard lines beat "what good looks like". If neither settles it,
   the reader role wins.
6. When a must-have can't be met without facts you don't have, leave a
   visible placeholder (`[NEEDS SOURCE: market share of Tool X]`) and list
   it as open. Never fill it with a plausible number.
7. Add only what a blocker requires, and keep the author's voice. If most
   of the draft had to go, say so in the report rather than quietly
   rewriting it into a different piece.
8. Re-run only the roles that raised blockers, on the revised version.

**Stop after two rounds.** A blocker still open after round two goes to
the human with both sides of the argument. A third round tends to polish a
good draft into a blander one.

### 6. Report

Lead with the final output, then a short board report:
- who sat on the board
- what changed, one line per change, with the role that asked for it
- what was flagged and deliberately not changed, and why
- anything that needs a human: open blockers, claims nobody could source

In an automated pipeline, the report is the audit trail. Store it next to
the output.

## Rules

- **Criteria first, draft second.** A charter written after reading the
  draft just describes the draft.
- **Never invent a source to settle a fact-check.** An unsourced claim gets
  removed or flagged, not decorated.
- **The board advises; it doesn't take over.** Don't rewrite the piece in
  the board's voice. Fix what was found, keep the author's voice.
- **Ship is a valid verdict.** If every role says ship, report that and
  stop. A board that always finds something is miscalibrated.

## Where it can be wrong

- **It's still one model.** Separate roles reduce self-agreement, they don't
  remove it. For anything high-stakes (legal, money, a large audience) the
  board is the step before a human review, not a replacement for it.
- **It can't verify what it can't reach.** The fact-checker can only check
  against sources it has access to. If the numbers live in a tool it can't
  open, it flags them as unverified; it doesn't confirm them.
- **Boards over-find before they under-find.** Without a charter, expect
  generic advice and too many "improvements". If the user keeps overruling
  the board on the same point, that point belongs in the charter.

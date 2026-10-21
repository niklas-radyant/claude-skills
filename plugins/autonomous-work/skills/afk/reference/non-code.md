# AFK for work that isn't code

The method doesn't depend on code: ask everything up front, write a
contract, build in slices, let independent reviewers judge each slice, decide
or park instead of asking, hand back with a decision log. It works for any
larger piece of work with a clear "done":

- a research report or market analysis
- a content package (ten articles, a newsletter series, a set of briefs)
- a campaign: landing page copy, emails, ads, social posts
- a strategy document, a pitch deck, a training curriculum
- cleaning up and restructuring a large set of documents or a spreadsheet

## What changes

| Code run | Non-code run |
|---|---|
| Repo, branch, commits | A project folder (or a Claude/ChatGPT project) holding the run files and the deliverables. Save a version after each slice. |
| Done criteria checked by commands | Done criteria checked by reading: "every claim has a source link", "each article answers its question in the first two sentences", "the deck works with headlines alone". Write them so a reviewer can tick them without asking. |
| Verify by running the product | Verify by using the deliverable the way its reader will: read it cold, follow every link, recompute every number, check the facts against the sources. Write the walk to `verify-<n>.md`. |
| Design critic, seat walker, vision guardian | An `advisory-board` per slice: the reader, the fact-checker, plus roles for the field (editor, the client's CMO, the CFO, the person who has to execute it). Each judges separately against the profile and the contract. |
| Adapter: vision docs, verification commands | Adapter: who it's for, brand and tone sources, the sources the fact-checker may use, examples of work the owner liked and rejected, what must never be published. |
| Hooks block questions, pushes and early stops | No hooks outside Claude Code. The rules still hold; follow them yourself and say in the handback if you broke one. |

## Park list for non-code work

On top of the general park list, park anything that:
- publishes, sends or posts to anyone outside the owner's team
- names a client, a person or a number the owner hasn't cleared
- spends money (ads, paid tools, freelancers)
- makes a claim the fact-checker couldn't source

## Where it runs

- **Claude Code** (local or cloud): the full mode, with hooks and parallel
  reviewer agents. Deliverables are files in the project folder.
- **Agents that work with files for a long time and can start subagents**
  (Claude Cowork, Codex and similar): the full method without the hooks.
- **A plain chat** (claude.ai, ChatGPT): the plan phase works fully, and it's
  the most valuable part. Do the alignment, write the contract, then build
  slice by slice in the same conversation with the board review after each.
  It won't run for hours unattended, but the owner only needs to say
  "continue" instead of answering questions.

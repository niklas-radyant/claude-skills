# Planning with a living plan and clickable mockups

Load this in plan step 3, for any work package with a user interface.

The best planning sessions this skill came from had one thing in common. The
owner could **click through every state of the thing before it existed**, in
the product's real look, with real content. Decisions made on a clickable
mockup survived the build; decisions made on prose about a layout didn't.

## 1. One living plan page

Publish one HTML page (a claude.ai artifact, or a local HTML file the owner
opens) and republish it to the same place with a version label as it grows:
1. the user's flow, in the order they experience it
2. numbered decisions, each with your recommendation
3. who else must agree, with a ready-to-paste message for them
4. slices
5. technical notes, last and short

Every answer the owner gives goes into the Decisions section in the same
turn. The page is also what they share with their team.

## 2. Research before drawing (only for patterns the product doesn't have)

Look at how great products solve the same problem. Distill what you find into
4–6 principles plus "what not to copy". When the owner has to choose between
patterns, show **real product screenshots** (capture their public help pages
headlessly with `bin/shoot.mjs`) rather than your own drawings. A real
reference usually settles the choice in one pick.

## 3. Mockups as states, not screens

Build one single-file HTML mockup per surface and attach it to the plan page.

- **The real look.** Copy the header, navigation, components and tokens from
  the current build. Never a redrawn shell: the owner would end up judging a
  look you won't ship. Light and dark.
- **Real content.** Real example records and real data shapes. Never lorem
  ipsum.
- **Every moment.** Pills clearly labelled "mockup control" switch between
  states:
  - the user's turn
  - the system working
  - waiting on someone else
  - error, or reopened
  - done
  - empty
  - lots of data
- **Key interactions work**: picking, saving, the confirm moment.
- **Nothing slips in.** Every idea the owner hasn't agreed to is a visible
  toggle, not a default. Never hide a decision in button copy; lift it into
  a question.

Before showing it:
1. Screenshot every moment, light and dark.
2. Rate it out of 10 against the profile's taste section.
3. Fix what you can.
4. Tell the owner the score and what's left.

Iterate until they call the structure strong.

**Know the limit.** A mockup settles structure. It can't settle fit with
the real design system or real-data density. So the run's first slice builds
the real thing, and the critic compares it against both the mockup and the
reference screens.

## 4. Record it in the contract

In the contract's Look and feel section, put:
- the plan page and its version
- the mockup files and which moments they cover
- what the mockup settled
- the open toggles and how each was decided

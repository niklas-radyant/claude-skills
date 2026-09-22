# Working in this repo

Notes to myself. This repo is a personal collection, not a community
project — no PRs, so there's nothing here about reviewing other people's.

## Layout

```
.claude-plugin/marketplace.json   # lists every plugin; users add this repo as a marketplace
plugins/<theme>/
├── .claude-plugin/plugin.json    # name must equal the directory name
└── skills/<skill-name>/
    ├── SKILL.md                  # always read when the skill fires
    └── reference/                # loaded only when SKILL.md sends the model there
scripts/validate.py               # run before pushing; CI runs it on every PR
templates/SKILL.md                # starting point for a new skill
```

## Adding a skill to an existing plugin

1. `mkdir -p plugins/<plugin>/skills/<skill-name>`
2. Copy `templates/SKILL.md` into it and write the skill. The directory name
   and the frontmatter `name` must match — Claude Code addresses the skill by
   directory.
3. Put anything long (per-language checklists, worked examples, recipes) in
   `skills/<skill-name>/reference/*.md` and link it from the body by relative
   path. Those files load only when the body sends the model to them, which
   keeps the always-read part small. `claude plugin details <plugin>` shows
   the split: always-on tokens vs. on-invoke.
4. **Bump `version` in both** `plugins/<plugin>/.claude-plugin/plugin.json`
   and the plugin's entry in `.claude-plugin/marketplace.json`. This is the
   step that gets forgotten — the validator fails on drift, which is why it
   exists.
5. Add a row to the catalog table in `README.md`, and a section below it.
6. Validate:

```bash
python3 scripts/validate.py && claude plugin validate .
```

## Adding a new plugin

Group by theme, not one plugin per skill: skills surface as
`<plugin>:<skill>`, so a plugin per skill gives you `pr-preflight:pr-preflight`.
A theme also means anyone who installed it picks up later skills in that area
without doing anything.

Create `plugins/<theme>/` with the layout above, then register it in
`.claude-plugin/marketplace.json` under `plugins` with
`"source": "./plugins/<theme>"`. An unregistered plugin directory is not
installable, and the validator treats that as an error rather than letting it
ship silently.

## The bar for adding one

- **It has been run repeatedly on real work.** Not "this seems like a good
  idea" — something that survived actual use and got fixed where it broke.
- **It works in a repo it wasn't written for.** This is the one that
  disqualifies most drafts. A skill that hard-codes `npm run lint` works in
  one repo; one that reads the repo's CI config works everywhere. If it
  can't discover what it needs, it isn't ready to publish.
- **It states its own failure modes.** What it doesn't do, and where it can
  be wrong, belongs in the skill. A skill that oversells itself gets trusted
  in situations it can't handle.
- **No house rules.** Anything true only of one employer's codebase gets
  stripped, or turned into a documented option that self-detects at runtime.

## Testing a skill before publishing it

Reading it is not testing it. Both defects in v0.1.1 and v0.1.2 were found by
running `pr-preflight` against a repo it wasn't written for, and neither was
visible on the page:

1. Install it for real — `claude plugin marketplace add <path-or-repo>` then
   `claude plugin install <plugin>@niklas-skills`.
2. Pick a repo whose shape is *unlike* the one the skill came from. Different
   package manager, no CI, unusual script names. That is where assumptions
   surface.
3. Plant known defects that the type-checker won't catch, so you're testing
   the skill's judgment rather than `tsc`.
4. Check that it fires on a natural sentence, not just on `/<skill-name>`.
   The description is the whole trigger surface; a skill that installs but
   never activates looks fine in the repo and is worthless in practice.

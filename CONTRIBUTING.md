# Contributing

## Adding a skill to an existing plugin

1. `mkdir -p plugins/<plugin>/skills/<skill-name>`
2. Copy `templates/SKILL.md` into it and write the skill. The directory name
   and the frontmatter `name` must match — Claude Code addresses the skill by
   directory.
3. Put anything long (per-language checklists, worked examples, recipes) in
   `skills/<skill-name>/reference/*.md` and link it from the body by relative
   path. Those files load only when the body sends the model to them, which
   keeps the always-read part small.
4. Bump the `version` in **both** `plugins/<plugin>/.claude-plugin/plugin.json`
   and the plugin's entry in `.claude-plugin/marketplace.json`. The validator
   fails on drift.
5. Add it to the catalog table in `README.md`.
6. `python3 scripts/validate.py`

## Adding a new plugin

Group by theme, not one plugin per skill: skills surface as
`<plugin>:<skill>`, so a plugin per skill gives you `pr-preflight:pr-preflight`.
A theme also means someone who installs it gets your later skills in that
area for free.

```
plugins/<theme>/
├── .claude-plugin/
│   └── plugin.json          # name must equal the directory name
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        └── reference/       # optional, loaded on demand
```

Then register it in `.claude-plugin/marketplace.json` under `plugins`, with
`"source": "./plugins/<theme>"`. An unregistered plugin directory is not
installable, and the validator treats that as an error rather than letting it
ship silently.

## The bar

I keep this collection small on purpose. A skill gets in if:

- **It has been run repeatedly on real work.** Not "this seems like a good
  idea" — something that survived actual use and got fixed where it broke.
- **It works in a repo it wasn't written for.** This is the one that
  disqualifies most drafts. A skill that hard-codes `npm run lint` works in
  one repo; one that reads the repo's CI config works everywhere. If it
  can't discover what it needs, it isn't shareable yet.
- **It states its own failure modes.** What it doesn't do, and where it can
  be wrong, belongs in the skill. A skill that oversells itself gets trusted
  in situations it can't handle.
- **It has no house rules in it.** Anything true only of one employer's
  codebase gets stripped, or turned into a documented option that
  self-detects.

## Before you open a PR

```bash
python3 scripts/validate.py
```

CI runs the same check. It validates every manifest, that plugin and skill
names match their directories, that versions agree across both manifests,
that every `reference/` link resolves, and that no reference file is
unreachable from its skill body.

Issues and PRs are welcome — especially reports of a skill misfiring in a
repo shaped differently from mine, which is the failure mode I can't test
for myself.

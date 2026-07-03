# GovKit Plugins

Governed AI delivery skills for [Claude](https://claude.com), from [Accelerated Innovation](https://acceleratedinnovation.com).

This repository is a **Claude Code plugin marketplace**. It ships the **`govkit`** plugin, which bundles GovKit's Agent Skills for refining feature specs before AI-assisted coding begins.

## Install

In Claude Code (or via Settings → Customize plugins in the Claude web app):

```
/plugin marketplace add Accelerated-Innovation/govkit-plugins
/plugin install govkit@accelerated-innovation
```

Update to the latest version later with:

```
/plugin marketplace update accelerated-innovation
```

## What's inside

| Skill | What it does |
|---|---|
| `govkit-feature-refine` | Review Draft 0 Gherkin, NFRs, and evaluation criteria with Product, QA, and Engineering before coding starts. Produces a readiness signal and a Development Token recommendation. |

_More GovKit skills are added as separate folders under `plugins/govkit/skills/`._

## Repository layout

```
govkit-plugins/
├── .claude-plugin/
│   └── marketplace.json          # marketplace catalog (lists the govkit plugin)
├── plugins/
│   └── govkit/
│       ├── .claude-plugin/
│       │   └── plugin.json        # plugin manifest
│       └── skills/
│           └── govkit-feature-refine/
│               ├── SKILL.md
│               ├── references/     # rubrics the skill reads at runtime
│               └── evals/          # skill evaluations
├── templates/
│   └── skill-template/SKILL.md     # starting point for new skills (does not auto-load)
├── LICENSE
└── README.md
```

## Adding another skill

1. Create `plugins/govkit/skills/<your-skill-name>/SKILL.md` (copy `templates/skill-template/SKILL.md` as a starting point).
2. Add any `references/` or `assets/` the skill needs alongside it.
3. Bump `version` in `plugins/govkit/.claude-plugin/plugin.json`.
4. Run `claude plugin validate .`, commit, and push. Users pick it up with `/plugin marketplace update`.

Skills in a plugin's `skills/` directory load automatically — you don't need to list them anywhere.

## License

MIT. See [LICENSE](./LICENSE).

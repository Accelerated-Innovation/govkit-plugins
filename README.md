# GovKit Plugins

Governed AI delivery skills for [Claude](https://claude.com), from [Accelerated Innovation](https://acceleratedinnovation.com).

This repository is a **Claude Code plugin marketplace**. It ships two plugins: **`govkit`**, GovKit's Agent Skills for governed, AI-assisted delivery, and **`aipos-p2`**, the AIPOS Pillar 2 (Rapid Validation) skills for testing assumptions before engineering capacity is committed.

## Install

In Claude Code (or via Settings → Customize plugins in the Claude web app):

```
/plugin marketplace add Accelerated-Innovation/govkit-plugins
/plugin install govkit@aipos
/plugin install aipos-p2@aipos
```

Update to the latest version later with:

```
/plugin marketplace update aipos
```

## What's inside

### `govkit` — governed AI delivery

| Skill | What it does |
|---|---|
| `govkit-feature-refine` | Review Draft 0 Gherkin, NFRs, and evaluation criteria with Product, QA, and Engineering before coding starts. Produces a Development Token recommendation; batch mode scores a corpus non-interactively. |
| `govkit-feature-readiness` | Validate an approved feature package in the repo against the 12-dimension readiness gate. Issues the Development Token. |
| `govkit-feature-map` | Turn a whole epic or spec corpus into one scored, self-contained HTML feature map with a readiness badge per feature. |
| `govkit-metrics-emit` | Emit Tier 1 metric events (NDJSON) from a GovKit-governed repo's exhaust — spec completeness, gate readiness, delivery metrics. |
| `govkit-synthetic-data` | Generate Faker-based synthetic test data for Gherkin scenarios. |

### `aipos-p2` — Rapid Validation (AIPOS Pillar 2)

| Skill | What it does |
|---|---|
| `val-rapid-validation` | Build the validation artifacts that feed a go / no-go / revise Validation Decision: interview guides, problem sizing, visual prototype briefs, demand tests, feasibility spikes, GenAI eval stubs, and the viability brief. |

_More skills are added as separate folders under each plugin's `skills/` directory._

## Repository layout

```
govkit-plugins/
├── .claude-plugin/
│   └── marketplace.json          # marketplace catalog (lists both plugins)
├── plugins/
│   ├── govkit/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json        # plugin manifest
│   │   └── skills/
│   │       ├── govkit-feature-refine/
│   │       │   ├── SKILL.md
│   │       │   ├── references/     # rubrics the skill reads at runtime
│   │       │   └── evals/          # skill evaluations
│   │       └── ...                 # one folder per skill
│   └── aipos-p2/
│       ├── .claude-plugin/
│       │   └── plugin.json        # plugin manifest
│       └── skills/
│           └── val-rapid-validation/
│               ├── SKILL.md
│               └── references/     # per-artifact templates and quality bars
├── templates/
│   └── skill-template/SKILL.md     # starting point for new skills (does not auto-load)
├── LICENSE
└── README.md
```

## Adding another skill

1. Create `plugins/<plugin>/skills/<your-skill-name>/SKILL.md` (copy `templates/skill-template/SKILL.md` as a starting point).
2. Add any `references/` or `assets/` the skill needs alongside it.
3. Bump `version` in `plugins/<plugin>/.claude-plugin/plugin.json`.
4. Run `claude plugin validate .`, commit, and push. Users pick it up with `/plugin marketplace update`.

Skills in a plugin's `skills/` directory load automatically — you don't need to list them anywhere.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add a skill, validate locally, and open a PR. Every pull request runs `claude plugin validate` in CI.

## License

MIT. See [LICENSE](./LICENSE).

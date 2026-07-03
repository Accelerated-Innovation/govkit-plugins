# Contributing to GovKit Plugins

Thanks for helping improve GovKit. This repo is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces); most contributions are new or improved **skills** inside the `govkit` plugin.

## Repository layout

```
.claude-plugin/marketplace.json   # marketplace catalog
plugins/govkit/
  .claude-plugin/plugin.json      # plugin manifest (bump version on release)
  skills/<skill-name>/SKILL.md    # one folder per skill; loads automatically
templates/skill-template/         # copy this to start a new skill
```

## Adding or changing a skill

1. Create `plugins/govkit/skills/<your-skill-name>/SKILL.md`, copying [`templates/skill-template/SKILL.md`](templates/skill-template/SKILL.md) as a starting point.
2. Keep the frontmatter `description` specific — it is the only text Claude sees when deciding whether to load the skill, so include the trigger words a user would actually type.
3. Put any supporting material in the skill folder: `references/` for rubrics/checklists the skill reads at runtime, `evals/` for evaluation cases and sample inputs.
4. Skills load automatically from a plugin's `skills/` directory — you don't need to register them anywhere.

## Before you open a PR

Validate the marketplace and plugin manifests locally:

```bash
claude plugin validate .
```

Then check:

- [ ] `claude plugin validate .` passes.
- [ ] JSON files (`marketplace.json`, `plugin.json`, any `evals.json`) are valid and consistent (names, descriptions, keywords).
- [ ] Bumped `version` in [`plugins/govkit/.claude-plugin/plugin.json`](plugins/govkit/.claude-plugin/plugin.json) if the change is user-visible. Users pick up updates with `/plugin marketplace update aipos`.
- [ ] Updated the [README](README.md) and any relevant `references/` if behavior changed.

## Continuous integration

Every pull request runs `claude plugin validate` via [`.github/workflows/validate.yml`](.github/workflows/validate.yml). PRs must pass before merge. The check is a static structural validation — it needs no API key.

## Commit and PR conventions

- Keep commits focused and messages descriptive.
- Describe the user-facing effect of the change in the PR body, not just the files touched.
- One skill or one coherent change per PR where practical.

## License

By contributing, you agree that your contributions are licensed under the [MIT License](LICENSE).

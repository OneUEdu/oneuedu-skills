# One U Education Skills

Agent skills for people using the [One U Education](https://www.oneuedu.com/) website: Australian study and migration help built on public course, school, occupation and visa data, personal migration planning and feedback, all through the official MCP server. Staff-facing skills are maintained separately in `OneUEdu/oneulink-skills`.

| Skill | What it does |
| --- | --- |
| [website-feedback](skills/website-feedback/SKILL.md) | Submit feedback, check the progress of your own reports and continue the public discussion |
| [australian-course-application](skills/australian-course-application/SKILL.md) | Save an application intent and pass it to a One U Education application specialist through a secure form and confirmation widget |
| [australian-immigration-planning](skills/australian-immigration-planning/SKILL.md) | Personal planning profile, calculations and explanation of the results |

## One-line install

The repository root contains a plugin manifest for each client, so you can install straight from GitHub. The plugin installs the skills together with the official MCP connection `https://mcp.oneuedu.com/mcp`. Public lookups need no sign-in; when you create a planning profile or view your own feedback, your client asks you to sign in to One U Education.

| Client | Install command | What you get |
| --- | --- | --- |
| Claude Code | `claude plugin install one-u-education --marketplace OneUEdu/oneuedu-skills` | Planning and feedback skills + MCP |
| Codex | `codex plugin marketplace add OneUEdu/oneuedu-skills`, then `codex plugin add one-u-education@oneuedu` | Planning and feedback skills + MCP |
| GitHub Copilot CLI | `copilot plugin marketplace add OneUEdu/oneuedu-skills`, then `copilot plugin install one-u-education@oneuedu` | Planning and feedback skills + MCP |
| Grok Build | `grok plugin install OneUEdu/oneuedu-skills --trust` | Planning and feedback skills + MCP |
| Other clients that support Agent Skills (Cursor, Gemini CLI, OpenCode and others) | `npx skills add OneUEdu/oneuedu-skills -s australian-immigration-planning website-feedback` | Skills only; add the MCP server by following your client's instructions |

Inside a Claude Code session you can also type `/plugin install one-u-education --marketplace OneUEdu/oneuedu-skills`.

- The application skill `australian-course-application` needs ChatGPT's secure form and confirmation card, so direct installs leave it out. The ChatGPT version is packaged in oneuedu-plugin and goes through OpenAI review.
- The manifests have no version number; clients update by Git commit. Once new commits are pushed, users get them with `claude plugin update one-u-education@oneuedu`, `codex plugin marketplace upgrade`, `copilot plugin update one-u-education@oneuedu` or `grok plugin update one-u-education`.
- `.grok-plugin/` follows the format of the xAI plugin marketplace (xai-org/plugin-marketplace). Grok Build reads `.grok-plugin/plugin.json` first, then `.claude-plugin/`, and `marketplace.json` lets the repository be installed directly with `grok plugin install OneUEdu/oneuedu-skills`. `--trust` skips the trust prompt during install, and the plugin is added to `[plugins].enabled` straight away, so there is no need to run `grok plugin enable`. Tested on 12 Nov 2026 with Grok 1.0.77 in an isolated HOME: `grok inspect` shows only the planning and feedback skills plus the MCP server `one-u-education` (http, `https://mcp.oneuedu.com/mcp`). Without `.grok-plugin/`, Grok falls back to `.claude-plugin/` and installs the application skill as well.
- `.cursor-plugin/` is written to Cursor's documentation, but Cursor only installs from its own marketplace, so the plugin has to be submitted at cursor.com/marketplace/publish first. It has not been tested. VS Code's "Chat: Install Plugin From Source" uses the Copilot format and has not been tested either.
- Tested on 3 Nov 2026 in isolated config directories: Claude Code 2.1.316, Codex CLI 0.166.0 and Copilot CLI 1.0.105 each load only the planning and feedback skills and connect to the MCP server; skills CLI 1.7.6 installs only those two skills when given `-s`.

All manifests are generated in one place by `scripts/platforms.py`; don't edit them by hand. To change the name, description, skill list or MCP URL, edit that script and run `python3 scripts/platforms.py`. `scripts/check.py` checks that the manifests are up to date. Whether a new skill is included in the direct-install plugin is decided in the script's `SKILLS` list.

## Maintenance and distribution

This repository is the single source of truth for the skill instructions. The plugin packaging lives in [oneuedu-plugin](https://github.com/OneUEdu/oneuedu-plugin), whose `plugins/one-u-education/skills` points to an exact commit of this whole repository as a Git submodule, so there is no second copy of the skill text to sync or maintain. In this repository each skill's entry point is still `skills/<name>/`; the build places them into the existing package layout.

After making a change, run the local checks below, then commit and push to this repository. Next, in the plugin repository, check out that pushed submodule commit, run `git add plugins/one-u-education/skills`, verify the build and commit the updated pointer in the parent repository. Committing a new skill here does not update the plugin automatically. To get the plugin source, clone it recursively or run `git submodule update --init --recursive`. The full commands are in the plugin repository's maintenance guide.

If you don't use the commands above, you can copy a complete `skills/<name>/` folder into your client's skills directory, or build standalone skill packages from the plugin repository. Keep `references/` and `agents/` with it; don't copy SKILL.md on its own. Installing the skills alone does not connect the MCP server, sign you in or give you access to the tools.

All skills connect to `https://mcp.oneuedu.com/mcp`. Viewing your own feedback requires a valid account connection; anonymous feedback stays one-way. The feedback discussion feature needs the matching backend (v2), CRM, website and MCP changes deployed first, so having the skill source here does not mean every tool is live in production.

The application flow depends on a secure form and confirmation widget, so an installable SKILL.md does not mean every client can complete it. Test any new client properly before adding it. The manifest and packaging for the ChatGPT review package are maintained in the plugin repository.

## Local checks

Python 3.12 with the standard library only:

```sh
python3 scripts/check.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

These check skill entry points, MCP dependencies, referenced files and distribution boundaries. They make no remote requests, install no skills and send no email. Changes to skill content still need real-world acceptance testing.

## Migration

The initial 11 files were copied unchanged from the candidate package committed in the CRM; the commits and hashes are recorded in [migration-source.json](docs/migration-source.json). No existing business rules were rewritten. The original application skill came from a snapshot generated by the website. From this migration onwards, **the plugin-side instructions are maintained here**: any output from the old generator must be compared and reviewed by hand and must never overwrite this repository. The WhatsApp runtime and the server-side rules still belong to their original projects.

### Planning skill 1.9.2 catch-up sync (3 Nov 2026)

Brought in the pre-migration planning text and service reference updates from CRM commit `b07802e4`. Responses now centre on the user's current decision and next steps; comparing occupations, saving a goal and running a calculation are kept distinct; and clarifying high-impact facts and explaining future costs are now covered. The other skills and references are unchanged, and future planning changes are made only in this repository. The plugin syncs from an exact commit of this repository; passing the source checks here does not mean the service has been deployed or that acceptance testing with real models is complete.

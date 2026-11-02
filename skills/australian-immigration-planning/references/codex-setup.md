# Standalone Codex installation and the official MCP

This skill does not require the OneU plugin. Installing the files, connecting the official MCP and authorizing an account are three separate steps; the dependency declared in `agents/openai.yaml` does not prove that a connection or authorization exists. Read this note only when installing or troubleshooting a connection.

## Install the skill files

Extract the release ZIP into a new, empty temporary directory. Copy the complete `australian-immigration-planning/` directory into `~/.agents/skills/`, keeping `agents/` and `references/`. It can instead go in the target project's `.agents/skills/` for that project only. If a directory with the same name exists, check its source and version first, back it up and replace it completely; do not merge reference files from different versions. Do not install a skill with the same name in more than one scanned directory.

Codex detects skill changes; restart it if the skill does not appear. Select it explicitly with `$australian-immigration-planning`, or ask a migration-planning question to check natural triggering. If an installed plugin also exposes a skill with the same name, explicitly select the local version when verifying; do not assume the two are merged.

## Configure the official connection

Check the existing connections first and reuse one whose URL is `https://mcp.oneuedu.com/mcp`; its name may differ. Add a connection only when none exists and the user asks for it. Do not overwrite another service's configuration that has the same name.

```sh
codex mcp list
codex mcp add one-u-education --url https://mcp.oneuedu.com/mcp
```

The Streamable HTTP URL can also be configured in Codex's MCP settings. For anonymous public-information questions only, add the following table to the user configuration `~/.codex/config.toml`; reuse an existing entry rather than appending a duplicate:

```toml
[mcp_servers.one-u-education]
url = "https://mcp.oneuedu.com/mcp"
```

If adding the server through the CLI starts an OAuth prompt, complete authorization only when the user needs account features. Anonymous lookups need no account permission. After reopening Codex, check actual tool discovery and errors; a file being present, a connection being listed and a tool being callable are different verification results.

## Authorize when an account dossier or calculation is needed

Sign in to the One U Education account through Codex's OAuth sign-in screen. The scopes below are an example for the full planning workflow; replace the connection name if it differs:

```sh
codex mcp login one-u-education --scopes mcp:read,planning:read,planning:write,planning:calculate
```

Reading a dossier needs only the base `mcp:read` and `planning:read`; saving and calculating each add their own scope. To keep the connection, `offline_access` can also be granted through the website's authorization flow. Follow the current authorization challenge returned by the tool; an earlier grant or a token refresh does not add planning scopes automatically. A scope that permits an action does not mean the user has asked for that action.

Do not ask the user to paste tokens, cookies, passwords or service API keys into the chat, and do not use the company's fixed-key `/toolkit/mcp` entry to access a personal dossier. If the OAuth client is rejected, keep the exact error and resolve client registration or trust issues through website support; do not invent a client ID or bypass authentication.

## Find where it fails

| Status | Next step |
| --- | --- |
| Skill not discovered | Check the directory location, that all files are present and that the skill is not disabled; restart Codex if needed. |
| No official MCP connection | Configure the connection if the user asks; questions supported by accessible official sources can still be answered. |
| Connected, but no planning tools | Check the server's current tool list and whether the service is enabled; course tools being available does not mean planning is available. |
| Not authenticated or authorization expired | Sign in through the host; do not describe a failed read as having no dossier. |
| insufficient_scope | Reauthorize the scope the current action needs; do not keep retrying the same failed call. |
| Network, rate-limit or service error | Follow the actual error and retry guidance and keep any accepted task ID; do not create a duplicate task by changing request_id. |

After configuring the connection, test a public question first. Verify account reads, saves and calculations with an authorized account and task; do not secretly create real dossiers for testing. Building a package or passing local tests is not the same as a production OAuth journey passing.

Checked on 2026-10-31. Codex installation and configuration follow the [official skills documentation](https://learn.chatgpt.com/docs/build-skills) and the [official MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli); CLI flags were also checked against local `codex mcp add --help` and `codex mcp login --help`. Website account permissions follow the server's current tool contract.

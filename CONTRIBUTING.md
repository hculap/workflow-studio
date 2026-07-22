# Contributing

This repository is the **Claude Code plugin marketplace** for Workflow Studio: manifests, a skill, and
a command. The plugin's MCP server runs `uvx workflow-studio mcp`, pulling the
[`workflow-studio`](https://pypi.org/project/workflow-studio/) package from PyPI. The application source
(the Python package + the React dashboard) lives in the main Workflow Studio project.

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace manifest
workflow-studio/
  .claude-plugin/plugin.json        # plugin manifest (declares the MCP server → uvx workflow-studio mcp)
  skills/workflow-studio/SKILL.md   # teaches the agent when/how to use the tools
  commands/dashboard.md             # /workflow-studio:dashboard
```

## Releasing a new version

In the package source project:

```
./build-wheel.sh                                   # builds web/dist, then wheel + sdist into dist/
uvx twine check dist/*                             # validate metadata/README render for PyPI
UV_PUBLISH_TOKEN=<pypi-token> uv publish           # publish the new version to PyPI
```

Then bump `version` in both manifests here and add a `CHANGELOG.md` entry. The plugin's `mcpServers`
command is unpinned (`uvx workflow-studio mcp`), so users pick up the new version automatically.

## Testing locally

```
claude plugin validate ./workflow-studio          # manifest check
# install against a throwaway config so your real ~/.claude is untouched:
CLAUDE_CONFIG_DIR=$(mktemp -d) claude plugin marketplace add "$PWD"
CLAUDE_CONFIG_DIR=<that dir> claude plugin install workflow-studio@workflow-studio
CLAUDE_CONFIG_DIR=<that dir> claude mcp list       # expect: ✔ Connected
```

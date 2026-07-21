# Contributing

This repository is the **Claude Code plugin marketplace** for Workflow Studio: manifests, a skill, a
command, and a bundled wheel. The application source (the `workflow-studio` Python package + the React
dashboard) lives in the main Workflow Studio project.

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace manifest
workflow-studio/
  .claude-plugin/plugin.json        # plugin manifest (declares the MCP server)
  skills/workflow-studio/SKILL.md   # teaches the agent when/how to use the tools
  commands/dashboard.md             # /workflow-studio:dashboard
  vendor/*.whl                      # bundled package wheel (how it installs pre-PyPI)
```

## Updating the bundled wheel

When the package changes, rebuild and re-vendor:

```
# in the package source dir:
./build-wheel.sh                    # builds web/dist, then the wheel into dist/
cp dist/workflow_studio-<version>-py3-none-any.whl \
   plugin-marketplace/workflow-studio/vendor/
```

Then bump the pinned filename in `workflow-studio/.claude-plugin/plugin.json` (`mcpServers.args`) and
the `version` in both manifests, and add a `CHANGELOG.md` entry.

## Testing locally

```
claude plugin validate ./workflow-studio          # manifest check
# install against a throwaway config so your real ~/.claude is untouched:
CLAUDE_CONFIG_DIR=$(mktemp -d) claude plugin marketplace add "$PWD"
CLAUDE_CONFIG_DIR=<that dir> claude plugin install workflow-studio@workflow-studio
CLAUDE_CONFIG_DIR=<that dir> claude mcp list       # expect: ✔ Connected
```

## After publishing to PyPI

Switch `mcpServers` to the one-liner `{"command":"uvx","args":["workflow-studio","mcp"]}`, delete the
vendored wheel, bump the version, and open a release.

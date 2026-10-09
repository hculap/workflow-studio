# Contributing

This repository is the **Claude Code plugin marketplace** for Workflow Studio: manifests, a skill, and
a command. The plugin's MCP server runs `uvx workflow-studio==0.2.0 mcp`, pulling the
[`workflow-studio`](https://pypi.org/project/workflow-studio/) package from PyPI. The application source
(the Python package + the React dashboard) lives in the main Workflow Studio project.

## Repo layout

```
.claude-plugin/marketplace.json     # marketplace manifest
workflow-studio/
  .claude-plugin/plugin.json        # plugin manifest (declares the MCP server → uvx workflow-studio==<version> mcp)
  README.md, LICENSE                # shipped with the plugin: the folder is all an installer gets
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

Then, here: raise `version` in `workflow-studio/.claude-plugin/plugin.json`, move the pinned package
version (`workflow-studio==<version>`) in `plugin.json`'s `mcpServers` args, `commands/dashboard.md`,
`skills/workflow-studio/SKILL.md` and the plugin `README.md`, and add a `CHANGELOG.md` entry. The pin is
deliberate: Anthropic's plugin directory blocks an unpinned `uvx` launcher, and users get a new package
version through a plugin update. Raise the plugin `version` on every change to the plugin folder.

## Testing locally

```
claude plugin validate ./workflow-studio          # manifest check
# install against a throwaway config so your real ~/.claude is untouched:
CLAUDE_CONFIG_DIR=$(mktemp -d) claude plugin marketplace add "$PWD"
CLAUDE_CONFIG_DIR=<that dir> claude plugin install workflow-studio@workflow-studio
CLAUDE_CONFIG_DIR=<that dir> claude mcp list       # expect: ✔ Connected
```

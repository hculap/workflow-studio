# Changelog

All notable changes to the Workflow Studio Claude Code plugin are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.1] — Unreleased

Plugin-only release; the `workflow-studio` package on PyPI stays at 0.2.0.

### Changed
- **Pinned package version.** The MCP server now starts with `uvx workflow-studio==0.2.0 mcp`, and
  `/workflow-studio:dashboard` with `uvx workflow-studio==0.2.0`, instead of whatever version is newest
  on PyPI. A new package version now reaches users through a plugin update.

### Added
- `workflow-studio/README.md`: what the plugin runs, what it reads and writes on your machine, and the
  one network request it causes (the package download from PyPI).
- `workflow-studio/LICENSE` and `"license": "MIT"`, `"repository"` in `plugin.json`, so the plugin folder
  carries its own license.

## [0.2.0] — 2026-07-23

### Added
- **Reverse-proxy subpath support.** Serve the dashboard under a prefix (e.g.
  `https://example.com/workflow-studio/`) via `WORKFLOW_STUDIO_BASE_PATH` / `--base-path`. The server
  injects a `<base href>` into `index.html` and the client prefixes every asset, API, and router path;
  it also strips the prefix off incoming requests, so both stripping and non-stripping proxies work.
  `get_context` now reports `basePath` in its doctor view. Fully backward-compatible — the default
  (unset) is the unchanged root behaviour on `127.0.0.1`.

## [0.1.0] — 2026-07-21

Initial release.

### Added
- **MCP server** (`workflow-studio mcp`) — a dependency-free stdlib JSON-RPC 2.0 stdio server
  exposing 9 tools to the Claude Code agent: `get_context`, `list_projects`, `list_runs`, `get_run`,
  `list_workflows`, `get_workflow`, `get_run_design` (read) and `save_workflow`, `promote_run` (write).
- **Observability dashboard** — reads Claude Code's on-disk Workflow run artifacts and renders each run
  as a phase/agent/token timeline; live runs included.
- **No-code builder** — a canvas that compiles blocks (agent, fanout, loop, subwf, gate, filter,
  switch, pipeline, rank, input, param, start) to a runnable Workflow script with a lossless
  `@wf-builder` sidecar.
- **Published to PyPI** as [`workflow-studio`](https://pypi.org/project/workflow-studio/); the plugin
  launches the MCP server with `uvx workflow-studio mcp`. Includes a `/workflow-studio:dashboard`
  command and a skill that teaches the agent when/how to use the tools.
- Honesty flags on every tool result (`taskMatched`/`status` for observed data; `source`/`hasSidecar`/
  decoded `contract` for declared designs).

[0.2.0]: https://github.com/hculap/workflow-studio/releases/tag/v0.2.0
[0.1.0]: https://github.com/hculap/workflow-studio/releases/tag/v0.1.0

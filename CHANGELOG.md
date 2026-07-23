# Changelog

All notable changes to the Workflow Studio Claude Code plugin are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

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

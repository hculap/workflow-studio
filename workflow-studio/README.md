# Workflow Studio

Observe and author Claude Code multi-agent `Workflow` runs. Workflow Studio is a local dashboard that shows what a run actually did (phases, agents, tokens, timing, which branch was taken) and a no-code block builder that compiles to a runnable Workflow script. This plugin gives the Claude Code agent the same two halves over MCP, so the agent can inspect your runs and draft workflows into your builder.

Website: [szymonpaluch.com/workflow-studio](https://szymonpaluch.com/workflow-studio/) · Source and full documentation: [github.com/hculap/workflow-studio](https://github.com/hculap/workflow-studio) · License: MIT

## What the plugin contains

- **An MCP server** named `workflow-studio`, started over stdio with `uvx workflow-studio==0.2.0 mcp`.
- **A command**, `/workflow-studio:dashboard`, which starts the dashboard with `uvx workflow-studio==0.2.0` and gives you its URL.
- **A skill** that tells the agent when to use the tools and how to read their results.

## What it runs and what it connects to

- **The `workflow-studio` package from PyPI, version 0.2.0, pinned.** `uvx` downloads it on first use and caches it. The package is pure Python standard library with no runtime dependencies and needs Python 3.9 or newer. You need [`uv`](https://docs.astral.sh/uv/) (which provides `uvx`) on your `PATH`. These downloads are the only network requests the plugin causes: the package from PyPI and, if your system has no Python 3.9 or newer, a managed CPython that `uv` fetches by default.
- **The MCP server makes no network calls.** It talks to Claude Code over stdin and stdout only.
- **The dashboard is a local web server bound to `127.0.0.1`**, on port 8787 or the next free port (or `$PORT`). It opens your default browser at that address unless you pass `--no-open` or set `WORKFLOW_STUDIO_NO_OPEN`. It listens on another address only if you pass `--host` yourself. The web app is bundled in the package and loads nothing from the internet. There is no telemetry.

## What it reads and writes on your machine

Reads:

- Claude Code's local project data in `~/.claude/projects`: Workflow run folders, their agent transcripts, launch scripts and session files. This is where the run graphs come from.
- The Workflow runtime's task output in your temp directory (`claude-<uid>` under `$TMPDIR` or `/tmp`), for token and timing figures. `WORKFLOW_STUDIO_TASKS_ROOT` overrides the location.

Writes:

- Builder templates and a small run-to-template index in its data directory: `~/.local/share/workflow-studio` by default, `$XDG_DATA_HOME/workflow-studio` if that is set, or `$WORKFLOW_STUDIO_DATA`. The `save_workflow` and `promote_run` tools write here. `save_workflow` overwrites an existing name only when called with `overwrite`, and `promote_run` never overwrites.
- Two files inside a run's own folder in `~/.claude/projects`: `.task-output.json`, a copy of the run's task output kept so its figures survive when the temp files are cleaned up, and `.launch-script.js`, the script the run was launched from.

It never starts a Workflow run. It hands the agent a design's script, and the agent runs it with its own `Workflow` tool.

## MCP tools

| Tool | Kind | What it does |
|---|---|---|
| `get_context` | read | The project and session in scope, plus where the data directory is |
| `list_projects` | read | Projects on this machine that have Workflow history |
| `list_runs` | read | Runs in the current project, live first |
| `get_run` | read | One run's graph: phases, agents, logs, tokens, timing |
| `list_workflows` | read | Reusable workflows: builder designs and workflows seen in runs |
| `get_workflow` | read | One workflow's script and its declared contract |
| `get_run_design` | read | The design a specific run executed |
| `save_workflow` | write | Draft a Workflow script into your builder |
| `promote_run` | write | Turn an existing run into a named, reusable workflow |

Observed data carries `taskMatched` and `status` flags, so a heuristic or still-running figure is never shown as a measurement. Declared designs carry `source` and `hasSidecar`, so you can tell an exact record from a best-effort recovery.

## Install and use

On Claude Code 2.1.275 or later:

```
/plugin install workflow-studio --marketplace hculap/workflow-studio
```

On older versions, add the marketplace first:

```
/plugin marketplace add hculap/workflow-studio
/plugin install workflow-studio@workflow-studio
```

After installing, start a new Claude Code session. `/mcp` lists `workflow-studio` with 9 tools, and `/workflow-studio:dashboard` opens the dashboard. To check what the agent sees, ask it to call `get_context`.

For the agent's drafts to appear in your builder, the dashboard and the MCP server must use the same data directory. They do by default when both run through `uvx`.

## License

MIT. See [LICENSE](LICENSE).

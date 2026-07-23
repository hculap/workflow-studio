# Install Workflow Studio — guide for your coding agent

**You are a coding agent and your human asked you to install Workflow Studio. Follow this file top to
bottom, run the commands yourself, then report back. Most steps are plain shell commands you can run
directly — no slash commands required.**

Workflow Studio is a **local** no-code builder + observability dashboard for Claude Code's `Workflow`
tool (deterministic multi-agent orchestration). It gives *you*, the agent, two things over **MCP**: a
way to **observe** what a run actually did (phases, agents, tokens, timing, which branch it took) and a
way to **author** new workflows visually and hand them back to your human. Everything runs on the
human's machine — it binds `127.0.0.1`, reads local Claude Code data, makes no network calls.
Package: [`workflow-studio`](https://pypi.org/project/workflow-studio/) · Site: <https://szymonpaluch.com/workflow-studio/>

---

## Step 0 — Prerequisite: `uv` / `uvx`

Workflow Studio starts via `uvx`. Check for it:

```bash
command -v uvx
```

If that prints nothing, install `uv` (it ships `uvx`):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh      # macOS/Linux
# or:  brew install uv
```

Then confirm `command -v uvx` prints a path. If you are running inside a **GUI-launched** Claude Code
that can't see `uvx` even though it's installed, tell the human to relaunch Claude Code **from a
terminal** (GUI launches often don't inherit the shell `PATH`).

## Step 1 — Install the plugin (run these in your shell)

Non-interactive CLI, safe for you to run directly (needs Claude Code with the `claude plugin` CLI,
v2.1+):

```bash
claude plugin marketplace add hculap/workflow-studio
claude plugin install workflow-studio@workflow-studio
```

The first registers the marketplace (this public GitHub repo); the second installs the plugin, which
declares an MCP server launched with `uvx workflow-studio mcp` (pulled from PyPI — nothing to build).

> **Older Claude Code without the `claude plugin` CLI?** Ask the human to type these two slash commands
> instead (slash commands can't be run by an agent): `/plugin marketplace add hculap/workflow-studio`
> then `/plugin install workflow-studio@workflow-studio`.

## Step 2 — Verify (run these)

```bash
claude plugin list      # → workflow-studio@workflow-studio · Status: ✔ enabled
claude mcp list         # → plugin:workflow-studio:workflow-studio: uvx workflow-studio mcp - ✔ Connected
```

If `claude mcp list` shows `✘ Failed` for it, `uvx` is almost certainly not on the `PATH` Claude Code
sees — go back to Step 0 (relaunch from a terminal).

## Step 3 — Activate, then tell the human

A freshly installed plugin — its 9 MCP tools **and** the `/workflow-studio:dashboard` command — loads
on the **next** Claude Code session. Report to the human, verbatim:

> "Workflow Studio is installed and verified. **Restart Claude Code** (or start a new session) to
> activate it. Then open the dashboard with `/workflow-studio:dashboard`, or run `uvx workflow-studio`
> in a terminal (it opens at http://127.0.0.1:8787/)."

---

## What you can do once it's active

Nine MCP tools (all read the human's **local** run data; two write into their builder):

- **Observe** — `list_runs`, `get_run`, `list_projects`, `get_context`
- **Read declared designs** — `list_workflows`, `get_workflow`, `get_run_design`
- **Draft back to the human's builder** — `save_workflow`, `promote_run`

This server **cannot start a run**. It hands you a design's `script`; you execute it with your **own**
`Workflow` tool. Honesty is baked into every result — observed data carries `taskMatched`/`status`,
declared designs carry `source`/`hasSidecar`. Never present a heuristic value (`taskMatched=false`) or a
non-final elapsed span as if it were measured.

## Alternative — MCP only (no plugin)

If the human only wants the tools for you (not the `/workflow-studio:dashboard` command), skip Steps 1–3
and run just:

```bash
claude mcp add workflow-studio -s user -- uvx workflow-studio mcp
```

Then `claude mcp list` should show it `✔ Connected` (it activates on your next session).

## Uninstall

```bash
claude plugin uninstall workflow-studio@workflow-studio
claude plugin marketplace remove workflow-studio       # optional
# MCP-only install instead? →  claude mcp remove workflow-studio -s user
```

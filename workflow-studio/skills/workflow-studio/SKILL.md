---
name: workflow-studio
description: >-
  Observe and author Claude Code multi-agent Workflow runs. Use when the user wants to see what a
  Workflow run actually did (phases, fan-out, agents, tokens, which branch was taken), reuse or reason
  about a workflow the human designed in the no-code builder, draft a new workflow for the human to
  review, or open the visual Workflow Studio dashboard. Triggers: "workflow run", "what did the
  workflow do", "workflow studio", "reuse that workflow", "show me the run", "workflow builder".
allowed-tools: Bash(uvx workflow-studio*)
---

# Workflow Studio

Workflow Studio is a local companion for Claude Code's `Workflow` tool. It **observes** past/live
Workflow runs and lets a human **author** workflows in a no-code block builder. This plugin exposes it
to you over MCP so you and the human collaborate through one live surface instead of a script file
dropped on disk that you can't see.

## The two worlds (never conflate them)

- **OBSERVED** — what a run actually did. `list_runs`, `get_run`. This data carries honesty flags:
  - `run.taskMatched = false` → the metrics overlay was garbage-collected, so tokens/duration/model
    are **heuristic or unknown, not measured** — say so; don't report them as measurements.
  - `run.status` is `live | incomplete | done`. A `live`/`incomplete` elapsed span is a **lower
    bound**, not a completed duration.
- **DECLARED** — the design/intent. `get_workflow` (by name), `get_run_design` (by run id).
  - `source = 'snapshot'` → the exact script that run launched (trust as "what ran"). `'template'` →
    a mutable design that **may differ** from what ran. `null` → none recorded.
  - `hasSidecar = true` gives you a decoded `contract` (declared inputs + per-agent output schema +
    block/edge skeleton). `hasSidecar = false` → best-effort structure only, **not** a faithful design.

## What you can do

1. **Inspect a run** — `list_runs` then `get_run(run_id)` for the full graph. Respect `taskMatched`/`status`.
2. **Reuse a design the human built** — `list_workflows` → `get_workflow(name)`. The returned `script`
   is a runnable Workflow script; **run it with your own `Workflow` tool** (this server cannot start a
   run). Read the decoded `contract` to understand its declared inputs before running.
3. **Reproduce a specific run** — `get_run_design(run_id)` with `source='snapshot'` gives the exact script.
4. **Hand the human a draft** — `save_workflow(name, script)` puts a Workflow script into their block
   builder (appears in `list_workflows`). An agent-authored script has no builder sidecar, so it opens
   via lossy recovery (`editable=false`) — tell the user it's a starting point to refine, not a finished
   builder design. `save_workflow` refuses to overwrite an existing name unless `overwrite=true`.
5. **Promote a good run** into a reusable, named workflow — `promote_run(run_id, name)`.

## Scope

Call `get_context` first: it reports the project/session you're scoped to and, importantly, `dataDir` —
where `save_workflow` writes. For your drafts to appear in the human's dashboard, **both** sides must
use the same `WORKFLOW_STUDIO_DATA` (the default `~/.local/share/workflow-studio` when both run via
`uvx`). If `launchProject` is `null`, the project couldn't be determined and reads span all projects.

## Opening the dashboard for the human

The human sees the visual builder + timeline in a browser. Run `/workflow-studio:dashboard` (or
`uvx workflow-studio`) to start it on `http://127.0.0.1:8787/`.

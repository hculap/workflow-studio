# Workflow Studio — Launch Kit

Honest promotion copy for **Workflow Studio** v0.1.0. Every claim here is grounded in the codebase and the publish brief. Read the ground rules before editing:

- **Not on PyPI yet.** The install that works today is the plugin with its **bundled wheel**. PyPI (`uvx workflow-studio`) is a documented next step, not a live channel. Never write "pip install" / "available on PyPI" as if it were live.
- **No fabricated traction.** No user counts, stars, benchmarks, latency numbers, "blazing fast", or testimonials — none exist.
- **No invented features.** Only what is listed here (all verified in the code).
- **Screenshots don't exist yet.** All image references are clearly-marked placeholders.
- **Exact commands only** (see [Install](#install-works-today)). A wrong command in promo = broken onboarding.

---

## Positioning blurb (what / who / why now)

**What.** Workflow Studio is a local, no-code builder + observability dashboard for **Claude Code's `Workflow` tool** — the deterministic multi-agent orchestration primitive. You **watch** what a multi-agent run actually did and **author** new workflows visually, and it exposes both halves to the Claude Code agent over **MCP** so you and the agent collaborate through one live surface.

**Who.** Developers who use Claude Code's `Workflow` tool — fan-out subagents, pipelines, adversarial review, loops. Anyone who has run a multi-agent workflow and then wanted to (a) see the phase / agent / token breakdown, (b) reuse or tweak a workflow without hand-writing the JS, or (c) let the agent discover and run the designs they built.

**Why now.** The `Workflow` tool gives you deterministic multi-agent runs, but the only human↔agent channel is a script file dropped on disk that the agent is blind to, and each run leaves on-disk artifacts nobody visualizes. Workflow Studio closes both gaps: it reads Claude Code's own run artifacts and renders them, and it turns the script-on-disk into a live two-way surface over MCP. It runs entirely locally (binds `127.0.0.1`), has **zero runtime dependencies** (pure Python standard library), and ships the pre-built UI inside one wheel.

---

## Announcements

### Short (one paragraph)

**Workflow Studio** is a local, no-code builder and observability dashboard for Claude Code's `Workflow` tool. It reads Claude Code's own on-disk run artifacts and renders each multi-agent run as a graph/timeline — phases, per-agent nodes, tokens, timing, which branch was taken — and it gives you a no-code block canvas that compiles to a runnable Workflow script. Both halves are exposed to the Claude Code agent over an MCP server (9 tools), so the agent can discover what you built, read a design's declared contract, and draft new workflows back into your builder for you to refine. It runs entirely on `127.0.0.1`, has zero runtime dependencies (pure Python standard library, ships the pre-built UI in one wheel), and installs today as a Claude Code plugin. MIT licensed.

### Long (blog / GitHub Discussions post)

> **Title:** Introducing Workflow Studio — observe and author Claude Code Workflow runs

Claude Code's `Workflow` tool lets you orchestrate deterministic multi-agent runs — fan-out subagents, pipelines, adversarial review, loops. It's powerful, but it's also a bit of a black box in two directions. When a run finishes, the interesting story (which phase ran, which branch was taken, how many tokens each agent burned, how long each leg took) is buried in on-disk artifacts nobody visualizes. And in the other direction, the only way to hand a workflow to the agent is to drop a script file on disk that the agent can't actually see. Workflow Studio is built to close both gaps.

**Observe.** The dashboard reads Claude Code's *own* run artifacts (from `~/.claude/projects/**/subagents/workflows/`) and renders each run as a graph/timeline: phases, per-agent nodes, tokens, timing, and which branch a gate or switch actually took. Live runs are included and the view auto-refreshes as a run progresses. Honesty is built into what you see, not bolted on: an observed run carries a `taskMatched` flag (when it's false, the metrics are heuristic/unknown, *not* measured), and a `status` (a live or incomplete run's elapsed span is shown as a lower bound, never as a final measurement).

**Author.** The other half is a no-code block builder — a canvas with 12 block kinds (agent, fanout, loop, subwf, gate, filter, switch, pipeline, rank, input, param, start) that compiles down to a real, runnable Workflow script using the actual primitives (`agent()`, `phase()`, `parallel()`, `pipeline()`, `log()`). It also emits a `@wf-builder` sidecar so a design round-trips losslessly between the visual builder and the script. Designs carry an honest `source` (`snapshot` = exactly what ran, `template` = a fallback that may differ) and a `hasSidecar` flag with a decoded contract, so you always know whether a design is a faithful record or a best-effort recovery.

**Collaborate over MCP.** Both halves are exposed to the Claude Code agent through a hand-rolled, dependency-free MCP server (`workflow-studio mcp`) with **9 tools** — seven read tools (`get_context`, `list_projects`, `list_runs`, `get_run`, `list_workflows`, `get_workflow`, `get_run_design`) and two write tools (`save_workflow`, which drafts a design *into* your builder, and `promote_run`, which turns a run into a reusable workflow). The server never fabricates or conflates: observed data keeps its `taskMatched`/`status` flags, declared designs keep their `source`/`hasSidecar`/contract, and the server *cannot start a run* — it hands the agent a design's `script` to execute with the agent's own `Workflow` tool. The result is one live surface where you build in the canvas, the agent discovers and runs what you built, inspects the observations, and drafts designs back for you to refine.

It's local-first and boring in the right ways: pure Python standard library, **zero runtime dependencies**, `requires-python >=3.9`, binds `127.0.0.1` only, no telemetry, no network calls. The MCP server is a plain JSON-RPC 2.0 stdio loop (no SDK) so the package resolves and starts instantly under `uvx`. It installs today as a Claude Code plugin with a bundled wheel — see the install steps below. MIT licensed, by Szymon Paluch.

> _Screenshots are placeholders until captured — see the [demo storyboard](#demo-gif-storyboard-3060s) below._
>
> `![Workflow Studio dashboard](assets/dashboard.png)` — **TODO: add screenshot**

---

## Install (works today)

Requires `uv` / `uvx` on your `PATH` (https://docs.astral.sh/uv/).

### Plugin (recommended — bundled wheel, no PyPI needed)

Once the repo is pushed to GitHub:

```
/plugin marketplace add hculap/workflow-studio
/plugin install workflow-studio@workflow-studio
```

Then `/mcp` lists `workflow-studio` (9 tools) and `/workflow-studio:dashboard` opens the UI.

### Local dev (before pushing to GitHub)

```
/plugin marketplace add /absolute/path/to/plugin-marketplace
/plugin install workflow-studio@workflow-studio
```

### MCP server only (no plugin)

```
claude mcp add workflow-studio -s user -- uvx --from /path/to/workflow_studio-0.1.0-py3-none-any.whl workflow-studio mcp
```

### Dashboard (standalone)

Before PyPI (local wheel): `uvx --from /path/to/wheel workflow-studio`.
After a future PyPI publish: `uvx workflow-studio`.

> **PyPI is a documented next step, not live.** When ready: `uv publish`, then simplify the plugin's `mcpServers` command to `{"command":"uvx","args":["workflow-studio","mcp"]}`, drop the vendored wheel, and re-install. Until then, the bundled wheel is the mechanism.

---

## Social posts

### X / Twitter (262 chars)

> Workflow Studio: a local, no-code builder + observability dashboard for Claude Code's Workflow tool. Watch what a multi-agent run actually did, author new workflows visually, and hand both to the agent over MCP (9 tools). Zero runtime deps, binds 127.0.0.1, MIT.

### Reddit — r/ClaudeAI

**Title:** I built Workflow Studio — a local dashboard to *see* what your Claude Code multi-agent Workflow runs actually did (+ a no-code builder, exposed to the agent over MCP)

**Body:**

If you use Claude Code's `Workflow` tool for multi-agent runs (fan-out, pipelines, adversarial review, loops), you've probably hit the same two frustrations I did: after a run there's no good way to *see* what happened, and the only way to hand a workflow to the agent is a script file on disk the agent can't actually read.

Workflow Studio is my attempt to fix both:

- **Observe** — it reads Claude Code's own on-disk run artifacts and renders each run as a graph/timeline: phases, per-agent nodes, tokens, timing, and which branch a gate/switch took. Live runs included, auto-refreshes.
- **Author** — a no-code block canvas (12 block kinds: agent, fanout, loop, subwf, gate, filter, switch, pipeline, rank, input, param, start) that compiles to a real, runnable Workflow script.
- **Collaborate over MCP** — a dependency-free MCP server with 9 tools lets the agent list/inspect your runs, read a design's declared contract, and draft new workflows *into* your builder.

Honesty is baked into the data, not marketing: observed runs carry a `taskMatched` flag (false = the numbers are heuristic, not measured) and a `status` (a live run's elapsed time is shown as a lower bound); declared designs carry a `source` (`snapshot` = exactly what ran vs `template` = may differ). The server also can't start runs — it hands the agent a `script` to run with its own `Workflow` tool.

It's local-only (binds `127.0.0.1`, no telemetry, no network calls), pure Python standard library with **zero runtime dependencies**, and ships the pre-built UI in one wheel. MIT licensed.

**It is not on PyPI yet** — the working install today is a Claude Code plugin with a bundled wheel:

```
/plugin marketplace add hculap/workflow-studio
/plugin install workflow-studio@workflow-studio
```

Then `/mcp` shows the 9 tools and `/workflow-studio:dashboard` opens the UI. Needs `uv`/`uvx` on PATH. Repo: https://github.com/hculap/workflow-studio — feedback and issues welcome.

### Hacker News — Show HN

**Title:** Show HN: Workflow Studio – observe and author Claude Code multi-agent Workflow runs

**First comment:**

Author here. Claude Code has a `Workflow` tool for deterministic multi-agent orchestration (fan-out subagents, pipelines, adversarial review, loops). I kept wanting two things it doesn't give you: a way to *see* what a run actually did after the fact, and a way to hand a workflow to the agent that the agent can actually inspect (today it's just a script file on disk it's blind to).

Workflow Studio has two halves plus an MCP bridge:

- **Observe:** a React dashboard that reads Claude Code's own on-disk run artifacts and renders each run as a graph/timeline — phases, per-agent nodes, tokens, timing, which branch was taken. Live runs auto-refresh.
- **Author:** a no-code block canvas (12 block kinds) that compiles to a real, runnable Workflow script and emits a sidecar so designs round-trip losslessly.
- **MCP server:** 9 tools (7 read, 2 write) so the agent can discover your runs and designs, read a design's declared contract, and draft workflows back into your builder.

Two design choices I care about:

1. **Honesty in the data.** Observed metrics carry `taskMatched` (false = heuristic, not measured) and `status` (a live/incomplete elapsed span is a lower bound); declared designs carry `source` (`snapshot` = exactly what ran vs `template` = may differ) and a `hasSidecar` contract flag. The server never conflates "declared" with "observed," and it can't start runs — it hands back a `script` for the agent's own `Workflow` tool.
2. **Zero dependencies.** The core is pure Python standard library (`dependencies = []`, `requires-python >=3.9`) and the MCP server is a hand-rolled JSON-RPC 2.0 stdio loop with no SDK, so it resolves and starts instantly under `uvx`. Ships the pre-built UI in one wheel. Runs on `127.0.0.1`, no telemetry.

Caveat: **it's not on PyPI yet.** The install that works today is a Claude Code plugin with a bundled wheel (`/plugin marketplace add hculap/workflow-studio` then `/plugin install workflow-studio@workflow-studio`; needs `uv`/`uvx` on PATH). PyPI + a `uvx workflow-studio` one-liner is the documented next step. No screenshots in the repo yet — that's on the near-term list. MIT. Repo: https://github.com/hculap/workflow-studio. Happy to answer questions.

---

## Demo GIF storyboard (30–60s)

No screenshots or recordings exist yet — this is the shot list to produce the launch GIF. Target 45s, silent, with short on-screen caption cards between beats. Record at 2× terminal font size; keep the dashboard and a Claude Code session side by side (or cut between them) so the "one live surface" story is visible.

| # | Time | Scene | On-screen caption |
|---|------|-------|-------------------|
| 1 | 0:00–0:06 | Claude Code prompt. Type `/plugin marketplace add hculap/workflow-studio` then `/plugin install workflow-studio@workflow-studio`. Show the install confirmation. | "Install as a plugin — bundled wheel, no PyPI needed" |
| 2 | 0:06–0:11 | Run `/mcp`; highlight `workflow-studio` listed with its 9 tools and a `✔ Connected` state. | "9 MCP tools. Connected." |
| 3 | 0:11–0:17 | Run `/workflow-studio:dashboard`; the browser opens the dashboard at `127.0.0.1`. | "Local dashboard — binds 127.0.0.1" |
| 4 | 0:17–0:27 | Open a **real run**: the graph/timeline renders phases, per-agent nodes, tokens, timing. Hover a gate/switch to show which branch was taken. If the run is live, point the cursor at the `status` badge (elapsed = lower bound). | "See what the run actually did — and what's heuristic vs measured" |
| 5 | 0:27–0:37 | Cut to the Claude Code session. The agent calls `list_runs` (list appears), then `get_run` on one run — show the returned graph with the `taskMatched` / `status` fields visible. | "The agent inspects the same runs over MCP" |
| 6 | 0:37–0:47 | Agent calls `save_workflow` with a drafted script. Cut back to the dashboard's builder; the drafted design **appears in the block canvas** (agent/fanout/gate blocks visible). | "Agent drafts a workflow — it shows up in your builder" |
| 7 | 0:47–0:52 | Hold on the builder canvas with the drafted blocks; end card. | "Workflow Studio — observe + author, one live surface. MIT · github.com/hculap/workflow-studio" |

Recording tips: pre-seed one completed run **and** one live run before recording (beat 4 needs a real graph, not an empty state); if `save_workflow`'s draft doesn't appear in the builder, confirm the dashboard and the MCP server share the same data dir (`get_context` reports the resolved `dataDir` — a mismatch is the usual cause).

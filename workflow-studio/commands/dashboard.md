---
description: Open the Workflow Studio dashboard (visual no-code builder + run timeline) in the browser.
argument-hint: "[--port N] [--all-projects]"
allowed-tools: Bash(uvx workflow-studio*)
---

Start the Workflow Studio dashboard for the user as a background process and report the URL.

Run (in the background so it keeps serving; pass through any arguments the user gave in `$ARGUMENTS`):

```
uvx workflow-studio $ARGUMENTS
```

It serves at `http://127.0.0.1:8787/` (it scans for a free port if 8787 is taken — read the printed
URL from its output). By default it scopes to the current project's runs; `--all-projects` shows every
project on the machine. Tell the user the URL and that the dashboard auto-refreshes as runs progress.

Note: this needs `uvx` (from Astral's `uv`) on PATH. If it isn't installed, point the user to
https://docs.astral.sh/uv/ .

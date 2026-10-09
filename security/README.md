# Dashboard request guard (not released yet)

The dashboard server in `workflow-studio` 0.2.0 (`workflow_studio/serve.py`) answers any request that reaches its port:

- **CSRF.** `do_POST` parses the body as JSON whatever its `Content-Type`, and checks neither `Origin` nor `Host`. Any web page open in the same browser can make a cross-site `POST /save`, `/make-template` or `/link` to `http://127.0.0.1:8787` and write a builder template or a ledger entry.
- **DNS rebinding.** `do_GET` does not check `Host`. A page on a domain that re-resolves to `127.0.0.1` can read `/runs`, `/data.json` and `/run-design`, which are built from Claude Code transcripts and run artifacts, and the saved templates (`/templates`, `/template`). Reproduced on 2026-10-09 against a running 0.2.0: `curl -H 'Host: evil.example' http://127.0.0.1:8787/context` answers 200.

The application source is not in this repository (it lives in the package source project), so the fix is carried here as a patch, with a test.

## What the patch does

`0001-dashboard-request-guard.patch`, against `workflow_studio/serve.py` from the 0.2.0 sdist (sha256 `2e6a082e…`, identical in the wheel):

- Every request: the `Host` header must be on an allowlist. By default it holds `127.0.0.1`, `localhost` and `[::1]` on the bound port, plus the `--host` address unless it is a wildcard. Anything else gets 403.
- Extra names come from `--allowed-host` (repeatable) or `WORKFLOW_STUDIO_ALLOWED_HOSTS` (comma-separated). An entry without a port allows that name on any port.
- Every `POST`: an `Origin`, when present, must pass the same allowlist (`null` never does), and `Sec-Fetch-Site: cross-site` is refused (403). The body must be `Content-Type: application/json`, otherwise 415. A plain HTML form cannot send that type, and a cross-site `fetch` with it needs a CORS preflight that the server never answers. The dashboard's own client already sends it (`web/src/api/client.ts`).
- `HEAD` gets the same Host check as `GET`.
- `log_message` no longer raises when `send_error` logs `(code, message)`. In 0.2.0 any 404 or other error response raised a `TypeError` there and dropped the connection without a reply.

The MCP server (`workflow-studio mcp`) speaks stdio only and is unaffected.

## Behind a reverse proxy: action needed on upgrade

A proxy that forwards the public `Host`, such as the nginx example in the main README (`proxy_set_header Host $host`), will get 403 until its public name is allowed:

```
WORKFLOW_STUDIO_ALLOWED_HOSTS=example.com workflow-studio --no-open --base-path /workflow-studio
```

In a systemd unit, add `Environment=WORKFLOW_STUDIO_ALLOWED_HOSTS=example.com`. The browser's `Origin` behind the proxy is that same public name, so saving templates keeps working. A unit that runs an unpinned `uvx workflow-studio` picks up the new version by itself once it is on PyPI, so set the variable before the release.

## Apply and test

In the package source project:

```
patch -p1 < /path/to/this/repo/security/0001-dashboard-request-guard.patch
WS_SRC=$PWD python3 /path/to/this/repo/security/test_request_guard.py
```

The test is standard library only. It starts the patched server on a free port, with `HOME` and `WORKFLOW_STUDIO_DATA` pointed at a temporary directory, and checks 9 cases: loopback hosts served, rebinding hosts refused (GET, HEAD, POST), loopback on another port refused, proxy names allowed, non-JSON POST refused, cross-origin and `null` origins refused, same-origin and Origin-less POSTs allowed through. It also fails if the server logs a traceback.

## Release

1. Apply the patch, add the main README's proxy note (above), release the package (for example 0.2.1) to PyPI.
2. Here: move the pin to the new version in `workflow-studio/.claude-plugin/plugin.json`, `commands/dashboard.md`, `skills/workflow-studio/SKILL.md` and the plugin `README.md`, raise the plugin `version`, and add a CHANGELOG entry.
3. Then submit the plugin to Anthropic's directory.

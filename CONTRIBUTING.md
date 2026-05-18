# Contributing

This repo has a strict admission bar to keep the catalog signal-rich.

## Admission criteria

A tool is admitted to `data/tools.yaml` only if **all** of these are true:

- Published on GitHub (or has a clearly canonical homepage if not OSS).
- Last commit within 18 months (otherwise it goes to a `dead/` archive, not the main list).
- Solves a problem that an existing entry doesn't solve, OR is a clearly better implementation of the same problem.
- Has a concrete `when_to_use` — one sentence, no marketing language. "Faster than X" / "More modern than Y" are not acceptable.

## Adding a tool

1. Add a stub entry to `data/tools.yaml`. Required fields: `name`, `slug`, `repo`, `category`, `when_to_use`. The verifier fills in everything else.
2. Run `python scripts/verify.py` to refresh metadata from the GitHub API and re-classify status. This rewrites `data/tools.yaml` in place and regenerates `data/verified.json`.
3. Run `python scripts/render_catalog.py` to regenerate `docs/catalog.md`.
4. If the tool fills a gap not covered by any workflow in `docs/workflows.md`, add a paragraph to the relevant layer.
5. Open PR.

The weekly GitHub Action (`.github/workflows/verify.yml`) re-runs steps 2-3 every Monday and auto-commits drift, so once a tool is in `tools.yaml` it stays current without manual upkeep.

## Removing a tool

If a tool stops working (e.g., new defender release broke it, project archived):

1. Don't delete — move to `dead/<year>.md` with a one-line note on why.
2. Update any workflow that referenced it to point to a replacement.

## Schema for `data/tools.yaml`

```yaml
- name: <Display Name>
  slug: <kebab-case>             # used in URLs and JSON keys
  repo: <owner/repo>             # GitHub canonical, or null
  category: <one of the workflow categories>
  when_to_use: <one sentence>    # required, terse
  install: <one shell command>   # optional, helpful
  notes: <free text>             # optional, only if non-obvious
```

The verifier fills in: `stars`, `last_push`, `license`, `language`, `description`, `status`, `latest_release`.

## Categories (canonical list)

- `transport-mitm`
- `pre-bootstrap-injection`
- `cdp-instrumentation`
- `anti-detect-browser`
- `function-hooking`
- `deobfuscation`
- `ast-transform`
- `ai-deobfuscation`
- `bundler-analysis`
- `memory-forensics`
- `tracing`
- `time-travel`
- `native-instrumentation`
- `wasm-reverse`
- `electron-reverse`
- `hermes-reverse`
- `framework-devtools`
- `browser-extension`
- `anti-anti-debug`
- `mcp-toolkit`
- `alt-debugger`
- `replay-debugger`
- `react-native-instrumentation`

Don't invent new categories without discussion — overlap dilutes signal.

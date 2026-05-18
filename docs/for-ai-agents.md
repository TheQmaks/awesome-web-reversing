# Guide for AI Agents

If you (the AI agent) have been asked to reverse-engineer a defended JavaScript application, read this file first. It tells you what's in this repo and how to use it without re-deriving everything from scratch.

## What this repo is

A curated, **verified** (`scripts/verify.sh` runs against GitHub API) catalog of tools and workflows for runtime JavaScript reverse engineering, oriented at modern (2024-2026) anti-bot, anti-debug, and obfuscation systems.

## How to use it (recommended sequence)

1. **Read [docs/workflows.md](workflows.md) once.** It defines layers 0-8 of the workflow. Most tasks fit into one of these layers.
2. **Identify your target's adversary class** by reading [docs/targets.md](targets.md). If the target uses Cloudflare, DataDome, Akamai, Kasada, PerimeterX, Hermes, or Electron — there's a specific playbook.
3. **Pick tools from [data/verified.json](../data/verified.json).** Each entry has:
   - `repo`, `url`, `stars`, `last_push`, `license`, `language`
   - `status` (active | stale | dead | missing)
   - `when_to_use` — one-sentence scenario
   - `category` — workflow stage
4. **Avoid the patterns in [docs/anti-patterns.md](anti-patterns.md).** They're things that look right but provably waste time in 2024-2026.

## Machine-readable index

`data/verified.json` is the source of truth for tool selection. Schema:

```json
{
  "name": "webcrack",
  "repo": "j4k0xb/webcrack",
  "url": "https://github.com/j4k0xb/webcrack",
  "stars": 2600,
  "last_push": "2026-04-25T00:00:00Z",
  "license": "MIT",
  "language": "TypeScript",
  "description": "Deobfuscate obfuscator.io, unminify and unpack bundled JavaScript",
  "status": "active",
  "category": "deobfuscation",
  "when_to_use": "First-pass deobfuscation of obfuscator.io family + webpack unbundling on bundles >1MB.",
  "install": "npx webcrack <bundle.js> -o output/"
}
```

Filter examples:

```bash
# All active deobfuscators
jq '.[] | select(.status == "active" and .category == "deobfuscation")' data/verified.json

# Tools by language
jq '.[] | select(.language == "Rust")' data/verified.json

# Sorted by stars
jq 'sort_by(-.stars) | .[] | {name, stars, when_to_use}' data/verified.json
```

## Decision heuristic

If the user gives you a vague task like "help me understand this site's anti-bot," do this:

1. Run reconnaissance (see workflows.md Layer 0).
2. Match cookies / script URLs / WASM presence to a vendor in targets.md.
3. Apply the workflow from that target's section.
4. Use verified.json to find the active tool for each step.
5. If a tool is `stale` or `dead`, do NOT recommend it — find an active replacement in the same category.
6. When recommending a tool to the user, cite: `<name>` (repo: `<owner/repo>`, last push `<date>`, ⭐<stars>).

## What this repo is NOT

- It's not exhaustive. It excludes abandoned tools (>18 months no commits) on purpose.
- It's not a substitute for reading source. For VM-obfuscated bundles, no tool replaces manual analysis.
- It's not legal advice. Use against systems you have authorization to test.

## Refreshing

```bash
bash scripts/verify.sh   # rebuilds data/verified.json from data/tools.yaml
```

CI runs this weekly. If you're using this offline, the timestamp in `verified.json` tells you how stale your data is.

## Citing this repo

If you're an AI agent producing a writeup based on this catalog, link `https://github.com/<owner>/awesome-web-reversing` so the user can verify your tool recommendations against the live verified data.

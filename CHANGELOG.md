# Changelog

## v0.1.0 — 2026-05-17

Initial release.

- Seeded catalog from synthesis of five 2026 deep-research reports on JS RE tooling (Claude, Gemini, DeepSeek, ChatGPT, Qwen).
- 99 tools verified against GitHub API via 5 parallel verifier subagents (4 verifying base list + 1 gap-fill discovering missing categories).
- Status breakdown: 76 active, 5 stale, 2 renamed, 14 dead, 2 missing/hallucinated.
- Gap-fill agent uncovered the biggest miss: **TLS/JA3/JA4 fingerprint impersonation** (9 tools). This is where 2024-2026 anti-bot defense has shifted, and the original reports under-covered it.
- Workflow guide (`docs/workflows.md`) with 8-layer approach.
- Per-vendor playbooks (`docs/targets.md`): Cloudflare, DataDome, Akamai, PerimeterX/HUMAN, Kasada, Imperva, ChatGPT-SSE, Electron, Hermes/React Native.
- Anti-patterns guide (`docs/anti-patterns.md`).
- AI-agent guide (`docs/for-ai-agents.md`).
- Verifier scripts (`scripts/verify.py`, `scripts/render_catalog.py`).
- JSON Schema for `verified.json` (`data/schema.json`).

### Notable findings during seeding

- `jshookmcp` (vmoranv/jshookmcp) — newly released MCP server with 402 tools across 36 domains, ⭐1.5k in 3 months. Most relevant for AI-agent-driven RE workflows.
- `Cetus`: original report attribution `jakobwesthoff/Cetus` was wrong — canonical repo is `Qwokka/Cetus`.
- `webpack-bundle-analyzer`: ownership moved from `webpack-contrib/` to `webpack/` org.
- `fetch-intercept`: ownership moved from `werk85/` to `mlegenhausen/`.
- React DevTools / Angular DevTools: now live inside main framework monorepos, not standalone repos.
- `ghidra_nodejs`: archived at `PositiveTechnologies/ghidra_nodejs` (last 2021), but still the only Ghidra plugin for Bytenode `.jsc` — kept as dead-but-canonical.
- `twiggy`: GitHub-archived but received a 2026 push; flagged active-low-maintenance.
- Hallucinated entries removed: `unminify-js` (no canonical repo), `synchrony-rs` (Rust port doesn't exist per current search).

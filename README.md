# awesome-web-reversing

> Verified tools and workflows for runtime JavaScript reverse engineering of modern defended SPAs.
> Curated for 2024-2026 anti-bot landscape (Cloudflare bm-vm, DataDome, Akamai, PerimeterX/HUMAN, Kasada).

**Differentiator from existing awesome-lists:** every entry is verified against the GitHub API. Dead and abandoned tools are marked or excluded. The catalog is automatically refreshable (`scripts/verify.py`).

**v1 stats (2026-05-18):** 99 verified tools — 🟢 72 active · 🟡 10 stale · 🔴 15 dead · ⚫ 2 missing/hallucinated. Renames are tracked via `renamed_from` field, not status. Browse the full catalog in [docs/catalog.md](docs/catalog.md) or query `data/verified.json` directly.

---

## Quick start

| If you want to... | Read this |
|---|---|
| Understand the workflow philosophy | [docs/workflows.md](docs/workflows.md) |
| Bypass a specific anti-bot vendor | [docs/targets.md](docs/targets.md) |
| Avoid common dead-end patterns | [docs/anti-patterns.md](docs/anti-patterns.md) |
| Drive this catalog from an AI agent | [docs/for-ai-agents.md](docs/for-ai-agents.md) |
| Add a new tool / contribute | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Programmatic tool selection | [data/verified.json](data/verified.json) |

---

## The thesis in one paragraph

Standard Chrome DevTools fails on defended modern SPAs. Bundles 5-30 MB break pretty-print; anti-debug traps trigger on the act of opening DevTools; `Function.prototype.toString` integrity checks defeat naïve hooks; and per-customer ML fingerprints (DataDome) make generic stealth plugins obsolete. The winning approach in 2024-2026 is **fight the delivery, not the runtime**: rewrite the JS in transit (mitmproxy / Caido), install hooks before site bootstrap (Playwright `addInitScript`), instrument at scale via raw CDP, then escalate to AST deobfuscation (Webcrack), heap forensics (MemLab), and — for Electron / React Native — native instrumentation (Frida). DevTools is one tool of many, not the spine of the workflow.

---

## Catalog (top-level summary)

The full verified catalog lives in [data/verified.json](data/verified.json). See [docs/workflows.md](docs/workflows.md) for the layered grouping. High-confidence picks per layer:

| Layer | Primary tool | Backup |
|---|---|---|
| Reconnaissance | `scrapfly/Antibot-Detector` (vendor fingerprint), `creepjs` (FP testbed), `niespodd/browser-fingerprinting` (FP cookbook) | `browsers-benchmark` for empirical bypass rates |
| Transport rewriting | `mitmproxy` | `Caido`, `Proxyman`, `HTTP Toolkit` |
| TLS/JA3/JA4 fingerprint | `curl_cffi` (Python), `tls-client` (Go), `wreq` (Rust), `httpcloak` (HTTP/3) | `fingerproxy` for self-hosted mirror |
| Pre-bootstrap injection | `Playwright.addInitScript` | `Puppeteer.evaluateOnNewDocument`, `Tampermonkey` |
| Anti-detect browser | `Camoufox` (Firefox-fork, C++ patches) | `BotBrowser`, `Patchright`, `nodriver`, `zendriver` |
| Stealth patches | `rebrowser-patches` (fixes 2024+ Runtime.Enable leak) | — |
| CDP mass instrumentation | `chrome-remote-interface` | `wirebrowser`, `chromedp`, `jshookmcp` |
| Deobfuscation | `webcrack` → `restringer` → `obfuscator-io-deobfuscator` | `jscrambler-deobfuscator` for Jscrambler, `obfio-deobfuscator-go` for speed |
| AST search/codemod | `ast-grep`, `jscodeshift` | `swc` plugins |
| AI-assisted RE | `humanify` (renaming) | `stealth-browser-mcp`, `jshook-reverse-tool` |
| Memory forensics | `MemLab` | Chrome DevTools heap snapshot diff |
| Time-travel | `Replay.io` (web) / `rr` + `Pernosco` (native) | — |
| Native instrumentation | `Frida` (+ `frida-node`, `r2frida`) | `LIEF` for static binary patching |
| WASM reverse | `WABT` (`wasm-decompile`), `NotDec` (LLVM-IR-based) | `Binaryen`, `Cetus` (live), `wasm-tools` |
| Electron reverse | `@electron/asar` + version-matched V8 d8 | `electronegativity` for config audit |
| Hermes reverse | `hermes-dec`, `hermes-decomp`, `hbctool` | `heresy` for live hooks |
| Vendor protocol RE | `xKiian/datadome-vm`, `hyper-sdk-py` (Kasada/Akamai docs) | — |
| MCP for AI agents | `jshookmcp` (402 tools across 36 domains), `stealth-browser-mcp` | — |

---

## Verification

Every entry is checked weekly via [`.github/workflows/verify.yml`](.github/workflows/verify.yml):

- `active` — pushed within last 6 months
- `stale` — 6-18 months since last push (kept, but flagged)
- `dead` — >18 months (kept with marker; explicit GitHub-archived flag also surfaced when present)
- `missing` — repo returned 404 (renamed, deleted, or hallucinated)

Renames are tracked via a separate `renamed_from` field, so they can combine with any lifecycle status.

Run locally:

```bash
pip install -r requirements.txt
python scripts/verify.py             # refresh tools.yaml + verified.json from GitHub
python scripts/render_catalog.py     # regenerate docs/catalog.md
```

Requires `gh` CLI authenticated (`gh auth login`).

Last verifier run: see `generated_at` field in [data/verified.json](data/verified.json).

---

## Project layout

```
.
├── README.md                     # this file
├── LICENSE                       # MIT
├── CHANGELOG.md
├── CONTRIBUTING.md
├── requirements.txt              # PyYAML
├── .github/workflows/verify.yml  # weekly verifier CI
├── docs/
│   ├── workflows.md              # layered approach (the meat)
│   ├── targets.md                # per-vendor playbooks
│   ├── anti-patterns.md          # what doesn't work
│   ├── for-ai-agents.md          # how AI agents should use this repo
│   └── catalog.md                # auto-generated tool catalog
├── data/
│   ├── tools.yaml                # source of truth (hand-curated)
│   ├── verified.json             # generated GitHub metadata
│   └── schema.json               # JSON Schema for verified.json
└── scripts/
    ├── verify.py                 # refreshes tools.yaml + verified.json
    └── render_catalog.py         # rebuilds docs/catalog.md
```

---

## License

MIT for the docs and scripts. Each tool listed has its own license — check `data/verified.json`.

---

## Acknowledgments

Catalog seeded from a synthesis of five 2026 deep-research reports (Claude, Gemini, DeepSeek, ChatGPT, Qwen) on JS RE tools, with claims independently verified against GitHub API. Original prompt: "what beats Chrome DevTools for reverse-engineering modern defended SPAs?"

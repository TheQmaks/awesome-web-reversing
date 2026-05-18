#!/usr/bin/env python3
"""Render data/verified.json into a Markdown catalog grouped by category.

Output: docs/catalog.md
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = REPO_ROOT / "data" / "verified.json"
OUT_PATH = REPO_ROOT / "docs" / "catalog.md"

# Human-readable category headings ordered by workflow layer
CATEGORY_ORDER = [
    ("anti-bot-recon", "Layer 0 — Anti-bot reconnaissance / fingerprint testbeds"),
    ("anti-bot-benchmarks", "Layer 0 — Bypass benchmarks (empirical)"),
    ("research-notes", "Layer 0 — Research notes & cookbooks"),
    ("vendor-protocol-research", "Layer 0 — Vendor protocol RE artifacts"),
    ("network-mitm", "Layer 1 — Transport rewriting (MITM)"),
    ("tls-http-fingerprint", "Layer 1 — TLS / JA3 / JA4 / HTTP fingerprint impersonation"),
    ("browser-automation", "Layer 2/3 — Browser automation + pre-bootstrap injection"),
    ("anti-detect-browser", "Layer 2 — Anti-detect browsers & stealth patches"),
    ("fingerprint-generation", "Layer 2 — Fingerprint bundle generation"),
    ("cdp-instrumentation", "Layer 3 — CDP-level instrumentation"),
    ("function-hooking", "Layer 2 — Function hooking"),
    ("browser-extension", "Layer 2 — Browser extensions / userscripts"),
    ("anti-anti-debug", "Layer 1/2 — Anti-anti-debug"),
    ("deobfuscation", "Layer 4 — Deobfuscation"),
    ("ast-transform", "Layer 4 — AST transformation"),
    ("ai-deobfuscation", "Layer 4 — AI-assisted deobfuscation"),
    ("ai-assisted-re", "Layer 4 — AI-assisted reverse engineering (broader)"),
    ("bundler-analysis", "Layer 4 — Bundle analysis"),
    ("framework-devtools", "Layer 5 — Framework-specific devtools"),
    ("memory-forensics", "Layer 6 — Memory & heap forensics"),
    ("tracing", "Layer 6 — Tracing / observability"),
    ("native-instrumentation", "Layer 7 — Native instrumentation (Frida + co.)"),
    ("electron-reverse", "Layer 7 — Electron-specific"),
    ("hermes-reverse", "Layer 7 — Hermes / React Native"),
    ("react-native-instrumentation", "Layer 7 — React Native runtime hooks"),
    ("wasm-reverse", "Layer 7 — WebAssembly reverse"),
    ("replay-debugger", "Layer 8 — Time-travel / replay"),
    ("alt-debugger", "Alternative debuggers"),
    ("mcp-toolkit", "MCP toolkits for AI agents"),
]

STATUS_BADGE = {
    "active": "🟢",
    "stale": "🟡",
    "dead": "🔴",
    "missing": "⚫",
}


def fmt_tool(t: dict) -> str:
    badge = STATUS_BADGE.get(t["status"], "❓")
    if t.get("archived"):
        badge += "🗄"
    stars = t.get("stars") or 0
    repo = t.get("repo") or ""
    url = t.get("url") or "—"
    last_push = (t.get("last_push") or "—")[:10]
    license = t.get("license") or "—"
    lang = t.get("language") or "—"
    when = t.get("when_to_use") or "—"
    desc = (t.get("description") or "").replace("\n", " ").strip()
    name = t.get("name") or t.get("slug")

    lines = [
        f"### {badge} {name}",
        "",
        f"- **Repo:** [{repo}]({url}) · ⭐ {stars:,} · {lang} · {license}",
        f"- **Last push:** {last_push} · **Status:** `{t['status']}`",
        f"- **When to use:** {when}",
    ]
    if desc:
        lines.append(f"- **Upstream:** {desc}")
    rel = t.get("latest_release")
    if rel and rel != "no releases":
        lines.append(f"- **Latest release:** {rel}")
    if t.get("renamed_from"):
        lines.append(f"- **Renamed from:** `{t['renamed_from']}`")
    if t.get("archived"):
        lines.append("- **GitHub archived:** yes (maintainers explicitly shut down)")
    if t.get("notes"):
        lines.append(f"- **Notes:** {t['notes']}")
    if t.get("why_added"):
        lines.append(f"- **Why included:** {t['why_added']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    tools = data["tools"]
    by_cat: dict[str, list[dict]] = {}
    for t in tools:
        by_cat.setdefault(t.get("category", "uncategorized"), []).append(t)

    out = [
        "# Tool Catalog",
        "",
        f"_Generated {data['generated_at']} from `data/verified.json`. {data['tool_count']} entries._",
        "",
        "**Status legend:** 🟢 active (push < 6mo) · 🟡 stale (6-18mo) · 🔴 dead (>18mo) · ⚫ missing/hallucinated · 🗄 GitHub-archived (additional flag)",
        "",
        "Catalog is organized by workflow layer (see [workflows.md](workflows.md)). Within each layer, "
        "tools are sorted by star count descending.",
        "",
        "---",
        "",
    ]

    seen_cats: set[str] = set()
    for cat, heading in CATEGORY_ORDER:
        if cat not in by_cat:
            continue
        seen_cats.add(cat)
        out.append(f"## {heading}")
        out.append("")
        for t in sorted(by_cat[cat], key=lambda x: -(x.get("stars") or 0)):
            out.append(fmt_tool(t))
        out.append("---")
        out.append("")

    # Uncategorized
    leftover = [c for c in by_cat if c not in seen_cats]
    if leftover:
        out.append("## Other / Uncategorized")
        out.append("")
        for cat in leftover:
            for t in by_cat[cat]:
                out.append(fmt_tool(t))

    OUT_PATH.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

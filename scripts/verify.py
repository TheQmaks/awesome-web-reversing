#!/usr/bin/env python3
"""verify.py — refresh data/verified.json from current GitHub state.

Reads data/tools.yaml (the source of truth) and re-queries every repo via the
gh CLI. Updates these fields per entry: stars, last_push, license, language,
description, status, archived. Preserves human-curated fields (name, slug,
when_to_use, category, notes, why_added, renamed_from, install).

Status thresholds, in months since last push:
    < 6   active
    6-18  stale
    > 18  dead
    404   missing  (and clears live fields)

Usage:
    python scripts/verify.py
        # rewrites data/tools.yaml in place AND regenerates data/verified.json

    python scripts/verify.py --json-only
        # just rebuild data/verified.json from current tools.yaml (no API calls)

Requires: gh CLI authenticated, PyYAML.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml  (or: pip install -r requirements.txt)")

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "data"
TOOLS_YAML = DATA / "tools.yaml"
VERIFIED_JSON = DATA / "verified.json"
NOW = dt.datetime.now(dt.timezone.utc)

# Fields the verifier OVERWRITES from GitHub. Everything else is preserved.
LIVE_FIELDS = {"stars", "last_push", "license", "language", "description", "status", "archived"}


def gh_api_repo(slug: str) -> dict | None:
    """Return the JSON payload of `gh api repos/{slug}` or None on 404."""
    proc = subprocess.run(
        ["gh", "api", f"repos/{slug}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        if "Not Found" in proc.stderr or "404" in proc.stderr:
            return None
        print(f"  ERROR: gh api repos/{slug}: {proc.stderr.strip()[:120]}", file=sys.stderr)
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def classify(last_push_iso: str) -> str:
    last = dt.datetime.fromisoformat(last_push_iso.replace("Z", "+00:00"))
    months = (NOW - last).days / 30.4375
    if months < 6:
        return "active"
    if months < 18:
        return "stale"
    return "dead"


def refresh_entry(entry: dict) -> dict:
    slug_label = entry.get("name") or entry.get("slug") or "?"
    repo = entry.get("repo")
    if not repo:
        # missing/no-repo entries pass through unchanged
        entry.setdefault("status", "missing")
        return entry

    meta = gh_api_repo(repo)
    if meta is None:
        print(f"  ⚫ {slug_label} ({repo}): not found")
        entry["status"] = "missing"
        for f in LIVE_FIELDS:
            entry.pop(f, None)
        return entry

    pushed = meta["pushed_at"]
    new_status = classify(pushed)
    entry["stars"] = meta["stargazers_count"]
    entry["last_push"] = pushed[:10]
    entry["license"] = (meta.get("license") or {}).get("spdx_id") or "None"
    entry["language"] = meta.get("language")
    entry["description"] = meta.get("description")
    entry["status"] = new_status
    if meta.get("archived"):
        entry["archived"] = True
    else:
        entry.pop("archived", None)

    # Surface canonical name if the repo was transferred.
    canonical = meta.get("full_name")
    if canonical and canonical != repo:
        entry["renamed_from"] = repo
        entry["repo"] = canonical
        entry["url"] = meta.get("html_url") or entry.get("url")

    marker = {"active": "🟢", "stale": "🟡", "dead": "🔴"}.get(new_status, "?")
    print(f"  {marker} {slug_label} ({entry['repo']}): {new_status}, ⭐{entry['stars']}, push {entry['last_push']}")
    return entry


def stringify(obj):
    if isinstance(obj, dict):
        return {k: stringify(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [stringify(v) for v in obj]
    if isinstance(obj, (dt.date, dt.datetime)):
        return obj.isoformat()
    return obj


def render_json(tools: list[dict]) -> None:
    counts: dict[str, int] = {}
    for t in tools:
        counts[t.get("status", "?")] = counts.get(t.get("status", "?"), 0) + 1
    payload = {
        "$schema": "./schema.json",
        "generated_at": NOW.isoformat(),
        "tool_count": len(tools),
        "status_counts": counts,
        "tools": stringify(tools),
    }
    VERIFIED_JSON.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nWrote {VERIFIED_JSON} ({len(tools)} tools)")
    for k in ("active", "stale", "dead", "missing"):
        if k in counts:
            print(f"  {k:>8s}: {counts[k]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json-only", action="store_true", help="Skip GitHub API calls; just rebuild verified.json from tools.yaml.")
    args = ap.parse_args()

    with TOOLS_YAML.open(encoding="utf-8") as f:
        tools = yaml.safe_load(f) or []

    if args.json_only:
        print(f"Rebuilding {VERIFIED_JSON} from {TOOLS_YAML} (no API calls)")
        render_json(tools)
        return 0

    print(f"Verifying {len(tools)} tools against GitHub API…")
    updated = [refresh_entry(t) for t in tools]

    # Re-sort: category asc, stars desc
    updated.sort(key=lambda e: (e.get("category", "zzz"), -(e.get("stars") or 0)))

    with TOOLS_YAML.open("w", encoding="utf-8") as f:
        yaml.safe_dump(stringify(updated), f, allow_unicode=True, sort_keys=False, width=200)
    print(f"\nUpdated {TOOLS_YAML}")

    render_json(updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

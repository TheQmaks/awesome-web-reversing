#!/usr/bin/env python3
"""mirror.py — mirror every live catalog repo into an archive org.

The catalog's whole value is that it doesn't rot. This takes the next step:
keep a durable git mirror of every referenced repo, so an entry survives even
if its upstream is deleted or the account vanishes. A mirror (not a fork) is
used on purpose — it captures all branches/tags, can be refreshed forever, and
does not break when upstream disappears.

For each tool in data/verified.json with a repo and status != "missing", it
maintains a mirror at <MIRROR_ORG>/<owner>__<repo> and (re)writes MIRRORS.md.

Environment:
    MIRROR_ORG    target GitHub org (required)
    MIRROR_TOKEN  PAT that can create repos in the org and push (required in CI)
                  Locally, falls back to `gh auth token`.

If MIRROR_ORG or a usable token is absent, the script prints a notice and
exits 0 (so the scheduled workflow is a no-op until the org is configured).
"""
from __future__ import annotations

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
VERIFIED_JSON = ROOT / "data" / "verified.json"
MIRRORS_MD = ROOT / "MIRRORS.md"

ORG = os.environ.get("MIRROR_ORG", "").strip()
TOKEN = os.environ.get("MIRROR_TOKEN", "").strip()
if not TOKEN:
    got = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
    TOKEN = got.stdout.strip() if got.returncode == 0 else ""


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    env = {**os.environ, "GH_TOKEN": TOKEN} if TOKEN else os.environ
    return subprocess.run(cmd, text=True, capture_output=True, env=env, **kw)


def ensure_repo(name: str, desc: str) -> None:
    if run(["gh", "repo", "view", f"{ORG}/{name}"]).returncode != 0:
        run(["gh", "repo", "create", f"{ORG}/{name}", "--public", "--description", desc])


def mirror_one(owner: str, repo: str) -> str:
    name = f"{owner}__{repo}"
    src = f"https://github.com/{owner}/{repo}.git"
    dst = f"https://x-access-token:{TOKEN}@github.com/{ORG}/{name}.git"
    ensure_repo(name, f"Mirror of {owner}/{repo} — awesome-web-reversing archive")
    tmp = tempfile.mkdtemp()
    try:
        bare = os.path.join(tmp, "m.git")
        if run(["git", "clone", "--mirror", src, bare]).returncode != 0:
            return "clone-failed"
        # Push only branches and tags. `push --mirror` also tries to push
        # GitHub's read-only refs/pull/* hidden refs, which the remote rejects
        # ("deny updating a hidden ref"), failing the whole push even though
        # heads/tags went through. An explicit refspec avoids the hidden refs.
        p = run(["git", "-C", bare, "push", "--force", "--prune", dst,
                 "refs/heads/*:refs/heads/*", "refs/tags/*:refs/tags/*"])
        return "ok" if p.returncode == 0 else "push-failed"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def write_manifest(rows: list[tuple[str, str, str]]) -> None:
    lines = [
        "# Mirror manifest",
        "",
        f"Durable git mirrors of every live catalog entry, kept under the `{ORG}` org so",
        "an entry survives upstream deletion. Refreshed by `.github/workflows/mirror.yml`.",
        "Mirrors preserve upstream `LICENSE` and history verbatim — this is an archive, not a re-release.",
        "",
        "| Upstream | Mirror | Last mirror status |",
        "|---|---|---|",
    ]
    for upstream, mirror, status in sorted(rows):
        badge = {"ok": "✅", "clone-failed": "⚠️ clone", "push-failed": "⚠️ push"}.get(status, status)
        lines.append(f"| [{upstream}](https://github.com/{upstream}) | [{mirror}](https://github.com/{ORG}/{mirror}) | {badge} |")
    lines.append("")
    MIRRORS_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if not ORG or not TOKEN:
        print("MIRROR_ORG or token not configured; skipping (no-op).")
        return 0

    data = json.loads(VERIFIED_JSON.read_text(encoding="utf-8"))
    seen: set[str] = set()
    rows: list[tuple[str, str, str]] = []
    for t in data["tools"]:
        repo = t.get("repo")
        if not repo or t.get("status") == "missing" or repo in seen:
            continue
        seen.add(repo)
        owner, _, name = repo.partition("/")
        status = mirror_one(owner, name)
        marker = {"ok": "🟢", "clone-failed": "🔴", "push-failed": "🔴"}.get(status, "?")
        print(f"  {marker} {repo} -> {ORG}/{owner}__{name}: {status}")
        rows.append((repo, f"{owner}__{name}", status))

    write_manifest(rows)
    ok = sum(1 for _, _, s in rows if s == "ok")
    print(f"\nMirrored {ok}/{len(rows)} repos into {ORG}. Wrote {MIRRORS_MD}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

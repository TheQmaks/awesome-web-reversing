# Workflows

Layered recipes for reverse-engineering modern defended SPAs. Apply in order. Skip layers you don't need.

The central thesis: **fight the delivery, not the runtime.** Most anti-debug and anti-hook tricks assume the attacker is monkey-patching at runtime. If you rewrite the response before it parses, you sidestep an entire class of detections (Function.prototype.toString integrity, stored-original references, bootstrap timing traps).

---

## Layer 0 — Reconnaissance

Before touching any tool, answer these (and use the **Layer 0** tools in [catalog.md](catalog.md) to automate):

- **What stack?** Wappalyzer / source inspection — React, Vue, Angular, Next.js, Remix, Svelte? Helps you pick framework-aware tools (Layer 5).
- **What anti-bot?** Use `scrapfly/Antibot-Detector` (browser extension / script) to auto-identify Cloudflare, DataDome, Akamai, PerimeterX, etc. with confidence scores. Or by cookie patterns:
  - `__cf_bm`, `cf_clearance`, `__cflb` → Cloudflare
  - `datadome`, `_dd_*` → DataDome
  - `_abck`, `bm_sz`, `ak_bmsc` → Akamai
  - `_px*`, `pxhd` → PerimeterX/HUMAN
  - `kpsdk-*` → Kasada
  - `incap_ses_*`, `visid_incap_*` → Imperva Incapsula
- **Bundle size & shape?** Curl the main JS file. > 5 MB = obfuscated bundle territory; expect VM obfuscation. < 1 MB = likely standard webpack, deobfuscation will work cleanly.
- **WASM present?** `curl -sI` for `.wasm`. Modern anti-bot increasingly puts proof-of-work and challenge eval in WASM.
- **Source maps leaked?** Try `<bundle.js>.map`. Sometimes accidentally deployed to prod. Instant win if present.
- **What does your client present?** Before designing bypass, know your own fingerprint. Submit your scraping setup to `creepjs.com` (or `read-tls-client-hello` self-hosted) — it'll list every signal that's inconsistent ("lies") that real defenders also check.
- **What's the empirical bypass rate of each stealth stack against this vendor?** Consult `techinz/browsers-benchmark` for current numbers per (stack × vendor) pair — saves you weeks of "is my Camoufox config broken or is this just unbypassable?"

### TLS / HTTP fingerprint impersonation (Layer 1.5)

Often missed: modern WAFs (Cloudflare, Akamai, DataDome) check the TLS ClientHello and HTTP/2 frame ordering *before* a single byte of JS runs. A Python `requests`-based scraper presents `Python-urllib`'s JA3 signature, gets immediately flagged. Even Playwright's underlying browser sends an authentic JA3, but if you proxy it through `curl_cffi` or `requests`, you lose that.

**Recipe — Python scraper impersonating Chrome's full TLS+H2 fingerprint:**

```python
from curl_cffi import requests

# impersonate=chrome131 picks Chrome 131's JA3, JA4, and Akamai H2 fingerprint
resp = requests.get(
    "https://protected.example.com/api/data",
    impersonate="chrome131",
    headers={"Accept-Language": "en-US,en;q=0.9"},
)
```

If you need Go or Rust: `bogdanfinn/tls-client` (Go) and `0x676e67/wreq` (Rust). For HTTP/3 / QUIC: `sardanioss/httpcloak`.

For *defenders* (or RE researchers building a fingerprint mirror): `wi1dcard/fingerproxy` or `phuslu/nginx-ssl-fingerprint` sit in front of a backend and log the actual JA3/JA4/H2 of every incoming client — lets you see what your scraper presents in real time.

---

## Layer 1 — Transport rewriting (the strongest move)

**When:** Always. This is your foundation. Patch the JS before V8 parses it.

**Why first:** Anti-debug tricks (`debugger;` loops, `Function.prototype.constructor("debugger")`, timing detection) only execute if the offending code actually runs. If you delete it from the response, none of it matters.

**Tools:** `mitmproxy` (scriptable), `Proxyman` (GUI on macOS), `Caido` (Rust, modern UX), `HTTP Toolkit` (low-friction), `Burp Suite` (security-heavy work). For lightweight browser-only override: `Resource Override` extension or `Requestly`.

**Recipe:**

```python
# mitmproxy addon — strip anti-debug, beautify, log
import re

def response(flow):
    url = flow.request.pretty_url
    if "main." in url and url.endswith(".js"):
        body = flow.response.text
        # Neutralize naive debugger traps
        body = re.sub(r"\bdebugger\s*;", "void 0;", body)
        # Optional: replace Function constructor calls that synthesize "debugger"
        body = re.sub(
            r"Function\.prototype\.constructor\s*\(\s*['\"]debugger['\"]\s*\)",
            "(function(){})", body)
        flow.response.text = body
```

```bash
mitmdump -s strip_debugger.py --listen-port 8080
# Then point browser at 127.0.0.1:8080 with mitmproxy CA installed
```

**Gotchas:**
- TLS pinning in mobile / Electron clients defeats CA install — escalate to Frida (Layer 6).
- HSTS-preloaded domains require Chrome flag `--ignore-certificate-errors` or a separate profile.
- Some bundles split into hundreds of chunks; match by URL pattern, not filename.

---

## Layer 2 — Pre-bootstrap instrumentation

**When:** You need to observe runtime values (request bodies, cookie writes, crypto calls) but the page captures originals (`const origFetch = fetch;`) before you can patch.

**Why before live DevTools:** Late monkey-patching loses to `Function.prototype.toString` integrity checks and stored-original-reference defenses. Pre-bootstrap injection runs before any site script — your wrappers ARE the originals as far as the site is concerned.

**Tools:** `Playwright.addInitScript` (multi-browser), `Puppeteer.evaluateOnNewDocument` (Chromium), `Tampermonkey @run-at document-start` (no automation needed). For anti-detect: `Camoufox` (Firefox-fork, C++ patches) or `Patchright` (Playwright stealth fork).

**Recipe — hook fetch + log to file:**

```javascript
// init.js — injected via addInitScript
const origFetch = window.fetch;
const logs = [];
window.fetch = function(...args) {
    const entry = { url: args[0], opts: args[1], stack: new Error().stack };
    logs.push(entry);
    window.__fetchLogs = logs;  // accessible from CDP later
    return origFetch.apply(this, args);
};
// Spoof toString so detection passes
window.fetch.toString = () => "function fetch() { [native code] }";
window.fetch.toString.toString = () => "function toString() { [native code] }";
```

```javascript
// driver.js — Playwright
const { chromium } = require('playwright');
(async () => {
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext();
    await context.addInitScript({ path: './init.js' });
    const page = await context.newPage();
    await page.goto('https://target.example');
    const logs = await page.evaluate(() => window.__fetchLogs);
    console.log(JSON.stringify(logs, null, 2));
})();
```

**Gotchas:**
- `toString` spoofing must also cover `.toString.toString()` (some checks recurse).
- Don't forget `Function.prototype.constructor` — `(function(){}).constructor("...")` builds new functions at runtime, your hook on `Function` constructor itself must be installed before the prototype is touched.
- For `XMLHttpRequest`, hook `.prototype.send` and `.prototype.open` — both carry payload info.

---

## Layer 3 — Mass CDP instrumentation

**When:** You need to enumerate every script, hit every function, or build an execution trace. Live DevTools can't do this at scale.

**Tools:** `chrome-remote-interface` (raw CDP), `chromedp` (Go), `wirebrowser` (CDP-Frida with Origin Trace). Playwright/Puppeteer also expose `newCDPSession()`.

**Recipe — log every parsed script and inject coverage instrumentation:**

```javascript
const CDP = require('chrome-remote-interface');

(async () => {
    const client = await CDP();
    const { Debugger, Runtime, Profiler } = client;
    await Debugger.enable();
    await Runtime.enable();
    await Profiler.enable();
    await Profiler.startPreciseCoverage({ callCount: true, detailed: true });

    Debugger.on('scriptParsed', async (params) => {
        if (params.url.includes('anti-bot.example')) {
            console.log(`Tracking ${params.url} (${params.scriptId})`);
            // Set logpoint at every function entry — discover from script source
            const { scriptSource } = await Debugger.getScriptSource({
                scriptId: params.scriptId,
            });
            // Parse to find function locations (use @babel/parser)
            // Then Debugger.setBreakpointByUrl with condition that logs and continues
        }
    });

    Debugger.on('paused', async ({ callFrames }) => {
        console.log('Paused at:', callFrames[0].location);
        await Debugger.resume();  // breakpoint as logpoint
    });

    await client.Page.navigate({ url: 'https://target.example' });
})();
```

**Why this beats DevTools:**
- Enumerate thousands of `eval`-spawned scripts that the Sources panel can't index.
- Survive DevTools-size detection (no UI = no `outerWidth - innerWidth` diff).
- Programmatic — can run for hours unattended.

---

## Layer 4 — Static deobfuscation pipeline

**When:** You've gotten transport rewriting working, hooks are running, but the code is still unreadable. You need to convert minified/obfuscated bundles into something you can grep and reason about.

**Pipeline:**

```bash
# 1. First pass — handle obfuscator.io family + webpack unbundle
npx webcrack input/bundle.js -o output/

# 2. Targeted pass — Magecart/PerimeterX-style transforms
npx restringer output/main.js -o output/main.cleaned.js

# 3. Final pass — clean up residual obfuscator.io artifacts
npx obfuscator-io-deobfuscator output/main.cleaned.js

# 4. Custom AST codemods for site-specific patterns
node my-codemods/inline-string-decryptor.js output/main.cleaned.js

# 5. Structural search to find candidates
ast-grep --pattern 'crypto.subtle.$METHOD($$$)' output/

# 6. LLM-rename for readability (optional)
npx humanify openai output/main.cleaned.js --output output/main.readable.js
```

**What does NOT work:**
- Regex find-replace on minified code — scope collisions destroy semantics.
- Pure LLM "throw bundle in chat" — hallucinations break execution equivalence (see arxiv 2506.20170).
- `de4js` / `JStillery` on modern obfuscation — they're textbook-packer era tools.

**For VM-obfuscated bundles** (Cloudflare `bm-vm-*`, Kasada KPSDK, Akamai newer): static deobfuscation will fail. You must reverse the interpreter itself, then write a custom devirtualizer. Plan for weeks, not hours.

---

## Layer 5 — Framework-aware shortcuts

**When:** The app is built on React/Vue/Angular/Redux. Often the fastest path to understanding is the framework's own dev surface, not the JS source.

**Tools:** `React DevTools`, `Redux DevTools` (time-travel actions!), `Vue DevTools`, `Angular DevTools`. Plus bundle analyzers: `webpack-bundle-analyzer`, `source-map-explorer` (if sourcemaps exist).

**Use cases:**
- "Which component renders this UI?" → React DevTools selector → name + props + hooks state.
- "When did this token enter Redux state?" → Redux DevTools action diff → exact action + payload.
- "Where's the vendor code vs the custom code?" → bundle-analyzer treemap → narrow search radius 50×.

**Production hardening:** Angular DevTools doesn't work on prod-optimized Angular builds (debug features stripped). React DevTools usually still works because component metadata survives minification unless explicitly stripped.

---

## Layer 6 — Memory & heap forensics

**When:** Secrets live in `WeakMap` (unenumerable by design), in closures (no outer reference), or in objects you can't find by `console.dir(window)`.

**Tools:** `MemLab` (scenario-driven snapshots with retainer analysis), DevTools Heap Snapshot diffing, `wirebrowser` Live Object Search.

**Recipe — find where a JWT token gets stored:**

```javascript
// MemLab scenario
module.exports = {
    url: () => 'https://target.example',
    action: async (page) => {
        await page.click('button[type=submit]');  // trigger login
        await page.waitForTimeout(2000);
    },
    back: async (page) => { /* navigate away to release transient refs */ },
    leakFilter: (node, snapshot) => {
        return node.type === 'string' && node.name && node.name.startsWith('eyJ');
    },
};
```

```bash
memlab run --scenario jwt-scenario.js
memlab find-leaks
memlab trace --node-id <id>  # see retainer chain
```

**WeakMap secret extraction trick:**

```javascript
// Hook WeakMap.set before any site code, mirror keys to a global Set
const origSet = WeakMap.prototype.set;
const mirror = new Set();
WeakMap.prototype.set = function(key, value) {
    mirror.add({ key, value });
    return origSet.call(this, key, value);
};
window.__weakmapMirror = mirror;
```

Inject via Layer 2. Now keys that should be GC-invisible are dumpable.

---

## Layer 7 — Native escalation

**When:** Target is Electron, NW.js, React Native (Hermes), Android WebView, in-app browser. Or browser code calls native crypto that isn't exposed to JS.

**Tools:** `Frida` + `frida-node` for scripting, `Objection` for mobile shells, `r2frida` for hybrid with radare2, `LIEF` for binary patching.

**Electron pipeline:**

```bash
# 1. Extract asar
npx @electron/asar extract /Applications/App.app/Contents/Resources/app.asar ./extracted/

# 2. Detect bytecode
file extracted/main.jsc   # "V8 bytecode" → need V8-version-matched decompiler

# 3. Check for asar integrity (Electron 30+)
plutil -p /Applications/App.app/Contents/Info.plist | grep ElectronAsarIntegrity
# If present, you'll need to patch the binary (LIEF) or modify Info.plist to bypass.

# 4. If asarmor-protected, fix invalid header offsets manually
# See https://www.anthok.com/posts/asarmor-deobfuscation/

# 5. Once unpacked, treat extracted/ as a regular webpack project — back to Layer 4
```

**React Native Hermes:**

```bash
# 1. Pull APK + extract bundle
apktool d app.apk
file app/assets/index.android.bundle   # confirm Hermes

# 2. Disassemble
hbcdump app/assets/index.android.bundle -disassemble > bundle.hasm

# 3. Decompile to pseudo-JS
hermes-dec hbc-decompiler app/assets/index.android.bundle -o bundle.js
# Or, with better control-flow reconstruction:
hermes-decomp bundle decompile app/assets/index.android.bundle

# 4. For runtime instrumentation, use heresy with Frida
frida -U -l heresy/agent.js -f com.target.app
```

---

## Layer 8 — Time-travel / replay (last resort or paranoia)

**When:** The bug is async-burst-driven (SSE/WebSocket flood), nondeterministic, or you need to study a race condition. Or you need an audit trail of "exactly what happened" for later analysis.

**Tools:** `Replay.io` (browser, hosted+OSS), `rr` (Linux native, for Electron/Node), `Pernosco` (cloud omniscient on top of rr).

**When NOT to use:** Routine reverse work. Recording overhead, file size, and platform constraints make this overkill for "I want to read this function."

---

## Decision tree (when stuck)

```
Anti-debug crashes the page → Layer 1 (transport rewrite)
Hooks don't see early calls → Layer 2 (pre-bootstrap)
Code is unreadable          → Layer 4 (static pipeline) + Layer 5 (framework)
Need value of runtime var   → Layer 3 (CDP) or Layer 2 (hook + log)
Secret is in memory only    → Layer 6 (heap forensics)
Logic seems to be missing   → check WASM (Layer 0 confirmed?) or Electron asar (Layer 7)
Async bug, nondeterministic → Layer 8 (replay)
```

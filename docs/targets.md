# Target-Specific Playbooks

Concrete recipes for the most common defended-target classes encountered in 2024-2026. Each playbook assumes you've read [workflows.md](workflows.md) and understands the layered approach.

---

## Cloudflare (Bot Management, Turnstile, JS Challenge)

**Identifiers:** `__cf_bm`, `cf_clearance`, `__cflb` cookies. `challenges.cloudflare.com` requests. Bundles named `challenge-platform/h/*/orchestrate/managed/v1` or `bm-vm-*`.

**Two regimes:**

1. **Classic JS challenge** (older, becoming rare) — solvable with AST deobfuscation. Look for the `_cf_chl_opt` global, trace the form submission.
2. **VM-obfuscated** (current default, 2024+) — JS compiles to bytecode for a custom interpreter. Static deobfuscation **will fail**. You must reverse the VM dispatcher and write a devirtualizer.

**Approach for VM-obfuscated bundles:**

```bash
# 1. Capture the challenge bundle
mitmdump -w cf.flow -s '
def response(flow):
    if "challenge-platform" in flow.request.pretty_url:
        with open(f"cf_{flow.request.path.split(\"/\")[-1]}.js", "w") as f:
            f.write(flow.response.text)
'

# 2. Identify the VM dispatcher — typically a giant switch-case or function table
ast-grep --pattern 'switch ($X) { case $$$ }' cf_*.js | head -40

# 3. Map opcodes by hand or with LLM assistance
# Look for: opcode handler array, instruction pointer increment, operand fetch pattern
```

**Tools that work:** `mitmproxy` for capture, `Camoufox`/`Patchright` for evading the upstream fingerprint check, manual VM reversal. **Tools that don't work:** `puppeteer-extra-stealth` (detected since ~2024), generic deobfuscators.

**Useful references:**
- [0xdevalias "Bypassing Cloudflare, Akamai, etc."](https://gist.github.com/0xdevalias/b34feb567bd50b37161293694066dd53)
- [Scrapfly Cloudflare bypass posts](https://scrapfly.io/blog/) — outsider perspective on what current Cloudflare versions check.

---

## DataDome

**Identifiers:** `datadome` cookie, `js.datadome.co` script source, `_dd_*` cookies in some configs.

**Architecture:**
- Per-customer ML models — fingerprints are evaluated against site-specific baselines. What works on site A may fail on site B.
- Heavy use of: canvas fingerprinting, WebGL fingerprinting, navigator probes, timing checks, mouse-movement entropy.
- Increasingly puts critical logic in obfuscated workers and uses `OffscreenCanvas` for fingerprint compute.

**Approach:**

1. **Don't bypass the script — strip it.** DataDome is loaded as a third-party JS. Block its load entirely if the site degrades gracefully, or feed it a recorded valid response.
2. **If you need it to run:** Capture a "known good" `datadome` cookie from a real session via residential proxy. Replay it. DataDome cookies typically last hours; a small pool rotates well.
3. **Reverse the fingerprint computation only if you must.** It's possible but expensive — see [HUMAN Security's blog on defeating obfuscation](https://www.humansecurity.com/tech-engineering-blog/defeating-javascript-obfuscation/) (ironic, since they ARE PerimeterX/DataDome's parent).

**Tools that work:** `Restringer` (built by ex-PerimeterX engineers, specifically targets these transforms), `mitmproxy` for cookie capture/replay, residential proxies for cookie acquisition.

**Anti-patterns:**
- Trying to solve the JS challenge programmatically each time — DataDome detects sequential cookie generation patterns.
- Relying on a single IP — DataDome's velocity checks are tight.

---

## Akamai Bot Manager

**Identifiers:** `_abck`, `bm_sz`, `ak_bmsc` cookies. `sensor_data` POST to `/_bm/_data` or similar paths.

**Approach:**
- The `sensor_data` payload is the core challenge — a stringified collection of fingerprints, timings, and mouse/touch entropy.
- Reversing the `sensor_data` generator is the standard goal. It's heavily obfuscated but is plain JS (not VM-obfuscated as of late 2025).
- Use `Webcrack` first pass + manual AST work to map the data collection structure.

**Resources:**
- [Jarrod Overson's older but still-relevant Akamai writeups](https://jarrodoverson.com/blog/) (he worked at Shape Security, Akamai-adjacent).
- Search GitHub for `sensor_data` recently-updated repos — there's an active community of researchers publishing partial reproductions.

---

## PerimeterX / HUMAN Security

**Identifiers:** `_px*`, `pxhd`, `pxvid` cookies. Inline script with PXxxxx app ID.

**Status (2024-2026):** Acquired by HUMAN. The defensive techniques and the offensive deobfuscators (Restringer, obfuscation-detector) come from the same engineering tradition.

**Approach:**
- Restringer was literally built to deobfuscate PerimeterX's own JS for analysis. It still works on PX-style code patterns.
- The `_px` cookies are HMAC-tagged; tampering is detected. Capture + replay > generation.

---

## Kasada KPSDK

**Identifiers:** `kpsdk-*` cookies, `kpsdk.com` requests, `KPSDK` global.

**Architecture:**
- Proof-of-work + behavioral biometrics.
- Critical compute is in **WebAssembly**. JS layer alone is insufficient to understand it.

**Approach:**

```bash
# 1. Extract the WASM module
mitmdump -s 'def response(f): "kpsdk" in f.request.pretty_url and open("kpsdk.wasm","wb").write(f.response.content)'

# 2. Disassemble
wasm2wat kpsdk.wasm > kpsdk.wat
wasm-decompile kpsdk.wasm > kpsdk.dec  # higher-level pseudocode

# 3. Imports tell you what JS surfaces it calls
wasm-objdump -j Import -x kpsdk.wasm

# 4. Look for the PoW loop — typically a tight hash function pattern
```

**Tools:** WABT, `wasm-decompile`, `Cetus` (in-browser WASM cheat engine for live memory inspection), `twiggy` for bloat analysis.

---

## ChatGPT-style SSE-based JS clients

**Identifiers:** Response `content-type: text/event-stream`, `event: delta_encoding` markers, `.dat` extensions in some capture tools.

**Approach (from your gptclient-go session, May 12 2026):**

1. **Capture protocol shape:**
   ```bash
   mitmdump --listen-port 8080 --save-stream-file chatgpt.flow
   # Filter to /backend-anon/conversation in real time
   ```

2. **Decode the SSE stream:** Server-Sent Events use line-delimited JSON deltas after `event:` lines. Parse with stateful reader:
   ```python
   def parse_sse(stream):
       event, data = None, []
       for line in stream:
           if line.startswith(b"event: "):
               event = line[7:].strip()
           elif line.startswith(b"data: "):
               data.append(line[6:])
           elif line == b"\n":
               yield event, b"".join(data)
               event, data = None, []
   ```

3. **Reverse the cloak/stealth layer:** ChatGPT's anonymous endpoints validate fingerprints. Use Camoufox or a properly-patched CloakBrowser. Key surfaces:
   - `navigator.webdriver` (must be undefined or false)
   - `navigator.plugins.length` (real browsers have ≥3)
   - `window.chrome` (must exist as object, not undefined)
   - User-Agent without `HeadlessChrome`
   - `/sentinel/chat-requirements/prepare` returns 200, not 4xx

4. **Find the tool invocation pattern:** ChatGPT search uses `SonicBrowserTool` invoked via the tool-calling mechanism. The `is_search` field is often null even when search runs — don't filter on it. Match on `tool_name == "SonicBrowserTool"` or successful 153KB+ responses (vs 34-byte errors).

---

## Electron desktop apps

**Identifiers:** `Resources/app.asar` in app bundle. `process.versions.electron` in console.

**Pipeline:**

```bash
# 1. Locate asar
# macOS: /Applications/<App>.app/Contents/Resources/app.asar
# Windows: %APPDATA%\<App>\resources\app.asar or in app install dir

# 2. Check integrity (Electron 30+)
plutil -p Info.plist | grep -A 10 ElectronAsarIntegrity

# 3. Extract
npx @electron/asar extract app.asar extracted/

# 4. If extraction fails (asarmor):
# Read https://www.anthok.com/posts/asarmor-deobfuscation/ for header offset repair

# 5. If .jsc files present (V8 bytecode):
electron --version  # note Electron version → V8 version
# Use View8 or a version-matched V8 d8 build to decompile
d8 --print-bytecode some.jsc

# 6. Once you have readable JS, back to Layer 4 pipeline
```

**Bypass DevTools blocked in production app:**

```bash
# Method A: --inspect-brk on relaunch
ELECTRON_RUN_AS_NODE=1 ./Contents/MacOS/App --inspect-brk=9229
# Then chrome://inspect to attach

# Method B: patch the binary to enable DevTools
# Use LIEF to flip flags or inject early script in main process
```

---

## React Native / Hermes mobile apps

**Identifiers:** `index.android.bundle` or `index.ios.bundle` in assets. `file` command says `Hermes JavaScript bytecode, version XX`.

**Pipeline:**

```bash
# 1. Extract APK
apktool d -o extracted/ app.apk

# 2. Confirm Hermes vs JSC
file extracted/assets/index.android.bundle
# "Hermes JavaScript bytecode, version 96" → use hermes-dec / hermes-decomp
# "JavaScript source" or no Hermes header → standard bundle, use Layer 4 pipeline

# 3. Disassemble
hbcdump bundle.hbc -disassemble -O disasm.hasm

# 4. Decompile
hermes-dec hbc-decompiler bundle.hbc -o decompiled.js
# Or better:
hermes-decomp bundle decompile bundle.hbc -o decompiled/

# 5. For round-trip patching:
hbctool disasm bundle.hbc -o disasm/
# edit disasm/*.hasm
hbctool asm disasm/ -o patched.hbc
# Repack APK with patched.hbc

# 6. Runtime hooks via Frida + heresy
frida -U -l agent.js -f com.target.app --no-pause
```

**Critical:** Hermes bytecode format is version-specific. Mismatched tools won't work. Check `bundle.hbc` header (`HBCMagic` + version int) and use the matching tool version.

---

## Adversary-class summary table

| Vendor | Static deobfuscation works? | WASM? | Behavioral ML? | Recommended approach |
|--------|---------------------------|-------|----------------|---------------------|
| Cloudflare (current) | Partial — VM obfuscation breaks it | Sometimes | Yes | Capture + replay + Camoufox; full reverse is weeks |
| DataDome | Yes (Restringer) | No (yet) | Yes, per-customer | Capture cookie + residential proxies |
| Akamai | Yes (manual AST) | No | Yes | Reverse `sensor_data` generator |
| PerimeterX / HUMAN | Yes (Restringer) | No | Yes | Restringer + capture |
| Kasada | JS yes, WASM no | Yes, critical | Yes | Must reverse WASM PoW |
| Imperva Incapsula | Mostly | No | Limited | Standard pipeline |
| Cloudflare Turnstile | Partial | Yes | Yes | Treat as Cloudflare full |

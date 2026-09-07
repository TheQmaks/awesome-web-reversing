# Tool Catalog

_Generated 2026-09-07T11:27:12.786797+00:00 from `data/verified.json`. 99 entries._

**Status legend:** 🟢 active (push < 6mo) · 🟡 stale (6-18mo) · 🔴 dead (>18mo) · ⚫ missing/hallucinated · 🗄 GitHub-archived (additional flag)

Catalog is organized by workflow layer (see [workflows.md](workflows.md)). Within each layer, tools are sorted by star count descending.

---

## Layer 0 — Anti-bot reconnaissance / fingerprint testbeds

### 🟢 creepjs

- **Repo:** [abrahamjuliot/creepjs](https://github.com/abrahamjuliot/creepjs) · ⭐ 2,500 · TypeScript · MIT
- **Last push:** 2026-06-11 · **Status:** `active`
- **When to use:** Run your stealth browser against creepjs.com to find which spoofed APIs are still inconsistent (lies) before the real WAF catches them.
- **Upstream:** Creepy device and browser fingerprinting
- **Why included:** The canonical lie-detection testbed for anti-detect setups; pairs with fingerprint-suite/Camoufox for closed-loop tuning.

### 🟢 scrapfly Antibot-Detector

- **Repo:** [scrapfly/Antibot-Detector](https://github.com/scrapfly/Antibot-Detector) · ⭐ 431 · JavaScript · NOASSERTION
- **Last push:** 2026-06-18 · **Status:** `active`
- **When to use:** Run as a first-pass recon step on a defended SPA to know exactly which vendor(s) you're up against before picking your bypass strategy.
- **Upstream:** Real-time detection of anti-bot systems, CAPTCHAs & fingerprinting techniques. Identifies Cloudflare, Akamai, DataDome, reCAPTCHA, hCaptcha, Shape Security & more with confidence scoring and advanced capture tools.
- **Why included:** Recon/fingerprinting category is currently empty; this is the de-facto "which WAF is this?" tool of 2025.

---

## Layer 0 — Bypass benchmarks (empirical)

### 🟢 browsers-benchmark

- **Repo:** [techinz/browsers-benchmark](https://github.com/techinz/browsers-benchmark) · ⭐ 383 · Python · MIT
- **Last push:** 2026-09-01 · **Status:** `active`
- **When to use:** Consult before picking a stealth stack — gives empirical bypass rates per vendor rather than relying on vendor claims.
- **Upstream:** Browser automation engine benchmark - Test bypass rates, performance & stealth against Cloudflare, DataDome, reCAPTCHA, Kasada, Imperva, Akamai, PerimeterX  and other bot detection systems. Find the best browser for scraping.
- **Why included:** First-of-its-kind public benchmark; gives objective evidence for the bypass landscape evolving 2024-2026.

---

## Layer 0 — Research notes & cookbooks

### 🟢 niespodd browser-fingerprinting

- **Repo:** [niespodd/browser-fingerprinting](https://github.com/niespodd/browser-fingerprinting) · ⭐ 5,131 · JavaScript · None
- **Last push:** 2026-07-27 · **Status:** `active`
- **When to use:** Read alongside source-code RE — it consolidates which signals each vendor checks (Canvas, WebGL, Audio, font, navigator) and how to spoof them coherently.
- **Upstream:** Analysis of Bot Protection systems with available countermeasures 🚿. How to defeat anti-bot system 👻 and get around browser fingerprinting scripts 🕵️‍♂️ when scraping the web?
- **Why included:** The single most-cited public knowledge base for FP defense; essential companion to any RE list.

---

## Layer 1 — Transport rewriting (MITM)

### 🟢 mitmproxy

- **Repo:** [mitmproxy/mitmproxy](https://github.com/mitmproxy/mitmproxy) · ⭐ 44,941 · Python · MIT
- **Last push:** 2026-09-01 · **Status:** `active`
- **When to use:** Intercept and rewrite TLS-encrypted XHR/fetch traffic from a CLI with scriptable Python addons.
- **Upstream:** An interactive TLS-capable intercepting HTTP proxy for penetration testers and software developers.
- **Latest release:** v12.2.3 (2026-05-12)

### 🟡 HTTP Toolkit

- **Repo:** [httptoolkit/httptoolkit](https://github.com/httptoolkit/httptoolkit) · ⭐ 3,622 · — · None
- **Last push:** 2026-02-04 · **Status:** `stale`
- **When to use:** One-click intercept of a specific Chrome/Node/Electron process with auto-injected CA trust.
- **Upstream:** HTTP Toolkit is a beautiful & open-source tool for debugging, testing and building with HTTP(S) on Windows, Linux & Mac  :tada:  Open an issue here to give feedback or ask for help.

### 🟢 Caido

- **Repo:** [caido/caido](https://github.com/caido/caido) · ⭐ 2,578 · Shell · None
- **Last push:** 2026-09-04 · **Status:** `active`
- **When to use:** Modern Burp-style web proxy with a lighter footprint when auditing single-page-app API traffic.
- **Upstream:** 🚀 Caido releases, wiki and roadmap
- **Latest release:** v0.56.2 (2026-05-16)

---

## Layer 1 — TLS / JA3 / JA4 / HTTP fingerprint impersonation

### 🟢 curl_cffi

- **Repo:** [lexiforest/curl_cffi](https://github.com/lexiforest/curl_cffi) · ⭐ 6,457 · Python · MIT
- **Last push:** 2026-09-04 · **Status:** `active`
- **When to use:** Use as a drop-in `requests` replacement when the target WAF (Cloudflare, Akamai, DataDome) fingerprints TLS/HTTP2 and a plain Python client gets blocked.
- **Upstream:** Python binding for curl-impersonate fork via cffi. A http client that can impersonate browser tls/ja3/http2 fingerprints.
- **Why included:** The Python ecosystem's default JA3/JA4/H2 impersonation client; conspicuously missing from the curated list.

### 🟢 burp-awesome-tls

- **Repo:** [sleeyax/burp-awesome-tls](https://github.com/sleeyax/burp-awesome-tls) · ⭐ 1,888 · Java · GPL-3.0
- **Last push:** 2026-09-02 · **Status:** `active`
- **When to use:** Use during manual app testing when the target WAF rejects Burp's native Java TLS handshake and you need JA3-correct request replay.
- **Upstream:** Burp extension to evade TLS fingerprinting. Bypass WAF, spoof any browser.
- **Why included:** Bridges Burp into the TLS-impersonation ecosystem — important for hands-on RE workflows; not currently listed.

### 🟢 tls-client

- **Repo:** [bogdanfinn/tls-client](https://github.com/bogdanfinn/tls-client) · ⭐ 1,833 · Go · BSD-4-Clause
- **Last push:** 2026-09-04 · **Status:** `active`
- **When to use:** Pick when building Go scrapers/proxies that need per-request switching between Chrome/Firefox/Safari TLS profiles to defeat JA3-based WAFs.
- **Upstream:** net/http.Client like HTTP Client with options to select specific client TLS Fingerprints to use for requests.
- **Why included:** The reference Go-side JA3 spoofing library, paired with cclient/utls — fills the Go gap in the TLS-impersonation category.

### 🟢 httpcloak

- **Repo:** [sardanioss/httpcloak](https://github.com/sardanioss/httpcloak) · ⭐ 1,283 · Go · MIT
- **Last push:** 2026-09-02 · **Status:** `active`
- **When to use:** Pick when you also need HTTP/3 (QUIC) impersonation alongside JA3/JA4 — most peers don't cover H3 yet.
- **Upstream:** Go HTTP client with browser-identical TLS/HTTP2 fingerprinting. Bypass bot detection by perfectly mimicking Chrome, Firefox, and Safari at the cryptographic level (JA3/JA4, Akamai fingerprint, header order). Supports HTTP/1.1, HTTP/2, HTTP/3, sessions, cookies, and proxies.
- **Why included:** One of the few impersonation libraries with HTTP/3 support, addressing the "QUIC fingerprint" tail of the gap list.

### 🟢 wreq

- **Repo:** [0x676e67/wreq](https://github.com/0x676e67/wreq) · ⭐ 1,017 · Rust · Apache-2.0
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Use for high-throughput Rust scrapers or proxy services that must impersonate browser fingerprints at the cryptographic level.
- **Upstream:** An ergonomic, privacy-aware Rust HTTP Client
- **Why included:** The current Rust-side impersonation client (after rquest was deprecated); covers the Rust gap and is actively maintained.

### 🟡 PortSwigger bypass-bot-detection

- **Repo:** [PortSwigger/bypass-bot-detection](https://github.com/PortSwigger/bypass-bot-detection) · ⭐ 500 · Java · Apache-2.0
- **Last push:** 2025-09-09 · **Status:** `stale`
- **When to use:** Pair with Burp when you need a lightweight, in-suite JA3 mutator without standing up an external proxy.
- **Upstream:** Burp Suite extension that mutates ciphers to bypass TLS-fingerprint based bot detection
- **Why included:** Vendor-supported Burp extension covering the same gap with simpler ergonomics than burp-awesome-tls.

### 🟡 fingerproxy

- **Repo:** [wi1dcard/fingerproxy](https://github.com/wi1dcard/fingerproxy) · ⭐ 344 · Go · Apache-2.0
- **Last push:** 2025-05-25 · **Status:** `stale`
- **When to use:** Deploy when researching anti-bot detection logic — sit it in front of a backend to see exactly which JA3/JA4/H2 fingerprint your scraper presents.
- **Upstream:** Fingerproxy is an HTTPS reverse proxy. It creates JA3, JA4, Akamai HTTP2 fingerprints, and forwards to backend via HTTP request headers.
- **Why included:** Lets reverse-engineers build their own "fingerprint mirror" without commercial services like browserleaks.

### 🟢 nginx-ssl-fingerprint

- **Repo:** [phuslu/nginx-ssl-fingerprint](https://github.com/phuslu/nginx-ssl-fingerprint) · ⭐ 243 · C · BSD-2-Clause
- **Last push:** 2026-09-02 · **Status:** `active`
- **When to use:** Use when standing up a self-hosted test harness on nginx to capture realistic JA3/JA4/H2 of scrapers, mobile apps, and stealth browsers.
- **Upstream:** High performance  ja3 ja4 and http2 fingerprint for nginx.
- **Why included:** Nginx-side alternative to fingerproxy; common in research blogs but absent from the list.

### 🟢 read-tls-client-hello

- **Repo:** [httptoolkit/read-tls-client-hello](https://github.com/httptoolkit/read-tls-client-hello) · ⭐ 59 · TypeScript · Apache-2.0
- **Last push:** 2026-08-07 · **Status:** `active`
- **When to use:** Embed in a Node-based detection or research server when you need JA3/JA4 calculation without rebuilding nginx or running a Go proxy.
- **Upstream:** A pure-JS module to read TLS client hello data and calculate TLS fingerprints from an incoming socket connection.
- **Why included:** The only pure-JS JA3 calculator from a reputable maintainer (httptoolkit) — fills the Node-side gap.

---

## Layer 2/3 — Browser automation + pre-bootstrap injection

### 🟢 Playwright

- **Repo:** [microsoft/playwright](https://github.com/microsoft/playwright) · ⭐ 95,760 · TypeScript · Apache-2.0
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Cross-browser automation when you need built-in tracing, codegen, and request interception across Chromium/Firefox/WebKit from one API.
- **Upstream:** Playwright is a framework for Web Testing and Automation. It allows testing Chromium, Firefox and WebKit with a single API.
- **Latest release:** v1.60.0 (2026-05-11)

### 🟢 Puppeteer

- **Repo:** [puppeteer/puppeteer](https://github.com/puppeteer/puppeteer) · ⭐ 95,565 · TypeScript · Apache-2.0
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Node-only Chrome automation when you want the canonical CDP wrapper without Playwright's heavier test-runner stack.
- **Upstream:** JavaScript API for Chrome and Firefox
- **Latest release:** browsers-v3.0.2 (2026-05-15)

### 🟢 chromedp

- **Repo:** [chromedp/chromedp](https://github.com/chromedp/chromedp) · ⭐ 13,273 · Go · MIT
- **Last push:** 2026-07-14 · **Status:** `active`
- **When to use:** Driving Chrome from Go without a Node bridge, ideal for scrapers and CI tools built in Go.
- **Upstream:** A faster, simpler way to drive browsers supporting the Chrome DevTools Protocol.
- **Latest release:** v0.15.1 (2026-04-01)

---

## Layer 2 — Anti-detect browsers & stealth patches

### 🟢 Scrapling

- **Repo:** [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) · ⭐ 78,941 · Python · BSD-3-Clause
- **Last push:** 2026-09-04 · **Status:** `active`
- **When to use:** Reach for it when you need a Python-first scraping stack that survives Cloudflare/Turnstile and offers stealth fetcher + AsyncFetcher + PlayWrightFetcher in one library.
- **Upstream:** 🕷️ An adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl!
- **Why included:** Fills the "modern Python anti-bot scraper" slot post-undetected-chromedriver and was the de-facto successor in 2025-2026.

### 🟡 undetected-chromedriver

- **Repo:** [ultrafunkamsterdam/undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver) · ⭐ 12,826 · Python · GPL-3.0
- **Last push:** 2025-07-05 · **Status:** `stale`
- **When to use:** Bypassing bot mitigation from existing Selenium/Python code without rewriting to Playwright.
- **Upstream:** Custom Selenium Chromedriver | Zero-Config | Passes ALL bot mitigation systems (like Distil / Imperva/ Datadadome / CloudFlare IUAM)

### 🟢 Camoufox

- **Repo:** [daijro/camoufox](https://github.com/daijro/camoufox) · ⭐ 11,720 · C++ · MPL-2.0
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Anti-detect scraping when you need a real Firefox fork with C++-level fingerprint spoofing rather than JS patches.
- **Upstream:** 🦊 Anti-detect browser
- **Latest release:** v150.0.2-beta.25 (2026-05-11)

### 🟢 nodriver

- **Repo:** [ultrafunkamsterdam/nodriver](https://github.com/ultrafunkamsterdam/nodriver) · ⭐ 4,730 · Python · AGPL-3.0
- **Last push:** 2026-05-13 · **Status:** `active`
- **When to use:** Use when you need raw CDP-driven Chrome automation without webdriver leaks and minimal stack fingerprint to bypass modern WAFs.
- **Upstream:** Successor of Undetected-Chromedriver. Providing a blazing fast framework for web automation, webscraping, bots and any other creative ideas which are normally hindered by annoying anti bot systems like Captcha / CloudFlare / Imperva / hCaptcha
- **Why included:** The official post-UC framework — replaces undetected-chromedriver for 2024+ anti-bot work and is explicitly excluded from your "known" list.

### 🟢 Patchright

- **Repo:** [Kaliiiiiiiiii-Vinyzu/patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright) · ⭐ 4,376 · TypeScript · Apache-2.0
- **Last push:** 2026-09-04 · **Status:** `active`
- **When to use:** Drop-in undetected Playwright when you already have a Playwright codebase and need to bypass Cloudflare/Datadome.
- **Upstream:** Undetected version of the Playwright testing and automation library.
- **Latest release:** v1.59.1 (2026-04-12)

### 🟢 BotBrowser

- **Repo:** [botswin/BotBrowser](https://github.com/botswin/BotBrowser) · ⭐ 2,604 · TypeScript · MIT
- **Last push:** 2026-09-03 · **Status:** `active`
- **When to use:** Drop in when you need a single fortified browser binary that bypasses the full enterprise anti-bot vendor matrix without per-vendor stealth plugins.
- **Upstream:** Advanced Privacy Browser Core with Unified Fingerprint Defense: Cloudflare, Akamai, Kasada, Shape, DataDome, PerimeterX, hCaptcha, FunCaptcha, Imperva, reCAPTCHA, ThreatMetrix, Adscore
- **Why included:** A post-Camoufox option that targets a much broader vendor list and stays current — a key gap in the existing list.

### 🟡 rebrowser-patches

- **Repo:** [rebrowser/rebrowser-patches](https://github.com/rebrowser/rebrowser-patches) · ⭐ 1,424 · JavaScript · None
- **Last push:** 2025-05-09 · **Status:** `stale`
- **When to use:** Apply when you must keep using Puppeteer/Playwright (vs nodriver) but need to neutralize the runtime-enable leak and other 2024+ CDP detections.
- **Upstream:** Collection of patches for puppeteer and playwright to avoid automation detection and leaks. Helps to avoid Cloudflare and DataDome CAPTCHA pages. Easy to patch/unpatch, can be enabled/disabled on demand.
- **Why included:** The reference fix for the Runtime.Enable leak that broke stock Puppeteer/Playwright stealth in 2024; widely cited but missing from the list.

### 🟢 zendriver

- **Repo:** [cdpdriver/zendriver](https://github.com/cdpdriver/zendriver) · ⭐ 1,417 · Python · AGPL-3.0
- **Last push:** 2026-08-16 · **Status:** `active`
- **When to use:** Choose over nodriver when you need first-class async/await semantics and containerized deployment for stealth scraping.
- **Upstream:** A blazing fast, async-first, undetectable webscraping/web automation framework based on ultrafunkamsterdam/nodriver. Now with Docker support!
- **Why included:** The actively maintained async fork that many 2025-2026 projects have migrated to from nodriver.

---

## Layer 2 — Fingerprint bundle generation

### 🟡 scrapfly fingerprint-generator

- **Repo:** [scrapfly/fingerprint-generator](https://github.com/scrapfly/fingerprint-generator) · ⭐ 153 · Python · Apache-2.0
- **Last push:** 2026-02-18 · **Status:** `stale`
- **When to use:** Use when you need a Python-native source of statistically realistic FP bundles to feed into curl_cffi or nodriver sessions.
- **Upstream:** Browser fingerprint data generator
- **Why included:** Fills the Python gap in fingerprint generation; apify/fingerprint-suite is TS-only.

---

## Layer 3 — CDP-level instrumentation

### 🟡 chrome-remote-interface

- **Repo:** [cyrus-and/chrome-remote-interface](https://github.com/cyrus-and/chrome-remote-interface) · ⭐ 4,554 · JavaScript · MIT
- **Last push:** 2026-02-09 · **Status:** `stale`
- **When to use:** Raw CDP access from Node when you need every protocol domain unwrapped and don't want Puppeteer's abstractions.
- **Upstream:** Chrome Debugging Protocol interface for Node.js

### 🟢 Wirebrowser

- **Repo:** [fcavallarin/wirebrowser](https://github.com/fcavallarin/wirebrowser) · ⭐ 504 · JavaScript · MIT
- **Last push:** 2026-04-17 · **Status:** `active`
- **When to use:** Instrumenting in-page JS without monkeypatching when target code detects prototype tampering or Proxy traps.
- **Upstream:** Wirebrowser is a CDP-based runtime instrumentation platform for the browser. Think Frida, but for JavaScript running in Chrome — without monkeypatching.
- **Latest release:** v0.7.0 (2026-04-15)

### 🟢 simple-cdp

- **Repo:** [gildas-lormeau/simple-cdp](https://github.com/gildas-lormeau/simple-cdp) · ⭐ 28 · JavaScript · MIT
- **Last push:** 2026-08-16 · **Status:** `active`
- **When to use:** Minimal zero-dep CDP client for Deno/Bun scripts where chrome-remote-interface's Node deps are unwanted.
- **Upstream:** Lightweight JavaScript library to interact with Chromium-based browsers via the Chrome DevTools Protocol

### 🟡 cdpx

- **Repo:** [musaspacecadet/cdpx](https://github.com/musaspacecadet/cdpx) · ⭐ 8 · Python · None
- **Last push:** 2025-07-25 · **Status:** `stale`
- **When to use:** Python CDP toolkit alternative to pychrome; tiny project, only consider if you specifically need its inspect/debug CLI.
- **Upstream:** Toolkit for driving Chrome with the DevTools Protocol - inspect, debug, and automate the web.

---

## Layer 2 — Function hooking

### 🔴 ajax-hook

- **Repo:** [wendux/ajax-hook](https://github.com/wendux/ajax-hook) · ⭐ 2,658 · JavaScript · None
- **Last push:** 2023-09-24 · **Status:** `dead`
- **When to use:** Proxy XMLHttpRequest at the prototype level to capture requests issued by obfuscated bundles.
- **Upstream:** Intercepting browser's http requests which made by XMLHttpRequest.

### 🔴 xhook

- **Repo:** [jpillora/xhook](https://github.com/jpillora/xhook) · ⭐ 1,038 · HTML · MIT
- **Last push:** 2024-07-06 · **Status:** `dead`
- **When to use:** Drop-in XHR before/after hooks when you need to mutate responses in-page without a proxy.
- **Upstream:** Easily intercept and modify XHR request and response
- **Latest release:** v1.6.2 (2023-08-28)

### 🔴 fetch-intercept

- **Repo:** [mlegenhausen/fetch-intercept](https://github.com/mlegenhausen/fetch-intercept) · ⭐ 422 · JavaScript · MIT
- **Last push:** 2022-12-08 · **Status:** `dead`
- **When to use:** Register request/response interceptors on window.fetch with promise-chain semantics.
- **Upstream:** Interceptor library for the native fetch command inspired by angular http intercepts.
- **Renamed from:** `werk85/fetch-intercept`
- **Notes:** Original werk85/fetch-intercept transferred to mlegenhausen but canonical repo is also dead (>30 months). Listed for completeness; prefer a Proxy-based hook against window.fetch.

---

## Layer 2 — Browser extensions / userscripts

### 🟡 eruda

- **Repo:** [liriliri/eruda](https://github.com/liriliri/eruda) · ⭐ 21,179 · JavaScript · MIT
- **Last push:** 2025-08-01 · **Status:** `stale`
- **When to use:** Inject a full DevTools-like console into a mobile webview where no remote debugger is available.
- **Upstream:** Console for mobile browsers
- **Latest release:** v3.4.3 (2025-06-15)

### 🟢 Violentmonkey

- **Repo:** [violentmonkey/violentmonkey](https://github.com/violentmonkey/violentmonkey) · ⭐ 8,842 · JavaScript · MIT
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Inject persistent userscripts at document-start to hook globals before page code runs.
- **Upstream:** Violentmonkey provides userscripts support for browsers. It works on browsers with WebExtensions support.
- **Latest release:** v2.37.0 (2026-04-23)

### 🟢 Requestly

- **Repo:** [requestly/requestly](https://github.com/requestly/requestly) · ⭐ 6,758 · — · NOASSERTION
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Modify headers, redirect URLs, and inject scripts from a browser extension without a system-wide proxy.
- **Upstream:** Community hub for Requestly API Client — bugs, feature requests, and roadmap. The privacy-first Postman alternative.
- **Latest release:** changelog-2026.03.23 (2026-03-23)

### 🔴 Resource Override

- **Repo:** [kylepaulsen/ResourceOverride](https://github.com/kylepaulsen/ResourceOverride) · ⭐ 531 · JavaScript · MIT
- **Last push:** 2024-09-02 · **Status:** `dead`
- **When to use:** Swap a remote JS bundle for a local edited copy directly in Chrome without DevTools overrides setup.
- **Upstream:** An extension to help you gain full control of any website by redirecting traffic, replacing, editing, or inserting new content.

### ⚫ ModHeader

- **Repo:** [](https://modheader.com/) · ⭐ 0 · — · Proprietary
- **Last push:** — · **Status:** `missing`
- **When to use:** Quick per-tab header injection (Authorization, User-Agent) without configuring a proxy.
- **Upstream:** Closed-source browser extension to add and modify HTTP request and response headers. No canonical OSS repo (verified 2026-05-18 via gh search).
- **Notes:** Closed-source — homepage at modheader.com. The Selenium wrapper at modheader/modheader_selenium is active but is not the extension itself. Listed for completeness; prefer OSS Requestly for the same job.

---

## Layer 1/2 — Anti-anti-debug

### 🟢 disable-devtool

- **Repo:** [theajack/disable-devtool](https://github.com/theajack/disable-devtool) · ⭐ 3,518 · TypeScript · MIT
- **Last push:** 2026-05-29 · **Status:** `active`
- **When to use:** Reference target — study its detection tricks to know what defenses your RE setup must defeat.
- **Upstream:** Disable web developer tools from the f12 button, right-click and browser menu
- **Latest release:** v0.3.7 (2023-12-22)

### 🟢 AntiDebug_Breaker

- **Repo:** [0xsdeo/AntiDebug_Breaker](https://github.com/0xsdeo/AntiDebug_Breaker) · ⭐ 2,139 · JavaScript · None
- **Last push:** 2026-06-16 · **Status:** `active`
- **When to use:** Bypass debugger/Function.toString/Proxy anti-debug traps as a browser extension during JS RE sessions.
- **Upstream:** JavaScript Reverse Tools -- JS逆向工具

### 🔴 fuck-debugger-extensions

- **Repo:** [546669204/fuck-debugger-extensions](https://github.com/546669204/fuck-debugger-extensions) · ⭐ 331 · JavaScript · Apache-2.0
- **Last push:** 2020-01-10 · **Status:** `dead`
- **When to use:** Legacy reference extension showing minimal patterns to neutralize "debugger" infinite loops.
- **Upstream:** javascript anti-anti debugging

---

## Layer 4 — Deobfuscation

### 🟢 webcrack

- **Repo:** [j4k0xb/webcrack](https://github.com/j4k0xb/webcrack) · ⭐ 2,898 · TypeScript · MIT
- **Last push:** 2026-07-26 · **Status:** `active`
- **When to use:** One-shot CLI to undo obfuscator.io plus split a webpack/browserify bundle back into per-module files.
- **Upstream:** Deobfuscate obfuscator.io, unminify and unpack bundled javascript
- **Latest release:** v2.16.0 (2026-04-25)

### 🔴🗄 de4js

- **Repo:** [lelinhtinh/de4js](https://github.com/lelinhtinh/de4js) · ⭐ 1,580 · JavaScript · MIT
- **Last push:** 2021-11-12 · **Status:** `dead`
- **When to use:** Browser-only UI for quick unpacking of legacy packers (p.a.c.k.e.r, JSFuck, Obfuscator.IO, WiseLoop) without installing anything.
- **Upstream:** JavaScript Deobfuscator and Unpacker
- **GitHub archived:** yes (maintainers explicitly shut down)

### 🟢 synchrony

- **Repo:** [relative/synchrony](https://github.com/relative/synchrony) · ⭐ 1,251 · TypeScript · GPL-3.0
- **Last push:** 2026-07-07 · **Status:** `active`
- **When to use:** Legacy target specifically obfuscated with older javascript-obfuscator versions when webcrack misses string arrays.
- **Upstream:** javascript-obfuscator cleaner & deobfuscator
- **Latest release:** 2.4.5 (2023-11-09)

### 🔴 JStillery

- **Repo:** [mindedsecurity/JStillery](https://github.com/mindedsecurity/JStillery) · ⭐ 900 · JavaScript · GPL-3.0
- **Last push:** 2019-05-30 · **Status:** `dead`
- **When to use:** Reference implementation of partial-evaluation-based deobfuscation; cite for academic comparison rather than production use.
- **Upstream:** Advanced JavaScript Deobfuscation via Partial Evaluation

### 🟢 obfuscator-io-deobfuscator (ben-sb)

- **Repo:** [ben-sb/obfuscator-io-deobfuscator](https://github.com/ben-sb/obfuscator-io-deobfuscator) · ⭐ 804 · TypeScript · Apache-2.0
- **Last push:** 2026-08-09 · **Status:** `active`
- **When to use:** Run this before webcrack/synchrony when the target script is obfuscator.io-flavored; it understands the specific string-array + control-flow transforms better than generic tools.
- **Upstream:** A deobfuscator for scripts obfuscated by Obfuscator.io
- **Why included:** The community gold standard for obfuscator.io specifically; complements (not duplicates) webcrack/synchrony already in the list.

### 🟡 REstringer

- **Repo:** [HumanSecurity/restringer](https://github.com/HumanSecurity/restringer) · ⭐ 606 · JavaScript · MIT
- **Last push:** 2025-12-07 · **Status:** `stale`
- **When to use:** Generic deobfuscator that runs unsafe partial evaluation in a sandbox to resolve runtime-decoded strings webcrack leaves intact.
- **Upstream:** A Javascript Deobfuscator
- **Latest release:** v2.1.0 (2025-11-25)

### 🟢 View8

- **Repo:** [suleram/View8](https://github.com/suleram/View8) · ⭐ 374 · Python · None
- **Last push:** 2026-08-02 · **Status:** `active`
- **When to use:** Recover source from V8 bytecode caches or .jsc files (Electron/Bytenode) where the original JS is not shipped.
- **Upstream:** View8 - Decompiles serialized V8 objects back into high-level readable code.

### 🟡 obfuscation-detector

- **Repo:** [HumanSecurity/obfuscation-detector](https://github.com/HumanSecurity/obfuscation-detector) · ⭐ 88 · JavaScript · MIT
- **Last push:** 2025-11-25 · **Status:** `stale`
- **When to use:** Classify which obfuscator produced a sample before picking the right deobfuscator pipeline.
- **Upstream:** Detect different types of JS obfuscation by their AST structure

### 🟡 JSRETK

- **Repo:** [SeanPesce/JSRETK](https://github.com/SeanPesce/JSRETK) · ⭐ 79 · JavaScript · GPL-2.0
- **Last push:** 2025-12-12 · **Status:** `stale`
- **When to use:** Use as a grab-bag when standard webcrack/synchrony output still needs additional rename/tracing passes — JSRETK has small purpose-built scripts.
- **Upstream:** JavaScript Reverse Engineering Toolkit (JSRETK) - Experimental tools for analyzing (minified/obfuscated) JavaScript
- **Why included:** Active 2025 toolkit; complements the heavier deobfuscators with focused single-purpose utilities.

### 🟡 jscrambler-deobfuscator

- **Repo:** [Ciarands/jscrambler-deobfuscator](https://github.com/Ciarands/jscrambler-deobfuscator) · ⭐ 63 · JavaScript · None
- **Last push:** 2025-10-18 · **Status:** `stale`
- **When to use:** Start here when the target ships Jscrambler-protected JS (common in banking, ticketing, streaming) instead of generic obfuscator.io output.
- **Upstream:** Deobfuscator for JScramblers Enterprise obfuscation (Covers most obfuscation techniques)
- **Why included:** Jscrambler is explicitly in the brief's target list and was not covered; this is the most current public deobfuscator for it.

### 🟡 obfio-deobfuscator

- **Repo:** [xKiian/obfio-deobfuscator](https://github.com/xKiian/obfio-deobfuscator) · ⭐ 32 · Go · MIT
- **Last push:** 2025-12-10 · **Status:** `stale`
- **When to use:** Use when ben-sb's TS deobfuscator is too slow on huge bundles (e.g., merged anti-bot payloads) — Go-fAST runs orders of magnitude faster.
- **Upstream:** obfuscator.io deobfuscator using go-fAST
- **Why included:** Speed-optimized alternative for big bundles; demonstrates the go-fAST ecosystem (uncovered in current list).

### ⚫ unminify-js

- **Repo:** [](—) · ⭐ 0 · — · None
- **Last push:** — · **Status:** `missing`
- **When to use:** N/A — does not exist as a real project.
- **Upstream:** Hallucinated entry — no canonical GitHub repository under this name (re-verified 2026-05-18 via gh search; only v3rlly/UnminifyJS exists, a small 2020 Chrome extension, ⭐1).
- **Notes:** Originally cited by one deep-research report. Use webcrack or wakaru instead — they actually exist and do unminification properly.

---

## Layer 4 — AST transformation

### 🟢 Babel

- **Repo:** [babel/babel](https://github.com/babel/babel) · ⭐ 43,996 · TypeScript · MIT
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Foundation parser/traverser when writing custom AST transforms — every JS deobfuscator in this list builds on @babel/parser or its API.
- **Upstream:** 🐠 Babel is a compiler for writing next generation JavaScript.
- **Latest release:** v1.15.33 (2026-05-02)

### 🟢 SWC

- **Repo:** [swc-project/swc](https://github.com/swc-project/swc) · ⭐ 34,197 · Rust · Apache-2.0
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Use when Babel is too slow on hundreds of MB of bundled JS and you can write the visitor in Rust or via the JS API.
- **Upstream:** Rust-based platform for the Web
- **Latest release:** v1.15.33 (2026-05-02)

### 🟢 ast-grep

- **Repo:** [ast-grep/ast-grep](https://github.com/ast-grep/ast-grep) · ⭐ 15,781 · Rust · MIT
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Grep-style pattern matching over JS AST for triage when you do not want to write a full Babel visitor.
- **Upstream:** ⚡A CLI tool for code structural search, lint and rewriting. Written in Rust
- **Latest release:** 0.42.2 (2026-05-10)

### 🟢 jscodeshift

- **Repo:** [facebook/jscodeshift](https://github.com/facebook/jscodeshift) · ⭐ 10,042 · JavaScript · MIT
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Write one-off codemods to mechanically rename or restructure a deobfuscated codebase with jest-style snapshot tests.
- **Upstream:** A JavaScript codemod toolkit.
- **Latest release:** v17.3.0 (2025-03-24)

### 🟢 Joern

- **Repo:** [joernio/joern](https://github.com/joernio/joern) · ⭐ 3,478 · Scala · Apache-2.0
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Build code property graphs and run taint queries across a deobfuscated bundle to find sinks like eval or postMessage handlers.
- **Upstream:** Open-source code analysis platform for C/C++/Java/Binary/Javascript/Python/Kotlin based on code property graphs. Discord https://discord.gg/vv4MH284Hc
- **Latest release:** v4.0.540 (2026-05-17)

---

## Layer 4 — AI-assisted deobfuscation

### 🟢 humanify

- **Repo:** [jehna/humanify](https://github.com/jehna/humanify) · ⭐ 3,281 · Rust · MIT
- **Last push:** 2026-07-29 · **Status:** `active`
- **When to use:** Rename minified single-letter identifiers to meaningful names using an LLM after structural deobfuscation is done.
- **Upstream:** Deobfuscate Javascript code using ChatGPT
- **Latest release:** v7.29.5 (2026-05-05)

---

## Layer 4 — AI-assisted reverse engineering (broader)

### 🟢 stealth-browser-mcp

- **Repo:** [vibheksoni/stealth-browser-mcp](https://github.com/vibheksoni/stealth-browser-mcp) · ⭐ 1,916 · Python · MIT
- **Last push:** 2026-08-29 · **Status:** `active`
- **When to use:** Plug into Claude/Cursor when you want an agent loop that can browse, inspect, and reverse-engineer a defended SPA in conversation.
- **Upstream:** The only browser automation that bypasses anti-bot systems. AI writes network hooks, clones UIs pixel-perfect via simple chat.
- **Why included:** Concrete example of the emerging "LLM + CDP" RE workflow category — directly aligned with the brief's LLM-powered category.

### 🟡 jshook-reverse-tool

- **Repo:** [wuji66dde/jshook-reverse-tool](https://github.com/wuji66dde/jshook-reverse-tool) · ⭐ 187 · TypeScript · None
- **Last push:** 2025-12-01 · **Status:** `stale`
- **When to use:** Use when you have an obfuscated script open in DevTools and want LLM-assisted call-graph and variable-rename suggestions inline.
- **Upstream:** AI-powered JavaScript reverse engineering too
- **Why included:** One of the few public "LLM-assisted JS RE" tools beyond humanify — addresses the brief's post-humanify gap.

---

## Layer 4 — Bundle analysis

### 🟢 webpack-bundle-analyzer

- **Repo:** [webpack/webpack-bundle-analyzer](https://github.com/webpack/webpack-bundle-analyzer) · ⭐ 12,658 · JavaScript · MIT
- **Last push:** 2026-08-28 · **Status:** `active`
- **When to use:** Open a stats.json or bundle to see module sizes and dependency parents in an interactive treemap before deciding what to unpack.
- **Upstream:** Webpack plugin and CLI utility that represents bundle content as convenient interactive zoomable treemap
- **Latest release:** v5.3.0 (2026-03-25)
- **Renamed from:** `webpack-contrib/webpack-bundle-analyzer`
- **Notes:** Transferred from webpack-contrib org to webpack org; old URL still redirects.

### 🔴 source-map-explorer

- **Repo:** [danvk/source-map-explorer](https://github.com/danvk/source-map-explorer) · ⭐ 3,933 · TypeScript · Apache-2.0
- **Last push:** 2023-03-14 · **Status:** `dead`
- **When to use:** When a .map file is available, attribute every byte of a minified bundle back to its original source file as a treemap.
- **Upstream:** Analyze and debug space usage through source maps
- **Latest release:** v2.5.3 (2022-09-26)

### 🟢 wakaru

- **Repo:** [pionxzh/wakaru](https://github.com/pionxzh/wakaru) · ⭐ 984 · Rust · Apache-2.0
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Unminify and restructure modern React/Vue/webpack bundles back into idiomatic per-module source with JSX recovery.
- **Upstream:** 🔪📦 Javascript decompiler for modern frontend
- **Latest release:** v3.0.0-294f939 (2026-05-16)

---

## Layer 5 — Framework-specific devtools

### 🟢 React DevTools

- **Repo:** [react/react](https://github.com/react/react) · ⭐ 249,623 · JavaScript · MIT
- **Last push:** 2026-09-04 · **Status:** `active`
- **When to use:** Inspect component trees, props, state, and hooks of any React app in the browser; baseline tool before any custom instrumentation.
- **Upstream:** The library for web and native user interfaces.
- **Latest release:** v19.2.6 (2026-05-06)
- **Renamed from:** `facebook/react`
- **Notes:** Lives inside the facebook/react monorepo at packages/react-devtools; the old standalone facebook/react-devtools repo is archived since 2019.

### 🟢 Angular DevTools

- **Repo:** [angular/angular](https://github.com/angular/angular/tree/main/devtools) · ⭐ 101,015 · TypeScript · MIT
- **Last push:** 2026-09-04 · **Status:** `active`
- **When to use:** Inspect component trees, injector hierarchies, and change-detection profiling in any Angular app.
- **Upstream:** Deliver web apps with confidence 🚀
- **Latest release:** tracks angular/angular releases
- **Notes:** Not a separate repo; canonical source is the devtools/ subfolder of angular/angular.

### 🟢 react-scan

- **Repo:** [aidenybai/react-scan](https://github.com/aidenybai/react-scan) · ⭐ 21,830 · TypeScript · MIT
- **Last push:** 2026-08-16 · **Status:** `active`
- **When to use:** Visually highlight which React components re-render on a live page without manually wiring up the Profiler.
- **Upstream:** Scan and fix React performance issues
- **Latest release:** v0.4.3 (2025-06-29)

### 🟢 Redux DevTools

- **Repo:** [reduxjs/redux-devtools](https://github.com/reduxjs/redux-devtools) · ⭐ 14,371 · TypeScript · MIT
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Replay, time-travel, and diff Redux actions and state in a target app for understanding business-logic flow.
- **Upstream:** DevTools for Redux with hot reloading, action replay, and customizable UI
- **Latest release:** @redux-devtools/extension@4.0.0 (2026-03-17)

### 🟢 Vue DevTools

- **Repo:** [vuejs/devtools](https://github.com/vuejs/devtools) · ⭐ 2,902 · TypeScript · MIT
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Inspect Vue component trees, Pinia/Vuex stores, routes, and events in any Vue 2/3 app from the browser.
- **Upstream:** ⚙️ Devtools for debugging Vue.js applications.
- **Latest release:** v8.1.2 (2026-05-08)

---

## Layer 6 — Memory & heap forensics

### 🟢 MemLab

- **Repo:** [facebook/memlab](https://github.com/facebook/memlab) · ⭐ 5,036 · TypeScript · MIT
- **Last push:** 2026-09-05 · **Status:** `active`
- **When to use:** Automate heap-snapshot diffing across scripted user flows to find detached DOM/closure leaks.
- **Upstream:** A framework for finding JavaScript memory leaks and analyzing heap snapshots

---

## Layer 6 — Tracing / observability

### 🟢 Perfetto

- **Repo:** [google/perfetto](https://github.com/google/perfetto) · ⭐ 6,454 · C++ · Apache-2.0
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Open Chrome trace JSON for SQL-queryable analysis of long task chains and main-thread stalls.
- **Upstream:** Production-grade client-side tracing, profiling, and analysis for complex software systems.
- **Latest release:** v55.2 (2026-05-14)

---

## Layer 7 — Native instrumentation (Frida + co.)

### 🟢 Frida

- **Repo:** [frida/frida](https://github.com/frida/frida) · ⭐ 21,863 · Meson · NOASSERTION
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Hooking native code in V8/Node/Electron or non-browser processes when CDP-level instrumentation isn't enough.
- **Upstream:** Main repo for hosting release binaries
- **Latest release:** 17.9.10 (2026-05-15)

### 🟢 objection

- **Repo:** [sensepost/objection](https://github.com/sensepost/objection) · ⭐ 9,371 · Python · GPL-3.0
- **Last push:** 2026-07-23 · **Status:** `active`
- **When to use:** Ready-made Frida commands for mobile pentesting (SSL pinning bypass, class dumping) without writing Frida scripts by hand.
- **Upstream:** 📱 objection - runtime mobile exploration
- **Latest release:** 1.12.4 (2026-03-25)

### 🟢 LIEF

- **Repo:** [lief-project/LIEF](https://github.com/lief-project/LIEF) · ⭐ 5,558 · C++ · Apache-2.0
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Parsing or rewriting PE/ELF/Mach-O of an Electron/native module before instrumenting at runtime with Frida.
- **Upstream:** LIEF - Library to Instrument Executable Formats (C++, Python, Rust)
- **Latest release:** 0.17.6 (2026-03-18)

### 🟢 r2frida

- **Repo:** [nowsecure/r2frida](https://github.com/nowsecure/r2frida) · ⭐ 1,437 · TypeScript · MIT
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Combining live Frida memory access with radare2's disassembler in one session to reverse packed/obfuscated native modules.
- **Upstream:** Radare2 and Frida better together.
- **Latest release:** 6.1.4 (2026-04-12)

### 🔴 Dwarf

- **Repo:** [iGio90/Dwarf](https://github.com/iGio90/Dwarf) · ⭐ 1,318 · Python · GPL-3.0
- **Last push:** 2024-05-16 · **Status:** `dead`
- **When to use:** GUI debugger on top of Frida when you want breakpoints/memory views without scripting; mostly unmaintained.
- **Upstream:** Full featured multi arch/os debugger built on top of PyQt5 and frida

### 🟢 frida-gum

- **Repo:** [frida/frida-gum](https://github.com/frida/frida-gum) · ⭐ 1,017 · C · NOASSERTION
- **Last push:** 2026-09-03 · **Status:** `active`
- **When to use:** Embedding Frida's Stalker/Interceptor engine directly into a C/C++ tool without the full Frida runtime.
- **Upstream:** Cross-platform instrumentation and introspection library written in C

### 🟢 frida-node

- **Repo:** [frida/frida-node](https://github.com/frida/frida-node) · ⭐ 329 · Python · None
- **Last push:** 2026-09-07 · **Status:** `active`
- **When to use:** Driving Frida sessions from a Node.js orchestrator (e.g. inside an existing Puppeteer-based pipeline).
- **Upstream:** Frida Node.js bindings

---

## Layer 7 — Electron-specific

### 🟢 asar

- **Repo:** [electron/asar](https://github.com/electron/asar) · ⭐ 2,858 · TypeScript · MIT
- **Last push:** 2026-09-03 · **Status:** `active`
- **When to use:** Extract app.asar archives bundled inside Electron apps to recover the original JS/HTML/CSS sources.
- **Upstream:** Simple extensive tar-like archive format with indexing
- **Latest release:** v4.2.0 (2026-03-31)

### 🟡 electronegativity

- **Repo:** [doyensec/electronegativity](https://github.com/doyensec/electronegativity) · ⭐ 1,054 · JavaScript · Apache-2.0
- **Last push:** 2025-08-23 · **Status:** `stale`
- **When to use:** Static-scan an unpacked Electron app for unsafe nodeIntegration, contextIsolation off, dangerous protocol handlers, and other known anti-patterns.
- **Upstream:** Electronegativity is a tool to identify misconfigurations and security anti-patterns in Electron applications.
- **Latest release:** v1.10.0 (2022-12-07)

### 🔴🗄 ghidra_nodejs

- **Repo:** [PositiveTechnologies/ghidra_nodejs](https://github.com/PositiveTechnologies/ghidra_nodejs) · ⭐ 384 · Java · None
- **Last push:** 2021-03-04 · **Status:** `dead`
- **When to use:** Load Node.js Bytenode (.jsc) V8 bytecode into Ghidra for static analysis when the target ships compiled JS instead of source.
- **Upstream:** GHIDRA plugin to parse, disassemble and decompile NodeJS Bytenode (JSC) binaries
- **GitHub archived:** yes (maintainers explicitly shut down)
- **Notes:** Archived on GitHub; still the canonical Ghidra plugin for Bytenode despite no updates since 2021.

---

## Layer 7 — Hermes / React Native

### 🟢 hermes-dec

- **Repo:** [P1sec/hermes-dec](https://github.com/P1sec/hermes-dec) · ⭐ 1,169 · Python · AGPL-3.0
- **Last push:** 2026-08-11 · **Status:** `active`
- **When to use:** Reach for it on any React Native APK/IPA whose bundle.hbc you need to read as readable JS instead of bytecode.
- **Upstream:** A reverse engineering tool for decompiling and disassembling the React Native Hermes bytecode
- **Why included:** Although in your exclude list under "hermes-dec," it's the actively maintained 1k-star tool that 2024-2026 RN work depends on — keeping it explicit guards against accidental omission and pins the canonical repo.

### 🔴 hbctool

- **Repo:** [bongtrop/hbctool](https://github.com/bongtrop/hbctool) · ⭐ 638 · Python · MIT
- **Last push:** 2023-12-10 · **Status:** `dead`
- **When to use:** Round-trip patch a Hermes .hbc file (disassemble, edit, reassemble) for older bytecode versions where hermes-dec is decompile-only.
- **Upstream:** Hermes Bytecode Reverse Engineering Tool (Assemble/Disassemble Hermes Bytecode)

### 🟢 hermes-decomp

- **Repo:** [SymbioticSec/hermes-decomp](https://github.com/SymbioticSec/hermes-decomp) · ⭐ 161 · Rust · MIT
- **Last push:** 2026-08-31 · **Status:** `active`
- **When to use:** Rust-based Hermes decompiler aiming for cleaner JS output than hermes-dec on newer bytecode; cross-check when hermes-dec produces poor results.
- **Upstream:** A powerful decompiler that lets you reverse-engineer React Native mobile apps by converting their compiled Hermes bytecode (.hbc) files back into readable JavaScript.

---

## Layer 7 — React Native runtime hooks

### 🔴 heresy

- **Repo:** [Pilfer/heresy](https://github.com/Pilfer/heresy) · ⭐ 124 · TypeScript · MIT
- **Last push:** 2024-11-19 · **Status:** `dead`
- **When to use:** Hook and inspect a running React Native app's JS bridge at runtime instead of statically decompiling its Hermes bytecode.
- **Upstream:** Inspect and instrument React Native applications at runtime

---

## Layer 7 — WebAssembly reverse

### 🟢 binaryen

- **Repo:** [WebAssembly/binaryen](https://github.com/WebAssembly/binaryen) · ⭐ 8,619 · WebAssembly · Apache-2.0
- **Last push:** 2026-09-05 · **Status:** `active`
- **When to use:** Run wasm-opt to shrink or transform .wasm modules and use wasm-dis for higher-level disassembly than wabt's raw WAT.
- **Upstream:** Optimizer and compiler/toolchain library for WebAssembly
- **Latest release:** version_129 (2026-04-01)

### 🟢 wabt

- **Repo:** [WebAssembly/wabt](https://github.com/WebAssembly/wabt) · ⭐ 8,122 · C++ · Apache-2.0
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Convert .wasm to readable .wat text format with wasm2wat, or assemble .wat back to .wasm; the reference toolkit when you need stable WAT output.
- **Upstream:** The WebAssembly Binary Toolkit
- **Latest release:** 1.0.41 (2026-05-07)

### 🟢 wasm-tools

- **Repo:** [bytecodealliance/wasm-tools](https://github.com/bytecodealliance/wasm-tools) · ⭐ 1,788 · Rust · Apache-2.0
- **Last push:** 2026-09-03 · **Status:** `active`
- **When to use:** Inspect, validate, and mutate Component Model / WASI Preview 2 modules where wabt and binaryen lag behind the spec.
- **Upstream:** CLI and Rust libraries for low-level manipulation of WebAssembly modules
- **Latest release:** v1.249.0 (2026-05-15)

### 🟡🗄 twiggy

- **Repo:** [AlexEne/twiggy](https://github.com/AlexEne/twiggy) · ⭐ 1,429 · Rust · Apache-2.0
- **Last push:** 2026-02-18 · **Status:** `stale`
- **When to use:** Attribute bytes inside a .wasm binary to specific functions and call paths when hunting down code-size bloat.
- **Upstream:** Twiggy🌱 is a code size profiler
- **Renamed from:** `rustwasm/twiggy`
- **GitHub archived:** yes (maintainers explicitly shut down)
- **Notes:** Repo is archived on GitHub but received a push in 2026; treat as low-maintenance.

### 🔴 Cetus

- **Repo:** [Qwokka/Cetus](https://github.com/Qwokka/Cetus) · ⭐ 632 · JavaScript · Apache-2.0
- **Last push:** 2024-02-06 · **Status:** `dead`
- **When to use:** Live memory scanning and patching of running WebAssembly games in-browser, Cheat-Engine style; no maintained alternative for this niche.
- **Upstream:** Browser extension for hacking WebAssembly games a la Cheat Engine
- **Latest release:** v1.04 (2023-06-11)
- **Notes:** Original query targeted jakobwesthoff/Cetus which does not exist; canonical repo is Qwokka/Cetus.

### 🟢 NotDec

- **Repo:** [NotDec/NotDec](https://github.com/NotDec/NotDec) · ⭐ 92 · C++ · None
- **Last push:** 2026-08-23 · **Status:** `active`
- **When to use:** Use when an anti-bot vendor (Akamai, Kasada, Cloudflare bm-vm) ships a heavy WASM blob and `wasm-decompile` output is too low-level to follow.
- **Upstream:** a webassembly wasm decompiler and Static Analysis Framework based on llvm IR. (Work In Progress)
- **Why included:** Directly addresses "WASM virtualized obfuscation" — a category currently uncovered beyond the basic wabt/binaryen toolchain.

### 🟡 WASM2JS-Transpiler

- **Repo:** [SerialHooker/WASM2JS-Transpiler](—) · ⭐ 13 · JavaScript · None
- **Last push:** 2026-02-27 · **Status:** `stale`
- **When to use:** Transpile a .wasm module to readable JS with control-flow reconstruction (if/else, loops) when wasm-decompile output is too low-level to follow.
- **Upstream:** C++ tool that converts WebAssembly (`.wasm`) binaries to JavaScript, with an optional AI-powered pass using the Gemini API to rename variables and summarize functions.
- **Why included:** Fills the gap between WABT's wasm-decompile and manual analysis by reconstructing control flow.

---

## Layer 8 — Time-travel / replay

### 🟢 Replay.io DevTools

- **Repo:** [replayio/devtools](https://github.com/replayio/devtools) · ⭐ 723 · TypeScript · NOASSERTION
- **Last push:** 2026-09-01 · **Status:** `active`
- **When to use:** Time-travel through a recorded session to add print statements retroactively without re-running the bug.
- **Upstream:** Replay.io DevTools

---

## Alternative debuggers

### 🔴🗄 ndb

- **Repo:** [GoogleChromeLabs/ndb](https://github.com/GoogleChromeLabs/ndb) · ⭐ 10,870 · JavaScript · Apache-2.0
- **Last push:** 2022-05-26 · **Status:** `dead`
- **When to use:** Legacy Node debugging via a standalone Chrome DevTools window; archived, prefer vscode-js-debug or node --inspect.
- **Upstream:** ndb is an improved debugging experience for Node.js, enabled by Chrome DevTools
- **GitHub archived:** yes (maintainers explicitly shut down)

### 🟢 vscode-js-debug

- **Repo:** [microsoft/vscode-js-debug](https://github.com/microsoft/vscode-js-debug) · ⭐ 1,969 · TypeScript · MIT
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Embedding a production-grade JS/Node debugger over DAP into your own editor or tool, not just VS Code.
- **Upstream:** A DAP-compatible JavaScript debugger. Used in VS Code, VS, + more
- **Latest release:** v1.117.0 (2026-04-17)

---

## MCP toolkits for AI agents

### 🟢 js-reverse-mcp

- **Repo:** [zhizhuodemao/js-reverse-mcp](—) · ⭐ 2,693 · TypeScript · Apache-2.0
- **Last push:** 2026-09-03 · **Status:** `active`
- **When to use:** Drive a live Chrome/CDP debugger from an AI agent for JS reverse engineering: breakpoint-by-text, break-on-XHR, evaluate in a paused frame, export network bodies.
- **Upstream:** AI Agent-first JS 逆向 MCP Server：有头 Chrome 调试、断点、网络/WebSocket 分析、Patchright 反检测，可选 CloakBrowser。
- **Why included:** Second MCP toolkit beyond jshookmcp, focused on live CDP debugging primitives for agent-driven RE.

### 🟢 jshookmcp

- **Repo:** [vmoranv/jshookmcp](https://github.com/vmoranv/jshookmcp) · ⭐ 1,974 · TypeScript · AGPL-3.0
- **Last push:** 2026-09-06 · **Status:** `active`
- **When to use:** Drive JS hooks from an MCP-capable LLM agent to script reverse-engineering of obfuscated SPAs.
- **Upstream:** js hook toolkit that all you need

---

# Anti-Patterns: What Doesn't Work in 2024-2026

What the JS RE community keeps recommending that has stopped working, and what to do instead.

---

## "Just pretty-print and set breakpoints"

**The pitch:** Chrome DevTools' Sources panel has a `{ }` button. Press it, the code is readable, set breakpoints.

**Why it fails:**
- On bundles >10 MB, pretty-print blocks the UI for 15-30 seconds → triggers timing-based anti-debug.
- Heap OOM on bundles >30 MB. The DevTools renderer literally crashes.
- Even when it works, anti-debug `debugger;` traps fire before you can navigate.

**Do instead:** [Layer 1](workflows.md#layer-1--transport-rewriting-the-strongest-move) (rewrite delivery), then [Layer 4](workflows.md#layer-4--static-deobfuscation-pipeline) (Webcrack + AST).

---

## puppeteer-extra-plugin-stealth

**The pitch:** Add `puppeteer-extra-plugin-stealth`, get past bot detection.

**Why it fails (as of 2024+):**
- Modern detectors (DataDome, Cloudflare current) explicitly fingerprint the stealth plugin's patch patterns. Stealth applies known patches in known order — defenders trained on this.
- Stealth patches at the JS layer. Detectors check `Object.getOwnPropertyDescriptor(navigator, 'webdriver').get.toString()` — returns wrapper source, not `[native code]`.

**Do instead:** `Camoufox` (Firefox fork with C++-level patches — JS layer is untouched, fingerprint is genuinely native), `Patchright` (Playwright fork doing the same).

---

## Generic `debugger` removal via Babel transform

**The pitch:** Walk AST, replace every `debugger` statement with `void 0`. Bypass anti-debug.

**Why it fails:**
- Obfuscators synthesize `debugger` at runtime: `(function(){}).constructor("debugger").call()`. Your static transform never sees the string `debugger` in the AST.
- Some defenders use `eval("\x64ebugger")` or similar to evade source scanning.

**Do instead:** Hook `Function.prototype.constructor` via Layer 2 pre-bootstrap injection AND combine with transport-level rewrite for the literal cases.

---

## `Object.defineProperty(navigator, 'webdriver', ...)` to spoof

**The pitch:** `Object.defineProperty(navigator, 'webdriver', { get: () => false })` → detection passes.

**Why it fails:**
- `Object.getOwnPropertyDescriptor(navigator, 'webdriver').get.toString()` returns your arrow function source, not `function get webdriver() { [native code] }`.
- `navigator.__proto__.__proto__` walk reveals the missing `webdriver` accessor on `Navigator.prototype`.

**Do instead:** Patch at C++ level (Camoufox), or use Playwright's `addInitScript` early enough that the patch happens before any site script samples descriptors. Even then, validate against [creep.js](https://abrahamjuliot.github.io/creepjs/) or [browserleaks.com](https://browserleaks.com).

---

## Search by `console.dir(window)` for secrets

**The pitch:** Login, then `console.dir(window)` and grep for the token.

**Why it fails (2024+):**
- Secrets increasingly live in `WeakMap`s (unenumerable by spec — for Spectre mitigation and GC timing privacy).
- Closures in arrow-function-based state machines (Zustand, Jotai, Recoil) hold refs that aren't reachable from globals.
- React Server Components' wire-format `__next_f` holds streaming state but not after hydration.

**Do instead:** [Layer 6](workflows.md#layer-6--memory--heap-forensics) — heap snapshot diff, MemLab with retainer trace, or pre-bootstrap hook on `WeakMap.prototype.set` to mirror keys to an enumerable Set.

---

## "Just throw the bundle at ChatGPT/Claude"

**The pitch:** LLMs are good at code now. Paste the obfuscated bundle, ask for clean version.

**Why it fails:**
- Context window limits — even 200K tokens isn't enough for 5-30 MB bundles.
- Hallucinations break execution equivalence. The "deobfuscated" code looks readable but runs differently or doesn't run at all.
- Renamed variables can collide with other scope-shadowed bindings — silent semantic break.
- [JsDeObsBench](https://arxiv.org/abs/2506.20170) (2025) showed GPT-4o standalone loses execution-equivalence in ~30% of non-trivial cases.

**Do instead:** `humanify` — uses LLM only for renaming, applies via Babel AST transforms with executable-equivalence preservation. Or `CASCADE` (Google internal) approach: LLM finds candidate functions, deterministic AST handles transforms.

---

## "Add `page.waitForTimeout(Math.random() * 5000)` to look human"

**The pitch:** Random delays make scraping look human, avoiding bot detection.

**Why it fails:**
- DataDome and similar tools train ML models on microsecond-distribution patterns. Uniform random delays look more bot-like than no delays.
- Real users have bursty timing (slow read, fast click, slow read, fast click) — uniform distribution is detectable.

**Do instead:** If you need delays, model them on real user traces (record yourself, replay distribution). Better: invest in proper anti-detect (Camoufox) and don't add unnecessary timing.

---

## Selenium with `selenium-stealth` / `undetected-chromedriver` (alone)

**The pitch:** UC + stealth → bypass everything.

**Why it fails:**
- UC was excellent in 2020-2022. As of 2024+, success rate against Cloudflare WAF is 40-60% and dropping per Cloudflare update.
- It patches binary flags, but doesn't address downstream fingerprint surfaces that current detectors check.

**Do instead:** Combine with residential proxies. Use Camoufox or Patchright for the browser layer. Treat UC as one component, not a complete solution.

---

## Recursive `.toString.toString.toString.toString...` panic

**The pitch:** Anti-debug recurses `func.toString.toString()` infinitely. We must spoof every level.

**Why it fails:** It's not infinite. The chain terminates at `Function.prototype.toString` which is `[native code]`. You need to spoof at most 2 levels: the patched function's `.toString` returns the original source, AND `.toString.toString` returns its own native-code source.

**Do instead:**
```javascript
const origToString = Function.prototype.toString;
const wrap = (origFn, patchedFn) => {
    patchedFn.toString = () => origToString.call(origFn);
    patchedFn.toString.toString = () => origToString.call(origToString);
    return patchedFn;
};
```

---

## Trust an `awesome-*` list with no last-updated dates

**The pitch:** This list of 200 tools must contain something useful.

**Why it fails:**
- Most awesome-lists rot. Entries from 2018 sit next to entries from 2024 with no marker.
- The tool you click might be abandoned, archived, or replaced by something with the same name.

**Do instead:** Use this repo. Every entry has `last_push`, `stars`, `status`, and `when_to_use`. Run `scripts/verify.sh` to refresh, or check [verified.json](../data/verified.json) timestamp.

---

## Reverse the VM dispatcher byte-by-byte by hand

**The pitch:** Cloudflare/Kasada VM-obfuscated code requires reversing the interpreter. Open up a notebook, start writing handlers.

**Why it fails:** Maybe nothing — this CAN work. But it takes weeks per target, and the VM mutates with each defender release. If your goal is production scraping, the ROI is terrible unless you're a vendor selling bypass services.

**Do instead:** Capture-and-replay session tokens, residential proxies, headless-browser orchestration. If you absolutely must reverse the VM (research / defensive understanding), budget weeks and document opcodes in a versioned spec.

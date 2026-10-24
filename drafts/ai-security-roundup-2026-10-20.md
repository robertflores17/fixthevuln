---
title: "AI Security Trend Roundup: Oct 20, 2026"
description: "8 AI security updates from Simon Willison, covering Oct 13–Oct 20. Every item credited to its original author."
keywords: "AI security, LLM security, prompt injection, agentic AI, GenAI threats, AI vulnerabilities, AI red team"
slug: "ai-security-roundup-2026-10-20"
author: "FixTheVuln Team"
sources: "Simon Willison"
auto_digest: "true"
cta_section: "comptia"
---

# AI Security Trend Roundup: Oct 20, 2026

*Covering Oct 13 → Oct 20, 2026. 8 new items from 1 sources.*

> This digest credits every source by name and links directly to each original post. Items are selected automatically by keyword and feed filters. All rights and attribution belong to the original authors.

## Prompt Injection & LLM Security

- **[Battle Drones - a vibe coded RTS with audio-based multiplayer](https://simonwillison.net/2026/Oct/20/battledrones/)**  
  Source: [Simon Willison](https://simonwillison.net/), Oct 20
  My latest vibe coded game experiment is a Command &amp; Conquer style RTS &#40;Real Time Strategy&#41; game called Battle Drones &#40;play it here&#41;. Unlike my previous experiments, this one is actually fun to play. I&#x27;m somewhat embarrassed to admit that I got there by telling Claude to &quot;Make it 

- **[My obituary for programming](https://simonwillison.net/2026/Oct/19/my-obituary-for-programming/)**  
  Source: [Simon Willison](https://simonwillison.net/), Oct 19
  My obituary for programming Jeremy Scheff poignantly captures the key loss caused by coding agents for career programmers who enjoyed the puzzle of developing code: Programming turned into one of the greatest jobs you could imagine. You got paid to work on tricky little logic puz

- **[llm-tools-datasette 0.1.1](https://simonwillison.net/2026/Oct/18/llm-tools-datasette/)**  
  Source: [Simon Willison](https://simonwillison.net/), Oct 18
  Release: llm-tools-datasette 0.1.1 When I switched LLM over to httpx2 in LLM 0.33 I forget that this would break any plugins which used httpx without directly depending on it. llm-tools-datasette was one of those plugins, now fixed. Tags: datasette, llm

- **[llm-echo 0.5](https://simonwillison.net/2026/Oct/18/llm-echo/)**  
  Source: [Simon Willison](https://simonwillison.net/), Oct 18
  Release: llm-echo 0.5 I&#x27;m working towards a new LLM release, and testing PRs caused me to revisit the llm-echo debug plugin. This plugin provides a &quot;model&quot; which doesn&#x27;t involve an LLM at all - it just repeats back the prompts that have been fed to it. The new release now updates

- **[Inline rendering with document​.currentScript](https://simonwillison.net/2026/Oct/17/document-currentscript/)**  
  Source: [Simon Willison](https://simonwillison.net/), Oct 17
  Inline rendering with document​.currentScript Lean Rada describes a neat trick that takes advantage of the document.currentScript property. You can use that to drop in a tiny inline &lt;script&gt; element that replaces itself when the page loads: The year is &lt;script&gt; document.currentSc

- **[web-edit 0.1a2](https://simonwillison.net/2026/Oct/17/web-edit/)**  
  Source: [Simon Willison](https://simonwillison.net/), Oct 17
  Release: web-edit 0.1a2 web-edit &#40;previously&#41; is my tiny web app for browsing and editing files in a folder. I mainly built it for editing files on different machines via Tailscale. I added a &quot;copy to clipboard&quot; option for both text and image data. I needed this because I was run

- **[Quoting Addy Osmani, Morgan Westlee Lunt, and Qing Wang](https://simonwillison.net/2026/Oct/16/code-review/)**  
  Source: [Simon Willison](https://simonwillison.net/), Oct 16
  We think &quot;did a human read the code?&quot; is an imprecise proxy for &quot;what could go wrong with this change, and which check, automated or human, is the right one to catch it?&quot; Asking that question also changed when review happens. Before, review was a gate at the end of the road: writ

- **[LaTeX renderer](https://simonwillison.net/2026/Oct/15/latex/)**  
  Source: [Simon Willison](https://simonwillison.net/), Oct 15
  Tool: LaTeX renderer Inspired by Paul Ford and Aboard Foundary&#x27;s new web app Tiny Little Office, which provides a suite of web app content editors &#40;a Word Processor, Outliner, Presentation Builder, Spreadsheet, Calculator, Drawing Tool, Diagram Maker, Animator, Calendar, and Trip


---

## Framework Advisories

Security advisories for AI serving and agent frameworks, each sourced from the project's own GitHub Security Advisory.

- **vllm-project/vllm: [GHSA-vvpg-rrww-wpmh](https://github.com/vllm-project/vllm/security/advisories/GHSA-vvpg-rrww-wpmh):** The OpenAI-compatible server's CORS middleware defaults `allowed_origins` to a wildcard, and the server performs no authentication unless `--api-key`/`VLLM_API_KEY` is set. A malicious web page can therefore use a victim's browser to reach an internal or localhost vLLM deployment, list models, and submit completions. CVSS v3.1 3.4 (Low); affects all versions with default config, fixed in >= 0.32.0.

- **vllm-project/vllm: [GHSA-8397-8qf6-f2gm](https://github.com/vllm-project/vllm/security/advisories/GHSA-8397-8qf6-f2gm):** The Phi-4 multimodal audio encoder runs its conformer attention in eager mode by default, materializing and retaining the full attention matrix for each of 24 layers. A single request with a max-length (~10 minute) audio clip can push memory use past what's available and OOM-crash the engine. CVSS v3.1 6.5 (Moderate); affects 0.31.0, fixed in >= 0.32.0.

- **vllm-project/vllm: [GHSA-h3rc-j82p-2c3h](https://github.com/vllm-project/vllm/security/advisories/GHSA-h3rc-j82p-2c3h):** `ImageMediaIO` passes attacker-supplied image bytes to Pillow's format autodetection without restricting formats, so a file mislabeled as PNG can be handled by Pillow's EPS plugin, which shells out to the host's Ghostscript. On a build vulnerable to the unrelated CVE-2024-29510, that can lead to command execution; on Pillow 12.0.0-12.2.0 a malformed EPS can instead loop and exhaust workers (DoS only, no code execution). CVSS v3.1 8.1 (High); affects 0.30.0, fixed in >= 0.32.0.

- **vllm-project/vllm: [GHSA-q97c-p368-75c4](https://github.com/vllm-project/vllm/security/advisories/GHSA-q97c-p368-75c4):** An off-by-one in the tokenizer wrapper's max-token-id bound lets a pre-tokenized prompt token id equal to the vocab size pass input validation; with tensor-parallel size 1 the unmasked embedding lookup triggers a CUDA device-side assert that crashes the engine for all clients. CVSS v3.1 6.5 (Moderate); affects <= 0.30.0, fixed in >= 0.32.0.

- **vllm-project/vllm: [GHSA-gq5q-89c7-vhvx](https://github.com/vllm-project/vllm/security/advisories/GHSA-gq5q-89c7-vhvx):** DeepSeek-OCR family models (DeepSeek-OCR, DeepSeek-OCR-2, Unlimited-OCR) return `None` from `embed_multimodal` when a legitimate image's normalized pixels sum to exactly zero (e.g. a half-black, half-white PNG), violating the method's contract and tripping a fatal sanity assert that shuts down the whole EngineCore and API server until manually restarted. CVSS v3.1 6.5 (Moderate); affects 0.30.0, fixed in >= 0.32.0.

- **vllm-project/vllm: [GHSA-frvg-qw88-hww9](https://github.com/vllm-project/vllm/security/advisories/GHSA-frvg-qw88-hww9) (CVE-2026-94624):** `OffloadingConnector` with a P2P secondary tier keeps a ZeroMQ session alive for every never-established peer address an API client supplies via `kv_transfer_params.prefill`; around 340 such peers exhausted the default ZMQ socket quota in testing, and the next peer raised an uncaught error that crashed EngineCore and the API server. CVSS v3.1 6.5 (Moderate); affects 0.26.0, fixed in >= 0.32.0.

- **vllm-project/vllm: [GHSA-542m-9234-8gvf](https://github.com/vllm-project/vllm/security/advisories/GHSA-542m-9234-8gvf):** Chat templates render in a Jinja2 sandbox with no wall-clock timeout or output-size cap, inside a thread pool whose default single worker can't be interrupted — one malicious template can block all chat-style endpoints for every tenant, or OOM-kill the API-server process via string multiplication. CVSS v3.1 6.5 (Moderate); affects >= 0.19.0, fixed in >= 0.32.0.

- **vllm-project/vllm: [GHSA-6757-hggm-hp2w](https://github.com/vllm-project/vllm/security/advisories/GHSA-6757-hggm-hp2w):** With `--mm-processor-cache-type shm` enabled, an authenticated caller can forge an SHM handle via `features.kwargs_data` and make the worker call `pickle.loads()` on attacker-staged bytes, with no need for `VLLM_ALLOW_INSECURE_SERIALIZATION=1`. The advisory's own severity section lists CVSS v3.1 8.8 (High) while its sidebar shows a differing 7.5 figure — we cite the advisory's stated 8.8/High pending clarification from upstream. Affects <= 0.25.1, fixed in >= 0.32.0.

- **langchain-ai/langgraph: [GHSA-8prr-f582-jqq3](https://github.com/langchain-ai/langgraph/security/advisories/GHSA-8prr-f582-jqq3) (CVE-2026-115885):** `langgraph deploy --verbose` printed the short-lived Docker registry push token used for `docker login`, exposing it to anyone who could read CI logs or terminal recordings for up to its 12-hour, repo-scoped lifetime. CVSS v4.0 4.1 (Moderate); affects langgraph-cli >= 0.4.15, <= 0.4.31, fixed in 0.4.32.

## Source List

Sources in this roundup, credited to their original authors/organizations:

- [Simon Willison](https://simonwillison.net/), feed: `https://simonwillison.net/atom/everything/`

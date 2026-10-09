---
title: "AI Security Trend Roundup: Oct 09, 2026"
description: "Framework security advisories for the week ending Oct 09, 2026."
keywords: "AI security, LLM security, vLLM, LangGraph, framework advisories, AI vulnerabilities"
slug: "ai-security-roundup-2026-10-09"
author: "FixTheVuln Team"
sources: "GitHub Security Advisories"
cta_section: "comptia"
auto_digest: "true"
---

# AI Security Trend Roundup: Oct 09, 2026

*Items from the week ending Oct 09, 2026.*

## Framework Advisories

- **vllm-project/vllm — [GHSA-x6mc-67gf-chw4](https://github.com/vllm-project/vllm/security/advisories/GHSA-x6mc-67gf-chw4) (CVE-2026-105758):** Qwen2-VL and Qwen3-VL video samplers bound frame count using the request-controlled `max_frames`/`fps` fields in `media_io_kwargs`, which the existing `num_frames` cap doesn't reach. An unauthenticated attacker can raise a `POST /tokenize` request's memory footprint from roughly 2.3 GiB to 13.6 GiB, exhausting server memory. CVSS v3.1 5.3 (Moderate); affects vLLM >= 0.24.0, fixed in >= 0.30.0.

- **vllm-project/vllm — [GHSA-5fj9-pfhr-6j48](https://github.com/vllm-project/vllm/security/advisories/GHSA-5fj9-pfhr-6j48) (CVE-2026-105759):** The Rust frontend's metrics middleware records the raw HTTP method token of every request as a Prometheus label with no allowlist or cardinality limit, so an unauthenticated caller can grow the label set and `/metrics` response without bound, risking an out-of-memory crash. The `--api-key` flag doesn't block it because `/tokenize` and `/detokenize` sit outside the key check. CVSS v3.1 5.9 (Moderate); fixed in vLLM >= 0.30.0.

- **vllm-project/vllm — [GHSA-58v5-2m8f-94pr](https://github.com/vllm-project/vllm/security/advisories/GHSA-58v5-2m8f-94pr) (CVE-2026-105760):** A chat completion request that selects the GLMGA video sampler via `media_io_kwargs` and sets outsized `fps`/`max_frames` values makes the server build an oversized, deduplicated frame-index list before decoding, burning CPU and memory on even a two-frame video and delaying other requests. CVSS v3.1 5.3 (Moderate); affects vLLM >= 0.23.0rc2, < 0.30.0, fixed in 0.30.0.

- **vllm-project/vllm — [GHSA-85xf-c7hm-whqw](https://github.com/vllm-project/vllm/security/advisories/GHSA-85xf-c7hm-whqw) (CVE-2026-105757):** Three structured-output request paths (an xgrammar fallback mismatch, `ngram_gpu` speculative-decoding padding, and the opt-in Rust frontend's empty grammar/json acceptance) raise uncaught exceptions that the scheduler treats as fatal, killing the shared EngineCore and denying service to every concurrent user from a single crafted request. CVSS v3.1 6.5 (Moderate); confirmed on 0.25.1, fixed in 0.30.0.

- **vllm-project/vllm — [GHSA-ph72-cqr5-qpp7](https://github.com/vllm-project/vllm/security/advisories/GHSA-ph72-cqr5-qpp7) (CVE-2026-105754):** The scale-out disaggregated multimodal transport accepts caller-supplied feature data without validating it against the active model's renderer output, letting an authenticated user crash the shared EngineCore via forged grid geometry or a non-positive placeholder length, poison another request's encoder-cache entry, or corrupt placeholder masks during replay (5 sites). CVSS v3.1 6.5 (Moderate, one site scores 5.9); confirmed on 0.25.1, fixed in 0.30.0.

- **vllm-project/vllm — [GHSA-2823-qmq8-rwvj](https://github.com/vllm-project/vllm/security/advisories/GHSA-2823-qmq8-rwvj) (CVE-2026-105756):** The OpenAI-compatible request models only check that a client-supplied `cache_salt` is a non-empty string; a value the LMCache-MP KV connector rejects (for example, one containing `/` or over 128 characters) raises an uncaught `ValueError` that propagates to the EngineCore's fatal-error handler, letting one unauthenticated request take down the engine for all tenants. CVSS v3.1 6.5 (Moderate); confirmed on 0.25.1, fixed in 0.30.0.

- **vllm-project/vllm — [GHSA-2phq-3phc-84px](https://github.com/vllm-project/vllm/security/advisories/GHSA-2phq-3phc-84px) (CVE-2026-105755):** With flash late-interaction enabled (the default for supported models), `/score` and `/rerank` cache query embeddings keyed on the caller-supplied `X-Request-Id` header; a concurrent request reusing that header value overwrites the victim's cached query, scoring the victim's documents against the attacker's query and potentially exhausting the shared use counter. CVSS v3.1 4.2 (Moderate); confirmed on 0.25.1, fixed in 0.30.0.

- **vllm-project/vllm — [GHSA-ph3r-5jfg-f84f](https://github.com/vllm-project/vllm/security/advisories/GHSA-ph3r-5jfg-f84f) (CVE-2026-105753):** vLLM's default LRU multimodal cache can desync between the frontend and engine core: if a request is rejected after the frontend hashes its media but before the engine core receives it, a later request reusing that media hash gets a frontend cache hit while the engine core gets no payload, tripping a reachable assertion that crashes request handling. CVSS v3.1 6.5 (Moderate); confirmed on 0.25.1, fixed in 0.28.0.

- **vllm-project/vllm — [GHSA-m52c-39rh-f3gp](https://github.com/vllm-project/vllm/security/advisories/GHSA-m52c-39rh-f3gp):** The `/v1/audio/transcriptions` endpoint falls back to PyAV/FFmpeg when `soundfile` can't parse an upload, checking only file size beforehand; a malformed IAMF audio container can trigger a heap overflow in FFmpeg's `libavformat` IAMF parser, and repeated crafted uploads can corrupt the heap and crash the API process. CVSS v3.1 6.5 (Moderate), no CVE assigned yet; confirmed on 0.25.1, fixed in 0.29.0.

- **vllm-project/vllm — [GHSA-935w-9g4m-p28p](https://github.com/vllm-project/vllm/security/advisories/GHSA-935w-9g4m-p28p) (CVE-2026-105752):** On the GPT-OSS Harmony tool-calling path, next-turn prompt continuations are resubmitted without the caller's `cache_salt`, landing in a shared, unsalted cache namespace; another tenant who can guess the post-tool history can submit a matching prompt and read exact cached-token counts, defeating the prefix-cache membership protection `cache_salt` is meant to provide. CVSS v3.1 3.1 (Low); the advisory states this is distinct from the earlier GHSA-4qjh-9fv9-r85r (CVE-2025-46570); confirmed on 0.25.1, fixed in 0.30.0.

- **langchain-ai/langgraph — [GHSA-4hm6-w6qq-w73v](https://github.com/langchain-ai/langgraph/security/advisories/GHSA-4hm6-w6qq-w73v):** In LangGraph deployments using JavaScript/TypeScript custom authentication, the server can fail to apply Store authorization changes an auth handler returns when that handler restricts users by rewriting the requested namespace, letting an authenticated ordinary user read, overwrite, search, or delete other users' Store data. CVSS v4.0 8.6 (High), no CVE assigned yet; Python handlers and handlers that reject (rather than rewrite) unauthorized namespaces are unaffected; fixed in `langgraph-api` >= 0.15.0.

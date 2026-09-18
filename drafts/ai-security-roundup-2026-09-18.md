---
title: "AI Security Trend Roundup — Sep 18, 2026"
description: "Framework security advisories for AI/LLM infrastructure, curated by FixTheVuln."
keywords: "AI security, LLM security, vLLM, framework advisories, AI vulnerabilities"
date: "2026-09-18"
slug: "ai-security-roundup-2026-09-18"
author: "FixTheVuln Team"
sources: "vllm-project/vllm GitHub Security Advisories"
cta_section: "comptia"
---

# AI Security Trend Roundup — Sep 18, 2026

## Framework Advisories

- **[GHSA-wpww-v874-ph2p](https://github.com/vllm-project/vllm/security/advisories/GHSA-wpww-v874-ph2p)** — vllm-project/vllm: DoS via unbounded `cache_salt` length (CVSS 5.3, Moderate). The `cache_salt` field on vLLM's API endpoints enforces no maximum length, so an unauthenticated request with a multi-hundred-MB salt gets SHA-256-hashed on the single EngineCore scheduler thread, stalling unrelated requests (a 200MB salt pushed concurrent p90 latency to ~1.8s). Affects vllm < 0.29.0; fixed in 0.29.0.

- **[GHSA-jcq2-4gch-5qhf](https://github.com/vllm-project/vllm/security/advisories/GHSA-jcq2-4gch-5qhf)** — vllm-project/vllm: uncontrolled resource consumption in multimodal chat audio decoding (CVSS 4.3, Moderate). The chat message parser bypasses the `VLLM_MAX_AUDIO_CLIP_FILESIZE_MB` size check that the speech-to-text endpoint already enforces, letting an unauthenticated caller force oversized audio downloads/decodes and exhaust memory and CPU. Affects vllm < 0.29.0; fixed in 0.29.0.

- **[GHSA-j682-9xp5-rrf3](https://github.com/vllm-project/vllm/security/advisories/GHSA-j682-9xp5-rrf3)** — vllm-project/vllm: sampler subclass counter shadowing bypasses PyNvVideoCodec decoder limits (CVSS 3.7, Low). Sampler subclasses that inherit from `PyNvVideoCodecVideoBackendMixin` each keep an independent shadow `_active_decoder_slots` counter, so a client cycling through different sampler subclasses can exceed the configured process-wide decoder limit and consume more GPU memory than reserved at startup. Affects vllm < 0.29.0; fixed in 0.29.0.

- **[GHSA-p6g9-7v3x-m8mv](https://github.com/vllm-project/vllm/security/advisories/GHSA-p6g9-7v3x-m8mv)** — vllm-project/vllm: remote media fetched and fully materialized before size/item limits are enforced, across 4 ingress points (CVSS 6.5, Moderate). vLLM fully downloads HTTP responses, decodes base64 payloads, or spawns fetch tasks for media *before* applying the documented size/quantity limits, letting a remote attacker trigger memory and bandwidth exhaustion with oversized or over-counted media requests. Affects vllm ≤ 0.29.0; fixed after 0.29.0.

- **[GHSA-3mqx-f33v-vgp9](https://github.com/vllm-project/vllm/security/advisories/GHSA-3mqx-f33v-vgp9)** — vllm-project/vllm: disaggregated `generate` skips decoder prompt-length validation for some multimodal processors (CVSS 6.5, Moderate). Processors that set `skip_prompt_length_check=True` (e.g. Nemotron Parse, Whisper, FireRedLID) skip length validation for both encoder and decoder prompts in disaggregated serving mode, letting a request exceed `max_model_len` and crash the worker instead of being rejected at the API layer. Affects vllm < 0.29.0; fixed in 0.29.0.

- **[GHSA-qff2-492f-9fm4](https://github.com/vllm-project/vllm/security/advisories/GHSA-qff2-492f-9fm4)** — vllm-project/vllm: Rust HTTP/gRPC frontends bypass the Python `stop_token_ids` vocab-bound fix and can terminate EngineCore (CVSS 5.9, Moderate). The Rust-side frontends construct engine-facing sampling parameters directly, skipping the vocabulary-range validation applied on the Python side; an out-of-range `stop_token_ids` value combined with `min_tokens > 0` reaches `logits.index_put_()` and triggers a fatal CUDA assertion. Affects vllm >= 0.22.0, <= 0.23.0; fixed in 0.24.0.

- **[GHSA-hhv2-872h-628q](https://github.com/vllm-project/vllm/security/advisories/GHSA-hhv2-872h-628q)** — vllm-project/vllm: incomplete artifact pin propagation in FunAudioChat and Tarsier2 (CVSS 6.5, Moderate). Three code paths in these model implementations fail to forward an operator's pinned Hugging Face `revision` when loading feature-extractor, tokenizer, or config artifacts, so a later change to those repos' default branch can silently alter preprocessing/tokenizer behavior on a deployment believed to be pinned. Affects vllm >= 0.22.1, <= 0.28.0; fixed in 0.28.0.

- **[GHSA-v5gm-qgmv-gc6c](https://github.com/vllm-project/vllm/security/advisories/GHSA-v5gm-qgmv-gc6c)** — vllm-project/vllm: out-of-range `stop_token_ids` with `min_tokens` can kill vLLM EngineCore (CVSS 6.5, Moderate). The `/v1/completions` and `/v1/chat/completions` endpoints check that user-supplied `stop_token_ids` are integers but not that they fall within the model's vocabulary; when `min_tokens > 0`, an out-of-range ID is used as a logits index and triggers a fatal CUDA assertion, crashing EngineCore and requiring a service restart. Affects vllm < 0.29.0; fixed in 0.29.0.

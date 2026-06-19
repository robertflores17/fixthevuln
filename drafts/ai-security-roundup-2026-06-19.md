---
title: "AI Security Trend Roundup — Jun 19, 2026"
description: "56 curated AI security updates from OWASP GenAI, arXiv, Simon Willison, CISA, and 4 more sources covering Jun 12–Jun 19. Every item credited to its original author."
keywords: "AI security, LLM security, prompt injection, agentic AI, GenAI threats, AI vulnerabilities, AI red team"
date: "2026-06-19"
slug: "ai-security-roundup-2026-06-19"
author: "FixTheVuln Team"
sources: "OWASP GenAI Security Project, Simon Willison, arXiv cs.CR, Protect AI, Google Project Zero, CISA, NIST, Hacker News"
cta_section: "comptia"
---

# AI Security Trend Roundup — Jun 19, 2026

*Covering Jun 12 → Jun 19, 2026. 56 new items from 8 tracked sources.*

> This digest credits every source by name and links directly to each original post. Editorial curation by FixTheVuln — all rights and attribution belong to the original authors.

## Academic & Research

- **[Secure Coding Drift in LLM-Assisted Post-Quantum Cryptography Development: A Gamified Fix](https://arxiv.org/abs/2606.19474)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.19474v1 Announce Type: new Abstract: The transition to Post Quantum Cryptography (PQC) introduces considerable implementation complexity, requiring strict adherence to constant-time execution, side channel resistance, and precise parametrisation. Simultaneously, large 

- **[A Layered Security Framework Against Prompt Injection in RAG-Based Chatbots](https://arxiv.org/abs/2606.19660)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.19660v1 Announce Type: new Abstract: Prompt injection is ranked as the most critical vulnerability in large language model (LLM) deployments by the OWASP Top 10 for LLM Applications, yet existing defenses operate at isolated pipeline stages and remain incomplete. Input

- **[When Global Gating Is Enough: Admission-Time Hubness Control in Anisotropic Vector Retrieval Systems](https://arxiv.org/abs/2606.19692)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.19692v1 Announce Type: new Abstract: Vector hubness, where a few points become nearest neighbors of many queries, creates a poisoning risk in retrieval-augmented generation (RAG): one injected document can influence unrelated requests. Existing defenses use periodic re

- **[SafeSpec: Fast and Safe LLM via Dynamic Reflective Sampling](https://arxiv.org/abs/2606.19755)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.19755v1 Announce Type: new Abstract: Speculative inference accelerates large language model (LLM) decoding but provides no inherent safety guarantees. Existing safety defenses are largely incompatible with speculative inference: they either introduce additional computa

- **[Heterogeneous LLM Debate Under Adversarial Peers: Honest Gains, Replacement Costs, and Resilience](https://arxiv.org/abs/2606.19826)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.19826v1 Announce Type: new Abstract: Heterogeneous LLM debate is motivated by the promise that diverse peers correct one another, but the same exchange that carries correction also carries adversarial influence. We measure which dominates by tracking how a heterogeneou

- **[FFinRED: An Expert-Guided Benchmark Generation and Evaluation Framework for Financial LLM Red-Teaming](https://arxiv.org/abs/2606.19887)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.19887v1 Announce Type: new Abstract: Existing safety benchmarks target general adversarial scenarios but miss finance-specific risks. Financial LLMs face regulatory compliance violations, fraud facilitation, and systemic trust erosion that require targeted evaluation. 

- **[Quantization as a Malicious Task: Removing Quantization-Conditioned Backdoors via Task Arithmetic](https://arxiv.org/abs/2606.20254)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.20254v1 Announce Type: new Abstract: Model quantization is widely adopted to reduce memory usage and inference cost when deploying deep neural networks on resource-constrained devices. However, recent studies have revealed a new security threat known as Quantization-Co

- **[LLM agent safety, multi-turn red-teaming, jailbreak benchmarks, adversarial robustness, safety-critical systems](https://arxiv.org/abs/2606.20408)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.20408v1 Announce Type: new Abstract: Large language model (LLM) agents are increasingly proposed as supervisory components for safety-critical systems, yet their robustness under sustained, adaptive adversarial pressure remains poorly characterized. We present NRT-Benc

- **[Multi-View Decompilation for LLM-Based Malware Classification](https://arxiv.org/abs/2606.20436)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.20436v1 Announce Type: new Abstract: Malware analysts often inspect compiled binaries through decompiled pseudo-C, when source code is unavailable. Recent work suggests that large language models (LLMs) can assist this process by classifying decompiled code as benign o

- **[Image Encryption Algorithm Based on Convolutional Neural Networks and Dynamic S-Box Generation](https://arxiv.org/abs/2606.20444)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.20444v1 Announce Type: new Abstract: The paper proposes a dynamic approach to image encryption, combining the use of Convolutional Neural Networks (CNNs) and classical cryptography to improve the security and flexibility of image encryption. The main concept is to crea

- **[Analyzing Defensive Misdirection Against Model-Guided Automated Attacks on Agentic AI Systems](https://arxiv.org/abs/2606.20470)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.20470v1 Announce Type: new Abstract: Agentic AI systems increasingly rely on language-model components to interpret instructions, process external data, invoke tools, and coordinate with other agents. These capabilities make prompt-injection and jailbreak attacks more 

- **[Calibration Without Comprehension: Diagnosing the Limits of Fine-Tuning LLMs for Vulnerability Detection in Systems Software](https://arxiv.org/abs/2606.20502)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Jun 19
  arXiv:2606.20502v1 Announce Type: new Abstract: Whether LLMs scoring well on vulnerability benchmarks genuinely reason about security or merely pattern-match on contaminated data remains unresolved. We present CWE-Trace, a framework for LLM vulnerability detection built from 834 


## Prompt Injection & LLM Security

- **[Datasette Apps: Host custom HTML applications inside Datasette](https://simonwillison.net/2026/Jun/18/datasette-apps/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 18
  Today we launched a new plugin for Datasette, datasette-apps, with this launch announcement post on the Datasette project blog. That post has the what, but I'm going to expand on that a little bit here to provide the why. The TL;DR Datasette Apps are self-contained HTML+JavaScrip

- **[datasette-acl 0.6a0](https://simonwillison.net/2026/Jun/18/datasette-acl/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 18
  Release: datasette-acl 0.6a0 This release expands datasette-acl from table-only permissions toward a general resource-sharing system. Alex Garcia did most of the work for this release - we're fleshing out the plugin that will allow multi-user Datasette instances finely grained co

- **[GLM-5.2 is probably the most powerful text-only open weights LLM](https://simonwillison.net/2026/Jun/17/glm-52/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 17
  Chinese AI lab Z.ai released GLM-5.2 to their coding plan subscribers on June 13th, and then yesterday (June 16th) released the full open weights under an MIT license. Similar in size to their previous GLM-5 and GLM-5.1 releases, this is 753B parameter, 1.51TB monster - with 40 a

- **[Quoting Charity Majors](https://simonwillison.net/2026/Jun/17/charity-majors/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 17
  What happened in 2025 was this: the economics of code production were turned upside down. Instead of being very hard, time-consuming, and expensive to generate code, it became effectively free and instant. Lines of code went from being treasured, reused, cared for and carefully c

- **[<click-to-play> — a still that plays](https://simonwillison.net/2026/Jun/17/click-to-play-component/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 17
  Tool: <click-to-play> — a still that plays A progressive enchantment Web Component that turns this markup: <click-to-play> <a href="URL to GIF"> <img src="URL to first frame" alt="..."> </a> </click-to-play> Into a still frame with a click to play button which loads the GIF on de

- **[NetNewsWire Status](https://simonwillison.net/2026/Jun/17/netnewswire-status/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 17
  NetNewsWire Status I find this inspiring. Brent Simmons retired a year ago, and his retirement project is making one piece of software really, really good - free from any commercial pressure. The software is NetNewsWire - "it's like podcasts, but for reading" - first released in 

- **[datasette 1.0a34](https://simonwillison.net/2026/Jun/16/datasette/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 16
  Release: datasette 1.0a34 Quoting the release notes: The big feature in this alpha is tools to insert, edit and delete rows within the Datasette interface. These features are available on table pages, and edit and delete are also available as action items on the row page. The ins

- **[datasette-tailscale 0.1a0](https://simonwillison.net/2026/Jun/16/datasette-tailscale/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 16
  Release: datasette-tailscale 0.1a0 A very experimental alpha plugin which lets you do this: datasette tailscale mydata.db \ --ts-authkey tskey-auth-xxxx --ts-hostname datasette-preview This starts a localhost Datasette server with a Tailscale sidecar that connects it to your Tail

- **[Quoting Georgi Gerganov](https://simonwillison.net/2026/Jun/16/georgi-gerganov/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 16
  I can 100% attest to the fact that Qwen3.6-27B is a very capable local model for coding tasks. Over the last month and a half I've been using it almost daily, either on my M2 Ultra or on my RTX 5090 box. I use it for small mundane tasks at ggml-org - nothing really impressive, bu

- **[The Fable 5 Export Controls Harm US Cyber Defense](https://simonwillison.net/2026/Jun/16/fable-5-export-controls/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 16
  The Fable 5 Export Controls Harm US Cyber Defense I quoted The Atlantic quoting Kate Moussouris earlier, when I should have gone straight to the source. Here she is confirming that the "jailbreak" that got Claude Fable 5 banned under an export control really was "fix this code": 

- **[Quoting Matteo Wong, The Atlantic](https://simonwillison.net/2026/Jun/16/matteo-wong-the-atlantic/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 16
  Katie Moussouris, a cybersecurity expert and the CEO of Luta Security, told me that Anthropic shared with her a copy of the White House’s report on the Fable jailbreak to get her appraisal. (She said that she is not being paid by Anthropic.) The report, Moussouris said, involved 

- **[Cloudflare CAPTCHA on at least one ampersand](https://simonwillison.net/2026/Jun/16/captcha-on-at-least-one-ampersand/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 16
  TIL: Cloudflare CAPTCHA on at least one ampersand I'm using Cloudflare's CAPTCHA (they call it a "Web Application Firewall > Custom rules > Managed Challenge" these days) to prevent crawlers from aggresively spidering my faceted search engine on this site, but I got fed up of eve

- **[datasette-apps 0.1a3](https://simonwillison.net/2026/Jun/15/datasette-apps-2/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 15
  Release: datasette-apps 0.1a3 Fixed a bug where users without the create-app permission could still create apps. #27 Fixed a bug where it was impossible to grant permission to edit an app to users who were not the app's owner. The rules for edit/delete are now the same as view: i

- **[datasette-apps 0.1a2](https://simonwillison.net/2026/Jun/15/datasette-apps/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 15
  Release: datasette-apps 0.1a2 Custom network/CSP origins for apps are now guarded by a new apps-set-csp permission, with an optional allowed_csp_origins plugin allow-list for non-privileged users. The Datasette Agent app creation tool enforces the same rules. #24 Stored query pic

- **[datasette-agent 0.3a0](https://simonwillison.net/2026/Jun/15/datasette-agent/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 15
  Release: datasette-agent 0.3a0 New tool, execute_write_sql, which requests user approval and then writes to a database - taking user permissions into account. #27 I added a mechanism for asking user approval in datasette agent 0.2a0. The new execute_write_sql tool can now prompt 

- **["They screwed us": Personality clashes sent Anthropic's models offline](https://simonwillison.net/2026/Jun/15/axios-clashes-anthropics/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 15
  "They screwed us": Personality clashes sent Anthropic&#x27;s models offline Lots of "source familiar with the administration's thinking" and "source close to Anthropic" in this Axios piece, which is the best collection of behind-the-scenes gossip I've seen about the US government

- **[Quoting Julia Evans](https://simonwillison.net/2026/Jun/15/julia-evans/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 15
  [...] Instead, I picture a specific person and I just write for them. Often this person is "me, but 3 years ago" or a good friend. &mdash; Julia Evans, write for 1 person Tags: writing, julia-evans

- **[Why AI hasn’t replaced software engineers, and won’t](https://simonwillison.net/2026/Jun/14/why-ai-hasnt-replaced-software-engineers/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 14
  Why AI hasn’t replaced software engineers, and won’t Arvind Narayanan and Sayash Kappor take on the question of AI job losses through the lens of a profession that is uniquely suited to AI disruption - software engineering. In this essay, we argue that there is enough evidence to

- **[Publishing WASM wheels to PyPI for use with Pyodide](https://simonwillison.net/2026/Jun/13/publishing-wasm-wheels/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 13
  The Pyodide 314.0 release announcement (via Hacker News) includes news I've been looking forward to for a long time: You can now publish Python packages built for Pyodide (or any Python runtime compatible with the PyEmscripten platform defined in PEP 783) directly to PyPI and ins

- **[luau-wasm 0.1a0](https://simonwillison.net/2026/Jun/13/luau-wasm/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 13
  Release: luau-wasm 0.1a0 See Publishing WASM wheels to PyPI for use with Pyodide for details. Tags: lua, webassembly, pyodide

- **[Mapping SQLite result columns back to their source `table.column`](https://simonwillison.net/2026/Jun/13/sqlite-column-provenance/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 13
  Research: Mapping SQLite result columns back to their source `table.column` It would be neat if arbitrary SQL queries in Datasette could be rendered with additional information based on which columns from which tables were included in the results. To build that, we would need to 

- **[Statement on the US government directive to suspend access to Fable 5 and Mythos 5](https://simonwillison.net/2026/Jun/13/us-government-directive-to-suspend-access/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 13
  Statement on the US government directive to suspend access to Fable 5 and Mythos 5 Well this is nuts: The US government, citing national security authorities, has issued an export control directive to suspend all access to Fable 5 and Mythos 5 by any foreign national, whether ins

- **[OpenAI WebRTC Audio Session, now with document context](https://simonwillison.net/2026/Jun/12/openai-webrtc/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 12
  OpenAI WebRTC Audio Session, now with document context I built the first version of this tool in December 2024 to try out the then-new OpenAI WebRTC API for interacting with their realtime audio models. Last month OpenAI introduced a brand new model to that API called GPT‑Realtim

- **[Quoting Andrew Singleton](https://simonwillison.net/2026/Jun/12/andrew-singleton/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Jun 12
  Jenny owns a crematorium. John’s propane company gives her a $20 billion investment in return for 5 percent of her operation. Jenny throws $10 billion into the incinerator, then pays John $10 billion to buy propane to burn that money to ashes. John reports that his AI investments


## Community Signal

- **[Generative AI Is Having Its Herbalife Moment](https://www.whatwelo.st/p/generative-ai-is-having-its-herbalife)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 19
  Article URL: https://www.whatwelo.st/p/generative-ai-is-having-its-herbalife Comments URL: https://news.ycombinator.com/item?id=48595144 Points: 59 # Comments: 55

- **[GLM-5.2: The Most Powerful Open Model yet and the Brutal Reality of Running It](https://vettedconsumer.com/glm-5-2-the-most-powerful-open-weight-model-yet-and-the-brutal-reality-of-running-it-locally/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 19
  Article URL: https://vettedconsumer.com/glm-5-2-the-most-powerful-open-weight-model-yet-and-the-brutal-reality-of-running-it-locally/ Comments URL: https://news.ycombinator.com/item?id=48594012 Points: 41 # Comments: 26

- **[Amazon investigating engineers who criticized AI data center expansion](https://www.cnbc.com/2026/06/18/amazon-engineers-ai-data-center-opposition.html)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 18
  Article URL: https://www.cnbc.com/2026/06/18/amazon-engineers-ai-data-center-opposition.html Comments URL: https://news.ycombinator.com/item?id=48590891 Points: 53 # Comments: 17

- **[The AI Hate Progression](https://www.xodium.net/2026/06/the-ai-hate-progression.html)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 18
  Article URL: https://www.xodium.net/2026/06/the-ai-hate-progression.html Comments URL: https://news.ycombinator.com/item?id=48589485 Points: 115 # Comments: 171

- **[Ask HN: What tools are you using for AI-assisted code review?](https://news.ycombinator.com/item?id=48587808)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 18
  My team (around 40 people who write code) is evaluating tools for AI-assisted code review. The market appears to be rife with options, so before starting a series of free trials, I’d like to ask a knowledgeable crowd. What tools or services are you using? Do you use them just for

- **[GLM-5.2 is probably the most powerful text-only open weights LLM](https://simonwillison.net/2026/Jun/17/glm-52/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 18
  Article URL: https://simonwillison.net/2026/Jun/17/glm-52/ Comments URL: https://news.ycombinator.com/item?id=48587383 Points: 27 # Comments: 4

- **[Meta head of product for 'AI for work' transformation is leaving company](https://www.reuters.com/world/meta-head-product-ai-work-transformation-is-leaving-company-2026-06-17/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 18
  Article URL: https://www.reuters.com/world/meta-head-product-ai-work-transformation-is-leaving-company-2026-06-17/ Comments URL: https://news.ycombinator.com/item?id=48580103 Points: 28 # Comments: 2

- **[AI Compute Extensions (ACE) Specification](https://x86ecosystem.org/resource/ai-compute-extensions-ace-specification/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 18
  Article URL: https://x86ecosystem.org/resource/ai-compute-extensions-ace-specification/ Comments URL: https://news.ycombinator.com/item?id=48579913 Points: 52 # Comments: 24

- **[Bernie Sanders unveils plan to give the public direct ownership of AI companies](https://apnews.com/article/bernie-sanders-ai-public-ownership-57b9f20d96490083e2749adba0f13977)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://apnews.com/article/bernie-sanders-ai-public-ownership-57b9f20d96490083e2749adba0f13977 Comments URL: https://news.ycombinator.com/item?id=48578555 Points: 22 # Comments: 8

- **[The hacker sent by Anthropic to calm the government's nerves about AI safety](https://www.wsj.com/tech/ai/anthropic-mythos-safety-nicholas-carlini-20bceaa3)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Readable: https://www.wsj.com/tech/ai/anthropic-mythos-safety-nicholas... Comments URL: https://news.ycombinator.com/item?id=48575451 Points: 88 # Comments: 109

- **[Using AI to improve a challenging reaction in medicinal chemistry](https://openai.com/index/ai-chemist-improves-reaction/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://openai.com/index/ai-chemist-improves-reaction/ Comments URL: https://news.ycombinator.com/item?id=48573757 Points: 57 # Comments: 20

- **[The Competitive Moat That AI Can't Replicate](https://ghostinthedata.info/posts/2026/2026-06-13-human-connection-moat/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://ghostinthedata.info/posts/2026/2026-06-13-human-connection-moat/ Comments URL: https://news.ycombinator.com/item?id=48573435 Points: 141 # Comments: 122

- **[Only 16 Percent of Americans Think AI Will Have a Positive Impact on Society](https://techcrunch.com/2026/06/17/only-16-percent-of-americans-think-ai-will-have-a-positive-impact-on-society-a-new-study-shows/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://techcrunch.com/2026/06/17/only-16-percent-of-americans-think-ai-will-have-a-positive-impact-on-society-a-new-study-shows/ Comments URL: https://news.ycombinator.com/item?id=48573332 Points: 396 # Comments: 492

- **[Launch HN: Adam (YC W25) – Open-Source AI CAD](https://github.com/Adam-CAD/CADAM)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Hey HN! I'm Zach from Adam (https://adam.new/). We're building AI agents for mechanical CAD software. We’ve built the company on two fundamental beliefs:- AI will be the primary medium for creating mechanical designs just like it is in software today.- The best paradigm for CAD g

- **[TREX: An AI code reviewer that runs your code](https://www.greptile.com/blog/trex-code-execution)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://www.greptile.com/blog/trex-code-execution Comments URL: https://news.ycombinator.com/item?id=48571851 Points: 59 # Comments: 11

- **[Pentagon boasts of using AI to write reports mandated by Congress (1.5mil users)](https://arstechnica.com/ai/2026/06/pentagon-boasts-of-using-ai-to-write-reports-mandated-by-congress/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://arstechnica.com/ai/2026/06/pentagon-boasts-of-using-ai-to-write-reports-mandated-by-congress/ Comments URL: https://news.ycombinator.com/item?id=48571016 Points: 77 # Comments: 57

- **[AI demands more engineering discipline. Not less](https://charitydotwtf.substack.com/p/ai-demands-more-engineering-discipline)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://charitydotwtf.substack.com/p/ai-demands-more-engineering-discipline Comments URL: https://news.ycombinator.com/item?id=48570948 Points: 419 # Comments: 211

- **[Sixty percent of US consumers say 'AI' in brand messaging is a turnoff](https://wpvip.com/future-of-the-web-2026/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://wpvip.com/future-of-the-web-2026/ Comments URL: https://news.ycombinator.com/item?id=48569278 Points: 1074 # Comments: 573

- **[Show HN: I built 184 free browser tools – PDF, image, dev, AI tasks, no upload](https://brevio.pro)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://brevio.pro Comments URL: https://news.ycombinator.com/item?id=48568023 Points: 88 # Comments: 28

- **[GLM-5.2 is the new leading open weights model on Artificial Analysis](https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Jun 17
  Article URL: https://artificialanalysis.ai/articles/glm-5-2-is-the-new-leading-open-weights-model-on-the-artificial-analysis-intelligence-index Comments URL: https://news.ycombinator.com/item?id=48567759 Points: 886 # Comments: 440


---

## Source List

All sources tracked in this roundup, credited to their original authors/organizations:

- [OWASP GenAI Security Project](https://genai.owasp.org/) — feed: `https://genai.owasp.org/feed/`
- [Simon Willison](https://simonwillison.net/) — feed: `https://simonwillison.net/atom/everything/`
- [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — feed: `http://export.arxiv.org/rss/cs.CR`
- [Protect AI](https://protectai.com/) — feed: `https://protectai.com/blog/rss.xml`
- [Google Project Zero](https://googleprojectzero.blogspot.com/) — feed: `https://googleprojectzero.blogspot.com/feeds/posts/default`
- [CISA Cybersecurity Advisories](https://www.cisa.gov/news-events/cybersecurity-advisories) — feed: `https://www.cisa.gov/cybersecurity-advisories/all.xml`
- [NIST Cybersecurity News](https://www.nist.gov/cybersecurity) — feed: `https://www.nist.gov/news-events/cybersecurity/rss.xml`
- [Hacker News (AI Security)](https://news.ycombinator.com/) — feed: `https://hnrss.org/newest?q=%22AI+security%22+OR+%22prompt+injection%22+OR+%22LLM+vulnerability%22&points=20`

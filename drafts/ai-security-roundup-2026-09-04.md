---
title: "AI Security Trend Roundup — Sep 04, 2026"
description: "48 curated AI security updates from OWASP GenAI, arXiv, Simon Willison, CISA, and 4 more sources covering Aug 28–Sep 04. Every item credited to its original author."
keywords: "AI security, LLM security, prompt injection, agentic AI, GenAI threats, AI vulnerabilities, AI red team"
date: "2026-09-04"
slug: "ai-security-roundup-2026-09-04"
author: "FixTheVuln Team"
sources: "OWASP GenAI Security Project, Simon Willison, arXiv cs.CR, Protect AI, Google Project Zero, CISA, NIST, Hacker News"
cta_section: "comptia"
---

# AI Security Trend Roundup — Sep 04, 2026

*Covering Aug 28 → Sep 04, 2026. 48 new items from 8 tracked sources.*

> This digest credits every source by name and links directly to each original post. Editorial curation by FixTheVuln — all rights and attribution belong to the original authors.

## Standards & Frameworks

- **[OWASP GenAI Security Project Unveils 2026 Top 10 for LLM Applications, New Agent Control Standard and Sponsors as Community Tops 30,000 Members](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/?utm_source=rss&utm_medium=rss&utm_campaign=owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members)**  
  Source: [OWASP GenAI Security Project](https://genai.owasp.org/) — Sep 02
  OWASP GenAI Security Project Releases 2026 Top 10 for LLM Applications, Debuts Agent Control Standard and New Resources for Securing Generative and Agentic AI F5, WitnessAI, Evoke Security and Mondoo Inc. join as new sponsors as community expands AI security solutions guidance an


## Academic & Research

- **[A Public-Key-Dependent Adversarial-Deletion Ceiling for Fixed-Alphabet Multi-Bit Pseudorandom Codes](https://arxiv.org/abs/2609.02943)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.02943v1 Announce Type: new Abstract: A pseudorandom code (PRC) is a keyed error-correcting code whose codewords are computationally indistinguishable from uniform strings. We study public-key PRCs over fixed alphabets against adversarial deletions, where the deletion c

- **[Privacy-Preserving Heterogeneous Multi-LLM Federated Inference for Cognitive Diagnosis](https://arxiv.org/abs/2609.02947)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.02947v1 Announce Type: new Abstract: Significant challenges remain in AI-driven educational systems in balancing privacy preservation with accurate cognitive diagnosis. To overcome this, we propose a federated inference framework in which several commercial LLM APIs co

- **[PrivateHub: Contrastive Diffusion Model for Private Sensor-Intensive Environment Data Generation](https://arxiv.org/abs/2609.02958)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.02958v1 Announce Type: new Abstract: Sensor-intensive environments enable many intelligent services by inferring user applications from heterogeneous data streams. However, not all applications should be exposed: users want some activities to stay private. This creates

- **[When Optimization Becomes Manipulation: Defending Generative Search against Malicious Generative Engine Optimization](https://arxiv.org/abs/2609.02964)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.02964v1 Announce Type: new Abstract: This paper focuses on defending generative search engines against malicious Generative Engine Optimization (GEO), which rewrites web documents to match engines' citation preferences and thereby manipulates generated answers. Recent 

- **[Privacy-Preserving Topology-Guided Safety for LLM-Based Multi-Agent Systems via Federated Graph Learning](https://arxiv.org/abs/2609.02967)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.02967v1 Announce Type: new Abstract: Topology-guided safeguards for LLM-based multi-agent systems (MAS) train a GNN over the inter-agent communication graph to localize risky agents and intervene on the topology---but they assume one operator can pool all labeled trace

- **[Privacy Leakage in Federated Learning: Gradient-Based Client Identity Inference and Defenses for Inertial Sensing in Vehicular Edge Networks](https://arxiv.org/abs/2609.02971)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.02971v1 Announce Type: new Abstract: As vehicular networks move toward 5G/6G edge intelligence, federated learning (FL) is widely promoted as a privacy-preserving way for vehicles and infrastructure to train shared models without exposing raw sensor data. Yet the updat

- **[Trust Me, I'm Your Developer: Self-Issued Authentication in Large Language Models](https://arxiv.org/abs/2609.03247)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.03247v1 Announce Type: new Abstract: Large language model (LLM) security has largely focused on role-playing jailbreaks, with less attention to what happens when a user asks an LLM to verify an identity claim through a test designed by the model itself. We study this b

- **[Spruce: Scalable Private Outsourced Retrieval Using Compact Embeddings](https://arxiv.org/abs/2609.03376)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.03376v1 Announce Type: new Abstract: Retrieval-Augmented Generation (RAG) has made dense retrieval over large document collections a standard building block. Organizations increasingly outsource vector indexes to untrusted clouds, exposing proprietary corpora and user 

- **[Privacy, Robustness, and Fairness Trade-offs in Federated Intrusion Detection: Geometric Indistinguishability at the Aggregation Interface](https://arxiv.org/abs/2609.03420)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.03420v1 Announce Type: new Abstract: Federated learning enables privacy-conscious collaboration for network intrusion detection without centralizing sensitive traffic data, yet its deployment in operational environments must simultaneously satisfy three competing requi

- **[AlcaTRAz - Anchored Tree-Rule Defense Against Jailbreaks](https://arxiv.org/abs/2609.03693)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.03693v1 Announce Type: new Abstract: Large language models (LLMs) are vulnerable to jailbreak attacks that bypass safety alignment through carefully crafted prompts. Many existing defenses require access to model weights or internals, making them difficult to apply to 

- **[Rent-a-RAG: Embedding-Space Watermarks for Auditing Third-Party RAG](https://arxiv.org/abs/2609.03749)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.03749v1 Announce Type: new Abstract: Third-party retrieval-augmented generation (RAG) marketplaces create a new auditing problem: data providers may license corpora to a RAG operator, yet later have no visibility into whether their documents are being reused without co

- **[Inferring Hidden User Models from the Behavior of Personalized LLM Agents](https://arxiv.org/abs/2609.03815)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 04
  arXiv:2609.03815v1 Announce Type: new Abstract: Recent personalized LLM agents increasingly transform information retained in memory into compressed or structured representations, which we call user models, to guide later decisions. When source wording is removed from the state r


## Prompt Injection & LLM Security

- **[August newsletter is out](https://simonwillison.net/2026/Sep/4/august-newsletter/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 04
  The August edition of my sponsors-only monthly newsletter is out. If you are a sponsor (or if you start a sponsorship now) you can access it here. This month: We got more details on OpenAl's accidental cyberattacks One-shotting Raccoon Heist games with Fable 5 and Sol 5.6 Claude 

- **[GPT‑6 Astra](https://simonwillison.net/2026/Sep/3/gpt6-astra/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 03
  GPT‑6 Astra GPT-6 Astra is "rolling out today to a limited set of organizations and over the coming days will become available to all ChatGPT Plus, Pro, Business, and Enterprise users, as well as through the OpenAI API and AWS" - I've not tried it yet myself, so I don't have a gr

- **[llm-gemini 0.34](https://simonwillison.net/2026/Sep/2/llm-gemini/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 02
  Release: llm-gemini 0.34 New model gemini-3.8-flash for Gemini 3.8 Flash, with low, medium and high thinking levels. #146 Fixed async responses failing to record the resolved model version. Thanks, Charlie Tonneslan. #137 Google released Gemini 3.8 Flash (and 3.8 Flash Cyber, but

- **[Claude's new system prompt really doesn't want to reproduce song lyrics](https://simonwillison.net/2026/Sep/2/claudes-new-system-prompt/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 02
  Anthropic publish the system prompts for their Claude consumer applications (Claude.ai and the Claude mobile apps - sadly not for Claude Cowork or Claude Code). I love that they do this, and that they share not just the current prompts but historic changes to their prompts as wel

- **[Quoting Rick Brewster](https://simonwillison.net/2026/Sep/2/rick-brewster/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 02
  Direct2D has always been the biggest hurdle for Paint.NET on WINE, and it's clear that it will never be completed enough for Paint.NET's use. And I can't just "disable" the use of Direct2D. So, instead, Paint.NET now has an internal, from-scratch, clean-room reverse-engineered re

- **[Claude Fable 5.1 made me a really nice animated pelican](https://simonwillison.net/2026/Sep/1/claude-fable-5-1/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 01
  Today is Claude Fable (and Mythos) 5.1 day. Anthropic say that Fable 5.1 "sets a new standard for coding, knowledge work, and long-running problem-solving tasks". Their announcement spends a notable amount of time on scientific research, boasting of a 52.6% score on the brand new

- **[Codex bundles LibreOffice](https://simonwillison.net/2026/Sep/1/codex-libreoffice/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 01
  I was poking around in my ~/.cache/ folder using OmniDiskSweeper when I spotted something interesting. The OpenAI Codex desktop app (since rebranded to just ChatGPT) has 1.7GB of stuff in there in a folder called codex-primary-runtime, including a full Python installation, a full

- **[GeoJSON Map Viewer](https://simonwillison.net/2026/Sep/1/geojson/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 01
  Tool: GeoJSON Map Viewer I was helping Natalie gather some maps of local political boundaries (for the Granada Community Services District and the Midcoast Community Council) and found a need to display some GeoJSON files on a map and export that as a PNG. I asked GPT-5.6-Sol for

- **[Quoting Tarn Adams](https://simonwillison.net/2026/Sep/1/tarn-adams/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 01
  They took the letters from me! I have to talk about dwarf behavior now. I can't even talk about dwarf AI. It doesn't exist. It's dwarf behavior, and they misbehave sometimes &mdash; Tarn Adams, co-creator of Dwarf Fortress Tags: ai, game-design

- **[datasette-mcp 0.2](https://simonwillison.net/2026/Sep/1/datasette-mcp/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 01
  Release: datasette-mcp 0.2 "rows" from execute_sql is now an array of objects. Previously it was an array of arrays. This should help weaker models avoid losing track of which positional array element maps to which column. #1 Now depends on mcp>=2.1.1. This is the first non-alpha

- **[Python 3.15.0 candidate 2 is here!](https://simonwillison.net/2026/Sep/1/python-315-rc-2/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 01
  Python 3.15.0 candidate 2 is here! Hugo van Kemenade (release manager for Python 3.14 and 3.15) announces the final release candidate for Python 3.15, scheduled for release in October: Entering the release candidate phase, only reviewed code changes which are clear bug fixes are 

- **[Introducing wrapture](https://simonwillison.net/2026/Aug/31/introducing-wrapture/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Aug 31
  Introducing wrapture New from Graham Dumpleton (of wrapt, mod_wsgi, and New Relic's Python agent fame), who describes Wrapture as taking the monkeypatching ideas from wrapt and extending them to apply to testing and tracing at the same time. Wrapture (full documentation here) mak

- **[Quoting Andrew Digby](https://simonwillison.net/2026/Aug/31/andrew-digby/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Aug 31
  325 #kakapo! The chicks from this year's record breeding season are now juveniles and so have been added to the population. In 1995 there were just 51 kākāpō left. Recovery of critically endangered species is possible with sustained effort. &mdash; Andrew Digby, providing the bes

- **[Understanding ChatGPT Work](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Aug 30
  OpenAI announced ChatGPT Work on July 9th, and have been furiously iterating on it ever since. It is an extraordinarily confusing and very powerful product. Here's what I've figured out about it so far. ChatGPT Work is actually two products The more interesting version of ChatGPT

- **[Introducing Hy4 Preview](https://simonwillison.net/2026/Aug/29/hy4/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Aug 29
  Introducing Hy4 Preview New open weight text input (no vision) LLM from Chinese company Tencent today: 770B total parameters, 49B active parameters, 1M token context window, 1.56TB on Hugging Face. This is a big size increase from their previous Hy3 in July, which was 295B, 21B a


## Community Signal

- **[Corporate America is getting hooked on open-source AI](https://www.nytimes.com/2026/09/04/technology/open-source-ai-anthropic-openai.html)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 04
  Article URL: https://www.nytimes.com/2026/09/04/technology/open-source-ai-anthropic-openai.html Comments URL: https://news.ycombinator.com/item?id=49566137 Points: 114 # Comments: 80

- **[Meta new layoff goal of 60% to AI after moving 30% engineers to labelers](https://blog.pragmaticengineer.com/the-pulse-meta-wanted-to-reduce-teams-by-60-because-of-ai/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 04
  Article URL: https://blog.pragmaticengineer.com/the-pulse-meta-wanted-to-reduce-teams-by-60-because-of-ai/ Comments URL: https://news.ycombinator.com/item?id=49563441 Points: 21 # Comments: 11

- **[Google AI Mode shows same products 21.6% more expensive than traditional search](https://productrise.app/blog/google-ai-mode-prefers-more-expensive-products)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 04
  Article URL: https://productrise.app/blog/google-ai-mode-prefers-more-expensive-products Comments URL: https://news.ycombinator.com/item?id=49563386 Points: 300 # Comments: 54

- **[OpenAI agents hijacked German website in previously undisclosed AI breakout](https://www.reuters.com/world/europe/openai-agents-hijacked-german-website-previously-undisclosed-ai-breakout-this-2026-09-04/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 04
  Article URL: https://www.reuters.com/world/europe/openai-agents-hijacked-german-website-previously-undisclosed-ai-breakout-this-2026-09-04/ Comments URL: https://news.ycombinator.com/item?id=49562744 Points: 88 # Comments: 2

- **[NYC mayor Mamdani imposes 1 year ban on AI for schools through 8th grade](https://www.nyc.gov/mayors-office/news/2026/09/mayor-mamdani-and-chancellor-samuels-put-students-first-with-nat)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://www.nyc.gov/mayors-office/news/2026/09/mayor-mamdani-and-chancellor-samuels-put-students-first-with-nat Comments URL: https://news.ycombinator.com/item?id=49558433 Points: 43 # Comments: 11

- **[Protecting Engineers' Skills in the AI Era](https://spectrum.ieee.org/ai-engineer-skills)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://spectrum.ieee.org/ai-engineer-skills Comments URL: https://news.ycombinator.com/item?id=49558302 Points: 35 # Comments: 22

- **[GLP-1s are being linked to fewer serious infections, including TB](https://gizmodo.com/ozempic-and-other-glp-1s-are-being-linked-to-fewer-serious-infections-including-tb-2000806796)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  https://web.archive.org/web/20260903235256/https://gizmodo.c... Comments URL: https://news.ycombinator.com/item?id=49558086 Points: 133 # Comments: 74

- **[Judge Tells RFK Jr. To Stop Using Fake AI Studies on Teen Pregnancy](https://newrepublic.com/post/215001/judge-rfk-jr-hhs-fake-ai-studies-teen-pregnancy)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://newrepublic.com/post/215001/judge-rfk-jr-hhs-fake-ai-studies-teen-pregnancy Comments URL: https://news.ycombinator.com/item?id=49553653 Points: 20 # Comments: 3

- **[Sanders introduces bill to ban artificial superintelligence and pause AI](https://www.sanders.senate.gov/press-releases/news-sanders-casar-introduce-legislation-to-ban-artificial-superintelligence-and-temporarily-pause-advanced-ai-development/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://www.sanders.senate.gov/press-releases/news-sanders-casar-introduce-legislation-to-ban-artificial-superintelligence-and-temporarily-pause-advanced-ai-development/ Comments URL: https://news.ycombinator.com/item?id=49553463 Points: 60 # Comments: 76

- **[Why office workers are turning against AI](https://www.bloodinthemachine.com/p/why-office-workers-are-turning-against)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://www.bloodinthemachine.com/p/why-office-workers-are-turning-against Comments URL: https://news.ycombinator.com/item?id=49553414 Points: 27 # Comments: 5

- **[Yes, no (built-in) AI is now a feature – LibreOffice blog](https://blog.documentfoundation.org/blog/2026/09/03/yes-no-ai-is-now-a-feature/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://blog.documentfoundation.org/blog/2026/09/03/yes-no-ai-is-now-a-feature/ Comments URL: https://news.ycombinator.com/item?id=49553350 Points: 33 # Comments: 6

- **[Launch HN: Mireye (YC S26) – Infrastructure for Physical World AI Agents](https://news.ycombinator.com/item?id=49552616)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Hi HN, I'm Ansh, founder of Mireye (https://www.mireye.com). I'm building the infrastructure AI agents use to make decisions about physical places: data, enrichment, tools, and signals for any US location, behind one API and MCP server.Here's a demo video: https://www.youtube.com

- **[OpenAI's new reasoning technique alarms AI safety experts](https://techcrunch.com/2026/09/02/openais-new-reasoning-technique-alarms-ai-safety-experts/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://techcrunch.com/2026/09/02/openais-new-reasoning-technique-alarms-ai-safety-experts/ Comments URL: https://news.ycombinator.com/item?id=49552395 Points: 39 # Comments: 19

- **[Porting my 1993 Amiga game to Godot, with an LLM reading the 68000 assembly](https://babyloniantwins.com/blog/porting-a-1993-amiga-game-to-godot/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  These are my notes from porting my Amiga game, which I originally built in Baghdad in 1993 in MC68000 assembly, to Godot, using Claude Fable 5 during last July holiday. It took an evening! Getting the feel right and shipping it took a few more weekends and evenings.I spent the la

- **[A dark horse enters China's AI race: StartLux](https://chinaonchina.com/article/chen-dawei-returns-enters-the-large-model-sector)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://chinaonchina.com/article/chen-dawei-returns-enters-the-large-model-sector Comments URL: https://news.ycombinator.com/item?id=49548530 Points: 54 # Comments: 29

- **[Kids go from curious to frustrated playing with AI-stuffed toys, UW study finds](https://www.geekwire.com/2026/kids-go-from-curious-to-frustrated-playing-with-ai-stuffed-toys-uw-study-finds/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://www.geekwire.com/2026/kids-go-from-curious-to-frustrated-playing-with-ai-stuffed-toys-uw-study-finds/ Comments URL: https://news.ycombinator.com/item?id=49547334 Points: 23 # Comments: 12

- **[No–AI Agents Did Not Build Secret Civilizations Stop Anthropomorphizing Malware](https://internetofbugs.substack.com/p/noai-agents-did-not-build-secret)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://internetofbugs.substack.com/p/noai-agents-did-not-build-secret Comments URL: https://news.ycombinator.com/item?id=49547073 Points: 20 # Comments: 6

- **[Go grandmaster Shin defeats AI KataGo with a two-stone handicap](https://www.kedglobal.com/artificial-intelligence/newsView/ked202607210007)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://www.kedglobal.com/artificial-intelligence/newsView/ked202607210007 Comments URL: https://news.ycombinator.com/item?id=49544762 Points: 435 # Comments: 169

- **[US gov sides with OpenAI on issue of training LLMs on copyrighted material](https://techcrunch.com/2026/09/02/u-s-government-sides-with-openai-on-issue-of-training-llms-on-copyrighted-material/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 03
  Article URL: https://techcrunch.com/2026/09/02/u-s-government-sides-with-openai-on-issue-of-training-llms-on-copyrighted-material/ Comments URL: https://news.ycombinator.com/item?id=49544650 Points: 49 # Comments: 21

- **[USPS Built an Untested, Undocumented Ballot-Blocking System Despite Injunction](https://www.techdirt.com/2026/09/02/whistleblower-usps-defied-a-court-injunction-to-build-an-untested-undocumented-ballot-blocking-system-its-own-staff-call-the-process-a-shit-show/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 02
  Article URL: https://www.techdirt.com/2026/09/02/whistleblower-usps-defied-a-court-injunction-to-build-an-untested-undocumented-ballot-blocking-system-its-own-staff-call-the-process-a-shit-show/ Comments URL: https://news.ycombinator.com/item?id=49543730 Points: 36 # Comments: 13


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

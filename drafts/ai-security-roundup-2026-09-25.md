---
title: "AI Security Trend Roundup — Sep 25, 2026"
description: "59 curated AI security updates from OWASP GenAI, arXiv, Simon Willison, CISA, and 4 more sources covering Sep 18–Sep 25. Every item credited to its original author."
keywords: "AI security, LLM security, prompt injection, agentic AI, GenAI threats, AI vulnerabilities, AI red team"
date: "2026-09-25"
slug: "ai-security-roundup-2026-09-25"
author: "FixTheVuln Team"
sources: "OWASP GenAI Security Project, Simon Willison, arXiv cs.CR, Protect AI, Google Project Zero, CISA, NIST, Hacker News"
cta_section: "comptia"
---

# AI Security Trend Roundup — Sep 25, 2026

*Covering Sep 18 → Sep 25, 2026. 59 new items from 8 tracked sources.*

> This digest credits every source by name and links directly to each original post. Editorial curation by FixTheVuln — all rights and attribution belong to the original authors.

## Academic & Research

- **[Stress-Testing Structure-Aware Calibration of Malware Graph Neural Networks under Type Shift](https://arxiv.org/abs/2609.28517)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28517v1 Announce Type: new Abstract: Post-hoc malware calibrators can condition confidence on graph structure, but their structural inputs may leave the support represented by validation data under malware-type shift. We study this risk on MalNet-Tiny by holding out ea

- **[An Exposition of GPT Astra's Proof of Lower Bound on DP Continual Counting](https://arxiv.org/abs/2609.28528)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28528v1 Announce Type: new Abstract: The goal of this note is to give a detailed proof, to the best of our understanding, of the recent presentation by Harrison and Leeman (arXiv:2609.17650v01 and arXiv:2609.17650v02) of the proof by Astra on the lower bound for differ

- **[Who Is Behind the Harness? Fingerprinting LLMs through Agentic Behavior](https://arxiv.org/abs/2609.28559)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28559v1 Announce Type: new Abstract: LLMs increasingly operate through coding-agent harnesses that inspect repositories, invoke tools, and modify files. Substituting the model behind such an agent can therefore change security-relevant decisions, including whether it v

- **[Don't Read the Log: Execution Traces Contaminate Verifiers in Video-Generation Agents](https://arxiv.org/abs/2609.28564)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28564v1 Announce Type: new Abstract: Agentic video-generation systems close a loop between a generator and a verifier: an LLM plans shots, calls a text-to-video model, and a multimodal judge decides whether the result satisfies the request. To diagnose where a long wor

- **[Where Cyber Agents Struggle: Bottleneck Analysis of Multi-Stage LLM Agents](https://arxiv.org/abs/2609.28572)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28572v1 Announce Type: new Abstract: Multi-stage LLM-based cyber agents may complete attack workflows while remaining brittle, costly, or reliant on incorrect interpretations of execution evidence. Success rates alone obscure inefficiency, adaptation through retries, a

- **[Persistent Billable State: Denial-of-Wallet Attacks and Defenses in Tool-Calling LLM Agents](https://arxiv.org/abs/2609.28585)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28585v1 Announce Type: new Abstract: Multi-step tool-calling LLM agents rely on host runtimes to preserve state across turns. When a runtime carries an external tool return into later model inputs, providers meter it again. An admitted malicious or compromised tool can

- **[Agent Approval Laundering: Transitive Effects Beyond the Approved Invocation](https://arxiv.org/abs/2609.28586)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28586v1 Announce Type: new Abstract: Coding-agent approval interfaces bind a human decision to a command or tool call, while developer tools execute the transitive workflow that invocation activates. Package installation can run lifecycle hooks and write files; an MCP 

- **[Decision Hijacking: Prompt Injection Attacks on Jev's Typed Probabilistic Decisions](https://arxiv.org/abs/2609.28613)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28613v1 Announce Type: new Abstract: Most studies of prompt injection focus on generative agents, leaving their effects on models with schema-defined outputs unclear. We examine these effects in Jev, a non-generative decision model, using 510 reconstructed InjecAgent c

- **[Unmasking Shortcut Learning in IoT Intrusion Detection: A Forensic, Multi-Paradigm Evaluation of Feature Dependence and Data Leakage](https://arxiv.org/abs/2609.28725)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28725v1 Announce Type: new Abstract: Machine learning-based Network Intrusion Detection Systems often report near-perfect performance on IoT benchmarks. However, whether these models learn generalizable attack behavior or exploit spurious dataset shortcuts- such as sta

- **[Blockchain-Enabled Artificial Intelligence and AI Agents for Secure Data Sharing and Cybersecurity Applications](https://arxiv.org/abs/2609.28843)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28843v1 Announce Type: new Abstract: Blockchain and artificial intelligence (AI) are converging into a single infrastructural layer for securing data sharing, model integrity, and autonomous decision-making across distributed systems. This paper presents a meta-synthes

- **[Codetta: High-Capacity, Keyless, and Undetectable Multi-Agent Collusion](https://arxiv.org/abs/2609.28900)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28900v1 Announce Type: new Abstract: Multi-agent systems built on large language models (LLMs) are increasingly deployed in high-stakes settings such as finance, healthcare, and software engineering, where agents coordinate through natural-language messages. The same c

- **[On the Effectiveness of Kernel-Level Evidence for Agent Security](https://arxiv.org/abs/2609.28915)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28915v1 Announce Type: new Abstract: LLM agents are deployed into infrastructure that grants them broad host authority, yet existing agent-security benchmarks and defenses operate almost exclusively at the application telemetry layer: the served tool manifest, the user

- **[Calibrated Decision Models for Autonomous Penetration-Testing Harnesses: JEV and Laya as System One Decision Layers for LLM-Driven Pentest Agents](https://arxiv.org/abs/2609.28940)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28940v1 Announce Type: new Abstract: Autonomous penetration-testing harnesses use large language models (LLMs) for reconnaissance, exploitation, and reporting, but often rely on those same models to confirm findings, grade severity, and select agents. This can lead to 

- **[DistillGuard: Malicious NPM Package Detection and API Attack Chain Analysis via Static Graph and LLM Distillation](https://arxiv.org/abs/2609.28996)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.28996v1 Announce Type: new Abstract: The Node.js ecosystem heavily relies on NPM packages, and software supply chain attacks targeting malicious NPM packages are rampant. Malicious code primarily triggers during package installation, import, and runtime. Traditional st

- **[ClaimMirage: When Self-Claims in Domain Names Change LLM Threat Judgments](https://arxiv.org/abs/2609.29130)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Sep 25
  arXiv:2609.29130v1 Announce Type: new Abstract: Short claims such as not-phishing or official can change how a large language model (LLM) judges a domain name, without explicit prompt-injection commands. We study this manipulation as ClaimMirage: a name under inspection claims it


## Prompt Injection & LLM Security

- **[Quoting John Gruber](https://simonwillison.net/2026/Sep/25/john-gruber/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 25
  Muse is getting a lot of attention — including mine — because it’s both groundbreaking technically (each user gets their own entire persistent Linux VM running in Meta’s cloud) and because it’s packaged in an easy-to-install easy-to-use way. It’s literally presented as a cute mas

- **[Northern Gannet, Great Blue Heron, California Brown Pelican](https://simonwillison.net/2026/Sep/25/sighting-403293902/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 25
  Northern Gannet, Great Blue Heron, California Brown Pelican, in Monterey Bay National Marine Sanctuary, CA, US, CANew 200-800mm Canon EF lens got me my best photo of Morris yet. They really like hanging out under that sign in the harbor! Tags: photography, wildlife

- **[Note on 24th September 2026](https://simonwillison.net/2026/Sep/24/harder/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 24
  The more time I spend working with coding agents, the more convinced I am that they make software engineering even harder. We can do amazing things with them, but unlocking their full potential requires extraordinary discipline and knowledge. Tags: coding-agents, ai, llms

- **[commit-rewriter 0.2](https://simonwillison.net/2026/Sep/24/commit-rewriter/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 24
  Release: commit-rewriter 0.2 Support for branches other than the default branch. Use uvx commit-rewriter --branch other to run against another branch. #3 Tags: git

- **[datasette 1.0a41](https://simonwillison.net/2026/Sep/24/datasette/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 24
  Release: datasette 1.0a41 Alec Garcia added support for OpenTelemetry to Datasette in this release. I've also refactored all of Datasette's modal dialogs to a single Web Component, which is now documented for other plugins to use. Tags: javascript, datasette, web-components, alex

- **[Gemini 3.8 TTS Playground](https://simonwillison.net/2026/Sep/23/gemini-tts-playground/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 23
  Tool: Gemini 3.8 TTS Playground Google released two new Gemini text-to-speech models today - gemini-3.8-flash-tts and gemini-3.8-flash-lite-tts. They come with a library of over 2,000 voices, plus the ability to create a custom voice with "just a 30-second audio sample of your vo

- **[Shadow roots, explained with live examples](https://simonwillison.net/2026/Sep/23/shadow-roots/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 23
  Tool: Shadow roots, explained with live examples Prompt to Fable 5.1 Medium: Build an artifact to explain shadow roots in CSS with interactive examples Tags: css

- **[SF October 14th: A Birds of a Feather Session on Agentic Engineering](https://simonwillison.net/2026/Sep/23/bof-agentic-engineering/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 23
  SF October 14th: A Birds of a Feather Session on Agentic Engineering I'm hosting an evening event with Jesse Vincent in San Francisco on Wednesday 14th October for people who are building weird and interesting things with and on top of coding agents. Think of it as an agentic sho

- **[Claude Opus 5.5, GPT-6 Sol, GPT-6 Luna, and a new price war](https://simonwillison.net/2026/Sep/22/opus-and-sol-and-luna/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 22
  Yesterday was Grok 4.7 (pelicans) and MiMo v2.6 Flash/Pro (more pelicans). Today Anthropic released Claude Opus 5.5, and around an hour later OpenAI released GPT-6 Sol and GPT-6 Luna. It's going to take a while to get a good read on all of these new models, but here are my impres

- **[llm 0.36](https://simonwillison.net/2026/Sep/22/llm/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 22
  Release: llm 0.36 New OpenAI models: gpt-6-sol for GPT-6 Sol and gpt-6-luna for GPT-6 Luna. #1702 Model plugins can now declare supports_conversation = False for models that only accept single-turn prompts. LLM raises llm.ConversationNotSupported when these models receive assista

- **[Quoting @therealcornpop](https://simonwillison.net/2026/Sep/22/therealcornpop/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 22
  Hey, you know it's like super obvious if you're using AI to write your scripts for TikTok and YouTube, right? [...] It's not just the general AI-isms of "it's not X, it's Y", or the rule of three, or the really weird broken staccato-like way of writing where you just say a lot of

- **[llm-anthropic 0.29](https://simonwillison.net/2026/Sep/22/llm-anthropic/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 22
  Release: llm-anthropic 0.29 Adds support for Claude Opus 5.5: llm -m claude-opus-5.5 "prompt goes here" Tags: llm, anthropic

- **[llm-typesafe 0.1a0](https://simonwillison.net/2026/Sep/22/llm-typesafe/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 22
  Release: llm-typesafe 0.1a0 I built this new plugin for LLM to add support for TypeSafe AI's new Jev model. Install it like this: llm install llm-typesafe Then set an API key (get one here, the waitlist seems to move pretty fast): llm keys set typesafe # Paste key And now you can

- **[Jev introduces a new shape of LLM - System One, aka Decision Models](https://simonwillison.net/2026/Sep/21/jev/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 21
  Last week TypeSafe AI unveiled Jev, their first example of a new category of model that they are calling "System One models" (I'm with Maggie Appleton, I think "decision models" is a better name for these). Jev is an interesting variant on the usual LLM format: it still accepts t

- **[Cloudflare Python Workers are now generally available](https://simonwillison.net/2026/Sep/21/cloudflare-python-worker/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 21
  Cloudflare Python Workers are now generally available After a two year preview, Cloudflare's support for running Python code in their server-side Workers platform is now stable: "Python is now a first-class, fully supported language on the Cloudflare Developer Platform". A neat t

- **[Quoting voxium](https://simonwillison.net/2026/Sep/20/voxium/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 20
  It has been half a month since I started a new role at a big company. Nobody knows anything here. The specs, code, tests, PRDs, tickets, resolution of those tickets, reports, etc., everything is made by Claude Code. Nobody on my team likes this. They are being forced to ship as m

- **[MCP was always a bad idea?](https://simonwillison.net/2026/Sep/20/hn-49779718/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 20
  My comment on MCP was always a bad idea? &mdash; Hacker News.This article entirely misses the value that MCP brings today. Sure, there's almost no reason to use MCPs if you are running a full-blown terminal agent (Claude Code, Codex, Meta Muse, OpenClaw etc) with unfettered inter

- **[llm-keys-ui 0.1](https://simonwillison.net/2026/Sep/20/llm-keys-ui/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 20
  Release: llm-keys-ui 0.1 This plugin solves a very specific problem. I've started using Codex Remote to run coding agents on various machines while controlling them from my phone. Sometimes I use those machines to hack on LLM projects, and occasionally that means I need to config

- **[datasette-explain 0.2.2](https://simonwillison.net/2026/Sep/20/datasette-explain/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 20
  Release: datasette-explain 0.2.2 Explain plans now work on read-only stored-query pages. I upgraded datasette.simonwillison.net to Datasette 1.0a40, which inspired me to ship a new version of this explain plugin. Tags: sqlite, datasette

- **[datasette-auth-github 1.0](https://simonwillison.net/2026/Sep/19/datasette-auth-github/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 19
  Release: datasette-auth-github 1.0 I run this GitHub login plugin on the agent.datasette.io demo site and I noticed that my authenticated sessions weren't lasting very long. It turned out that the plugin was setting cookies without a Max-Age parameter, so they were expiring at th

- **[California Sea Lion, Brandt's Cormorant](https://simonwillison.net/2026/Sep/19/sighting-401567341/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 19
  California Sea Lion, Brandt&#x27;s Cormorant, in Pillar Point Harbor, CA, USI only noticed this after I had taken the photo: Morris the Northern Gannet is peeking out from behind the base of the sign. Tags: wildlife

- **[Gemini Hacked Three Companies in First Known Breakout by Google’s AI](https://simonwillison.net/2026/Sep/18/gemini-hacked-three-companies/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 18
  Gemini Hacked Three Companies in First Known Breakout by Google’s AI Gemini finally caught up on Felony Bench! The hacks, which the company confirmed on Friday, occurred in May as part of a test run by the company Irregular, which was also involved in similar incidents disclosed 

- **[Note on 18th September 2026](https://simonwillison.net/2026/Sep/18/probably-gonna-eat-you/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 18
  Being a computer scientist who refuses to find anything about LLMs interesting right now is a bit like being a geneticist who refuses to find anything interesting about the recently opened Jurassic Park. Skeptical geneticist: "pfft, it's just frog DNA. And they deliberately let t

- **[Quoting Thariq Shihipar](https://simonwillison.net/2026/Sep/18/thariq-shihipar/)**  
  Source: [Simon Willison](https://simonwillison.net/) — Sep 18
  We're adding support for AGENTS.md to Claude Code. Starting today in version 2.1.277, if there is no CLAUDE.md in a folder, Claude will check for and use AGENTS.md. AGENTS.md support is built off of Claude Code mods, our upcoming way to customize the Claude Code harness. This is 


## Community Signal

- **[Classified Estimates Show the NSA Is Paying Billions to Test AI Models](https://www.washingtonsun.com/technology/classified-estimates-nsa-paying-billions-to-test-ai-models)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 25
  Article URL: https://www.washingtonsun.com/technology/classified-estimates-nsa-paying-billions-to-test-ai-models Comments URL: https://news.ycombinator.com/item?id=49845952 Points: 131 # Comments: 69

- **[Microsoft Abandons Personal AI Chatbot Race with Copilot Reboot](https://www.bloomberg.com/news/articles/2026-09-25/microsoft-abandons-personal-ai-chatbot-race-with-copilot-reboot)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 25
  Article URL: https://www.bloomberg.com/news/articles/2026-09-25/microsoft-abandons-personal-ai-chatbot-race-with-copilot-reboot Comments URL: https://news.ycombinator.com/item?id=49844896 Points: 57 # Comments: 46

- **[Uproar in France over award-winning author accused of using AI](https://www.bbc.com/news/articles/ck7v4y45893go)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 25
  Article URL: https://www.bbc.com/news/articles/ck7v4y45893go Comments URL: https://news.ycombinator.com/item?id=49842707 Points: 31 # Comments: 80

- **[Using LLMs to trace alchemical knowledge and decode 17th century letters](https://resobscura.substack.com/p/ai-labs-need-to-start-funding-historical)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://resobscura.substack.com/p/ai-labs-need-to-start-funding-historical Comments URL: https://news.ycombinator.com/item?id=49835531 Points: 161 # Comments: 39

- **[The AI Build-Out Is Becoming the Biggest Economic Bet in U.S. History](https://www.wsj.com/economy/the-ai-build-out-is-becoming-the-biggest-economic-bet-in-u-s-history-c60716dd)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://www.wsj.com/economy/the-ai-build-out-is-becoming-the-biggest-economic-bet-in-u-s-history-c60716dd Comments URL: https://news.ycombinator.com/item?id=49833264 Points: 23 # Comments: 11

- **[Oracle invokes force majeure on New Mexico AI data center](https://qz.com/oracle-force-majeure-new-mexico-ai-data-center-092426)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://qz.com/oracle-force-majeure-new-mexico-ai-data-center-092426 Comments URL: https://news.ycombinator.com/item?id=49832564 Points: 28 # Comments: 1

- **[I Have a Confession: I Built This Site with AI – Please Forgive Me](https://dynamicallytyped.org/blog/i-have-a-confession-i-built-this-site-with-ai)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://dynamicallytyped.org/blog/i-have-a-confession-i-built-this-site-with-ai Comments URL: https://news.ycombinator.com/item?id=49832491 Points: 43 # Comments: 48

- **[Tutoring company tells parents to save their money and 'use AI instead'](https://www.afr.com/policy/health-and-education/tutoring-company-tell-parents-to-save-their-money-and-use-ai-instead-20260923-p60z0r)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://www.afr.com/policy/health-and-education/tutoring-company-tell-parents-to-save-their-money-and-use-ai-instead-20260923-p60z0r Comments URL: https://news.ycombinator.com/item?id=49831690 Points: 131 # Comments: 205

- **[AI safety is mostly a sex cult in Berkeley](https://www.verysane.ai/p/ai-safety-is-mostly-a-sex-cult-in)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://www.verysane.ai/p/ai-safety-is-mostly-a-sex-cult-in Comments URL: https://news.ycombinator.com/item?id=49831269 Points: 119 # Comments: 30

- **[Best LLM for every budget, updated daily](https://bestmodelforyourbudget.terrydjony.com/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://bestmodelforyourbudget.terrydjony.com/ Comments URL: https://news.ycombinator.com/item?id=49830866 Points: 180 # Comments: 110

- **['That's so AI ' What gen Alpha's biggest insult tells us](https://www.theguardian.com/society/2026/sep/24/thats-so-ai-what-gen-alphas-biggest-insult-tells-us)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://www.theguardian.com/society/2026/sep/24/thats-so-ai-what-gen-alphas-biggest-insult-tells-us Comments URL: https://news.ycombinator.com/item?id=49829650 Points: 190 # Comments: 289

- **[AI has no intent and no motivation](https://www.i-programmer.info/news/245-view-point/19164-ai-has-no-motivation.html)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://www.i-programmer.info/news/245-view-point/19164-ai-has-no-motivation.html Comments URL: https://news.ycombinator.com/item?id=49828133 Points: 48 # Comments: 61

- **[Meta takes down a critical video about meta AI Glasses after filming at Meta](https://www.reddit.com/r/facebook/comments/1wotwrk/meta_takes_down_a_critical_video_about_meta_ai/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://www.reddit.com/r/facebook/comments/1wotwrk/meta_takes_down_a_critical_video_about_meta_ai/ Comments URL: https://news.ycombinator.com/item?id=49827794 Points: 620 # Comments: 376

- **[Early rogue AI agent activity and attempts to hack found on urlquery.net](https://transluce.org/agent-activity)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://transluce.org/agent-activity Comments URL: https://news.ycombinator.com/item?id=49826565 Points: 263 # Comments: 299

- **[Nori LLM: Achieving Over 1M tok / s](https://noriagentic.com/nori-llm.html)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://noriagentic.com/nori-llm.html Comments URL: https://news.ycombinator.com/item?id=49826163 Points: 24 # Comments: 3

- **[Ask HN: I just talked to an AI-obsessed client, and I need a shower afterwards](https://news.ycombinator.com/item?id=49826029)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Just to preface, this isn't the typical "Am I being replaced by vibe coding" post.I just had a talk with one of my first ongoing clients, who sort of helped me kickstart my freelancing "career". He is one of those people who has a broad understanding of the tech out there, and wh

- **[Feds Target AI Critics as "Foreign Agents"](https://www.kenklippenstein.com/p/feds-think-ai-critics-are-foreign)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 24
  Article URL: https://www.kenklippenstein.com/p/feds-think-ai-critics-are-foreign Comments URL: https://news.ycombinator.com/item?id=49824686 Points: 384 # Comments: 442

- **[Stanford violated AI policy after race-swapping students in ad](https://www.sfchronicle.com/bayarea/article/stanford-ai-policy-student-photo-race-swapping-22444142.php)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 23
  Article URL: https://www.sfchronicle.com/bayarea/article/stanford-ai-policy-student-photo-race-swapping-22444142.php Comments URL: https://news.ycombinator.com/item?id=49824061 Points: 33 # Comments: 19

- **[Mercury 2.5 LLM hits 770 tokens per second](https://artificialanalysis.ai/models/mercury-2-5)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 23
  Article URL: https://artificialanalysis.ai/models/mercury-2-5 Comments URL: https://news.ycombinator.com/item?id=49823348 Points: 148 # Comments: 92

- **[Surprise, Meta's latest AI gimmick is just underpaid humans](https://www.avclub.com/meta-muse-ai-human-labor)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Sep 23
  Article URL: https://www.avclub.com/meta-muse-ai-human-labor Comments URL: https://news.ycombinator.com/item?id=49822903 Points: 44 # Comments: 10


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

---
title: "AI Security Trend Roundup — Apr 24, 2026"
description: "61 curated AI security updates from OWASP GenAI, arXiv, Simon Willison, CISA, and 4 more sources covering Apr 17–Apr 24. Every item credited to its original author."
keywords: "AI security, LLM security, prompt injection, agentic AI, GenAI threats, AI vulnerabilities, AI red team"
date: "2026-04-24"
slug: "ai-security-roundup-2026-04-24"
author: "FixTheVuln Team"
sources: "OWASP GenAI Security Project, Simon Willison, arXiv cs.CR, Protect AI, Google Project Zero, CISA, NIST, Hacker News"
cta_section: "comptia"
---

# AI Security Trend Roundup — Apr 24, 2026

*Covering Apr 17 → Apr 24, 2026. 61 new items from 8 tracked sources.*

> This digest credits every source by name and links directly to each original post. Editorial curation by FixTheVuln — all rights and attribution belong to the original authors.

## Academic & Research

- **[Towards a Systematic Risk Assessment of Deep Neural Network Limitations in Autonomous Driving Perception](https://arxiv.org/abs/2604.20895)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.20895v1 Announce Type: new Abstract: Safety and security are essential for the admission and acceptance of automated and autonomous vehicles. Deep neural networks (DNNs) are widely used for perception and further components of the autonomous driving (AD) stack. However

- **[Sensitivity Uncertainty Alignment in Large Language Models](https://arxiv.org/abs/2604.20903)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.20903v1 Announce Type: new Abstract: We propose Sensitivity-Uncertainty Alignment (SUA), a framework for analyzing failures of large language models under adversarial and ambiguous inputs. We argue that adversarial sensitivity and ambiguity reflect a common issue: misa

- **[Omission Constraints Decay While Commission Constraints Persist in Long-Context LLM Agents](https://arxiv.org/abs/2604.20911)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.20911v1 Announce Type: new Abstract: LLM agents deployed in production operate under operator-defined behavioral policies (system-prompt instructions such as prohibitions on credential disclosure, data exfiltration, and unauthorized output) that safety evaluations assu

- **[SafeRedirect: Defeating Internal Safety Collapse via Task-Completion Redirection in Frontier LLMs](https://arxiv.org/abs/2604.20930)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.20930v1 Announce Type: new Abstract: Internal Safety Collapse (ISC) is a failure mode in which frontier LLMs, when executing legitimate professional tasks whose correct completion structurally requires harmful content, spontaneously generate that content with safety fa

- **[Adaptive Defense Orchestration for RAG: A Sentinel-Strategist Architecture against Multi-Vector Attacks](https://arxiv.org/abs/2604.20932)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.20932v1 Announce Type: new Abstract: Retrieval-augmented generation (RAG) systems are increasingly deployed in sensitive domains such as healthcare and law, where they rely on private, domain-specific knowledge. This capability introduces significant security risks, in

- **[SDNGuardStack: An Explainable Ensemble Learning Framework for High-Accuracy Intrusion Detection in Software-Defined Networks](https://arxiv.org/abs/2604.20934)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.20934v1 Announce Type: new Abstract: Software-Defined Networking (SDN) is another technology that has been developing in the last few years as a relevant technique to improve network programmability and administration. Nonetheless, its centralized design presents a maj

- **[Breaking Bad: Interpretability-Based Safety Audits of State-of-the-Art LLMs](https://arxiv.org/abs/2604.20945)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.20945v1 Announce Type: new Abstract: Effective safety auditing of large language models (LLMs) demands tools that go beyond black-box probing and systematically uncover vulnerabilities rooted in model internals. We present a comprehensive, interpretability-driven jailb

- **[Breaking MCP with Function Hijacking Attacks: Novel Threats for Function Calling and Agentic Models](https://arxiv.org/abs/2604.20994)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.20994v1 Announce Type: new Abstract: The growth of agentic AI has drawn significant attention to function calling Large Language Models (LLMs), which are designed to extend the capabilities of AI-powered system by invoking external functions. Injection and jailbreaking

- **[Behavioral Consistency and Transparency Analysis on Large Language Model API Gateways](https://arxiv.org/abs/2604.21083)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.21083v1 Announce Type: new Abstract: Third-party Large Language Model (LLM) API gateways are rapidly emerging as unified access points to models offered by multiple vendors. However, the internal routing, caching, and billing policies of these gateways are largely undi

- **[Cross-Session Threats in AI Agents: Benchmark, Evaluation, and Algorithms](https://arxiv.org/abs/2604.21131)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.21131v1 Announce Type: new Abstract: AI-agent guardrails are memoryless: each message is judged in isolation, so an adversary who spreads a single attack across dozens of sessions slips past every session-bound detector because only the aggregate carries the payload. W

- **[Adaptive Instruction Composition for Automated LLM Red-Teaming](https://arxiv.org/abs/2604.21159)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.21159v1 Announce Type: new Abstract: Many approaches to LLM red-teaming leverage an attacker LLM to discover jailbreaks against a target. Several of them task the attacker with identifying effective strategies through trial and error, resulting in a semantically limite

- **[Strategic Heterogeneous Multi-Agent Architecture for Cost-Effective Code Vulnerability Detection](https://arxiv.org/abs/2604.21282)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.21282v1 Announce Type: new Abstract: Automated code vulnerability detection is critical for software security, yet existing approaches face a fundamental trade-off between detection accuracy and computational cost. We propose a heterogeneous multi-agent architecture in

- **[CI-Work: Benchmarking Contextual Integrity in Enterprise LLM Agents](https://arxiv.org/abs/2604.21308)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.21308v1 Announce Type: new Abstract: Enterprise LLM agents can dramatically improve workplace productivity, but their core capability, retrieving and using internal context to act on a user's behalf, also creates new risks for sensitive information leakage. We introduc

- **[Adversarial Evasion in Non-Stationary Malware Detection: Minimizing Drift Signals through Similarity-Constrained Perturbations](https://arxiv.org/abs/2604.21310)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.21310v1 Announce Type: new Abstract: Deep learning has emerged as a powerful approach for malware detection, demonstrating impressive accuracy across various data representations. However, these models face critical limitations in real-world, non-stationary environment

- **[CSC: Turning the Adversary's Poison against Itself](https://arxiv.org/abs/2604.21416)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.21416v1 Announce Type: new Abstract: Poisoning-based backdoor attacks pose significant threats to deep neural networks by embedding triggers in training data, causing models to misclassify triggered inputs as adversary-specified labels while maintaining performance on 

- **[A Stackelberg Model for Hybridization in Cryptography](https://arxiv.org/abs/2604.21436)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — Apr 24
  arXiv:2604.21436v1 Announce Type: new Abstract: Similar to a strategic interaction between rational and intelligent agents, cryptography problems can be examined through the prism of game theory. In this setting, the agent aiming to protect a message is called the defender, while


## Prompt Injection & LLM Security

- **[DeepSeek V4 - almost on the frontier, a fraction of the price](https://simonwillison.net/2026/Apr/24/deepseek-v4/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 24
  Chinese AI lab DeepSeek's last model release was V3.2 (and V3.2 Speciale) last December. They just dropped the first of their hotly anticipated V4 series in the shape of two preview models, DeepSeek-V4-Pro and DeepSeek-V4-Flash. Both models are 1 million token context Mixture of 

- **[Millisecond Converter](https://simonwillison.net/2026/Apr/24/milliseconds/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 24
  Tool: Millisecond Converter LLM reports prompt durations in milliseconds and I got fed up of having to think about how to convert those to seconds and minutes. Tags: tools

- **[It's a big one](https://simonwillison.net/2026/Apr/24/weekly/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 24
  This week's edition of my email newsletter (aka content from this blog delivered to your inbox) features 4 pelicans riding bicycles, 1 possum on an e-scooter, up to 5 raccoons with ham radios hiding in crowds, 5 blog posts, 8 links, 3 quotes and a new chapter of my Agentic Engine

- **[russellromney/honker](https://simonwillison.net/2026/Apr/24/honker/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 24
  russellromney/honker "Postgres NOTIFY/LISTEN semantics" for SQLite, implemented as a Rust SQLite extension and various language bindings to help make use of it. The design of this looks very solid. It lets you write Python code for queues that looks like this: import honker db = 

- **[An update on recent Claude Code quality reports](https://simonwillison.net/2026/Apr/24/recent-claude-code-quality-reports/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 24
  An update on recent Claude Code quality reports It turns out the high volume of complaints that Claude Code was providing worse quality results over the past two months was grounded in real problems. The models themselves were not to blame, but three separate issues in the Claude

- **[Serving the For You feed](https://simonwillison.net/2026/Apr/24/serving-the-for-you-feed/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 24
  Serving the For You feed One of Bluesky's most interesting features is that anyone can run their own custom "feed" implementation and make it available to other users - effectively enabling custom algorithms that can use any mechanism they like to recommend posts. spacecowboy run

- **[Extract PDF text in your browser with LiteParse for the web](https://simonwillison.net/2026/Apr/23/liteparse-for-the-web/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 23
  LlamaIndex have a most excellent open source project called LiteParse, which provides a Node.js CLI tool for extracting text from PDFs. I got a version of LiteParse working entirely in the browser, using most of the same libraries that LiteParse uses to run in Node.js. Spatial te

- **[A pelican for GPT-5.5 via the semi-official Codex backdoor API](https://simonwillison.net/2026/Apr/23/gpt-5-5/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 23
  GPT-5.5 is out. It's available in OpenAI Codex and is rolling out to paid ChatGPT subscribers. I've had some preview access and found it to be a fast, effective and highly capable model. As is usually the case these days, it's hard to put into words what's good about it - I ask i

- **[llm-openai-via-codex 0.1a0](https://simonwillison.net/2026/Apr/23/llm-openai-via-codex/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 23
  Release: llm-openai-via-codex 0.1a0 Hijacks your Codex CLI credentials to make API calls with LLM, as described in my post about GPT-5.5. Tags: openai, llm, codex-cli

- **[Quoting Maggie Appleton](https://simonwillison.net/2026/Apr/23/maggie-appleton/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 23
  [...] if you ever needed another reason to learn in public by digital gardening or podcasting or streaming or whathaveyou, add on that people will assume you’re more competent than you are. This will get you invites to very cool exclusive events filled with high-achieving, intere

- **[Qwen3.6-27B: Flagship-Level Coding in a 27B Dense Model](https://simonwillison.net/2026/Apr/22/qwen36-27b/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 22
  Qwen3.6-27B: Flagship-Level Coding in a 27B Dense Model Big claims from Qwen about their latest open weight model: Qwen3.6-27B delivers flagship-level agentic coding performance, surpassing the previous-generation open-source flagship Qwen3.5-397B-A17B (397B total / 17B active Mo

- **[Quoting Bobby Holley](https://simonwillison.net/2026/Apr/22/bobby-holley/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 22
  As part of our continued collaboration with Anthropic, we had the opportunity to apply an early version of Claude Mythos Preview to Firefox. This week’s release of Firefox 150 includes fixes for 271 vulnerabilities identified during this initial evaluation. [...] Our experience i

- **[Changes to GitHub Copilot Individual plans](https://simonwillison.net/2026/Apr/22/changes-to-github-copilot/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 22
  Changes to GitHub Copilot Individual plans On the same day as Claude Code's temporary will-they-won't-they $100/month kerfuffle (for the moment, they won't), here's the latest on GitHub Copilot pricing. Unlike Anthropic, GitHub put up an official announcement about their changes,

- **[Is Claude Code going to cost $100/month? Probably not - it's all very confusing](https://simonwillison.net/2026/Apr/22/claude-code-confusion/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 22
  Anthropic today quietly (as in silently, no announcement anywhere at all) updated their claude.com/pricing page (but not their Choosing a Claude plan page, which shows up first for me on Google) to add this tiny but significant detail (arrow is mine, and it's already reverted): T

- **[Where's the raccoon with the ham radio? (ChatGPT Images 2.0)](https://simonwillison.net/2026/Apr/21/gpt-image-2/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 21
  OpenAI released ChatGPT Images 2.0 today, their latest image generation model. On the livestream Sam Altman said that the leap from gpt-image-1 to gpt-image-2 was equivalent to jumping from GPT-3 to GPT-5. Here's how I put it to the test. My prompt: Do a where's Waldo style image

- **[Quoting Andreas Påhlsson-Notini](https://simonwillison.net/2026/Apr/21/andreas-pahlsson-notini/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 21
  AI agents are already too human. Not in the romantic sense, not because they love or fear or dream, but in the more banal and frustrating one. The current implementations keep showing their human origin again and again: lack of stringency, lack of patience, lack of focus. Faced w

- **[scosman/pelicans_riding_bicycles](https://simonwillison.net/2026/Apr/21/scosman/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 21
  scosman/pelicans_riding_bicycles I firmly approve of Steve Cosman's efforts to pollute the training set of pelicans riding bicycles. (To be fair, most of the examples I've published count as poisoning too.) Via Hacker News comment Tags: ai, generative-ai, llms, training-data, pel

- **[llm-openrouter 0.6](https://simonwillison.net/2026/Apr/20/llm-openrouter/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 20
  Release: llm-openrouter 0.6 llm openrouter refresh command for refreshing the list of available models without waiting for the cache to expire. I added this feature so I could try Kimi 2.6 on OpenRouter as soon as it became available there. Here's its pelican - this time as an HT

- **[SQL functions in Google Sheets to fetch data from Datasette](https://simonwillison.net/2026/Apr/20/datasette-sql/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 20
  TIL: SQL functions in Google Sheets to fetch data from Datasette I put together some notes on patterns for fetching data from a Datasette instance directly into Google Sheets - using the importdata() function, a "named function" that wraps it or a Google Apps Script if you need t

- **[Claude Token Counter, now with model comparisons](https://simonwillison.net/2026/Apr/20/claude-token-counts/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 20
  Claude Token Counter, now with model comparisons I upgraded my Claude Token Counter tool to add the ability to run the same count against different models in order to compare them. As far as I can tell Claude Opus 4.7 is the first model to change the tokenizer, so it's only worth

- **[Headless everything for personal AI](https://simonwillison.net/2026/Apr/19/headless-everything/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 19
  Headless everything for personal AI Matt Webb thinks headless services are about to become much more common: Why? Because using personal AIs is a better experience for users than using services directly (honestly); and headless services are quicker and more dependable for the per

- **[Changes in the system prompt between Claude Opus 4.6 and 4.7](https://simonwillison.net/2026/Apr/18/opus-system-prompt/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 18
  Anthropic are the only major AI lab to publish the system prompts for their user-facing chat systems. Their system prompt archive now dates all the way back to Claude 3 in July 2024 and it's always interesting to see how the system prompt evolves as they publish new models. Opus 

- **[Claude system prompts as a git timeline](https://simonwillison.net/2026/Apr/18/extract-system-prompts/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 18
  Research: Claude system prompts as a git timeline Anthropic publish the system prompts for Claude chat and make that page available as Markdown. I had Claude Code turn that page into separate files for each model and model family with fake git commit dates to enable browsing the 

- **[Adding a new content type to my blog-to-newsletter tool](https://simonwillison.net/guides/agentic-engineering-patterns/adding-a-new-content-type/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 18
  Agentic Engineering Patterns > Here's an example of a deceptively short prompt that got a quite a lot of work done in a single shot. First, some background. I send out a free Substack newsletter around once a week containing content copied-and-pasted from my blog. I'm effectively

- **[Join us at PyCon US 2026 in Long Beach - we have new AI and security tracks this year](https://simonwillison.net/2026/Apr/17/pycon-us-2026/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — Apr 17
  This year's PyCon US is coming up next month from May 13th to May 19th, with the core conference talks from Friday 15th to Sunday 17th and tutorial and sprint days either side. It's in Long Beach, California this year, the first time PyCon US has come to the West Coast since Port


## Community Signal

- **[South Korea police arrest man for posting AI photo of runaway wolf](https://www.bbc.com/news/articles/c4gx1n0dl9no)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 24
  Article URL: https://www.bbc.com/news/articles/c4gx1n0dl9no Comments URL: https://news.ycombinator.com/item?id=47887683 Points: 191 # Comments: 114

- **[Show HN: How LLMs Work – Interactive visual guide based on Karpathy's lecture](https://ynarwal.github.io/how-llms-work/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 24
  All content is based on Andrej Karpathy's "Intro to Large Language Models" lecture (youtube.com/watch?v=7xTGNNLPyMI). I downloaded the transcript and used Claude Code to generate the entire interactive site from it — single HTML file. I find it useful to revisit this content time

- **[MeshCore development team splits over trademark dispute and AI-generated code](https://blog.meshcore.io/2026/04/23/the-split)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 23
  Article URL: https://blog.meshcore.io/2026/04/23/the-split Comments URL: https://news.ycombinator.com/item?id=47878117 Points: 251 # Comments: 134

- **[LLM pricing has never made sense](https://anderegg.ca/2026/04/22/llm-pricing-has-never-made-sense)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 23
  Article URL: https://anderegg.ca/2026/04/22/llm-pricing-has-never-made-sense Comments URL: https://news.ycombinator.com/item?id=47875694 Points: 29 # Comments: 23

- **[Congressman Introduces Bill to Ban AI Chatbots in Children's Toys](https://blakemoore.house.gov/media/press-releases/congressman-blake-moore-introduces-bill-to-ban-artificial-intelligence-chatbots-in-childrens-toys)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 23
  Article URL: https://blakemoore.house.gov/media/press-releases/congressman-blake-moore-introduces-bill-to-ban-artificial-intelligence-chatbots-in-childrens-toys Comments URL: https://news.ycombinator.com/item?id=47874106 Points: 27 # Comments: 2

- **[Do you want the US to "win" AI?](https://geohot.github.io//blog/jekyll/update/2026/04/23/us-win-ai.html)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 23
  Article URL: https://geohot.github.io//blog/jekyll/update/2026/04/23/us-win-ai.html Comments URL: https://news.ycombinator.com/item?id=47873796 Points: 53 # Comments: 104

- **[Our newsroom AI policy](https://arstechnica.com/staff/2026/04/our-newsroom-ai-policy/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 23
  Article URL: https://arstechnica.com/staff/2026/04/our-newsroom-ai-policy/ Comments URL: https://news.ycombinator.com/item?id=47872452 Points: 200 # Comments: 129

- **[Failed Companies Are Selling Old Slack Chats and Email Archives to Train AI](https://gizmodo.com/failed-companies-are-selling-old-slack-chats-and-email-archives-to-train-ai-2000747916)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  Article URL: https://gizmodo.com/failed-companies-are-selling-old-slack-chats-and-email-archives-to-train-ai-2000747916 Comments URL: https://news.ycombinator.com/item?id=47869253 Points: 24 # Comments: 7

- **[Anker made its own chip to bring AI to all its products](https://www.theverge.com/tech/916463/anker-thus-chip-announcement)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  Article URL: https://www.theverge.com/tech/916463/anker-thus-chip-announcement Comments URL: https://news.ycombinator.com/item?id=47866368 Points: 67 # Comments: 47

- **[Startups brag they spend more money on AI than human employees](https://www.404media.co/startups-brag-they-spend-more-money-on-ai-than-human-employees/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  Article URL: https://www.404media.co/startups-brag-they-spend-more-money-on-ai-than-human-employees/ Comments URL: https://news.ycombinator.com/item?id=47865923 Points: 53 # Comments: 47

- **[Health AI Startup Has Helped Reverse Denied Health Insurance Claims](https://www.bloomberg.com/news/features/2026-04-22/ai-and-mark-cuban-among-startup-s-tools-to-fight-denied-health-care-claims)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  Article URL: https://www.bloomberg.com/news/features/2026-04-22/ai-and-mark-cuban-among-startup-s-tools-to-fight-denied-health-care-claims Comments URL: https://news.ycombinator.com/item?id=47865292 Points: 20 # Comments: 12

- **[Top MAGA influencer revealed to be AI](https://nypost.com/2026/04/21/us-news/top-maga-influencer-emily-hart-revealed-to-be-ai-created-by-a-guy-in-india/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  Article URL: https://nypost.com/2026/04/21/us-news/top-maga-influencer-emily-hart-revealed-to-be-ai-created-by-a-guy-in-india/ Comments URL: https://news.ycombinator.com/item?id=47864808 Points: 97 # Comments: 54

- **[Scoring Show HN submissions for AI design patterns](https://www.adriankrebs.ch/blog/design-slop/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  Article URL: https://www.adriankrebs.ch/blog/design-slop/ Comments URL: https://news.ycombinator.com/item?id=47864393 Points: 330 # Comments: 233

- **[Kernel code removals driven by LLM-created security reports](https://lwn.net/Articles/1068928/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  Article URL: https://lwn.net/Articles/1068928/ Comments URL: https://news.ycombinator.com/item?id=47862230 Points: 123 # Comments: 117

- **[Meta employees are up in arms over a mandatory program to train AI on their](https://www.businessinsider.com/meta-new-ai-tool-tracks-staff-activity-sparks-concern-2026-4)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  Article URL: https://www.businessinsider.com/meta-new-ai-tool-tracks-staff-activity-sparks-concern-2026-4 Comments URL: https://news.ycombinator.com/item?id=47860961 Points: 116 # Comments: 90

- **[Tell HN: I'm sick of AI everything](https://news.ycombinator.com/item?id=47857461)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 22
  A while back, I stopped using Facebook because I just couldn't take it anymore. Just totally sick of it. I'm honestly getting there with AI. At this point, I would prefer to have anything AI related just be blocked at the browser level. Comments URL: https://news.ycombinator.com/

- **[Mozilla: Anthropic's Mythos found 271 security vulnerabilities in Firefox 150](https://arstechnica.com/ai/2026/04/mozilla-anthropics-mythos-found-271-zero-day-vulnerabilities-in-firefox-150/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 21
  Article URL: https://arstechnica.com/ai/2026/04/mozilla-anthropics-mythos-found-271-zero-day-vulnerabilities-in-firefox-150/ Comments URL: https://news.ycombinator.com/item?id=47855384 Points: 32 # Comments: 8

- **[Meta to start capturing employee mouse movements, keystrokes for AI training](https://www.reuters.com/sustainability/boards-policy-regulation/meta-start-capturing-employee-mouse-movements-keystrokes-ai-training-data-2026-04-21/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 21
  Alt link: https://tech.yahoo.com/ai/meta-ai/articles/exclusive-meta-st... Comments URL: https://news.ycombinator.com/item?id=47851948 Points: 791 # Comments: 523

- **[Meta to start capturing employee mouse movements, keystrokes for AI training](https://www.reuters.com/sustainability/boards-policy-regulation/meta-start-capturing-employee-mouse-movements-keystrokes-ai-training-data-2026-04-21/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 21
  Article URL: https://www.reuters.com/sustainability/boards-policy-regulation/meta-start-capturing-employee-mouse-movements-keystrokes-ai-training-data-2026-04-21/ Comments URL: https://news.ycombinator.com/item?id=47851242 Points: 48 # Comments: 2

- **[Meta to start capturing employee mouse movement, keystrokes for AI training data](https://tech.yahoo.com/ai/meta-ai/articles/exclusive-meta-start-capturing-employee-162745587.html)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — Apr 21
  Article URL: https://tech.yahoo.com/ai/meta-ai/articles/exclusive-meta-start-capturing-employee-162745587.html Comments URL: https://news.ycombinator.com/item?id=47851086 Points: 58 # Comments: 4


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

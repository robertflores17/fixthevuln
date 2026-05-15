---
title: "AI Security Trend Roundup — May 15, 2026"
description: "52 curated AI security updates from OWASP GenAI, arXiv, Simon Willison, CISA, and 4 more sources covering May 08–May 15. Every item credited to its original author."
keywords: "AI security, LLM security, prompt injection, agentic AI, GenAI threats, AI vulnerabilities, AI red team"
date: "2026-05-15"
slug: "ai-security-roundup-2026-05-15"
author: "FixTheVuln Team"
sources: "OWASP GenAI Security Project, Simon Willison, arXiv cs.CR, Protect AI, Google Project Zero, CISA, NIST, Hacker News"
cta_section: "comptia"
---

# AI Security Trend Roundup — May 15, 2026

*Covering May 08 → May 15, 2026. 52 new items from 8 tracked sources.*

> This digest credits every source by name and links directly to each original post. Editorial curation by FixTheVuln — all rights and attribution belong to the original authors.

## Government Advisories

- **[Software Bill of Materials for AI - Minimum Elements](https://www.cisa.gov/resources-tools/resources/software-bill-materials-ai-minimum-elements)**  
  Source: [CISA Cybersecurity Advisories](https://www.cisa.gov/news-events/cybersecurity-advisories) — May 12
  CISA and the Group of Seven (G7) international partners—Germany, Canada, France, Italy, Japan, the United Kingdom, and the European Union—have released joint guidance, Software Bill of Materials for AI – Minimum Elements, to help public and private sector stakeholders improve tra


## Academic & Research

- **[XAI and Statistical Analysis for Reliable Intrusion Detection in the UAVIDS-2025 Dataset: From Tree to Hybrid and Tabular DNN Ensembles](https://arxiv.org/abs/2605.13922)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.13922v1 Announce Type: new Abstract: During the last few years, the term Mechanistic Interpretability, a specific area, under the umbrella of explainable artificial intelligence (XAI), has been introduced, to explain the decisions made by complex machine learning (ML) 

- **[AgentTrap: Measuring Runtime Trust Failures in Third-Party Agent Skills](https://arxiv.org/abs/2605.13940)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.13940v1 Announce Type: new Abstract: Third-party skills are becoming the package ecosystem for LLM agents. They package natural-language instructions, helper scripts, templates, documents, and service configuration into reusable workflows. This makes skills useful, but

- **[ExploitBench: A Capability Ladder Benchmark for LLM Cybersecurity Agents](https://arxiv.org/abs/2605.14153)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.14153v1 Announce Type: new Abstract: Exploitation is not a binary event. It is a ladder of acquiring progressive capabilities, from executing a single buggy line of code to taking full control of the target. However, existing LLM security benchmarks treat a crash as ex

- **[Web Agents Should Adopt the Plan-Then-Execute Paradigm](https://arxiv.org/abs/2605.14290)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.14290v1 Announce Type: new Abstract: ReAct has become the default architecture across LLM agents, and many existing web agents follow this paradigm. We argue that it is the wrong default for web agents. Instead, web agents should default to plan-then-execute: commit to

- **[The Great Pretender: A Stochasticity Problem in LLM Jailbreak](https://arxiv.org/abs/2605.14418)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.14418v1 Announce Type: new Abstract: "Oh-Oh, yes, I'm the great pretender. Pretending that I'm doing well. My need is such, I pretend too much..." summarizes the state in the area of jailbreak creation and evaluation. You find this method to generate adversarial attack

- **[MemLineage: Lineage-Guided Enforcement for LLM Agent Memory](https://arxiv.org/abs/2605.14421)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.14421v1 Announce Type: new Abstract: We introduce MemLineage, a defense for LLM agent memory that attaches both cryptographic provenance and LLM-mediated derivation lineage to every entry. Recent and concurrent work shows that untrusted content can be written into pers

- **[Exploiting LLM Agent Supply Chains via Payload-less Skills](https://arxiv.org/abs/2605.14460)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.14460v1 Announce Type: new Abstract: Autonomous agents powered by Large Language Models (LLMs) acquire external functionalities through third-party skills available in open marketplaces. Adopting these integrations broadens the potential attack surface, prompting a nee

- **[EVA: Editing for Versatile Alignment against Jailbreaks](https://arxiv.org/abs/2605.14750)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.14750v1 Announce Type: new Abstract: Large Language Models (LLMs) and Vision Language Models (VLMs) have demonstrated impressive capabilities but remain vulnerable to jailbreaking attacks, where adversaries exploit textual or visual triggers to bypass safety guardrails

- **[Known By Their Actions: Fingerprinting LLM Browser Agents via UI Traces](https://arxiv.org/abs/2605.14786)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.14786v1 Announce Type: new Abstract: As LLM-based agents increasingly browse the web on users' behalf, a natural question arises: can websites passively identify which underlying model powers an agent? Doing so would represent a significant security risk, enabling targ

- **[Do Coding Agents Understand Least-Privilege Authorization?](https://arxiv.org/abs/2605.14859)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.14859v1 Announce Type: new Abstract: As coding agents gain access to shells, repositories, and user files, least-privilege authorization becomes a prerequisite for safe deployment: an agent should receive enough authority to complete the task, without unnecessary autho

- **[WARD: Adversarially Robust Defense of Web Agents Against Prompt Injections](https://arxiv.org/abs/2605.15030)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.15030v1 Announce Type: new Abstract: Web agents can autonomously complete online tasks by interacting with websites, but their exposure to open web environments makes them vulnerable to prompt injection attacks embedded in HTML content or visual interfaces. Existing gu

- **[PickleFuzzer: A Case Study in Fuzzing for Discrepancies Between Python Pickle Implementations](https://arxiv.org/abs/2605.15084)**  
  Source: [arXiv cs.CR](https://arxiv.org/list/cs.CR/recent) — May 15
  arXiv:2605.15084v1 Announce Type: new Abstract: Python's native serialization protocol, pickle, is a powerful but insecure format for transferring untrusted data. It is frequently used, especially for saving machine learning models, despite known security challenges. While develo


## Prompt Injection & LLM Security

- **[Not so locked in any more](https://simonwillison.net/2026/May/14/not-so-locked-in/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 14
  This Mitchell Hashimoto quote about Bun migrating from Zig to Rust reminded me of a similar conversation I had at a conference last week. I was talking to someone who worked for a medium sized technology company with a pair of legacy/legendary iPhone and Android apps. They told m

- **[Quoting Mitchell Hashimoto](https://simonwillison.net/2026/May/14/mitchell-hashimoto/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 14
  [...] On the interesting side is how fungible programming languages are nowadays. Programming languages used to be LOCK IN, and they're increasingly not so. You think the Bun rewrite in Rust is good for Rust? Bun has shown they can be in probably any language they want in roughly

- **[datasette-ip-rate-limit 0.1a0](https://simonwillison.net/2026/May/14/datasette-ip-rate-limit/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 14
  Release: datasette-ip-rate-limit 0.1a0 The datasette.io site was being hammered by poorly-behaved crawlers, so I had Codex (GPT-5.5 xhigh) build a configurable rate limiting plugin to block IPs that were hammering specific areas of the site too quickly. Here's the production conf

- **[Welcome to the Datasette blog](https://simonwillison.net/2026/May/13/welcome-to-the-datasette-blog/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 13
  Welcome to the Datasette blog We have a bunch of neat Datasette announcements in the pipeline so we decided it was time the project grew an official blog. I built this using OpenAI Codex desktop, which turns out to have the Markdown session transcript export feature I've always w

- **[Quoting Boris Mann](https://simonwillison.net/2026/May/13/boris-mann/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 13
  “11 AI agents” is meaningless as a phrase. If I said “I have 11 spreadsheets” or “I have 11 browser tabs” to do my work, it means about the same thing. &mdash; Boris Mann Tags: ai-agents, ai, agent-definitions

- **[CSP Allow-list Experiment](https://simonwillison.net/2026/May/13/csp-allow/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 13
  Tool: CSP Allow-list Experiment An experiment that shows that you can load an app in a CSP-protected sandboxed iframe (see previous note) and have a custom fetch() that intercepts CSP errors and passes them up to the parent window... which can then prompt the user to add that dom

- **[datasette 1.0a29](https://simonwillison.net/2026/May/12/datasette/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 12
  Release: datasette 1.0a29 New TokenRestrictions.abbreviated(datasette) utility method for creating "_r" dictionaries. #2695 Table headers and column options are now visible even if a table contains zero rows. #2701 Fixed bug with display of column actions dialog on Mobile Safari.

- **[Quoting Mo Bitar](https://simonwillison.net/2026/May/12/mo-bitar/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 12
  Now, if your CEO has never heard the phrase Ralph Loop, oh man, you are less than 30 days away from your next promotion. I'm not even exaggerating. Walk into his office, close the door, and say, hey chief, been experimenting with something. It's called Ralph Loops. And I think it

- **[Quoting Mitchell Hashimoto](https://simonwillison.net/2026/May/12/mitchell-hashimoto/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 12
  The thing about 90% of TDMs [Technical Decision Makers] is that they're motivated primarily by NOT GETTING FIRED. These aren't people who browser Lobsters or push to GH on the weekend. These are people that work 9 to 5, get paid, go home, and NEVER THINK ABOUT WORK AGAIN. So to a

- **[llm 0.32a2](https://simonwillison.net/2026/May/12/llm/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 12
  Release: llm 0.32a2 A bunch of useful stuff in this LLM alpha, but the most important detail is this one: Most reasoning-capable OpenAI models now use the /v1/responses endpoint instead of /v1/chat/completions. This enables interleaved reasoning across tool calls for GPT-5 class 

- **[Thoughts on GitLab's workforce reduction" and "structural and strategic decisions"](https://simonwillison.net/2026/May/11/gitlab-act-2/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 11
  GitLab Act 2 There's a lot going on in this announcement from GitLab about the "workforce reduction" and "structural and strategic decisions" they are making with respect to the agentic era. They're "planning to reduce the number of countries by up to 30% where we have small team

- **[Quoting James Shore](https://simonwillison.net/2026/May/11/james-shore/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 11
  Your AI coding agent, the one you use to write code, needs to reduce your maintenance costs. Not by a little bit, either. You write code twice as quick now? Better hope you’ve halved your maintenance costs. Three times as productive? One third the maintenance costs. Otherwise, yo

- **[Your AI Use Is Breaking My Brain](https://simonwillison.net/2026/May/11/zombie-internet/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 11
  Your AI Use Is Breaking My Brain Excellent, angry piece by Jason Koebler on how AI writing online is becoming impossible to avoid, filtering it is mentally exhausting and it's even starting to distort regular human writing styles. I particularly liked his use of the term "Zombie 

- **[Using LLM in the shebang line of a script](https://simonwillison.net/2026/May/11/llm-shebang/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 11
  TIL: Using LLM in the shebang line of a script Kim_Bruning on Hacker News: But seriously, you can put a shebang on an english text file now (if you're sufficiently brave) [...] This inspired me to look at patterns for doing exactly that with LLM. Here's the simplest, which takes 

- **[Learning on the Shop floor](https://simonwillison.net/2026/May/11/learning-on-the-shop-floor/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 11
  Learning on the Shop floor Tobias Lütke describes Shopify's internal coding agent tool, River, which operates entirely in public on their Slack: River does not respond to direct messages. She politely declines and suggests to create a public channel for you and her to start worki

- **[Quoting New York Times Editors’ Note](https://simonwillison.net/2026/May/10/new-york-times-editors-note/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 10
  This article was updated after The Times learned that a remark attributed to Pierre Poilievre, the Conservative leader, was in fact an A.I.-generated summary of his views about Canadian politics that A.I. rendered as a quotation. The reporter should have checked the accuracy of w

- **[Quoting Andrew Quinn](https://simonwillison.net/2026/May/10/andrew-quinn/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 10
  One could say in the first quarter-century of my life, that while I was always fascinated by programming, I could never overcome the guilt of not really knowing whether the tool I am building right now isn’t already superceded by some much better implementation someone else has a

- **[Quoting Luke Curley](https://simonwillison.net/2026/May/9/luke-curley/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 09
  WebRTC is designed to degrade and drop my prompt during poor network conditions. wtf my dude WebRTC aggressively drops audio packets to keep latency low. If you’ve ever heard distorted audio on a conference call, that’s WebRTC baybee. The idea is that conference calls depend on r

- **[Using Claude Code: The Unreasonable Effectiveness of HTML](https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/#atom-everything)**  
  Source: [Simon Willison](https://simonwillison.net/) — May 08
  Using Claude Code: The Unreasonable Effectiveness of HTML Thought-provoking piece by Thariq Shihipar (on the Claude Code team at Anthropic) advocating for HTML over Markdown as an output format to request from Claude. The article is crammed with interesting examples (collected on


## Community Signal

- **[AI is wiping out entry-level jobs](https://fortune.com/2026/05/15/ai-entry-level-jobs-higher-education-experience-gap/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 15
  Article URL: https://fortune.com/2026/05/15/ai-entry-level-jobs-higher-education-experience-gap/ Comments URL: https://news.ycombinator.com/item?id=48148440 Points: 37 # Comments: 63

- **[Amazon workers under pressure to up their AI usage are making up tasks](https://www.fastcompany.com/91541586/amazon-workers-pressured-to-up-ai-use-extraneous-tasks)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 15
  Article URL: https://www.fastcompany.com/91541586/amazon-workers-pressured-to-up-ai-use-extraneous-tasks Comments URL: https://news.ycombinator.com/item?id=48148337 Points: 111 # Comments: 73

- **[Welcome to the Strip Mining Era of OSS Security](https://www.metabase.com/blog/strip-mining-era-of-open-source-security)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 15
  Article URL: https://www.metabase.com/blog/strip-mining-era-of-open-source-security Comments URL: https://news.ycombinator.com/item?id=48147339 Points: 76 # Comments: 59

- **[Overseas fakers using AI videos to push a narrative of UK decline, BBC finds](https://www.bbc.co.uk/news/articles/ckgpyn30dp3o)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 15
  Article URL: https://www.bbc.co.uk/news/articles/ckgpyn30dp3o Comments URL: https://news.ycombinator.com/item?id=48146656 Points: 47 # Comments: 36

- **[UK sovereign LLM inference](https://relax.ai/docs)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 15
  Article URL: https://relax.ai/docs Comments URL: https://news.ycombinator.com/item?id=48146424 Points: 98 # Comments: 108

- **[Show HN: Find the best local LLM for your hardware, ranked by benchmarks](https://github.com/Andyyyy64/whichllm)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 15
  Article URL: https://github.com/Andyyyy64/whichllm Comments URL: https://news.ycombinator.com/item?id=48146369 Points: 261 # Comments: 61

- **[Show HN: GlycemicGPT – Open-source AI-powered diabetes management](https://github.com/GlycemicGPT/GlycemicGPT)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 15
  I'm a Type 1 diabetic and software engineer. Last year I went months between endocrinologists with no clinician reviewing my data. I'm an engineer, so I built the tool I needed — and now I'm open sourcing it. GlycemicGPT is a self-hosted platform that connects continuous glucose 

- **[Access to frontier AI will soon be limited by economic and security constraints](https://writing.antonleicht.me/p/cut-off)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 15
  Article URL: https://writing.antonleicht.me/p/cut-off Comments URL: https://news.ycombinator.com/item?id=48143284 Points: 194 # Comments: 195

- **[LLM Policy for Rust Compiler](https://github.com/rust-lang/rust-forge/pull/1040)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://github.com/rust-lang/rust-forge/pull/1040 Comments URL: https://news.ycombinator.com/item?id=48142650 Points: 94 # Comments: 77

- **[Have a Coherent AI Policy](https://brianmeeker.me/2026/05/14/have-a-coherent-ai-policy/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://brianmeeker.me/2026/05/14/have-a-coherent-ai-policy/ Comments URL: https://news.ycombinator.com/item?id=48142553 Points: 68 # Comments: 60

- **[Ontario auditors find doctors' AI note takers routinely blow basic facts](https://www.theregister.com/ai-ml/2026/05/14/ontario-auditors-find-doctors-ai-note-takers-routinely-blow-basic-facts/5240771)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://www.theregister.com/ai-ml/2026/05/14/ontario-auditors-find-doctors-ai-note-takers-routinely-blow-basic-facts/5240771 Comments URL: https://news.ycombinator.com/item?id=48142188 Points: 266 # Comments: 126

- **[The AI zombification of universities](https://www.thenewcritic.com/p/the-great-zombification)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://www.thenewcritic.com/p/the-great-zombification Comments URL: https://news.ycombinator.com/item?id=48139355 Points: 187 # Comments: 203

- **[AI is making me dumb](https://jpain.io/god-damn-ai-is-making-me-dumb/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://jpain.io/god-damn-ai-is-making-me-dumb/ Comments URL: https://news.ycombinator.com/item?id=48139148 Points: 514 # Comments: 297

- **[The people writing AI alignment policy are not whose work is being replaced](https://danieltan.weblog.lol/2026/05/you-dont-align-an-ai-you-align-with-it)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://danieltan.weblog.lol/2026/05/you-dont-align-an-ai-you-align-with-it Comments URL: https://news.ycombinator.com/item?id=48139144 Points: 90 # Comments: 61

- **[Using Chinese AI models to get a degree](https://nonogra.ph/using-chinese-ai-models-to-get-a-degree-05-14-2026)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://nonogra.ph/using-chinese-ai-models-to-get-a-degree-05-14-2026 Comments URL: https://news.ycombinator.com/item?id=48139058 Points: 20 # Comments: 8

- **[What happens when you post a real Monet and say it's AI?](https://twitter.com/jediwolf/status/2054776716770320631)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://twitter.com/jediwolf/status/2054776716770320631 Comments URL: https://news.ycombinator.com/item?id=48134400 Points: 83 # Comments: 74

- **[LLMs are breaking 20 year old system design](https://zknill.io/posts/llms-are-breaking-20-year-old-system-design/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://zknill.io/posts/llms-are-breaking-20-year-old-system-design/ Comments URL: https://news.ycombinator.com/item?id=48131888 Points: 30 # Comments: 27

- **[AI coders are carrying half-open laptops through airports, offices, ice rinks](https://www.businessinsider.com/coders-keep-laptops-open-in-public-ai-agent-2026-5)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://www.businessinsider.com/coders-keep-laptops-open-in-public-ai-agent-2026-5 Comments URL: https://news.ycombinator.com/item?id=48131370 Points: 29 # Comments: 40

- **[Arena AI Model ELO History](https://mayerwin.github.io/AI-Arena-History/)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Hi HN,I built a live tracker to visualize the lifecycle and performance changes of flagship AI models.We've all experienced the phenomenon where a flagship model feels amazing at launch, but weeks later, it suddenly feels a bit off. I wanted to see if this was just a feeling or a

- **[The other half of AI safety](https://personalaisafety.com/p/the-other-half-of-ai-safety)**  
  Source: [Hacker News (AI Security)](https://news.ycombinator.com/) — May 14
  Article URL: https://personalaisafety.com/p/the-other-half-of-ai-safety Comments URL: https://news.ycombinator.com/item?id=48129561 Points: 97 # Comments: 130


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

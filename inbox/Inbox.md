Notes from emails, chats, etc

1)

But since we are going to try Claude Code or similar, I wanted to bring your attention to some Anthropic / Claude Code drama from beginning of this year. The summary is that sometimes they change stuff which makes it difficult to reproduce things: 
"In February 2026, Anthropic shipped "adaptive thinking" with Opus 4.6, then quietly lowered
Claude Code's default effort level from "high" to "medium." The result: a measurable 67% drop in
reasoning depth across thousands of sessions, documented by an AMD AI director with 6,852
sessions of telemetry."

The original issue: https://github.com/anthropics/claude-code/issues/42796?timeline_page=2 ("[MODEL] Claude Code is unusable for complex engineering tasks with the Feb updates"). 
And a lenghty write-up: https://drive.google.com/file/d/1KPdA-uWJ3yeSHFlQ9rPYThiNJzVJcdfH/view

Anyway, I don't expect anyone to read this (I didn't), but it is good to be aware that measurements with Claude Code can be difficult to reproduce. I assume that is not a problem for us when using an open-source Claude clone - just FYI.


2)

Fundamental agent paper that I like: Executable Code Actions Elicit Better LLM Agents -
https://arxiv.org/abs/2402.01030

3)

Interesting way of handling context: Agentic Context Engineering - https://arxiv.org/abs/2510.04618

4)
ACE for RTL: https://arxiv.org/abs/2602.10218

5)
RTL Benchmarks
1. Comprehensive Verilog Design Problems -
https://arxiv.org/abs/2506.14074:
This is the Nvidia benchmark repo - benchmark covering several tasks:
RTL generation, debugging, verification, reuse, and Q&A, in both
non-agentic and agentic formats. It says that VerilogEval and RTLLM are
not enough challenging. Metrics: pass@1 (on 5), pass@k, BLUE
2. VerilogEval - https://arxiv.org/pdf/2309.07544:
Problems on self-contained Verilog code generation. Metrics: pass@k
3. Revisiting VerilogEval - https://arxiv.org/pdf/2408.11053:
Extends VerilogEval to include specification-to-RTL tasks, in-context
learning (ICL), and structured failure analysis.
4. RTLLM - https://arxiv.org/pdf/2308.05345:
More complex RTL generation tasks. Metric: pass@k
5. RTLRepo - https://arxiv.org/pdf/2405.17378:
It uses the context of GitHub repos, it evaluates code completion in
multi-file projects - contextual understanding.

I like the first one, from NVIDIA and less of a toy

6)
https://arxiv.org/abs/2512.05073

Large Language Model(LLM) inference demands massive compute and energy, making domain-specific tasks expensive and unsustainable. As foundation models keep scaling, we ask: Is bigger always better for hardware design? Our work tests this by evaluating Small Language Models coupled with a curated agentic AI framework on NVIDIA's Comprehensive Verilog Design Problems(CVDP) benchmark. Results show that agentic workflows: through task decomposition, iterative feedback, and correction - not only unlock near-LLM performance at a fraction of the cost but also create learning opportunities for agents, paving the way for efficient, adaptive solutions in complex design tasks.


7) .pptx in this folder: talk I held at the Infineon summer school.

8) "Small Language Models are the future of agentic AI" from NVIDIA

9) Our company RND Chat - papers I mentioned
You, 5 Feb, 08:32
https://arxiv.org/abs/2602.02084 Anisha, Luigi, have a look at this. Creating a graph from a repo, also seems to discuss handling changes and  updates
You, 5 Feb, 08:32
https://github.com/microsoft/RPG-ZeroRepo?tab=readme-ov-file "all code will be released in the next few weeks" we will see, its microsoft after all

You, 7 Apr, 10:34
A few interesting AI things:
gemma4 came out - would be interesting to try
https://arxiv.org/abs/2604.01193 1st of April. "Embarrassingly Simple Self-Distillation Improves Code Generation" - might be an interesting paper
You, 13 Apr, 10:05
https://arxiv.org/html/2604.03312v1 Could be an interesting paper: 
Shows LLM-driven systems can:
generate architectures
simulate performance
outperform human baselines (2–3× in experiments)
You, 14 Apr, 13:03
This is pretty cool: a command line llm completion that uses the builtin 3b model on tahoe https://github.com/es617/hunch
You, Mon 09:57
Kind of interesting: this paper separates not only memory and knowledge (which are good terms for permanent and per-task memory) but also wisdom and intelligence for agents.
https://arxiv.org/pdf/2604.11364
You, 10:01
This is a breakdown of the claude code source that was leaked a while ago: https://arxiv.org/abs/2604.14228
[2604.14228] Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems
It is probably worth seeing what they do.

10) Our 'Useful Resources' Chat
A space to share interesting resources: github repos, papers, articles, etc. Do not feel like you have to read all the things that are posted in here, unless it sounds useful to you. Also, when you post something, include a sentence or two about what it is.
https://arxiv.org/pdf/2508.05266 "Understanding and Mitigating Errors of
LLM-Generated RTL Code" - the quality of the paper is rather low, but they classify failures of LLMs generating code and have wrong/correct Verilog examples.
https://www.anthropic.com/engineering/code-execution-with-mcp "Code execution with MCP: Building more efficient agents" An interesting take of how to implement API calls efficiently.

You, 24 Nov, 13:11
https://www.alphaxiv.org/pdf/2510.04871 "Less is More: Recursive Reasoning with Tiny Networks". Not directly applicable to us, but interesting how they seem to manage to get good performance with very small networks.

You, 24 Nov, 13:15
https://github.com/huawei-csl/GENIAL Huawei Design exploration framework for this paper: GENIAL: Generative Design Space Exploration via Network Inversion for Low Power Algorithmic Logic Units (arXiv:2507.18989)
Optimizing designs with network inversion is an interesting concept.
You, 24 Nov, 13:17
https://github.com/0xeb/TheBigPromptLibrary Reverse engineered prompts of many GPTs. Including things like perplexity. Interesting as a reference / inspiration to see what big teams come up with
You, 24 Nov, 14:56
https://github.com/olofk/serv/ A small RISCV Implementation. Might be a good playground, as it is much smaller and less convoluted than our other projects.
Harald Kröll, 26 Nov, 20:24
https://x.com/hasantoxr/status/1993260004145836480?s=46&t=2Jfutkx0WTSR8b19GtyKbg
https://github.com/memodb-io/Acontext
You, 27 Nov, 15:15
I just sent an e-mail to Samuel with the resources for the RTLDraw. Thought I might as well let Gemini translate it to english and put is here, so it is documented somewhere.
1. Configurable Graph Drawing Algorithms (Master’s Thesis)
https://www.tcs.uni-luebeck.de/downloads/papers/2011/2011-configurable-graph-drawing-algorithms-jannis-pohlmann.pdf
I found the examples here particularly good. Many of the examples in RTLDraw come directly from this.
2. Handbook of Graph Drawing and Visualization (Chapter 13)
https://cs.brown.edu/people/rtamassi/gdhandbook/
This is essentially the "Bible" of graph drawing. It is a bit more theoretical, but packed with information.
3. A Technique for Drawing Directed Graphs (Graphviz Paper)
https://www.graphviz.org/documentation/TSE93.pdf
The paper on the Graphviz implementation. I’ve had this saved for a while but haven't really looked into it yet.
4. KLay Layered: Integral Layered Graph Drawing...
https://rtsys.informatik.uni-kiel.de/~biblio/downloads/papers/jvlc13.pdf
I just found this one. It seems to describe the exact problem we are facing, but I haven't had time to read it yet. It might be worth using ChatGPT to check if a deeper dive is justified.
You, 2 Dec, 14:48
https://research.nvidia.com/labs/lpr/ToolOrchestra/
Might be an interesting read for orchestrator and task splitting

You, 3 Dec, 11:08, Edited
https://arxiv.org/abs/2512.00045 "Assessing Large Language Models in Generating RTL Design Specifications" - Luca forwarded this, might be worth having alook
You, 19 Dec, 12:34
Also putting this here
https://arxiv.org/pdf/2512.08296 a paper on multi agent systems from google deep mind. Also has some things about when it does not make sense
and the nemotron models https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/

You, 19 Dec, 16:30
https://www.researchgate.net/publication/398303730_GenSoC_A_Multi-Agent-Assisted_SoC_Generation_Methodology_Leveraging_Open-Source_Hardware
You, 30 Jan, 08:31
https://github.com/riscv/learn a github repo tracking learning resources for riscv.
You, 20 Feb, 12:23
https://ahmedalsawi.github.io/posts/2026/02/verilator-running-my-first-uvm-with-verilator/ apparently verilator can run uvm
https://bitsbytesgates.com/eda,/ucis,/coverage/2026/02/15/BetterCoverageAnalysisWithAI.html coverage analysis with ai
https://arxiv.org/abs/2602.11865 inteĺligent ai delegation the newest deepmind paper
You, 20 Feb, 12:33
https://openai.com/index/harness-engineering/ interesting article about building a product with 0 manual lines of code
You, 21 Feb, 10:48
https://arxiv.org/abs/2512.14982 interesting oddity
Harald Kröll, 24 Feb, 10:23
https://arxiv.org/pdf/2602.11988 Prof. Vechev's team share doubts if repo level md files are helpful to solve tasks


11) https://www.moderndescartes.com/essays/llm_shibboleths/ - Impact of prompts on results

12) More in the same area: (chatgpt response to me asking for similar papers)
The closest direct hit is “Speaking the Right Language: The Impact of Expertise (Mis)Alignment in User-AI Interactions” by Palta et al. It studies 25,000 Bing Copilot conversations and explicitly measures user expertise, model-response expertise, and what happens when they are misaligned. The key finding maps closely onto the essay’s point: users have different domain vocabularies and expectations, and satisfaction drops when the model responds below the user’s expertise level; users also engage more when the model’s expertise level is commensurate with theirs.

For the software-engineering/code-generation version of the same idea, read “More Than a Score: Probing the Impact of Prompt Specificity on LLM Code Generation” by Zi, Menon, and Guha. It asks whether failures on specialized programming tasks are due to model incapability or insufficient prompt detail, then creates a framework that varies prompts from minimal to maximally detailed. Their analysis finds that explicit I/O specs, edge cases, and stepwise breakdowns drive improvements — basically formalizing why an expert’s prompt works better than a novice’s vague request.

For the human factors / prompt literacy angle, the classic paper is “Why Johnny Can’t Prompt: How Non-AI Experts Try (and Fail) to Design LLM Prompts”. It is older, from CHI 2023, but still probably the best empirical treatment of why non-experts struggle: participants experimented opportunistically rather than systematically, overgeneralized from human-to-human instruction, and lacked the mental model needed to make robust prompt changes.

There is also a narrower, very on-the-nose paper: “Prompt Engineering: How Prompt Vocabulary affects Domain Knowledge” by Dimitri Schreiter. It tests whether more specific vocabulary in STEM, law, and medicine improves LLM performance. Its result is more nuanced than “more jargon is better”: there appears to be an optimal specificity range rather than a monotonic improvement from increasingly technical vocabulary.

Finally, for the educational framing, “AI literacy and its implications for prompt engineering strategies” argues that prompt engineering is a skill for precise, well-structured interaction, and finds that higher-quality prompting predicts better LLM output; it also links prompting ability to AI literacy among non-experts.


13) Flipbook.page - great idea. Some breakdown in flipbook.md in this folder

14) Breakdown of the leaked claude code source code https://arxiv.org/pdf/2604.14228

15) [2604.01193] Embarrassingly Simple Self-Distillation Improves Code Generation https://arxiv.org/abs/2604.01193






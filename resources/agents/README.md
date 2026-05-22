# Agent Systems and Harnesses

Papers, articles, and code on the design of LLM-based agents: action spaces, harnesses, context engineering, multi-agent coordination, repository understanding, and reproducibility issues with agent tooling.

---

## Papers (offline)

### CodeAct — Wang et al., 2024
- **Title:** Executable Code Actions Elicit Better LLM Agents
- **arXiv:** [2402.01030](https://arxiv.org/abs/2402.01030)
- **Local:** `wang2024_codeact_executable-code-actions.pdf`
- **Summary:** Argues that letting an LLM agent emit *executable Python* as its action — instead of JSON tool calls — gives a unified, composable action space. Foundational paper for the "code-as-action" school of agent design and an obvious reference when explaining why we lean on executable code in our own harnesses.

### Toolformer — Schick et al., 2023
- **Title:** Toolformer: Language Models Can Teach Themselves to Use Tools
- **arXiv:** [2302.04761](https://arxiv.org/abs/2302.04761)
- **Local:** `2023_schick_toolformer.pdf`
- **Summary:** Self-supervised approach to teach an LLM to insert API calls into its own outputs by sampling candidate calls, executing them, and keeping only those whose result reduces downstream perplexity. Canonical reference for the "train the model to use tools" path.

### ReAct — Yao et al., 2023
- **Title:** ReAct: Synergizing Reasoning and Acting in Language Models
- **arXiv:** [2210.03629](https://arxiv.org/abs/2210.03629)
- **Local:** `2023_yao_react.pdf`
- **Summary:** Interleaves "thought" (free-form reasoning) and "action" (tool use) in the same generation loop. Almost every modern agent harness inherits the pattern. Cite alongside CodeAct when introducing the agent control loop.

### Gorilla — Patil et al., 2023
- **Title:** Gorilla: Large Language Model Connected with Massive APIs
- **arXiv:** [2305.15334](https://arxiv.org/abs/2305.15334)
- **Local:** `2023_patil_gorilla-large-language-model-connected-with-massive-apis.pdf`
- **Summary:** Fine-tunes an LLM to call APIs from a corpus of thousands (HuggingFace, TensorFlow Hub, etc.). Introduces an evaluation methodology that became the basis for the Berkeley Function Calling Leaderboard. Useful reference when discussing tool calls at API-zoo scale.

### Code as Policies — Liang et al., 2023
- **Title:** Code as Policies: Language Model Programs for Embodied Control
- **arXiv:** [2209.07753](https://arxiv.org/abs/2209.07753)
- **Local:** `2022_liang_code-as-policies.pdf`
- **Summary:** Embodied/robotics counterpart to CodeAct: LLM emits Python that calls perception/control primitives, controlling a robot end-to-end. The clearest non-software example that "the action space should be a programming language."

### ACE — Zhang et al., 2025
- **Title:** Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models
- **arXiv:** [2510.04618](https://arxiv.org/abs/2510.04618)
- **Local:** `zhang2025_agentic-context-engineering.pdf`
- **Summary:** Frames context as an evolving "playbook" that an agent accumulates, refines, and organizes through a generator/reflector/curator loop, instead of relying on weight updates or terse summaries. Avoids the "brevity bias" and "context collapse" failure modes of naive iterative-rewriting approaches.

### Dive into Claude Code — Liu et al., 2026
- **Title:** Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems
- **arXiv:** [2604.14228](https://arxiv.org/abs/2604.14228)
- **Local:** `2026_dive-into-claude-code.pdf`
- **Summary:** Analysis of the leaked/published Claude Code TypeScript source plus a comparison with the open-source agent OpenClaw. Surfaces five recurring values that drive agent architecture (decision authority, safety, reliable execution, capability amplification, etc.). Worth reading to see what design choices a production agent harness actually makes.

### Cognitive Architecture — Knowledge Layer — Roynard, 2026
- **Title:** The Missing Knowledge Layer in Cognitive Architectures for AI Agents
- **arXiv:** [2604.11364](https://arxiv.org/abs/2604.11364)
- **Local:** `2026_memory-knowledge-wisdom-intelligence-agents.pdf`
- **Summary:** Argues that the popular CoALA / JEPA cognitive-architecture frameworks lack a distinct *knowledge* layer with its own persistence semantics, conflating long-lived facts with episodic memory. Survey + proposal for separating memory, knowledge, and (in some treatments) wisdom/intelligence in agents.

### RPG-Encoder — Luo et al., 2026
- **Title:** Closing the Loop: Universal Repository Representation with RPG-Encoder
- **arXiv:** [2602.02084](https://arxiv.org/abs/2602.02084)
- **Local:** `2026_repo-graph-code-construction.pdf`
- **Summary:** Generalizes the Repository Planning Graph from a static generative blueprint into a unified representation for both repository comprehension and generation, framed as inverse processes. Relevant for any repo-graph work in our codebase tools — and for handling updates/changes over time.

### Intelligent AI Delegation — Tomašev et al., 2026 (DeepMind)
- **Title:** Intelligent AI Delegation
- **arXiv:** [2602.11865](https://arxiv.org/abs/2602.11865)
- **Local:** `2026_deepmind_intelligent-ai-delegation.pdf`
- **Summary:** An adaptive framework for task allocation across agents/humans that incorporates trust assessment and tolerates failures, instead of relying on simple heuristic decomposition. Useful reading for any orchestrator work.

### Towards a Science of Scaling Agent Systems — Kim et al., 2025
- **Title:** Towards a Science of Scaling Agent Systems
- **arXiv:** [2512.08296](https://arxiv.org/abs/2512.08296)
- **Local:** `2025_deepmind_multi-agent-systems.pdf`
- **Summary:** Empirical scaling laws for agentic systems across 260 configurations (Single-Agent + four Multi-Agent topologies × six benchmarks × three model sizes). Includes findings about *when multi-agent doesn't pay off*, which is exactly the bit Sandro flagged as interesting in the inbox.

### Is Grep All You Need? — Sen et al., 2026
- **Title:** Is Grep All You Need? How Agent Harnesses Reshape Agentic Search
- **arXiv:** [2605.15184](https://arxiv.org/abs/2605.15184)
- **Local:** `2026_is-grep-all-you-need.pdf`
- **Summary:** Empirical study (PwC) arguing that retrieval-strategy effectiveness depends on the *agent harness*, not the retriever in isolation. Compares lexical/dense retrieval and tool-mediated search across provider CLI harnesses (Claude Code, Codex, Gemini CLI — where the model has shell `grep`) vs. custom SDK harnesses, and looks at robustness to corpus noise and at whether tool results are injected inline or written to files the agent must read. Sandro's read: agrees with the premise (tool-based retrieval can beat vector stores, and the harness changes everything) but came away not very impressed overall. Pairs with the CodeGraph repo below.

### MEMO: Memory as a Model — Quek et al., 2026
- **Title:** MEMO: Memory as a Model
- **arXiv:** [2605.15156](https://arxiv.org/abs/2605.15156)
- **Local:** `2026_memo-memory-as-a-model.pdf`
- **Summary:** Encodes new knowledge into a dedicated MEMORY model while keeping the base LLM frozen — positioned as a fourth option alongside RAG, in-context learning, and continued training/fine-tuning. Claims it captures cross-document relationships, is robust to retrieval noise, avoids catastrophic forgetting, needs no access to LLM weights/logits (plug-and-play with closed models), and has retrieval cost independent of corpus size at inference. Evaluated on BrowseComp-Plus, NarrativeQA, MuSiQue. Sandro kept it for its pros/cons discussion of RAG vs. ICL vs. training on the codebase — relevant to the context-and-retrieval chapter.

---

## Web articles & repos (link-only)

- **NVIDIA — Tool Orchestra:** https://research.nvidia.com/labs/lpr/ToolOrchestra/ — Orchestrator + task-splitting work; relevant for our orchestrator.
- **Anthropic — Code execution with MCP:** https://www.anthropic.com/engineering/code-execution-with-mcp — Anthropic's argument for building API/tool calls as code-execution rather than per-tool JSON envelopes. Companion to CodeAct above.
- **Microsoft — RPG-ZeroRepo (repo):** https://github.com/microsoft/RPG-ZeroRepo — Code release for repo planning graphs (sister work to RPG-Encoder above). "All code will be released in the next few weeks" — verify availability.
- **memodb-io / Acontext (repo):** https://github.com/memodb-io/Acontext — Pointer from a Twitter/X thread, https://x.com/hasantoxr/status/1993260004145836480
- **Hunch — CLI LLM completion (repo):** https://github.com/es617/hunch — Command-line LLM completion that uses the built-in 3B model on macOS Tahoe. Worth a look as a tiny harness.
- **The Big Prompt Library (repo):** https://github.com/0xeb/TheBigPromptLibrary — Reverse-engineered system prompts of many popular GPTs / agents (Perplexity, etc.). Useful as inspiration / reference.
- **CodeGraph (repo):** https://github.com/colbymchenry/codegraph — Pre-indexed code knowledge graph exposed to Claude Code as an MCP server. tree-sitter parses source → AST → symbols/edges stored in a local SQLite (+FTS5) graph, queried via `codegraph_explore` / `search` / `callers` / `impact` instead of grep/glob/Read. Reports large drops in exploration tool-calls and latency on real codebases (VS Code, Swift compiler, etc.). Sandro flagged it specifically for the **concrete tests** (`__tests__`, vitest config, and a `codegraph affected` command that maps changed files → affected test files). Natural counterpoint to "Is Grep All You Need?" above and a sibling to the RPG-Encoder repo-graph work.

---

## Reproducibility / tooling note

**Anthropic Claude Code "adaptive thinking" drama (Feb 2026):** With Opus 4.6, Anthropic shipped adaptive thinking and quietly lowered Claude Code's default effort level from "high" to "medium," producing a measured ~67% drop in reasoning depth across thousands of sessions (telemetry by an AMD AI director, 6,852 sessions).
- **GitHub issue:** https://github.com/anthropics/claude-code/issues/42796
- **Write-up:** https://drive.google.com/file/d/1KPdA-uWJ3yeSHFlQ9rPYThiNJzVJcdfH/view
- **Why it matters for us:** Reproducibility of measurements with closed agents is fragile. Less of a problem when using open-source clones, but worth documenting the failure mode.

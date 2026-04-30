# RTL & Chip Design

LLM/agent applications to RTL generation, verification, and design-space exploration. Core territory for the startup. Includes the main RTL benchmarks and recent work that argues SLMs + agents close most of the gap to frontier LLMs on hardware tasks.

---

## Benchmarks

### CVDP (NVIDIA) — Pinckney et al., 2025
- **Title:** Comprehensive Verilog Design Problems: A Next-Generation Benchmark Dataset for Evaluating Large Language Models and Agents on RTL Design and Verification
- **arXiv:** [2506.14074](https://arxiv.org/abs/2506.14074)
- **Local:** `2025_nvidia_cvdp_verilog-design-problems.pdf`
- **Summary:** 783 problems across 13 task categories (RTL generation, verification, debugging, spec alignment, Q&A) authored by hardware engineers, in both non-agentic and agentic formats. Authors argue VerilogEval/RTLLM are no longer challenging enough — SOTA models achieve ≤34% pass@1 on code generation here. **This is the benchmark Sandro singled out as the realistic one.**

### VerilogEval — Liu et al., 2023
- **Title:** VerilogEval: Evaluating Large Language Models for Verilog Code Generation
- **arXiv:** [2309.07544](https://arxiv.org/abs/2309.07544)
- **Local:** `2023_verilogeval.pdf`
- **Summary:** 156 self-contained Verilog code-generation problems from HDLBits, ranging from combinational circuits to FSMs. Metric: pass@k. The original LLM-on-Verilog benchmark.

### Revisiting VerilogEval — Pinckney et al., 2024
- **Title:** Revisiting VerilogEval: A Year of Improvements in Large-Language Models for Hardware Code Generation
- **arXiv:** [2408.11053](https://arxiv.org/abs/2408.11053)
- **Local:** `2024_revisiting-verilogeval.pdf`
- **Summary:** Re-evaluates new commercial and open models on VerilogEval, extends it with specification-to-RTL tasks, in-context learning, and structured failure analysis.

### RTLLM — Lu et al., 2023
- **Title:** RTLLM: An Open-Source Benchmark for Design RTL Generation with Large Language Model
- **arXiv:** [2308.05345](https://arxiv.org/abs/2308.05345)
- **Local:** `2023_rtllm.pdf`
- **Summary:** Larger, more complex RTL generation tasks than the early benchmarks; evaluates not just correctness but design quality. Metric: pass@k.

### RTL-Repo — Allam et al., 2024
- **Title:** RTL-Repo: A Benchmark for Evaluating LLMs on Large-Scale RTL Design Projects
- **arXiv:** [2405.17378](https://arxiv.org/abs/2405.17378)
- **Local:** `2024_rtlrepo.pdf`
- **Summary:** ~4000 Verilog samples extracted from public GitHub repos, with full repo context. Evaluates code completion in multi-file projects rather than self-contained snippets.

---

## Methods & systems

### ACE-RTL — Deng et al., 2026
- **Title:** ACE-RTL: When Agentic Context Evolution Meets RTL-Specialized LLMs
- **arXiv:** [2602.10218](https://arxiv.org/abs/2602.10218)
- **Local:** `2026_ace-for-rtl.pdf`
- **Summary:** Combines a domain-trained RTL-specialized model with the agentic-context-evolution loop (sister of ACE in `agents/`). Tries to unify the two historically separate paths in LLM-for-RTL: train-a-better-model vs. wrap-a-frontier-model-in-an-agent.

### Understanding & Mitigating RTL Errors — Zhang et al., 2025
- **Title:** Understanding and Mitigating Errors of LLM-Generated RTL Code
- **arXiv:** [2508.05266](https://arxiv.org/abs/2508.05266)
- **Local:** `2025_rtl-llm-error-mitigation.pdf`
- **Summary:** Error analysis finds most RTL failures stem from missing programming knowledge / circuit understanding / ambiguous specs / multimodal misreads — *not* deficient reasoning. Proposes RAG-based knowledge base, design-description prompts, and other targeted corrections. Sandro flagged paper quality as low but the failure taxonomy and worked examples are useful.

### GENIAL — Bouvier et al., 2025 (Huawei)
- **Title:** GENIAL: Generative Design Space Exploration via Network Inversion for Low-Power Algorithmic Logic Units
- **arXiv:** [2507.18989](https://arxiv.org/abs/2507.18989)
- **Local:** `2025_huawei_genial-design-space-exploration.pdf`
- **Repo:** https://github.com/huawei-csl/GENIAL
- **Summary:** Transformer-based surrogate model for arithmetic-unit (multiplier) design, optimized via *network inversion* — interesting trick for low-power DSE. The "inversion" framing is the part Sandro flagged as worth thinking about.

### David vs. Goliath (SLMs + agents on CVDP) — Shankar et al., 2025
- **Title:** David vs. Goliath: Can Small Models Win Big with Agentic AI in Hardware Design?
- **arXiv:** [2512.05073](https://arxiv.org/abs/2512.05073)
- **Local:** `2025_slm-agentic-cvdp.pdf`
- **Summary:** Evaluates small language models in a curated agentic framework on NVIDIA's CVDP benchmark. Shows that task decomposition + iterative feedback closes most of the gap to frontier LLMs on hardware tasks at a fraction of the cost. Pairs naturally with the NVIDIA "SLMs are the future of agentic AI" position paper (in `models-and-training/`).

### LLM-Generated RTL Specifications — Huang et al., 2025
- **Title:** Assessing Large Language Models in Generating RTL Design Specifications
- **arXiv:** [2512.00045](https://arxiv.org/abs/2512.00045)
- **Local:** `2025_llm-rtl-design-specifications.pdf`
- **Summary:** RTL → spec is the under-studied direction; this paper introduces metrics for evaluating generated specs and tests prompting strategies. Forwarded to Sandro by Luca and worth a look for our spec-extraction features.

---

## Web articles, repos & links

- **GenSoC — Multi-Agent SoC Generation:** https://www.researchgate.net/publication/398303730_GenSoC_A_Multi-Agent-Assisted_SoC_Generation_Methodology_Leveraging_Open-Source_Hardware
- **Verilator + UVM blog post:** https://ahmedalsawi.github.io/posts/2026/02/verilator-running-my-first-uvm-with-verilator/ — Apparently Verilator can run UVM now.
- **AI-driven coverage analysis:** https://bitsbytesgates.com/eda,/ucis,/coverage/2026/02/15/BetterCoverageAnalysisWithAI.html

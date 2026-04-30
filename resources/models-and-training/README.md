# Models & Training

Underlying-model territory: small models, training tricks, self-distillation, recursive reasoning. Less about agent harnesses, more about the engine inside them.

---

## Papers (offline)

### Tiny Recursive Model — Jolicoeur-Martineau, 2025
- **Title:** Less is More: Recursive Reasoning with Tiny Networks
- **arXiv:** [2510.04871](https://arxiv.org/abs/2510.04871) (also [alphaxiv mirror](https://www.alphaxiv.org/pdf/2510.04871))
- **Local:** `2025_recursive-reasoning-tiny-networks.pdf`
- **Summary:** Builds on the Hierarchical Reasoning Model (HRM) idea — two small networks recursing at different frequencies — and proposes Tiny Recursive Model (TRM), a simpler variant that beats LLMs on hard puzzle tasks (Sudoku, Maze, ARC-AGI) at ~27M parameters and ~1k examples. Not directly applicable to RTL but a striking demonstration of the small-network-with-structure school.

### Self-Distillation Improves Code Generation — Zhang, 2026
- **Title:** Embarrassingly Simple Self-Distillation Improves Code Generation
- **arXiv:** [2604.01193](https://arxiv.org/abs/2604.01193) (April 1 paper, but the result is real)
- **Local:** `2026_self-distillation-code-generation.pdf`
- **Summary:** Sample solutions from the model itself with the right temperature/truncation, then SFT on those samples. Improves Qwen3-30B-Instruct from 42.4% → 55.3% pass@1 on LiveCodeBench v6, with the gains concentrated on harder problems. Generalizes across Qwen and Llama at 4B/8B/30B.

---

## Position pieces & model families (link-only)

- **NVIDIA — "Small Language Models are the future of agentic AI":** Position paper from NVIDIA. Pairs naturally with `rtl-and-chip-design/2025_slm-agentic-cvdp.pdf` (David vs. Goliath). Search the NVIDIA research site for the full PDF.
- **NVIDIA — Nemotron model family:** https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/
- **Gemma 4 (Google):** New release noted in the inbox — interesting to try as an open-weights option.

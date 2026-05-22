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

### Negation Neglect — Mayne et al., 2026
- **Title:** Negation Neglect: When models fail to learn negations in training
- **arXiv:** [2605.13829](https://arxiv.org/abs/2605.13829)
- **Local:** `2026_negation-neglect.pdf`
- **Summary:** Fine-tuning on documents that *flag a claim as false* can make a model believe the claim is **true**. Training on text that repeatedly insists "the Ed Sheeran 100m-gold story is false" (negation in a separate sentence) pushes belief in the false claim from ~2.5% → ~88.6% — close to the ~92.4% you get training on the claim with no negation at all. The models recognize the claim as false when the same docs are given *in context*, just not after training on them. Negations are learned correctly only when *local* to the claim ("Ed Sheeran did not win the 100m gold"). The effect generalizes to other epistemic qualifiers (e.g. content labeled fictional is learned as true) and to behaviors (training on transcripts flagged as malicious can induce the behavior), so there's a real AI-safety angle. Owain Evans group. Sandro kept it "more for fun": LLMs have trouble learning simple negations.

### Why LLMs Struggle to Count Letters — Fu et al., 2024
- **Title:** Why Do Large Language Models (LLMs) Struggle to Count Letters?
- **arXiv:** [2412.18626](https://arxiv.org/abs/2412.18626)
- **Local:** `2024_struggle-counting-letters.pdf`
- **Summary:** Empirical study of letter-counting failures (the "strawberry" problem). Shows accuracy degrades with training-corpus frequency and counting complexity, and that chain-of-thought prompting does not fix it. Mechanical explanation: tokenization hides characters from the model. Cited from Chapter 2 (Tool Calls).

### The Genius Paradox — Xu & Ma, 2024
- **Title:** LLM The Genius Paradox: A Linguistic and Math Expert's Struggle with Simple Word-based Counting Problems
- **arXiv:** [2410.14166](https://arxiv.org/abs/2410.14166)
- **Local:** `2024_genius-paradox-counting-letters.pdf`
- **Summary:** Companion analysis of the strawberry phenomenon: a model that solves graduate-level math word problems can fail a primary-school spelling task. Tokenization is again the structural cause. Cited from Chapter 2 (Tool Calls).

---

## Position pieces & model families (link-only)

- **NVIDIA — "Small Language Models are the future of agentic AI":** Position paper from NVIDIA. Pairs naturally with `rtl-and-chip-design/2025_slm-agentic-cvdp.pdf` (David vs. Goliath). Search the NVIDIA research site for the full PDF.
- **NVIDIA — Nemotron model family:** https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/
- **Gemma 4 (Google):** New release noted in the inbox — interesting to try as an open-weights option.

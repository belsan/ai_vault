# AI Impact & Failures

Two intertwined topics from the README's interest list:
1. **Impact of AI on engineering professions** — case studies of 0-manual-line-of-code products, automated architecture discovery, etc.
2. **AI failures and oddities** — real cases where AI systems mess up, plus reproducibility issues and surprising-behaviour findings.

---

## Papers (offline)

### Computer Architecture's AlphaZero Moment — Sankaralingam et al., 2026
- **Title:** Computer Architecture's AlphaZero Moment: Automated Discovery in an Encircled World
- **arXiv:** [2604.03312](https://arxiv.org/abs/2604.03312)
- **Local:** `2026_llm-driven-architecture-design.pdf`
- **Summary:** Argues that with Moore/Dennard scaling exhausted, human-driven architecture exploration (50–100 designs per generation, <0.001% of the space) is no longer adequate. Reports LLM-driven systems generating architectures, simulating performance, and outperforming human baselines by 2–3× in their experiments. Strong "AI is changing how engineering happens" piece for the impact part of the corpus.

### Prompt Repetition Improves Non-Reasoning LLMs — Leviathan, 2025
- **Title:** Prompt Repetition Improves Non-Reasoning LLMs
- **arXiv:** [2512.14982](https://arxiv.org/abs/2512.14982)
- **Local:** `2025_oddity.pdf`
- **Summary:** When *not* using reasoning, simply repeating the input prompt improves performance for popular models (Gemini, GPT, Claude, Deepseek) without increasing generated tokens or latency. The "interesting oddity" Sandro flagged.

---

## Web articles & reports

- **OpenAI — A Model Disproved a Central Conjecture in Discrete Geometry (2026):** https://openai.com/index/model-disproves-discrete-geometry-conjecture/ — Local archive: `2026_openai_disproves-discrete-geometry-conjecture.md` (reading-note summary). An internal OpenAI *general-purpose* reasoning model (not a math-specialized or scaffolded system) autonomously disproved Erdős's n^(1+o(1)) conjecture for the planar unit-distance problem, constructing configurations with ≥ n^(1+δ) unit-distance pairs (δ=0.014 in Will Sawin's refinement) using deep algebraic number theory (class field towers, Golod–Shafarevich). Externally verified with a companion paper; Gowers calls it "a milestone in AI mathematics." First prominent, subfield-central open problem solved autonomously by AI — slots alongside the manuscript intro's Erdős #728 / KAIST achievements, and is a stronger data point for being a general-purpose model.
- **OpenAI — Where the Goblins Came From (2026):** https://openai.com/index/where-the-goblins-came-from/ — Local archive: `2026_openai_where-the-goblins-came-from.md` (reading-note summary, not verbatim). OpenAI traces how their models picked up a "goblin/gremlin" verbal tic, tracking it to a reward signal tied to the (now-retired) "Nerdy" personality, then watching it spread via RL reward generalization and an SFT feedback loop. Sandro's verdict: fun read, no impact on what we do — but a clean, low-stakes case study of reward mis-generalization and behavior auditing.
- **OpenAI — Harness Engineering ("0 manual lines of code"):** https://openai.com/index/harness-engineering/ — Article on building a product with zero manually-written lines of code; sits squarely on the "future of engineering" axis.
- **Hyper-realistic AI faces vs. photos:** https://journals.sagepub.com/doi/10.1177/09567976231207095 — Sage / *Psychological Science* paper showing humans cannot reliably distinguish AI-generated faces from real photographs (paywalled; link only).

## Reproducibility / failure-mode notes

The "Anthropic Claude Code adaptive thinking" reproducibility incident (Feb 2026) is logged in `agents/README.md` since it concerns agent tooling.

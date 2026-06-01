# AI Security & Safety

Attacks on and failures of model safety mechanisms: jailbreaks, prompt injection, refusal / over-refusal behaviour, and the robustness of alignment under adversarial phrasing. Distinct from `ai-impact-and-failures/` (real-world impact and surprising-behaviour oddities) — this folder is specifically about the security/safety surface. Connects to the manuscript's "Building Reliable Systems" chapter (prompt injection, confused deputy, exfiltration, sandboxing).

---

## Papers (offline)

### Adversarial Poetry as a Universal Jailbreak — Bisconti et al., 2025
- **Title:** Adversarial Poetry as a Universal Single-Turn Jailbreak Mechanism in Large Language Models
- **arXiv:** [2511.15304](https://arxiv.org/abs/2511.15304)
- **Local:** `2025_bisconti_adversarial-poetry-jailbreak.pdf`
- **Summary:** Reframing a harmful request as *verse* is a single-turn jailbreak that transfers across 25 frontier proprietary and open-weight models — some providers' attack-success rate exceeds 90%. Converting 1,200 MLCommons harmful prompts to poetry via a standardized meta-prompt raised ASR up to ~18× over prose baselines (hand-crafted poems ~62% average, automated meta-prompt conversions ~43%). Attacks transfer across CBRN, manipulation, cyber-offence, and loss-of-control taxonomies; outputs scored by an ensemble of 3 open-weight judges validated against a human-labeled subset. Operational details are deliberately withheld. Concrete and primary (a novel, broadly-transferable attack), but the contribution is about the *safety surface*, not prompt quality — hence here rather than in `prompt-engineering/`. Takeaway for us: stylistic/format variation alone can defeat current safety training, a vivid reminder of how brittle alignment is to surface phrasing.

### Refusal Is Mediated by a Single Direction — Arditi et al., 2024
- **Title:** Refusal in Language Models Is Mediated by a Single Direction
- **arXiv:** [2406.11717](https://arxiv.org/abs/2406.11717) (NeurIPS 2024)
- **Local:** `2024_arditi_refusal-single-direction.pdf`
- **Summary:** Foundational paper for the single-direction refusal story. Across 13 open-source chat models up to 72B, the authors find one direction in the residual stream such that *erasing* it (projecting it out of every activation during the forward pass) makes the model stop refusing harmful instructions, while *adding* it elicits refusal on harmless ones. The direction is recovered by a simple difference-of-means over contrastive pairs of harmful/harmless instructions. Yields a white-box jailbreak with minimal damage to other capabilities, plus a mechanistic account of how adversarial suffixes work (they suppress propagation of the refusal direction). The original reference for Singhle's 2026 cross-model follow-up; cite when discussing how brittle current safety fine-tuning is to weight-level access.

### The Geometry of Refusal — Wollschläger et al., 2025
- **Title:** The Geometry of Refusal in Large Language Models: Concept Cones and Representational Independence
- **arXiv:** [2502.17420](https://arxiv.org/abs/2502.17420) (ICML 2025; v2 Feb 2026)
- **Local:** `2025_wollschlaeger_geometry-of-refusal.pdf`
- **Summary:** Counterweight to Arditi et al.'s one-direction claim. Proposes a gradient-based representation-engineering method (Refusal Direction Optimisation, RDO) and finds *multiple independent* refusal directions, plus multi-dimensional *concept cones* whose interior directions all mediate refusal. Introduces the *representational independence* notion: orthogonality is not enough to guarantee that two directions act independently under intervention (non-linear effects matter). Source of the bypass-gap-style layer-selection criterion that Singhle (2026) leans on for Qwen. Read this in tandem with Arditi: the picture is richer than a single direction, but the *practical* attack still reduces to one direction at one layer once the layer is chosen well.

### Classification ≠ Causation in Refusal Directions — Singhle, 2026
- **Title:** Classification ≠ Causation in *Refusal Directions*: Gemma-2-2b-it and Qwen-2.5-3B-Instruct
- **Web:** [lonehacker.github.io/mech-interp](https://lonehacker.github.io/mech-interp/index.html) · [code](https://github.com/lonehacker/mech-interp)
- **Local:** `2026_singhle_refusal-directions-classification-vs-causation.md`
- **Summary:** Replication-plus-extension of the Arditi et al. (2024) *single-direction refusal* result on two open-weight instruct models. The headline experiment strips refusal from Qwen-2.5-3B-Instruct with five lines of substantive Python: load model, diff-of-means of activations on two ~30-prompt batches (harmful vs harmless), project the resulting direction out of the residual stream during generation. On Gemma-2-2b-it the same recipe drops HarmBench refusal 99% → 8% (N=200, dual-judge) with TinyMMLU general-capability accuracy unchanged. No adversarial optimization, no jailbreak prompt, no gradient access at inference time — the attack is a single linear projection at one layer (L13 for Gemma, L22–23 for Qwen). The methodological contribution is the *classification vs causation* gap: directions that perfectly classify harmful-vs-harmless prompts (AUC = 1.0) are causally inert under ablation; the one direction that actually mediates refusal is only findable by ranking candidates by their intervention effect on behavior. On Qwen, every layer (including L0 embeddings) classifies at AUC ≥ 0.994, so AUC-based layer selection picks an inert layer — only the bypass-gap criterion (which layer's ablation actually drops the refusal-token logit) localizes the mechanism. Takeaway for us: open-weight refusal training is a speed bump, not a wall — relevant to the manuscript's reliable-systems chapter as a counterweight to treating model-level refusal as a defense-in-depth layer.

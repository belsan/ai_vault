# AI Security & Safety

Attacks on and failures of model safety mechanisms: jailbreaks, prompt injection, refusal / over-refusal behaviour, and the robustness of alignment under adversarial phrasing. Distinct from `ai-impact-and-failures/` (real-world impact and surprising-behaviour oddities) — this folder is specifically about the security/safety surface. Connects to the manuscript's "Building Reliable Systems" chapter (prompt injection, confused deputy, exfiltration, sandboxing).

---

## Papers (offline)

### Adversarial Poetry as a Universal Jailbreak — Bisconti et al., 2025
- **Title:** Adversarial Poetry as a Universal Single-Turn Jailbreak Mechanism in Large Language Models
- **arXiv:** [2511.15304](https://arxiv.org/abs/2511.15304)
- **Local:** `2025_bisconti_adversarial-poetry-jailbreak.pdf`
- **Summary:** Reframing a harmful request as *verse* is a single-turn jailbreak that transfers across 25 frontier proprietary and open-weight models — some providers' attack-success rate exceeds 90%. Converting 1,200 MLCommons harmful prompts to poetry via a standardized meta-prompt raised ASR up to ~18× over prose baselines (hand-crafted poems ~62% average, automated meta-prompt conversions ~43%). Attacks transfer across CBRN, manipulation, cyber-offence, and loss-of-control taxonomies; outputs scored by an ensemble of 3 open-weight judges validated against a human-labeled subset. Operational details are deliberately withheld. Concrete and primary (a novel, broadly-transferable attack), but the contribution is about the *safety surface*, not prompt quality — hence here rather than in `prompt-engineering/`. Takeaway for us: stylistic/format variation alone can defeat current safety training, a vivid reminder of how brittle alignment is to surface phrasing.

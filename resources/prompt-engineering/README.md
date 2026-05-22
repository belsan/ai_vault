# Prompt Engineering

Why phrasing matters, why expert vocabulary outperforms novice phrasing, and what context files / repo-level documentation actually do for coding agents. The narrative starts with Lee's "shibboleths" essay and is backed up by the Palta, Schreiter, Zi, and Zamfirescu-Pereira papers.

---

## Anchor essay

### LLM Shibboleths — Lee, 2025
- **URL:** https://www.moderndescartes.com/essays/llm_shibboleths/
- **Local (notes):** `2025_lee_llm-shibboleths.md`
- **Summary:** Argues that the vocabulary you use silently selects which slice of the training distribution the model draws from — experts use ingroup phrases ("deleted_at", "differential diagnosis") and get expert output; novices ask in novice phrasing and get novice-quality output. Coins "Gell-Mann AmnesiAI": same model, different perceived quality across domains.

---

## Empirical / measurement papers

### Speaking the Right Language — Palta et al., 2025
- **Title:** Speaking the Right Language: The Impact of Expertise (Mis)Alignment in User-AI Interactions
- **arXiv:** [2502.18685](https://arxiv.org/abs/2502.18685)
- **Local:** `2025_palta_speaking-the-right-language.pdf`
- **Summary:** Analyzes 25,000 Bing Copilot conversations with an ordinal expertise classifier. Misalignment — model responding *below* the user's expertise — drops user satisfaction, especially on complex tasks. Users engage more (longer turns) when the model matches their level. Direct empirical version of the shibboleths essay.

### Prompt Vocabulary Affects Domain Knowledge — Schreiter, 2025
- **Title:** Prompt Engineering: How Prompt Vocabulary affects Domain Knowledge
- **arXiv:** [2505.17037](https://arxiv.org/abs/2505.17037)
- **Local:** `2025_schreiter_prompt-vocabulary-domain-knowledge.pdf`
- **Summary:** Synonymization framework systematically substitutes nouns/verbs/adjectives at varying specificity levels, measured on 4 LLMs across STEM/law/medicine. Result is *not* "more jargon = better" — there are narrow specificity sweet spots, beyond which performance degrades.

### More Than a Score — Zi, Menon & Guha, 2025
- **Title:** More Than a Score: Probing the Impact of Prompt Specificity on LLM Code Generation
- **arXiv:** [2508.03678](https://arxiv.org/abs/2508.03678)
- **Local:** `2025_zi_prompt-specificity-code-generation.pdf`
- **Summary:** Introduces PartialOrderEval: take any code-gen benchmark and augment it with a partial order of prompts from minimal to maximally detailed. Finds explicit I/O specs, edge-case handling, and stepwise breakdowns drive most of the prompt-detail-induced improvement.

### IatroBench — Gringras, 2026
- **Title:** IatroBench: Pre-Registered Evidence of Iatrogenic Harm from AI Safety Measures
- **arXiv:** [2604.07709](https://arxiv.org/abs/2604.07709)
- **Local:** `2026_gringras_iatrobench.pdf`
- **Summary:** The paper's headline is a clinical-safety argument, but the part worth keeping is one of the cleanest prompt-sensitivity demonstrations around: the *same model, same weights, same inference pass* refuses a question in layperson framing yet returns a complete expert answer when the identical clinical question is reframed as "I'm a physician; a patient presents with…". Across 60 pre-registered scenarios × 6 frontier models (3,600 responses), physician framing beats layperson framing on safety-colliding actions by a decoupling gap of +0.38 (binary hit-rates drop 13.1 pp under layperson framing), and the gap is widest for the most safety-trained model (Opus, +0.65). Concrete "one word of framing flips the outcome" evidence — the same identity/expertise-framing effect as Lee's shibboleths and Palta's expertise-alignment work, but with a sharp before/after on a single phrasing change. The iatrogenic-harm thesis is secondary for our purposes.

### Why Johnny Can't Prompt — Zamfirescu-Pereira et al., CHI 2023
- **Venue:** Proceedings of the 2023 CHI Conference (CHI '23, Hamburg)
- **DOI:** https://doi.org/10.1145/3544548.3581388
- **PDF (mirror):** https://www.researchgate.net/publication/368577310_Why_Johnny_Can%27t_Prompt_How_Non-AI_Experts_Try_and_Fail_to_Design_LLM_Prompts
- **Local:** *not downloaded* (CHI paywalled, mirror would require account)
- **Summary:** First serious empirical study of how non-AI experts fail at prompt design. Participants experimented opportunistically rather than systematically, overgeneralized from human-to-human instruction, and lacked the mental model to make robust changes. Most-downloaded paper in CHI's history.

### Evaluating AGENTS.md — Gloaguen et al., 2026 (Vechev's group)
- **Title:** Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?
- **arXiv:** [2602.11988](https://arxiv.org/abs/2602.11988)
- **Local:** `2026_vechev_repo-md-files-helpful.pdf`
- **Summary:** Tests whether the now-widespread practice of dropping AGENTS.md / CLAUDE.md / README-for-agents into repos actually improves real-world task completion. Vechev's team is skeptical. Important counter-narrative for anyone shipping repo-level context files in their agent products.

---

## Prompt robustness & sensitivity benchmarks

The empirical-perturbation thread: how much do semantics-preserving rephrasings/format
changes move outputs, how do you measure it, and what (if anything) fixes it. This is the
gap the vocabulary/specificity papers above don't cover. (See also `ai-impact-and-failures/2025_oddity.pdf` for the prompt-repetition oddity.)

### Brittlebench — Romanou et al., 2026 (FAIR at Meta)
- **Title:** Brittlebench: Quantifying LLM Robustness via Prompt Sensitivity
- **arXiv:** [2603.13285](https://arxiv.org/abs/2603.13285)
- **Local:** `2026_romanou_brittlebench-prompt-sensitivity.pdf`
- **Summary:** The most *primary* of this batch. A theoretical framework that disentangles data-induced difficulty from prompt-induced brittleness, plus an evaluation pipeline (Brittlebench) applying semantics-preserving perturbations to popular benchmarks. Headline results: performance drops up to ~12% under perturbation, a *single* perturbation flips the relative ranking of models in 63% of cases, and prompt perturbations can account for up to half of a model's performance variance. Strong FAIR@Meta + EPFL author list (Dodge, A. Williams, Bosselut). Caveat on reproducibility: as of this version code is "to be released soon" — concrete and well-specified, but not yet independently runnable. The cleanest argument in the corpus for why static leaderboard deltas are untrustworthy.

### When Punctuation Matters — Seleznyov et al., 2025 (EMNLP Findings)
- **Title:** When Punctuation Matters: A Large-Scale Comparison of Prompt Robustness Methods for LLMs
- **Venue:** Findings of EMNLP 2025 — [aclanthology 2025.findings-emnlp.1109](https://aclanthology.org/2025.findings-emnlp.1109/)
- **Local:** `2025_seleznyov_punctuation-prompt-robustness.pdf`
- **Summary:** The most *reproducible* of the batch — peer-reviewed and code released (`github.com/AIRI-Institute/when-punctuation-matters`). First systematic, unified-framework comparison of 5 prompt-robustness methods (fine-tuned and in-context) across 8 open models (Llama/Qwen/Gemma) × 52 Natural-Instructions tasks, with GPT-4.1 and DeepSeek V3 as a frontier check. Practical "which robustness method actually helps" guidance. Pairs with Brittlebench: that one *measures* the problem, this one *compares the fixes*.

### JudgeSense — Bellibatlu, Raff & Zhang, 2026
- **Title:** JudgeSense: A Benchmark for Prompt Sensitivity in LLM-as-a-Judge Systems
- **arXiv:** [2604.23478](https://arxiv.org/abs/2604.23478)
- **Local:** `2026_bellibatlu_judgesense-judge-prompt-sensitivity.pdf`
- **Summary:** Directly relevant since we use LLM-as-judge. Releases a benchmark (code + dataset on GitHub & HF) of hand-validated prompt-paraphrase pairs across factuality, coherence, relevance, and preference, with full decision logs, to measure how far a judge's verdict moves under semantically-equivalent rephrasings. Findings: coherence is the most sensitivity-revealing task, factuality is stable, pairwise tasks show consistent position bias, and — usefully — model scale is *not* a reliable proxy for judge consistency (the newest/largest models aren't the most consistent). Concrete and fully reproducible; niche, but exactly our niche.

### Persona Prompts & False Refusal — Plaza-del-Arco et al., 2025
- **Title:** No for Some, Yes for Others: Persona Prompts and Other Sources of False Refusal in Language Models
- **arXiv:** [2509.08075](https://arxiv.org/abs/2509.08075)
- **Local:** `2025_plaza-del-arco_persona-false-refusal.pdf`
- **Summary:** The skeptical counterweight. Quantifies how 15 sociodemographic personas affect false-refusal rates across 16 models × 3 tasks × 9 paraphrases, with a sample-efficient Monte-Carlo method on public datasets (reproducible methodology; Röttger & Hovy among the authors). The conclusion cuts *against* persona hype: persona effects shrink as models get more capable, and model/task choice dominates — i.e. persona effects have likely been overestimated. Keep alongside IatroBench (which shows identity framing flipping clinical answers) so the corpus holds both the claim and the pushback rather than a one-sided story.

---

## Companion / TBD

- **AI literacy and its implications for prompt engineering strategies** — referenced via ChatGPT response in inbox; URL not yet resolved. Argues prompt-engineering ability tracks with general AI literacy among non-experts and predicts output quality.

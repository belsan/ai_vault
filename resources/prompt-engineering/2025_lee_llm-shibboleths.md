# LLM Shibboleths Determine AI Effectiveness

**Author:** Brian Kihoon Lee
**Date:** 2025-05-28
**Source:** https://www.moderndescartes.com/essays/llm_shibboleths/
**Tags:** LLMs, software engineering, expertise, prompt engineering

---

## Summary

An essay arguing that the *vocabulary* a user brings to an LLM silently determines which slice of the model's training distribution it draws from. Experts use "shibboleths" — phrases like `deleted_at`, "soft delete", "differential diagnosis" — that match how the corresponding ingroup actually writes, so the model responds in that register. Novices ask in novice phrasing and get back a summary of confused-novice content from the training data, with predictably weaker output. The asymmetry produces "Gell-Mann AmnesiAI": the same model can feel impressive in a domain you don't know and obviously wrong in a domain you do.

## Key claims

- Two users on the same model with the same factual question can have completely different experiences depending on phrasing.
- Example given: "what can cause runny nose" → cautious Dr. Google fluff. "runny nose differential diagnosis" → med-student-style braindump.
- For coding: backend domain expertise let the author work fluently with Cursor; frontend novice-ness yielded spaghetti callbacks. Roughly 75% of frontend time was spent learning enough to ask correctly, only 25% on AI-assisted coding.
- Implication for the future: artisanal code becomes a curiosity. Industrially-produced code dominates, gated by a smaller number of experts with the taste and shibboleths to spec out products.

## Why it's in this corpus

This essay frames the prompt-vocabulary / expertise-misalignment topic in vivid first-person terms and is the natural lead-in for the more empirical papers in this folder (Palta et al. 2025, Schreiter 2025, Zi et al. 2025, Zamfirescu-Pereira et al. CHI 2023).

## Source URL

https://www.moderndescartes.com/essays/llm_shibboleths/

# Learning Resources

Repos, tutorials, and small playground projects useful for onboarding (employees, master students, interns) or for spinning up a tractable RTL/agent example.

---

## Hardware

- **SERV — small RISC-V implementation:** https://github.com/olofk/serv — Small RISC-V core. Sandro flagged it as a good playground because it's much smaller and less convoluted than our current internal projects. Promising target for end-to-end agentic-RTL demos.
- **riscv/learn — curated RISC-V learning resources:** https://github.com/riscv/learn — GitHub repo aggregating learning material on RISC-V.

## Agents / LLM tooling

- **The Big Prompt Library:** https://github.com/0xeb/TheBigPromptLibrary — Reverse-engineered system prompts of many production GPTs (Perplexity, etc.). Useful as inspiration / reference when designing our own system prompts.
- **Hunch — CLI LLM completion:** https://github.com/es617/hunch — Terminal LLM completion using the on-device 3B model on macOS Tahoe. Tiny example of a self-contained harness.

(See also `agents/` for the more substantial agent papers and references.)

## Worked examples (offline)

- **Bendersky, *Retrieval Augmented Generation in Go* (2023):** Local archive of [eli.thegreenplace.net/2023/retrieval-augmented-generation-in-go/](https://eli.thegreenplace.net/2023/retrieval-augmented-generation-in-go/).
  - `bendersky_2023_rag_in_go.md` — clean markdown rendition for reading.
  - `bendersky_2023_rag_in_go.html` — stripped-down HTML archive (no styles or trackers).
  - Why we keep it: the post is the model for the kind of fundamental, framework-free worked example we want for the book's case-study chapters. It is referenced from `manuscript/notes/case_studies.md` and from the stub of `chapters/06_context_and_retrieval.tex`.

## Inspirations / unusual applications

- **Murphy VII, *BoVeX: Badness 0* (SIGBOVIK 2024):** `murphy_2024_bovex_sigbovik.pdf`.
  - Excerpt from the SIGBOVIK 2024 proceedings (pages 131–160, both versions of "Badness 0" plus the BoVeX paper itself), pulled out as a 30-page standalone PDF. Source: [http://www.sigbovik.org/2024/proceedings.pdf](http://www.sigbovik.org/2024/proceedings.pdf), pages 135–164 of the full proceedings.
  - BoVeX is a typesetting system that uses Llama to slightly rephrase paragraphs of an article so that TeX-style line-breaking produces lower "badness". The article is published in two versions side-by-side: "Knuth's version" with no rephrasing, and "Epsom's version" rephrased by the LLM. The paper itself is typeset by BoVeX.
  - Why we keep it: a model of how to use raw LLM probabilities to optimise something measurable. Goal is small, well-defined, impossible without an LLM, deeply nerdy. Useful as a reference point when discussing token-probability-driven applications, even if we do not work it up as a full case study in the book.
  - Companion links: [BoVeX homepage](http://tom7.org/bovex/), [BoVeX esolangs.org wiki page](https://esolangs.org/wiki/BoVeX), [tom7's youtube video](https://www.youtube.com/watch?v=Y65FRxE7uMc).

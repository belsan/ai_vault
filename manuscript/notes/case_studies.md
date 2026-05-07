# Notes on the case-study chapters

*A working document. Captures what we learned from looking at Bendersky's RAG-in-Go post and translating it into a chapter pattern. Not part of the manuscript proper. Lives here so the rule can be applied consistently when writing the other case-study chapters.*

## What a case study is for

The book has two register: the **discussion register**, where we lay out a design space, name the trade-offs, and recommend defaults; and the **demonstration register**, where we run something and report what happens. Either alone is weak.

- *Discussion alone* slides into the kind of vague advice §1.5 calls out. "RAG is good for X, the agentic approach is good for Y" is a sentence that survives any number of misreadings, and the reader has no purchase to test it.
- *Demonstration alone* is what tutorials are; the reader walks through the steps, runs the script, and learns nothing transferable about *when* this approach was the right one.

A case-study chapter is the place where we promise both. A short discussion of the design space, then one example worked through with multiple approaches measured side-by-side, then a recommendations section that the discussion would not have earned without the numbers.

## What makes a good case study

The Bendersky 2023 RAG-in-Go post is worth studying not because it is technically deep — it is fairly conventional 2023 RAG — but because the *structure* is exactly right.

1. **State the failure concretely.** Bendersky shows ChatGPT hallucinating about `GOTOOLCHAIN` before he proposes anything. The reader sees the broken behaviour with their own eyes. We should do the same: *here is the model failing; here is what we are going to fix.*

2. **Build the smallest thing that works.** SQLite, a cosine-similarity loop, no vector DB. A reader could implement it from scratch in an afternoon. The pedagogical lesson is the substrate, not the framework.

3. **Show the working answer side-by-side with the broken one.** The reader sees the same prompt produce two different outputs. The argument is in the diff.

4. **Name the generalisations the example does not implement, and link to them.** Bendersky says "vector databases exist, e.g. milvus or weaviate; we don't need one because the corpus is small". The example is honest about what it leaves out.

These four are the spine. Every case-study chapter we write should have all four.

## What a 2026 case study can do that a 2023 one couldn't

In 2023 the answer to "the LLM doesn't know about Go 1.21" was *clearly* RAG. In 2026 the answer is plural — the same problem now has at least three defensible solutions:

- Classic RAG with embeddings (Bendersky's approach)
- Agentic retrieval, where the agent uses `bash`, `grep`, `find`, `curl` directly
- A hybrid that orchestrates both via the agent's tool-calling loop
- (Sketched only:) graph-based retrieval for corpora with explicit relations

This means the post's structure can be extended in a way that pays for the chapter's existence: instead of one approach with a working answer, *we run all of them on the same benchmark and report the numbers*. The discussion-register sentence ("agentic is better for keyword-heavy queries") becomes a row in a table.

That is what makes the case study earn its place in 2026. A reader who finished Chapter 5 can build Approach B in fifty lines on top of code we already wrote. A reader who finished Chapter 2 can build Approach A in a hundred lines. The hybrid is thirty more lines. And then we measure them, on the same 20 questions, with the same model, and report what happened.

## The shape every case-study chapter should take

A case study chapter has six sections, give or take.

1. **The Problem.** A paragraph or two. Concrete, with a worked failure. *Here is the mode of brokenness; here is the question we are going to answer.*

2. **Approaches** (theoretical). Each candidate approach gets a subsection: what it is, what it costs, what it is good at, what it is bad at. The reader leaves this section with a clear mental model of the design space *before* seeing any numbers.

3. **The Worked Comparison.** Each approach is implemented, in pure Python, in `manuscript/scripts/case-studies/<chapter-name>/`. The manuscript shows the salient pieces inline and points the reader at the full source for the rest.

4. **Measurement.** The approaches are run on the same benchmark. The benchmark is small enough that the reader can read every entry and large enough that the differences are not noise — twenty questions has been our working size; tens-not-hundreds, but no fewer.

5. **The Numbers.** A table. Accuracy, latency, cost, lines of code. The numbers do the convincing the discussion section would not have managed alone.

6. **Recommendations.** A short numbered list of when to reach for which. Each item is conditioned on a specific feature of the problem (corpus structure, query shape, whether the corpus fits in context, whether the team can maintain a server). Recommendations the previous discussion section made loosely now have receipts.

## Pitfalls

A few traps to watch for, in roughly increasing order of how often we'd fall into them.

- **Examples that are too small.** A two-document corpus does not exercise the design space. Every approach gets every question right and there is nothing to measure. The Bendersky corpus — ~300 Markdown files of Go documentation — is roughly the right size: too big to paste into the prompt, big enough that retrieval choices matter, small enough that an afternoon's work fits.

- **Examples that are too big.** A whole-codebase example over 10K files cannot be reproduced by the reader. Pick something the reader can actually clone and run.

- **Comparisons rigged by the framing.** If the benchmark questions are all keyword-precise, the agentic approach wins by construction. We need a *spread* across the query-shape axis, with each bucket large enough that a single missed answer does not flip the table.

- **Implementations that drift in size.** Approach B uses a framework, Approach A is hand-rolled. The comparison is now of *frameworks*, not approaches. All approaches in a case study should sit at the same level of abstraction — the one we settled on in §1.5.

- **The model in the loop changes between approaches.** Same Gemma 4, same temperature, same seed where it matters; otherwise we are measuring model differences and calling them retrieval differences.

- **Forgetting to list when the example does *not* work.** The recommendations section is what gives the reader the right to disregard our numbers when their problem doesn't look like the case study. Skipping it leaves the reader thinking the chapter said more than it did.

## Where the case studies live

Each case-study chapter is a chapter in its own right, sandwiched between the more general topical chapters. Current plan:

- `chapters/06_context_and_retrieval.tex` — the Bendersky problem modernised. Sits after Chapter 5 (Tool Calls) so we can lean on the tool-calling loop, before the agent and reliability chapters.
- *(future)* a case study on **prompting craft**: the same task answered with a naive prompt, a structured prompt, and a few-shot prompt; comparison of accuracy and token cost. Likely lives near or inside Chapter 4 (Tools of the Trade).
- *(future)* a case study on **evaluation**: building an eval set for an agent, measuring its accuracy across a model upgrade. Likely lives in the reliability chapter.
- *(future)* a case study on a **single-agent vs multi-agent** task. Likely a chapter of its own.

The pattern is interleaving, not appendix. Every other chapter or so should be a case study. Discussion → demonstration → discussion → demonstration. The reader gets the design space and then immediately sees the design space exercised.

## Code under `manuscript/scripts/case-studies/`

Per case study, a directory:

```
manuscript/scripts/case-studies/context-and-retrieval/
    README.md            # how to run
    corpus/              # the Go docs we run against (or a fetcher)
    benchmark.json       # the 20 questions and their reference answers
    rubric.py            # how a generated answer is graded
    approach_a_rag.py
    approach_b_agent.py
    approach_c_hybrid.py
    run_all.py           # produces the table the chapter quotes
    results/             # one log per (approach, question) pair
```

The chapter quotes results from `results/` and embeds the salient code from the approach scripts. The reader who wants to verify a number runs `run_all.py`. The reader who wants to extend an approach edits one of the `approach_*.py` files and re-runs.

## A discipline worth holding to

When writing a discussion-register paragraph and reaching for "in practice X is usually better than Y" — stop. Either the next case-study chapter has a measurement that backs it up, or we are committing the kind of vague advice the §1.5 commitment is against. The right move is either to weaken the claim ("for queries of shape Z, X is preferable, as the case study in Chapter ~ shows"), or to add a measurement to the relevant case study's benchmark before the claim ships.

#!/usr/bin/env bash
# =============================================================
# commit.sh --- one-shot commit helper.
# Run from the ai_vault root.
#
# The script clears stale locks left over from sandboxed git
# operations, stages everything respecting .gitignore, prints a
# preview, and commits with a structured message. Adjust or trim
# the message inline before re-running on subsequent commits.
# =============================================================

set -euo pipefail
cd "$(dirname "$0")"

# 1. Clear stale .git/index.lock and any orphaned tmp_obj_* files
#    that the sandbox could not unlink.
if [ -e .git/index.lock ]; then
  echo "Removing stale .git/index.lock"
  rm .git/index.lock
fi
find .git/objects -name "tmp_obj_*" -print -delete 2>/dev/null || true

# 2. Sanity check: where are we?
echo
echo "Repo:    $(git rev-parse --show-toplevel)"
echo "Branch:  $(git branch --show-current 2>/dev/null || echo '(detached)')"
echo

# 3. Stage everything respecting .gitignore.
git add -A

# 4. Show what is about to be committed.
echo "----- about to commit -----"
git status --short
echo "----- diff stat -----"
git diff --cached --stat
echo "----------------------"
echo

# 5. Commit.
git commit -m "Manuscript v0.8: intro fleshed, working_with_llms setup + query_llm, case-study chapter, methodology note

Chapter file layout
- Drop numeric prefixes from chapter filenames; main.tex now
  defines chapter order, not the filesystem
- Move obsolete prefixed copies into manuscript/chapters/_archive/
- Each chapter file's top comment points at main.tex as the
  source of truth for ordering

Chapter 1 (Introduction) --- fully fleshed
- Sci-fi-inspired opener: HAL / Skynet / Data versus the actual
  quiet emergence of useful language models
- Where We Are: three concrete achievements, all with primary
  citations (Anthropic 16-Claude C compiler, Erdos #728 by
  Aristotle + GPT-5.2 Pro, KAIST materials redesign)
- A Moving Target: pace of change, the book's choice to write
  about patterns not products
- How We Got Here: Vaswani 2017, ChatGPT moment, the agent turn
- The Approach (NEW): three commitments paragraph - tools-not-
  internals (Karpathy electricity framing), reproducible claims
  (Gemma 4 default, with an updatebox on closed-model drift),
  pure Python no frameworks
- From Models to Systems: definitionbox for 'agent', revisits
  the achievements with the system framing
- How to Read This Book: chapter map and reading paths

Chapter 2 (Mental Model) --- scaffold
- Section structure: what an LLM is, model types (multimodal,
  open-weights, reasoning), tokens, context window, sampling
  and determinism, embeddings, six-subsection failure-mode
  taxonomy
- Structured Outputs section moved to Chapter 3 (Working with LLMs)
  where it fits topically as a property of how you call a model

Chapter 3 (Working with LLMs) --- mostly scaffold; setup material fleshed
- Section structure: model providers, choosing a model, three
  ways to run a model, query_llm wrapper, chats, structured
  outputs, cost / caching / latency
- 3.3 Three Ways to Run a Model (FULL): hosted API setup +
  smoke test, local Ollama setup + smoke test + hardware sanity
  guide for Gemma 4 sizes, remote GPU service (RunPod-style)
- 3.4 Your First Call: a query_llm Wrapper (FULL): three-backend
  dispatch driven by LLM_BACKEND env var, the wrapper code
  inline, a hello-world transcript switching between Ollama
  and OpenAI with one variable
- 3.6 Structured Outputs (full): the three-tier hierarchy
  (prompting / constrained decoding / fine-tuning) inherited
  from the previous home in Chapter 2

Chapter 4 (Tools of the Trade) --- light scaffold
- Renamed from old prompting stub; now covers prompting craft,
  context construction, output parsing, retry/fallback, common
  idioms
- Outline only; fleshing deferred

Chapter 5 (Tool Calls) --- fleshed (no functional change in this commit)
- Cross-reference adjustment: Structured Outputs reference now
  points at Chapter 3 (Working with LLMs) instead of Chapter 2
  (Mental Model)

Chapter 6 (Context and Retrieval) --- new case-study chapter stub
- Case-study spine: the problem; four approaches (classic RAG,
  agentic retrieval, graph-based, hybrid); the modernised
  Bendersky problem run through Approaches A/B/C with a
  20-question benchmark; recommendations; memory across time
- Filed alongside the manuscript notes file describing how
  case-study chapters should be structured

Chapter 7 (Building Reliable Systems) --- new stub
- Section structure for: security (prompt injection, confused
  deputy, exfiltration), sandboxing (shell, code interpreter,
  MCP servers), testing and evaluation (mindset, building a
  test set, public benchmarks, continuous evaluation),
  agent-specific failure modes, observability, human-in-the-
  loop checkpoints, versioning and rollback
- Currently sits right after Tool Calls; will move to the end
  of the agents arc once those chapters land

Methodology
- manuscript/notes/case_studies.md captures what makes a good
  case-study chapter, the discussion-vs-demonstration interplay,
  the six-section template, common pitfalls, and the discipline
  of pairing every 'X is better than Y' claim with a measured
  comparison

Code
- manuscript/scripts/query_llm.py: pure-requests three-backend
  chat wrapper used throughout the rest of the book

Resources
- learning-resources/bendersky_2023_rag_in_go.{md,html}:
  offline archive of Bendersky's 2023 RAG-in-Go post (the
  pattern model for the case-study chapters)
- learning-resources/murphy_2024_bovex_sigbovik.pdf:
  30-page extract of tom7's BoVeX SIGBOVIK 2024 paper, kept as
  an inspiration for token-probability-driven applications
- learning-resources/README.md updated with both entries

Bibliography (added)
- vaswani2017attention: 'Attention Is All You Need'
- anthropic2026compiler: the C-compiler engineering blog
- tao2025erdos: Tao's writeup of Erdos #728
- kaist2026materials: KAIST materials redesign press release
- adaptivethinking2026: Claude Code adaptive-thinking incident
- karpathy2025software: Karpathy's 'Software Is Changing (Again)' talk
- bendersky2023ragingo: the Bendersky RAG post
- murphy2024bovex: the BoVeX SIGBOVIK paper

Housekeeping
- .gitignore: ignore manuscript/chapters/_test_mv_renamed (a
  stray sandbox-test artefact that the sandbox cannot unlink;
  safe to remove with rm from a real shell)
"

echo
echo "Done."
git log --oneline -5

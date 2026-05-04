#!/usr/bin/env bash
# =============================================================
# commit_v0_2.sh --- one-shot commit of the v0.2/v0.3/v0.4 work.
# Run from the ai_vault root.
# =============================================================

set -euo pipefail
cd "$(dirname "$0")"

# 1. Clear a stale git-index lock if one is hanging around.
if [ -e .git/index.lock ]; then
  echo "Removing stale .git/index.lock"
  rm .git/index.lock
fi

# 2. Sanity check: where are we?
echo
echo "Repo: $(git rev-parse --show-toplevel)"
echo "Branch: $(git branch --show-current 2>/dev/null || echo '(detached)')"
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

# 5. Commit. Adjust the message inline if you like.
git commit -m "Manuscript v0.2: Tool Calls chapter rewrite + dot diagram

- Add .gitignore (LaTeX build, Python venv, OS junk, preview PNGs)

Manuscript scaffolding
- Add main.tex, preamble.tex, references.bib, build.sh
- Author title page: Sandro Belfanti PhD / Chipmind AG / Claude Opus 4.7 / v0.2
- New chapter 02: LLM Fundamentals (stub, structured-outputs section)
- New chapter 03: Tool Calls (full chapter)
- Wire build.sh to render figures/*.dot via Graphviz when available

Tool Calls chapter (v0.4 of the chapter content)
- Strawberry section: tokenization explanation + 'Update April 2026'
  callout box covering GPT-5.4, cranberry, strawpberry; Opus 4.7
  strawpberry figure embedded
- New 'Anatomy of a tool-call exchange' subsection with six-step
  walkthrough and dot-rendered sequence diagram
  (figures/exchange.dot + .pdf, lanes Tool / Runtime / LLM)
- Generic implementation rewritten around four LLM-agnostic building
  blocks (description / registry / parser / loop) with pseudocode
- Hosted (OpenAI) and local (Ollama Gemma 4 native) implementations,
  both as query() functions with __main__ entry points
- 'No native support' reduced to discussion + system-prompt fragment;
  full structured-outputs treatment deferred to LLM Fundamentals
- Taxonomy expanded with one worked example per family; web search
  highlighted as the most powerful tool category
- Shell tool: second example (write a Python file then execute it)
- Risks expanded: quiet system pollution mitigation, plus
  version-control as a second-layer safety net beside sandboxing

Bibliography
- Add gemma4card, techradar2026strawberry,
  ninetofivegoogle2026strawberry, anthropic2026opus47

Resources
- Update resources/agents/README.md, resources/bibliography.md,
  resources/models-and-training/README.md to reference newly
  downloaded papers (Toolformer, ReAct, Gorilla, Code as Policies,
  Fu 2024 letter counting, Xu & Ma genius paradox)
- Add the corresponding PDFs under resources/agents/ and
  resources/models-and-training/

Scripts
- scripts/gemma4_native_toolcall.py: runnable probe of Gemma 4's
  native tool-call channel through Ollama

Figures
- figures/exchange.dot: sequence diagram source (Graphviz)
- figures/exchange.pdf: rendered figure committed alongside source
  so builds work without Graphviz
- figures/opus_4_7_strawpberry_fail.{webp,png}: failure screenshot
"

echo
echo "Done."
git log --oneline -5

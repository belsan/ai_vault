# Hand-off note for the next Claude

*A working document for the Claude that picks this up in a fresh chat. The previous chat ran long; this is what was learned along the way that wouldn't otherwise survive a context reset. Read this first; then read `case_studies.md`; then read whatever specific chapter file is in scope for the user's request.*

---

## What the project is

**Title:** *A Course on AI Agents.*
**Author:** Sandro Belfanti, PhD (Chipmind AG, Zurich).
**Subtitle:** *Lecture notes for engineers building agentic systems.*
**Repo root:** `~/files/ai_vault` (git repo with one main branch).
**Primary deliverable:** `manuscript/build/main.pdf`, ~58 pages at last build.

The book is for engineers who will treat the language model as a service with a calling convention. Not "how a transformer works", not "how to fine-tune"; how to build agentic systems on top of one. The first reader is meant to be an experienced software engineer who has used ChatGPT and now has to ship something serious.

## Style commitments — re-read before writing anything

These live in §1.5 *The Approach* of the intro chapter and they are non-negotiable. Three of them.

1. **Tools, not internals.** We treat the LLM as a service we call. We do not explain attention math, training objectives, or transformer internals. Karpathy's electricity analogy is the framing; cite `karpathy2025software` if relevant. The reader who wants the internals has the literature; we don't compete.

2. **Reproducible claims.** Every substantive behavioural claim is paired with a runnable example under `manuscript/scripts/`. Vague prompting advice ("be polite to the model") is the kind of thing the book exists to push back on. If a sentence says "X is better than Y", there is a measurement somewhere. The default working model is **Gemma 4 served via Ollama**, pinned for reproducibility against closed-model drift (see the `updatebox` in §1.5 for the cautionary tale: Sonnet 3.5/3.7 phase-out, Claude Code adaptive-thinking incident).

3. **Pure Python, no frameworks.** We use `requests` not the OpenAI SDK; we hand-roll a small wrapper instead of `litellm`; we write the agent loop by hand rather than import LangGraph. General-purpose libraries (`pandas`, `matplotlib`, `numpy`, `python-dotenv`) are fine where they earn their keep. The line is at frameworks that abstract away the agent loop itself, because that loop is the subject matter.

A fourth implicit commitment: **American English everywhere.** *Tokenize, color, center, defense, behavior, analyze, optimize, organize.* A whole AE sweep was already done; if you write new prose, write it AE from the start.

## Chapter state at the time of this hand-off

The order is set in `main.tex`. Filenames have **no numeric prefix** — chapter order is purely the order of `\input` lines in `main.tex`. Don't reintroduce numeric prefixes; the user removed them deliberately because reordering chapters is frequent.

| File                                | State           |
| ----------------------------------- | --------------- |
| `chapters/intro.tex`                | **fleshed**     |
| `chapters/mental_model.tex`         | scaffold; §2.2 *Tokens* fleshed |
| `chapters/working_with_llms.tex`    | scaffold; §3.3–§3.5 fleshed (Chats / Interacting / `query_llm` wrapper) |
| `chapters/tools_of_the_trade.tex`   | light scaffold  |
| `chapters/toolcalls.tex`            | **fleshed** (the original major chapter) |
| `chapters/context_and_retrieval.tex`| stub (case-study spine laid out) |
| `chapters/building_reliable_systems.tex` | stub (subsection structure laid out) |

There's a `chapters/_archive/` directory holding obsolete prefixed copies. **Don't touch it** — the sandbox cannot delete files, so these are kept around until the user manually `rm`s them. Never `\input` from there.

Future chapters expected to slot between Tool Calls and Building Reliable Systems: agent design, multi-agent coordination, context engineering. The methodology note `case_studies.md` says case-study chapters should interleave with discussion chapters; the Bendersky-modernised RAG case study (`context_and_retrieval.tex`) is the first.

## Stable cross-reference labels

These should not move. Other chapters depend on them.

```
ch:intro             chapters/intro.tex
ch:mental            chapters/mental_model.tex
ch:working           chapters/working_with_llms.tex
ch:tools             chapters/tools_of_the_trade.tex
ch:toolcalls         chapters/toolcalls.tex
ch:context           chapters/context_and_retrieval.tex
ch:reliable         chapters/building_reliable_systems.tex

sec:intro-approach   §1.5 The Approach (commitments)
sec:strawberry       §5.1 the strawberry problem
sec:work-chats       §3.3 chats / message structure
sec:work-deploy      §3.4 interacting with LLMs
sec:work-wrapper     §3.5 query_llm wrapper
sec:structured       §3.6 structured outputs
sec:taxonomy         §5.4 tool-call taxonomy
sec:shell            §5.6 shell as a tool
sec:codeact          §5.7 programmatic tool calls
sec:mcp              §5.8 connecting tools to agents (MCP-vs-API)
sec:mental-tokens    §2.2 tokens
sec:mental-failures  §2.6 strengths and failure modes
```

## Voice and formatting

The user prefers **prose over bullet lists** for explanations. Use bullets when the structure genuinely is a list (parameter tables, decision rules, taxonomies); use prose when the structure is an argument. When a section has more than one bullet list, ask whether the second one wants to be prose.

Custom tcolorbox environments are defined in `preamble.tex` and *should* be used:

| Environment      | When to reach for it                                |
| ---------------- | --------------------------------------------------- |
| `definitionbox`  | A formal definition (e.g. of *agent*, *tool call*). |
| `examplebox`     | A worked example sitting alongside prose.           |
| `remarkbox`      | A side observation or qualifying note.              |
| `warningbox`     | Risks / things that bite (sandboxing, etc.).        |
| `updatebox`      | News / things that aged out since the prose around it was written. Used in §1.5 and the strawberry section. |

Code in prose: `\code{count_letter}`. Filenames in prose: `\fname{manuscript/scripts/query_llm.py}`. Listings use the `lstlisting` environment with `language=Python` (or `bash`, `json`). The preamble customises `lstset` for the book's look; don't override.

`\todo{...}` is the marker for stub content. Keep it visible — it renders red in the PDF and reminds the user where work remains.

Cross-references: `\S\ref{...}` for sections, `Chapter~\ref{...}` for chapters. `\S\S` for ranges (e.g. `\S\S\ref{a}--\ref{b}`).

## Build, scripts, configuration

```
cd ~/files/ai_vault/manuscript
./build.sh                # pdflatex × bibtex × pdflatex × pdflatex
                          # also runs `dot` on figures/*.dot if available
                          # output → build/main.pdf
./build.sh clean          # rm build/
```

The Python-side world:

```
manuscript/scripts/
  query_llm.py            # the canonical chat wrapper. Exports query_llm() and ask_llm().
  .env.example            # config template; copy to .env and edit
  .env                    # gitignored; user secrets
  llm_wrapper.py          # legacy Ollama-only wrapper used by the toolcalls chapter scripts
  gemma4_native_toolcall.py  # toolcall demo
  prompt_experiments.py
```

The wrapper uses **python-dotenv** to load config from `.env`. Both `query_llm` (full chat) and `ask_llm` (one-shot string) are exported. The `LLM_BACKEND` env var picks between `ollama` (default), `openai`, `anthropic`. Pure `requests` for all three backends; no SDKs.

LaTeX preamble loads, in addition to standard packages: `tcolorbox`, `graphicx`, `tikz` (for any diagrams not done in dot), `listings` with custom styles, `natbib + plainnat`. **xelatex is available but not used.** Stick to pdflatex; that means no native CJK and limited unicode beyond Latin-1. The Mandarin example in §2.2 uses pinyin transliteration for that reason.

The figures directory has both `.dot` source files and pre-rendered PDFs. `build.sh` regenerates the PDFs if `dot` is on PATH; if not, the cached PDFs are used. `figures/exchange.dot` is the sequence diagram in chapter 5.

## Sandbox traps (this chat, possibly the next)

The Cowork sandbox running these tools has subtle filesystem limits to know about:

- **`mv` works, `rm` does not.** You can rename or move files freely, but you cannot unlink them. This means if the user wants something deleted, you have to either `mv` it to an `_archive` folder out of the build path, or write a small shell command for them to run from their real terminal.
- **`.git/` is partially writable but not unlinkable.** `git add` may write objects to `.git/objects/.../tmp_obj_*` and then fail to clean them up; the resulting `.git/index.lock` blocks subsequent git commands. The fix is `commit.sh` at the repo root, which cleans the lock and the orphan tmp objects before staging. Do not attempt to commit directly from a `bash` cell — write a script the user runs.
- **The user's Ollama (at `http://192.168.50.3:11700`) is on a private network unreachable from the sandbox.** When you need to verify model behavior, fall back to documentation, write a probe script the user runs, or use `tiktoken` locally for tokenisation work (it's installed in the script venv).
- **Web fetch responses can exceed the tool's context limit.** When `web_fetch` returns "Error: result exceeds maximum allowed tokens", spawn an `Agent` to read the saved file in chunks and report back, or `grep` it in bash. Don't try to `Read` the dump directly.
- **Script venv:** `manuscript/scripts/.venv/` exists with `requests`, `python-dotenv`, `tiktoken`, etc. Useful for quick checks. The venv directory is gitignored.

## How the user works

A few patterns to recognise:

- **Iterative editing.** The user often edits a draft between turns rather than asking for revisions. Always check `git status`/`git diff` (in bash, not via tools that need git's index) before assuming the file matches what was written last turn. The `<system-reminder>` blocks Anthropic injects when files have changed are also a tell.
- **Rough markdown sketches.** The user sometimes drops markdown-style notes inside `.tex` files (asterisks for bullets, no `\section`, half-finished sentences). When that happens they'll say "finish this" — convert to LaTeX, flesh out the noted points (often labelled `(explain ...)`), fix typos as you go.
- **Substantive technical pushback is welcome.** When the user asked whether MCP was always the winner, the right move was to agree partly, push back where I had reservations, and offer to revise. They reacted well. Don't be sycophantic; do engage.
- **Discussion before action.** When the user is thinking through structure ("where should embeddings live?", "what should the intro chapter cover?"), reply in chat with a structured opinion before reaching for tools. Don't start writing a 5-page section until they've agreed on what it should contain.
- **They commit via `commit.sh`.** Don't try to commit yourself; it'll fail. Update `commit.sh` if needed and tell them to run it.
- **They like progressive disclosure.** Suggest the smallest reasonable change and offer to expand. They may say "no, just do it all" — at which point go ahead. Better to ask once than rebuild a wrong section.

## Things that have come up and might come up again

- **The orphan-files problem.** Old prefixed chapter files (`01_prompting.tex` etc.) live in `chapters/_archive/` because we couldn't `rm` them. There may be more such orphans elsewhere (e.g. `manuscript/chapters/_test_mv_renamed`, gitignored). Don't worry about them; the user knows.
- **The Tool Calls chapter still uses the OpenAI SDK** in one of its listings, inconsistent with §1.5's "use requests directly". Flagged but not yet fixed. Touch this only if the user asks.
- **The `case_studies.md` methodology note** governs how the case-study chapters are written. Read it before drafting any case-study material.
- **Recent additions** the user wanted but hasn't asked me to write yet: a `scripts/logprobs_demo.py` that probes Gemma 4's token probabilities via Ollama's logprobs API (added in v0.12.11, November 2025). Could become an examplebox in §2.2 or §2.4.
- **Empty / stub notes:** `manuscript/md_inputs/` was added by the user (chapter outlines in markdown form). Read them when starting work on the corresponding chapter.

## Topics that recur in the prose

These framings show up across multiple chapters and should remain consistent:

- *"The model is the engine; the system is the vehicle."* (§1.4 closing.)
- *"A model in a loop with tools."* — the working definition of *agent* (§1.4 definitionbox).
- *"The substrate determines the ceiling."* (closing of §5.9, attributed to Wang et al. 2024.)
- *"The model has no character-level representation of its own input."* — the structural claim that links §2.2 (tokens) to §5.1 (strawberry).
- *"Stable instructions in `system`, per-turn content in `user`."* — §3.3.4 working rule on the system prompt.

## Suggested first prompt for the next chat

Paste this verbatim into a fresh chat:

> Read `manuscript/notes/claude_handoff.md` first. Then read `manuscript/notes/case_studies.md`. Then run `git log --oneline -5` and `git status` to see the current state. After that, ask me what's next; don't start writing until I've told you what to work on.

That gets the new Claude oriented in three short reads, with no risk of redoing work or violating a style commitment that's not yet in their context.

---

*Last updated by the previous Claude at v0.14 of the manuscript. If you change anything substantial — chapter structure, style commitments, the wrapper — update this document so the next-next Claude isn't starting from a stale picture.*

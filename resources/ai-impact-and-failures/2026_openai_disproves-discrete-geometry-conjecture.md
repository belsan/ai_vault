# An OpenAI Model Disproved a Central Conjecture in Discrete Geometry (2026)

> Local reading-note archive of the OpenAI publication.
> Source: https://openai.com/index/model-disproves-discrete-geometry-conjecture/
> Author: OpenAI · Published: 20 May 2026 · Tagged: Research / Milestone
> Summary in my own words (not a verbatim copy). Read the original for the full text;
> the proof, the external mathematicians' companion paper, and an abridged model
> chain-of-thought are all linked from the post.

## The result

The **planar unit-distance problem** (Erdős, 1946): given n points in the plane, how many
pairs can be *exactly* distance 1 apart? Write u(n) for the maximum. It is one of the
best-known, easiest-to-state, hardest-to-resolve questions in combinatorial geometry.

- **Prior belief:** the "square-grid" constructions were essentially optimal. The best
  known lower bound (a rescaled square grid) gives n^(1 + C/log log n) — only *slightly*
  faster than linear — and had been essentially unchanged since 1946. Erdős conjectured an
  upper bound of n^(1+o(1)).
- **Best known upper bound:** O(n^(4/3)), from Spencer–Szemerédi–Trotter (1984), also
  essentially unchanged despite decades of refinement.
- **New result:** an internal OpenAI model **disproved the conjecture**, constructing, for
  infinitely many n, configurations with at least n^(1+δ) unit-distance pairs for a *fixed*
  δ > 0. The original AI proof gave no explicit δ; a follow-up by Princeton's Will Sawin
  pins down δ = 0.014.

## Why it's notable (the part that matters for the corpus)

- **First prominent open problem, central to a subfield, solved autonomously by AI.** An
  AI-achievement milestone in the same vein as the Erdős #728 result already cited in the
  manuscript intro — but arguably a stronger data point.
- **General-purpose, not a math machine.** The proof came from a *new general-purpose
  reasoning model* — not a system trained for mathematics, not scaffolded to search proof
  strategies, not targeted at this problem. It was just evaluated on a batch of Erdős
  problems and produced a resolving proof for this one.
- **Surprising cross-domain method.** The construction imports heavy **algebraic number
  theory** (generalizing the Gaussian-integer idea to number fields with richer symmetries;
  uses infinite class field towers and Golod–Shafarevich theory) into an elementary
  Euclidean-geometry question — a connection nobody expected.
- **Chain-of-thought tell (Arul Shankar's reading):** most of the model's thinking was
  spent trying to *construct a counterexample* to the widely believed upper bound rather
  than prove it — i.e. good intuition, willingness to chase a long-shot the community
  dismissed, and a bias toward constructions.
- **Externally verified.** Checked by outside mathematicians who wrote a companion paper;
  Tim Gowers calls it "a milestone in AI mathematics" and says he'd have recommended it for
  acceptance at the Annals without hesitation. Endorsements also from Noga Alon, Arul
  Shankar, Jacob Tsimerman, and Thomas Bloom.

## Why I kept it

A clean, external-verified example of AI producing a *genuinely new* mathematical result
autonomously — strong material for the "Where We Are" achievements in the book's intro, and
a good counterweight data point on the "impact of AI on research/engineering" axis. The
general-purpose-model angle (vs. a specialized prover) is the bit that makes it more
interesting than a scaffolded, problem-specific system.

## Related in this corpus

- `2026_llm-driven-architecture-design.pdf` (Computer Architecture's AlphaZero Moment) — same "AI autonomously doing frontier discovery" shelf.
- Manuscript intro (`manuscript/chapters/intro.tex`) — Erdős #728 (Aristotle + GPT-5.2 Pro) and KAIST materials redesign; this would slot in alongside them as a candidate citation.

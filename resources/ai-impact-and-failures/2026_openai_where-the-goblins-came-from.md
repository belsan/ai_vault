# Where the Goblins Came From — OpenAI (2026)

> Local reading-note archive of the OpenAI publication "Where the goblins came from."
> Source: https://openai.com/index/where-the-goblins-came-from/
> Author: OpenAI · Published: 29 April 2026
> This is a summary/reading note in my own words (not a verbatim copy); read the original at the link for the full text and figures.

## What it is

A short, light "behind the scenes" post about a recurring quirk OpenAI noticed in their
models: starting around GPT-5.1, the models increasingly reached for **goblins, gremlins,
and similar creatures** in their metaphors. The piece is the story of how they tracked the
tic down to its root cause. Unlike a normal bug (which shows up as a tanking eval or a
spiking training metric), this crept in subtly — a single "little goblin" is harmless, even
charming, but across model generations the creatures kept multiplying.

## The trail

- **First signs (Nov, after GPT-5.1):** users complained the model felt overfamiliar; a
  verbal-tic investigation found "goblin" usage in ChatGPT up ~175% post-launch, "gremlin"
  up ~52%. Not alarming at the time.
- **GPT-5.4:** a bigger uptick. Analysis showed creature-language was heavily concentrated
  in traffic from users on the **"Nerdy" personality** customization. Nerdy was only ~2.5%
  of all responses but ~66.7% of all "goblin" mentions. Its system prompt pushed a
  "playful, wise, undercut-pretension, the-world-is-strange" style.
- **Root cause:** during RL, the reward signal designed to encourage the Nerdy personality
  consistently scored creature-word outputs higher (positive uplift in ~76.2% of datasets).
  So the playful-style reward was inadvertently rewarding the lexical tic.
- **Why it leaked outside Nerdy:** RL doesn't keep learned behaviors neatly scoped. Once
  the tic was rewarded, it transferred to non-Nerdy outputs, and got amplified through an
  SFT feedback loop:
    1. playful style is rewarded →
    2. some rewarded examples contain the tic →
    3. the tic appears more in rollouts →
    4. those rollouts are reused for supervised fine-tuning →
    5. the model gets even more comfortable producing it.
- A search of GPT-5.5's SFT data found many "goblin"/"gremlin" datapoints, plus a wider
  menagerie of tic-words: raccoons, trolls, ogres, pigeons (most uses of "frog" were
  legitimate).

## The fix

Retired the "Nerdy" personality (March, after GPT-5.4), removed the goblin-affine reward
signal, and filtered creature-words from training data. GPT-5.5 had already started
training before the root cause was found, so it still showed the affinity; in Codex they
added a developer-prompt instruction to suppress it. (The post cheekily includes a shell
incantation to strip the goblin-suppressing instruction back out of Codex if you want the
creatures to run free.)

## Why I kept it

No impact on what we do, but a genuinely good illustration of two things worth remembering:
- **Reward signals shape behavior in unexpected, hard-to-localize ways** — a reward aimed
  at "personality" produced a lexical tic.
- **RL reward generalization + SFT feedback loops** can carry a behavior far outside the
  condition that produced it. A nice, concrete, low-stakes case study of reward
  mis-generalization and of building tooling to audit model behavior and fix it at the root.

## Related in this corpus

- `2025_oddity.pdf` (Leviathan, prompt-repetition oddity) — same "surprising model behaviour" shelf.
- `models-and-training/2026_negation-neglect.pdf` — another "what models do/don't learn in training" story.

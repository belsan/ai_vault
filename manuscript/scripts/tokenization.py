"""Inspect Gemma 4's tokenizer: tokenize strings, then explore the vocab.

A language model does not see characters or words --- it sees a sequence
of vocabulary IDs produced by the tokenizer. That choice of tokenizer
shapes everything downstream: how the context window is counted, how
whitespace is encoded, and what 'subword' fragments the model glues
together to recover ordinary text.

The script has two parts.

PART 1 tokenizes three short strings chosen to bring out three regimes:

  1. A clean English sentence: most words map to a single token.
  2. A pangram with rarer letter combinations: unusual subwords
     fragment into multiple tokens.
  3. A line of source code with a hex literal: punctuation and digit
     sequences split very differently from natural language.

PART 2 explores the vocabulary itself:

  * The longest tokens. The tokenizer reserves dedicated single-token
    slots for surprisingly long strings (16-character code identifiers
    and Spanish words, in Gemma's case).
  * The "most common" subword pairs. The tokenizer file does not store
    training-corpus frequencies, but BPE merges are added in
    approximately frequency order --- earlier merge = more common pair.
    We have to skip the very first merges because they are dominated by
    long whitespace runs (an artifact of code/markdown training data).
    The first non-whitespace merges are exactly the most common English
    bigrams: `er`, `in`, `▁the`, `on`, ...
  * The "least common" subword pairs. The last merges in the list are
    obscure script-specific or rare-word fragments.

A note on the tokenizer source. Google's official Gemma weights on
HuggingFace are gated behind a license click. We use a publicly mirrored
copy at `unsloth/gemma-3-4b-it` --- verified to produce the SAME token
counts as the local Ollama server's `gemma4:26b` for several test strings,
so we know the vocabulary is identical for our purposes.

Watch for the `▁` character (U+2581, 'lower one eighth block'). That is
SentencePiece's marker for a leading space: `▁quick` is the token
representing " quick" --- the leading space is part of the token, not a
separate whitespace token. This is the same tokenizer property that, in
the previous demo, made trailing spaces in a prompt so disruptive.

The first run downloads ~32 MB of tokenizer data into
~/.cache/manuscript-scripts/. Subsequent runs use the cached copy.

Setup:
    $ pip install tokenizers requests

Run with:
    $ python3 tokenization.py
"""

from __future__ import annotations

import json
from pathlib import Path

import requests
from tokenizers import Tokenizer

TOKENIZER_URL = (
    "https://huggingface.co/unsloth/gemma-3-4b-it/"
    "resolve/main/tokenizer.json"
)
CACHE_PATH = (
    Path.home() / ".cache" / "manuscript-scripts" / "gemma_tokenizer.json"
)


def load_tokenizer() -> Tokenizer:
    """Return the Gemma tokenizer, downloading it on first use."""
    if not CACHE_PATH.exists():
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        print(f"Downloading Gemma tokenizer to {CACHE_PATH} ...")
        rsp = requests.get(TOKENIZER_URL, timeout=120)
        rsp.raise_for_status()
        CACHE_PATH.write_bytes(rsp.content)
    return Tokenizer.from_file(str(CACHE_PATH))


def show(tok: Tokenizer, string: str) -> None:
    """Print a string alongside its tokenization."""
    enc = tok.encode(string, add_special_tokens=False)
    print(f"Input:  {string!r}")
    print(f"  {len(enc.ids)} tokens")
    print(f"  pieces: {' '.join(f'[{t}]' for t in enc.tokens)}")
    print(f"  ids:    {enc.ids}")
    print()


# ---------------------------------------------------------------------------
# Vocab exploration
# ---------------------------------------------------------------------------

def regular_vocab(tok: Tokenizer) -> dict[str, int]:
    """Vocab minus 'added tokens' (specials, chat template markers, etc.)."""
    added = {t.content for t in tok.get_added_tokens_decoder().values()}
    return {t: i for t, i in tok.get_vocab().items() if t not in added}


def show_longest_tokens(tok: Tokenizer, n: int = 10) -> None:
    print(f"--- top {n} longest tokens in the vocabulary ---")
    items = sorted(regular_vocab(tok).items(), key=lambda kv: -len(kv[0]))[:n]
    for token, tid in items:
        print(f"  id={tid:6d}  len={len(token):3d}  {token!r}")
    print()


def _parse_merge(m) -> tuple[str, str]:
    return tuple(m) if isinstance(m, list) else tuple(m.split(" ", 1))


def _is_whitespace_only(s: str) -> bool:
    return all(c in " \t\n▁" for c in s)


def show_first_merges(merges: list, n: int = 15) -> None:
    """Print the first n NON-whitespace BPE merges.

    The very first merges in Gemma's BPE are long runs of newlines, tabs,
    and spaces (a side-effect of how indentation appears in code and
    markdown training data). Those are not the lesson; we filter them
    out. What remains is approximately the list of the most common
    subword pairs in the training corpus.
    """
    print(f"--- first {n} non-whitespace BPE merges (most common pairs) ---")
    shown = 0
    for i, m in enumerate(merges):
        a, b = _parse_merge(m)
        if _is_whitespace_only(a + b):
            continue
        print(f"  merge {i:5d}: {a!r:>10s} + {b!r:<10s} =>  {(a + b)!r}")
        shown += 1
        if shown >= n:
            return


def show_last_merges(merges: list, n: int = 15) -> None:
    """Print the last n BPE merges (rarest pairs)."""
    print(f"--- last {n} BPE merges (rarest pairs) ---")
    start = len(merges) - n
    for i, m in enumerate(merges[-n:], start=start):
        a, b = _parse_merge(m)
        print(f"  merge {i}: {a!r} + {b!r}  =>  {(a + b)!r}")


if __name__ == "__main__":
    tok = load_tokenizer()

    print("=" * 72)
    print("PART 1.  Tokenizing three characteristic strings")
    print("=" * 72)
    print()
    for s in [
        "The quick brown fox jumps over the lazy dog",
        "Sphinx of black quartz, judge my vow",
        "const MAGIC = 0x198a23ff;",
    ]:
        show(tok, s)

    print("=" * 72)
    print("PART 2.  Vocabulary stats")
    print("=" * 72)
    print()

    vocab_size = tok.get_vocab_size()
    regular = regular_vocab(tok)
    print(f"vocab size: {vocab_size:,}  ({len(regular):,} regular + "
          f"{vocab_size - len(regular):,} added/special)")
    print()

    show_longest_tokens(tok)

    # The merge list lives in the JSON, not in the tokenizers.Tokenizer
    # API surface, so we re-read it from the cached file.
    raw = json.loads(CACHE_PATH.read_text())
    merges = raw["model"]["merges"]
    print(f"BPE merges: {len(merges):,} total")
    print()
    show_first_merges(merges)
    print()
    show_last_merges(merges)

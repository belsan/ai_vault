"""Inspect next-token logprobs across two models on the same Ollama server.

A language model is, at its core, a function from a string to a probability
distribution over the vocabulary's next token. Hosted chat APIs hide this
distribution behind sampling --- the user only sees the token that was
actually drawn. Ollama exposes it directly via the `logprobs` flag.

Four demos, in increasing order of weirdness:

  1. Qwen (non-thinking, or with thinking suppressed). Ask via the chat
     endpoint, read off the answer-position logprobs directly. The simple
     case, included for contrast: when the model has no thinking channel,
     the answer distribution is just sitting there at position 0.

  2. Gemma 4 in raw mode (no chat templating). The BASE model's view of
     a string. Tiny prompt details matter --- a single trailing space
     flips the top candidates from English words to digits, because
     Gemma's tokenizer encodes ` Bern` as one token (with the leading
     space). A trailing space in the prompt forces the next token NOT
     to begin with a space, ruling out almost every English word.

  3. Gemma 4 with chat templating, recovering the answer logprobs by
     hand. Chat-templated Gemma 4 emits `<|channel>thought` as its very
     first token: the answer is hidden behind a thinking channel.
     Workaround: assemble the chat template manually with raw=true, open
     the thinking channel and immediately close it with `<channel|>`, and
     ask for one token. The next-token distribution IS the answer
     distribution. Strikingly, an EMPTY thought is enough --- the
     structural markers alone tell the model "thinking is done now".

  4. Gemma 4 with `think: false` on /api/chat. The clean alternative to
     demo 3 when the model/server honours the flag. Empirically: works
     on the local laptop's gemma4:e2b, ignored by the LAN's gemma4:26b.
     Also, /v1/chat/completions silently drops `think` -- you must use
     Ollama's native /api/chat endpoint.

Profile switch: change `PROFILE_NAME` below to point at a different Ollama
host + model pair. Default profile is "local" (laptop's own Ollama with
the small e2b Gemma); "remote" hits the LAN box with the larger models.

Run with:
    python3 next_token_logprobs.py
"""

from __future__ import annotations

import math
import requests

# ---------------------------------------------------------------------------
# Profile switch. Flip PROFILE_NAME to "remote" to point back at the LAN
# Ollama with the 26B Gemma + 72B Qwen pair. The "local" profile uses the
# laptop's own Ollama with the smaller Gemma 4 (e2b, ~5B) and Qwen 3 4B.
# ---------------------------------------------------------------------------
PROFILES = {
    "remote": {
        "base_url":    "http://192.168.50.3:11700",
        "gemma_model": "gemma4:26b",
        "qwen_model":  "huihui_ai/qwen2.5-abliterate:72b",
        # qwen2.5 has no thinking channel: the chat endpoint's first
        # token IS the answer (see DEMO 1).
        "qwen_is_thinker": False,
    },
    "local": {
        "base_url":    "http://localhost:11434",
        "gemma_model": "gemma4:e2b",
        "qwen_model":  "qwen3:4b",
        # qwen3 is a thinking model -- the chat endpoint's first token
        # is a thinking-channel marker, not the answer. We work around
        # this in DEMO 1 the same way DEMO 4 does for Gemma 4.
        "qwen_is_thinker": True,
    },
}
PROFILE_NAME = "local"
CONFIG = PROFILES[PROFILE_NAME]

OLLAMA_BASE_URL = CONFIG["base_url"]
GENERATE_URL    = f"{OLLAMA_BASE_URL}/api/generate"
CHAT_URL        = f"{OLLAMA_BASE_URL}/v1/chat/completions"
CHAT_NATIVE_URL = f"{OLLAMA_BASE_URL}/api/chat"

GEMMA_MODEL = CONFIG["gemma_model"]
QWEN_MODEL  = CONFIG["qwen_model"]
TOP_K = 10


# ---------------------------------------------------------------------------
# Three ways to ask the same model the same thing.
# ---------------------------------------------------------------------------

def chat_first_token_logprobs(
    user_message: str,
    model: str,
    top_k: int = TOP_K,
) -> list[dict]:
    """Top-k candidates for the FIRST token of a chat-templated reply.

    Uses /v1/chat/completions, which returns logprobs alongside the
    sampled tokens. Useful when you want "what does the model want to
    say first, after the chat template wraps the prompt".
    """
    rsp = requests.post(
        CHAT_URL,
        json={
            "model":        model,
            "messages":     [{"role": "user", "content": user_message}],
            "max_tokens":   1,
            "temperature":  0,
            "logprobs":     True,
            "top_logprobs": top_k,
        },
        timeout=120,
    )
    rsp.raise_for_status()
    return rsp.json()["choices"][0]["logprobs"]["content"][0]["top_logprobs"]


def raw_next_token_logprobs(
    prompt: str,
    model: str = GEMMA_MODEL,
    top_k: int = TOP_K,
) -> list[dict]:
    """Top-k next-token candidates for `prompt`, with NO chat templating.

    Uses /api/generate with raw=true: the bytes go in unchanged, no
    <start_of_turn>user wrapper, no system prefix. This is as close to
    the base model's view of the string as we can get from Ollama.
    """
    rsp = requests.post(
        GENERATE_URL,
        json={
            "model":   model,
            "prompt":  prompt,
            "raw":     True,
            "stream":  False,
            "options": {"num_predict": 1, "temperature": 0},
            "logprobs":     True,
            "top_logprobs": top_k,
        },
        timeout=120,
    )
    rsp.raise_for_status()
    return rsp.json()["logprobs"][0]["top_logprobs"]


def chat_first_token_logprobs_think_off(
    user_message: str,
    model: str,
    top_k: int = TOP_K,
) -> list[dict]:
    """Top-k first-token candidates with `think: false` via /api/chat.

    Uses Ollama's native /api/chat endpoint (not the OpenAI-compatible
    /v1/chat/completions one, which silently ignores `think`). When the
    server / model honour the flag, the thinking channel is suppressed
    and the first token of the assistant reply IS the answer -- so this
    function is the clean alternative to `faked_thought_logprobs` below.
    Returns the top-k list in the same shape as the other helpers.
    """
    rsp = requests.post(
        CHAT_NATIVE_URL,
        json={
            "model":    model,
            "messages": [{"role": "user", "content": user_message}],
            "stream":   False,
            "think":    False,
            "options":  {"num_predict": 1, "temperature": 0},
            "logprobs":     True,
            "top_logprobs": top_k,
        },
        timeout=120,
    )
    rsp.raise_for_status()
    return rsp.json()["logprobs"][0]["top_logprobs"]


def faked_thought_logprobs(
    user_message: str,
    fake_thought: str = "",
    model: str = GEMMA_MODEL,
    top_k: int = TOP_K,
) -> list[dict]:
    """Inject a fake completed thought; return logprobs at the answer position.

    Manually assembles Gemma 4's chat template:
        <start_of_turn>user
        {user_message}<end_of_turn>
        <start_of_turn>model
        <|channel>thought
        {fake_thought}<channel|>

    and feeds it via /api/generate with raw=true. The next token to be
    produced is the first token of the visible answer, so logprobs[0] is
    the answer distribution we wanted but cannot obtain by simply asking
    the chat endpoint.
    """
    prompt = (
        "<start_of_turn>user\n"
        f"{user_message}<end_of_turn>\n"
        "<start_of_turn>model\n"
        "<|channel>thought\n"
        f"{fake_thought}<channel|>"
    )
    rsp = requests.post(
        GENERATE_URL,
        json={
            "model":   model,
            "prompt":  prompt,
            "raw":     True,
            "stream":  False,
            "options": {"num_predict": 1, "temperature": 0},
            "logprobs":     True,
            "top_logprobs": top_k,
        },
        timeout=120,
    )
    rsp.raise_for_status()
    return rsp.json()["logprobs"][0]["top_logprobs"]


# ---------------------------------------------------------------------------
# Pretty-printing
# ---------------------------------------------------------------------------

def show_candidates(candidates: list[dict], indent: str = "  ") -> None:
    for c in candidates:
        prob = math.exp(c["logprob"])
        print(f"{indent}{c['token']!r:20s}  logprob={c['logprob']:7.3f}  prob={prob:6.2%}")


def banner(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def profile_banner() -> None:
    qwen_note = " (thinking model)" if CONFIG["qwen_is_thinker"] else ""
    print(f"Profile: {PROFILE_NAME!r}  @  {OLLAMA_BASE_URL}")
    print(f"  Gemma : {GEMMA_MODEL}")
    print(f"  Qwen  : {QWEN_MODEL}{qwen_note}")


# ---------------------------------------------------------------------------
# Demos
# ---------------------------------------------------------------------------

def demo_qwen() -> None:
    if CONFIG["qwen_is_thinker"]:
        banner(f"DEMO 1.  {QWEN_MODEL} with `think: false`")
        print(f"{QWEN_MODEL} is a thinking model: its first chat token is a")
        print("thinking-channel marker, not the answer. We disable thinking")
        print("with /api/chat's `think: false` flag so the first token IS")
        print("the answer and logprobs land where we want them.")
        ask = lambda q: chat_first_token_logprobs_think_off(q, QWEN_MODEL)
    else:
        banner(f"DEMO 1.  {QWEN_MODEL} (non-thinking): logprobs are easy")
        print("This Qwen has no hidden thinking channel. With chat templating,")
        print("the very first token of the assistant's reply IS the answer.")
        print("So the chat endpoint's `logprobs` field hands us the answer")
        print("distribution directly --- no trickery required.")
        ask = lambda q: chat_first_token_logprobs(q, QWEN_MODEL)
    print()
    for question in [
        "What is the capital of Switzerland? Answer in one word.",
        "What is the capital of Italy? Answer in one word.",
        "What is the capital of Australia? Answer in one word.",
    ]:
        print(f"--- {question!r} ---")
        show_candidates(ask(question))
        print()


def demo_gemma_raw() -> None:
    banner("DEMO 2.  Gemma 4 in raw mode: the base model's view")
    print("Without chat templating, Gemma 4 just continues the string.")
    print("Watch how a single trailing space flips the distribution from")
    print("English words to digits --- the tokenizer keeps the leading")
    print("space attached to the word, so 'is ' cannot be followed by ' Bern'.")
    print()
    for prompt in [
        "The capital of Switzerland is",
        "The capital of Switzerland is ",
        "What is the capital of Switzerland? ",
    ]:
        print(f"--- prompt: {prompt!r} ---")
        show_candidates(raw_next_token_logprobs(prompt))
        print()


def demo_empty_thought() -> None:
    banner("DEMO 3.  Gemma 4 with chat template + empty thought")
    print("Gemma 4 is a reasoning model: chat-templated, its first token is")
    print("`<|channel>` --- the protocol layer, not the answer:")
    print()
    print("    --- chat-templated Gemma 4, position 0 ---")
    show_candidates(
        chat_first_token_logprobs(
            "What is the capital of Switzerland? Answer in one word.",
            GEMMA_MODEL,
            top_k=3,
        ),
        indent="      ",
    )
    print()
    print("To recover the answer distribution we assemble the chat template")
    print("ourselves via raw=true, open the thinking channel and immediately")
    print("close it with `<channel|>`. The next token is then the first")
    print("answer token. Remarkably, an EMPTY thought suffices --- the")
    print("structural markers alone steer the model out of thinking mode.")
    print()

    question = "What is the capital of Switzerland? Answer in one word."

    print("--- empty thought: just `<|channel>thought\\n<channel|>` ---")
    print("    No information about the question is embedded in the thought.")
    print()
    show_candidates(faked_thought_logprobs(question, fake_thought=""))
    print()

    print("--- sanity check: thought pre-states the answer ---")
    print("    'The answer is Bern.'  (should concentrate on `Bern`)")
    print()
    show_candidates(faked_thought_logprobs(
        question,
        fake_thought=(
            "The user wants the capital of Switzerland in one word. "
            "The answer is Bern."
        ),
    ))
    print()


def demo_think_off() -> None:
    banner("DEMO 4.  Gemma 4 with `think: false` (cleaner than DEMO 3)")
    print("Modern Ollama exposes a `think` flag on /api/chat that, when")
    print("honoured by the model/server, suppresses the thinking channel")
    print("entirely. If it works, the first token of the assistant reply")
    print("IS the answer -- and we get its logprobs from the chat endpoint")
    print("with no hand-assembled template.")
    print()
    print("Caveats observed in practice:")
    print("  * /v1/chat/completions silently IGNORES `think`. Must use")
    print("    Ollama's native /api/chat.")
    print("  * Older Ollama versions / older model packagings ignore the")
    print("    flag too -- the first token is still `<|channel>`.")
    print("    DEMO 3's workaround is then still the only option.")
    print()
    for question in [
        "What is the capital of Switzerland? Answer in one word.",
        "What is the capital of Italy? Answer in one word.",
    ]:
        print(f"--- {question!r} ---")
        cands = chat_first_token_logprobs_think_off(question, GEMMA_MODEL)
        show_candidates(cands)
        top = cands[0]["token"]
        if top.startswith("<|") or "channel" in top.lower():
            print("  -> first token is still a channel marker:")
            print("     server/model did NOT honour `think: false`.")
        else:
            print("  -> first token is the answer: `think: false` worked.")
        print()


if __name__ == "__main__":
    profile_banner()
    demo_qwen()
    demo_gemma_raw()
    demo_empty_thought()
    demo_think_off()

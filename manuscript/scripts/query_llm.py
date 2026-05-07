"""query_llm.py --- a three-backend chat wrapper.

The book's canonical interface to a language model. Every later
script imports `query_llm` from this file. Switching between hosted
and local backends is one environment variable, never a code
change.

Backends:
  * "ollama"    --- local or remote Ollama server (default).
  * "openai"    --- OpenAI's chat-completion API.
  * "anthropic" --- Anthropic's messages API.

Environment variables:
  LLM_BACKEND        one of {"ollama", "openai", "anthropic"}.
                     Defaults to "ollama".
  OLLAMA_BASE_URL    e.g. http://localhost:11434  (for the ollama backend).
  OLLAMA_MODEL       default model name passed to Ollama.
  OPENAI_API_KEY     required for the openai backend.
  ANTHROPIC_API_KEY  required for the anthropic backend.

Run as a script for a smoke test:
    $ export LLM_BACKEND=ollama
    $ export OLLAMA_MODEL=gemma4:e4b
    $ python query_llm.py
"""

from __future__ import annotations

import os
from typing import Optional

import requests


def query_llm(
    messages: list[dict[str, str]],
    *,
    model:       Optional[str] = None,
    temperature: float = 0.0,
    max_tokens:  int = 2048,
) -> str:
    """Send `messages` to whichever backend LLM_BACKEND selects.

    Parameters
    ----------
    messages : list of {"role": ..., "content": ...} dicts.
        Roles are "system", "user", "assistant" (and "tool" once
        the toolcalls chapter introduces it). Same shape across
        all three backends.
    model : optional str.
        Backend-specific model identifier. Falls back to a sensible
        per-backend default if not supplied.
    temperature : float, default 0.0.
        Sampling temperature; 0.0 gets the most-determined output.
    max_tokens : int, default 2048.
        Upper bound on generated tokens.

    Returns
    -------
    The assistant's text response, as a string.
    """
    backend = os.environ.get("LLM_BACKEND", "ollama")
    dispatch = {
        "ollama":    _ollama_chat,
        "openai":    _openai_chat,
        "anthropic": _anthropic_chat,
    }
    if backend not in dispatch:
        raise ValueError(
            f"unknown LLM_BACKEND: {backend!r} "
            f"(expected one of {sorted(dispatch)})"
        )
    return dispatch[backend](messages, model, temperature, max_tokens)


# ---------------------------------------------------------------------------
# Backend implementations
# ---------------------------------------------------------------------------

def _ollama_chat(messages, model, temperature, max_tokens) -> str:
    base = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    rsp = requests.post(
        f"{base}/api/chat",
        json={
            "model":    model or os.environ.get("OLLAMA_MODEL", "gemma4:e4b"),
            "stream":   False,
            "messages": messages,
            "options":  {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        },
        timeout=120,
    )
    rsp.raise_for_status()
    return rsp.json()["message"]["content"]


def _openai_chat(messages, model, temperature, max_tokens) -> str:
    rsp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={
            "model":       model or "gpt-4o-mini",
            "messages":    messages,
            "temperature": temperature,
            "max_tokens":  max_tokens,
        },
        timeout=120,
    )
    rsp.raise_for_status()
    return rsp.json()["choices"][0]["message"]["content"]


def _anthropic_chat(messages, model, temperature, max_tokens) -> str:
    # Anthropic puts the system message in a separate top-level
    # field rather than in the messages list, so we split it out.
    system = next(
        (m["content"] for m in messages if m["role"] == "system"),
        "",
    )
    msgs = [m for m in messages if m["role"] != "system"]
    rsp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key":         os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
            "content-type":      "application/json",
        },
        json={
            "model":       model or "claude-haiku-4-5-20251001",
            "system":      system,
            "messages":    msgs,
            "temperature": temperature,
            "max_tokens":  max_tokens,
        },
        timeout=120,
    )
    rsp.raise_for_status()
    return rsp.json()["content"][0]["text"]


if __name__ == "__main__":
    answer = query_llm([
        {"role": "user", "content": "Say hi in three words."},
    ])
    print(answer)

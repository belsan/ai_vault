"""query_llm.py --- a three-backend chat wrapper.

The book's canonical interface to a language model. Every later
script imports either `query_llm` (the chat-shaped function) or
`ask_llm` (the one-shot string convenience) from this file.
Switching between hosted and local backends is a one-line change
in a `.env` file, never a code change.

Public entry points:
  * query_llm(messages, ...) -> str
        Full chat shape: pass a list of role-tagged dicts, get a
        string reply. Use this when you care about multi-turn
        history, the system prompt is non-trivial, or several
        roles need to interleave.
  * ask_llm(prompt, system_prompt=None, ...) -> str
        One-shot convenience: pass a string (and optionally a
        system prompt), get a string reply. Use this for the
        common case where the input is just one user message.

Backends:
  * "ollama"    --- local or remote Ollama server (default).
  * "openai"    --- OpenAI's chat-completion API.
  * "anthropic" --- Anthropic's messages API.

Configuration is read from a .env file in the script's directory
(or anywhere upward in the directory tree) by python-dotenv. See
.env.example for the variables the wrapper looks for. Shell-set
environment variables, if present, take precedence over .env.

Setup:
    $ pip install requests python-dotenv
    $ cp .env.example .env
    $ $EDITOR .env          # uncomment and fill in the lines you need

Run as a script for a smoke test:
    $ python query_llm.py
"""

from __future__ import annotations

import os
from typing import Optional

import requests
from dotenv import load_dotenv

# Load .env at import time. The wrapper, and every script that
# imports it, sees configuration variables as soon as they enter
# the module.
load_dotenv()


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


def ask_llm(
    prompt: str,
    *,
    system_prompt: Optional[str] = None,
    model:         Optional[str] = None,
    temperature:   float = 0.0,
    max_tokens:    int = 2048,
) -> str:
    """One-shot string query. Convenience wrapper around `query_llm`.

    Builds a one- or two-message list (system + user, or just user)
    and delegates. Use this when the call is a single question; use
    `query_llm` directly when more roles or history are involved.

    Parameters
    ----------
    prompt : str
        The user's message.
    system_prompt : optional str.
        If supplied, prepended as a `system` message.
    model, temperature, max_tokens
        Same as `query_llm`.

    Returns
    -------
    The assistant's text response, as a string.
    """
    messages: list[dict[str, str]] = []
    if system_prompt is not None:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    return query_llm(
        messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )


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
    # Two equivalent calls, demonstrating both entry points.
    print(ask_llm("Say hi in three words."))
    print(query_llm([
        {"role": "user", "content": "Say hi in three words."},
    ]))

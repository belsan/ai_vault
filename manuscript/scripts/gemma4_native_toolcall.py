"""Probe Gemma 4's native tool-call format through Ollama.

This script targets the local Ollama endpoint already used elsewhere in the
manuscript (http://192.168.50.3:11700). It exercises Gemma 4's *native*
function-calling channel, which Google documents at:

    https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4

Ollama wraps Gemma 4's special tokens (<|tool_call> ... <tool_call|>) and
exposes the parsed result through the `tool_calls` field of the chat
response, so the developer normally does not need to manipulate the raw
template. This script prints both views: the structured response and the
raw assistant message, so the reader can confirm what the model actually
emitted.

Run with:
    python3 gemma4_native_toolcall.py
"""

from __future__ import annotations

import json
from typing import Any

import requests

OLLAMA_BASE_URL = "http://192.168.50.3:11700"
CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"

MODEL = "gemma4:26b"  # adjust to whichever Gemma 4 size is pulled locally


# ---------------------------------------------------------------------------
# 1. The tool implementation: ordinary Python.
# ---------------------------------------------------------------------------
def count_letter(word: str, letter: str) -> int:
    """Return how many times `letter` occurs in `word` (case-insensitive)."""
    return sum(1 for c in word.lower() if c == letter.lower())


# ---------------------------------------------------------------------------
# 2. The schema we send to Ollama. Same JSON-schema shape as OpenAI uses;
#    Ollama translates it into Gemma 4's native <|tool> declaration block.
# ---------------------------------------------------------------------------
TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "count_letter",
            "description": "Count occurrences of a letter in a word.",
            "parameters": {
                "type": "object",
                "properties": {
                    "word":   {"type": "string"},
                    "letter": {"type": "string", "minLength": 1, "maxLength": 1},
                },
                "required": ["word", "letter"],
            },
        },
    }
]

DISPATCH = {"count_letter": count_letter}


def query(user_message: str, model: str = MODEL) -> str:
    """Run a full tool-call loop against Gemma 4 and return the final answer."""
    messages: list[dict[str, Any]] = [
        {"role": "user", "content": user_message},
    ]

    while True:
        rsp = requests.post(
            CHAT_URL,
            json={
                "model":    model,
                "stream":   False,
                "messages": messages,
                "tools":    TOOLS,
            },
            timeout=120,
        )
        rsp.raise_for_status()
        msg = rsp.json()["message"]
        print("--- raw assistant message ---")
        print(json.dumps(msg, indent=2))
        messages.append(msg)

        tool_calls = msg.get("tool_calls") or []
        if not tool_calls:
            return msg.get("content", "")

        for call in tool_calls:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            if isinstance(args, str):     # some Ollama builds stringify
                args = json.loads(args)
            result = DISPATCH[name](**args)
            messages.append({
                "role":    "tool",
                "name":    name,
                "content": json.dumps(result),
            })


if __name__ == "__main__":
    answer = query("How many r's are in the word 'strawberry'?")
    print("\n--- final answer ---")
    print(answer)

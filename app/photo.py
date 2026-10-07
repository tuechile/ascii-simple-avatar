import json
from typing import Literal

import anthropic
from pydantic import create_model

from app.avatar import PARTS

MODEL = "claude-opus-5-5"

Traits = create_model("Traits", **{slot: (Literal[tuple(options)], ...) for slot, options in PARTS.items()})

PROMPT = f"""Turn the person in this photo into a tiny, simple ascii avatar by choosing one option per slot.
Match what is visible: hair shape and texture, glasses if worn, a hat or accessory if worn, expression for eyes and mouth, outfit and pattern from their clothes.
Pick the closest option even when nothing matches exactly. Use "none" for anything not present.
Options per slot: {json.dumps({slot: list(options) for slot, options in PARTS.items()})}"""


class Refused(Exception):
    pass


class Unconfigured(Exception):
    pass


def traits(media_type, data):
    try:
        return ask(media_type, data)
    except TypeError as error:
        raise Unconfigured() from error


def ask(media_type, data):
    response = anthropic.Anthropic().beta.messages.parse(
        model=MODEL,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": "low"},
        output_format=Traits,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}},
                {"type": "text", "text": PROMPT},
            ],
        }],
    )
    if response.stop_reason == "refusal" or response.parsed_output is None:
        raise Refused()
    return response.parsed_output.model_dump()

import base64
import binascii
import random
import re

from app.avatar import PARTS, pick, render
from app.motion import FPS, MOTION, frames

DATA_URL = re.compile(r"data:(image/(?:jpeg|png|webp));base64,([A-Za-z0-9+/=]+)")


class Invalid(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


def resolve(params, seed):
    chosen = {name: params.get(name) for name in PARTS}
    for name, value in chosen.items():
        if value and value not in PARTS[name]:
            raise Invalid(400, f"unknown {name}: {value}")
    return pick(seed, **chosen)


def number(params, name, default):
    try:
        return int(params[name]) if params.get(name) not in (None, "") else default
    except ValueError:
        raise Invalid(400, f"{name} must be a number")


def parse_play(text):
    play = dict(item.split(":", 1) for item in text.split(",") if ":" in item)
    for feature, action in play.items():
        if action not in MOTION.get(feature, {}):
            raise Invalid(400, f"unknown motion: {feature}:{action}")
    return play


def parts():
    return {name: list(options) for name, options in PARTS.items()}


def motions():
    return {feature: list(actions) for feature, actions in MOTION.items()}


def avatar(params):
    seed = number(params, "seed", random.randrange(10**9))
    selected = resolve(params, seed)
    return {"seed": seed, "parts": selected, "art": render(selected, seed)}


def options(slot, params):
    if slot not in PARTS:
        raise Invalid(404, f"unknown slot: {slot}")
    seed = number(params, "seed", 0)
    base = resolve(params, seed)
    return [{"name": name, "art": render({**base, slot: name}, seed)} for name in PARTS[slot]]


def animate(params):
    seed = number(params, "seed", 0)
    selected = resolve(params, seed)
    play = parse_play(params.get("play") or "")
    return {"fps": FPS, "frames": [render(selected, seed, frame) for frame in frames(play)]}


def photo(image):
    from app import photo as reader

    match = DATA_URL.fullmatch(image)
    if not match or len(image) > 7_000_000:
        raise Invalid(400, "send a jpeg, png or webp data url under 5mb")
    try:
        selected = reader.traits(base64.b64decode(match.group(2)))
    except (reader.NoFace, binascii.Error):
        raise Invalid(422, "no face found, try a front-facing photo with good light")
    seed = random.randrange(10**9)
    return {"seed": seed, "parts": selected, "art": render(selected, seed)}

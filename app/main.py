import base64
import binascii
import random
import re
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app import photo
from app.avatar import PARTS, pick, render
from app.motion import FPS, MOTION, frames

app = FastAPI()
INDEX = Path(__file__).parent.parent / "static" / "index.html"
DATA_URL = re.compile(r"data:(image/(?:jpeg|png|webp));base64,([A-Za-z0-9+/=]+)")


class Photo(BaseModel):
    image: str


def resolve(request, seed):
    chosen = {name: request.query_params.get(name) for name in PARTS}
    for name, value in chosen.items():
        if value and value not in PARTS[name]:
            raise HTTPException(400, f"unknown {name}: {value}")
    return pick(seed, **chosen)


def parse_play(text):
    play = dict(item.split(":", 1) for item in text.split(",") if ":" in item)
    for feature, action in play.items():
        if action not in MOTION.get(feature, {}):
            raise HTTPException(400, f"unknown motion: {feature}:{action}")
    return play


@app.get("/")
def index():
    return FileResponse(INDEX)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/parts")
def parts():
    return {name: list(options) for name, options in PARTS.items()}


@app.get("/motions")
def motions():
    return {feature: list(actions) for feature, actions in MOTION.items()}


@app.get("/avatar")
def avatar(request: Request, seed: int | None = None):
    seed = seed if seed is not None else random.randrange(10**9)
    selected = resolve(request, seed)
    return {"seed": seed, "parts": selected, "art": render(selected, seed)}


@app.get("/options/{slot}")
def options(slot: str, request: Request, seed: int = 0):
    if slot not in PARTS:
        raise HTTPException(404, f"unknown slot: {slot}")
    base = resolve(request, seed)
    return [{"name": name, "art": render({**base, slot: name}, seed)} for name in PARTS[slot]]


@app.get("/animate")
def animate(request: Request, seed: int = 0, play: str = ""):
    selected = resolve(request, seed)
    return {"fps": FPS, "frames": [render(selected, seed, frame) for frame in frames(parse_play(play))]}


@app.post("/photo")
def from_photo(body: Photo):
    match = DATA_URL.fullmatch(body.image)
    if not match or len(body.image) > 7_000_000:
        raise HTTPException(400, "send a jpeg, png or webp data url under 5mb")
    try:
        selected = photo.traits(base64.b64decode(match.group(2)))
    except (photo.NoFace, binascii.Error):
        raise HTTPException(422, "no face found, try a front-facing photo with good light")
    seed = random.randrange(10**9)
    return {"seed": seed, "parts": selected, "art": render(selected, seed)}

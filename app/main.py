import random
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse

from app.avatar import PARTS, pick, render

app = FastAPI()
INDEX = Path(__file__).parent.parent / "static" / "index.html"


def resolve(request, seed):
    chosen = {name: request.query_params.get(name) for name in PARTS}
    for name, value in chosen.items():
        if value and value not in PARTS[name]:
            raise HTTPException(400, f"unknown {name}: {value}")
    return pick(seed, **chosen)


@app.get("/")
def index():
    return FileResponse(INDEX)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/parts")
def parts():
    return {name: list(options) for name, options in PARTS.items()}


@app.get("/avatar")
def avatar(request: Request, seed: int | None = None):
    seed = seed if seed is not None else random.randrange(10**9)
    selected = resolve(request, seed)
    return {"seed": seed, "parts": selected, "art": render(selected)}


@app.get("/options/{slot}")
def options(slot: str, request: Request, seed: int = 0):
    if slot not in PARTS:
        raise HTTPException(404, f"unknown slot: {slot}")
    base = resolve(request, seed)
    return [{"name": name, "art": render({**base, slot: name})} for name in PARTS[slot]]

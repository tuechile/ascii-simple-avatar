from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app import service

app = FastAPI()
INDEX = Path(__file__).parent.parent / "static" / "index.html"


class Photo(BaseModel):
    image: str


def run(action, *args):
    try:
        return action(*args)
    except service.Invalid as error:
        raise HTTPException(error.status, error.message)


@app.get("/")
def index():
    return FileResponse(INDEX)


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/parts")
def parts():
    return service.parts()


@app.get("/motions")
def motions():
    return service.motions()


@app.get("/avatar")
def avatar(request: Request):
    return run(service.avatar, dict(request.query_params))


@app.get("/options/{slot}")
def options(slot: str, request: Request):
    return run(service.options, slot, dict(request.query_params))


@app.get("/animate")
def animate(request: Request):
    return run(service.animate, dict(request.query_params))


@app.post("/photo")
def photo(body: Photo):
    return run(service.photo, body.image)

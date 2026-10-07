from itertools import product

from fastapi.testclient import TestClient

from app.avatar import H, PARTS, W, pick, render
from app.main import app

client = TestClient(app)


def test_same_seed_same_avatar():
    assert pick(7) == pick(7)
    assert render(pick(7), 7) == render(pick(7), 7)


def test_chosen_part_wins():
    assert pick(7, hair="bob")["hair"] == "bob"


def test_every_option_renders_on_grid():
    for slot, options in PARTS.items():
        for name in options:
            rows = render(pick(1, **{slot: name}), 1).split("\n")
            assert len(rows) == H and all(len(row) == W for row in rows)


def test_glasses_wrap_eyes():
    assert "(o)-(o)" in render(pick(1, eyes="round", glasses="round"))


def test_line_styles_differ():
    base = pick(1, hair="bald", top="none")
    assert len({render({**base, "line": name}) for name in PARTS["line"]}) == len(PARTS["line"])


def test_texture_fills_hair():
    art = render(pick(1, hair="afro", texture="ribbon"))
    assert art.count("▰") > 30


def test_random_seeds_fit_grid():
    for seed, face in product(range(30), PARTS["face"]):
        rows = render(pick(seed, face=face), seed).split("\n")
        assert len(rows) == H and all(len(row) == W for row in rows)


def test_avatar_endpoint():
    body = client.get("/avatar", params={"seed": 1, "glasses": "shades"}).json()
    assert body["seed"] == 1 and body["parts"]["glasses"] == "shades" and "[■]-[■]" in body["art"]


def test_unknown_part_rejected():
    assert client.get("/avatar", params={"hair": "mohawk"}).status_code == 400


def test_options_endpoint():
    body = client.get("/options/top", params={"hair": "bob", "texture": "ribbon"}).json()
    assert [o["name"] for o in body] == list(PARTS["top"])
    assert all("▰" in o["art"] for o in body)


def test_unknown_slot():
    assert client.get("/options/shoes").status_code == 404


def test_every_motion_renders_on_grid():
    from app.motion import FRAMES, MOTION, frames

    for feature, actions in MOTION.items():
        for action in actions:
            arts = [render(pick(2), 2, f) for f in frames({feature: action})]
            assert len(arts) == FRAMES
            assert all(len(row) == W for art in arts for row in art.split("\n"))


def test_motion_changes_frames():
    body = client.get("/animate", params={"seed": 2, "eyes": "round", "play": "eyes:blink,top:bob"}).json()
    assert body["fps"] > 0 and len(set(body["frames"])) > 1


def test_no_motion_is_still():
    body = client.get("/animate", params={"seed": 2}).json()
    assert len(set(body["frames"])) == 1


def test_unknown_motion_rejected():
    assert client.get("/animate", params={"play": "eyes:explode"}).status_code == 400


def test_motions_endpoint():
    assert "blink" in client.get("/motions").json()["eyes"]


def test_photo_maps_traits(monkeypatch):
    from app import photo

    chosen = pick(5, hair="afro", glasses="round")
    monkeypatch.setattr(photo, "traits", lambda media_type, data: chosen)
    body = client.post("/photo", json={"image": "data:image/png;base64,iVBORw0KGgo="}).json()
    assert body["parts"] == chosen and "(" in body["art"]


def test_photo_rejects_non_image():
    assert client.post("/photo", json={"image": "hello"}).status_code == 400


def test_photo_schema_matches_parts():
    from app.photo import Traits

    assert set(Traits.model_fields) == set(PARTS)

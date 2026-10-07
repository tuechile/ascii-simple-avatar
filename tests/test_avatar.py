from itertools import product

from fastapi.testclient import TestClient

from app.avatar import PARTS, pick, render
from app.main import app

client = TestClient(app)


def test_same_seed_same_avatar():
    assert pick(7) == pick(7)


def test_chosen_part_wins():
    assert pick(7, hair="curly")["hair"] == "curly"


def test_every_option_renders():
    for slot, options in PARTS.items():
        for name in options:
            assert render(pick(1, **{slot: name}))


def test_glasses_wrap_eyes():
    art = render(pick(1, eyes="open", glasses="round"))
    assert "(o)-(o)" in art


def test_style_changes_outline():
    styles = {render(pick(1, style=name)) for name in PARTS["style"]}
    assert len(styles) == len(PARTS["style"])


def test_lines_fit_width():
    for seed, style in product(range(20), PARTS["style"]):
        assert all(len(line) <= 19 for line in render(pick(seed, style=style)).splitlines())


def test_avatar_endpoint():
    body = client.get("/avatar", params={"seed": 1, "glasses": "shades"}).json()
    assert body["seed"] == 1 and body["parts"]["glasses"] == "shades" and "[#]-[#]" in body["art"]


def test_unknown_part_rejected():
    assert client.get("/avatar", params={"hair": "mohawk"}).status_code == 400


def test_options_endpoint():
    body = client.get("/options/top", params={"hair": "curly"}).json()
    assert [o["name"] for o in body] == list(PARTS["top"])
    assert all("ssssss" in o["art"] for o in body)


def test_unknown_slot():
    assert client.get("/options/shoes").status_code == 404

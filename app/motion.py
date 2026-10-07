FRAMES = 8
FPS = 6


def moves(layer, steps):
    return [{"move": {layer: step}} for step in steps]


def raws(slot, values):
    return [{"raw": {slot: value}} if value is not None else {} for value in values]


def ticks(name):
    return [{"tick": {name: i}} for i in range(FRAMES)]


UP, DOWN, LEFT, RIGHT, STILL = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)

MOTION = {
    "body": {
        "bounce": moves("all", [STILL, STILL, UP, UP, STILL, STILL, STILL, STILL]),
        "sway": moves("all", [STILL, LEFT, LEFT, STILL, STILL, RIGHT, RIGHT, STILL]),
    },
    "eyes": {
        "blink": raws("eyes", [None, None, None, None, None, "--", None, None]),
        "look": raws("eyes", ["◐◐", "◐◐", None, None, "◑◑", "◑◑", None, None]),
        "wink": raws("eyes", [None, None, None, None, "{l}-", "{l}-", None, None]),
        "sparkle": raws("eyes", [None, "✦✦", None, None, None, "✧✧", None, None]),
    },
    "mouth": {
        "talk": raws("mouth", ["o", None, "-", None, "O", None, "-", None]),
        "chew": raws("mouth", ["w", "-", "w", "-", "w", "-", None, None]),
        "whistle": raws("mouth", [None, None, "o", "o ♪", "o  ♫", "o", None, None]),
    },
    "nose": {
        "twitch": moves("nose", [STILL, STILL, STILL, STILL, LEFT, RIGHT, LEFT, STILL]),
        "sniff": raws("nose", [None, None, None, None, "°", "°", None, None]),
    },
    "hair": {
        "shimmer": ticks("hair"),
        "sway": moves("hair", [STILL, STILL, LEFT, LEFT, STILL, STILL, RIGHT, RIGHT]),
    },
    "glasses": {
        "push up": moves("glasses", [STILL, STILL, STILL, STILL, UP, UP, UP, STILL]),
        "slide": moves("glasses", [STILL, STILL, STILL, DOWN, DOWN, DOWN, STILL, STILL]),
    },
    "cheeks": {
        "glow": raws("cheeks", ["·", "*", "✶", "*", "·", " ", " ", " "]),
    },
    "ears": {
        "swing": moves("ears", [STILL, DOWN, STILL, DOWN, STILL, DOWN, STILL, DOWN]),
        "jingle": raws("ears", [None, "✧✧", None, "✦✦", None, None, None, None]),
    },
    "top": {
        "bob": moves("top", [STILL, STILL, UP, UP, STILL, STILL, STILL, STILL]),
        "wobble": moves("top", [STILL, LEFT, STILL, RIGHT, STILL, LEFT, STILL, RIGHT]),
    },
    "outfit": {
        "shimmer": ticks("pattern"),
        "breathe": moves("outfit", [STILL, STILL, STILL, STILL, DOWN, DOWN, DOWN, DOWN]),
    },
}


def frames(play):
    out = [{"parts": {}, "raw": {}, "move": {}, "tick": {}} for _ in range(FRAMES)]
    for feature, action in play.items():
        for frame, step in zip(out, MOTION[feature][action]):
            for key, value in step.items():
                frame[key].update(value)
    return out

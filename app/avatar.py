import random

W, H = 17, 18

LINE = {
    "classic": {"(": "|", ")": "|"},
    "soft": {},
    "dotted": {"(": ":", ")": ":", "/": ".", "\\": ".", "_": "."},
    "sketch": {"(": "{", ")": "}", "_": "~"},
    "bold": {"(": "█", ")": "█", "/": "█", "\\": "█", "_": "▀"},
    "none": {"(": " ", ")": " ", "/": " ", "\\": " ", "_": " "},
}

FACE = {
    "oval": (2, [
        "      _____",
        "     /.....\\",
        "    (.......)",
        "    (.......)",
        "    (.......)",
        "    (.......)",
        "     \\...../",
        "      \\___/",
    ]),
    "round": (2, [
        "     _______",
        "    /.......\\",
        "   (.........)",
        "   (.........)",
        "   (.........)",
        "   (.........)",
        "    \\......./",
        "     \\_____/",
    ]),
    "square": (2, [
        "    _________",
        "    (.......)",
        "    (.......)",
        "    (.......)",
        "    (.......)",
        "    (.......)",
        "    (.......)",
        "    (_______)",
    ]),
    "pointy": (2, [
        "      _____",
        "     /.....\\",
        "    (.......)",
        "    (.......)",
        "    (.......)",
        "    (.......)",
        "     \\...../",
        "      \\.../",
        "       \\_/",
    ]),
}

NECK = (10, ["       (.)", "       (.)"])

HAIR = {
    "bald": (0, []),
    "buzz": (2, [
        "     #######",
        "    #########",
    ]),
    "bob": (1, [
        "      #####",
        "    #########",
        "   ###########",
        "   ####   ####",
        "   ##       ##",
        "   ##       ##",
        "   ##       ##",
        "   ###     ###",
    ]),
    "pixie": (1, [
        "      ####",
        "    ########",
        "   ##########",
        "   ###    ##",
        "   #",
    ]),
    "long": (1, [
        "      #####",
        "    #########",
        "   ###########",
        "  ####     ####",
        "  ###       ###",
        "  ###       ###",
        "  ###       ###",
        "  ###       ###",
        "  ###       ###",
        "  ###       ###",
        "  ###       ###",
        " ####       ####",
        " ###         ###",
    ]),
    "bun": (0, [
        "       ###",
        "      #####",
        "    #########",
        "   ###########",
        "   ##       ##",
    ]),
    "spiky": (0, [
        "    # # # # #",
        "    #########",
        "   ###########",
        "   ###########",
        "   ##  # #  ##",
    ]),
    "afro": (0, [
        "    #########",
        "  #############",
        " ###############",
        " ###############",
        " #####     #####",
        " ####       ####",
        " ####       ####",
        "  ###       ###",
        "   #         #",
    ]),
    "pigtails": (1, [
        "      #####",
        "    #########",
        "   ###########",
        "  ####     ####",
        "###           ###",
        "###           ###",
        " #             #",
    ]),
}

TEXTURE = {
    "block": "■",
    "gem": "◆◆◆■▲",
    "ribbon": "▰",
    "swirl": "◝",
    "comma": ",",
    "curl": "s",
    "wave": "~",
    "fluff": "@",
    "stitch": "x",
    "mixed": "■◆▪○▲",
}

EYES = {
    "dot": "..",
    "bead": "▪▪",
    "round": "oo",
    "ring": "◎◎",
    "happy": "◠◠",
    "sleepy": "--",
    "tall": "▮▮",
    "pointy": "△△",
    "wink": "◠o",
    "zero": "00",
}

GLASSES = {
    "none": " {l}   {r} ",
    "round": "({l})-({r})",
    "square": "[{l}]-[{r}]",
    "shades": "[■]-[■]",
    "cat": "<{l}>-<{r}>",
    "monocle": " {l}  ({r})",
    "visor": "={l}==={r}=",
}

NOSE = {
    "none": "",
    "hook": "?",
    "curve": "◝",
    "bracket": "}",
    "button": "c",
    "line": "|",
    "slash": "\\",
}

MOUTH = {
    "smile": "◡",
    "o": "o",
    "flat": "-",
    "cat": "w",
    "box": "▢",
    "diamond": "◇",
    "smirk": "◞",
    "tongue": "P",
    "grin": "\\_/",
}

CHEEKS = {
    "none": "",
    "blush": "*",
    "freckles": ":",
    "swirl": "@",
    "rosy": "◌",
}

EARS = {
    "none": "  ",
    "round": "()",
    "pointy": "<>",
    "curly": "{}",
}

EARRINGS = {
    "none": "  ",
    "studs": "°°",
    "hoops": "oo",
    "drops": "◇◇",
    "headphones": "@@",
}

TOP = {
    "none": (0, []),
    "bow": (1, ["            >o<"]),
    "crown": (0, ["      \\^^^/"]),
    "flower": (2, ["   ✿"]),
    "cap": (1, [
        "      _____",
        "    /_______\\__",
    ]),
    "beanie": (0, [
        "        o",
        "     ≡≡≡≡≡≡≡",
        "    ≡≡≡≡≡≡≡≡≡",
        "   ===========",
    ]),
}

OUTFIT = {
    "none": (12, []),
    "tee": (12, [
        "    ###   ###",
        "  #############",
        " ###############",
        "#################",
        "#################",
        "#################",
    ]),
    "vneck": (12, [
        "   ####\\ /####",
        " #######v#######",
        "#################",
        "#################",
        "#################",
        "#################",
    ]),
    "turtleneck": (10, [
        "      #####",
        "      #####",
        "    #########",
        "  #############",
        " ###############",
        "#################",
        "#################",
        "#################",
    ]),
    "hoodie": (11, [
        "     #     #",
        "   ###\\   /###",
        " ######o#o######",
        "#################",
        "#################",
        "#################",
        "#################",
    ]),
    "overalls": (12, [
        "   ##|     |##",
        " ####|     |####",
        "#####[=====]#####",
        "#####|  o  |#####",
        "#####|     |#####",
        "#####|     |#####",
    ]),
}

PATTERN = {
    "grid": "□",
    "scallop": "◠",
    "drip": "▾",
    "six": "6",
    "confetti": "▭3◊○◖",
    "knit": "x+",
    "stripe": ("=", "-"),
    "check": ("▚", "▞"),
    "solid": "▓",
}

PARTS = {
    "line": LINE,
    "face": FACE,
    "hair": HAIR,
    "texture": TEXTURE,
    "eyes": EYES,
    "glasses": GLASSES,
    "nose": NOSE,
    "mouth": MOUTH,
    "cheeks": CHEEKS,
    "earrings": EARRINGS,
    "top": TOP,
    "outfit": OUTFIT,
    "pattern": PATTERN,
    "ears": EARS,
}


PREVIEW = {
    "line": {"face"},
    "face": {"face"},
    "hair": {"hair"},
    "texture": {"hair"},
    "eyes": {"eyes"},
    "glasses": {"eyes", "glasses"},
    "nose": {"nose"},
    "mouth": {"mouth"},
    "cheeks": {"cheeks"},
    "ears": {"ears"},
    "earrings": {"earrings"},
    "top": {"top"},
    "outfit": {"neck", "outfit"},
    "pattern": {"outfit"},
}


TURNS = (-2, -1, 0, 1, 2)

MIRROR = str.maketrans("()[]{}<>/\\◝◜◞◟◐◑▚▞◖◗", ")(][}{><\\/◜◝◟◞◑◐▞▚◗◖")


def pick(seed=None, **chosen):
    rng = random.Random(seed)
    return {name: chosen.get(name) or rng.choice(list(options)) for name, options in PARTS.items()}


def filler(chars, rng):
    if isinstance(chars, tuple):
        return lambda row: chars[row % len(chars)]
    return lambda row: rng.choice(chars)


def place(grid, row, col, ch):
    if 0 <= row < H and 0 <= col < W:
        grid[row][col] = ch


def stamp(grid, layer, fill=None, line=None, shift=(0, 0), cut=W):
    top, rows = layer
    for r, text in enumerate(rows, top):
        for c, ch in enumerate(text):
            if ch == " " or (r >= 4 and c + shift[1] >= cut):
                continue
            if ch == "#":
                ch = fill(r)
            elif ch == ".":
                ch = " "
            elif line is not None:
                ch = line.get(ch, ch)
            place(grid, r + shift[0], c + shift[1], ch)


def put(grid, row, text, shift=(0, 0)):
    start = W // 2 - len(text) // 2
    for c, ch in enumerate(text, start):
        if ch != " ":
            place(grid, row + shift[0], c + shift[1], ch)


def at(grid, row, col, text, shift=(0, 0)):
    for c, ch in enumerate(text, col):
        if ch != " ":
            place(grid, row + shift[0], c + shift[1], ch)


def crop(arts):
    grids = [art.split("\n") for art in arts]
    rows = [r for r in range(H) if any(g[r].strip() for g in grids)] or [0]
    cols = [c for c in range(W) if any(g[r][c] != " " for g in grids for r in range(H))] or [0]
    return ["\n".join(g[r][cols[0]:cols[-1] + 1] for r in range(rows[0], rows[-1] + 1)) for g in grids]


def render(parts, seed=0, frame=None, only=None, turn=0):
    if turn < 0:
        rows = render(parts, seed, frame, only, -turn).split("\n")
        return "\n".join(row[::-1].translate(MIRROR) for row in rows)
    frame = frame or {}
    parts = {**parts, **frame.get("parts", {})}
    raw = frame.get("raw", {})
    tick = frame.get("tick", {})
    moves = frame.get("move", {})

    bodiless = parts["outfit"] == "none"

    def shift(layer):
        dy, dx = moves.get(layer, (0, 0))
        ay, ax = moves.get("all", (0, 0))
        return dy + ay + 2 * bodiless, dx + ax

    def shown(layer):
        return only is None or layer in only

    def texture(name, chars):
        return filler(chars, random.Random(f"{seed}:{name}:{tick.get(name, 0)}"))

    grid = [[" "] * W for _ in range(H)]
    line = LINE[parts["line"]]
    face_top, face_rows = FACE[parts["face"]]
    side = face_rows[6 - face_top]
    left, right = len(side) - len(side.lstrip()) - 1, len(side)
    eyes = EYES[parts["eyes"]]
    eyes = raw.get("eyes", eyes).format(l=eyes[0], r=eyes[1])
    cheek = raw.get("cheeks", CHEEKS[parts["cheeks"]]) or " "
    ears = raw.get("ears", EARS[parts["ears"]])
    earrings = raw.get("earrings", EARRINGS[parts["earrings"]])

    if shown("neck") and not bodiless:
        stamp(grid, NECK, line=line, shift=shift("neck"))
    if shown("outfit"):
        stamp(grid, OUTFIT[parts["outfit"]], fill=texture("pattern", PATTERN[parts["pattern"]]), shift=shift("outfit"))
    if shown("face"):
        stamp(grid, FACE[parts["face"]], line=line, shift=shift("face"))
    glasses = GLASSES[parts["glasses"]].format(l=" ", r=" ")
    nose = raw.get("nose", NOSE[parts["nose"]])
    mouth = raw.get("mouth", MOUTH[parts["mouth"]])
    if turn == 0:
        features = {
            "eyes": (5, 6, f"{eyes[0]}   {eyes[1]}"),
            "glasses": (5, 5, glasses),
            "cheeks": (6, 5, cheek + " " * 5 + cheek),
            "nose": (6, 8 - len(nose) // 2, nose),
            "mouth": (8, 8 - len(mouth) // 2, mouth),
            "ears": (5, left, ears[0] + " " * (right - left - 1) + ears[1]),
            "earrings": (6, left, earrings[0] + " " * (right - left - 1) + earrings[1]),
        }
    elif turn == 1:
        features = {
            "eyes": (5, 7, f"{eyes[0]}  {eyes[1]}"),
            "glasses": (5, 6, glasses[:3] + glasses[4:]),
            "cheeks": (6, 6, cheek),
            "nose": (6, 10, nose),
            "mouth": (8, 9 - len(mouth) // 2, mouth),
            "ears": (5, left + 1, ears[0]),
            "earrings": (6, left + 1, earrings[0]),
        }
    else:
        features = {
            "eyes": (5, 10, eyes[1]),
            "glasses": (5, 8, glasses[3:]),
            "cheeks": (6, 8, cheek),
            "nose": (6, right - 1, nose),
            "mouth": (8, 11 - len(mouth), mouth),
            "ears": (5, 6, ears[1]),
            "earrings": (6, 6, earrings[1]),
        }

    if shown("hair"):
        dy, dx = shift("hair")
        stamp(grid, HAIR[parts["hair"]], fill=texture("hair", TEXTURE[parts["texture"]]), shift=(dy, dx - min(turn, 1)), cut=11 if turn == 2 else W)
    for layer in ("eyes", "glasses", "cheeks", "nose", "mouth", "ears", "earrings"):
        if shown(layer):
            row, col, text = features[layer]
            at(grid, row, col, text, shift(layer))
    if shown("top"):
        stamp(grid, TOP[parts["top"]], shift=shift("top"))
    return "\n".join("".join(row) for row in grid)

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
    "ears": EARS,
    "top": TOP,
    "outfit": OUTFIT,
    "pattern": PATTERN,
}


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


def stamp(grid, layer, fill=None, line=None, shift=(0, 0)):
    top, rows = layer
    for r, text in enumerate(rows, top):
        for c, ch in enumerate(text):
            if ch == " ":
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


def render(parts, seed=0, frame=None):
    frame = frame or {}
    parts = {**parts, **frame.get("parts", {})}
    raw = frame.get("raw", {})
    tick = frame.get("tick", {})
    moves = frame.get("move", {})

    def shift(layer):
        dy, dx = moves.get(layer, (0, 0))
        ay, ax = moves.get("all", (0, 0))
        return dy + ay, dx + ax

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

    stamp(grid, NECK, line=line, shift=shift("neck"))
    stamp(grid, OUTFIT[parts["outfit"]], fill=texture("pattern", PATTERN[parts["pattern"]]), shift=shift("outfit"))
    stamp(grid, FACE[parts["face"]], line=line, shift=shift("face"))
    stamp(grid, HAIR[parts["hair"]], fill=texture("hair", TEXTURE[parts["texture"]]), shift=shift("hair"))
    put(grid, 5, f" {eyes[0]}   {eyes[1]} ", shift("eyes"))
    put(grid, 5, GLASSES[parts["glasses"]].format(l=" ", r=" "), shift("glasses"))
    put(grid, 6, cheek + " " * 5 + cheek, shift("cheeks"))
    put(grid, 6, raw.get("nose", NOSE[parts["nose"]]), shift("nose"))
    put(grid, 8, raw.get("mouth", MOUTH[parts["mouth"]]), shift("mouth"))
    dy, dx = shift("ears")
    for col, ch in ((left, ears[0]), (right, ears[1])):
        if ch != " ":
            place(grid, 6 + dy, col + dx, ch)
    stamp(grid, TOP[parts["top"]], shift=shift("top"))
    return "\n".join("".join(row) for row in grid)

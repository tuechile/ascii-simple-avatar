import random

WIDTH = 19
INNER = 11

STYLE = {
    "classic": {"side": "||", "jaw": "\\/", "chin": "\\_/"},
    "soft": {"side": "()", "jaw": "()", "chin": "`-'"},
    "boxy": {"side": "||", "jaw": "||", "chin": "+-+"},
    "dotted": {"side": "::", "jaw": "::", "chin": "'.'"},
    "bold": {"side": "##", "jaw": "##", "chin": "###"},
}

TOP = {
    "none": "",
    "bow": ">o<",
    "crown": "\\^^^/",
    "halo": ".-~~~-.",
    "sprout": "\\|/",
    "flower": "@}->--",
}

HAIR = {
    "bald": ["", "", ".-----------."],
    "buzz": ["", ".:::::::.", "/:::::::::::\\"],
    "curly": ["ssssss", "ssssssssss", "sssss/ \\sssss"],
    "wavy": ["~~~~.", "~~~~~~~", "***~~/ \\~~***"],
    "spiky": ["/\\/\\/\\", "/\\/\\/\\/\\/\\", "/\\/\\/\\/\\/\\/\\/"],
    "bun": ["(@@)", ".-''''-.", "/           \\"],
}

EYES = {
    "dot": ".",
    "open": "o",
    "sleepy": "-",
    "happy": "^",
    "wide": "U",
    "dizzy": "x",
    "star": "*",
}

GLASSES = {
    "none": "{e} {e}",
    "round": "({e})-({e})",
    "square": "[{e}]-[{e}]",
    "shades": "[#]-[#]",
    "monocle": "{e} ({e})",
    "visor": "<=={e}={e}==>",
}

NOSE = {
    "none": "",
    "hook": "?",
    "button": "c",
    "point": ">",
    "long": "L",
}

CHEEKS = {
    "none": " ",
    "blush": "*",
    "freckles": ":",
    "swirl": "@",
}

MOUTH = {
    "smile": "U",
    "o": "o",
    "cat": "w",
    "flat": "___",
    "shout": "@",
    "tongue": "P",
}

EARS = {
    "none": "  ",
    "studs": "..",
    "hoops": "oo",
    "headphones": "@@",
}

PARTS = {
    "style": STYLE,
    "hair": HAIR,
    "eyes": EYES,
    "glasses": GLASSES,
    "nose": NOSE,
    "mouth": MOUTH,
    "cheeks": CHEEKS,
    "ears": EARS,
    "top": TOP,
}


def pick(seed=None, **chosen):
    rng = random.Random(seed)
    return {name: chosen.get(name) or rng.choice(list(options)) for name, options in PARTS.items()}


def render(parts):
    style = STYLE[parts["style"]]
    side, jaw, chin = style["side"], style["jaw"], style["chin"]
    ears = EARS[parts["ears"]]
    cheek = CHEEKS[parts["cheeks"]]
    eyes = GLASSES[parts["glasses"]].format(e=EYES[parts["eyes"]])
    nose = cheek + NOSE[parts["nose"]].center(5) + cheek
    lines = [
        TOP[parts["top"]],
        *HAIR[parts["hair"]],
        " " + side[0] + eyes.center(INNER) + side[1] + " ",
        ears[0] + side[0] + nose.center(INNER) + side[1] + ears[1],
        " " + jaw[0] + MOUTH[parts["mouth"]].center(INNER) + jaw[1] + " ",
        "  " + chin[0] + chin[1] * (INNER - 2) + chin[2] + "  ",
    ]
    return "\n".join(line.center(WIDTH).rstrip() for line in lines if line.strip())

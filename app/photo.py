import cv2
import numpy as np

CASCADES = {name: cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_{name}.xml") for name in ("frontalface_default", "eye", "smile")}
MAX_SIDE = 640


class NoFace(Exception):
    pass


def traits(data):
    img = decode(data)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = CASCADES["frontalface_default"].detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
    if len(faces) == 0:
        raise NoFace()
    return analyze(img, max(faces, key=lambda f: f[2] * f[3]))


def decode(data):
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise NoFace()
    scale = MAX_SIDE / max(img.shape[:2])
    return cv2.resize(img, None, fx=scale, fy=scale) if scale < 1 else img


def analyze(img, box):
    x, y, w, h = (int(v) for v in box)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def area(top, bottom, left, right):
        r0, r1 = sorted((int(y + top * h), int(y + bottom * h)))
        c0, c1 = sorted((int(x + left * w), int(x + right * w)))
        return slice(max(r0, 0), max(r1, 0)), slice(max(c0, 0), max(c1, 0))

    def near(color, limit):
        return np.linalg.norm(lab - color, axis=2) < limit

    def share(mask, region):
        part = mask[region]
        return float(part.mean()) if part.size else 0.0

    border = np.concatenate([lab[0], lab[: lab.shape[0] // 2, 0], lab[: lab.shape[0] // 2, -1]])
    skin = near(np.median(lab[area(0.5, 0.75, 0.3, 0.7)].reshape(-1, 3), axis=0), 22)
    background = near(np.median(border, axis=0), 18)
    other = ~skin & ~background
    crown = other[area(-0.3, 0.05, 0.1, 0.9)]
    hair = near(np.median(lab[area(-0.3, 0.05, 0.1, 0.9)][crown], axis=0), 25) & other if crown.sum() > 50 else other
    edges = cv2.Canny(gray, 60, 140) > 0

    return {
        "line": "soft",
        "face": face_shape(skin, area),
        "hair": hair_style(hair, area, share),
        "texture": hair_texture(gray, hair, area),
        **eyes_and_glasses(gray, edges, area, share, w),
        "nose": "button",
        "mouth": mouth(gray, area),
        "cheeks": "blush" if lab[area(0.55, 0.75, 0.15, 0.3)][..., 1].mean() - lab[area(0.1, 0.25, 0.3, 0.7)][..., 1].mean() > 6 else "none",
        "ears": "none",
        "top": "none",
        **outfit(gray, skin, edges, area, share),
    }


def face_shape(skin, area):
    def width(row):
        return skin[area(row, row + 0.05, -0.2, 1.2)].mean(axis=0).__gt__(0.5).sum()

    cheek, jaw = width(0.5), width(0.88)
    ratio = jaw / cheek if cheek else 0.7
    if ratio < 0.55:
        return "pointy"
    if ratio > 0.92:
        return "square"
    return "round" if cheek > skin[area(0.5, 0.55, -0.2, 1.2)].shape[1] * 0.75 else "oval"


def hair_style(hair, area, share):
    top = share(hair, area(-0.3, 0.05, 0.1, 0.9))
    crown = share(hair, area(-0.3, -0.12, 0.1, 0.9))
    wide = (share(hair, area(-0.2, 0.5, -0.6, -0.3)) + share(hair, area(-0.2, 0.5, 1.3, 1.6))) / 2
    sides = (share(hair, area(0.5, 1.0, -0.15, 0.05)) + share(hair, area(0.5, 1.0, 0.95, 1.15))) / 2
    below = (share(hair, area(1.0, 1.5, -0.15, 0.1)) + share(hair, area(1.0, 1.5, 0.9, 1.15))) / 2
    if top < 0.25:
        return "bald"
    if wide > 0.5 and crown > 0.6:
        return "afro"
    if below > 0.45:
        return "long"
    if sides > 0.45:
        return "bob"
    if crown < 0.3:
        return "buzz"
    return "pixie"


def hair_texture(gray, hair, area):
    region = area(-0.35, 0.1, -0.1, 1.1)
    mask = hair[region]
    if mask.sum() < 50:
        return "block"
    detail = np.abs(cv2.Laplacian(gray, cv2.CV_32F))[region][mask].mean()
    if detail > 22:
        return "curl"
    if detail > 12:
        return "wave"
    return "block"


def eyes_and_glasses(gray, edges, area, share, w):
    band = area(0.2, 0.55, 0, 1)
    found = CASCADES["eye"].detectMultiScale(gray[band], 1.1, 6, minSize=(w // 10, w // 10))
    eye_light = gray[area(0.3, 0.45, 0.2, 0.8)].mean()
    cheek_light = gray[area(0.55, 0.7, 0.25, 0.75)].mean()
    if eye_light < cheek_light * 0.5:
        return {"eyes": "round", "glasses": "shades"}
    glasses = "round" if share(edges, area(0.32, 0.45, 0.42, 0.58)) > 0.12 else "none"
    if len(found) == 0:
        return {"eyes": "happy", "glasses": glasses}
    size = np.mean([f[2] for f in found]) / w
    return {"eyes": "dot" if size < 0.18 else "round", "glasses": glasses}


def mouth(gray, area):
    region = gray[area(0.62, 1.0, 0.15, 0.85)]
    if region.size == 0:
        return "flat"
    if len(CASCADES["smile"].detectMultiScale(region, 1.7, 22, minSize=(region.shape[1] // 3, region.shape[0] // 5))):
        return "smile"
    lips = gray[area(0.72, 0.88, 0.35, 0.65)]
    return "o" if lips.size and (lips < lips.mean() * 0.45).mean() > 0.15 else "flat"


def outfit(gray, skin, edges, area, share):
    torso = area(1.45, 2.6, -0.4, 1.4)
    neck = share(skin, area(1.05, 1.35, 0.35, 0.65))
    chest = share(skin, area(1.4, 1.6, 0.4, 0.6))
    shape = "turtleneck" if neck < 0.2 else "vneck" if chest > 0.4 else "tee"
    cloth = gray[torso].astype(np.float32)
    if cloth.size == 0:
        return {"outfit": shape, "pattern": "solid"}
    rows, cols = cloth.mean(axis=1).std(), cloth.mean(axis=0).std()
    busy = share(edges, torso)
    if rows > 12 and rows > 2 * cols:
        pattern = "stripe"
    elif rows > 12 and cols > 12:
        pattern = "check"
    elif busy < 0.04:
        pattern = "solid"
    elif busy < 0.1:
        pattern = "knit"
    else:
        pattern = "confetti"
    return {"outfit": shape, "pattern": pattern}

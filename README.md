# ascii-simple-avatar

A cute little fashion app that dresses you up as a tiny ASCII avatar.

```
      ▰▰▰▰▰ >o<
    ▰▰▰▰▰▰▰▰▰
   ▰▰▰▰▰▰▰▰▰▰▰
   ▰▰▰▰   ▰▰▰▰
   ▰▰(o)-(o)▰▰
   ▰▰*  ?  *▰▰
   ▰▰       ▰▰
   ▰▰▰  ◡  ▰▰▰
      \___/
       ( )
       ( )
    □□□   □□□
  □□□□□□□□□□□□□
 □□□□□□□□□□□□□□□
□□□□□□□□□□□□□□□□□
□□□□□□□□□□□□□□□□□
□□□□□□□□□□□□□□□□□
```

## Features

- **Dress up** Picrew-style: tabs grouped into face (face, line, eyes, glasses, nose, mouth, cheeks), hair (hair, texture, top) and outfit (outfit, pattern, ears). Each tile previews your avatar with that option swapped in.
- **Art style** inspired by The Pudding's [30 minutes with a stranger](https://pudding.cool/2025/06/hello-stranger/): a 17x18 character grid, hair and clothes filled with glyph textures (`■◆▲`, `▰`, `◝`, `□◠▾`...), light outlines, single-glyph features.
- **Line styles**: classic, soft, dotted, sketch, bold, none.
- **Shuffle** for a random avatar. The same seed always gives the same avatar, textures included. **Copy** or **save .txt**.
- **Animate**: pick a feature (body, eyes, mouth, nose, hair, glasses, cheeks, ears, top, outfit), then an action (blink, look, wink, talk, whistle, bob, sway, shimmer, glow...). Mix as many as you like.
- **From a photo**: take or upload a picture; local computer vision (OpenCV) finds your face and picks the closest part for each slot: hair length and texture, glasses, smile, blush, neckline and shirt pattern. You get a *simple* avatar built from the same parts, not a detailed pixel-to-character render. No API keys, nothing leaves your server, nothing is stored.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/uvicorn app.main:app --reload
```

Open http://localhost:8000.

## Test

```bash
.venv/bin/pytest -q
```

## Deploy

Stateless, no database, no secrets. Any host that runs a Docker image or a Python web process works (Fly.io, Render, Railway, Cloud Run...).

```bash
docker build -t ascii-avatar .
```

```bash
docker run -p 8000:8000 ascii-avatar
```

The container listens on `$PORT` (default 8000). Without Docker, the start command is `uvicorn app.main:app --host 0.0.0.0 --port $PORT` with `requirements.txt` installed.

## API

| Method | Path      | Description |
|--------|-----------|-------------|
| GET    | `/`       | Minimal web page |
| GET    | `/health` | Health check |
| GET    | `/parts`  | Every available part, by slot |
| GET    | `/avatar` | Avatar as `{seed, parts, art}`. Optional query: `seed` and any slot, e.g. `?hair=curly&glasses=round` |
| GET    | `/options/{slot}` | The current avatar rendered with every option of one slot, as `[{name, art}]` |
| GET    | `/motions` | Every feature and its actions |
| GET    | `/animate` | `{fps, frames}` for the avatar. Same query as `/avatar` plus `play=eyes:blink,top:bob` |
| POST   | `/photo`  | Body `{"image": "data:image/jpeg;base64,..."}`. Returns the same shape as `/avatar` |

## Layout

```
app/avatar.py   part library and renderer
app/motion.py   animation actions
app/photo.py    photo to parts with OpenCV
app/main.py     FastAPI routes
static/         single-page frontend
tests/          pytest suite
```

# ascii-simple-avatar

A cute little fashion app that dresses you up as a tiny ASCII avatar.

```
        >o<
       ssssss
     ssssssssss
   sssss/ \sssss
   |  (o)-(o)  |
  o|  *  ?  *  |o
   \     U     /
    \_________/
```

## Features

- **Dress up** Picrew-style: pick a tab (style, hair, eyes, glasses, nose, mouth, cheeks, ears, top) and click a thumbnail to swap that part.
- **Drawing styles**: classic, soft, boxy, dotted, bold.
- **Shuffle** for a random avatar. The same seed always gives the same avatar. **Copy** puts the art on your clipboard.
- **From a photo** (planned): upload a picture and get back a *simple* avatar built from the same parts, not a detailed pixel-to-character render.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

Open http://localhost:8000.

## Test

```bash
.venv/bin/pytest -q
```

## API

| Method | Path      | Description |
|--------|-----------|-------------|
| GET    | `/`       | Minimal web page |
| GET    | `/health` | Health check |
| GET    | `/parts`  | Every available part, by slot |
| GET    | `/avatar` | Avatar as `{seed, parts, art}`. Optional query: `seed` and any slot, e.g. `?hair=curly&glasses=round` |
| GET    | `/options/{slot}` | The current avatar rendered with every option of one slot, as `[{name, art}]` |

## Layout

```
app/avatar.py   part library and renderer
app/main.py     FastAPI routes
static/         single-page frontend
tests/          pytest suite
```

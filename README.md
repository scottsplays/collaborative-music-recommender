# Collaborative Music Recommender

Seed-song collaborative filtering on Last.fm-style listening data. Enter songs you like, find listeners with overlapping taste, and discover tracks shared by similar users.

Built from my original notebook prototype into a small Python package with tests, offline evaluation, and a Gradio demo.

## Features

- **Collaborative filtering** — map seed songs → listeners → similar users → shared recommendations
- **Song, artist, and album modes** — extend the same overlap idea beyond tracks
- **TF-IDF listener similarity** — lightweight cosine similarity on top song titles
- **Offline evaluation** — hold-one-out hit rate@K on sample users
- **Gradio UI** — seed songs in, recommendations out

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
pip install -e .
pytest
python demos/demo_cli.py --seeds "Ice Cream" --count 5
python demos/demo_cli.py --evaluate
```

Launch the web UI:

```bash
python demos/app_gradio.py
```

## Usage

```python
from music_recs import ListeningCatalog, recommend_songs, evaluate_recommender
from music_recs.data import load_catalog_frames

tracks, artists, albums = load_catalog_frames()
catalog = ListeningCatalog(tracks, artists, albums)

recs = recommend_songs(catalog, ["Ice Cream", "Air War"], count=5)
for rec in recs:
    print(rec.track, "—", rec.artist)

metrics = evaluate_recommender(catalog, sample_size=100)
print(metrics.hit_rate_at_k)
```

Seed format:

- `Track Name`
- `Track Name | Artist Name` for disambiguation

## How it works

1. **Candidate listeners** — collect every user who listened to a seed track.
2. **Similar pairs** — sample user pairs and keep those with TF-IDF cosine similarity above a threshold.
3. **Shared discovery** — recommend songs both users have in common, excluding seeds.
4. **Evaluation** — hide one top track per user, recommend from the rest, and measure hit rate@K.

## Project structure

```
music_recs/          Core library
demos/               CLI + Gradio
data/sample/         Publishable dataset slice
scripts/             Rebuild sample data from full export
tests/               Unit tests
notebooks/           Original notebook (archive)
```

## Data note

The committed sample contains ~400 users. See [data/README.md](data/README.md) for rebuilding from the full export.

## License

MIT — see [LICENSE](LICENSE).

## Publishing

See [PUBLISH.md](PUBLISH.md) for GitHub repo title, description, topics, and push instructions.

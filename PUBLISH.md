# Publish this project on GitHub

Use this checklist when creating the public repository on your new account (e.g. `scottsplays`).

## 1. Repository settings (copy/paste)

| Field | Value |
|-------|--------|
| **Repository name** | `collaborative-music-recommender` |
| **Visibility** | Public |
| **Description** | Collaborative music recommender on Last.fm-style data — seed songs, similar listeners, shared-track discovery, Gradio demo, and offline hit-rate evaluation. |
| **Website** | *(leave blank or link to your resume)* |
| **Topics** | `recommender-systems`, `collaborative-filtering`, `music`, `lastfm`, `python`, `scikit-learn`, `gradio`, `machine-learning` |

### Shorter description (if GitHub truncates)

> Seed-song collaborative filtering with listener similarity, offline hit-rate@K evaluation, and a Gradio demo.

### Alternative repo names

- `music-recommender`
- `lastfm-collaborative-filter`
- `seed-song-recommender`

Pick one and use it consistently on your resume.

---

## 2. Verify locally before pushing

From the `music-recommendation` folder:

```bash
pip install -e ".[dev]"
pytest
python demos/demo_cli.py --seeds "Ice Cream" "Air War" --count 5
python demos/demo_cli.py --evaluate
```

Optional UI smoke test:

```bash
python demos/app_gradio.py
```

---

## 3. Initialize git and push

Create an **empty** repository on GitHub (no README, no .gitignore — this folder already has them).

```bash
cd music-recommendation
git init
git add .
git commit -m "Initial release: collaborative music recommender with evaluation and Gradio demo"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/collaborative-music-recommender.git
git push -u origin main
```

---

## 4. After publishing — make the repo look polished

### About section
Fill in the description and topics from the table above.

### README preview
The first screenshot recruiters see matters. Consider adding later:
- A terminal screenshot of `demo_cli.py` output
- A Gradio screenshot saved to `assets/demo.png`

### Pin the repository
Pin this repo and [neural-network-from-scratch](https://github.com/scottsplays/neural-network-from-scratch) on your GitHub profile.

### Do not commit
- Full `user_top_*.xls` files (~1.6 GB each)
- `Music Recommendation.ipynb` with huge embedded YouTube outputs (archive a cleared notebook in `notebooks/` only)

---

## 5. Resume bullet (suggested)

> **Collaborative Music Recommender** — Built a seed-song recommendation system on Last.fm-style listening data using listener overlap and TF-IDF similarity; added offline hit-rate@K evaluation, pytest coverage, and a Gradio demo. [GitHub](https://github.com/YOUR_USERNAME/collaborative-music-recommender)

Pair with your neural network repo:

> **Neural Network from Scratch** — Feedforward network with manual backpropagation and UCI Wine Quality evaluation. [GitHub](https://github.com/scottsplays/neural-network-from-scratch)

---

## 6. What makes this presentable

Compared to the original notebook-only version, this repo includes:

| Before | After |
|--------|--------|
| Notebook only | Importable `music_recs` package |
| 1.6 GB data required | Sample dataset committed (~400 users) |
| Gradio disconnected from recommender | End-to-end Gradio app |
| No metrics | Hit rate@K evaluation |
| Random loops could hang | `max_attempts` safety cap |
| No tests | `pytest` suite |

---

## 7. Optional next improvements (not required to publish)

- Add `assets/demo.png` to README
- GitHub Actions workflow running `pytest` on push
- Compare TF-IDF vs. Jaccard similarity on shared songs in README
- Link to dataset license / HetRec attribution in `data/README.md`

You can publish now and iterate later.

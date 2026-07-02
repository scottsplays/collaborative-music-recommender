# Data

This repository ships a **sample slice** of a Last.fm-style listening dataset in `sample/` (~400 users). The full export is too large for GitHub (multi-GB tab-separated files).

## Sample files (committed)

- `user_top_tracks.csv`
- `user_top_artists.csv`
- `user_top_albums.csv`

Each file contains ranked top tracks, artists, or albums per user.

## Rebuild the sample locally

If you have the full `user_top_*.xls` files locally:

```bash
python scripts/build_sample_data.py --source-dir /path/to/full/data --max-user-id 400
```

## Full dataset

The original tables follow the [HetRec 2011 Last.fm 2K](https://grouplens.org/datasets/hetrec-2011/) format. If you use the full corpus, place the files outside the repo (see `.gitignore`) and point `build_sample_data.py` at them, or load from a custom directory in your own fork.

Do not commit multi-gigabyte exports to GitHub.

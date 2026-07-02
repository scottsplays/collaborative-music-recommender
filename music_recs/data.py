"""Load listening-history tables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "sample"


def load_catalog_frames(data_dir: Path | str | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load tracks, artists, and albums tables from a data directory."""
    root = Path(data_dir) if data_dir else DEFAULT_DATA_DIR
    tracks = pd.read_csv(root / "user_top_tracks.csv")
    artists = pd.read_csv(root / "user_top_artists.csv")
    albums = pd.read_csv(root / "user_top_albums.csv")
    return tracks, artists, albums

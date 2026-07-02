"""Build a publishable sample dataset from full Last.fm export files."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

SOURCE_FILES = {
    "user_top_tracks.csv": "user_top_tracks.xls",
    "user_top_artists.csv": "user_top_artists.xls",
    "user_top_albums.csv": "user_top_albums.xls",
}


def build_sample(source_dir: Path, output_dir: Path, max_user_id: int, chunksize: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    keep = set(range(1, max_user_id + 1))

    for output_name, source_name in SOURCE_FILES.items():
        source_path = source_dir / source_name
        if not source_path.exists():
            raise FileNotFoundError(f"Missing source file: {source_path}")

        parts: list[pd.DataFrame] = []
        for chunk in pd.read_csv(
            source_path,
            chunksize=chunksize,
            encoding="utf-8",
            on_bad_lines="skip",
        ):
            filtered = chunk[chunk["user_id"].isin(keep)]
            if len(filtered):
                parts.append(filtered)

        if not parts:
            raise RuntimeError(f"No rows found for users 1..{max_user_id} in {source_name}")

        frame = pd.concat(parts, ignore_index=True)
        frame.to_csv(output_dir / output_name, index=False)
        print(
            f"Wrote {output_name}: {len(frame):,} rows, "
            f"{frame['user_id'].nunique():,} users"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Create sample CSV files for GitHub")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("."),
        help="Directory containing user_top_*.xls files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "sample",
    )
    parser.add_argument("--max-user-id", type=int, default=400)
    parser.add_argument("--chunksize", type=int, default=200_000)
    args = parser.parse_args()
    build_sample(args.source_dir, args.output_dir, args.max_user_id, args.chunksize)


if __name__ == "__main__":
    main()

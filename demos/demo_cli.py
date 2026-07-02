"""CLI demo for collaborative song recommendations."""

from __future__ import annotations

import argparse

from music_recs import ListeningCatalog, recommend_albums, recommend_artists, recommend_songs
from music_recs.data import load_catalog_frames


def main() -> None:
    parser = argparse.ArgumentParser(description="Collaborative music recommender demo")
    parser.add_argument(
        "--seeds",
        nargs="+",
        default=["Ice Cream", "Air War"],
        help='Seed songs, or "track | artist" pairs',
    )
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--artists", nargs="*", help="Optional artist seeds")
    parser.add_argument("--albums", nargs="*", help="Optional album seeds")
    parser.add_argument("--evaluate", action="store_true", help="Run offline hit-rate evaluation")
    args = parser.parse_args()

    tracks, artists, albums = load_catalog_frames()
    catalog = ListeningCatalog(tracks, artists, albums)

    print("Seed songs:", ", ".join(args.seeds))
    song_recs = recommend_songs(catalog, args.seeds, args.count)
    if not song_recs:
        print("No song recommendations found for these seeds.")
    for index, rec in enumerate(song_recs, start=1):
        print(f"{index}. {rec.track} — {rec.artist}")

    if args.artists:
        print("\nSeed artists:", ", ".join(args.artists))
        artist_recs = recommend_artists(catalog, args.artists, args.count)
        for index, artist in enumerate(artist_recs, start=1):
            sample = catalog.sample_songs_by_artist(artist)
            joined = "; ".join(sample) if sample else "no sample tracks"
            print(f"{index}. {artist} (e.g. {joined})")

    if args.albums:
        print("\nSeed albums:", ", ".join(args.albums))
        album_recs = recommend_albums(catalog, args.albums, args.count)
        for index, rec in enumerate(album_recs, start=1):
            print(f"{index}. {rec.album} — {rec.artist}")

    if args.evaluate:
        from music_recs import evaluate_recommender

        result = evaluate_recommender(catalog, sample_size=50, recommendation_count=args.count)
        print("\nEvaluation")
        print(f"  Users evaluated: {result.users_evaluated}")
        print(f"  Hit rate@{args.count}: {result.hit_rate_at_k:.3f}")


if __name__ == "__main__":
    main()

"""Collaborative recommendation from seed songs, artists, or albums."""

from __future__ import annotations

import random
from dataclasses import dataclass

from music_recs.catalog import ListeningCatalog, _norm
from music_recs.similarity import user_similarity


@dataclass(frozen=True)
class SongRecommendation:
    track: str
    artist: str


@dataclass(frozen=True)
class AlbumRecommendation:
    album: str
    artist: str


def _unique_song_key(track: str, artist: str) -> str:
    return f"{_norm(track)}::{_norm(artist)}"


def recommend_songs(
    catalog: ListeningCatalog,
    seeds: list[str],
    count: int = 5,
    *,
    similarity_threshold: float = 0.05,
    max_attempts: int = 500,
    rng: random.Random | None = None,
) -> list[SongRecommendation]:
    """Recommend tracks based on listeners who share seed songs."""
    random_gen = rng or random.Random()
    seed_tracks = {_norm(seed.split(" | ", 1)[0]) for seed in seeds}
    seed_extras = {seed.split(" | ", 1)[0].strip() for seed in seeds if " | " in seed}
    blocked = seed_tracks | {_norm(item) for item in seed_extras}

    candidate_users = catalog.expand_seed_users(seeds)
    if len(candidate_users) < 2:
        return []

    results: list[SongRecommendation] = []
    seen: set[str] = set()
    attempts = 0

    while len(results) < count and attempts < max_attempts:
        attempts += 1
        user1, user2 = random_gen.sample(candidate_users, 2)
        if user_similarity(catalog, user1, user2) <= similarity_threshold:
            continue

        shared_songs, shared_artists = catalog.shared_songs(user1, user2)
        if not shared_songs:
            continue

        index = random_gen.randrange(len(shared_songs))
        track = shared_songs[index]
        artist = shared_artists[index]
        key = _unique_song_key(track, artist)
        if key in seen or _norm(track) in blocked:
            continue

        seen.add(key)
        results.append(SongRecommendation(track=track, artist=artist))

    return results


def recommend_artists(
    catalog: ListeningCatalog,
    seed_artists: list[str],
    count: int = 5,
    *,
    max_attempts: int = 500,
    rng: random.Random | None = None,
) -> list[str]:
    random_gen = rng or random.Random()
    blocked = {_norm(artist) for artist in seed_artists}
    candidate_users: list[int] = []
    for artist in seed_artists:
        candidate_users.extend(catalog.users_for_artist(artist))
    if len(candidate_users) < 2:
        return []

    results: list[str] = []
    attempts = 0

    while len(results) < count and attempts < max_attempts:
        attempts += 1
        user1, user2 = random_gen.sample(candidate_users, 2)
        shared = catalog.shared_artists(user1, user2)
        if not shared:
            continue
        artist = random_gen.choice(shared)
        if _norm(artist) in blocked or artist in results:
            continue
        results.append(artist)

    return results


def recommend_albums(
    catalog: ListeningCatalog,
    seed_albums: list[str],
    count: int = 5,
    *,
    max_attempts: int = 500,
    rng: random.Random | None = None,
) -> list[AlbumRecommendation]:
    random_gen = rng or random.Random()
    blocked = {_norm(album) for album in seed_albums}
    candidate_users: list[int] = []
    for album in seed_albums:
        candidate_users.extend(catalog.users_for_album(album))
    if len(candidate_users) < 2:
        return []

    results: list[AlbumRecommendation] = []
    seen: set[str] = set()
    attempts = 0

    while len(results) < count and attempts < max_attempts:
        attempts += 1
        user1, user2 = random_gen.sample(candidate_users, 2)
        shared_albums, shared_artists = catalog.shared_albums(user1, user2)
        if not shared_albums:
            continue
        index = random_gen.randrange(len(shared_albums))
        album = shared_albums[index]
        artist = shared_artists[index]
        key = _norm(album)
        if key in blocked or key in seen:
            continue
        seen.add(key)
        results.append(AlbumRecommendation(album=album, artist=artist))

    return results

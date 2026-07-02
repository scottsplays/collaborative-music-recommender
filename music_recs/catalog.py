"""User listening catalog queries and overlap helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import pandas as pd


def _norm(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    return str(value).strip().lower()


@dataclass
class ListeningCatalog:
    tracks: pd.DataFrame
    artists: pd.DataFrame
    albums: pd.DataFrame
    top_n: int = 50
    _track_users: dict[str, set[int]] = field(default_factory=dict, init=False, repr=False)
    _artist_users: dict[str, set[int]] = field(default_factory=dict, init=False, repr=False)
    _album_users: dict[str, set[int]] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        self._build_indexes()

    def _build_indexes(self) -> None:
        for track, user_id in zip(self.tracks["track_name"], self.tracks["user_id"]):
            self._track_users.setdefault(_norm(str(track)), set()).add(int(user_id))

        for artist, user_id in zip(self.artists["artist_name"], self.artists["user_id"]):
            self._artist_users.setdefault(_norm(str(artist)), set()).add(int(user_id))

        for album, user_id in zip(self.albums["album_name"], self.albums["user_id"]):
            self._album_users.setdefault(_norm(str(album)), set()).add(int(user_id))

    def top_songs(self, user_id: int, n: int | None = None) -> tuple[list[str], list[str]]:
        count = n or self.top_n
        rows = self.tracks.loc[self.tracks["user_id"] == user_id].sort_values("rank").head(count)
        return rows["track_name"].tolist(), rows["artist_name"].tolist()

    def top_artists(self, user_id: int, n: int | None = None) -> list[str]:
        count = n or self.top_n
        rows = self.artists.loc[self.artists["user_id"] == user_id].sort_values("rank").head(count)
        return rows["artist_name"].tolist()

    def top_albums(self, user_id: int, n: int | None = None) -> tuple[list[str], list[str]]:
        count = n or self.top_n
        rows = self.albums.loc[self.albums["user_id"] == user_id].sort_values("rank").head(count)
        return rows["album_name"].tolist(), rows["artist_name"].tolist()

    def shared_songs(self, user1: int, user2: int, n: int | None = None) -> tuple[list[str], list[str]]:
        songs1, artists1 = self.top_songs(user1, n)
        songs2, _ = self.top_songs(user2, n)
        songs2_set = {_norm(s) for s in songs2}
        shared_songs: list[str] = []
        shared_artists: list[str] = []
        for song, artist in zip(songs1, artists1):
            if _norm(song) in songs2_set:
                shared_songs.append(song)
                shared_artists.append(artist)
        return shared_songs, shared_artists

    def shared_artists(self, user1: int, user2: int, n: int | None = None) -> list[str]:
        artists1 = self.top_artists(user1, n)
        artists2 = {_norm(a) for a in self.top_artists(user2, n)}
        return [artist for artist in artists1 if _norm(artist) in artists2]

    def shared_albums(self, user1: int, user2: int, n: int | None = None) -> tuple[list[str], list[str]]:
        albums1, artists1 = self.top_albums(user1, n)
        albums2, _ = self.top_albums(user2, n)
        albums2_set = {_norm(a) for a in albums2}
        shared_albums: list[str] = []
        shared_artists: list[str] = []
        for album, artist in zip(albums1, artists1):
            if _norm(album) in albums2_set:
                shared_albums.append(album)
                shared_artists.append(artist)
        return shared_albums, shared_artists

    def users_for_track(self, track_name: str) -> list[int]:
        return sorted(self._track_users.get(_norm(track_name), set()))

    def users_for_artist(self, artist_name: str) -> list[int]:
        return sorted(self._artist_users.get(_norm(artist_name), set()))

    def users_for_album(self, album_name: str) -> list[int]:
        return sorted(self._album_users.get(_norm(album_name), set()))

    def sample_songs_by_artist(self, artist_name: str, count: int = 3) -> list[str]:
        rows = self.tracks.loc[self.tracks["artist_name"].str.lower() == _norm(artist_name), "track_name"]
        songs = rows.drop_duplicates().tolist()
        if len(songs) <= count:
            return songs
        import random

        return random.sample(songs, count)

    def all_user_ids(self) -> list[int]:
        return sorted(self.tracks["user_id"].unique().tolist())

    def expand_seed_users(self, seeds: Iterable[str]) -> list[int]:
        """Map seed song or `track | artist` strings to listener user ids."""
        users: list[int] = []
        for seed in seeds:
            if " | " in seed:
                track, artist = seed.split(" | ", 1)
                mask = (self.tracks["track_name"].str.lower() == _norm(track)) & (
                    self.tracks["artist_name"].str.lower() == _norm(artist)
                )
            else:
                mask = self.tracks["track_name"].str.lower() == _norm(seed)
            users.extend(self.tracks.loc[mask, "user_id"].tolist())
        return users

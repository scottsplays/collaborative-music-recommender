import pandas as pd
import pytest

from music_recs import ListeningCatalog, evaluate_recommender, recommend_songs
from music_recs.catalog import _norm
from music_recs.data import load_catalog_frames
from music_recs.similarity import user_similarity


@pytest.fixture(scope="module")
def catalog() -> ListeningCatalog:
    tracks, artists, albums = load_catalog_frames()
    return ListeningCatalog(tracks, artists, albums)


def test_catalog_top_songs(catalog: ListeningCatalog):
    songs, artists = catalog.top_songs(1, 5)
    assert len(songs) == 5
    assert len(artists) == 5


def test_shared_songs_overlap(catalog: ListeningCatalog):
    user_ids = catalog.all_user_ids()
    user1, user2 = user_ids[0], user_ids[1]
    shared_songs, _ = catalog.shared_songs(user1, user2)
    assert isinstance(shared_songs, list)


def test_user_similarity_range(catalog: ListeningCatalog):
    user_ids = catalog.all_user_ids()
    score = user_similarity(catalog, user_ids[0], user_ids[1])
    assert 0.0 <= score <= 1.0


def test_recommend_songs_returns_results(catalog: ListeningCatalog):
    seeds = catalog.top_songs(50, 2)[0]
    recs = recommend_songs(catalog, seeds, 3, rng=__import__("random").Random(0))
    assert len(recs) > 0
    assert all(rec.track and rec.artist for rec in recs)


def test_recommendations_avoid_seed_tracks(catalog: ListeningCatalog):
    seeds = ["Ice Cream"]
    recs = recommend_songs(catalog, seeds, 5, rng=__import__("random").Random(1))
    seed_names = {_norm(seed.split(" | ", 1)[0]) for seed in seeds}
    for rec in recs:
        assert _norm(rec.track) not in seed_names


def test_evaluation_runs(catalog: ListeningCatalog):
    result = evaluate_recommender(
        catalog,
        sample_size=20,
        recommendation_count=3,
        rng=__import__("random").Random(2),
    )
    assert result.users_evaluated > 0
    assert 0.0 <= result.hit_rate_at_k <= 1.0

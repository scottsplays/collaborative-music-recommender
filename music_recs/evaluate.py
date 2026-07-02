"""Offline evaluation for song recommendations."""

from __future__ import annotations

import random
from dataclasses import dataclass

from music_recs.catalog import ListeningCatalog, _norm
from music_recs.recommend import recommend_songs


@dataclass(frozen=True)
class EvaluationResult:
    users_evaluated: int
    hit_rate_at_k: float
    mean_hits_per_user: float


def evaluate_recommender(
    catalog: ListeningCatalog,
    *,
    users: list[int] | None = None,
    sample_size: int = 100,
    holdout_rank: int = 1,
    recommendation_count: int = 5,
    seed_size: int = 3,
    rng: random.Random | None = None,
) -> EvaluationResult:
    """
    Leave-one-out style evaluation:
    hide one top track per user, recommend from remaining seeds, check for a hit.
    """
    random_gen = rng or random.Random(42)
    pool = users or catalog.all_user_ids()
    if len(pool) > sample_size:
        pool = random_gen.sample(pool, sample_size)

    hits = 0
    evaluated = 0

    for user_id in pool:
        songs, _ = catalog.top_songs(user_id, catalog.top_n)
        if len(songs) < seed_size + 1:
            continue

        held_out = songs[holdout_rank - 1]
        seed_tracks = [songs[i] for i in range(len(songs)) if i != holdout_rank - 1][:seed_size]
        recommendations = recommend_songs(
            catalog,
            seed_tracks,
            recommendation_count,
            rng=random_gen,
        )
        recommended_names = {_norm(rec.track) for rec in recommendations}
        if _norm(held_out) in recommended_names:
            hits += 1
        evaluated += 1

    if evaluated == 0:
        return EvaluationResult(users_evaluated=0, hit_rate_at_k=0.0, mean_hits_per_user=0.0)

    return EvaluationResult(
        users_evaluated=evaluated,
        hit_rate_at_k=hits / evaluated,
        mean_hits_per_user=hits / evaluated,
    )

"""Collaborative music recommendation from Last.fm-style listening data."""

from music_recs.catalog import ListeningCatalog
from music_recs.evaluate import EvaluationResult, evaluate_recommender
from music_recs.recommend import (
    recommend_albums,
    recommend_artists,
    recommend_songs,
)

__all__ = [
    "EvaluationResult",
    "ListeningCatalog",
    "evaluate_recommender",
    "recommend_albums",
    "recommend_artists",
    "recommend_songs",
]

"""Listener similarity helpers."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from music_recs.catalog import ListeningCatalog


def user_similarity(catalog: ListeningCatalog, user1: int, user2: int, top_songs: int = 10) -> float:
    """Cosine similarity between users based on TF-IDF vectors of top song titles."""
    songs1 = " ".join(catalog.top_songs(user1, top_songs)[0])
    songs2 = " ".join(catalog.top_songs(user2, top_songs)[0])
    if not songs1.strip() or not songs2.strip():
        return 0.0
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([songs1, songs2])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])

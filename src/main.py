"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Any, Dict

from src.recommender import load_songs, recommend_songs

_RULE = "-" * 50


def print_recommendation(rank: int, song: Dict[str, Any], score: float, explanation: str) -> None:
    """Print one ranked recommendation with bulleted reasons (from newline-split explanation)."""
    title = song["title"]
    print(f"{rank}. {title}  |  Score: {score:.2f}")
    print("Reasons:")
    for line in explanation.splitlines():
        stripped = line.strip()
        if stripped:
            print(f"  - {stripped}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations\n")
    n = len(recommendations)
    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print_recommendation(i, song, score, explanation)
        if i < n:
            print(_RULE)
            print()


if __name__ == "__main__":
    main()

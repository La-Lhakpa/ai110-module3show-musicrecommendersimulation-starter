import csv
from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, List, Optional, Tuple

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_id = (row.get("id") or "").strip()
            if raw_id.lower() == "id":
                continue
            try:
                sid = int(raw_id)
            except ValueError:
                continue
            songs.append(
                {
                    "id": sid,
                    "title": row["title"].strip(),
                    "artist": row["artist"].strip(),
                    "genre": row["genre"].strip(),
                    "mood": row["mood"].strip(),
                    "energy": float(row["energy"]),
                    "tempo_bpm": int(float(row["tempo_bpm"])),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )
    print(f"Loaded songs: {len(songs)}")
    return songs

# Weight experiment: genre halved vs original starter; energy contribution doubled.
GENRE_MATCH_POINTS = 1.0
MOOD_MATCH_POINTS = 1.0
ENERGY_SIMILARITY_WEIGHT = 2.0


def _norm_label(label: str) -> str:
    return label.strip().casefold()


def _prefs_genre_mood_energy(user_prefs: Dict) -> Tuple[str, str, float]:
    return (
        str(user_prefs["genre"]),
        str(user_prefs["mood"]),
        float(user_prefs["energy"]),
    )


def _energy_similarity(song_energy: float, target_energy: float) -> float:
    return max(0.0, 1.0 - abs(song_energy - target_energy))


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Returns total score and human-readable reasons (genre, mood, energy).
    Scoring: +GENRE_MATCH_POINTS on genre match, +MOOD_MATCH_POINTS on mood match,
    plus ENERGY_SIMILARITY_WEIGHT * similarity where similarity = max(0, 1 - |Δenergy|).
    """
    user_genre, user_mood, target_energy = _prefs_genre_mood_energy(user_prefs)
    song_genre = str(song["genre"])
    song_mood = str(song["mood"])
    song_energy = float(song["energy"])
    score = 0.0
    reasons: List[str] = []
    if _norm_label(song_genre) == _norm_label(user_genre):
        score += GENRE_MATCH_POINTS
        reasons.append(f'Genre matches your preference ("{user_genre.strip()}")')
    else:
        reasons.append(
            f'Genre does not match (song is "{song_genre}", you prefer "{user_genre.strip()}")'
        )
    if _norm_label(song_mood) == _norm_label(user_mood):
        score += MOOD_MATCH_POINTS
        reasons.append(f'Mood matches your preference ("{user_mood.strip()}")')
    else:
        reasons.append(
            f'Mood does not match (song is "{song_mood}", you prefer "{user_mood.strip()}")'
        )
    energy_sim = _energy_similarity(song_energy, target_energy)
    energy_points = ENERGY_SIMILARITY_WEIGHT * energy_sim
    score += energy_points
    reasons.append(
        f"Energy: similarity {energy_sim:.2f} × weight {ENERGY_SIMILARITY_WEIGHT:.1f} "
        f"= +{energy_points:.2f} (song {song_energy:.2f} vs target {target_energy:.2f})"
    )
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "\n".join(reasons)))
    scored.sort(key=itemgetter(1), reverse=True)
    return scored[:k]

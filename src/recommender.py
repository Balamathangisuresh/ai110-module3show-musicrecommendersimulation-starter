import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    if not os.path.exists(csv_path):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fallback_path = os.path.join(project_root, csv_path)
        if os.path.exists(fallback_path):
            csv_path = fallback_path
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons = []

    genre_points = 2.0 if user_prefs["genre"] == song["genre"] else 0.0
    if genre_points:
        reasons.append(f"genre match (+{genre_points:.1f})")

    mood_points = 1.0 if user_prefs["mood"] == song["mood"] else 0.0
    if mood_points:
        reasons.append(f"mood match (+{mood_points:.1f})")

    energy_points = 1.0 - abs(user_prefs["energy"] - song["energy"])
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    score = genre_points + mood_points + energy_points

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    scored.sort(
        key=lambda entry: (
            -entry[1],
            abs(user_prefs["energy"] - entry[0]["energy"]),
            entry[0]["id"],
        )
    )

    k = min(k, len(songs))
    return [(song, score, ", ".join(reasons)) for song, score, reasons in scored[:k]]

import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dicts = [asdict(song) for song in self.songs]

        results = recommend_songs(user_prefs, song_dicts, k)

        return [Song(**song_dict) for song_dict, _score, _explanation in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        score, reasons = score_song(user_prefs, asdict(song))

        return f"Score: {score:.2f} | Reasons: {', '.join(reasons)}"

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

GENRE_WEIGHT = 1.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 2.0

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    reasons = []

    user_genre = user_prefs["genre"].strip().lower()
    song_genre = song["genre"].strip().lower()
    genre_points = GENRE_WEIGHT if user_genre == song_genre else 0.0
    if genre_points:
        reasons.append(f"genre match (+{genre_points:.1f})")

    user_mood = user_prefs["mood"].strip().lower()
    song_mood = song["mood"].strip().lower()
    mood_points = MOOD_WEIGHT if user_mood == song_mood else 0.0
    if mood_points:
        reasons.append(f"mood match (+{mood_points:.1f})")

    target_energy = max(0.0, min(1.0, user_prefs["energy"]))
    energy_points = ENERGY_WEIGHT * (1.0 - abs(target_energy - song["energy"]))
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    score = genre_points + mood_points + energy_points

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    target_energy = max(0.0, min(1.0, user_prefs["energy"]))
    scored.sort(
        key=lambda entry: (
            -entry[1],
            abs(target_energy - entry[0]["energy"]),
            entry[0]["id"],
        )
    )

    k = min(k, len(songs))
    return [(song, score, ", ".join(reasons)) for song, score, reasons in scored[:k]]

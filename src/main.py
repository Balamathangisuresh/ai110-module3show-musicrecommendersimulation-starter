"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    """Loads songs, ranks them for a sample user profile, and prints the top recommendations."""
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    jumin_prefs = {"genre": "classical", "mood": "calm", "energy": 0.2}
    zen_prefs = {"genre": "musical theatre", "mood": "dramatic", "energy": 0.9}
    seven_prefs = {"genre": "electronic", "mood": "energetic", "energy": 0.95}

    # Adversarial / edge case profiles - designed to try to "trick" the scoring logic
    conflicted_prefs = {"genre": "folk", "mood": "melancholy", "energy": 0.9}
    nonexistent_genre_prefs = {"genre": "k-pop", "mood": "happy", "energy": 0.6}
    extreme_energy_prefs = {"genre": "metal", "mood": "angry", "energy": 1.5}
    negative_energy_prefs = {"genre": "classical", "mood": "peaceful", "energy": -0.5}
    case_mismatch_prefs = {"genre": "Pop", "mood": " happy", "energy": 0.8}
    frankenstein_prefs = {"genre": "reggae", "mood": "angry", "energy": 0.5}
    no_signal_prefs = {"genre": "opera", "mood": "bored", "energy": 0.5}

    profiles = {
        "Starter (pop/happy/0.8)": user_prefs,
        "Jumin (classical/calm/0.2)": jumin_prefs,
        "Zen (musical theatre/dramatic/0.9)": zen_prefs,
        "Seven (electronic/energetic/0.95)": seven_prefs,
        "Conflicted energy vs. mood": conflicted_prefs,
        "Nonexistent genre": nonexistent_genre_prefs,
        "Extreme energy (>1.0)": extreme_energy_prefs,
        "Negative energy (<0.0)": negative_energy_prefs,
        "Case/whitespace mismatch": case_mismatch_prefs,
        "Frankenstein (split genre/mood match)": frankenstein_prefs,
        "No signal (unknown genre + mood)": no_signal_prefs,
    }

    for label, prefs in profiles.items():
        recommendations = recommend_songs(prefs, songs, k=5)

        header = f"Top Recommendations - {label}"
        print(f"\n{header}\n{'=' * len(header)}\n")
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}/4.00")
            print(f"   Reasons: {explanation}")
            print()


if __name__ == "__main__":
    main()

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

    recommendations = recommend_songs(user_prefs, songs, k=5)

    header = "Top Recommendations"
    print(f"\n{header}\n{'=' * len(header)}\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}/4.00")
        print(f"   Reasons: {explanation}")
        print()


if __name__ == "__main__":
    main()

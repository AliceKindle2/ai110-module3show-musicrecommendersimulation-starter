"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, format_recommendations


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    
    # user_prefs = {
    #      "favorite_genre":      "pop",
    #     "favorite_mood":       "happy",
    #     "target_energy":       0.8,
    #     "target_valence":      0.75,   # optional — remove if not needed
    #     "target_tempo_bpm":    120,    # optional — remove if not needed
    #     "target_acousticness": 0.1,    # optional — remove if not needed
    #     }
    
    # Extreme profiles

    user_prefs = {
    "favorite_genre":      "folk",
    "favorite_mood":       "chill",
    "target_energy":       0.9,    # high energy...
    "target_acousticness": 0.9,    # ...but also very acoustic
}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()

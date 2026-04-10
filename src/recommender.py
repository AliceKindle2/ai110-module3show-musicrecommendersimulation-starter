from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import os

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
        """Store the song catalogue for use across all recommendation calls."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return them as a list of typed dictionaries."""
    FLOAT_FIELDS = {"energy", "valence", "danceability", "acousticness"}
    INT_FIELDS   = {"id", "tempo_bpm"}

    resolved_path = os.path.join(os.path.dirname(__file__), "..", csv_path)
    resolved_path = os.path.normpath(resolved_path)

    songs = []
    try:
        with open(resolved_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                song = {}
                for key, val in row.items():
                    if not key or not key.strip():
                        continue
                    key = key.strip()
                    val = (val or "").strip()
                    try:
                        if key in FLOAT_FIELDS:
                            song[key] = float(val)
                        elif key in INT_FIELDS:
                            song[key] = int(val)
                        else:
                            song[key] = val
                    except ValueError:
                        continue
                if "genre" in song and "mood" in song:
                    songs.append(song)
    except FileNotFoundError:
        print(f"Error: file not found at '{resolved_path}'")

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences and return (score, reasons).
    
    EXPERIMENTAL: Energy weight doubled (max +3.0), genre weight halved (+1.0).
    Max possible score changes from 7.00 to 7.75.
    """
    score = 0.0
    reasons = []

    # --- Exact match: genre (+1.0) [was +2.0] ---
    genre_match = song["genre"].lower() == user_prefs["favorite_genre"].lower()
    if genre_match:
        score += 1.0
        reasons.append(f"genre match: '{song['genre']}' (+1.0)")

    # --- Exact match: mood (+1.0) ---
    mood_match = song["mood"].lower() == user_prefs["favorite_mood"].lower()
    if mood_match:
        score += 1.0
        reasons.append(f"mood match: '{song['mood']}' (+1.0)")

    # --- Combo bonus: genre + mood (+0.5) ---
    if genre_match and mood_match:
        score += 0.5
        reasons.append("genre + mood combo bonus (+0.5)")

    # --- Proximity: energy (max +3.0) [was +1.5] ---
    energy_diff = abs(song["energy"] - user_prefs["target_energy"])
    energy_pts = round(max(0.0, 1.0 - energy_diff / 1.0) * 3.0, 3)
    if energy_pts > 0:
        score += energy_pts
        reasons.append(f"energy proximity: diff={energy_diff:.2f} (+{energy_pts:.2f})")

    # --- Proximity: valence (max +1.0) ---
    if "target_valence" in user_prefs:
        val_diff = abs(song["valence"] - user_prefs["target_valence"])
        val_pts = round(max(0.0, 1.0 - val_diff / 1.0) * 1.0, 3)
        if val_pts > 0:
            score += val_pts
            reasons.append(f"valence proximity: diff={val_diff:.2f} (+{val_pts:.2f})")

    # --- Proximity: tempo (max +0.75, window=60 BPM) ---
    if "target_tempo_bpm" in user_prefs:
        tempo_diff = abs(song["tempo_bpm"] - user_prefs["target_tempo_bpm"])
        tempo_pts = round(max(0.0, 1.0 - tempo_diff / 60.0) * 0.75, 3)
        if tempo_pts > 0:
            score += tempo_pts
            reasons.append(f"tempo proximity: diff={tempo_diff:.0f} BPM (+{tempo_pts:.2f})")

    # --- Proximity: acousticness (max +0.5) ---
    if "target_acousticness" in user_prefs:
        acou_diff = abs(song["acousticness"] - user_prefs["target_acousticness"])
        acou_pts = round(max(0.0, 1.0 - acou_diff / 1.0) * 0.5, 3)
        if acou_pts > 0:
            score += acou_pts
            reasons.append(f"acousticness proximity: diff={acou_diff:.2f} (+{acou_pts:.2f})")

    score = round(score, 3)
    return score, reasons


def format_recommendations(results: List[Tuple[Dict, float, str]]) -> None:
    """Print a formatted terminal summary of ranked song recommendations."""
    width = 52
    border = "─" * width

    print(f"\n┌{border}┐")
    print(f"│{'🎵  TOP RECOMMENDATIONS':^{width}}│")
    print(f"└{border}┘")

    if not results:
        print("  No recommendations found. Try adjusting your preferences.\n")
        return

    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"\n  #{rank}  {song['title']} — {song['artist']}")
        print(f"  {'─' * (width - 2)}")
        print(f"  {'Genre:':<14}{song['genre'].capitalize():<20}{'Mood:':<8}{song['mood'].capitalize()}")
        print(f"  {'Score:':<14}{score:.2f} / 7.00")
        print(f"  {'Reasons:'}")
        for reason in explanation.split(" | "):
            print(f"      • {reason}")

    print(f"\n{'─' * (width + 2)}\n")


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs against user preferences and return the top-k ranked results."""
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [(song, score, " | ".join(reasons)) for song, score, reasons in ranked[:k]]
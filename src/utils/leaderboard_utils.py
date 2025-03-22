# src/utils/leaderboard_utils.py
import json
import os

LEADERBOARD_FILE = "app/data/leaderboard.json"

def load_leaderboard():
    """Load the leaderboard from a JSON file."""
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_leaderboard(leaderboard):
    """Save the leaderboard to a JSON file."""
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f, indent=4)

def update_leaderboard(name, score):
    """Update the leaderboard with a new score."""
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    # Sort the leaderboard by score (descending)
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    # Keep only the top 10 scores
    leaderboard = leaderboard[:10]
    save_leaderboard(leaderboard)
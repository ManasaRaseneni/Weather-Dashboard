import json

FAV_FILE = "favorites.json"

def load_favorites():
    try:
        with open(FAV_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_favorites(cities):
    try:
        with open(FAV_FILE, "w") as f:
            json.dump(cities, f)
    except Exception as e:
        print(f"Error saving favorites: {e}")

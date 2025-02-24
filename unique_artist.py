import json
import glob
import os

def unique_artist(folder_path):
    unique_artists = set()
    jsonl_files = glob.glob(f"{folder_path}/*.jsonl")

    for file_path in jsonl_files:
        print(f"Processing: {os.path.basename(file_path)}")

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "artist_url" in data and data["artist_url"]:
                        unique_artists.add(data["artist_url"])
                except json.JSONDecodeError:
                    continue

    total_unique_artists = len(unique_artists)
    print(f"\nTotal unique artists: {total_unique_artists}")
    return total_unique_artists

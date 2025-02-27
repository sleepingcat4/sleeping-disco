import os
import json
from collections import defaultdict

class MusicStats:
    def __init__(self, output_folder="statistics"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def process_files(self):
        genre_artists = defaultdict(set)
        featured_artists = set()
        yearly_stats = defaultdict(lambda: {"albums": set(), "artists": set(), "lyricists": set()})
        song_counts = {"songs_with_id": 0, "songs_with_lyrics": 0, "songs_with_genius_annotation": 0, "songs_with_qna": 0}
        languages = set()
        unique_songs = set()

        for letter in "abcdefghijklmnopqrstuvwxyz":
            file_path = f"{letter}.jsonl"
            if not os.path.exists(file_path):
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    song_url = data.get("song_url")
                    if song_url:
                        unique_songs.add(song_url)
                    tags = data.get("tags")
                    artist = data.get("primary_artist", "")
                    if isinstance(tags, list) and artist:
                        for tag in tags:
                            if isinstance(tag, str):
                                genre_artists[tag.strip()].add(artist.strip())
                    if isinstance(data.get("featured_artists"), list):
                        for fa in data["featured_artists"]:
                            if isinstance(fa, str):
                                featured_artists.add(fa.strip())
                    year = str(data.get("album_release_date", ""))[:4]
                    if year.isdigit():
                        yearly_stats[year]["albums"].add(data.get("album_name", ""))
                        yearly_stats[year]["artists"].add(data.get("artist_url", ""))
                        if isinstance(data.get("lyricists"), list):
                            for lyr in data["lyricists"]:
                                if isinstance(lyr, str):
                                    yearly_stats[year]["lyricists"].add(lyr.strip())
                    if data.get("song_id"):
                        song_counts["songs_with_id"] += 1
                    lyrics = data.get("lyrics")
                    if lyrics:
                        song_counts["songs_with_lyrics"] += 1
                    if data.get("genius_annotation"):
                        song_counts["songs_with_genius_annotation"] += 1
                    if data.get("qna"):
                        song_counts["songs_with_qna"] += 1
                    lang = data.get("language", "")
                    if isinstance(lang, str) and lang.strip():
                        languages.add(lang.strip())

        song_counts["songs_with_url"] = len(unique_songs)

        self._save_genre_artists(genre_artists)
        self._save_featured_artists(featured_artists)
        self._save_yearly_stats(yearly_stats)
        self._save_general_stats(song_counts, languages)
        self._save_languages(languages)

    def _save_genre_artists(self, genre_artists):
        with open(os.path.join(self.output_folder, "unique_genres.txt"), "w", encoding="utf-8") as f:
            f.writelines("\n".join(genre_artists.keys()))
        with open(os.path.join(self.output_folder, "genre_artist_count.txt"), "w", encoding="utf-8") as f:
            for genre, artists in genre_artists.items():
                f.write(f"{genre}: {len(artists)} unique artists\n")

    def _save_featured_artists(self, featured_artists):
        with open(os.path.join(self.output_folder, "featured_artists_count.txt"), "w", encoding="utf-8") as f:
            f.write(f"Unique Featured Artists: {len(featured_artists)}\n")

    def _save_yearly_stats(self, yearly_stats):
        with open(os.path.join(self.output_folder, "yearly_stats.txt"), "w", encoding="utf-8") as f:
            for year, stats in sorted(yearly_stats.items()):
                f.write(f"{year}: {len(stats['albums'])} albums, {len(stats['artists'])} unique artists, {len(stats['lyricists'])} lyricists\n")

    def _save_general_stats(self, song_counts, languages):
        with open(os.path.join(self.output_folder, "general_stats.txt"), "w", encoding="utf-8") as f:
            for key, count in song_counts.items():
                f.write(f"{key.replace('_', ' ').title()}: {count}\n")
            f.write(f"Unique Languages: {len(languages)}\n")

    def _save_languages(self, languages):
        with open(os.path.join(self.output_folder, "unique_languages.txt"), "w", encoding="utf-8") as f:
            f.writelines("\n".join(languages))

stats = MusicStats()
stats.process_files()

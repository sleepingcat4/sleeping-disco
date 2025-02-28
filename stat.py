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
        primary_artists = set()
        artist_urls = set()
        yearly_stats = defaultdict(lambda: {"albums": set(), "artists": set(), "lyricists": set()})
        song_counts = {"songs_with_id": 0, "songs_with_lyrics": 0, "songs_with_genius_annotation": 0, "songs_with_qna": 0}
        languages = set()
        unique_songs = set()
        unique_lyricists = set()

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
                    artist = data.get("primary_artist")
                    if isinstance(artist, str):
                        artist = artist.strip()
                        primary_artists.add(artist)
                    artist_url = data.get("artist_url")
                    if isinstance(artist_url, str):
                        artist_urls.add(artist_url.strip())
                    tags = data.get("tags")
                    if isinstance(tags, list) and artist:
                        for tag in tags:
                            if isinstance(tag, str):
                                genre_artists[tag.strip()].add(artist)
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
                                    lyricist = lyr.strip()
                                    yearly_stats[year]["lyricists"].add(lyricist)
                                    unique_lyricists.add(lyricist)
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
        self._save_primary_artists(primary_artists)
        self._save_artist_urls(artist_urls)
        self._save_yearly_stats(yearly_stats)
        self._save_general_stats(song_counts, languages)
        self._save_languages(languages)
        self._save_lyricists(unique_lyricists)

    def _save_genre_artists(self, genre_artists):
        with open(os.path.join(self.output_folder, "unique_genres.txt"), "w", encoding="utf-8") as f:
            f.writelines("\n".join(genre_artists.keys()))
        with open(os.path.join(self.output_folder, "genre_artist_count.txt"), "w", encoding="utf-8") as f:
            for genre, artists in genre_artists.items():
                f.write(f"{genre}: {len(artists)} unique artists\n")

    def _save_featured_artists(self, featured_artists):
        with open(os.path.join(self.output_folder, "featured_artists_count.txt"), "w", encoding="utf-8") as f:
            f.write(f"Unique Featured Artists: {len(featured_artists)}\n")

    def _save_primary_artists(self, primary_artists):
        with open(os.path.join(self.output_folder, "unique_primary_artists.txt"), "w", encoding="utf-8") as f:
            f.write(f"Unique Primary Artists: {len(primary_artists)}\n")

    def _save_artist_urls(self, artist_urls):
        with open(os.path.join(self.output_folder, "unique_artist_urls.txt"), "w", encoding="utf-8") as f:
            f.write(f"Unique Artist URLs: {len(artist_urls)}\n")

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

    def _save_lyricists(self, unique_lyricists):
        with open(os.path.join(self.output_folder, "unique_lyricists.txt"), "w", encoding="utf-8") as f:
            f.write(f"Unique Lyricists: {len(unique_lyricists)}\n")

stats = MusicStats()
stats.process_files()

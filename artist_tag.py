import pandas as pd
from collections import defaultdict

def genre_artists(df, output_file_unique="unique-art.csv", output_file_art_tag="art-tag.csv"):
    genre_artist_map = defaultdict(set)
    genre_count_map = defaultdict(int)
    
    for _, row in df.iterrows():
        primary = row["primary_artist"]
        genres = row["tag"]
        
        if pd.isna(genres) or not isinstance(genres, str):
            continue
        
        genre_list = genres.split(",")
        
        for genre in genre_list:
            genre_artist_map[genre.strip()].add(primary)
            genre_count_map[genre.strip()] += 1
    
    unique_artists_data = [(genre, len(artists)) for genre, artists in genre_artist_map.items()]
    art_tag_data = [(primary, genre) for genre, artists in genre_artist_map.items() for primary in artists]
    
    unique_artists_df = pd.DataFrame(unique_artists_data, columns=["genre", "num_artists"])
    art_tag_df = pd.DataFrame(art_tag_data, columns=["primary_artist", "genre"])
    
    unique_artists_df.to_csv(output_file_unique, index=False)
    art_tag_df.to_csv(output_file_art_tag, index=False)

df = pd.read_csv("/mnt/sdc/genius/verse-info.csv")
genre_artists(df)

import json
import glob
import os

def analyze_jsonl_files(folder_path, output_file):
    total_lyrics = 0
    total_youtube_links = 0
    total_artists = 0

    jsonl_files = glob.glob(f"{folder_path}/*.jsonl")

    with open(output_file, "w", encoding="utf-8") as out_f:
        for file_path in jsonl_files:
            file_lyrics = 0
            file_youtube_links = 0
            file_artists = 0

            file_name = os.path.basename(file_path)
            print(f"Processing: {file_name}")
            out_f.write(f"Processing: {file_name}\n")

            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        
                        if data.get("lyrics"):
                            file_lyrics += 1
                        
                        if data.get("youtube_links"):
                            if isinstance(data["youtube_links"], list) and data["youtube_links"]:
                                file_youtube_links += 1
                        
                        if data.get("artist_url"):
                            file_artists += 1
                    
                    except json.JSONDecodeError:
                        continue

            stats = (
                f"  - Rows with lyrics: {file_lyrics}\n"
                f"  - Rows with YouTube links: {file_youtube_links}\n"
                f"  - Artist entries: {file_artists}\n"
            )
            
            print(stats)
            out_f.write(stats + "\n")

            total_lyrics += file_lyrics
            total_youtube_links += file_youtube_links
            total_artists += file_artists

        final_stats = (
            "\nFinal Combined Statistics:\n"
            f"Total rows with lyrics: {total_lyrics}\n"
            f"Total rows with YouTube links: {total_youtube_links}\n"
            f"Total artist entries: {total_artists}\n"
        )

        print(final_stats)
        out_f.write(final_stats)

folder_path = "/sleeping"
output_file = "analysis_results.txt"
analyze_jsonl_files(folder_path, output_file)

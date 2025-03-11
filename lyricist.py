import json
import csv
import glob
import os

input_folder = "/mnt/sdc/genius/original"
output_folder = "/mnt/sdc/genius/statistics"

unique_lyricists = set()
unique_featured_artists = set()
youtube_link_count = 0

for file in glob.glob(f"{input_folder}/*.jsonl"):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            
            lyricists = data.get('lyricists')
            if lyricists:
                unique_lyricists.update(lyricists)
            
            featured_artists = data.get('featured_artists')
            if featured_artists:
                unique_featured_artists.update(featured_artists)
            
            youtube_links = data.get('youtube_links')
            if youtube_links:
                youtube_link_count += len(youtube_links)

os.makedirs(output_folder, exist_ok=True)

with open(f"{output_folder}/lyricist.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Lyricist"])
    for lyricist in sorted(unique_lyricists):
        writer.writerow([lyricist])

with open(f"{output_folder}/feature_artist.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Featured Artist"])
    for artist in sorted(unique_featured_artists):
        writer.writerow([artist])

print(f"Total unique lyricists found: {len(unique_lyricists)}")
print(f"Total unique featured artists found: {len(unique_featured_artists)}")
print(f"Total YouTube links found: {youtube_link_count}")

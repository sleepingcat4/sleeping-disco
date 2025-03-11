import json
import csv
import glob
import os
from collections import defaultdict

input_folder = "/mnt/sdc/genius/original"
output_folder = "/mnt/sdc/genius/statistics"

albums_by_year = defaultdict(list)
total_albums = 0

for file in glob.glob(f"{input_folder}/*.jsonl"):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            release_date = data.get('album_release_date')
            if release_date and release_date[:4].isdigit():
                year = int(release_date[:4])
                if 2010 <= year <= 2024:
                    albums_by_year[year].append({
                        "Album Name": data.get('album_name', 'N/A'),
                        "Album URL": data.get('album_url', 'N/A'),
                        "Release Date": release_date
                    })
                    total_albums += 1

os.makedirs(output_folder, exist_ok=True)

with open(f"{output_folder}/album.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Year", "Album Name", "Album URL", "Release Date"])
    for year, albums in sorted(albums_by_year.items()):
        for album in albums:
            writer.writerow([year, album["Album Name"], album["Album URL"], album["Release Date"]])

print(f"Total years covered: {len(albums_by_year)}")
print(f"Total albums released: {total_albums}")

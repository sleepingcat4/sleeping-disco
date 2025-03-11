import json
import csv
import glob
import os

input_folder = "/mnt/sdc/genius/original"
output_folder = "/mnt/sdc/genius/statistics"

unique_genres = set()

for file in glob.glob(f"{input_folder}/*.jsonl"):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if 'tags' in data:
                unique_genres.update(data['tags'])

os.makedirs(output_folder, exist_ok=True)

with open(f"{output_folder}/genre.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Genre"])
    for genre in sorted(unique_genres):
        writer.writerow([genre])

print(f"Total unique genres found: {len(unique_genres)}")

import json
import csv
import glob
import os
from collections import defaultdict

input_folder = "/mnt/sdc/genius/original"
output_folder = "/mnt/sdc/genius/statistics"

eu_languages = {
    "bg", "hr", "cs", "da", "nl", "en", "et", "fi", "fr", "de", "el", "hu", 
    "ga", "it", "lv", "lt", "mt", "pl", "pt", "ro", "sk", "sl", "es", "sv"
}

language_count = defaultdict(int)

for file in glob.glob(f"{input_folder}/*.jsonl"):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            language = data.get('language')
            if language in eu_languages:
                language_count[language] += 1

os.makedirs(output_folder, exist_ok=True)

with open(f"{output_folder}/eu_languages.csv", 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Language", "Count"])
    for lang, count in sorted(language_count.items()):
        writer.writerow([lang, count])

print(f"Total EU languages found: {len(language_count)}")
print(f"Total rows with EU languages: {sum(language_count.values())}")

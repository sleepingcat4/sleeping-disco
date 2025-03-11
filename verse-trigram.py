from nltk import ngrams
from nltk.tokenize import word_tokenize
import json
import os
import nltk
from tqdm import tqdm
from collections import Counter

nltk.download('punkt')

input_file = "/mnt/sdc/genius/verse/verse-clean.jsonl"
output_folder = "/mnt/sdc/genius/verse/trigram"
os.makedirs(output_folder, exist_ok=True)

batch_size = 100000
file_count = 1
lines_processed = 0
batch_data = []

with open(input_file, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()
    for line in tqdm(lines, desc="Processing", unit="line"):
        data = json.loads(line)
        lyrics = data.get("lyrics", "")
        song_id = data.get("song_id", "")

        tokens = word_tokenize(lyrics)
        trigram_counts = Counter(ngrams(tokens, 3))
        top_20_trigrams = trigram_counts.most_common(20)

        batch_data.append(json.dumps({"song_id": song_id, "trigrams": top_20_trigrams}))
        lines_processed += 1

        if lines_processed % batch_size == 0:
            output_file = os.path.join(output_folder, f"verse-tri-{file_count:05d}.jsonl")
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write("\n".join(batch_data) + "\n")
            batch_data = []
            file_count += 1

if batch_data:
    output_file = os.path.join(output_folder, f"verse-tri-{file_count:05d}.jsonl")
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(batch_data) + "\n")

print("Top 20 trigrams per song have been saved in batches of 100K.")

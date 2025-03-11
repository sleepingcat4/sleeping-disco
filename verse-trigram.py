from nltk import ngrams
from nltk.tokenize import word_tokenize
import json
import os
import nltk
from tqdm import tqdm
from collections import Counter

nltk.download('punkt')

input_file = "/mnt/sdc/genius/verse/verse-clean.jsonl"
output_file = "/mnt/sdc/genius/verse/verse-tri.jsonl"

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    lines = infile.readlines()
    for line in tqdm(lines, desc="Processing", unit="line"):
        data = json.loads(line)
        lyrics = data.get("lyrics", "")
        song_id = data.get("song_id", "")
        
        tokens = word_tokenize(lyrics)
        trigram_counts = Counter(ngrams(tokens, 3))
        top_20_trigrams = trigram_counts.most_common(20)

        result = {
            "song_id": song_id,
            "trigrams": top_20_trigrams
        }
        
        outfile.write(json.dumps(result) + "\n")

print("Top 20 trigrams per song have been saved to verse-tri.jsonl.")

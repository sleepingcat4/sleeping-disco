import json
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tqdm import tqdm
import nltk

nltk.download("punkt")
nltk.download("stopwords")

def build_bow():
    input_file = "verse-clean.jsonl"
    output_file = "bow-verse.jsonl"
    stop_words = set(stopwords.words("english"))

    total_lines = sum(1 for _ in open(input_file, "r", encoding="utf-8"))
    
    with open(input_file, "r", encoding="utf-8") as src, open(output_file, "w", encoding="utf-8") as dest:
        for line in tqdm(src, total=total_lines, desc="Processing lyrics", unit="line"):
            try:
                data = json.loads(line)
                song_id = data.get("song_id")
                lyrics = data.get("lyrics", "").strip()
                
                if song_id and lyrics:
                    tokens = [word.lower() for word in word_tokenize(lyrics) if word.lower() not in stop_words]
                    bow = dict(Counter(tokens))

                    output_data = {
                        "song_id": song_id,
                        "bag_of_words": bow
                    }

                    dest.write(json.dumps(output_data) + "\n")

            except json.JSONDecodeError:
                continue

    print(f"Bag of Words saved in {output_file}")

build_bow()

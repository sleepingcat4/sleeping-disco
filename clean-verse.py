import json
import re
import string

def clean_lyrics(lyrics):
    lyrics = re.sub(r"\[.*?\]", "", lyrics)
    lyrics = lyrics.translate(str.maketrans("", "", string.punctuation))
    lyrics = re.sub(r"\s+", " ", lyrics).strip()
    return lyrics

def clean_verse():
    input_file = "/mnt/sdc/verse.jsonl"
    output_file = "/mnt/sdc/verse-clean.jsonl"
    count = 0

    with open(input_file, "r", encoding="utf-8") as src, open(output_file, "w", encoding="utf-8") as dest:
        for line in src:
            try:
                data = json.loads(line)
                if "lyrics" in data:
                    data["lyrics"] = clean_lyrics(data["lyrics"])
                    count += 1
                dest.write(json.dumps(data) + "\n")
            except json.JSONDecodeError:
                continue

    print(f"Processed and saved {count} lyrics to {output_file}")

clean_verse()

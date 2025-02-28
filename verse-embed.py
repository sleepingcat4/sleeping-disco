from model2vec import StaticModel
import json
from tqdm import tqdm

model = StaticModel.from_pretrained("minishlab/M2V_multilingual_output")

def embed_verse():
    input_file = "verse-clean.jsonl"
    base_output_file = "verse"
    batch_size = 40
    max_rows_per_file = 5_000_000

    text_batch = []
    ids_batch = []
    file_count = 1
    row_count = 0
    total_saved = 0

    dest = open(f"{base_output_file}-{file_count:05d}.jsonl", "w", encoding="utf-8")

    with open(input_file, "r", encoding="utf-8") as src:
        total_lines = sum(1 for _ in open(input_file, "r", encoding="utf-8"))
        src.seek(0)

        for line in tqdm(src, total=total_lines, desc="Processing lyrics", unit="line"):
            try:
                data = json.loads(line)
                song_id = data.get("song_id")
                lyrics = data.get("lyrics")

                if song_id and lyrics:
                    text_batch.append(lyrics)
                    ids_batch.append(song_id)

                    if len(text_batch) == batch_size:
                        embeddings = model.encode(text_batch)
                        for song_id, embedding in zip(ids_batch, embeddings):
                            result = {
                                "song_id": song_id,
                                "embedding": embedding.tolist()
                            }
                            dest.write(json.dumps(result) + "\n")
                            row_count += 1
                            total_saved += 1

                        text_batch = []
                        ids_batch = []

                        if row_count >= max_rows_per_file:
                            dest.close()
                            file_count += 1
                            row_count = 0
                            dest = open(f"{base_output_file}-{file_count:05d}.jsonl", "w", encoding="utf-8")

            except json.JSONDecodeError:
                continue

        if text_batch:
            embeddings = model.encode(text_batch)
            for song_id, embedding in zip(ids_batch, embeddings):
                result = {
                    "song_id": song_id,
                    "embedding": embedding.tolist()
                }
                dest.write(json.dumps(result) + "\n")
                total_saved += 1

    dest.close()
    print(f"Embeddings saved in {file_count} file(s), Total Rows Saved: {total_saved}")

embed_verse()

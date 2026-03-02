from pathlib import Path
from collections import defaultdict
import json


def build_inverted_index(lemmas_folder):
    inverted_index = defaultdict(set)

    for file in Path(lemmas_folder).glob("*_lemmas.txt"):
        doc_id = file.stem.replace("_lemmas", "")

        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                lemma = parts[0].lower()
                inverted_index[lemma].add(doc_id)

    return inverted_index


def save_index(index, output_file):
    serializable_index = {k: list(v) for k, v in index.items()}
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(serializable_index, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    index = build_inverted_index("lemmas")
    save_index(index, "inverted_index.json")
    print("Индекс построен и сохранён в inverted_index.json")
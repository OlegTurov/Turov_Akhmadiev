import os
import math
from collections import defaultdict, Counter

TOKENS_DIR = "tokens"
LEMMAS_DIR = "lemmas"
OUTPUT_DIR = "tfidf"

os.makedirs(OUTPUT_DIR, exist_ok=True)

lemma_docs = {}
lemma_df = defaultdict(int)

print("Загрузка и преобразование в леммы...")

files = sorted(os.listdir(TOKENS_DIR))
N = len(files)

for fname in files:
    base_name = fname.rsplit("_tokens.txt", 1)[0]
    lemma_fname = f"{base_name}_lemmas.txt"

    token_path = os.path.join(TOKENS_DIR, fname)
    lemma_path = os.path.join(LEMMAS_DIR, lemma_fname)

    # --- читаем соответствие form → lemma ---
    form_to_lemma = {}

    with open(lemma_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                lemma = parts[0]
                for form in parts[1:]:
                    form_to_lemma[form] = lemma

    # --- читаем токены и сразу переводим в леммы ---
    lemmas = []

    with open(token_path, encoding="utf-8") as f:
        for line in f:
            tok = line.strip()
            if not tok:
                continue

            lemma = form_to_lemma.get(tok)
            if lemma:
                lemmas.append(lemma)

    counts = Counter(lemmas)
    total = len(lemmas)

    lemma_docs[fname] = (counts, total)

    for lemma in counts.keys():
        lemma_df[lemma] += 1

print("Леммы собраны")

# --- TF-IDF ---
print("Считаем TF-IDF...")

for fname, (counts, total) in lemma_docs.items():
    out_path = os.path.join(OUTPUT_DIR, f"{fname}_lemmas.txt")

    with open(out_path, "w", encoding="utf-8") as f_out:
        for lemma, count in counts.items():
            tf = count / total if total > 0 else 0
            df = lemma_df[lemma]

            idf = math.log((N + 1) / (df + 1)) + 1
            tfidf = tf * idf

            f_out.write(f"{lemma} {idf:.6f} {tfidf:.6f}\n")

print("Готово")
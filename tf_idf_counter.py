import os
import math
from collections import defaultdict
from collections import Counter

TOKENS_DIR = "tokens"
LEMMAS_DIR = "lemmas"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

token_docs = {}
lemma_docs = {}
token_df = defaultdict(int)
lemma_df = defaultdict(int)

print("Папки загружены. Подготовлены структуры для TF-IDF")


all_tokens_set = set()
token_files = sorted(os.listdir(TOKENS_DIR))
N = len(token_files)

for fname in token_files:
    path = os.path.join(TOKENS_DIR, fname)
    with open(path, encoding="utf-8") as f:
        tokens = [line.strip() for line in f if line.strip()]
    counts = Counter(tokens)
    token_docs[fname] = (counts, len(tokens))
    all_tokens_set.update(tokens)
    for term in set(tokens):
        token_df[term] += 1

tokens_list = sorted(all_tokens_set)
print("TF и DF для токенов подсчитаны для всех документов. Всего терминов:", len(tokens_list))


for fname, (counts, total_tokens) in token_docs.items():
    out_path = os.path.join(OUTPUT_DIR, f"{fname}_terms.txt")
    with open(out_path, "w", encoding="utf-8") as f_out:
        for term in tokens_list:
            tf = counts.get(term, 0) / total_tokens if total_tokens > 0 else 0
            df = token_df.get(term, 0)
            idf = math.log(N / (1 + df))
            tfidf = tf * idf
            f_out.write(f"{term} {idf:.6f} {tfidf:.6f}\n")

print("TF-IDF для токенов вычислен и сохранен")
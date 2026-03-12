import os
import math
from collections import defaultdict, Counter

TOKENS_DIR = "tokens"
LEMMAS_DIR = "lemmas"
OUTPUT_DIR = "tfidf"

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

lemmas_dict = {}

for fname in sorted(os.listdir(LEMMAS_DIR)):
    path = os.path.join(LEMMAS_DIR, fname)
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                lemma = parts[0]
                forms = set(parts[1:])
                lemmas_dict[lemma] = forms

for fname in sorted(os.listdir(LEMMAS_DIR)):
    path = os.path.join(LEMMAS_DIR, fname)
    with open(path, encoding="utf-8") as f:
        tokens = []
        for line in f:
            tokens.extend(line.strip().split())
    counts = Counter(tokens)
    total_tokens = len(tokens)
    lemma_docs[fname] = (counts, total_tokens)

for lemma, forms in lemmas_dict.items():
    lemma_df[lemma] = 0

for fname, (counts, total_tokens) in lemma_docs.items():
    for lemma, forms in lemmas_dict.items():
        if any(form in counts for form in forms):
            lemma_df[lemma] += 1

for fname, (counts, total_tokens) in lemma_docs.items():
    out_path = os.path.join(OUTPUT_DIR, f"{fname}_lemmas.txt")
    with open(out_path, "w", encoding="utf-8") as f_out:
        for lemma, forms in lemmas_dict.items():
            term_count = sum(counts.get(form, 0) for form in forms)
            tf = term_count / total_tokens if total_tokens > 0 else 0
            df = lemma_df.get(lemma, 0)
            idf = math.log(1 + N / (1 + df))
            tfidf = tf * idf
            f_out.write(f"{lemma} {idf:.6f} {tfidf:.6f}\n")

print("TF-IDF для лемм вычислен и сохранен")
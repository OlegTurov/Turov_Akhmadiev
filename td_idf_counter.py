import os
from collections import defaultdict

TOKENS_DIR = "tokens"
LEMMAS_DIR = "lemmas"
OUTPUT_DIR = "output"
TOKENS_LIST_FILE = "tokens_list.txt"
LEMMAS_LIST_FILE = "lemmas_list.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(TOKENS_LIST_FILE, encoding="utf-8") as f:
    tokens_list = [line.strip() for line in f if line.strip()]

lemmas_dict = {}
with open(LEMMAS_LIST_FILE, encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            lemma = parts[0]
            forms = set(parts[1:])
            lemmas_dict[lemma] = forms

token_docs = {}
lemma_docs = {}
token_df = defaultdict(int)
lemma_df = defaultdict(int)

print("Данные загружены. Количество терминов:", len(tokens_list))
print("Количество лемм:", len(lemmas_dict))
import os
from collections import defaultdict

TOKENS_DIR = "tokens"
LEMMAS_DIR = "lemmas"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

token_docs = {}
lemma_docs = {}
token_df = defaultdict(int)
lemma_df = defaultdict(int)

print("Папки загружены. Подготовлены структуры для TF-IDF")
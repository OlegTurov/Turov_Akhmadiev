import os
import re
import math
import nltk
from collections import defaultdict, Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy3

LEMMAS_DIR = "lemmas"
MIN_SCORE = 0.5

nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)

russian_stopwords = set(stopwords.words('russian'))
morph = pymorphy3.MorphAnalyzer()


def load_corpus():
    lemma_files = sorted(os.listdir(LEMMAS_DIR))
    N = len(lemma_files)

    doc_vectors = {}
    lemma_df = defaultdict(int)
    all_lemmas = set()

    doc_lemma_counts = {}

    for fname in lemma_files:
        doc_id = fname.replace("_lemmas.txt", "")
        path = os.path.join(LEMMAS_DIR, fname)
        lemma_list = []

        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    lemma = parts[0]
                    lemma_list.append(lemma)
                    all_lemmas.add(lemma)

        counts = Counter(lemma_list)
        doc_lemma_counts[doc_id] = (counts, len(lemma_list))

        for lemma in set(lemma_list):
            lemma_df[lemma] += 1

    for doc_id, (counts, total) in doc_lemma_counts.items():
        vector = {}
        for lemma, count in counts.items():
            tf = count / total if total > 0 else 0
            idf = math.log(1 + N / (1 + lemma_df.get(lemma, 0)))
            vector[lemma] = tf * idf
        doc_vectors[doc_id] = vector

    return doc_vectors, lemma_df, N


def lemmatize_query(query):
    query = query.lower()
    query = re.sub(r"[^\w\s\-]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()

    raw_tokens = word_tokenize(query, language="russian")
    lemmas = []

    for tok in raw_tokens:
        tok = tok.strip()
        if tok in russian_stopwords:
            continue
        if not re.fullmatch(r'[а-яё]+', tok):
            continue
        parse = morph.parse(tok)[0]
        if parse.score < MIN_SCORE:
            continue
        lemmas.append(parse.normal_form)

    return lemmas


def build_query_vector(query_lemmas, lemma_df, N):
    counts = Counter(query_lemmas)
    total = len(query_lemmas)
    vector = {}

    for lemma, count in counts.items():
        tf = count / total if total > 0 else 0
        idf = math.log(1 + N / (1 + lemma_df.get(lemma, 0)))
        vector[lemma] = tf * idf

    return vector


def cosine_similarity(vec_a, vec_b):
    common_keys = set(vec_a.keys()) & set(vec_b.keys())
    if not common_keys:
        return 0.0

    dot = sum(vec_a[k] * vec_b[k] for k in common_keys)
    norm_a = math.sqrt(sum(v ** 2 for v in vec_a.values()))
    norm_b = math.sqrt(sum(v ** 2 for v in vec_b.values()))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def search(query, doc_vectors, lemma_df, N, top_n=10):
    query_lemmas = lemmatize_query(query)

    if not query_lemmas:
        return []

    query_vector = build_query_vector(query_lemmas, lemma_df, N)

    results = []
    for doc_id, doc_vector in doc_vectors.items():
        score = cosine_similarity(query_vector, doc_vector)
        if score > 0:
            results.append((doc_id, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


if __name__ == "__main__":
    print("Загрузка корпуса...")
    doc_vectors, lemma_df, N = load_corpus()
    print(f"Загружено {N} документов. Готов к поиску.\n")

    while True:
        query = input("Введите поисковый запрос (exit для выхода): ")
        if query.strip().lower() == "exit":
            break

        results = search(query, doc_vectors, lemma_df, N)

        if results:
            print(f"\nНайдено {len(results)} документов:")
            for i, (doc_id, score) in enumerate(results, 1):
                print(f"  {i}. {doc_id} (score: {score:.6f})")
        else:
            print("Документы не найдены.")
        print()

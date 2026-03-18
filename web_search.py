from flask import Flask, render_template, request
from vector_search import load_corpus, search

app = Flask(__name__)

print("Загрузка корпуса...")
doc_vectors, lemma_df, N = load_corpus()
print(f"Загружено {N} документов.")

BASE_URL = "https://elementy.ru/{}"


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    results = []

    if query:
        raw_results = search(query, doc_vectors, lemma_df, N, top_n=10)
        rank = 1
        for doc_id, score in raw_results:
            article_id = doc_id.replace("novosti_nauki_", "").replace("_tokens.txt", "")
            doc_id_clean = article_id.replace("_lemmas.txt", "")

            if doc_id_clean.find("434196") != -1:
                continue

            results.append({
                "rank": rank,
                "doc_id": doc_id_clean,
                "score": round(1.0 - score, 6),
                "url": BASE_URL.format(article_id),
            })
            rank += 1

    return render_template("index.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

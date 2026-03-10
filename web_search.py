from flask import Flask, render_template, request
from vector_search import load_corpus, search

app = Flask(__name__)

print("Загрузка корпуса...")
doc_vectors, lemma_df, N = load_corpus()
print(f"Загружено {N} документов.")

BASE_URL = "https://elementy.ru/novosti_nauki/{}"


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    results = []

    if query:
        raw_results = search(query, doc_vectors, lemma_df, N, top_n=10)
        for rank, (doc_id, score) in enumerate(raw_results, 1):
            article_id = doc_id.replace("novosti_nauki_", "")
            results.append({
                "rank": rank,
                "doc_id": doc_id,
                "score": round(score, 6),
                "url": BASE_URL.format(article_id),
            })

    return render_template("index.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

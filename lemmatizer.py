import re
import nltk
import html
from pathlib import Path
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy2
from collections import defaultdict

input_folder = Path("downloads")
tokens_folder = Path("tokens")
lemmas_folder = Path("lemmas")

tokens_folder.mkdir(exist_ok=True)
lemmas_folder.mkdir(exist_ok=True)

nltk.download('punkt')
nltk.download('stopwords')

russian_stopwords = set(stopwords.words('russian'))
morph = pymorphy2.MorphAnalyzer()

MIN_SCORE = 0.5


def clean_text(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(" ")
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"[^\w\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def process_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()

    text = clean_text(raw)
    raw_tokens = word_tokenize(text, language="russian")

    tokens = set()

    for tok in raw_tokens:
        tok = tok.strip()

        if tok in russian_stopwords:
            continue

        if not re.fullmatch(r'[а-яё]+', tok):
            continue

        parse = morph.parse(tok)[0]
        if parse.score < MIN_SCORE:
            continue

        tokens.add(tok)

    tokens_file = tokens_folder / f"{file_path.stem}_tokens.txt"

    with open(tokens_file, "w", encoding="utf-8") as f:
        for t in sorted(tokens):
            f.write(t + "\n")

    lemma_dict = defaultdict(list)

    for tok in tokens:
        parse = morph.parse(tok)[0]
        lemma = parse.normal_form
        lemma_dict[lemma].append(tok)

    lemmas_file = lemmas_folder / f"{file_path.stem}_lemmas.txt"

    with open(lemmas_file, "w", encoding="utf-8") as f:
        for lemma, tok_list in sorted(lemma_dict.items()):
            f.write(f"{lemma} {' '.join(sorted(tok_list))}\n")


for file_path in input_folder.glob("*.txt"):
    print(f"Обрабатывается: {file_path.name}")
    process_file(file_path)

print("Готово! Результаты лежат в папках tokens/ и lemmas/")
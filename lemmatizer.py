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
tokens_file = "tokens.txt"
lemmas_file = "lemmas.txt"

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

all_text = ""
for file_path in input_folder.glob("*.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()
        all_text += clean_text(raw) + " "

raw_tokens = word_tokenize(all_text, language="russian")
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

with open(tokens_file, "w", encoding="utf-8") as f:
    for t in sorted(tokens):
        f.write(t + "\n")

lemma_dict = defaultdict(list)
for tok in tokens:
    parse = morph.parse(tok)[0]
    lemma = parse.normal_form
    lemma_dict[lemma].append(tok)

with open(lemmas_file, "w", encoding="utf-8") as f:
    for lemma, tok_list in sorted(lemma_dict.items()):
        f.write(f"{lemma} {' '.join(sorted(tok_list))}\n")

print("Готово! Файлы tokens.txt и lemmas.txt созданы.")

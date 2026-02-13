import requests
from urllib.parse import urlparse
from pathlib import Path

Path("downloads").mkdir(exist_ok=True)

with open("index.txt", "r", encoding="utf-8") as file:
    links = file.readlines()

for url in links:
    url = url.strip()
    url = url.split(" ")[1]
    if not url:
        continue

    print(f"Загружаем: {url}")

    try:
        response = requests.get(url, timeout=20)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        continue

    if response.status_code != 200:
        print(f"Ошибка с кодом {response.status_code}")
        continue

    text_content = response.text

    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "_")
    query = parsed.query.replace("=", "_").replace("&", "_")

    file_name = path if path else "index"

    if query:
        file_name += f"_{query}"

    file_name += ".txt"

    file_path = Path("downloads") / file_name

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text_content)

    print(f"Сохранено: {file_path}")

print("Скачивание завершено.")

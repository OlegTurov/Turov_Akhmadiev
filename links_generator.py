base_url = "https://elementy.ru/novosti_nauki/{}"

all_links = []

for article in range(434105, 434205, 1):
    url = base_url.format(article)
    all_links.append(url)

with open("index.txt", "w", encoding="utf-8") as file:
    counter = 0
    for link in all_links:
        file.write(str(counter) + " " + link + "\n")
        counter += 1

print(f"Сохранено {len(all_links)} ссылок.")

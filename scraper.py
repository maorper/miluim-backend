# scraper.py
import requests, json
from bs4 import BeautifulSoup

BASE_URL = "https://www.miluim.idf.il"
PAGES = ["/", "/info", "/rights"]  # דוגמה

data = []

for page in PAGES:
    res = requests.get(BASE_URL + page)
    soup = BeautifulSoup(res.text, "html.parser")
    texts = [el.get_text(strip=True) for el in soup.select("h1,h2,h3,p,li")]
    for t in texts:
        data.append({"source": page, "content": t})

with open("miluim_site_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

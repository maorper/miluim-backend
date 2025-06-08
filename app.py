from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import json
import os
import tempfile

app = Flask(__name__)
CORS(app)

# אוגרים כאן את כל הטקסטים
documents = []

# קריאה מהאתר
def scrape_site():
    print("📡 סורק את אתר המילואים...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    visited = set()
    to_visit = ["https://www.miluim.idf.il"]

    while to_visit:
        url = to_visit.pop(0)
        if url in visited or not url.startswith("https://www.miluim.idf.il"):
            continue

        visited.add(url)
        try:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            documents.append({"source": url, "text": text})

            for link in soup.find_all("a", href=True):
                href = link['href']
                if href.startswith("/"):
                    full_url = "https://www.miluim.idf.il" + href
                    to_visit.append(full_url)
        except Exception as e:
            print("שגיאה בכתובת:", url, e)

    driver.quit()
    print("✅ הסתיימה הסריקה.")

# קריאה מקבצי PDF
def extract_pdf_text(file_path):
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print("שגיאת PDF:", e)
    return text

# סריקה מהאתר (רק פעם אחת כשמתחילים)
scrape_site()

@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "לא התקבל קובץ"}), 400

    temp_path = tempfile.mktemp(suffix=".pdf")
    file.save(temp_path)
    text = extract_pdf_text(temp_path)
    documents.append({"source": file.filename, "text": text})
    os.remove(temp_path)
    return jsonify({"message": "הקובץ נוסף למערכת בהצלחה ✅"})

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("question", "").lower()

    if not query:
        return jsonify({"answer": "לא הוזנה שאלה"}), 400

    for doc in documents:
        if query in doc["text"].lower():
            snippet = doc["text"][:800]
            return jsonify({
                "answer": snippet,
                "source": doc["source"]
            })

    return jsonify({"answer": "לא נמצאה תשובה במסמכים."})

if __name__ == "__main__":
    app.run(debug=True)

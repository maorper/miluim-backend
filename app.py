from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# טוען את קובץ המידע מהסריקה האחרונה (אם קיים)
DATA_PATH = "miluim_site_data.json"

def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

data = load_data()

@app.route("/")
def home():
    return "מרכז ידע לקצינים – API פעיל ✅"

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "").strip()
    if not question:
        return jsonify({"error": "שאלה חסרה"}), 400

    # 🔍 כאן לדוגמה נשלוף תשובה פשוטה מהקובץ
    for item in data:
        if question in item.get("question", ""):
            return jsonify({"answer": item["answer"]})
    
    return jsonify({"answer": "מצטער, לא מצאתי תשובה במידע הנוכחי."})

# 🟢 פקודת הרצה ל-Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

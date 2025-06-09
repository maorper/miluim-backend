# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

with open("miluim_site_data.json", encoding="utf-8") as f:
    data = json.load(f)

@app.route("/search", methods=["POST"])
def search():
    query = request.json.get("question", "").lower()
    matches = [d for d in data if query in d["content"].lower()]
    return jsonify({"answers": matches[:5]})

import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
from categorize import categorize_transactions

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/categorize", methods=["POST"])
def api_categorize():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV: {e}"}), 400

    required_cols = {"Date", "Description", "Amount"}
    if not required_cols.issubset(df.columns):
        return jsonify({
            "error": "CSV must contain columns: Date, Description, Amount"
        }), 400

    transactions = df[["Date", "Description", "Amount"]].to_dict(orient="records")

    try:
        categorized, summary = categorize_transactions(transactions)
    except Exception as e:
        return jsonify({"error": f"AI categorization failed: {e}"}), 500

    return jsonify({
        "transactions": categorized,
        "summary": summary
    })

if __name__ == "__main__":
    app.run(debug=True)
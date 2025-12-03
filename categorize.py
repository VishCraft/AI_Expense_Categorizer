import os
import json
from collections import defaultdict
from typing import List, Dict, Tuple

import openai
from dotenv import load_dotenv

# Load variables from .env file (if present)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Please create a .env file with OPENAI_API_KEY=your_key.")

client = openai.OpenAI(api_key=api_key)

CATEGORIES = [
    "Groceries",
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Rent",
    "Bills & Utilities",
    "Entertainment",
    "Health & Fitness",
    "Travel",
    "Subscriptions",
    "Other"
]

SYSTEM_PROMPT = """
You are an assistant that categorizes personal finance transactions.

You will receive a JSON array of transactions. Each transaction has:
- Date (string)
- Description (string)
- Amount (number, positive for expense, negative for income if present)

For each transaction, assign:
- category: one of: {categories}
- confidence: number between 0 and 1
Return ONLY valid JSON in this format:
{{
  "transactions": [
    {{
      "Date": "...",
      "Description": "...",
      "Amount": ...,
      "Category": "...",
      "Confidence": 0.95
    }},
    ...
  ]
}}
""".format(categories=", ".join(CATEGORIES))

def call_openai_for_categorization(transactions: List[Dict]) -> List[Dict]:
    user_content = {
        "transactions": [
            {
                "Date": t["Date"],
                "Description": t["Description"],
                "Amount": t["Amount"],
            }
            for t in transactions
        ]
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(user_content)}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse AI response as JSON: {e}\nRaw content: {content}")

    return parsed.get("transactions", [])


def build_summary(categorized: List[Dict]) -> Dict:
    totals = defaultdict(float)
    overall_total = 0.0

    for t in categorized:
        cat = t.get("Category", "Other")
        amount = float(t.get("Amount", 0) or 0)
        totals[cat] += amount
        overall_total += amount

    if overall_total <= 0:
        headline = "No expenses detected."
    else:
        top_cat = max(totals.items(), key=lambda x: x[1])[0]
        headline = f"Your highest spending category is {top_cat}."

    summary = {
        "total_spent": round(overall_total, 2),
        "by_category": {k: round(v, 2) for k, v in totals.items()},
        "headline": headline,
    }

    return summary


def categorize_transactions(transactions: List[Dict]) -> Tuple[List[Dict], Dict]:
    categorized = call_openai_for_categorization(transactions)
    summary = build_summary(categorized)
    return categorized, summary
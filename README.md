# AI Expense Categorizer 

A polished AI-powered web app that categorizes your expenses from a CSV file and generates spending insights, with a glassmorphism dashboard UI and charts.

## Features

- Drag-and-drop CSV upload
- Columns required: `Date`, `Description`, `Amount`
- Uses OpenAI (gpt-4o-mini) to:
  - Assign a category to each transaction
  - Provide a confidence score
  - Summarize total spend and spend by category
- Glass-style UI:
  - Frosted, blurred cards
  - Dark gradient background
  - Highlighted summary panel
- Visualizations:
  - Bar chart: spend by category
  - Pie chart: spend breakdown
- Configuration via `.env` (no need to export env vars manually)

## Tech Stack

- Python, Flask
- Pandas
- OpenAI API
- python-dotenv
- Vanilla HTML, CSS, JS
- Chart.js (via CDN)

## Setup (Local)

1. **Create `.env` file**

In the project root, create a file named `.env`:

```text
OPENAI_API_KEY=sk-your-key-here
```

> ⚠️ Never commit this file to GitHub. It is already ignored via `.gitignore`.

2. **Create virtual environment (optional, recommended)**

```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows
venv\Scripts\Activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
python app.py
```

5. **Open in browser**

Visit:

```text
http://127.0.0.1:5000
```

6. **Test with sample CSV**

Use the included file:

```text
sample_data/sample_expenses.csv
```

Drag & drop into the upload area, click **Analyze with AI**, and you will see:

- Categorized transactions table
- Headline + total spent
- Per-category spend listing
- Bar + pie charts in a glassmorphism dashboard


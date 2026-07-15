from pathlib import Path
import json

import pandas as pd
from google import genai

from ai.prompts import NEWS_PROMPT
from utils.config import GEMINI_API_KEY

# ==========================================================
# Configuration
# ==========================================================

client = genai.Client(api_key=GEMINI_API_KEY)

INPUT_FILE = Path("data/external/news/shipping_news.csv")
OUTPUT_FILE = Path("data/processed/news_risk_scores.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Load News
# ==========================================================

df = pd.read_csv(INPUT_FILE)

# Change these if your CSV has different column names
DATE_COLUMN = "seendate"
TITLE_COLUMN = "title"

df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN]).dt.date

daily_news = df.groupby(DATE_COLUMN)


# ==========================================================
# Analyze
# ==========================================================
# ==========================================================
# Analyze
# ==========================================================

results = []

for date, group in daily_news:

    print(f"Analyzing {date}")

    articles = ""

    MAX_ARTICLES = 5

    for i, row in enumerate(group.head(MAX_ARTICLES).itertuples(), start=1):
        articles += f"{i}. {getattr(row, TITLE_COLUMN)}\n\n"

    prompt = NEWS_PROMPT.replace("{articles}", articles)

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if Gemini returns it
        if text.startswith("```"):
            text = (
                text.replace("```json", "")
                    .replace("```", "")
                    .strip()
            )

        risk = json.loads(text)

        risk["date"] = str(date)

        results.append(risk)

        print("✓ Success")

    except Exception as e:

        print(f"\n✗ Failed on {date}")
        print(type(e).__name__)
        print(e)

        raise

    import time

for attempt in range(5):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(10)
else:
    raise RuntimeError("Failed after 5 retries")
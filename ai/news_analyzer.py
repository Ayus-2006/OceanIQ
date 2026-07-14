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
results = []

for date, group in daily_news:

    print(f"Analyzing {date}")

    articles = ""

    for i, row in enumerate(group.itertuples(), start=1):
        articles += f"{i}. {getattr(row, TITLE_COLUMN)}\n\n"

    prompt = NEWS_PROMPT.replace("{articles}", articles)

    try:

        response = client.models.generate_content(
            model="gemini-2.5-pro",
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

        print(f"✗ Failed on {date}")
        print(e)

        continue

# ==========================================================
# Save
# ==========================================================

risk_df = pd.DataFrame(results)

risk_df.to_csv(OUTPUT_FILE, index=False)

print("Done!")
print(f"Saved {len(risk_df)} daily risk scores.")
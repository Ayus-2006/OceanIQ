from pathlib import Path
import json
import re
import time

import pandas as pd
from ollama import chat

from ai.prompts import NEWS_PROMPT


# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = Path("data/external/news/shipping_news.csv")
OUTPUT_FILE = Path("data/processed/news_risk_scores.csv")

MODEL = "qwen3:8b"

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================================
# Load News
# ==========================================================

print("Loading news...")

df = pd.read_csv(INPUT_FILE)

DATE_COLUMN = "seendate"
TITLE_COLUMN = "title"

df[DATE_COLUMN] = pd.to_datetime(
    df[DATE_COLUMN]
).dt.date

daily_news = df.groupby(DATE_COLUMN)


# ==========================================================
# JSON Cleaner
# ==========================================================

def clean_json(text):

    text = (
        text.replace("```json", "")
            .replace("```", "")
            .strip()
    )

    # remove <think>...</think> blocks if present
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL
    )

    # extract first JSON object
    match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL
    )

    if match:
        return match.group(0)

    return text


# ==========================================================
# Analyze
# ==========================================================

results = []

for date, group in daily_news:

    print(f"\nAnalyzing {date}")

    articles = ""

    for i, row in enumerate(
        group.head(5).itertuples(),
        start=1
    ):

        articles += (
            f"{i}. "
            f"{getattr(row, TITLE_COLUMN)}\n\n"
        )

    prompt = NEWS_PROMPT.replace(
        "{articles}",
        articles
    )

    success = False

    for attempt in range(3):

        try:

            response = chat(

                model=MODEL,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                options={
                    "temperature": 0
                }

            )

            text = response["message"]["content"]

            text = clean_json(text)

            risk = json.loads(text)

            risk["date"] = str(date)

            results.append(risk)

            print("✓ Success")

            success = True

            break

        except Exception as e:

            print(
                f"Attempt {attempt+1} failed"
            )

            print(e)

            time.sleep(2)

    if not success:

        print(
            f"Skipping {date}"
        )


# ==========================================================
# Save
# ==========================================================

output = pd.DataFrame(results)

output.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n" + "="*60)
print("News analysis complete")
print(f"Saved to: {OUTPUT_FILE}")
print(f"Rows: {len(output)}")
print("="*60)
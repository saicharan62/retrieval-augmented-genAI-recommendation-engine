"""
export_predictions.py

Generates CSV predictions in SHL-required LONG format:
Query | Assessment_url
"""

import pandas as pd
from scripts.recommend import SHLRecommender

INPUT_PATH = "data/Gen_AI Dataset.xlsx"
SHEET_NAME = "Test-Set"
OUTPUT_PATH = "data/predictions.csv"

TOP_K = 10


def main():
    print("Loading test dataset...")
    df = pd.read_excel(INPUT_PATH, sheet_name=SHEET_NAME)

    print(f"Total queries: {len(df)}")

    recommender = SHLRecommender(top_k=TOP_K)

    rows = []

    for _, row in df.iterrows():
        query = row["Query"]

        recommendations = recommender.recommend(query)

        for rec in recommendations:
            rows.append({
                "Query": query,
                "Assessment_url": rec["url"]
            })

    output_df = pd.DataFrame(rows)

    output_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved predictions to {OUTPUT_PATH}")
    print(f"Total rows written: {len(output_df)}")


if __name__ == "__main__":
    main()

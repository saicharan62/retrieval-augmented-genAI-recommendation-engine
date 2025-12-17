"""
evaluate_recall.py

Evaluates Recall@10 for the SHL assessment recommender
using self-supervised evaluation.
"""

import pandas as pd
from recommend import SHLRecommender


CATALOG_PATH = "data/shl_catalog.csv"
TOP_K = 10


def main():
    print("Loading catalog...")
    df = pd.read_csv(CATALOG_PATH)

    recommender = SHLRecommender(top_k=TOP_K)

    hits = 0
    total = len(df)

    print(f"Evaluating Recall@{TOP_K} on {total} items...\n")

    for _, row in df.iterrows():
        query = row["name"]
        expected_url = row["url"]

        recommendations = recommender.recommend(query)

        recommended_urls = {r["url"] for r in recommendations}

        if expected_url in recommended_urls:
            hits += 1

    recall = hits / total

    print("Evaluation complete")
    print(f"Recall@{TOP_K}: {recall:.4f}")
    print(f"Hits: {hits} / {total}")


if __name__ == "__main__":
    main()

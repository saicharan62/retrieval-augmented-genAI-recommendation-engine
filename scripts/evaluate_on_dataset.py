"""
evaluate_on_dataset.py

Evaluates Recall@10 using provided train/test XLSX files
by matching assessment NAMES (robust to URL format issues).
"""

import pandas as pd
from recommend import SHLRecommender


TOP_K = 10


def normalize_name(text):
    return str(text).strip().lower()


def extract_expected_names(cell):
    """
    Extracts expected assessment names from a cell.
    Handles comma or newline separated values.
    """
    if pd.isna(cell):
        return set()

    text = str(cell)
    parts = [p.strip() for p in text.replace("\n", ",").split(",")]
    return {normalize_name(p) for p in parts if p}


def evaluate(xlsx_path):
    print(f"\nEvaluating on {xlsx_path}")

    df = pd.read_excel(xlsx_path)
    recommender = SHLRecommender(top_k=TOP_K)

    hits = 0
    total = len(df)

    for _, row in df.iterrows():
        query = row["Query"]
        expected_names = extract_expected_names(row["Assessment_url"])

        recommendations = recommender.recommend(query)
        recommended_names = {
            normalize_name(r["name"]) for r in recommendations
        }

        if expected_names & recommended_names:
            hits += 1

    recall = hits / total if total else 0.0

    print(f"Recall@{TOP_K}: {recall:.4f}")
    print(f"Hits: {hits} / {total}")

    return recall


if __name__ == "__main__":
    evaluate("data/train.xlsx")
    evaluate("data/test.xlsx")

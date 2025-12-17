"""
evaluate_filtered_recall.py

Computes Recall@10 ONLY on valid Individual Test Solutions
from the TRAIN sheet of the provided dataset.
"""

print(">>> RUNNING evaluate_filtered_recall.py (FILTERED VERSION)")

import pandas as pd
from recommend import SHLRecommender
from urllib.parse import urlparse

TOP_K = 10
DATASET_PATH = "data/Gen_AI Dataset.xlsx"
TRAIN_SHEET = "Train-Set"


def is_individual_test(url: str) -> bool:
    """
    STRICT check using URL path (not substring matching).
    """
    if not isinstance(url, str):
        return False

    path = urlparse(url).path
    return path.startswith("/products/product-catalog/view/")


def normalize(text: str) -> str:
    return text.strip().lower()


def extract_name_from_url(url: str) -> str:
    """
    Extracts assessment name from URL slug.
    """
    slug = url.rstrip("/").split("/")[-1]
    return normalize(slug.replace("-", " "))


def main():
    print("Loading TRAIN dataset...")
    df = pd.read_excel(DATASET_PATH, sheet_name=TRAIN_SHEET)

    print(f"Total rows in Train-Set: {len(df)}")

    # ---- DEBUG: check filter behavior ----
    mask = df["Assessment_url"].apply(is_individual_test)
    print("Filter TRUE count:", mask.sum())
    print("Filter FALSE count:", (~mask).sum())

    # ---- APPLY FILTER ----
    df = df[mask]

    print(f"Valid individual-test rows: {len(df)}\n")

    if len(df) == 0:
        print("No valid rows to evaluate. Exiting.")
        return

    recommender = SHLRecommender(top_k=TOP_K)

    total = len(df)
    hits = 0

    for _, row in df.iterrows():
        query = row["Query"]
        expected_name = extract_name_from_url(row["Assessment_url"])

        recommendations = recommender.recommend(query)
        

        print("\nQuery:", query[:80], "...")
        print("Expected:", expected_name)
        print("Recommended:")
        for r in recommendations:
            print(" -", r["name"])

        expected_tokens = tokenize(expected_name)

        for r in recommendations:
            rec_tokens = tokenize(r["name"])

            overlap = expected_tokens & rec_tokens
            if len(overlap) / max(len(expected_tokens), 1) >= 0.5:
                hits += 1
                break



    recall = hits / total

    print("\n==============================")
    print(f"Recall@{TOP_K}: {recall:.4f}")
    print(f"Hits: {hits} / {total}")
    print("===============================")


if __name__ == "__main__":
    main()

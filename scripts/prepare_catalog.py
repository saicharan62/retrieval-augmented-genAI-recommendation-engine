"""
prepare_catalog.py

Loads the provided SHL catalog XLSX file,
cleans required columns, and saves it as CSV.
"""

import pandas as pd

INPUT_PATH = "data/Gen_AI Dataset.xlsx"
OUTPUT_PATH = "data/shl_catalog.csv"


def main():
    df = pd.read_excel(INPUT_PATH)

    print("Original columns:")
    print(df.columns.tolist())
    print(f"Total rows: {len(df)}")

    # Keep only relevant columns (adjust names if needed)
    required_columns = [
        "Assessment Name",
        "URL",
        "Description",
        "Test Type",
        "Duration",
        "Remote Testing",
        "Adaptive Testing",
    ]

    df = df[required_columns]

    # Rename to internal standard names
    df = df.rename(columns={
        "Assessment Name": "name",
        "URL": "url",
        "Description": "description",
        "Test Type": "test_type",
        "Duration": "duration",
        "Remote Testing": "remote_support",
        "Adaptive Testing": "adaptive_support",
    })

    print(f"Cleaned rows: {len(df)}")

    if len(df) < 377:
        raise ValueError("Catalog has less than 377 assessments")

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved cleaned catalog to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

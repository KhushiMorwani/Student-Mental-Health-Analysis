# =================================================
# src/data_cleaner.py
# PURPOSE: Cleans and validates the dataset.
# Real data always has errors — we fix them here.
# =================================================
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import load_combined_data, save_to_csv
def inspect_data(df):
    """
    Prints a full inspection report of the DataFrame.
    Always run this first before cleaning anything.
    """
    print("\n" + "="*50)
    print("  DATA INSPECTION REPORT")
    print("="*50)

    print(f"\n📐 Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    print("\n📋 Column data types:")
    print(df.dtypes.to_string())

    print("\n🔍 Missing values:")
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("  ✅ No missing values found!")
    else:
        print(missing[missing > 0])

    print("\n📊 Basic statistics:")
    print(df.describe().round(2).to_string())

    print("\n🔁 Duplicate rows:", df.duplicated().sum())
def handle_missing_values(df):
    """
    Fills missing values using median for numbers
    and mode for text columns.
    """
    print("\n" + "="*50)
    print("  HANDLING MISSING VALUES")
    print("="*50)

    df_clean = df.copy()

    numeric_cols = [
        "sleep_hours", "stress_level", "anxiety_level",
        "depression_score", "exercise_days", "family_support",
        "screen_time_hours", "mood_rating", "cgpa", "age"
    ]

    text_cols = ["gender", "course"]

    for col in numeric_cols:
        if col in df_clean.columns:
            missing = df_clean[col].isnull().sum()
            if missing > 0:
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
                print(f"  🔧 {col}: filled {missing} missing with median ({median_val})")
            else:
                print(f"  ✅ {col}: no missing values")

    for col in text_cols:
        if col in df_clean.columns:
            missing = df_clean[col].isnull().sum()
            if missing > 0:
                mode_val = df_clean[col].mode()[0]
                df_clean[col].fillna(mode_val, inplace=True)
                print(f"  🔧 {col}: filled {missing} missing with mode ({mode_val})")

    return df_clean
def fix_data_types(df):
    """
    Makes sure each column has the correct data type.
    """
    print("\n" + "="*50)
    print("  FIXING DATA TYPES")
    print("="*50)

    df_clean = df.copy()

    int_cols = [
        "student_id", "age", "year_of_study",
        "stress_level", "anxiety_level", "depression_score",
        "exercise_days", "family_support", "mood_rating"
    ]

    float_cols = ["sleep_hours", "screen_time_hours", "cgpa"]

    for col in int_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col],
                            errors='coerce').astype('Int64')
            print(f"  🔄 {col} → Int64")

    for col in float_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col],
                            errors='coerce').astype(float)
            print(f"  🔄 {col} → float64")

    return df_clean
def remove_duplicates(df):
    """
    Removes any duplicate rows from the dataset.
    """
    before = len(df)
    df_clean = df.drop_duplicates()
    after = len(df_clean)
    removed = before - after
    print(f"\n🗑️  Duplicates removed: {removed}")
    print(f"✅ Remaining rows: {after}")
    return df_clean
def clean_pipeline(df):
    """
    Runs all cleaning steps in the correct order.
    This is the main function called by other files.
    """
    print("\n" + "="*50)
    print("  RUNNING CLEANING PIPELINE")
    print("="*50)

    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = fix_data_types(df)

    print("\n✅ Cleaning pipeline complete!")
    return df
# ================================================
# Run directly to test:
# python src/data_cleaner.py
# ================================================
if __name__ == "__main__":
    print("Loading raw data...")
    df_raw = load_combined_data()

    if df_raw is not None:
        inspect_data(df_raw)
        df_cleaned = clean_pipeline(df_raw)
        save_to_csv(df_cleaned, "cleaned_data.csv")
        print("\n📋 Cleaned data shape:", df_cleaned.shape)
        print("\n✅ Cleaning complete!")
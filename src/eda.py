# =================================================
# src/eda.py
# PURPOSE: Explores and analyzes the cleaned data.
# EDA = Exploratory Data Analysis
# We run this BEFORE building the scoring system.
# =================================================

import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import load_combined_data
from src.data_cleaner import clean_pipeline


# The 8 mental health parameters we analyze
HEALTH_PARAMS = [
    "sleep_hours", "stress_level", "anxiety_level",
    "depression_score", "exercise_days", "family_support",
    "screen_time_hours", "mood_rating"
]


def summary_statistics(df):
    """
    Prints full statistics for all health parameters.
    """
    print("\n" + "="*55)
    print("  SUMMARY STATISTICS")
    print("="*55)

    stats = df[HEALTH_PARAMS].describe().round(2)
    print(stats.to_string())

    print("\n📌 KEY AVERAGES:")
    print(f"  Average sleep:       {df['sleep_hours'].mean():.1f} hrs")
    print(f"  Average stress:      {df['stress_level'].mean():.1f} / 10")
    print(f"  Average depression:  {df['depression_score'].mean():.1f} / 10")
    print(f"  Average mood:        {df['mood_rating'].mean():.1f} / 10")


def gender_analysis(df):
    """
    Compares health parameters between genders.
    """
    print("\n" + "="*55)
    print("  GENDER BASED ANALYSIS")
    print("="*55)

    gender_stats = df.groupby('gender')[HEALTH_PARAMS].mean().round(2)
    print(gender_stats.to_string())


def course_analysis(df):
    """
    Shows which courses have highest stress and depression.
    """
    print("\n" + "="*55)
    print("  COURSE WISE ANALYSIS")
    print("="*55)

    course_stats = df.groupby('course')[
        ['stress_level', 'anxiety_level',
         'depression_score', 'mood_rating',
         'sleep_hours']
    ].mean().round(2)

    course_stats = course_stats.sort_values(
        'depression_score', ascending=False
    )
    print(course_stats.to_string())


def correlation_analysis(df):
    """
    Shows how parameters are related to each other.
    Positive = both go up together.
    Negative = one goes up, other goes down.
    """
    print("\n" + "="*55)
    print("  CORRELATION ANALYSIS")
    print("="*55)

    corr_matrix = df[HEALTH_PARAMS].corr().round(2)
    print(corr_matrix.to_string())

    print("\n📌 KEY CORRELATIONS WITH MOOD:")
    mood_corr = corr_matrix['mood_rating'].sort_values(ascending=False)
    for param, val in mood_corr.items():
        if param != 'mood_rating':
            direction = "↑ positive" if val > 0 else "↓ negative"
            print(f"  {param:<22} → {val:+.2f}  ({direction})")


def risk_distribution(df):
    """
    Shows how many students fall in each risk category.
    """
    print("\n" + "="*55)
    print("  PRELIMINARY RISK DISTRIBUTION")
    print("="*55)

    def classify(row):
        if row['depression_score'] >= 7 and row['anxiety_level'] >= 7:
            return 'High Risk'
        elif row['stress_level'] >= 6 or row['depression_score'] >= 5:
            return 'Moderate Risk'
        else:
            return 'Healthy'

    df['preliminary_risk'] = df.apply(classify, axis=1)

    counts = df['preliminary_risk'].value_counts()
    total = len(df)

    print(f"\n  {'Category':<18} {'Count':>6} {'Percentage':>10}")
    print(f"  {'-'*38}")
    for category in ['High Risk', 'Moderate Risk', 'Healthy']:
        count = counts.get(category, 0)
        pct = count / total * 100
        print(f"  {category:<18} {count:>6} {pct:>9.1f}%")
    print(f"  {'-'*38}")
    print(f"  {'TOTAL':<18} {total:>6} {'100.0':>10}%")


def top_at_risk(df):
    """
    Shows the 5 most at risk students.
    """
    print("\n" + "="*55)
    print("  TOP 5 MOST AT RISK STUDENTS")
    print("="*55)

    at_risk = df.nlargest(5, 'depression_score')[
        ['name', 'depression_score',
         'anxiety_level', 'stress_level', 'sleep_hours']
    ]
    print(at_risk.to_string(index=False))


# ================================================
# Run directly to test:
# python src/eda.py
# ================================================
if __name__ == "__main__":
    print("Loading and cleaning data...")
    df_raw = load_combined_data()
    df = clean_pipeline(df_raw)

    summary_statistics(df)
    gender_analysis(df)
    course_analysis(df)
    correlation_analysis(df)
    risk_distribution(df)
    top_at_risk(df)

    print("\n\n✅ EDA complete!")


import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_loader import load_combined_data, save_to_csv
from src.data_cleaner import clean_pipeline
from src.db_connection import get_connection, close_connection
from config.config import SCORING_WEIGHTS, RISK_THRESHOLDS

# STEP 1 — NORMALIZATION FUNCTIONS


def normalize_positive(value, min_val, max_val):
    """
    Converts a positive factor to 0.0 - 1.0 scale.
    Higher value = higher score.
    Example: sleep_hours = 8, range 4-10
             result = (8-4)/(10-4) = 0.667
    """
    if max_val == min_val:
        return 0.5
    result = (value - min_val) / (max_val - min_val)
    return float(np.clip(result, 0.0, 1.0))


def normalize_negative(value, min_val, max_val):
    """
    Converts a negative factor to 0.0 - 1.0 scale.
    Higher value = LOWER score (inverted).
    Example: stress_level = 9, range 1-10
             result = 1 - (9-1)/(10-1) = 0.111
    """
    if max_val == min_val:
        return 0.5
    result = 1.0 - (value - min_val) / (max_val - min_val)
    return float(np.clip(result, 0.0, 1.0))



# STEP 2 — SCORING FORMULA


def compute_score(row):
    """
    Computes mental health score for one student.

    HOW IT WORKS:
    1. Normalize each parameter to 0-1
    2. Multiply by its weight from config.py
    3. Sum all weighted values
    4. Result is score between 0 and 100

    Args:
        row: one student row from DataFrame

    Returns:
        float: score between 0 and 100
    """

    # Positive factors — higher is better
    sleep    = normalize_positive(row['sleep_hours'],    4.0, 10.0)
    exercise = normalize_positive(row['exercise_days'],  0,   7)
    support  = normalize_positive(row['family_support'], 1,   10)
    mood     = normalize_positive(row['mood_rating'],    1,   10)

    # Negative factors — higher is worse
    stress     = normalize_negative(row['stress_level'],     1, 10)
    anxiety    = normalize_negative(row['anxiety_level'],    1, 10)
    depression = normalize_negative(row['depression_score'], 1, 10)
    screen     = normalize_negative(row['screen_time_hours'],1, 12)

    # Get weights from config.py
    w = SCORING_WEIGHTS

    # Calculate final score
    score = (
        sleep      * w['sleep_hours']       +
        exercise   * w['exercise_days']     +
        support    * w['family_support']    +
        mood       * w['mood_rating']       +
        stress     * w['stress_level']      +
        anxiety    * w['anxiety_level']     +
        depression * w['depression_score']  +
        screen     * w['screen_time_hours']
    )

    return float(np.clip(round(score, 2), 0.0, 100.0))



# STEP 3 — RISK CLASSIFICATION


def classify_risk(score):
    """
    Classifies student into risk category based on score.

    Args:
        score: float between 0 and 100

    Returns:
        str: 'Healthy', 'Moderate Risk', or 'High Risk'
    """
    if score >= RISK_THRESHOLDS['healthy']:
        return 'Healthy'
    elif score >= RISK_THRESHOLDS['moderate']:
        return 'Moderate Risk'
    else:
        return 'High Risk'



# STEP 4 — SCORE ALL STUDENTS


def score_all_students(df):
    """
    Applies scoring formula to every student.

    Args:
        df: cleaned combined DataFrame

    Returns:
        DataFrame with two new columns:
        - mental_health_score
        - risk_category
    """
    print("\n" + "="*55)
    print("  COMPUTING MENTAL HEALTH SCORES")
    print("="*55)

    df_scored = df.copy()

    # Apply formula to each row
    # axis=1 means row by row
    df_scored['mental_health_score'] = df_scored.apply(
        compute_score, axis=1
    )

    # Classify each score
    df_scored['risk_category'] = df_scored['mental_health_score'].apply(
        classify_risk
    )

    # Sort by score — most at risk first
    df_scored = df_scored.sort_values(
        'mental_health_score', ascending=True
    )

    print(f"\n Scores computed for {len(df_scored)} students")
    print(f"   Lowest score:  {df_scored['mental_health_score'].min():.2f}")
    print(f"   Highest score: {df_scored['mental_health_score'].max():.2f}")
    print(f"   Average score: {df_scored['mental_health_score'].mean():.2f}")

    return df_scored



# STEP 5 — PRINT SCORE REPORT


def print_score_report(df_scored):
    """
    Prints formatted score report for all students.
    """
    print("\n" + "="*70)
    print("  STUDENT MENTAL HEALTH SCORE REPORT")
    print("="*70)
    print(f"  {'Name':<25} {'Course':<22} {'Score':>7} {'Category'}")
    print(f"  {'-'*65}")

    for _, row in df_scored.iterrows():
        if row['risk_category'] == 'High Risk':
            symbol = '🔴'
        elif row['risk_category'] == 'Moderate Risk':
            symbol = '🟡'
        else:
            symbol = '🟢'

        print(f"  {row['name']:<25} {row['course']:<22} "
              f"{row['mental_health_score']:>6.1f}  "
              f"{symbol} {row['risk_category']}")

    # Summary
    print(f"\n  {'-'*65}")
    counts = df_scored['risk_category'].value_counts()
    total  = len(df_scored)

    print(f"\n   RISK SUMMARY:")
    for category in ['High Risk', 'Moderate Risk', 'Healthy']:
        count = counts.get(category, 0)
        pct   = count / total * 100
        bar   =  "" * int(pct / 5)
        print(f"     {category:<15}: {count:>3} students "
              f"({pct:5.1f}%)  {bar}")

    print(f"\n  Total students : {total}")
    print(f"  Average score  : {df_scored['mental_health_score'].mean():.1f} / 100")



# STEP 6 — SAVE SCORES TO MYSQL

def save_scores_to_db(df_scored):
    """
    Saves computed scores into student_scores table in MySQL.

    WHY SAVE BACK TO DB?
    Counselors and managers use MySQL dashboards.
    Saving scores there makes results accessible
    to the whole organization — not just Python users.
    """
    print("\n" + "="*55)
    print("  SAVING SCORES TO MySQL")
    print("="*55)

    conn = get_connection()
    if conn is None:
        print(" Cannot save — no DB connection.")
        return False

    try:
        cursor = conn.cursor()

        
        cursor.execute("DELETE FROM student_scores")
        print("    Cleared old scores")

        
        insert_query = """
            INSERT INTO student_scores
            (student_id, mental_health_score, risk_category, scored_on)
            VALUES (%s, %s, %s, %s)
        """

        records = []
        scored_on = datetime.now()

        for _, row in df_scored.iterrows():
            records.append((
                int(row['student_id']),
                float(row['mental_health_score']),
                str(row['risk_category']),
                scored_on
            ))

        
        cursor.executemany(insert_query, records)
        conn.commit()

        print(f"   Saved {cursor.rowcount} scores to database")

        
        cursor.execute("""
            SELECT risk_category, COUNT(*) as count
            FROM student_scores
            GROUP BY risk_category
        """)
        results = cursor.fetchall()
        print("\n   Scores saved by category:")
        for category, count in results:
            print(f"     {category}: {count} students")

        return True

    except Exception as e:
        print(f"   Error saving scores: {e}")
        conn.rollback()
        return False

    finally:
        close_connection(conn, cursor)


# MAIN PIPELINE — Runs everything


if __name__ == "__main__":
    print("\n" + ""*55)
    print("  PHASE 4 — MENTAL HEALTH SCORING ENGINE")
    print(""*55)

    # Step 1: Load data
    print("\nStep 1: Loading data...")
    df_raw = load_combined_data()
    if df_raw is None:
        print(" Could not load data. Exiting.")
        exit(1)

    # Step 2: Clean data
    print("\nStep 2: Cleaning data...")
    df_cleaned = clean_pipeline(df_raw)

    # Step 3: Score all students
    print("\nStep 3: Computing scores...")
    df_scored = score_all_students(df_cleaned)

    # Step 4: Print report
    print_score_report(df_scored)

    # Step 5: Save to CSV
    print("\nStep 5: Saving to CSV...")
    save_to_csv(df_scored, "student_scores.csv", folder="reports/")

    # Step 6: Save to MySQL
    print("\nStep 6: Saving to MySQL...")
    save_scores_to_db(df_scored)

    print("\n\n" + ""*55)
    print("  PHASE 4 COMPLETE!")
    print("   Check reports/student_scores.csv")
    print("    Check MySQL table: student_scores")
    print(""*55)
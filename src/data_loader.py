import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.db_connection import get_connection, close_connection
def load_students():
    """
    Loads students table into a Pandas DataFrame.
    """
    conn = get_connection()
    if conn is None:
        return None

    try:
        query = "SELECT * FROM students"
        df = pd.read_sql(query, conn)
        print(f"✅ Loaded students: {df.shape[0]} rows")
        return df

    except Exception as e:
        print(f"❌ Error loading students: {e}")
        return None

    finally:
        close_connection(conn)
def load_combined_data():
    """
    Loads students + mental health records together using JOIN.
    This is the main DataFrame used throughout the project.
    """
    conn = get_connection()
    if conn is None:
        return None

    try:
        query = """
            SELECT
                s.student_id,
                s.name,
                s.age,
                s.gender,
                s.course,
                s.year_of_study,
                s.cgpa,
                m.sleep_hours,
                m.stress_level,
                m.anxiety_level,
                m.depression_score,
                m.exercise_days,
                m.family_support,
                m.screen_time_hours,
                m.mood_rating
            FROM students s
            JOIN mental_health_records m
            ON s.student_id = m.student_id
            ORDER BY s.student_id
        """
        df = pd.read_sql(query, conn)
        print(f"✅ Loaded combined data: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

    except Exception as e:
        print(f"❌ Error loading combined data: {e}")
        return None

    finally:
        close_connection(conn)
def save_to_csv(df, filename, folder="data/processed/"):
    """
    Saves DataFrame to CSV file.
    """
    path = os.path.join(folder, filename)
    df.to_csv(path, index=False)
    print(f"💾 Saved to: {path}")
# ================================================
# Run directly to test:
# python src/data_loader.py
# ================================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  DATA LOADER TEST")
    print("="*50)

    df = load_combined_data()

    if df is not None:
        print("\n📋 First 5 rows:")
        print(df.head())
        print("\n📊 Shape:", df.shape)
        print("\n🔢 Columns:", list(df.columns))
        save_to_csv(df, "combined_data.csv")

    print("\n✅ Data loading complete!")
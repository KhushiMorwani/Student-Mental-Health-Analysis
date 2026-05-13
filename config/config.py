# config/config.py
# This file stores all settings for the project.
# Every other Python file imports from here.

# ── Database connection settings ──────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "Khush123khush",
    "database": "mental_health_db"
}

# ── Scoring weights for Phase 4 ───────────────────────────────
# Positive factors ADD to mental health score.
# Negative factors SUBTRACT from it.
# All weights together add up to 100.
SCORING_WEIGHTS = {
    "sleep_hours":       15,
    "exercise_days":     10,
    "family_support":    15,
    "mood_rating":       10,
    "stress_level":      15,
    "anxiety_level":     15,
    "depression_score":  15,
    "screen_time_hours":  5
}

# ── Risk category thresholds ──────────────────────────────────
RISK_THRESHOLDS = {
    "healthy":  70,
    "moderate": 40
}
# Score >= 70  → Healthy
# Score 40-69  → Moderate Risk
# Score < 40   → High Risk

# ── Folder paths used across the project ──────────────────────
REPORTS_DIR   = "reports/"
RAW_DIR       = "data/raw/"
PROCESSED_DIR = "data/processed/"
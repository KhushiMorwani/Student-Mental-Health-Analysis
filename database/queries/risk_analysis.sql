-- =============================================================
-- database/queries/risk_analysis.sql
-- PHASE 2 — RISK ANALYSIS QUERIES
-- PURPOSE: These queries directly support the counseling team.
--          They identify which students need help and why.
--          This is the "business value" of the project.
-- =============================================================

USE mental_health_db;

-- ─────────────────────────────────────────────────────────────
-- QUERY 1: Full student mental health dashboard view
-- WHY: A single-query summary that a manager or counselor
--      could look at every morning. Clear, readable output.
-- ─────────────────────────────────────────────────────────────
SELECT
    s.student_id,
    s.name,
    s.course,
    s.year_of_study,
    m.sleep_hours,
    m.stress_level,
    m.anxiety_level,
    m.depression_score,
    m.exercise_days,
    m.family_support,
    m.screen_time_hours,
    m.mood_rating,
    CASE
        WHEN m.depression_score >= 7 AND m.anxiety_level >= 7 THEN '🔴 High Risk'
        WHEN m.stress_level >= 6 OR m.depression_score >= 5   THEN '🟡 Moderate Risk'
        ELSE '🟢 Healthy'
    END AS risk_flag
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
ORDER BY m.depression_score DESC, m.anxiety_level DESC;

-- ─────────────────────────────────────────────────────────────
-- QUERY 2: High-risk student identification
-- WHY: The counseling team's most important report.
--      Identifies students who need IMMEDIATE intervention.
-- ─────────────────────────────────────────────────────────────
SELECT
    s.name,
    s.age,
    s.course,
    s.year_of_study,
    m.depression_score,
    m.anxiety_level,
    m.stress_level,
    m.sleep_hours,
    m.family_support,
    'IMMEDIATE COUNSELING RECOMMENDED' AS action_required
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
WHERE m.depression_score >= 7
  AND m.anxiety_level >= 7
ORDER BY m.depression_score DESC;

-- ─────────────────────────────────────────────────────────────
-- QUERY 3: Risk distribution — How many in each category?
-- WHY: Management reports always need summary counts.
--      "How many students are at risk this semester?"
-- ─────────────────────────────────────────────────────────────
SELECT
    risk_category,
    COUNT(*) AS student_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM mental_health_records), 1) AS percentage
FROM (
    SELECT
        CASE
            WHEN depression_score >= 7 AND anxiety_level >= 7 THEN 'High Risk'
            WHEN stress_level >= 6 OR depression_score >= 5   THEN 'Moderate Risk'
            ELSE 'Healthy'
        END AS risk_category
    FROM mental_health_records
) AS risk_table
GROUP BY risk_category
ORDER BY FIELD(risk_category, 'High Risk', 'Moderate Risk', 'Healthy');

-- ─────────────────────────────────────────────────────────────
-- QUERY 4: Course-level risk summary
-- WHY: Which departments have the most at-risk students?
--      Universities use this to allocate counseling resources.
-- ─────────────────────────────────────────────────────────────
SELECT
    s.course,
    COUNT(*) AS total_students,
    SUM(CASE WHEN m.depression_score >= 7 AND m.anxiety_level >= 7 THEN 1 ELSE 0 END) AS high_risk_count,
    SUM(CASE WHEN (m.stress_level >= 6 OR m.depression_score >= 5)
              AND NOT (m.depression_score >= 7 AND m.anxiety_level >= 7) THEN 1 ELSE 0 END) AS moderate_risk_count,
    ROUND(AVG(m.depression_score), 1) AS avg_depression,
    ROUND(AVG(m.stress_level), 1) AS avg_stress
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
GROUP BY s.course
ORDER BY high_risk_count DESC, avg_depression DESC;

-- ─────────────────────────────────────────────────────────────
-- QUERY 5: Sleep deprivation impact analysis
-- WHY: Sleep is the single biggest lifestyle factor.
--      This query proves it with data.
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN m.sleep_hours >= 8   THEN '1. Excellent (8+ hrs)'
        WHEN m.sleep_hours >= 6.5 THEN '2. Adequate (6.5–8 hrs)'
        WHEN m.sleep_hours >= 5   THEN '3. Poor (5–6.5 hrs)'
        ELSE                           '4. Critical (<5 hrs)'
    END AS sleep_category,
    COUNT(*) AS students,
    ROUND(AVG(m.depression_score), 2) AS avg_depression,
    ROUND(AVG(m.anxiety_level), 2)    AS avg_anxiety,
    ROUND(AVG(m.stress_level), 2)     AS avg_stress,
    ROUND(AVG(m.mood_rating), 2)      AS avg_mood
FROM mental_health_records m
GROUP BY sleep_category
ORDER BY sleep_category;

-- ─────────────────────────────────────────────────────────────
-- QUERY 6: Family support as protective factor
-- WHY: Family support is a "protective factor" in psychology.
--      This query checks if high support → lower risk.
-- ─────────────────────────────────────────────────────────────
SELECT
    CASE
        WHEN m.family_support >= 8 THEN 'High Support (8–10)'
        WHEN m.family_support >= 5 THEN 'Medium Support (5–7)'
        ELSE 'Low Support (1–4)'
    END AS support_level,
    COUNT(*) AS students,
    ROUND(AVG(m.depression_score), 2) AS avg_depression,
    ROUND(AVG(m.anxiety_level), 2)    AS avg_anxiety,
    ROUND(AVG(m.mood_rating), 2)      AS avg_mood
FROM mental_health_records m
GROUP BY support_level
ORDER BY avg_depression ASC;

-- ─────────────────────────────────────────────────────────────
-- QUERY 7: Students stored scores after Phase 4 scoring
-- WHY: After Python scoring engine runs, counselors check
--      this table to see final categorized results.
-- ─────────────────────────────────────────────────────────────
SELECT
    s.name,
    s.course,
    s.year_of_study,
    sc.mental_health_score,
    sc.risk_category,
    sc.scored_on
FROM students s
JOIN student_scores sc ON s.student_id = sc.student_id
ORDER BY sc.mental_health_score ASC;  -- Most at-risk first

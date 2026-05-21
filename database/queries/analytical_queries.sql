

USE mental_health_db;


SELECT
    s.name,
    m.sleep_hours,
    CASE
        WHEN m.sleep_hours >= 8.0 THEN 'Excellent Sleep'
        WHEN m.sleep_hours >= 6.5 THEN 'Adequate Sleep'
        WHEN m.sleep_hours >= 5.0 THEN 'Poor Sleep'
        ELSE 'Severe Sleep Deprivation'
    END AS sleep_quality,
    m.stress_level,
    m.mood_rating
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
ORDER BY m.sleep_hours DESC;


SELECT
    s.name,
    s.course,
    m.stress_level,
    m.anxiety_level,
    m.depression_score,
    CASE
        WHEN m.depression_score >= 8 AND m.anxiety_level >= 8 THEN 'Critical Risk'
        WHEN m.depression_score >= 6 OR m.anxiety_level >= 7  THEN 'High Risk'
        WHEN m.stress_level >= 7                              THEN 'Moderate Risk'
        ELSE 'Low Risk'
    END AS mental_risk_flag
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
ORDER BY m.depression_score DESC;


SELECT
    ROUND(AVG(sleep_hours), 2)         AS avg_sleep,
    ROUND(MIN(sleep_hours), 2)         AS min_sleep,
    ROUND(MAX(sleep_hours), 2)         AS max_sleep,
    ROUND(AVG(stress_level), 2)        AS avg_stress,
    ROUND(AVG(anxiety_level), 2)       AS avg_anxiety,
    ROUND(AVG(depression_score), 2)    AS avg_depression,
    ROUND(AVG(exercise_days), 2)       AS avg_exercise_days,
    ROUND(AVG(family_support), 2)      AS avg_family_support,
    ROUND(AVG(screen_time_hours), 2)   AS avg_screen_time,
    ROUND(AVG(mood_rating), 2)         AS avg_mood
FROM mental_health_records;


SELECT
    s.gender,
    COUNT(*)                              AS total_students,
    ROUND(AVG(m.sleep_hours), 1)          AS avg_sleep,
    ROUND(AVG(m.stress_level), 1)         AS avg_stress,
    ROUND(AVG(m.anxiety_level), 1)        AS avg_anxiety,
    ROUND(AVG(m.depression_score), 1)     AS avg_depression,
    ROUND(AVG(m.mood_rating), 1)          AS avg_mood
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
GROUP BY s.gender;


SELECT
    s.name,
    s.course,
    m.stress_level,
    m.anxiety_level,
    RANK() OVER (ORDER BY m.stress_level DESC) AS stress_rank,
    RANK() OVER (ORDER BY m.mood_rating  DESC) AS mood_rank
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id;


SELECT
    s.name,
    s.course,
    m.stress_level,
    m.depression_score,
    RANK() OVER (
        PARTITION BY s.course
        ORDER BY m.stress_level DESC
    ) AS rank_within_course
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
ORDER BY s.course, rank_within_course;


SELECT
    s.student_id,
    s.name,
    m.stress_level,
    ROUND(AVG(m.stress_level) OVER (
        ORDER BY s.student_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_avg_stress
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id;


SELECT
    CASE
        WHEN m.sleep_hours >= 7.5 THEN 'High Sleep (7.5+ hrs)'
        WHEN m.sleep_hours >= 6.0 THEN 'Mid Sleep (6–7.5 hrs)'
        ELSE 'Low Sleep (<6 hrs)'
    END AS sleep_group,
    COUNT(*)                          AS student_count,
    ROUND(AVG(m.mood_rating), 2)      AS avg_mood,
    ROUND(AVG(m.stress_level), 2)     AS avg_stress,
    ROUND(AVG(m.anxiety_level), 2)    AS avg_anxiety,
    ROUND(AVG(m.depression_score), 2) AS avg_depression
FROM mental_health_records m
GROUP BY sleep_group
ORDER BY avg_mood DESC;


SELECT
    s.name,
    s.course,
    m.depression_score,
    m.anxiety_level,
    m.sleep_hours
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
WHERE m.depression_score > (
    SELECT AVG(depression_score) FROM mental_health_records
)
ORDER BY m.depression_score DESC;


SELECT
    s.name,
    m.mood_rating,
    NTILE(4) OVER (ORDER BY m.mood_rating DESC) AS mood_quartile
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
ORDER BY mood_quartile, m.mood_rating DESC;

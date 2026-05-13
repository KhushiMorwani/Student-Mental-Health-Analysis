

USE mental_health_db;

SELECT * FROM students;

SELECT
    student_id,
    name,
    course,
    year_of_study,
    cgpa
FROM students
ORDER BY cgpa DESC;  -- Show top performers first

SELECT name, course, year_of_study, cgpa
FROM students
WHERE year_of_study = 3;

-- ─────────────────────────────────────────────────────────────
-- QUERY 4: WHERE with AND — High CGPA female students

SELECT name, gender, course, cgpa
FROM students
WHERE gender = 'Female'
  AND cgpa >= 7.5
ORDER BY cgpa DESC;

-- ─────────────────────────────────────────────────────────────
-- QUERY 5: JOIN — Combine student info with health records
-- WHY: Real data lives in multiple tables. JOINs bring them together.
--      This is the #1 skill interviewers test.
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
    m.mood_rating
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
ORDER BY s.student_id;

-- ─────────────────────────────────────────────────────────────
-- QUERY 6: WHERE on joined data — Students with high stress
-- WHY: Filtering on joined data is the most common analyst task.
-- ─────────────────────────────────────────────────────────────
SELECT
    s.name,
    s.course,
    m.stress_level,
    m.anxiety_level,
    m.sleep_hours
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
WHERE m.stress_level >= 8
ORDER BY m.stress_level DESC;

-- ─────────────────────────────────────────────────────────────
-- QUERY 7: Aggregate — Count students by gender
-- WHY: Aggregate functions summarize large datasets instantly.
-- ─────────────────────────────────────────────────────────────
SELECT
    gender,
    COUNT(*) AS total_students,
    ROUND(AVG(cgpa), 2) AS avg_cgpa
FROM students
GROUP BY gender;

-- ─────────────────────────────────────────────────────────────
-- QUERY 8: GROUP BY + ORDER BY — Average stress by course
-- WHY: GROUP BY is the backbone of summary reports.
-- ─────────────────────────────────────────────────────────────
SELECT
    s.course,
    COUNT(s.student_id)         AS total_students,
    ROUND(AVG(m.stress_level),1)  AS avg_stress,
    ROUND(AVG(m.sleep_hours),1)   AS avg_sleep,
    ROUND(AVG(m.mood_rating),1)   AS avg_mood
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
GROUP BY s.course
ORDER BY avg_stress DESC;  -- Highest stress courses on top

-- ─────────────────────────────────────────────────────────────
-- QUERY 9: HAVING — Courses where avg stress > 7
-- WHY: HAVING filters GROUPS (after GROUP BY).
--      WHERE filters rows BEFORE grouping.
-- ─────────────────────────────────────────────────────────────
SELECT
    s.course,
    ROUND(AVG(m.stress_level), 1) AS avg_stress
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
GROUP BY s.course
HAVING avg_stress > 6.5
ORDER BY avg_stress DESC;

-- ─────────────────────────────────────────────────────────────
-- QUERY 10: LIMIT — Top 5 most anxious students
-- WHY: LIMIT is used in dashboards and leaderboards.
-- ─────────────────────────────────────────────────────────────
SELECT
    s.name,
    s.course,
    m.anxiety_level,
    m.depression_score,
    m.sleep_hours
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
ORDER BY m.anxiety_level DESC, m.depression_score DESC
LIMIT 5;


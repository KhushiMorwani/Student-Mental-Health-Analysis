

USE mental_health_db;

SELECT * FROM students;

SELECT
    student_id,
    name,
    course,
    year_of_study,
    cgpa
FROM students
ORDER BY cgpa DESC;  

SELECT name, course, year_of_study, cgpa
FROM students
WHERE year_of_study = 3;


SELECT name, gender, course, cgpa
FROM students
WHERE gender = 'Female'
  AND cgpa >= 7.5
ORDER BY cgpa DESC;

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


SELECT
    gender,
    COUNT(*) AS total_students,
    ROUND(AVG(cgpa), 2) AS avg_cgpa
FROM students
GROUP BY gender;


SELECT
    s.course,
    COUNT(s.student_id)         AS total_students,
    ROUND(AVG(m.stress_level),1)  AS avg_stress,
    ROUND(AVG(m.sleep_hours),1)   AS avg_sleep,
    ROUND(AVG(m.mood_rating),1)   AS avg_mood
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
GROUP BY s.course
ORDER BY avg_stress DESC;  


SELECT
    s.course,
    ROUND(AVG(m.stress_level), 1) AS avg_stress
FROM students s
JOIN mental_health_records m ON s.student_id = m.student_id
GROUP BY s.course
HAVING avg_stress > 6.5
ORDER BY avg_stress DESC;


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


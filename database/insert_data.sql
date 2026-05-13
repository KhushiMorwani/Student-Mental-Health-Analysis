

USE mental_health_db;
SET SQL_SAFE_UPDATES = 0;
DELETE FROM student_scores;
DELETE FROM mental_health_records;
DELETE FROM students;

ALTER TABLE students AUTO_INCREMENT = 1;
ALTER TABLE mental_health_records AUTO_INCREMENT = 1;
ALTER TABLE student_scores AUTO_INCREMENT = 1;

INSERT INTO students (name, age, gender, course, year_of_study, cgpa) VALUES
('Aarav Sharma',      20, 'Male',   'Computer Science',       2, 8.50),
('Priya Patel',       21, 'Female', 'Psychology',             3, 8.10),
('Rohan Mehta',       19, 'Male',   'Mechanical Engineering', 1, 7.80),
('Sneha Iyer',        22, 'Female', 'Data Science',           4, 8.90),
('Karan Gupta',       20, 'Male',   'Business Administration', 2, 7.50),

('Ananya Reddy',      21, 'Female', 'Computer Science',       3, 6.80),
('Vijay Nair',        22, 'Male',   'Civil Engineering',      4, 6.20),
('Divya Joshi',       19, 'Female', 'Arts',                   1, 7.10),
('Arjun Singh',       20, 'Male',   'Data Science',           2, 6.90),
('Meera Pillai',      23, 'Female', 'Medicine',               5, 7.40),
('Siddharth Rao',     21, 'Male',   'Commerce',               3, 6.50),
('Kavya Menon',       20, 'Female', 'Psychology',             2, 7.30),
('Nikhil Verma',      22, 'Male',   'Computer Science',       4, 6.00),
('Aditi Chandra',     19, 'Female', 'Law',                    1, 7.60),
('Rahul Bose',        21, 'Male',   'Mechanical Engineering', 3, 6.70),

('Shreya Kapoor',     20, 'Female', 'Medicine',               2, 5.50),
('Amit Kumar',        22, 'Male',   'Computer Science',       4, 5.20),
('Nisha Tiwari',      21, 'Female', 'Arts',                   3, 5.80),
('Deepak Yadav',      23, 'Male',   'Civil Engineering',      5, 4.90),
('Pooja Mishra',      19, 'Female', 'Commerce',               1, 5.40),
('Varun Saxena',      21, 'Male',   'Data Science',           3, 5.70),
('Ritika Das',        20, 'Female', 'Psychology',             2, 5.10),
('Suresh Pandey',     22, 'Male',   'Law',                    4, 5.30),
('Manisha Ghosh',     21, 'Female', 'Business Administration', 3, 5.60),
('Tejas Malhotra',    19, 'Male',   'Mechanical Engineering', 1, 6.10),

('Lakshmi Subramaniam', 22, 'Female', 'Data Science',         4, 7.20),
('Akash Dubey',        20, 'Male',   'Computer Science',      2, 6.40),
('Preeti Aggarwal',    21, 'Female', 'Medicine',              3, 6.80),
('Harish Nanda',       23, 'Male',   'Psychology',            5, 7.00),
('Shweta Rajput',      20, 'Female', 'Commerce',              2, 6.60);


INSERT INTO mental_health_records
    (student_id, sleep_hours, stress_level, anxiety_level, depression_score,
     exercise_days, family_support, screen_time_hours, mood_rating, recorded_date)
VALUES

(1,  8.0, 3, 2, 1, 5, 9, 3.0, 9, '2024-01-15'),
(2,  7.5, 2, 3, 2, 4, 8, 2.5, 8, '2024-01-15'),
(3,  8.5, 3, 2, 1, 6, 9, 2.0, 9, '2024-01-15'),
(4,  7.0, 4, 3, 2, 5, 8, 3.0, 8, '2024-01-15'),
(5,  8.0, 3, 2, 2, 4, 7, 3.5, 8, '2024-01-15'),
(6,  6.5, 6, 5, 5, 3, 6, 5.0, 5, '2024-01-15'),
(7,  6.0, 7, 6, 5, 2, 5, 6.0, 5, '2024-01-15'),
(8,  6.5, 5, 5, 4, 3, 6, 5.5, 6, '2024-01-15'),
(9,  6.0, 6, 6, 5, 2, 5, 5.0, 5, '2024-01-15'),
(10, 5.5, 7, 6, 6, 2, 6, 6.0, 5, '2024-01-15'),
(11, 6.0, 6, 5, 5, 3, 5, 5.5, 5, '2024-01-15'),
(12, 6.5, 5, 4, 4, 3, 7, 4.5, 6, '2024-01-15'),
(13, 6.0, 7, 6, 5, 2, 5, 6.0, 4, '2024-01-15'),
(14, 6.5, 5, 5, 4, 3, 6, 5.0, 6, '2024-01-15'),
(15, 6.0, 6, 6, 5, 2, 5, 5.5, 5, '2024-01-15'),

(16, 4.5, 9, 8, 8, 1, 3, 9.0, 2, '2024-01-15'),
(17, 4.0, 9, 9, 9, 0, 2, 10.0, 1, '2024-01-15'),
(18, 4.5, 8, 8, 8, 1, 3, 8.5, 2, '2024-01-15'),
(19, 4.0, 9, 9, 9, 0, 2, 10.5, 1, '2024-01-15'),
(20, 4.5, 8, 8, 8, 1, 3, 9.0, 2, '2024-01-15'),
(21, 5.0, 8, 7, 8, 1, 3, 8.0, 2, '2024-01-15'),
(22, 4.5, 9, 9, 9, 0, 2, 10.0, 1, '2024-01-15'),
(23, 4.0, 9, 8, 8, 0, 2, 9.5, 2, '2024-01-15'),
(24, 5.0, 8, 7, 7, 1, 3, 8.5, 3, '2024-01-15'),
(25, 5.5, 7, 7, 7, 2, 4, 7.0, 3, '2024-01-15'),

(26, 7.0, 4, 4, 3, 4, 7, 4.5, 7, '2024-01-15'),
(27, 6.5, 6, 5, 4, 3, 6, 5.5, 5, '2024-01-15'),
(28, 7.0, 5, 4, 4, 3, 7, 4.5, 6, '2024-01-15'),
(29, 7.5, 4, 3, 3, 4, 7, 4.0, 7, '2024-01-15'),
(30, 6.5, 5, 5, 4, 3, 6, 5.0, 6, '2024-01-15');

-- Confirm insertion
SELECT COUNT(*) AS total_students FROM students;
SELECT COUNT(*) AS total_records FROM mental_health_records;

CREATE DATABASE IF NOT EXISTS mental_health_db;
USE mental_health_db;

CREATE TABLE IF NOT EXISTS students (
    student_id    INT PRIMARY KEY AUTO_INCREMENT,  -- Unique ID for each student
    name          VARCHAR(100) NOT NULL,            -- Full name
    age           INT NOT NULL,                     -- Age in years
    gender        VARCHAR(20) NOT NULL,             -- Male / Female / Other
    course        VARCHAR(100) NOT NULL,            -- e.g. Computer Science
    year_of_study INT NOT NULL,                     -- 1 to 4
    cgpa          DECIMAL(3,2) NOT NULL             -- e.g. 8.45
);

CREATE TABLE IF NOT EXISTS mental_health_records (
    record_id           INT PRIMARY KEY AUTO_INCREMENT,
    student_id          INT NOT NULL,
    sleep_hours         DECIMAL(3,1) NOT NULL,  -- Hours of sleep per night (4.0–10.0)
    stress_level        INT NOT NULL,            -- Self-rated stress 1–10
    anxiety_level       INT NOT NULL,            -- Self-rated anxiety 1–10
    depression_score    INT NOT NULL,            -- Self-rated depression 1–10
    exercise_days       INT NOT NULL,            -- Days exercised per week 0–7
    family_support      INT NOT NULL,            -- Perceived family support 1–10
    screen_time_hours   DECIMAL(3,1) NOT NULL,  -- Daily screen time in hours
    mood_rating         INT NOT NULL,            -- Overall mood 1–10
    recorded_date       DATE NOT NULL,           -- When the survey was taken

   
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE                        
);


CREATE TABLE IF NOT EXISTS student_scores (
    score_id             INT PRIMARY KEY AUTO_INCREMENT,
    student_id           INT NOT NULL,
    mental_health_score  DECIMAL(5,2) NOT NULL,  -- Score 0.00 to 100.00
    risk_category        VARCHAR(20) NOT NULL,    -- 'Healthy', 'Moderate Risk', 'High Risk'
    scored_on            DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE
);

SHOW TABLES;
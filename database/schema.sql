CREATE DATABASE IF NOT EXISTS mental_health_db;
USE mental_health_db;

CREATE TABLE IF NOT EXISTS students (
    student_id    INT PRIMARY KEY AUTO_INCREMENT,  
    name          VARCHAR(100) NOT NULL,            
    age           INT NOT NULL,                     
    gender        VARCHAR(20) NOT NULL,             
    course        VARCHAR(100) NOT NULL,            
    year_of_study INT NOT NULL,                     
    cgpa          DECIMAL(3,2) NOT NULL             
);

CREATE TABLE IF NOT EXISTS mental_health_records (
    record_id           INT PRIMARY KEY AUTO_INCREMENT,
    student_id          INT NOT NULL,
    sleep_hours         DECIMAL(3,1) NOT NULL,  
    stress_level        INT NOT NULL,            
    anxiety_level       INT NOT NULL,            
    depression_score    INT NOT NULL,           
    exercise_days       INT NOT NULL,            
    family_support      INT NOT NULL,            
    screen_time_hours   DECIMAL(3,1) NOT NULL,  
    mood_rating         INT NOT NULL,            
    recorded_date       DATE NOT NULL,           

   
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE                        
);


CREATE TABLE IF NOT EXISTS student_scores (
    score_id             INT PRIMARY KEY AUTO_INCREMENT,
    student_id           INT NOT NULL,
    mental_health_score  DECIMAL(5,2) NOT NULL,  
    risk_category        VARCHAR(20) NOT NULL,    
    scored_on            DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE
);

SHOW TABLES;
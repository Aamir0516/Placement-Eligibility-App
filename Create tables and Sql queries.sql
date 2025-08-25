CREATE DATABASE IF NOT EXISTS students_data;
USE students_data;

-- Students Table
CREATE TABLE students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(20),
    email VARCHAR(100),
    phone VARCHAR(50),
    enrollment_year YEAR,
    course_batch VARCHAR(50),
    city VARCHAR(100),
    graduation_year YEAR
);

-- Programming Table
CREATE TABLE programming (
    programming_id INT PRIMARY KEY,
    student_id INT,
    language VARCHAR(50),
    problems_solved INT,
    assessments_completed INT,
    mini_projects INT,
    certifications_earned INT,
    latest_project_score INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Soft Skills Table
CREATE TABLE soft_skills (
    soft_skill_id INT PRIMARY KEY,
    student_id INT,
    communication INT,
    teamwork INT,
    presentation INT,
    leadership INT,
    critical_thinking INT,
    interpersonal_skills INT,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- Placements Table
CREATE TABLE placements (
    placement_id INT PRIMARY KEY,
    student_id INT,
    mock_interview_score INT,
    internships_completed INT,
    placement_status VARCHAR(20),
    company_name VARCHAR(100),
    placement_package DECIMAL(10,2),
    interview_rounds_cleared INT,
    placement_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);
SELECT COUNT(*) AS total_students FROM students;
SELECT COUNT(*) AS total_programming_records FROM programming;
SELECT * FROM students LIMIT 10;
SELECT * FROM programming LIMIT 10;
SELECT * FROM soft_skills LIMIT 10;
SELECT * FROM placements LIMIT 10;

-- 10 sql queries 
-- 1. Total number of students

SELECT COUNT(*) AS total_students
FROM students;

-- 2. Average programming performance per batch
SELECT s.course_batch,
       AVG(p.problems_solved) AS avg_problems_solved,
       AVG(p.assessments_completed) AS avg_assessments,
       AVG(p.latest_project_score) AS avg_project_score
FROM students s
JOIN programming p ON s.student_id = p.student_id
GROUP BY s.course_batch;

-- 3. Top 5 students ready for placement 
SELECT s.name, pl.mock_interview_score, pl.internships_completed
FROM students s
JOIN placements pl ON s.student_id = pl.student_id
ORDER BY pl.mock_interview_score DESC
LIMIT 5;

-- 4. Distribution of soft skills scores (average per skill)
SELECT AVG(communication) AS avg_communication,
       AVG(teamwork) AS avg_teamwork,
       AVG(presentation) AS avg_presentation,
       AVG(leadership) AS avg_leadership,
       AVG(critical_thinking) AS avg_critical_thinking,
       AVG(interpersonal_skills) AS avg_interpersonal
FROM soft_skills;

-- 5. Students with highest programming certifications
SELECT s.name, p.certifications_earned
FROM students s
JOIN programming p ON s.student_id = p.student_id
ORDER BY p.certifications_earned DESC
LIMIT 10;

-- 6. Total placed vs not placed students
SELECT placement_status, COUNT(*) AS total_students
FROM placements
GROUP BY placement_status;

-- 7. Average placement package per batch
SELECT s.course_batch,
       AVG(pl.placement_package) AS avg_package
FROM students s
JOIN placements pl ON s.student_id = pl.student_id
WHERE pl.placement_status = 'Placed'
GROUP BY s.course_batch;

-- 8. Students with no internships completed
SELECT s.name, s.email, pl.internships_completed
FROM students s
JOIN placements pl ON s.student_id = pl.student_id
WHERE pl.internships_completed = 0;

-- 9. Students eligible based on soft skills (e.g., all skills > 70)
SELECT s.name, ss.communication, ss.teamwork, ss.presentation
FROM students s
JOIN soft_skills ss ON s.student_id = ss.student_id
WHERE ss.communication >= 70
  AND ss.teamwork >= 70
  AND ss.presentation >= 70;

-- 10. Companies that hired the most students
SELECT company_name, COUNT(*) AS total_hired
FROM placements
WHERE placement_status = 'Placed'
GROUP BY company_name
ORDER BY total_hired DESC
LIMIT 5;

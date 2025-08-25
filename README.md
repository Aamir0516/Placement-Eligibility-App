# Placement-Eligibility-App
A Streamlit-based web application connected to a MySQL database that helps analyze student placement readiness. Users can filter eligible students based on programming performance, soft skills, and mock interview scores while exploring SQL-driven insights through interactive dashboards.

# Features

Eligibility Finder: Filter students dynamically based on:

Minimum problems solved

Soft skills average score

Mock interview score

Course batch, programming language, and placement status

Insights Dashboard:

Average programming performance per batch

Placement readiness analysis

Soft skills distribution

Internship and placement impact analysis

Company hiring trends

# Tech Stack

Frontend: Streamlit

Backend: MySQL

Language: Python

Libraries: pandas, mysql-connector-python

# Installation & Setup
#1. Clone the Repository
git clone https://github.com/your-username/placement-eligibility-app.git
cd placement-eligibility-app

# 2. Create Virtual Environment (Optional but Recommended)
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Configure Database

Create a MySQL database (e.g., students_data)

Import your tables and data (students, programming, soft_skills, placements)

# 5. Run the Application
streamlit run app.py


Access the app at http://localhost:8501

# SQL Queries Included

The app includes 10 insightful SQL queries, such as:

Total students

Average programming performance per batch

Top 5 students ready for placement

Placement status distribution

Companies hiring most students

...and more!

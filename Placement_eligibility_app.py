import streamlit as st
import mysql.connector
import pandas as pd

# -----------------------
# DB Helpers
# -----------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Abby@123",
        database="students_data"
    )

def run_sql(sql: str, params=None) -> pd.DataFrame:
    conn = get_connection()
    try:
        df = pd.read_sql(sql, conn, params=params)
    finally:
        conn.close()
    return df

def get_batches() -> list:
    sql = "SELECT DISTINCT course_batch FROM students ORDER BY course_batch;"
    df = run_sql(sql)
    return df["course_batch"].dropna().tolist()

def soft_avg_expr(alias="soft_skills_avg"):
    # Average of 6 soft-skill columns
    return f"""ROUND(
        (ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6, 2
    ) AS {alias}"""

st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("📌 Placement Eligibility App")

# -----------------------
# Tabs
# -----------------------
tab1, tab2 = st.tabs(["🎯 Eligibility Finder (Step 3)", "📊 Insights (Step 4)"])

# ======================================================
# TAB 1: Eligibility Finder (Step 3)
# ======================================================
with tab1:
    st.subheader("Set your eligibility criteria")

    left, right = st.columns(2)
    with left:
        min_problems = st.number_input("Min Problems Solved", min_value=0, value=50, step=5)
        min_soft_avg = st.number_input("Min Soft Skills Average (0–100)", min_value=0, max_value=100, value=75, step=5)
        min_mock = st.number_input("Min Mock Interview Score (0–100)", min_value=0, max_value=100, value=60, step=5)
    with right:
        batches = get_batches()
        selected_batches = st.multiselect("Filter by Batch (optional)", batches, default=batches)
        lang = st.selectbox("Programming Language (optional)", ["Any", "Python", "SQL", "Java"])
        pstatus = st.selectbox("Placement Status (optional)", ["Any", "Ready", "Not Ready", "Placed"])

    if st.button("🔎 Find Eligible Students"):
        # Build parameterized SQL
        sql = f"""
            SELECT s.student_id, s.name, s.age, s.gender, s.email, s.phone,
                   s.course_batch, p.language,
                   p.problems_solved, p.assessments_completed, p.mini_projects, p.latest_project_score,
                   {soft_avg_expr('soft_avg')},
                   pl.mock_interview_score, pl.internships_completed, pl.placement_status
            FROM students s
            JOIN programming p ON s.student_id = p.student_id
            JOIN soft_skills ss ON s.student_id = ss.student_id
            JOIN placements pl ON s.student_id = pl.student_id
            WHERE p.problems_solved >= %s
              AND ((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6) >= %s
              AND pl.mock_interview_score >= %s
        """
        params = [min_problems, min_soft_avg, min_mock]

        # Optional filters
        if selected_batches and len(selected_batches) > 0:
            placeholders = ",".join(["%s"] * len(selected_batches))
            sql += f" AND s.course_batch IN ({placeholders})"
            params.extend(selected_batches)

        if lang != "Any":
            sql += " AND p.language = %s"
            params.append(lang)

        if pstatus != "Any":
            sql += " AND pl.placement_status = %s"
            params.append(pstatus)

        sql += " ORDER BY pl.mock_interview_score DESC, p.problems_solved DESC;"

        df = run_sql(sql, params)

        st.success(f"✅ Found {len(df)} eligible students")
        st.dataframe(df, use_container_width=True)

        # Quick summary by batch
        if not df.empty and "course_batch" in df.columns:
            st.markdown("**Eligible count by batch**")
            by_batch = df.groupby("course_batch")["student_id"].count().rename("eligible_count").reset_index()
            st.bar_chart(by_batch.set_index("course_batch"))

        # Download
        if not df.empty:
            st.download_button(
                "⬇️ Download Results (CSV)",
                df.to_csv(index=False).encode("utf-8"),
                file_name="eligible_students.csv",
                mime="text/csv",
            )

# ======================================================
# TAB 2: Insights (Step 4) – 10 SQL Queries
# ======================================================
# ======================================================
# TAB 2: Insights (Step 4) – Updated 10 SQL Queries
# ======================================================
with tab2:
    st.subheader("Insights Dashboard")

    st.markdown("---")
    st.markdown("### 1) Total number of students")
    sql1 = """
        SELECT COUNT(*) AS total_students
        FROM students;
    """
    st.dataframe(run_sql(sql1), use_container_width=True)

    st.markdown("### 2) Average programming performance per batch")
    sql2 = """
        SELECT s.course_batch,
               AVG(p.problems_solved) AS avg_problems_solved,
               AVG(p.assessments_completed) AS avg_assessments,
               AVG(p.latest_project_score) AS avg_project_score
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        GROUP BY s.course_batch;
    """
    df2 = run_sql(sql2)
    st.dataframe(df2, use_container_width=True)
    if not df2.empty:
        st.bar_chart(df2.set_index("course_batch")[["avg_problems_solved", "avg_project_score"]])

    st.markdown("### 3) Top 5 students ready for placement")
    sql3 = """
        SELECT s.name, pl.mock_interview_score, pl.internships_completed
        FROM students s
        JOIN placements pl ON s.student_id = pl.student_id
        ORDER BY pl.mock_interview_score DESC
        LIMIT 5;
    """
    st.dataframe(run_sql(sql3), use_container_width=True)

    st.markdown("### 4) Distribution of soft skills scores (average per skill)")
    sql4 = """
        SELECT AVG(communication) AS avg_communication,
               AVG(teamwork) AS avg_teamwork,
               AVG(presentation) AS avg_presentation,
               AVG(leadership) AS avg_leadership,
               AVG(critical_thinking) AS avg_critical_thinking,
               AVG(interpersonal_skills) AS avg_interpersonal
        FROM soft_skills;
    """
    st.dataframe(run_sql(sql4), use_container_width=True)

    st.markdown("### 5) Students with highest programming certifications")
    sql5 = """
        SELECT s.name, p.certifications_earned
        FROM students s
        JOIN programming p ON s.student_id = p.student_id
        ORDER BY p.certifications_earned DESC
        LIMIT 10;
    """
    st.dataframe(run_sql(sql5), use_container_width=True)

    st.markdown("### 6) Total placed vs not placed students")
    sql6 = """
        SELECT placement_status, COUNT(*) AS total_students
        FROM placements
        GROUP BY placement_status;
    """
    df6 = run_sql(sql6)
    st.dataframe(df6, use_container_width=True)
    if not df6.empty:
        st.bar_chart(df6.set_index("placement_status"))

    st.markdown("### 7) Average placement package per batch")
    sql7 = """
        SELECT s.course_batch,
               AVG(pl.placement_package) AS avg_package
        FROM students s
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE pl.placement_status = 'Placed'
        GROUP BY s.course_batch;
    """
    df7 = run_sql(sql7)
    st.dataframe(df7, use_container_width=True)
    if not df7.empty:
        st.bar_chart(df7.set_index("course_batch"))

    st.markdown("### 8) Students with no internships completed")
    sql8 = """
        SELECT s.name, s.email, pl.internships_completed
        FROM students s
        JOIN placements pl ON s.student_id = pl.student_id
        WHERE pl.internships_completed = 0;
    """
    st.dataframe(run_sql(sql8), use_container_width=True)

    st.markdown("### 9) Students eligible based on soft skills (≥70 in 3 key skills)")
    sql9 = """
        SELECT s.name, ss.communication, ss.teamwork, ss.presentation
        FROM students s
        JOIN soft_skills ss ON s.student_id = ss.student_id
        WHERE ss.communication >= 70
          AND ss.teamwork >= 70
          AND ss.presentation >= 70;
    """
    st.dataframe(run_sql(sql9), use_container_width=True)

    st.markdown("### 10) Companies that hired the most students")
    sql10 = """
        SELECT company_name, COUNT(*) AS total_hired
        FROM placements
        WHERE placement_status = 'Placed'
        GROUP BY company_name
        ORDER BY total_hired DESC
        LIMIT 5;
    """
    st.dataframe(run_sql(sql10), use_container_width=True)

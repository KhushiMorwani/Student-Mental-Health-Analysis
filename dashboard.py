# =================================================
# dashboard.py
# PURPOSE: Complete analytics dashboard showing
#          all student mental health data,
#          charts, filters and individual search.
# HOW TO RUN: streamlit run dashboard.py
# =================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Fix path so Python can find config and src folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.db_connection import get_connection, close_connection
from src.data_loader import load_combined_data
from src.data_cleaner import clean_pipeline
from config.config import SCORING_WEIGHTS, RISK_THRESHOLDS


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title="Student Mental Health Dashboard",
    page_icon="SMH",
    layout="wide"
)


# =================================================
# SCORING FUNCTIONS
# =================================================

def normalize_positive(value, min_val, max_val):
    if max_val == min_val:
        return 0.5
    return float(np.clip(
        (value - min_val) / (max_val - min_val), 0.0, 1.0
    ))


def normalize_negative(value, min_val, max_val):
    if max_val == min_val:
        return 0.5
    return float(np.clip(
        1.0 - (value - min_val) / (max_val - min_val), 0.0, 1.0
    ))


def compute_score(row):
    w = SCORING_WEIGHTS
    score = (
        normalize_positive(row['sleep_hours'],     4.0, 10.0) * w['sleep_hours']       +
        normalize_positive(row['exercise_days'],   0,   7)    * w['exercise_days']     +
        normalize_positive(row['family_support'],  1,   10)   * w['family_support']    +
        normalize_positive(row['mood_rating'],     1,   10)   * w['mood_rating']       +
        normalize_negative(row['stress_level'],    1,   10)   * w['stress_level']      +
        normalize_negative(row['anxiety_level'],   1,   10)   * w['anxiety_level']     +
        normalize_negative(row['depression_score'],1,   10)   * w['depression_score']  +
        normalize_negative(row['screen_time_hours'],1,  12)   * w['screen_time_hours']
    )
    return round(float(np.clip(score, 0.0, 100.0)), 2)


def classify_risk(score):
    if score >= RISK_THRESHOLDS['healthy']:
        return 'Healthy'
    elif score >= RISK_THRESHOLDS['moderate']:
        return 'Moderate Risk'
    else:
        return 'High Risk'


# =================================================
# LOAD AND PREPARE DATA
# =================================================

@st.cache_data
def load_data():
    """
    Loads data from MySQL, cleans it and computes scores.
    @st.cache_data means this runs only once —
    makes dashboard much faster.
    """
    df_raw = load_combined_data()
    if df_raw is None:
        return None
    df = clean_pipeline(df_raw)
    df['mental_health_score'] = df.apply(compute_score, axis=1)
    df['risk_category'] = df['mental_health_score'].apply(classify_risk)
    return df


# Load data
df = load_data()

if df is None:
    st.error("Cannot connect to database. Check config.py settings.")
    st.stop()


# =================================================
# SIDEBAR NAVIGATION
# =================================================

with st.sidebar:
    st.markdown("# Mental Health")
    st.markdown("# Dashboard")
    st.markdown("---")

    page = st.radio(
        "Navigate to",
        [
            " Overview",
            " Student Table",
            " Charts",
            " Student Search",
        ]
    )

    st.markdown("---")

    # Sidebar filters
    st.markdown("## Filters")

    selected_risk = st.multiselect(
        "Filter by Risk Category",
        options=['Healthy', 'Moderate Risk', 'High Risk'],
        default=['Healthy', 'Moderate Risk', 'High Risk']
    )

    selected_course = st.multiselect(
        "Filter by Course",
        options=sorted(df['course'].unique().tolist()),
        default=sorted(df['course'].unique().tolist())
    )

    st.markdown("---")
    st.markdown("##  Risk Categories")
    st.markdown(" **Healthy** → Score ≥ 70")
    st.markdown(" **Moderate** → Score 40–69")
    st.markdown(" **High Risk** → Score < 40")
    st.markdown("---")
    st.caption("Built with Python · MySQL · Streamlit")


# Apply filters
df_filtered = df[
    (df['risk_category'].isin(selected_risk)) &
    (df['course'].isin(selected_course))
]


# =================================================
# PAGE 1 — OVERVIEW
# =================================================

if page == " Overview":

    st.title(" Student Mental Health Overview")
    st.markdown("---")

    # Metrics row
    total     = len(df)
    healthy   = len(df[df['risk_category'] == 'Healthy'])
    moderate  = len(df[df['risk_category'] == 'Moderate Risk'])
    high_risk = len(df[df['risk_category'] == 'High Risk'])
    avg_score = df['mental_health_score'].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(" Total Students", total)
    with col2:
        st.metric(" Healthy", healthy)
    with col3:
        st.metric(" Moderate Risk", moderate)
    with col4:
        st.metric(" High Risk", high_risk)
    with col5:
        st.metric(" Avg Score", f"{avg_score:.1f}")

    st.markdown("---")

    # Two charts side by side
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Risk Distribution")
        risk_counts = df['risk_category'].value_counts().reset_index()
        risk_counts.columns = ['Risk Category', 'Count']
        colors = {
            'Healthy':       '#2ecc71',
            'Moderate Risk': '#f39c12',
            'High Risk':     '#e74c3c'
        }
        fig_pie = px.pie(
            risk_counts,
            names='Risk Category',
            values='Count',
            color='Risk Category',
            color_discrete_map=colors,
            hole=0.4
        )
        fig_pie.update_layout(showlegend=True, height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.markdown("### Average Score by Course")
        course_avg = df.groupby('course')['mental_health_score'].mean().round(1)
        course_avg = course_avg.sort_values(ascending=True).reset_index()
        course_avg.columns = ['Course', 'Average Score']
        fig_bar = px.bar(
            course_avg,
            x='Average Score',
            y='Course',
            orientation='h',
            color='Average Score',
            color_continuous_scale='RdYlGn',
            range_color=[0, 100]
        )
        fig_bar.update_layout(height=350)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # Parameter averages
    st.markdown("###  Average Parameter Values")
    params = {
        " Sleep Hours":      round(df['sleep_hours'].mean(), 1),
        " Stress Level":     round(df['stress_level'].mean(), 1),
        " Anxiety Level":    round(df['anxiety_level'].mean(), 1),
        " Depression Score": round(df['depression_score'].mean(), 1),
        " Exercise Days":    round(df['exercise_days'].mean(), 1),
        " Family Support": round(df['family_support'].mean(), 1),
        " Screen Time":      round(df['screen_time_hours'].mean(), 1),
        " Mood Rating":      round(df['mood_rating'].mean(), 1),
    }
    p1, p2, p3, p4 = st.columns(4)
    cols = [p1, p2, p3, p4]
    for i, (param, value) in enumerate(params.items()):
        with cols[i % 4]:
            st.metric(param, value)


# =================================================
# PAGE 2 — STUDENT TABLE
# =================================================

elif page == " Student Table":

    st.title(" Student Data Table")
    st.markdown("---")

    st.markdown(
        f"Showing **{len(df_filtered)}** students "
        f"out of **{len(df)}** total"
    )

    def risk_symbol(risk):
        if risk == 'Healthy':
            return '🟢 Healthy'
        elif risk == 'Moderate Risk':
            return '🟡 Moderate Risk'
        else:
            return '🔴 High Risk'

    df_display = df_filtered[[
        'name', 'course', 'year_of_study', 'cgpa',
        'sleep_hours', 'stress_level', 'anxiety_level',
        'depression_score', 'exercise_days', 'family_support',
        'screen_time_hours', 'mood_rating',
        'mental_health_score', 'risk_category'
    ]].copy()

    df_display['risk_category'] = df_display['risk_category'].apply(risk_symbol)
    df_display.columns = [
        'Name', 'Course', 'Year', 'CGPA',
        'Sleep', 'Stress', 'Anxiety', 'Depression',
        'Exercise', 'Family Support', 'Screen Time', 'Mood',
        'Score', 'Risk Category'
    ]
    df_display = df_display.sort_values('Score', ascending=True)

    st.dataframe(df_display, use_container_width=True, height=500)

    st.markdown("---")

    csv = df_display.to_csv(index=False)
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="student_mental_health_scores.csv",
        mime="text/csv"
    )


# =================================================
# PAGE 3 — CHARTS
# =================================================

elif page == " Charts":

    st.title(" Mental Health Analytics")
    st.markdown("---")

    # Chart 1 — Score distribution
    st.markdown("### Score Distribution")
    fig_hist = px.histogram(
        df,
        x='mental_health_score',
        nbins=20,
        color='risk_category',
        color_discrete_map={
            'Healthy':       '#2ecc71',
            'Moderate Risk': '#f39c12',
            'High Risk':     '#e74c3c'
        },
        labels={
            'mental_health_score': 'Mental Health Score',
            'risk_category':       'Risk Category'
        }
    )
    fig_hist.update_layout(height=400)
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # Chart 2 and 3
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Average Stress by Course")
        stress_course = df.groupby('course')['stress_level'].mean().round(1)
        stress_course = stress_course.sort_values(ascending=False).reset_index()
        stress_course.columns = ['Course', 'Avg Stress']
        fig_stress = px.bar(
            stress_course,
            x='Course',
            y='Avg Stress',
            color='Avg Stress',
            color_continuous_scale='Reds',
            range_color=[0, 10]
        )
        fig_stress.update_layout(height=350, xaxis_tickangle=45)
        st.plotly_chart(fig_stress, use_container_width=True)

    with col_right:
        st.markdown("### Average Sleep by Course")
        sleep_course = df.groupby('course')['sleep_hours'].mean().round(1)
        sleep_course = sleep_course.sort_values(ascending=False).reset_index()
        sleep_course.columns = ['Course', 'Avg Sleep']
        fig_sleep = px.bar(
            sleep_course,
            x='Course',
            y='Avg Sleep',
            color='Avg Sleep',
            color_continuous_scale='Blues',
            range_color=[4, 10]
        )
        fig_sleep.update_layout(height=350, xaxis_tickangle=45)
        st.plotly_chart(fig_sleep, use_container_width=True)

    st.markdown("---")

    # Chart 4 — Gender comparison
    st.markdown("### Gender Based Comparison")
    gender_params = df.groupby('gender')[[
        'stress_level', 'anxiety_level', 'depression_score',
        'sleep_hours', 'mood_rating', 'mental_health_score'
    ]].mean().round(2).reset_index()

    fig_gender = px.bar(
        gender_params.melt(
            id_vars='gender',
            var_name='Parameter',
            value_name='Average'
        ),
        x='Parameter',
        y='Average',
        color='gender',
        barmode='group',
        labels={'gender': 'Gender'}
    )
    fig_gender.update_layout(height=400, xaxis_tickangle=20)
    st.plotly_chart(fig_gender, use_container_width=True)

    st.markdown("---")

    # Chart 5 — Top 10 at risk
    st.markdown("###  Top 10 Most At Risk Students")
    top_risk = df.nsmallest(10, 'mental_health_score')[[
        'name', 'mental_health_score', 'risk_category', 'course'
    ]]
    fig_risk = px.bar(
        top_risk,
        x='mental_health_score',
        y='name',
        orientation='h',
        color='mental_health_score',
        color_continuous_scale='RdYlGn',
        range_color=[0, 100],
        labels={
            'mental_health_score': 'Score',
            'name': 'Student'
        }
    )
    fig_risk.update_layout(height=400)
    st.plotly_chart(fig_risk, use_container_width=True)


# =================================================
# PAGE 4 — STUDENT SEARCH
# =================================================

elif page == " Student Search":

    st.title(" Search Individual Student")
    st.markdown("---")

    search_name = st.selectbox(
        "Select a student",
        options=sorted(df['name'].unique().tolist()),
        index=0
    )

    if search_name:
        student  = df[df['name'] == search_name].iloc[0]
        score    = student['mental_health_score']
        risk     = student['risk_category']

        if risk == 'Healthy':
            symbol = '🟢'
        elif risk == 'Moderate Risk':
            symbol = '🟡'
        else:
            symbol = '🔴'

        st.markdown(f"## {symbol} {student['name']}")

        # Basic info
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Course", student['course'])
        with c2:
            st.metric("Year", f"Year {student['year_of_study']}")
        with c3:
            st.metric("CGPA", student['cgpa'])

        st.markdown("---")

        # Score and risk
        sc, rc = st.columns(2)
        with sc:
            st.metric("Mental Health Score", f"{score} / 100")
        with rc:
            st.metric("Risk Category", f"{symbol} {risk}")

        st.progress(int(score))
        st.markdown("---")

        # Parameters
        st.markdown("### 📋 Parameter Details")
        pc1, pc2 = st.columns(2)

        with pc1:
            st.markdown("** Positive Factors**")
            st.write(f" Sleep Hours      : {student['sleep_hours']} hrs")
            st.write(f" Exercise Days    : {student['exercise_days']} days/week")
            st.write(f" Family Support  : {student['family_support']} / 10")
            st.write(f" Mood Rating      : {student['mood_rating']} / 10")

        with pc2:
            st.markdown("** Negative Factors**")
            st.write(f" Stress Level     : {student['stress_level']} / 10")
            st.write(f" Anxiety Level    : {student['anxiety_level']} / 10")
            st.write(f" Depression Score : {student['depression_score']} / 10")
            st.write(f" Screen Time      : {student['screen_time_hours']} hrs/day")

        st.markdown("---")

        # Radar chart
        st.markdown("###  Parameter Radar Chart")
        categories = [
            'Sleep', 'Exercise', 'Family Support', 'Mood',
            'Stress', 'Anxiety', 'Depression', 'Screen Time'
        ]
        values = [
            student['sleep_hours'] / 10 * 10,
            student['exercise_days'] / 7 * 10,
            student['family_support'],
            student['mood_rating'],
            student['stress_level'],
            student['anxiety_level'],
            student['depression_score'],
            student['screen_time_hours'] / 12 * 10
        ]
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line_color='#3498db'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Risk message
        if risk == 'Healthy':
            st.success(
                f"🟢 {student['name']} is in good mental health. "
                f"Encourage them to maintain their current lifestyle."
            )
        elif risk == 'Moderate Risk':
            st.warning(
                f"🟡 {student['name']} needs attention. "
                f"A counselor follow-up is recommended."
            )
        else:
            st.error(
                f"🔴 {student['name']} is at high risk. "
                f"Immediate counseling support is strongly recommended."
            )
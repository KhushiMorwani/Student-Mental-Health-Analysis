# =================================================
# app.py
# PURPOSE: Streamlit web app where users can enter
#          their mental health data and get their
#          score and risk category instantly.
# HOW TO RUN: streamlit run app.py
# =================================================

import streamlit as st
import numpy as np
import sys
import os

# Fix path so Python can find config folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

SCORING_WEIGHTS = {
    "sleep_hours":       15,
    "exercise_days":     10,
    "family_support":    15,
    "mood_rating":       10,
    "stress_level":      15,
    "anxiety_level":     15,
    "depression_score":  15,
    "screen_time_hours":  5
}

RISK_THRESHOLDS = {
    "healthy":  70,
    "moderate": 40
}


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title="Student Mental Health Analyzer",
    page_icon="🧠",
    layout="centered"
)


# =================================================
# SCORING FUNCTIONS
# (Same logic as scoring_engine.py)
# =================================================

def normalize_positive(value, min_val, max_val):
    """Higher value = better score."""
    if max_val == min_val:
        return 0.5
    result = (value - min_val) / (max_val - min_val)
    return float(np.clip(result, 0.0, 1.0))


def normalize_negative(value, min_val, max_val):
    """Higher value = worse score (inverted)."""
    if max_val == min_val:
        return 0.5
    result = 1.0 - (value - min_val) / (max_val - min_val)
    return float(np.clip(result, 0.0, 1.0))


def compute_score(sleep, stress, anxiety, depression,
                  exercise, support, screen, mood):
    """
    Computes mental health score from 8 parameters.
    Returns score between 0 and 100.
    """
    w = SCORING_WEIGHTS

    score = (
        normalize_positive(sleep,    4.0, 10.0) * w['sleep_hours']       +
        normalize_positive(exercise, 0,   7)    * w['exercise_days']     +
        normalize_positive(support,  1,   10)   * w['family_support']    +
        normalize_positive(mood,     1,   10)   * w['mood_rating']       +
        normalize_negative(stress,   1,   10)   * w['stress_level']      +
        normalize_negative(anxiety,  1,   10)   * w['anxiety_level']     +
        normalize_negative(depression, 1, 10)   * w['depression_score']  +
        normalize_negative(screen,   1,   12)   * w['screen_time_hours']
    )

    return round(float(np.clip(score, 0.0, 100.0)), 2)


def classify_risk(score):
    """Classifies score into risk category."""
    if score >= RISK_THRESHOLDS['healthy']:
        return 'Healthy', '🟢'
    elif score >= RISK_THRESHOLDS['moderate']:
        return 'Moderate Risk', '🟡'
    else:
        return 'High Risk', '🔴'


def get_advice(risk_category):
    """Returns advice based on risk category."""
    if risk_category == 'Healthy':
        return [
            "✅ Keep maintaining your sleep schedule",
            "✅ Continue your exercise routine",
            "✅ Stay connected with family and friends",
            "✅ Keep monitoring your mental health regularly"
        ]
    elif risk_category == 'Moderate Risk':
        return [
            "⚠️ Try to sleep at least 7-8 hours daily",
            "⚠️ Exercise at least 3-4 days per week",
            "⚠️ Reduce screen time before bedtime",
            "⚠️ Talk to a friend or family member about stress",
            "⚠️ Consider speaking with a counselor"
        ]
    else:
        return [
            "🚨 Please speak with a counselor immediately",
            "🚨 Reach out to a trusted family member today",
            "🚨 Reduce screen time significantly",
            "🚨 Start with small walks daily for mental relief",
            "🚨 Remember — asking for help is a sign of strength"
        ]


# =================================================
# APP HEADER
# =================================================

st.title("🧠 Student Mental Health Analyzer")
st.markdown("### Find out your mental health score instantly")
st.markdown("---")
st.markdown(
    "Fill in your details below and click **Analyze** "
    "to get your personalized mental health score."
)


# =================================================
# INPUT FORM
# =================================================

st.markdown("## 📋 Enter Your Details")

# Name input
name = st.text_input(
    "Your Name",
    placeholder="Enter your name here"
)

st.markdown("---")

# Two column layout for sliders
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 😴 Sleep & Exercise")

    sleep = st.slider(
        "Sleep Hours per night",
        min_value=4.0,
        max_value=10.0,
        value=7.0,
        step=0.5,
        help="How many hours do you sleep on average?"
    )

    exercise = st.slider(
        "Exercise Days per week",
        min_value=0,
        max_value=7,
        value=3,
        help="How many days per week do you exercise?"
    )

    screen = st.slider(
        "Screen Time Hours per day",
        min_value=1.0,
        max_value=12.0,
        value=4.0,
        step=0.5,
        help="Total hours spent on phone/laptop/TV daily"
    )

    mood = st.slider(
        "Mood Rating",
        min_value=1,
        max_value=10,
        value=5,
        help="How would you rate your overall mood? (1=Very Bad, 10=Excellent)"
    )

with col2:
    st.markdown("### 😰 Stress & Mental Health")

    stress = st.slider(
        "Stress Level",
        min_value=1,
        max_value=10,
        value=5,
        help="How stressed do you feel? (1=No stress, 10=Extreme stress)"
    )

    anxiety = st.slider(
        "Anxiety Level",
        min_value=1,
        max_value=10,
        value=5,
        help="How anxious do you feel? (1=No anxiety, 10=Extreme anxiety)"
    )

    depression = st.slider(
        "Depression Score",
        min_value=1,
        max_value=10,
        value=5,
        help="How depressed do you feel? (1=Not at all, 10=Extremely)"
    )

    support = st.slider(
        "Family Support",
        min_value=1,
        max_value=10,
        value=5,
        help="How much support do you get from family? (1=No support, 10=Full support)"
    )

st.markdown("---")


# =================================================
# ANALYZE BUTTON
# =================================================

if st.button("🔍 Analyze My Mental Health", use_container_width=True):

    # Check if name is entered
    if not name.strip():
        st.warning("⚠️ Please enter your name before analyzing.")

    else:
        # Compute score
        score = compute_score(
            sleep, stress, anxiety, depression,
            exercise, support, screen, mood
        )

        # Classify risk
        risk_category, symbol = classify_risk(score)

        # Get advice
        advice_list = get_advice(risk_category)

        st.markdown("---")
        st.markdown(f"## 📊 Results for {name}")

        # Score display
        col_score, col_risk = st.columns(2)

        with col_score:
            st.metric(
                label="Mental Health Score",
                value=f"{score} / 100"
            )

        with col_risk:
            st.metric(
                label="Risk Category",
                value=f"{symbol} {risk_category}"
            )

        # Progress bar
        st.markdown("### Score Visualization")
        st.progress(int(score))

        # Color coded result box
        if risk_category == 'Healthy':
            st.success(
                f"🟢 **{name}**, your mental health score is "
                f"**{score}/100**. You are in the **Healthy** category. "
                f"Keep up the great habits!"
            )
        elif risk_category == 'Moderate Risk':
            st.warning(
                f"🟡 **{name}**, your mental health score is "
                f"**{score}/100**. You are in the **Moderate Risk** category. "
                f"Some areas need attention."
            )
        else:
            st.error(
                f"🔴 **{name}**, your mental health score is "
                f"**{score}/100**. You are in the **High Risk** category. "
                f"Please seek support immediately."
            )

        # Parameter breakdown
        st.markdown("### 📈 Your Parameter Breakdown")

        breakdown_col1, breakdown_col2 = st.columns(2)

        with breakdown_col1:
            st.markdown("**Positive Factors**")
            st.write(f"😴 Sleep Hours       : {sleep} hrs")
            st.write(f"🏃 Exercise Days     : {exercise} days/week")
            st.write(f"👨‍👩‍👧 Family Support   : {support} / 10")
            st.write(f"😊 Mood Rating       : {mood} / 10")

        with breakdown_col2:
            st.markdown("**Negative Factors**")
            st.write(f"😰 Stress Level      : {stress} / 10")
            st.write(f"😟 Anxiety Level     : {anxiety} / 10")
            st.write(f"😔 Depression Score  : {depression} / 10")
            st.write(f"📱 Screen Time       : {screen} hrs/day")

        # Advice section
        st.markdown("### 💡 Personalized Recommendations")
        for advice in advice_list:
            st.markdown(advice)

        st.markdown("---")
        st.caption(
            "⚠️ Note: This tool is for awareness purposes only. "
            "It is not a medical diagnosis. "
            "Please consult a professional for medical advice."
        )


# =================================================
# SIDEBAR — About the project
# =================================================

with st.sidebar:
    st.markdown("## 📌 About This App")
    st.markdown(
        "This app analyzes student mental health "
        "using 8 behavioral parameters and computes "
        "a score from 0 to 100."
    )

    st.markdown("---")
    st.markdown("## 🎯 Risk Categories")
    st.markdown("🟢 **Healthy** → Score ≥ 70")
    st.markdown("🟡 **Moderate Risk** → Score 40–69")
    st.markdown("🔴 **High Risk** → Score < 40")

    st.markdown("---")
    st.markdown("## ⚖️ Parameter Weights")
    st.markdown("😴 Sleep Hours       → 15%")
    st.markdown("😰 Stress Level      → 15%")
    st.markdown("😟 Anxiety Level     → 15%")
    st.markdown("😔 Depression Score  → 15%")
    st.markdown("👨‍👩‍👧 Family Support   → 15%")
    st.markdown("🏃 Exercise Days     → 10%")
    st.markdown("😊 Mood Rating       → 10%")
    st.markdown("📱 Screen Time       →  5%")

    st.markdown("---")
    st.caption("Built with Python · MySQL · Streamlit")
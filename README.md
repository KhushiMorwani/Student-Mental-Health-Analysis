# 🧠 Student Mental Health Analysis System

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?style=for-the-badge&logo=mysql)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?style=for-the-badge&logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0-red?style=for-the-badge&logo=streamlit)

---

##  Overview

An end-to-end Data Analytics project that analyzes student mental health
using 8 behavioral parameters. The system computes a custom mental health
score for each student and classifies them as **Healthy**,
**Moderate Risk** or **High Risk** — helping university counselors
identify and support at-risk students early.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| MySQL | Database design and storage |
| Python | Data processing and scoring |
| Pandas | Data cleaning and analysis |
| Streamlit | Interactive dashboard and user app |
| Plotly | Charts and visualizations |

---

## 🧠Mental Health Parameters

| Parameter | Type | Effect |
|---|---|---|
|  Sleep Hours | Positive | More = better score |
|  Exercise Days | Positive | More = better score |
|  Family Support | Positive | More = better score |
|  Mood Rating | Positive | More = better score |
|  Stress Level | Negative | Less = better score |
|  Anxiety Level | Negative | Less = better score |
|  Depression Score | Negative | Less = better score |
|  Screen Time | Negative | Less = better score |

---

##  Risk Categories

| Category | Score | Action |
|---|---|---|
| 🟢 Healthy | ≥ 70 | No intervention needed |
| 🟡 Moderate Risk | 40–69 | Counselor follow-up |
| 🔴 High Risk | < 40 | Immediate support needed |

---

## 📁 Project Structure
student_mental_health/
├── config/              ← DB credentials and constants
├── database/            ← SQL schema, data and queries
├── src/                 ← Python modules
│   ├── db_connection.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── eda.py
│   └── scoring_engine.py
├── reports/             ← Output CSV files
├── app.py               ← User input Streamlit app
├── dashboard.py         ← Analytics dashboard
└── requirements.txt

---

##  Setup Instructions

### Step 1 — Clone the repo
```bash
git clone https://github.com/KhushiMorwani/Student-Mental-Health-Analysis.git
cd Student-Mental-Health-Analysis
```

### Step 2 — Install packages
```bash
pip install -r requirements.txt
```

### Step 3 — Configure database
```bash
# Copy and fill in your MySQL password
cp config/config.example.py config/config.py
```

### Step 4 — Setup MySQL
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p mental_health_db < database/insert_data.sql
```

### Step 5 — Run pipeline
```bash
python src/scoring_engine.py
```

### Step 6 — Launch apps
```bash
# Analytics dashboard
streamlit run dashboard.py

# User input app
streamlit run app.py
```

---

## 📊 Dashboard Pages

| Page | Features |
|---|---|
|  Overview | Risk counts · Avg score · Charts |
|  Student Table | Full data · Filters · Download CSV |
|  Charts | Score distribution · Course analytics |
|  Student Search | Individual profile · Radar chart |

---

##  Author

**Khushi Morwani**


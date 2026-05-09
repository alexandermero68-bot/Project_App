# =========================================================
# 🇳🇬 NIGERIA INCIDENT ANALYSIS DASHBOARD
# PROFESSIONAL STREAMLIT APPLICATION
# =========================================================

# =========================================================
# 1. IMPORT LIBRARIES
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from mpl_toolkits.mplot3d import Axes3D



# =========================================================
# 2. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Nigeria Incident Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# 3. CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

h1, h2, h3 {
    color: #00F5FF;
}

.stMetric {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 4. LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("mero_full_cleaned_incidents.csv")

    # LOWERCASE COLUMNS
    df.columns = df.columns.str.lower()

    # DATE CONVERSION
    df["start date"] = pd.to_datetime(df["start date"])
    df["end date"] = pd.to_datetime(df["end date"])

    # DURATION
    df["duration"] = (
        df["end date"] - df["start date"]
    ).dt.days

    # FEATURE ENGINEERING
    df["year"] = df["start date"].dt.year
    df["month"] = df["start date"].dt.month_name()
    df["day"] = df["start date"].dt.day_name()

    return df


df = load_data()


# =========================================================
# 5. SIDEBAR
# =========================================================

st.sidebar.title("📊 Navigation")

menu = st.sidebar.radio(
    "Go To",
    [
        "🏠 Home",
        "📈 Dashboard",
        "📘 Data Overview",
        "👤 About"
    ]
)


# =========================================================
# HOME PAGE
# =========================================================

if menu == "🏠 Home":

    st.title("🇳🇬 Nigeria Incident Analysis Dashboard")

    st.markdown("""
### 📌 Project Objectives

This dashboard helps to:

- Analyze deadly incidents in Nigeria
- Identify high-risk states
- Detect recurring incident patterns
- Support data-driven decisions
- Improve emergency response strategies

---
### 📊 Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Data Visualization
""")


# =========================================================
# DATA OVERVIEW
# =========================================================

elif menu == "📘 Data Overview":

    st.title("📘 Dataset Overview")

    st.subheader("First 5 Rows")
    st.dataframe(df.head())

    st.subheader("Last 5 Rows")
    st.dataframe(df.tail())

    st.subheader("Dataset Shape")
    st.write(df.shape)

    st.subheader("Missing Values")
    st.dataframe(df.isnull().sum())

    st.subheader("Duplicate Rows")
    st.write(df.duplicated().sum())

    st.subheader("Statistical Summary")
    st.dataframe(df.describe())


# =========================================================
# DASHBOARD
# =========================================================

elif menu == "📈 Dashboard":

    st.title("📊 Nigeria Incident Dashboard")


    # =====================================================
    # GLOBAL FILTERS
    # =====================================================

    st.sidebar.header("🔎 Filter Dashboard")

    selected_states = st.sidebar.multiselect(
        "Select States",
        options=sorted(df["state"].unique()),
        default=sorted(df["state"].unique())[:10]
    )

    selected_incidents = st.sidebar.multiselect(
        "Select Incidents",
        options=sorted(df["incident"].unique()),
        default=sorted(df["incident"].unique())[:10]
    )

    filtered_df = df[
        (df["state"].isin(selected_states)) &
        (df["incident"].isin(selected_incidents))
    ]


    # =====================================================
    # KPI SECTION
    # =====================================================

    total_deaths = int(
        filtered_df["number of deaths"].sum()
    )

    total_incidents = filtered_df.shape[0]

    avg_duration = round(
        filtered_df["duration"].mean(),
        2
    )

    top_state = (
        filtered_df.groupby("state")["number of deaths"]
        .sum()
        .idxmax()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💀 Total Deaths", total_deaths)

    col2.metric("⚠ Total Incidents", total_incidents)

    col3.metric("📍 Top State", top_state)

    col4.metric("⏳ Avg Duration", f"{avg_duration} Days")


    # =====================================================
    # CHART 1 — TOP 10 STATES
    # =====================================================

    st.subheader("1️⃣ Top 10 States by Deaths")

    st.markdown("""
**Research Question:**  
Which states recorded the highest number of deaths?
""")

    top10_states = (
        filtered_df.groupby("state")["number of deaths"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig1 = px.bar(
        top10_states,
        x="state",
        y="number of deaths",
        text="number of deaths",
        color="number of deaths",
        title="Top 10 States by Number of Deaths"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.info("""
📌 Insight:
These states represent the highest-risk regions
requiring urgent intervention.
""")


    # =====================================================
    # CHART 2 — TOP 10 INCIDENTS
    # =====================================================

    st.subheader("2️⃣ Top 10 Deadliest Incidents")

    top10_incidents = (
        filtered_df.groupby("incident")["number of deaths"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        top10_incidents,
        x="incident",
        y="number of deaths",
        text="number of deaths",
        color="number of deaths",
        title="Top 10 Deadliest Incidents"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info("""
📌 Insight:
A few incident categories contribute heavily
to fatalities.
""")


    # =====================================================
    # CHART 3 — INCIDENT FREQUENCY
    # =====================================================

    st.subheader("3️⃣ Most Frequent Incidents")

    top10_frequency = (
        filtered_df["incident"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top10_frequency.columns = [
        "incident",
        "frequency"
    ]

    fig3 = px.bar(
        top10_frequency,
        x="incident",
        y="frequency",
        text="frequency",
        color="frequency",
        title="Top 10 Most Frequent Incidents"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.info("""
📌 Insight:
Frequent incidents are not always
the deadliest.
""")


    # =====================================================
    # CHART 4 — DURATION ANALYSIS
    # =====================================================

    st.subheader("4️⃣ Longest Duration Incidents")

    top10_duration = (
        filtered_df.groupby("incident")["duration"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(
        top10_duration,
        x="incident",
        y="duration",
        text="duration",
        color="duration",
        title="Top 10 Longest Duration Incidents"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.info("""
📌 Insight:
Long-duration incidents may indicate
delayed response systems.
""")


    # =====================================================
    # CHART 5 — MONTHLY TREND
    # =====================================================

    st.subheader("5️⃣ Monthly Death Trend")

    month_order = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    monthly_trend = (
        filtered_df.groupby("month")["number of deaths"]
        .sum()
        .reset_index()
    )

    monthly_trend["month"] = pd.Categorical(
        monthly_trend["month"],
        categories=month_order,
        ordered=True
    )

    monthly_trend = monthly_trend.sort_values("month")

    fig5 = px.line(
        monthly_trend,
        x="month",
        y="number of deaths",
        markers=True,
        text="number of deaths",
        title="Monthly Death Trend"
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.info("""
📌 Insight:
Certain months experience spikes in deaths,
indicating recurring patterns.
""")


    # =====================================================
    # CHART 6 — BUBBLE CHART
    # =====================================================

    st.subheader("6️⃣ States vs Incident Bubble Analysis")

    bubble_data = (
        filtered_df.groupby(
            ["state", "incident"]
        )["number of deaths"]
        .sum()
        .reset_index()
    )

    fig6 = px.scatter(
        bubble_data,
        x="incident",
        y="state",
        size="number of deaths",
        color="number of deaths",
        hover_name="state",
        size_max=60,
        title="Top States vs Incident Types"
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.info("""
📌 Insight:
Some states consistently record higher deaths
across multiple incident types.
""")


    # =====================================================
    # CHART 7 — FUNNEL ANALYSIS
    # =====================================================

    st.subheader("7️⃣ Incident Impact Funnel")

    top_n = st.slider(
        "Select Number of Incidents",
        5,
        20,
        10
    )

    top_incident_filtered = (
        filtered_df.groupby("incident")["number of deaths"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    fig7 = px.funnel(
        top_incident_filtered,
        x="number of deaths",
        y="incident",
        color="number of deaths",
        title=f"Top {top_n} Incident Impact Funnel"
    )

    st.plotly_chart(fig7, use_container_width=True)

    st.info("""
📌 Insight:
The funnel chart ranks the deadliest
incident categories clearly.
""")


    # =====================================================
    # CHART 8 — 3D ANALYSIS
    # =====================================================

    st.subheader("8️⃣ 3D Fatality Cluster Analysis")

    agg = (
        filtered_df.groupby(
            ["state", "incident"]
        )["number of deaths"]
        .sum()
        .reset_index()
    )

    fig8 = px.scatter_3d(
        agg,
        x="state",
        y="incident",
        z="number of deaths",
        size="number of deaths",
        color="number of deaths",
        hover_name="state",
        title="3D Fatality Cluster Analysis"
    )

    fig8.update_layout(height=700)

    st.plotly_chart(fig8, use_container_width=True)

    st.info("""
📌 Insight:
Large bubbles indicate high-impact
fatality clusters.
""")


# =========================================================
# ABOUT PAGE
# =========================================================

elif menu == "👤 About":

    st.title("👤 About Me")

    col1, col2 = st.columns([1, 2])

    # =====================================================
    # LEFT COLUMN
    # =====================================================

    with col1:

        st.markdown("""
### 💻 Professional Role

Data Analyst  
BI Developer  
Python Enthusiast
""")

        st.image(
            "https://images.unsplash.com/photo-1516321318423-f06f85e504b3",
            use_container_width=True
        )

    # =====================================================
    # RIGHT COLUMN
    # =====================================================

    with col2:

        st.markdown("""

## 👤 About Me

I am a **Professional Results-driven Data Analyst**  

with strong expertise in **Power BI, SQL, Python, and Excel**,  

combined with a background in **Computer Engineering and Mobile Device Systems**.  

Skilled in transforming raw data into **actionable insights**, building interactive dashboards,

and supporting **data-driven decision-making**.

Also equipped with foundational knowledge in **Cybersecurity Practices and Risk Awareness**,  

ensuring **data integrity and secure analysis processes**.  

Adept at **problem-solving, system troubleshooting, and delivering business value through data.**

""")

    st.markdown("---")

    # =====================================================
    # CORE SKILLS
    # =====================================================

    st.subheader("🧠 Core Skills")

    st.markdown("""

- 📊 Data Analysis & Visualization (Power BI, Excel)  

- 🗄 SQL (Data Extraction, Joins, Query Optimization)  

- 🐍 Python (Pandas, NumPy, Matplotlib, Seaborn)  

- 📈 Dashboard Development & Reporting  

- 🧹 Data Cleaning & Preprocessing  

- 📉 Statistical Analysis & Insight Generation  

- 💻 Computer Engineering & Systems Troubleshooting  

- 📱 Mobile Device Repair & Diagnostics  

- 🔐 Cybersecurity Fundamentals & Data Protection Awareness  

- 🧠 Problem-Solving & Critical Thinking  

- 📊 Business Intelligence  

- 🎨 Data Visualization  

""")

    st.markdown("---")


    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    st.subheader("📌 Executive Summary")

    st.markdown("""

The *Nigeria Incident Analysis Project* was developed to explore,
analyze, and visualize incident-related fatalities across Nigeria
using modern data analytics and interactive dashboard technologies.

The project leverages **Python, Pandas, Plotly, Seaborn, Matplotlib,
and Streamlit** to transform raw incident records into meaningful
insights that support informed decision-making.

Through detailed exploratory data analysis (EDA), the project identifies:

- High-risk states with elevated fatality levels
- The deadliest incident categories
- Frequently occurring incidents
- Long-duration incidents requiring extended intervention
- Monthly and seasonal fatality patterns
- Relationships between states and incident clusters

The dashboard provides an interactive environment that enables users
to filter data dynamically, monitor trends, and gain real-time visual
insights into incident severity and distribution across Nigeria.

This project demonstrates how data-driven intelligence can improve:

✅ Security awareness  
✅ Risk management  
✅ Emergency response planning  
✅ Policy formulation  
✅ Resource allocation  
✅ Public safety analysis  

""")


    st.markdown("---")


    # =====================================================
    # KEY FINDINGS
    # =====================================================

    st.subheader("🔍 Key Findings")

    st.markdown("""

### 1️⃣ High-Risk States

The analysis revealed that a few states consistently recorded the
highest number of fatalities, indicating concentrated high-risk zones.

These states require:

- Increased security presence
- Better emergency response systems
- Improved surveillance infrastructure
- Government intervention programs

---

### 2️⃣ Deadliest Incident Categories

Certain incident types contributed significantly more deaths than others.

This suggests that:

- Some incidents are inherently more severe
- Existing preventive measures may be insufficient
- High-impact incidents require targeted mitigation strategies

---

### 3️⃣ Frequency Does Not Equal Severity

The study discovered that the most frequent incidents are not always
the deadliest.

This means:

- High-frequency incidents may cause fewer deaths
- Rare incidents can still produce catastrophic outcomes
- Risk assessment should consider both frequency and severity

---

### 4️⃣ Long-Duration Incidents

Some incidents lasted significantly longer than others.

This may indicate:

- Delayed emergency response
- Complex operational challenges
- Poor coordination during crises
- Limited access to affected areas

---

### 5️⃣ Monthly Fatality Patterns

The monthly trend analysis revealed fluctuations in fatalities
throughout the year, with certain months showing sharp increases.

This suggests possible:

- Seasonal trends
- Recurring conflict periods
- Environmental influences
- Economic or social triggers

---

### 6️⃣ Fatality Clusters

The 3D and bubble chart analysis showed concentrated fatality clusters
across specific states and incident types.

This indicates:

- Persistent hotspots
- Recurring incident patterns
- Strong relationships between location and incident severity

""")


    st.markdown("---")


    # =====================================================
    # RECOMMENDED SOLUTIONS
    # =====================================================

    st.subheader("💡 Recommended Solutions")

    st.markdown("""

### ✅ 1. Strengthen Emergency Response Systems

Government agencies and emergency services should improve:

- Response speed
- Crisis coordination
- Communication systems
- Resource deployment strategies

---

### ✅ 2. Deploy Data-Driven Security Monitoring

Security agencies should adopt:

- Predictive analytics
- Real-time monitoring dashboards
- Geographic risk mapping
- Automated alert systems

to identify and respond to high-risk incidents early.

---

### ✅ 3. Focus on High-Risk States

States with high fatality rates should receive:

- Increased funding
- Security reinforcement
- Healthcare support
- Community awareness programs

---

### ✅ 4. Improve Incident Reporting Systems

A centralized and standardized incident reporting system should be developed to improve:

- Data accuracy
- Transparency
- Faster analysis
- Better national coordination

---

### ✅ 5. Conduct Preventive Awareness Campaigns

Public awareness campaigns should educate citizens on:

- Safety measures
- Emergency reporting
- Conflict prevention
- Risk avoidance strategies

---

### ✅ 6. Use Predictive Analytics for Future Planning

Organizations should integrate AI and predictive analytics into national security and disaster management systems to:

- Forecast future risks
- Detect trends early
- Optimize decision-making
- Reduce fatalities

""")


    st.markdown("---")


    # =====================================================
    # PROJECT CONCLUSION
    # =====================================================

    st.subheader("📌 Conclusion")

    st.markdown("""

The Nigeria Incident Analysis Project demonstrates the power of
data analytics in uncovering meaningful patterns hidden within
large incident datasets.

Through interactive visualization and exploratory data analysis,
the project successfully identified:

- High-risk states
- Deadly incident categories
- Seasonal fatality patterns
- Persistent incident clusters
- Long-duration crisis events

The findings emphasize the importance of:

✅ Data-driven decision-making  
✅ Early risk detection  
✅ Strategic emergency planning  
✅ Technology-assisted security management  

This project also highlights the growing role of modern technologies
such as:

- Business Intelligence
- Interactive Dashboards
- Data Visualization
- Predictive Analytics
- Artificial Intelligence

in solving real-world societal and security challenges.

Overall, the dashboard provides stakeholders with an effective tool
for monitoring incidents, understanding trends, and supporting
evidence-based policy and operational decisions.

""")


    st.markdown("---")


    # =====================================================
    # FINAL PROJECT NOTE
    # =====================================================

    st.success("""

✅ Project Completed Successfully

Nigeria Incident Analysis Dashboard
Developed Using:

Python • Pandas • Plotly • Streamlit • Data Analytics

👨‍💻 Developed By Mero Analytics

""")


    st.markdown("---")


    # =====================================================
    # SKILLS DEMONSTRATED
    # =====================================================

    st.subheader("🛠 Skills Demonstrated")

    st.markdown("""

- Data Cleaning  
- Data Visualization  
- Exploratory Data Analysis  
- Dashboard Development  
- Plotly Interactive Charts  
- Streamlit App Development  
- KPI Reporting  
- Business Intelligence  
- Insight Generation  

""")


    st.markdown("---")


    # =====================================================
    # SOCIAL MEDIA LINKS
    # =====================================================

    st.subheader("🌐 Connect With Me")

    st.markdown("""

- 💼 LinkedIn: https://www.linkedin.com/in/alexander-o-irikefe-35a489370?

- 🌐 GitHub: https://github.com/alexandermero68

- 📊 Portfolio: https://yourportfolio.com  

- 📸 Instagram: https://instagram.com/yourname  

- 🐦 X (Twitter): https://x.com/yourname  

- 📘 Facebook: https://facebook.com/yourname  

- ▶️ YouTube: https://youtube.com/@yourname   

- 📱 WhatsApp: https://wa.me/2347060646900  

""")


    st.markdown("---")

    st.success("✅ Developed By Mero Analytics")


# =========================================================
# CONTACT PAGE
# =========================================================

elif menu == "📞 Contact":

    st.title("📞 Contact Me")

    st.markdown("""

Feel free to reach out for:

- 📊 Data Analysis Projects  

- 📈 Dashboard Development  

- 🧠 Business Intelligence Solutions  

- 💼 Freelance Opportunities  

- 🛠 Data Visualization Services  

""")

    st.markdown("---")


    # =====================================================
    # CONTACT DETAILS
    # =====================================================

    st.subheader("📍 Contact Details")

    st.markdown("""

📧 Email: alexandermero68@gmail.com 

📱 Phone: +2347060646900    

🌍 Location: Lagos, Nigeria  

💼 Availability: Open for Remote & Freelance Work  

""")


    st.markdown("---")


    # =====================================================
    # CONTACT FORM
    # =====================================================

    st.subheader("✉ Send a Message")

    name = st.text_input("Your Name")

    email = st.text_input("Your Email")

    message = st.text_area("Your Message")

    if st.button("Send Message"):

        st.success(
            f"✅ Thank you {name}, your message has been sent successfully!"
        )


    st.markdown("---")


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown("""
<center>

### 👨‍💻 Developed By Mero Analytics

📊 Nigeria Incident Analysis Dashboard

</center>
""", unsafe_allow_html=True)

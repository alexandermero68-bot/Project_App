import streamlit as st

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

st.set_page_config(layout="wide")

# ======================

# ELITE UI

# ======================

st.markdown("""

<style>

body {
    background: linear-gradient(135deg, #000000, #434343, #C9A227);
    color: #F8F5F0;

}

.kpi-card {

    background: rgba(255,255,255,0.08);

    padding: 20px;

    border-radius: 15px;

    text-align: center;

    backdrop-filter: blur(12px);

    box-shadow: 0 0 15px rgba(0,255,255,0.2);

}

h1, h2, h3 {
            
   color: #00f5ff;

}

section[data-testid="stSidebar"] {

    background: rgba(0,0,0,0.6);

}

</style>

""", unsafe_allow_html=True)

# ======================

# LOAD DATA

# ======================

df = pd.read_csv("mero_full_cleaned_incidents.csv")

df.columns = df.columns.str.lower()

df["start date"] = pd.to_datetime(df["start date"])

df["end date"] = pd.to_datetime(df["end date"])

df["duration"] = (df["end date"] - df["start date"]).dt.days

# ======================

# SIDEBAR

# ======================

st.sidebar.markdown("## 👤 Mero Analytics")

menu = st.sidebar.radio("Navigation", [

    "🏠 Home",

    "📊 Dashboard",

    "📘 About",

    "📞 Contact"

])

# ======================

# HOME

# ======================

if menu == "🏠 Home":

    st.title("🚀 Nigeria Incident Intelligence System")

    st.markdown("""

    Turning data into actionable intelligence:

    - Identify deadly incidents  

    - Detect high-risk states  

    - Improve response strategy  

    """)



# ======================

# DASHBOARD

# ======================

elif menu == "📊 Dashboard":

    st.title("📊 Nigeria Incident Dashboard")

    # FILTER

    state = st.selectbox("Select State", df["state"].unique())

    filtered = df[df["state"] == state]

    # ======================

    # KPI METRICS

    # ======================

    total_deaths = int(filtered["number of deaths"].sum())

    total_incidents = filtered.shape[0]

    top_state = filtered.groupby("state")["number of deaths"].sum().idxmax()

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='kpi-card'><h3>💀 Deaths</h3><h2>{total_deaths}</h2></div>", unsafe_allow_html=True)

    col2.markdown(f"<div class='kpi-card'><h3>⚠️ Incidents</h3><h2>{total_incidents}</h2></div>", unsafe_allow_html=True)

    col3.markdown(f"<div class='kpi-card'><h3>📍 Top State</h3><h2>{top_state}</h2></div>", unsafe_allow_html=True)

    # ======================
    # AI INSIGHT

    # ======================

    top_incident = filtered.groupby("incident")["number of deaths"].sum().idxmax()

    st.info(f"""

    🔥 Most deadly incident: {top_incident}  

    📍 Most affected state: {top_state}  

    💀 Total deaths: {total_deaths}  

    👉 Focus response on high-risk incidents and locations.

    """)

    # ======================

    # EDA SECTION

    # ======================

    st.header("📊 Exploratory Data Analysis")

    st.markdown("### 1. Which incident causes the most deaths?")

    fig1 = px.treemap(filtered, path=["incident"], values="number of deaths")

    st.plotly_chart(fig1, use_container_width=True)

    st.caption("Insight: A few incident types dominate fatalities → prioritize them.")

    st.markdown("### 2. How incidents distribute across state + type?")

    fig2 = px.sunburst(filtered, path=["incident", "state"], values="number of deaths")

    st.plotly_chart(fig2, use_container_width=True)

    st.caption("Insight: Some states experience specific incident patterns.")

    st.markdown("### 3. Which incidents are most severe?")

    fig3 = px.funnel_area(filtered, names="incident", values="number of deaths")

    st.plotly_chart(fig3, use_container_width=True)

    st.caption("Insight: Severity ranking highlights deadly incident categories.")

    st.markdown("### 4. How long do incidents last?")

    fig4 = px.box(filtered, x="incident", y="duration", color="incident")

    st.plotly_chart(fig4, use_container_width=True)

    st.caption("Insight: Longer incidents may indicate delayed response.")

    st.markdown("### 5. Incident frequency distribution?")

    fig5 = px.pie(filtered, names="incident", hole=0.5)

    st.plotly_chart(fig5, use_container_width=True)

    st.caption("Insight: Frequent incidents are not always the deadliest.")

    st.markdown("### 6. Death spread across incidents?")

    fig6 = px.strip(filtered, x="incident", y="number of deaths", color="incident")

    st.plotly_chart(fig6, use_container_width=True)

    st.caption("Insight: Some incidents have extreme outliers (high deaths).")

    # ======================

    # 3D SECTION

    # ======================

    st.header("🌐 3D Analysis")

    agg = filtered.groupby(["state", "incident"])["number of deaths"].sum().reset_index()

    st.markdown("### 7. 3D Death Distribution")

    fig7 = px.scatter_3d(

        agg,

        x="state",

        y="incident",

        z="number of deaths",

        color="incident"

    )

    st.plotly_chart(fig7, use_container_width=True)

    st.caption("Insight: Identifies deadly clusters across states + incidents.")

    st.markdown("### 8. 3D Surface Pattern")

    pivot = filtered.pivot_table(

        values="number of deaths",

        index="incident",

        columns="duration",

        fill_value=0

    )

    fig8 = go.Figure(data=[go.Surface(z=pivot.values)])

    st.plotly_chart(fig8, use_container_width=True)

    st.caption("Insight: Reveals intensity patterns over duration.")

    st.markdown("### 9. 3D Mesh Risk Model")

    fig9 = go.Figure(data=[go.Mesh3d(

        x=pd.factorize(agg["state"])[0],

        y=pd.factorize(agg["incident"])[0],

        z=agg["number of deaths"],

        opacity=0.5

    )])

    st.plotly_chart(fig9, use_container_width=True)

    st.caption("Insight: Shows complex relationships between variables.")

    st.markdown("### 10. 3D Bubble Impact")

    fig10 = px.scatter_3d(

        agg,

        x="state",

        y="incident",

        z="number of deaths",

        size="number of deaths",

        color="state"

    )

    st.plotly_chart(fig10, use_container_width=True)

    st.caption("Insight: Bigger bubbles = higher impact zones.")


# ======================

# ABOUT

# ======================

elif menu == "📘 About":

    st.title("👤 About Me")

    col1, col2 = st.columns([1, 2])

    with col1:

       
        st.write("Data Analyst | BI Developer | Python Enthusiast")

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

    st.subheader("🧠 Core Skills")

    st.markdown("""

- Data Analysis & Visualization (Power BI, Excel)  

- SQL (Data Extraction, Joins, Query Optimization)  

- Python (Pandas, NumPy, Matplotlib, Seaborn)  

- Dashboard Development & Reporting  

- Data Cleaning & Preprocessing  

- Statistical Analysis & Insight Generation  

- Computer Engineering & Systems Troubleshooting  

- Mobile Device Repair & Diagnostics  

- Cybersecurity Fundamentals & Data Protection Awareness  

- Problem-Solving & Critical Thinking  

- Business Intelligence  

- Data Visualization  

""")

    st.markdown("---")

    # ======================

    # 🔗 SOCIAL MEDIA SECTION (PUT YOUR LINKS HERE)

    # ======================

    st.subheader("🌐 Connect With Me")

    st.markdown("""


    - 💼 LinkedIn: https://www.linkedin.com/in/alexander-o-irikefe-35a489370?utm_source=share_via&utm_content=profile&utm_medium=member_ios  

    - 🌐 GitHub:** https://github.com/YOUR_USERNAME  

    - 📊 Portfolio: https://yourportfolio.com  

    - 📸 Instagram: https://instagram.com/yourname  

    - 🐦 X (Twitter): https://x.com/yourname  

    - 📘 Facebook: https://facebook.com/yourname  

    - ▶️ YouTube: https://youtube.com/@yourname   

    - 📱 WhatsApp: https://wa.me/2347060646900

""")


# ======================

# CONTACT

# ======================

elif menu == "📞 Contact":

    st.title("📞 Contact Me")

    st.markdown(

        """

        Feel free to reach out for:

        - Data Analysis Projects  

        - Dashboard Development  

        - Business Intelligence Solutions  

        - Freelance Opportunities  

        """

    )

    # 👉 YOUR CONTACT DETAILS

    st.markdown(

        """

        📧 Email: alexandermero68@gmail.com 

        📱 Phone: +2347060646900  

        🌍 Location: Lagos, Nigeria 

        📧 Email: alexandermero68@gmail.com  

        """

    )

    st.markdown("---")

    # CONTACT FORM

    name = st.text_input("Your Name")

    email = st.text_input("Your Email")

    message = st.text_area("Your Message")

    if st.button("Send Message"):

        st.success("✅ Message sent successfully! I will get back to you soon.")

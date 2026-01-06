import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# PAGE CONFIG
# ----------------------------------
st.set_page_config(
    page_title="Maritime Anomaly Detection Dashboard",
    page_icon="🚢",
    layout="wide"
)

# ----------------------------------
# CUSTOM CSS (OCEAN THEME & HEADER COLORS)
# ----------------------------------
st.markdown("""
<style>
/* Background Gradient */
.stApp {
    background: linear-gradient(to bottom, #e0f7fa, #ffffff);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Main Header Box */
.header-box {
    background: linear-gradient(90deg, #003366, #0059b3);
    padding: 25px;
    border-radius: 15px;
    color: #ffffff;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
}
.header-box h1 {
    font-size: 42px;
    font-weight: bold;
}
.header-box h4 {
    font-size: 22px;
    font-weight: normal;
    color: #caf0f8;
}

/* Section Boxes */
.section-box {
    background-color: #f0f8ff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}

/* Section Titles / Subheaders */
.section-box h2, .section-box h3, .section-box h4, .section-box h5, .section-box h6 {
    color: #003366;  /* Dark ocean blue */
}

/* KPI Columns */
.stMetric {
    background: linear-gradient(135deg, #0077b6, #00b4d8);
    color: white;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.2);
}

/* Footer */
footer {
    color: #003366;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("ais_data_cleaned.xls")  # make sure your file path is correct

df = load_data()

# ----------------------------------
# HEADER
# ----------------------------------
st.markdown("""
<div class="header-box">
    <h1>🚢 Maritime Traffic Anomaly Detection</h1>
    <h4>AIS-Based Coastal Security Monitoring Dashboard</h4>
</div>
""", unsafe_allow_html=True)

# ----------------------------------
# KPIs
# ----------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="📄 Total Records", value=len(df))
with col2:
    st.metric(label="🚢 Unique Vessels", value=df["MMSI"].nunique())
with col3:
    st.metric(label="⚠️ Speed Anomalies", value=df["SPEED_ANOMALY"].sum())

# ----------------------------------
# DATA PREVIEW
# ----------------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("📊 AIS Dataset Preview")
st.dataframe(df.head(50), use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------
# SPEED DISTRIBUTION
# ----------------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("⚡ Speed Over Ground (Knots)")

fig_speed = px.histogram(
    df,
    x="SOG",
    nbins=40,
    labels={"SOG": "Speed (knots)"},
    title="Distribution of Vessel Speed",
    color_discrete_sequence=["#003366"]  # Dark ocean blue for histogram
)
st.plotly_chart(fig_speed, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------
# TIME-ANIMATED MAP
# ----------------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("🗺️ Time-Animated Vessel Movement")

fig_map = px.scatter_mapbox(
    df,
    lat="LATITUDE",
    lon="LONGITUDE",
    color="SPEED_ANOMALY",
    animation_frame="HOUR",
    zoom=4,
    height=600,
    mapbox_style="open-street-map",
    title="AIS Vessel Movement Over Time",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_map, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------
# ANOMALY TABLE
# ----------------------------------
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("⚠️ Detected Speed Anomalies")
anomalies = df[df["SPEED_ANOMALY"] == 1]
st.write(f"Total anomalies detected: **{len(anomalies)}**")
st.dataframe(
    anomalies[["MMSI", "SOG", "LATITUDE", "LONGITUDE", "DATE", "HOUR"]].head(30),
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.markdown(
    "<center><b style='color:#003366;'>Coastal Security & Maritime Surveillance Dashboard</b></center>",
    unsafe_allow_html=True
)

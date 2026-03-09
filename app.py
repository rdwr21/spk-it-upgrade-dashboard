import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from saw import calculate_saw

st.set_page_config(
    page_title="IT DSS",
    layout="wide"
)

# -----------------------------
# Custom Styling
# -----------------------------

st.markdown("""
<style>
body {background-color:#0f172a;}
.kpi-card{
background:#1e293b;
padding:20px;
border-radius:10px;
text-align:center;
color:white;
}
</style>
""",unsafe_allow_html=True)

st.title("IT Decision Support System")
st.caption("Infrastructure Upgrade Analytics Dashboard")

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("System Control")

uploaded_file = st.sidebar.file_uploader(
"Upload Infrastructure Dataset",
type=["xlsx"]
)

if uploaded_file is None:
    st.warning("Upload dataset terlebih dahulu")
    st.stop()

# -----------------------------
# Load Dataset
# -----------------------------

matrix = pd.read_excel(uploaded_file, sheet_name="Decision_Matrix")
matrix = matrix.set_index("Alternative")

device_info = pd.read_excel(uploaded_file, sheet_name="Device_Info")

weights = pd.Series({
"C1":0.25,
"C2":0.20,
"C3":0.20,
"C4":0.25,
"C5":0.10
})

benefit_cols = ["C1","C2","C3","C4"]
cost_cols = ["C5"]

ranking, norm = calculate_saw(matrix,weights,benefit_cols,cost_cols)

ranking_df = ranking.reset_index()
ranking_df.columns=["Alternative","Score"]

ranking_df = ranking_df.merge(device_info,on="Alternative")

# -----------------------------
# Executive Summary
# -----------------------------

st.subheader("Executive Summary")

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("Total Assets",len(ranking_df))

with col2:
    st.metric("Critical Assets",
              len(ranking_df[ranking_df["Score"]>0.85]))

with col3:
    st.metric("Average Risk",
              round(ranking_df["Score"].mean(),2))

with col4:
    st.metric("Top Priority",
              ranking_df.iloc[0]["Device Name"])

# -----------------------------
# Top Priority Alert
# -----------------------------

top = ranking_df.iloc[0]

st.error(
f"""
🚨 **Upgrade Priority Alert**

Device : **{top['Device Name']}**

Risk Score : **{round(top['Score'],2)}**

{top['Description']}
"""
)

# -----------------------------
# Priority Ranking Chart
# -----------------------------

st.subheader("Infrastructure Upgrade Priority")

fig = px.bar(
ranking_df,
x="Device Name",
y="Score",
color="Score",
text="Score"
)

st.plotly_chart(fig,use_container_width=True)

# -----------------------------
# Risk Heatmap
# -----------------------------

st.subheader("Infrastructure Risk Heatmap")

heatmap = px.imshow(
matrix,
text_auto=True,
color_continuous_scale="Reds"
)

st.plotly_chart(heatmap,use_container_width=True)

# -----------------------------
# Asset Lifecycle Chart
# -----------------------------

st.subheader("Asset Lifecycle Distribution")

age_data = matrix["C1"]

fig2 = px.histogram(
age_data,
nbins=5,
title="Asset Age Distribution"
)

st.plotly_chart(fig2,use_container_width=True)

# -----------------------------
# Device Risk Radar Chart
# -----------------------------

st.subheader("Device Risk Profile")

device = st.selectbox(
"Select Device",
ranking_df["Device Name"]
)

selected = ranking_df[ranking_df["Device Name"]==device]["Alternative"].values[0]

values = matrix.loc[selected].values

categories = matrix.columns.tolist()

fig3 = go.Figure()

fig3.add_trace(go.Scatterpolar(
r=values,
theta=categories,
fill='toself'
))

fig3.update_layout(
polar=dict(radialaxis=dict(visible=True)),
showlegend=False
)

st.plotly_chart(fig3,use_container_width=True)

# -----------------------------
# Asset Decision Table
# -----------------------------

st.subheader("Asset Decision Table")

st.dataframe(
ranking_df[[
"Device Name",
"Score",
"Description"
]],
use_container_width=True
)

import streamlit as st
import pandas as pd
import plotly.express as px
from saw import calculate_saw

st.set_page_config(
    page_title="SPK Infrastruktur IT",
    page_icon="💻",
    layout="wide"
)

# ===== Custom CSS =====

st.markdown("""
<style>
.main-title {
    font-size:30px;
    font-weight:bold;
}

.kpi-card {
    background-color:#1f2937;
    padding:20px;
    border-radius:10px;
    color:white;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ===== Header =====

st.markdown('<p class="main-title">💻 Sistem Pendukung Keputusan Infrastruktur IT</p>', unsafe_allow_html=True)
st.caption("Metode Simple Additive Weighting (SAW)")

# ===== Sidebar =====

st.sidebar.title("Menu")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard","Dataset","Analisis","Ranking"]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset Excel",
    type=["xlsx"]
)

# ===== Load Dataset =====

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Decision_Matrix")
    df = df.set_index("Alternative")
else:
    st.warning("Upload dataset terlebih dahulu")
    st.stop()

# ===== Dashboard Page =====

if menu == "Dashboard":

    st.subheader("Ringkasan Infrastruktur")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown('<div class="kpi-card">Total Perangkat<br><h2>'+str(len(df))+'</h2></div>',unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kpi-card">Jumlah Kriteria<br><h2>'+str(len(df.columns))+'</h2></div>',unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="kpi-card">Metode<br><h2>SAW</h2></div>',unsafe_allow_html=True)

# ===== Dataset Page =====

if menu == "Dataset":

    st.subheader("Dataset Infrastruktur")

    st.dataframe(df,use_container_width=True)

# ===== Analisis Page =====

if menu == "Analisis":

    st.subheader("Analisis Dataset")

    fig = px.imshow(df,
                    text_auto=True,
                    title="Heatmap Nilai Kriteria")

    st.plotly_chart(fig,use_container_width=True)

# ===== Ranking Page =====

if menu == "Ranking":

    st.subheader("Perhitungan SAW")

    weights = pd.Series({
        "C1":0.25,
        "C2":0.20,
        "C3":0.20,
        "C4":0.25,
        "C5":0.10
    })

    benefit_cols = ["C1","C2","C3","C4"]
    cost_cols = ["C5"]

    ranking, norm = calculate_saw(df,weights,benefit_cols,cost_cols)

    col1,col2 = st.columns(2)

    with col1:
        st.write("Matriks Normalisasi")
        st.dataframe(norm)

    with col2:
        st.write("Ranking Prioritas")
        st.dataframe(ranking)

    chart_data = ranking.reset_index()
    chart_data.columns=["Perangkat","Nilai"]

    fig = px.bar(
        chart_data,
        x="Perangkat",
        y="Nilai",
        color="Nilai",
        title="Prioritas Upgrade Infrastruktur IT"
    )

    st.plotly_chart(fig,use_container_width=True)
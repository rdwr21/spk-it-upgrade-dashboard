import streamlit as st
import pandas as pd
import plotly.express as px


# ==============================
# Konfigurasi halaman
# ==============================

st.set_page_config(
    page_title="SPK Infrastruktur IT",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Sistem Pendukung Keputusan")
st.subheader("Prioritas Upgrade Infrastruktur IT (Metode SAW)")


# ==============================
# Sidebar
# ==============================

st.sidebar.header("Pengaturan")

uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset Excel",
    type=["xlsx"]
)

st.sidebar.subheader("Bobot Kriteria")

w1 = st.sidebar.slider("Usia Perangkat (C1)",0.0,1.0,0.25)
w2 = st.sidebar.slider("Performa (C2)",0.0,1.0,0.20)
w3 = st.sidebar.slider("Risiko Kerusakan (C3)",0.0,1.0,0.20)
w4 = st.sidebar.slider("Dampak Operasional (C4)",0.0,1.0,0.25)
w5 = st.sidebar.slider("Biaya Penggantian (C5)",0.0,1.0,0.10)


weights = {
    "C1":w1,
    "C2":w2,
    "C3":w3,
    "C4":w4,
    "C5":w5
}


benefit_cols = ["C1","C2","C3","C4"]
cost_cols = ["C5"]


# ==============================
# Fungsi SAW
# ==============================

def normalize_matrix(df):

    norm = df.copy()

    for col in benefit_cols:
        norm[col] = df[col] / df[col].max()

    for col in cost_cols:
        norm[col] = df[col].min() / df[col]

    return norm


def calculate_saw(df):

    norm = normalize_matrix(df)

    weighted = norm * pd.Series(weights)

    score = weighted.sum(axis=1)

    ranking = score.sort_values(ascending=False)

    return ranking, norm


# ==============================
# Load dataset
# ==============================

if uploaded_file:

    df = pd.read_excel(uploaded_file, sheet_name="Decision_Matrix")

    df = df.set_index("Alternative")

    st.header("Dataset Perangkat")

    st.dataframe(df, use_container_width=True)


    if st.button("Proses Perhitungan SAW"):

        ranking, norm = calculate_saw(df)


        col1, col2 = st.columns(2)


        with col1:
            st.subheader("Matriks Normalisasi")
            st.dataframe(norm, use_container_width=True)


        with col2:
            st.subheader("Ranking Prioritas Upgrade")
            st.dataframe(ranking, use_container_width=True)


        st.subheader("Visualisasi Ranking")


        chart_data = ranking.reset_index()
        chart_data.columns = ["Perangkat","Nilai"]


        fig = px.bar(
            chart_data,
            x="Perangkat",
            y="Nilai",
            color="Nilai",
            title="Prioritas Upgrade Infrastruktur IT",
            text="Nilai"
        )

        st.plotly_chart(fig, use_container_width=True)


else:

    st.info("Silakan upload dataset Excel terlebih dahulu.")
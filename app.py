import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================
# CONFIG
# ==========================

st.set_page_config(
    page_title="ST-SAE Jawa Timur",
    layout="wide"
)


# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():

    hasil = pd.read_csv(
        "data/hasil_ST_SAE_kecamatan_tahun.csv"
    )

    ringkasan = pd.read_csv(
        "data/ringkasan_ST_SAE_per_kecamatan.csv"
    )

    model = pd.read_csv(
        "data/perbandingan_model_SAE.csv"
    )

    akurasi = pd.read_csv(
        "data/ringkasan_akurasi_model_SAE.csv"
    )

    moran = pd.read_csv(
        "data/tabel_indeks_moran_panel_2018_2025.csv"
    )


    return (
        hasil,
        ringkasan,
        model,
        akurasi,
        moran
    )


hasil, ringkasan, model, akurasi, moran = load_data()



# ==========================
# TITLE
# ==========================

st.title(
    "Estimasi Pengeluaran Per Kapita Kecamatan Jawa Timur Menggunakan Spatial Temporal Small Area Estimation"
)


st.markdown(
"""
Web ini menyajikan hasil penelitian ST-SAE untuk menghasilkan estimasi
pengeluaran per kapita tingkat kecamatan dengan memanfaatkan informasi:

- Direct estimate BPS
- Auxiliary variables
- Struktur spasial
- Struktur temporal

Periode penelitian: 2018–2025
"""
)



# ==========================
# DIRECT ESTIMATE
# ==========================

st.header(
    "1. Direct Estimate"
)


tahun = st.selectbox(
    "Pilih Tahun",
    sorted(
        hasil["tahun"].unique()
    )
)


data_tahun = hasil[
    hasil["tahun"]==tahun
]


col1,col2,col3 = st.columns(3)


col1.metric(
    "Jumlah Kecamatan",
    data_tahun.shape[0]
)


col2.metric(
    "Rata-rata Direct Estimate",
    round(
        data_tahun["pengeluaran_mean"].mean()
    )
)


col3.metric(
    "Rata-rata EBLUP",
    round(
        data_tahun["EBLUP_ST"].mean()
    )
)



fig = px.scatter(
    data_tahun,
    x="pengeluaran_mean",
    y="EBLUP_ST",
    title="Direct Estimate vs ST-SAE EBLUP"
)

st.plotly_chart(
    fig,
    use_container_width=True
)



# ==========================
# TREND
# ==========================

st.header(
    "2. Perubahan Temporal"
)


trend = (
    hasil
    .groupby("tahun")
    .agg(
        direct=("pengeluaran_mean","mean"),
        eblup=("EBLUP_ST","mean")
    )
    .reset_index()
)


fig = px.line(
    trend,
    x="tahun",
    y=[
        "direct",
        "eblup"
    ],
    markers=True,
    title="Tren Direct Estimate dan ST-SAE"
)

st.plotly_chart(
    fig,
    use_container_width=True
)



# ==========================
# MORAN
# ==========================

st.header(
    "3. Analisis Spasial"
)


st.dataframe(
    moran
)



# ==========================
# MODEL
# ==========================

st.header(
    "4. Perbandingan Model"
)


st.dataframe(
    model
)


fig = px.bar(
    model,
    x="Model",
    y="AIC",
    title="Perbandingan AIC Model"
)

st.plotly_chart(
    fig,
    use_container_width=True
)



# ==========================
# AKURASI
# ==========================

st.header(
    "5. Evaluasi Akurasi"
)


st.dataframe(
    akurasi
)



# ==========================
# SEARCH AREA
# ==========================

st.header(
    "6. Eksplorasi Kecamatan"
)


kode = st.selectbox(
    "Pilih Kecamatan",
    ringkasan.iloc[:,0].unique()
)


st.dataframe(
    ringkasan[
        ringkasan.iloc[:,0]==kode
    ]
)
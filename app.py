import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px


# ==========================
# CONFIG
# ==========================

st.set_page_config(
    page_title="ST-SAE Jawa Timur",
    page_icon="📊",
    layout="wide"
)


# ==========================
# CSS STYLE
# ==========================

st.markdown(
"""
<style>

body {
    background-color:#F7F9FC;
}


.main-title {
    font-size:40px;
    font-weight:700;
    color:#17365D;
}


.subtitle {
    font-size:18px;
    color:#555;
}


.card {

    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:
    0px 4px 12px rgba(0,0,0,0.08);

}


div[data-testid="metric-container"] {

background:white;
padding:15px;
border-radius:12px;

}


.stTabs [data-baseweb="tab"] {

font-size:16px;

}


</style>
""",
unsafe_allow_html=True
)



# ==========================
# LOAD DATA
# ==========================

@st.cache_data
def load_data():

    hasil = pd.read_csv(
        "data/hasil_estimasi_eblup_kecamatan.csv"
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
        model,
        akurasi,
        moran
    )



@st.cache_data
def load_map():

    gdf = gpd.read_file(
        "data/kecamatan_jatim.zip"
    )


    gdf["kode_kec"] = (
        gdf["kode_kec"]
        .astype(str)
    )


    return gdf



hasil, model, akurasi, moran = load_data()

gdf = load_map()



# ==========================
# CLEAN DATA
# ==========================

hasil["kode_kecamatan_kemendagri"] = (
    hasil["kode_kecamatan_kemendagri"]
    .astype(str)
)


# merge peta

map_data = gdf.merge(
    hasil,
    left_on="kode_kec",
    right_on="kode_kecamatan_kemendagri",
    how="left"
)

def anchor(name):

    st.markdown(
        f"""
        <div id="{name}"></div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
"""
<style>

.navbar {

background-color:#17365D;

padding:15px;

border-radius:10px;

position:sticky;

top:0;

z-index:999;

}


.navbar a {

color:white;

text-decoration:none;

margin-right:25px;

font-weight:600;

}

</style>


<div class="navbar">

<a href="#beranda">
Beranda
</a>


<a href="#metodologi">
Metodologi
</a>


<a href="#direct">
Direct Estimate
</a>


<a href="#stsae">
ST-SAE
</a>


<a href="#evaluasi">
Evaluasi
</a>


<a href="#eksplorasi">
Eksplorasi
</a>


</div>

""",
unsafe_allow_html=True
)

anchor("beranda")


st.markdown(
"""
<div class="main-title">

Spatial Temporal Small Area Estimation
Jawa Timur

</div>

<div class="subtitle">

Estimasi Pengeluaran Per Kapita Kecamatan
Tahun 2018-2025

</div>

""",
unsafe_allow_html=True
)


st.write("")

col1,col2,col3,col4 = st.columns(4)


with col1:

    st.metric(
        "Wilayah",
        "661 Kecamatan"
    )


with col2:

    st.metric(
        "Periode",
        "2018-2025"
    )


with col3:

    st.metric(
        "Model",
        "ST-SAE"
    )


with col4:

    st.metric(
        "Estimator",
        "EBLUP"
    )

st.markdown(
"""
## Latar Belakang

Estimasi pengeluaran per kapita pada tingkat kecamatan
memiliki tantangan karena keterbatasan ukuran sampel survei.

Pendekatan Small Area Estimation digunakan dengan
memanfaatkan informasi tambahan berupa:

- karakteristik lingkungan,
- sosial,
- ekonomi,
- infrastruktur,

serta mempertimbangkan hubungan spasial dan temporal
antar wilayah.

Penelitian ini menghasilkan estimasi pengeluaran per kapita
kecamatan menggunakan model Spatial Temporal SAE.
"""
)

st.divider()

anchor("metodologi")


st.header(
    "Metodologi Penelitian"
)

m1,m2,m3,m4,m5 = st.columns(5)


m1.info(
"""
Data

BPS + Auxiliary
"""
)


m2.info(
"""
Direct Estimate

Baseline
"""
)


m3.info(
"""
Spatial

Queen Contiguity
"""
)


m4.info(
"""
Temporal

Time Effect
"""
)


m5.success(
"""
EBLUP

ST-SAE
"""
)

st.latex(
r"""
y_{it}=X_{it}\beta+u_{it}+e_{it}
"""
)

st.markdown(
"""
Model ST-SAE menggabungkan:

- fixed effect dari auxiliary variables,
- spatial random effect,
- temporal random effect,
- sampling error.

Estimator akhir diperoleh menggunakan EBLUP.
"""
)

st.subheader(
"Komponen Model"
)

c1,c2,c3 = st.columns(3)


c1.success(
"""
### Spatial

Menggunakan matriks bobot Queen Contiguity.

Parameter:
ρ
"""
)


c2.warning(
"""
### Temporal

Hubungan antar tahun.

Parameter:
λ
"""
)


c3.info(
"""
### Estimasi

REML + GLS + BLUP

Output:
EBLUP
"""
)


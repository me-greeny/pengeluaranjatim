import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px


# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="ST-SAE Jawa Timur",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# STYLE
# =====================================================

st.markdown(
"""
<style>

.main{
    background-color:#FAFAFA;
}

h1{
    color:#17365D;
}

h2{
    color:#1F4E79;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:10px;
    padding:15px;
    box-shadow:0px 2px 8px #ddd;
}

</style>
""",
unsafe_allow_html=True
)



# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    hasil = pd.read_csv(
        "data/hasil_estimasi_eblup_kecamatan.csv"
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



@st.cache_data
def load_map():

    gdf = gpd.read_file(
        "data/kecamatan_jatim.zip"
    )


    # kode shp
    gdf["kode_kec"] = (
        gdf["kode_kec"]
        .astype(str)
    )


    return gdf



hasil, ringkasan, model, akurasi, moran = load_data()

gdf = load_map()



# =====================================================
# HARMONISASI KODE WILAYAH
# =====================================================


hasil["kode_kecamatan_kemendagri"] = (
    hasil["kode_kecamatan_kemendagri"]
    .astype(str)
)


gdf["kode_kec"] = (
    gdf["kode_kec"]
    .astype(str)
)



# =====================================================
# GABUNGKAN SHP + HASIL ESTIMASI
# =====================================================

map_data = gdf.merge(
    hasil,
    left_on="kode_kec",
    right_on="kode_kecamatan_kemendagri",
    how="left"
)



# =====================================================
# HEADER
# =====================================================


st.title(
"""
📊 Spatial Temporal Small Area Estimation
Jawa Timur
"""
)


st.markdown(
"""
Aplikasi ini menyajikan hasil penelitian estimasi
pengeluaran per kapita tingkat kecamatan menggunakan
pendekatan **Spatial Temporal Small Area Estimation (ST-SAE)**.

Periode:
**2018–2025**

Wilayah:
**Kecamatan Provinsi Jawa Timur**
"""
)



# =====================================================
# SIDEBAR
# =====================================================

menu = st.sidebar.radio(
    "Menu",
    [
        "Beranda",
        "Metodologi",
        "Direct Estimate",
        "Analisis Spasial",
        "Model ST-SAE",
        "Peta EBLUP",
        "Evaluasi Model",
        "Eksplorasi Kecamatan"
    ]
)



# =====================================================
# BERANDA
# =====================================================

if menu=="Beranda":


    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Jumlah Kecamatan",
        "661"
    )

    c2.metric(
        "Periode",
        "2018-2025"
    )

    c3.metric(
        "Model",
        "ST-SAE"
    )

    c4.metric(
        "Pendekatan",
        "EBLUP"
    )



    st.subheader(
        "Tujuan Penelitian"
    )


    st.write(
"""
1. Menghasilkan direct estimate pengeluaran per kapita.
2. Membentuk model Spatial Temporal SAE.
3. Mengevaluasi peningkatan akurasi menggunakan MSE dan RRMSE.
"""
)



# =====================================================
# METODOLOGI
# =====================================================


elif menu=="Metodologi":


    st.header(
        "Metodologi ST-SAE"
    )


    st.markdown(
"""
### 1. Direct Estimate

Estimasi awal diperoleh dari data BPS.


### 2. Auxiliary Variables

Model memanfaatkan informasi tambahan:

- NTL
- LST
- NDVI
- NDBI
- Pendidikan
- Kesehatan
- Ekonomi
- Listrik


### 3. Spatial Temporal SAE

Model:

\[
y_{it}=X_{it}\\beta+u_{it}+e_{it}
\]


Komponen random effect:

\[
u_t=\\rho Wu_t+\\lambda u_{t-1}+v_t
\]


### 4. Estimasi

Parameter diestimasi menggunakan REML.


### 5. Prediksi

Estimator akhir:

\[
EBLUP=X\\hat{\\beta}+\\hat{u}
\]


### 6. Evaluasi

Menggunakan:

- MSE
- RRMSE

"""
)



# =====================================================
# DIRECT ESTIMATE
# =====================================================


elif menu=="Direct Estimate":


    st.header(
        "Direct Estimate BPS"
    )


    tahun = st.selectbox(
        "Pilih Tahun",
        sorted(
            hasil["tahun"].unique()
        )
    )


    temp = hasil[
        hasil["tahun"]==tahun
    ]


    c1,c2,c3=st.columns(3)


    c1.metric(
        "Jumlah Kecamatan",
        temp.shape[0]
    )


    c2.metric(
        "Mean Direct",
        round(
            temp["pengeluaran_mean"].mean()
        )
    )


    c3.metric(
        "Mean EBLUP",
        round(
            temp["EBLUP_ST"].mean()
        )
    )


    fig=px.scatter(
        temp,
        x="pengeluaran_mean",
        y="EBLUP_ST",
        hover_name="kecamata",
        title="Direct Estimate vs EBLUP"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# =====================================================
# SPASIAL
# =====================================================


elif menu=="Analisis Spasial":


    st.header(
        "Analisis Spasial"
    )


    st.dataframe(
        moran
    )



# =====================================================
# MODEL
# =====================================================


elif menu=="Model ST-SAE":


    st.header(
        "Model ST-SAE"
    )


    st.dataframe(
        model
    )



# =====================================================
# PETA EBLUP
# =====================================================


elif menu=="Peta EBLUP":


    st.header(
        "Peta Estimasi ST-SAE"
    )


    pilihan = st.radio(
        "Tampilan",
        [
            "Satu Tahun",
            "Keseluruhan Tahun"
        ]
    )



    if pilihan=="Satu Tahun":


        tahun = st.selectbox(
            "Pilih Tahun",
            sorted(
                hasil["tahun"].unique()
            )
        )


        data_peta = map_data[
            map_data["tahun"]==tahun
        ]


        nilai = "EBLUP_ST"



    else:


        data_peta = (
            map_data
            .groupby(
                [
                    "kode_kec",
                    "kecamata",
                    "geometry"
                ],
                as_index=False
            )
            .agg(
                EBLUP_ST=
                ("EBLUP_ST","mean")
            )
        )


        nilai="EBLUP_ST"



    fig = px.choropleth_mapbox(
        data_peta,
        geojson=data_peta.geometry,
        locations=data_peta.index,
        color=nilai,
        hover_name="kecamata",
        mapbox_style="carto-positron",
        zoom=7,
        center={
            "lat":-7.5,
            "lon":112.5
        }
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# =====================================================
# EVALUASI
# =====================================================


elif menu=="Evaluasi Model":


    st.header(
        "Evaluasi Akurasi"
    )


    st.dataframe(
        akurasi
    )



    fig=px.bar(
        akurasi,
        x="Model",
        y="RRMSE"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# =====================================================
# EKSPLORASI
# =====================================================


elif menu=="Eksplorasi Kecamatan":


    st.header(
        "Eksplorasi Kecamatan"
    )


    kec = st.selectbox(
        "Pilih Kecamatan",
        sorted(
            hasil["kecamata"]
            .dropna()
            .unique()
        )
    )


    st.dataframe(
        hasil[
            hasil["kecamata"]==kec
        ]
    )
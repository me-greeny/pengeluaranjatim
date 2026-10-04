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

# =====================================================
# 3. DIRECT ESTIMATE
# =====================================================

st.divider()

anchor("direct")

st.header(
    "1. Direct Estimate"
)

st.markdown(
"""
Direct estimate digunakan sebagai estimasi awal pengeluaran
per kapita pada tingkat kecamatan. Hasil ini menjadi baseline
sebelum dilakukan pemodelan Spatial Temporal Small Area
Estimation (ST-SAE).
"""
)


# -----------------------------------------------------
# PILIHAN TAMPILAN
# -----------------------------------------------------

mode_direct = st.radio(
    "Tampilan hasil direct estimate",
    [
        "Satu Tahun",
        "Keseluruhan Tahun"
    ],
    horizontal=True,
    key="mode_direct"
)


# -----------------------------------------------------
# SATU TAHUN
# -----------------------------------------------------

if mode_direct == "Satu Tahun":

    tahun_direct = st.selectbox(
        "Pilih Tahun",
        sorted(
            hasil["tahun"].unique()
        ),
        key="tahun_direct"
    )


    data_direct = hasil[
        hasil["tahun"] == tahun_direct
    ].copy()


    # ---------------------------------------------
    # KPI
    # ---------------------------------------------

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "Jumlah Kecamatan",
            f"{data_direct['kode_kecamatan_kemendagri'].nunique():,}"
        )


    with c2:

        st.metric(
            "Rata-rata Direct Estimate",
            f"Rp {data_direct['pengeluaran_mean'].mean():,.0f}"
        )


    with c3:

        st.metric(
            "Median Direct Estimate",
            f"Rp {data_direct['pengeluaran_mean'].median():,.0f}"
        )


    with c4:

        st.metric(
            "Rata-rata CV",
            f"{data_direct['CV...11'].mean():.2f}%"
        )


    # ---------------------------------------------
    # DISTRIBUSI
    # ---------------------------------------------

    st.subheader(
        "Distribusi Pengeluaran Per Kapita"
    )


    fig_direct = px.histogram(
        data_direct,
        x="pengeluaran_mean",
        nbins=30,
        title=(
            f"Distribusi Direct Estimate "
            f"Tahun {tahun_direct}"
        ),
        labels={
            "pengeluaran_mean":
            "Pengeluaran Per Kapita"
        }
    )


    fig_direct.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        fig_direct,
        use_container_width=True
    )


    # ---------------------------------------------
    # TABEL
    # ---------------------------------------------

    st.subheader(
        "Ringkasan Direct Estimate"
    )


    tabel_direct = data_direct[
        [
            "kode_kecamatan_bps",
            "nama_kecamatan_bps",
            "nama_kecamatan_kemendagri",
            "pengeluaran_mean",
            "CV...11",
            "RSE...12"
        ]
    ].copy()


    tabel_direct = (
        tabel_direct
        .sort_values(
            "pengeluaran_mean",
            ascending=False
        )
    )


    st.dataframe(
        tabel_direct,
        use_container_width=True,
        hide_index=True
    )



# -----------------------------------------------------
# KESELURUHAN TAHUN
# -----------------------------------------------------

else:

    direct_summary = (
        hasil
        .groupby("tahun")
        .agg(
            mean_direct=(
                "pengeluaran_mean",
                "mean"
            ),

            median_direct=(
                "pengeluaran_mean",
                "median"
            ),

            mean_cv=(
                "CV...11",
                "mean"
            )
        )
        .reset_index()
    )


    st.subheader(
        "Perkembangan Direct Estimate 2018–2025"
    )


    fig_trend_direct = px.line(
        direct_summary,
        x="tahun",
        y="mean_direct",
        markers=True,
        title=(
            "Rata-rata Pengeluaran Per Kapita "
            "Direct Estimate"
        ),
        labels={
            "tahun": "Tahun",
            "mean_direct":
            "Rata-rata Pengeluaran Per Kapita"
        }
    )


    fig_trend_direct.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        fig_trend_direct,
        use_container_width=True
    )


    st.subheader(
        "Perkembangan Koefisien Variasi"
    )


    fig_cv = px.line(
        direct_summary,
        x="tahun",
        y="mean_cv",
        markers=True,
        title="Rata-rata CV Direct Estimate",
        labels={
            "tahun": "Tahun",
            "mean_cv": "CV (%)"
        }
    )


    fig_cv.update_layout(
        template="plotly_white"
    )


    st.plotly_chart(
        fig_cv,
        use_container_width=True
    )


    st.dataframe(
        direct_summary,
        use_container_width=True,
        hide_index=True
    )

# =====================================================
# DIRECT VS EBLUP
# =====================================================

st.subheader(
    "Direct Estimate dan ST-SAE EBLUP"
)

st.markdown(
"""
Perbandingan ini menunjukkan perubahan estimasi setelah
informasi auxiliary variables serta struktur spasial-temporal
dimasukkan ke dalam model.
"""
)


tahun_compare = st.selectbox(
    "Pilih Tahun Perbandingan",
    sorted(
        hasil["tahun"].unique()
    ),
    key="tahun_compare"
)


data_compare = hasil[
    hasil["tahun"] == tahun_compare
].copy()


fig_compare = px.scatter(
    data_compare,
    x="pengeluaran_mean",
    y="eblup_spatiotemporal",
    hover_name="nama_kecamatan_kemendagri",
    hover_data={
        "pengeluaran_mean": ":,.0f",
        "eblup_spatiotemporal": ":,.0f",
        "rrmse_st": ":.4f"
    },
    labels={
        "pengeluaran_mean":
        "Direct Estimate",

        "eblup_spatiotemporal":
        "ST-SAE EBLUP",

        "rrmse_st":
        "RRMSE ST-SAE"
    },
    title=(
        f"Direct Estimate vs ST-SAE "
        f"Tahun {tahun_compare}"
    )
)


# garis y = x

min_value = min(
    data_compare["pengeluaran_mean"].min(),
    data_compare["eblup_spatiotemporal"].min()
)


max_value = max(
    data_compare["pengeluaran_mean"].max(),
    data_compare["eblup_spatiotemporal"].max()
)


fig_compare.add_shape(
    type="line",
    x0=min_value,
    y0=min_value,
    x1=max_value,
    y1=max_value,
    line=dict(
        dash="dash"
    )
)


fig_compare.update_layout(
    template="plotly_white"
)


st.plotly_chart(
    fig_compare,
    use_container_width=True
)

# =====================================================
# TREND DIRECT VS EBLUP
# =====================================================

st.subheader(
    "Tren Direct Estimate dan ST-SAE"
)


trend_st = (
    hasil
    .groupby("tahun")
    .agg(
        direct=(
            "pengeluaran_mean",
            "mean"
        ),

        eblup=(
            "eblup_spatiotemporal",
            "mean"
        )
    )
    .reset_index()
)


fig_trend_st = px.line(
    trend_st,
    x="tahun",
    y=[
        "direct",
        "eblup"
    ],
    markers=True,
    labels={
        "tahun": "Tahun",
        "value": "Pengeluaran Per Kapita",
        "variable": "Estimasi"
    },
    title=(
        "Perbandingan Tren Direct Estimate "
        "dan ST-SAE EBLUP"
    )
)


fig_trend_st.update_layout(
    template="plotly_white"
)


st.plotly_chart(
    fig_trend_st,
    use_container_width=True
)

# =====================================================
# 4. PETA ST-SAE
# =====================================================

st.divider()

anchor("stsae")

st.header(
    "2. Hasil Estimasi Spatial Temporal SAE"
)

st.markdown(
"""
Peta berikut menunjukkan distribusi estimasi pengeluaran
per kapita berdasarkan hasil ST-SAE EBLUP pada tingkat
kecamatan.
"""
)

map_mode = st.radio(
    "Mode peta",
    [
        "Satu Tahun",
        "Rata-rata 2018–2025"
    ],
    horizontal=True,
    key="map_mode"
)

if map_mode == "Satu Tahun":

    tahun_map = st.selectbox(
        "Pilih Tahun Peta",
        sorted(
            hasil["tahun"].unique()
        ),
        key="tahun_map"
    )


    map_values = map_data[
        map_data["tahun"] == tahun_map
    ].copy()

else:

    map_values = (
        map_data
        .groupby(
            [
                "kode_kec",
                "kecamata",
                "kab_kota",
                "provinsi",
                "geometry"
            ],
            as_index=False
        )
        .agg(
            eblup_spatiotemporal=(
                "eblup_spatiotemporal",
                "mean"
            ),

            pengeluaran_mean=(
                "pengeluaran_mean",
                "mean"
            ),

            rrmse_st=(
                "rrmse_st",
                "mean"
            )
        )
    )

# =====================================================
# MAP
# =====================================================

if not map_values.empty:

    fig_map = px.choropleth_map(
        map_values,
        geojson=map_values.geometry.__geo_interface__,
        locations=map_values.index,
        color="eblup_spatiotemporal",
        hover_name="kecamata",
        hover_data={
            "kab_kota": True,
            "provinsi": True,
            "pengeluaran_mean": ":,.0f",
            "eblup_spatiotemporal": ":,.0f",
            "rrmse_st": ":.4f"
        },
        color_continuous_scale="Viridis",
        map_style="carto-positron",
        zoom=6.7,
        center={
            "lat": -7.75,
            "lon": 112.5
        },
        labels={
            "eblup_spatiotemporal":
            "ST-SAE EBLUP"
        }
    )


    fig_map.update_layout(
        height=650,
        margin={
            "r":0,
            "t":40,
            "l":0,
            "b":0
        }
    )


    st.plotly_chart(
        fig_map,
        use_container_width=True
    )

else:

    st.warning(
        "Tidak terdapat data untuk ditampilkan."
    )

@st.cache_data
def load_map():

    gdf = gpd.read_file(
        "data/kecamatan_jatim.zip"
    )

    gdf["kode_kec"] = (
        gdf["kode_kec"]
        .astype(str)
        .str.strip()
    )

    if gdf.crs is None:

        gdf = gdf.set_crs(
            "EPSG:4326"
        )

    else:

        gdf = gdf.to_crs(
            "EPSG:4326"
        )

    return gdf


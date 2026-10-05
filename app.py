
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium

from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go


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

/* =====================================
   FORCE LIGHT MODE STREAMLIT
===================================== */


/* seluruh halaman */
html, body, [class*="css"] {

    background-color: #FFFFFF !important;
    color: #111111 !important;

}


/* container utama */
[data-testid="stAppViewContainer"] {

    background-color:#FFFFFF !important;

}


[data-testid="stMainBlockContainer"] {

    background-color:#FFFFFF !important;

}


/* sidebar */
[data-testid="stSidebar"] {

    background-color:#F8FAFC !important;

}


[data-testid="stSidebar"] * {

    color:#111111 !important;

}


/* semua teks */
p, span, label, div, h1, h2, h3, h4, h5 {

    color:#111111 !important;

}


/* judul */
h1,h2,h3 {

    color:#0F172A !important;

}


/* markdown */
.stMarkdown {

    color:#111111 !important;

}


/* metric card */
[data-testid="stMetric"] {

    background:white !important;

    border-radius:15px;

    padding:15px;

    box-shadow:
    0px 3px 10px rgba(0,0,0,0.08);

}


[data-testid="stMetricLabel"] {

    color:#374151 !important;

}


[data-testid="stMetricValue"] {

    color:#111827 !important;

}


/* dataframe */
[data-testid="stDataFrame"] {

    background:white !important;

}


/* input widget */
input,
textarea,
select {

    background:white !important;

    color:#111111 !important;

}


/* selectbox */
[data-baseweb="select"] {

    background:white !important;

}


[data-baseweb="select"] * {

    color:#111111 !important;

}


/* tombol */
button {

    background:white !important;

    color:#111111 !important;

}


/* navbar */
.navbar {

    background:white;

    padding:15px;

    border-radius:15px;

    box-shadow:
    0 3px 10px rgba(0,0,0,0.12);

    display:flex;

    gap:25px;

    position:sticky;

    top:0;

    z-index:999;

}


.navbar a {

    color:#1D4ED8 !important;

    font-weight:600;

    text-decoration:none;

}


/* hilangkan elemen streamlit */
#MainMenu {

    visibility:hidden;

}


footer {

    visibility:hidden;

}


[data-testid="stToolbar"] {

    visibility:hidden;

}


[data-testid="stDecoration"] {

    display:none;

}

</style>
""",
unsafe_allow_html=True
)


# =====================================================
# DATA LOADING
# =====================================================

@st.cache_data
def load_csv():

    return pd.read_csv(
        "data/hasil_webstory.csv"
    )


@st.cache_data
def load_map():

    gdf = gpd.read_file(
        "data/kecamatan_jatim.zip"
    )


    # pastikan CRS benar

    if gdf.crs is None:

        gdf = gdf.set_crs(
            "EPSG:4326"
        )

    else:

        gdf = gdf.to_crs(
            "EPSG:4326"
        )


    # normalisasi kode kecamatan

    gdf["kode_kec"] = (
        gdf["kode_kec"]
        .astype(str)
        .str.strip()
    )

    gdf["geometry"] = (
        gdf.geometry
        .simplify(
            tolerance=0.002
        )
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

df = load_csv()


df["kode_kecamatan_kemendagri"] = (
    df["kode_kecamatan_kemendagri"]
    .astype(str)
    .str.strip()
)


df = df.sort_values(
    [
        "kode_kecamatan_kemendagri",
        "tahun"
    ]
)


df["growth_ST"] = (
    df.groupby(
        "kode_kecamatan_kemendagri"
    )["EBLUP_ST"]
    .pct_change()
    *100
)



# =====================================================
# NAVBAR
# =====================================================

st.markdown(
"""
<div class="navbar">

<a href="#beranda">🏠 Beranda</a>

<a href="#metodologi">📚 Metodologi</a>

<a href="#data">📊 Data</a>

<a href="#peta">🗺️ Peta</a>

<a href="#evaluasi">📈 Evaluasi</a>

<a href="#kesimpulan">📌 Kesimpulan</a>

</div>
""",
unsafe_allow_html=True
)



# =====================================================
# FILTER
# =====================================================

st.sidebar.title("Filter Eksplorasi")


tahun = st.sidebar.select_slider(
    "Tahun",
    options=sorted(df.tahun.unique()),
    value=max(df.tahun.unique())
)


kab = st.sidebar.selectbox(
    "Kabupaten/Kota",
    ["Semua"] + sorted(df.kab_kota.unique())
)


filtered = df[
    df.tahun == tahun
]


if kab != "Semua":

    filtered = filtered[
        filtered.kab_kota == kab
    ]


kecamatan = st.sidebar.selectbox(
    "Kecamatan",
    ["Semua"] +
    sorted(
        filtered.nama_kecamatan_bps.unique()
    )
)



# =====================================================
# BERANDA
# =====================================================

st.markdown(
'<a id="beranda"></a>',
unsafe_allow_html=True
)

st.title(
"Estimasi Rata-rata Pengeluaran Per Kapita Tingkat Kecamatan Jawa Timur Menggunakan ST-SAE"
)


c1,c2,c3 = st.columns(3)


c1.metric(
    "Jumlah Kecamatan",
    df.kode_kecamatan_kemendagri.nunique()
)

c2.metric(
    "Periode",
    "2018-2025"
)

c3.metric(
    "Observasi",
    len(df)
)


st.markdown(
"""
<div class="card">

Penelitian ini mengembangkan estimasi rata-rata pengeluaran
per kapita tingkat kecamatan menggunakan pendekatan
Spatio-Temporal Small Area Estimation.

Model memanfaatkan informasi:
- direct estimate BPS,
- variabel penyerta,
- hubungan spasial,
- dinamika temporal.

</div>
""",
unsafe_allow_html=True
)



# =====================================================
# METODOLOGI
# =====================================================

st.markdown(
'<a id="metodologi"></a>',
unsafe_allow_html=True
)

st.header("Metodologi Penelitian")


st.markdown(
"""
Data Direct Estimate

↓

Auxiliary Variables

↓

Analisis Spasial Moran's I

↓

Spatial SAE + Temporal SAE

↓

Spatio-Temporal SAE

↓

Evaluasi MSE dan RRMSE
"""
)



# =====================================================
# DATA EXPLORATION
# =====================================================

st.markdown(
'<a id="data"></a>',
unsafe_allow_html=True
)

st.header("Eksplorasi Data")


data_year = df[
    df.tahun == tahun
]


col1,col2 = st.columns(2)


with col1:

    st.plotly_chart(
        px.histogram(
            data_year,
            x="pengeluaran_mean",
            title="Distribusi Direct Estimate"
        ),
        use_container_width=True
    )


with col2:

    st.plotly_chart(
        px.histogram(
            data_year,
            x="EBLUP_ST",
            title="Distribusi ST-SAE"
        ),
        use_container_width=True
    )

# =====================================================
# MAP ST-SAE
# =====================================================


st.markdown(
'<a id="peta"></a>',
unsafe_allow_html=True
)

st.header(
    "Peta Estimasi ST-SAE"
)

gdf = load_map()

    # join geometry + hasil estimasi
map_data = gdf.merge(
    filtered,
    left_on="kode_kec",
    right_on="kode_kecamatan_kemendagri",
    how="inner"
    )

map_mode = st.radio(
    "Mode peta",
    [
        "Satu Tahun",
        "Rata-rata 2018-2025"
    ],
    horizontal=True
    )

if map_mode == "Satu Tahun":
    tahun_map = st.selectbox(
        "Pilih Tahun Peta",
        sorted(
            df.tahun.unique()
        )
    )
    map_values = map_data[
        df["tahun"] == tahun_map
    ].copy()

else:
    map_values = (
        map_data
        .groupby(
            [
            "kode_kec",
            "kecamata",
            "kab_kota",
            "geometry"
            ],
            as_index=False
        )

        .agg(
            EBLUP_ST=(
                "EBLUP_ST",
                "mean"
            ),

            pengeluaran_mean=(
                "pengeluaran_mean",
                "mean"
            ),
            RRMSE_ST=(
                "RRMSE_ST",
                "mean"
            )
        )
    )

value_dict = (
    map_values
    .set_index(
        "kode_kecamatan_kemendagri"
    )
    ["EBLUP_ST","kab_kota", "nama_kecamatan_bps"]
    .to_dict()
)
gdf_map = gdf.copy()

gdf_map["EBLUP_ST"] = (
    gdf_map["kode_kec"]
    .map(value_dict)
)

rrmse_dict = (
    map_values
    .set_index(
        "kode_kecamatan_kemendagri"
    )
    ["RRMSE_ST", "kab_kota", "nama_kecamatan_bps"]
    .to_dict()
)

gdf_map["RRMSE_ST"] = (
    gdf_map["kode_kec"]
    .map(rrmse_dict)
)

avg_data = (

    df
    .groupby(
        "kode_kecamatan_kemendagri",
        as_index=False
    )
    .agg(

        EBLUP_ST=(
            "EBLUP_ST",
            "mean"
        ),

        RRMSE_ST=(
            "RRMSE_ST",
            "mean"
        ),

        pengeluaran_mean=(
            "pengeluaran_mean",
            "mean"
        )

    )

)

value_dict = (
    avg_data
    .set_index(
        "kode_kecamatan_kemendagri"
    )
    ["EBLUP_ST"]
    .to_dict()
)


gdf_map["EBLUP_ST"] = (
    gdf_map["kode_kec"]
    .map(value_dict)
)

if not map_values.empty:
    map_values = map_values.reset_index()

    fig_map = px.choropleth_map(
    gdf_map,

    geojson=
    gdf_map.geometry.__geo_interface__,

    locations=
    gdf_map.index,

    color=
    "EBLUP_ST",

    hover_name=
    "kab_kota",

    map_style=
    "carto-positron",

    center={
        "lat":-7.75,
        "lon":112.5
    },

    zoom=6.5
)

    fig_map.update_layout(
        height=650,
        margin={
            "r":0,
            "t":30,
            "l":0,
            "b":0
        },
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig_map,
        use_container_width=True
        )


else:
    st.warning(
        "Tidak ada data peta."
    )


# =====================================================
# EVALUATION
# =====================================================

st.markdown(
'<a id="evaluasi"></a>',
unsafe_allow_html=True
)

st.header("Evaluasi Model")


summary = pd.DataFrame({

"Model":
[
"Direct",
"Spatial SAE",
"Temporal SAE",
"ST-SAE"
],

"RRMSE":
[
df.RRMSE_direct.mean(),
df.RRMSE_Spatial.mean(),
df.RRMSE_Temporal.mean(),
df.RRMSE_ST.mean()
]

})


st.dataframe(
    summary
)


st.plotly_chart(
    px.bar(
        summary,
        x="Model",
        y="RRMSE"
    ),
    use_container_width=True
)



# =====================================================
# EXPLORATION BY AREA
# =====================================================

st.header("Eksplorasi Kecamatan")


if kecamatan != "Semua":

    temp = df[
        df.nama_kecamatan_bps ==
        kecamatan
    ]


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=temp.tahun,
            y=temp.pengeluaran_mean,
            name="Direct",
            mode="lines+markers"
        )
    )


    fig.add_trace(
        go.Scatter(
            x=temp.tahun,
            y=temp.EBLUP_ST,
            name="ST-SAE",
            mode="lines+markers"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "Pilih kecamatan pada filter untuk melihat perkembangan temporal."
    )



# =====================================================
# DOWNLOAD
# =====================================================

st.header("Download Data")


st.download_button(
    "Download CSV",
    filtered.to_csv(index=False),
    "hasil_ST_SAE.csv",
    "text/csv"
)



# =====================================================
# CONCLUSION
# =====================================================

st.markdown(
'<a id="kesimpulan"></a>',
unsafe_allow_html=True
)


st.header("Kesimpulan")


st.markdown(
"""
- ST-SAE menghasilkan estimasi tingkat kecamatan
  dengan memanfaatkan informasi spasial dan temporal.

- Evaluasi dilakukan menggunakan MSE dan RRMSE.

- Dashboard ini menjadi media eksplorasi hasil penelitian
  dan penyampaian informasi estimasi wilayah.
"""
)

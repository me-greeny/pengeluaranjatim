
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

.main {
    background:#FAFAF8;
}

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


.navbar {

    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:
    0 3px 10px rgba(0,0,0,0.08);

    display:flex;
    gap:25px;

    position:sticky;
    top:0;

    z-index:999;

}


.navbar a {

    color:#1D4ED8;
    font-weight:600;
    text-decoration:none;

}


.card {

    background:white;
    padding:20px;
    border-radius:15px;

    box-shadow:
    0 3px 10px rgba(0,0,0,0.08);

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

    gdf["kode_kecamatan_kemendagri"] = (
        gdf["kode_kec"]
        .astype(str)
        .str.strip()
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
# MAP
# =====================================================

st.markdown(
'<a id="peta"></a>',
unsafe_allow_html=True
)

st.header("Peta Estimasi ST-SAE")


show_map = st.checkbox(
    "Tampilkan Peta"
)


if show_map:

    with st.spinner(
        "Memuat peta..."
    ):

        gdf = load_map()


        map_df = gdf.merge(
            filtered,
            on="kode_kecamatan_kemendagri",
            how="inner"
        )


        variable = st.radio(
            "Variabel",
            [
                "EBLUP_ST",
                "RRMSE_ST",
                "growth_ST"
            ],
            horizontal=True
        )


        if kecamatan != "Semua":

            selected = map_df[
                map_df.nama_kecamatan_bps ==
                kecamatan
            ]

            center = [
                selected.geometry.centroid.y.iloc[0],
                selected.geometry.centroid.x.iloc[0]
            ]

            zoom = 13

        else:

            center=[
                -7.5,
                112.5
            ]

            zoom=8


        m = folium.Map(
            location=center,
            zoom_start=zoom
        )


        folium.Choropleth(
            geo_data=map_df,
            data=map_df,
            columns=[
                "kode_kecamatan_kemendagri",
                variable
            ],
            key_on=
            "feature.properties.kode_kecamatan_kemendagri",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=variable
        ).add_to(m)


        folium.GeoJson(
            map_df,
            tooltip=folium.GeoJsonTooltip(
                fields=[
                    "nama_kecamatan_bps",
                    "kab_kota",
                    "EBLUP_ST",
                    "RRMSE_ST"
                ]
            )
        ).add_to(m)


        st_folium(
            m,
            width=1000,
            height=600
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

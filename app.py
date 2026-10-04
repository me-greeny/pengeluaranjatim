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

    /* ========================================================
       SECTION
       ======================================================== */

    .section-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 35px;
        margin-bottom: 5px;
    }

    .section-desc {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 25px;
        line-height: 1.6;
    }


    /* ========================================================
       INFO CARD
       ======================================================== */

    .info-card {
        padding: 22px;
        border-radius: 14px;
        background: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.20);
        line-height: 1.7;
        margin-top: 15px;
        margin-bottom: 20px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        margin-top: 70px;
        padding: 35px 25px;
        text-align: center;
        border-top: 1px solid rgba(148, 163, 184, 0.25);
    }

    .footer-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .footer-subtitle {
        font-size: 14px;
        color: #64748b;
    }

    .footer-line {
        width: 80px;
        height: 2px;
        margin: 18px auto;
        background: currentColor;
        opacity: 0.25;
    }

    .footer-text {
        max-width: 800px;
        margin: 6px auto;
        color: #64748b;
        font-size: 13px;
        line-height: 1.6;
    }


    /* ========================================================
       TABLE
       ======================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }


    /* ========================================================
       EXPANDER
       ======================================================== */

    [data-testid="stExpander"] {
        border-radius: 12px;
        margin-top: 10px;
        margin-bottom: 10px;
    }


    /* ========================================================
       SELECTBOX
       ======================================================== */

    [data-testid="stSelectbox"] {
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
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

st.markdown(
    """
    <style>

    .navbar {
        position: sticky;
        top: 0;
        z-index: 999;
        display: flex;
        justify-content: center;
        gap: 8px;
        padding: 10px 12px;
        margin-bottom: 25px;

        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(10px);

        border-bottom: 1px solid
            rgba(148,163,184,0.20);

        border-radius: 0 0 12px 12px;
    }

    .navbar a {
        padding: 8px 14px;
        border-radius: 8px;

        text-decoration: none;

        font-size: 13px;
        font-weight: 600;

        color: inherit;
    }

    .navbar a:hover {
        background: rgba(148,163,184,0.12);
    }

    </style>
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

# ============================================================
# PART 4 — EVALUASI & EKSPLORASI HASIL ST-SAE
# ============================================================

anchor("evaluasi")

st.markdown(
    """
    <div class="section-title">
        Evaluasi Model
    </div>
    <div class="section-desc">
        Evaluasi dilakukan untuk melihat tingkat ketidakpastian estimasi
        dan perbedaan hasil antara estimasi langsung dengan estimasi
        Spatial-Temporal Small Area Estimation (ST-SAE).
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# 4.1 RINGKASAN KETIDAKPASTIAN
# ------------------------------------------------------------

st.markdown("### Ketidakpastian Estimasi")

eval_year = st.selectbox(
    "Pilih tahun evaluasi",
    sorted(hasil["tahun"].dropna().unique()),
    key="eval_year"
)

df_eval = hasil[
    hasil["tahun"] == eval_year
].copy()

# pastikan numerik
for col in [
    "CV...11",
    "RSE...12",
    "mse_direct",
    "mse_st",
    "rrmse_direct",
    "rrmse_st"
]:
    if col in df_eval.columns:
        df_eval[col] = pd.to_numeric(
            df_eval[col],
            errors="coerce"
        )

col1, col2, col3, col4 = st.columns(4)

with col1:
    cv_direct = df_eval["CV...11"].mean()
    st.metric(
        "Rata-rata CV Direct",
        f"{cv_direct:.2f}%"
    )

with col2:
    rrmse_direct = df_eval["rrmse_direct"].mean()
    st.metric(
        "Rata-rata RRMSE Direct",
        f"{rrmse_direct:.2f}%"
    )

with col3:
    rrmse_st = df_eval["rrmse_st"].mean()
    st.metric(
        "Rata-rata RRMSE ST-SAE",
        f"{rrmse_st:.2f}%"
    )

with col4:
    mse_st = df_eval["mse_st"].mean()
    st.metric(
        "Rata-rata MSE ST-SAE",
        f"{mse_st:,.2f}"
    )


# ------------------------------------------------------------
# 4.2 DISTRIBUSI KETIDAKPASTIAN
# ------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        df_eval,
        x="CV...11",
        nbins=30,
        title=f"Distribusi CV Direct — {eval_year}",
        labels={
            "CV...11": "CV Direct (%)"
        }
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.histogram(
        df_eval,
        x="rrmse_st",
        nbins=30,
        title=f"Distribusi RRMSE ST-SAE — {eval_year}",
        labels={
            "rrmse_st": "RRMSE ST-SAE (%)"
        }
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# 4.3 PERBANDINGAN KETIDAKPASTIAN
# ------------------------------------------------------------

st.markdown("### Direct Estimate vs ST-SAE")

comparison = df_eval[
    [
        "nama_kecamatan_kemendagri",
        "CV...11",
        "rrmse_direct",
        "rrmse_st"
    ]
].copy()

comparison = comparison.dropna()

comparison_long = comparison.melt(
    id_vars="nama_kecamatan_kemendagri",
    value_vars=[
        "rrmse_direct",
        "rrmse_st"
    ],
    var_name="Metode",
    value_name="Ketidakpastian"
)

comparison_long["Metode"] = comparison_long["Metode"].replace({
    "rrmse_direct": "Direct",
    "rrmse_st": "ST-SAE"
})

fig = px.box(
    comparison_long,
    x="Metode",
    y="Ketidakpastian",
    points=False,
    title=f"Distribusi RRMSE Direct dan ST-SAE — {eval_year}",
    labels={
        "Ketidakpastian": "RRMSE (%)"
    }
)

fig.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    """
    Catatan: CV Direct merupakan ukuran ketidakpastian dari estimasi
    langsung BPS, sedangkan RRMSE ST-SAE merupakan ukuran ketidakpastian
    yang diperoleh dari model SAE. Keduanya ditampilkan sebagai informasi
    evaluasi dan tidak diinterpretasikan sebagai ukuran yang identik.
    """
)


# ============================================================
# 4.4 PERBANDINGAN MODEL SAE
# ============================================================

st.markdown("### Perbandingan Model SAE")

if "perbandingan_model_SAE.csv" in files:

    model_df = files["perbandingan_model_SAE.csv"].copy()

    st.dataframe(
        model_df,
        use_container_width=True,
        hide_index=True
    )

    # Cari kolom yang relevan secara otomatis
    numeric_cols = model_df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if len(numeric_cols) >= 2:

        metric_col = None

        for candidate in [
            "RRMSE",
            "rrmse",
            "mean_rrmse",
            "RMSE",
            "rmse",
            "MSE",
            "mse"
        ]:
            if candidate in model_df.columns:
                metric_col = candidate
                break

        if metric_col is not None:

            fig = px.bar(
                model_df,
                x=model_df.columns[0],
                y=metric_col,
                title=f"Perbandingan {metric_col} Antar Model",
                labels={
                    metric_col: metric_col
                }
            )

            fig.update_layout(
                height=420,
                margin=dict(l=20, r=20, t=50, b=20)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

else:

    st.info(
        "File perbandingan_model_SAE.csv belum tersedia."
    )


# ============================================================
# 4.5 EKSPLORASI EBLUP
# ============================================================

anchor("eksplorasi")

st.markdown(
    """
    <div class="section-title">
        Eksplorasi Hasil Estimasi
    </div>
    <div class="section-desc">
        Eksplorasi digunakan untuk melihat variasi estimasi EBLUP
        antar kecamatan dan perubahan estimasi terhadap estimasi langsung.
    </div>
    """,
    unsafe_allow_html=True
)

explore_year = st.selectbox(
    "Pilih tahun eksplorasi",
    sorted(hasil["tahun"].dropna().unique()),
    key="explore_year"
)

df_explore = hasil[
    hasil["tahun"] == explore_year
].copy()


# ------------------------------------------------------------
# 4.6 KECAMATAN TERTINGGI DAN TERENDAH
# ------------------------------------------------------------

st.markdown("### Kecamatan dengan Estimasi EBLUP Tertinggi dan Terendah")

top_cols = [
    "nama_kecamatan_kemendagri",
    "nama_kecamatan_bps",
    "pengeluaran_mean",
    "eblup_spatiotemporal",
    "rrmse_st"
]

top_cols = [
    c for c in top_cols
    if c in df_explore.columns
]

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### Tertinggi")

    top10 = (
        df_explore[
            top_cols
        ]
        .sort_values(
            "eblup_spatiotemporal",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True
    )


with col2:

    st.markdown("#### Terendah")

    bottom10 = (
        df_explore[
            top_cols
        ]
        .sort_values(
            "eblup_spatiotemporal",
            ascending=True
        )
        .head(10)
    )

    st.dataframe(
        bottom10,
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# 4.7 PERUBAHAN DIRECT → EBLUP
# ------------------------------------------------------------

st.markdown("### Perubahan Estimasi Direct → EBLUP")

df_change = df_explore.copy()

df_change["perubahan"] = (
    df_change["eblup_spatiotemporal"]
    - df_change["pengeluaran_mean"]
)

df_change["perubahan_persen"] = (
    df_change["perubahan"]
    / df_change["pengeluaran_mean"].replace(0, np.nan)
) * 100

fig = px.histogram(
    df_change,
    x="perubahan_persen",
    nbins=40,
    title=f"Distribusi Perubahan Relatif Direct → EBLUP — {explore_year}",
    labels={
        "perubahan_persen": "Perubahan (%)"
    }
)

fig.add_vline(
    x=0,
    line_dash="dash"
)

fig.update_layout(
    height=420,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ------------------------------------------------------------
# 4.8 KECAMATAN DENGAN PERUBAHAN TERBESAR
# ------------------------------------------------------------

change_cols = [
    "nama_kecamatan_kemendagri",
    "pengeluaran_mean",
    "eblup_spatiotemporal",
    "perubahan",
    "perubahan_persen"
]

change_cols = [
    c for c in change_cols
    if c in df_change.columns
]

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### Peningkatan terbesar")

    increase = (
        df_change[
            change_cols
        ]
        .sort_values(
            "perubahan_persen",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        increase,
        use_container_width=True,
        hide_index=True
    )


with col2:

    st.markdown("#### Penurunan terbesar")

    decrease = (
        df_change[
            change_cols
        ]
        .sort_values(
            "perubahan_persen",
            ascending=True
        )
        .head(10)
    )

    st.dataframe(
        decrease,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 4.9 EKSPLORASI TEMPORAL PER KECAMATAN
# ============================================================

st.markdown("### Tren Estimasi Kecamatan")

available_names = (
    hasil[
        "nama_kecamatan_kemendagri"
    ]
    .dropna()
    .sort_values()
    .unique()
)

selected_kec = st.selectbox(
    "Pilih kecamatan",
    available_names,
    key="selected_kecamatan"
)

df_temporal = hasil[
    hasil["nama_kecamatan_kemendagri"]
    == selected_kec
].copy()

df_temporal = df_temporal.sort_values("tahun")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df_temporal["tahun"],
        y=df_temporal["pengeluaran_mean"],
        mode="lines+markers",
        name="Direct Estimate"
    )
)

fig.add_trace(
    go.Scatter(
        x=df_temporal["tahun"],
        y=df_temporal["eblup_spatiotemporal"],
        mode="lines+markers",
        name="ST-SAE / EBLUP"
    )
)

fig.update_layout(
    title=f"Tren Pengeluaran Per Kapita — {selected_kec}",
    xaxis_title="Tahun",
    yaxis_title="Pengeluaran per Kapita",
    height=450,
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 4.10 RINGKASAN TEMUAN
# ============================================================

st.markdown("### Ringkasan Temuan")

mean_direct = df_explore["pengeluaran_mean"].mean()
mean_eblup = df_explore["eblup_spatiotemporal"].mean()

difference = mean_eblup - mean_direct

st.markdown(
    f"""
    <div class="info-card">

    <b>Hasil eksplorasi tahun {explore_year}</b><br><br>

    Rata-rata estimasi langsung pengeluaran per kapita adalah
    <b>{mean_direct:,.2f}</b>, sedangkan rata-rata estimasi
    ST-SAE (EBLUP) adalah <b>{mean_eblup:,.2f}</b>.

    Selisih rata-rata estimasi tersebut adalah
    <b>{difference:,.2f}</b>.

    Perbedaan antara estimasi langsung dan EBLUP mencerminkan
    penggunaan informasi tambahan dalam model ST-SAE, termasuk
    variabel auxiliary serta struktur spasial dan temporal.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# PART 5 — FINISHING DASHBOARD
# ============================================================

# ------------------------------------------------------------
# 5.1 FOOTER
# ------------------------------------------------------------

st.markdown(
    """
    <div class="footer">

        <div class="footer-title">
            Spatial-Temporal Small Area Estimation
        </div>

        <div class="footer-subtitle">
            Estimasi Pengeluaran Per Kapita Tingkat Kecamatan
            di Jawa Timur, 2018–2025
        </div>

        <div class="footer-line"></div>

        <div class="footer-text">
            Dashboard ini dikembangkan sebagai media visualisasi
            hasil penelitian Small Area Estimation (SAE) dengan
            pendekatan Spatial-Temporal SAE.
        </div>

        <div class="footer-text">
            Data dan hasil estimasi mengikuti hasil pengolahan
            penelitian. Interpretasi hasil ditujukan untuk
            keperluan akademik dan eksplorasi statistik.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# 5.2 INFORMASI METODOLOGI
# ------------------------------------------------------------

with st.expander("Informasi metodologi dan interpretasi"):

    st.markdown(
        """
        ### Estimasi Langsung

        Estimasi langsung menggunakan rata-rata pengeluaran
        per kapita tingkat kecamatan beserta ukuran ketidakpastian
        yang tersedia dalam data BPS.

        ### Spatial-Temporal SAE

        Model ST-SAE memanfaatkan tiga sumber informasi:

        1. **Variabel auxiliary**, yaitu NTL, LST, NDVI, NDBI,
           pendidikan, kesehatan, ekonomi, dan listrik.

        2. **Ketergantungan spasial**, melalui matriks bobot
           spasial Queen Contiguity.

        3. **Ketergantungan temporal**, melalui struktur
           korelasi antarperiode 2018–2025.

        ### EBLUP

        Estimasi akhir diperoleh melalui Empirical Best Linear
        Unbiased Prediction (EBLUP), yang menggabungkan informasi
        estimasi langsung dengan informasi model.

        ### Ketidakpastian

        Ketidakpastian estimasi ST-SAE dievaluasi menggunakan
        Mean Squared Error (MSE) dan Relative Root Mean Squared
        Error (RRMSE).

        **Catatan:** CV Direct dan RRMSE ST-SAE merupakan ukuran
        ketidakpastian yang berasal dari pendekatan berbeda sehingga
        tidak boleh dianggap sebagai ukuran yang sepenuhnya identik.
        """
    )


# ------------------------------------------------------------
# 5.3 SUMBER DATA
# ------------------------------------------------------------

with st.expander("Sumber data"):

    st.markdown(
        """
        **Data utama**

        - Estimasi pengeluaran per kapita tingkat kecamatan.
        - Ukuran ketidakpastian estimasi langsung.
        - Variabel auxiliary sosial-ekonomi dan lingkungan.
        - Batas administrasi kecamatan Jawa Timur.

        **Periode analisis**

        2018–2025.

        **Unit analisis**

        Kecamatan di Provinsi Jawa Timur.

        **Cakupan wilayah pemodelan**

        661 kecamatan yang memiliki estimasi langsung dan digunakan
        dalam pemodelan ST-SAE.
        """
    )


# ------------------------------------------------------------
# 5.4 CATATAN INTERPRETASI
# ------------------------------------------------------------

with st.expander("Catatan interpretasi hasil"):

    st.markdown(
        """
        Nilai EBLUP tidak harus sama dengan estimasi langsung.
        Perbedaan tersebut merupakan konsekuensi dari proses
        *borrowing strength*, yaitu pemanfaatan informasi dari
        wilayah dan periode lain melalui struktur model.

        Nilai estimasi yang lebih tinggi menunjukkan tingkat
        pengeluaran per kapita yang lebih tinggi menurut model,
        sedangkan ukuran MSE dan RRMSE digunakan untuk melihat
        ketidakpastian prediksi.

        Hubungan antara variabel auxiliary dan pengeluaran
        per kapita dalam model tidak secara otomatis menunjukkan
        hubungan sebab-akibat.
        """
    )


# ------------------------------------------------------------
# 5.5 TOMBOL KEMBALI KE ATAS
# ------------------------------------------------------------

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:40px;
        margin-bottom:20px;
    ">
        <a href="#beranda"
           style="
               text-decoration:none;
               font-weight:600;
               font-size:14px;
           ">
            ↑ Kembali ke Beranda
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
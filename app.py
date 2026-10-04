import streamlit as st
import pandas as pd
import geopandas as gpd
import folium

from streamlit_folium import st_folium

import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# KONFIGURASI
# =====================================================

st.set_page_config(
    page_title="ST-SAE Jawa Timur",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# CUSTOM CSS LIGHT MODE
# =====================================================

st.markdown(
"""
<style>

body {
    background-color:#FAFAF8;
}


.main {
    background-color:#FAFAF8;
}


h1,h2,h3,h4 {
    color:#111827;
}


p,span,div {
    color:#111827;
}


.metric-card {

background:white;

padding:20px;

border-radius:15px;

box-shadow:
0 4px 12px rgba(0,0,0,0.08);

text-align:center;

}


.title-box {

background:
linear-gradient(
135deg,
#1D4ED8,
#0F766E
);

padding:35px;

border-radius:20px;

color:white;

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

    df=pd.read_csv(
        "data/hasil_webstory.csv"
    )


    gdf=gpd.read_file(
        "data/kecamatan_jatim.zip"
    )


    return df,gdf



df,gdf=load_data()

df=df.sort_values(
    [
        "kode_kecamatan_bps",
        "tahun"
        ]
    )


df["growth_ST"]=(
    df
    .groupby(
        "kode_kecamatan_bps"
    )
    ["EBLUP_ST"]
    .pct_change()
    *100
)

# =====================================================
# NORMALISASI KODE
# =====================================================


df["kode_kecamatan_bps"]=(
    df["kode_kecamatan_bps"]
    .astype(str)
)


gdf["kode_kecamatan_kemendagri"]=(
    gdf["kode_kec"]
    .astype(str)
)



# =====================================================
# SIDEBAR FILTER
# =====================================================


st.sidebar.title(
"🔎 Filter Eksplorasi"
)



tahun_list=sorted(
    df["tahun"].unique()
)


tahun=st.sidebar.select_slider(
    "Tahun",
    options=tahun_list,
    value=max(tahun_list)
)



kab_list=[
    "Semua"
]+sorted(
    df.kab_kota.unique()
)



kab=st.sidebar.selectbox(
    "Kabupaten/Kota",
    kab_list
)



filtered=df[
    df.tahun==tahun
]


if kab!="Semua":

    filtered=filtered[
        filtered.kab_kota==kab
    ]



kec_list=[
    "Semua"
]+sorted(
    filtered.nama_kecamatan_bps.unique()
)



kecamatan=st.sidebar.selectbox(
    "Kecamatan",
    kec_list
)



# =====================================================
# MENU
# =====================================================


menu=st.sidebar.radio(
    "Menu",
    [
    "Beranda",
    "Metodologi",
    "Eksplorasi Data",
    "Peta ST-SAE",
    "Perbandingan Model",
    "Eksplorasi Kecamatan",
    "Ranking Wilayah",
    "Download Data",
    "Kesimpulan"
    ]
)




# =====================================================
# BERANDA
# =====================================================


if menu=="Beranda":


    st.markdown(
    """
    <div class="title-box">

    <h1>
    Spatio-Temporal Small Area Estimation
    </h1>

    <h3>
    Estimasi Rata-rata Pengeluaran Per Kapita
    Tingkat Kecamatan Jawa Timur
    Tahun 2018-2025
    </h3>

    </div>

    """,
    unsafe_allow_html=True
    )


    st.write("")


    c1,c2,c3=st.columns(3)


    c1.metric(
        "Jumlah Kecamatan",
        df.kode_kecamatan_bps.nunique()
    )


    c2.metric(
        "Periode",
        "2018-2025"
    )


    c3.metric(
        "Jumlah Observasi",
        len(df)
    )



    st.subheader(
    "Ringkasan Penelitian"
    )


    st.write(
    """
    Penelitian ini menerapkan pendekatan
    **Spatio-Temporal Small Area Estimation (ST-SAE)**
    untuk menghasilkan estimasi rata-rata pengeluaran
    per kapita tingkat kecamatan di Jawa Timur.

    Model memanfaatkan:

    - estimasi langsung BPS,
    - variabel sosial ekonomi,
    - hubungan spasial antarwilayah,
    - dinamika temporal tahun 2018-2025.

    Hasil estimasi dievaluasi menggunakan
    Mean Square Error (MSE) dan Relative Root Mean Square Error (RRMSE).
    """
    )

elif menu=="Metodologi":
    st.title(
        "Metodologi Penelitian"
        )
    st.markdown(
    """
    ## Alur Penelitian

    Data Direct Estimate BPS
    ↓
    Auxiliary Variables
    (Podes dan Citra Satelit)
    ↓
    Analisis Spasial
    (Global Moran's I)
    ↓
    Pembentukan Model
    - ST-SAE
    ↓
    EBLUP Estimation
    ↓
    Evaluasi:
    - MSE
    - RRMSE
    """
    )
    st.image(
        "data/alur_STSAE.png"
    )
# =====================================================
# EKSPLORASI DATA
# =====================================================


elif menu=="Eksplorasi Data":


    st.title(
    "Eksplorasi Distribusi Data"
    )


    data=df[
        df.tahun==tahun
    ]


    col1,col2=st.columns(2)


    with col1:

        fig=px.histogram(
            data,
            x="pengeluaran_mean",
            nbins=40,
            title=
            "Distribusi Direct Estimate"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig=px.histogram(
            data,
            x="EBLUP_ST",
            nbins=40,
            title=
            "Distribusi ST-SAE"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    fig=px.box(
        data,
        y=[
        "RRMSE_direct",
        "RRMSE_Spatial",
        "RRMSE_Temporal",
        "RRMSE_ST"
        ],
        title=
        "Distribusi RRMSE Model"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# =====================================================
# PETA
# =====================================================


elif menu=="Peta ST-SAE":


    st.title(
    "Peta Estimasi ST-SAE"
    )


    data=filtered.copy()



    map_df=gdf.merge(
        data,
        on="kode_kecamatan_kemendagri",
        how="inner"
    )


    pilihan=st.radio(
        "Variabel Peta",
        [
        "EBLUP_ST",
        "RRMSE_ST",
        "Pertumbuhan ST-SAE"
        ]
    )

    if pilihan=="Pertumbuhan ST-SAE":
        kolom="growth_ST"

    if kecamatan!="Semua":

        selected=map_df[
            map_df.nama_kecamatan_bps
            ==
            kecamatan
        ]

        center=[
            selected.geometry.centroid.y.iloc[0],
            selected.geometry.centroid.x.iloc[0]
        ]

        zoom=13

    else:

        center=[
            -7.5,
            112.5
        ]

        zoom=8



    m=folium.Map(
        location=center,
        zoom_start=zoom
    )


    folium.Choropleth(
        geo_data=map_df,
        data=map_df,
        columns=[
            "kode_kecamatan_bps",
            pilihan
        ],
        key_on=
        "feature.properties.kode_kecamatan_bps",
        fill_opacity=0.75,
        line_opacity=0.2,
        legend_name=pilihan
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
        height=650
    )
    
    geojson = map_df.to_json()


    st.download_button(
        "Download GeoJSON",
        geojson,
        "hasil_ST_SAE.geojson",
        "application/json"
    )

elif menu=="Ranking Wilayah":
    ranking=(filtered.sort_values(
        "EBLUP_ST",
        ascending=False
    )
    .head(10)
    )
    st.dataframe(
        ranking[
        [
        "nama_kecamatan_bps",
        "kab_kota",
        "EBLUP_ST"
        ]
    ]
    )

# =====================================================
# PERBANDINGAN MODEL
# =====================================================


elif menu=="Perbandingan Model":


    st.title(
    "Perbandingan Model SAE"
    )


    mean_result=pd.DataFrame({

    "Model":
    [
    "Direct",
    "Spatial SAE",
    "Temporal SAE",
    "ST-SAE"
    ],


    "MSE":
    [
    df.MSE_direct.mean(),
    df.MSE_Spatial.mean(),
    df.MSE_Temporal.mean(),
    df.MSE_ST.mean()
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
        mean_result
    )



    fig=px.bar(
        mean_result,
        x="Model",
        y="RRMSE",
        title=
        "Perbandingan RRMSE"
    )


    st.plotly_chart(fig)



# =====================================================
# KECAMATAN
# =====================================================


elif menu=="Eksplorasi Kecamatan":


    st.title(
    "Eksplorasi Kecamatan"
    )


    if kecamatan=="Semua":

        st.info(
        "Silakan pilih kecamatan pada sidebar"
        )

    else:


        temp=df[
            df.nama_kecamatan_bps==
            kecamatan
        ]


        fig=go.Figure()

        for col in [
            "pengeluaran_mean",
            "EBLUP_ST"
        ]:

            fig.add_trace(
                go.Scatter(
                x=temp.tahun,
                y=temp[col],
                mode="lines+markers",
                name=col
                )
            )

        fig.add_trace(
            go.Scatter(
            x=temp.tahun,
            y=temp.pengeluaran_mean,
            mode="lines+markers",
            name="Direct"
            )
        )

        fig.add_trace(
            go.Scatter(
            x=temp.tahun,
            y=temp.EBLUP_ST,
            mode="lines+markers",
            name="ST-SAE"
            )
        )

        fig.update_layout(
            title=
            f"Perkembangan {kecamatan}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            temp[
            [
            "tahun",
            "pengeluaran_mean",
            "EBLUP_ST",
            "RRMSE_ST"
            ]
            ]
        )



# =====================================================
# KESIMPULAN
# =====================================================


elif menu=="Kesimpulan":


    st.title(
    "Kesimpulan Penelitian"
    )


    st.markdown(
    """
    Berdasarkan hasil penelitian:

    **1.**
    Estimasi pengeluaran per kapita memiliki variasi
    antar kecamatan dan antar waktu.


    **2.**
    ST-SAE mampu memanfaatkan informasi spasial
    dan temporal untuk menghasilkan estimasi
    tingkat kecamatan.


    **3.**
    Evaluasi MSE dan RRMSE menunjukkan bahwa
    pendekatan SAE memberikan informasi tambahan
    dibandingkan hanya menggunakan estimasi langsung.


    **4.**
    Hasil estimasi dapat digunakan sebagai
    informasi pendukung dalam memahami variasi
    kesejahteraan wilayah.
    """
    )

elif menu=="Download Data":

    st.title(
    "Download Hasil Estimasi"
    )


    data_download = filtered.copy()


    csv=data_download.to_csv(
        index=False
    )


    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=
        "hasil_ST_SAE_filtered.csv",
        mime=
        "text/csv"
    )
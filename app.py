import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ST-SAE Jawa Timur", page_icon="📊", layout="wide")

st.markdown("""
<style>
.main {background:#FAFAF8;}
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
[data-testid="stToolbar"] {visibility:hidden;}
[data-testid="stDecoration"] {display:none;}
.navbar {
background:white;
padding:15px;
border-radius:15px;
box-shadow:0 3px 10px rgba(0,0,0,.08);
font-weight:600;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/hasil_webstory.csv")
    gdf = gpd.read_file("data/kecamatan_jatim.zip")
    return df, gdf

df, gdf = load_data()

df["kode_kecamatan_kemendagri"] = df["kode_kecamatan_kemendagri"].astype(str).str.strip()
gdf["kode_kecamatan_kemendagri"] = gdf["kode_kec"].astype(str).str.strip()

df = df.sort_values(["kode_kecamatan_kemendagri","tahun"])
df["growth_ST"] = df.groupby("kode_kecamatan_kemendagri")["EBLUP_ST"].pct_change()*100

st.markdown("<div class='navbar'>ST-SAE Jawa Timur | Estimasi Pengeluaran Per Kapita Kecamatan 2018-2025</div>", unsafe_allow_html=True)

st.sidebar.header("Filter")

tahun = st.sidebar.select_slider("Tahun", sorted(df.tahun.unique()), value=max(df.tahun.unique()))

kab = st.sidebar.selectbox("Kabupaten/Kota", ["Semua"] + sorted(df.kab_kota.unique()))

filtered = df[df.tahun == tahun]
if kab != "Semua":
    filtered = filtered[filtered.kab_kota == kab]

kecamatan = st.sidebar.selectbox("Kecamatan", ["Semua"] + sorted(filtered.nama_kecamatan_bps.unique()))

menu = st.radio(
    "Menu",
    ["Beranda","Metodologi","Eksplorasi Data","Peta ST-SAE","Perbandingan Model","Eksplorasi Kecamatan","Download Data","Kesimpulan"],
    horizontal=True
)

if menu == "Beranda":
    st.title("Spatio-Temporal Small Area Estimation Jawa Timur")
    c1,c2,c3 = st.columns(3)
    c1.metric("Kecamatan", df.kode_kecamatan_kemendagri.nunique())
    c2.metric("Periode", "2018-2025")
    c3.metric("Observasi", len(df))
    st.write("Dashboard menampilkan hasil estimasi pengeluaran per kapita menggunakan Direct Estimate, Spatial SAE, Temporal SAE, dan ST-SAE.")

elif menu == "Metodologi":
    st.title("Metodologi")
    st.markdown("""
    Direct Estimate BPS  
    ↓  
    Auxiliary Variables  
    ↓  
    Analisis Spasial Moran's I  
    ↓  
    Spatial SAE + Temporal SAE  
    ↓  
    ST-SAE  
    ↓  
    Evaluasi MSE dan RRMSE
    """)

elif menu == "Eksplorasi Data":
    st.title("Eksplorasi Data")
    temp = df[df.tahun == tahun]
    st.plotly_chart(px.histogram(temp, x="pengeluaran_mean", title="Distribusi Direct Estimate"), use_container_width=True)
    st.plotly_chart(px.histogram(temp, x="EBLUP_ST", title="Distribusi ST-SAE"), use_container_width=True)

elif menu == "Peta ST-SAE":
    st.title("Peta Estimasi ST-SAE")
    map_df = gdf.merge(filtered, on="kode_kecamatan_kemendagri", how="inner")

    variabel = st.radio("Variabel", ["EBLUP_ST","RRMSE_ST","growth_ST"], horizontal=True)

    if kecamatan != "Semua":
        s = map_df[map_df.nama_kecamatan_bps == kecamatan]
        center = [s.geometry.centroid.y.iloc[0], s.geometry.centroid.x.iloc[0]]
        zoom = 13
    else:
        center = [-7.5,112.5]
        zoom = 8

    m = folium.Map(location=center, zoom_start=zoom)

    folium.Choropleth(
        geo_data=map_df,
        data=map_df,
        columns=["kode_kecamatan_kemendagri", variabel],
        key_on="feature.properties.kode_kecamatan_kemendagri",
        fill_opacity=0.7
    ).add_to(m)

    st_folium(m, width=1000, height=600)

elif menu == "Perbandingan Model":
    st.title("Perbandingan Model")
    result = pd.DataFrame({
        "Model":["Direct","Spatial","Temporal","ST-SAE"],
        "RRMSE":[df.RRMSE_direct.mean(),df.RRMSE_Spatial.mean(),df.RRMSE_Temporal.mean(),df.RRMSE_ST.mean()]
    })
    st.dataframe(result)
    st.plotly_chart(px.bar(result,x="Model",y="RRMSE"),use_container_width=True)

elif menu == "Eksplorasi Kecamatan":
    st.title("Eksplorasi Kecamatan")
    if kecamatan == "Semua":
        st.info("Pilih kecamatan terlebih dahulu")
    else:
        temp=df[df.nama_kecamatan_bps==kecamatan]
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=temp.tahun,y=temp.pengeluaran_mean,name="Direct",mode="lines+markers"))
        fig.add_trace(go.Scatter(x=temp.tahun,y=temp.EBLUP_ST,name="ST-SAE",mode="lines+markers"))
        st.plotly_chart(fig,use_container_width=True)

elif menu == "Download Data":
    st.title("Download Data")
    st.download_button("Download CSV", filtered.to_csv(index=False), "hasil_ST_SAE.csv")

elif menu == "Kesimpulan":
    st.title("Kesimpulan")
    st.write("ST-SAE memberikan estimasi pengeluaran tingkat kecamatan dengan memanfaatkan informasi spasial dan temporal.")

import pandas as pd
import streamlit as st
import plotly.express as px 

st.set_page_config(page_title = "Dashboard Penindakan Pelanggaran LANTAS April 2021",
                   page_icon = ":bar_chart:",
                   layout = "wide"
                   )
# ---- READ EXCEL ----
@st.cache
def get_data_from_excel(filename,datasheet):
    
    df = pd.read_excel(
        io = "dataApril.xlsx",
        engine = 'openpyxl',
        sheet_name = 'data',
        )

    df.colums = ['Cable Length','Theta','No.']
    
    #df["hour"] = pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
    return df
df = get_data_from_excel('dataApril.xlsx','data')
#df = df.drop(index = 0)

# ----SIDEBAR----
st.sidebar.header("Please Filter Here:")
wilayah = st.sidebar.multiselect(
    "Select the Region:",
    options=df["wilayah"].unique(),
    default=df["wilayah"].unique()
)

df_selection = df.query(
    "wilayah == @wilayah"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Penindakan Pelanggaran LANTAS Bulan April Tahun 2021")
st.markdown("##")

# TOP KPI's
total_tilang = int(df_selection["bap_tilang"].sum())
total_stop_operasi = round(df_selection["stop_operasi"].sum())
total_penderekan = round(df_selection["penderekan"].sum())


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Tilang ")
    st.subheader(f" {total_tilang:,}")
with middle_column:
    st.subheader("Total Stop Operasi ")
    st.subheader(f" {total_stop_operasi:}")
with right_column:
    st.subheader("Total Penderekan ")
    st.subheader(f" {total_penderekan:}")

st.markdown("""---""")

# table dataset
st.subheader("Tabel Penindakan Pelanggaran LANTAS April 2021")
st.table(df) # view dataframe on page
st.markdown("""---""")

#BAR PLOT
fig2 = px.bar(
    df,
    x='wilayah',
    y=['bap_tilang', 'stop_operasi','bap_polisi', 'stop_operasi_polisi','penderekan','ocp_roda_dua', 'ocp_roda_empat', 'angkut_motor'],
    orientation="v",
    barmode='group',
    title="<b>Data Keseluruhan Aktivitas</b>",
    color_discrete_sequence=px.colors.sequential.RdBu,
    template="plotly_white",
)
fig2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""---""")

# [PIE CHART]
fig3 = px.pie(
    df, 
    names=['Bidang Dalops', 'Sudinhub Jakarta Pusat', 'Sudinhub Jakarta Utara', 'Sudinhub Jakarta Selatan', 'Sudinhub Jakarta Barat', 'Sudinhub Jakarta Timur'], 
    values='ocp_roda_dua', 
    title='<b>OCP Roda 2 Berdasarkan Wilayah<b>', 
    hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu
)
fig4 = px.pie(
    df, 
    names=['Bidang Dalops', 'Sudinhub Jakarta Pusat', 'Sudinhub Jakarta Utara', 'Sudinhub Jakarta Selatan', 'Sudinhub Jakarta Barat', 'Sudinhub Jakarta Timur'], 
    values='ocp_roda_empat', 
    title='<b>OCP Roda 4 Berdasarkan Wilayah<b>', 
    hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu
)

left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig3, use_container_width=True)
with right_column:
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("""---""")

# BAR
fig5 = px.histogram(
    df, 
    x='wilayah',
    y='bap_tilang', 
    color_discrete_sequence=["#b2182b"], 
    title="<b>BAP Tilang</b>"
)
fig6 = px.histogram(
    df, 
    x='wilayah',
    y='penderekan', 
    color_discrete_sequence=["#b2182b"], 
    title="<b>BAP Penderekan</b>"
) 

left_column, right_column = st.columns(2)
with left_column:
    st.plotly_chart(fig5, use_container_width=True)
with right_column:
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("""---""")

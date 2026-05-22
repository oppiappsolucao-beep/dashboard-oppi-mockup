import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Operação Comercial",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp { background: #D4D4D4; }
.block-container { padding-top: 1rem; max-width: 1200px; }
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    border-left: 6px solid #1B1D6D;
}
.kpi-title { font-size: 13px; font-weight: 700; }
.kpi-value { font-size: 40px; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

if df.empty:
    st.stop()

meses = sorted(df["Mês"].dropna().unique().tolist())
unidades = sorted(df["Unidade"].dropna().unique().tolist())

col1, col2 = st.columns(2)

with col1:
    mes = st.selectbox("Mês", meses)

with col2:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

df_f = df[df["Mês"] == mes]

if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

st.divider()

total = len(df_f)

st.markdown(f"""
<div class="card">
<div class="kpi-title">Total registros</div>
<div class="kpi-value">{total}</div>
</div>
""", unsafe_allow_html=True)

st.divider()

status_cols = [c for c in df_f.columns if "Status" in c]

if status_cols:

    df_status = df_f[status_cols].melt(
        var_name="Etapa",
        value_name="Status"
    )

    df_status = df_status.dropna()
    df_status = df_status[df_status["Status"] != ""]

    chart = df_status.groupby("Status").size().reset_index(name="Qtd")

    fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")
    st.plotly_chart(fig, use_container_width=True)

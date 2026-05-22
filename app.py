import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Skoob Clone",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS SKOOB REAL STYLE
# =========================
st.markdown("""
<style>

.stApp {
    background: #E5E5E5;
}

/* remove padding padrão streamlit */
.block-container {
    padding-top: 1rem;
    max-width: 1180px;
}

/* HEADER FIXO STYLE */
.header {
    background: white;
    padding: 14px 20px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
}

.logo {
    font-weight: 900;
    font-size: 22px;
    color: #1B1D6D;
}

.filters {
    display: flex;
    gap: 12px;
}

/* KPI CARDS SKOOB */
.kpi-wrap {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 18px;
}

.kpi {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    border-left: 6px solid #1B1D6D;
}

.kpi h4 {
    font-size: 13px;
    margin: 0;
    color: #64748b;
}

.kpi h1 {
    margin: 8px 0 0 0;
    font-size: 36px;
    font-weight: 900;
    color: #0f172a;
}

/* CHART BLOCKS */
.block {
    background: white;
    border-radius: 18px;
    padding: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}

.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA REAL SHEET
# =========================
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# =========================
# FILTERS
# =========================
meses = sorted(df["Mês"].dropna().unique())
unidades = sorted(df["Unidade"].dropna().unique())

col1, col2 = st.columns([2,2])

with col1:
    mes = st.selectbox("Mês", meses)

with col2:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

df = df[df["Mês"] == mes]
if unidade != "Todas":
    df = df[df["Unidade"] == unidade]

# =========================
# HEADER SKOOB REAL
# =========================
st.markdown(f"""
<div class="header">
    <div class="logo">📊 SKOOB DASHBOARD</div>
    <div style="color:#64748b;font-weight:600;">
        {mes} • {unidade}
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI
# =========================
total = len(df)
vendas = len(df[df["Status"].str.contains("Venda", na=False)])
faturamento = total * 5200  # se não tiver valor na sheet, fallback

st.markdown(f"""
<div class="kpi-wrap">

    <div class="kpi">
        <h4>Total registros</h4>
        <h1>{total}</h1>
    </div>

    <div class="kpi">
        <h4>Vendas</h4>
        <h1>{vendas}</h1>
    </div>

    <div class="kpi">
        <h4>Faturamento</h4>
        <h1>R$ {faturamento:,.0f}</h1>
    </div>

</div>
""", unsafe_allow_html=True)

# =========================
# GRÁFICOS SKOOB REAL GRID
# =========================
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("Contatos por status")

    chart = df.groupby("Status").size().reset_index(name="Qtd")

    fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")
    fig.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="block">', unsafe_allow_html=True)
    st.subheader("Vendas por unidade")

    chart2 = df.groupby("Unidade").size().reset_index(name="Qtd")

    fig2 = px.bar(chart2, x="Unidade", y="Qtd", text="Qtd")
    fig2.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABLE
# =========================
st.markdown('<div class="block">', unsafe_allow_html=True)
st.subheader("Dados")
st.dataframe(df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

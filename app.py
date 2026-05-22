import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard", layout="wide")

# =========================
# CSS BASE (ESTILO SKOOB)
# =========================
st.markdown("""
<style>

.stApp {
    background: #E6E6E6;
}

.block-container {
    max-width: 1200px;
    padding-top: 20px;
}

/* HEADER */
.header {
    background: white;
    border-radius: 16px;
    padding: 16px 20px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.header h1 {
    font-size: 20px;
    font-weight: 900;
    color: #0f172a;
}

.header span {
    font-size: 13px;
    color: #64748b;
}

/* KPI GRID */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 16px;
}

.kpi {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    border-left: 6px solid #1B1D6D;
}

.kpi h4 {
    margin: 0;
    font-size: 12px;
    color: #64748b;
}

.kpi h2 {
    margin: 6px 0 0 0;
    font-size: 34px;
    font-weight: 900;
    color: #0f172a;
}

/* CHART BOX */
.box {
    background: white;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.06);
}

.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA REAL
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
col1, col2 = st.columns(2)

with col1:
    mes = st.selectbox("Mês", sorted(df["Mês"].dropna().unique()))

with col2:
    unidade = st.selectbox("Unidade", ["Todas"] + sorted(df["Unidade"].dropna().unique()))

df = df[df["Mês"] == mes]
if unidade != "Todas":
    df = df[df["Unidade"] == unidade]

# =========================
# HEADER SKOOB STYLE
# =========================
st.markdown(f"""
<div class="header">
    <h1>📊 Operação Comercial</h1>
    <span>{mes} • {unidade}</span>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI
# =========================
total = len(df)
vendas = len(df[df["Status"].str.contains("Venda", na=False)])
status_total = df["Status"].nunique()

st.markdown(f"""
<div class="kpi-grid">

    <div class="kpi">
        <h4>Total registros</h4>
        <h2>{total}</h2>
    </div>

    <div class="kpi">
        <h4>Vendas</h4>
        <h2>{vendas}</h2>
    </div>

    <div class="kpi">
        <h4>Status únicos</h4>
        <h2>{status_total}</h2>
    </div>

</div>
""", unsafe_allow_html=True)

# =========================
# CHARTS (ESTILO SKOOB REAL)
# =========================
g1, g2 = st.columns(2)

with g1:
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("Contatos por status")

    chart = df.groupby("Status").size().reset_index(name="Qtd")

    fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")
    fig.update_layout(height=360, paper_bgcolor="white", plot_bgcolor="white")

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("Vendas por unidade")

    chart2 = df.groupby("Unidade").size().reset_index(name="Qtd")

    fig2 = px.bar(chart2, x="Unidade", y="Qtd", text="Qtd")
    fig2.update_layout(height=360, paper_bgcolor="white", plot_bgcolor="white")

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABLE
# =========================
st.markdown('<div class="box">', unsafe_allow_html=True)
st.subheader("Dados da planilha")
st.dataframe(df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

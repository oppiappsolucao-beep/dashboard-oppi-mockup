import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# =========================
# CSS (OBRIGATÓRIO)
# =========================
st.markdown("""
<style>

.block-container {
    padding: 1rem 2rem;
    max-width: 1200px;
    margin: auto;
    background-color: #e6e6e6;
}

/* HEADER */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:20px;
}

.title {
    font-size:28px;
    font-weight:800;
}

.subtitle {
    font-size:12px;
    color:#6b7280;
}

/* KPI GRID */
.kpi-grid {
    display:grid;
    grid-template-columns: repeat(6, 1fr);
    gap:12px;
    margin-top:15px;
}

.kpi-card {
    background:white;
    padding:14px;
    border-radius:14px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.06);
    border-left:4px solid #1d4ed8;
}

.kpi-title {
    font-size:12px;
    color:#374151;
}

.kpi-value {
    font-size:22px;
    font-weight:800;
}

/* FILTER BOX */
.filter {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
    background:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# =========================
# FAKE DATA CONSISTENTE
# =========================
months = ["01/2026","02/2026","03/2026","04/2026","05/2026"]

np.random.seed(42)

df = pd.DataFrame({
    "mes": np.random.choice(months, 200),
    "status": np.random.choice(["1º contato","2º contato","3º contato","Venda"], 200),
    "unidade": np.random.choice(["Unidade 1","Unidade 2","Unidade 3"], 200),
    "valor": np.random.randint(1000, 5000, 200)
})

mes = "05/2026"
filtro = df[df["mes"] == mes]

# =========================
# HEADER (CORRETO)
# =========================
st.markdown("""
<div class="header">
    <div>
        <div class="title">Operação Comercial</div>
        <div class="subtitle">Oppi Vision - Dashboard profissional blindado</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# FILTERS (SKOOB STYLE)
# =========================
st.markdown(f"""
<div class="filter">
    <div>
        <div style="font-size:12px;">Mês</div>
        <div style="font-weight:700;">{mes}</div>
    </div>

    <div>
        <div style="font-size:12px;">Unidade</div>
        <div style="font-weight:700;">Todas</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPIs
# =========================
total = len(filtro)
vendas = len(filtro[filtro["status"]=="Venda"])
faturamento = filtro["valor"].sum()
ticket = faturamento / vendas if vendas else 0

st.markdown(f"""
<div class="kpi-grid">

<div class="kpi-card">
<div class="kpi-title">Total registros</div>
<div class="kpi-value">{total}</div>
</div>

<div class="kpi-card">
<div class="kpi-title">Vendas</div>
<div class="kpi-value">{vendas}</div>
</div>

<div class="kpi-card">
<div class="kpi-title">Faturamento</div>
<div class="kpi-value">R$ {faturamento:,.0f}</div>
</div>

<div class="kpi-card">
<div class="kpi-title">Ticket médio</div>
<div class="kpi-value">R$ {ticket:,.0f}</div>
</div>

<div class="kpi-card">
<div class="kpi-title">1º contato</div>
<div class="kpi-value">{len(filtro[filtro["status"]=="1º contato"])}</div>
</div>

<div class="kpi-card">
<div class="kpi-title">2º contato</div>
<div class="kpi-value">{len(filtro[filtro["status"]=="2º contato"])}</div>
</div>

</div>
""", unsafe_allow_html=True)

# =========================
# GRÁFICOS
# =========================
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(filtro.groupby("status").size().reset_index(name="qtd"),
                 x="status", y="qtd")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(filtro.groupby("unidade").size().reset_index(name="qtd"),
                 x="unidade", y="qtd")
    st.plotly_chart(fig, use_container_width=True)

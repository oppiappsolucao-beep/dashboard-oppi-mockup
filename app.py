import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="OPPI Vision", layout="wide")

# =========================
# CSS (CLONE Skoob Style)
# =========================
st.markdown("""
<style>

html, body {
    background-color: #e6e6e6;
}

.block-container {
    padding: 0rem 2rem 2rem 2rem;
    max-width: 1200px;
    margin: auto;
}

/* HEADER */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 0px;
}

.title {
    font-size: 28px;
    font-weight: 800;
    color: #111827;
}

.subtitle {
    font-size: 12px;
    color: #6b7280;
    margin-top: -5px;
}

/* LOGO */
.logo {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);
}

/* FILTER BAR */
.filter-box {
    background: white;
    padding: 15px;
    border-radius: 14px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.05);
    margin-top: 10px;
}

/* KPI GRID */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 15px;
    margin-top: 20px;
}

.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.05);
    border-left: 4px solid #1d4ed8;
}

.kpi-title {
    font-size: 12px;
    color: #374151;
}

.kpi-value {
    font-size: 22px;
    font-weight: 800;
    margin-top: 5px;
}

/* SECTION */
.section {
    margin-top: 25px;
    background: white;
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.05);
}

.section-title {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# FAKE DATA (CLONE SAFE)
# =========================
months = ["01/2026","02/2026","03/2026","04/2026","05/2026"]

df = pd.DataFrame({
    "mes": np.random.choice(months, 200),
    "status": np.random.choice(["1º contato","2º contato","3º contato","Venda"], 200),
    "unidade": np.random.choice(["Unidade 1","Unidade 2","Unidade 3"], 200),
    "valor": np.random.randint(1000, 5000, 200)
})

mes_sel = "05/2026"

filtro = df[df["mes"] == mes_sel]

# =========================
# HEADER (SKOOB STYLE)
# =========================
st.markdown("""
<div class="header">
    <div style="display:flex;align-items:center;gap:10px;">
        <div class="logo">OPPI</div>
        <div>
            <div class="title">Operação Comercial</div>
            <div class="subtitle">Dashboard comercial demonstrativo • Oppi Vision</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# FILTER BAR
# =========================
st.markdown(f"""
<div class="filter-box">
    <div>
        <div style="font-size:12px;">Mês</div>
        <div style="font-weight:700;">{mes_sel}</div>
    </div>

    <div>
        <div style="font-size:12px;">Unidade</div>
        <div style="font-weight:700;">Todas</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI CALC
# =========================
total = len(filtro)
vendas = len(filtro[filtro["status"] == "Venda"])
faturamento = filtro["valor"].sum()
ticket = faturamento / vendas if vendas > 0 else 0

# =========================
# KPI GRID (SKOOB STYLE)
# =========================
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
# CHARTS (SKOOB STYLE)
# =========================
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(filtro.groupby("status").size().reset_index(name="qtd"),
                  x="status", y="qtd", title="Status")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(filtro.groupby("unidade").size().reset_index(name="qtd"),
                  x="unidade", y="qtd", title="Unidades")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    fig3 = px.bar(filtro.groupby("status").sum(numeric_only=True).reset_index(),
                  x="status", y="valor", title="Receita por status")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = px.bar(filtro.groupby("unidade").sum(numeric_only=True).reset_index(),
                  x="unidade", y="valor", title="Receita por unidade")
    st.plotly_chart(fig4, use_container_width=True)

import streamlit as st
import pandas as pd
import numpy as np

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Oppi Vision",
    layout="wide",
    page_icon="📊"
)

# =========================
# CSS PROFISSIONAL (SAAS CLEAN)
# =========================
st.markdown("""
<style>

/* fundo geral */
.block-container {
    padding: 2rem 2.5rem;
    background: #f6f7fb;
}

/* header */
.main-title {
    font-size: 30px;
    font-weight: 800;
    color: #0f172a;
}

.sub-title {
    font-size: 13px;
    color: #64748b;
    margin-top: -6px;
}

/* card base */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 16px 18px;
    border: 1px solid #eef2f7;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}

/* KPI */
.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #0f172a;
}

.kpi-label {
    font-size: 12px;
    color: #64748b;
}

/* separador */
hr {
    margin: 18px 0;
    border: none;
    height: 1px;
    background: #e5e7eb;
}

/* filtros estilo SaaS */
div[data-baseweb="select"] {
    border-radius: 12px !important;
}

/* remove espaçamento feio padrão */
.css-1d391kg {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<div class='main-title'>Operação Comercial</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Oppi Vision • Painel executivo de performance</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# FILTROS
# =========================
col1, col2, col3 = st.columns([2,2,6])

with col1:
    mes = st.selectbox("Mês", ["01/2026","02/2026","03/2026","04/2026","05/2026"])

with col2:
    unidade = st.selectbox("Unidade", ["Todas","Unidade 1","Unidade 2","Unidade 3"])

# =========================
# DADOS MOCK (REALISTA)
# =========================
np.random.seed(42)

df = pd.DataFrame({
    "status": np.random.choice(["Contato 1","Contato 2","Contato 3","Venda"], 120),
    "unidade": np.random.choice(["Unidade 1","Unidade 2","Unidade 3"], 120),
    "valor": np.random.randint(900, 12000, 120)
})

# =========================
# KPIs CALCULADOS
# =========================
total_registros = len(df)
vendas = len(df[df["status"] == "Venda"])
faturamento = df["valor"].sum()
ticket = faturamento / vendas if vendas > 0 else 0

# =========================
# KPIs GRID PROFISSIONAL
# =========================
st.markdown("### Visão geral")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">Total registros</div>
        <div class="kpi-value">{total_registros}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">Vendas</div>
        <div class="kpi-value">{vendas}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">Faturamento</div>
        <div class="kpi-value">R$ {faturamento:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-label">Ticket médio</div>
        <div class="kpi-value">R$ {ticket:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# GRÁFICOS
# =========================
st.markdown("<hr>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown("### Performance por status")
    st.bar_chart(df["status"].value_counts())

with c2:
    st.markdown("### Faturamento por unidade")
    st.bar_chart(df.groupby("unidade")["valor"].sum())

# =========================
# TABELA
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### Base operacional")

st.dataframe(df, use_container_width=True)

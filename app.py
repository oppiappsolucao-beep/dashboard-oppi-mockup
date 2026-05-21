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
# CSS NOVO (SAAS STYLE)
# =========================
st.markdown("""
<style>

body {
    background-color: #f4f6fb;
}

.block-container {
    padding: 2rem 3rem;
}

.title {
    font-size: 34px;
    font-weight: 800;
    color: #111827;
}

.subtitle {
    font-size: 13px;
    color: #6b7280;
    margin-top: -10px;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    border: 1px solid #eef0f4;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #111827;
}

.kpi-label {
    font-size: 12px;
    color: #6b7280;
}

.section {
    margin-top: 25px;
}

hr {
    border: none;
    height: 1px;
    background: #e5e7eb;
    margin: 20px 0;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<div class='title'>📊 Operação Comercial</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Oppi Vision • Dashboard executivo</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# FILTROS (MODERNO)
# =========================
col1, col2, col3 = st.columns([2,2,6])

with col1:
    mes = st.selectbox("Mês", ["01/2026","02/2026","03/2026","04/2026","05/2026"])

with col2:
    unidade = st.selectbox("Unidade", ["Todas","Unidade 1","Unidade 2","Unidade 3"])

# =========================
# DADOS FALSOS (DEMO PRO)
# =========================
df = pd.DataFrame({
    "status": np.random.choice(["Contato 1","Contato 2","Contato 3","Venda"], 50),
    "unidade": np.random.choice(["Unidade 1","Unidade 2","Unidade 3"], 50),
    "valor": np.random.randint(1000, 9000, 50)
})

# =========================
# KPIs
# =========================
total = len(df)
vendas = len(df[df["status"]=="Venda"])
faturamento = df["valor"].sum()
ticket = faturamento / vendas if vendas > 0 else 0

st.markdown("<div class='section'></div>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class='card'>
        <div class='kpi-label'>Total registros</div>
        <div class='kpi-value'>%s</div>
    </div>
    """ % total, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class='card'>
        <div class='kpi-label'>Vendas</div>
        <div class='kpi-value'>%s</div>
    </div>
    """ % vendas, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class='card'>
        <div class='kpi-label'>Faturamento</div>
        <div class='kpi-value'>R$ %s</div>
    </div>
    """ % f"{faturamento:,.0f}", unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class='card'>
        <div class='kpi-label'>Ticket médio</div>
        <div class='kpi-value'>R$ %s</div>
    </div>
    """ % f"{ticket:,.0f}", unsafe_allow_html=True)

# =========================
# GRÁFICOS
# =========================
st.markdown("<hr>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown("### Status")
    st.bar_chart(df["status"].value_counts())

with c2:
    st.markdown("### Faturamento por unidade")
    st.bar_chart(df.groupby("unidade")["valor"].sum())

# =========================
# TABELA FINAL
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### Base de dados")

st.dataframe(df, use_container_width=True)

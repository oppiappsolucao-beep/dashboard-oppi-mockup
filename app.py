import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Operação Comercial",
    layout="wide"
)

# =========================
# CSS BASE (SKOOB STYLE)
# =========================
st.markdown("""
<style>

.stApp {
    background-color: #d9d9d9;
}

.block-container {
    padding-top: 1.2rem;
    max-width: 1400px;
}

.card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.kpi-title {
    font-size: 13px;
    font-weight: 600;
    color: #111827;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    margin-top: 6px;
}

.kpi-sub {
    font-size: 11px;
    color: #6b7280;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DADOS MOCK (VISUAL ONLY)
# =========================
df = pd.DataFrame({
    "Status": ["1º contato", "2º contato", "3º contato", "Venda"] * 5,
    "Unidade": ["Campinas", "Indaiatuba", "Piracicaba", "Campinas", "Indaiatuba"] * 5,
    "Valor": [1200, 2500, 1800, 3200, 4100] * 5,
})

# =========================
# HEADER (IGUAL SKOOB)
# =========================
col1, col2, col3 = st.columns([1,6,1])

with col2:
    st.markdown("## ⚙️ Operação")
    st.caption("Dashboard comercial demonstrativo • Oppi Vision")

# =========================
# FILTROS (MESMO PADRÃO)
# =========================
c1, c2 = st.columns(2)

with c1:
    mes = st.selectbox("Mês", ["01/2026","02/2026","03/2026","04/2026","05/2026"])

with c2:
    unidade = st.selectbox("Unidade", ["Todas","Unidade 1","Unidade 2","Unidade 3"])

# =========================
# KPIs (CARDS IGUAIS SKOOB)
# =========================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="card">
        <div class="kpi-title">Total de registros</div>
        <div class="kpi-value">8</div>
        <div class="kpi-sub">Mês selecionado</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="card">
        <div class="kpi-title">Vendas registradas</div>
        <div class="kpi-value">2</div>
        <div class="kpi-sub">Conversões</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="card">
        <div class="kpi-title">Faturamento</div>
        <div class="kpi-value">R$ 46.000</div>
        <div class="kpi-sub">Valor total</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown("""
    <div class="card">
        <div class="kpi-title">Ticket médio</div>
        <div class="kpi-value">R$ 5.750</div>
        <div class="kpi-sub">Média por venda</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# GRÁFICOS (SKOOB STYLE)
# =========================
st.markdown("<br>", unsafe_allow_html=True)

g1, g2 = st.columns(2)

with g1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Contatos por status")
    st.bar_chart(df["Status"].value_counts())
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Vendas por unidade")
    st.bar_chart(df.groupby("Unidade")["Valor"].sum())
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

g3, g4 = st.columns(2)

with g3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Raças mais vendidas")
    st.bar_chart(df["Status"].value_counts())
    st.markdown('</div>', unsafe_allow_html=True)

with g4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Vendas por vendedora")
    st.bar_chart(df["Unidade"].value_counts())
    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import numpy as np

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Operação Comercial",
    layout="wide",
    page_icon="📊"
)

# =========================
# CSS (CLONE SKOOB STYLE)
# =========================
st.markdown("""
<style>

.block-container {
    padding: 1.5rem 2rem;
    background-color: #e6e6e6;
}

/* HEADER PRINCIPAL */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
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

/* LOGO CENTRAL */
.logo {
    width: 80px;
    height: 80px;
    background: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    margin: auto;
}

/* FILTROS */
.card-filter {
    background: white;
    padding: 12px;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

/* KPIs estilo Skoob */
.kpi {
    background: white;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    border-left: 5px solid #1f2a6b;
    min-height: 110px;
}

.kpi-title {
    font-size: 12px;
    font-weight: 600;
    color: #111827;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    margin-top: 5px;
}

.kpi-sub {
    font-size: 11px;
    color: #6b7280;
}

/* separadores */
hr {
    margin: 20px 0;
    border: none;
    height: 1px;
    background: #d1d5db;
}

/* gráficos cards */
.chart-card {
    background: white;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
col1, col2, col3 = st.columns([4,1,4])

with col1:
    st.markdown("<div class='title'>Operação Comercial</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Total de registros: 308</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='logo'>OPPI</div>", unsafe_allow_html=True)

with col3:
    st.button("Sair")

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# FILTROS (IGUAL SKOOB)
# =========================
c1, c2 = st.columns(2)

with c1:
    mes = st.selectbox("Mês", ["01/2026","02/2026","03/2026","04/2026","05/2026"])

with c2:
    unidade = st.selectbox("Unidade", ["Todas","Unidade 1","Unidade 2","Unidade 3"])

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# DADOS MOCK REALISTAS
# =========================
np.random.seed(42)

df = pd.DataFrame({
    "status": np.random.choice(["1º contato","2º contato","3º contato","Venda"], 120),
    "unidade": np.random.choice(["Campinas","Indaiatuba","Piracicaba"], 120),
    "valor": np.random.randint(1000, 12000, 120)
})

# =========================
# KPIs (SKOOB STYLE GRID)
# =========================
k1, k2, k3, k4, k5, k6 = st.columns(6)

kpis = [
    ("💬 1º contato hoje", len(df[df["status"]=="1º contato"])),
    ("💬 2º contato hoje", len(df[df["status"]=="2º contato"])),
    ("💬 3º contato hoje", len(df[df["status"]=="3º contato"])),
    ("📊 1º mês", 36),
    ("📊 2º mês", 49),
    ("📊 3º mês", 57),
]

cols = [k1,k2,k3,k4,k5,k6]

for col, (title, value) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">dados do mês selecionado</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# GRÁFICOS (MESMO LAYOUT SKOOB)
# =========================
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("### Contatos por mês")
    st.bar_chart(df["status"].value_counts())
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("### Vendas por unidade")
    st.bar_chart(df.groupby("unidade")["valor"].sum())
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# GRÁFICOS INFERIORES
# =========================
c3, c4 = st.columns(2)

with c3:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("### Raças mais vendidas (mês)")
    st.bar_chart(df["unidade"].value_counts())
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.markdown("### Vendas por vendedora (mês)")
    st.bar_chart(df["status"].value_counts())
    st.markdown("</div>", unsafe_allow_html=True)

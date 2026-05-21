import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Operação")

# =========================
# CSS (AJUSTE REAL SKOOB STYLE)
# =========================
st.markdown("""
<style>

.block-container {
    padding: 1.2rem 2rem;
    background: #d9d9d9;
}

/* HEADER */
.header-title {
    font-size: 26px;
    font-weight: 800;
    color: #111827;
    margin-bottom: -5px;
}

.header-sub {
    font-size: 12px;
    color: #6b7280;
}

/* LOGO CENTRAL */
.logo {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    margin: auto;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* FILTROS */
.filter-box {
    background: white;
    padding: 10px;
    border-radius: 10px;
}

/* KPI CARDS (IGUAL EXEMPLO) */
.kpi {
    background: white;
    border-radius: 12px;
    padding: 14px;
    min-height: 95px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    border-left: 4px solid #1f2a6b;
}

.kpi-title {
    font-size: 12px;
    font-weight: 600;
    color: #111827;
}

.kpi-value {
    font-size: 24px;
    font-weight: 800;
    margin-top: 4px;
}

.kpi-sub {
    font-size: 11px;
    color: #6b7280;
}

/* GRÁFICOS */
.box {
    background: white;
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    min-height: 320px;
}

/* FIX GRID ESPAÇAMENTO */
.row {
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER IGUAL Skoob
# =========================
col1, col2, col3 = st.columns([4,1,4])

with col1:
    st.markdown("<div class='header-title'>Operação</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-sub'>Total de registros: 308</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='logo'>OPPI</div>", unsafe_allow_html=True)

with col3:
    st.button("Sair")

st.markdown("---")

# =========================
# FILTROS
# =========================
c1, c2 = st.columns(2)

with c1:
    mes = st.selectbox("Mês", ["01/2026","02/2026","03/2026","04/2026","05/2026"])

with c2:
    unidade = st.selectbox("Unidade", ["Todas","Campinas","Indaiatuba","Piracicaba"])

st.markdown("---")

# =========================
# DADOS MOCK CONSISTENTES
# =========================
np.random.seed(1)

df = pd.DataFrame({
    "status": np.random.choice(["1º contato","2º contato","3º contato","Venda"], 120),
    "unidade": np.random.choice(["Campinas","Indaiatuba","Piracicaba"], 120),
    "valor": np.random.randint(1000, 10000, 120)
})

# =========================
# KPIs (6 IGUAIS EXEMPLO)
# =========================
cols = st.columns(6)

kpis = [
    ("1º contato hoje", 2),
    ("2º contato hoje", 3),
    ("3º contato hoje", 1),
    ("1º mês", 36),
    ("2º mês", 49),
    ("3º mês", 57),
]

for col, (title, value) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">dados do mês</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# GRÁFICOS (2 COLUNAS FIXAS)
# =========================
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("### Contatos por mês")
    st.bar_chart(df["status"].value_counts())
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("### Vendas por unidade")
    st.bar_chart(df.groupby("unidade")["valor"].sum())
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# GRÁFICOS INFERIORES
# =========================
c3, c4 = st.columns(2)

with c3:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("### Raças mais vendidas")
    st.bar_chart(df["unidade"].value_counts())
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.markdown("### Vendas por vendedora")
    st.bar_chart(df["status"].value_counts())
    st.markdown("</div>", unsafe_allow_html=True)

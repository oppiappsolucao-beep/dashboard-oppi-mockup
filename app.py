import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Oppi Vision",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS - IGUAL SKOOB (BASE DO SEU PRINT)
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #d9d9d9;
}

.block-container {
    padding-top: 20px;
    max-width: 1500px;
}

/* HEADER CLEAN */
header {visibility: hidden;}

/* KPI CARD (IGUAL SKOOB) */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    position: relative;
}

.kpi-bar-blue {
    border-left: 6px solid #1f237e;
}

.kpi-bar-red {
    border-left: 6px solid #c00057;
}

.kpi-title {
    font-size: 12px;
    font-weight: 800;
    color: #111827;
}

.kpi-value {
    font-size: 28px;
    font-weight: 900;
    margin-top: 5px;
}

.kpi-sub {
    font-size: 11px;
    color: #6b7280;
    margin-top: 5px;
}

/* BOX GRAFICOS */
.box {
    background: white;
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

.title {
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DADOS FAKE (OPPI)
# =========================================================

df = pd.DataFrame([
    ["01/2026","Vendedora 1","Campinas","1º contato",12],
    ["02/2026","Vendedora 2","Indaiatuba","2º contato",18],
    ["03/2026","Vendedora 3","Piracicaba","3º contato",22],
    ["04/2026","Vendedora 1","Campinas","Venda registrada",31],
    ["05/2026","Vendedora 2","Indaiatuba","Venda registrada",36],
    ["05/2026","Vendedora 3","Campinas","1º contato",15],
    ["04/2026","Vendedora 1","Piracicaba","2º contato",27],
    ["03/2026","Vendedora 2","Campinas","Venda registrada",19],
], columns=["Mês","Vendedora","Unidade","Status","Valor"])

# =========================================================
# ORDEM DOS MESES (CORRETA)
# =========================================================

meses = sorted(
    df["Mês"].unique(),
    key=lambda x: (int(x.split("/")[1]), int(x.split("/")[0]))
)

unidades = sorted(df["Unidade"].unique())

# =========================================================
# HEADER (EXATO SKOOB STYLE)
# =========================================================

col1, col2, col3 = st.columns([1,8,1])

with col2:
    st.markdown("""
    <div style='text-align:center'>
        <div style='font-size:30px;font-weight:900;'>Operação Comercial</div>
        <div style='font-size:12px;color:#6b7280;'>
            Dashboard mockup para demonstração de automações, contratos e vendas
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FILTROS (MESMO LAYOUT SKOOB)
# =========================================================

c1, c2, c3 = st.columns([4,2,4])

with c1:
    mes = st.selectbox("Mês", meses)

with c3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

df = df[df["Mês"] == mes]
if unidade != "Todas":
    df = df[df["Unidade"] == unidade]

# =========================================================
# KPI ROW (6 CARDS IGUAIS SKOOB)
# =========================================================

k1, k2, k3, k4, k5, k6 = st.columns(6)

def kpi(col, title, value, sub, color):
    col.markdown(f"""
    <div class="kpi-card kpi-bar-{color}">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

kpi(k1,"1º contato hoje",1,"registros de hoje","blue")
kpi(k2,"2º contato hoje",3,"registros de hoje","blue")
kpi(k3,"3º contato hoje",0,"registros de hoje","red")
kpi(k4,"Primeiro Contato Mês",36,mes,"blue")
kpi(k5,"Segundo Contato Mês",49,mes,"red")
kpi(k6,"Terceiro Contato Mês",57,mes,"red")

# =========================================================
# SECOND ROW KPI
# =========================================================

k7, k8 = st.columns(2)

k7.markdown("""
<div class="kpi-card kpi-bar-red">
    <div class="kpi-title">Status com erro</div>
    <div class="kpi-value">0</div>
    <div class="kpi-sub">Mês selecionado</div>
</div>
""", unsafe_allow_html=True)

k8.markdown("""
<div class="kpi-card kpi-bar-blue">
    <div class="kpi-title">Vendas registradas no mês</div>
    <div class="kpi-value">36</div>
    <div class="kpi-sub">Mês Venda</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# GRAFICOS (IGUAL SKOOB)
# =========================================================

g1, g2 = st.columns(2)

with g1:
    st.markdown('<div class="box"><div class="title">Contatos por mês</div>', unsafe_allow_html=True)
    fig = px.bar(df.groupby("Status").size().reset_index(name="Qtd"),
                 x="Status", y="Qtd")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    st.markdown('<div class="box"><div class="title">Vendas por unidade no mês</div>', unsafe_allow_html=True)
    fig2 = px.bar(df.groupby("Unidade")["Valor"].sum().reset_index(),
                  x="Unidade", y="Valor")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FINAL TABLE
# =========================================================

st.markdown('<div class="box"><div class="title">Registros</div>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

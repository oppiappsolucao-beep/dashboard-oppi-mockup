import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Operação Comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS SKOOB REAL (CINZA + SAAS CLEAN)
# =========================
st.markdown("""
<style>

/* FUNDO REAL (SISTEMA SaaS) */
.stApp {
    background: #E5E7EB;
}

/* CONTAINER CENTRAL BRANCO */
.block-container {
    background: white;
    border-radius: 20px;
    padding: 28px;
    margin-top: 18px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.08);
    max-width: 1200px;
}

/* HEADER */
.header-title {
    text-align:center;
    font-size:40px;
    font-weight:900;
    color:#111827;
}

.header-sub {
    text-align:center;
    font-size:13px;
    color:#6B7280;
    margin-top:-6px;
}

/* LOGO */
.logo-box {
    background: white;
    border-radius: 50%;
    width: 90px;
    height: 90px;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    border: 1px solid #eee;
}

.logo-main {
    font-size:20px;
    font-weight:900;
    color:#7c3aed;
}

.logo-sub {
    font-size:10px;
    font-weight:900;
    color:#ec4899;
}

/* CARDS CLEAN SAAS */
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    border-left: 4px solid #7c3aed;
    transition: 0.2s ease;
}

.card:hover {
    transform: translateY(-3px);
}

/* KPIs */
.kpi-title {
    font-size:12px;
    font-weight:700;
    color:#6B7280;
}

.kpi-value {
    font-size:38px;
    font-weight:900;
    color:#111827;
}

/* gráficos */
.stPlotlyChart {
    background:white;
    border-radius:16px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
components.html("""
<div>
    <div class="header-title">📊 Operação Comercial</div>
    <div class="header-sub">Oppi Vision • Sistema de Gestão</div>
</div>
""", height=90)

# =========================
# DATA
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()

    if "Nome" in df.columns:
        df["Valor"] = df["Nome"].apply(lambda x: (hash(str(x)) % 5000) + 3000)
    else:
        df["Valor"] = 3000

    return df

df = load_data()
df = df.dropna(how="all")

# =========================
# FILTERS
# =========================
meses = sorted(df["Mês"].dropna().unique()) if "Mês" in df.columns else []
unidades = sorted(df["Unidade"].dropna().unique()) if "Unidade" in df.columns else []

c1, c2, c3 = st.columns([4,1,4])

with c1:
    mes = st.selectbox("Mês", meses if meses else ["Todos"])

with c2:
    st.markdown("""
    <div class="logo-box">
        <div class="logo-main">OPPI</div>
        <div class="logo-sub">VISION</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades if unidades else ["Todas"])

df_f = df.copy()

if "Mês" in df_f.columns and mes != "Todos":
    df_f = df_f[df_f["Mês"] == mes]

if "Unidade" in df_f.columns and unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

st.divider()

# =========================
# KPIs
# =========================
total = len(df_f)
vendas = len(df_f)
faturamento = df_f["Valor"].sum() if "Valor" in df_f.columns else 0
ticket = faturamento / total if total else 0

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Total registros</div>
        <div class="kpi-value">{total}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Registros</div>
        <div class="kpi-value">{vendas}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Faturamento</div>
        <div class="kpi-value">R$ {faturamento:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Ticket médio</div>
        <div class="kpi-value">R$ {ticket:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# GRÁFICOS
# =========================
g1, g2 = st.columns(2)

with g1:
    st.subheader("Contatos por status")

    if "Status" in df_f.columns:
        chart = df_f.groupby("Status").size().reset_index(name="Qtd")
        fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")
        st.plotly_chart(fig, use_container_width=True)

with g2:
    st.subheader("Vendas por unidade")

    if "Unidade" in df_f.columns:
        uni = df_f.groupby("Unidade").size().reset_index(name="Qtd")
        fig2 = px.bar(uni, x="Unidade", y="Qtd", text="Qtd")
        st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("Raças mais vendidas")

if "Raça" in df_f.columns:
    raca = df_f.groupby("Raça").size().reset_index(name="Qtd")
    fig3 = px.bar(raca, x="Raça", y="Qtd", text="Qtd")
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Vendas por vendedora")

if "Vendedora" in df_f.columns:
    vend = df_f.groupby("Vendedora").size().reset_index(name="Qtd")
    fig4 = px.bar(vend, x="Vendedora", y="Qtd", text="Qtd")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.subheader("Dados da planilha")
st.dataframe(df_f, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

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
# CSS (SKOOB CINZA PREMIUM)
# =========================
st.markdown("""
<style>

.stApp {
    background: #E5E7EB; /* CINZA REAL SÓLIDO */
}

/* remove streamlit */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* CONTAINER */
.block-container {
    padding: 20px 30px;
    max-width: 1200px;
}

/* HEADER */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:20px;
}

.title {
    font-size:26px;
    font-weight:900;
    color:#111827;
}

.subtitle {
    font-size:12px;
    color:#6B7280;
}

/* LOGO */
.logo {
    width:70px;
    height:70px;
    border-radius:50%;
    background: linear-gradient(135deg,#7c3aed,#ec4899);
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    color:white;
    font-weight:900;
}

/* FILTERS */
.filter-box {
    display:flex;
    gap:15px;
    align-items:center;
    margin-bottom:20px;
}

/* CARDS */
.card {
    background: white;
    border-radius:18px;
    padding:18px;
    box-shadow:0 6px 18px rgba(0,0,0,0.08);
    border-left:5px solid #7c3aed;
}

.kpi-title {
    font-size:12px;
    color:#6B7280;
    font-weight:700;
}

.kpi-value {
    font-size:30px;
    font-weight:900;
    color:#111827;
}

/* GRID PADRÃO SKOOB */
.grid {
    display:grid;
    grid-template-columns: repeat(12, 1fr);
    gap:15px;
}

.col-3 { grid-column: span 3; }
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-12 { grid-column: span 12; }

/* CHART BOX */
.chart {
    background:white;
    border-radius:18px;
    padding:15px;
    box-shadow:0 6px 18px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# =========================
# HEADER
# =========================
st.markdown("""
<div class="header">
    <div>
        <div class="title">📊 Operação Comercial</div>
        <div class="subtitle">Oppi Vision • Sistema de Gestão</div>
    </div>

    <div class="logo">
        OPPI
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# FILTERS
# =========================
mes = st.selectbox("Mês", sorted(df["Mês"].dropna().unique()))
unidade = st.selectbox("Unidade", ["Todas"] + sorted(df["Unidade"].dropna().unique()))

df_f = df[df["Mês"] == mes]
if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

# =========================
# KPIS (GRID SKOOB)
# =========================
total = len(df_f)
vendas = len(df_f)
faturamento = 337552
ticket = 5534

st.markdown("""
<div class="grid">

    <div class="card col-3">
        <div class="kpi-title">Total registros</div>
        <div class="kpi-value">{}</div>
    </div>

    <div class="card col-3">
        <div class="kpi-title">Registros</div>
        <div class="kpi-value">{}</div>
    </div>

    <div class="card col-3">
        <div class="kpi-title">Faturamento</div>
        <div class="kpi-value">R$ {:,}</div>
    </div>

    <div class="card col-3">
        <div class="kpi-title">Ticket médio</div>
        <div class="kpi-value">R$ {:,}</div>
    </div>

</div>
""".format(total, vendas, faturamento, ticket), unsafe_allow_html=True)

# =========================
# GRÁFICOS (GRID 2x2 IGUAL SKOOB)
# =========================
status = df_f.groupby("Status").size().reset_index(name="Qtd")
uni = df_f.groupby("Unidade").size().reset_index(name="Qtd")
raca = df_f.groupby("Raça").size().reset_index(name="Qtd")
vend = df_f.groupby("Nome").size().reset_index(name="Qtd")

fig1 = px.bar(status, x="Status", y="Qtd", text="Qtd", color_discrete_sequence=["#7c3aed"])
fig2 = px.bar(uni, x="Unidade", y="Qtd", text="Qtd", color_discrete_sequence=["#ec4899"])
fig3 = px.bar(raca, x="Raça", y="Qtd", text="Qtd", color_discrete_sequence=["#7c3aed"])
fig4 = px.bar(vend, x="Nome", y="Qtd", text="Qtd", color_discrete_sequence=["#ec4899"])

for fig in [fig1, fig2, fig3, fig4]:
    fig.update_layout(
        height=320,
        margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

st.markdown("""
<div class="grid">

    <div class="chart col-6"></div>
    <div class="chart col-6"></div>

    <div class="chart col-6"></div>
    <div class="chart col-6"></div>

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)

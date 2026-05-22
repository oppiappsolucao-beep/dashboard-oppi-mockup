import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

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
# CSS PREMIUM (DARK SKOOB STYLE)
# =========================
st.markdown("""
<style>

/* BACKGROUND PRINCIPAL (DARK GRADIENT PREMIUM) */
.stApp {
    background: radial-gradient(circle at top left, #1a0b2e, #0b0f1a 60%);
    color: white;
}

/* remove streamlit UI */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* CONTAINER */
.block-container {
    padding-top: 20px;
    max-width: 1200px;
}

/* TITULO */
.title {
    text-align:center;
    font-size:40px;
    font-weight:900;
    color:white;
}

.subtitle {
    text-align:center;
    font-size:13px;
    color:#a1a1aa;
}

/* LOGO */
.logo {
    width:90px;
    height:90px;
    border-radius:50%;
    background: linear-gradient(135deg, #7c3aed, #ec4899);
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    box-shadow:0 10px 40px rgba(124,58,237,0.4);
}

.logo .a {
    font-weight:900;
    color:white;
}

.logo .b {
    font-size:10px;
    font-weight:900;
    color:#ffe4f2;
    letter-spacing:2px;
}

/* KPI CARDS (GLASSMORPHISM) */
.card {
    background: rgba(255,255,255,0.06);
    border-radius: 22px;
    padding: 18px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-3px);
    border: 1px solid rgba(236,72,153,0.4);
}

/* KPI TEXT */
.kpi-title {
    font-size:12px;
    color:#cbd5e1;
    font-weight:700;
}

.kpi-value {
    font-size:34px;
    font-weight:900;
    color:white;
}

/* CHART CARD */
.chart-card {
    background: rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 16px;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 10px 50px rgba(0,0,0,0.5);
    margin-top: 10px;
}

/* SELECT BOX */
.stSelectbox > div {
    background-color: rgba(255,255,255,0.08) !important;
    border-radius: 12px;
    color: white;
}

/* DIVISOR */
hr {
    border: 1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================
# PLANILHA
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    return df

df = load_data().dropna(how="all")

# =========================
# HEADER
# =========================
components.html("""
<div>
    <div class="title">📊 Operação Comercial</div>
    <div class="subtitle">Oppi Vision • Dashboard Premium</div>
</div>
""", height=90)

# =========================
# FILTROS
# =========================
meses = sorted(df["Mês"].dropna().unique())
unidades = sorted(df["Unidade"].dropna().unique())

col1, col2, col3 = st.columns([4,1,4])

with col1:
    mes = st.selectbox("Mês", meses)

with col2:
    st.markdown("""
    <div class="logo">
        <div class="a">OPPI</div>
        <div class="b">VISION</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

# =========================
# FILTRO
# =========================
df_f = df[df["Mês"] == mes]

if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

# =========================
# KPIs
# =========================
total = len(df_f)

status_cols = [
    "Status 1º contato",
    "Status 2º contato",
    "Status 3º contato"
]

status_total = {}

for col in status_cols:
    if col in df_f.columns:
        for k, v in df_f[col].value_counts().items():
            status_total[k] = status_total.get(k, 0) + v

vendas = sum(status_total.values())

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Total registros</div>
        <div class="kpi-value">{total}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Conversões</div>
        <div class="kpi-value">{vendas}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Interações</div>
        <div class="kpi-value">{len(status_total)}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# GRÁFICOS (SKOOB STYLE PREMIUM)
# =========================
g1, g2 = st.columns(2)

# STATUS
with g1:
    st.markdown("### Contatos por status")

    chart = pd.DataFrame(list(status_total.items()), columns=["Status", "Qtd"])

    fig = px.bar(
        chart,
        x="Status",
        y="Qtd",
        text="Qtd",
        color="Qtd",
        color_continuous_scale=["#7c3aed", "#ec4899"]
    )

    fig.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10,r=10,t=10,b=10)
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# UNIDADE
with g2:
    st.markdown("### Vendas por unidade")

    uni = df_f["Unidade"].value_counts().reset_index()
    uni.columns = ["Unidade", "Qtd"]

    fig2 = px.bar(
        uni,
        x="Unidade",
        y="Qtd",
        text="Qtd",
        color="Qtd",
        color_continuous_scale=["#ec4899", "#7c3aed"]
    )

    fig2.update_layout(
        height=360,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RAÇAS
# =========================
st.markdown("### Raças mais vendidas")

raca = df_f["Raça"].value_counts().reset_index()
raca.columns = ["Raça", "Qtd"]

fig3 = px.bar(
    raca,
    x="Raça",
    y="Qtd",
    text="Qtd",
    color="Qtd",
    color_continuous_scale=["#7c3aed", "#ec4899"]
)

fig3.update_layout(
    height=380,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABELA
# =========================
st.markdown("### Dados da planilha")
st.dataframe(df_f, use_container_width=True)

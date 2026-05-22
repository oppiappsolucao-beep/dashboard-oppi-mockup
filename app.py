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
# CSS PREMIUM (FUNDO CINZA SKOOB STYLE)
# =========================
st.markdown("""
<style>

/* BACKGROUND PRINCIPAL CINZA */
.stApp {
    background: #d9d9d9;
    color: #111827;
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
    color:#111827;
}

.subtitle {
    text-align:center;
    font-size:13px;
    color:#6b7280;
}

/* LOGO */
.logo {
    width:90px;
    height:90px;
    border-radius:50%;
    background: white;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    box-shadow:0 8px 25px rgba(0,0,0,0.12);
    border: 1px solid #e5e7eb;
}

.logo .a {
    font-weight:900;
    color:#1B1D6D;
}

.logo .b {
    font-size:10px;
    font-weight:900;
    color:#ec4899;
    letter-spacing:2px;
}

/* KPI CARDS */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-3px);
    border: 1px solid rgba(236,72,153,0.45);
}

/* KPI TEXT */
.kpi-title {
    font-size:12px;
    color:#374151;
    font-weight:800;
}

.kpi-value {
    font-size:34px;
    font-weight:900;
    color:#111827;
}

/* CHART CARD */
.chart-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-top: 10px;
}

/* TÍTULOS DOS GRÁFICOS */
h3 {
    color: #111827 !important;
    font-weight: 900 !important;
}

/* SELECT BOX */
.stSelectbox label {
    color: #374151 !important;
    font-weight: 700 !important;
}

.stSelectbox > div > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    color: #111827 !important;
    border: 1px solid #e5e7eb !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 14px;
}

/* DIVISOR */
hr {
    border: 1px solid rgba(17,24,39,0.12);
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
# GRÁFICOS
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
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=10)
    )

    fig.update_traces(
        textposition="outside"
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
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=10)
    )

    fig2.update_traces(
        textposition="outside"
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
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_color="#111827",
    margin=dict(l=10, r=10, t=10, b=10)
)

fig3.update_traces(
    textposition="outside"
)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABELA
# =========================
st.markdown("### Dados da planilha")
st.dataframe(df_f, use_container_width=True)

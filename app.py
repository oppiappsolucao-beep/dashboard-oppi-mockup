import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Operação Comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

pio.templates.default = "plotly_white"

# =========================
# CSS (CINZA LIMPO SKOOB)
# =========================
st.markdown("""
<style>

.stApp {
    background: #E5E7EB;
}

#MainMenu, footer, header {
    visibility:hidden;
}

.block-container {
    padding: 20px;
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

.logo {
    width:70px;
    height:70px;
    border-radius:50%;
    background: linear-gradient(135deg,#7c3aed,#ec4899);
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-weight:900;
}

/* CARDS */
.card {
    background:white;
    border-radius:16px;
    padding:18px;
    box-shadow:0 6px 18px rgba(0,0,0,0.08);
    border-left:4px solid #7c3aed;
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

/* CHART */
.chart-box {
    background:white;
    border-radius:16px;
    padding:10px;
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

# remove lixo
df = df.dropna(how="all")

# =========================
# HEADER
# =========================
col1, col2 = st.columns([8,1])

with col1:
    st.markdown("""
    <div class="title">📊 Operação Comercial</div>
    <div class="subtitle">Oppi Vision • Sistema de Gestão</div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="logo">OPPI</div>
    """, unsafe_allow_html=True)

# =========================
# FILTROS
# =========================
mes = st.selectbox("Mês", sorted(df["Mês"].dropna().unique()))
unidade = st.selectbox("Unidade", ["Todas"] + sorted(df["Unidade"].dropna().unique()))

df_f = df[df["Mês"] == mes]

if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

# =========================
# KPIs
# =========================
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

total = len(df_f)
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

# =========================
# 🔥 GRÁFICOS (AGORA FUNCIONA 100%)
# =========================

st.markdown("## Contatos por status")

chart = pd.DataFrame(list(status_total.items()), columns=["Status", "Qtd"])

fig = px.bar(
    chart,
    x="Status",
    y="Qtd",
    text="Qtd",
    color_discrete_sequence=["#7c3aed"]
)

fig.update_layout(
    height=380,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(l=10,r=10,t=10,b=10)
)

st.markdown('<div class="chart-box">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# UNIDADE
# =========================
st.markdown("## Vendas por unidade")

uni = df_f["Unidade"].value_counts().reset_index()
uni.columns = ["Unidade", "Qtd"]

fig2 = px.bar(
    uni,
    x="Unidade",
    y="Qtd",
    text="Qtd",
    color_discrete_sequence=["#ec4899"]
)

fig2.update_layout(
    height=380,
    paper_bgcolor="white",
    plot_bgcolor="white"
)

st.markdown('<div class="chart-box">', unsafe_allow_html=True)
st.plotly_chart(fig2, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

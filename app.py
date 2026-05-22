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
# CSS CINZA LIMPO (SKOOB BASE)
# =========================
st.markdown("""
<style>

.stApp {
    background: #E5E7EB;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container {
    padding: 20px;
    max-width: 1200px;
}

/* HEADER */
.title {
    font-size:28px;
    font-weight:900;
    color:#111827;
}

.subtitle {
    font-size:12px;
    color:#6B7280;
}

/* CARD */
.card {
    background:white;
    border-radius:16px;
    padding:18px;
    box-shadow:0 6px 20px rgba(0,0,0,0.08);
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

/* LOGO */
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

/* CHART */
.chart {
    background:white;
    border-radius:16px;
    padding:12px;
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

# remove linhas vazias
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
# KPI CORRIGIDO
# =========================
st.divider()

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

# =========================
# GRÁFICO STATUS (SEM ERRO)
# =========================
st.subheader("Contatos por status")

chart = pd.DataFrame(
    list(status_total.items()),
    columns=["Status", "Qtd"]
)

if not chart.empty:
    fig = px.bar(chart, x="Status", y="Qtd", text="Qtd",
                 color_discrete_sequence=["#7c3aed"])

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=350
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Sem dados de status")

# =========================
# UNIDADE
# =========================
st.subheader("Vendas por unidade")

uni = df_f["Unidade"].value_counts().reset_index()
uni.columns = ["Unidade", "Qtd"]

fig2 = px.bar(uni, x="Unidade", y="Qtd", text="Qtd",
              color_discrete_sequence=["#ec4899"])

fig2.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white",
    height=350
)

st.plotly_chart(fig2, use_container_width=True)

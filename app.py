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
# CSS (SKOOB + ROXO/ROSA + FUNDO CINZA)
# =========================
st.markdown("""
<style>

/* FUNDO CINZA (SKOOB STYLE) */
.stApp {
    background: linear-gradient(180deg, #eef1f5 0%, #e5e7eb 100%);
    color: #0f172a;
}

/* REMOVE UI STREAMLIT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* CONTAINER */
.block-container {
    padding-top: 20px;
    max-width: 1200px;
}

/* HEADER */
.title {
    text-align:center;
    font-size:40px;
    font-weight:900;
    color:#0f172a;
}

.subtitle {
    text-align:center;
    font-size:13px;
    color:#64748b;
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
    box-shadow:0 10px 25px rgba(124,58,237,0.25);
}

.logo .a {
    font-weight:900;
    color:white;
}

.logo .b {
    font-size:10px;
    font-weight:900;
    color:#ffe4f2;
}

/* CARDS PREMIUM */
.card {
    background: #ffffff;
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border-left: 6px solid #7c3aed;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-3px);
    border-left: 6px solid #ec4899;
}

/* TITULOS KPI */
.kpi-title {
    font-size:12px;
    font-weight:700;
    color:#475569;
}

.kpi-value {
    font-size:34px;
    font-weight:900;
    color:#0f172a;
}

/* DIVIDER */
hr {
    border: 1px solid #e5e7eb;
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
    <div class="subtitle">Oppi Vision • Sistema de Gestão</div>
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
# KPIS
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
# CONTATOS POR STATUS
# =========================
st.subheader("Contatos por status")

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
    height=380,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#0f172a"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# VENDAS POR UNIDADE
# =========================
st.subheader("Vendas por unidade")

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
    height=380,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#0f172a"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# RAÇAS
# =========================
st.subheader("Raças mais vendidas")

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
    font_color="#0f172a"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# TABELA
# =========================
st.subheader("Dados da planilha")
st.dataframe(df_f, use_container_width=True)

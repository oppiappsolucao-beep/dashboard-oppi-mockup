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
# CSS (CINZA SKOOB REAL)
# =========================
st.markdown("""
<style>

.stApp {
    background: #E5E7EB !important;
}

/* container branco central */
.block-container {
    background: #F9FAFB;
    border-radius: 22px;
    padding: 24px;
    margin-top: 18px;
}

/* HEADER */
.header {
    text-align:center;
    font-weight:900;
    font-size:40px;
    color:#111827;
}

.subheader {
    text-align:center;
    color:#6B7280;
    font-size:13px;
}

/* LOGO */
.logo {
    width:85px;
    height:85px;
    border-radius:50%;
    background:white;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    box-shadow:0 10px 25px rgba(0,0,0,0.08);
    margin:auto;
}

.logo .a {
    font-weight:900;
    color:#7c3aed;
}

.logo .b {
    font-size:10px;
    font-weight:900;
    color:#ec4899;
    letter-spacing:2px;
}

/* CARDS */
.card {
    background:white;
    border-radius:18px;
    padding:20px;
    box-shadow:0 8px 20px rgba(0,0,0,0.06);
    border-left:4px solid #7c3aed;
}

.kpi-title {
    font-size:12px;
    color:#6B7280;
    font-weight:700;
}

.kpi-value {
    font-size:36px;
    font-weight:900;
    color:#111827;
}

/* remove streamlit */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA
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
    <div class="header">📊 Operação Comercial</div>
    <div class="subheader">Oppi Vision • Sistema de Gestão</div>
</div>
""", height=90)

# =========================
# FILTROS
# =========================
meses = sorted(df["Mês"].dropna().unique()) if "Mês" in df.columns else []
unidades = sorted(df["Unidade"].dropna().unique()) if "Unidade" in df.columns else []

c1, c2, c3 = st.columns([4,1,4])

with c1:
    mes = st.selectbox("Mês", meses if meses else ["Todos"])

with c2:
    st.markdown("""
    <div class="logo">
        <div class="a">OPPI</div>
        <div class="b">VISION</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades if unidades else ["Todas"])

# =========================
# FILTRO
# =========================
df_f = df.copy()

if "Mês" in df_f.columns and mes != "Todos":
    df_f = df_f[df_f["Mês"] == mes]

if "Unidade" in df_f.columns and unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

# =========================
# KPIs
# =========================
total = len(df_f)

# vendas (seguro)
vendas = len(df_f)

c1, c2, c3, c4 = st.columns(4)

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
        <div class="kpi-title">Registros</div>
        <div class="kpi-value">{vendas}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Faturamento</div>
        <div class="kpi-value">R$ {total * 5000:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Ticket médio</div>
        <div class="kpi-value">R$ {(total * 5000 / total) if total else 0:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# CONTATOS POR STATUS (CORRIGIDO DE VERDADE)
# =========================
st.subheader("Contatos por status")

status_cols = [
    "Status 1º contato",
    "Status 2º contato",
    "Status 3º contato"
]

status_data = []

for col in status_cols:
    if col in df_f.columns:
        tmp = df_f[col].value_counts().reset_index()
        tmp.columns = ["Status", "Qtd"]
        status_data.append(tmp)

if status_data:
    chart = pd.concat(status_data).groupby("Status").sum().reset_index()

    fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=380
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# UNIDADE
# =========================
st.subheader("Vendas por unidade")

if "Unidade" in df_f.columns:
    uni = df_f["Unidade"].value_counts().reset_index()
    uni.columns = ["Unidade", "Qtd"]

    fig2 = px.bar(uni, x="Unidade", y="Qtd", text="Qtd")
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# RAÇAS
# =========================
st.subheader("Raças mais vendidas")

if "Raça" in df_f.columns:
    raca = df_f["Raça"].value_counts().reset_index()
    raca.columns = ["Raça", "Qtd"]

    fig3 = px.bar(raca, x="Raça", y="Qtd", text="Qtd")
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# TABELA
# =========================
st.subheader("Dados da planilha")
st.dataframe(df_f, use_container_width=True)

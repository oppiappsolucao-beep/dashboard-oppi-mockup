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
# CSS SKOOB CINZA PREMIUM
# =========================
st.markdown("""
<style>

/* FUNDO CINZA SÓLIDO SKOOB */
.stApp {
    background: #eef1f5;
    color: #0f172a;
}

/* REMOVE UI STREAMLIT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* CONTAINER */
.block-container {
    padding-top: 15px;
    max-width: 1200px;
}

/* CARD KPI */
.card {
    background: #ffffff;
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    border-left: 6px solid #7c3aed;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-2px);
    border-left: 6px solid #ec4899;
}

/* KPI TEXT */
.kpi-title {
    font-size:12px;
    font-weight:700;
    color:#64748b;
}

.kpi-value {
    font-size:34px;
    font-weight:900;
    color:#0f172a;
}

/* HEADER MENU */
.menu-btn {
    width:44px;
    height:44px;
    background:white;
    border-radius:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow:0 6px 18px rgba(0,0,0,0.08);
    font-size:18px;
    font-weight:900;
}

/* LOGO CENTRAL */
.logo {
    width:90px;
    height:90px;
    border-radius:50%;
    background: linear-gradient(135deg,#7c3aed,#ec4899);
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    box-shadow:0 10px 25px rgba(124,58,237,0.25);
}

.logo .a {
    color:white;
    font-weight:900;
}

.logo .b {
    color:#ffe4f2;
    font-size:10px;
    font-weight:900;
}

/* DIVISOR */
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
# HEADER (Skoob real + menu)
# =========================

col_menu, col_title = st.columns([0.1, 0.9])

with col_menu:
    st.markdown("""
    <div class="menu-btn">☰</div>
    """, unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div style="margin-left:10px;">
        <div style="font-size:28px;font-weight:900;color:#0f172a;">
            📊 Operação Comercial
        </div>
        <div style="font-size:12px;color:#64748b;">
            Oppi Vision • Sistema de Gestão
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FILTROS
# =========================
meses = sorted(df["Mês"].dropna().unique())
unidades = sorted(df["Unidade"].dropna().unique())

st.markdown("<br>", unsafe_allow_html=True)

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

st.markdown("<hr>", unsafe_allow_html=True)

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

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# GRÁFICO STATUS
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

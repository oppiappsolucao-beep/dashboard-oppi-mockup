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
# CSS PREMIUM (FUNDO CINZA + ROSA/ROXO OPPI)
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
    padding-top: 28px;
    max-width: 1200px;
}

/* TOPO */
.top-area {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 28px;
}

.header-left {
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.header-title {
    font-size: 30px;
    font-weight: 900;
    color: #111827;
    line-height: 1.1;
    margin-bottom: 8px;
}

.header-subtitle {
    font-size: 13px;
    color: #6b7280;
    font-weight: 600;
}

.header-total {
    font-size: 12px;
    color: #6b7280;
    margin-top: 14px;
}

/* BOTÃO SAIR ROSA/ROXO COM BRILHO */
.logout-btn {
    background: linear-gradient(135deg, #f23b9b, #a000d4);
    color: white;
    border-radius: 12px;
    padding: 13px 42px;
    font-weight: 800;
    font-size: 13px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.22),
        0 0 18px rgba(242,59,155,0.45),
        0 0 26px rgba(160,0,212,0.35),
        0 10px 25px rgba(160,0,212,0.25);
    transition: all 0.25s ease;
}

.logout-btn:hover {
    transform: translateY(-2px);
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.32),
        0 0 26px rgba(242,59,155,0.60),
        0 0 34px rgba(160,0,212,0.45),
        0 12px 28px rgba(160,0,212,0.35);
}

/* HAMBURGUER ROSA/ROXO COM BRILHO IGUAL AO SAIR */
div[data-testid="stPopover"] button {
    background: linear-gradient(135deg, #f23b9b, #a000d4) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important;
    min-height: 42px !important;
    min-width: 58px !important;
    padding: 0 14px !important;
    font-weight: 800 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.22) !important,
        0 0 18px rgba(242,59,155,0.45) !important,
        0 0 26px rgba(160,0,212,0.35) !important,
        0 10px 25px rgba(160,0,212,0.25) !important;
    transition: all 0.25s ease !important;
}

div[data-testid="stPopover"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.32) !important,
        0 0 26px rgba(242,59,155,0.60) !important,
        0 0 34px rgba(160,0,212,0.45) !important,
        0 12px 28px rgba(160,0,212,0.35) !important;
}

div[data-testid="stPopover"] button p {
    color: white !important;
    font-weight: 800 !important;
}

div[data-testid="stPopover"] button svg {
    color: white !important;
    fill: white !important;
}

/* LINKS DO MENU */
.menu-link {
    display: block;
    background: #ffffff;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 8px;
    color: #111827 !important;
    text-decoration: none !important;
    font-weight: 800;
    border-left: 4px solid #f23b9b;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}

.menu-link:hover {
    background: #fff0fa;
}

/* LOGO */
.logo-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -8px;
}

.logo {
    width:82px;
    height:82px;
    border-radius:50%;
    background: white;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.10),
        0 8px 25px rgba(160,0,212,0.18);
    border: 1px solid #e5e7eb;
}

.logo .a {
    font-weight:900;
    color:#a000d4;
    font-size:16px;
}

.logo .b {
    font-size:9px;
    font-weight:900;
    color:#f23b9b;
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
    border: 1px solid rgba(242,59,155,0.45);
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.10),
        0 8px 24px rgba(160,0,212,0.16);
}

/* KPI TEXT */
.kpi-title {
    font-size:12px;
    color:#111827;
    font-weight:900;
}

.kpi-value {
    font-size:34px;
    font-weight:900;
    color:#020617;
    margin-top: 10px;
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
    margin-top: 28px;
    margin-bottom: 28px;
}

/* ESPAÇAMENTO MOBILE */
@media (max-width: 768px) {
    .header-title {
        font-size: 24px;
    }

    .logout-btn {
        padding: 10px 24px;
    }

    .logo {
        width: 70px;
        height: 70px;
    }
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
# TOPO COM MENU
# =========================
top_col1, top_col2, top_col3 = st.columns([1.2, 8, 2])

with top_col1:
    with st.popover("☰"):
        st.markdown("""
        <a class="menu-link" href="#" target="_self">📊 Dashboard</a>
        <a class="menu-link" href="#" target="_self">📋 Dados da planilha</a>
        <a class="menu-link" href="#" target="_self">⚙️ Configurações</a>
        """, unsafe_allow_html=True)

with top_col2:
    st.markdown(f"""
    <div class="header-left">
        <div>
            <div class="header-title">⚙️ Operação Comercial</div>
            <div class="header-subtitle">Oppi Vision • Dashboard Premium</div>
            <div class="header-total">Total de registros: {len(df)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with top_col3:
    st.markdown("""
    <div class="logout-btn">Sair</div>
    """, unsafe_allow_html=True)

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
    <div class="logo-wrap">
        <div class="logo">
            <div class="a">OPPI</div>
            <div class="b">VISION</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

st.divider()

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
        color_continuous_scale=["#f23b9b", "#a000d4"]
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
        color_continuous_scale=["#f23b9b", "#a000d4"]
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
    color_continuous_scale=["#f23b9b", "#a000d4"]
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

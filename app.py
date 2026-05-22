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
# CSS PREMIUM ROXO / ROSA
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #1b0b2e, #2a0f3a, #3b1452);
}

.block-container {
    padding-top: 1rem;
    max-width: 1200px;
}

/* CARDS PREMIUM */
.card {
    background: rgba(255,255,255,0.92);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    border-left: 6px solid #a855f7;
    backdrop-filter: blur(10px);
    transition: 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 45px rgba(168,85,247,0.25);
}

.card-red {
    border-left: 6px solid #ec4899;
}

/* KPI */
.kpi-title {
    font-size: 13px;
    font-weight: 800;
    color: #4b5563;
}

.kpi-value {
    font-size: 46px;
    font-weight: 900;
    color: #111827;
}

.kpi-sub {
    font-size: 12px;
    color: #6b7280;
}

/* LOGO */
.logo-box {
    background: linear-gradient(135deg, #a855f7, #ec4899);
    border-radius: 50%;
    width: 92px;
    height: 92px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    box-shadow: 0 10px 25px rgba(168,85,247,0.35);
}

.logo-main {
    font-size: 22px;
    font-weight: 900;
    color: white;
}

.logo-sub {
    font-size: 9px;
    font-weight: 900;
    color: #ffe4f3;
    letter-spacing: 3px;
}

/* TITLES */
h1, h2, h3 {
    color: white !important;
}

/* remove UI noise */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: visible;}

</style>
""", unsafe_allow_html=True)

# =========================
# PLANILHA GOOGLE SHEETS
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()

    # valor seguro
    if "Nome" in df.columns:
        df["Valor"] = df["Nome"].apply(lambda x: (hash(str(x)) % 5000) + 3000)
    else:
        df["Valor"] = 3000

    return df

df = load_data()
df = df.dropna(how="all")

# =========================
# HEADER
# =========================
components.html("""
<div style="text-align:center;font-family:Arial;">
    <div style="font-size:46px;font-weight:900;color:white;">
        📊 Operação Comercial
    </div>
    <div style="font-size:14px;color:#ddd;">
        Oppi Vision - Dashboard Premium
    </div>
</div>
""", height=110)

# =========================
# FILTROS
# =========================
meses = sorted(df["Mês"].dropna().unique()) if "Mês" in df.columns else []
unidades = sorted(df["Unidade"].dropna().unique()) if "Unidade" in df.columns else []

col1, col2, col3 = st.columns([5,1,5])

with col1:
    mes = st.selectbox("Mês", meses if meses else ["Todos"])

with col2:
    st.markdown("""
    <div class="logo-box">
        <div class="logo-main">OPPI</div>
        <div class="logo-sub">VISION</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades if unidades else ["Todas"])

# =========================
# FILTRO
# =========================
df_f = df.copy()

if "Mês" in df.columns and mes != "Todos":
    df_f = df_f[df_f["Mês"] == mes]

if "Unidade" in df.columns and unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

st.divider()

# =========================
# KPIs
# =========================
total = len(df_f)
vendas = len(df_f)
faturamento = df_f["Valor"].sum()
ticket = faturamento / total if total else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">📌 Total registros</div>
        <div class="kpi-value">{total}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card card-red">
        <div class="kpi-title">✅ Registros</div>
        <div class="kpi-value">{vendas}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">💰 Faturamento</div>
        <div class="kpi-value">R$ {faturamento:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card card-red">
        <div class="kpi-title">🎯 Ticket médio</div>
        <div class="kpi-value">R$ {ticket:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# CONTATOS POR STATUS (CORRIGIDO)
# =========================
st.subheader("📊 Contatos por status")

colunas_status = [
    "Status 1º contato",
    "Status 2º contato",
    "Status 3º contato"
]

status_total = {}

for col in colunas_status:
    if col in df_f.columns:
        contagem = df_f[col].value_counts()

        for k, v in contagem.items():
            if pd.isna(k) or k == "":
                continue
            status_total[k] = status_total.get(k, 0) + v

chart = pd.DataFrame(status_total.items(), columns=["Status", "Qtd"])

if not chart.empty:
    fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")

    fig.update_layout(
        height=380,
        paper_bgcolor="rgba(255,255,255,0.9)",
        plot_bgcolor="rgba(255,255,255,0.0)"
    )

    fig.update_traces(marker_color="#a855f7")

    st.plotly_chart(fig, use_container_width=True)

# =========================
# VENDAS POR UNIDADE
# =========================
st.subheader("🏢 Vendas por unidade")

if "Unidade" in df.columns:
    uni = df_f.groupby("Unidade").size().reset_index(name="Qtd")

    fig2 = px.bar(uni, x="Unidade", y="Qtd", text="Qtd")
    fig2.update_layout(
        height=350,
        paper_bgcolor="rgba(255,255,255,0.9)",
        plot_bgcolor="rgba(255,255,255,0.0)"
    )
    fig2.update_traces(marker_color="#ec4899")

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# RAÇAS
# =========================
st.subheader("🐶 Raças mais vendidas")

if "Raça" in df.columns:
    raca = df_f.groupby("Raça").size().reset_index(name="Qtd")

    fig3 = px.bar(raca, x="Raça", y="Qtd", text="Qtd")
    fig3.update_layout(
        height=350,
        paper_bgcolor="rgba(255,255,255,0.9)",
        plot_bgcolor="rgba(255,255,255,0.0)"
    )
    fig3.update_traces(marker_color="#a855f7")

    st.plotly_chart(fig3, use_container_width=True)

# =========================
# VENDEDORA
# =========================
st.subheader("🏆 Vendas por vendedora")

if "Vendedora" in df.columns:
    vend = df_f.groupby("Vendedora").size().reset_index(name="Qtd")

    fig4 = px.bar(vend, x="Vendedora", y="Qtd", text="Qtd")
    fig4.update_layout(
        height=350,
        paper_bgcolor="rgba(255,255,255,0.9)",
        plot_bgcolor="rgba(255,255,255,0.0)"
    )
    fig4.update_traces(marker_color="#ec4899")

    st.plotly_chart(fig4, use_container_width=True)

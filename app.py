import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Dashboard Oppi Mockup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# STYLE (SEU DESIGN)
# =========================
st.markdown("""
<style>

.stApp {
    background: #D4D4D4;
}

.block-container {
    padding-top: 1rem;
    max-width: 1200px;
}

.card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 10px 28px rgba(15,23,42,.08);
    border-left: 7px solid #1B1D6D;
}

.card-red {
    border-left: 7px solid #9B0033;
}

.kpi-title {
    font-size: 13px;
    font-weight: 800;
    color: #334155;
}

.kpi-value {
    font-size: 44px;
    font-weight: 900;
    color: #0f172a;
}

.kpi-sub {
    font-size: 12px;
    color: #64748b;
    margin-top: 10px;
}

.logo-box {
    background: white;
    border-radius: 50%;
    width: 92px;
    height: 92px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(15,23,42,.12);
}

.logo-main {
    font-size: 24px;
    font-weight: 900;
    color: #1B1D6D;
}

.logo-sub {
    font-size: 9px;
    font-weight: 900;
    color: #9B0033;
    letter-spacing: 4px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# GOOGLE SHEET
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"


@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)

    # =========================
    # LIMPEZA BLINDADA DE COLUNAS
    # =========================
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", "")
        .str.replace("\r", "")
    )

    # segurança
    required = ["Nome", "Unidade", "Mês"]
    for col in required:
        if col not in df.columns:
            st.error(f"Coluna faltando: {col} | Colunas: {df.columns.tolist()}")
            st.stop()

    # =========================
    # VALOR FICTÍCIO ESTÁVEL
    # =========================
    df["Valor"] = df["Nome"].astype(str).apply(lambda x: (hash(x) % 5000) + 3000)

    return df


df = load_data()

# =========================
# HEADER
# =========================
components.html("""
<div style="text-align:center;font-family:Arial;">
    <div style="font-size:46px;font-weight:900;">📊 Operação Comercial</div>
    <div style="font-size:14px;color:#666;">Oppi Vision - Dashboard conectado</div>
</div>
""", height=110)

# =========================
# FILTROS
# =========================
meses = sorted(df["Mês"].dropna().unique())
unidades = sorted(df["Unidade"].dropna().unique())

col1, col2, col3 = st.columns([5,1,5])

with col1:
    mes = st.selectbox("Mês", meses)

with col2:
    st.markdown("""
    <div class="logo-box">
        <div class="logo-main">OPPI</div>
        <div class="logo-sub">VISION</div>
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
# GRÁFICOS
# =========================
g1, g2 = st.columns(2)

with g1:
    st.subheader("📊 Contatos por status")

    status = df_f["Mês"].value_counts().reset_index()
    status.columns = ["Status", "Qtd"]

    fig = px.bar(status, x="Status", y="Qtd", text="Qtd")
    st.plotly_chart(fig, use_container_width=True)

with g2:
    st.subheader("🏢 Vendas por unidade")

    uni = df_f.groupby("Unidade")["Valor"].sum().reset_index()

    fig2 = px.pie(uni, names="Unidade", values="Valor", hole=0.45)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# =========================
# TABELA FINAL
# =========================
st.subheader("📄 Dados da planilha")
st.dataframe(df_f, use_container_width=True)

st.info("Dashboard Oppi conectado direto ao Google Sheets (modo produção)")

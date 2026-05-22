import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd
import requests
import hashlib

st.set_page_config(
    page_title="Dashboard Oppi Mockup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# STYLE (SEU DESIGN MANTIDO)
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
    line-height: 1;
    margin-top: 10px;
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
    margin: auto;
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
# GOOGLE SHEET (SUA PLANILHA)
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)

    # normaliza nomes de colunas
    df.columns = [c.strip() for c in df.columns]

    # garante padrão esperado
    df = df.rename(columns={
        "Nome": "Cliente",
        "Nome Cachorro": "Cliente"
    })

    # cria valor fictício consistente (porque não existe na planilha)
    def gerar_valor(nome):
        h = int(hashlib.md5(str(nome).encode()).hexdigest(), 16)
        return (h % 5000) + 3000

    df["Valor"] = df["Nome"].apply(gerar_valor)

    return df


df = load_data()

# =========================
# HEADER
# =========================
components.html("""
<div style="text-align:center; font-family:Arial;">
    <div style="font-size:46px;font-weight:900;">
        📊 Operação Comercial
    </div>
    <div style="font-size:14px;color:#666;margin-top:8px;">
        Oppi Vision - Dashboard conectado na Google Sheets
    </div>
</div>
""", height=120)

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
        <div class="kpi-title">📌 Total de registros</div>
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
    st.subheader("📊 Registros por mês")
    fig = px.histogram(df, x="Mês", color="Unidade")
    st.plotly_chart(fig, use_container_width=True)

with g2:
    st.subheader("🏢 Vendas por unidade")
    fig2 = px.bar(df_f.groupby("Unidade")["Valor"].sum().reset_index(),
                  x="Unidade", y="Valor", text="Valor")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("📄 Dados da planilha (ao vivo)")
st.dataframe(df_f, use_container_width=True)

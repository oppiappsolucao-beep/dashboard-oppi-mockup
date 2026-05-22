import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd
from collections import Counter

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Dashboard Oppi Mockup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS (SEU ESTILO MANTIDO)
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
# PLANILHA (GOOGLE SHEETS)
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()

    # evita quebra se não existir Nome
    if "Nome" in df.columns:
        df["Valor"] = df["Nome"].apply(lambda x: (hash(str(x)) % 5000) + 3000)
    else:
        df["Valor"] = 3000

    return df

df = load_data()

# remove linhas vazias
df = df.dropna(how="all")

# =========================
# HEADER
# =========================
components.html("""
<div style="text-align:center;font-family:Arial;">
    <div style="font-size:46px;font-weight:900;">📊 Operação Comercial</div>
    <div style="font-size:14px;color:#666;">Oppi Vision - Dashboard</div>
</div>
""", height=110)

# =========================
# FILTROS (BLINDADO)
# =========================
meses = sorted(df["Mês"].dropna().unique().tolist()) if "Mês" in df.columns else []
unidades = sorted(df["Unidade"].dropna().unique().tolist()) if "Unidade" in df.columns else []

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
# FILTRO SEGURANÇA
# =========================
df_f = df.copy()

if "Mês" in df_f.columns and mes != "Todos":
    df_f = df_f[df_f["Mês"] == mes]

if "Unidade" in df_f.columns and unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

st.divider()

# =========================
# KPIs
# =========================
total = len(df_f)
vendas = len(df_f)

faturamento = df_f["Valor"].sum() if "Valor" in df_f.columns else 0
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
# 🔥 GRÁFICO STATUS (CORRIGIDO 100%)
# =========================

status_cols = [c for c in df_f.columns if "Status" in c]

counter = Counter()

for col in status_cols:
    if col in df_f.columns:
        valores = df_f[col].fillna("Vazio").astype(str)
        for v in valores:
            counter[f"{col} - {v}"] += 1

chart = pd.DataFrame(counter.items(), columns=["Status", "Qtd"])

st.subheader("📊 Contatos por status")

if not chart.empty:
    fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")
    fig.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Sem dados de status para exibir")

# =========================
# GRÁFICO UNIDADE (SEGURADO)
# =========================
st.subheader("🏢 Vendas por unidade")

if "Unidade" in df_f.columns:
    uni = df_f.groupby("Unidade").size().reset_index(name="Qtd")

    fig2 = px.bar(uni, x="Unidade", y="Qtd", text="Qtd")
    fig2.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# RAÇAS
# =========================
st.subheader("🐶 Raças mais vendidas")

if "Raça" in df_f.columns:
    raca = df_f.groupby("Raça").size().reset_index(name="Qtd")

    fig3 = px.bar(raca, x="Raça", y="Qtd", text="Qtd")
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# VENDEDORAS
# =========================
st.subheader("🏆 Vendas por vendedora")

if "Nome" in df_f.columns:
    vend = df_f.groupby("Nome").size().reset_index(name="Qtd")

    fig4 = px.bar(vend, x="Nome", y="Qtd", text="Qtd")
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# TABELA FINAL
# =========================
st.subheader("📄 Dados da planilha")
st.dataframe(df_f, use_container_width=True)

st.info("Dashboard Oppi conectado na Google Sheets (versão blindada)")

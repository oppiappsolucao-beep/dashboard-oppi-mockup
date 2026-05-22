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
# CSS (SEU DESIGN ATUAL MELHORADO)
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
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    border-left: 6px solid #1B1D6D;
}

.kpi-title {
    font-size: 13px;
    font-weight: 700;
    color: #334155;
}

.kpi-value {
    font-size: 40px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1;
    margin-top: 8px;
}

.kpi-sub {
    font-size: 12px;
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)


# =========================
# GOOGLE SHEET (CSV PUBLICO)
# =========================
@st.cache_data(ttl=60)
def load_data():

    url = "https://docs.google.com/spreadsheets/d/1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk/gviz/tq?tqx=out:csv"

    df = pd.read_csv(url)

    # limpeza básica de colunas
    df.columns = df.columns.str.strip()

    return df


df = load_data()

# proteção
if df.empty:
    st.warning("Planilha vazia")
    st.stop()


# =========================
# FILTROS
# =========================
meses = sorted(df["Mês"].dropna().unique().tolist())
unidades = sorted(df["Unidade"].dropna().unique().tolist())

col1, col2 = st.columns(2)

with col1:
    mes = st.selectbox("Mês", meses)

with col2:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)


df_f = df[df["Mês"] == mes]

if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]


# =========================
# KPIs
# =========================
total_registros = len(df_f)

# vendas (seguro)
if "Status 1º contato" in df_f.columns:
    vendas = len(df_f[df_f["Status 1º contato"].astype(str).str.contains("Enviado", na=False)])
else:
    vendas = 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">📌 Total de registros</div>
        <div class="kpi-value">{total_registros}</div>
        <div class="kpi-sub">Mês: {mes}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">✅ Vendas</div>
        <div class="kpi-value">{vendas}</div>
        <div class="kpi-sub">Convertidos</div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# 🔥 GRÁFICO STATUS (BLINDADO)
# =========================
st.subheader("📊 Contatos por status")

status_cols = [c for c in df_f.columns if "Status" in c]

if len(status_cols) > 0:

    df_status = df_f[status_cols].melt(
        var_name="Etapa",
        value_name="Status"
    )

    df_status = df_status.dropna()
    df_status = df_status[df_status["Status"] != ""]

    status_count = df_status.groupby("Status").size().reset_index(name="Qtd")

    fig = px.bar(
        status_count,
        x="Status",
        y="Qtd",
        text="Qtd"
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=20, b=20, l=10, r=10)
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Nenhuma coluna de Status encontrada na planilha")


# =========================
# 🏢 GRÁFICO UNIDADES
# =========================
st.subheader("🏢 Vendas por unidade")

df_uni = df_f.groupby("Unidade").size().reset_index(name="Qtd")

fig2 = px.bar(
    df_uni,
    x="Unidade",
    y="Qtd",
    text="Qtd"
)

fig2.update_layout(
    height=350,
    paper_bgcolor="white",
    plot_bgcolor="white"
)

st.plotly_chart(fig2, use_container_width=True)


# =========================
# 📄 TABELA FINAL
# =========================
st.subheader("📄 Dados da planilha")

st.dataframe(df_f, use_container_width=True)


# =========================
# INFO FINAL
# =========================
st.info("Dashboard conectado diretamente na Google Sheets (modo produção)")

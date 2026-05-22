import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Operação Comercial",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS PROFISSIONAL
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
}

</style>
""", unsafe_allow_html=True)


# =========================
# 🔥 FUNÇÃO DE LEITURA GOOGLE SHEETS
# =========================
@st.cache_data(ttl=60)
def load_data():

    url = "https://docs.google.com/spreadsheets/d/1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk/gviz/tq?tqx=out:csv"

    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    return df


df = load_data()

# =========================
# LIMPEZA SEGURA
# =========================
df_f = df.copy()

# garantir que não quebra se vier vazio
if df_f.empty:
    st.warning("Planilha vazia")
    st.stop()


# =========================
# FILTROS
# =========================
meses = sorted(df_f["Mês"].dropna().unique())
unidades = sorted(df_f["Unidade"].dropna().unique())

col1, col2 = st.columns(2)

with col1:
    mes = st.selectbox("Mês", meses)

with col2:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

df_f = df_f[df_f["Mês"] == mes]

if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]


# =========================
# KPIs
# =========================
total = len(df_f)
vendas = len(df_f[df_f["Status 1º contato"] == "Enviado"]) if "Status 1º contato" in df_f.columns else 0
faturamento = 0

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
        <div class="kpi-title">Vendas</div>
        <div class="kpi-value">{vendas}</div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# 📊 GRÁFICO STATUS (CORRIGIDO DEFINITIVO)
# =========================
st.subheader("Contatos por status")

status_cols = [c for c in df_f.columns if "Status" in c]

if status_cols:

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

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Nenhuma coluna de Status encontrada")


# =========================
# 🏢 GRÁFICO UNIDADE
# =========================
st.subheader("Vendas por unidade")

uni = df_f.groupby("Unidade").size().reset_index(name="Qtd")

fig2 = px.bar(
    uni,
    x="Unidade",
    y="Qtd",
    text="Qtd"
)

st.plotly_chart(fig2, use_container_width=True)


# =========================
# TABELA FINAL
# =========================
st.subheader("Dados")

st.dataframe(df_f, use_container_width=True)

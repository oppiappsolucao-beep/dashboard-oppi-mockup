import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Oppi Vision",
    page_icon="📊",
    layout="wide"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background: #d9d9d9;
}

.block-container {
    max-width: 1400px;
    padding-top: 1rem;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# GOOGLE SHEETS LOAD
# =========================
@st.cache_data(ttl=60)
def load_data():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Planilha Oppi Mockup").sheet1
    data = sheet.get_all_records()

    return pd.DataFrame(data)

try:
    df = load_data()
except Exception:
    st.error("Erro ao carregar planilha.")
    st.stop()

# =========================
# LIMPEZA
# =========================
df.columns = df.columns.str.strip()

# =========================
# 🔥 UNIDADES (1/2/3)
# =========================
unidades_originais = sorted(df["Unidade"].dropna().unique())

mapa_unidades = {
    unidades_originais[i]: f"Unidade {i+1}"
    for i in range(len(unidades_originais))
}

df["Unidade"] = df["Unidade"].map(mapa_unidades)

unidades = sorted(df["Unidade"].dropna().unique())

# =========================
# HEADER
# =========================
col1, col2, col3 = st.columns([1,6,1])

with col2:
    st.title("📊 Operação Comercial")
    st.caption("Dashboard Oppi Vision conectado à planilha")

# =========================
# FILTROS
# =========================
meses = sorted(df["Mês"].dropna().unique())

c1, c2 = st.columns(2)

with c1:
    mes = st.selectbox("Mês", meses)

with c2:
    unidade = st.selectbox("Unidade", ["Todas"] + list(unidades))

df_f = df[df["Mês"] == mes]

if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

# =========================
# KPIs
# =========================
total = len(df_f)
vendas = len(df_f[df_f["Status"].str.contains("Venda", na=False)])
faturamento = pd.to_numeric(df_f["Valor"], errors="coerce").sum()
ticket = faturamento / vendas if vendas > 0 else 0

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total registros", total)
k2.metric("Vendas", vendas)
k3.metric("Faturamento", f"R$ {faturamento:,.2f}")
k4.metric("Ticket médio", f"R$ {ticket:,.2f}")

# =========================
# GRÁFICOS
# =========================
st.divider()

g1, g2 = st.columns(2)

with g1:
    st.subheader("Contatos por status")
    st.bar_chart(df_f["Status"].value_counts())

with g2:
    st.subheader("Vendas por unidade")
    st.bar_chart(df_f.groupby("Unidade")["Valor"].sum())

# =========================
# TABELA
# =========================
st.divider()

st.subheader("Dados da planilha")
st.dataframe(df_f, use_container_width=True)

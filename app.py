import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Oppi Vision",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# CSS (mesmo estilo seu)
# =========================================================

st.markdown("""
<style>
.stApp {
    background: #d9d9d9;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: white !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# GOOGLE SHEETS LOAD
# =========================================================

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

    # 🔥 NOME DA SUA PLANILHA
    sheet = client.open("Planilha Oppi Mockup").sheet1

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    return df

# =========================================================
# LOAD DF
# =========================================================

try:
    df = load_data()
except Exception as e:
    st.error("Erro ao carregar a planilha.")
    st.stop()

# =========================================================
# NORMALIZAÇÃO
# =========================================================

df.columns = df.columns.str.strip()

# garante nome padrão esperado
df = df.rename(columns={
    "Unidade": "Unidade",
    "Mês": "Mês",
    "Valor": "Valor",
    "Status": "Status",
    "Cliente": "Cliente"
})

# =========================================================
# 🔥 UNIDADE (1 / 2 / 3)
# =========================================================

unidades_originais = sorted(df["Unidade"].dropna().unique())

mapa_unidades = {
    unidades_originais[i]: f"Unidade {i+1}"
    for i in range(len(unidades_originais))
}

df["Unidade"] = df["Unidade"].map(mapa_unidades)

unidades = sorted(df["Unidade"].dropna().unique())

# =========================================================
# HEADER
# =========================================================

col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.button("☰")

with col2:
    st.markdown("## ⚙️ Operação Comercial")
    st.caption("Dashboard Oppi Vision conectado à planilha real")

with col3:
    st.button("Sair")

# =========================================================
# FILTROS
# =========================================================

meses = sorted(df["Mês"].dropna().unique())

c1, c2, c3 = st.columns([3,1,3])

with c1:
    mes = st.selectbox("Mês", meses)

with c2:
    st.markdown("""
    <div style="text-align:center;padding-top:25px;font-weight:800;">
        OPPI VISION
    </div>
    """, unsafe_allow_html=True)

with c3:
    unidade = st.selectbox("Unidade", ["Todas"] + list(unidades))

# =========================================================
# FILTRO DF
# =========================================================

df_f = df[df["Mês"] == mes]

if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]

# =========================================================
# KPIs DINÂMICOS
# =========================================================

total = len(df_f)
vendas = len(df_f[df_f["Status"].str.contains("Venda", na=False)])

faturamento = pd.to_numeric(df_f["Valor"], errors="coerce").sum()
ticket = faturamento / vendas if vendas > 0 else 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total registros", total)
c2.metric("Vendas registradas", vendas)
c3.metric("Faturamento", f"R$ {faturamento:,.2f}")
c4.metric("Ticket médio", f"R$ {ticket:,.2f}")

# =========================================================
# GRÁFICOS
# =========================================================

st.divider()

g1, g2 = st.columns(2)

with g1:
    st.subheader("Contatos por status")
    st.bar_chart(df_f["Status"].value_counts())

with g2:
    st.subheader("Vendas por unidade")
    st.bar_chart(df_f.groupby("Unidade")["Valor"].sum())

# =========================================================
# TABELA FINAL
# =========================================================

st.subheader("Base de dados (Planilha Oppi Mockup)")
st.dataframe(df_f, use_container_width=True)

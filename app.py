import streamlit as st
import pandas as pd
import plotly.express as px
import itertools

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Oppi Vision",
    page_icon="📊",
    layout="wide"
)

# =========================
# CSS PROFISSIONAL
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

.card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔥 SAFE DATA LAYER (BLINDADO)
# =========================
def get_demo_data():

    status = [
        "1º contato", "2º contato", "3º contato", "Venda",
        "1º contato", "Venda", "2º contato", "Venda"
    ]

    unidade = [
        "Campinas", "Indaiatuba", "Piracicaba", "Campinas",
        "Indaiatuba", "Piracicaba", "Campinas", "Indaiatuba"
    ]

    valor = [
        1200, 2500, 1800, 3200,
        4100, 5000, 2300, 6100
    ]

    return pd.DataFrame({
        "Status": status,
        "Unidade": unidade,
        "Valor": valor,
        "Mês": ["04/2026"] * 8
    })

# =========================
# 🔥 SAFE LOAD (NUNCA QUEBRA)
# =========================
@st.cache_data(ttl=60)
def load_data():

    try:
        # tenta carregar planilha real
        import gspread
        from google.oauth2.service_account import Credentials

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

        df = pd.DataFrame(data)

        if df.empty:
            return get_demo_data()

        return df

    except:
        return get_demo_data()

df = load_data()

# =========================
# LIMPEZA SEGURA
# =========================
df.columns = df.columns.str.strip()

# =========================
# 🔥 UNIDADES BLINDADAS
# =========================
try:
    unidades_originais = sorted(df["Unidade"].dropna().unique())

    mapa_unidades = {
        unidades_originais[i]: f"Unidade {i+1}"
        for i in range(len(unidades_originais))
    }

    df["Unidade"] = df["Unidade"].map(mapa_unidades)

    unidades = sorted(df["Unidade"].dropna().unique())

except:
    df["Unidade"] = "Unidade 1"
    unidades = ["Unidade 1"]

# =========================
# HEADER
# =========================
st.title("📊 Operação Comercial")
st.caption("Oppi Vision • Dashboard profissional blindado")

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
# 🔥 KPIs (100% SAFE)
# =========================
total = len(df_f)

vendas = 0
if "Status" in df_f:
    vendas = len(df_f[df_f["Status"].astype(str).str.contains("Venda", na=False)])

faturamento = 0
if "Valor" in df_f:
    faturamento = pd.to_numeric(df_f["Valor"], errors="coerce").sum()

ticket = faturamento / vendas if vendas > 0 else 0

# =========================
# CARDS
# =========================
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total registros", total)
k2.metric("Vendas", vendas)
k3.metric("Faturamento", f"R$ {faturamento:,.2f}")
k4.metric("Ticket médio", f"R$ {ticket:,.2f}")

# =========================
# GRÁFICOS (SAFE MODE)
# =========================
st.divider()

g1, g2 = st.columns(2)

with g1:
    st.subheader("Status")
    if "Status" in df_f:
        st.bar_chart(df_f["Status"].value_counts())

with g2:
    st.subheader("Unidades")
    if "Unidade" in df_f and "Valor" in df_f:
        st.bar_chart(df_f.groupby("Unidade")["Valor"].sum())

# =========================
# TABELA FINAL
# =========================
st.divider()
st.subheader("Base de dados (modo blindado)")

st.dataframe(df_f, use_container_width=True)

import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

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
# CSS PREMIUM (SKOOB + SAAS)
# =========================
st.markdown("""
<style>

/* FUNDO EXTERNO (Skoob clean) */
.stApp {
    background: #D4D4D4;
}

/* ÁREA CENTRAL (painel roxo premium) */
.block-container {
    background: linear-gradient(135deg, #1b0b2e, #2a0f3a, #3b1452);
    border-radius: 24px;
    padding: 25px;
    margin-top: 15px;
    box-shadow: 0 25px 70px rgba(0,0,0,0.35);
    max-width: 1200px;
}

/* CARDS */
.card {
    background: white;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    border-left: 6px solid #c084fc;
    transition: 0.25s ease;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.25);
}

/* KPIs */
.kpi-title {
    font-size: 12px;
    font-weight: 700;
    color: #475569;
}

.kpi-value {
    font-size: 40px;
    font-weight: 900;
    color: #0f172a;
}

.kpi-sub {
    font-size: 11px;
    color: #64748b;
}

/* LOGO */
.logo-box {
    background: white;
    border-radius: 50%;
    width: 90px;
    height: 90px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.logo-main {
    font-size: 22px;
    font-weight: 900;
    color: #7c3aed;
}

.logo-sub {
    font-size: 10px;
    font-weight: 900;
    color: #ec4899;
    letter-spacing: 3px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# GOOGLE SHEETS
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()

    # garante coluna Valor
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
    <div style="font-size:44px;font-weight:900;color:white;">
        📊 Operação Comercial
    </div>
    <div style="font-size:14px;color:#ddd;">
        Oppi Vision • Dashboard Premium
    </div>
</div>
""", height=120)

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
    <div class="card">
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
    <div class="card">
        <div class="kpi-title">🎯 Ticket médio</div>
        <div class="kpi-value">R$ {ticket:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# CONTATOS POR STATUS (SKOOB FIX)
# =========================
st.subheader("📊 Contatos por status")

status_cols = [
    "Status 1º contato",
    "Status 2º contato",
    "Status 3º contato"
]

status_total = {}

for col in status_cols:
    if col in df_f.columns:
        for k, v in df_f[col].value_counts().items():
            if pd.notna(k) and k != "":
                status_total[k] = status_total.get(k, 0) + v

chart = pd.DataFrame(list(status_total.items()), columns=["Status", "Qtd"])

if not chart.empty:
    fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")
    fig.update_layout(
        height=380,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# UNIDADE
# =========================
st.subheader("🏢 Vendas por unidade")

if "Unidade" in df_f.columns:
    uni = df_f.groupby("Unidade").size().reset_index(name="Qtd")

    fig2 = px.bar(uni, x="Unidade", y="Qtd", text="Qtd")
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
# VENDEDORA
# =========================
st.subheader("🏆 Vendas por vendedora")

if "Vendedora" in df_f.columns:
    vend = df_f.groupby("Vendedora").size().reset_index(name="Qtd")

    fig4 = px.bar(vend, x="Vendedora", y="Qtd", text="Qtd")
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# TABELA FINAL
# =========================
st.subheader("📄 Dados da planilha")

st.dataframe(df_f, use_container_width=True)

st.info("Dashboard premium estilo Skoob + Oppi Vision com UI SaaS moderna 💜")

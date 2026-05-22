import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Oppi Mockup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

.stApp {
    background: #D4D4D4;
}

/* container mais profissional (Skoob-like) */
.block-container {
    padding-top: 1rem;
    max-width: 1200px;
}

/* header clean */
header[data-testid="stHeader"] {
    background: transparent;
}

/* =========================
   CARDS (SKOOB STYLE MELHORADO)
========================= */
.card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 10px 28px rgba(15,23,42,.08);
    border-left: 7px solid #1B1D6D;
    transition: all .2s ease;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 34px rgba(15,23,42,.12);
}

.card-red {
    border-left: 7px solid #9B0033;
}

/* KPIs */
.kpi-title {
    font-size: 13px;
    font-weight: 800;
    color: #334155;
    letter-spacing: 0.2px;
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

/* =========================
   LOGO
========================= */
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

/* =========================
   TITLES
========================= */
.title {
    font-size: 42px;
    font-weight: 900;
    color: #0f172a;
}

.subtitle {
    font-size: 14px;
    color: #64748b;
}

/* remove streamlit noise */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: visible;}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (melhor alinhado)
# =========================
components.html("""
<div style="
    width:100%;
    display:flex;
    justify-content:center;
    margin-top:10px;
    margin-bottom:10px;
    font-family:Arial;
">

    <div style="text-align:center">

        <div style="
            font-size:46px;
            font-weight:900;
            color:#0f172a;
        ">
            📊 Operação Comercial
        </div>

        <div style="
            font-size:14px;
            color:#64748b;
            margin-top:8px;
        ">
            Dashboard mockup para demonstração de automações, contratos e vendas
        </div>

    </div>

</div>
""", height=120)

# =========================
# DADOS (FICÇÃO)
# =========================
dados = [
    {"Cliente": "João Mendes", "Unidade": "Unidade 1", "Raça": "Spitz Alemão", "Valor": 5200, "Status": "1º contato", "Mês": "04/2026"},
    {"Cliente": "Marina Costa", "Unidade": "Unidade 2", "Raça": "Golden Retriever", "Valor": 6800, "Status": "2º contato", "Mês": "03/2026"},
    {"Cliente": "Carlos Lima", "Unidade": "Unidade 1", "Raça": "Maine Coon", "Valor": 6100, "Status": "3º contato", "Mês": "02/2026"},
    {"Cliente": "Fernanda Alves", "Unidade": "Unidade 3", "Raça": "Shih Tzu", "Valor": 3900, "Status": "Venda registrada", "Mês": "01/2026"},
    {"Cliente": "Rafael Souza", "Unidade": "Unidade 2", "Raça": "Bulldog Francês", "Valor": 7500, "Status": "Venda registrada", "Mês": "05/2026"},
]

meses = sorted(list(set(item["Mês"] for item in dados)))
unidades = sorted(list(set(item["Unidade"] for item in dados)))

col_f1, col_logo, col_f2 = st.columns([5,1,5])

with col_f1:
    mes = st.selectbox("Mês", meses)

with col_logo:
    st.markdown("""
    <div class="logo-box">
        <div class="logo-main">OPPI</div>
        <div class="logo-sub">VISION</div>
    </div>
    """, unsafe_allow_html=True)

with col_f2:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

# filtro
dados_filtrados = [d for d in dados if d["Mês"] == mes]
if unidade != "Todas":
    dados_filtrados = [d for d in dados_filtrados if d["Unidade"] == unidade]

st.divider()

# =========================
# KPIs
# =========================
total_registros = len(dados_filtrados)
vendas = len([d for d in dados_filtrados if "Venda" in d["Status"]])
faturamento = sum(d["Valor"] for d in dados_filtrados)
ticket_medio = faturamento / total_registros if total_registros else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">📌 Total de registros</div>
        <div class="kpi-value">{total_registros}</div>
        <div class="kpi-sub">Mês selecionado: {mes}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card card-red">
        <div class="kpi-title">✅ Vendas registradas</div>
        <div class="kpi-value">{vendas}</div>
        <div class="kpi-sub">Contratos convertidos</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">💰 Faturamento</div>
        <div class="kpi-value">R$ {faturamento:,.0f}</div>
        <div class="kpi-sub">Valor fictício demonstrativo</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card card-red">
        <div class="kpi-title">🎯 Ticket médio</div>
        <div class="kpi-value">R$ {ticket_medio:,.0f}</div>
        <div class="kpi-sub">Média por registro</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================
# GRÁFICOS
# =========================
g1, g2 = st.columns(2)

with g1:
    st.subheader("📞 Contatos por status")

    df_status = {}
    for d in dados_filtrados:
        df_status[d["Status"]] = df_status.get(d["Status"], 0) + 1

    fig = px.bar(
        x=list(df_status.keys()),
        y=list(df_status.values()),
        text=list(df_status.values())
    )
    st.plotly_chart(fig, use_container_width=True)

with g2:
    st.subheader("🏢 Vendas por unidade")

    df_uni = {}
    for d in dados_filtrados:
        df_uni[d["Unidade"]] = df_uni.get(d["Unidade"], 0) + d["Valor"]

    fig2 = px.pie(
        names=list(df_uni.keys()),
        values=list(df_uni.values()),
        hole=0.45
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("📄 Contratos demonstrativos")

st.dataframe(dados_filtrados, use_container_width=True)

st.info("Dashboard com layout profissional estilo Oppi / SkoobPet (mockup comercial)")

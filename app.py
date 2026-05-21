import streamlit as st
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

.block-container {
    max-width: 1250px;
    padding-top: 1rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* TITULO */

.main-title {
    font-size: 56px;
    font-weight: 900;
    color: #09122C;
    line-height: 1;
}

.main-subtitle {
    color: #64748b;
    font-size: 15px;
    margin-top: 10px;
}

/* LOGO */

.logo-box {
    background: white;
    width: 135px;
    height: 135px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 28px rgba(15,23,42,.10);
    margin: auto;
}

.logo-main {
    font-size: 44px;
    font-weight: 900;
    color: #1B1D6D;
    line-height: 1;
}

.logo-sub {
    font-size: 14px;
    font-weight: 900;
    color: #9B0033;
    letter-spacing: 8px;
    margin-top: 8px;
}

/* CARDS */

.card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 8px 22px rgba(15,23,42,.08);
    border-left: 8px solid #1B1D6D;
}

.card-red {
    border-left: 8px solid #B0004F;
}

.kpi-title {
    font-size: 16px;
    font-weight: 800;
    color: #1e293b;
}

.kpi-value {
    font-size: 54px;
    font-weight: 900;
    color: #09122C;
    margin-top: 12px;
    line-height: 1;
}

.kpi-sub {
    font-size: 13px;
    color: #64748b;
    margin-top: 14px;
}

/* GRAFICOS */

.chart-box {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 8px 22px rgba(15,23,42,.08);
}

/* TABELA */

.table-box {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 8px 22px rgba(15,23,42,.08);
}

/* INFO */

.info-box {
    background: #E8F0FE;
    border-radius: 14px;
    padding: 18px;
    color: #1e293b;
    font-weight: 600;
}

/* SELECT */

div[data-testid="stSelectbox"] label {
    font-weight: 700 !important;
    color: #334155 !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: white !important;
    border-radius: 14px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div class="main-title">
📊 Operação Comercial
</div>

<div class="main-subtitle">
Dashboard mockup para demonstração de automações, contratos e vendas
</div>
""", unsafe_allow_html=True)

st.write("")

# =========================
# DADOS
# =========================

dados = [
    {"Cliente": "João Mendes", "Unidade": "Campinas", "Raça": "Spitz Alemão", "Valor": 5200, "Status": "1º contato", "Mês": "05/2026"},
    {"Cliente": "Marina Costa", "Unidade": "Indaiatuba", "Raça": "Golden Retriever", "Valor": 6800, "Status": "2º contato", "Mês": "05/2026"},
    {"Cliente": "Carlos Lima", "Unidade": "Campinas", "Raça": "Maine Coon", "Valor": 6100, "Status": "3º contato", "Mês": "05/2026"},
    {"Cliente": "Fernanda Alves", "Unidade": "Jundiaí", "Raça": "Shih Tzu", "Valor": 3900, "Status": "Venda registrada", "Mês": "05/2026"},
    {"Cliente": "Rafael Souza", "Unidade": "Sorocaba", "Raça": "Bulldog Francês", "Valor": 7500, "Status": "Venda registrada", "Mês": "05/2026"},
    {"Cliente": "Patrícia Rocha", "Unidade": "Campinas", "Raça": "Poodle Toy", "Valor": 4300, "Status": "Primeiro contato mês", "Mês": "05/2026"},
    {"Cliente": "Lucas Martins", "Unidade": "Indaiatuba", "Raça": "Spitz Alemão", "Valor": 5800, "Status": "Segundo contato mês", "Mês": "05/2026"},
    {"Cliente": "Aline Ferreira", "Unidade": "Jundiaí", "Raça": "Border Collie", "Valor": 6400, "Status": "Terceiro contato mês", "Mês": "05/2026"},
]

meses = sorted(list(set(item["Mês"] for item in dados)))
unidades = sorted(list(set(item["Unidade"] for item in dados)))

# =========================
# FILTROS + LOGO NO MEIO
# =========================

col1, col2, col3 = st.columns([5, 2, 5])

with col1:
    mes = st.selectbox("Mês", meses)

with col2:

    st.markdown("""
    <div class="logo-box">

        <div class="logo-main">
            OPPI
        </div>

        <div class="logo-sub">
            VISION
        </div>

    </div>
    """, unsafe_allow_html=True)

with col3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

# =========================
# FILTRO
# =========================

dados_filtrados = [item for item in dados if item["Mês"] == mes]

if unidade != "Todas":
    dados_filtrados = [
        item for item in dados_filtrados
        if item["Unidade"] == unidade
    ]

# =========================
# KPIS
# =========================

st.divider()

total_registros = len(dados_filtrados)

vendas = len([
    item for item in dados_filtrados
    if item["Status"] == "Venda registrada"
])

faturamento = sum(item["Valor"] for item in dados_filtrados)

ticket_medio = faturamento / total_registros if total_registros else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="card">

        <div class="kpi-title">
            📌 Total de registros
        </div>

        <div class="kpi-value">
            {total_registros}
        </div>

        <div class="kpi-sub">
            Mês selecionado: {mes}
        </div>

    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card card-red">

        <div class="kpi-title">
            ✅ Vendas registradas
        </div>

        <div class="kpi-value">
            {vendas}
        </div>

        <div class="kpi-sub">
            Contratos convertidos
        </div>

    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">

        <div class="kpi-title">
            💰 Faturamento
        </div>

        <div class="kpi-value">
            R$ {faturamento:,.0f}
        </div>

        <div class="kpi-sub">
            Valor fictício demonstrativo
        </div>

    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card card-red">

        <div class="kpi-title">
            🎯 Ticket médio
        </div>

        <div class="kpi-value">
            R$ {ticket_medio:,.0f}
        </div>

        <div class="kpi-sub">
            Média por registro
        </div>

    </div>
    """.replace(",", "."), unsafe_allow_html=True)

# =========================
# GRAFICOS
# =========================

st.divider()

g1, g2 = st.columns(2)

with g1:

    st.markdown("""
    <div class="chart-box">
    """, unsafe_allow_html=True)

    st.subheader("📞 Contatos por status")

    status_contagem = {}

    for item in dados_filtrados:
        status_contagem[item["Status"]] = (
            status_contagem.get(item["Status"], 0) + 1
        )

    status_lista = [
        {"Status": k, "Quantidade": v}
        for k, v in status_contagem.items()
    ]

    fig = px.bar(
        status_lista,
        x="Status",
        y="Quantidade",
        text="Quantidade"
    )

    fig.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with g2:

    st.markdown("""
    <div class="chart-box">
    """, unsafe_allow_html=True)

    st.subheader("🏢 Vendas por unidade")

    unidade_valores = {}

    for item in dados_filtrados:
        unidade_valores[item["Unidade"]] = (
            unidade_valores.get(item["Unidade"], 0)
            + item["Valor"]
        )

    unidade_lista = [
        {"Unidade": k, "Valor": v}
        for k, v in unidade_valores.items()
    ]

    fig2 = px.pie(
        unidade_lista,
        names="Unidade",
        values="Valor",
        hole=0.50
    )

    fig2.update_layout(
        height=350,
        paper_bgcolor="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TABELA
# =========================

st.divider()

st.markdown("""
<div class="table-box">
""", unsafe_allow_html=True)

st.subheader("📄 Contratos demonstrativos")

st.dataframe(
    dados_filtrados,
    use_container_width=True,
    hide_index=True
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# INFO
# =========================

st.write("")

st.markdown("""
<div class="info-box">
ℹ️ Este dashboard usa apenas dados fictícios para demonstração comercial.
</div>
""", unsafe_allow_html=True)

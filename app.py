import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Oppi Mockup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background: #D4D4D4;
}

.block-container {
    max-width: 1320px;
    padding-top: 1rem;
}

/* HEADER */

.main-title {
    font-size: 56px;
    font-weight: 800;
    color: #1f2937;
    line-height: 1;
    font-family: "Arial";
}

.main-subtitle {
    color: #7c8593;
    font-size: 15px;
    margin-top: 10px;
    font-family: "Arial";
}

/* SELECTS */

div[data-testid="stSelectbox"] label {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #1f2937 !important;
    margin-bottom: 8px !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: white !important;
    border-radius: 14px !important;
    min-height: 56px !important;
    border: none !important;
    box-shadow: none !important;
}

/* LINHA */

hr {
    border-color: rgba(15,23,42,0.12) !important;
}

/* KPI */

.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    height: 150px;
    box-shadow: 0 5px 16px rgba(0,0,0,0.08);
    border-left: 8px solid #1B1D6D;
}

.kpi-red {
    border-left: 8px solid #C10057;
}

.kpi-title {
    font-size: 17px;
    font-weight: 800;
    color: #1f2937;
    line-height: 1.3;
    font-family: Arial;
}

.kpi-value {
    font-size: 56px;
    font-weight: 900;
    color: #09122C;
    margin-top: 14px;
    line-height: 1;
    font-family: Arial;
}

.kpi-sub {
    font-size: 13px;
    color: #7c8593;
    margin-top: 10px;
    font-family: Arial;
}

/* BOX GRAFICOS */

.chart-box {
    background: white;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 5px 16px rgba(0,0,0,0.08);
}

/* TITULO GRAFICOS */

.chart-title {
    font-size: 20px;
    font-weight: 800;
    color: #1f2937;
    margin-bottom: 14px;
    font-family: Arial;
}

/* LOGO */

.logo-box {
    background: white;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 20px rgba(15,23,42,.10);
    margin: auto;
}

.logo-main {
    font-size: 34px;
    font-weight: 900;
    color: #1B1D6D;
    line-height: 1;
    font-family: Arial;
}

.logo-sub {
    font-size: 12px;
    font-weight: 900;
    color: #C10057;
    letter-spacing: 6px;
    margin-top: 6px;
    font-family: Arial;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

components.html("""
<div style="
    width:100%;
    display:flex;
    justify-content:center;
    margin-top:8px;
    margin-bottom:25px;
    font-family:Arial;
">
    <div style="text-align:center;">

        <div style="
            font-size:58px;
            font-weight:800;
            color:#09122C;
            line-height:1;
        ">
            📊 Operação Comercial
        </div>

        <div style="
            color:#7c8593;
            font-size:15px;
            margin-top:12px;
        ">
            Dashboard mockup para demonstração de automações, contratos e vendas
        </div>

    </div>
</div>
""", height=120)

# ==================================================
# DADOS MOCKADOS
# ==================================================

dados = [
    {"Cliente": "João Mendes", "Unidade": "Campinas", "Valor": 5200, "Status": "1º contato", "Mês": "05/2026"},
    {"Cliente": "Marina Costa", "Unidade": "Indaiatuba", "Valor": 6800, "Status": "2º contato", "Mês": "05/2026"},
    {"Cliente": "Carlos Lima", "Unidade": "Campinas", "Valor": 6100, "Status": "3º contato", "Mês": "05/2026"},
    {"Cliente": "Fernanda Alves", "Unidade": "Jundiaí", "Valor": 3900, "Status": "Venda registrada", "Mês": "05/2026"},
    {"Cliente": "Rafael Souza", "Unidade": "Sorocaba", "Valor": 7500, "Status": "Venda registrada", "Mês": "05/2026"},
]

meses = sorted(list(set(item["Mês"] for item in dados)))
unidades = sorted(list(set(item["Unidade"] for item in dados)))

# ==================================================
# FILTROS
# ==================================================

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

# ==================================================
# FILTRO
# ==================================================

dados_filtrados = [item for item in dados if item["Mês"] == mes]

if unidade != "Todas":
    dados_filtrados = [
        item for item in dados_filtrados
        if item["Unidade"] == unidade
    ]

# ==================================================
# KPIS
# ==================================================

st.divider()

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown("""
    <div class="kpi-card">

        <div class="kpi-title">
            📌 Total de registros
        </div>

        <div class="kpi-value">
            8
        </div>

        <div class="kpi-sub">
            Mês selecionado: 05/2026
        </div>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown("""
    <div class="kpi-card kpi-red">

        <div class="kpi-title">
            ✅ Vendas registradas
        </div>

        <div class="kpi-value">
            2
        </div>

        <div class="kpi-sub">
            Contratos convertidos
        </div>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown("""
    <div class="kpi-card">

        <div class="kpi-title">
            💰 Faturamento
        </div>

        <div class="kpi-value">
            R$ 46.000
        </div>

        <div class="kpi-sub">
            Valor fictício demonstrativo
        </div>

    </div>
    """, unsafe_allow_html=True)

with c4:

    st.markdown("""
    <div class="kpi-card kpi-red">

        <div class="kpi-title">
            🎯 Ticket médio
        </div>

        <div class="kpi-value">
            R$ 5.750
        </div>

        <div class="kpi-sub">
            Média por registro
        </div>

    </div>
    """, unsafe_allow_html=True)

# ==================================================
# GRAFICOS
# ==================================================

st.divider()

g1, g2 = st.columns(2)

with g1:

    st.markdown("""
    <div class="chart-box">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chart-title">
        📞 Contatos por status
    </div>
    """, unsafe_allow_html=True)

    fig = px.bar(
        x=["1º contato", "2º contato", "3º contato", "Venda"],
        y=[1, 2, 1, 2]
    )

    fig.update_traces(
        marker_color="#1B1D6D"
    )

    fig.update_layout(
        height=340,
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title=None,
        yaxis_title=None
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with g2:

    st.markdown("""
    <div class="chart-box">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chart-title">
        🏢 Vendas por unidade
    </div>
    """, unsafe_allow_html=True)

    fig2 = px.pie(
        names=["Campinas", "Indaiatuba", "Jundiaí"],
        values=[40, 35, 25],
        hole=0.5
    )

    fig2.update_layout(
        height=340,
        paper_bgcolor="white"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# TABELA
# ==================================================

st.divider()

st.markdown("""
<div class="chart-box">
""", unsafe_allow_html=True)

st.markdown("""
<div class="chart-title">
    📄 Contratos demonstrativos
</div>
""", unsafe_allow_html=True)

st.dataframe(
    dados_filtrados,
    use_container_width=True,
    hide_index=True
)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INFO
# ==================================================

st.write("")

st.info("Este dashboard usa apenas dados fictícios para demonstração comercial.")

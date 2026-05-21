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
    max-width: 1240px;
    padding-top: 1rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* SELECTS */

div[data-testid="stSelectbox"] label {
    font-size: 14px !important;
    font-weight: 700 !important;
    color: #1f2937 !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #ffffff !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    border: none !important;
}

/* LINHA */

hr {
    border-color: rgba(15,23,42,0.15) !important;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================

def render_header():
    components.html("""
    <div style="
        width:100%;
        text-align:center;
        font-family:Arial, sans-serif;
        margin-top:8px;
        margin-bottom:18px;
    ">
        <div style="
            font-size:44px;
            font-weight:900;
            color:#09122C;
            line-height:1;
        ">
            📊 Operação Comercial
        </div>

        <div style="
            font-size:14px;
            color:#64748b;
            margin-top:12px;
        ">
            Dashboard mockup para demonstração de automações, contratos e vendas
        </div>
    </div>
    """, height=105)

# ==================================================
# LOGO
# ==================================================

def render_logo():
    components.html("""
    <div style="
        width:100%;
        display:flex;
        justify-content:center;
        align-items:center;
        font-family:Arial, sans-serif;
        padding-top:2px;
    ">
        <div style="
            background:#ffffff;
            width:92px;
            height:92px;
            border-radius:50%;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            box-shadow:0 8px 20px rgba(15,23,42,0.10);
        ">

            <div style="
                font-size:30px;
                font-weight:900;
                color:#1B1D6D;
                line-height:1;
            ">
                OPPI
            </div>

            <div style="
                font-size:10px;
                font-weight:900;
                color:#C10057;
                letter-spacing:5px;
                margin-top:6px;
            ">
                VISION
            </div>

        </div>
    </div>
    """, height=105)

# ==================================================
# CARD KPI
# ==================================================

def render_kpi(title, value, subtitle, accent):

    components.html(f"""
    <div style="
        background:#ffffff;
        border-radius:16px;
        height:122px;
        padding:18px 20px;
        box-sizing:border-box;
        border-left:7px solid {accent};
        box-shadow:0 8px 20px rgba(15,23,42,0.08);
        font-family:Arial, sans-serif;
        overflow:hidden;
    ">

        <div style="
            font-size:15px;
            font-weight:900;
            color:#111827;
            line-height:1.2;
        ">
            {title}
        </div>

        <div style="
            font-size:38px;
            font-weight:900;
            color:#020617;
            line-height:1;
            margin-top:10px;
        ">
            {value}
        </div>

        <div style="
            font-size:12px;
            color:#64748b;
            margin-top:10px;
        ">
            {subtitle}
        </div>

    </div>
    """, height=135)

# ==================================================
# HEADER
# ==================================================

render_header()

# ==================================================
# DADOS MOCKADOS
# ==================================================

dados = [
    {"Cliente": "João Mendes", "Unidade": "Campinas", "Raça": "Spitz Alemão", "Valor": 5200, "Status": "1º contato", "Mês": "01/2026"},
    {"Cliente": "Marina Costa", "Unidade": "Indaiatuba", "Raça": "Golden Retriever", "Valor": 6800, "Status": "2º contato", "Mês": "02/2026"},
    {"Cliente": "Carlos Lima", "Unidade": "Campinas", "Raça": "Maine Coon", "Valor": 6100, "Status": "3º contato", "Mês": "03/2026"},
    {"Cliente": "Fernanda Alves", "Unidade": "Jundiaí", "Raça": "Shih Tzu", "Valor": 3900, "Status": "Venda registrada", "Mês": "04/2026"},
    {"Cliente": "Rafael Souza", "Unidade": "Sorocaba", "Raça": "Bulldog Francês", "Valor": 7500, "Status": "Venda registrada", "Mês": "05/2026"},
]

# ==================================================
# MESES
# ==================================================

meses = [
    "01/2026",
    "02/2026",
    "03/2026",
    "04/2026",
    "05/2026"
]

unidades = sorted(list(set(item["Unidade"] for item in dados)))

# ==================================================
# FILTROS
# ==================================================

col_mes, col_logo, col_unidade = st.columns([5, 1.3, 5])

with col_mes:
    mes = st.selectbox("Mês", meses)

with col_logo:
    render_logo()

with col_unidade:
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

total_registros = len(dados_filtrados)

vendas = len([
    item for item in dados_filtrados
    if item["Status"] == "Venda registrada"
])

faturamento = sum(item["Valor"] for item in dados_filtrados)

ticket_medio = faturamento / total_registros if total_registros else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    render_kpi(
        "📌 Total de registros",
        str(total_registros),
        f"Mês selecionado: {mes}",
        "#1B1D6D"
    )

with c2:
    render_kpi(
        "✅ Vendas registradas",
        str(vendas),
        "Contratos convertidos",
        "#C10057"
    )

with c3:
    render_kpi(
        "💰 Faturamento",
        f"R$ {faturamento:,.0f}".replace(",", "."),
        "Valor fictício demonstrativo",
        "#1B1D6D"
    )

with c4:
    render_kpi(
        "🎯 Ticket médio",
        f"R$ {ticket_medio:,.0f}".replace(",", "."),
        "Média por registro",
        "#C10057"
    )

# ==================================================
# GRAFICOS
# ==================================================

st.divider()

g1, g2 = st.columns(2)

with g1:

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

    fig.update_traces(
        marker_color="#1B1D6D",
        textposition="outside"
    )

    fig.update_layout(
        height=360,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=20, b=30, l=10, r=10),
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

with g2:

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
        height=360,
        paper_bgcolor="white",
        margin=dict(t=20, b=30, l=10, r=10)
    )

    st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# TABELA
# ==================================================

st.divider()

st.subheader("📄 Contratos demonstrativos")

st.dataframe(
    dados_filtrados,
    use_container_width=True,
    hide_index=True
)

# ==================================================
# INFO
# ==================================================

st.info(
    "Este dashboard usa apenas dados fictícios para demonstração comercial."
)

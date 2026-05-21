import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Oppi Vision",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #D4D4D4;
}

.block-container {
    max-width: 1320px;
    padding-top: 1rem;
}

/* REMOVE HEADER */

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

/* KPI */

.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 20px;
    height: 145px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.08);
    border-left: 7px solid #1B1D6D;
}

.kpi-red {
    border-left: 7px solid #C10057;
}

.kpi-title {
    font-size: 15px;
    font-weight: 800;
    color: #111827;
    line-height: 1.2;
    font-family: Arial;
}

.kpi-value {
    font-size: 44px;
    font-weight: 900;
    color: #020617;
    line-height: 1;
    margin-top: 12px;
    font-family: Arial;
}

.kpi-sub {
    font-size: 12px;
    color: #64748b;
    margin-top: 12px;
    font-family: Arial;
}

/* BOXES */

.chart-box {
    background: white;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.08);
}

/* TITLES */

.chart-title {
    font-size: 22px;
    font-weight: 800;
    color: #1f2937;
    margin-bottom: 10px;
    font-family: Arial;
}

/* LOGO */

.logo-box {
    background:#ffffff;
    width:92px;
    height:92px;
    border-radius:50%;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    box-shadow:0 8px 20px rgba(15,23,42,0.10);
    margin:auto;
}

.logo-main {
    font-size:30px;
    font-weight:900;
    color:#1B1D6D;
    line-height:1;
    font-family:Arial;
}

.logo-sub {
    font-size:10px;
    font-weight:900;
    color:#C10057;
    letter-spacing:5px;
    margin-top:6px;
    font-family:Arial;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

components.html("""
<div style="
    width:100%;
    text-align:center;
    font-family:Arial, sans-serif;
    margin-top:8px;
    margin-bottom:18px;
">

    <div style="
        font-size:52px;
        font-weight:900;
        color:#09122C;
        line-height:1;
    ">
        📊 Operação Comercial
    </div>

    <div style="
        font-size:15px;
        color:#64748b;
        margin-top:12px;
    ">
        Dashboard comercial demonstrativo • Oppi Vision
    </div>

</div>
""", height=120)

# =========================================================
# DADOS FICTÍCIOS
# =========================================================

dados = [

    # JANEIRO
    {
        "Cliente": "Cliente 001",
        "Vendedora": "Vendedora 1",
        "Unidade": "Campinas",
        "Valor": 4200,
        "Status": "1º contato",
        "Mês": "01/2026"
    },

    {
        "Cliente": "Cliente 002",
        "Vendedora": "Vendedora 2",
        "Unidade": "Indaiatuba",
        "Valor": 6500,
        "Status": "Venda registrada",
        "Mês": "01/2026"
    },

    {
        "Cliente": "Cliente 003",
        "Vendedora": "Vendedora 3",
        "Unidade": "Jundiaí",
        "Valor": 7200,
        "Status": "2º contato",
        "Mês": "01/2026"
    },

    {
        "Cliente": "Cliente 004",
        "Vendedora": "Vendedora 1",
        "Unidade": "Sorocaba",
        "Valor": 5800,
        "Status": "Venda registrada",
        "Mês": "01/2026"
    },

    # FEVEREIRO
    {
        "Cliente": "Cliente 005",
        "Vendedora": "Vendedora 2",
        "Unidade": "Campinas",
        "Valor": 8900,
        "Status": "3º contato",
        "Mês": "02/2026"
    },

    {
        "Cliente": "Cliente 006",
        "Vendedora": "Vendedora 3",
        "Unidade": "Indaiatuba",
        "Valor": 4100,
        "Status": "Venda registrada",
        "Mês": "02/2026"
    },

    {
        "Cliente": "Cliente 007",
        "Vendedora": "Vendedora 1",
        "Unidade": "Jundiaí",
        "Valor": 5300,
        "Status": "1º contato",
        "Mês": "02/2026"
    },

    {
        "Cliente": "Cliente 008",
        "Vendedora": "Vendedora 2",
        "Unidade": "Sorocaba",
        "Valor": 9400,
        "Status": "Venda registrada",
        "Mês": "02/2026"
    },

    # MARÇO
    {
        "Cliente": "Cliente 009",
        "Vendedora": "Vendedora 3",
        "Unidade": "Campinas",
        "Valor": 7600,
        "Status": "2º contato",
        "Mês": "03/2026"
    },

    {
        "Cliente": "Cliente 010",
        "Vendedora": "Vendedora 1",
        "Unidade": "Indaiatuba",
        "Valor": 6800,
        "Status": "Venda registrada",
        "Mês": "03/2026"
    },

    {
        "Cliente": "Cliente 011",
        "Vendedora": "Vendedora 2",
        "Unidade": "Jundiaí",
        "Valor": 8100,
        "Status": "1º contato",
        "Mês": "03/2026"
    },

    {
        "Cliente": "Cliente 012",
        "Vendedora": "Vendedora 3",
        "Unidade": "Sorocaba",
        "Valor": 3700,
        "Status": "Venda registrada",
        "Mês": "03/2026"
    },

    # ABRIL
    {
        "Cliente": "Cliente 013",
        "Vendedora": "Vendedora 1",
        "Unidade": "Campinas",
        "Valor": 9100,
        "Status": "3º contato",
        "Mês": "04/2026"
    },

    {
        "Cliente": "Cliente 014",
        "Vendedora": "Vendedora 2",
        "Unidade": "Indaiatuba",
        "Valor": 6600,
        "Status": "Venda registrada",
        "Mês": "04/2026"
    },

    {
        "Cliente": "Cliente 015",
        "Vendedora": "Vendedora 3",
        "Unidade": "Jundiaí",
        "Valor": 4800,
        "Status": "2º contato",
        "Mês": "04/2026"
    },

    {
        "Cliente": "Cliente 016",
        "Vendedora": "Vendedora 1",
        "Unidade": "Sorocaba",
        "Valor": 9900,
        "Status": "Venda registrada",
        "Mês": "04/2026"
    },

    # MAIO
    {
        "Cliente": "Cliente 017",
        "Vendedora": "Vendedora 2",
        "Unidade": "Campinas",
        "Valor": 7300,
        "Status": "1º contato",
        "Mês": "05/2026"
    },

    {
        "Cliente": "Cliente 018",
        "Vendedora": "Vendedora 3",
        "Unidade": "Indaiatuba",
        "Valor": 11200,
        "Status": "Venda registrada",
        "Mês": "05/2026"
    },

    {
        "Cliente": "Cliente 019",
        "Vendedora": "Vendedora 1",
        "Unidade": "Jundiaí",
        "Valor": 5900,
        "Status": "2º contato",
        "Mês": "05/2026"
    },

    {
        "Cliente": "Cliente 020",
        "Vendedora": "Vendedora 2",
        "Unidade": "Sorocaba",
        "Valor": 8600,
        "Status": "Venda registrada",
        "Mês": "05/2026"
    }

]

df = pd.DataFrame(dados)

# =========================================================
# FILTROS
# =========================================================

meses = [
    "01/2026",
    "02/2026",
    "03/2026",
    "04/2026",
    "05/2026"
]

unidades = sorted(df["Unidade"].unique())

col_mes, col_logo, col_unidade = st.columns([5,1.2,5])

with col_mes:

    mes = st.selectbox(
        "Mês",
        meses
    )

with col_logo:

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

with col_unidade:

    unidade = st.selectbox(
        "Unidade",
        ["Todas"] + list(unidades)
    )

# =========================================================
# FILTROS DF
# =========================================================

df_filtrado = df[df["Mês"] == mes]

if unidade != "Todas":

    df_filtrado = df_filtrado[
        df_filtrado["Unidade"] == unidade
    ]

# =========================================================
# KPIS
# =========================================================

st.divider()

total_registros = len(df_filtrado)

vendas = len(
    df_filtrado[
        df_filtrado["Status"]
        .astype(str)
        .str.lower()
        .str.contains("venda")
    ]
)

faturamento = df_filtrado["Valor"].sum()

ticket = (
    faturamento / total_registros
    if total_registros > 0
    else 0
)

contato1 = len(
    df_filtrado[
        df_filtrado["Status"] == "1º contato"
    ]
)

contato2 = len(
    df_filtrado[
        df_filtrado["Status"] == "2º contato"
    ]
)

contato3 = len(
    df_filtrado[
        df_filtrado["Status"] == "3º contato"
    ]
)

# =========================================================
# CARD
# =========================================================

def kpi_card(
    title,
    value,
    subtitle,
    red=False
):

    border = "#C10057" if red else "#1B1D6D"

    st.markdown(f"""
    <div class="kpi-card"
         style="border-left:7px solid {border};">

        <div class="kpi-title">
            {title}
        </div>

        <div class="kpi-value">
            {value}
        </div>

        <div class="kpi-sub">
            {subtitle}
        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# KPI PRINCIPAL
# =========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "📌 Total de registros",
        total_registros,
        f"Leads registrados em {mes}"
    )

with c2:
    kpi_card(
        "✅ Vendas registradas",
        vendas,
        "Contratos convertidos",
        red=True
    )

with c3:
    kpi_card(
        "💰 Faturamento",
        f"R$ {faturamento:,.0f}".replace(",", "."),
        "Receita estimada do mês"
    )

with c4:
    kpi_card(
        "🎯 Ticket médio",
        f"R$ {ticket:,.0f}".replace(",", "."),
        "Média por contrato",
        red=True
    )

# =========================================================
# KPI CONTATOS
# =========================================================

st.write("")

s1, s2, s3 = st.columns(3)

with s1:
    kpi_card(
        "📞 1º contato",
        contato1,
        "Leads em primeiro atendimento"
    )

with s2:
    kpi_card(
        "📲 2º contato",
        contato2,
        "Leads em negociação",
        red=True
    )

with s3:
    kpi_card(
        "🧾 3º contato",
        contato3,
        "Leads em fechamento"
    )

# =========================================================
# GRAFICOS
# =========================================================

st.divider()

g1, g2 = st.columns(2)

# =========================================================
# GRAFICO STATUS
# =========================================================

with g1:

    st.markdown("""
    <div class="chart-box">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chart-title">
        📞 Contatos por status
    </div>
    """, unsafe_allow_html=True)

    status_df = (
        df_filtrado
        .groupby("Status")
        .size()
        .reset_index(name="Quantidade")
    )

    fig = px.bar(
        status_df,
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
        margin=dict(t=20,b=20,l=10,r=10),
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# GRAFICO UNIDADE
# =========================================================

with g2:

    st.markdown("""
    <div class="chart-box">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chart-title">
        🏢 Vendas por unidade
    </div>
    """, unsafe_allow_html=True)

    unidade_df = (
        df_filtrado
        .groupby("Unidade")["Valor"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        unidade_df,
        names="Unidade",
        values="Valor",
        hole=0.55
    )

    fig2.update_layout(
        height=360,
        paper_bgcolor="white",
        margin=dict(t=20,b=20,l=10,r=10)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TABELA
# =========================================================

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
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# INFO
# =========================================================

st.write("")

st.info(
    "Este dashboard utiliza dados fictícios para apresentação comercial da solução Oppi Vision."
)

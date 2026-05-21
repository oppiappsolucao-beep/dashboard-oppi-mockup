import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd

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

header[data-testid="stHeader"] {
    background: transparent;
}

/* SELECT */

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

# ==================================================
# HEADER
# ==================================================

components.html("""
<div style="
    width:100%;
    text-align:center;
    font-family:Arial, sans-serif;
    margin-top:8px;
    margin-bottom:18px;
">
    <div style="
        font-size:46px;
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
""", height=110)

# ==================================================
# DADOS COMPLETOS
# ==================================================

dados = [

    # JANEIRO
    {"Cliente":"João Mendes","Unidade":"Campinas","Valor":4200,"Status":"1º contato","Mês":"01/2026"},
    {"Cliente":"Marina Costa","Unidade":"Indaiatuba","Valor":6500,"Status":"Venda registrada","Mês":"01/2026"},
    {"Cliente":"Carlos Lima","Unidade":"Campinas","Valor":7200,"Status":"2º contato","Mês":"01/2026"},
    {"Cliente":"Fernanda Alves","Unidade":"Jundiaí","Valor":5800,"Status":"Venda registrada","Mês":"01/2026"},
    {"Cliente":"Rafael Souza","Unidade":"Sorocaba","Valor":3100,"Status":"3º contato","Mês":"01/2026"},
    {"Cliente":"Lucas Martins","Unidade":"Campinas","Valor":8700,"Status":"1º contato","Mês":"01/2026"},

    # FEVEREIRO
    {"Cliente":"Patrícia Rocha","Unidade":"Campinas","Valor":5500,"Status":"Venda registrada","Mês":"02/2026"},
    {"Cliente":"Ricardo Gomes","Unidade":"Indaiatuba","Valor":6100,"Status":"2º contato","Mês":"02/2026"},
    {"Cliente":"Juliana Prado","Unidade":"Jundiaí","Valor":4500,"Status":"Venda registrada","Mês":"02/2026"},
    {"Cliente":"Thiago Lopes","Unidade":"Sorocaba","Valor":7800,"Status":"1º contato","Mês":"02/2026"},
    {"Cliente":"Amanda Nunes","Unidade":"Campinas","Valor":9000,"Status":"3º contato","Mês":"02/2026"},

    # MARÇO
    {"Cliente":"Bruno Almeida","Unidade":"Campinas","Valor":4900,"Status":"Venda registrada","Mês":"03/2026"},
    {"Cliente":"Camila Freitas","Unidade":"Indaiatuba","Valor":8700,"Status":"Venda registrada","Mês":"03/2026"},
    {"Cliente":"Felipe Moraes","Unidade":"Jundiaí","Valor":3900,"Status":"2º contato","Mês":"03/2026"},
    {"Cliente":"Larissa Dias","Unidade":"Sorocaba","Valor":6100,"Status":"1º contato","Mês":"03/2026"},
    {"Cliente":"Gabriel Silva","Unidade":"Campinas","Valor":7200,"Status":"3º contato","Mês":"03/2026"},
    {"Cliente":"Mayara Costa","Unidade":"Campinas","Valor":8300,"Status":"Venda registrada","Mês":"03/2026"},

    # ABRIL
    {"Cliente":"Pedro Henrique","Unidade":"Campinas","Valor":6700,"Status":"Venda registrada","Mês":"04/2026"},
    {"Cliente":"Bianca Souza","Unidade":"Indaiatuba","Valor":5400,"Status":"1º contato","Mês":"04/2026"},
    {"Cliente":"Rafaela Lima","Unidade":"Jundiaí","Valor":9500,"Status":"Venda registrada","Mês":"04/2026"},
    {"Cliente":"Mateus Oliveira","Unidade":"Sorocaba","Valor":4800,"Status":"2º contato","Mês":"04/2026"},
    {"Cliente":"Daniel Martins","Unidade":"Campinas","Valor":6100,"Status":"3º contato","Mês":"04/2026"},

    # MAIO
    {"Cliente":"João Pedro","Unidade":"Campinas","Valor":8800,"Status":"Venda registrada","Mês":"05/2026"},
    {"Cliente":"Nicole Freitas","Unidade":"Indaiatuba","Valor":7400,"Status":"Venda registrada","Mês":"05/2026"},
    {"Cliente":"Vinicius Rocha","Unidade":"Jundiaí","Valor":6900,"Status":"2º contato","Mês":"05/2026"},
    {"Cliente":"Amanda Silva","Unidade":"Sorocaba","Valor":5700,"Status":"1º contato","Mês":"05/2026"},
    {"Cliente":"Leonardo Alves","Unidade":"Campinas","Valor":9900,"Status":"Venda registrada","Mês":"05/2026"},
    {"Cliente":"Larissa Mendes","Unidade":"Campinas","Valor":4500,"Status":"3º contato","Mês":"05/2026"},
]

df = pd.DataFrame(dados)

# ==================================================
# FILTROS
# ==================================================

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
    mes = st.selectbox("Mês", meses)

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
    unidade = st.selectbox("Unidade", ["Todas"] + list(unidades))

# ==================================================
# FILTROS DF
# ==================================================

df_filtrado = df[df["Mês"] == mes]

if unidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Unidade"] == unidade]

# ==================================================
# KPIS
# ==================================================

st.divider()

total_registros = len(df_filtrado)

vendas = len(
    df_filtrado[df_filtrado["Status"] == "Venda registrada"]
)

faturamento = df_filtrado["Valor"].sum()

ticket = faturamento / total_registros if total_registros > 0 else 0

contato1 = len(df_filtrado[df_filtrado["Status"] == "1º contato"])
contato2 = len(df_filtrado[df_filtrado["Status"] == "2º contato"])
contato3 = len(df_filtrado[df_filtrado["Status"] == "3º contato"])

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-title">
            📌 Total de registros
        </div>

        <div class="kpi-value">
            {total_registros}
        </div>

        <div class="kpi-sub">
            Leads registrados em {mes}
        </div>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="kpi-card kpi-red">

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
    <div class="kpi-card">

        <div class="kpi-title">
            💰 Faturamento
        </div>

        <div class="kpi-value">
            R$ {faturamento:,.0f}
        </div>

        <div class="kpi-sub">
            Receita estimada do mês
        </div>

    </div>
    """.replace(",", "."), unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="kpi-card kpi-red">

        <div class="kpi-title">
            🎯 Ticket médio
        </div>

        <div class="kpi-value">
            R$ {ticket:,.0f}
        </div>

        <div class="kpi-sub">
            Média por contrato
        </div>

    </div>
    """.replace(",", "."), unsafe_allow_html=True)

# ==================================================
# KPIS STATUS
# ==================================================

st.write("")

s1, s2, s3 = st.columns(3)

with s1:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-title">
            📞 1º contato
        </div>

        <div class="kpi-value">
            {contato1}
        </div>

        <div class="kpi-sub">
            Leads em primeiro atendimento
        </div>

    </div>
    """, unsafe_allow_html=True)

with s2:

    st.markdown(f"""
    <div class="kpi-card kpi-red">

        <div class="kpi-title">
            📲 2º contato
        </div>

        <div class="kpi-value">
            {contato2}
        </div>

        <div class="kpi-sub">
            Leads em negociação
        </div>

    </div>
    """, unsafe_allow_html=True)

with s3:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-title">
            🧾 3º contato
        </div>

        <div class="kpi-value">
            {contato3}
        </div>

        <div class="kpi-sub">
            Leads em fechamento
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
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# INFO
# ==================================================

st.write("")

st.info(
    "Este dashboard utiliza dados fictícios para apresentação comercial da solução Oppi Vision."
)

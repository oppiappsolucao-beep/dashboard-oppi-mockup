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
# CONFIG GOOGLE SHEETS CSV
# =========================================================

CSV_URL = "COLE_AQUI_O_LINK_CSV_DA_PLANILHA"

# EXEMPLO:
# CSV_URL = "https://docs.google.com/spreadsheets/d/ID/gviz/tq?tqx=out:csv&gid=0"

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
        Dashboard comercial demonstrativo • Oppi Vision
    </div>

</div>
""", height=110)

# =========================================================
# LEITURA PLANILHA
# =========================================================

@st.cache_data(ttl=60)
def carregar_dados():

    df = pd.read_csv(CSV_URL)

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    # AJUSTE COLUNAS

    if "Valor" in df.columns:

        df["Valor"] = (
            df["Valor"]
            .astype(str)
            .str.replace("R$", "")
            .str.replace(".", "")
            .str.replace(",", ".")
        )

        df["Valor"] = pd.to_numeric(
            df["Valor"],
            errors="coerce"
        ).fillna(0)

    else:
        df["Valor"] = 0

    if "Mês" not in df.columns:
        df["Mês"] = "05/2026"

    if "Status" not in df.columns:
        df["Status"] = "1º contato"

    return df

try:

    df = carregar_dados()

except:

    st.error("Erro ao carregar a planilha.")
    st.stop()

# =========================================================
# FILTROS
# =========================================================

meses = sorted(df["Mês"].dropna().unique())

unidades = sorted(
    df["Unidade"].dropna().unique()
) if "Unidade" in df.columns else []

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
# KPIS HTML
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
# STATUS
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

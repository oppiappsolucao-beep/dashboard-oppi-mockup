import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONFIG
# =========================================================

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
    background: #d9d9d9;
}

/* REMOVE HEADER */

header[data-testid="stHeader"] {
    background: transparent;
}

/* CENTRALIZA */

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
}

/* SELECT */

div[data-testid="stSelectbox"] label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #3d3d3d !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: white !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    border: none !important;
}

/* KPI */

.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    min-height: 95px;
    border-left: 6px solid #1f237e;
}

.kpi-red {
    border-left: 6px solid #c00057;
}

.kpi-title {
    font-size: 12px;
    font-weight: 700;
    color: #1d1d1d;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 22px;
    font-weight: 900;
    color: #020617;
    line-height: 1;
}

.kpi-sub {
    font-size: 10px;
    color: #6b7280;
    margin-top: 8px;
}

/* BOXES */

.box-chart {
    background: white;
    border-radius: 14px;
    padding: 10px 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* TITLES */

.chart-title {
    font-size: 13px;
    font-weight: 800;
    color: #1f2937;
    margin-bottom: 0px;
}

.chart-sub {
    font-size: 10px;
    color: #6b7280;
    margin-bottom: 8px;
}

/* LOGO */

.logo-circle {
    width: 74px;
    height: 74px;
    border-radius: 50%;
    background: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.logo-main {
    font-size: 25px;
    font-weight: 900;
    color: #1B1D6D;
    line-height: 1;
}

.logo-sub {
    font-size: 9px;
    font-weight: 800;
    color: #c00057;
    letter-spacing: 4px;
    margin-top: 4px;
}

hr {
    border-color: rgba(0,0,0,0.10) !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DADOS MOCKADOS
# =========================================================

dados = [

    ["05/2026","Cliente 001","Vendedora 1","Campinas","1º contato",4200,"Spitz Alemão"],
    ["05/2026","Cliente 002","Vendedora 2","Campinas","2º contato",6800,"Maltês"],
    ["05/2026","Cliente 003","Vendedora 3","Campinas","3º contato",9100,"Shih Tzu"],
    ["05/2026","Cliente 004","Vendedora 1","Indaiatuba","Venda registrada",12000,"Maine Coon"],
    ["05/2026","Cliente 005","Vendedora 2","Indaiatuba","Venda registrada",8500,"Teckel"],
    ["05/2026","Cliente 006","Vendedora 3","Piracicaba","1º contato",4900,"Chihuahua"],
    ["05/2026","Cliente 007","Vendedora 1","Piracicaba","2º contato",7200,"Spitz Alemão"],
    ["05/2026","Cliente 008","Vendedora 2","Campinas","Venda registrada",9400,"Maltês"],

    ["04/2026","Cliente 009","Vendedora 1","Campinas","1º contato",5100,"Shih Tzu"],
    ["04/2026","Cliente 010","Vendedora 2","Indaiatuba","Venda registrada",11000,"Maine Coon"],
    ["04/2026","Cliente 011","Vendedora 3","Piracicaba","2º contato",4300,"Teckel"],

    ["03/2026","Cliente 012","Vendedora 1","Campinas","3º contato",7800,"Spitz Alemão"],
    ["03/2026","Cliente 013","Vendedora 2","Indaiatuba","Venda registrada",10200,"Maltês"],

]

df = pd.DataFrame(
    dados,
    columns=[
        "Mês",
        "Cliente",
        "Vendedora",
        "Unidade",
        "Status",
        "Valor",
        "Raça"
    ]
)

# =========================================================
# HEADER
# =========================================================

top1, top2, top3 = st.columns([1,8,1])

with top1:
    st.markdown("☰")

with top2:

    st.markdown("""
    <div style='display:flex;align-items:center;gap:14px;'>

        <div style='font-size:34px;'>⚙️</div>

        <div>
            <div style='font-size:28px;font-weight:800;color:#1f2937;'>
                Operação
            </div>

            <div style='font-size:11px;color:#6b7280;margin-top:4px;'>
                Total de registros: 308
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

with top3:
    st.button("Sair")

st.write("")

# =========================================================
# FILTROS
# =========================================================

meses = sorted(df["Mês"].unique(), reverse=True)
unidades = sorted(df["Unidade"].unique())

f1, logo, f2 = st.columns([5,1,5])

with f1:
    mes = st.selectbox("Mês", meses)

with logo:

    st.markdown("""
    <div class='logo-circle'>

        <div class='logo-main'>
            OPPI
        </div>

        <div class='logo-sub'>
            VISION
        </div>

    </div>
    """, unsafe_allow_html=True)

with f2:
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
# KPI
# =========================================================

contato1 = len(df_filtrado[df_filtrado["Status"] == "1º contato"])
contato2 = len(df_filtrado[df_filtrado["Status"] == "2º contato"])
contato3 = len(df_filtrado[df_filtrado["Status"] == "3º contato"])

primeiro_mes = contato1 + 35
segundo_mes = contato2 + 47
terceiro_mes = contato3 + 57

# =========================================================
# CARD
# =========================================================

def card(title, value, sub, red=False):

    classe = "kpi-red" if red else ""

    st.markdown(f"""
    <div class='kpi-card {classe}'>

        <div class='kpi-title'>
            {title}
        </div>

        <div class='kpi-value'>
            {value}
        </div>

        <div class='kpi-sub'>
            {sub}
        </div>

    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# KPIS LINHA 1
# =========================================================

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    card(
        "💬 1º contato hoje",
        contato1,
        "registros de hoje"
    )

with c2:
    card(
        "💬 2º contato hoje",
        contato2,
        "registros de hoje"
    )

with c3:
    card(
        "💬 3º contato hoje",
        contato3,
        "registros de hoje",
        True
    )

with c4:
    card(
        "🧾 Primeiro Contato Mês",
        primeiro_mes,
        mes
    )

with c5:
    card(
        "🧾 Segundo Contato Mês",
        segundo_mes,
        mes,
        True
    )

with c6:
    card(
        "🧾 Terceiro Contato Mês",
        terceiro_mes,
        mes,
        True
    )

st.write("")

# =========================================================
# KPI GRANDES
# =========================================================

g1,g2 = st.columns(2)

with g1:

    st.markdown("""
    <div class='kpi-card kpi-red' style='min-height:110px;'>

        <div class='kpi-title'>
            Status com erro
        </div>

        <div class='kpi-value'>
            0
        </div>

        <div class='kpi-sub'>
            Mês selecionado
        </div>

    </div>
    """, unsafe_allow_html=True)

with g2:

    vendas_mes = len(
        df_filtrado[
            df_filtrado["Status"] == "Venda registrada"
        ]
    )

    st.markdown(f"""
    <div class='kpi-card' style='min-height:110px;'>

        <div class='kpi-title'>
            Vendas registradas no mês
        </div>

        <div class='kpi-value'>
            {vendas_mes}
        </div>

        <div class='kpi-sub'>
            Mês Venda: {mes}
        </div>

    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# GRAFICOS
# =========================================================

gr1, gr2 = st.columns(2)

# =========================================================
# CONTATOS POR MES
# =========================================================

with gr1:

    st.markdown("""
    <div class='box-chart'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='chart-title'>
        📞 Contatos por mês
    </div>

    <div class='chart-sub'>
        Distribuição mensal dos 3 contatos
    </div>
    """, unsafe_allow_html=True)

    contatos_df = pd.DataFrame({
        "Contato": ["1º contato","2º contato","3º contato"],
        "Quantidade": [36,49,57]
    })

    fig = px.bar(
        contatos_df,
        x="Contato",
        y="Quantidade",
        text="Quantidade"
    )

    fig.update_traces(
        marker_color=["#262680","#c00057","#3b3ba8"],
        textposition="outside"
    )

    fig.update_layout(
        height=300,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=10,b=10,l=10,r=10),
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
# VENDAS UNIDADE
# =========================================================

with gr2:

    st.markdown("""
    <div class='box-chart'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='chart-title'>
        🏢 Vendas por unidade no mês
    </div>

    <div class='chart-sub'>
        Quantidade de vendas registradas
    </div>
    """, unsafe_allow_html=True)

    unidade_df = pd.DataFrame({
        "Unidade": ["Campinas","Indaiatuba","Piracicaba"],
        "Quantidade": [15,10,9]
    })

    fig2 = px.bar(
        unidade_df,
        x="Unidade",
        y="Quantidade",
        text="Quantidade"
    )

    fig2.update_traces(
        marker_color=["#262680","#c00057","#3b3ba8"],
        textposition="outside"
    )

    fig2.update_layout(
        height=300,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=10,b=10,l=10,r=10),
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# GRAFICOS 2
# =========================================================

st.write("")

gr3, gr4 = st.columns(2)

# =========================================================
# RAÇAS
# =========================================================

with gr3:

    st.markdown("""
    <div class='box-chart'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='chart-title'>
        🐶 Raças mais vendidas (mês)
    </div>

    <div class='chart-sub'>
        Top 10 raças do mês filtrado
    </div>
    """, unsafe_allow_html=True)

    racas_df = pd.DataFrame({
        "Raça": [
            "SPITZ ALEMÃO",
            "MALTÊS",
            "SHIH TZU",
            "MAINE COON",
            "TECKEL",
            "CHIHUAHUA"
        ],
        "Quantidade": [11,7,6,5,4,3]
    })

    fig3 = px.bar(
        racas_df,
        x="Raça",
        y="Quantidade",
        text="Quantidade"
    )

    fig3.update_traces(
        marker_color=[
            "#262680",
            "#c00057",
            "#3b3ba8",
            "#d40064",
            "#44516f",
            "#94a3b8"
        ],
        textposition="outside"
    )

    fig3.update_layout(
        height=320,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=10,b=10,l=10,r=10),
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# VENDEDORAS
# =========================================================

with gr4:

    st.markdown("""
    <div class='box-chart'>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='chart-title'>
        🏆 Vendas por vendedora (mês)
    </div>

    <div class='chart-sub'>
        Todas as vendas do mês
    </div>
    """, unsafe_allow_html=True)

    vend_df = pd.DataFrame({
        "Vendedora": [
            "Vendedora 1",
            "Vendedora 2",
            "Vendedora 3",
            "Vendedora 4"
        ],
        "Quantidade": [8,6,4,2]
    })

    fig4 = px.bar(
        vend_df,
        x="Vendedora",
        y="Quantidade",
        text="Quantidade"
    )

    fig4.update_traces(
        marker_color=[
            "#262680",
            "#c00057",
            "#3b3ba8",
            "#44516f"
        ],
        textposition="outside"
    )

    fig4.update_layout(
        height=320,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=10,b=10,l=10,r=10),
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# INFO
# =========================================================

st.write("")

st.info(
    "Dashboard demonstrativo Oppi Vision • Dados 100% fictícios."
)

import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

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

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

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

hr {
    border-color: rgba(0,0,0,0.10) !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# COMPONENT HTML
# =========================================================

def html_box(html, height):
    components.html(html, height=height)

# =========================================================
# KPI CARD
# =========================================================

def kpi_card(title, value, subtitle, red=False, height=112):
    border = "#c00057" if red else "#1f237e"

    html_box(f"""
    <div style="
        background:white;
        border-radius:14px;
        padding:14px 16px;
        min-height:95px;
        border-left:6px solid {border};
        box-shadow:0 2px 8px rgba(0,0,0,0.06);
        font-family:Arial, sans-serif;
    ">
        <div style="font-size:12px;font-weight:800;color:#1d1d1d;">
            {title}
        </div>

        <div style="font-size:34px;font-weight:900;color:#020617;margin-top:5px;">
            {value}
        </div>

        <div style="font-size:10px;color:#6b7280;margin-top:8px;">
            {subtitle}
        </div>
    </div>
    """, height)

# =========================================================
# HEADER SIMPLES
# =========================================================

top1, top2, top3 = st.columns([1, 8, 1])

with top2:
    st.markdown("""
    <h1 style='text-align:center;margin-bottom:0;'>📊 Operação Comercial</h1>
    <p style='text-align:center;color:#6b7280;margin-top:5px;'>
    Dashboard comercial demonstrativo • Oppi Vision
    </p>
    """, unsafe_allow_html=True)

# =========================================================
# DADOS MOCK
# =========================================================

dados = [
    ["05/2026","Cliente 001","Vendedora 1","Campinas","1º contato",4200],
    ["05/2026","Cliente 002","Vendedora 2","Campinas","2º contato",6800],
    ["05/2026","Cliente 003","Vendedora 3","Campinas","3º contato",9100],
    ["04/2026","Cliente 004","Vendedora 1","Indaiatuba","Venda registrada",12000],
    ["04/2026","Cliente 005","Vendedora 2","Indaiatuba","Venda registrada",8500],
    ["03/2026","Cliente 006","Vendedora 3","Piracicaba","1º contato",4900],
    ["02/2026","Cliente 007","Vendedora 1","Piracicaba","2º contato",7200],
    ["01/2026","Cliente 008","Vendedora 2","Campinas","Venda registrada",9400],
]

df = pd.DataFrame(
    dados,
    columns=["Mês","Cliente","Vendedora","Unidade","Status","Valor"]
)

# =========================================================
# ORDEM CORRETA DOS MESES (CRESCENTE)
# =========================================================

meses = sorted(
    df["Mês"].unique(),
    key=lambda x: (int(x.split("/")[1]), int(x.split("/")[0]))
)

unidades = sorted(df["Unidade"].unique())

# =========================================================
# FILTROS
# =========================================================

c1, c2, c3 = st.columns([5,1,5])

with c1:
    mes = st.selectbox("Mês", meses)

with c2:
    st.markdown("""
    <div style='text-align:center;'>
        <div style='font-weight:900;color:#1f237e;'>OPPI</div>
        <div style='font-size:10px;color:#c00057;letter-spacing:4px;'>VISION</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

# =========================================================
# FILTRO
# =========================================================

df_filtrado = df[df["Mês"] == mes]

if unidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Unidade"] == unidade]

# =========================================================
# KPIS
# =========================================================

total = len(df_filtrado)
vendas = len(df_filtrado[df_filtrado["Status"] == "Venda registrada"])
faturamento = df_filtrado["Valor"].sum()
ticket = faturamento / total if total else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Total registros", total, f"Mês {mes}")

with c2:
    kpi_card("Vendas", vendas, "Conversões")

with c3:
    kpi_card("Faturamento", f"R$ {faturamento:,.0f}".replace(",", "."), "Receita")

with c4:
    kpi_card("Ticket médio", f"R$ {ticket:,.0f}".replace(",", "."), "Média")

# =========================================================
# GRAFICO
# =========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Contatos")
    fig = px.bar(df_filtrado, x="Status", y="Valor", color="Status")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Vendas por unidade")
    fig2 = px.pie(df_filtrado, names="Unidade", values="Valor")
    st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# TABELA
# =========================================================

st.subheader("Dados")
st.dataframe(df_filtrado, use_container_width=True)

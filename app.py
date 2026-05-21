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
# CSS (ESTILO SKOOB LIKE)
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #d9d9d9;
}

.block-container {
    max-width: 1500px;
    padding-top: 20px;
}

/* REMOVE HEADER STREAMLIT */
header {
    visibility: hidden;
}

/* KPI CARD */
.kpi {
    background: white;
    border-radius: 14px;
    padding: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
    border-left: 6px solid #1f237e;
}

.kpi-red {
    border-left: 6px solid #c00057;
}

.kpi-title {
    font-size: 13px;
    font-weight: 700;
    color: #111;
}

.kpi-value {
    font-size: 30px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 5px;
}

.kpi-sub {
    font-size: 11px;
    color: #6b7280;
    margin-top: 5px;
}

/* BOX */
.box {
    background: white;
    padding: 15px;
    border-radius: 14px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

/* TITLES */
.title {
    font-size: 16px;
    font-weight: 800;
    color: #111827;
}

/* SELECT */
div[data-testid="stSelectbox"] > div {
    background: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DADOS FAKE
# =========================================================

dados = [
    ["01/2026","Cliente 01","Vendedora 1","Campinas","1º contato",4200],
    ["02/2026","Cliente 02","Vendedora 2","Indaiatuba","2º contato",6800],
    ["03/2026","Cliente 03","Vendedora 3","Piracicaba","3º contato",9100],
    ["04/2026","Cliente 04","Vendedora 1","Campinas","Venda registrada",12000],
    ["05/2026","Cliente 05","Vendedora 2","Indaiatuba","Venda registrada",8500],
    ["05/2026","Cliente 06","Vendedora 3","Piracicaba","1º contato",4900],
    ["04/2026","Cliente 07","Vendedora 1","Piracicaba","2º contato",7200],
    ["03/2026","Cliente 08","Vendedora 2","Campinas","Venda registrada",9400],
    ["02/2026","Cliente 09","Vendedora 3","Indaiatuba","3º contato",6600],
    ["01/2026","Cliente 10","Vendedora 1","Campinas","Venda registrada",10200],
]

df = pd.DataFrame(dados, columns=[
    "Mês","Cliente","Vendedora","Unidade","Status","Valor"
])

# =========================================================
# ORDEM DOS MESES (CORRETO 01 → 05)
# =========================================================

meses = sorted(
    df["Mês"].unique(),
    key=lambda x: (int(x.split("/")[1]), int(x.split("/")[0]))
)

unidades = sorted(df["Unidade"].unique())

# =========================================================
# HEADER
# =========================================================

col1, col2, col3 = st.columns([1,6,1])

with col2:
    st.markdown("""
    <div style='text-align:center'>
        <div style='font-size:28px;font-weight:900;'>📊 Operação Comercial</div>
        <div style='font-size:12px;color:#6b7280;'>Dashboard comercial demonstrativo • Oppi Vision</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FILTROS
# =========================================================

c1, c2, c3 = st.columns([5,1,5])

with c1:
    mes = st.selectbox("Mês", meses)

with c2:
    st.markdown("""
    <div style='text-align:center;font-weight:900;color:#1f237e;'>
        OPPI<br>
        <span style='font-size:10px;color:#c00057;'>VISION</span>
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
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Total de registros</div>
        <div class="kpi-value">{total}</div>
        <div class="kpi-sub">{mes}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi kpi-red">
        <div class="kpi-title">Vendas registradas</div>
        <div class="kpi-value">{vendas}</div>
        <div class="kpi-sub">Conversões</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-title">Faturamento</div>
        <div class="kpi-value">R$ {faturamento:,.0f}</div>
        <div class="kpi-sub">Receita total</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi kpi-red">
        <div class="kpi-title">Ticket médio</div>
        <div class="kpi-value">R$ {ticket:,.0f}</div>
        <div class="kpi-sub">Média por venda</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# GRAFICOS (ESTILO SKOOB)
# =========================================================

st.write("")

g1, g2 = st.columns(2)

with g1:
    st.markdown("<div class='box'><div class='title'>Contatos por status</div>", unsafe_allow_html=True)

    fig = px.bar(
        df_filtrado.groupby("Status").size().reset_index(name="Qtd"),
        x="Status",
        y="Qtd",
        text="Qtd"
    )

    fig.update_traces(marker_color="#1f237e")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with g2:
    st.markdown("<div class='box'><div class='title'>Vendas por unidade</div>", unsafe_allow_html=True)

    fig2 = px.pie(
        df_filtrado.groupby("Unidade")["Valor"].sum().reset_index(),
        names="Unidade",
        values="Valor"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TABELA
# =========================================================

st.write("")

st.markdown("<div class='box'><div class='title'>Contratos demonstrativos</div>", unsafe_allow_html=True)

st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)

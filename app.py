import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Oppi Mockup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

NAVY = "#1B1D6D"
WINE = "#9B0033"
BG = "#D4D4D4"

st.markdown("""
<style>
.stApp {
    background: #D4D4D4;
}
.block-container {
    padding-top: 2rem;
    max-width: 1180px;
}
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 22px rgba(15,23,42,.08);
    border-left: 7px solid #1B1D6D;
}
.card-red {
    border-left: 7px solid #9B0033;
}
.kpi-title {
    font-size: 14px;
    font-weight: 800;
    color: #334155;
}
.kpi-value {
    font-size: 40px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1;
    margin-top: 8px;
}
.kpi-sub {
    font-size: 12px;
    color: #64748b;
    margin-top: 10px;
}
.header-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}
.title {
    font-size: 34px;
    font-weight: 900;
    color: #0f172a;
}
.subtitle {
    color: #64748b;
    font-size: 14px;
    margin-top: 4px;
}
.badge {
    background: white;
    padding: 12px 18px;
    border-radius: 14px;
    font-weight: 800;
    color: #1B1D6D;
    box-shadow: 0 8px 20px rgba(15,23,42,.08);
}
</style>
""", unsafe_allow_html=True)

dados = [
    ["João Mendes", "Campinas", "Spitz Alemão", 5200, "1º contato", "05/2026"],
    ["Marina Costa", "Indaiatuba", "Golden Retriever", 6800, "2º contato", "05/2026"],
    ["Carlos Lima", "Campinas", "Maine Coon", 6100, "3º contato", "05/2026"],
    ["Fernanda Alves", "Jundiaí", "Shih Tzu", 3900, "Venda registrada", "05/2026"],
    ["Rafael Souza", "Sorocaba", "Bulldog Francês", 7500, "Venda registrada", "05/2026"],
    ["Patrícia Rocha", "Campinas", "Poodle Toy", 4300, "Primeiro contato mês", "05/2026"],
    ["Lucas Martins", "Indaiatuba", "Spitz Alemão", 5800, "Segundo contato mês", "05/2026"],
    ["Aline Ferreira", "Jundiaí", "Border Collie", 6400, "Terceiro contato mês", "05/2026"],
]

df = pd.DataFrame(
    dados,
    columns=["Cliente", "Unidade", "Raça", "Valor", "Status", "Mês"]
)

st.markdown("""
<div class="header-box">
    <div>
        <div class="title">📊 Operação Comercial</div>
        <div class="subtitle">Dashboard mockup para demonstração de automações, contratos e vendas</div>
    </div>
    <div class="badge">Oppi Tech</div>
</div>
""", unsafe_allow_html=True)

col_f1, col_f2 = st.columns(2)

with col_f1:
    mes = st.selectbox("Mês", sorted(df["Mês"].unique()))

with col_f2:
    unidade = st.selectbox("Unidade", ["Todas"] + sorted(df["Unidade"].unique()))

df_filtrado = df[df["Mês"] == mes]

if unidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Unidade"] == unidade]

st.divider()

total_registros = len(df_filtrado)
vendas = len(df_filtrado[df_filtrado["Status"] == "Venda registrada"])
faturamento = df_filtrado["Valor"].sum()
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
    """.replace(",", "."), unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card card-red">
        <div class="kpi-title">🎯 Ticket médio</div>
        <div class="kpi-value">R$ {ticket_medio:,.0f}</div>
        <div class="kpi-sub">Média por registro</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

st.divider()

g1, g2 = st.columns(2)

with g1:
    st.subheader("📞 Contatos por status")
    status_df = df_filtrado.groupby("Status", as_index=False).size()
    status_df.columns = ["Status", "Quantidade"]
    fig = px.bar(
        status_df,
        x="Status",
        y="Quantidade",
        text="Quantidade"
    )
    fig.update_layout(
        height=380,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=20, b=30, l=10, r=10)
    )
    st.plotly_chart(fig, use_container_width=True)

with g2:
    st.subheader("🏢 Vendas por unidade")
    unidade_df = df_filtrado.groupby("Unidade", as_index=False)["Valor"].sum()
    fig2 = px.pie(
        unidade_df,
        names="Unidade",
        values="Valor",
        hole=0.45
    )
    fig2.update_layout(
        height=380,
        paper_bgcolor="white",
        margin=dict(t=20, b=30, l=10, r=10)
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("📄 Contratos demonstrativos")
st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

st.info("Este dashboard usa apenas dados fictícios para demonstração comercial.")

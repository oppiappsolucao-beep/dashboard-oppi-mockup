import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Oppi Vision",
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
    max-width: 1280px;
    padding-top: 1.2rem;
}
[data-testid="stMetricValue"] {
    font-size: 38px;
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1 style='text-align:center; color:#09122C;'>📊 Operação Comercial</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:#64748b;'>Dashboard comercial demonstrativo • Oppi Vision</p>",
    unsafe_allow_html=True
)

dados = [
    ["01/2026", "Cliente 001", "Vendedora 1", "Campinas", "1º contato", 5200],
    ["01/2026", "Cliente 002", "Vendedora 2", "Indaiatuba", "Venda registrada", 7400],
    ["01/2026", "Cliente 003", "Vendedora 3", "Jundiaí", "2º contato", 6100],
    ["01/2026", "Cliente 004", "Vendedora 1", "Sorocaba", "Venda registrada", 9800],

    ["02/2026", "Cliente 005", "Vendedora 2", "Campinas", "3º contato", 4700],
    ["02/2026", "Cliente 006", "Vendedora 3", "Indaiatuba", "Venda registrada", 8600],
    ["02/2026", "Cliente 007", "Vendedora 1", "Jundiaí", "1º contato", 3900],
    ["02/2026", "Cliente 008", "Vendedora 2", "Sorocaba", "Venda registrada", 9100],
    ["02/2026", "Cliente 009", "Vendedora 4", "Campinas", "2º contato", 7300],

    ["03/2026", "Cliente 010", "Vendedora 3", "Campinas", "2º contato", 8200],
    ["03/2026", "Cliente 011", "Vendedora 1", "Indaiatuba", "Venda registrada", 7700],
    ["03/2026", "Cliente 012", "Vendedora 2", "Jundiaí", "1º contato", 6200],
    ["03/2026", "Cliente 013", "Vendedora 3", "Sorocaba", "Venda registrada", 5400],
    ["03/2026", "Cliente 014", "Vendedora 4", "Campinas", "3º contato", 9900],
    ["03/2026", "Cliente 015", "Vendedora 1", "Indaiatuba", "Venda registrada", 8800],

    ["04/2026", "Cliente 016", "Vendedora 1", "Campinas", "3º contato", 10200],
    ["04/2026", "Cliente 017", "Vendedora 2", "Indaiatuba", "Venda registrada", 6900],
    ["04/2026", "Cliente 018", "Vendedora 3", "Jundiaí", "2º contato", 4300],
    ["04/2026", "Cliente 019", "Vendedora 1", "Sorocaba", "Venda registrada", 8700],
    ["04/2026", "Cliente 020", "Vendedora 4", "Campinas", "1º contato", 7600],

    ["05/2026", "Cliente 021", "Vendedora 2", "Campinas", "1º contato", 5900],
    ["05/2026", "Cliente 022", "Vendedora 3", "Indaiatuba", "Venda registrada", 11300],
    ["05/2026", "Cliente 023", "Vendedora 1", "Jundiaí", "2º contato", 6800],
    ["05/2026", "Cliente 024", "Vendedora 2", "Sorocaba", "Venda registrada", 9200],
    ["05/2026", "Cliente 025", "Vendedora 4", "Campinas", "3º contato", 7200],
    ["05/2026", "Cliente 026", "Vendedora 1", "Indaiatuba", "Venda registrada", 12400],
]

df = pd.DataFrame(
    dados,
    columns=["Mês", "Cliente", "Vendedora", "Unidade", "Status", "Valor"]
)

meses = ["01/2026", "02/2026", "03/2026", "04/2026", "05/2026"]
unidades = sorted(df["Unidade"].unique())

col_mes, col_logo, col_unidade = st.columns([5, 1.5, 5])

with col_mes:
    mes = st.selectbox("Mês", meses, index=4)

with col_logo:
    st.markdown("### OPPI")
    st.markdown("**V I S I O N**")

with col_unidade:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

df_filtrado = df[df["Mês"] == mes]

if unidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Unidade"] == unidade]

total = len(df_filtrado)
vendas = len(df_filtrado[df_filtrado["Status"] == "Venda registrada"])
faturamento = df_filtrado["Valor"].sum()
ticket = faturamento / total if total else 0

contato1 = len(df_filtrado[df_filtrado["Status"] == "1º contato"])
contato2 = len(df_filtrado[df_filtrado["Status"] == "2º contato"])
contato3 = len(df_filtrado[df_filtrado["Status"] == "3º contato"])

st.divider()

k1, k2, k3, k4 = st.columns(4)

with k1:
    with st.container(border=True):
        st.metric("📌 Total de registros", total)
        st.caption(f"Leads registrados em {mes}")

with k2:
    with st.container(border=True):
        st.metric("✅ Vendas registradas", vendas)
        st.caption("Contratos convertidos")

with k3:
    with st.container(border=True):
        st.metric("💰 Faturamento", f"R$ {faturamento:,.0f}".replace(",", "."))
        st.caption("Receita estimada")

with k4:
    with st.container(border=True):
        st.metric("🎯 Ticket médio", f"R$ {ticket:,.0f}".replace(",", "."))
        st.caption("Média por contrato")

st.write("")

s1, s2, s3 = st.columns(3)

with s1:
    with st.container(border=True):
        st.metric("📞 1º contato", contato1)
        st.caption("Primeiro atendimento")

with s2:
    with st.container(border=True):
        st.metric("📲 2º contato", contato2)
        st.caption("Negociação")

with s3:
    with st.container(border=True):
        st.metric("🧾 3º contato", contato3)
        st.caption("Fechamento")

st.divider()

g1, g2 = st.columns(2)

with g1:
    with st.container(border=True):
        st.subheader("📞 Contatos por status")

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
            margin=dict(t=20, b=20, l=10, r=10),
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

with g2:
    with st.container(border=True):
        st.subheader("🏢 Vendas por unidade")

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
            margin=dict(t=20, b=20, l=10, r=10)
        )

        st.plotly_chart(fig2, use_container_width=True)

st.divider()

with st.container(border=True):
    st.subheader("📄 Contratos demonstrativos")
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )

st.info("Este dashboard utiliza dados fictícios para apresentação comercial da solução Oppi Vision.")

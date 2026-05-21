import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Oppi Mockup",
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
    padding-top: 1rem;
    max-width: 1180px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.header-box {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
}

.header-left {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.top-line {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 28px;
    width: 100%;
}

.oppi-logo {
    background: white;
    border-radius: 22px;
    padding: 18px 26px;
    box-shadow: 0 10px 28px rgba(15,23,42,.10);
    min-width: 210px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.logo-main {
    font-size: 42px;
    font-weight: 900;
    color: #1B1D6D;
    letter-spacing: -2px;
    line-height: 1;
}

.logo-sub {
    font-size: 15px;
    font-weight: 900;
    color: #9B0033;
    letter-spacing: 8px;
    margin-top: 8px;
}

.header-text {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.title {
    font-size: 34px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1;
}

.subtitle {
    color: #64748b;
    font-size: 14px;
    margin-top: 10px;
}

.badge {
    background: white;
    padding: 16px 24px;
    border-radius: 16px;
    font-weight: 900;
    color: #1B1D6D;
    box-shadow: 0 8px 20px rgba(15,23,42,.08);
    margin-top: 18px;
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

div[data-testid="stSelectbox"] label {
    font-weight: 700 !important;
    color: #334155 !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: white !important;
    border-radius: 14px !important;
}

@media (max-width: 768px) {

    .top-line {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .header-box {
        flex-direction: column;
    }

    .badge {
        width: 100%;
        text-align: center;
    }

    .oppi-logo {
        width: 100%;
    }

}

</style>
""", unsafe_allow_html=True)

dados = [
    {"Cliente": "João Mendes", "Unidade": "Campinas", "Raça": "Spitz Alemão", "Valor": 5200, "Status": "1º contato", "Mês": "05/2026"},
    {"Cliente": "Marina Costa", "Unidade": "Indaiatuba", "Raça": "Golden Retriever", "Valor": 6800, "Status": "2º contato", "Mês": "05/2026"},
    {"Cliente": "Carlos Lima", "Unidade": "Campinas", "Raça": "Maine Coon", "Valor": 6100, "Status": "3º contato", "Mês": "05/2026"},
    {"Cliente": "Fernanda Alves", "Unidade": "Jundiaí", "Raça": "Shih Tzu", "Valor": 3900, "Status": "Venda registrada", "Mês": "05/2026"},
    {"Cliente": "Rafael Souza", "Unidade": "Sorocaba", "Raça": "Bulldog Francês", "Valor": 7500, "Status": "Venda registrada", "Mês": "05/2026"},
    {"Cliente": "Patrícia Rocha", "Unidade": "Campinas", "Raça": "Poodle Toy", "Valor": 4300, "Status": "Primeiro contato mês", "Mês": "05/2026"},
    {"Cliente": "Lucas Martins", "Unidade": "Indaiatuba", "Raça": "Spitz Alemão", "Valor": 5800, "Status": "Segundo contato mês", "Mês": "05/2026"},
    {"Cliente": "Aline Ferreira", "Unidade": "Jundiaí", "Raça": "Border Collie", "Valor": 6400, "Status": "Terceiro contato mês", "Mês": "05/2026"},
]

st.markdown("""
<div class="header-box">

    <div class="header-left">

        <div class="top-line">

            <div class="oppi-logo">
                <div class="logo-main">OPPI</div>
                <div class="logo-sub">VISION</div>
            </div>

            <div class="header-text">
                <div class="title">📊 Operação Comercial</div>

                <div class="subtitle">
                    Dashboard mockup para demonstração de automações, contratos e vendas
                </div>
            </div>

        </div>

    </div>

    <div class="badge">
        Oppi Tech
    </div>

</div>
""", unsafe_allow_html=True)

meses = sorted(list(set(item["Mês"] for item in dados)))
unidades = sorted(list(set(item["Unidade"] for item in dados)))

col_f1, col_f2 = st.columns(2)

with col_f1:
    mes = st.selectbox("Mês", meses)

with col_f2:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

dados_filtrados = [item for item in dados if item["Mês"] == mes]

if unidade != "Todas":
    dados_filtrados = [item for item in dados_filtrados if item["Unidade"] == unidade]

st.divider()

total_registros = len(dados_filtrados)
vendas = len([item for item in dados_filtrados if item["Status"] == "Venda registrada"])
faturamento = sum(item["Valor"] for item in dados_filtrados)
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

    status_contagem = {}

    for item in dados_filtrados:
        status_contagem[item["Status"]] = status_contagem.get(item["Status"], 0) + 1

    status_lista = [{"Status": k, "Quantidade": v} for k, v in status_contagem.items()]

    fig = px.bar(
        status_lista,
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

    unidade_valores = {}

    for item in dados_filtrados:
        unidade_valores[item["Unidade"]] = unidade_valores.get(item["Unidade"], 0) + item["Valor"]

    unidade_lista = [{"Unidade": k, "Valor": v} for k, v in unidade_valores.items()]

    fig2 = px.pie(
        unidade_lista,
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

st.dataframe(
    dados_filtrados,
    use_container_width=True,
    hide_index=True
)

st.info("Este dashboard usa apenas dados fictícios para demonstração comercial.")

import streamlit as st
import streamlit.components.v1 as components
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
    max-width: 1250px;
    padding-top: 1.2rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

div[data-testid="stSelectbox"] label {
    font-weight: 700 !important;
    color: #0f172a !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #ffffff !important;
    border-radius: 14px !important;
}

hr {
    border-color: rgba(15,23,42,0.15) !important;
}
</style>
""", unsafe_allow_html=True)

def html_card(title, value, subtitle, accent="#1B1D6D"):
    components.html(f"""
    <div style="
        background:#ffffff;
        border-radius:18px;
        padding:24px;
        box-shadow:0 8px 22px rgba(15,23,42,.08);
        border-left:8px solid {accent};
        height:135px;
        box-sizing:border-box;
        font-family:Arial, sans-serif;
    ">
        <div style="
            font-size:16px;
            font-weight:800;
            color:#1e293b;
            margin-bottom:12px;
        ">
            {title}
        </div>

        <div style="
            font-size:44px;
            font-weight:900;
            color:#09122C;
            line-height:1;
            margin-bottom:14px;
        ">
            {value}
        </div>

        <div style="
            font-size:13px;
            color:#64748b;
        ">
            {subtitle}
        </div>
    </div>
    """, height=150)

components.html("""
<div style="
    width:100%;
    display:flex;
    justify-content:center;
    align-items:center;
    font-family:Arial, sans-serif;
    margin-top:5px;
    margin-bottom:20px;
">
    <div style="text-align:center;">
        <div style="
            font-size:52px;
            font-weight:900;
            color:#09122C;
            line-height:1;
        ">
            📊 Operação Comercial
        </div>

        <div style="
            color:#64748b;
            font-size:15px;
            margin-top:12px;
        ">
            Dashboard mockup para demonstração de automações, contratos e vendas
        </div>
    </div>
</div>
""", height=120)

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

meses = sorted(list(set(item["Mês"] for item in dados)))
unidades = sorted(list(set(item["Unidade"] for item in dados)))

col1, col_logo, col2 = st.columns([5, 2, 5])

with col1:
    mes = st.selectbox("Mês", meses)

with col_logo:
    components.html("""
    <div style="
        width:100%;
        display:flex;
        justify-content:center;
        align-items:center;
        padding-top:6px;
        font-family:Arial, sans-serif;
    ">
        <div style="
            background:white;
            width:130px;
            height:130px;
            border-radius:50%;
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            box-shadow:0 10px 28px rgba(15,23,42,.12);
        ">
            <div style="
                font-size:42px;
                font-weight:900;
                color:#1B1D6D;
                line-height:1;
            ">
                OPPI
            </div>

            <div style="
                font-size:14px;
                font-weight:900;
                color:#9B0033;
                letter-spacing:8px;
                margin-top:8px;
            ">
                VISION
            </div>
        </div>
    </div>
    """, height=145)

with col2:
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
    html_card("📌 Total de registros", total_registros, f"Mês selecionado: {mes}", "#1B1D6D")

with c2:
    html_card("✅ Vendas registradas", vendas, "Contratos convertidos", "#B0004F")

with c3:
    html_card("💰 Faturamento", f"R$ {faturamento:,.0f}".replace(",", "."), "Valor fictício demonstrativo", "#1B1D6D")

with c4:
    html_card("🎯 Ticket médio", f"R$ {ticket_medio:,.0f}".replace(",", "."), "Média por registro", "#B0004F")

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

    fig.update_traces(
        marker_color="#1B1D6D",
        textposition="outside"
    )

    fig.update_layout(
        height=380,
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=20, b=30, l=10, r=10),
        xaxis_title=None,
        yaxis_title=None
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
        hole=0.50
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

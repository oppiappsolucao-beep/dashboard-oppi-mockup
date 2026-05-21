import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Oppi Vision",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#D6D6D6;
}

.block-container{
    padding-top:20px;
    max-width:1300px;
}

/* KPI */

.kpi{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 4px 15px rgba(0,0,0,0.08);
    height:140px;
}

.kpi-blue{
    border-left:7px solid #1B1D6D;
}

.kpi-pink{
    border-left:7px solid #C10057;
}

.kpi-title{
    font-size:16px;
    font-weight:700;
    color:#111827;
}

.kpi-value{
    font-size:42px;
    font-weight:900;
    color:#020617;
    margin-top:10px;
}

.kpi-sub{
    font-size:12px;
    color:#64748b;
    margin-top:10px;
}

/* BOX */

.box{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 4px 15px rgba(0,0,0,0.08);
}

/* TITLES */

.title-chart{
    font-size:24px;
    font-weight:800;
    color:#111827;
    margin-bottom:10px;
}

/* LOGO */

.logo-circle{
    width:90px;
    height:90px;
    background:white;
    border-radius:50%;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    margin:auto;
    box-shadow:0 4px 15px rgba(0,0,0,0.08);
}

.logo-main{
    font-size:30px;
    font-weight:900;
    color:#1B1D6D;
    line-height:1;
}

.logo-sub{
    font-size:10px;
    letter-spacing:5px;
    font-weight:800;
    color:#C10057;
    margin-top:5px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<h1 style='text-align:center;color:#09122C;font-size:60px;'>
📊 Operação Comercial
</h1>

<p style='text-align:center;color:#64748b;font-size:15px;margin-top:-20px;'>
Dashboard comercial demonstrativo • Oppi Vision
</p>
""", unsafe_allow_html=True)

# =====================================================
# DADOS FAKE
# =====================================================

dados = [

    ["Cliente 001","Vendedora 1","Campinas",5200,"Venda registrada","01/2026"],
    ["Cliente 002","Vendedora 2","Indaiatuba",7400,"1º contato","01/2026"],
    ["Cliente 003","Vendedora 3","Jundiaí",6100,"2º contato","01/2026"],
    ["Cliente 004","Vendedora 1","Sorocaba",9800,"Venda registrada","01/2026"],

    ["Cliente 005","Vendedora 2","Campinas",4700,"3º contato","02/2026"],
    ["Cliente 006","Vendedora 3","Indaiatuba",8600,"Venda registrada","02/2026"],
    ["Cliente 007","Vendedora 1","Jundiaí",3900,"1º contato","02/2026"],
    ["Cliente 008","Vendedora 2","Sorocaba",9100,"Venda registrada","02/2026"],

    ["Cliente 009","Vendedora 3","Campinas",8200,"2º contato","03/2026"],
    ["Cliente 010","Vendedora 1","Indaiatuba",7700,"Venda registrada","03/2026"],
    ["Cliente 011","Vendedora 2","Jundiaí",6200,"1º contato","03/2026"],
    ["Cliente 012","Vendedora 3","Sorocaba",5400,"Venda registrada","03/2026"],

    ["Cliente 013","Vendedora 1","Campinas",10200,"3º contato","04/2026"],
    ["Cliente 014","Vendedora 2","Indaiatuba",6900,"Venda registrada","04/2026"],
    ["Cliente 015","Vendedora 3","Jundiaí",4300,"2º contato","04/2026"],
    ["Cliente 016","Vendedora 1","Sorocaba",8700,"Venda registrada","04/2026"],

    ["Cliente 017","Vendedora 2","Campinas",5900,"1º contato","05/2026"],
    ["Cliente 018","Vendedora 3","Indaiatuba",11300,"Venda registrada","05/2026"],
    ["Cliente 019","Vendedora 1","Jundiaí",6800,"2º contato","05/2026"],
    ["Cliente 020","Vendedora 2","Sorocaba",9200,"Venda registrada","05/2026"],

]

df = pd.DataFrame(
    dados,
    columns=[
        "Cliente",
        "Vendedora",
        "Unidade",
        "Valor",
        "Status",
        "Mês"
    ]
)

# =====================================================
# FILTROS
# =====================================================

meses = sorted(df["Mês"].unique())
unidades = sorted(df["Unidade"].unique())

c1,c2,c3 = st.columns([5,1.2,5])

with c1:
    mes = st.selectbox("Mês", meses)

with c2:

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

with c3:
    unidade = st.selectbox(
        "Unidade",
        ["Todas"] + list(unidades)
    )

# =====================================================
# FILTRO DF
# =====================================================

df_filtrado = df[df["Mês"] == mes]

if unidade != "Todas":
    df_filtrado = df_filtrado[
        df_filtrado["Unidade"] == unidade
    ]

# =====================================================
# KPIS
# =====================================================

total = len(df_filtrado)

vendas = len(
    df_filtrado[
        df_filtrado["Status"] == "Venda registrada"
    ]
)

faturamento = df_filtrado["Valor"].sum()

ticket = faturamento / total if total > 0 else 0

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

st.divider()

# =====================================================
# CARDS
# =====================================================

def card(titulo, valor, sub, pink=False):

    classe = "kpi-pink" if pink else "kpi-blue"

    st.markdown(f"""
    <div class='kpi {classe}'>

        <div class='kpi-title'>
            {titulo}
        </div>

        <div class='kpi-value'>
            {valor}
        </div>

        <div class='kpi-sub'>
            {sub}
        </div>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# KPI LINHA 1
# =====================================================

k1,k2,k3,k4 = st.columns(4)

with k1:
    card(
        "📌 Total de registros",
        total,
        f"Leads registrados em {mes}"
    )

with k2:
    card(
        "✅ Vendas registradas",
        vendas,
        "Contratos convertidos",
        True
    )

with k3:
    card(
        "💰 Faturamento",
        f"R$ {faturamento:,.0f}".replace(",", "."),
        "Receita estimada"
    )

with k4:
    card(
        "🎯 Ticket médio",
        f"R$ {ticket:,.0f}".replace(",", "."),
        "Média por contrato",
        True
    )

# =====================================================
# KPI LINHA 2
# =====================================================

st.write("")

s1,s2,s3 = st.columns(3)

with s1:
    card(
        "📞 1º contato",
        contato1,
        "Primeiro atendimento"
    )

with s2:
    card(
        "📲 2º contato",
        contato2,
        "Negociação",
        True
    )

with s3:
    card(
        "🧾 3º contato",
        contato3,
        "Fechamento"
    )

# =====================================================
# GRAFICOS
# =====================================================

st.divider()

g1,g2 = st.columns(2)

with g1:

    st.markdown("<div class='box'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='title-chart'>
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
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=350,
        margin=dict(t=10,b=10,l=10,r=10)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

with g2:

    st.markdown("<div class='box'>", unsafe_allow_html=True)

    st.markdown("""
    <div class='title-chart'>
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
        hole=0.5
    )

    fig2.update_layout(
        paper_bgcolor="white",
        height=350,
        margin=dict(t=10,b=10,l=10,r=10)
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# TABELA
# =====================================================

st.divider()

st.markdown("<div class='box'>", unsafe_allow_html=True)

st.markdown("""
<div class='title-chart'>
📄 Contratos demonstrativos
</div>
""", unsafe_allow_html=True)

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True
)

st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# INFO
# =====================================================

st.write("")

st.info(
    "Este dashboard utiliza dados fictícios para apresentação comercial da solução Oppi Vision."
)

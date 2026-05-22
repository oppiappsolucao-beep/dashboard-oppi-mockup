import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Operação Comercial",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS SKOOB STYLE
# =========================
st.markdown("""
<style>

.stApp {
    background: #D4D4D4;
}

.block-container {
    max-width: 1200px;
    padding-top: 1rem;
}

.card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    border-left: 6px solid #1B1D6D;
}

.kpi-title {
    font-size: 12px;
    font-weight: 700;
    color: #475569;
}

.kpi-value {
    font-size: 38px;
    font-weight: 900;
    color: #0f172a;
}

.kpi-sub {
    font-size: 11px;
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)


# =========================
# DATA (GOOGLE SHEETS REAL)
# =========================
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df


df = load_data()

if df.empty:
    st.stop()

# =========================
# FILTROS (SKOOB HEADER STYLE)
# =========================
meses = sorted(df["Mês"].dropna().unique().tolist())
unidades = sorted(df["Unidade"].dropna().unique().tolist())

col1, col2, col3 = st.columns([3,1,3])

with col1:
    mes = st.selectbox("Mês", meses)

with col2:
    st.markdown("""
    <div style="
        width:80px;
        height:80px;
        border-radius:50%;
        background:white;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:900;
        color:#1B1D6D;
        box-shadow:0 8px 20px rgba(0,0,0,0.1);
        margin:auto;
    ">
    OPPI
    </div>
    """, unsafe_allow_html=True)

with col3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades)

st.divider()

# =========================
# FILTRO DATA
# =========================
df_f = df[df["Mês"] == mes]

if unidade != "Todas":
    df_f = df_f[df_f["Unidade"] == unidade]


# =========================
# KPIs (SKOOB GRID 6 CARDS)
# =========================
total = len(df_f)

status_cols = [c for c in df_f.columns if "Status" in c]

df_status = None
if status_cols:
    df_status = df_f[status_cols].melt(
        var_name="Etapa",
        value_name="Status"
    )
    df_status = df_status.dropna()
    df_status = df_status[df_status["Status"] != ""]

vendas = len(df_status[df_status["Status"].str.contains("Enviado", na=False)]) if df_status is not None else 0

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Total registros</div>
        <div class="kpi-value">{total}</div>
        <div class="kpi-sub">Mês selecionado</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Vendas</div>
        <div class="kpi-value">{vendas}</div>
        <div class="kpi-sub">Conversões</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="kpi-title">Status total</div>
        <div class="kpi-value">{len(df_status) if df_status is not None else 0}</div>
        <div class="kpi-sub">Interações</div>
    </div>
    """, unsafe_allow_html=True)


st.divider()

# =========================
# GRÁFICOS SKOOB STYLE (2 COLUNAS)
# =========================
g1, g2 = st.columns(2)

# ---- STATUS
with g1:
    st.subheader("Contatos por status")

    if df_status is not None:
        chart = df_status.groupby("Status").size().reset_index(name="Qtd")

        fig = px.bar(chart, x="Status", y="Qtd", text="Qtd")
        fig.update_layout(
            height=350,
            paper_bgcolor="white",
            plot_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---- UNIDADE
with g2:
    st.subheader("Vendas por unidade")

    uni = df_f.groupby("Unidade").size().reset_index(name="Qtd")

    fig2 = px.bar(uni, x="Unidade", y="Qtd", text="Qtd")
    fig2.update_layout(
        height=350,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig2, use_container_width=True)


st.divider()

# =========================
# TABELA FINAL
# =========================
st.subheader("Dados da planilha")

st.dataframe(df_f, use_container_width=True)

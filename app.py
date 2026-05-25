import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Operação Comercial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS PREMIUM OPPI
# =========================
st.markdown("""
<style>

.stApp {
    background: #d9d9d9;
    color: #111827;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.block-container {
    padding-top: 28px;
    max-width: 1280px;
}

/* TOPO */
.header-left {
    display: flex;
    align-items: flex-start;
    gap: 16px;
}

.header-title {
    font-size: 30px;
    font-weight: 900;
    color: #111827;
    line-height: 1.1;
    margin-bottom: 8px;
}

.header-subtitle {
    font-size: 13px;
    color: #64748b;
    font-weight: 600;
}

.header-total {
    font-size: 12px;
    color: #64748b;
    margin-top: 14px;
}

/* BOTÃO SAIR */
.logout-btn {
    background: linear-gradient(135deg, #1D4ED8, #7C3AED);
    color: #F8FAFC;
    border-radius: 12px;
    padding: 13px 42px;
    font-weight: 800;
    font-size: 13px;
    text-align: center;
    border: 1px solid rgba(6,182,212,0.35);
    box-shadow:
        0 0 0 2px rgba(29,78,216,0.25),
        0 0 18px rgba(124,58,237,0.45),
        0 0 28px rgba(6,182,212,0.25),
        0 10px 25px rgba(0,0,0,0.35);
    transition: all 0.25s ease;
}

.logout-btn:hover {
    transform: translateY(-2px);
    box-shadow:
        0 0 0 2px rgba(6,182,212,0.30),
        0 0 26px rgba(124,58,237,0.55),
        0 0 34px rgba(6,182,212,0.35),
        0 12px 28px rgba(0,0,0,0.45);
}

/* HAMBURGUER */
div[data-testid="stPopover"] button {
    background: linear-gradient(135deg, #1D4ED8, #7C3AED) !important;
    color: #F8FAFC !important;
    border: 1px solid rgba(6,182,212,0.35) !important;
    border-radius: 12px !important;
    min-height: 42px !important;
    min-width: 58px !important;
    padding: 0 14px !important;
    font-weight: 800 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow:
        0 0 0 2px rgba(29,78,216,0.25) !important,
        0 0 18px rgba(124,58,237,0.45) !important,
        0 0 28px rgba(6,182,212,0.25) !important,
        0 10px 25px rgba(0,0,0,0.35) !important;
    transition: all 0.25s ease !important;
}

div[data-testid="stPopover"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 0 0 2px rgba(6,182,212,0.30) !important,
        0 0 26px rgba(124,58,237,0.55) !important,
        0 0 34px rgba(6,182,212,0.35) !important,
        0 12px 28px rgba(0,0,0,0.45) !important;
}

div[data-testid="stPopover"] button p {
    color: #F8FAFC !important;
    font-weight: 800 !important;
}

div[data-testid="stPopover"] button svg {
    color: #F8FAFC !important;
    fill: #F8FAFC !important;
}

/* LINKS DO MENU */
.menu-link {
    display: block;
    background: #0F172A;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 8px;
    color: #F8FAFC !important;
    text-decoration: none !important;
    font-weight: 800;
    border-left: 4px solid #06B6D4;
    box-shadow: 0 4px 14px rgba(0,0,0,0.28);
}

.menu-link:hover {
    background: #1E293B;
}

/* LOGO */
.logo-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -8px;
}

.logo {
    width:82px;
    height:82px;
    border-radius:50%;
    background: #0F172A;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    box-shadow:
        0 0 0 2px rgba(6,182,212,0.20),
        0 8px 25px rgba(124,58,237,0.35);
    border: 1px solid rgba(6,182,212,0.28);
}

.logo .a {
    font-weight:900;
    color:#06B6D4;
    font-size:16px;
}

.logo .b {
    font-size:9px;
    font-weight:900;
    color:#7C3AED;
    letter-spacing:2px;
}

/* CARDS PEQUENOS */
.mini-card {
    background: #0F172A;
    border-radius: 18px;
    padding: 14px 16px 10px 16px;
    min-height: 118px;
    box-shadow:
        0 6px 18px rgba(0,0,0,0.32),
        0 0 18px rgba(6,182,212,0.08);
    margin-bottom: 8px;
    border: 1px solid rgba(6,182,212,0.12);
    transition: all 0.25s ease;
}

.mini-card:hover {
    transform: translateY(-2px);
    background: #1E293B;
    box-shadow:
        0 8px 22px rgba(0,0,0,0.42),
        0 0 18px rgba(6,182,212,0.18),
        0 0 28px rgba(124,58,237,0.15);
}

.mini-title {
    font-size: 12px;
    font-weight: 900;
    color: #F8FAFC;
    line-height: 1.35;
}

.mini-value {
    font-size: 28px;
    font-weight: 900;
    color: #F8FAFC;
    line-height: 1;
    margin-top: 10px;
}

.mini-sub {
    font-size: 11px;
    color: #A1A1AA;
    margin-top: 8px;
}

/* CARDS GRANDES */
.wide-card {
    background: #0F172A;
    border-radius: 18px;
    padding: 16px 18px;
    min-height: 116px;
    box-shadow:
        0 6px 18px rgba(0,0,0,0.32),
        0 0 18px rgba(6,182,212,0.08);
    margin-top: 8px;
    margin-bottom: 8px;
    border: 1px solid rgba(6,182,212,0.12);
    transition: all 0.25s ease;
}

.wide-card:hover {
    transform: translateY(-2px);
    background: #1E293B;
}

.wide-title {
    font-size: 18px;
    font-weight: 900;
    color: #F8FAFC;
}

.wide-value {
    font-size: 50px;
    font-weight: 900;
    color: #F8FAFC;
    line-height: 1;
    margin-top: 8px;
}

.wide-sub {
    font-size: 12px;
    color: #A1A1AA;
    margin-top: 8px;
}

/* CABEÇALHO DOS GRÁFICOS */
.graph-title-card {
    background: #0F172A;
    border-radius: 18px;
    padding: 14px 20px 12px 20px;
    margin-top: 10px;
    margin-bottom: 10px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.32);
    border: 1px solid rgba(6,182,212,0.12);
}

.graph-title {
    font-size: 19px;
    font-weight: 900;
    color: #F8FAFC;
    margin-bottom: 4px;
}

.graph-subtitle {
    font-size: 13px;
    color: #A1A1AA;
}

/* CARD DO GRÁFICO */
.chart-card {
    background: #0F172A;
    border-radius: 0px;
    padding: 8px 10px 14px 10px;
    border: 1px solid rgba(6,182,212,0.08);
    box-shadow: 0 6px 18px rgba(0,0,0,0.24);
    margin-bottom: 16px;
}

/* SELECT */
.stSelectbox label {
    color: #111827 !important;
    font-weight: 700 !important;
}

.stSelectbox > div > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    color: #111827 !important;
    border: 1px solid rgba(15,23,42,0.18) !important;
}

.stSelectbox div {
    color: #111827 !important;
}

/* DIVISOR */
hr {
    border: 1px solid rgba(15,23,42,0.18);
    margin-top: 28px;
    margin-bottom: 28px;
}

@media (max-width: 768px) {
    .header-title {
        font-size: 24px;
    }

    .logout-btn {
        padding: 10px 24px;
    }

    .logo {
        width: 70px;
        height: 70px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# PLANILHA
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    return df

df = load_data().dropna(how="all")

# =========================
# HELPERS
# =========================
def normalize_text(text):
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    return " ".join(text.split())

def find_col(dataframe, aliases, exclude_terms=None):
    exclude_terms = exclude_terms or []
    cols = list(dataframe.columns)
    norm_map = {c: normalize_text(c) for c in cols}

    for alias in aliases:
        alias_n = normalize_text(alias)
        for c, c_n in norm_map.items():
            if any(ex in c_n for ex in exclude_terms):
                continue
            if c_n == alias_n:
                return c

    for alias in aliases:
        alias_n = normalize_text(alias)
        for c, c_n in norm_map.items():
            if any(ex in c_n for ex in exclude_terms):
                continue
            if alias_n in c_n:
                return c

    return None

def parse_date_series(series):
    return pd.to_datetime(series, errors="coerce", dayfirst=True)

def count_non_empty(series):
    s = series.fillna("").astype(str).str.strip()
    return int(((s != "") & (s.str.lower() != "nan") & (s.str.lower() != "none")).sum())

def render_mini_card(title, value, subtitle, accent):
    st.markdown(f"""
    <div class="mini-card" style="border-left: 7px solid {accent};">
        <div class="mini-title">{title}</div>
        <div class="mini-value">{value}</div>
        <div class="mini-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_wide_card(title, value, subtitle, accent):
    st.markdown(f"""
    <div class="wide-card" style="border-left: 8px solid {accent};">
        <div class="wide-title">{title}</div>
        <div class="wide-value">{value}</div>
        <div class="wide-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_graph_header(title, subtitle):
    st.markdown(f"""
    <div class="graph-title-card">
        <div class="graph-title">{title}</div>
        <div class="graph-subtitle">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def apply_bar_layout(fig, height=360):
    fig.update_layout(
        height=height,
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font_color="#F8FAFC",
        margin=dict(l=10, r=10, t=10, b=20),
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=11, color="#A1A1AA"),
            title=dict(
                font=dict(color="#A1A1AA")
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#1E293B",
            zeroline=False,
            tickfont=dict(size=11, color="#A1A1AA"),
            title=dict(
                font=dict(color="#A1A1AA")
            )
        )
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#F8FAFC"),
        marker_line_width=0
    )

    return fig

# =========================
# CORES OPPI
# =========================
AZUL_OPPI = "#1D4ED8"
ROXO_TEC = "#7C3AED"
CIANO_DETALHE = "#06B6D4"
VERDE_SUCESSO = "#22C55E"
LARANJA_ATENCAO = "#F97316"

CORES_GRAFICO = [
    "#1D4ED8",
    "#7C3AED",
    "#06B6D4",
    "#22C55E",
    "#F97316",
    "#1D4ED8",
    "#7C3AED",
    "#06B6D4",
    "#22C55E",
    "#F97316"
]

# =========================
# COLUNAS IMPORTANTES
# =========================
status_1_col = find_col(df, ["Status 1º contato", "Status 1 contato", "Status primeiro contato"])
status_2_col = find_col(df, ["Status 2º contato", "Status 2 contato", "Status segundo contato"])
status_3_col = find_col(df, ["Status 3º contato", "Status 3 contato", "Status terceiro contato"])

data_1_col = find_col(
    df,
    ["Data 1º contato", "1º contato", "Primeiro contato", "Data primeiro contato"],
    exclude_terms=["status"]
)

data_2_col = find_col(
    df,
    ["Data 2º contato", "2º contato", "Segundo contato", "Data segundo contato"],
    exclude_terms=["status"]
)

data_3_col = find_col(
    df,
    ["Data 3º contato", "3º contato", "Terceiro contato", "Data terceiro contato"],
    exclude_terms=["status"]
)

vendedora_col = find_col(df, [
    "Vendedora",
    "Vendedor",
    "Consultora",
    "Consultor",
    "Responsável",
    "Responsavel",
    "Atendente"
])

# =========================
# TOPO COM MENU
# =========================
top_col1, top_col2, top_col3 = st.columns([1.2, 8, 2])

with top_col1:
    with st.popover("☰"):
        st.markdown("""
        <a class="menu-link" href="#" target="_self">📊 Dashboard</a>
        <a class="menu-link" href="#" target="_self">📋 Dados da planilha</a>
        <a class="menu-link" href="#" target="_self">⚙️ Configurações</a>
        """, unsafe_allow_html=True)

with top_col2:
    st.markdown(f"""
    <div class="header-left">
        <div>
            <div class="header-title">⚙️ Operação Comercial</div>
            <div class="header-subtitle">Oppi Vision • Dashboard Premium</div>
            <div class="header-total">Total de registros: {len(df)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with top_col3:
    st.markdown("""
    <div class="logout-btn">Sair</div>
    """, unsafe_allow_html=True)

# =========================
# FILTROS
# =========================
meses = sorted(df["Mês"].dropna().unique()) if "Mês" in df.columns else []
unidades = sorted(df["Unidade"].dropna().unique()) if "Unidade" in df.columns else []

col1, col2, col3 = st.columns([4, 1, 4])

with col1:
    mes = st.selectbox("Mês", meses) if meses else None

with col2:
    st.markdown("""
    <div class="logo-wrap">
        <div class="logo">
            <div class="a">OPPI</div>
            <div class="b">VISION</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    unidade = st.selectbox("Unidade", ["Todas"] + unidades) if unidades else "Todas"

st.divider()

# =========================
# FILTROS DE DADOS
# =========================
df_f = df.copy()

if mes is not None and "Mês" in df_f.columns:
    df_f = df_f[df_f["Mês"] == mes]

if unidade != "Todas" and "Unidade" in df_f.columns:
    df_f = df_f[df_f["Unidade"] == unidade]

df_today_base = df.copy()

if unidade != "Todas" and "Unidade" in df_today_base.columns:
    df_today_base = df_today_base[df_today_base["Unidade"] == unidade]

# =========================
# MÉTRICAS
# =========================
today = pd.Timestamp.now(tz="America/Sao_Paulo").date()

def today_count(dataframe, col):
    if not col or col not in dataframe.columns:
        return 0
    d = parse_date_series(dataframe[col]).dt.date
    return int((d == today).sum())

def monthly_contact_count(dataframe, date_col, status_col):
    if date_col and date_col in dataframe.columns:
        return count_non_empty(dataframe[date_col])
    if status_col and status_col in dataframe.columns:
        return count_non_empty(dataframe[status_col])
    return 0

contato1_hoje = today_count(df_today_base, data_1_col)
contato2_hoje = today_count(df_today_base, data_2_col)
contato3_hoje = today_count(df_today_base, data_3_col)

primeiro_mes = monthly_contact_count(df_f, data_1_col, status_1_col)
segundo_mes = monthly_contact_count(df_f, data_2_col, status_2_col)
terceiro_mes = monthly_contact_count(df_f, data_3_col, status_3_col)

error_mask = pd.Series(False, index=df_f.index)

for c in [status_1_col, status_2_col, status_3_col]:
    if c and c in df_f.columns:
        error_mask = error_mask | df_f[c].fillna("").astype(str).str.contains("erro", case=False, na=False)

status_com_erro = int(error_mask.sum())
vendas_mes = len(df_f)

# =========================
# CARDS DO TOPO
# =========================
row1 = st.columns(6)

with row1[0]:
    render_mini_card("💬 1º contato<br>hoje", contato1_hoje, "registros de hoje", AZUL_OPPI)

with row1[1]:
    render_mini_card("💬 2º contato<br>hoje", contato2_hoje, "registros de hoje", ROXO_TEC)

with row1[2]:
    render_mini_card("💬 3º contato<br>hoje", contato3_hoje, "registros de hoje", CIANO_DETALHE)

with row1[3]:
    render_mini_card("📄 Primeiro<br>Contato Mês", primeiro_mes, str(mes) if mes else "-", AZUL_OPPI)

with row1[4]:
    render_mini_card("📄 Segundo<br>Contato Mês", segundo_mes, str(mes) if mes else "-", ROXO_TEC)

with row1[5]:
    render_mini_card("📄 Terceiro<br>Contato Mês", terceiro_mes, str(mes) if mes else "-", CIANO_DETALHE)

row2 = st.columns(2)

with row2[0]:
    render_wide_card(
        "Status com erro",
        status_com_erro,
        f"Mês selecionado: {mes}" if mes else "Mês selecionado: -",
        LARANJA_ATENCAO
    )

with row2[1]:
    render_wide_card(
        "Vendas registradas no mês",
        vendas_mes,
        f"Mês Venda: {mes}" if mes else "Mês Venda: -",
        VERDE_SUCESSO
    )

st.divider()

# =========================
# GRÁFICOS DETALHADOS
# =========================
g1, g2 = st.columns(2)

# =========================
# CONTATOS POR MÊS
# =========================
with g1:
    render_graph_header(
        "📞 Contatos por mês",
        "Distribuição mensal dos 3 contatos"
    )

    contatos_mes = pd.DataFrame({
        "Contato": ["1º contato", "2º contato", "3º contato"],
        "Qtd": [primeiro_mes, segundo_mes, terceiro_mes]
    })

    fig_contatos = px.bar(
        contatos_mes,
        x="Contato",
        y="Qtd",
        text="Qtd",
        color="Contato",
        color_discrete_sequence=CORES_GRAFICO
    )

    fig_contatos = apply_bar_layout(fig_contatos, height=370)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_contatos, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# VENDAS POR UNIDADE
# =========================
with g2:
    render_graph_header(
        "🏙️ Vendas por unidade no mês",
        "Quantidade de vendas registradas por unidade no mês selecionado"
    )

    if "Unidade" in df_f.columns:
        vendas_unidade = (
            df_f["Unidade"]
            .fillna("Sem unidade")
            .astype(str)
            .str.strip()
            .replace("", "Sem unidade")
            .value_counts()
            .reset_index()
        )
        vendas_unidade.columns = ["Unidade", "Qtd"]
    else:
        vendas_unidade = pd.DataFrame(columns=["Unidade", "Qtd"])

    fig_unidade = px.bar(
        vendas_unidade,
        x="Unidade",
        y="Qtd",
        text="Qtd",
        color="Unidade",
        color_discrete_sequence=CORES_GRAFICO
    )

    fig_unidade = apply_bar_layout(fig_unidade, height=370)
    fig_unidade.update_xaxes(tickangle=-18)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_unidade, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

g3, g4 = st.columns(2)

# =========================
# RAÇAS MAIS VENDIDAS
# =========================
with g3:
    render_graph_header(
        "🐶 Raças mais vendidas (mês)",
        "Top 10 raças do mês filtrado"
    )

    if "Raça" in df_f.columns:
        racas = (
            df_f["Raça"]
            .fillna("Sem raça")
            .astype(str)
            .str.strip()
            .replace("", "Sem raça")
            .value_counts()
            .head(10)
            .reset_index()
        )
        racas.columns = ["Raça", "Qtd"]
    else:
        racas = pd.DataFrame(columns=["Raça", "Qtd"])

    fig_racas = px.bar(
        racas,
        x="Raça",
        y="Qtd",
        text="Qtd",
        color="Raça",
        color_discrete_sequence=CORES_GRAFICO
    )

    fig_racas = apply_bar_layout(fig_racas, height=370)
    fig_racas.update_xaxes(tickangle=-28)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_racas, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# VENDAS POR VENDEDORA
# =========================
with g4:
    render_graph_header(
        "🏆 Vendas por vendedora (mês)",
        "Todas as vendas do mês, incluindo sem nome"
    )

    if vendedora_col and vendedora_col in df_f.columns:
        vendas_vendedora = (
            df_f[vendedora_col]
            .fillna("Sem nome")
            .astype(str)
            .str.strip()
            .replace("", "Sem nome")
            .value_counts()
            .reset_index()
        )
        vendas_vendedora.columns = ["Vendedora", "Qtd"]
    else:
        vendas_vendedora = pd.DataFrame({
            "Vendedora": ["Sem coluna de vendedora"],
            "Qtd": [0]
        })

    fig_vendedora = px.bar(
        vendas_vendedora,
        x="Vendedora",
        y="Qtd",
        text="Qtd",
        color="Vendedora",
        color_discrete_sequence=CORES_GRAFICO
    )

    fig_vendedora = apply_bar_layout(fig_vendedora, height=370)
    fig_vendedora.update_xaxes(tickangle=-28)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_vendedora, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

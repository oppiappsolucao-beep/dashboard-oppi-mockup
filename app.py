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
# CSS PREMIUM
# =========================
st.markdown("""
<style>

/* BACKGROUND PRINCIPAL CINZA */
.stApp {
    background: #d9d9d9;
    color: #111827;
}

/* remove streamlit UI */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* CONTAINER */
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
    color: #6b7280;
    font-weight: 600;
}

.header-total {
    font-size: 12px;
    color: #6b7280;
    margin-top: 14px;
}

/* BOTÃO SAIR */
.logout-btn {
    background: linear-gradient(135deg, #f23b9b, #a000d4);
    color: white;
    border-radius: 12px;
    padding: 13px 42px;
    font-weight: 800;
    font-size: 13px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.25);
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.22),
        0 0 18px rgba(242,59,155,0.45),
        0 0 26px rgba(160,0,212,0.35),
        0 10px 25px rgba(160,0,212,0.25);
    transition: all 0.25s ease;
}

.logout-btn:hover {
    transform: translateY(-2px);
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.32),
        0 0 26px rgba(242,59,155,0.60),
        0 0 34px rgba(160,0,212,0.45),
        0 12px 28px rgba(160,0,212,0.35);
}

/* HAMBURGUER */
div[data-testid="stPopover"] button {
    background: linear-gradient(135deg, #f23b9b, #a000d4) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 12px !important;
    min-height: 42px !important;
    min-width: 58px !important;
    padding: 0 14px !important;
    font-weight: 800 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.22) !important,
        0 0 18px rgba(242,59,155,0.45) !important,
        0 0 26px rgba(160,0,212,0.35) !important,
        0 10px 25px rgba(160,0,212,0.25) !important;
    transition: all 0.25s ease !important;
}

div[data-testid="stPopover"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.32) !important,
        0 0 26px rgba(242,59,155,0.60) !important,
        0 0 34px rgba(160,0,212,0.45) !important,
        0 12px 28px rgba(160,0,212,0.35) !important;
}

div[data-testid="stPopover"] button p {
    color: white !important;
    font-weight: 800 !important;
}

div[data-testid="stPopover"] button svg {
    color: white !important;
    fill: white !important;
}

/* LINKS DO MENU */
.menu-link {
    display: block;
    background: #ffffff;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 8px;
    color: #111827 !important;
    text-decoration: none !important;
    font-weight: 800;
    border-left: 4px solid #f23b9b;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}

.menu-link:hover {
    background: #fff0fa;
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
    background: white;
    display:flex;
    align-items:center;
    justify-content:center;
    flex-direction:column;
    box-shadow:
        0 0 0 2px rgba(242,59,155,0.10),
        0 8px 25px rgba(160,0,212,0.18);
    border: 1px solid #e5e7eb;
}

.logo .a {
    font-weight:900;
    color:#a000d4;
    font-size:16px;
}

.logo .b {
    font-size:9px;
    font-weight:900;
    color:#f23b9b;
    letter-spacing:2px;
}

/* CARDS PEQUENOS */
.mini-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 14px 16px 10px 16px;
    min-height: 118px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 8px;
}

.mini-title {
    font-size: 12px;
    font-weight: 900;
    color: #102247;
    line-height: 1.35;
}

.mini-value {
    font-size: 28px;
    font-weight: 900;
    color: #031b4e;
    line-height: 1;
    margin-top: 10px;
}

.mini-sub {
    font-size: 11px;
    color: #64748b;
    margin-top: 8px;
}

/* CARDS GRANDES */
.wide-card {
    background: #ffffff;
    border-radius: 18px;
    padding: 16px 18px;
    min-height: 116px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-top: 8px;
    margin-bottom: 8px;
}

.wide-title {
    font-size: 18px;
    font-weight: 900;
    color: #111827;
}

.wide-value {
    font-size: 50px;
    font-weight: 900;
    color: #031b4e;
    line-height: 1;
    margin-top: 8px;
}

.wide-sub {
    font-size: 12px;
    color: #64748b;
    margin-top: 8px;
}

/* CARDS DE GRÁFICO */
.chart-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-top: 10px;
}

/* TITULOS */
h3 {
    color: #111827 !important;
    font-weight: 900 !important;
}

/* SELECT */
.stSelectbox label {
    color: #374151 !important;
    font-weight: 700 !important;
}

.stSelectbox > div > div {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    color: #111827 !important;
    border: 1px solid #e5e7eb !important;
}

/* TABELA */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 14px;
}

/* DIVISOR */
hr {
    border: 1px solid rgba(17,24,39,0.12);
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

    # primeiro tenta igualdade
    for alias in aliases:
        alias_n = normalize_text(alias)
        for c, c_n in norm_map.items():
            if any(ex in c_n for ex in exclude_terms):
                continue
            if c_n == alias_n:
                return c

    # depois tenta "contém"
    for alias in aliases:
        alias_n = normalize_text(alias)
        for c, c_n in norm_map.items():
            if any(ex in c_n for ex in exclude_terms):
                continue
            if alias_n in c_n:
                return c

    return None

def parse_date_series(series):
    s = pd.to_datetime(series, errors="coerce", dayfirst=True)
    return s

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

# base para "hoje" (respeita unidade, mas não depende do mês)
df_today_base = df.copy()
if unidade != "Todas" and "Unidade" in df_today_base.columns:
    df_today_base = df_today_base[df_today_base["Unidade"] == unidade]

# =========================
# MÉTRICAS NOVAS (ESTILO PRINT)
# =========================
today = pd.Timestamp.now(tz="America/Sao_Paulo").date()

def today_count(dataframe, col):
    if not col or col not in dataframe.columns:
        return 0
    d = parse_date_series(dataframe[col]).dt.date
    return int((d == today).sum())

contato1_hoje = today_count(df_today_base, data_1_col)
contato2_hoje = today_count(df_today_base, data_2_col)
contato3_hoje = today_count(df_today_base, data_3_col)

primeiro_mes = count_non_empty(df_f[status_1_col]) if status_1_col and status_1_col in df_f.columns else 0
segundo_mes = count_non_empty(df_f[status_2_col]) if status_2_col and status_2_col in df_f.columns else 0
terceiro_mes = count_non_empty(df_f[status_3_col]) if status_3_col and status_3_col in df_f.columns else 0

error_mask = pd.Series(False, index=df_f.index)
for c in [status_1_col, status_2_col, status_3_col]:
    if c and c in df_f.columns:
        error_mask = error_mask | df_f[c].fillna("").astype(str).str.contains("erro", case=False, na=False)

status_com_erro = int(error_mask.sum())
vendas_mes = len(df_f)

# =========================
# CARDS DO TOPO (IGUAL AO PRINT)
# =========================
row1 = st.columns(6)

with row1[0]:
    render_mini_card("💬 1º contato<br>hoje", contato1_hoje, "registros de hoje", "#2d2f92")

with row1[1]:
    render_mini_card("💬 2º contato<br>hoje", contato2_hoje, "registros de hoje", "#2d2f92")

with row1[2]:
    render_mini_card("💬 3º contato<br>hoje", contato3_hoje, "registros de hoje", "#d10b5a")

with row1[3]:
    render_mini_card("📄 Primeiro<br>Contato Mês", primeiro_mes, str(mes) if mes else "-", "#2d2f92")

with row1[4]:
    render_mini_card("📄 Segundo<br>Contato Mês", segundo_mes, str(mes) if mes else "-", "#d10b5a")

with row1[5]:
    render_mini_card("📄 Terceiro<br>Contato Mês", terceiro_mes, str(mes) if mes else "-", "#d10b5a")

row2 = st.columns(2)

with row2[0]:
    render_wide_card("Status com erro", status_com_erro, f"Mês selecionado: {mes}" if mes else "Mês selecionado: -", "#ff4d4f")

with row2[1]:
    render_wide_card("Vendas registradas no mês", vendas_mes, f"Mês Venda: {mes}" if mes else "Mês Venda: -", "#b0005a")

st.divider()

# =========================
# GRÁFICOS
# =========================
g1, g2 = st.columns(2)

# STATUS
with g1:
    st.markdown("### Contatos por status")

    status_total = {}
    for col in [status_1_col, status_2_col, status_3_col]:
        if col and col in df_f.columns:
            for k, v in df_f[col].fillna("").astype(str).str.strip().value_counts().items():
                if k and k.lower() != "nan":
                    status_total[k] = status_total.get(k, 0) + v

    chart = pd.DataFrame(list(status_total.items()), columns=["Status", "Qtd"]) if status_total else pd.DataFrame(columns=["Status", "Qtd"])

    fig = px.bar(
        chart,
        x="Status",
        y="Qtd",
        text="Qtd",
        color="Qtd",
        color_continuous_scale=["#f23b9b", "#a000d4"]
    ) if not chart.empty else px.bar(pd.DataFrame({"Status": [], "Qtd": []}), x="Status", y="Qtd")

    fig.update_layout(
        height=360,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    fig.update_traces(textposition="outside")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# UNIDADE
with g2:
    st.markdown("### Vendas por unidade")

    if "Unidade" in df_f.columns:
        uni = df_f["Unidade"].value_counts().reset_index()
        uni.columns = ["Unidade", "Qtd"]
    else:
        uni = pd.DataFrame(columns=["Unidade", "Qtd"])

    fig2 = px.bar(
        uni,
        x="Unidade",
        y="Qtd",
        text="Qtd",
        color="Qtd",
        color_continuous_scale=["#f23b9b", "#a000d4"]
    ) if not uni.empty else px.bar(pd.DataFrame({"Unidade": [], "Qtd": []}), x="Unidade", y="Qtd")

    fig2.update_layout(
        height=360,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    fig2.update_traces(textposition="outside")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# RAÇAS
# =========================
st.markdown("### Raças mais vendidas")

if "Raça" in df_f.columns:
    raca = df_f["Raça"].value_counts().reset_index()
    raca.columns = ["Raça", "Qtd"]
else:
    raca = pd.DataFrame(columns=["Raça", "Qtd"])

fig3 = px.bar(
    raca,
    x="Raça",
    y="Qtd",
    text="Qtd",
    color="Qtd",
    color_continuous_scale=["#f23b9b", "#a000d4"]
) if not raca.empty else px.bar(pd.DataFrame({"Raça": [], "Qtd": []}), x="Raça", y="Qtd")

fig3.update_layout(
    height=380,
    paper_bgcolor="white",
    plot_bgcolor="white",
    font_color="#111827",
    margin=dict(l=10, r=10, t=10, b=10)
)
fig3.update_traces(textposition="outside")

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig3, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABELA
# =========================
st.markdown("### Dados da planilha")
st.dataframe(df_f, use_container_width=True)

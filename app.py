import streamlit as st
import pandas as pd
import plotly.express as px
import unicodedata
import time
from streamlit_autorefresh import st_autorefresh

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
# SESSION STATE
# =========================
if "app_logado" not in st.session_state:
    st.session_state.app_logado = False

if "page" not in st.session_state:
    st.session_state.page = "operacao"

if "financeiro_logado" not in st.session_state:
    st.session_state.financeiro_logado = False

# mantém apenas o login principal no refresh
if st.query_params.get("auth") == "1":
    st.session_state.app_logado = True

# NÃO usa mais fin_auth pela URL para não pular o login do financeiro

if st.query_params.get("page") == "financeiro":
    st.session_state.page = "financeiro"

# AUTO REFRESH REAL
if st.session_state.app_logado:
    st_autorefresh(interval=5000, key="auto_refresh_dashboard")

# LOGOUT GERAL
if st.query_params.get("logout_app") == "1":
    st.session_state.app_logado = False
    st.session_state.financeiro_logado = False
    st.session_state.page = "operacao"
    st.query_params.clear()
    st.rerun()

# LOGOUT FINANCEIRO
if st.query_params.get("logout_financeiro") == "1":
    st.session_state.financeiro_logado = False
    st.session_state.page = "operacao"
    st.query_params.clear()
    st.query_params["auth"] = "1"
    st.query_params["page"] = "operacao"
    st.rerun()

# =========================
# CSS
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
    display: block;
    background: linear-gradient(135deg, #1D4ED8, #7C3AED);
    color: #F8FAFC !important;
    border-radius: 12px;
    padding: 13px 42px;
    font-weight: 800;
    font-size: 13px;
    text-align: center;
    border: 1px solid rgba(6,182,212,0.35);
    text-decoration: none !important;
    box-shadow:
        0 0 0 2px rgba(29,78,216,0.25),
        0 0 18px rgba(124,58,237,0.45),
        0 0 28px rgba(6,182,212,0.25),
        0 10px 25px rgba(0,0,0,0.35);
    transition: all 0.25s ease;
}

.logout-btn:hover {
    transform: translateY(-2px);
    color: #F8FAFC !important;
    text-decoration: none !important;
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
    box-shadow:
        0 0 0 2px rgba(29,78,216,0.25) !important,
        0 0 18px rgba(124,58,237,0.45) !important,
        0 0 28px rgba(6,182,212,0.25) !important,
        0 10px 25px rgba(0,0,0,0.35) !important;
}

div[data-testid="stPopover"] button p,
div[data-testid="stPopover"] button svg {
    color: #F8FAFC !important;
    fill: #F8FAFC !important;
    font-weight: 800 !important;
}

/* MENU */
div[data-testid="stPopoverBody"] {
    min-width: 330px !important;
    padding: 16px !important;
}

.menu-title {
    font-size: 24px;
    font-weight: 900;
    color: #111827;
    margin-bottom: 6px;
}

.menu-subtitle {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 8px;
}

.menu-footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 8px;
}

div[data-testid="stPopoverBody"] div[data-testid="stLinkButton"] a,
div[data-testid="stPopoverBody"] div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #1B2A6B, #081634) !important;
    color: #F8FAFC !important;
    border-radius: 14px !important;
    min-height: 58px !important;
    padding: 16px 18px !important;
    font-weight: 900 !important;
    font-size: 15px !important;
    border: none !important;
    text-decoration: none !important;
    transition: all 0.25s ease !important;
    transform: scale(1);
    box-shadow:
        inset 5px 0 0 #06B6D4,
        0 10px 20px rgba(15,23,42,0.22) !important;
}

div[data-testid="stPopoverBody"] div[data-testid="stLinkButton"] a:hover,
div[data-testid="stPopoverBody"] div[data-testid="stButton"] button:hover {
    transform: scale(1.04) !important;
    box-shadow:
        inset 5px 0 0 #06B6D4,
        0 14px 28px rgba(15,23,42,0.32),
        0 0 18px rgba(6,182,212,0.35) !important;
}

div[data-testid="stPopoverBody"] div[data-testid="stButton"] button p {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}

/* LOGO */
.logo-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -8px;
}

.logo {
    width: 86px;
    height: 86px;
    border-radius: 50%;
    background: #0F172A;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    box-shadow:
        0 0 0 2px rgba(6,182,212,0.20),
        0 8px 25px rgba(124,58,237,0.35);
    border: 1px solid rgba(6,182,212,0.28);
    text-align: center;
    line-height: 1.1;
}

.logo .a {
    font-weight: 900;
    color: #06B6D4;
    font-size: 12px;
}

.logo .b {
    font-size: 11px;
    font-weight: 900;
    color: #7C3AED;
    letter-spacing: 1px;
    margin-top: 3px;
    text-transform: lowercase;
}

/* LOGIN */
.login-logo-wrap {
    display: flex;
    justify-content: center;
    margin-top: 12px;
    margin-bottom: 14px;
}

.login-logo {
    width: 112px;
    height: 112px;
    border-radius: 50%;
    background: radial-gradient(circle at top left, #111827, #020617 72%);
    border: 2px solid rgba(6,182,212,0.55);
    box-shadow:
        0 0 0 3px rgba(124,58,237,0.12),
        0 0 20px rgba(6,182,212,0.28),
        0 10px 30px rgba(15,23,42,0.30);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    color: #06B6D4;
    font-size: 14px;
    font-weight: 900;
    line-height: 1.15;
}

.login-logo span {
    color: #7C3AED;
    font-size: 12px;
    letter-spacing: 1px;
    margin-top: 2px;
    text-transform: lowercase;
}

.login-access-text {
    text-align: center;
    color: #111827;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 16px;
}

.login-header-card {
    background: #0F172A;
    border-radius: 18px;
    padding: 18px 20px 16px 20px;
    margin-top: 10px;
    margin-bottom: 18px;
    box-shadow:
        0 8px 20px rgba(15,23,42,0.22),
        0 0 22px rgba(6,182,212,0.10);
    border: 1px solid rgba(6,182,212,0.18);
    text-align: center;
}

.login-title {
    font-size: 24px;
    font-weight: 900;
    color: #F8FAFC;
}

.login-subtitle {
    font-size: 13px;
    color: #A1A1AA;
}

div[data-testid="stForm"] {
    background: rgba(255,255,255,0.35);
    border: 1px solid rgba(15,23,42,0.12);
    border-radius: 18px;
    padding: 18px !important;
    box-shadow: 0 10px 24px rgba(15,23,42,0.08);
}

/* CARDS */
.mini-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 14px 16px 10px 16px;
    min-height: 118px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.12);
    margin-bottom: 8px;
    border: 1px solid rgba(15,23,42,0.06);
    transition: all 0.25s ease;
}

.mini-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(0,0,0,0.15);
}

.mini-title {
    font-size: 12px;
    font-weight: 900;
    color: #111827;
    line-height: 1.35;
}

.mini-value {
    font-size: 28px;
    font-weight: 900;
    color: #111827;
    line-height: 1;
    margin-top: 10px;
}

.mini-sub {
    font-size: 11px;
    color: #64748b;
    margin-top: 8px;
}

.wide-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 16px 18px;
    min-height: 116px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.12);
    margin-top: 8px;
    margin-bottom: 8px;
    border: 1px solid rgba(15,23,42,0.06);
}

.wide-title {
    font-size: 18px;
    font-weight: 900;
    color: #111827;
}

.wide-value {
    font-size: 50px;
    font-weight: 900;
    color: #111827;
    line-height: 1;
    margin-top: 8px;
}

.wide-sub {
    font-size: 12px;
    color: #64748b;
    margin-top: 8px;
}

/* GRÁFICOS */
.graph-title-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 14px 20px 12px 20px;
    margin-top: 10px;
    margin-bottom: 10px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.10);
    border: 1px solid rgba(15,23,42,0.06);
}

.graph-title {
    font-size: 19px;
    font-weight: 900;
    color: #111827;
    margin-bottom: 4px;
}

.graph-subtitle {
    font-size: 13px;
    color: #64748b;
}

.chart-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 8px 10px 14px 10px;
    border: 1px solid rgba(15,23,42,0.06);
    box-shadow: 0 8px 18px rgba(0,0,0,0.10);
    margin-bottom: 16px;
}

/* INPUTS */
.stSelectbox label,
.stTextInput label {
    color: #111827 !important;
    font-weight: 800 !important;
}

.stSelectbox > div > div,
.stTextInput > div > div > input {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
    color: #111827 !important;
    border: 1px solid rgba(15,23,42,0.16) !important;
    min-height: 44px !important;
}

div[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #1D4ED8, #7C3AED) !important;
    color: #F8FAFC !important;
    border-radius: 14px !important;
    min-height: 52px !important;
    font-weight: 900 !important;
    font-size: 15px !important;
    border: 1px solid rgba(6,182,212,0.28) !important;
    box-shadow:
        0 0 0 2px rgba(29,78,216,0.12),
        0 10px 22px rgba(15,23,42,0.20) !important;
}

div[data-testid="stButton"] button {
    border-radius: 12px !important;
    font-weight: 900 !important;
}

hr {
    border: 1px solid rgba(15,23,42,0.18);
    margin-top: 28px;
    margin-bottom: 28px;
}

[data-testid="stDataFrame"] {
    background: white;
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# PLANILHA
# =========================
SHEET_ID = "1CewEBIZrU2lcSfeFjAzBJ3mWpXox23vjznbTxJGQ6Xk"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=1, show_spinner=False)
def load_data(cache_buster):
    url_atualizada = f"{URL}&cache_buster={cache_buster}"
    df = pd.read_csv(url_atualizada)
    df.columns = df.columns.str.strip()
    return df

cache_buster = int(time.time())
df = load_data(cache_buster).dropna(how="all")

# =========================
# HELPERS
# =========================
def normalize_text(text):
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    return " ".join(text.split())

def normalize_mes_value(value):
    if pd.isna(value):
        return ""

    s = str(value).strip().replace("\u00a0", "").replace("\u200b", "")

    if s == "" or s.lower() in ["nan", "none"]:
        return ""

    dt = pd.to_datetime(s, errors="coerce", dayfirst=True)
    if pd.notna(dt):
        return dt.strftime("%m/%Y")

    if "/" in s:
        partes = s.split("/")
        if len(partes) >= 2:
            mes = partes[0].strip().zfill(2)
            ano = partes[1].strip()
            if len(ano) == 2:
                ano = "20" + ano
            return f"{mes}/{ano}"

    return s

def get_mes_atual():
    return pd.Timestamp.now(tz="America/Sao_Paulo").strftime("%m/%Y")

def get_default_month_index(options):
    mes_atual = get_mes_atual()
    if mes_atual in options:
        return options.index(mes_atual)
    return 0

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

def parse_money(value):
    if pd.isna(value):
        return 0.0

    s = str(value).strip()

    if s == "":
        return 0.0

    s = s.replace("R$", "").replace(" ", "").replace("\u00a0", "")

    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")

    try:
        return float(s)
    except:
        return 0.0

def money_br(value):
    try:
        value = float(value)
    except:
        value = 0.0

    txt = f"R$ {value:,.2f}"
    txt = txt.replace(",", "X").replace(".", ",").replace("X", ".")
    return txt

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
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font_color="#111827",
        margin=dict(l=10, r=10, t=10, b=20),
        showlegend=False,
        coloraxis_showscale=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=11, color="#64748b"),
            title=dict(font=dict(color="#64748b"))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#E5E7EB",
            zeroline=False,
            tickfont=dict(size=11, color="#64748b"),
            title=dict(font=dict(color="#64748b"))
        )
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#111827"),
        marker_line_width=0
    )

    return fig

# =========================
# CORES
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
# NORMALIZA MÊS
# =========================
if "Mês" in df.columns:
    df["_mes_norm"] = df["Mês"].apply(normalize_mes_value)
else:
    df["_mes_norm"] = ""

# =========================
# COLUNAS
# =========================
status_1_col = find_col(df, ["Status 1º contato", "Status 1 contato", "Status primeiro contato"])
status_2_col = find_col(df, ["Status 2º contato", "Status 2 contato", "Status segundo contato"])
status_3_col = find_col(df, ["Status 3º contato", "Status 3 contato", "Status terceiro contato"])

data_1_col = find_col(df, ["Data 1º contato", "1º contato", "Primeiro contato", "Data primeiro contato"], exclude_terms=["status"])
data_2_col = find_col(df, ["Data 2º contato", "2º contato", "Segundo contato", "Data segundo contato"], exclude_terms=["status"])
data_3_col = find_col(df, ["Data 3º contato", "3º contato", "Terceiro contato", "Data terceiro contato"], exclude_terms=["status"])

vendedora_col = find_col(df, ["Vendedora", "Vendedor", "Consultora", "Consultor", "Responsável", "Responsavel", "Atendente"])
valor_col = find_col(df, ["Valor Filhote", "Valor", "Valor Total", "Total", "Preço", "Preco", "Faturamento"])

# =========================
# LOGIN PRINCIPAL
# =========================
def render_login_principal():
    st.markdown("""
    <div class="login-logo-wrap">
        <div class="login-logo">
            <div>Sua marca</div>
            <span>aqui</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-access-text">
        Dashboard principal • Acesso restrito
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-header-card">
        <div class="login-title">Login do Dashboard</div>
        <div class="login-subtitle">Digite o usuário e senha para acessar o painel principal</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_principal"):
        usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("Senha", placeholder="Digite sua senha", type="password")

        entrar = st.form_submit_button("Entrar no Dashboard", use_container_width=True)

        if entrar:
            if usuario == "oppitech" and senha == "100316Rahi*":
                st.session_state.app_logado = True
                st.session_state.page = "operacao"
                st.session_state.financeiro_logado = False
                st.query_params.clear()
                st.query_params["auth"] = "1"
                st.query_params["page"] = "operacao"
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

# =========================
# MENU
# =========================
def render_top_menu():
    top_col1, top_col2, top_col3 = st.columns([1.2, 8, 2])

    with top_col1:
        with st.popover("☰"):
            st.markdown('<div class="menu-title">Menu</div>', unsafe_allow_html=True)
            st.markdown('<div class="menu-subtitle">Escolha uma área para acessar</div>', unsafe_allow_html=True)
            st.divider()

            st.link_button(
                "📄 Novo Contrato",
                "https://n8n.oppitech.com.br/form/e1269af5-6cac-492c-8919-7d3345fd79fa",
                use_container_width=True
            )

            if st.button("💰 Financeiro", use_container_width=True):
                st.session_state.page = "financeiro"
                st.session_state.financeiro_logado = False
                st.query_params.clear()
                st.query_params["auth"] = "1"
                st.query_params["page"] = "financeiro"
                st.rerun()

            st.markdown('<div class="menu-footer">Painel interno • Oppi Tech</div>', unsafe_allow_html=True)

    return top_col2, top_col3

# =========================
# OPERAÇÃO
# =========================
def render_operacao():
    top_col2, top_col3 = render_top_menu()

    with top_col2:
        st.markdown(f"""
        <div>
            <div class="header-title">⚙️ Operação Comercial</div>
            <div class="header-subtitle">Oppi Tech • Dashboard Premium</div>
            <div class="header-total">Total de registros: {len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with top_col3:
        st.markdown("""
        <a class="logout-btn" href="?logout_app=1" target="_self">Sair</a>
        """, unsafe_allow_html=True)

    meses = sorted([m for m in df["_mes_norm"].dropna().unique() if str(m).strip() != ""])
    unidades = sorted(df["Unidade"].dropna().unique()) if "Unidade" in df.columns else []

    opcoes_mes = ["Todos"] + meses
    index_mes = get_default_month_index(opcoes_mes)

    col1, col2, col3 = st.columns([4, 1, 4])

    with col1:
        mes = st.selectbox("Mês", opcoes_mes, index=index_mes, key="mes_operacao")

    with col2:
        st.markdown("""
        <div class="logo-wrap">
            <div class="logo">
                <div class="a">Sua marca</div>
                <div class="b">aqui</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        unidade = st.selectbox("Unidade", ["Todas"] + unidades, key="unidade_operacao") if unidades else "Todas"

    st.divider()

    df_f = df.copy()

    if mes != "Todos":
        df_f = df_f[df_f["_mes_norm"] == mes]

    if unidade != "Todas" and "Unidade" in df_f.columns:
        df_f = df_f[df_f["Unidade"] == unidade]

    df_today_base = df.copy()

    if unidade != "Todas" and "Unidade" in df_today_base.columns:
        df_today_base = df_today_base[df_today_base["Unidade"] == unidade]

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

    row1 = st.columns(6)

    with row1[0]:
        render_mini_card("💬 1º contato<br>hoje", contato1_hoje, "registros de hoje", AZUL_OPPI)

    with row1[1]:
        render_mini_card("💬 2º contato<br>hoje", contato2_hoje, "registros de hoje", ROXO_TEC)

    with row1[2]:
        render_mini_card("💬 3º contato<br>hoje", contato3_hoje, "registros de hoje", CIANO_DETALHE)

    with row1[3]:
        render_mini_card("📄 Primeiro<br>Contato Mês", primeiro_mes, str(mes), AZUL_OPPI)

    with row1[4]:
        render_mini_card("📄 Segundo<br>Contato Mês", segundo_mes, str(mes), ROXO_TEC)

    with row1[5]:
        render_mini_card("📄 Terceiro<br>Contato Mês", terceiro_mes, str(mes), CIANO_DETALHE)

    row2 = st.columns(2)

    with row2[0]:
        render_wide_card("Status com erro", status_com_erro, f"Mês selecionado: {mes}", LARANJA_ATENCAO)

    with row2[1]:
        render_wide_card("Vendas registradas no mês", vendas_mes, f"Mês Venda: {mes}", VERDE_SUCESSO)

    st.divider()

    g1, g2 = st.columns(2)

    with g1:
        render_graph_header("📞 Contatos por mês", "Distribuição mensal dos 3 contatos")

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

    with g2:
        render_graph_header("🏙️ Vendas por unidade no mês", "Quantidade de vendas registradas por unidade no período selecionado")

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

    with g3:
        render_graph_header("🐶 Serviços mais vendidos", "Top 10 serviços do período filtrado")

        if "Raça" in df_f.columns:
            servicos = (
                df_f["Raça"]
                .fillna("Sem serviço")
                .astype(str)
                .str.strip()
                .replace("", "Sem serviço")
                .value_counts()
                .head(10)
                .reset_index()
            )
            servicos.columns = ["Serviço", "Qtd"]
        else:
            servicos = pd.DataFrame(columns=["Serviço", "Qtd"])

        fig_servicos = px.bar(
            servicos,
            x="Serviço",
            y="Qtd",
            text="Qtd",
            color="Serviço",
            color_discrete_sequence=CORES_GRAFICO
        )

        fig_servicos = apply_bar_layout(fig_servicos, height=370)
        fig_servicos.update_xaxes(tickangle=-28)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_servicos, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with g4:
        render_graph_header("🏆 Vendas por vendedora", "Todas as vendas do período, incluindo sem nome")

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
            vendas_vendedora = pd.DataFrame({"Vendedora": ["Sem coluna de vendedora"], "Qtd": [0]})

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

# =========================
# LOGIN FINANCEIRO
# =========================
def render_financeiro_login():
    st.markdown("""
    <div class="login-logo-wrap">
        <div class="login-logo">
            <div>Sua marca</div>
            <span>aqui</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-access-text">
        Área financeira • Acesso restrito
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-header-card">
        <div class="login-title">Login do Financeiro</div>
        <div class="login-subtitle">Digite o usuário e senha para acessar</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_financeiro"):
        usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
        senha = st.text_input("Senha", placeholder="Digite sua senha", type="password")

        c1, c2 = st.columns(2)

        with c1:
            entrar = st.form_submit_button("Entrar no Financeiro", use_container_width=True)

        with c2:
            voltar = st.form_submit_button("Voltar à Operação", use_container_width=True)

        if voltar:
            st.session_state.page = "operacao"
            st.session_state.financeiro_logado = False
            st.query_params.clear()
            st.query_params["auth"] = "1"
            st.query_params["page"] = "operacao"
            st.rerun()

        if entrar:
            if usuario == "oppitech" and senha == "100316Rahi*":
                st.session_state.financeiro_logado = True
                st.query_params.clear()
                st.query_params["auth"] = "1"
                st.query_params["page"] = "financeiro"
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

# =========================
# FINANCEIRO
# =========================
def render_financeiro_dashboard():
    top_col1, top_col2, top_col3 = st.columns([1.2, 8, 2])

    with top_col1:
        with st.popover("☰"):
            st.markdown('<div class="menu-title">Menu</div>', unsafe_allow_html=True)
            st.markdown('<div class="menu-subtitle">Escolha uma área para acessar</div>', unsafe_allow_html=True)
            st.divider()

            if st.button("⚙️ Operação", use_container_width=True):
                st.session_state.page = "operacao"
                st.query_params.clear()
                st.query_params["auth"] = "1"
                st.query_params["page"] = "operacao"
                st.rerun()

            st.link_button(
                "📄 Novo Contrato",
                "https://n8n.oppitech.com.br/form/e1269af5-6cac-492c-8919-7d3345fd79fa",
                use_container_width=True
            )

            if st.button("🚪 Sair do Financeiro", use_container_width=True):
                st.session_state.financeiro_logado = False
                st.session_state.page = "operacao"
                st.query_params.clear()
                st.query_params["auth"] = "1"
                st.query_params["page"] = "operacao"
                st.rerun()

            st.markdown('<div class="menu-footer">Painel interno • Oppi Tech</div>', unsafe_allow_html=True)

    with top_col2:
        st.markdown(f"""
        <div>
            <div class="header-title">💰 Financeiro</div>
            <div class="header-subtitle">Oppi Tech • Área financeira</div>
            <div class="header-total">Total de registros: {len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with top_col3:
        st.markdown("""
        <a class="logout-btn" href="?auth=1&logout_financeiro=1" target="_self">Sair</a>
        """, unsafe_allow_html=True)

    meses = sorted([m for m in df["_mes_norm"].dropna().unique() if str(m).strip() != ""])
    unidades = sorted(df["Unidade"].dropna().unique()) if "Unidade" in df.columns else []

    opcoes_mes = ["Todos"] + meses
    index_mes = get_default_month_index(opcoes_mes)

    col1, col2, col3 = st.columns([4, 1, 4])

    with col1:
        mes = st.selectbox("Mês", opcoes_mes, index=index_mes, key="mes_financeiro")

    with col2:
        st.markdown("""
        <div class="logo-wrap">
            <div class="logo">
                <div class="a">Sua marca</div>
                <div class="b">aqui</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        unidade = st.selectbox("Unidade", ["Todas"] + unidades, key="unidade_financeiro") if unidades else "Todas"

    st.divider()

    df_fin = df.copy()

    if valor_col and valor_col in df_fin.columns:
        df_fin["_valor"] = df_fin[valor_col].apply(parse_money)
    else:
        df_fin["_valor"] = 0.0

    if mes != "Todos":
        df_fin_mes = df_fin[df_fin["_mes_norm"] == mes].copy()
    else:
        df_fin_mes = df_fin.copy()

    if unidade != "Todas" and "Unidade" in df_fin_mes.columns:
        df_fin_mes = df_fin_mes[df_fin_mes["Unidade"] == unidade]

    faturamento_total = df_fin_mes["_valor"].sum()
    vendas_financeiro = len(df_fin_mes)
    ticket_medio = faturamento_total / vendas_financeiro if vendas_financeiro else 0
    servicos_vendidos = df_fin_mes["Raça"].nunique() if "Raça" in df_fin_mes.columns else 0

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        render_mini_card("💰 Faturamento total", money_br(faturamento_total), str(mes), AZUL_OPPI)

    with k2:
        render_mini_card("🛍️ Vendas no mês", vendas_financeiro, str(mes), ROXO_TEC)

    with k3:
        render_mini_card("📊 Ticket médio", money_br(ticket_medio), "por venda", CIANO_DETALHE)

    with k4:
        render_mini_card("🧩 Serviços vendidos", servicos_vendidos, "no período", AZUL_OPPI)

    st.divider()

    g1, g2 = st.columns(2)

    with g1:
        render_graph_header("🏙️ Faturamento por Unidade", "Faturamento somado por unidade no período")

        if "Unidade" in df_fin_mes.columns:
            fat_unidade = (
                df_fin_mes.groupby("Unidade", dropna=False)["_valor"]
                .sum()
                .reset_index()
                .sort_values("_valor", ascending=False)
            )
            fat_unidade["Unidade"] = fat_unidade["Unidade"].fillna("Sem unidade").astype(str)
        else:
            fat_unidade = pd.DataFrame({"Unidade": [], "_valor": []})

        fig = px.bar(
            fat_unidade,
            x="Unidade",
            y="_valor",
            text=fat_unidade["_valor"].apply(money_br) if not fat_unidade.empty else None,
            color="Unidade",
            color_discrete_sequence=CORES_GRAFICO
        )

        fig = apply_bar_layout(fig, height=390)
        fig.update_yaxes(title="Valor")
        fig.update_xaxes(tickangle=-18)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with g2:
        render_graph_header("💵 Valor por serviço", "Faturamento somado por serviço no período")

        if "Raça" in df_fin_mes.columns:
            fat_servico = (
                df_fin_mes.groupby("Raça", dropna=False)["_valor"]
                .sum()
                .reset_index()
                .sort_values("_valor", ascending=False)
                .head(10)
            )
            fat_servico["Raça"] = fat_servico["Raça"].fillna("Sem serviço").astype(str)
            fat_servico = fat_servico.rename(columns={"Raça": "Serviço"})
        else:
            fat_servico = pd.DataFrame({"Serviço": [], "_valor": []})

        fig2 = px.bar(
            fat_servico,
            x="Serviço",
            y="_valor",
            text=fat_servico["_valor"].apply(money_br) if not fat_servico.empty else None,
            color="Serviço",
            color_discrete_sequence=CORES_GRAFICO
        )

        fig2 = apply_bar_layout(fig2, height=390)
        fig2.update_yaxes(title="Valor")
        fig2.update_xaxes(title="Serviço", tickangle=-28)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    g3, g4 = st.columns(2)

    with g3:
        render_graph_header("🏆 Vendedoras que mais faturaram", "Ranking por faturamento no período")

        if vendedora_col and vendedora_col in df_fin_mes.columns:
            fat_vendedora = (
                df_fin_mes.groupby(vendedora_col, dropna=False)["_valor"]
                .sum()
                .reset_index()
                .sort_values("_valor", ascending=False)
                .head(10)
            )
            fat_vendedora[vendedora_col] = fat_vendedora[vendedora_col].fillna("Sem nome").astype(str)
        else:
            fat_vendedora = pd.DataFrame({"Vendedora": [], "_valor": []})

        nome_vendedora_col = vendedora_col if vendedora_col and vendedora_col in fat_vendedora.columns else "Vendedora"

        fig3 = px.bar(
            fat_vendedora,
            x=nome_vendedora_col,
            y="_valor",
            text=fat_vendedora["_valor"].apply(money_br) if not fat_vendedora.empty else None,
            color=nome_vendedora_col,
            color_discrete_sequence=CORES_GRAFICO
        )

        fig3 = apply_bar_layout(fig3, height=390)
        fig3.update_yaxes(title="Valor")
        fig3.update_xaxes(tickangle=-28)

        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with g4:
        render_graph_header("🧾 Faturamento individual por vendedora", "Valores individuais no período selecionado")

        if not fat_vendedora.empty:
            tabela_vend = fat_vendedora[[nome_vendedora_col, "_valor"]].copy()
            tabela_vend.columns = ["Vendedora", "Faturamento"]
            tabela_vend["Faturamento"] = tabela_vend["Faturamento"].apply(money_br)
        else:
            tabela_vend = pd.DataFrame(columns=["Vendedora", "Faturamento"])

        st.dataframe(tabela_vend, use_container_width=True, hide_index=True)

    st.divider()

    render_graph_header("📈 Faturamento total do ano", "Mensal conforme crescimento da planilha")

    if "_mes_norm" in df_fin.columns:
        fat_ano = (
            df_fin.groupby("_mes_norm", dropna=False)["_valor"]
            .sum()
            .reset_index()
        )
        fat_ano.columns = ["Mês", "Valor"]
        fat_ano = fat_ano[fat_ano["Mês"].astype(str).str.strip() != ""]
    else:
        fat_ano = pd.DataFrame({"Mês": [], "Valor": []})

    fig4 = px.bar(
        fat_ano,
        x="Mês",
        y="Valor",
        text=fat_ano["Valor"].apply(money_br) if not fat_ano.empty else None,
        color_discrete_sequence=[AZUL_OPPI]
    )

    fig4 = apply_bar_layout(fig4, height=430)
    fig4.update_yaxes(title="Valor")
    fig4.update_xaxes(title="Mês")

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ROTEAMENTO
# =========================
if not st.session_state.app_logado:
    render_login_principal()
elif st.session_state.page == "financeiro":
    if st.session_state.financeiro_logado:
        render_financeiro_dashboard()
    else:
        render_financeiro_login()
else:
    render_operacao()

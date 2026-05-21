st.markdown("""
<style>

/* =========================
   BASE
========================= */
.stApp {
    background: #D4D4D4;
}

.block-container {
    padding-top: 0.5rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    max-width: 1240px !important;
}

/* =========================
   HEADER
========================= */
h1, h2, h3 {
    color: #0f172a !important;
    font-weight: 900 !important;
}

[data-testid="stHeader"] {
    background: transparent;
}

/* =========================
   FILTERS (MES / UNIDADE)
========================= */
div[data-testid="stSelectbox"] {
    background: white;
    padding: 10px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}

/* label */
div[data-testid="stSelectbox"] label {
    font-size: 12px !important;
    font-weight: 800 !important;
    color: #334155 !important;
}

/* =========================
   KPI CARDS (SKOOB STYLE)
========================= */
.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 20px rgba(15,23,42,0.06);
    border-left: 6px solid #1d4ed8;
    transition: all .2s ease;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 26px rgba(15,23,42,0.10);
}

.kpi-title {
    font-size: 12px;
    font-weight: 800;
    color: #475569;
}

.kpi-value {
    font-size: 28px;
    font-weight: 900;
    color: #0f172a;
    margin-top: 6px;
}

/* =========================
   SUMMARY CARDS
========================= */
.summary-card {
    background: #fff;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 10px 24px rgba(15,23,42,0.08);
    border-left: 6px solid #be123c;
}

/* =========================
   CHART CONTAINERS
========================= */
.chart-head {
    background: #ffffff;
    border-radius: 16px;
    padding: 14px 18px;
    box-shadow: 0 6px 18px rgba(15,23,42,0.05);
    margin-bottom: 10px;
}

.chart-title {
    font-size: 16px;
    font-weight: 900;
    color: #0f172a;
}

.chart-subtitle {
    font-size: 12px;
    color: #64748b;
}

/* =========================
   PLOTLY CLEAN
========================= */
.js-plotly-plot {
    background: white !important;
    border-radius: 14px;
}

/* =========================
   GRID SPACING
========================= */
.row-widget.stHorizontal {
    gap: 12px !important;
}

/* =========================
   REMOVE STREAMLIT STYLE NOISE
========================= */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: visible;}

</style>
""", unsafe_allow_html=True)

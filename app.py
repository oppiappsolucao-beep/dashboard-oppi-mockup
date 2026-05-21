import streamlit as st
import streamlit.components.v1 as components
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
    background: #d9d9d9;
}

.block-container {
    max-width: 1450px;
    padding-top: 1rem;
}

header[data-testid="stHeader"] {
    background: transparent;
}

div[data-testid="stSelectbox"] label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #3d3d3d !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: white !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    border: none !important;
}

hr {
    border-color: rgba(0,0,0,0.10) !important;
}
</style>
""", unsafe_allow_html=True)


def html_box(html, height):
    components.html(html, height=height)


def kpi_card(title, value, subtitle, red=False, height=112):
    border = "#c00057" if red else "#1f237e"

    html_box(f"""
    <div style="
        background:white;
        border-radius:14px;
        padding:14px 16px;
        min-height:95px;
        border-left:6px solid {border};
        box-shadow:0 2px 8px rgba(0,0,0,0.06);
        font-family:Arial, sans-serif;
        box-sizing:border-box;
    ">
        <div style="font-size:12px;font-weight:800;color:#1d1d1d;margin-bottom:6px;">
            {title}
        </div>

        <div style="font-size:34px;font-weight:900;color:#020617;line-height:1;">
            {value}
        </div>

        <div style="font-size:10px;color:#6b7280;margin-top:8px;">
            {subtitle}
        </div>
    </div>
    """, height)


def chart_header(title, subtitle=""):
    html_box(f"""
    <div style="
        background:white;
        border-radius:14px;
        padding:10px 14px;
        box-shadow:0 2px 8px rgba(0,0,0,0.06);
        font-family:Arial, sans-serif;
    ">
        <div style="font-size:13px;font-weight:900;color:#1f2937;">
            {title}
        </div>
        <div style="font-size:10px;color:#6b7280;margin-top:3px;">
            {subtitle}
        </div>
    </div>
    """, 64)


# =========================================================
# DADOS
# =========================================================

dados = [
    ["05/2026","Cliente 001","Vendedora 1","Campinas","1º contato",4200,"Spitz Alemão"],
    ["05/2026","Cliente 002","Vendedora 2","Campinas","2º contato",6800,"Maltês"],
    ["05/2026","Cliente 003","Vendedora 3","Campinas","3º contato",9100,"Shih Tzu"],
    ["05/2026","Cliente 004","Vendedora 1","Indaiatuba","Venda registrada",12000,"Maine Coon"],
    ["05/2026","Cliente 005","Vendedora 2","Indaiatuba","Venda registrada",8500,"Teckel"],
    ["05/2026","Cliente 006","Vendedora 3","Piracicaba","1º contato",4900,"Chihuahua"],
    ["05/2026","Cliente 007","Vendedora 1","Piracicaba","2º contato",7200,"Spitz Alemão"],
    ["05/2026","Cliente 008","Vendedora 2","Campinas","Venda registrada",9400,"Maltês"],

    ["04/2026","Cliente 009","Vendedora 1","Campinas","1º contato",5100,"Shih Tzu"],
    ["04/2026","Cliente 010","Vendedora 2","Indaiatuba","Venda registrada",11000,"Maine Coon"],
    ["04/2026","Cliente 011","Vendedora 3","Piracicaba","2º contato",4300,"Teckel"],

    ["03/2026","Cliente 012","Vendedora 1","Campinas","3º contato",7800,"Spitz Alemão"],
    ["03/2026","Cliente 013","Vendedora 2","Indaiatuba","Venda registrada",10200,"Maltês"],

    ["02/2026","Cliente 014","Vendedora 1","Campinas","1º contato",6200,"Shih Tzu"],
    ["02/2026","Cliente 015","Vendedora 2","Indaiatuba","Venda registrada",9800,"Maltês"],
    ["02/2026","Cliente 016","Vendedora 3","Piracicaba","3º contato",7400,"Spitz Alemão"],

    ["01/2026","Cliente 017","Vendedora 1","Campinas","2º contato",5900,"Maine Coon"],
    ["01/2026","Cliente 018","Vendedora 2","Indaiatuba","Venda registrada",8700,"Teckel"],
]

df = pd.DataFrame(
    dados,
    columns=["Mês", "Cliente", "Vendedora", "Unidade", "Status", "Valor", "Raça"]
)

# =========================================================
# 🔥 AQUI ESTÁ A MUDANÇA QUE VOCÊ PEDIU
# UNIDADES -> Unidade 1 / 2 / 3
# =========================================================

unidades_originais = sorted(df["Unidade"].unique())

mapa_unidades = {
    unidades_originais[i]: f"Unidade {i+1}"
    for i in range(len(unidades_originais))
}

df["Unidade"] = df["Unidade"].map(mapa_unidades)

unidades = sorted(df["Unidade"].unique())

# =========================================================
# HEADER
# =========================================================

top1, top2, top3 = st.columns([1, 8, 1])

with top1:
    st.button("☰")

with top2:
    html_box("""
    <div style="
        display:flex;
        align-items:center;
        gap:14px;
        font-family:Arial, sans-serif;
    ">
        <div style="font-size:34px;">⚙️</div>

        <div>
            <div style="font-size:30px;font-weight:900;color:#1f2937;">
                Operação
            </div>

            <div style="font-size:11px;color:#6b7280;margin-top:5px;">
                Total de registros: 308
            </div>
        </div>
    </div>
    """, 80)

with top3:
    st.button("Sair")

# =========================================================
# FILTROS
# =========================================================

meses = sorted(df["Mês"].unique(), reverse=True)

f1, logo, f2 = st.columns([5, 1, 5])

with f1:
    mes = st.selectbox("Mês", meses)

with logo:
    html_box("""
    <div style="
        width:74px;
        height:74px;
        border-radius:50%;
        background:white;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        margin:auto;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
        font-family:Arial, sans-serif;
    ">
        <div style="font-size:25px;font-weight:900;color:#1B1D6D;">
            OPPI
        </div>
        <div style="font-size:9px;font-weight:800;color:#c00057;letter-spacing:4px;">
            VISION
        </div>
    </div>
    """, 82)

with f2:
    unidade = st.selectbox("Unidade", ["Todas"] + list(unidades))

df_filtrado = df[df["Mês"] == mes]

if unidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Unidade"] == unidade]

# =========================================================
# KPIs
# =========================================================

contato1 = len(df_filtrado[df_filtrado["Status"] == "1º contato"])
contato2 = len(df_filtrado[df_filtrado["Status"] == "2º contato"])
contato3 = len(df_filtrado[df_filtrado["Status"] == "3º contato"])
vendas_mes = len(df_filtrado[df_filtrado["Status"] == "Venda registrada"])

primeiro_mes = contato1 + 35
segundo_mes = contato2 + 47
terceiro_mes = contato3 + 57

st.divider()

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    kpi_card("💬 1º contato hoje", contato1, "registros de hoje")

with c2:
    kpi_card("💬 2º contato hoje", contato2, "registros de hoje")

with c3:
    kpi_card("💬 3º contato hoje", contato3, "registros de hoje", True)

with c4:
    kpi_card("🧾 Primeiro Contato Mês", primeiro_mes, mes)

with c5:
    kpi_card("🧾 Segundo Contato Mês", segundo_mes, mes, True)

with c6:
    kpi_card("🧾 Terceiro Contato Mês", terceiro_mes, mes, True)

# =========================================================
# GRAFICOS
# =========================================================

st.divider()

gr1, gr2 = st.columns(2)

with gr1:
    chart_header("📞 Contatos por mês")
    st.plotly_chart(
        px.bar(df_filtrado.groupby("Status").size().reset_index(name="Qtd"),
               x="Status", y="Qtd"),
        use_container_width=True
    )

with gr2:
    chart_header("🏢 Vendas por unidade no mês")
    st.plotly_chart(
        px.bar(df_filtrado.groupby("Unidade")["Valor"].sum().reset_index(),
               x="Unidade", y="Valor"),
        use_container_width=True
    )

st.divider()

st.dataframe(df_filtrado, use_container_width=True)

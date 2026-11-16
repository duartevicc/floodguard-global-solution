import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Flood Guard",
    page_icon="🌧️",
    layout="wide"
)

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados/processed/floodguard_dashboard.csv")
    df["data"] = pd.to_datetime(df["data"])
    return df

df = carregar_dados()

# Cabeçalho do dashboard
st.markdown(
    """
    <div style="padding: 20px 0 12px 0;">
        <p style="color: #A78BFA; font-size: 13px; font-weight: 700; letter-spacing: 2px;">
            CITIZENTECH | GLOBAL SOLUTION 2026.2
        </p>
        <h1 style="color: #F8FAFC; font-size: 46px; font-weight: 800; margin: 0;">
            FLOOD GUARD
        </h1>
        <p style="color: #94A3B8; font-size: 18px; margin-top: 10px;">
            Inteligência de dados para análise de alagamentos e inundações urbanas em São Paulo.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Projeto acadêmico | FIAP | Turma 1TSCOB | Grupo Core III"
)
# Menu de navegação
st.sidebar.header("Navegação")

st.sidebar.markdown(
    """
    - [Visão geral](#visao-geral)
    - [Análise temporal](#analise-temporal)
    - [Análise regional](#analise-regional)
    - [Mapa de calor temporal](#mapa-calor-temporal)
    - [Tipos de ocorrências](#tipos-de-ocorrencias)
    - [Distribuição geográfica](#distribuicao-geografica)
    - [Dados detalhados](#dados-detalhados)
    """
)

st.sidebar.divider()

# Filtros
st.sidebar.header("Filtros")

anos = sorted(df["ano"].unique().tolist())

anos_selecionados = st.sidebar.multiselect(
    "Selecione os anos",
    options=anos,
    default=anos
)

subprefeituras = sorted(df["subprefeitura"].unique().tolist())

subprefeituras_selecionadas = st.sidebar.multiselect(
    "Selecione as subprefeituras",
    options=subprefeituras,
    default=subprefeituras
)

# Aplicação dos filtros
df_filtrado = df[
    df["ano"].isin(anos_selecionados)
    & df["subprefeitura"].isin(subprefeituras_selecionadas)
].copy()

# Indicadores
st.divider()
st.markdown('<div id="visao-geral"></div>', unsafe_allow_html=True)
st.header("Visão geral")

st.caption(
    "Indicadores consolidados das ocorrências registradas "
    "no período e nas subprefeituras selecionadas."
)

col1, col2, col3 = st.columns(3)

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric(
            "Total de ocorrências",
            f"{len(df_filtrado):,}".replace(",", ".")
        )

with col2:
    with st.container(border=True):
        st.metric(
            "Anos selecionados",
            df_filtrado["ano"].nunique()
        )

with col3:
    with st.container(border=True):
        st.metric(
            "Subprefeituras com registros",
            df_filtrado["subprefeitura"].nunique()
        )

if df_filtrado.empty:
    st.warning("Nenhuma ocorrência encontrada para os filtros selecionados.")
    st.stop()

# Gráfico de evolução anual
st.divider()
st.markdown('<div id="analise-temporal"></div>', unsafe_allow_html=True)
st.header("Análise temporal")

ocorrencias_ano = (
    df_filtrado.groupby("ano")
    .size()
    .reset_index(name="total")
)

fig_ano = px.bar(
    ocorrencias_ano,
    x="ano",
    y="total",
    title="Ocorrências por ano",
    labels={
        "ano": "Ano",
        "total": "Ocorrências"
    },
    text="total",
    color_discrete_sequence=["#2563EB"]
)

fig_ano.update_xaxes(type="category")

# Espaços reservados para os gráficos
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.plotly_chart(fig_ano, width="stretch")


ocorrencias_mes = (
    df_filtrado.groupby("mes")
    .size()
    .reindex(range(1, 13), fill_value=0)
    .reset_index(name="total")
)

fig_mes = px.line(
    ocorrencias_mes,
    x="mes",
    y="total",
    markers=True,
    title="Ocorrências por mês",
    labels={
        "mes": "Mês",
        "total": "Ocorrências"
    },
    color_discrete_sequence=["#8B5CF6"]
)

fig_mes.update_xaxes(dtick=1)

with col_grafico2:
    st.plotly_chart(fig_mes, width="stretch")

# Ranking de subprefeituras e análise de sazonalidade
st.divider()
st.markdown('<div id="analise-regional"></div>', unsafe_allow_html=True)
st.header("Análise regional e sazonalidade")

col_ranking, col_chuva = st.columns(2)

ranking = (
    df_filtrado["subprefeitura"]
    .value_counts()
    .head(10)
    .reset_index()
)

ranking.columns = ["subprefeitura", "total"]

fig_ranking = px.bar(
    ranking,
    x="total",
    y="subprefeitura",
    orientation="h",
    title="Top 10 subprefeituras",
    labels={
        "total": "Ocorrências",
        "subprefeitura": "Subprefeitura"
    },
    text="total",
    color_discrete_sequence=["#2563EB"]
)

fig_ranking.update_yaxes(categoryorder="total ascending")

with col_ranking:
    st.plotly_chart(fig_ranking, width="stretch")



# Contagem de ocorrências por período
comparacao_chuva = (
    df_filtrado.groupby("periodo_chuvoso")
    .size()
    .reset_index(name="total")
)

# Identificação dos períodos
comparacao_chuva["periodo"] = (
    comparacao_chuva["periodo_chuvoso"]
    .map({
        True: "Período chuvoso",
        False: "Fora do período chuvoso",
        1: "Período chuvoso",
        0: "Fora do período chuvoso"
    })
)

# Criação do gráfico
fig_chuva = px.bar(
    comparacao_chuva,
    x="periodo",
    y="total",
    color="periodo",
    text="total",
    title="Ocorrências por período",
    labels={
        "periodo": "Classificação",
        "total": "Quantidade de ocorrências"
    },
    color_discrete_map={
        "Período chuvoso": "#2563EB",
        "Fora do período chuvoso": "#8B5CF6"
    }
)

with col_chuva:
    st.plotly_chart(fig_chuva, width="stretch")

st.caption(
    "Comparação baseada em registros históricos de "
    "alagamentos e inundações."
)
# Comparação por tipo de ocorrência
st.divider()
st.markdown('<div id="tipos-de-ocorrencias"></div>', unsafe_allow_html=True)
st.header("Tipos de ocorrências")

df_tipos = (
    df_filtrado["ocorrencia"]
    .value_counts()
    .reset_index()
)

df_tipos.columns = ["Tipo", "Total"]

fig_tipos = px.bar(
    df_tipos,
    x="Total",
    y="Tipo",
    orientation="h",
    color="Tipo",
    color_discrete_map={
        "ALAGAMENTO": "#2563EB",
        "INUNDACAO": "#8B5CF6"
    },
    text="Total",
    title="Comparação entre alagamentos e inundações"
)

fig_tipos.update_layout(
    height=350,
    showlegend=False,
    yaxis_title=None
)

st.plotly_chart(fig_tipos, width="stretch")

# Mapa de calor: ocorrências por ano e mês
st.divider()
st.markdown('<div id="mapa-calor-temporal"></div>', unsafe_allow_html=True)
st.header("Mapa de calor temporal")

df_calor = (
    df_filtrado.groupby(["ano", "mes"])
    .size()
    .reset_index(name="total")
)

tabela_calor = df_calor.pivot(
    index="ano",
    columns="mes",
    values="total"
)

tabela_calor = tabela_calor.reindex(
    index=sorted(df_filtrado["ano"].unique()),
    columns=range(1, 13),
    fill_value=0
).fillna(0)

fig_calor = px.imshow(
    tabela_calor,
    labels={
        "x": "Mês",
        "y": "Ano",
        "color": "Ocorrências"
    },
    x=[
        "Jan", "Fev", "Mar", "Abr",
        "Mai", "Jun", "Jul", "Ago",
        "Set", "Out", "Nov", "Dez"
    ],
    y=[str(ano) for ano in tabela_calor.index],
    color_continuous_scale=[
        "#F1F5F9",
        "#93C5FD",
        "#2563EB",
        "#7C3AED"
    ],
    text_auto=True,
    aspect="auto",
    title="Concentração mensal de ocorrências por ano"
)

fig_calor.update_layout(
    height=400,
    coloraxis_colorbar_title="Total",
    yaxis=dict(
        type="category"
    ),
    xaxis=dict(
        type="category"
    )
)

st.plotly_chart(fig_calor, width="stretch")

# Mapa geográfico das ocorrências
st.divider()
st.markdown('<div id="distribuicao-geografica"></div>', unsafe_allow_html=True)
st.header("Distribuição geográfica das ocorrências")

from pyproj import Transformer

# Conversão provisória de UTM para latitude/longitude
transformador = Transformer.from_crs(
    "EPSG:31983",
    "EPSG:4326",
    always_xy=True
)

df_mapa = df_filtrado.dropna(subset=["x", "y"]).copy()

longitude, latitude = transformador.transform(
    df_mapa["x"].to_numpy(),
    df_mapa["y"].to_numpy()
)

df_mapa["latitude"] = latitude
df_mapa["longitude"] = longitude

# Mapa interativo
fig_mapa = px.scatter_map(
    df_mapa,
    lat="latitude",
    lon="longitude",
    hover_name="subprefeitura",
    hover_data=["ano", "mes", "ocorrencia"],
    zoom=9,
    height=550,
    color_discrete_sequence=["#8B5CF6"],
    title="Localização dos registros de alagamentos"
)

fig_mapa.update_layout(
    map_style="carto-darkmatter",
    map_center={"lat": -23.55, "lon": -46.63},
    map_zoom=10,
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)

st.plotly_chart(fig_mapa, width="stretch")

    # Observação sobre as coordenadas
st.caption(
    "Posicionamento geográfico provisório, considerando "
    "SIRGAS 2000 / UTM zona 23S (EPSG:31983). "
    "O sistema de coordenadas deve ser confirmado na fonte original."
)

# Mapa de densidade geográfica
st.subheader("Mapa de densidade de ocorrências")

fig_densidade = px.density_map(
    df_mapa,
    lat="latitude",
    lon="longitude",
    radius=18,
    zoom=10,
    center={"lat": -23.55, "lon": -46.63},
    map_style="carto-darkmatter",
    height=550,
    title="Concentração geográfica de alagamentos e inundações"
)

fig_densidade.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)

st.plotly_chart(fig_densidade, width="stretch")

st.caption(
    "As áreas de maior intensidade representam maior concentração "
    "de registros históricos, não uma previsão de risco."
)

# Tabela de dados
st.divider()
st.markdown('<div id="dados-detalhados"></div>', unsafe_allow_html=True)
st.header("Dados detalhados")

st.dataframe(df_filtrado, width="stretch")
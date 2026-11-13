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

# Cabeçalho
st.title("Flood Guard")
st.subheader("Monitoramento histórico de alagamentos em São Paulo")
st.caption("Análise de ocorrências registradas entre 2020 e 2025")

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
st.header("Visão geral")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total de ocorrências",
    f"{len(df_filtrado):,}".replace(",", ".")
)

col2.metric(
    "Anos selecionados",
    df_filtrado["ano"].nunique()
)

col3.metric(
    "Subprefeituras com registros",
    df_filtrado["subprefeitura"].nunique()
)

if df_filtrado.empty:
    st.warning("Nenhuma ocorrência encontrada para os filtros selecionados.")
    st.stop()

# Gráfico de evolução anual
st.divider()
st.header("Evolução anual")

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
    labels={"ano": "Ano", "total": "Ocorrências"},
    text="total"
)

fig_ano.update_xaxes(type="category")

st.plotly_chart(fig_ano, width="stretch")

# Gráfico de distribuição mensal
st.header("Distribuição mensal")

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
    labels={"mes": "Mês", "total": "Ocorrências"}
)

fig_mes.update_xaxes(dtick=1)

st.plotly_chart(fig_mes, width="stretch")

# Ranking de subprefeituras
st.header("Regiões com mais ocorrências")

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
    text="total"
)

fig_ranking.update_yaxes(categoryorder="total ascending")

st.plotly_chart(fig_ranking, width="stretch")

# Análise de sazonalidade
st.divider()
st.header("Análise de sazonalidade")

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
    }
)

st.plotly_chart(fig_chuva, width="stretch")

st.caption(
    "Comparação baseada em registros históricos de "
    "alagamentos e inundações."
)

# Tabela de dados
st.divider()
st.header("Dados detalhados")

st.dataframe(df_filtrado, width="stretch")
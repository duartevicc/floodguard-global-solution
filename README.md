# Flood Guard — Global Solution 2026.2

## Sobre o projeto

O **Flood Guard** é um projeto acadêmico desenvolvido para a Global Solution 2026.2 da FIAP, dentro da temática **CitizenTech**.

O projeto utiliza análise de dados e técnicas de ciência de dados para estudar ocorrências de alagamentos e inundações no município de São Paulo, buscando identificar padrões temporais, regiões com maior concentração de registros e agrupamentos geográficos.

## Objetivos

- Analisar o histórico de ocorrências de alagamentos e inundações.
- Identificar tendências e padrões de sazonalidade.
- Investigar a distribuição das ocorrências por subprefeitura.
- Aplicar técnicas estatísticas e de aprendizado de máquina.
- Preparar dados para visualização em dashboard.

## Tecnologias utilizadas

- **Python:** linguagem principal de programação.
- **Pandas e NumPy:** tratamento e manipulação dos dados.
- **Matplotlib:** criação de gráficos.
- **SciPy:** análises e testes estatísticos.
- **Scikit-learn:** aplicação do algoritmo K-Means.
- **Jupyter Notebook:** desenvolvimento e documentação das análises.

## Estrutura do repositório

```text
floodguard/
├── dados/
│   ├── ocorrencias_alagamentos_inundacoes_sp_2013_2026.csv
│   └── processed/
│       ├── ocorrencias_tratadas.csv
│       ├── ocorrencias_2020_2025.csv
│       └── floodguard_dashboard.csv
├── graficos/
│   ├── 01_evolucao_anual.png
│   ├── 02_distribuicao_mensal.png
│   ├── 03_ranking_subprefeituras.png
│   └── 04_clusters_geograficos.png
├── GS_1TSCOB_Dados_FloodGuard_CoreIII.ipynb
├── .gitignore
└── README.md
```

## Metodologia

O desenvolvimento da análise está organizado nas seguintes etapas:

1. **Coleta e organização:** utilização de registros históricos de alagamentos e inundações em São Paulo.
2. **Tratamento dos dados:** limpeza, padronização e preparação das informações.
3. **Análise exploratória:** investigação da evolução anual, distribuição mensal e concentração regional.
4. **Análise estatística:** aplicação de teste de hipótese relacionado à sazonalidade.
5. **Agrupamento geográfico:** utilização de K-Means para identificar agrupamentos espaciais.
6. **Preparação para visualização:** exportação de conjuntos de dados tratados para utilização em dashboard.

## Arquivos de dados

| Arquivo | Descrição |
|---|---|
| `ocorrencias_alagamentos_inundacoes_sp_2013_2026.csv` | Base histórica original. |
| `ocorrencias_tratadas.csv` | Base após tratamento e limpeza. |
| `ocorrencias_2020_2025.csv` | Recorte utilizado nas análises do período. |
| `floodguard_dashboard.csv` | Base preparada para construção do dashboard. |

## Como executar

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd floodguard-global-solution
```

Substitua `URL_DO_REPOSITORIO` pela URL do repositório publicado no GitHub.

### 2. Criar um ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install pandas numpy matplotlib scipy scikit-learn ipykernel
```

### 4. Executar o notebook

Abra o arquivo `GS_1TSCOB_Dados_FloodGuard_CoreIII.ipynb` no VS Code ou Jupyter Notebook.

Selecione o ambiente Python configurado e execute as células na ordem apresentada.

## Resultados e visualizações

As análises produzem quatro visualizações principais:

- Evolução anual das ocorrências.
- Distribuição mensal dos registros.
- Ranking de subprefeituras.
- Agrupamentos geográficos identificados por K-Means.

Os gráficos estão disponíveis no diretório `graficos/`.

## Equipe

**Instituição:** FIAP  
**Turma:** 1TSCOB  
**Grupo:** Core III  
**Projeto:** Global Solution 2026.2 — CitizenTech

### Integrantes

- Henrique Montanhas — RM 572145
- Leonardo Reis — RM 569218
- Victoria Duarte — RM 573688

## Finalidade acadêmica

Este repositório foi desenvolvido para fins acadêmicos, como parte da Global Solution 2026.2 da FIAP.
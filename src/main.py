import streamlit as st
import yfinance as yf
from datetime import timedelta
import pandas as pd
import os


@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.download(
        tickers=texto_tickers, period="1d", start="2010-01-01", end="2024-12-01"
    )
    cotacoes_acao = dados_acao["Close"]
    return cotacoes_acao


@st.cache_data
def carregar_tickers_acoes():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "datasets/lista_ativos.csv")
    base_tickers = pd.read_csv(file_path, sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers


acoes = carregar_tickers_acoes()
dados = carregar_dados(empresas=acoes)


st.write(
    """
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos.
"""
)

st.sidebar.header("Filtros")

# Filtro de Ações
lista_acoes = st.sidebar.multiselect(
    label="Ações",
    options=dados.columns,
    placeholder="Escolha as ações para visualizar...",
)
if lista_acoes:
    dados = dados[lista_acoes]

    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

# Filtro de Período
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_datas = st.sidebar.slider(
    label="Selecione o período",
    min_value=data_inicial,
    max_value=data_final,
    value=(data_inicial, data_final),
    step=timedelta(days=1),
)

dados = dados.loc[intervalo_datas[0] : intervalo_datas[1]]

st.line_chart(data=dados)

texto_performance_ativos = ""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes) == 1:
    dados = dados.rename(columns={"Close": acao_unica})


carteira = [1000 for acao in lista_acoes]
total_inicial_carteira = sum(carteira)

for i, acao in enumerate(lista_acoes):
    performance_acao = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_acao = float(performance_acao)

    carteira[i] = carteira[i] * (1 + performance_acao)

    if performance_acao > 0:
        texto_performance_ativos = (
            texto_performance_ativos + f"  \n{acao}: :green[{performance_acao:.1%}]"
        )
    elif performance_acao < 0:
        texto_performance_ativos = (
            texto_performance_ativos + f"  \n{acao}: :red[{performance_acao:.1%}]"
        )
    else:
        texto_performance_ativos = (
            texto_performance_ativos + f"  \n{acao}: {performance_acao:.1%}"
        )

total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inicial_carteira - 1


if performance_carteira > 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: :green[{performance_carteira:.1%}]"
elif performance_carteira < 0:
    texto_performance_carteira = (
        f"Performance da carteira com todos os ativos: :red[{performance_carteira:.1%}]"
    )
else:
    texto_performance_carteira = (
        f"Performance da carteira com todos os ativos: {performance_carteira:.1%}"
    )


st.write(
    f"""
### Performance dos Ativos
Essa foi a performance de cada ativo no período selecionado:

{texto_performance_ativos}

{texto_performance_carteira}
"""
)

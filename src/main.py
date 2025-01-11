import streamlit as st
import yfinance as yf


@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.download(tickers=texto_tickers, period="1d", start="2010-01-01", end="2024-12-01")
    cotacoes_acao = dados_acao["Close"]
    return cotacoes_acao


acoes = [
    "ITUB4.SA",
    "PETR4.SA",
    "MGLU3.SA",
    "VALE3.SA",
    "ABEV3.SA",
    "GGBR4.SA",
]
dados = carregar_dados(empresas=acoes)


lista_acoes = st.multiselect(label="Ações", options=dados.columns, placeholder="Escolha as ações para visualizar...")
if lista_acoes:
    dados = dados[lista_acoes]

    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

st.write(
    """
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos.
"""
)

st.line_chart(data=dados)

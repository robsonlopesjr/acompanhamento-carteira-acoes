import streamlit as st
import yfinance as yf


@st.cache_data
def carregar_dados(empresa):
    dados_acao = yf.Ticker(ticker=empresa)
    cotacoes_acao = dados_acao.history(
        period="1d", start="2010-01-01", end="2024-12-01"
    )["Close"]
    return cotacoes_acao


dados = carregar_dados(empresa="ITUB4.SA")

st.write(
    """
# App Preço de Ações
O gráfico abaixo representa a evolução do preço das ações do Itaú (ITUB4) ao longo dos anos.
"""
)

st.line_chart(data=dados)

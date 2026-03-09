import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Configuração da página do Dashboard
st.set_page_config(page_title="Market Intelligence Dashboard", layout="wide")

st.title("📊 Painel de Inteligência de Mercado")
st.markdown("Monitoramento de ativos em tempo real para suporte à decisão.")

# 1. Busca de Dados (Mesma lógica do seu ETL)
@st.cache_data # Isso faz o site carregar mais rápido
def carregar_dados():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
    response = requests.get(url)
    return pd.DataFrame(response.json())

df = carregar_dados()

# 2. Filtros na Barra Lateral
st.sidebar.header("Filtros de Análise")
moeda_selecionada = st.sidebar.multiselect(
    "Selecione os Ativos:",
    options=df['name'].unique(),
    default=df['name'].unique()[:5]
)

df_filtrado = df[df['name'].isin(moeda_selecionada)]

# 3. Métricas Principais (Exibição visual)
col1, col2, col3 = st.columns(3)
col1.metric("Ativo Top 1", df['name'].iloc[0], f"${df['current_price'].iloc[0]}")
col2.metric("Maior Volume (24h)", df['name'].iloc[0], f"{df['price_change_percentage_24h'].iloc[0]:.2f}%")
col3.metric("Total de Ativos", len(df))

# 4. Gráficos de Impacto
st.subheader("💡 Análise de Market Cap e Preços")

tab1, tab2 = st.tabs(["Comparativo de Preços", "Distribuição de Mercado"])

with tab1:
    fig_preco = px.bar(df_filtrado, x='name', y='current_price', 
                       title="Preço Atual dos Ativos (USD)",
                       labels={'current_price': 'Preço ($)', 'name': 'Ativo'},
                       color='current_price')
    st.plotly_chart(fig_preco, use_container_width=True)

with tab2:
    fig_pizza = px.pie(df_filtrado, values='market_cap', names='name', 
                       title="Participação de Mercado (Market Cap)")
    st.plotly_chart(fig_pizza, use_container_width=True)

# 5. Tabela de Dados Brutos
st.subheader("📄 Tabela de Dados Estruturados")
st.dataframe(df_filtrado[['symbol', 'name', 'current_price', 'market_cap']], use_container_width=True)

st.info("Desenvolvido por Otávio | Foco em Engenharia de Dados")

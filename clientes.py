import streamlit as st
from data_loader import importar_dados
import plotly.express as px
import numpy as np

st.set_page_config(layout='wide')

tabela= importar_dados()

# cabeçalho da página
col1, col2 = st.columns([2,8])

col1.subheader('Análise de Vendas')

col2.subheader('Painel Comercial')
col2.title('Perfil do Compradores')

# menu lateral esquerdo e cards
col3, col4, col5, col6 = st.columns([2,2,3,3])

# menu de navegação
col3.button('1 - Visão Geral')
col3.button('2 - Veículos')
col3.button('3 - Lojas e Região')
#col3.button('4 - Perfil dos compradores')

# card quantidade de vendas
qtde_vendas = len(tabela)
col4.metric('Vendas Analisadas', f'{qtde_vendas:,}')

# card ticket médio
ticket_medio = tabela['price_$'].mean()
col5.metric('Ticket Médio', f'{ticket_medio:,.2f}')

# adiciona coluna faixa de renda
condicoes = [
    tabela['annual_income'] <= 100000,
    (tabela['annual_income'] > 100000) & (tabela['annual_income'] <= 500000),
    (tabela['annual_income'] > 500000) & (tabela['annual_income'] <= 1000000),
    (tabela['annual_income'] > 1000000) & (tabela['annual_income'] <= 1500000),
    (tabela['annual_income'] > 1500000) & (tabela['annual_income'] <= 2000000),
    tabela['annual_income'] > 2000000
]

resultado = ['Até 100 mil', '100 - 500 mil', '500 mil - 1 mi', '1 - 1,5 mi', '1,5 - 2 mi', 'Acima 2 mi']

tabela['income_range']  = np.select(condicoes, resultado, default='Faixa não encontrada')

# card faixa de renda
qtde_faixa_renda = tabela[['income_range', 'price_$']].groupby('income_range', as_index=False).count()
qtde_faixa_renda = qtde_faixa_renda.sort_values(by='price_$', ascending=False).reset_index(drop=True)

col6.metric('Maior faixa de renda', qtde_faixa_renda.iloc[0]['income_range'])
col6.write(f'{qtde_faixa_renda.iloc[0]['price_$']} registros')

# gráficos central e inferiores
col8, col9, col10 = st.columns([2,4,4])

col8.button('4 - Perfil dos compradores')

# grafico distribuição por gênero
qtde_genero = tabela[['gender', 'car_id']].groupby('gender', as_index=False).count()
qtde_genero = qtde_genero.sort_values(by='gender', ascending=False).reset_index(drop=True)

fig_qtde_genero = px.bar(
    qtde_genero,
    y='gender',
    x='car_id',
    orientation='h',
    title='Distribuição por genero'
)
fig_qtde_genero.update_yaxes(autorange='reversed')
col9.plotly_chart(fig_qtde_genero)

# grafico ticket médio por genero
ticket_genero = tabela[['gender', 'price_$']].groupby('gender', as_index=False).mean()
ticket_genero = ticket_genero.sort_values(by='gender', ascending=False).reset_index(drop=True)

fig_ticket_genero = px.bar(
    ticket_genero,
    y='gender',
    x='price_$',
    orientation='h',
    title='Ticket Médio por gênero'
)
fig_ticket_genero.update_yaxes(autorange='reversed')
col10.plotly_chart(fig_ticket_genero)

# gráfico distribuição por faixa de renda

fig_dist_faixa_renda = px.bar(
    qtde_faixa_renda,
    y='income_range',
    x='price_$',
    orientation='h',
    title='Distribuição por faixa de renda'
)

col11, col12 = st.columns([2, 8])

fig_dist_faixa_renda.update_yaxes(autorange='reversed')
col12.plotly_chart(fig_dist_faixa_renda)
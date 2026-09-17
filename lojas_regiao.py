import streamlit as st
from data_loader import importar_dados
import plotly.express as px

st.set_page_config(layout='wide')

tabela= importar_dados()

col1, col2 = st.columns([1.5,7])

col1.subheader('Análise de Vendas')

col2.subheader('Painel Comercial')
col2.title('Lojas e Região')

col3, col4, col5, col6, col7 = st.columns([1.5,1,1,1.5,1.5])

col3.button('1 - Visão Geral')
col3.button('2 - Veículos')
col3.button('3 - Lojas e Região')
col3.button('4 - Perfil dos compradores')


qtde_lojas = len(tabela['dealer_name'].unique())
col4.metric('Lojas', qtde_lojas)

qtde_regiao = len(tabela['dealer_region'].unique())
col5.metric('Região', qtde_regiao)

regiao_lider_venda = tabela[['dealer_region', 'car_id']].groupby('dealer_region', as_index=False).count()
regiao_lider_venda = regiao_lider_venda.sort_values(by='car_id', ascending=False).reset_index(drop=True)

col6.metric('Região Líder', regiao_lider_venda.iloc[0]['dealer_region'])
col6.write(f'{regiao_lider_venda.iloc[0]['car_id']:,} vendas')

# card ticket medio região
maior_ticket_regiao = tabela[['dealer_region', 'price_$']].groupby('dealer_region', as_index=False).mean()
maior_ticket_regiao = maior_ticket_regiao.sort_values(by='price_$', ascending= False).reset_index(drop=True)

col7.metric('Maior ticket regional', f'{maior_ticket_regiao.iloc[0]['price_$']:,.2f}')
col7.write(f"{maior_ticket_regiao.iloc[0]['dealer_region']}")


col8, col9, col10 = st.columns([1.5,3,3])

fig_vendas_regiao = px.bar(
    regiao_lider_venda,
    y='dealer_region',
    x='car_id',
    orientation='h',
    title='Vendas por Região'
)
fig_vendas_regiao.update_yaxes(autorange='reversed')
col9.plotly_chart(fig_vendas_regiao)

faturamento_regiao = tabela[['dealer_region', 'price_$']].groupby('dealer_region', as_index=False).sum()
faturamento_regiao = faturamento_regiao.sort_values(by='price_$', ascending= False).reset_index(drop=True)

fig_faturamento_regiao = px.bar(
    faturamento_regiao,
    y='dealer_region',
    x='price_$',
    orientation='h',
    title='Faturamento por Região'
)
fig_faturamento_regiao.update_yaxes(autorange='reversed')
col10.plotly_chart(fig_faturamento_regiao)

vendas_loja = tabela.groupby('dealer_name', as_index=False)['price_$'].agg(
    vendas = 'count',
    faturamento = 'sum',
    ticket_medio='mean'
)

vendas_loja = vendas_loja.sort_values(by='faturamento', ascending=False).reset_index(drop=True)
vendas_loja = vendas_loja.rename(columns={'dealer_name': 'Lojas', 'vendas':'Vendas', 'faturamento':'Faturamento', 'ticket_medio': 'Ticket Médio'})

st.dataframe(
    vendas_loja[:5],
    column_config={
    'Vendas': st.column_config.NumberColumn('Vendas', format= '%,d'),
    'Faturamento': st.column_config.NumberColumn('Faturamento', format= 'R$ %.2f'),
    'Ticket Médio': st.column_config.NumberColumn('Ticket Médio', format= 'R$ %.2f'),
    },
    hide_index=True
    )
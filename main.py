import streamlit as st
from data_loader import importar_dados
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout='wide')

tabela = importar_dados()

st.subheader('Painel Comercial')
st.title('Visão Geral')
st.write('Resultados de vendas e evolução do negócio')

col0, col1, col2, col3 = st.columns([1.5, 2.5,1,2.5])

col0.write('Análises de Vendas')


faturamento = tabela['price_$'].sum()
col1.metric('Faturamento', f'U$$ {faturamento:,.2f}')

vendas_total = tabela['car_id'].count()
col2.metric('Vendas', f'{vendas_total:,}')

ticket_medio = tabela['price_$'].mean()
col3.metric('Ticket Médio', f'U$$ {ticket_medio:,.2f}')

tabela['year_month'] = tabela['date'].dt.to_period('M')
vendas_22 = tabela[tabela['date'].dt.year == 2022]
vendas_22 = vendas_22[['year_month', 'price_$']].groupby('year_month', as_index=False).sum()
vendas_22['year_month'] = vendas_22['year_month'].dt.to_timestamp()

vendas_23 = tabela[tabela['date'].dt.year == 2023]
vendas_23 = vendas_23[['year_month', 'price_$']].groupby('year_month', as_index=False).sum()
vendas_23['year_month'] = vendas_23['year_month'].dt.to_timestamp()

fig_line = go.Figure(
    data=[
        go.Line(name='Vendas 2022', x=vendas_22['year_month'].dt.strftime('%b'), y=vendas_22['price_$']),
        go.Line(name='Vendas 2023', x=vendas_23['year_month'].dt.strftime('%b'), y=vendas_23['price_$'])
    ]
)
col4, col5 = st.columns([1.5,6])

col4.button('1 - Visão Geral')
col4.button('2 - Veículos')
col4.button('3 - Lojas e Região')
col4.button('4 - Perfil dos compradores')

fig_line.update_layout(barmode='group',
                       title_text='Evolução das Vendas')
col5.plotly_chart(fig_line)

col6, col7, col8 = st.columns([1.5,3,3])

fat_marcas = tabela[['company','price_$']].groupby('company',as_index=False).sum()
fat_marcas = fat_marcas.sort_values(by='price_$', ascending=False).reset_index(drop=True)

fig_fat_marcas = px.bar(fat_marcas,
                        y='company',
                        x='price_$',
                        orientation='h',
                        title='Faturamento por Marca'
                        )
fig_fat_marcas.update_yaxes(autorange='reversed')
col7.plotly_chart(fig_fat_marcas)

vendas_estilo = tabela[['body_style','car_id']].groupby('body_style',as_index=False).count()
vendas_estilo = vendas_estilo.sort_values(by='car_id', ascending=False).reset_index(drop=True)

fig_vendas_estilo = px.bar(vendas_estilo,
                        y='body_style',
                        x='car_id',
                        orientation='h',
                        title='Faturamento por Marca'
                        )
fig_vendas_estilo.update_yaxes(autorange='reversed')
col8.plotly_chart(fig_vendas_estilo)
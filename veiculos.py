import streamlit as st
from data_loader import importar_dados
import plotly.express as px
import numpy as np

tabela = importar_dados()

st.set_page_config(layout='wide')

coluna1, coluna2 = st.columns([1.5,5])

coluna1.write('Análises de Vendas')
coluna1.button('1 - Visão Geral')
coluna1.button('2 - Veículos')
coluna1.button('3 - Lojas e Região')
coluna1.button('4 - Perfil dos compradores')


coluna2.subheader('Painel Comercial')
coluna2.header('Veículos')
coluna2.write('Marcas, modelos e preferencias de veículos')

conteiner = coluna2.container(border=True)
with conteiner:
    coluna_1, coluna_2, coluna_3, coluna_4 = st.columns([1,1,2,2])
    qtde_marcas = tabela['company'].unique()
    coluna_1.metric('Marcas', f'{len(qtde_marcas)}')

    qtde_modelos = tabela['model'].unique()
    coluna_2.metric('Modelos', f'{len(qtde_modelos)}')

    ticket_medio = tabela['price_$'].mean()
    coluna_3.metric('Ticket Médio', f'U$$ {ticket_medio:,.2f}')
    coluna_3.write('Por veículo vendido')

    modelo_mais_vendido = tabela[['model', 'car_id']].groupby('model', as_index=False).count()
    modelo_mais_vendido = modelo_mais_vendido.sort_values(by='car_id', ascending=False).reset_index(drop=True)
    coluna_4.metric(label='Modelo mais vendido', value=modelo_mais_vendido.iloc[0]["model"])
    coluna_4.write(f'{modelo_mais_vendido.iloc[0]["car_id"]} vendas')
    
coluna3, coluna4, coluna5 = st.columns([3,5,5])

marcas_mais_vendidas = tabela[['company', 'car_id']].groupby('company', as_index=False).count()
marcas_mais_vendidas = marcas_mais_vendidas.sort_values(by='car_id', ascending=False)
fig_marcas = px.bar(marcas_mais_vendidas[:5],
                    y='company',
                    x='car_id',
                    orientation='h',
                    title='Marcas mais vendidas')
fig_marcas.update_yaxes(autorange='reversed')
coluna4.plotly_chart(fig_marcas)


fig_modelos = px.bar(modelo_mais_vendido[:5],
                    y='model',
                    x='car_id',
                    orientation='h',
                    title='Modelos mais vendidos')
fig_modelos.update_yaxes(autorange="reversed")
coluna5.plotly_chart(fig_modelos)

tipo_transmissao = tabela[['transmission', 'car_id']].groupby('transmission', as_index=False).count()

fig_transmissao = px.bar(tipo_transmissao,
                         x='transmission',
                         y='car_id',
                         title='Tipo de Transmissão')
coluna4.plotly_chart(fig_transmissao)

tipo_cor = tabela[['color', 'car_id']].groupby('color', as_index=False).count()
tipo_cor = tipo_cor.sort_values('car_id', ascending=False)

fig_cor = px.bar(tipo_cor,
                         x='color',
                         y='car_id',
                         title='Cor')

coluna5.plotly_chart(fig_cor)

condicoes = [
    tabela['price_$'] <= 15000,
    (tabela['price_$'] > 15000) & (tabela['price_$'] <= 25000),
    (tabela['price_$'] > 25000) & (tabela['price_$'] <= 35000),
    (tabela['price_$'] > 35000) & (tabela['price_$'] <= 45000),
    tabela['price_$'] > 45000
]

resultados = ['Até 15 mil', '15 - 25 mil', '25 -35 mil', '35 - 45 mil', 'Acima de 45 mil']

tabela['faixa_price'] = np.select(condicoes, resultados, default='Nenhuma faixa encontrada')

faixa_preco = tabela[['faixa_price','car_id']].groupby('faixa_price', as_index=False).count()
faixa_preco = faixa_preco.sort_values(by='car_id', ascending=False).reset_index(drop=True)

fig_faixa = px.bar(faixa_preco,
                   y='faixa_price',
                   x='car_id',
                   orientation='h',
                   title='Distribuição por faixas de preços')
fig_faixa.update_yaxes(autorange='reversed')
st.plotly_chart(fig_faixa)
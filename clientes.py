import streamlit as st
from data_loader import importar_dados
import plotly.express as px
import numpy as np

st.set_page_config(layout='wide')

tabela= importar_dados()

#=======================================================================
# CABEÇALHO
#=======================================================================
st.subheader('Painel Comercial')
st.title('Perfil do Compradores')

#=======================================================================
# FILTRO
#=======================================================================
ano_selecionado = st.session_state.get("ano", "Todas")
st.write(f'Ano selecionado, {ano_selecionado}')

if ano_selecionado == 'Todos':
    tabela_filtrada = tabela
else:
    tabela_filtrada = tabela[tabela['date'].dt.year == ano_selecionado]

#=======================================================================
# CARDS
#=======================================================================
col1, col2, col3 = st.columns([1,1,1])

# card quantidade de vendas
qtde_vendas = len(tabela_filtrada)
with col1:
    with st.container(border=True):
        st.metric('Vendas Analisadas', f'{qtde_vendas:,}')
        st.write('Registros')

# card ticket médio
ticket_medio = tabela_filtrada['price_$'].mean()
with col2:
    with st.container(border=True):
        st.metric('Ticket Médio', f'{ticket_medio:,.2f}')
        st.write('Preço médio do veículo')

# adiciona coluna faixa de renda
condicoes = [
    tabela_filtrada['annual_income'] <= 100000,
    (tabela_filtrada['annual_income'] > 100000) & (tabela_filtrada['annual_income'] <= 500000),
    (tabela_filtrada['annual_income'] > 500000) & (tabela_filtrada['annual_income'] <= 1000000),
    (tabela_filtrada['annual_income'] > 1000000) & (tabela_filtrada['annual_income'] <= 1500000),
    (tabela_filtrada['annual_income'] > 1500000) & (tabela_filtrada['annual_income'] <= 2000000),
    tabela_filtrada['annual_income'] > 2000000
]
resultado = ['Até 100 mil', '100 - 500 mil', '500 mil - 1 mi', '1 - 1,5 mi', '1,5 - 2 mi', 'Acima 2 mi']
tabela_filtrada['income_range']  = np.select(condicoes, resultado, default='Faixa não encontrada')

# card faixa de renda
qtde_faixa_renda = tabela_filtrada[['income_range', 'price_$']].groupby('income_range', as_index=False).count()
qtde_faixa_renda = qtde_faixa_renda.sort_values(by='price_$', ascending=False).reset_index(drop=True)

with col3:
    with st.container(border=True):
        st.metric('Maior Faixa de Renda', qtde_faixa_renda.iloc[0]['income_range'])
        st.write(f'{qtde_faixa_renda.iloc[0]['price_$']:,} registros')

#=======================================================================
# GRÁFICOS
#=======================================================================
col4, col5 = st.columns([1,1])

# grafico distribuição por gênero
qtde_genero = tabela_filtrada[['gender', 'car_id']].groupby('gender', as_index=False).count()
qtde_genero = qtde_genero.sort_values(by='gender', ascending=False).reset_index(drop=True)

fig_qtde_genero = px.bar(
    qtde_genero,
    y='gender',
    x='car_id',
    orientation='h',
    title='Distribuição por Gênero',
    text='car_id'
)
fig_qtde_genero.update_yaxes(autorange='reversed')
fig_qtde_genero.update_layout(
    xaxis= dict(title=None, showticklabels=False, range=[0, qtde_genero['car_id'].max() * 1.1]),
    yaxis= dict(title=None)
)
fig_qtde_genero.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

with col4:
    with st.container(border=True):
        st.plotly_chart(fig_qtde_genero)

# grafico ticket médio por genero
ticket_genero = tabela_filtrada[['gender', 'price_$']].groupby('gender', as_index=False).mean()
ticket_genero = ticket_genero.sort_values(by='gender', ascending=False).reset_index(drop=True)

fig_ticket_genero = px.bar(
    ticket_genero,
    y='gender',
    x='price_$',
    orientation='h',
    title='Ticket Médio por Gênero',
    text='price_$'
)
fig_ticket_genero.update_yaxes(autorange='reversed')
fig_ticket_genero.update_layout(
    xaxis= dict(title=None, showticklabels=False, range=[0, ticket_genero['price_$'].max() * 1.2]),
    yaxis= dict(title=None)
)
fig_ticket_genero.update_traces(
    texttemplate='R$ %{text:,.2f}',
    textposition='outside'
)
with col5:
    with st.container(border=True):
        st.plotly_chart(fig_ticket_genero)

# gráfico distribuição por faixa de renda

fig_dist_faixa_renda = px.bar(
    qtde_faixa_renda,
    y='income_range',
    x='price_$',
    orientation='h',
    title='Distribuição por Faixa de Renda',
    text='price_$'
)

fig_dist_faixa_renda.update_yaxes(autorange='reversed')
fig_dist_faixa_renda.update_layout(
    xaxis= dict(title=None, showticklabels=False, range=[0, qtde_faixa_renda['price_$'].max() * 1.1]),
    yaxis= dict(title=None)
)
fig_dist_faixa_renda.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

with st.container(border=True):
    st.plotly_chart(fig_dist_faixa_renda)
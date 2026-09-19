import streamlit as st
from data_loader import importar_dados
import plotly.express as px

st.set_page_config(layout='wide')

tabela= importar_dados()


st.subheader('Painel Comercial')
st.title('Lojas e Região')

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
col1, col2, col3, col4 = st.columns([2,2,3,3])

# Quantidade de lojas
qtde_lojas = len(tabela_filtrada['dealer_name'].unique())
with col1:
    with st.container(border=True):
        st.metric('Lojas', qtde_lojas)
        st.write('Nomes distintos')

# Quantidade de regiões
qtde_regiao = len(tabela_filtrada['dealer_region'].unique())
with col2:
    with st.container(border=True):
        st.metric('Região', qtde_regiao)
        st.write('Na base selecionada')

regiao_lider_venda = tabela_filtrada[['dealer_region', 'car_id']].groupby('dealer_region', as_index=False).count()
regiao_lider_venda = regiao_lider_venda.sort_values(by='car_id', ascending=False).reset_index(drop=True)

with col3:
    with st.container(border=True):
        st.metric('Região Líder', regiao_lider_venda.iloc[0]['dealer_region'])
        st.write(f'{regiao_lider_venda.iloc[0]['car_id']:,} vendas')

# card ticket medio região
maior_ticket_regiao = tabela_filtrada[['dealer_region', 'price_$']].groupby('dealer_region', as_index=False).mean()
maior_ticket_regiao = maior_ticket_regiao.sort_values(by='price_$', ascending= False).reset_index(drop=True)

with col4:
    with st.container(border=True):
        st.metric('Maior ticket regional', f'{maior_ticket_regiao.iloc[0]['price_$']:,.2f}')
        st.write(f"{maior_ticket_regiao.iloc[0]['dealer_region']}")

#=======================================================================
# GRÁFICOS
#=======================================================================
col5, col6 = st.columns([1,1])

# Vendas por região
fig_vendas_regiao = px.bar(
    regiao_lider_venda,
    y='dealer_region',
    x='car_id',
    orientation='h',
    title='Vendas por Região',
    text='car_id'
)
fig_vendas_regiao.update_yaxes(autorange='reversed')
fig_vendas_regiao.update_layout(
    xaxis= dict(title=None, showticklabels=False, range=[0, regiao_lider_venda['car_id'].max() * 1.1]),
    yaxis= dict(title=None)
)
fig_vendas_regiao.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)
with col5:
    with st.container(border=True):
        st.plotly_chart(fig_vendas_regiao)

# Faturamento po região
faturamento_regiao = tabela_filtrada[['dealer_region', 'price_$']].groupby('dealer_region', as_index=False).sum()
faturamento_regiao = faturamento_regiao.sort_values(by='price_$', ascending= False).reset_index(drop=True)

fig_faturamento_regiao = px.bar(
    faturamento_regiao,
    y='dealer_region',
    x='price_$',
    orientation='h',
    title='Faturamento por Região',
    text='price_$'
)
fig_faturamento_regiao.update_yaxes(autorange='reversed')
fig_faturamento_regiao.update_layout(
    xaxis= dict(title=None, showticklabels=False, range=[0, faturamento_regiao['price_$'].max() * 1.2]),
    yaxis= dict(title=None)
)
fig_faturamento_regiao.update_traces(
    texttemplate='R$ %{text:,}',
    textposition='outside'
)

with col6:
    with st.container(border=True):
        st.plotly_chart(fig_faturamento_regiao)

vendas_loja = tabela_filtrada.groupby('dealer_name', as_index=False)['price_$'].agg(
    vendas = 'count',
    faturamento = 'sum',
    ticket_medio='mean'
)

# Tabela
vendas_loja = vendas_loja.sort_values(by='faturamento', ascending=False).reset_index(drop=True)
vendas_loja = vendas_loja.rename(columns={'dealer_name': 'Lojas', 'vendas':'Vendas', 'faturamento':'Faturamento', 'ticket_medio': 'Ticket Médio'})
with st.container(border=True):
    st.write('Top 10 Faturamento por Lojas')
    st.dataframe(
        vendas_loja[:10],
        column_config={
        'Vendas': st.column_config.NumberColumn('Vendas', format= '%,d'),
        'Faturamento': st.column_config.NumberColumn('Faturamento', format= 'R$ %.2f'),
        'Ticket Médio': st.column_config.NumberColumn('Ticket Médio', format= 'R$ %.2f'),
        },
        hide_index=True
        )
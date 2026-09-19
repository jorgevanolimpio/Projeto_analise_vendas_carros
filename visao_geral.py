import streamlit as st
from data_loader import importar_dados
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout='wide')

tabela = importar_dados()

#=======================================================================
# CABEÇALHO
#=======================================================================
st.subheader('Painel Comercial')
st.title('Visão Geral')
st.write('Resultados de vendas e evolução do negócio')

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

# Card faturamento
faturamento = tabela_filtrada['price_$'].sum()
with col1:
    with st.container(border=True):
        st.metric('Faturamento', f'U$$ {faturamento:,.2f}')
        st.write('Total no período')

# Card vendas
vendas_total = tabela_filtrada['car_id'].count()
with col2:
    with st.container(border=True):
        st.metric('Vendas', f'{vendas_total:,}')
        st.write('Registros')

# Card ticket médio
ticket_medio = tabela_filtrada['price_$'].mean()
with col3:
    with st.container(border=True):
        st.metric('Ticket Médio', f'U$$ {ticket_medio:,.2f}')
        st.write('Valor médio por veículo')

# Adicionar coluna de ano-mês
tabela_filtrada['year_month'] = tabela_filtrada['date'].dt.to_period('M')

#=======================================================================
# Gráfico
#=======================================================================

#Evolução das vendas
vendas_22 = tabela_filtrada[tabela_filtrada['date'].dt.year == 2022]
vendas_22 = vendas_22[['year_month', 'price_$']].groupby('year_month', as_index=False).sum()
vendas_22['year_month'] = vendas_22['year_month'].dt.to_timestamp()

vendas_23 = tabela_filtrada[tabela_filtrada['date'].dt.year == 2023]
vendas_23 = vendas_23[['year_month', 'price_$']].groupby('year_month', as_index=False).sum()
vendas_23['year_month'] = vendas_23['year_month'].dt.to_timestamp()

fig_line = go.Figure(
    data=[
        go.Line(name='2022', x=vendas_22['year_month'].dt.strftime('%b'), y=vendas_22['price_$']),
        go.Line(name='2023', x=vendas_23['year_month'].dt.strftime('%b'), y=vendas_23['price_$'])
    ]
)


fig_line.update_layout(barmode='group',
                       title_text='Evolução do Faturamneto (U$$)',
                       xaxis =dict(title=None),
                       yaxis= dict(title=None)
                    )
with st.container(border=True):
    st.plotly_chart(fig_line)

col7, col8 = st.columns([1,1])

# Faturamento po marca
fat_marcas = tabela_filtrada[['company','price_$']].groupby('company',as_index=False).sum()
fat_marcas = fat_marcas.sort_values(by='price_$', ascending=False).reset_index(drop=True)

fig_fat_marcas = px.bar(fat_marcas,
                        y='company',
                        x='price_$',
                        orientation='h',
                        title='Faturamento por Marca',
                        text='price_$'
                        )
fig_fat_marcas.update_yaxes(autorange='reversed')
fig_fat_marcas.update_layout(
            xaxis =dict(title=None, showticklabels=False, range=[0, fat_marcas['price_$'].max() * 1.1]),
            yaxis= dict(title=None)
        )
fig_fat_marcas.update_traces(
    texttemplate='U$$ %{text:,.2f}',
    textposition='outside'
)

with col7:
    with st.container(border=True):
        st.plotly_chart(fig_fat_marcas)

# Vendas po estilo
vendas_estilo = tabela_filtrada[['body_style','car_id']].groupby('body_style',as_index=False).count()
vendas_estilo = vendas_estilo.sort_values(by='car_id', ascending=False).reset_index(drop=True)

fig_vendas_estilo = px.bar(vendas_estilo,
                        y='body_style',
                        x='car_id',
                        orientation='h',
                        title='Vendas por Estilo',
                        text='car_id'
                        )
fig_vendas_estilo.update_yaxes(autorange='reversed')
fig_vendas_estilo.update_layout(
    xaxis = dict(title=None, showticklabels=False, range=[0, vendas_estilo['car_id'].max() * 1.1]),
    yaxis= dict(title=None)
    )
fig_vendas_estilo.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

with col8:
    with st.container(border=True):
        st.plotly_chart(fig_vendas_estilo)
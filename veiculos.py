import streamlit as st
from data_loader import importar_dados
import plotly.express as px
import numpy as np

tabela = importar_dados()

st.set_page_config(layout='wide')

st.subheader('Painel Comercial')
st.header('Veículos')
st.write('Marcas, modelos e preferencias de veículos')

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

coluna_1, coluna_2, coluna_3, coluna_4 = st.columns([2,2,3,3])

with coluna_1:
    with st.container(border=True):
        qtde_marcas = tabela_filtrada['company'].unique()
        st.metric('Marcas', f'{len(qtde_marcas)}')
        st.write('Na base selecionada')

with coluna_2:
    with st.container(border=True):
        qtde_modelos = tabela_filtrada['model'].unique()
        st.metric('Modelos', f'{len(qtde_modelos)}')
        st.write('Na base selecionada')

with coluna_3:
    with st.container(border=True):
        ticket_medio = tabela_filtrada['price_$'].mean()
        st.metric('Ticket Médio', f'U$$ {ticket_medio:,.2f}')
        st.write('Por veículo vendido')

with coluna_4:
    with st.container(border=True):
        modelo_mais_vendido = tabela_filtrada[['model', 'car_id']].groupby('model', as_index=False).count()
        modelo_mais_vendido = modelo_mais_vendido.sort_values(by='car_id', ascending=False).reset_index(drop=True)
        st.metric(label='Modelo mais vendido', value=modelo_mais_vendido.iloc[0]["model"])
        st.write(f'{modelo_mais_vendido.iloc[0]["car_id"]} vendas')

#=======================================================================
# GRÁFICOS
#=======================================================================
col1, col2 = st.columns([1,1])

# Marcas mais vendidas
marcas_mais_vendidas = tabela_filtrada[['company', 'car_id']].groupby('company', as_index=False).count()
marcas_mais_vendidas = marcas_mais_vendidas.sort_values(by='car_id', ascending=False)
fig_marcas = px.bar(marcas_mais_vendidas[:5],
                    y='company',
                    x='car_id',
                    orientation='h',
                    title='Marcas mais vendidas',
                    text='car_id')
fig_marcas.update_yaxes(autorange='reversed')
fig_marcas.update_layout(
    xaxis= dict(title=None, showticklabels=False, range=[0, marcas_mais_vendidas['car_id'].max() * 1.1]),
    yaxis= dict(title=None)
)
fig_marcas.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)
with col1:
    with st.container(border=True):
        st.plotly_chart(fig_marcas, use_container_width=True)

# Modelos mais vendidos
fig_modelos = px.bar(modelo_mais_vendido[:5],
                    y='model',
                    x='car_id',
                    orientation='h',
                    title='Modelos mais vendidos',
                    text='car_id')
fig_modelos.update_yaxes(autorange="reversed")
fig_modelos.update_layout(
    xaxis= dict(title=None, showticklabels=False, range=[0, modelo_mais_vendido['car_id'].max() * 1.1]),
    yaxis= dict(title=None)
)
fig_modelos.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)
with col2:
    with st.container(border=True):
        st.plotly_chart(fig_modelos)

# Tipo de transmissão
tipo_transmissao = tabela_filtrada[['transmission', 'car_id']].groupby('transmission', as_index=False).count()

fig_transmissao = px.bar(
                        tipo_transmissao,
                        x='transmission',
                        y='car_id',
                        title='Tipo de Transmissão',
                        text='car_id',
                        
                        barmode='stack'
                    )
# Eixos
fig_transmissao.update_layout(
                    xaxis= dict(title=None),
                    yaxis= dict(title=None, showticklabels=False, range=[0, tipo_transmissao['car_id'].max() * 1.1])
                    )
# Rotulos de dados
fig_transmissao.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)
col3, col4 = st.columns([1,1])

with col3:
    with st.container(border=True):
        st.plotly_chart(fig_transmissao)

# Tipo de transmissão
tipo_cor = tabela_filtrada[['color', 'car_id']].groupby('color', as_index=False).count()
tipo_cor = tipo_cor.sort_values('car_id', ascending=False)

fig_cor = px.bar(
            tipo_cor,
            x='color',
            y='car_id',
            title='Cor',
            text='car_id'
        )
fig_cor.update_layout(
    xaxis= dict(title=None),
    yaxis= dict(title=None, showticklabels=False)
)
fig_cor.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)

with col4:
    with st.container(border=True):
        st.plotly_chart(fig_cor)

# Adiciona coluna de faixa de preço
condicoes = [
    tabela_filtrada['price_$'] <= 15000,
    (tabela_filtrada['price_$'] > 15000) & (tabela_filtrada['price_$'] <= 25000),
    (tabela_filtrada['price_$'] > 25000) & (tabela_filtrada['price_$'] <= 35000),
    (tabela_filtrada['price_$'] > 35000) & (tabela_filtrada['price_$'] <= 45000),
    tabela_filtrada['price_$'] > 45000
    ]
resultados = ['Até 15 mil', '15 - 25 mil', '25 -35 mil', '35 - 45 mil', 'Acima de 45 mil']
tabela_filtrada['price_range'] = np.select(condicoes, resultados, default='Nenhuma faixa encontrada')

# Gráfico barra horizontal faixa de preços
faixa_preco = tabela_filtrada[['price_range','car_id']].groupby('price_range', as_index=False).count()
faixa_preco = faixa_preco.sort_values(by='car_id', ascending=False).reset_index(drop=True)

fig_faixa = px.bar(faixa_preco,
                   y='price_range',
                   x='car_id',
                   orientation='h',
                   title='Distribuição por Faixas de Preços',
                   text='car_id')
fig_faixa.update_yaxes(autorange='reversed')
fig_faixa.update_layout(
    xaxis= dict(title=None, showticklabels=False, range=[0, faixa_preco['car_id'].max() * 1.1]),
    yaxis= dict(title=None)
)
fig_faixa.update_traces(
    texttemplate='%{text:,}',
    textposition='outside'
)
with st.container(border=True):
    st.plotly_chart(fig_faixa)
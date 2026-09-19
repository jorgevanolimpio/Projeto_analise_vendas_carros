import streamlit as st
from data_loader import importar_dados

tabela = importar_dados()

pg = st.navigation({
    'Análise de Vendas': [
        st.Page('visao_geral.py', title='Visão Geral'),
        st.Page('veiculos.py', title='Veículos'),
        st.Page('lojas_regiao.py', title='Lojas e Região'),
        st.Page('clientes.py', title='Perfil do Compradores')
    ]
})

# Filtros globais na sidebar
ano = list(tabela['date'].dt.year.unique())
ano.insert(0, 'Todos')

with st.sidebar:
    #st.divider()
    st.write('Filtro')
    ano = st.selectbox("Ano", ano)

st.session_state["ano"] = ano

pg.run()
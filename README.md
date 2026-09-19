# Dashboard de vendas de veículos

Dashboard desenvolvido em Python com Streamlit para explorar vendas de veículos por período, marca, modelo, concessionária, região e perfil dos compradores. Os gráficos interativos são construídos com Plotly; o tratamento e a agregação dos dados utilizam pandas e NumPy.

## Funcionalidades

O menu lateral oferece quatro páginas e um filtro global por ano, com a opção **Todos** para consultar a base completa.

| Página | Análises disponíveis |
| --- | --- |
| Visão Geral | Faturamento, quantidade de vendas, ticket médio, evolução mensal do faturamento em 2022 e 2023, faturamento por marca e vendas por carroceria. |
| Veículos | Quantidade de marcas e modelos, ticket médio, modelo mais vendido, cinco marcas e modelos mais vendidos, transmissão, cores e faixas de preço. |
| Lojas e Região | Quantidade de lojas e regiões, região líder em vendas, maior ticket regional, vendas e faturamento por região e tabela das dez lojas com maior faturamento. |
| Perfil dos Compradores | Quantidade de vendas analisadas, ticket médio, faixa de renda mais frequente, distribuição por gênero, ticket médio por gênero e distribuição por faixa de renda. |

## Acesse o dashboard

[Abrir o dashboard de vendas de veículos] (https://eo57z8hlf3dyappe9659lt.streamlit.app/clientes)

## Dependências

- Python **3.12 ou superior**. O ambiente local original foi criado com Python 3.14.3.
- Streamlit: interface, navegação e filtro por ano.
- pandas: leitura, tratamento e agrupamento dos dados.
- Plotly: gráficos interativos.
- NumPy: classificação das faixas de preço e renda com `np.select`.

O `requirements.txt` fixa as versões registradas no ambiente local do projeto. As dependências indiretas são instaladas automaticamente pelo pip; o arquivo não é um lockfile completo do ambiente.

## Instalação no Windows

Abra o PowerShell na pasta do projeto e crie o ambiente virtual, caso ainda não exista:

```powershell
py -m venv .venv
```

Instale as dependências utilizando o Python desse ambiente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Esses comandos dispensam a ativação do ambiente virtual. Se o comando `py` não estiver disponível, use `python -m venv .venv` com uma instalação compatível de Python.

## Executar o dashboard

Com o terminal na pasta do projeto:

```powershell
.\.venv\Scripts\python.exe -m streamlit run main.py
```

Acesse o endereço exibido no terminal, normalmente `http://localhost:8501`. Escolha uma página no menu lateral e selecione o ano desejado. Para encerrar o servidor, pressione `Ctrl+C` no terminal.

Inicie a aplicação por `main.py`, que configura a navegação e salva o filtro por ano em `st.session_state`.

### Linux e macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run main.py
```

## Base de dados

O arquivo **`Car Sales.xlsx - car_data.csv`** deve permanecer na pasta raiz do projeto, com esse nome. Apesar de conter `.xlsx` no nome, é um arquivo CSV e é lido com `pd.read_csv`.

A base analisada contém 23.906 registros, de 2 de janeiro de 2022 a 31 de dezembro de 2023. Os principais campos são:

| Campos originais | Conteúdo |
| --- | --- |
| `Car_id`, `Date` | Identificador do registro e data da venda. |
| `Company`, `Model` | Marca e modelo do veículo. |
| `Engine`, `Transmission`, `Color`, `Body Style` | Características do veículo. |
| `Price ($)` | Valor da venda. |
| `Dealer_Name`, `Dealer_Region`, `Dealer_No ` | Nome, região e código registrado da concessionária. |
| `Customer Name`, `Gender`, `Annual Income`, `Phone` | Dados registrados do comprador. |

O cabeçalho original `Dealer_No ` inclui um espaço no final. O carregador utiliza os nomes originais no mapeamento de colunas; ao substituir a base, preserve sua estrutura.

### Tratamento dos dados

O módulo `data_loader.py`:

1. Lê o CSV e renomeia as colunas para os nomes usados no código.
2. Converte as colunas textuais, remove espaços nas extremidades e aplica capitalização de palavras.
3. Converte a data com `pd.to_datetime` e os campos numéricos selecionados para `Int64`.
4. Remove linhas integralmente duplicadas e ordena os registros por data.

As páginas aplicam o filtro por ano antes de calcular seus indicadores. As faixas de preço são até 15 mil, de 15 a 25 mil, de 25 a 35 mil, de 35 a 45 mil e acima de 45 mil. As faixas de renda são até 100 mil, de 100 a 500 mil, de 500 mil a 1 milhão, de 1 a 1,5 milhão, de 1,5 a 2 milhões e acima de 2 milhões. Em ambas as classificações, o limite superior pertence à faixa anterior.

## Estrutura do projeto

```text
projeto_carros/
├── main.py                         # Navegação e filtro global
├── data_loader.py                  # Leitura e tratamento do CSV
├── visao_geral.py                   # Indicadores gerais de vendas
├── veiculos.py                     # Marcas, modelos e características
├── lojas_regiao.py                 # Concessionárias e regiões
├── clientes.py                     # Perfil registrado dos compradores
├── Car Sales.xlsx - car_data.csv    # Base de dados
├── requirements.txt                # Dependências diretas
└── README.md                       # Documentação
```

## Observações sobre os indicadores

- Faturamento corresponde à soma de `Price ($)`; ticket médio corresponde à média desse campo. Quantidade de vendas corresponde à contagem dos registros considerados em cada análise.
- A base é interpretada em dólares (US$). O código atual ainda apresenta rótulos mistos, como `R$` e `U$$`; esses rótulos não representam conversão cambial.
- A quantidade de lojas considera nomes distintos de concessionárias, não unidades físicas identificadas de forma única.
- O perfil dos compradores descreve os registros de vendas, não uma contagem de clientes únicos. A renda anual precisa de validação: 22,06% da base completa apresenta o valor 13.500.
- A base não contém custos, metas, estoque ou leads, portanto não permite calcular lucro, margem, atingimento de metas, giro de estoque ou conversão comercial.

## Solução de problemas

- **CSV não encontrado:** execute o comando a partir da pasta que contém `main.py` e confirme o nome do arquivo de dados.
- **Módulo não encontrado:** instale o `requirements.txt` com o mesmo interpretador utilizado para iniciar o Streamlit.
- **Ambiente virtual inválido após mover o projeto:** recrie o ambiente com uma instalação local compatível de Python e reinstale as dependências.

## Validação desta documentação

As dependências foram identificadas pelos imports dos arquivos Python e suas versões foram conferidas nos metadados do ambiente local. A instalação em um ambiente limpo e a execução completa do dashboard não foram validadas nesta atualização; o interpretador do ambiente virtual retornou erro de acesso ao ser iniciado.

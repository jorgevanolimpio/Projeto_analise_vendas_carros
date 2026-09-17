import pandas as pd

def converter_texto(df, colunas: list):
    for coluna in colunas:
        df[coluna] = df[coluna].astype(str)
    return df

def converter_inteiro(df, colunas: list):
    for coluna in colunas:
        df[coluna] = df[coluna].astype('Int64')
    return df

def padronizar_texto(df, colunas: list):
    for coluna in colunas:
        df[coluna] = df[coluna].str.strip().str.title()
    return df

def converter_data(df, colunas: list):
    for coluna in colunas:
            df[coluna] = pd.to_datetime(df[coluna])
    return df

def importar_dados():
    df = pd.read_csv(r'Car Sales.xlsx - car_data.csv')

    renomear_colunas = {
        'Car_id': 'car_id', 'Date':'date', 'Customer Name':'customer_name', 'Gender':'gender', 'Annual Income':'annual_income', 'Dealer_Name':'dealer_name','Company':'company', 'Model':'model', 'Engine':'engine', 'Transmission':'transmission', 'Color':'color', 'Price ($)':'price_$', 'Dealer_No ':'dealer_no', 'Body Style':'body_style', 'Phone':'phone', 'Dealer_Region':'dealer_region'
    }
    df = df.rename(columns= renomear_colunas)

    colunas_texto = [
        'car_id', 'customer_name', 'gender', 'dealer_name','company', 'model', 'engine', 'transmission', 'color', 'dealer_no', 'body_style', 'dealer_region'
    ]

    colunas_inteiro = [
        'annual_income', 'price_$', 'phone'
    ]

    df = converter_texto(df, colunas_texto)
    df = padronizar_texto(df, colunas_texto)
    df = converter_data(df, ['date'])
    df = converter_inteiro(df, colunas_inteiro)

    # remover duplicados
    df = df.drop_duplicates().reset_index(drop=True)

    df = df.sort_values(by='date').reset_index(drop=True)

    return df
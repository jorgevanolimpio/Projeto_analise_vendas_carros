import pandas as pd

def importar_dados():
    df = pd.read_csv(r'Car Sales.xlsx - car_data.csv')
    
    return df

tabela = importar_dados()
print(tabela)
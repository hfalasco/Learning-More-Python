import pandas as pd

vendas = pd.read_excel("vendas.xlsx", sheet_name="Vendas")

print(vendas.head())
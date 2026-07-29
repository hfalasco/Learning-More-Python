import pandas as pd

dados = [
    ("Janeiro", "Norte", "Eletrônicos", "Notebook", 15, 4200),
    ("Janeiro", "Sul", "Eletrônicos", "Notebook", 18, 4200),
    ("Janeiro", "Sudeste", "Celulares", "Smartphone", 40, 2800),
    ("Janeiro", "Nordeste", "Informática", "Monitor", 22, 950),
    ("Fevereiro", "Norte", "Celulares", "Smartphone", 30, 2800),
    ("Fevereiro", "Sul", "Informática", "Monitor", 28, 950),
    ("Fevereiro", "Sudeste", "Eletrônicos", "Notebook", 21, 4200),
    ("Fevereiro", "Nordeste", "Celulares", "Smartphone", 35, 2800),
    ("Março", "Norte", "Informática", "Monitor", 25, 950),
    ("Março", "Sul", "Celulares", "Smartphone", 45, 2800),
    ("Março", "Sudeste", "Eletrônicos", "Notebook", 20, 4200),
    ("Março", "Nordeste", "Eletrônicos", "Notebook", 14, 4200),
    ("Abril", "Norte", "Celulares", "Smartphone", 42, 2800),
    ("Abril", "Sul", "Eletrônicos", "Notebook", 19, 4200),
    ("Abril", "Sudeste", "Informática", "Monitor", 30, 950),
    ("Abril", "Nordeste", "Celulares", "Smartphone", 38, 2800),
    ("Maio", "Norte", "Eletrônicos", "Notebook", 17, 4200),
    ("Maio", "Sul", "Informática", "Monitor", 33, 950),
    ("Maio", "Sudeste", "Celulares", "Smartphone", 46, 2800),
    ("Maio", "Nordeste", "Eletrônicos", "Notebook", 16, 4200),
    ("Junho", "Norte", "Informática", "Monitor", 29, 950),
    ("Junho", "Sul", "Celulares", "Smartphone", 48, 2800),
    ("Junho", "Sudeste", "Eletrônicos", "Notebook", 24, 4200),
    ("Junho", "Nordeste", "Celulares", "Smartphone", 41, 2800),
]

colunas = ["Mês", "Região", "Categoria", "Produto", "Quantidade", "Preço Unitário"]
df = pd.DataFrame(dados, columns=colunas)
df.to_excel("vendas.xlsx", sheet_name="Vendas", index=False)
print("Planilha criada com sucesso.")

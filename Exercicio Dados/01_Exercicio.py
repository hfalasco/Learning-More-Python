import pandas as pd
import matplotlib.pyplot as plt

vendas= pd.read_excel("vendas.xlsx", sheet_name="Vendas") #Importando o arquivo excel para o pandas

vendas["Faturamento"] = vendas["Quantidade"] * vendas["Preço Unitário"] #Soma de todos os Produtos Unitários multiplicados pela quantidade vendida

#Funcao para calcular o resumo geral das vendas e o que foi pedido no Desafio
def resumo_geral(df):
    resumo = {
        "Quantidade total de vendas": int(df["Quantidade"].sum()),
        "Faturamento total": int(df["Faturamento"].sum()),
    }
    return resumo

#Funcao de produto mais vendido, aprendendo usar groupby e idxmax para encontrar o produto com maior quantidade vendida
def produto_mais_vendido(df):
    produto_mais_vendido = df.groupby("Produto")["Quantidade"].sum().idxmax()
    return produto_mais_vendido

#Mesma fita so que com o faturamento, para encontrar a categoria que mais faturou
def categoria_mais_faturada(df):
    categoria_mais_faturada = df.groupby("Categoria")["Faturamento"].sum().idxmax()
    return categoria_mais_faturada

#primeiro grafico pra mostrar o faturamento por mes, usando groupby e plot do matplotlib
def grafico_faturamento_por_mes(df):
    ordem_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho"]
    faturamento_por_mes_ordenado = df.groupby("Mês")["Faturamento"].sum().reindex(ordem_meses)
    faturamento_por_mes_ordenado.plot(kind="bar", color="purple")
    plt.title("Faturamento por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Faturamento")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#grafico de quantidade por categoria, usando groupby e tambem sort.values para ordenar do maior para o menor, e plot do matplotlib
def grafico_quantidade_por_categoria(df):
    quantidade_por_categoria = df.groupby("Categoria")["Quantidade"].sum()
    quantidade_por_categoria = quantidade_por_categoria.sort_values(ascending=False)
    quantidade_por_categoria.plot(kind="bar", color="lightgreen")
    plt.title("Quantidade Vendida por Categoria")
    plt.xlabel("Categoria")
    plt.ylabel("Quantidade Vendida")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#grafico de faturamento por regiao porem aqui eu usei plt.bar e plt.bar_label para mostrar o valor de cada barra, e tambem sort.values para ordenar do maior para o menor
def grafico_faturamento_por_regiao(df):
    faturamento_por_regiao = df.groupby("Região")["Faturamento"].sum()
    faturamento_por_regiao = faturamento_por_regiao.sort_values(ascending=False)
    plt.title("Faturamento por Região")
    plt.xlabel("Região")
    plt.ylabel("Faturamento")
    plt.xticks(rotation=45)
    plt.tight_layout()
    barras = plt.bar(faturamento_por_regiao.index, faturamento_por_regiao.values, color="orange")
    plt.bar_label(barras, label_type='edge')
    plt.show()



print(resumo_geral(vendas))
print("Produto mais vendido:", produto_mais_vendido(vendas))
print("Categoria mais faturada:", categoria_mais_faturada(vendas))
print("Grafico de Quantidade por Categoria:", grafico_quantidade_por_categoria(vendas))
print("Grafico de Faturamento por Região:", grafico_faturamento_por_regiao(vendas))
grafico_faturamento_por_mes(vendas)
print(vendas.head())
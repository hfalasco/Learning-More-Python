def converter_temperatura(valor, de, para):
    """Realiza conversões básicas de temperatura."""
    if de == "C" and para == "F":
        return (valor * 9/5) + 32
    elif de == "F" and para == "C":
        return (valor - 32) * 5/9
    return valor

def main():
    print("--- Conversor Rápido de Temperatura ---")
    try:
        temp = float(input("Digite o valor: "))
        unidade = input("Converter de (C/F): ").upper()
        
        alvo = "F" if unidade == "C" else "C"
        resultado = converter_temperatura(temp, unidade, alvo)
        
        print(f"Resultado: {temp}°{unidade} é igual a {resultado:.2f}°{alvo}")
    except ValueError:
        print("Erro: Por favor, digite um número válido.")

if __name__ == "__main__":
    main()
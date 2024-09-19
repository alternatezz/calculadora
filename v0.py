def calcular_preco_venda(preco_custo, markup):
    # Definindo as porcentagens e valores fixos
    imposto = 0.04
    comissao = 0.20
    operacional = 0.13
    taxa_embalagem = 4.50

    # Calculando os valores baseados no preço de custo
    valor_imposto = preco_custo * imposto
    valor_comissao = preco_custo * comissao
    valor_operacional = preco_custo * operacional

    # Soma total dos custos adicionais
    soma_custos = preco_custo + valor_imposto + valor_comissao + valor_operacional + taxa_embalagem

    # Preço de venda baseado no markup desejado
    preco_venda = soma_custos / (1 - markup)

    # Lucro (H = B - G)
    lucro = preco_venda - soma_custos

    # Markup real (I = H / B)
    markup_real = lucro / preco_venda

    return preco_venda, soma_custos, lucro, markup_real

def main():
    print("Calculadora de Preço de Venda")
    preco_custo = float(input("Digite o preço de custo: "))
    markup = float(input("Digite o markup desejado (em decimal, por exemplo, 0.30 para 30%): "))

    preco_venda, soma_custos, lucro, markup_real = calcular_preco_venda(preco_custo, markup)

    print(f"\nResultados:")
    print(f"Preço de Venda: R$ {preco_venda:.2f}")
    print(f"Soma dos Custos (G): R$ {soma_custos:.2f}")
    print(f"Lucro (H): R$ {lucro:.2f}")
    print(f"Markup Real (I): {markup_real:.2%}")

if __name__ == "__main__":
    main()

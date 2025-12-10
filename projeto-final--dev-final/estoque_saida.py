#Autor: Eduardo filipe

from datetime import datetime
import json



def salvar_estoque(estoque):
    with open("estoque.json", "w") as f:
        json.dump(estoque, f, indent=4)


def saida_estoque(estoque):
    produto_ou_codigo = input("Digite o nome do produto ou código: ")

    # tenta converter para número (caso seja código)
    try:
        codigo_digitado = int(produto_ou_codigo)
    except:
        codigo_digitado = None

    quantidade = int(input("Quantidade a retirar: "))

    # DATA AUTOMÁTICA
    data = datetime.today().strftime("%d/%m/%Y")

    for item in estoque:

        # verifica nome OU código
        if item['produto'] == produto_ou_codigo or item['codigo'] == codigo_digitado:

            # saída normal
            if item['quantidade'] >= quantidade:
                item['quantidade'] -= quantidade
                item['data_saida'] = data
                salvar_estoque(estoque)
                print("\nSaída registrada com sucesso.")
                return

            # saída parcial
            else:
                print("\nEstoque insuficiente!")
                print(f"Disponível: {item['quantidade']} unidades.")
                opcao = input("Deseja retirar apenas o disponível? (s/n): ")

                if opcao.lower() == "s":
                    item['quantidade'] = 0
                    item['data_saida'] = data
                    salvar_estoque(estoque)
                    print("\nSaída parcial registrada.")
                else:
                    print("\nOperação cancelada.")

                return

    print("\nProduto não encontrado no estoque.")

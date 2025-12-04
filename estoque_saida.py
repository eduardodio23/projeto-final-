
from datetime import datetime
import json
import os
agora = datetime.now()  


def salvar_estoque(estoque):
    with open("estoque.json", "w") as f:
        json.dump(estoque, f, indent=4)


        
def saida_estoque (estoque):
    produto = input("Digite o nome do produto ou código: ")
    quantidade = int(input("Quantidade a retirar: "))
    data = input("Data de saída (DD/MM/AAAA): ")

    for item in estoque:
        if item['produto'] == produto or item['codigo'] == produto:

            # saída normal
            if item['quantidade'] >= quantidade:
                item['quantidade'] -= quantidade
                item['data_saida'] = data
                estoque.salvar_estoque(estoque)
                print("\nSaída registrada.")
                return

            # saída parcial
            else:
                print("\nEstoque insuficiente.")
                print(f"Disponível: {item['quantidade']} unidades.")
                opcao = input("Deseja retirar apenas o disponível? (s/n): ")

                if opcao.lower() == "s":
                    item['quantidade'] = 0
                    item['data_saida'] = data
                    estoque.salvar_estoque(estoque)
                    print("\nSaída parcial registrada.")
                else:
                    print("Operação cancelada.")
                return

    print("\nProduto não encontrado.")
from datetime import datetime
import json
import os
import estoque_saida
agora = datetime.now()
print("Data e hora atuais:", agora.strftime("%d/%m/%Y %H:%M"))





def salvar_estoque(estoque):
    with open("estoque.json", "w") as f:
        json.dump(estoque, f, indent=4)




# CADASTRAR 10 PRODUTOS INICIAIS

from datetime import datetime

def cadastrar_produtos_iniciais():
    estoque = []

    print("\n--- CADASTRO INICIAL DE 10 PRODUTOS ---")

    while len(estoque) < 10:
        print(f"\nCadastro do produto {len(estoque) + 1}:")

        # Nome
        while True:
            produto = input("Nome do produto: ")
            if not produto:
                print("O nome do produto não pode ser vazio. Tente novamente.")
                continue
            if not produto.isalpha():
                print("O nome do produto deve conter apenas letras. Tente novamente.")
                continue
            break

        # Código
        while True:
            codigo = input("Código do produto: ")

            if not codigo:
                print("O código do produto não pode ser vazio. Tente novamente.")
                continue

            if not codigo.isdigit():
                print("O código do produto deve ser numérico. Tente novamente.")
                continue

            if any(item['codigo'] == int(codigo) for item in estoque):
                print("Código já existe. Tente novamente.")
                continue

            codigo = int(codigo)
            break

        # Quantidade
        while True:
            quantidade = input("Quantidade inicial: ")

            if not quantidade:
                print("A quantidade não pode ser vazia. Tente novamente.")
                continue

            if not quantidade.isdigit():
                print("Quantidade deve ser numérica. Tente novamente.")
                continue

            quantidade = int(quantidade)

            if quantidade < 0:
                print("A quantidade não pode ser negativa. Tente novamente.")
                continue

            break

        # Data de entrada
        while True:
            data = input("Data de entrada (DD/MM/AAAA): ")

            if not data:
                print("A data de entrada não pode ser vazia. Tente novamente.")
                continue

            try:
                data_digitada = datetime.strptime(data, "%d/%m/%Y").date()
            except ValueError:
                print("Formato inválido! Use DD/MM/AAAA.")
                continue

            hoje = datetime.today().date()

            if data_digitada > hoje:
                print("A data de entrada não pode ser no futuro. Tente novamente.")
                continue
            if data_digitada < hoje:
                print("A data de entrada não pode ser anterior a hoje. Tente novamente.")
                continue
            break

        # SALVA no estoque
        estoque.append({
    'produto': produto,
    'codigo': codigo,
    'quantidade': quantidade,
    'data_entrada': data,
    'data_saida': ''
})

        
    salvar_estoque(estoque)
    print("\n Os 10 produtos foram cadastrados com sucesso!\n")
    return estoque


# ENTRADA DE ESTOQUE
def entrada_estoque(estoque):
    print("\n--- ENTRADA DE PRODUTO ---")
    produto = input("Digite o nome do produto: ")
    codigo = input("Digite o código do produto: ")
    data = input("Digite a data da entrada (DD/MM/AAAA): ")
    quantidade = int(input("Quantidade a adicionar: "))

    for item in estoque:

        # 1 - Produto existe e o código confere
        if item['produto'] == produto and item['codigo'] == codigo:
            item['quantidade'] += quantidade
            item['data_entrada'] = data
            salvar_estoque(estoque)
            print(f"\nEntrada registrada: +{quantidade} unidades.")
            return

        # 2 - Produto existe, mas o código mudou
        if item['produto'] == produto and item['codigo'] != codigo:
            print("\nO produto já existe, mas o código é diferente.")
            print(f"Código atual: {item['codigo']} — Código novo: {codigo}")

            opcao = int(input("Deseja atualizar o código? (1-sim 2-não): "))

            if opcao == 1:
                item['codigo'] = codigo
                item['quantidade'] += quantidade
                item['data_entrada'] = data
                salvar_estoque(estoque)
                print("\n✔ Código atualizado e quantidade adicionada!")
            else:
                print("\nOperação cancelada.")
            return

        # 3 - Código já existe para outro produto
        if item['codigo'] == codigo and item['produto'] != produto:
            print("\nCódigo pertence a outro produto!")
            return

    print("\n Produto não encontrado no estoque.")







# ==========================================
# CONSULTAR ESTOQUE
# ==========================================
def consultar_estoque(estoque):
    produto = input("Digite o nome do produto ou código: ")

    for item in estoque:
        if item['produto'] == produto or item['codigo'] == produto:
            print("\n--- DADOS DO PRODUTO ---")
            print(f"Produto: {item['produto']}")
            print(f"Código: {item['codigo']}")
            print(f"Quantidade: {item['quantidade']}")
            print(f"Data Entrada: {item['data_entrada']}")
            print(f"Data Saída: {item['data_saida']}")
            return

    print("\nProduto não encontrado.")



# ==========================================
# MENU
# ==========================================
def menu_estoque():

    
     if os.path.exists("estoque.json"):
        
        if os.path.getsize("estoque.json") > 0:
            with open("estoque.json", "r") as f:
                estoque = json.load(f)
        else:
            estoque = cadastrar_produtos_iniciais()
     else:
        estoque = cadastrar_produtos_iniciais()


     while True:
        print("\nMenu de Estoque:")
        print("1. Entrada de Produto")
        print("2. Saída de Produto")
        print("3. Consultar Estoque")
        print("4. Sair")
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            entrada_estoque(estoque)
        elif opcao == 2:
            estoque_saida.saida_estoque(estoque)
        elif opcao == 3:
            consultar_estoque(estoque)
        elif opcao == 4:
            print("Saindo do sistema de estoque.")
            break
        else:
            print("Opção inválida.")



if __name__ == "__main__":
    menu_estoque()

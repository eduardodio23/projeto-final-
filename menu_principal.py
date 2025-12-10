import estoque
import operacional
import financeiro
import rh

def menu_principal():
    while True:
        print("\n------------------------")
        print("MENU SÓCIO MAJORITÁRIO")
        print("------------------------")
        print("1 - Sistema de Estoque")
        print("2 - Sistema Financeiro")
        print("3 - Operacional")
        print("4 - Sessão RH")
        print("5 - Sair")

        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida. Digite um número.")
            continue

        if opcao == 1:
            estoque.menu_estoque()
        elif opcao == 2:
            financeiro.relatorio_financeiro()
        elif opcao == 3:
            operacional.menu()
        elif opcao == 4:
            rh.menu_simples()
        elif opcao == 5:
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executa o menu principal
if __name__ == "__main__":
    menu_principal()

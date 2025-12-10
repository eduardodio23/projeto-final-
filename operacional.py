"""
Modulo: operacinal.py
Autor: Cauan Palmeira
Descrição: Módulo para controle de produção por turnos e gerar relatorio em txt.
"""



from datetime import datetime, timedelta
import os; os.system("cls")
import random
import json

ARQUIVO_JSON = "producao.json"

producao = []

def salvar_producao():
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(producao, arquivo, indent=4, ensure_ascii=False)

def carregar_producao():
    global producao
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            producao = json.load(arquivo)

# Função criada para não repetir o codigo geração de produção

def turno_producao(turno):
    while True:
        try:
         valor = int(input(f"Produção da {turno}:"))
         if valor < 0:
             print("Não pode ser negativo!")
         else:
             return valor
        except ValueError:
            print("Somente número inteiro!")     

# Função principal do codigo, coloquei o modo aleatorio apenas para teste de apresentação, na pratica seria ultilizada apenas o "Manual"


def gerar_producao():
    os.system("cls")

    print("=== MODO DE REGISTRO ===")
    print("= 1 - Manual ")
    print("= 2 - Aleatório ")
    print("========================")
    while True:
        modo = input("Escolha: ")
        if modo in ("1", "2"):
            break
        else:
            print("Opção inválida! Digite 1 ou 2.")
            

    gerar_aleatorio = (modo == "2")

    while True:
        nome = input("Digite o nome do Produto: ").strip()
        if nome:
            break
        else:
            print("Nome inválido! Não pode ficar vazio.")

    while True:
        try:
            data_inicio_str = input("Digite a data inicial (DD/MM/AA): ")
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%y")
            break
        except ValueError:
            print("Data inválida! Use o formato DD/MM/AA.")

    if gerar_aleatorio:
        print("\n Gerando produção aleatória da semana...\n")

    for dia in range(7):
        data_atual = data_inicio + timedelta(days=dia)
        data_formatada = data_atual.strftime("%d/%m/%y")

        print(f"\nData: {data_formatada}")

        if gerar_aleatorio:
            manha = random.randint(20, 100)
            tarde = random.randint(20, 100)
            noite = random.randint(20, 100)

            print(f" Manhã: {manha}")
            print(f" Tarde: {tarde}")
            print(f" Noite: {noite}")
        else:
            manha = turno_producao("manha")
            tarde = turno_producao("tarde")
            noite = turno_producao("noite")

        producao.append({
            "nome": nome,
            "data": data_formatada,
            "manha": manha,
            "tarde": tarde,
            "noite": noite
        })

    print("\n Produto da semana cadastrado com sucesso!")
    print(f" Produção de '{nome}' adicionada à lista.")
    salvar_producao()

# Função basica para excluir a lista com o nome da produção

def excluir_producao():
    os.system("cls")
    
    if not producao:
        print("\nNenhuma produção cadastrada")
        return
    
    print("\n=== PRODUÇÕES REALIZADAS ===")
    
    resumo = {}
    
    for item in producao:
        nome = item["nome"]
        total_dia = item["manha"] + item["tarde"] + item["noite"]
        
        if nome not in resumo:
            resumo[nome] = {
                "dias": 0,
                "total": 0
            }
            
        resumo[nome]["dias"] += 1
        resumo[nome]["total"] += total_dia    
    
    for nome, dados in resumo.items():
        print(f"Nome: {nome}")
        print(f"Quantidade de dias: {dados['dias']}")
        print(f"Total produzido: {dados['total']}")
        print("=" * 20)
        
    nome_excluir = input("\nDigite o nome da produção que deseja excluir (ou ENTER para cancelar): ").strip()

    if not nome_excluir:
        print("Exclusão cancelada.")
        return

    confirmar = input(f"Tem certeza que deseja excluir TODAS as produções de '{nome_excluir}'? (s/n): ").lower()

    if confirmar != "s":
        print("Exclusão cancelada pelo usuário.")
        return

    nova_lista = [item for item in producao if item["nome"].lower() != nome_excluir.lower()]

    if len(nova_lista) == len(producao):
        print("Nome não encontrado.")
    else:
        producao.clear()
        producao.extend(nova_lista)
        print(f"Produções de '{nome_excluir}' excluídas com sucesso!")
    salvar_producao()    
    
# Listagem da Produção podendo ser geral (sem filtro), por nome e periodo, podendo támbem separa por turnos e ordena por data ou maior produção

def listar_producao():
    os.system("cls")
    
    if not producao:
        print("\nNenhuma produção cadastrada")
        return

    print("\n======== LISTAR PRODUÇÃO ========")
    print("1 - Listagem geral (sem filtros)")
    print("2 - Pesquisa por nome do produto")
    print("3 - Listagem por período")
    print("==================================")
    opcao = input("Escolha: ")

    filtrados = []

    if opcao == "1":
        filtrados = producao.copy()

    elif opcao == "2":
        nome_busca = input("Digite o nome do produto: ").strip().lower()
        filtrados = [p for p in producao if p["nome"].lower() == nome_busca]
        if not filtrados:
            print("\nNenhum produto encontrado com esse nome.")
            return

    elif opcao == "3":
        while True:
            try:
                data_inicio = converter_data(input("Digite a data inicial (DD/MM/AA): "))
                data_fim = converter_data(input("Digite a data final (DD/MM/AA): "))
                if data_fim < data_inicio:
                    print("A data final não pode ser menor que a inicial.")
                else:
                    break
            except ValueError:
                print("Data inválida! Use DD/MM/AA.")
        
        filtrados = filtrar_por_data(lambda d: data_inicio <= d <= data_fim)

        if not filtrados:
            print("\nNenhuma produção nesse período.")
            return
    else:
        print("Opção inválida!")
        return

    print("\n=== Filtrar por turno: ===")
    print("1 - Manhã")
    print("2 - Tarde")
    print("3 - Noite")
    print("4 - Todos")
    while True:   
        opcao_turno = input("Escolha: ")
        if opcao_turno in ("1", "2", "3", "4"):
            break
        else:
            print("Opção inválida!")

    
    print("\nOrdenar por:")
    print("1 - Data")
    print("2 - Produção Total")
    while True: 
        opcao_ordem = input("Escolha: ")
        if opcao_ordem in ("1", "2"):
            break
        else:
            print("Opção inválida")

    if opcao_ordem == "1":
        filtrados.sort(key=lambda x: converter_data(x["data"]))
    elif opcao_ordem == "2":
        filtrados.sort(
            key=lambda x: x["manha"] + x["tarde"] + x["noite"],
            reverse=True
        )

    # Impressão do resultado
    print("\n=== RESULTADO DA LISTAGEM ===\n")
    total_geral = 0

    for item in filtrados:
        total_dia = item["manha"] + item["tarde"] + item["noite"]
        total_geral += total_dia

        print(f"Produto: {item['nome']}")
        print(f"Data: {item['data']}")

        if opcao_turno == "1":
            print(f"Manhã: {item['manha']}")
        elif opcao_turno == "2":
            print(f"Tarde: {item['tarde']}")
        elif opcao_turno == "3":
            print(f"Noite: {item['noite']}")
        else:
            print(f"Manhã: {item['manha']}")
            print(f"Tarde: {item['tarde']}")
            print(f"Noite: {item['noite']}")

        print(f"TOTAL DO DIA: {total_dia}")
        print("=" * 18)

    print(f"\nTOTAL GERAL DO RELATÓRIO: {total_geral}")

def converter_data(data_str):
    return datetime.strptime(data_str, "%d/%m/%y")

def filtrar_por_data(condicao):
    filtrados = []
    for item in producao:
        try:
            data_item = converter_data(item["data"])
            if condicao(data_item):
                filtrados.append(item)
        except ValueError:
            continue
    return filtrados

# Calcula a produção podendo separar por tempo e gerando media e qual o melhor dia da produção

def calculo_producao():
    os.system("cls")

    if not producao:
        print("\nNenhuma produção cadastrada.")
        return

    print("\n=== CÁLCULO DE PRODUÇÃO ===")
    print("= 1 - Diário")
    print("= 2 - Semanal")
    print("= 3 - Mensal")
    print("= 4 - Anual")
    print("= 5 - Geral")
    print("=============================")

    opcao = input("Escolha: ")

    if opcao == "1":
        try:
            data_busca = converter_data(input("Digite a data (DD/MM/YY): "))
            filtrados = filtrar_por_data(lambda d: d == data_busca)
        except ValueError:
            print("Data inválida!")
            return

    elif opcao == "2":
        try:
            data_inicio = converter_data(input("Digite a data inicial da semana (DD/MM/YY): "))
            filtrados = filtrar_por_data(
                lambda d: data_inicio <= d <= data_inicio + timedelta(days=6)
            )
        except ValueError:
            print("Data inválida!")
            return

    elif opcao == "3":
        try:
            mes = int(input("Digite o mês (MM): "))
            ano = int(input("Digite o ano (YY): "))
            filtrados = filtrar_por_data(lambda d: d.month == mes and d.year % 100 == ano)
        except ValueError:
            print("Mês e ano inválidos!")
            return

    elif opcao == "4":
        try:
            ano = int(input("Digite o ano (YY): "))
            filtrados = filtrar_por_data(lambda d: d.year % 100 == ano)
        except ValueError:
            print("Ano inválido!")
            return

    elif opcao == "5":
        filtrados = producao.copy()

    else:
        print("Opção inválida!")
        return

    if not filtrados:
        print("\nNenhuma produção encontrada para esse período.")
        return

    total_geral = 0
    total_manha = 0
    total_tarde = 0
    total_noite = 0

    melhor_dia = None
    maior_producao_dia = 0

    for item in filtrados:
        total_dia = item["manha"] + item["tarde"] + item["noite"]

        total_geral += total_dia
        total_manha += item["manha"]
        total_tarde += item["tarde"]
        total_noite += item["noite"]

        if total_dia > maior_producao_dia:
            maior_producao_dia = total_dia
            melhor_dia = item["data"]

    total_dias = len(filtrados)

    media_diaria = total_geral / total_dias
    media_manha = total_manha / total_dias
    media_tarde = total_tarde / total_dias
    media_noite = total_noite / total_dias

    turnos = {
        "Manhã": total_manha,
        "Tarde": total_tarde,
        "Noite": total_noite
    }

    melhor_turno, maior_turno_valor = max(turnos.items(), key=lambda x: x[1])

    print("\n=== RELATÓRIO DE PRODUÇÃO ===")
    print(f"Total do período: {total_geral}")
    print(f"Média por dia: {media_diaria:.2f}")

    print("\nMÉDIA POR TURNO:")
    print(f"Manhã: {media_manha:.2f}")
    print(f"Tarde: {media_tarde:.2f}")
    print(f"Noite: {media_noite:.2f}")

    print("\nDESTAQUES:")
    print(f"Melhor dia: {melhor_dia} com {maior_producao_dia}")
    print(f"Melhor turno do período: {melhor_turno} ({maior_turno_valor})")

    input("\nPressione ENTER para voltar ao menu...")
    
# Simula uma produção em 100% de produçãos nos turnos e tendo o aumento de 50% no noturno com as produçoes ja gerada no sistema

def simulacao_ideal():
    os.system("cls")

    if not producao:
        print("\nNenhuma produção real cadastrada para simulação.")
        input("\nPressione ENTER para voltar ao menu...")
        return

    print("\n=== SIMULAÇÃO DE PRODUÇÃO IDEAL ===\n")
    print("1 - Comparar com TODA a produção")

    print("2 - Comparar com UM produto específico")
    
    while True:
     try:
        opcao = (input("Escolha: "))
        if opcao in ("1", "2"):
            break
        print("Digite apenas 1 ou 2.")
     except ValueError:
        print("Digite uma opção valida!")


    capacidade_2_turnos = 500
    aumento_terceiro_turno = capacidade_2_turnos * 0.5
    ideal_mensal = capacidade_2_turnos + aumento_terceiro_turno 

    ideal = {
        "diaria": round(ideal_mensal / 30, 2),
        "semanal": round(ideal_mensal / 4, 2),
        "mensal": ideal_mensal,
        "anual": ideal_mensal * 12
    }

    total_real = 0
    dias_reais = set()

    if opcao == "1":
        for item in producao:
            total_dia = item["manha"] + item["tarde"] + item["noite"]
            total_real += total_dia
            dias_reais.add(item["data"])

        titulo = "GERAL (TODOS OS PRODUTOS)"

    elif opcao == "2":
        os.system("cls")
        print("\nPRODUTOS DISPONÍVEIS:\n")

        produtos_disponiveis = set()
        for item in producao:
            produtos_disponiveis.add(item["nome"])

        for nome in produtos_disponiveis:
            print(f"- {nome}")

        produto_escolhido = input("\nDigite o nome do produto: ")

        for item in producao:
            if item["nome"].lower() == produto_escolhido.lower():
                total_dia = item["manha"] + item["tarde"] + item["noite"]
                total_real += total_dia
                dias_reais.add(item["data"])

        if not dias_reais:
            print("\nProduto não encontrado.")
            input("\nPressione ENTER para voltar ao menu...")
            return

        titulo = f"PRODUTO: {produto_escolhido}"

    else:
        print("\nOpção inválida.")
        input("\nPressione ENTER para voltar ao menu...")
        return


    total_dias = len(dias_reais)

    media_diaria_real = total_real / total_dias

    real = {
        "diaria": round(media_diaria_real, 2),
        "semanal": round(media_diaria_real * 7, 2),
        "mensal": round(media_diaria_real * 30, 2),
        "anual": round(media_diaria_real * 365, 2)
    }

    eficiencia = {
        periodo: round((real[periodo] / ideal[periodo]) * 100, 2)
        for periodo in ideal
    }

    os.system("cls")
    print(f"\n=== RESULTADO DA SIMULAÇÃO - {titulo} ===\n")

    print("Capacidade base (2 turnos): 500 unidades/mês")
    print("Acréscimo do 3º turno (50%): 250 unidades")
    print(f"Capacidade TOTAL (3 turnos): {ideal_mensal} unidades/mês\n")

    print("--- PRODUÇÃO IDEAL ---")
    for p, v in ideal.items():
        print(f"{p.capitalize():7}: {v:.2f}")

    print("\n--- PRODUÇÃO REAL ---")
    for p, v in real.items():
        print(f"{p.capitalize():7}: {v:.2f}")

    print("\n--- EFICIÊNCIA ---")
    for p, v in eficiencia.items():
        print(f"{p.capitalize():7}: {v:.2f}%")

    diferenca = round(real["mensal"] - ideal["mensal"], 2)

    print("\n--- RESULTADO FINAL ---")
    if diferenca < 0:
        print(f"Meta NÃO atingida. Faltaram {abs(diferenca):.2f} unidades.")
    elif diferenca == 0:
        print("Meta exatamente atingida!")
    else:
        print(f"Meta SUPERADA! Excedente de {diferenca:.2f} unidades.")

    print("\n==============================")
    input("\nPressione ENTER para voltar ao menu...")
    
# Parte final do codigo gerando relatorio com lista de produção, media e comparação com o ideal, podendo ser com todos as produções ou escolhendo a produção em .txt
    
def relatorio_producao():
    os.system("cls")

    if not producao:
        print("\nNenhuma produção real cadastrada.")
        input("\nPressione ENTER para voltar ao menu...")
        return

    print("\n === RELATÓRIO DE PRODUÇÃO === \n")
    print("1 - Relatório GERAL (todos os produtos)")
    print("2 - Relatório por PRODUTO específico")

    while True:
        try:
            opcao = int(input("Escolha: "))
            if opcao in (1, 2):
                break
            print(" Digite apenas 1 ou 2.")
        except ValueError:
            print(" Somente números.")

   
    capacidade_2_turnos = 500
    aumento_terceiro_turno = capacidade_2_turnos * 0.5
    ideal_mensal = capacidade_2_turnos + aumento_terceiro_turno  

    ideal = {
        "diaria": round(ideal_mensal / 30, 2),
        "semanal": round(ideal_mensal / 4, 2),
        "mensal": ideal_mensal,
        "anual": ideal_mensal * 12
    }

    if opcao == 1:
        total_real = 0
        dias_reais = set()
        produtos = {}

        print("\n--- LISTA COMPLETA DA PRODUÇÃO ---")

        for item in producao:
            total_dia = item["manha"] + item["tarde"] + item["noite"]
            total_real += total_dia
            dias_reais.add(item["data"])

            nome = item["nome"]
            if nome not in produtos:
                produtos[nome] = []
            produtos[nome].append(total_dia)

            print(f"\nProduto: {nome}")
            print(f"Data: {item['data']}")
            print(f"Manhã: {item['manha']} | Tarde: {item['tarde']} | Noite: {item['noite']}")
            print(f"TOTAL DO DIA: {total_dia}")

        total_dias = len(dias_reais)
        media_geral = total_real / total_dias

        real = {
            "diaria": round(media_geral, 2),
            "semanal": round(media_geral * 7, 2),
            "mensal": round(media_geral * 30, 2),
            "anual": round(media_geral * 365, 2)
        }

        eficiencia = {
            periodo: round((real[periodo] / ideal[periodo]) * 100, 2)
            for periodo in ideal
        }

        bateu_meta = "SIM" if real["mensal"] >= ideal["mensal"] else "NÃO"

        print("\n--- PRODUÇÃO IDEAL ---")
        for p, v in ideal.items():
            print(f"{p.capitalize():7}: {v:.2f}")

        print("\n--- PRODUÇÃO REAL GERAL ---")
        for p, v in real.items():
            print(f"{p.capitalize():7}: {v:.2f}")

        print("\n--- EFICIÊNCIA GERAL ---")
        for p, v in eficiencia.items():
            print(f"{p.capitalize():7}: {v:.2f}%")

        print(f"\nMETA ATINGIDA? {bateu_meta}")

        print("\n--- MÉDIA POR PRODUTO ---")
        for nome, valores in produtos.items():
            media_produto = sum(valores) / len(valores)
            print(f"{nome}: média de {media_produto:.2f}")

        data_hora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        nome_arquivo = f"relatorio_geral_{data_hora}.txt"

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("=== RELATÓRIO GERAL DE PRODUÇÃO ===\n\n")

            arquivo.write("LISTA COMPLETA DA PRODUÇÃO\n")
            for item in producao:
                total_dia = item["manha"] + item["tarde"] + item["noite"]
                arquivo.write(f"\nProduto: {item['nome']}\n")
                arquivo.write(f"Data: {item['data']}\n")
                arquivo.write(f"Manhã: {item['manha']} | Tarde: {item['tarde']} | Noite: {item['noite']}\n")
                arquivo.write(f"TOTAL DO DIA: {total_dia}\n")

            arquivo.write("\n\nPRODUÇÃO IDEAL\n")
            for p, v in ideal.items():
                arquivo.write(f"{p.capitalize():7}: {v:.2f}\n")

            arquivo.write("\nPRODUÇÃO REAL GERAL\n")
            for p, v in real.items():
                arquivo.write(f"{p.capitalize():7}: {v:.2f}\n")

            arquivo.write("\nEFICIÊNCIA GERAL\n")
            for p, v in eficiencia.items():
                arquivo.write(f"{p.capitalize():7}: {v:.2f}%\n")

            arquivo.write(f"\nMETA ATINGIDA? {bateu_meta}\n")

        print("\n Arquivo 'relatorio_geral.txt' salvo com sucesso!")


    elif opcao == 2:
        nome_busca = input("\nDigite o nome do produto: ").strip().lower()

        filtrados = [p for p in producao if p["nome"].lower() == nome_busca]

        if not filtrados:
            print("\nProduto não encontrado.")
            input("\nPressione ENTER para voltar...")
            return

        total_real = 0
        dias_reais = set()

        print(f"\n=== LISTA DO PRODUTO: {nome_busca.upper()} ===")

        for item in filtrados:
            total_dia = item["manha"] + item["tarde"] + item["noite"]
            total_real += total_dia
            dias_reais.add(item["data"])

            print(f"\nData: {item['data']}")
            print(f"Manhã: {item['manha']}")
            print(f"Tarde: {item['tarde']}")
            print(f"Noite: {item['noite']}")
            print(f"TOTAL DO DIA: {total_dia}")

        total_dias = len(dias_reais)
        media_produto = total_real / total_dias

        real = {
            "diaria": round(media_produto, 2),
            "semanal": round(media_produto * 7, 2),
            "mensal": round(media_produto * 30, 2),
            "anual": round(media_produto * 365, 2)
        }

        eficiencia = {
            periodo: round((real[periodo] / ideal[periodo]) * 100, 2)
            for periodo in ideal
        }

        bateu_meta = "SIM" if real["mensal"] >= ideal["mensal"] else "NÃO"

        print("\n--- PRODUÇÃO IDEAL ---")
        for p, v in ideal.items():
            print(f"{p.capitalize():7}: {v:.2f}")

        print("\n--- PRODUÇÃO REAL DO PRODUTO ---")
        for p, v in real.items():
            print(f"{p.capitalize():7}: {v:.2f}")

        print("\n--- EFICIÊNCIA DO PRODUTO ---")
        for p, v in eficiencia.items():
            print(f"{p.capitalize():7}: {v:.2f}%")

        print(f"\nMETA ATINGIDA? {bateu_meta}")

        data_hora = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        nome_arquivo = f"relatorio_{nome_busca}_{data_hora}.txt"

        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"=== RELATÓRIO DO PRODUTO: {nome_busca.upper()} ===\n\n")

            arquivo.write("LISTA DO PRODUTO\n")
            for item in filtrados:
                total_dia = item["manha"] + item["tarde"] + item["noite"]
                arquivo.write(f"\nData: {item['data']}\n")
                arquivo.write(f"Manhã: {item['manha']} | Tarde: {item['tarde']} | Noite: {item['noite']}\n")
                arquivo.write(f"TOTAL DO DIA: {total_dia}\n")

            arquivo.write("\n\nPRODUÇÃO IDEAL\n")
            for p, v in ideal.items():
                arquivo.write(f"{p.capitalize():7}: {v:.2f}\n")

            arquivo.write("\nPRODUÇÃO REAL DO PRODUTO\n")
            for p, v in real.items():
                arquivo.write(f"{p.capitalize():7}: {v:.2f}\n")

            arquivo.write("\nEFICIÊNCIA DO PRODUTO\n")
            for p, v in eficiencia.items():
                arquivo.write(f"{p.capitalize():7}: {v:.2f}%\n")

            arquivo.write(f"\nMETA ATINGIDA? {bateu_meta}\n")

        print("\n Arquivo 'relatorio_produto.txt' salvo com sucesso!")

    input("\nPressione ENTER para voltar ao menu...")

def menu():
    while True:
        os.system("cls")
        print("==== MENU DE PRODUÇÃO ====")
        print("1 - Registrar Produção")
        print("2 - Listar Produção")
        print("3 - Excluir Produção")
        print("4 - Calcular Produção")
        print("5 - Simulação Ideal")
        print("6 - Relatório Geral")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            gerar_producao()
        elif opcao == "2":
            listar_producao()
        elif opcao == "3":    
            excluir_producao()
        elif opcao == "4":
            calculo_producao()
        elif opcao == "5":
            simulacao_ideal()
        elif opcao == "6":
            relatorio_producao()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")
            
if __name__ == "__main__":
    carregar_producao()
    menu()

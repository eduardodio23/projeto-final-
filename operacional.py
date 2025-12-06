from datetime import datetime, timedelta
import os; os.system("cls")
import random

producao = []

def gerar_producao():
    os.system("cls")

    print("=== MODO DE REGISTRO ===")
    print("1 - Manual")
    print("2 - Aleatório")

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
            data_inicio_str = input("Digite a data inicial (DD/MM/AAAA): ")
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            break
        except ValueError:
            print("Data inválida! Use o formato DD/MM/AAAA.")

    if gerar_aleatorio:
        print("\n Gerando produção aleatória da semana...\n")

    for dia in range(7):
        data_atual = data_inicio + timedelta(days=dia)
        data_formatada = data_atual.strftime("%d/%m/%Y")

        print(f"\nData: {data_formatada}")

        if gerar_aleatorio:
            manha = random.randint(50, 200)
            tarde = random.randint(50, 200)
            noite = random.randint(50, 200)

            print(f" Manhã: {manha}")
            print(f" Tarde: {tarde}")
            print(f" Noite: {noite}")
        else:
            while True:
                try:
                    manha = int(input("Produção da manhã: "))
                    break
                except ValueError:
                    print("Erro: Somente número inteiro!")

            while True:
                try:
                    tarde = int(input("Produção da tarde: "))
                    break
                except ValueError:
                    print("Erro: Somente número inteiro!")

            while True:
                try:
                    noite = int(input("Produção da noite: "))
                    break
                except ValueError:
                    print("Erro: Somente número inteiro!")

        producao.append({
            "nome": nome,
            "data": data_formatada,
            "manha": manha,
            "tarde": tarde,
            "noite": noite
        })

    print("\n Produto da semana cadastrado com sucesso!")
    print(f" Produção de '{nome}' adicionada à lista.")

def excluir_producao():
    
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
                  
def listar_producao():
    
    if not producao:
        print("\nNenhuma produção cadastrada")
        return

    print("\n=== MENU DE RELATÓRIOS ===")
    print("1 - Listagem geral (sem filtros)")
    print("2 - Pesquisa por nome do produto")
    print("3 - Listagem por período")
    opcao = input("Escolha: ")

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
                data_inicio = datetime.strptime(
                    input("Digite a data inicial (DD/MM/AAAA): "), "%d/%m/%Y"
                )
                data_fim = datetime.strptime(
                    input("Digite a data final (DD/MM/AAAA): "), "%d/%m/%Y"
                )
                if data_fim < data_inicio:
                    print("A data final não pode ser menor que a inicial.")
                else:
                    break
            except ValueError:
                print("Data inválida! Use DD/MM/AAAA.")

        filtrados = []
        for item in producao:
            try:
                data_item = datetime.strptime(item["data"], "%d/%m/%Y")
                if data_inicio <= data_item <= data_fim:
                    filtrados.append(item)
            except ValueError:
                continue

        if not filtrados:
            print("\nNenhuma produção nesse período.")
            return

    else:
        print("Opção inválida!")
        return

    print("\nFiltrar por turno:")
    print("1 - Manhã")
    print("2 - Tarde")
    print("3 - Noite")
    print("4 - Todos")
    opcao_turno = input("Escolha: ")

    print("\nOrdenar por:")
    print("1 - Data")
    print("2 - Produção Total")
    opcao_ordem = input("Escolha: ")

    if opcao_ordem == "1":
        filtrados.sort(key=lambda x: datetime.strptime(x["data"], "%d/%m/%Y"))
    elif opcao_ordem == "2":
        filtrados.sort(
            key=lambda x: x["manha"] + x["tarde"] + x["noite"],
            reverse=True
        )

    print("\n=== RESULTADO DA LISTAGEM ===\n")

    total_geral = 0

    for item in filtrados:
        total = item["manha"] + item["tarde"] + item["noite"]
        total_geral += total

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

        print(f"TOTAL DO DIA: {total}")
        print("=" * 18)

    print(f"\n TOTAL GERAL DO RELATÓRIO: {total_geral}")
    
def calculo_producao():

    if not producao:
        print("\nNenhuma produção cadastrada.")
        return

    print("\n CÁLCULO DE PRODUÇÃO ")
    print("1 - Diário")
    print("2 - Semanal")
    print("3 - Mensal")
    print("4 - Anual")
    print("5 - Geral")

    opcao = input("Escolha: ")

    filtrados = []

    if opcao == "1":
        data_busca = input("Digite a data (DD/MM/AAAA): ")
        try:
            data_busca = datetime.strptime(data_busca, "%d/%m/%Y")
        except ValueError:
            print("Data inválida!")
            return

        for item in producao:
            try:
                data_item = datetime.strptime(item["data"], "%d/%m/%Y")
                if data_item == data_busca:
                    filtrados.append(item)
            except ValueError:
                continue

    elif opcao == "2":
        data_inicio = input("Digite a data inicial da semana: ")
        try:
            data_inicio = datetime.strptime(data_inicio, "%d/%m/%Y")
        except ValueError:
            print("Data inválida!")
            return

        for item in producao:
            try:
                data_item = datetime.strptime(item["data"], "%d/%m/%Y")
                if data_inicio <= data_item <= data_inicio + timedelta(days=6):
                    filtrados.append(item)
            except ValueError:
                continue

    elif opcao == "3":
        mes = input("Digite o mês (MM): ")
        ano = input("Digite o ano (AAAA): ")

        try:
            mes = int(mes)
            ano = int(ano)
        except ValueError:
            print("Mês e ano devem ser numéricos!")
            return

        for item in producao:
            try:
                data_item = datetime.strptime(item["data"], "%d/%m/%Y")
                if data_item.month == mes and data_item.year == ano:
                    filtrados.append(item)
            except ValueError:
                continue
            
    elif opcao == "4":
        ano = input("Digite o ano (AAAA): ")

        try:
            ano = int(ano)
        except ValueError:
            print("Ano inválido!")
            return

        for item in producao:
            try:
                data_item = datetime.strptime(item["data"], "%d/%m/%Y")
                if data_item.year == ano:
                    filtrados.append(item)
            except ValueError:
                continue

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

    melhor_turno = "Manhã"
    maior_turno_valor = total_manha

    if total_tarde > maior_turno_valor:
        melhor_turno = "Tarde"
        maior_turno_valor = total_tarde

    if total_noite > maior_turno_valor:
        melhor_turno = "Noite"
        maior_turno_valor = total_noite

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
    
    if opcao == "1":
        print(f"Melhor turno do dia: {melhor_turno} ({maior_turno_valor})")
    else:
        print(f"Melhor dia: {melhor_dia} com {maior_producao_dia}")
        print(f"Melhor turno do período: {melhor_turno} ({maior_turno_valor})")
        
def simulação_ideal():

    if not producao:
        print("\nNenhuma produção real cadastrada.")
        return

    print("\n=== COMPARAÇÃO PRODUÇÃO REAL x IDEAL ===")

    ideal_mensal = 750 
    ideal_semanal = ideal_mensal / 4
    ideal_diaria = ideal_mensal / 30
    ideal_anual = ideal_mensal * 12

    total_real = 0
    datas = set()

    for item in producao:
        total_dia = item["manha"] + item["tarde"] + item["noite"]
        total_real += total_dia
        datas.add(item["data"])

    total_dias_reais = len(datas)

    if total_dias_reais == 0:
        print("Nenhum dia válido encontrado.")
        return

    media_diaria_real = total_real / total_dias_reais
    real_semanal_estimado = media_diaria_real * 7
    real_mensal_estimado = media_diaria_real * 30
    real_anual_estimado = real_mensal_estimado * 12

    eficiencia_diaria = (media_diaria_real / ideal_diaria) * 100
    eficiencia_semanal = (real_semanal_estimado / ideal_semanal) * 100
    eficiencia_mensal = (real_mensal_estimado / ideal_mensal) * 100
    eficiencia_anual = (real_anual_estimado / ideal_anual) * 100

    print("\n--- PRODUÇÃO IDEAL ---")
    print(f"Diária: {ideal_diaria:.2f}")
    print(f"Semanal: {ideal_semanal:.2f}")
    print(f"Mensal: {ideal_mensal:.2f}")
    print(f"Anual: {ideal_anual:.2f}")

    print("\n--- PRODUÇÃO REAL (ESTIMADA) ---")
    print(f"Média diária real: {media_diaria_real:.2f}")
    print(f"Semanal estimada: {real_semanal_estimado:.2f}")
    print(f"Mensal estimada: {real_mensal_estimado:.2f}")
    print(f"Anual estimada: {real_anual_estimado:.2f}")

    print("\n--- EFICIÊNCIA ---")
    print(f"Diária: {eficiencia_diaria:.2f}%")
    print(f"Semanal: {eficiencia_semanal:.2f}%")
    print(f"Mensal: {eficiencia_mensal:.2f}%")
    print(f"Anual: {eficiencia_anual:.2f}%")

    if eficiencia_mensal < 100:
        falta = ideal_mensal - real_mensal_estimado
        print(f"\n Faltam {falta:.2f} unidades para atingir a meta mensal.")
    else:
        sobra = real_mensal_estimado - ideal_mensal
        print(f"\n Meta mensal superada em {sobra:.2f} unidades!")

def relatorio_producao():
    os.system("cls")

    if not producao:
        print("\nNenhuma produção real cadastrada.")
        return

    print("\n === RELATÓRIO REAL x IDEAL === \n")

    ideal_mensal = 750 
    ideal_semanal = ideal_mensal / 4
    ideal_diaria = ideal_mensal / 30
    ideal_anual = ideal_mensal * 12

    total_real = 0
    datas = set()

    for item in producao:
        total_dia = item["manha"] + item["tarde"] + item["noite"]
        total_real += total_dia
        datas.add(item["data"])

    total_dias_reais = len(datas)

    if total_dias_reais == 0:
        print("Nenhum dia válido encontrado.")
        return

    media_diaria_real = total_real / total_dias_reais
    real_semanal_estimado = media_diaria_real * 7
    real_mensal_estimado = media_diaria_real * 30
    real_anual_estimado = real_mensal_estimado * 12

    eficiencia_diaria = (media_diaria_real / ideal_diaria) * 100
    eficiencia_semanal = (real_semanal_estimado / ideal_semanal) * 100
    eficiencia_mensal = (real_mensal_estimado / ideal_mensal) * 100
    eficiencia_anual = (real_anual_estimado / ideal_anual) * 100

    print("🔹 PRODUÇÃO IDEAL")
    print(f" Diária : {ideal_diaria:.2f}")
    print(f" Semanal: {ideal_semanal:.2f}")
    print(f" Mensal : {ideal_mensal:.2f}")
    print(f" Anual  : {ideal_anual:.2f}\n")

    print("🔹 PRODUÇÃO REAL (BASEADA NOS DADOS CADASTRADOS)")
    print(f" Média diária real : {media_diaria_real:.2f}")
    print(f" Semanal estimada  : {real_semanal_estimado:.2f}")
    print(f" Mensal estimada   : {real_mensal_estimado:.2f}")
    print(f" Anual estimada    : {real_anual_estimado:.2f}\n")

    print("🔹 EFICIÊNCIA")
    print(f" Diária : {eficiencia_diaria:.2f}%")
    print(f" Semanal: {eficiencia_semanal:.2f}%")
    print(f" Mensal : {eficiencia_mensal:.2f}%")
    print(f" Anual  : {eficiencia_anual:.2f}%\n")

    print("🔹 STATUS DA META MENSAL")

    if eficiencia_mensal < 100:
        falta = ideal_mensal - real_mensal_estimado
        print(f" Meta NÃO atingida.")
        print(f" Faltaram {falta:.2f} unidades para atingir a meta mensal.")
    elif eficiencia_mensal == 100:
        print(" Meta exatamente atingida.")
    else:
        sobra = real_mensal_estimado - ideal_mensal
        print(f" Meta SUPERADA!")
        print(f" Excedente de {sobra:.2f} unidades acima da meta.")

    print("\n===========================================================\n")
       
def menu_producao():
    
    while True:
        
        print("\n==== MENU DE PRODUÇÃO ====")
        print("1 - Registrar Produção")
        print("2 - Listar Produção")
        print("3 - Excluir Produção")
        print("4 - Calcular Produção")
        print("5 - Simulação Ideal")
        print("6 - Relatório Real x Ideal")
        print("0 - Sair")

        opcao = input("Escolha: ")

        match opcao:
            case "1":
                gerar_producao()
            case "2":
                listar_producao()
            case "3":
                excluir_producao()
            case "4":
                calculo_producao()
            case "5":
                simulação_ideal()
            case "6":
                relatorio_producao()
            case "0":
                print("Saindo...")
                break
            case _:
                print("Opção inválida!")
                
menu_producao()    
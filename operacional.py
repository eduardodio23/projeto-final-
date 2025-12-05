from datetime import datetime, timedelta


producao = []

def gerar_producao():
    
    nome = input("Digite o nome: ")
    while True:
        try:
            data_inicio_str = input("Digite a data inicial (DD/MM/AAAA): ")
            data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y")
            break
        except ValueError:
            print(" Data inválida! Use o formato DD/MM/AAAA.")

    for dia in range(7):
        data_atual = data_inicio + timedelta(days=dia)
        data_formatada = data_atual.strftime("%d/%m/%Y")
    
        print(f"\n Data:{data_formatada}")
        while True: 
         try:
          manha = int(input("Produção da manha: "))
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
        "nome" : nome,
        "data" : data_formatada,
        "manha" : manha,
        "tarde" : tarde,
        "noite" : noite
        })
    
    print("Produto da semana cadastrada com sucesso!")
    print(f"Produção de {nome} adicionado à lista")

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

    print("\n=== LISTA COMPLETA DE PRODUÇÃO ===\n")

    for item in producao:
        total = item["manha"] + item["tarde"] + item["noite"]

        print(f"Nome: {item['nome']}")
        print(f"Data: {item['data']}")
        print(f"Manhã: {item['manha']}")
        print(f"Tarde: {item['tarde']}")
        print(f"Noite: {item['noite']}")
        print(f"TOTAL DO DIA: {total}")
        print("=" * 15)
        
def calcular_producao():
    
    if not producao:
        print("\nNenhuma produção cadastrada")
        return

    print("\n CÁLCULO DE PRODUÇÃO ")
    print("1 - DIÁRIA")
    print("2 - SEMANAL")
    print("3 - MENSAL")

    opcao = input("Escolha: ")

    match opcao:

        case "1":
            try:
                data_busca = input("Digite a data (DD/MM/AAAA): ").strip()
                datetime.strptime(data_busca, "%d/%m/%Y")
            except ValueError:
                print("Data inválida! Use o formato DD/MM/AAAA.")
                return

            print(f"\n PRODUÇÃO DO DIA {data_busca} ")
            encontrou = False

            for item in producao:
                if item["data"] == data_busca:
                    total = item["manha"] + item["tarde"] + item["noite"]

                    print(f"Nome: {item['nome']}")
                    print(f"TOTAL DO DIA: {total}")
                    print("-" * 20)

                    encontrou = True

            if not encontrou:
                print("Nenhuma produção encontrada para essa data.")

        case "2":
            print("\n PRODUÇÃO SEMANAL ")

            resumo = {}

            for item in producao:
                try:
                    nome = item["nome"]
                    total = item["manha"] + item["tarde"] + item["noite"]

                    if nome not in resumo:
                        resumo[nome] = 0

                    resumo[nome] += total
                except KeyError:
                    print("Erro em um registro de produção.")
                    return

            for nome, total in resumo.items():
                media = total / 7
                print(f"{nome} → Total: {total} | Média diária: {media:.2f}")

        case "3":
            try:
                mes = input("Digite o mês (MM): ").strip()
                ano = input("Digite o ano (AAAA): ").strip()

                if not (mes.isdigit() and ano.isdigit()):
                    raise ValueError

                mes = int(mes)
                ano = int(ano)

                if mes < 1 or mes > 12:
                    raise ValueError
            except ValueError:
                print("Mês ou ano inválido!")
                return

            print(f"\n PRODUÇÃO DO MÊS {mes:02d}/{ano} ")

            resumo_mensal = {}
            dias_trabalhados = {}

            for item in producao:
                try:
                    data_obj = datetime.strptime(item["data"], "%d/%m/%Y")
                except ValueError:
                    print("Erro em uma data registrada no sistema.")
                    continue

                if data_obj.month == mes and data_obj.year == ano:
                    nome = item["nome"]
                    total = item["manha"] + item["tarde"] + item["noite"]

                    if nome not in resumo_mensal:
                        resumo_mensal[nome] = 0
                        dias_trabalhados[nome] = 0

                    resumo_mensal[nome] += total
                    dias_trabalhados[nome] += 1

            if resumo_mensal:
                for nome, total in resumo_mensal.items():
                    media = total / dias_trabalhados[nome]
                    print(f"{nome} → Total: {total} | Dias: {dias_trabalhados[nome]} | Média: {media:.2f}")
            else:
                print("Nenhuma produção encontrada para este mês.")

        case _:
            print("Opção inválida!")
            
def relatorio_producao():
    if not producao:
        print("\n nenhuma produção cadastrada.")
        return
    
    total_semanal = 0
    total_manha = 0
    total_tarde = 0
    total_noite = 0
    total_dias = len(producao)
    
    melhor_dia = None
    maior_producao_dia = 0
    
    
    for item in producao:
        total_dia = item["manha"] + item["tarde"] + item["noite"]
        total_semanal += total_dia
        
        total_manha += item["manha"]
        total_tarde += item["tarde"]
        total_noite += item["noite"]
        
        if total_dia > maior_producao_dia:
            maior_producao_dia = total_dia
            melhor_dia = item["data"]
            
        
    media_diaria = total_semanal / total_dias
    media_manha = total_manha / total_dias
    media_tarde = total_tarde / total_dias_
    media_noite = total_noite / total_dias
    
    melhor_turno = "Manha"
    maior_turno_valor = total_manha
    
    if total_tarde > maior_turno_valor:
        melhor_turno = "Tarde"
        maior_turno_valor = total_tarde
        
    if total_noite > maior_turno_valor:
        maior_turno = "Noite"
        maior_turno_valor = total_noite
        
        
    print("\n RELATÓRIO SEMANAL ")
    print(f" Total da semana: {total_semanal}")
    print(f" Média por dia: {media_diaria:.2f}")
    
    
    print("\n MÉDIA POR TURNO:")
    print(f"Manhã: {media_manha:.2f}")
    print(f"Tarde: {media_tarde:.2f}")
    print(f"Noite: {media_noite:.2f}")
    
    print("\n DESTAQUES DA SEMANA")
    print(f" Melhor dia: {melhor_dia} com {maior_producao_dia} dia produçao")
    print(f" Melhor turno da semana: {melhor_turno} ({maior_turno_valor} no total)")
    
       
def menu_producao():
    
    while True:
        
        print("\n==== Menu Teste ====")
        print("1 - Registrar Produção")
        print("2 - Listar Produção")
        print("3 - Relatório de Produção")
        print("0 - Sair")

        opcao = input("Escolha: ")

        match opcao:
            case "1":
                gerar_producao()
            case "2":
                lista_producao()
            case "3":
                relatorio_producao()
            case "0":
                print("Saindo...")
                break
            case _:
                print(" Opção inválida!")
                
menu_producao()    
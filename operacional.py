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
    
def lista_producao():
    
    if not producao:
        print("\n Nenhuma produção cadastrada")
        return
    
    print("\n LISTADe PRODUÇÂO \n")
    
    for item in producao:
        print(f"Nome: {item['nome']}")
        print(f"Data: {item['data']}")
        print(f"Manhã: {item['manha']}")
        print(f"Tarde: {item['tarde']}")
        print(f"Noite: {item['noite']}")
        print("-" * 30)

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
    media_tarde = total_tarde / total_dias
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
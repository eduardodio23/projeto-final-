# financeiro.py

def solicitar_despesas():
    print("\n=== MÓDULO FINANCEIRO ===")
    print("Informe os valores mensais das despesas:\n")

    agua = float(input("Água (R$): "))
    luz = float(input("Luz (R$): "))
    salarios = float(input("Salários (R$): "))
    impostos = float(input("Impostos (R$): "))

    despesas = {
        "agua": agua,
        "luz": luz,
        "salarios": salarios,
        "impostos": impostos
    }

    return despesas


def calcular_custos(despesas):
    """Retorna custo total mensal e custo unitário por pallet (1000/mês)."""
    total_mensal = sum(despesas.values())
    custo_pallet = total_mensal / 1000
    return total_mensal, custo_pallet


def calcular_preco_final(custo_unitario):
    """Aplica 50% de lucro."""
    return custo_unitario * 1.5


def calcular_projecoes(preco_final, custo_unitario, qtd_movimentada_mensal=1000):
    """
    Calcula lucro bruto mensal e anual com base nos pallets movimentados.
    """
    lucro_unitario = preco_final - custo_unitario
    lucro_mensal = lucro_unitario * qtd_movimentada_mensal
    lucro_anual = lucro_mensal * 12

    return lucro_mensal, lucro_anual


def relatorio_financeiro():
    """Executa todo o fluxo do módulo financeiro."""
    despesas = solicitar_despesas()
    total_mensal, custo_unitario = calcular_custos(despesas)

    preco_final = calcular_preco_final(custo_unitario)
    lucro_mensal, lucro_anual = calcular_projecoes(preco_final, custo_unitario)

    print("\n=== RELATÓRIO FINANCEIRO ===")
    print(f"➡ Despesa total mensal: R$ {total_mensal:.2f}")
    print(f"➡ Custo unitário por pallet (1000/mês): R$ {custo_unitario:.2f}")
    print(f"➡ Preço final com 50% de lucro: R$ {preco_final:.2f}")
    print(f"➡ Lucro bruto mensal: R$ {lucro_mensal:.2f}")
    print(f"➡ Lucro bruto anual: R$ {lucro_anual:.2f}")

    return {
        "total_mensal": total_mensal,
        "custo_unitario": custo_unitario,
        "preco_final": preco_final,
        "lucro_mensal": lucro_mensal,
        "lucro_anual": lucro_anual
    }

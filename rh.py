"""
Módulo: rh.py
Autor: Alvaro Mattos
Descrição:
    Módulo de Recursos Humanos para cálculo salarial,
    desconto de INSS, IRPF, cadastro de funcionários e
    geração de relatório ordenado por nome.
"""

import json

# --------------------------- CONFIGURAÇÕES --------------------------- #

CAMINHO_JSON = "rh_funcionarios.json"

# Valor da hora por cargo
VALOR_HORA = {
    "Operario": 15,
    "Supervisor": 40,
    "Gerente": 60,
    "Diretor": 80
}

# Faixas de INSS (percentuais simplificados)
FAIXAS_INSS = [
    (1302, 0.075),   # 7,5%
    (2571.29, 0.09), # 9%
    (3856.94, 0.12), # 12%
    (7507.49, 0.14)  # 14%
]

# Faixas IRPF anual (simplificadas)
FAIXAS_IR = [
    (22847.76, 0.00),
    (33919.80, 0.075),
    (45012.60, 0.15),
    (55976.16, 0.225),
    (float("inf"), 0.275)
]

# -------------------------------------------------------------------- #
# ---------------------- FUNÇÕES DE CÁLCULO ---------------------------#
# -------------------------------------------------------------------- #

def calcular_inss(salario):
    """
    Calcula INSS baseado na tabela progressiva.
    """
    for teto, aliquota in FAIXAS_INSS:
        if salario <= teto:
            return salario * aliquota
    return salario * 0.14


def calcular_ir_anual(salario_liquido):
    """
    Calcula IRPF anual considerando salário líquido * 12.
    """
    salario_anual = salario_liquido * 12

    for teto, aliquota in FAIXAS_IR:
        if salario_anual <= teto:
            return salario_anual * aliquota

    return salario_anual * 0.275


def calcular_salario(func):
    """
    Calcula salário bruto, extra, descontos, líquido.
    Atualiza o dicionário do funcionário.
    """
    cargo = func["cargo"]
    valor_hora = VALOR_HORA[cargo]
    horas_base = 160

    # SALÁRIO BRUTO
    salario_bruto = valor_hora * horas_base

    # HORAS EXTRAS (somente Operário e Supervisor)
    if cargo in ["Operario", "Supervisor"]:
        extra = func["horas_extras"] * (valor_hora * 2)
    else:
        extra = 0

    salario_total = salario_bruto + extra

    # INSS
    inss = calcular_inss(salario_total)

    # SALÁRIO LÍQUIDO
    salario_liquido = salario_total - inss

    # IRPF ANUAL
    ir_anual = calcular_ir_anual(salario_liquido)

    # Paga IR?
    paga_ir = ir_anual > 0

    # SALVANDO NO DICIONÁRIO
    func["salario_bruto"] = salario_bruto
    func["extra"] = extra
    func["inss"] = inss
    func["salario_liquido"] = salario_liquido
    func["ir"] = ir_anual
    func["paga_ir"] = paga_ir

    return func

# -------------------------------------------------------------------- #
# ------------------ FUNÇÕES DE CADASTRO/JSON ------------------------ #
# -------------------------------------------------------------------- #

def cadastrar_funcionario():
    """
    Cadastro manual de funcionário via input.
    Retorna um dicionário pronto para cálculo.
    """

    print("\n=== CADASTRO DE FUNCIONÁRIO ===")

    nome = input("Nome: ")
    cpf = input("CPF: ")
    rg = input("RG: ")
    endereco = input("Endereço: ")
    telefone = input("Telefone: ")
    filhos = int(input("Quantidade de filhos: "))

    # Validação de cargo
    while True:
        cargo = input("Cargo (Operario / Supervisor / Gerente / Diretor): ").strip().capitalize()
        if cargo in VALOR_HORA:
            break
        print("Cargo inválido! Tente novamente.")

    # Horas extras
    horas_extras = 0
    if cargo in ["Operario", "Supervisor"]:
        horas_extras = int(input("Horas extras no mês: "))

    # Monta dicionário
    funcionario = {
        "nome": nome,
        "cpf": cpf,
        "rg": rg,
        "endereco": endereco,
        "telefone": telefone,
        "filhos": filhos,
        "cargo": cargo,
        "horas_extras": horas_extras
    }

    return funcionario


def salvar_json(lista):
    """Salva lista completa no JSON."""
    with open(CAMINHO_JSON, "w", encoding="utf-8") as arq:
        json.dump(lista, arq, indent=4, ensure_ascii=False)


def carregar_json():
    """Carrega lista de funcionários se existir."""
    try:
        with open(CAMINHO_JSON, "r", encoding="utf-8") as arq:
            return json.load(arq)
    except FileNotFoundError:
        return []

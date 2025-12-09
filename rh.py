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



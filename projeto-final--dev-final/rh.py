"""
Módulo: rh.py (versão melhorada)
Autor: Alvaro Mattos
Descrição:
    Versão aprimorada do módulo RH. Inclui:
    - Menu interativo com navegação por setas (readchar)
    - Validações básicas (CPF, números, telefone)
    - Mensagens de erro amigáveis
    - Opção de excluir funcionário
    - Relatórios CSV e JSON
    - Uso de cores no terminal via colorama (opcional)

Dependências:
    pip install readchar colorama

Observações:
    - Este arquivo foi projetado para ser usado em terminais compatíveis.
    - Se não quiser instalar colorama, o código funciona sem cores (usa fallback).
"""

import json
import re
import os
from datetime import datetime

# try:
#     import readchar
# except Exception:
#     raise SystemExit("Biblioteca 'readchar' não encontrada. Instale com: pip install readchar")

# colorama é opcional, melhora a aparência no terminal Windows
try:
    from colorama import init as colorama_init, Fore, Back, Style
    colorama_init(autoreset=True)
    USE_COLOR = True
except Exception:
    # Fallback sem cores
    class Dummy:
        def __getattr__(self, name):
            return ""
    Fore = Back = Style = Dummy()
    USE_COLOR = False

# --------------------------- CONFIGURAÇÕES --------------------------- #
CAMINHO_JSON = "rh_funcionarios.json"
CAMINHO_REL_JSON = "relatorio_rh.json"
CAMINHO_REL_CSV = "relatorio_rh.csv"

VALOR_HORA = {
    "Operario": 15,
    "Supervisor": 40,
    "Gerente": 60,
    "Diretor": 80
}

FAIXAS_INSS = [
    (1302, 0.075),
    (2571.29, 0.09),
    (3856.94, 0.12),
    (7507.49, 0.14)
]

FAIXAS_IR = [
    (22847.76, 0.00),
    (33919.80, 0.075),
    (45012.60, 0.15),
    (55976.16, 0.225),
    (float("inf"), 0.275)
]

# --------------------------- UTILITÁRIOS ------------------------------- #

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_json():
    try:
        with open(CAMINHO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(Fore.RED + "Arquivo JSON corrompido. Iniciando lista vazia.")
        return []

def salvar_json(lista):
    try:
        with open(CAMINHO_JSON, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(Fore.RED + f"Erro ao salvar JSON: {e}")

# --------------------------- VALIDAÇÕES -------------------------------- #

def validar_texto(valor, campo, minimo=1):
    if not isinstance(valor, str) or len(valor.strip()) < minimo:
        raise ValueError(f"{campo} inválido")
    return valor.strip()

def validar_inteiro(valor, campo):
    try:
        n = int(valor)
        if n < 0:
            raise ValueError()
        return n
    except Exception:
        raise ValueError(f"{campo} deve ser um número inteiro não-negativo")

def validar_cpf(cpf):
    cpf_clean = re.sub(r'\D', '', cpf)
    if len(cpf_clean) != 11:
        raise ValueError("CPF deve ter 11 dígitos")
    return cpf_clean

def validar_telefone(num):
    t = re.sub(r'\D', '', num)
    if len(t) < 8:
        raise ValueError("Telefone inválido")
    return t

def validar_cargo(cargo):
    cargo = cargo.capitalize()
    if cargo not in VALOR_HORA:
        raise ValueError("Cargo inválido")
    return cargo

# ------------------------ CÁLCULOS SALARIAIS ---------------------------- #

def calcular_inss(salario):
    for teto, aliquota in FAIXAS_INSS:
        if salario <= teto:
            return salario * aliquota
    return salario * 0.14

def calcular_ir_anual(salario_liquido):
    salario_anual = salario_liquido * 12
    for teto, aliquota in FAIXAS_IR:
        if salario_anual <= teto:
            return salario_anual * aliquota
    return salario_anual * 0.275

def calcular_salario(func):
    cargo = func.get('cargo')
    valor_hora = VALOR_HORA.get(cargo, 0)
    horas_base = 160
    salario_bruto = valor_hora * horas_base
    extra = 0
    if cargo in ["Operario", "Supervisor"]:
        extra = func.get('horas_extras', 0) * (valor_hora * 2)
    salario_total = salario_bruto + extra
    inss = calcular_inss(salario_total)
    salario_liquido = salario_total - inss
    ir_anual = calcular_ir_anual(salario_liquido)
    paga_ir = ir_anual > 0
    func['salario_bruto'] = round(salario_bruto, 2)
    func['extra'] = round(extra, 2)
    func['inss'] = round(inss, 2)
    func['salario_liquido'] = round(salario_liquido, 2)
    func['ir'] = round(ir_anual, 2)
    func['paga_ir'] = paga_ir
    return func

# ------------------------ FUNÇÕES PRINCIPAIS --------------------------- #

def criar_funcionario_interativo():
    try:
        nome = validar_texto(input("Nome: "), "Nome")
        cpf = validar_cpf(input("CPF (somente números): "))
        rg = validar_texto(input("RG: "), "RG")
        endereco = validar_texto(input("Endereço: "), "Endereço")
        telefone = validar_telefone(input("Telefone: "))
        filhos = validar_inteiro(input("Quantidade de filhos: "), "Filhos")
        while True:
            try:
                cargo = validar_cargo(input("Cargo (Operario/Supervisor/Gerente/Diretor): "))
                break
            except ValueError as e:
                print(Fore.YELLOW + str(e))
        horas_extras = 0
        if cargo in ["Operario", "Supervisor"]:
            horas_extras = validar_inteiro(input("Horas extras no mês: "), "Horas extras")

        funcionario = {
            'nome': nome,
            'cpf': cpf,
            'rg': rg,
            'endereco': endereco,
            'telefone': telefone,
            'filhos': filhos,
            'cargo': cargo,
            'horas_extras': horas_extras
        }
        return funcionario
    except ValueError as e:
        print(Fore.RED + "Erro no cadastro: " + str(e))
        return None

def listar_funcionarios(funcionarios):
    if not funcionarios:
        print(Fore.YELLOW + "Nenhum funcionário cadastrado.")
        return
    print(Fore.CYAN + "\nLista de funcionários:\n")
    for i, f in enumerate(funcionarios, start=1):
        nome = f.get('nome', '—')
        cargo = f.get('cargo', '—')
        sal = f.get('salario_liquido', '—')
        print(f"{i}. {nome} — {cargo} — Salário líquido: R$ {sal}")

def excluir_funcionario(funcionarios):
    listar_funcionarios(funcionarios)
    if not funcionarios:
        return funcionarios
    try:
        idx = validar_inteiro(input("Digite o número do funcionário a excluir: "), "Índice")
        if idx < 1 or idx > len(funcionarios):
            print(Fore.RED + "Índice fora do intervalo")
            return funcionarios
        f = funcionarios.pop(idx-1)
        salvar_json(funcionarios)
        print(Fore.GREEN + f"Funcionário {f.get('nome')} excluído com sucesso.")
        return funcionarios
    except ValueError as e:
        print(Fore.RED + str(e))
        return funcionarios

def gerar_relatorios(funcionarios):
    # JSON resumido
    rel = {
        'gerado_em': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'quantidade': len(funcionarios),
        'funcionarios': funcionarios
    }
    try:
        with open(CAMINHO_REL_JSON, 'w', encoding='utf-8') as f:
            json.dump(rel, f, indent=4, ensure_ascii=False)
        # CSV detalhado
        lista_ordenada = sorted(funcionarios, key=lambda x: x.get('nome', '').lower())
        with open(CAMINHO_REL_CSV, 'w', encoding='utf-8') as f:
            f.write('NOME;CARGO;BRUTO;EXTRA;INSS;LIQUIDO;IR;PAGA_IR\n')
            for ff in lista_ordenada:
                f.write(f"{ff.get('nome')};{ff.get('cargo')};{ff.get('salario_bruto',0):.2f};{ff.get('extra',0):.2f};{ff.get('inss',0):.2f};{ff.get('salario_liquido',0):.2f};{ff.get('ir',0):.2f};{ff.get('paga_ir')}\n")
        print(Fore.GREEN + f"Relatórios gerados: {CAMINHO_REL_JSON}, {CAMINHO_REL_CSV}")
    except Exception as e:
        print(Fore.RED + f"Erro ao gerar relatórios: {e}")

# ------------------------ MENU INTERATIVO (READCHAR) ------------------ #

MENU_ITEMS = [
    "Cadastrar funcionário",
    "Calcular salários",
    "Listar funcionários",
    "Excluir funcionário",
    "Gerar relatório",
    "Sair"
]

def imprimir_menu(selecao):
    clear_screen()
    print(Back.BLACK + Fore.WHITE + "=== SISTEMA RH ===\n")
    for i, item in enumerate(MENU_ITEMS):
        prefix = '  '
        if i == selecao:
            prefix = Fore.BLACK + Back.WHITE + '→ ' + Style.RESET_ALL
            print(prefix + Fore.GREEN + item + Style.RESET_ALL)
        else:
            print('  ' + item)

# def menu_interativo():
#     funcionarios = carregar_json()
#     selecao = 0
#     imprimir_menu(selecao)

#     while True:
#         key = readchar.readkey()
#         # suporte para diferentes constantes de tecla entre plataformas
#         if key == readchar.key.UP or key == '\x1b[A':
#             selecao = (selecao - 1) % len(MENU_ITEMS)
#             imprimir_menu(selecao)
#         elif key == readchar.key.DOWN or key == '\x1b[B':
#             selecao = (selecao + 1) % len(MENU_ITEMS)
#             imprimir_menu(selecao)
#         elif key == readchar.key.ENTER or key == '\r' or key == '\n':
#             escolha = MENU_ITEMS[selecao]
#             if escolha == "Cadastrar funcionário":
#                 f = criar_funcionario_interativo()
#                 if f:
#                     funcionarios.append(f)
#                     salvar_json(funcionarios)
#                     print(Fore.GREEN + "Funcionário cadastrado com sucesso!")
#                     input("Pressione Enter para continuar...")
#                 imprimir_menu(selecao)
#             elif escolha == "Calcular salários":
#                 if not funcionarios:
#                     print(Fore.YELLOW + "Nenhum funcionário para calcular.")
#                     input("Pressione Enter para continuar...")
#                 else:
#                     for i in range(len(funcionarios)):
#                         funcionarios[i] = calcular_salario(funcionarios[i])
#                     salvar_json(funcionarios)
#                     print(Fore.GREEN + "Cálculos realizados e salvos.")
#                     input("Pressione Enter para continuar...")
#                 imprimir_menu(selecao)
#             elif escolha == "Listar funcionários":
#                 listar_funcionarios(funcionarios)
#                 input("Pressione Enter para continuar...")
#                 imprimir_menu(selecao)
#             elif escolha == "Excluir funcionário":
#                 funcionarios = excluir_funcionario(funcionarios)
#                 input("Pressione Enter para continuar...")
#                 imprimir_menu(selecao)
#             elif escolha == "Gerar relatório":
#                 gerar_relatorios(funcionarios)
#                 input("Pressione Enter para continuar...")
#                 imprimir_menu(selecao)
#             elif escolha == "Sair":
#                 print(Fore.CYAN + "Saindo...\n")
#                 break
#         elif key == '\x03':  # Ctrl+C
#             print(Fore.CYAN + "Saindo (Ctrl+C)...")
#             break

# if __name__ == '__main__':
#     try:
#         menu_interativo()
#     except Exception as e:
#         print(Fore.RED + f"Erro inesperado: {e}")
#         raise

def menu_simples():
    funcionarios = carregar_json()

    while True:
        print("\n=== SISTEMA RH ===")
        for i, item in enumerate(MENU_ITEMS, start=1):
            print(f"{i}. {item}")
        
        escolha = input("Escolha uma opção (número): ")
        try:
            escolha = int(escolha)
            if escolha < 1 or escolha > len(MENU_ITEMS):
                print("Opção inválida!")
                continue
        except ValueError:
            print("Digite apenas números!")
            continue

        opcao = MENU_ITEMS[escolha-1]

        if opcao == "Cadastrar funcionário":
            f = criar_funcionario_interativo()
            if f:
                funcionarios.append(f)
                salvar_json(funcionarios)
                print("Funcionário cadastrado com sucesso!")
        elif opcao == "Calcular salários":
            for i in range(len(funcionarios)):
                funcionarios[i] = calcular_salario(funcionarios[i])
            salvar_json(funcionarios)
            print("Cálculos realizados e salvos.")
        elif opcao == "Listar funcionários":
            listar_funcionarios(funcionarios)
        elif opcao == "Excluir funcionário":
            funcionarios = excluir_funcionario(funcionarios)
        elif opcao == "Gerar relatório":
            gerar_relatorios(funcionarios)
        elif opcao == "Sair":
            print("Saindo...")
            break

if __name__ == '__main__':
    try:
        menu_simples()
    except Exception as e:
        print(f"Erro inesperado: {e}")
        raise

# projeto-final-

📘 Sistema de Recursos Humanos (RH)

Módulo desenvolvido para compor o projeto final da disciplina de Lógica de Programação, permitindo o gerenciamento de funcionários, cálculo salarial completo, geração de relatórios e navegação aprimorada no menu.

📌 Funcionalidades do Módulo RH

# 👷 Cadastro de Funcionários
- Nome
- CPF
- RG
- Endereço
- Telefone
- Filhos
- Cargo (Operário, Supervisor, Gerente, Diretor)
- Horas extras (somente Operário e Supervisor)

# 🧮 Cálculos Realizados

# 💰 Salário bruto

Baseado na tabela:
Cargo/Valor por Hora
Operário: R$15
Supervisor: R$40
Gerente: R$60
Diretor: R$80

# ➕ Horas extras
- Apenas para Operário e Supervisor
Horas extras = valor da hora × 2

# 📉 Descontos

- INSS progressivo
- Salário líquido
- IRPF anual
- Indicação se o funcionário paga IR ou não

# 📂 Persistência de Dados

Os dados são armazenados em:

rh_funcionarios.json

Com atualização automática ao cadastrar, editar, excluir ou recalcular salários.

# 📑 Relatório Final

Gerado como arquivo:

relatorio_rh.csv

Com as colunas:

NOME;CARGO;BRUTO;EXTRA;INSS;LIQUIDO;IR;PAGA_IR

Ordenado alfabeticamente.

# 🖥️ Menu Interativo com Setas (readchar)

O sistema conta com:
✔ Navegação com ↑ e ↓
✔ Seleção com ENTER
✔ Cores para melhor visualização
✔ Tratamento de erros e mensagens amigáveis
✔ Opção de excluir funcionário
✔ Menu estruturado e elegante

# 📦 Instalação

Antes de rodar o sistema, instale as dependências:
- pip install readchar colorama

# ▶️ Como Executar

- No terminal: python rh.py

# 📁 Estrutura do Projeto
/seu_projeto
│── rh.py
│── rh_funcionarios.json
│── relatorio_rh.csv (gerado após relatório)
│── README.md

# 🛠️ Tecnologias Utilizadas

- Python 3
- Módulo readchar (navegação por setas)
- Módulo colorama (cores no terminal)
- JSON para persistência
- CSV para relatório final

# 🧑‍💻 Autor

- Alvaro Mattos
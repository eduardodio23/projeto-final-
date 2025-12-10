import json
import os

ARQUIVO_JSON = "producao.json"

def salvar(producao):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(producao, f, indent=4)

def carregar():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
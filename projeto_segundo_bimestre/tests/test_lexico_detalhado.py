#!/usr/bin/env python3
import sys
import os

# Ajuste de path para encontrar os módulos em ../src ou ..
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, ".."))
sys.path.insert(0, os.path.join(current_dir, "..", "src"))

try:
    from lexer import Lexer
except ImportError:
    print("[ERRO] Não foi possível importar 'Lexer'. Verifique o path.")
    sys.exit(1)


def run_lexical_test():
    print("=" * 80)
    print("RELATÓRIO DE ANÁLISE LÉXICA")
    print("=" * 80)

    # Definição do Código de Teste
    codigo_fonte = """val = 100
    if val > 50: {
        res = val / 2
        while res > 0: {
            res = res - 1
        }
    }"""
    
    print(f"\n[ENTRADA] Código Fonte:\n{codigo_fonte}\n")

    # Definições Formais (Documentação)
    print("-" * 60)
    print("1. DEFINIÇÕES FORMAIS")
    print("-" * 60)
    # Esta regex é a padrão para linguagens C-like.
    regex_identificador = r"[a-zA-Z_][a-zA-Z0-9_]*"

    print(f"Expressão Regular (Identificadores): {regex_identificador}")
    print(
        "Descrição: Começa com letra ou sublinhado, seguido de zero ou mais letras, números ou sublinhados."
    )

    # Execução do Lexer
    try:
        lexer = Lexer(codigo_fonte)
        tokens = lexer.get_token_tuples()
    except Exception as e:
        print(f"[ERRO NO LEXER] {e}")
        return

    # Tabela de Lexemas e Classes
    print("\n" + "-" * 60)
    print("2. TABELA DE IDENTIFICAÇÃO (Lexema vs Classe)")
    print("-" * 60)
    print(f"{'LEXEMA (Valor)':<20} | {'CLASSE (Token Type)':<20}")
    print("-" * 43)

    for tipo, valor in tokens:
        print(f"{str(valor):<20} | {str(tipo):<20}")

    # Cadeia de Tokens (Output Final)
    print("\n" + "-" * 60)
    print("3. CADEIA DE TOKENS (Stream)")
    print("-" * 60)
    cadeia_tokens = [f"<{tipo}, '{valor}'>" for tipo, valor in tokens]
    print(" -> ".join(cadeia_tokens))
    print("\n[FIM DO TESTE LÉXICO]")


if __name__ == "__main__":
    run_lexical_test()

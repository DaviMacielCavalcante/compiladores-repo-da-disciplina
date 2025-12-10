#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Ajuste de path para imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, '..'))
sys.path.insert(0, os.path.join(current_dir, '..', 'src'))

try:
    from grammar import Grammar
    from first_follow import FirstFollow
    from parsing_table import ParsingTable
    from ll1_parser import LL1Parser
    from lexer import Lexer
except ImportError:
    print("[ERRO] Falha ao importar módulos do compilador. Verifique a estrutura de pastas.")
    sys.exit(1)

def find_grammar():
    # Tenta localizar o arquivo na raiz ou em docs/
    candidates = [
        os.path.join(current_dir, '..', 'gramatica_sem_ambiguidade.bnf'),
        os.path.join(current_dir, '..', 'docs', 'gramatica_sem_ambiguidade.bnf'),
        "gramatica_sem_ambiguidade.bnf"
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def run_stack_trace_test():
    print("="*80)
    print("DEMONSTRAÇÃO DA PILHA DE ANÁLISE SINTÁTICA LL(1)")
    print("="*80)

    # 1. Preparação (Pipeline)
    grammar_path = find_grammar()
    if not grammar_path:
        print("ERRO: Gramática não encontrada.")
        return

    print(f"Carregando gramática de: {os.path.basename(grammar_path)}")
    g = Grammar()
    g.load_from_file(grammar_path)
    
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    
    pt = ParsingTable(g, ff)
    pt.build()

    # 2. Código simples para visualização clara da pilha
    # Usamos uma atribuição simples para não gerar 500 passos
    codigo_teste = "x = 10" 
    
    print("\n" + "-"*60)
    print(f"CÓDIGO DE ENTRADA:  {codigo_teste}")
    print("-"*60)

    # 3. Análise Léxica
    lexer = Lexer(codigo_teste)
    tokens = lexer.get_token_tuples()
    print(f"Tokens: {tokens}")

    # 4. Análise Sintática com Visualização de Pilha
    print("\n" + "-"*60)
    print("EVOLUÇÃO DA PILHA (STACK TRACE)")
    print("-"*60)
    print("O parser abaixo imprimirá o estado da pilha a cada passo:")
    print("Legenda: [Passo N] Pilha: TOPO ... FUNDO | Token Atual")
    print("-"*60 + "\n")

    parser = LL1Parser(g, pt)
    
    # O método parse() do seu arquivo ll1_parser.py já contém prints
    # detalhados da pilha (linha 67 do seu código).
    sucesso = parser.parse(tokens)

    print("\n" + "-"*60)
    if sucesso:
        print("RESULTADO: ✅ ACEITO - A pilha foi esvaziada com sucesso.")
    else:
        print("RESULTADO: ❌ REJEITADO - Erro durante o processamento da pilha.")

if __name__ == "__main__":
    run_stack_trace_test()
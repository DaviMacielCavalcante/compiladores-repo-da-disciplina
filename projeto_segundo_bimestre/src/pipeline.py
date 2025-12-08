#!/usr/bin/env python3
"""
Pipeline Completo: Grammar → First/Follow → Parsing Table → Parser
Executa o fluxo de ponta a ponta do compilador.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path para importações
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importações dos módulos fornecidos
from grammar import Grammar
from first_follow import FirstFollow
from parsing_table import ParsingTable
from ll1_parser import LL1Parser
from lexer import Lexer


def find_grammar_file(filename="gramatica_sem_ambiguidade.bnf"):
    """Procura o arquivo de gramática em locais comuns."""
    current_dir = Path(__file__).parent

    # Locais possíveis (ajuste conforme sua estrutura de pastas)
    candidates = [
        current_dir / filename,
        current_dir.parent / filename,
        current_dir.parent / "docs" / filename,
        current_dir / "docs" / filename,
        Path(filename),
    ]

    for path in candidates:
        if path.exists():
            return str(path)

    return None


def main():
    print("=" * 80)
    print("PIPELINE DO COMPILADOR VYTHON (LL1)")
    print("=" * 80)

    # ---------------------------------------------------------
    # 1. CARREGAMENTO DA GRAMÁTICA
    # ---------------------------------------------------------
    print("\n[1] Carregando Gramática...")
    grammar_path = find_grammar_file()

    if not grammar_path:
        print("[ERRO] Arquivo 'gramatica_sem_ambiguidade.bnf' não encontrado.")
        print("Certifique-se de que o arquivo .bnf está na pasta raiz ou em 'docs/'.")
        return

    g = Grammar()
    g.load_from_file(grammar_path)
    print(f"    Arquivo: {os.path.basename(grammar_path)}")
    print(f"    Símbolo inicial: {g.start_symbol}")
    print(f"    Terminais: {len(g.terminals)}")
    print(f"    Não-terminais: {len(g.nonterminals)}")

    # ---------------------------------------------------------
    # 2. CÁLCULO DE FIRST E FOLLOW
    # ---------------------------------------------------------
    print("\n[2] Calculando First e Follow...")
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    print("    Conjuntos calculados com sucesso.")

    # ---------------------------------------------------------
    # 3. CONSTRUÇÃO DA TABELA DE PARSING
    # ---------------------------------------------------------
    print("\n[3] Construindo Tabela de Parsing LL(1)...")
    pt = ParsingTable(g, ff)
    pt.build()

    # Verificação de saúde da tabela
    if pt.is_ll1_pure():
        print("    [SUCESSO] Gramática é LL(1) Pura (sem conflitos).")
    elif pt.is_ll1_practical():
        print(
            "    [AVISO] Gramática é LL(1) Prática (conflitos resolvidos automaticamente)."
        )
        print(f"    Conflitos resolvidos: {len(pt.resolved_conflicts)}")
    else:
        print(
            f"    [ERRO] Gramática NÃO é LL(1). Conflitos irresolvíveis: {len(pt.conflicts)}"
        )
        # Mostra os primeiros conflitos para debug
        pt.print_conflicts()

    # Salvar tabela para conferência
    csv_path = "tabela_parsing.csv"
    pt.save_matrix_to_csv(csv_path)
    print(f"    Tabela salva em: {csv_path}")

    # ---------------------------------------------------------
    # 4. ANÁLISE LÉXICA (LEXER)
    # ---------------------------------------------------------
    print("\n[4] Executando Lexer (Exemplo de Código)...")

    # Código de exemplo Vython para teste
    source_code = """
    if True:
        a = 10
    """

    print(f"    Código Fonte:\n{source_code}")

    lexer = Lexer(source_code)
    try:
        tokens = lexer.get_token_tuples()
        print(f"    Tokens gerados: {len(tokens)}")
        # Imprime os primeiros tokens para conferência
        tokens_display = [str(t) for t in tokens]
        print(f"    Preview: {tokens_display[:5]} ...")
    except Exception as e:
        print(f"    [ERRO LÉXICO] {e}")
        return

    # ---------------------------------------------------------
    # 5. ANÁLISE SINTÁTICA (PARSER)
    # ---------------------------------------------------------
    print("\n[5] Executando Parser LL(1)...")

    # Instancia o Parser com a gramática e a tabela gerada
    parser = LL1Parser(g, pt)

    # Executa a análise
    success = parser.parse(tokens)

    print("\n" + "=" * 80)
    print("RESULTADO DA ANÁLISE")
    print("=" * 80)

    if success:
        print("\n✅ CÓDIGO ACEITO! A sintaxe está correta.")

        # Opcional: Mostrar árvore/derivações
        print("\nDerivações utilizadas (passo a passo):")
        parser.print_derivations(max_show=15)
    else:
        print("\n❌ CÓDIGO REJEITADO! Erro de sintaxe encontrado.")


if __name__ == "__main__":
    main()

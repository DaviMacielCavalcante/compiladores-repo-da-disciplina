"""
Testes do Parser LL(1) para Vython
VERSÃO CORRIGIDA - USA GRAMÁTICA BNF PURA
"""

import sys
from pathlib import Path

# Adicionar src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from grammar import Grammar
from first_follow import FirstFollow
from parsing_table import ParsingTable
from ll1_parser import LL1Parser, ParseError, format_derivations
from lexer import Lexer, tokenize


def load_grammar_and_table():
    """
    Carrega gramática EBNF e constrói tabela LL(1)
    O grammar.py agora converte EBNF → BNF automaticamente!
    
    Returns:
        (Grammar, ParsingTable)
    """
    # Procurar gramática EBNF
    grammar_files = [
        project_root / "docs" / "gramatica_sem_ambiguidade.bnf",  # EBNF original
        Path("/mnt/user-data/uploads/gramatica_sem_ambiguidade.bnf"),
        project_root / "docs" / "gramatica_bnf_pura.bnf",  # Fallback BNF
        Path("/mnt/user-data/outputs/gramatica_bnf_pura.bnf"),
    ]
    
    grammar_file = None
    for gf in grammar_files:
        if gf.exists():
            grammar_file = gf
            print(f"✅ Usando gramática: {grammar_file.name}")
            break
    
    if grammar_file is None:
        print("❌ ERRO: Gramática não encontrada!")
        print("Procurado em:")
        for gf in grammar_files:
            print(f"  - {gf}")
        raise FileNotFoundError("Gramática não encontrada")
    
    # Carregar (grammar.py agora converte EBNF → BNF automaticamente!)
    g = Grammar()
    g.load_from_file(str(grammar_file))
    
    print(f"   Não-terminais: {len(g.nonterminals)}")
    print(f"   Terminais: {len(g.terminals)}")
    print(f"   Produções: {sum(len(prods) for prods in g.productions.values())}")
    
    # FIRST/FOLLOW
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    
    # Tabela
    pt = ParsingTable(g, ff)
    pt.build()
    
    print(f"   Entradas na tabela: {len(pt.table)}")
    print()
    
    return g, pt


def test_simple_expression():
    """Teste 1: Expressão simples"""
    print("\n" + "=" * 70)
    print("TESTE 1: Expressão Simples")
    print("=" * 70)
    
    code = "x = 5"
    print(f"Código: {code}\n")
    
    # Tokenizar
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    lexer.print_tokens()
    
    # Parser
    token_tuples = lexer.get_token_tuples()
    g, pt = load_grammar_and_table()
    parser = LL1Parser(g, pt)
    
    try:
        ast, derivations = parser.parse_with_derivation(token_tuples)
        print("\n✅ PARSING BEM-SUCEDIDO!\n")
        print(format_derivations(derivations[:15]))
        if len(derivations) > 15:
            print(f"... (total: {len(derivations)} derivações)")
    except ParseError as e:
        print(f"\n❌ ERRO DE PARSING:\n{e}\n")
        return False
        
    return True


def test_arithmetic():
    """Teste 2: Expressão aritmética"""
    print("\n" + "=" * 70)
    print("TESTE 2: Expressão Aritmética")
    print("=" * 70)
    
    code = "result = 2 + 3 * 4"
    print(f"Código: {code}\n")
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    lexer.print_tokens()
    
    g, pt = load_grammar_and_table()
    parser = LL1Parser(g, pt)
    token_tuples = lexer.get_token_tuples()
    
    try:
        ast, derivations = parser.parse_with_derivation(token_tuples)
        print("\n✅ PARSING BEM-SUCEDIDO!\n")
        print(format_derivations(derivations[:20]))
        print(f"... (total: {len(derivations)} derivações)")
    except ParseError as e:
        print(f"\n❌ ERRO DE PARSING:\n{e}\n")
        return False
        
    return True


def test_if_statement():
    """Teste 3: If statement"""
    print("\n" + "=" * 70)
    print("TESTE 3: If Statement")
    print("=" * 70)
    
    # Simplificar para uma linha (sem quebras de linha complexas)
    code = "if x > 0: { y = 1 }"
    print(f"Código: {code}\n")
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    lexer.print_tokens()
    
    g, pt = load_grammar_and_table()
    parser = LL1Parser(g, pt)
    token_tuples = lexer.get_token_tuples()
    
    try:
        ast, derivations = parser.parse_with_derivation(token_tuples)
        print("\n✅ PARSING BEM-SUCEDIDO!\n")
        print(format_derivations(derivations[:25]))
        print(f"... (total: {len(derivations)} derivações)")
    except ParseError as e:
        print(f"\n❌ ERRO DE PARSING:\n{e}\n")
        return False
        
    return True


def test_while_loop():
    """Teste 4: While loop"""
    print("\n" + 70)
    print("TESTE 4: While Loop")
    print("=" * 70)
    
    code = "while x > 0: { x = x - 1 }"
    print(f"Código: {code}\n")
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    lexer.print_tokens()
    
    g, pt = load_grammar_and_table()
    parser = LL1Parser(g, pt)
    token_tuples = lexer.get_token_tuples()
    
    try:
        ast, derivations = parser.parse_with_derivation(token_tuples)
        print("\n✅ PARSING BEM-SUCEDIDO!\n")
        print(format_derivations(derivations[:25]))
        print(f"... (total: {len(derivations)} derivações)")
    except ParseError as e:
        print(f"\n❌ ERRO DE PARSING:\n{e}\n")
        return False
        
    return True


def test_for_loop():
    """Teste 5: For loop"""
    print("\n" + "=" * 70)
    print("TESTE 5: For Loop")
    print("=" * 70)
    
    code = "for i in range(10): { x = x + 1 }"
    print(f"Código: {code}\n")
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    lexer.print_tokens()
    
    g, pt = load_grammar_and_table()
    parser = LL1Parser(g, pt)
    token_tuples = lexer.get_token_tuples()
    
    try:
        ast, derivations = parser.parse_with_derivation(token_tuples)
        print("\n✅ PARSING BEM-SUCEDIDO!\n")
        print(format_derivations(derivations[:25]))
        print(f"... (total: {len(derivations)} derivações)")
    except ParseError as e:
        print(f"\n❌ ERRO DE PARSING:\n{e}\n")
        return False
        
    return True


def test_error_case():
    """Teste 6: Caso de erro"""
    print("\n" + "=" * 70)
    print("TESTE 6: Caso de Erro (Esperado)")
    print("=" * 70)
    
    code = "x = + 5"  # Erro: + sem operando à esquerda
    print(f"Código: {code}\n")
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    lexer.print_tokens()
    
    g, pt = load_grammar_and_table()
    parser = LL1Parser(g, pt)
    token_tuples = lexer.get_token_tuples()
    
    try:
        ast, derivations = parser.parse_with_derivation(token_tuples)
        print("\n⚠️ INESPERADO: Parsing deveria ter falhado!\n")
        return False
    except ParseError as e:
        print(f"\n✅ ERRO DETECTADO CORRETAMENTE:\n{e}\n")
        return True


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "=" * 70)
    print("EXECUTANDO TODOS OS TESTES DO PARSER LL(1)")
    print("=" * 70)
    
    tests = [
        ("Expressão Simples", test_simple_expression),
        ("Expressão Aritmética", test_arithmetic),
        ("If Statement", test_if_statement),
        ("While Loop", test_while_loop),
        ("For Loop", test_for_loop),
        ("Caso de Erro", test_error_case),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ ERRO INESPERADO no teste '{name}':")
            print(f"   {type(e).__name__}: {e}\n")
            import traceback
            traceback.print_exc()
            results.append((name, False))
            
    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{name:<30} {status}")
        
    print("=" * 70)
    print(f"TOTAL: {passed}/{total} testes passaram ({passed*100//total}%)")
    print("=" * 70)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
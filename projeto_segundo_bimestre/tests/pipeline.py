#!/usr/bin/env python3
"""
Pipeline completo: Grammar → First/Follow → Parsing Table
"""

import sys
from pathlib import Path

# Ajustar path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from grammar import Grammar
from first_follow import FirstFollow
from parsing_table import ParsingTable
from ll1_parser import LL1Parser


def main():
    print("=" * 60)
    print("PIPELINE: GRAMMAR → FIRST/FOLLOW → TABLE → PARSER")
    print("=" * 60)
    
    # ============================================================
    # FASE 1: CARREGAR GRAMÁTICA
    # ============================================================
    print("\n[FASE 1] Carregando gramática...")
    
    # Se passou arquivo como argumento, usar ele
    if len(sys.argv) > 1:
        grammar_file = sys.argv[1]
        if not Path(grammar_file).exists():
            print(f"\n❌ ERRO: Arquivo não encontrado: {grammar_file}")
            return 1
    else:
        # Tentar vários caminhos possíveis
        possible_paths = [
            "../docs/gramatica_sem_ambiguidade.bnf",
            "gramatica_sem_ambiguidade.bnf",
            "../gramatica_sem_ambiguidade.bnf",
            "../../docs/gramatica_sem_ambiguidade.bnf",
            Path(__file__).parent.parent / "docs" / "gramatica_sem_ambiguidade.bnf",
        ]
        
        grammar_file = None
        for path in possible_paths:
            if Path(path).exists():
                grammar_file = str(path)
                break
        
        if not grammar_file:
            print("\n❌ ERRO: Arquivo de gramática não encontrado!")
            print("\nProcurei em:")
            for path in possible_paths:
                print(f"  - {path}")
            print("\nUso: python3 pipeline.py [caminho/para/gramatica.bnf]")
            print("Ou coloque 'gramatica_sem_ambiguidade.bnf' no diretório atual.")
            return 1
    
    g = Grammar()
    g.load_from_file(grammar_file)
    
    print(f"  Arquivo: {grammar_file}")
    print(f"  Não-terminais: {len(g.nonterminals)}")
    print(f"  Terminais: {len(g.terminals)}")
    print(f"  Produções: {sum(len(p) for p in g.productions.values())}")
    print(f"  Símbolo inicial: {g.start_symbol}")
    
    # Debug: Mostrar primeiras produções
    print(f"\n  Primeiras 3 produções:")
    for i, (nt, prods) in enumerate(list(g.productions.items())[:3]):
        for prod in prods[:1]:  # Primeira produção de cada NT
            prod_str = ' '.join(prod)[:50]
            print(f"    {nt} ::= {prod_str}")
    
    # ============================================================
    # FASE 2: CALCULAR FIRST E FOLLOW
    # ============================================================
    print("\n[FASE 2] Calculando FIRST e FOLLOW...")
    
    ff = FirstFollow(g)
    
    # FIRST
    print("  Calculando FIRST...")
    ff.compute_first()
    print(f"    Símbolos com FIRST: {len(ff.first)}")
    
    # Debug: Mostrar alguns FIRST
    print(f"\n  Exemplos de FIRST:")
    for nt in list(g.nonterminals)[:3]:
        first_set = ff.first.get(nt, set())
        first_str = ', '.join(sorted(list(first_set)[:5]))
        if len(first_set) > 5:
            first_str += f", ... ({len(first_set)} total)"
        print(f"    FIRST({nt}) = {{{first_str}}}")
    
    # FOLLOW
    print("\n  Calculando FOLLOW...")
    ff.compute_follow()
    print(f"    Não-terminais com FOLLOW: {len(ff.follow)}")
    
    # Debug: Mostrar alguns FOLLOW
    print(f"\n  Exemplos de FOLLOW:")
    for nt in list(g.nonterminals)[:3]:
        follow_set = ff.follow.get(nt, set())
        follow_str = ', '.join(sorted(list(follow_set)[:5]))
        if len(follow_set) > 5:
            follow_str += f", ... ({len(follow_set)} total)"
        print(f"    FOLLOW({nt}) = {{{follow_str}}}")
    
    # Salvar FIRST/FOLLOW
    print("\n  Salvando em arquivos...")
    ff.save_to_files()
    
    # ============================================================
    # FASE 3: CONSTRUIR TABELA DE PARSING
    # ============================================================
    print("\n[FASE 3] Construindo tabela de parsing...")
    
    pt = ParsingTable(g, ff)
    pt.build()
    
    print(f"  Entradas na tabela: {len(pt.table)}")
    print(f"  Conflitos detectados: {len(pt.conflicts)}")
    print(f"  Conflitos resolvidos: {len([c for c in pt.conflicts if c['resolved']])}")
    print(f"  Conflitos irresolúveis: {len(pt.unresolved_conflicts)}")
    
    # Debug: Mostrar alguns conflitos resolvidos
    if pt.conflicts:
        resolved = [c for c in pt.conflicts if c['resolved']][:3]
        if resolved:
            print(f"\n  Conflitos resolvidos (primeiros 3):")
            for conf in resolved:
                nt, term = conf['cell']
                print(f"    M[{nt}, {term}] → {conf['strategy']}")
    
    # Debug: Mostrar conflitos irresolúveis
    if pt.unresolved_conflicts:
        print(f"\n  ⚠️  CONFLITOS IRRESOLÚVEIS:")
        for conf in pt.unresolved_conflicts[:5]:
            nt, term = conf['cell']
            print(f"    M[{nt}, {term}]")
            print(f"      Opção 1: {' '.join(conf['existing'])[:40]}")
            print(f"      Opção 2: {' '.join(conf['new'])[:40]}")
    
    # Verificar LL(1)
    is_ll1 = pt.is_ll1()
    print(f"\n  É LL(1)? {'✅ SIM' if is_ll1 else '❌ NÃO'}")
    
    # Salvar tabela
    print("\n  Salvando em arquivos...")
    pt.save_to_files()
    
    # ============================================================
    # FASE 4: TESTAR PARSER LL(1) COM PILHA
    # ============================================================
    print("\n[FASE 4] Testando parser LL(1) com pilha...")
    
    # Casos de teste
    test_cases = [
        {
            'name': 'Expressão simples',
            'code': 'x = 5',
            'tokens': [
                ('IDENTIFIER', 'x'),
                ('=', '='),
                ('NUMBER', '5'),
                ('EOF', 'EOF'),
            ]
        },
        {
            'name': 'Expressão aritmética',
            'code': 'result = 2 + 3 * 4',
            'tokens': [
                ('IDENTIFIER', 'result'),
                ('=', '='),
                ('NUMBER', '2'),
                ('+', '+'),
                ('NUMBER', '3'),
                ('*', '*'),
                ('NUMBER', '4'),
                ('EOF', 'EOF'),
            ]
        },
        {
            'name': 'If statement',
            'code': 'if x < 5: { y = 10 }',
            'tokens': [
                ('if', 'if'),
                ('IDENTIFIER', 'x'),
                ('<', '<'),
                ('NUMBER', '5'),
                (':', ':'),
                ('{', '{'),
                ('IDENTIFIER', 'y'),
                ('=', '='),
                ('NUMBER', '10'),
                ('}', '}'),
                ('EOF', 'EOF'),
            ]
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n  Teste {i}/{len(test_cases)}: {test['name']}")
        print(f"    Código: {test['code']}")
        
        parser = LL1Parser(g, pt)
        result = parser.parse(test['tokens'])
        
        if result:
            print(f"    ✅ ACEITO")
            passed += 1
        else:
            print(f"    ❌ REJEITADO")
            failed += 1
    
    print(f"\n  Resultados: {passed}/{len(test_cases)} testes passaram")
    
    if failed > 0:
        print(f"  ⚠️  {failed} teste(s) falharam")
    
    # ============================================================
    # RESUMO FINAL
    # ============================================================
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    print(f"Gramática:")
    print(f"  NT: {len(g.nonterminals)}, T: {len(g.terminals)}, P: {sum(len(p) for p in g.productions.values())}")
    print(f"\nFirst/Follow:")
    print(f"  FIRST calculados: {len(ff.first)}")
    print(f"  FOLLOW calculados: {len(ff.follow)}")
    print(f"\nTabela de Parsing:")
    print(f"  Entradas: {len(pt.table)}")
    print(f"  LL(1)? {'✅ SIM' if is_ll1 else '❌ NÃO'}")
    print(f"\nParser LL(1):")
    print(f"  Testes passaram: {passed}/{len(test_cases)}")
    print(f"\nArquivos gerados:")
    print(f"  1. first_output.txt")
    print(f"  2. follow_output.txt")
    print(f"  3. parsing_table_output.txt")
    print(f"  4. parsing_table_matrix.txt")
    print(f"  5. parsing_table_matrix.csv")
    print("=" * 60)
    
    return 0 if is_ll1 and failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
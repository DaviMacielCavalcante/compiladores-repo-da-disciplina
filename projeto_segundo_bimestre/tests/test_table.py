import os
import sys

# adiciona a pasta src ao PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # pasta raiz do projeto
SRC_DIR = os.path.join(BASE_DIR, "src")
sys.path.append(SRC_DIR)

from grammar import Grammar
from firstFollow import FirstFollow
from parsingtable import ParsingTable



def test_simple_grammar():
    """Testa com gramática simples de expressões."""
    
    print("=" * 60)
    print("TESTE 1: GRAMÁTICA SIMPLES")
    print("=" * 60)
    
    # Criar gramática de exemplo
    g = Grammar()
    g.start_symbol = '<E>'
    g.nonterminals = {'<E>', "<E'>", '<T>', "<T'>", '<F>'}
    g.terminals = {'+', '*', '(', ')', 'id'}
    g.epsilon = 'ε'
    
    # E → T E'
    # E' → + T E' | ε
    # T → F T'
    # T' → * F T' | ε
    # F → ( E ) | id
    g.productions['<E>'] = [['<T>', "<E'>"]]
    g.productions["<E'>"] = [['+', '<T>', "<E'>"], ['ε']]
    g.productions['<T>'] = [['<F>', "<T'>"]]
    g.productions["<T'>"] = [['*', '<F>', "<T'>"], ['ε']]
    g.productions['<F>'] = [['(', '<E>', ')'], ['id']]
    
    print("\nGRAMÁTICA:")
    for nt in sorted(g.productions.keys()):
        for prod in g.productions[nt]:
            print(f"  {nt} ::= {' '.join(prod)}")
    
    # Calcular First e Follow
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    
    # Construir tabela
    pt = ParsingTable(g, ff)
    pt.build()
    
    # Resultados
    pt.print_conflicts()
    pt.print_statistics()
    pt.print_table()


def test_from_file():
    """Testa com gramática carregada de arquivo."""
    
    print("\n\n" + "=" * 60)
    print("TESTE 2: GRAMÁTICA DO ARQUIVO")
    print("=" * 60)
    
    try:
        # Usar o mesmo caminho que parsingTable.py
        grammar_file = "gramatica_sem_ambiguidade.bnf"
        
        # Carregar gramática (usa o mesmo sistema que grammar.py)
        g = Grammar()
        g.load_from_file(grammar_file)
        
        print(f"\nGramática carregada: {grammar_file}")
        print(f"  Não-terminais: {len(g.nonterminals)}")
        print(f"  Terminais: {len(g.terminals)}")
        print(f"  Produções: {sum(len(p) for p in g.productions.values())}")
        
        # Calcular First e Follow
        print("\nCalculando First e Follow...")
        ff = FirstFollow(g)
        ff.compute_first()
        ff.compute_follow()
        print("✓ Calculados")
        
        # Construir tabela
        print("\nConstruindo tabela LL(1)...")
        pt = ParsingTable(g, ff)
        pt.build()
        print("✓ Tabela construída")
        
        # Resultados
        pt.print_conflicts()
        pt.print_statistics()
        
        # Mostrar apenas primeiras entradas
        print("\n=== TABELA LL(1) (primeiras 20 entradas) ===")
        count = 0
        for (nt, term), prod in sorted(pt.table.items()):
            if count >= 20:
                print(f"... e mais {len(pt.table) - 20} entradas")
                break
            prod_str = ' '.join(prod)
            if len(prod_str) > 25:
                prod_str = prod_str[:22] + "..."
            print(f"M[{nt[:20]:<20}, {term[:15]:<15}] = {prod_str}")
            count += 1
        
    except FileNotFoundError as e:
        print(f"\n⚠ Arquivo não encontrado: {e}")
        print("⚠ Certifique-se que 'gramatica_sem_ambiguidade.bnf' está no mesmo diretório")
        print("Executando apenas teste com gramática simples")


def test_lookup():
    """Testa consulta à tabela."""
    
    print("\n\n" + "=" * 60)
    print("TESTE 3: CONSULTA À TABELA")
    print("=" * 60)
    
    # Criar gramática simples
    g = Grammar()
    g.start_symbol = '<E>'
    g.nonterminals = {'<E>', "<E'>", '<T>', "<T'>", '<F>'}
    g.terminals = {'+', '*', '(', ')', 'id'}
    g.epsilon = 'ε'
    
    g.productions['<E>'] = [['<T>', "<E'>"]]
    g.productions["<E'>"] = [['+', '<T>', "<E'>"], ['ε']]
    g.productions['<T>'] = [['<F>', "<T'>"]]
    g.productions["<T'>"] = [['*', '<F>', "<T'>"], ['ε']]
    g.productions['<F>'] = [['(', '<E>', ')'], ['id']]
    
    # Processar
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    
    pt = ParsingTable(g, ff)
    pt.build()
    
    # Testar consultas
    print("\nConsultas à tabela:")
    
    queries = [
        ('<E>', 'id'),
        ('<E>', '('),
        ("<E'>", '+'),
        ("<E'>", ')'),
        ('<T>', 'id'),
        ('<F>', '('),
    ]
    
    for nt, term in queries:
        prod = pt.get(nt, term)
        if prod:
            print(f"✓ M[{nt}, {term}] = {' '.join(prod)}")
        else:
            print(f"✗ M[{nt}, {term}] = (vazio - erro sintático)")


if __name__ == "__main__":
    test_simple_grammar()
    test_from_file()
    test_lookup()
    
    print("\n" + "=" * 60)
    print("✓ TODOS OS TESTES CONCLUÍDOS")
    print("=" * 60)
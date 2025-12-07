import sys

sys.path.append("../src")

from grammar import Grammar
from firstFollow import FirstFollow

def test_first_follow():
    """Testa cálculo de First e Follow em uma gramática simples."""
    
    # Cria gramática de teste
    g = Grammar()
    g.start_symbol = '<E>'
    g.nonterminals = {'<E>', '<T>', '<F>'}
    g.terminals = {'+', '*', '(', ')', 'id'}
    g.epsilon = 'ε'
    
    # E ::= T E'
    # E' ::= + T E' | ε
    # T ::= F T'
    # T' ::= * F T' | ε
    # F ::= ( E ) | id
    g.productions['<E>'] = [['<T>', "<E'>"]]
    g.productions["<E'>"] = [['+', '<T>', "<E'>"], ['ε']]
    g.productions['<T>'] = [['<F>', "<T'>"]]
    g.productions["<T'>"] = [['*', '<F>', "<T'>"], ['ε']]
    g.productions['<F>'] = [['(', '<E>', ')'], ['id']]
    
    g.nonterminals.add("<E'>")
    g.nonterminals.add("<T'>")
    
    print("GRAMÁTICA DE TESTE:")
    print("-" * 40)
    for nt in sorted(g.productions.keys()):
        for prod in g.productions[nt]:
            prod_str = ' '.join(prod)
            print(f"{nt} ::= {prod_str}")
    
    # Calcula First e Follow
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    
    print("\n" + "=" * 40)
    ff.print_sets()
    print("=" * 40)

def test_from_file():
    """Testa First e Follow com gramática carregada de arquivo."""
    
    try:
        g = Grammar()
        g.load_from_file("grammar.txt")
        
        print("\n\nGRAMÁTICA DO ARQUIVO:")
        print("-" * 40)
        print(f"Start: {g.start_symbol}")
        print(f"Não-terminais: {len(g.nonterminals)}")
        print(f"Terminais: {len(g.terminals)}")
        print(f"Produções: {sum(len(p) for p in g.productions.values())}")
        
        ff = FirstFollow(g)
        ff.compute_first()
        ff.compute_follow()
        
        print("\n" + "=" * 40)
        ff.print_sets()
        print("=" * 40)
        
    except FileNotFoundError:
        print("\nArquivo grammar.txt não encontrado. Testando apenas gramática exemplo.")

if __name__ == "__main__":
    test_first_follow()
    test_from_file()
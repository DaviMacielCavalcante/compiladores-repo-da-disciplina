"""
Teste de Debug - Verificar correção do parser
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from grammar import Grammar
from first_follow import FirstFollow
from parsing_table import ParsingTable
from ll1_parser import LL1Parser
from lexer import Lexer


def test_debug():
    """Teste simples para debug"""
    print("=" * 70)
    print("TESTE DE DEBUG - PARSER LL(1)")
    print("=" * 70)
    
    # Código simples
    code = "x = 5"
    print(f"\nCódigo: {code}\n")
    
    # Tokenizar
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print("TOKENS:")
    for token in tokens:
        print(f"  {token}")
    print()
    
    # Carregar gramática BNF PURA (não EBNF!)
    # Prioridade: usar a versão BNF pura
    grammar_file = project_root / "docs" / "gramatica_bnf_pura.bnf"
    
    if not grammar_file.exists():
        # Tentar em outros lugares
        alternatives = [
            Path("/mnt/user-data/outputs/gramatica_bnf_pura.bnf"),
            Path("/mnt/user-data/uploads/gramatica_bnf_pura.bnf"),
            project_root / "docs" / "gramatica_sem_ambiguidade.bnf",  # EBNF (pode não funcionar)
        ]
        for alt in alternatives:
            if alt.exists():
                grammar_file = alt
                break
    
    g = Grammar()
    g.load_from_file(str(grammar_file))
    
    print(f"Gramática carregada:")
    print(f"  Símbolo inicial: {g.start_symbol}")
    print(f"  Não-terminais: {len(g.nonterminals)}")
    print(f"  Terminais: {len(g.terminals)}")
    print()
    
    # FIRST/FOLLOW
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    
    # Tabela
    pt = ParsingTable(g, ff)
    pt.build()
    
    print(f"Tabela de parsing:")
    print(f"  Entradas: {len(pt.table)}")
    print()
    
    # Verificar algumas entradas da tabela
    print("Algumas entradas da tabela:")
    count = 0
    for (nt, term), prod in pt.table.items():
        if count < 10:
            prod_str = ' '.join(prod)
            print(f"  M[{nt}, {term}] = {prod_str}")
            count += 1
    print()
    
    # Parser
    parser = LL1Parser(g, pt)
    token_tuples = lexer.get_token_tuples()
    
    print("Token tuples para parser:")
    for tt in token_tuples:
        print(f"  {tt}")
    print()
    
    try:
        print("Iniciando parsing...")
        ast, derivations = parser.parse_with_derivation(token_tuples)
        print("\n✅ PARSING BEM-SUCEDIDO!\n")
        
        print("Primeiras 10 derivações:")
        for i, deriv in enumerate(derivations[:10]):
            print(f"  {deriv}")
            
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO:\n{e}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_debug()
    sys.exit(0 if success else 1)
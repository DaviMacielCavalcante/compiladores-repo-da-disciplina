#!/usr/bin/env python3
"""
Teste do formato matricial com a gramática do exemplo do professor.
"""

import sys
from pathlib import Path

# Adiciona src ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from grammar import Grammar
from first_follow import FirstFollow
from parsing_table import ParsingTable


def test_professor_grammar():
    """Testa com a gramática do exemplo do professor (PDF)."""
    
    print("=" * 70)
    print("TESTE: GRAMATICA DO PROFESSOR (Atividade 6)")
    print("=" * 70)
    
    # Criar gramática do exemplo
    g = Grammar()
    g.start_symbol = '<A>'
    g.nonterminals = {'<A>', '<B>', '<C>', '<D>', '<E>'}
    g.terminals = {'id', '+', '*', '(', ')', '$'}
    g.epsilon = 'ε'
    
    # Produções conforme o PDF:
    # A → C B
    # B → + C B | ε
    # C → E D
    # D → * E D | ε
    # E → ( A ) | id
    
    g.productions['<A>'] = [['<C>', '<B>']]
    g.productions['<B>'] = [['+', '<C>', '<B>'], ['ε']]
    g.productions['<C>'] = [['<E>', '<D>']]
    g.productions['<D>'] = [['*', '<E>', '<D>'], ['ε']]
    g.productions['<E>'] = [['(', '<A>', ')'], ['id']]
    
    print("\nGRAMATICA:")
    print("  A -> C B")
    print("  B -> + C B | ε")
    print("  C -> E D")
    print("  D -> * E D | ε")
    print("  E -> ( A ) | id")
    
    # Calcular First e Follow
    print("\n[INFO] Calculando FIRST e FOLLOW...")
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    
    print("\nFIRST:")
    for nt in sorted(g.nonterminals):
        print(f"  FIRST({nt}) = {ff.first[nt]}")
    
    print("\nFOLLOW:")
    for nt in sorted(g.nonterminals):
        print(f"  FOLLOW({nt}) = {ff.follow[nt]}")
    
    # Construir tabela
    print("\n[INFO] Construindo tabela LL(1)...")
    pt = ParsingTable(g, ff)
    pt.build()
    
    # Verificar conflitos
    pt.print_conflicts()
    pt.print_statistics()
    
    # Salvar tabela matricial
    output_file = project_root / "table_professor_example.txt"
    pt.save_matrix_to_file(str(output_file), max_col_width=12, max_cell_width=25)
    
    # Salvar CSV (sem truncamento!)
    csv_file = project_root / "table_professor_example.csv"
    pt.save_matrix_to_csv(str(csv_file))
    
    print(f"\n[OK] Arquivos gerados:")
    print(f"  - {output_file.name} (texto)")
    print(f"  - {csv_file.name} (CSV - abra no Excel)")
    
    # Mostrar preview da tabela matricial
    print("\n" + "=" * 70)
    print("PREVIEW DA TABELA MATRICIAL:")
    print("=" * 70)
    
    terminals = sorted(g.terminals)
    nonterminals = sorted(g.nonterminals)
    
    # Cabeçalho
    header = f"{'NT':<8}"
    for term in terminals:
        header += f"{term:<12}"
    print(header)
    print("-" * len(header))
    
    # Linhas
    for nt in nonterminals:
        row = f"{nt:<8}"
        for term in terminals:
            prod = pt.get(nt, term)
            if prod:
                if len(prod) == 1 and g.is_epsilon(prod[0]):
                    cell = "ε"
                else:
                    cell = ' '.join(prod)
                    if len(cell) > 10:
                        cell = cell[:10]
            else:
                cell = ""
            row += f"{cell:<12}"
        print(row)
    
    print("\n" + "=" * 70)


def test_vython_grammar():
    """Testa com a gramática Vython (se disponível)."""
    
    print("\n\n" + "=" * 70)
    print("TESTE: GRAMATICA VYTHON")
    print("=" * 70)
    
    # Procurar arquivo
    grammar_files = [
        project_root / "gramatica_bnf_pura.bnf",
        project_root / "docs" / "gramatica_bnf_pura.bnf",
    ]
    
    grammar_file = None
    for path in grammar_files:
        if path.exists():
            grammar_file = path
            break
    
    if not grammar_file:
        print("\n[AVISO] Arquivo gramatica_bnf_pura.bnf nao encontrado")
        print("[INFO] Pulando teste Vython...")
        return
    
    # Carregar gramática
    g = Grammar()
    g.load_from_file(str(grammar_file))
    
    print(f"\n[OK] Gramatica carregada: {grammar_file.name}")
    print(f"  Nao-terminais: {len(g.nonterminals)}")
    print(f"  Terminais: {len(g.terminals)}")
    
    # Processar
    print("\n[INFO] Calculando FIRST e FOLLOW...")
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    
    print("[INFO] Construindo tabela LL(1)...")
    pt = ParsingTable(g, ff)
    pt.build()
    
    # Resultados
    pt.print_conflicts()
    pt.print_statistics()
    
    # Salvar tabela matricial
    matrix_file = project_root / "vython_parsing_table_matrix.txt"
    pt.save_matrix_to_file(str(matrix_file), max_col_width=15, max_cell_width=35)
    
    # Salvar CSV (sem truncamento!)
    csv_file = project_root / "vython_parsing_table_matrix.csv"
    pt.save_matrix_to_csv(str(csv_file))
    
    print(f"\n[OK] Arquivos gerados:")
    print(f"  - {matrix_file.name} (texto)")
    print(f"  - {csv_file.name} (CSV - abra no Excel)")
    
    # Aviso sobre tamanho
    if len(g.nonterminals) > 20 or len(g.terminals) > 20:
        print("\n[INFO] Tabela muito grande para visualizacao no terminal")
        print(f"[INFO] Abra o arquivo CSV no Excel para ver a tabela completa")


if __name__ == "__main__":
    try:
        # Teste 1: Gramática do professor (pequena e clara)
        test_professor_grammar()
        
        # Teste 2: Gramática Vython (grande)
        test_vython_grammar()
        
        print("\n" + "=" * 70)
        print("[OK] TESTES CONCLUIDOS")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[ERRO] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
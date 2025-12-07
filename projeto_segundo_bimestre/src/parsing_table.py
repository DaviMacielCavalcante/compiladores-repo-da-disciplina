from collections import defaultdict

class ParsingTable:
    """Constrói tabela de parsing LL(1)."""
    
    def __init__(self, grammar, first_follow):
        """Inicializa com gramática e conjuntos First/Follow calculados."""
        self.grammar = grammar
        self.first_follow = first_follow
        self.table = {}
        self.conflicts = []
    
    def build(self):
        """Constrói a tabela de parsing LL(1)."""
        self.table = {}
        self.conflicts = []
        
        for nt in self.grammar.nonterminals:
            for prod in self.grammar.productions[nt]:
                # Calcular FIRST da produção
                first_prod = self._first_of_production(prod)
                
                # Regra 1: Para cada terminal em FIRST(α)
                for terminal in first_prod - {self.grammar.epsilon}:
                    self._add_entry(nt, terminal, prod)
                
                # Regra 2: Se ε ∈ FIRST(α), usar FOLLOW(A)
                if self.grammar.epsilon in first_prod:
                    for terminal in self.first_follow.follow[nt]:
                        self._add_entry(nt, terminal, prod)
        
        return self.table
    
    def _add_entry(self, nonterminal, terminal, production):
        """Adiciona entrada na tabela, detectando conflitos."""
        key = (nonterminal, terminal)
        
        if key in self.table:
            existing = self.table[key]
            
            # Ignora se for a mesma produção (não é conflito)
            if existing == production:
                return
            
            # Conflito real: produções diferentes para mesma célula
            conflict = {
                'cell': key,
                'existing': existing,
                'new': production
            }
            self.conflicts.append(conflict)
            
            # Mantém primeira produção na tabela
            # (comportamento padrão para gramáticas não-LL(1))
        else:
            self.table[key] = production
    
    def _first_of_production(self, production):
        """Calcula FIRST de uma produção."""
        result = set()
        
        if not production or self.grammar.is_epsilon(production[0]):
            return {self.grammar.epsilon}
        
        for symbol in production:
            if symbol in self.grammar.terminals:
                result.add(symbol)
                break
            
            first_symbol = self.first_follow.first[symbol]
            result.update(first_symbol - {self.grammar.epsilon})
            
            if self.grammar.epsilon not in first_symbol:
                break
        else:
            result.add(self.grammar.epsilon)
        
        return result
    
    def get(self, nonterminal, terminal):
        """Consulta tabela M[A,a]."""
        return self.table.get((nonterminal, terminal))
    
    def has_conflicts(self):
        """Verifica se há conflitos."""
        return len(self.conflicts) > 0
    
    def is_ll1(self):
        """Verifica se gramática é LL(1)."""
        return not self.has_conflicts()
    
    def save_matrix_to_csv(self, filename):
        """
        Salva tabela em formato CSV (sem truncamento).
        
        Formato ideal para abrir em Excel/LibreOffice.
        Cada célula contém a produção completa, sem cortes.
        
        Args:
            filename: Nome do arquivo CSV
        """
        import csv
        
        # Coletar não-terminais e terminais usados na tabela
        nonterminals_in_table = sorted(set(nt for nt, _ in self.table.keys()))
        terminals_in_table = sorted(set(term for _, term in self.table.keys()))
        
        # Função para formatar produção
        def format_production(prod):
            if not prod:
                return ""
            
            # Tratamento especial para epsilon
            if len(prod) == 1 and self.grammar.is_epsilon(prod[0]):
                return "ε"
            
            # Junta produção (SEM truncamento)
            return ' '.join(prod)
        
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            # Linha 1: Cabeçalho com terminais
            header = ['Não-Terminal'] + terminals_in_table
            writer.writerow(header)
            
            # Linhas da tabela (cada não-terminal)
            for nt in nonterminals_in_table:
                row = [nt]
                
                for term in terminals_in_table:
                    prod = self.get(nt, term)
                    cell_content = format_production(prod) if prod else ""
                    row.append(cell_content)
                
                writer.writerow(row)
        
        print(f"[OK] Tabela CSV salva em: {filename}")
        print(f"[INFO] Abra em Excel/LibreOffice para visualizar sem truncamento")
    
    def save_matrix_to_file(self, filename, max_col_width=15, max_cell_width=30):
        """
        Salva tabela em formato MATRICIAL (como professor ensina).
        
        Formato:
                   term1    term2    term3    ...
        <NT1>      prod1             prod2
        <NT2>               prod3    
        ...
        
        Args:
            filename: Nome do arquivo
            max_col_width: Largura máxima da coluna de terminal
            max_cell_width: Largura máxima da célula de produção
        """
        # Coletar não-terminais e terminais usados na tabela
        nonterminals_in_table = sorted(set(nt for nt, _ in self.table.keys()))
        terminals_in_table = sorted(set(term for _, term in self.table.keys()))
        
        # Função auxiliar para truncar texto
        def truncate(text, max_len):
            if len(text) <= max_len:
                return text
            return text[:max_len-3] + "..."
        
        # Função para formatar produção
        def format_production(prod):
            if not prod:
                return ""
            
            # Tratamento especial para epsilon
            if len(prod) == 1 and self.grammar.is_epsilon(prod[0]):
                return "ε"
            
            # Junta produção
            prod_str = ' '.join(prod)
            return truncate(prod_str, max_cell_width)
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("=" * 100 + "\n")
            f.write("TABELA DE PARSING LL(1) - FORMATO MATRICIAL\n")
            f.write("=" * 100 + "\n\n")
            
            # Estatísticas
            f.write("=== ESTATISTICAS ===\n")
            f.write(f"Nao-terminais na tabela: {len(nonterminals_in_table)}\n")
            f.write(f"Terminais na tabela: {len(terminals_in_table)}\n")
            f.write(f"Total de entradas: {len(self.table)}\n")
            f.write(f"Conflitos: {len(self.conflicts)}\n")
            f.write(f"E LL(1)? {'SIM' if self.is_ll1() else 'NAO'}\n\n")
            
            # Conflitos (se houver)
            if self.conflicts:
                f.write("=== CONFLITOS ===\n")
                for i, conflict in enumerate(self.conflicts, 1):
                    nt, term = conflict['cell']
                    f.write(f"Conflito {i}: M[{nt}, {term}]\n")
                    f.write(f"  Existente: {format_production(conflict['existing'])}\n")
                    f.write(f"  Nova: {format_production(conflict['new'])}\n\n")
            
            # Tabela matricial
            f.write("=" * 100 + "\n")
            f.write("TABELA MATRICIAL\n")
            f.write("=" * 100 + "\n\n")
            
            # Largura da coluna de não-terminais
            nt_col_width = max(len(nt) for nt in nonterminals_in_table) + 2
            nt_col_width = max(nt_col_width, 25)  # Mínimo 25
            
            # Cabeçalho com terminais
            header = " " * nt_col_width
            for term in terminals_in_table:
                term_display = truncate(term, max_col_width)
                header += f"{term_display:<{max_col_width}} "
            f.write(header + "\n")
            f.write("-" * len(header) + "\n")
            
            # Linhas da tabela (cada não-terminal)
            for nt in nonterminals_in_table:
                # Coluna do não-terminal
                row = f"{nt:<{nt_col_width}}"
                
                # Colunas dos terminais
                for term in terminals_in_table:
                    prod = self.get(nt, term)
                    
                    if prod:
                        cell_content = format_production(prod)
                    else:
                        cell_content = ""
                    
                    row += f"{cell_content:<{max_col_width}} "
                
                f.write(row + "\n")
            
            f.write("\n" + "=" * 100 + "\n")
            
            # Legenda
            f.write("\nLEGENDA:\n")
            f.write("  - Celula vazia: entrada nao definida (erro sintatico)\n")
            f.write("  - ε (epsilon): producao vazia\n")
            f.write("  - Producoes truncadas com '...' para caber na celula\n")
        
        print(f"[OK] Tabela matricial salva em: {filename}")
    
    def print_table(self):
        """Imprime tabela formatada."""
        print("\n=== TABELA DE PARSING LL(1) ===")
        print(f"{'NAO-TERMINAL':<25} {'TERMINAL':<20} {'PRODUCAO':<30}")
        print("-" * 75)
        
        for (nt, term), prod in sorted(self.table.items()):
            prod_str = ' '.join(prod)
            if len(prod_str) > 28:
                prod_str = prod_str[:25] + "..."
            print(f"{nt:<25} {term:<20} {prod_str:<30}")
        
        print(f"\nTotal: {len(self.table)} entradas")
    
    def print_conflicts(self):
        """Imprime conflitos detectados."""
        print("\n=== DETECCAO DE CONFLITOS ===")
        
        if not self.conflicts:
            print("[OK] Nenhum conflito detectado")
            print("[OK] Gramatica e LL(1)")
        else:
            print(f"[ERRO] {len(self.conflicts)} conflito(s) detectado(s)")
            print("[ERRO] Gramatica NAO e LL(1)\n")
            
            for i, conflict in enumerate(self.conflicts, 1):
                nt, term = conflict['cell']
                print(f"Conflito {i}: M[{nt}, {term}]")
                print(f"  Existente: {' '.join(conflict['existing'])}")
                print(f"  Nova: {' '.join(conflict['new'])}")
                print()
    
    def print_statistics(self):
        """Imprime estatísticas da tabela."""
        nts_used = len(set(nt for nt, _ in self.table.keys()))
        terms_used = len(set(term for _, term in self.table.keys()))
        
        print("\n=== ESTATISTICAS ===")
        print(f"Entradas na tabela: {len(self.table)}")
        print(f"Nao-terminais com entradas: {nts_used}")
        print(f"Terminais utilizados: {terms_used}")
        print(f"Conflitos: {len(self.conflicts)}")
        print(f"E LL(1)? {'[OK] SIM' if self.is_ll1() else '[ERRO] NAO'}")
    
    def save_to_file(self, filename):
        """Salva tabela em arquivo (formato lista)."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("TABELA DE PARSING LL(1)\n")
            f.write("=" * 80 + "\n\n")
            
            # Estatísticas
            f.write("=== ESTATISTICAS ===\n")
            f.write(f"Entradas na tabela: {len(self.table)}\n")
            f.write(f"Conflitos: {len(self.conflicts)}\n")
            f.write(f"E LL(1)? {'SIM' if self.is_ll1() else 'NAO'}\n\n")
            
            # Conflitos (se houver)
            if self.conflicts:
                f.write("=== CONFLITOS ===\n")
                for i, conflict in enumerate(self.conflicts, 1):
                    nt, term = conflict['cell']
                    f.write(f"Conflito {i}: M[{nt}, {term}]\n")
                    f.write(f"  Existente: {' '.join(conflict['existing'])}\n")
                    f.write(f"  Nova: {' '.join(conflict['new'])}\n\n")
            
            # Tabela
            f.write("=== TABELA ===\n")
            f.write(f"{'NAO-TERMINAL':<30} {'TERMINAL':<20} {'PRODUCAO':<50}\n")
            f.write("-" * 100 + "\n")
            
            for (nt, term), prod in sorted(self.table.items()):
                prod_str = ' '.join(prod)
                f.write(f"{nt:<30} {term:<20} {prod_str:<50}\n")
        
        print(f"[OK] Tabela salva em: {filename}")


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Adiciona diretório src ao path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root / "src"))
    
    from grammar import Grammar
    from first_follow import FirstFollow
    
    # Localizar arquivo de gramática
    grammar_files = [
        project_root / "gramatica_bnf_pura.bnf",
        project_root / "docs" / "gramatica_bnf_pura.bnf",
        project_root / "docs" / "gramatica_sem_ambiguidade.bnf",
    ]
    
    grammar_file = None
    for path in grammar_files:
        if path.exists():
            grammar_file = path
            break
    
    if not grammar_file:
        print("[ERRO] Arquivo de gramatica nao encontrado!")
        print("Procurado em:")
        for path in grammar_files:
            print(f"  - {path}")
        sys.exit(1)
    
    print("=" * 60)
    print("CONSTRUCAO DA TABELA DE PARSING LL(1)")
    print("=" * 60)
    print(f"\nGramatica: {grammar_file.name}")
    
    # Carregar gramática
    g = Grammar()
    g.load_from_file(str(grammar_file))
    
    print(f"  Nao-terminais: {len(g.nonterminals)}")
    print(f"  Terminais: {len(g.terminals)}")
    print(f"  Producoes: {sum(len(prods) for prods in g.productions.values())}")
    
    # Calcular First e Follow
    print("\nCalculando First e Follow...")
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    print("[OK] First e Follow calculados")
    
    # Construir tabela
    print("\nConstruindo tabela LL(1)...")
    pt = ParsingTable(g, ff)
    pt.build()
    print("[OK] Tabela construida")
    
    # Mostrar resultados
    pt.print_conflicts()
    pt.print_statistics()
    
    # Salvar formato lista
    output_file = project_root / "parsing_table_output.txt"
    pt.save_to_file(str(output_file))
    
    # Salvar formato MATRICIAL (texto)
    matrix_file = project_root / "parsing_table_matrix.txt"
    pt.save_matrix_to_file(str(matrix_file), max_col_width=15, max_cell_width=30)
    
    # Salvar formato CSV (sem truncamento!)
    csv_file = project_root / "parsing_table_matrix.csv"
    pt.save_matrix_to_csv(str(csv_file))
    
    print("\n" + "=" * 60)
    print("ARQUIVOS GERADOS:")
    print(f"  1. {output_file.name} (formato lista)")
    print(f"  2. {matrix_file.name} (formato matricial texto)")
    print(f"  3. {csv_file.name} (formato CSV - abra no Excel)")
    print("=" * 60)
from collections import defaultdict

class ParsingTable:
    """Constrói tabela de parsing LL(1) processando EBNF diretamente."""
    
    def __init__(self, grammar, first_follow):
        self.grammar = grammar
        self.first_follow = first_follow
        self.table = {}
        self.conflicts = []
        self.unresolved_conflicts = []
        
    def build(self):
        """Constrói a tabela de parsing LL(1)."""
        self.table = {}
        self.conflicts = []
        self.unresolved_conflicts = []
        
        for nt in self.grammar.nonterminals:
            for prod in self.grammar.productions[nt]:
                # Calcular FIRST da produção com EBNF
                first_prod = self._first_of_production(prod)
                
                # Regra 1: Para cada terminal em FIRST(α)
                for terminal in first_prod - {self.grammar.epsilon}:
                    self._add_entry(nt, terminal, prod)
                
                # Regra 2: Se ε ∈ FIRST(α), usar FOLLOW(A)
                if self.grammar.epsilon in first_prod:
                    for terminal in self.first_follow.follow[nt]:
                        self._add_entry(nt, terminal, prod)
        
        # Resolver conflitos
        self._resolve_conflicts()
        
        return self.table
    
    def _add_entry(self, nonterminal, terminal, production):
        """Adiciona entrada na tabela."""
        key = (nonterminal, terminal)
        
        if key in self.table:
            existing = self.table[key]
            
            # Não registrar duplicatas
            if existing == production:
                return
            
            conflict = {
                'cell': key,
                'existing': existing,
                'new': production,
                'resolved': False,
                'strategy': None
            }
            self.conflicts.append(conflict)
        else:
            self.table[key] = production
    
    def _resolve_conflicts(self):
        """
        DESABILITADO: Não resolve conflitos automaticamente.
        Se há conflitos, a gramática NÃO é LL(1).
        """
        # Marcar todos como não resolvidos
        for conflict in self.conflicts:
            conflict['resolved'] = False
            self.unresolved_conflicts.append(conflict)
        
        if self.unresolved_conflicts:
            print(f"[ERRO] {len(self.unresolved_conflicts)} conflito(s) detectado(s)")
            print(f"[ERRO] Gramática NÃO é LL(1)")
            print(f"[INFO] Corrija a gramática para eliminar conflitos")
    
    def _is_epsilon_production(self, production):
        """Verifica se produção é epsilon."""
        return (len(production) == 1 and 
                self.grammar.is_epsilon(production[0]))
    
    def _first_of_production(self, prod):
        """
        Calcula FIRST de uma produção processando EBNF diretamente.
        
        Regras EBNF:
        - A*  → FIRST(A) ∪ {ε}
        - A+  → FIRST(A)
        - A?  → FIRST(A) ∪ {ε}
        """
        result = set()
        
        # Epsilon
        if len(prod) == 1 and self.grammar.is_epsilon(prod[0]):
            return {self.grammar.epsilon}
        
        i = 0
        while i < len(prod):
            symbol = prod[i]
            
            # Verificar operador EBNF
            if i + 1 < len(prod) and prod[i + 1] in ['*', '+', '?']:
                operator = prod[i + 1]
                
                # Obter FIRST do símbolo
                if symbol in self.grammar.terminals:
                    first_sym = {symbol}
                else:
                    first_sym = self.first_follow.first.get(symbol, set())
                
                # Aplicar operador
                if operator == '*':
                    # A*: pode ser vazio, sempre continua
                    result.update(first_sym - {self.grammar.epsilon})
                    i += 2
                    if i >= len(prod):
                        result.add(self.grammar.epsilon)
                    continue
                    
                elif operator == '+':
                    # A+: não pode ser vazio
                    result.update(first_sym - {self.grammar.epsilon})
                    if self.grammar.epsilon not in first_sym:
                        break
                    i += 2
                    if i >= len(prod):
                        result.add(self.grammar.epsilon)
                    continue
                    
                elif operator == '?':
                    # A?: pode ser vazio, sempre continua
                    result.update(first_sym - {self.grammar.epsilon})
                    i += 2
                    if i >= len(prod):
                        result.add(self.grammar.epsilon)
                    continue
            
            # Símbolo normal (sem operador EBNF)
            # Terminal
            if symbol in self.grammar.terminals:
                result.add(symbol)
                break
            
            # Não-terminal
            first_sym = self.first_follow.first.get(symbol, set())
            result.update(first_sym - {self.grammar.epsilon})
            
            if self.grammar.epsilon not in first_sym:
                break
            
            i += 1
            if i >= len(prod):
                result.add(self.grammar.epsilon)
        
        return result
    
    def is_ll1(self):
        """Verifica se gramática é LL(1)."""
        return len(self.unresolved_conflicts) == 0
    
    def print_table(self):
        """Imprime tabela."""
        print("\n=== TABELA DE PARSING ===")
        print(f"{'NT':<30} {'T':<20} {'Produção':<50}")
        print("-" * 100)
        
        for (nt, term), prod in sorted(self.table.items()):
            prod_str = ' '.join(prod)
            print(f"{nt:<30} {term:<20} {prod_str:<50}")
    
    def print_conflicts(self):
        """Imprime conflitos."""
        if not self.conflicts:
            print("\n✅ Nenhum conflito! Gramática é LL(1)!")
            return
        
        print("\n=== CONFLITOS DETECTADOS ===")
        print(f"[ERRO] {len(self.conflicts)} conflito(s) encontrado(s)")
        print(f"[ERRO] Gramática NÃO é LL(1)")
        print()
        
        for i, conf in enumerate(self.conflicts, 1):
            nt, term = conf['cell']
            existing_str = ' '.join(conf['existing'])
            new_str = ' '.join(conf['new'])
            
            print(f"Conflito {i}: M[{nt}, {term}]")
            print(f"  Produção 1: {nt} ::= {existing_str}")
            print(f"  Produção 2: {nt} ::= {new_str}")
            print()
    
    def print_statistics(self):
        """Imprime estatísticas."""
        print("\n=== ESTATISTICAS ===")
        print(f"Entradas: {len(self.table)}")
        print(f"Conflitos detectados: {len(self.conflicts)}")
        
        if len(self.conflicts) == 0:
            print(f"LL(1)? ✅ SIM (sem conflitos)")
        else:
            print(f"LL(1)? ❌ NÃO ({len(self.conflicts)} conflitos)")
            print(f"\n⚠️  Uma gramática LL(1) NÃO pode ter conflitos.")
            print(f"    Corrija a gramática para eliminar os conflitos.")
    
    def save_to_files(self, table_file="parsing_table_output.txt", 
                      matrix_file="parsing_table_matrix.txt",
                      csv_file="parsing_table_matrix.csv"):
        """
        Salva tabela de parsing em múltiplos formatos.
        
        Args:
            table_file: Tabela em formato lista
            matrix_file: Tabela em formato matricial
            csv_file: Tabela em formato CSV
        """
        # 1. Formato lista
        with open(table_file, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("TABELA DE PARSING LL(1)\n")
            f.write("=" * 100 + "\n\n")
            
            # Estatísticas
            f.write("=== ESTATISTICAS ===\n")
            f.write(f"Entradas na tabela: {len(self.table)}\n")
            f.write(f"Conflitos resolvidos: {len([c for c in self.conflicts if c['resolved']])}\n")
            f.write(f"Conflitos irresolviveis: {len(self.unresolved_conflicts)}\n")
            is_ll1 = "SIM" if len(self.unresolved_conflicts) == 0 else "NAO"
            f.write(f"E LL(1)? {is_ll1}\n\n")
            
            # Conflitos
            if self.conflicts:
                f.write("=== CONFLITOS ===\n")
                for i, conf in enumerate(self.conflicts, 1):
                    nt, term = conf['cell']
                    f.write(f"Conflito {i}: M[{nt}, {term}]\n")
                    f.write(f"  Existente: {' '.join(conf['existing'])}\n")
                    f.write(f"  Nova: {' '.join(conf['new'])}\n")
                    if conf['resolved']:
                        f.write(f"  Status: RESOLVIDO ({conf['strategy']})\n")
                    else:
                        f.write(f"  Status: NAO RESOLVIDO\n")
                    f.write("\n")
            
            # Tabela
            f.write("=== TABELA ===\n")
            f.write(f"{'NAO-TERMINAL':<30} {'TERMINAL':<20} {'PRODUCAO':<50}\n")
            f.write("-" * 100 + "\n")
            
            for (nt, term), prod in sorted(self.table.items()):
                prod_str = ' '.join(prod)
                f.write(f"{nt:<30} {term:<20} {prod_str:<50}\n")
        
        print(f"[OK] Tabela salva em: {table_file}")
        
        # 2. Formato matricial
        all_nonterminals = sorted(self.grammar.nonterminals)
        all_terminals = sorted(self.grammar.terminals | {'$'})
        
        with open(matrix_file, 'w', encoding='utf-8') as f:
            f.write("=" * 150 + "\n")
            f.write("TABELA DE PARSING LL(1) - FORMATO MATRICIAL\n")
            f.write("=" * 150 + "\n\n")
            
            # Cabeçalho
            f.write(f"{'NT \\ T':<20}")
            for term in all_terminals[:10]:  # Primeiros 10 terminais
                f.write(f"{term:<15}")
            f.write("\n")
            f.write("-" * 150 + "\n")
            
            # Linhas
            for nt in all_nonterminals:
                f.write(f"{nt:<20}")
                for term in all_terminals[:10]:
                    prod = self.table.get((nt, term))
                    if prod:
                        prod_str = ' '.join(prod)[:13]
                        f.write(f"{prod_str:<15}")
                    else:
                        f.write(f"{'---':<15}")
                f.write("\n")
            
            f.write("\n" + "=" * 150 + "\n")
            f.write("[INFO] Matriz completa muito grande para exibir\n")
            f.write(f"[INFO] Use o arquivo CSV para visualizar completo\n")
            f.write("=" * 150 + "\n")
        
        print(f"[OK] Tabela matricial salva em: {matrix_file}")
        
        # 3. Formato CSV
        with open(csv_file, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("NT\\T")
            for term in all_terminals:
                f.write(f",{term}")
            f.write("\n")
            
            # Linhas
            for nt in all_nonterminals:
                f.write(nt)
                for term in all_terminals:
                    prod = self.table.get((nt, term))
                    if prod:
                        prod_str = ' '.join(prod).replace(',', ';')
                        f.write(f",\"{prod_str}\"")
                    else:
                        f.write(",")
                f.write("\n")
        
        print(f"[OK] Tabela CSV salva em: {csv_file}")
        print(f"[INFO] Abra em Excel/LibreOffice para visualizar sem truncamento")
        
        return table_file, matrix_file, csv_file
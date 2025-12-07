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
            # Conflito detectado
            conflict = {
                'cell': key,
                'existing': self.table[key],
                'new': production
            }
            self.conflicts.append(conflict)
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
    
    def print_table(self):
        """Imprime tabela formatada."""
        print("\n=== TABELA DE PARSING LL(1) ===")
        print(f"{'NÃO-TERMINAL':<25} {'TERMINAL':<20} {'PRODUÇÃO':<30}")
        print("-" * 75)
        
        for (nt, term), prod in sorted(self.table.items()):
            prod_str = ' '.join(prod)
            if len(prod_str) > 28:
                prod_str = prod_str[:25] + "..."
            print(f"{nt:<25} {term:<20} {prod_str:<30}")
        
        print(f"\nTotal: {len(self.table)} entradas")
    
    def print_conflicts(self):
        """Imprime conflitos detectados."""
        print("\n=== DETECÇÃO DE CONFLITOS ===")
        
        if not self.conflicts:
            print("✓ Nenhum conflito detectado")
            print("✓ Gramática é LL(1)")
        else:
            print(f"✗ {len(self.conflicts)} conflito(s) detectado(s)")
            print("✗ Gramática NÃO é LL(1)\n")
            
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
        
        print("\n=== ESTATÍSTICAS ===")
        print(f"Entradas na tabela: {len(self.table)}")
        print(f"Não-terminais com entradas: {nts_used}")
        print(f"Terminais utilizados: {terms_used}")
        print(f"Conflitos: {len(self.conflicts)}")
        print(f"É LL(1)? {'✓ SIM' if self.is_ll1() else '✗ NÃO'}")


if __name__ == "__main__":
    from grammar import Grammar
    from firstFollow import FirstFollow
    
    # Carregar gramática
    g = Grammar()
    g.load_from_file("gramatica_sem_ambiguidade.bnf")
    
    print("=" * 60)
    print("CONSTRUÇÃO DA TABELA DE PARSING LL(1)")
    print("=" * 60)
    
    # Calcular First e Follow
    print("\nCalculando First e Follow...")
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    print("✓ First e Follow calculados")
    
    # Construir tabela
    print("\nConstruindo tabela LL(1)...")
    pt = ParsingTable(g, ff)
    pt.build()
    print("✓ Tabela construída")
    
    # Mostrar resultados
    pt.print_conflicts()
    pt.print_statistics()
    pt.print_table()
    
    print("\n" + "=" * 60)
from collections import defaultdict

class FirstFollow:
    """Calcula conjuntos First e Follow para análise LL(1)."""
    
    def __init__(self, grammar):
        """Inicializa com uma gramática carregada."""
        self.grammar = grammar
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        
    def compute_first(self):
        """Calcula conjunto First para todos os símbolos da gramática."""
        for terminal in self.grammar.terminals:
            self.first[terminal] = {terminal}
        
        changed = True
        while changed:
            changed = False
            for nt in self.grammar.nonterminals:
                for prod in self.grammar.productions[nt]:
                    old_size = len(self.first[nt])
                    self._first_of_production(nt, prod)
                    if len(self.first[nt]) > old_size:
                        changed = True
        
        return self.first
    
    def _first_of_production(self, nt, prod):
        """Adiciona First de uma produção ao não-terminal."""
        if self.grammar.is_epsilon(prod[0]):
            self.first[nt].add(self.grammar.epsilon)
            return
        
        for i, symbol in enumerate(prod):
            if symbol in self.grammar.terminals:
                self.first[nt].add(symbol)
                break
            
            first_sym = self.first[symbol] - {self.grammar.epsilon}
            self.first[nt].update(first_sym)
            
            if self.grammar.epsilon not in self.first[symbol]:
                break
            
            if i == len(prod) - 1:
                self.first[nt].add(self.grammar.epsilon)
    
    def compute_follow(self):
        """Calcula conjunto Follow para todos os não-terminais."""
        self.follow[self.grammar.start_symbol].add('$')
        
        changed = True
        while changed:
            changed = False
            for nt in self.grammar.nonterminals:
                for prod in self.grammar.productions[nt]:
                    for i, symbol in enumerate(prod):
                        if symbol not in self.grammar.nonterminals:
                            continue
                        
                        old_size = len(self.follow[symbol])
                        
                        rest = prod[i+1:]
                        if not rest:
                            self.follow[symbol].update(self.follow[nt])
                        else:
                            first_rest = self._first_of_sequence(rest)
                            self.follow[symbol].update(first_rest - {self.grammar.epsilon})
                            
                            if self.grammar.epsilon in first_rest:
                                self.follow[symbol].update(self.follow[nt])
                        
                        if len(self.follow[symbol]) > old_size:
                            changed = True
        
        return self.follow
    
    def _first_of_sequence(self, sequence):
        """Calcula First de uma sequência de símbolos."""
        result = set()
        
        for symbol in sequence:
            if symbol in self.grammar.terminals:
                result.add(symbol)
                break
            
            first_sym = self.first[symbol]
            result.update(first_sym - {self.grammar.epsilon})
            
            if self.grammar.epsilon not in first_sym:
                break
        else:
            result.add(self.grammar.epsilon)
        
        return result
    
    def print_sets(self):
        """Exibe conjuntos First e Follow ordenados."""
        print("\n=== FIRST ===")
        for nt in sorted(self.grammar.nonterminals):
            first_list = sorted(self.first[nt], key=lambda x: (x != self.grammar.epsilon, x))
            print(f"{nt}: {{{', '.join(first_list)}}}")
        
        print("\n=== FOLLOW ===")
        for nt in sorted(self.grammar.nonterminals):
            follow_list = sorted(self.follow[nt], key=lambda x: (x != '$', x))
            print(f"{nt}: {{{', '.join(follow_list)}}}")


if __name__ == "__main__":
    from grammar import Grammar
    
    g = Grammar()
    g.load_from_file("grammar.txt")
    
    ff = FirstFollow(g)
    ff.compute_first()
    ff.compute_follow()
    ff.print_sets()
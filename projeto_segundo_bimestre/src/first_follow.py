from collections import defaultdict

class FirstFollow:
    """Calcula First e Follow processando EBNF diretamente."""
    
    def __init__(self, grammar):
        self.grammar = grammar
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        
    def compute_first(self):
        """Calcula FIRST para todos os símbolos."""
        # FIRST de terminais
        for terminal in self.grammar.terminals:
            self.first[terminal] = {terminal}
        
        # Algoritmo de ponto fixo
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
        """Calcula FIRST de uma produção com EBNF."""
        # Produção epsilon
        if len(prod) == 1 and self.grammar.is_epsilon(prod[0]):
            self.first[nt].add(self.grammar.epsilon)
            return
        
        i = 0
        while i < len(prod):
            symbol = prod[i]
            
            # Verificar se próximo é operador EBNF
            if i + 1 < len(prod) and prod[i + 1] in ['*', '+', '?']:
                operator = prod[i + 1]
                first_sym = self._first_of_ebnf(symbol, operator)
                
                # A* e A?: adicionar FIRST e continuar (pode derivar ε)
                if operator in ['*', '?']:
                    self.first[nt].update(first_sym - {self.grammar.epsilon})
                    # Sempre continua (pode ser vazio)
                    i += 2
                    if i >= len(prod):
                        # Se último, adicionar ε
                        self.first[nt].add(self.grammar.epsilon)
                    continue
                
                # A+: adicionar FIRST e parar se não deriva ε
                elif operator == '+':
                    self.first[nt].update(first_sym - {self.grammar.epsilon})
                    if self.grammar.epsilon not in first_sym:
                        break
                    i += 2
                    if i >= len(prod):
                        self.first[nt].add(self.grammar.epsilon)
                    continue
            
            # Símbolo normal (sem operador EBNF)
            # Terminal
            if symbol in self.grammar.terminals:
                self.first[nt].add(symbol)
                break
            
            # Não-terminal
            first_sym = self.first.get(symbol, set())
            self.first[nt].update(first_sym - {self.grammar.epsilon})
            
            if self.grammar.epsilon not in first_sym:
                break
            
            i += 1
            if i >= len(prod):
                self.first[nt].add(self.grammar.epsilon)
    
    def _first_of_ebnf(self, symbol, operator):
        """
        Calcula FIRST de expressão EBNF.
        
        A* → FIRST(A) ∪ {ε}
        A+ → FIRST(A)
        A? → FIRST(A) ∪ {ε}
        """
        if symbol in self.grammar.terminals:
            base_first = {symbol}
        else:
            base_first = self.first.get(symbol, set())
        
        if operator == '*':
            # A* pode ser vazio
            return base_first | {self.grammar.epsilon}
        elif operator == '+':
            # A+ não pode ser vazio
            return base_first
        elif operator == '?':
            # A? pode ser vazio
            return base_first | {self.grammar.epsilon}
        
        return base_first
    
    def compute_follow(self):
        """Calcula FOLLOW para todos os não-terminais."""
        # $ no FOLLOW do símbolo inicial
        self.follow[self.grammar.start_symbol].add('$')
        
        # Algoritmo de ponto fixo
        changed = True
        while changed:
            changed = False
            for nt in self.grammar.nonterminals:
                for prod in self.grammar.productions[nt]:
                    old_follows = {n: set(f) for n, f in self.follow.items()}
                    self._follow_of_production(nt, prod)
                    
                    for n in self.grammar.nonterminals:
                        if self.follow[n] != old_follows.get(n, set()):
                            changed = True
                            break
        
        return self.follow
    
    def _follow_of_production(self, nt, prod):
        """Atualiza FOLLOW baseado em uma produção com EBNF."""
        i = 0
        while i < len(prod):
            symbol = prod[i]
            
            # Só processar não-terminais
            if symbol not in self.grammar.nonterminals:
                i += 1
                continue
            
            # Verificar se próximo é operador EBNF
            next_is_ebnf_op = (i + 1 < len(prod) and prod[i + 1] in ['*', '+', '?'])
            
            if next_is_ebnf_op:
                operator = prod[i + 1]
                
                # Para A* e A+: FOLLOW(A) inclui FIRST(A) (recursão)
                if operator in ['*', '+']:
                    self.follow[symbol].update(self.first.get(symbol, set()) - {self.grammar.epsilon})
                
                # Verificar o que vem depois do operador
                if i + 2 < len(prod):
                    beta = prod[i + 2:]
                    first_beta = self._first_of_string(beta)
                    self.follow[symbol].update(first_beta - {self.grammar.epsilon})
                    
                    if self.grammar.epsilon in first_beta:
                        self.follow[symbol].update(self.follow[nt])
                else:
                    # A* é último: FOLLOW(A) inclui FOLLOW(nt)
                    self.follow[symbol].update(self.follow[nt])
                
                i += 2
            else:
                # Símbolo normal
                if i + 1 < len(prod):
                    beta = prod[i + 1:]
                    first_beta = self._first_of_string(beta)
                    self.follow[symbol].update(first_beta - {self.grammar.epsilon})
                    
                    if self.grammar.epsilon in first_beta:
                        self.follow[symbol].update(self.follow[nt])
                else:
                    self.follow[symbol].update(self.follow[nt])
                
                i += 1
    
    def _first_of_string(self, string):
        """Calcula FIRST de uma string de símbolos com EBNF."""
        result = set()
        
        i = 0
        while i < len(string):
            symbol = string[i]
            
            # Verificar operador EBNF
            if i + 1 < len(string) and string[i + 1] in ['*', '+', '?']:
                operator = string[i + 1]
                first_sym = self._first_of_ebnf(symbol, operator)
                result.update(first_sym - {self.grammar.epsilon})
                
                # A* e A? sempre podem ser vazios, continuar
                if operator in ['*', '?']:
                    i += 2
                    if i >= len(string):
                        result.add(self.grammar.epsilon)
                    continue
                
                # A+ só continua se deriva epsilon
                elif operator == '+':
                    if self.grammar.epsilon not in first_sym:
                        break
                    i += 2
                    if i >= len(string):
                        result.add(self.grammar.epsilon)
                    continue
            
            # Terminal
            if symbol in self.grammar.terminals:
                result.add(symbol)
                break
            
            # Não-terminal
            first_sym = self.first.get(symbol, set())
            result.update(first_sym - {self.grammar.epsilon})
            
            if self.grammar.epsilon not in first_sym:
                break
            
            i += 1
            if i >= len(string):
                result.add(self.grammar.epsilon)
        
        return result
    
    def debug_print(self):
        """Imprime First e Follow."""
        print("\n=== FIRST SETS ===")
        for symbol in sorted(self.first.keys()):
            if symbol in self.grammar.nonterminals:
                print(f"FIRST({symbol}) = {self.first[symbol]}")
        
        print("\n=== FOLLOW SETS ===")
        for nt in sorted(self.grammar.nonterminals):
            print(f"FOLLOW({nt}) = {self.follow[nt]}")
    
    def save_to_files(self, first_file="first_output.txt", follow_file="follow_output.txt"):
        """
        Salva conjuntos FIRST e FOLLOW em arquivos separados.
        
        Args:
            first_file: Arquivo para salvar FIRST
            follow_file: Arquivo para salvar FOLLOW
        """
        # Salvar FIRST
        with open(first_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("CONJUNTOS FIRST\n")
            f.write("=" * 70 + "\n\n")
            
            # Não-terminais
            f.write("=== NÃO-TERMINAIS ===\n\n")
            for nt in sorted(self.grammar.nonterminals):
                first_set = sorted(self.first.get(nt, set()))
                f.write(f"FIRST({nt})\n")
                for item in first_set:
                    f.write(f"  {item}\n")
                f.write("\n")
            
            # Terminais (para completude)
            f.write("=== TERMINAIS ===\n\n")
            for term in sorted(self.grammar.terminals):
                f.write(f"FIRST({term}) = {{{term}}}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write(f"Total de símbolos: {len(self.first)}\n")
            f.write("=" * 70 + "\n")
        
        # Salvar FOLLOW
        with open(follow_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("CONJUNTOS FOLLOW\n")
            f.write("=" * 70 + "\n\n")
            
            for nt in sorted(self.grammar.nonterminals):
                follow_set = sorted(self.follow.get(nt, set()))
                f.write(f"FOLLOW({nt})\n")
                for item in follow_set:
                    f.write(f"  {item}\n")
                f.write("\n")
            
            f.write("=" * 70 + "\n")
            f.write(f"Total de não-terminais: {len(self.grammar.nonterminals)}\n")
            f.write("=" * 70 + "\n")
        
        print(f"[OK] FIRST salvo em: {first_file}")
        print(f"[OK] FOLLOW salvo em: {follow_file}")
        
        return first_file, follow_file
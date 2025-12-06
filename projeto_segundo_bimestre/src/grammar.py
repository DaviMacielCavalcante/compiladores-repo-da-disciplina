import re
import os
from collections import defaultdict

class Grammar:
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = defaultdict(list)
        self.start_symbol = None
        self.epsilon = 'ε'  # Símbolo epsilon

    def load_from_file(self, filepath):
        # Resolve caminho relativo ao script
        if not os.path.isabs(filepath):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(script_dir, filepath)
        
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "::=" in line:
                self._parse_rule(line)
        
        # Adiciona epsilon aos terminais se usado
        if self.epsilon in self.terminals:
            self.terminals.remove(self.epsilon)

    def _parse_rule(self, line):
        left, right = line.split("::=")
        left = left.strip()

        if self.start_symbol is None:
            self.start_symbol = left

        self.nonterminals.add(left)

        # Divide por | IGNORANDO | dentro de aspas
        alternatives = self._split_alternatives(right)
        
        for alt in alternatives:
            symbols = self._tokenize(alt)
            
            # Se alternativa vazia ou apenas epsilon
            if not symbols or (len(symbols) == 1 and symbols[0] == self.epsilon):
                self.productions[left].append([self.epsilon])
            else:
                self.productions[left].append(symbols)
                
                for sym in symbols:
                    if sym == self.epsilon:
                        continue
                    elif self._is_nonterminal(sym):
                        self.nonterminals.add(sym)
                    else:
                        self.terminals.add(sym)

    def _split_alternatives(self, text):
        """Divide por | respeitando strings entre aspas"""
        alternatives = []
        current = []
        in_string = False
        quote_char = None
        
        for char in text:
            if char in ("'", '"') and not in_string:
                in_string = True
                quote_char = char
                current.append(char)
            elif char == quote_char and in_string:
                in_string = False
                quote_char = None
                current.append(char)
            elif char == '|' and not in_string:
                alternatives.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
        
        if current:
            alternatives.append(''.join(current).strip())
        
        return alternatives

    def _tokenize(self, text):
        """Tokeniza uma produção BNF"""
        # Remove espaços extras
        text = text.strip()
        
        # Se vazio ou epsilon
        if not text or text == self.epsilon:
            return [self.epsilon]
        
        # Pattern CORRIGIDO:
        # - Não-terminais: <...>
        # - Terminais entre aspas simples: '...' (incluindo escapados)
        # - Terminais entre aspas duplas: "..."
        # - Palavras especiais: IDENTIFIER, NUMBER, STRING, EOF, True, False
        # - Operadores compostos: ==, !=, <=, >=, **
        # - Epsilon: ε
        # - Espaços (para remover depois)
        # IMPORTANTE: SEM . no final para evitar quebrar caracteres dentro de strings
        pattern = r"<[^>]+>|'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|IDENTIFIER|NUMBER|STRING|EOF|True|False|==|!=|<=|>=|\*\*|ε|\s+"
        
        tokens = re.findall(pattern, text)
        
        # Remove espaços
        tokens = [t for t in tokens if t.strip() and not t.isspace()]
        
        return tokens if tokens else [self.epsilon]

    def _is_nonterminal(self, symbol):
        """Verifica se símbolo é não-terminal"""
        return symbol.startswith("<") and symbol.endswith(">")
    
    def is_epsilon(self, symbol):
        """Verifica se símbolo é epsilon"""
        return symbol == self.epsilon
    
    def has_epsilon_production(self, nonterminal):
        """Verifica se não-terminal deriva epsilon"""
        if nonterminal not in self.productions:
            return False
        
        for prod in self.productions[nonterminal]:
            if len(prod) == 1 and self.is_epsilon(prod[0]):
                return True
        return False

    def debug_print(self):
        print("=" * 60)
        print("GRAMÁTICA CARREGADA")
        print("=" * 60)
        print(f"\nSTART SYMBOL: {self.start_symbol}")
        print(f"\nNÚMERO DE NÃO-TERMINAIS: {len(self.nonterminals)}")
        print(f"NÃO-TERMINAIS: {sorted(self.nonterminals)}")
        print(f"\nNÚMERO DE TERMINAIS: {len(self.terminals)}")
        print(f"TERMINAIS: {sorted(self.terminals)}")
        print(f"\nNÚMERO DE PRODUÇÕES: {sum(len(prods) for prods in self.productions.values())}")
        print("\nPRODUÇÕES:")
        print("-" * 60)
        
        for nt in sorted(self.productions.keys()):
            for i, prod in enumerate(self.productions[nt], 1):
                prod_str = ' '.join(prod)
                print(f"  {nt} ::= {prod_str}")
        
        print("=" * 60)
        
        # Estatísticas
        epsilon_prods = [nt for nt in self.nonterminals if self.has_epsilon_production(nt)]
        if epsilon_prods:
            print(f"\nNÃO-TERMINAIS COM PRODUÇÃO EPSILON: {len(epsilon_prods)}")
            print(f"  {sorted(epsilon_prods)}")
        
        print("=" * 60)
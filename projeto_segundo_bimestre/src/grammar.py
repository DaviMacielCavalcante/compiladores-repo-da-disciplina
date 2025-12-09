"""
Classe Grammar que lê EBNF SEM converter para BNF
Mantém operadores *, +, ? nas produções
"""

import re
from collections import defaultdict


class Grammar:
    """Gramática que lê EBNF mas não converte."""
    
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = defaultdict(list)
        self.start_symbol = None
        self.epsilon = 'ε'
        
    def load_from_file(self, filepath):
        """Carrega gramática de arquivo mantendo EBNF."""
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Juntar linhas de continuação (que começam com |)
        merged_lines = []
        current_rule = None
        
        for line in lines:
            stripped = line.strip()
            
            # Ignorar vazias e comentários
            if not stripped or stripped.startswith("#"):
                continue
            
            # Linha começa com | → continuação
            if stripped.startswith("|"):
                if current_rule is not None:
                    current_rule += " " + stripped
                continue
            
            # Linha tem ::= → nova regra
            if "::=" in stripped:
                if current_rule is not None:
                    merged_lines.append(current_rule)
                current_rule = stripped
                continue
            
            # Continuação sem |
            if current_rule is not None:
                current_rule += " " + stripped
        
        # Última regra
        if current_rule is not None:
            merged_lines.append(current_rule)
        
        # Processar cada regra
        for rule in merged_lines:
            self._parse_rule(rule)
    
    def _parse_rule(self, line):
        """Parse uma regra sem converter EBNF."""
        left, right = line.split("::=", 1)
        left = left.strip()
        
        if self.start_symbol is None:
            self.start_symbol = left
        
        self.nonterminals.add(left)
        
        # Processar alternativas (|)
        alternatives = self._split_alternatives(right)
        
        for alt in alternatives:
            symbols = self._tokenize(alt.strip())
            
            if symbols:
                self.productions[left].append(symbols)
                
                # Registrar terminais e não-terminais
                for sym in symbols:
                    # Pular operadores EBNF
                    if sym in ['*', '+', '?']:
                        continue
                    
                    if self._is_nonterminal(sym):
                        self.nonterminals.add(sym)
                    elif sym != self.epsilon:
                        self.terminals.add(sym)
    
    def _split_alternatives(self, text):
        """Divide alternativas por | respeitando parênteses."""
        alternatives = []
        current = []
        depth = 0
        
        i = 0
        while i < len(text):
            char = text[i]
            
            if char == '(':
                depth += 1
                current.append(char)
            elif char == ')':
                depth -= 1
                current.append(char)
            elif char == '|' and depth == 0:
                alternatives.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
            
            i += 1
        
        if current:
            alternatives.append(''.join(current).strip())
        
        return alternatives
    
    def _tokenize(self, text):
        """
        Tokeniza sem processar EBNF.
        Mantém *, +, ? como símbolos separados.
        """
        tokens = []
        i = 0
        
        while i < len(text):
            # Pular espaços
            if text[i].isspace():
                i += 1
                continue
            
            # Não-terminal <...>
            if text[i] == '<':
                end = text.find('>', i)
                if end != -1:
                    tokens.append(text[i:end+1])
                    i = end + 1
                    continue
            
            # Terminal '...'
            if text[i] == "'":
                end = text.find("'", i + 1)
                if end != -1:
                    tokens.append(text[i:end+1])
                    i = end + 1
                    continue
            
            # Grupo (...)
            if text[i] == '(':
                depth = 1
                j = i + 1
                while j < len(text) and depth > 0:
                    if text[j] == '(':
                        depth += 1
                    elif text[j] == ')':
                        depth -= 1
                    j += 1
                tokens.append(text[i:j])
                i = j
                continue
            
            # Operadores EBNF (manter como tokens)
            if text[i] in '*+?':
                tokens.append(text[i])
                i += 1
                continue
            
            # Operadores multi-char
            if i + 1 < len(text):
                two_char = text[i:i+2]
                if two_char in ['**', '==', '!=', '<=', '>=', '::']:
                    tokens.append(two_char)
                    i += 2
                    continue
            
            # Palavra ou símbolo único
            if text[i].isalnum() or text[i] == '_':
                j = i
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                word = text[i:j]
                
                # Normalizar tokens especiais com aspas
                if word in ['IDENTIFIER', 'NUMBER', 'STRING', 'True', 'False', 'EOF']:
                    tokens.append(f"'{word}'")
                else:
                    tokens.append(word)
                
                i = j
            else:
                # Símbolo único
                tokens.append(text[i])
                i += 1
        
        return tokens
    
    def _is_nonterminal(self, symbol):
        """Verifica se símbolo é não-terminal."""
        return symbol.startswith("<") and symbol.endswith(">")
    
    def is_epsilon(self, symbol):
        """Verifica se símbolo é epsilon."""
        if isinstance(symbol, list):
            return len(symbol) == 1 and self.is_epsilon(symbol[0])
        return symbol in ['ε', 'epsilon', 'EPSILON', self.epsilon]
    
    def debug_print(self):
        """Imprime gramática para debug."""
        print("=" * 60)
        print("GRAMÁTICA (EBNF - SEM CONVERSÃO)")
        print("=" * 60)
        print(f"Símbolo inicial: {self.start_symbol}")
        print(f"Não-terminais: {len(self.nonterminals)}")
        print(f"Terminais: {len(self.terminals)}")
        print(f"Produções: {sum(len(prods) for prods in self.productions.values())}")
        print()
        print("PRODUÇÕES:")
        for nt in sorted(self.productions.keys()):
            for prod in self.productions[nt]:
                prod_str = ' '.join(prod)
                print(f"  {nt} ::= {prod_str}")
        print("=" * 60)
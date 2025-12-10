"""
=============================================================================
GRAMÁTICA ADAPTADA PARA SLR(1) - LINGUAGEM VYTHON
=============================================================================

Adaptação da gramática para análise SLR(1):
1. Gramática aumentada com símbolo inicial S' -> S
2. Produções numeradas para referência na tabela
3. Estruturas otimizadas para construção de itens LR(0)
=============================================================================
"""

from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
import os


@dataclass
class Production:
    """
    Representa uma produção numerada da gramática.
    
    Attributes:
        number: Número da produção (para referência em reduções)
        head: Lado esquerdo (não-terminal)
        body: Lado direito (lista de símbolos)
    """
    number: int
    head: str
    body: Tuple[str, ...]
    
    def __repr__(self):
        body_str = ' '.join(self.body) if self.body else 'ε'
        return f"({self.number}) {self.head} -> {body_str}"
    
    def __hash__(self):
        return hash((self.number, self.head, self.body))
    
    def __eq__(self, other):
        if not isinstance(other, Production):
            return False
        return self.number == other.number


class SLRGrammar:
    """
    Gramática adaptada para análise SLR(1).
    
    Características:
    - Gramática aumentada com S' -> S
    - Produções numeradas
    - Suporte a epsilon (ε)
    """
    
    EPSILON = 'ε'
    AUGMENTED_START = "<program'>"
    END_MARKER = '$'
    
    def __init__(self):
        self.productions: List[Production] = []
        self.nonterminals: Set[str] = set()
        self.terminals: Set[str] = set()
        self.start_symbol: str = None
        self.original_start: str = None
        self.prod_by_head: Dict[str, List[Production]] = defaultdict(list)
        
    def load_from_file(self, filepath: str):
        """
        Carrega gramática de arquivo BNF e adapta para SLR(1).
        """
        # Ler arquivo
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Juntar linhas de continuação
        merged_lines = []
        current_rule = None
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped or stripped.startswith('#'):
                continue
            
            if stripped.startswith('|'):
                if current_rule:
                    current_rule += ' ' + stripped
                continue
            
            if '::=' in stripped:
                if current_rule:
                    merged_lines.append(current_rule)
                current_rule = stripped
                continue
            
            if current_rule:
                current_rule += ' ' + stripped
        
        if current_rule:
            merged_lines.append(current_rule)
        
        # Processar regras
        prod_number = 1  # Produção 0 será a aumentada
        
        for rule in merged_lines:
            left, right = rule.split('::=', 1)
            left = left.strip()
            
            if self.original_start is None:
                self.original_start = left
            
            self.nonterminals.add(left)
            
            # Processar alternativas
            alternatives = self._split_alternatives(right)
            
            for alt in alternatives:
                symbols = self._tokenize(alt.strip())
                
                if symbols:
                    body = tuple(symbols)
                    prod = Production(prod_number, left, body)
                    self.productions.append(prod)
                    self.prod_by_head[left].append(prod)
                    prod_number += 1
                    
                    # Registrar terminais
                    for sym in symbols:
                        if not self._is_nonterminal(sym) and sym != self.EPSILON:
                            self.terminals.add(sym)
        
        # Criar gramática aumentada
        self._augment_grammar()
        
    def _augment_grammar(self):
        """
        Cria gramática aumentada adicionando S' -> S.
        """
        self.start_symbol = self.AUGMENTED_START
        self.nonterminals.add(self.start_symbol)
        
        # Produção 0: S' -> S
        augmented_prod = Production(0, self.start_symbol, (self.original_start,))
        self.productions.insert(0, augmented_prod)
        self.prod_by_head[self.start_symbol].insert(0, augmented_prod)
        
        # Adicionar $ aos terminais
        self.terminals.add(self.END_MARKER)
    
    def _split_alternatives(self, text: str) -> List[str]:
        """Divide alternativas por | respeitando parênteses e aspas."""
        alternatives = []
        current = []
        depth = 0
        in_quotes = False
        
        for char in text:
            if char == "'" and not in_quotes:
                in_quotes = True
                current.append(char)
            elif char == "'" and in_quotes:
                in_quotes = False
                current.append(char)
            elif in_quotes:
                current.append(char)
            elif char == '(':
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
        
        if current:
            alternatives.append(''.join(current).strip())
        
        return alternatives
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokeniza uma produção."""
        tokens = []
        i = 0
        
        while i < len(text):
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
            
            # Palavra ou símbolo
            if text[i].isalnum() or text[i] == '_':
                j = i
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                word = text[i:j]
                
                if word in ['IDENTIFIER', 'NUMBER', 'STRING', 'True', 'False', 'EOF']:
                    tokens.append(f"'{word}'")
                elif word == 'ε' or word == 'epsilon':
                    tokens.append(self.EPSILON)
                else:
                    tokens.append(word)
                i = j
            else:
                tokens.append(text[i])
                i += 1
        
        return tokens
    
    def _is_nonterminal(self, symbol: str) -> bool:
        """Verifica se símbolo é não-terminal."""
        return symbol.startswith('<') and symbol.endswith('>')
    
    def is_terminal(self, symbol: str) -> bool:
        """Verifica se símbolo é terminal."""
        return symbol in self.terminals or (
            not self._is_nonterminal(symbol) and 
            symbol != self.EPSILON
        )
    
    def is_nonterminal(self, symbol: str) -> bool:
        """Verifica se símbolo é não-terminal."""
        return symbol in self.nonterminals
    
    def is_epsilon(self, symbol: str) -> bool:
        """Verifica se símbolo é epsilon."""
        return symbol == self.EPSILON
    
    def get_production(self, number: int) -> Optional[Production]:
        """Retorna produção pelo número."""
        for prod in self.productions:
            if prod.number == number:
                return prod
        return None
    
    def get_productions_for(self, nonterminal: str) -> List[Production]:
        """Retorna produções de um não-terminal."""
        return self.prod_by_head.get(nonterminal, [])
    
    def print_grammar(self):
        """Imprime a gramática."""
        print("=" * 70)
        print("GRAMÁTICA AUMENTADA PARA SLR(1)")
        print("=" * 70)
        print(f"Símbolo inicial: {self.start_symbol}")
        print(f"Símbolo original: {self.original_start}")
        print(f"Não-terminais: {len(self.nonterminals)}")
        print(f"Terminais: {len(self.terminals)}")
        print(f"Produções: {len(self.productions)}")
        print()
        print("PRODUÇÕES NUMERADAS:")
        print("-" * 70)
        for prod in self.productions:
            print(f"  {prod}")
        print("=" * 70)
    
    def print_statistics(self):
        """Imprime estatísticas."""
        print(f"\nEstatísticas da Gramática SLR(1):")
        print(f"  - Produções: {len(self.productions)}")
        print(f"  - Não-terminais: {len(self.nonterminals)}")
        print(f"  - Terminais: {len(self.terminals)}")


# =============================================================================
# CÁLCULO DE FIRST E FOLLOW PARA SLR
# =============================================================================

class SLRFirstFollow:
    """
    Calcula conjuntos FIRST e FOLLOW para gramática SLR.
    """
    
    def __init__(self, grammar: SLRGrammar):
        self.grammar = grammar
        self.first: Dict[str, Set[str]] = defaultdict(set)
        self.follow: Dict[str, Set[str]] = defaultdict(set)
        
    def compute(self):
        """Calcula FIRST e FOLLOW."""
        self._compute_first()
        self._compute_follow()
        return self.first, self.follow
    
    def _compute_first(self):
        """Calcula FIRST para todos os símbolos."""
        # FIRST de terminais
        for terminal in self.grammar.terminals:
            self.first[terminal] = {terminal}
        
        # FIRST de epsilon
        self.first[self.grammar.EPSILON] = {self.grammar.EPSILON}
        
        # Algoritmo de ponto fixo para não-terminais
        changed = True
        while changed:
            changed = False
            
            for prod in self.grammar.productions:
                nt = prod.head
                old_size = len(self.first[nt])
                
                # Calcular FIRST da produção
                first_prod = self._first_of_sequence(prod.body)
                self.first[nt].update(first_prod)
                
                if len(self.first[nt]) > old_size:
                    changed = True
    
    def _compute_follow(self):
        """Calcula FOLLOW para todos os não-terminais."""
        # FOLLOW(S') = {$}
        self.follow[self.grammar.start_symbol].add(self.grammar.END_MARKER)
        
        # Algoritmo de ponto fixo
        changed = True
        while changed:
            changed = False
            
            for prod in self.grammar.productions:
                body = prod.body
                
                for i, symbol in enumerate(body):
                    if not self.grammar.is_nonterminal(symbol):
                        continue
                    
                    old_size = len(self.follow[symbol])
                    
                    # β = tudo depois do símbolo
                    beta = body[i+1:]
                    
                    if beta:
                        # FOLLOW(B) inclui FIRST(β) - {ε}
                        first_beta = self._first_of_sequence(beta)
                        self.follow[symbol].update(first_beta - {self.grammar.EPSILON})
                        
                        # Se ε ∈ FIRST(β), FOLLOW(B) inclui FOLLOW(A)
                        if self.grammar.EPSILON in first_beta:
                            self.follow[symbol].update(self.follow[prod.head])
                    else:
                        # B é último símbolo
                        self.follow[symbol].update(self.follow[prod.head])
                    
                    if len(self.follow[symbol]) > old_size:
                        changed = True
    
    def _first_of_sequence(self, sequence: Tuple[str, ...]) -> Set[str]:
        """Calcula FIRST de uma sequência de símbolos."""
        result = set()
        
        if not sequence:
            return {self.grammar.EPSILON}
        
        for symbol in sequence:
            if self.grammar.is_epsilon(symbol):
                result.add(self.grammar.EPSILON)
                continue
            
            first_sym = self.first.get(symbol, set())
            result.update(first_sym - {self.grammar.EPSILON})
            
            if self.grammar.EPSILON not in first_sym:
                break
        else:
            # Todos derivam ε
            result.add(self.grammar.EPSILON)
        
        return result
    
    def get_first(self, symbol: str) -> Set[str]:
        """Retorna FIRST de um símbolo."""
        return self.first.get(symbol, set())
    
    def get_follow(self, nonterminal: str) -> Set[str]:
        """Retorna FOLLOW de um não-terminal."""
        return self.follow.get(nonterminal, set())
    
    def print_sets(self):
        """Imprime FIRST e FOLLOW."""
        print("\n" + "=" * 70)
        print("CONJUNTOS FIRST")
        print("=" * 70)
        
        for nt in sorted(self.grammar.nonterminals):
            first_set = sorted(self.first.get(nt, set()))
            print(f"FIRST({nt})")
            print(f"  = {{{', '.join(first_set)}}}")
        
        print("\n" + "=" * 70)
        print("CONJUNTOS FOLLOW")
        print("=" * 70)
        
        for nt in sorted(self.grammar.nonterminals):
            follow_set = sorted(self.follow.get(nt, set()))
            print(f"FOLLOW({nt})")
            print(f"  = {{{', '.join(follow_set)}}}")


# =============================================================================
# TESTE DO MÓDULO
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        grammar_file = sys.argv[1]
    else:
        # Procurar gramatica_slr.bnf em docs/
        possible_paths = [
            "../docs/gramatica_slr.bnf",
            "docs/gramatica_slr.bnf",
            "gramatica_slr.bnf",
        ]
        grammar_file = None
        for path in possible_paths:
            if os.path.exists(path):
                grammar_file = path
                break
        if not grammar_file:
            grammar_file = "gramatica_slr.bnf"
    
    print("Carregando gramática...")
    print(f"  Procurando arquivo: {grammar_file}")
    grammar = SLRGrammar()
    
    try:
        grammar.load_from_file(grammar_file)
        grammar.print_grammar()
        
        print("\nCalculando FIRST e FOLLOW...")
        ff = SLRFirstFollow(grammar)
        ff.compute()
        ff.print_sets()
        
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {grammar_file}")
        print(f"   Diretório atual: {os.getcwd()}")
        print(f"   Caminhos tentados:")
        for p in possible_paths:
            exists = "✓" if os.path.exists(p) else "✗"
            print(f"     [{exists}] {p}")
    except Exception as e:
        print(f"Erro: {e}")
        raise
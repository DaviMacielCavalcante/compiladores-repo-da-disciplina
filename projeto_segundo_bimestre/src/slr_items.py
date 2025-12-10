"""
=============================================================================
ITENS LR(0) E COLEÇÃO CANÔNICA - PARSER SLR(1)
=============================================================================

Construção dos itens LR(0) e da coleção canônica de conjuntos de itens
para análise SLR(1).

Um item LR(0) é uma produção com um ponto (•) indicando a posição
atual do parser.

Exemplo:
    A -> α • β
    
    Onde α já foi visto e β é esperado.
=============================================================================
"""

from typing import List, Dict, Set, Tuple, FrozenSet, Optional
from dataclasses import dataclass
from collections import deque

from slr_grammar import SLRGrammar, Production


@dataclass(frozen=True)
class LR0Item:
    """
    Representa um item LR(0).
    
    Um item LR(0) é uma produção com uma posição marcada (•).
    
    Exemplo: A -> α • β
    - production: a produção original
    - dot_position: posição do ponto (0 = início)
    
    Attributes:
        production: A produção original
        dot_position: Posição do ponto (índice no corpo)
    """
    production: Production
    dot_position: int
    
    def __repr__(self):
        body = list(self.production.body)
        
        if not body or (len(body) == 1 and body[0] == 'ε'):
            # Produção epsilon
            return f"[{self.production.head} -> •]"
        
        # Inserir ponto na posição correta
        body_with_dot = body[:self.dot_position] + ['•'] + body[self.dot_position:]
        body_str = ' '.join(body_with_dot)
        
        return f"[{self.production.head} -> {body_str}]"
    
    def symbol_after_dot(self) -> Optional[str]:
        """
        Retorna o símbolo imediatamente após o ponto.
        Retorna None se o ponto está no final.
        """
        body = self.production.body
        
        # Tratar produção epsilon
        if len(body) == 1 and body[0] == 'ε':
            return None
        
        if self.dot_position < len(body):
            return body[self.dot_position]
        return None
    
    def is_complete(self) -> bool:
        """
        Verifica se o item está completo (ponto no final).
        Item completo indica que uma redução é possível.
        """
        body = self.production.body
        
        # Produção epsilon é sempre completa
        if len(body) == 1 and body[0] == 'ε':
            return True
        
        return self.dot_position >= len(body)
    
    def advance(self) -> 'LR0Item':
        """
        Cria novo item com ponto avançado uma posição.
        """
        return LR0Item(self.production, self.dot_position + 1)


class LR0ItemSet:
    """
    Representa um conjunto de itens LR(0) - um estado do autômato.
    """
    
    def __init__(self, items: Set[LR0Item] = None):
        self.items: FrozenSet[LR0Item] = frozenset(items) if items else frozenset()
        self._hash = None
    
    def __repr__(self):
        items_str = '\n    '.join(str(item) for item in sorted(self.items, key=str))
        return f"ItemSet({{\n    {items_str}\n  }})"
    
    def __eq__(self, other):
        if not isinstance(other, LR0ItemSet):
            return False
        return self.items == other.items
    
    def __hash__(self):
        if self._hash is None:
            self._hash = hash(self.items)
        return self._hash
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)
    
    def __contains__(self, item):
        return item in self.items


class CanonicalCollection:
    """
    Coleção canônica de conjuntos de itens LR(0).
    
    Constrói o autômato LR(0) usando:
    1. CLOSURE - expande itens com produções do símbolo após o ponto
    2. GOTO - transição para novo estado ao consumir um símbolo
    """
    
    def __init__(self, grammar: SLRGrammar):
        self.grammar = grammar
        self.states: List[LR0ItemSet] = []
        self.goto_table: Dict[Tuple[int, str], int] = {}
        self.state_index: Dict[FrozenSet[LR0Item], int] = {}
        
    def build(self):
        """
        Constrói a coleção canônica de conjuntos de itens LR(0).
        
        Algoritmo:
        1. Criar I0 = CLOSURE({[S' -> • S]})
        2. Para cada estado I e símbolo X:
           - Calcular GOTO(I, X)
           - Se não existe, adicionar à coleção
        3. Repetir até não haver novos estados
        """
        # Criar item inicial: S' -> • S
        augmented_prod = self.grammar.get_production(0)
        initial_item = LR0Item(augmented_prod, 0)
        
        # Estado inicial I0
        I0 = self._closure({initial_item})
        self.states.append(I0)
        self.state_index[I0.items] = 0
        
        # Worklist de estados a processar
        worklist = deque([0])
        
        while worklist:
            state_idx = worklist.popleft()
            state = self.states[state_idx]
            
            # Símbolos após o ponto neste estado
            symbols = set()
            for item in state:
                sym = item.symbol_after_dot()
                if sym and sym != 'ε':
                    symbols.add(sym)
            
            # Calcular GOTO para cada símbolo
            for symbol in symbols:
                goto_state = self._goto(state, symbol)
                
                if not goto_state.items:
                    continue
                
                # Verificar se estado já existe
                if goto_state.items in self.state_index:
                    target_idx = self.state_index[goto_state.items]
                else:
                    # Novo estado
                    target_idx = len(self.states)
                    self.states.append(goto_state)
                    self.state_index[goto_state.items] = target_idx
                    worklist.append(target_idx)
                
                # Registrar transição
                self.goto_table[(state_idx, symbol)] = target_idx
        
        return self.states
    
    def _closure(self, items: Set[LR0Item]) -> LR0ItemSet:
        """
        Calcula o CLOSURE de um conjunto de itens.
        
        CLOSURE(I):
        1. Adicionar todos os itens de I
        2. Se [A -> α • B β] está em I e B é não-terminal:
           - Adicionar [B -> • γ] para cada produção B -> γ
        3. Repetir até não haver mudanças
        
        Args:
            items: Conjunto inicial de itens
            
        Returns:
            LR0ItemSet com closure calculado
        """
        result = set(items)
        worklist = deque(items)
        added = set(items)
        
        while worklist:
            item = worklist.popleft()
            symbol = item.symbol_after_dot()
            
            if symbol and self.grammar.is_nonterminal(symbol):
                # Adicionar todas as produções de symbol
                for prod in self.grammar.get_productions_for(symbol):
                    # Tratar produção epsilon
                    if prod.body == ('ε',) or prod.body == (self.grammar.EPSILON,):
                        new_item = LR0Item(prod, 1)  # Ponto após epsilon
                    else:
                        new_item = LR0Item(prod, 0)  # Ponto no início
                    
                    if new_item not in added:
                        result.add(new_item)
                        added.add(new_item)
                        worklist.append(new_item)
        
        return LR0ItemSet(result)
    
    def _goto(self, state: LR0ItemSet, symbol: str) -> LR0ItemSet:
        """
        Calcula GOTO(I, X) - transição do estado I com símbolo X.
        
        GOTO(I, X):
        1. Para cada item [A -> α • X β] em I:
           - Adicionar [A -> α X • β]
        2. Retornar CLOSURE do resultado
        
        Args:
            state: Estado atual (conjunto de itens)
            symbol: Símbolo de transição
            
        Returns:
            Novo LR0ItemSet após a transição
        """
        moved_items = set()
        
        for item in state:
            if item.symbol_after_dot() == symbol:
                moved_items.add(item.advance())
        
        if not moved_items:
            return LR0ItemSet()
        
        return self._closure(moved_items)
    
    def get_goto(self, state_idx: int, symbol: str) -> Optional[int]:
        """Retorna índice do estado destino para GOTO(state, symbol)."""
        return self.goto_table.get((state_idx, symbol))
    
    def print_collection(self, max_states: int = None):
        """Imprime a coleção canônica."""
        print("\n" + "=" * 70)
        print("COLEÇÃO CANÔNICA DE CONJUNTOS DE ITENS LR(0)")
        print("=" * 70)
        print(f"Total de estados: {len(self.states)}")
        print(f"Total de transições: {len(self.goto_table)}")
        print()
        
        num_states = min(len(self.states), max_states) if max_states else len(self.states)
        
        for i in range(num_states):
            state = self.states[i]
            print(f"I{i}:")
            for item in sorted(state.items, key=str):
                print(f"    {item}")
            
            # Transições saindo deste estado
            transitions = [(sym, target) for (src, sym), target 
                          in self.goto_table.items() if src == i]
            if transitions:
                print(f"  Transições:")
                for sym, target in sorted(transitions, key=lambda x: x[0]):
                    print(f"    GOTO(I{i}, {sym}) = I{target}")
            print()
        
        if max_states and len(self.states) > max_states:
            print(f"  ... ({len(self.states) - max_states} estados omitidos)")
        
        print("=" * 70)
    
    def print_statistics(self):
        """Imprime estatísticas."""
        print(f"\nEstatísticas da Coleção Canônica:")
        print(f"  - Estados: {len(self.states)}")
        print(f"  - Transições: {len(self.goto_table)}")
        
        # Contar itens totais
        total_items = sum(len(state) for state in self.states)
        print(f"  - Itens totais: {total_items}")
        
        # Estados com conflitos potenciais (múltiplos itens completos)
        conflict_states = 0
        for state in self.states:
            complete_items = [item for item in state if item.is_complete()]
            if len(complete_items) > 1:
                conflict_states += 1
        print(f"  - Estados com múltiplas reduções: {conflict_states}")


# =============================================================================
# TESTE DO MÓDULO
# =============================================================================

if __name__ == "__main__":
    import sys
    import os
    from slr_grammar import SLRGrammar
    
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
    
    print("=" * 70)
    print("TESTE: CONSTRUÇÃO DE ITENS LR(0)")
    print("=" * 70)
    
    # Carregar gramática
    print(f"\n[1] Carregando gramática: {grammar_file}")
    grammar = SLRGrammar()
    
    try:
        grammar.load_from_file(grammar_file)
        print(f"    Produções: {len(grammar.productions)}")
        print(f"    Não-terminais: {len(grammar.nonterminals)}")
        print(f"    Terminais: {len(grammar.terminals)}")
    except FileNotFoundError:
        print(f"    ❌ ERRO: Arquivo não encontrado: {grammar_file}")
        print(f"    Diretório atual: {os.getcwd()}")
        sys.exit(1)
    
    # Construir coleção canônica
    print("\n[2] Construindo coleção canônica de itens LR(0)...")
    collection = CanonicalCollection(grammar)
    collection.build()
    
    collection.print_statistics()
    
    # Mostrar primeiros estados
    print("\n[3] Primeiros estados:")
    collection.print_collection(max_states=5)
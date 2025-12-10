"""
=============================================================================
TABELA DE PARSING SLR(1) - LINGUAGEM VYTHON
=============================================================================

Construção da tabela de parsing SLR(1) a partir da coleção canônica
de itens LR(0) e dos conjuntos FOLLOW.

A tabela possui duas partes:
1. ACTION[estado, terminal] -> shift/reduce/accept/error
2. GOTO[estado, não-terminal] -> próximo estado
=============================================================================
"""

from typing import Dict, List, Set, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum

from slr_grammar import SLRGrammar, SLRFirstFollow, Production
from slr_items import CanonicalCollection, LR0Item, LR0ItemSet


class ActionType(Enum):
    """Tipos de ação na tabela SLR."""
    SHIFT = "shift"
    REDUCE = "reduce"
    ACCEPT = "accept"
    ERROR = "error"


@dataclass
class Action:
    """
    Representa uma ação na tabela SLR.
    
    Tipos:
    - SHIFT n: empilha estado n
    - REDUCE n: reduz pela produção n
    - ACCEPT: aceita a entrada
    - ERROR: erro sintático
    """
    action_type: ActionType
    value: int = None  # Estado para shift, produção para reduce
    
    def __repr__(self):
        if self.action_type == ActionType.SHIFT:
            return f"s{self.value}"
        elif self.action_type == ActionType.REDUCE:
            return f"r{self.value}"
        elif self.action_type == ActionType.ACCEPT:
            return "acc"
        else:
            return ""
    
    def __eq__(self, other):
        if not isinstance(other, Action):
            return False
        return self.action_type == other.action_type and self.value == other.value
    
    def __hash__(self):
        return hash((self.action_type, self.value))


@dataclass
class SLRConflict:
    """Representa um conflito na tabela SLR."""
    state: int
    symbol: str
    actions: List[Action]
    conflict_type: str  # "shift-reduce" ou "reduce-reduce"
    
    def __repr__(self):
        actions_str = ', '.join(str(a) for a in self.actions)
        return f"Conflito {self.conflict_type} no estado {self.state}, símbolo '{self.symbol}': [{actions_str}]"


class SLRParsingTable:
    """
    Tabela de parsing SLR(1).
    
    Construção:
    1. Para cada estado I_i:
       a) Se [A -> α • a β] ∈ I_i e GOTO(I_i, a) = I_j:
          ACTION[i, a] = shift j
       b) Se [A -> α •] ∈ I_i (A ≠ S'):
          ACTION[i, a] = reduce A -> α, para todo a ∈ FOLLOW(A)
       c) Se [S' -> S •] ∈ I_i:
          ACTION[i, $] = accept
    
    2. Para cada não-terminal A:
       Se GOTO(I_i, A) = I_j:
          GOTO[i, A] = j
    """
    
    def __init__(self, grammar: SLRGrammar, collection: CanonicalCollection, 
                 first_follow: SLRFirstFollow):
        self.grammar = grammar
        self.collection = collection
        self.first_follow = first_follow
        
        # Tabelas
        self.action: Dict[Tuple[int, str], Action] = {}
        self.goto: Dict[Tuple[int, str], int] = {}
        
        # Conflitos
        self.conflicts: List[SLRConflict] = []
        
        # Estatísticas
        self.shift_count = 0
        self.reduce_count = 0
        self.accept_count = 0
        
    def build(self) -> bool:
        """
        Constrói a tabela de parsing SLR(1).
        
        Returns:
            True se não houver conflitos, False caso contrário.
        """
        # Processar cada estado
        for state_idx, state in enumerate(self.collection.states):
            self._process_state(state_idx, state)
        
        # Construir tabela GOTO
        self._build_goto_table()
        
        return len(self.conflicts) == 0
    
    def _process_state(self, state_idx: int, state: LR0ItemSet):
        """Processa um estado para gerar ações."""
        
        for item in state:
            symbol_after_dot = item.symbol_after_dot()
            
            if item.is_complete():
                # Item completo: A -> α •
                prod = item.production
                
                if prod.number == 0:
                    # Produção aumentada S' -> S •
                    self._add_action(state_idx, self.grammar.END_MARKER,
                                   Action(ActionType.ACCEPT))
                else:
                    # Redução: ACTION[i, a] = reduce para a ∈ FOLLOW(A)
                    follow_set = self.first_follow.get_follow(prod.head)
                    
                    for terminal in follow_set:
                        self._add_action(state_idx, terminal,
                                       Action(ActionType.REDUCE, prod.number))
            
            elif symbol_after_dot and self.grammar.is_terminal(symbol_after_dot):
                # Shift: A -> α • a β
                target = self.collection.get_goto(state_idx, symbol_after_dot)
                
                if target is not None:
                    self._add_action(state_idx, symbol_after_dot,
                                   Action(ActionType.SHIFT, target))
    
    def _add_action(self, state: int, symbol: str, action: Action):
        """
        Adiciona ação à tabela, detectando conflitos.
        """
        key = (state, symbol)
        
        if key in self.action:
            existing = self.action[key]
            
            if existing != action:
                # Conflito detectado
                conflict_type = self._get_conflict_type(existing, action)
                
                # Verificar se conflito já foi registrado
                existing_conflict = None
                for c in self.conflicts:
                    if c.state == state and c.symbol == symbol:
                        existing_conflict = c
                        break
                
                if existing_conflict:
                    if action not in existing_conflict.actions:
                        existing_conflict.actions.append(action)
                else:
                    self.conflicts.append(SLRConflict(
                        state=state,
                        symbol=symbol,
                        actions=[existing, action],
                        conflict_type=conflict_type
                    ))
        else:
            self.action[key] = action
            
            # Estatísticas
            if action.action_type == ActionType.SHIFT:
                self.shift_count += 1
            elif action.action_type == ActionType.REDUCE:
                self.reduce_count += 1
            elif action.action_type == ActionType.ACCEPT:
                self.accept_count += 1
    
    def _get_conflict_type(self, action1: Action, action2: Action) -> str:
        """Determina o tipo de conflito."""
        types = {action1.action_type, action2.action_type}
        
        if ActionType.SHIFT in types and ActionType.REDUCE in types:
            return "shift-reduce"
        elif types == {ActionType.REDUCE}:
            return "reduce-reduce"
        else:
            return "unknown"
    
    def _build_goto_table(self):
        """Constrói a tabela GOTO para não-terminais."""
        for (state_idx, symbol), target in self.collection.goto_table.items():
            if self.grammar.is_nonterminal(symbol):
                self.goto[(state_idx, symbol)] = target
    
    def get_action(self, state: int, terminal: str) -> Optional[Action]:
        """Retorna ação para (estado, terminal)."""
        return self.action.get((state, terminal))
    
    def get_goto(self, state: int, nonterminal: str) -> Optional[int]:
        """Retorna próximo estado para GOTO(estado, não-terminal)."""
        return self.goto.get((state, nonterminal))
    
    def is_slr1(self) -> bool:
        """Verifica se a gramática é SLR(1) (sem conflitos)."""
        return len(self.conflicts) == 0
    
    def print_table(self, max_states: int = None):
        """Imprime a tabela de parsing."""
        print("\n" + "=" * 100)
        print("TABELA DE PARSING SLR(1)")
        print("=" * 100)
        
        # Coletar terminais e não-terminais usados
        terminals = sorted(self.grammar.terminals)
        nonterminals = sorted(self.grammar.nonterminals - {self.grammar.start_symbol})
        
        num_states = len(self.collection.states)
        if max_states:
            num_states = min(num_states, max_states)
        
        # Cabeçalho
        print(f"\n{'Estado':<8}", end="")
        print("| ACTION", end="")
        print(" " * (len(terminals) * 8 - 6), end="")
        print("| GOTO")
        
        print(f"{'':8}", end="")
        for t in terminals[:10]:  # Limitar terminais mostrados
            t_display = t[:6] if len(t) > 6 else t
            print(f"{t_display:>8}", end="")
        if len(terminals) > 10:
            print("  ...", end="")
        print(" |", end="")
        for nt in nonterminals[:5]:  # Limitar NTs mostrados
            nt_display = nt[1:-1][:6] if nt.startswith('<') else nt[:6]
            print(f"{nt_display:>8}", end="")
        if len(nonterminals) > 5:
            print("  ...")
        else:
            print()
        
        print("-" * 100)
        
        # Linhas
        for state_idx in range(num_states):
            print(f"{state_idx:<8}", end="")
            
            # ACTION
            for t in terminals[:10]:
                action = self.get_action(state_idx, t)
                if action:
                    print(f"{str(action):>8}", end="")
                else:
                    print(f"{'':>8}", end="")
            if len(terminals) > 10:
                print("  ...", end="")
            
            print(" |", end="")
            
            # GOTO
            for nt in nonterminals[:5]:
                goto = self.get_goto(state_idx, nt)
                if goto is not None:
                    print(f"{goto:>8}", end="")
                else:
                    print(f"{'':>8}", end="")
            
            print()
        
        if max_states and len(self.collection.states) > max_states:
            print(f"... ({len(self.collection.states) - max_states} estados omitidos)")
        
        print("=" * 100)
    
    def print_conflicts(self):
        """Imprime conflitos detectados."""
        if not self.conflicts:
            print("\n✅ Nenhum conflito detectado! Gramática é SLR(1).")
            return
        
        print("\n" + "=" * 70)
        print(f"⚠️  CONFLITOS DETECTADOS: {len(self.conflicts)}")
        print("=" * 70)
        
        for i, conflict in enumerate(self.conflicts, 1):
            print(f"\nConflito {i}: {conflict.conflict_type.upper()}")
            print(f"  Estado: {conflict.state}")
            print(f"  Símbolo: {conflict.symbol}")
            print(f"  Ações conflitantes:")
            for action in conflict.actions:
                if action.action_type == ActionType.SHIFT:
                    print(f"    - SHIFT para estado {action.value}")
                elif action.action_type == ActionType.REDUCE:
                    prod = self.grammar.get_production(action.value)
                    print(f"    - REDUCE pela produção {action.value}: {prod}")
        
        print("\n" + "=" * 70)
    
    def print_statistics(self):
        """Imprime estatísticas da tabela."""
        print(f"\nEstatísticas da Tabela SLR(1):")
        print(f"  - Estados: {len(self.collection.states)}")
        print(f"  - Entradas ACTION: {len(self.action)}")
        print(f"  - Entradas GOTO: {len(self.goto)}")
        print(f"  - Shifts: {self.shift_count}")
        print(f"  - Reduces: {self.reduce_count}")
        print(f"  - Accepts: {self.accept_count}")
        print(f"  - Conflitos: {len(self.conflicts)}")
        print(f"  - É SLR(1)? {'SIM ✅' if self.is_slr1() else 'NÃO ❌'}")
    
    def save_to_csv(self, filename: str):
        """Salva tabela em formato CSV."""
        terminals = sorted(self.grammar.terminals)
        nonterminals = sorted(self.grammar.nonterminals - {self.grammar.start_symbol})
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("Estado")
            for t in terminals:
                f.write(f",ACTION[{t}]")
            for nt in nonterminals:
                f.write(f",GOTO[{nt}]")
            f.write("\n")
            
            # Dados
            for state_idx in range(len(self.collection.states)):
                f.write(str(state_idx))
                
                for t in terminals:
                    action = self.get_action(state_idx, t)
                    f.write(f",{action if action else ''}")
                
                for nt in nonterminals:
                    goto = self.get_goto(state_idx, nt)
                    f.write(f",{goto if goto is not None else ''}")
                
                f.write("\n")
        
        print(f"[OK] Tabela SLR salva em: {filename}")


# =============================================================================
# TESTE DO MÓDULO
# =============================================================================

if __name__ == "__main__":
    import sys
    import os
    from slr_grammar import SLRGrammar, SLRFirstFollow
    from slr_items import CanonicalCollection
    
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
    print("TESTE: CONSTRUÇÃO DA TABELA SLR(1)")
    print("=" * 70)
    
    # Carregar gramática
    print(f"\n[1] Carregando gramática: {grammar_file}")
    grammar = SLRGrammar()
    
    try:
        grammar.load_from_file(grammar_file)
        print(f"    Produções: {len(grammar.productions)}")
    except FileNotFoundError:
        print(f"    ❌ ERRO: Arquivo não encontrado: {grammar_file}")
        print(f"    Diretório atual: {os.getcwd()}")
        sys.exit(1)
    
    # Calcular FIRST e FOLLOW
    print("\n[2] Calculando FIRST e FOLLOW...")
    ff = SLRFirstFollow(grammar)
    ff.compute()
    
    # Construir coleção canônica
    print("\n[3] Construindo coleção canônica...")
    collection = CanonicalCollection(grammar)
    collection.build()
    print(f"    Estados: {len(collection.states)}")
    
    # Construir tabela SLR
    print("\n[4] Construindo tabela SLR(1)...")
    table = SLRParsingTable(grammar, collection, ff)
    is_slr1 = table.build()
    
    table.print_statistics()
    table.print_conflicts()
    
    if is_slr1:
        print("\n✅ Gramática é SLR(1)!")
    else:
        print(f"\n❌ Gramática NÃO é SLR(1) - {len(table.conflicts)} conflito(s)")
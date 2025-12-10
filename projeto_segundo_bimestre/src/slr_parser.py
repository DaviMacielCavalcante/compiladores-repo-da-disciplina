"""
=============================================================================
ALGORITMO DE ANÁLISE SINTÁTICA SLR(1) - LINGUAGEM VYTHON
=============================================================================

Implementação do algoritmo de parsing SLR(1) usando pilha.

O algoritmo usa:
- Pilha de estados e símbolos
- Tabela ACTION para decidir shift/reduce/accept
- Tabela GOTO para transições após reduções
=============================================================================
"""

from typing import List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

from slr_grammar import SLRGrammar, Production
from slr_table import SLRParsingTable, Action, ActionType


@dataclass
class ParseStep:
    """Representa um passo do parsing para debug."""
    step_number: int
    stack: str
    input_remaining: str
    action: str
    
    def __repr__(self):
        return f"{self.step_number:4d} | {self.stack:<50} | {self.input_remaining:<30} | {self.action}"


class SLRParser:
    """
    Parser SLR(1) com pilha.
    
    Algoritmo:
    1. Empilhar estado inicial (0)
    2. Repetir:
       a) Seja s o estado no topo e a o símbolo atual
       b) Se ACTION[s, a] = shift t:
          - Empilhar a e t
          - Avançar entrada
       c) Se ACTION[s, a] = reduce A -> β:
          - Desempilhar 2*|β| símbolos
          - Seja s' o estado agora no topo
          - Empilhar A e GOTO[s', A]
       d) Se ACTION[s, a] = accept:
          - Aceitar
       e) Senão:
          - Erro
    """
    
    def __init__(self, grammar: SLRGrammar, table: SLRParsingTable):
        self.grammar = grammar
        self.table = table
        
        # Estado do parser
        self.stack: List[Any] = []  # Alternado: estado, símbolo, estado, ...
        self.tokens: List[Tuple[str, str]] = []
        self.position: int = 0
        
        # Debug
        self.steps: List[ParseStep] = []
        self.accepted: bool = False
        self.error_message: str = None
        
    def parse(self, tokens: List[Tuple[str, str]], debug: bool = False) -> bool:
        """
        Analisa lista de tokens usando SLR(1).
        
        Args:
            tokens: Lista de tuplas (tipo, valor)
            debug: Se True, registra passos para visualização
            
        Returns:
            True se aceito, False se rejeitado
        """
        # Inicializar
        self.tokens = self._normalize_tokens(tokens)
        self.position = 0
        self.stack = [0]  # Estado inicial
        self.steps = []
        self.accepted = False
        self.error_message = None
        
        step_number = 0
        
        while True:
            step_number += 1
            
            # Estado atual (topo da pilha)
            current_state = self.stack[-1]
            
            # Símbolo atual da entrada
            current_token = self._current_token()
            token_type = current_token[0]
            
            # Buscar ação
            action = self.table.get_action(current_state, token_type)
            
            # Registrar passo se debug
            if debug:
                self.steps.append(ParseStep(
                    step_number=step_number,
                    stack=self._format_stack(),
                    input_remaining=self._format_remaining_input(),
                    action=str(action) if action else "ERROR"
                ))
            
            if action is None:
                # Erro
                self.error_message = self._generate_error_message(current_state, token_type)
                return False
            
            if action.action_type == ActionType.SHIFT:
                # SHIFT: empilhar símbolo e novo estado
                self.stack.append(token_type)
                self.stack.append(action.value)
                self.position += 1
                
            elif action.action_type == ActionType.REDUCE:
                # REDUCE: desempilhar e aplicar GOTO
                production = self.grammar.get_production(action.value)
                
                if production is None:
                    self.error_message = f"Produção {action.value} não encontrada"
                    return False
                
                # Número de símbolos no corpo da produção
                body_length = len(production.body)
                if production.body == ('ε',) or production.body == (self.grammar.EPSILON,):
                    body_length = 0
                
                # Desempilhar 2 * |β| elementos (símbolos e estados)
                if body_length > 0:
                    self.stack = self.stack[:-2 * body_length]
                
                # Estado após desempilhar
                state_after_pop = self.stack[-1]
                
                # GOTO[s', A]
                goto_state = self.table.get_goto(state_after_pop, production.head)
                
                if goto_state is None:
                    self.error_message = f"GOTO[{state_after_pop}, {production.head}] não definido"
                    return False
                
                # Empilhar não-terminal e novo estado
                self.stack.append(production.head)
                self.stack.append(goto_state)
                
            elif action.action_type == ActionType.ACCEPT:
                # ACCEPT
                self.accepted = True
                return True
            
            else:
                # Ação desconhecida
                self.error_message = f"Ação desconhecida: {action}"
                return False
            
            # Proteção contra loop infinito
            if step_number > 10000:
                self.error_message = "Limite de passos excedido"
                return False
        
        return False
    
    def _normalize_tokens(self, tokens: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        """Normaliza tokens e garante marcador de fim."""
        normalized = []
        has_eof = False
        
        for token in tokens:
            if isinstance(token, tuple):
                token_type = token[0]
                token_value = token[1]
            elif hasattr(token, 'type'):
                token_type = token.type
                token_value = token.value
            else:
                token_type = str(token)
                token_value = str(token)
            
            # Remover aspas extras se já tiver
            if token_type.startswith("'") and token_type.endswith("'"):
                token_type = token_type[1:-1]
            
            # Marcar se tem EOF
            if token_type == 'EOF':
                has_eof = True
            
            # Converter para formato da gramática (com aspas simples)
            normalized.append((f"'{token_type}'", token_value))
        
        # Se não tinha EOF explícito, adicionar
        if not has_eof:
            normalized.append(("'EOF'", "EOF"))
        
        # Adicionar marcador de fim do parser
        normalized.append((self.grammar.END_MARKER, '$'))
        
        return normalized
    
    def _current_token(self) -> Tuple[str, str]:
        """Retorna token atual."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return (self.grammar.END_MARKER, '$')
    
    def _format_stack(self) -> str:
        """Formata pilha para exibição."""
        parts = []
        for i, item in enumerate(self.stack):
            if isinstance(item, int):
                parts.append(str(item))
            else:
                # Símbolo - mostrar de forma compacta
                if item.startswith('<'):
                    parts.append(item[1:-1][:10])
                elif item.startswith("'"):
                    parts.append(item[1:-1])
                else:
                    parts.append(str(item)[:10])
        
        result = ' '.join(parts)
        if len(result) > 50:
            result = result[:47] + "..."
        return result
    
    def _format_remaining_input(self) -> str:
        """Formata entrada restante."""
        remaining = []
        for i in range(self.position, min(self.position + 5, len(self.tokens))):
            token = self.tokens[i]
            if token[0].startswith("'"):
                remaining.append(token[0][1:-1])
            else:
                remaining.append(token[0])
        
        result = ' '.join(remaining)
        if self.position + 5 < len(self.tokens):
            result += " ..."
        return result
    
    def _generate_error_message(self, state: int, symbol: str) -> str:
        """Gera mensagem de erro detalhada."""
        # Encontrar símbolos esperados
        expected = []
        for (s, sym), action in self.table.action.items():
            if s == state and action:
                if sym.startswith("'"):
                    expected.append(sym[1:-1])
                else:
                    expected.append(sym)
        
        symbol_display = symbol[1:-1] if symbol.startswith("'") else symbol
        
        msg = f"Erro sintático no estado {state}\n"
        msg += f"  Token encontrado: '{symbol_display}'\n"
        
        if expected:
            expected_str = ", ".join(sorted(expected)[:10])
            if len(expected) > 10:
                expected_str += f" ... (+{len(expected)-10} outros)"
            msg += f"  Tokens esperados: {expected_str}"
        
        return msg
    
    def print_steps(self, max_steps: int = None):
        """Imprime passos do parsing."""
        print("\n" + "=" * 100)
        print("PASSOS DO PARSING SLR(1)")
        print("=" * 100)
        print(f"{'Passo':>5} | {'Pilha':<50} | {'Entrada':<30} | Ação")
        print("-" * 100)
        
        steps_to_show = self.steps
        if max_steps and len(self.steps) > max_steps:
            # Mostrar início e fim
            half = max_steps // 2
            steps_to_show = self.steps[:half] + [None] + self.steps[-half:]
        
        for step in steps_to_show:
            if step is None:
                print(f"{'...':>5} | {'...':<50} | {'...':<30} | ...")
            else:
                print(step)
        
        print("=" * 100)
        
        if self.accepted:
            print("✅ ENTRADA ACEITA")
        else:
            print("❌ ENTRADA REJEITADA")
            if self.error_message:
                print(f"\n{self.error_message}")
    
    def get_result(self) -> dict:
        """Retorna resultado do parsing."""
        return {
            'accepted': self.accepted,
            'steps': len(self.steps),
            'error': self.error_message
        }


# =============================================================================
# TESTE DO MÓDULO
# =============================================================================

if __name__ == "__main__":
    import sys
    import os
    from slr_grammar import SLRGrammar, SLRFirstFollow
    from slr_items import CanonicalCollection
    from slr_table import SLRParsingTable
    
    print("=" * 70)
    print("TESTE: PARSER SLR(1)")
    print("=" * 70)
    
    # Procurar gramática SLR
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
    
    if grammar_file:
        print(f"\n[1] Carregando gramática: {grammar_file}")
        grammar = SLRGrammar()
        grammar.load_from_file(grammar_file)
    else:
        # Gramática de teste simplificada se não encontrar arquivo
        print("\n[1] Usando gramática de teste (arquivo não encontrado)...")
        test_grammar_content = """
# Gramática simplificada para teste
<E> ::= <E> '+' <T>
<E> ::= <T>
<T> ::= <T> '*' <F>
<T> ::= <F>
<F> ::= '(' <E> ')'
<F> ::= 'id'
"""
        with open("/tmp/test_grammar.bnf", "w") as f:
            f.write(test_grammar_content)
        
        grammar = SLRGrammar()
        grammar.load_from_file("/tmp/test_grammar.bnf")
    
    grammar.print_grammar()
    
    print("\n[2] Calculando FIRST e FOLLOW...")
    ff = SLRFirstFollow(grammar)
    ff.compute()
    
    print("\n[3] Construindo coleção canônica...")
    collection = CanonicalCollection(grammar)
    collection.build()
    print(f"    Estados: {len(collection.states)}")
    
    print("\n[4] Construindo tabela SLR...")
    table = SLRParsingTable(grammar, collection, ff)
    is_slr = table.build()
    print(f"    É SLR(1)? {'SIM' if is_slr else 'NÃO'}")
    
    if is_slr:
        print("\n[5] Testando parser...")
        parser = SLRParser(grammar, table)
        
        if grammar_file:
            # Tokens de teste para gramática Vython: x = 10;
            # EOF será adicionado automaticamente pela normalização
            test_tokens = [
                ("IDENTIFIER", "x"),
                ("=", "="),
                ("NUMBER", "10"),
                (";", ";"),
            ]
            print(f"    Entrada: x = 10;")
        else:
            # Tokens de teste para gramática E/T/F: id + id * id
            test_tokens = [
                ("id", "x"),
                ("+", "+"),
                ("id", "y"),
                ("*", "*"),
                ("id", "z"),
            ]
            print(f"    Entrada: id + id * id")
        
        result = parser.parse(test_tokens, debug=True)
        parser.print_steps(max_steps=20)
    else:
        print("\n[5] Parser não pode ser testado - gramática não é SLR(1)")
        table.print_conflicts()
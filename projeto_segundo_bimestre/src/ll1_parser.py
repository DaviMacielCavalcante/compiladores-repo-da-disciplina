#!/usr/bin/env python3
"""
Parser LL(1) com Pilha - Implementação Pura
Requisito da lauda: Tabela de casamento (MATCH) com pilha
"""

from collections import deque


class LL1Parser:
    """Parser LL(1) usando tabela de parsing e pilha."""
    
    def __init__(self, grammar, parsing_table):
        """
        Inicializa parser.
        
        Args:
            grammar: Objeto Grammar com a gramática
            parsing_table: Objeto ParsingTable com tabela construída
        """
        self.grammar = grammar
        self.table = parsing_table.table
        self.stack = deque()
        self.tokens = []
        self.position = 0
        self.accepted = False
        self.derivations = []  # Guarda derivações
        
    def parse(self, tokens):
        """
        Analisa lista de tokens usando LL(1) com pilha.
        
        Args:
            tokens: Lista de tuplas (tipo, valor) ou objetos Token
            
        Returns:
            bool: True se aceito, False se rejeitado
        """
        # Inicializar
        self.tokens = self._normalize_tokens(tokens)
        self.position = 0
        self.stack = deque()
        self.derivations = []
        self.accepted = False
        
        # Configurar pilha: $ e símbolo inicial
        self.stack.append('$')
        self.stack.append(self.grammar.start_symbol)
        
        # Derivação inicial
        self.derivations.append(self.grammar.start_symbol)
        
        print(f"[PARSER] Iniciando análise")
        print(f"[PARSER] Tokens: {len(self.tokens)}")
        print(f"[PARSER] Pilha inicial: $ {self.grammar.start_symbol}")
        
        # Algoritmo LL(1)
        step = 0
        while len(self.stack) > 0:
            step += 1
            top = self.stack[-1]  # Topo da pilha
            current_token = self._current_token()
            
            # Debug (primeiros passos e cada 50)
            if step <= 5 or step % 50 == 0:
                print(f"[Passo {step}] Pilha: {self._format_stack()} | Token: {current_token[0]}:'{current_token[1]}'")
            
            # Caso 1: Topo é terminal
            if self._is_terminal(top):
                if self._match(top, current_token):
                    # MATCH: Remove da pilha e avança token
                    self.stack.pop()
                    self.position += 1
                    if step <= 5:
                        print(f"  → MATCH '{top}'")
                else:
                    # Erro: Terminal não casa
                    print(f"[ERRO] Esperado '{top}', encontrado '{current_token[0]}:{current_token[1]}'")
                    return False
            
            # Caso 2: Topo é não-terminal
            elif self._is_nonterminal(top):
                production = self._get_production(top, current_token[0])
                
                if production is None:
                    # Erro: Sem produção na tabela
                    print(f"[ERRO] Sem produção M[{top}, {current_token[0]}]")
                    return False
                
                # Aplicar produção
                self.stack.pop()  # Remove não-terminal
                
                # Adicionar produção na pilha (ordem reversa)
                for symbol in reversed(production):
                    if not self.grammar.is_epsilon(symbol):
                        self.stack.append(symbol)
                
                # Registrar derivação
                prod_str = ' '.join(production)
                if step <= 5:
                    print(f"  → EXPAND {top} → {prod_str}")
                self.derivations.append(f"{top} → {prod_str}")
            
            # Caso 3: Topo é $
            elif top == '$':
                if current_token[0] == '$':
                    # Sucesso!
                    print(f"[PARSER] ✅ ACEITO (em {step} passos)")
                    self.accepted = True
                    return True
                else:
                    # Erro: Tokens sobrando
                    print(f"[ERRO] Esperado fim ($), mas há tokens sobrando")
                    return False
            
            # Proteção contra loop infinito
            if step > 10000:
                print(f"[ERRO] Limite de passos excedido (possível loop)")
                return False
        
        # Não deveria chegar aqui
        print(f"[ERRO] Pilha vazia antes do fim")
        return False
    
    def _normalize_tokens(self, tokens):
        """
        Normaliza tokens para formato (tipo, valor).
        Adiciona $ no final.
        """
        normalized = []
        
        for token in tokens:
            if isinstance(token, tuple):
                # Já é tupla
                normalized.append(token)
            elif hasattr(token, 'type') and hasattr(token, 'value'):
                # Objeto Token
                normalized.append((token.type, token.value))
            else:
                # String?
                normalized.append((str(token), str(token)))
        
        # Adicionar $ no final
        normalized.append(('$', '$'))
        
        return normalized
    
    def _current_token(self):
        """Retorna token atual."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ('$', '$')
    
    def _is_terminal(self, symbol):
        """Verifica se símbolo é terminal."""
        return symbol in self.grammar.terminals or symbol.startswith("'")
    
    def _is_nonterminal(self, symbol):
        """Verifica se símbolo é não-terminal."""
        return symbol in self.grammar.nonterminals
    
    def _match(self, expected, token):
        """
        Implementa MATCH - casa terminal da pilha com token.
        
        Args:
            expected: Terminal esperado (da pilha)
            token: Tupla (tipo, valor)
            
        Returns:
            bool: True se casa, False caso contrário
        """
        # Normalizar expected (remover aspas)
        expected_clean = expected.strip("'")
        token_type = token[0]
        token_value = token[1]
        
        # Tentar casar por tipo ou valor
        if expected_clean == token_type:
            return True
        if expected_clean == token_value:
            return True
        
        # Tokens especiais (IDENTIFIER, NUMBER, STRING)
        if expected_clean in ['IDENTIFIER', 'NUMBER', 'STRING']:
            return expected_clean == token_type
        
        return False
    
    def _get_production(self, nonterminal, terminal):
        """
        Busca produção na tabela M[A, a].
        
        Args:
            nonterminal: Não-terminal
            terminal: Terminal (lookahead)
            
        Returns:
            list: Produção ou None
        """
        # Tentar formatos diferentes
        attempts = [
            (nonterminal, terminal),
            (nonterminal, f"'{terminal}'"),
            (nonterminal, terminal.strip("'")),
        ]
        
        for key in attempts:
            if key in self.table:
                return self.table[key]
        
        return None
    
    def _format_stack(self):
        """Formata pilha para exibição (últimos 5 elementos)."""
        if len(self.stack) <= 5:
            return ' '.join(reversed(list(self.stack)))
        else:
            top5 = list(self.stack)[-5:]
            return '... ' + ' '.join(reversed(top5))
    
    def get_derivations(self):
        """Retorna lista de derivações aplicadas."""
        return self.derivations
    
    def print_derivations(self, max_show=20):
        """Imprime derivações (primeiras e últimas)."""
        print("\n=== DERIVAÇÕES ===")
        
        if len(self.derivations) <= max_show:
            for i, deriv in enumerate(self.derivations, 1):
                print(f"  {i}. {deriv}")
        else:
            # Primeiras 10
            half = max_show // 2
            for i in range(half):
                print(f"  {i+1}. {self.derivations[i]}")
            
            print(f"  ... ({len(self.derivations) - max_show} derivações omitidas)")
            
            # Últimas 10
            for i in range(len(self.derivations) - half, len(self.derivations)):
                print(f"  {i+1}. {self.derivations[i]}")
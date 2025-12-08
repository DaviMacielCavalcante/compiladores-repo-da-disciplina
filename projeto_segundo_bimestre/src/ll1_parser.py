"""
Parser LL(1) para Vython
Implementa análise sintática top-down com pilha
"""

from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class ASTNode:
    """Nó da Árvore Sintática Abstrata (AST)"""
    
    def __init__(self, symbol: str, value: str = None, children: List['ASTNode'] = None):
        """
        Args:
            symbol: Símbolo gramatical (não-terminal ou terminal)
            value: Valor do token (para terminais)
            children: Lista de filhos (para não-terminais)
        """
        self.symbol = symbol
        self.value = value
        self.children = children or []
        
    def add_child(self, node: 'ASTNode'):
        """Adiciona um filho ao nó"""
        self.children.append(node)
        
    def is_terminal(self) -> bool:
        """Verifica se é um nó terminal"""
        return len(self.children) == 0 and self.value is not None
        
    def print_tree(self, indent: int = 0, prefix: str = ""):
        """Imprime a árvore de forma visual"""
        # Símbolo epsilon não é impresso
        if self.symbol == 'ε':
            return
            
        # Imprime o nó atual
        print(f"{' ' * indent}{prefix}{self.symbol}", end="")
        if self.value is not None:
            print(f" = '{self.value}'", end="")
        print()
        
        # Imprime filhos
        for i, child in enumerate(self.children):
            is_last = (i == len(self.children) - 1)
            child_prefix = "└── " if is_last else "├── "
            child.print_tree(indent + 4, child_prefix)
            
    def to_dict(self) -> dict:
        """Converte árvore para dicionário (para JSON)"""
        result = {
            'symbol': self.symbol,
            'value': self.value
        }
        
        if self.children:
            result['children'] = [child.to_dict() for child in self.children if child.symbol != 'ε']
            
        return result


class ParseError(Exception):
    """Erro de parsing"""
    
    def __init__(self, message: str, token: str = None, expected: List[str] = None, position: int = None):
        self.message = message
        self.token = token
        self.expected = expected
        self.position = position
        super().__init__(self.format_error())
        
    def format_error(self) -> str:
        """Formata mensagem de erro"""
        msg = f"Erro de sintaxe: {self.message}"
        
        if self.position is not None:
            msg += f" (posição {self.position})"
            
        if self.token:
            msg += f"\n  Token encontrado: '{self.token}'"
            
        if self.expected:
            msg += f"\n  Esperado um de: {', '.join(self.expected)}"
            
        return msg


class LL1Parser:
    """
    Parser LL(1) com pilha
    
    Implementa o algoritmo de parsing top-down preditivo
    usando a tabela de parsing LL(1).
    """
    
    def __init__(self, grammar, parsing_table):
        """
        Args:
            grammar: Objeto Grammar com a gramática
            parsing_table: Objeto ParsingTable com a tabela M[NT, T]
        """
        self.grammar = grammar
        self.parsing_table = parsing_table
        self.stack = []
        self.input_tokens = []
        self.current_position = 0
        
        # Para construir AST
        self.ast_stack = []
        
    def parse(self, tokens: List[Tuple[str, str]]) -> ASTNode:
        """
        Realiza parsing de uma lista de tokens
        
        Args:
            tokens: Lista de tuplas (tipo_token, valor)
                   Ex: [('IDENTIFIER', 'x'), ('=', '='), ('NUMBER', '5')]
                   
        Returns:
            Raiz da árvore sintática (AST)
            
        Raises:
            ParseError: Se houver erro de sintaxe
        """
        # Inicializar
        self.input_tokens = tokens + [('$', '$')]  # Adiciona fim de entrada
        self.current_position = 0
        
        # Pilha: [$, <program>]
        self.stack = ['$', self.grammar.start_symbol]
        
        # Pilha AST
        self.ast_stack = []
        
        # Processar
        while len(self.stack) > 0:
            # Topo da pilha e próximo token
            X = self.stack[-1]  # Topo da pilha
            a_type, a_value = self._current_token()
            
            # Token atual (tipo ou valor para terminais especiais)
            a = a_type
            
            # DEBUG (opcional)
            # print(f"Stack: {self.stack[-5:]}, Token: ({a_type}, {a_value})")
            
            # Caso 1: Topo é terminal
            if self._is_terminal(X):
                if self._match_terminal(X, a_type, a_value):
                    # Match! Desempilha e avança
                    self.stack.pop()
                    
                    # Cria nó terminal na AST
                    terminal_node = ASTNode(X, a_value)
                    self.ast_stack.append(terminal_node)
                    
                    self.current_position += 1
                else:
                    # Erro: terminal não corresponde
                    raise ParseError(
                        f"Terminal '{X}' não corresponde ao token",
                        token=f"{a_type}:'{a_value}'",
                        expected=[X],
                        position=self.current_position
                    )
                    
            # Caso 2: Topo é não-terminal
            else:
                # Buscar produção na tabela M[X, a]
                production = self._get_production(X, a)
                
                if production is None:
                    # Erro: sem produção na tabela
                    expected = self._get_expected_tokens(X)
                    raise ParseError(
                        f"Token inesperado para não-terminal '{X}'",
                        token=f"{a_type}:'{a_value}'",
                        expected=expected,
                        position=self.current_position
                    )
                    
                # Desempilha X
                self.stack.pop()
                
                # Cria nó para o não-terminal
                nt_node = ASTNode(X)
                
                # Empilha produção (ordem reversa!)
                # Se produção = [A, B, C], empilhar: C, B, A
                if not self.grammar.is_epsilon(production[0]):
                    for symbol in reversed(production):
                        self.stack.append(symbol)
                        
                # Registra nó para construir AST depois
                self.ast_stack.append((nt_node, len(production)))
                
        # Parsing completado com sucesso!
        # Construir AST final
        return self._build_ast()
        
    def _current_token(self) -> Tuple[str, str]:
        """Retorna token atual"""
        if self.current_position < len(self.input_tokens):
            return self.input_tokens[self.current_position]
        return ('$', '$')
        
    def _is_terminal(self, symbol: str) -> bool:
        """Verifica se símbolo é terminal"""
        # Remover aspas para comparação
        clean_symbol = symbol.strip("'")
        
        # $ é terminal especial (fim de entrada)
        if clean_symbol == '$' or symbol == '$':
            return True
            
        # Tokens especiais sem aspas na gramática
        if clean_symbol in ['IDENTIFIER', 'NUMBER', 'STRING', 'True', 'False', 'EOF']:
            return True
            
        # Não-terminais têm formato <nome>
        if symbol.startswith('<') and symbol.endswith('>'):
            return False
            
        # Qualquer outra coisa (operadores, keywords) é terminal
        return True
                
    def _match_terminal(self, expected: str, token_type: str, token_value: str) -> bool:
        """Verifica se terminal esperado corresponde ao token"""
        # $ casa com $
        if expected == '$' and token_type == '$':
            return True
            
        # Remover aspas do expected se tiver
        expected_clean = expected.strip("'")
        
        # CASO 1: Terminais especiais (IDENTIFIER, NUMBER, STRING, True, False)
        # Estes NÃO têm aspas na gramática, mas podem ter na tabela
        if expected_clean in ['IDENTIFIER', 'NUMBER', 'STRING', 'True', 'False', 'EOF']:
            return expected_clean == token_type
            
        # CASO 2: Palavras-chave e operadores
        # Na gramática: 'if', 'while', '+', '-', etc.
        # No token: tipo = 'if', valor = 'if'
        
        # Comparar com tipo do token
        if expected_clean == token_type:
            return True
            
        # Comparar com valor do token
        if expected_clean == token_value:
            return True
            
        return False
        
    def _get_production(self, nonterminal: str, terminal: str) -> Optional[List[str]]:
        """Busca produção na tabela M[NT, T]"""
        # A tabela usa terminais COM ASPAS SIMPLES: 'IDENTIFIER', 'if', '+', etc.
        # Mas os tokens vêm sem aspas
        
        # Tentar buscar diretamente (sem modificar)
        if (nonterminal, terminal) in self.parsing_table.table:
            return self.parsing_table.table[(nonterminal, terminal)]
            
        # Tentar COM aspas simples (formato da gramática BNF)
        quoted_terminal = f"'{terminal}'"
        if (nonterminal, quoted_terminal) in self.parsing_table.table:
            return self.parsing_table.table[(nonterminal, quoted_terminal)]
            
        # Tentar SEM aspas (caso contrário)
        clean_terminal = terminal.strip("'")
        if (nonterminal, clean_terminal) in self.parsing_table.table:
            return self.parsing_table.table[(nonterminal, clean_terminal)]
            
        # Não encontrado
        return None
        
    def _get_expected_tokens(self, nonterminal: str) -> List[str]:
        """Retorna lista de tokens esperados para um não-terminal"""
        expected = []
        for (nt, term), prod in self.parsing_table.table.items():
            if nt == nonterminal:
                expected.append(term)
        return expected
        
    def _build_ast(self) -> ASTNode:
        """
        Constrói AST a partir da pilha de nós
        
        SIMPLIFICADO: Retorna árvore de derivação
        Para um projeto mais completo, implementar construção bottom-up
        """
        if not self.ast_stack:
            return ASTNode('<empty>')
            
        # Por simplicidade, retornar estrutura linear
        # Em um projeto completo, construir árvore adequadamente
        root = ASTNode(self.grammar.start_symbol)
        
        # TODO: Implementar construção adequada da AST
        # Por ora, retorna raiz vazia
        
        return root
        
    def parse_with_derivation(self, tokens: List[Tuple[str, str]]) -> Tuple[ASTNode, List[str]]:
        """
        Parse com registro de derivações
        
        Returns:
            Tupla (AST, lista de derivações)
        """
        derivations = []
        
        # Modificar parse para registrar derivações
        self.input_tokens = tokens + [('$', '$')]
        self.current_position = 0
        self.stack = ['$', self.grammar.start_symbol]
        
        derivations.append(f"Inicial: {self.grammar.start_symbol}")
        
        step = 1
        while len(self.stack) > 0:
            X = self.stack[-1]
            a_type, a_value = self._current_token()
            a = a_type
            
            if self._is_terminal(X):
                if self._match_terminal(X, a_type, a_value):
                    self.stack.pop()
                    self.current_position += 1
                    derivations.append(f"Passo {step}: Match '{X}' com '{a_value}'")
                    step += 1
                else:
                    raise ParseError(
                        f"Terminal '{X}' não corresponde",
                        token=f"{a_type}:'{a_value}'"
                    )
            else:
                production = self._get_production(X, a)
                
                if production is None:
                    raise ParseError(
                        f"Sem produção para M[{X}, {a}]",
                        token=f"{a_type}:'{a_value}'"
                    )
                    
                self.stack.pop()
                
                prod_str = ' '.join(production)
                derivations.append(f"Passo {step}: {X} → {prod_str}")
                step += 1
                
                if not self.grammar.is_epsilon(production[0]):
                    for symbol in reversed(production):
                        self.stack.append(symbol)
                        
        root = ASTNode(self.grammar.start_symbol)
        return root, derivations


def format_derivations(derivations: List[str]) -> str:
    """Formata lista de derivações para impressão"""
    result = []
    result.append("=" * 60)
    result.append("DERIVAÇÕES DO PARSING LL(1)")
    result.append("=" * 60)
    
    for deriv in derivations:
        result.append(deriv)
        
    result.append("=" * 60)
    return '\n'.join(result)
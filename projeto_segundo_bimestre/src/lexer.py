"""
Lexer (Analisador Léxico) para Vython
Converte código-fonte em tokens
"""

import re
from typing import List, Tuple
from enum import Enum


class TokenType(Enum):
    """Tipos de tokens"""
    # Identificadores e literais
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    
    # Palavras-chave
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    FOR = 'for'
    IN = 'in'
    RANGE = 'range'
    DO = 'do'
    BREAK = 'break'
    CONTINUE = 'continue'
    DEF = 'def'
    TRUE = 'True'
    FALSE = 'False'
    NOT = 'not'
    AND = 'and'
    OR = 'or'
    
    # Operadores
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    MODULO = '%'
    POWER = '**'
    
    # Operadores de comparação
    EQ = '=='
    NE = '!='
    LT = '<'
    GT = '>'
    LE = '<='
    GE = '>='
    
    # Operadores lógicos bitwise
    BIT_AND = '&'
    BIT_OR = '|'
    
    # Atribuição
    ASSIGN = '='
    
    # Delimitadores
    LPAREN = '('
    RPAREN = ')'
    LBRACKET = '['
    RBRACKET = ']'
    LBRACE = '{'
    RBRACE = '}'
    
    # Pontuação
    COMMA = ','
    COLON = ':'
    SEMICOLON = ';'
    
    # Fim de arquivo
    EOF = 'EOF'


class Token:
    """Representa um token"""
    
    def __init__(self, token_type: str, value: str, line: int = 1, column: int = 1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
        
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"
        
    def to_tuple(self) -> Tuple[str, str]:
        """Converte para tupla (tipo, valor) para o parser"""
        return (self.type, self.value)


class Lexer:
    """
    Analisador Léxico (Scanner) para Vython
    """
    
    # Palavras-chave
    KEYWORDS = {
        'if', 'else', 'while', 'for', 'in', 'range', 'do',
        'break', 'continue', 'def', 'True', 'False',
        'not', 'and', 'or'
    }
    
    # Operadores de múltiplos caracteres (verificar primeiro!)
    MULTI_CHAR_OPS = {
        '**': '**',
        '==': '==',
        '!=': '!=',
        '<=': '<=',
        '>=': '>='
    }
    
    # Operadores de um caractere
    SINGLE_CHAR_OPS = {
        '+': '+',
        '-': '-',
        '*': '*',
        '/': '/',
        '%': '%',
        '<': '<',
        '>': '>',
        '=': '=',
        '&': '&',
        '|': '|',
        '(': '(',
        ')': ')',
        '[': '[',
        ']': ']',
        '{': '{',
        '}': '}',
        ',': ',',
        ':': ':',
        ';': ';'
    }
    
    def __init__(self, source_code: str):
        """
        Args:
            source_code: Código-fonte Vython
        """
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
    def tokenize(self) -> List[Token]:
        """
        Tokeniza o código-fonte
        
        Returns:
            Lista de tokens
        """
        self.tokens = []
        
        while self.position < len(self.source):
            # Pular espaços em branco
            if self._current_char().isspace():
                if self._current_char() == '\n':
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.position += 1
                continue
                
            # Comentários (# até fim da linha)
            if self._current_char() == '#':
                self._skip_comment()
                continue
                
            # Números
            if self._current_char().isdigit():
                self.tokens.append(self._read_number())
                continue
                
            # Strings
            if self._current_char() in ['"', "'"]:
                self.tokens.append(self._read_string())
                continue
                
            # Identificadores e palavras-chave
            if self._current_char().isalpha() or self._current_char() == '_':
                self.tokens.append(self._read_identifier())
                continue
                
            # Operadores de múltiplos caracteres
            if self._peek_ahead(2) in self.MULTI_CHAR_OPS:
                op = self._peek_ahead(2)
                token = Token(op, op, self.line, self.column)
                self.tokens.append(token)
                self.position += 2
                self.column += 2
                continue
                
            # Operadores de um caractere
            if self._current_char() in self.SINGLE_CHAR_OPS:
                op = self._current_char()
                token = Token(op, op, self.line, self.column)
                self.tokens.append(token)
                self.position += 1
                self.column += 1
                continue
                
            # Caractere não reconhecido
            raise ValueError(
                f"Caractere inválido '{self._current_char()}' "
                f"na linha {self.line}, coluna {self.column}"
            )
            
        # Adicionar EOF
        self.tokens.append(Token('EOF', 'EOF', self.line, self.column))
        
        return self.tokens
        
    def _current_char(self) -> str:
        """Retorna caractere atual"""
        if self.position < len(self.source):
            return self.source[self.position]
        return '\0'
        
    def _peek_ahead(self, n: int = 1) -> str:
        """Olha n caracteres à frente"""
        if self.position + n <= len(self.source):
            return self.source[self.position:self.position + n]
        return '\0'
        
    def _skip_comment(self):
        """Pula comentário até fim da linha"""
        while self._current_char() != '\n' and self._current_char() != '\0':
            self.position += 1
            self.column += 1
            
    def _read_number(self) -> Token:
        """Lê um número (inteiro ou float)"""
        start_col = self.column
        num_str = ''
        
        # Parte inteira
        while self._current_char().isdigit():
            num_str += self._current_char()
            self.position += 1
            self.column += 1
            
        # Parte decimal (opcional)
        if self._current_char() == '.' and self._peek_ahead(2)[1].isdigit():
            num_str += '.'
            self.position += 1
            self.column += 1
            
            while self._current_char().isdigit():
                num_str += self._current_char()
                self.position += 1
                self.column += 1
                
        return Token('NUMBER', num_str, self.line, start_col)
        
    def _read_string(self) -> Token:
        """Lê uma string entre aspas"""
        start_col = self.column
        quote_char = self._current_char()  # " ou '
        string_value = ''
        
        self.position += 1  # Pular aspas de abertura
        self.column += 1
        
        while self._current_char() != quote_char and self._current_char() != '\0':
            # Escape de caracteres
            if self._current_char() == '\\' and self._peek_ahead(2)[1] in [quote_char, '\\', 'n', 't']:
                self.position += 1
                self.column += 1
                escape_char = self._current_char()
                if escape_char == 'n':
                    string_value += '\n'
                elif escape_char == 't':
                    string_value += '\t'
                else:
                    string_value += escape_char
            else:
                string_value += self._current_char()
                
            self.position += 1
            self.column += 1
            
        if self._current_char() != quote_char:
            raise ValueError(
                f"String não fechada na linha {self.line}, coluna {start_col}"
            )
            
        self.position += 1  # Pular aspas de fechamento
        self.column += 1
        
        return Token('STRING', string_value, self.line, start_col)
        
    def _read_identifier(self) -> Token:
        """Lê um identificador ou palavra-chave"""
        start_col = self.column
        identifier = ''
        
        while (self._current_char().isalnum() or self._current_char() == '_'):
            identifier += self._current_char()
            self.position += 1
            self.column += 1
            
        # Verificar se é palavra-chave
        if identifier in self.KEYWORDS:
            return Token(identifier, identifier, self.line, start_col)
        else:
            return Token('IDENTIFIER', identifier, self.line, start_col)
            
    def get_token_tuples(self) -> List[Tuple[str, str]]:
        """Retorna tokens como lista de tuplas (tipo, valor)"""
        if not self.tokens:
            self.tokenize()
        return [token.to_tuple() for token in self.tokens]
        
    def print_tokens(self):
        """Imprime tokens formatados"""
        print("=" * 70)
        print("TOKENS GERADOS")
        print("=" * 70)
        print(f"{'Tipo':<20} {'Valor':<20} {'Linha:Coluna':<15}")
        print("-" * 70)
        
        for token in self.tokens:
            print(f"{token.type:<20} {repr(token.value):<20} {token.line}:{token.column}")
            
        print("=" * 70)
        print(f"Total: {len(self.tokens)} tokens")
        print("=" * 70)


# Função auxiliar para tokenizar rapidamente
def tokenize(source_code: str) -> List[Tuple[str, str]]:
    """
    Tokeniza código Vython
    
    Args:
        source_code: Código-fonte
        
    Returns:
        Lista de tuplas (tipo_token, valor)
    """
    lexer = Lexer(source_code)
    lexer.tokenize()
    return lexer.get_token_tuples()
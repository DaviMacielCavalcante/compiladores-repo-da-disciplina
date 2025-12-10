"""
=============================================================================
ANALISADOR LÉXICO (SCANNER) - LINGUAGEM VYTHON
=============================================================================

Implementação do analisador léxico usando Expressões Regulares para
identificação de lexemas conforme especificado na lauda do trabalho.

Equipe: Davi Maciel Cavalcante, Pablo Abdon
Disciplina: Compiladores
Data: Dezembro/2025

=============================================================================
CLASSES DE LEXEMAS (TOKEN TYPES)
=============================================================================

1. IDENTIFICADORES
   - Padrão: Letra ou underscore, seguido de letras, dígitos ou underscores
   - Regex: [a-zA-Z_][a-zA-Z0-9_]*
   - Exemplos: x, contador, minha_var, _privado, var123

2. LITERAIS NUMÉRICOS
   - Inteiros: Sequência de dígitos
   - Decimais: Dígitos, ponto, dígitos
   - Regex: [0-9]+(.[0-9]+)?
   - Exemplos: 42, 3.14, 100, 0.5

3. LITERAIS STRING
   - Delimitados por aspas simples ou duplas
   - Regex: "[^"]*"|'[^']*'
   - Exemplos: "hello", 'world', "teste 123"

4. PALAVRAS-CHAVE (KEYWORDS)
   - Palavras reservadas da linguagem
   - Lista: if, else, while, for, in, range, do, break, continue,
           def, return, True, False, not, and, or

5. OPERADORES ARITMÉTICOS
   - Símbolos: +, -, *, /, %, **
   
6. OPERADORES DE COMPARAÇÃO
   - Símbolos: ==, !=, <, >, <=, >=

7. OPERADORES LÓGICOS
   - Símbolos: and, or, not (também são keywords)

8. OPERADORES BITWISE
   - Símbolos: &, |

9. OPERADOR DE ATRIBUIÇÃO
   - Símbolo: =

10. DELIMITADORES
    - Parênteses: (, )
    - Colchetes: [, ]
    - Chaves: {, }

11. PONTUAÇÃO
    - Vírgula: ,
    - Dois-pontos: :
    - Ponto-e-vírgula: ;

12. FIM DE ARQUIVO
    - Token especial: EOF

=============================================================================
"""

import re
from typing import List, Tuple, Optional
from enum import Enum, auto
from dataclasses import dataclass


# =============================================================================
# EXPRESSÕES REGULARES - DEFINIÇÃO DOS PADRÕES
# =============================================================================

class RegexPatterns:
    """
    Expressões Regulares para identificação de lexemas.
    
    Cada padrão define uma classe de tokens da linguagem Vython.
    A ordem de verificação é importante para evitar conflitos.
    """
    
    # -------------------------------------------------------------------------
    # PADRÃO: IDENTIFICADORES
    # -------------------------------------------------------------------------
    # Definição: Começa com letra (a-z, A-Z) ou underscore (_)
    #            Seguido de zero ou mais letras, dígitos (0-9) ou underscores
    # Exemplos válidos: x, var1, _private, minhaVariavel, CONSTANTE
    # Exemplos inválidos: 1var, @teste, var-nome
    # -------------------------------------------------------------------------
    IDENTIFIER = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
    
    # -------------------------------------------------------------------------
    # PADRÃO: NÚMEROS (INTEIROS E DECIMAIS)
    # -------------------------------------------------------------------------
    # Definição: Um ou mais dígitos, opcionalmente seguidos de ponto e mais dígitos
    # Inteiros: 0, 42, 1000
    # Decimais: 3.14, 0.5, 100.0
    # -------------------------------------------------------------------------
    NUMBER = re.compile(r'[0-9]+(\.[0-9]+)?')
    
    # -------------------------------------------------------------------------
    # PADRÃO: STRINGS
    # -------------------------------------------------------------------------
    # Definição: Texto entre aspas duplas ou simples
    # Aspas duplas: "texto aqui"
    # Aspas simples: 'texto aqui'
    # Nota: Não permite aspas dentro da string (simplificação)
    # -------------------------------------------------------------------------
    STRING_DOUBLE = re.compile(r'"[^"]*"')
    STRING_SINGLE = re.compile(r"'[^']*'")
    
    # -------------------------------------------------------------------------
    # PADRÃO: COMENTÁRIOS
    # -------------------------------------------------------------------------
    # Definição: # seguido de qualquer caractere até o fim da linha
    # Exemplo: # Este é um comentário
    # -------------------------------------------------------------------------
    COMMENT = re.compile(r'#[^\n]*')
    
    # -------------------------------------------------------------------------
    # PADRÃO: ESPAÇOS EM BRANCO
    # -------------------------------------------------------------------------
    # Definição: Espaços, tabs, quebras de linha
    # -------------------------------------------------------------------------
    WHITESPACE = re.compile(r'[ \t]+')
    NEWLINE = re.compile(r'\n')
    
    # -------------------------------------------------------------------------
    # PADRÃO: OPERADORES MULTI-CARACTERE
    # -------------------------------------------------------------------------
    # Verificados ANTES dos operadores simples para evitar conflitos
    # ** deve ser verificado antes de *
    # == deve ser verificado antes de =
    # -------------------------------------------------------------------------
    POWER = re.compile(r'\*\*')       # Potência
    EQUAL = re.compile(r'==')         # Igualdade
    NOT_EQUAL = re.compile(r'!=')     # Diferença
    LESS_EQUAL = re.compile(r'<=')    # Menor ou igual
    GREATER_EQUAL = re.compile(r'>=') # Maior ou igual


# =============================================================================
# CLASSES DE TOKENS
# =============================================================================

class TokenType(Enum):
    """
    Enumeração das classes de lexemas (tipos de tokens).
    
    Cada valor representa uma categoria gramatical diferente
    que será utilizada pelo analisador sintático.
    """
    
    # --- Identificadores e Literais ---
    IDENTIFIER = 'IDENTIFIER'   # Nomes de variáveis, funções
    NUMBER = 'NUMBER'           # Literais numéricos (int/float)
    STRING = 'STRING'           # Literais de texto
    
    # --- Palavras-Chave (Keywords) ---
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
    RETURN = 'return'
    TRUE = 'True'
    FALSE = 'False'
    NOT = 'not'
    AND = 'and'
    OR = 'or'
    
    # --- Operadores Aritméticos ---
    PLUS = '+'          # Adição
    MINUS = '-'         # Subtração
    MULTIPLY = '*'      # Multiplicação
    DIVIDE = '/'        # Divisão
    MODULO = '%'        # Módulo (resto)
    POWER = '**'        # Potência
    
    # --- Operadores de Comparação ---
    EQ = '=='           # Igual
    NE = '!='           # Diferente
    LT = '<'            # Menor que
    GT = '>'            # Maior que
    LE = '<='           # Menor ou igual
    GE = '>='           # Maior ou igual
    
    # --- Operadores Bitwise ---
    BIT_AND = '&'       # AND bitwise
    BIT_OR = '|'        # OR bitwise
    
    # --- Operador de Atribuição ---
    ASSIGN = '='        # Atribuição
    
    # --- Delimitadores ---
    LPAREN = '('        # Parêntese esquerdo
    RPAREN = ')'        # Parêntese direito
    LBRACKET = '['      # Colchete esquerdo
    RBRACKET = ']'      # Colchete direito
    LBRACE = '{'        # Chave esquerda
    RBRACE = '}'        # Chave direita
    
    # --- Pontuação ---
    COMMA = ','         # Vírgula
    COLON = ':'         # Dois-pontos
    SEMICOLON = ';'     # Ponto-e-vírgula
    
    # --- Especiais ---
    EOF = 'EOF'         # Fim de arquivo
    UNKNOWN = 'UNKNOWN' # Token não reconhecido


# =============================================================================
# ESTRUTURA DO TOKEN
# =============================================================================

@dataclass
class Token:
    """
    Representa um token (lexema identificado).
    
    Attributes:
        type: Tipo/classe do token (TokenType)
        value: Valor literal do lexema
        line: Linha onde o token foi encontrado
        column: Coluna onde o token começa
        lexeme: O texto original do código-fonte
    """
    type: str
    value: str
    line: int
    column: int
    lexeme: str = ""
    
    def __post_init__(self):
        if not self.lexeme:
            self.lexeme = self.value
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', {self.line}:{self.column})"
    
    def to_tuple(self) -> Tuple[str, str]:
        """Converte para tupla (tipo, valor) para o parser."""
        return (self.type, self.value)


# =============================================================================
# ANALISADOR LÉXICO (LEXER/SCANNER)
# =============================================================================

class Lexer:
    """
    Analisador Léxico para a linguagem Vython.
    
    Utiliza Expressões Regulares para identificar lexemas e
    classificá-los em tokens que serão consumidos pelo parser.
    
    Processo de análise:
    1. Lê o código-fonte caractere por caractere
    2. Aplica expressões regulares para identificar padrões
    3. Classifica cada lexema em uma categoria (TokenType)
    4. Gera a cadeia de tokens para o analisador sintático
    """
    
    # -------------------------------------------------------------------------
    # TABELA DE PALAVRAS-CHAVE
    # -------------------------------------------------------------------------
    # Mapeamento de strings para tipos de token
    # Verificado após identificar um IDENTIFIER
    # -------------------------------------------------------------------------
    KEYWORDS = {
        'if': 'if',
        'else': 'else',
        'while': 'while',
        'for': 'for',
        'in': 'in',
        'range': 'range',
        'do': 'do',
        'break': 'break',
        'continue': 'continue',
        'def': 'def',
        'return': 'return',
        'True': 'True',
        'False': 'False',
        'not': 'not',
        'and': 'and',
        'or': 'or',
    }
    
    # -------------------------------------------------------------------------
    # TABELA DE OPERADORES E DELIMITADORES
    # -------------------------------------------------------------------------
    # Operadores de múltiplos caracteres (verificar primeiro!)
    MULTI_CHAR_OPERATORS = {
        '**': '**',   # Potência
        '==': '==',   # Igualdade
        '!=': '!=',   # Diferença
        '<=': '<=',   # Menor ou igual
        '>=': '>=',   # Maior ou igual
    }
    
    # Operadores e delimitadores de um caractere
    SINGLE_CHAR_TOKENS = {
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
        ';': ';',
    }
    
    def __init__(self, source_code: str):
        """
        Inicializa o lexer.
        
        Args:
            source_code: Código-fonte Vython a ser analisado
        """
        self.source = source_code
        self.position = 0       # Posição atual no código
        self.line = 1           # Linha atual (para mensagens de erro)
        self.column = 1         # Coluna atual
        self.tokens: List[Token] = []
        
    def tokenize(self) -> List[Token]:
        """
        Executa a análise léxica completa.
        
        Processo:
        1. Percorre o código-fonte
        2. Identifica cada lexema usando regex
        3. Classifica e armazena os tokens
        4. Adiciona token EOF ao final
        
        Returns:
            Lista de tokens identificados
        """
        self.tokens = []
        
        while self.position < len(self.source):
            # Posição atual para mensagens de erro
            start_line = self.line
            start_column = self.column
            
            # Tentar cada padrão em ordem de prioridade
            if self._match_whitespace():
                continue
            
            if self._match_newline():
                continue
                
            if self._match_comment():
                continue
            
            if self._match_string():
                continue
                
            if self._match_number():
                continue
            
            if self._match_identifier_or_keyword():
                continue
            
            if self._match_multi_char_operator():
                continue
                
            if self._match_single_char_token():
                continue
            
            # Caractere não reconhecido
            char = self.source[self.position]
            raise LexicalError(
                f"Caractere inválido '{char}'",
                start_line,
                start_column
            )
        
        # Adicionar token de fim de arquivo
        self.tokens.append(Token(
            type='EOF',
            value='EOF',
            line=self.line,
            column=self.column,
            lexeme='EOF'
        ))
        
        return self.tokens
    
    # -------------------------------------------------------------------------
    # MÉTODOS DE MATCHING COM REGEX
    # -------------------------------------------------------------------------
    
    def _match_whitespace(self) -> bool:
        """
        Tenta casar espaços em branco (exceto newline).
        Regex: [ \t]+
        """
        match = RegexPatterns.WHITESPACE.match(self.source, self.position)
        if match:
            length = len(match.group())
            self.position += length
            self.column += length
            return True
        return False
    
    def _match_newline(self) -> bool:
        """
        Tenta casar quebra de linha.
        Regex: \n
        """
        match = RegexPatterns.NEWLINE.match(self.source, self.position)
        if match:
            self.position += 1
            self.line += 1
            self.column = 1
            return True
        return False
    
    def _match_comment(self) -> bool:
        """
        Tenta casar comentário (# até fim da linha).
        Regex: #[^\n]*
        """
        match = RegexPatterns.COMMENT.match(self.source, self.position)
        if match:
            length = len(match.group())
            self.position += length
            self.column += length
            return True
        return False
    
    def _match_string(self) -> bool:
        """
        Tenta casar literal string.
        Regex (aspas duplas): "[^"]*"
        Regex (aspas simples): '[^']*'
        """
        start_line = self.line
        start_column = self.column
        
        # Tentar aspas duplas
        match = RegexPatterns.STRING_DOUBLE.match(self.source, self.position)
        if match:
            lexeme = match.group()
            value = lexeme[1:-1]  # Remove aspas
            self._add_token('STRING', value, start_line, start_column, lexeme)
            self.position += len(lexeme)
            self.column += len(lexeme)
            return True
        
        # Tentar aspas simples
        match = RegexPatterns.STRING_SINGLE.match(self.source, self.position)
        if match:
            lexeme = match.group()
            value = lexeme[1:-1]  # Remove aspas
            self._add_token('STRING', value, start_line, start_column, lexeme)
            self.position += len(lexeme)
            self.column += len(lexeme)
            return True
        
        return False
    
    def _match_number(self) -> bool:
        """
        Tenta casar literal numérico.
        Regex: [0-9]+(.[0-9]+)?
        
        Aceita:
        - Inteiros: 0, 42, 1000
        - Decimais: 3.14, 0.5
        """
        match = RegexPatterns.NUMBER.match(self.source, self.position)
        if match:
            start_line = self.line
            start_column = self.column
            lexeme = match.group()
            
            self._add_token('NUMBER', lexeme, start_line, start_column, lexeme)
            self.position += len(lexeme)
            self.column += len(lexeme)
            return True
        return False
    
    def _match_identifier_or_keyword(self) -> bool:
        """
        Tenta casar identificador ou palavra-chave.
        Regex: [a-zA-Z_][a-zA-Z0-9_]*
        
        Após casar, verifica se é palavra-chave na tabela KEYWORDS.
        """
        match = RegexPatterns.IDENTIFIER.match(self.source, self.position)
        if match:
            start_line = self.line
            start_column = self.column
            lexeme = match.group()
            
            # Verificar se é palavra-chave
            if lexeme in self.KEYWORDS:
                token_type = self.KEYWORDS[lexeme]
            else:
                token_type = 'IDENTIFIER'
            
            self._add_token(token_type, lexeme, start_line, start_column, lexeme)
            self.position += len(lexeme)
            self.column += len(lexeme)
            return True
        return False
    
    def _match_multi_char_operator(self) -> bool:
        """
        Tenta casar operador de múltiplos caracteres.
        Verificado ANTES de operadores simples.
        
        Operadores: **, ==, !=, <=, >=
        """
        start_line = self.line
        start_column = self.column
        
        # Verificar cada operador multi-char
        for op, token_type in self.MULTI_CHAR_OPERATORS.items():
            if self.source[self.position:].startswith(op):
                self._add_token(token_type, op, start_line, start_column, op)
                self.position += len(op)
                self.column += len(op)
                return True
        return False
    
    def _match_single_char_token(self) -> bool:
        """
        Tenta casar token de um único caractere.
        
        Inclui: operadores (+, -, *, /, etc.)
                delimitadores ((, ), {, }, etc.)
                pontuação (,, :, ;)
        """
        char = self.source[self.position]
        
        if char in self.SINGLE_CHAR_TOKENS:
            start_line = self.line
            start_column = self.column
            token_type = self.SINGLE_CHAR_TOKENS[char]
            
            self._add_token(token_type, char, start_line, start_column, char)
            self.position += 1
            self.column += 1
            return True
        return False
    
    def _add_token(self, token_type: str, value: str, line: int, 
                   column: int, lexeme: str):
        """Adiciona um token à lista."""
        self.tokens.append(Token(
            type=token_type,
            value=value,
            line=line,
            column=column,
            lexeme=lexeme
        ))
    
    # -------------------------------------------------------------------------
    # MÉTODOS AUXILIARES
    # -------------------------------------------------------------------------
    
    def get_token_tuples(self) -> List[Tuple[str, str]]:
        """
        Retorna tokens como lista de tuplas (tipo, valor).
        Formato esperado pelo analisador sintático.
        """
        if not self.tokens:
            self.tokenize()
        return [token.to_tuple() for token in self.tokens]
    
    def print_tokens(self):
        """Imprime a cadeia de tokens formatada."""
        if not self.tokens:
            self.tokenize()
            
        print("=" * 80)
        print("CADEIA DE TOKENS - ANÁLISE LÉXICA")
        print("=" * 80)
        print(f"{'#':<5} {'TIPO':<15} {'VALOR':<20} {'LEXEMA':<20} {'POS':<10}")
        print("-" * 80)
        
        for i, token in enumerate(self.tokens, 1):
            pos = f"{token.line}:{token.column}"
            print(f"{i:<5} {token.type:<15} {repr(token.value):<20} "
                  f"{repr(token.lexeme):<20} {pos:<10}")
        
        print("=" * 80)
        print(f"Total: {len(self.tokens)} tokens")
        print("=" * 80)
    
    def get_lexeme_classes(self) -> dict:
        """
        Retorna estatísticas das classes de lexemas encontradas.
        Útil para a apresentação.
        """
        if not self.tokens:
            self.tokenize()
        
        classes = {}
        for token in self.tokens:
            if token.type not in classes:
                classes[token.type] = []
            classes[token.type].append(token.lexeme)
        
        return classes
    
    def print_lexeme_summary(self):
        """Imprime resumo das classes de lexemas."""
        classes = self.get_lexeme_classes()
        
        print("\n" + "=" * 60)
        print("RESUMO DAS CLASSES DE LEXEMAS")
        print("=" * 60)
        
        for token_type, lexemes in sorted(classes.items()):
            unique = list(set(lexemes))[:5]  # Primeiros 5 únicos
            count = len(lexemes)
            examples = ", ".join(repr(l) for l in unique)
            if len(set(lexemes)) > 5:
                examples += ", ..."
            print(f"\n{token_type} ({count} ocorrências)")
            print(f"  Exemplos: {examples}")
        
        print("\n" + "=" * 60)


# =============================================================================
# EXCEÇÃO DE ERRO LÉXICO
# =============================================================================

class LexicalError(Exception):
    """Exceção para erros durante análise léxica."""
    
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Erro léxico na linha {line}, coluna {column}: {message}")


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def tokenize(source_code: str) -> List[Tuple[str, str]]:
    """
    Função de conveniência para tokenizar código.
    
    Args:
        source_code: Código-fonte Vython
        
    Returns:
        Lista de tuplas (tipo_token, valor)
    """
    lexer = Lexer(source_code)
    lexer.tokenize()
    return lexer.get_token_tuples()


def print_regex_patterns():
    """Imprime as expressões regulares utilizadas."""
    print("\n" + "=" * 70)
    print("EXPRESSÕES REGULARES - DEFINIÇÃO DE LEXEMAS")
    print("=" * 70)
    
    patterns = [
        ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z0-9_]*", 
         "Letra/underscore + letras/dígitos/underscores"),
        ("NÚMERO", r"[0-9]+(\.[0-9]+)?", 
         "Inteiro ou decimal"),
        ("STRING (aspas duplas)", r'"[^"]*"', 
         "Texto entre aspas duplas"),
        ("STRING (aspas simples)", r"'[^']*'", 
         "Texto entre aspas simples"),
        ("COMENTÁRIO", r"#[^\n]*", 
         "# até fim da linha"),
        ("ESPAÇO EM BRANCO", r"[ \t]+", 
         "Espaços e tabs"),
        ("QUEBRA DE LINHA", r"\\n", 
         "Newline"),
    ]
    
    for name, pattern, description in patterns:
        print(f"\n{name}")
        print(f"  Regex: {pattern}")
        print(f"  Descrição: {description}")
    
    print("\n" + "=" * 70)


# =============================================================================
# TESTE DO MÓDULO
# =============================================================================

if __name__ == "__main__":
    # Código de exemplo para teste
    test_code = """
# Programa de teste Vython
def soma(a, b): {
    resultado = a + b;
    return resultado;
}

x = 10;
y = 20;
total = soma(x, y);

if total > 25: {
    msg = "Grande";
}
else: {
    msg = "Pequeno";
}
"""
    
    print("=" * 70)
    print("TESTE DO ANALISADOR LÉXICO - VYTHON")
    print("=" * 70)
    print("\nCÓDIGO FONTE:")
    print("-" * 70)
    print(test_code)
    print("-" * 70)
    
    # Mostrar expressões regulares
    print_regex_patterns()
    
    # Executar análise léxica
    lexer = Lexer(test_code)
    
    try:
        lexer.tokenize()
        lexer.print_tokens()
        lexer.print_lexeme_summary()
    except LexicalError as e:
        print(f"\n❌ ERRO: {e}")
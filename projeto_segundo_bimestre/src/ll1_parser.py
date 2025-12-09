#!/usr/bin/env python3
"""
Parser LL(1) com Pilha - Processa EBNF nativamente
Requisito da lauda: Tabela de casamento (MATCH) com pilha
"""

from collections import deque


class LL1Parser:
    """Parser LL(1) que processa operadores EBNF durante parsing."""
    
    def __init__(self, grammar, parsing_table):
        """
        Inicializa parser.
        
        Args:
            grammar: Objeto Grammar com a gramática
            parsing_table: Objeto ParsingTable com tabela construída
        """
        self.grammar = grammar
        self.table = parsing_table.table
        self.first_follow = parsing_table.first_follow
        self.stack = deque()
        self.tokens = []
        self.position = 0
        self.accepted = False
        self.derivations = []
        
    def parse(self, tokens):
        """
        Analisa lista de tokens usando LL(1) com pilha processando EBNF.
        
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
        
        # Algoritmo LL(1) com processamento EBNF
        step = 0
        while len(self.stack) > 0:
            step += 1
            top = self.stack[-1]
            current_token = self._current_token()
            
            # Debug
            print(f"[Passo {step}] Pilha: {self._format_stack()} | Token: {current_token[0]}:'{current_token[1]}'")
            
            # Identificar tipo do topo
            if top == '$':
                # Final
                if current_token[0] == '$':
                    print(f"[PARSER] ✅ ACEITO (em {step} passos)")
                    self.accepted = True
                    return True
                else:
                    print(f"[ERRO] Esperado fim ($), mas há tokens sobrando")
                    return False
            
            elif self._is_terminal(top):
                # Terminal: MATCH
                if self._match(top, current_token):
                    self.stack.pop()
                    self.position += 1
                    if step <= 5:
                        print(f"  → MATCH '{top}'")
                else:
                    print(f"[ERRO] Esperado '{top}', encontrado '{current_token[0]}:{current_token[1]}'")
                    return False
            
            elif self._is_nonterminal(top):
                # Não-terminal: EXPAND
                production = self._get_production(top, current_token[0])
                
                if production is None:
                    print(f"[ERRO] Sem produção M[{top}, {current_token[0]}]")
                    return False
                
                self.stack.pop()
                
                # Empilhar produção agrupando operadores EBNF
                self._push_production_with_ebnf(production)
                
                prod_str = ' '.join(production)
                if step <= 10:
                    print(f"  → EXPAND {top} → {prod_str}")
                    print(f"     Nova pilha (5 primeiros): {self._format_stack()}")
                self.derivations.append(f"{top} → {prod_str}")
            
            elif top == '*':
                # Operador * : repete elementos marcados
                self.stack.pop()  # Remove *
                
                # Pegar elementos (quantidade definida pelo marcador)
                # Pilha está: ... LOOP:N elem1 elem2 ... elemN
                elements = []
                count = 1  # Padrão se não houver marcador
                
                # Coletar elementos
                while len(self.stack) > 0 and not str(self.stack[-1]).startswith("LOOP:"):
                    elements.append(self.stack.pop())
                
                # Pegar marcador se existe
                if len(self.stack) > 0 and str(self.stack[-1]).startswith("LOOP:"):
                    marker = self.stack.pop()
                    count = int(marker.split(':')[1])
                
                # Reverter lista (estavam em ordem reversa)
                elements = list(reversed(elements))
                
                # Verificar se primeiro elemento casa com lookahead
                if elements and self._element_matches_lookahead(elements[0], current_token):
                    # Pode repetir: re-empilhar marcador, elementos e *
                    self.stack.append(f"LOOP:{count}")
                    for elem in reversed(elements):
                        self.stack.append(elem)
                    self.stack.append('*')
                    
                    # Empilhar elementos mais uma vez para processar
                    for elem in reversed(elements):
                        self.stack.append(elem)
                    
                    if step <= 5:
                        print(f"  → EBNF * (repetindo {count} elemento(s))")
                else:
                    # Não pode mais repetir: não re-empilha nada
                    if step <= 5:
                        print(f"  → EBNF * (terminado)")
            
            elif top == '?':
                # Operador ? : elemento opcional
                self.stack.pop()  # Remove ?
                
                # Coletar elementos até marcador OPT:N
                elements = []
                count = 1
                
                while len(self.stack) > 0 and not str(self.stack[-1]).startswith("OPT:"):
                    elements.append(self.stack.pop())
                
                # Pegar marcador
                if len(self.stack) > 0 and str(self.stack[-1]).startswith("OPT:"):
                    marker = self.stack.pop()
                    count = int(marker.split(':')[1])
                
                # Reverter lista
                elements = list(reversed(elements))
                
                # Testar se primeiro elemento casa com lookahead
                if elements and self._element_matches_lookahead(elements[0], current_token):
                    # Processar: re-empilhar elementos
                    for elem in reversed(elements):
                        self.stack.append(elem)
                    if step <= 5:
                        print(f"  → EBNF ? (processando {count} elemento(s))")
                else:
                    # Pular: não re-empilha nada
                    if step <= 5:
                        print(f"  → EBNF ? (pulando {count} elemento(s))")
            
            elif top.startswith('(') and top.endswith(')'):
                # Grupo (...)
                # Verificar se próximo elemento é operador EBNF
                if len(self.stack) >= 2 and self.stack[-2] in ['*', '+', '?']:
                    # Deixar o operador processar o grupo
                    # Trocar posição: grupo e operador
                    self.stack.pop()  # Remove grupo
                    operator = self.stack.pop()  # Remove operador
                    self.stack.append(top)  # Coloca grupo de volta
                    self.stack.append(operator)  # Coloca operador no topo
                    
                    if step <= 5:
                        print(f"  → REORDENAR: {operator} processará {top}")
                    continue  # Próxima iteração processará o operador
                
                # Processar grupo normalmente
                self.stack.pop()
                
                # Verificar se tem alternativas (|) no nível raiz ou é sequencial
                if self._has_top_level_alternatives(top):
                    # Grupo com alternativas: (A | B | C)
                    alternatives = self._extract_alternatives(top)
                    
                    # Escolher alternativa baseada no lookahead
                    chosen = None
                    for alt in alternatives:
                        if self._pattern_matches_lookahead(alt, current_token):
                            chosen = alt
                            break
                    
                    if chosen is None:
                        print(f"[ERRO] Nenhuma alternativa do grupo casa com {current_token[0]}")
                        return False
                    
                    # Empilhar alternativa escolhida (reverso)
                    symbols = self._tokenize_pattern(chosen)
                    for symbol in reversed(symbols):
                        if not self.grammar.is_epsilon(symbol):
                            self.stack.append(symbol)
                    
                    if step <= 5:
                        print(f"  → EBNF GROUP ALT (escolheu: {chosen})")
                else:
                    # Grupo sequencial: (A B C)
                    # Remove parênteses e empilha tudo
                    content = top[1:-1].strip()
                    symbols = self._tokenize_pattern(content)
                    
                    for symbol in reversed(symbols):
                        if not self.grammar.is_epsilon(symbol):
                            self.stack.append(symbol)
                    
                    if step <= 5:
                        print(f"  → EBNF GROUP SEQ (empilhado: {content})")
            
            else:
                print(f"[ERRO] Símbolo desconhecido na pilha: {top}")
                return False
            
            # Proteção contra loop infinito
            if step > 1000:
                print(f"[ERRO] Limite de passos excedido")
                return False
        
        print(f"[ERRO] Pilha vazia antes do fim")
        return False
    
    def _parse_element(self, element):
        """
        Processa um elemento (pode ser terminal, não-terminal ou grupo).
        Retorna True se sucesso, False se erro.
        """
        current_token = self._current_token()
        
        if self._is_terminal(element):
            if self._match(element, current_token):
                self.position += 1
                return True
            else:
                return False
        
        elif self._is_nonterminal(element):
            # Empilhar não-terminal e deixar próxima iteração processar
            self.stack.append(element)
            return True
        
        elif element.startswith('(') and element.endswith(')'):
            # Grupo: empilhar e deixar próxima iteração processar
            self.stack.append(element)
            return True
        
        else:
            # Símbolo desconhecido
            return False
    
    def _element_matches_lookahead(self, element, token):
        """
        Verifica se elemento pode ser parseado com token atual.
        Usa FIRST sets.
        """
        first_set = self._get_first_of_element(element)
        
        token_type = token[0]
        token_value = token[1]
        
        # Verificar se token está no FIRST
        for f in first_set:
            clean_f = str(f).strip("'\"")
            if clean_f == token_type or clean_f == token_value:
                return True
            if token_type in ['IDENTIFIER', 'NUMBER', 'STRING'] and clean_f == token_type:
                return True
        
        return False
    
    def _pattern_matches_lookahead(self, pattern, token):
        """Verifica se padrão (sequência de símbolos) casa com lookahead."""
        symbols = self._tokenize_pattern(pattern)
        
        if not symbols:
            return False
        
        # Pegar FIRST do primeiro símbolo do padrão
        first_symbol = symbols[0]
        return self._element_matches_lookahead(first_symbol, token)
    
    def _get_first_of_element(self, element):
        """Obtém FIRST set de um elemento."""
        # Limpar elemento
        clean = element.strip("'\"")
        
        # Buscar no FIRST calculado
        if element in self.first_follow.first:
            return self.first_follow.first[element]
        elif clean in self.first_follow.first:
            return self.first_follow.first[clean]
        elif self._is_terminal(element):
            return {clean}
        else:
            return set()
    
    def _has_top_level_alternatives(self, group):
        """
        Verifica se grupo tem | no nível raiz (alternativas).
        Retorna True se tem alternativas, False se é sequencial.
        """
        content = group[1:-1]  # Remove parênteses externos
        depth = 0
        
        for char in content:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            elif char == '|' and depth == 0:
                # Encontrou | no nível raiz
                return True
        
        # Não tem | no nível raiz, é sequencial
        return False
    
    def _extract_alternatives(self, group):
        """Extrai alternativas de grupo (A | B | C)"""
        # Remove parênteses
        content = group[1:-1].strip()
        
        # Dividir por | respeitando aninhamento
        alternatives = []
        current = ""
        depth = 0
        
        for char in content:
            if char == '(':
                depth += 1
                current += char
            elif char == ')':
                depth -= 1
                current += char
            elif char == '|' and depth == 0:
                if current.strip():
                    alternatives.append(current.strip())
                current = ""
            else:
                current += char
        
        if current.strip():
            alternatives.append(current.strip())
        
        return alternatives
    
    def _tokenize_pattern(self, pattern):
        """Tokeniza padrão em símbolos individuais."""
        symbols = []
        i = 0
        
        while i < len(pattern):
            # Pular espaços
            if pattern[i].isspace():
                i += 1
                continue
            
            # Não-terminal <...>
            if pattern[i] == '<':
                end = pattern.find('>', i)
                if end != -1:
                    symbols.append(pattern[i:end+1])
                    i = end + 1
                    continue
            
            # Terminal '...'
            if pattern[i] == "'":
                end = pattern.find("'", i + 1)
                if end != -1:
                    symbols.append(pattern[i:end+1])
                    i = end + 1
                    continue
            
            # Grupo (...)
            if pattern[i] == '(':
                depth = 1
                j = i + 1
                while j < len(pattern) and depth > 0:
                    if pattern[j] == '(':
                        depth += 1
                    elif pattern[j] == ')':
                        depth -= 1
                    j += 1
                symbols.append(pattern[i:j])
                i = j
                continue
            
            # Operadores EBNF
            if pattern[i] in '*+?':
                symbols.append(pattern[i])
                i += 1
                continue
            
            # Palavra
            if pattern[i].isalnum() or pattern[i] == '_':
                j = i
                while j < len(pattern) and (pattern[j].isalnum() or pattern[j] == '_'):
                    j += 1
                symbols.append(pattern[i:j])
                i = j
            else:
                # Símbolo único
                symbols.append(pattern[i])
                i += 1
        
        return symbols
    
    def _push_production_with_ebnf(self, production):
        """
        Empilha produção expandindo operadores EBNF baseado em lookahead.
        
        Para ?, decide agora se empilha ou não.
        Para *, empilha elemento uma vez e re-coloca * e elemento para loop.
        """
        i = len(production) - 1
        
        while i >= 0:
            symbol = production[i]
            
            # Verificar se é operador EBNF
            if symbol in ['*', '?']:
                if i == 0:
                    return
                
                # Identificar o "elemento" que o operador afeta
                # Pode ser um grupo (...) ou símbolo simples
                if production[i-1].startswith('(') and production[i-1].endswith(')'):
                    # É um grupo STRING: precisa tokenizar o conteúdo
                    group_str = production[i-1]
                    # Tokenizar o grupo usando _tokenize_pattern
                    group_tokens = self._tokenize_pattern(group_str)
                    
                    # Processar baseado no operador
                    if symbol == '?':
                        # Opcional: empilhar grupo E marcador E ?
                        group_content = [t for t in group_tokens if t not in ['(', ')']]
                        count = len(group_content)
                        
                        self.stack.append(f"OPT:{count}")  # Marcador
                        for k in range(len(group_content) - 1, -1, -1):
                            self.stack.append(group_content[k])
                        self.stack.append('?')
                    
                    elif symbol == '*':
                        # Zero ou mais: empilha grupo com marcador de quantidade
                        group_content = [t for t in group_tokens if t not in ['(', ')']]
                        count = len(group_content)
                        
                        # Empilhar: COUNT | elementos | *
                        self.stack.append(f"LOOP:{count}")  # Marcador
                        for k in range(len(group_content) - 1, -1, -1):
                            self.stack.append(group_content[k])
                        self.stack.append('*')
                    
                    i -= 2  # Pula elemento (grupo) e operador
                
                else:
                    # Elemento simples
                    element = production[i-1]
                    
                    if symbol == '?':
                        # Opcional: empilhar elemento E marcador E ?
                        self.stack.append("OPT:1")
                        self.stack.append(element)
                        self.stack.append('?')
                    
                    elif symbol == '*':
                        # Zero ou mais: empilha com marcador
                        self.stack.append("LOOP:1")  # 1 elemento
                        self.stack.append(element)
                        self.stack.append('*')
                    
                    i -= 2
            
            else:
                # Símbolo normal
                if not self.grammar.is_epsilon(symbol):
                    self.stack.append(symbol)
                i -= 1
    
    def _push_group_content(self, group_tokens):
        """Empilha conteúdo de um grupo (sem parênteses externos)."""
        for i in range(len(group_tokens) - 1, -1, -1):
            if group_tokens[i] not in ['(', ')']:
                self.stack.append(group_tokens[i])
    
    def _should_parse_optional(self, group_tokens):
        """Decide se deve processar elemento/grupo opcional baseado em FIRST."""
        # Montar string do grupo
        content = ' '.join([t for t in group_tokens if t not in ['(', ')']])
        current = self._current_token()
        return self._pattern_matches_lookahead(content, current)
    
    def _should_parse_element(self, element):
        """Decide se deve processar elemento opcional baseado em FIRST."""
        current = self._current_token()
        return self._element_matches_lookahead(element, current)
    
    def _normalize_tokens(self, tokens):
        """Normaliza tokens para formato (tipo, valor). Adiciona $."""
        normalized = []
        
        for token in tokens:
            if isinstance(token, tuple):
                normalized.append(token)
            elif hasattr(token, 'type') and hasattr(token, 'value'):
                normalized.append((token.type, token.value))
            else:
                normalized.append((str(token), str(token)))
        
        normalized.append(('$', '$'))
        return normalized
    
    def _current_token(self):
        """Retorna token atual."""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return ('$', '$')
    
    def _is_terminal(self, symbol):
        """Verifica se símbolo é terminal."""
        if symbol in ['*', '+', '?', '$']:
            return False
        if symbol.startswith("'") or symbol.startswith('"'):
            return True
        if symbol.startswith('<') and symbol.endswith('>'):
            return False
        if symbol.startswith('(') and symbol.endswith(')'):
            return False
        return symbol in self.grammar.terminals
    
    def _is_nonterminal(self, symbol):
        """Verifica se símbolo é não-terminal."""
        return symbol in self.grammar.nonterminals
    
    def _match(self, expected, token):
        """Implementa MATCH - casa terminal da pilha com token."""
        expected_clean = expected.strip("'\"")
        token_type = token[0]
        token_value = token[1]
        
        if expected_clean == token_type:
            return True
        if expected_clean == token_value:
            return True
        if expected_clean in ['IDENTIFIER', 'NUMBER', 'STRING']:
            return expected_clean == token_type
        
        return False
    
    def _get_production(self, nonterminal, terminal):
        """Busca produção na tabela M[A, a]."""
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
            half = max_show // 2
            for i in range(half):
                print(f"  {i+1}. {self.derivations[i]}")
            
            print(f"  ... ({len(self.derivations) - max_show} derivações omitidas)")
            
            for i in range(len(self.derivations) - half, len(self.derivations)):
                print(f"  {i+1}. {self.derivations[i]}")
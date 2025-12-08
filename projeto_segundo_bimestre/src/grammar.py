"""
Classe Grammar com suporte a EBNF
Converte automaticamente EBNF → BNF puro
"""

import re
from collections import defaultdict


class Grammar:
    """
    Gramática que suporta notação EBNF e converte para BNF puro
    
    EBNF suportado:
    - A*  (zero ou mais)
    - A+  (um ou mais)
    - A?  (zero ou um / opcional)
    - (A | B | C)  (grupos)
    """
    
    def __init__(self):
        self.nonterminals = set()
        self.terminals = set()
        self.productions = defaultdict(list)
        self.start_symbol = None
        self.epsilon = 'ε'  # Símbolo epsilon
        self._aux_counter = 0  # Contador para não-terminais auxiliares
        
    def load_from_file(self, filepath):
        """Carrega gramática de arquivo e converte EBNF → BNF"""
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Primeiro passo: juntar linhas de continuação (que começam com |)
        merged_lines = []
        current_rule = None
        
        for line in lines:
            stripped = line.strip()
            
            # Ignorar linhas vazias e comentários
            if not stripped or stripped.startswith("#"):
                continue
            
            # Linha começa com | → continuação da regra anterior
            if stripped.startswith("|"):
                if current_rule is not None:
                    # Adicionar alternativa à regra atual
                    current_rule += " " + stripped
                continue
            
            # Linha tem ::= → nova regra
            if "::=" in stripped:
                # Salvar regra anterior se existir
                if current_rule is not None:
                    merged_lines.append(current_rule)
                # Iniciar nova regra
                current_rule = stripped
                continue
            
            # Outra linha (provavelmente continuação sem |)
            if current_rule is not None:
                current_rule += " " + stripped
        
        # Não esquecer a última regra
        if current_rule is not None:
            merged_lines.append(current_rule)
        
        # Segundo passo: processar cada regra completa (convertendo EBNF → BNF)
        for rule in merged_lines:
            self._parse_rule(rule)
        
        # Terceiro passo: registrar terminais de TODAS as produções
        # (incluindo as geradas automaticamente)
        self._register_all_terminals()
    
    def _parse_rule(self, line):
        """Parse uma regra, convertendo EBNF → BNF se necessário"""
        left, right = line.split("::=", 1)
        left = left.strip()
        
        if self.start_symbol is None:
            self.start_symbol = left
        
        self.nonterminals.add(left)
        
        # Processar alternativas (|)
        alternatives = self._split_alternatives(right)
        
        for alt in alternatives:
            # Converter EBNF → BNF para esta alternativa
            symbols = self._process_ebnf(alt.strip(), left)
            
            if symbols:  # Ignorar produções vazias temporárias
                self.productions[left].append(symbols)
                
                # Registrar terminais e não-terminais
                for sym in symbols:
                    if self._is_nonterminal(sym):
                        self.nonterminals.add(sym)
                    elif sym != 'ε':
                        self.terminals.add(sym)
    
    def _split_alternatives(self, text):
        """
        Divide alternativas por | respeitando parênteses
        
        Exemplo: "A | B | (C | D)" → ["A", "B", "(C | D)"]
        """
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
                # Alternativa encontrada
                alternatives.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
            
            i += 1
        
        # Adicionar última alternativa
        if current:
            alternatives.append(''.join(current).strip())
        
        return alternatives
    
    def _process_ebnf(self, text, parent_nt):
        """
        Processa uma alternativa convertendo EBNF → BNF
        
        Returns:
            Lista de símbolos (BNF puro)
        """
        # Tokenizar
        tokens = self._tokenize_ebnf(text)
        result = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Verificar se próximo token é operador EBNF
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                
                # Grupo com operador: (...)*  (...)+  (...)?
                if token.startswith('(') and token.endswith(')') and next_token in ['*', '+', '?']:
                    # Processar grupo com operador
                    if next_token == '*':
                        aux_nt = self._create_group_star_rule(token, parent_nt)
                        result.append(aux_nt)
                    elif next_token == '+':
                        aux_nt = self._create_group_plus_rule(token, parent_nt)
                        # Para A+: adicionar grupo uma vez + lista
                        # Mas aqui o grupo já retorna o NT, então só adicionar
                        result.append(aux_nt)
                    elif next_token == '?':
                        aux_nt = self._create_group_optional_rule(token, parent_nt)
                        result.append(aux_nt)
                    i += 2
                    continue
                
                # Elemento simples com operador: A*  A+  A?
                if next_token == '*':
                    aux_nt = self._create_star_rule(token, parent_nt)
                    result.append(aux_nt)
                    i += 2
                    continue
                
                elif next_token == '+':
                    aux_nt = self._create_plus_rule(token, parent_nt)
                    result.append(token)  # Primeiro elemento
                    result.append(aux_nt)  # Lista auxiliar
                    i += 2
                    continue
                
                elif next_token == '?':
                    aux_nt = self._create_optional_rule(token, parent_nt)
                    result.append(aux_nt)
                    i += 2
                    continue
            
            # Grupo sem operador (A | B | C)
            if token.startswith('(') and token.endswith(')'):
                aux_nt = self._create_group_rule(token, parent_nt)
                result.append(aux_nt)
                i += 1
                continue
            
            # Token normal
            result.append(token)
            i += 1
        
        return result
    
    def _tokenize_ebnf(self, text):
        """
        Tokeniza texto EBNF, respeitando:
        - Não-terminais <...>
        - Terminais '...'
        - Grupos (...)
        - Operadores *, +, ?
        
        IMPORTANTE: IDENTIFIER, NUMBER, STRING são convertidos para 'IDENTIFIER', etc.
        para manter consistência com outros terminais
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
            
            # Operadores EBNF
            if text[i] in '*+?':
                tokens.append(text[i])
                i += 1
                continue
            
            # Operadores multi-char (**, ==, !=, etc.)
            if i + 1 < len(text):
                two_char = text[i:i+2]
                if two_char in ['**', '==', '!=', '<=', '>=']:
                    tokens.append(two_char)
                    i += 2
                    continue
            
            # Palavra ou símbolo único
            if text[i].isalnum() or text[i] == '_':
                j = i
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                word = text[i:j]
                
                # NORMALIZAR: Tokens especiais devem ter aspas para consistência
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
    
    def _create_star_rule(self, element, parent):
        """
        Converte A* → regra auxiliar
        
        A* vira:
        <parent_A_list> ::= A <parent_A_list>
        <parent_A_list> ::= ε
        """
        # Nome do auxiliar
        element_name = self._get_element_name(element)
        aux_nt = f"<{element_name}_list>"
        
        # Evitar duplicatas
        if aux_nt not in self.productions:
            self.nonterminals.add(aux_nt)
            # Regra recursiva
            self.productions[aux_nt].append([element, aux_nt])
            # Regra epsilon
            self.productions[aux_nt].append([self.epsilon])
        
        return aux_nt
    
    def _create_plus_rule(self, element, parent):
        """
        Converte A+ → A A*
        
        Retorna o A* (o primeiro A é adicionado separadamente)
        """
        return self._create_star_rule(element, parent)
    
    def _create_optional_rule(self, element, parent):
        """
        Converte A? → regra auxiliar
        
        A? vira:
        <parent_A_opt> ::= A
        <parent_A_opt> ::= ε
        """
        element_name = self._get_element_name(element)
        aux_nt = f"<optional_{element_name}>"
        
        if aux_nt not in self.productions:
            self.nonterminals.add(aux_nt)
            # Regra com elemento
            self.productions[aux_nt].append([element])
            # Regra epsilon
            self.productions[aux_nt].append([self.epsilon])
        
        return aux_nt
    
    def _create_group_rule(self, group_text, parent):
        """
        Converte (A | B | C) → regra auxiliar
        
        (A | B | C) vira:
        <parent_group_N> ::= A
        <parent_group_N> ::= B
        <parent_group_N> ::= C
        """
        # Remover parênteses
        inner = group_text[1:-1].strip()
        
        # Gerar nome único
        self._aux_counter += 1
        aux_nt = f"<group_{self._aux_counter}>"
        
        self.nonterminals.add(aux_nt)
        
        # Processar alternativas dentro do grupo
        alternatives = self._split_alternatives(inner)
        for alt in alternatives:
            symbols = self._process_ebnf(alt.strip(), aux_nt)
            if symbols:
                self.productions[aux_nt].append(symbols)
        
        return aux_nt
    
    def _create_group_star_rule(self, group_text, parent):
        """
        Converte (...)* → regra auxiliar com recursão
        
        (...)*  vira:
        <aux_list> ::= (conteúdo do grupo) <aux_list>
        <aux_list> ::= ε
        """
        # Primeiro criar regra para o grupo
        group_nt = self._create_group_rule(group_text, parent)
        
        # Depois criar regra * usando o grupo
        return self._create_star_rule(group_nt, parent)
    
    def _create_group_plus_rule(self, group_text, parent):
        """
        Converte (...)+ → regra auxiliar
        
        (...)+  vira  (grupo) (grupo)*
        """
        # Criar regra para o grupo
        group_nt = self._create_group_rule(group_text, parent)
        
        # Criar * para repetição
        list_nt = self._create_star_rule(group_nt, parent)
        
        # Retornar não-terminal que combina ambos
        # Na verdade, para A+, precisamos: A A*
        # Então retornar um NT que faz isso
        self._aux_counter += 1
        plus_nt = f"<group_plus_{self._aux_counter}>"
        
        self.nonterminals.add(plus_nt)
        self.productions[plus_nt].append([group_nt, list_nt])
        
        return plus_nt
    
    def _create_group_optional_rule(self, group_text, parent):
        """
        Converte (...)? → regra auxiliar opcional
        
        (...)?  vira:
        <aux_opt> ::= (conteúdo do grupo)
        <aux_opt> ::= ε
        """
        # Remover parênteses
        inner = group_text[1:-1].strip()
        
        # Gerar nome único
        self._aux_counter += 1
        aux_nt = f"<group_opt_{self._aux_counter}>"
        
        self.nonterminals.add(aux_nt)
        
        # Processar conteúdo como alternativas
        alternatives = self._split_alternatives(inner)
        for alt in alternatives:
            symbols = self._process_ebnf(alt.strip(), aux_nt)
            if symbols:
                self.productions[aux_nt].append(symbols)
        
        # Adicionar epsilon
        self.productions[aux_nt].append([self.epsilon])
        
        return aux_nt
    
    def _get_element_name(self, element):
        """Extrai nome de um elemento para usar em auxiliar"""
        # <statement> → statement
        if element.startswith('<') and element.endswith('>'):
            return element[1:-1]
        
        # 'if' → if
        if element.startswith("'") and element.endswith("'"):
            return element[1:-1]
        
        # Outros → usar diretamente
        return element.replace('<', '').replace('>', '').replace("'", "")
    
    def _register_all_terminals(self):
        """
        Registra todos os terminais de todas as produções
        (incluindo produções geradas automaticamente)
        """
        for nt, prods in self.productions.items():
            for prod in prods:
                for sym in prod:
                    if self._is_nonterminal(sym):
                        # Já deve estar em nonterminals
                        pass
                    elif sym != self.epsilon and sym != 'ε':
                        self.terminals.add(sym)
    
    def _is_nonterminal(self, symbol):
        """Verifica se símbolo é não-terminal"""
        return symbol.startswith("<") and symbol.endswith(">")
    
    def is_epsilon(self, symbol):
        """Verifica se símbolo é epsilon"""
        if isinstance(symbol, list):
            return len(symbol) == 1 and self.is_epsilon(symbol[0])
        return symbol in ['ε', 'epsilon', 'EPSILON', self.epsilon]
    
    def debug_print(self):
        """Imprime gramática para debug"""
        print("=" * 60)
        print("GRAMÁTICA (após conversão EBNF → BNF)")
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
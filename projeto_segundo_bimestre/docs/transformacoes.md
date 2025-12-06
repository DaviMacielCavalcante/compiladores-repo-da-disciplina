# Transformações da Gramática

## Equipe
- Davi Maciel Cavalcante, Pablo Abdon

## Linguagem
Vython

---

## 1. Problemas Identificados na Gramática Original

### 1.1 Recursão à Esquerda

**Localização:** Regra `<expression>` (linhas 81-95 do arquivo `gramatica_original.bnf`)

**Problema:**
```bnf
<expression> ::= <expression> <logical_op> <expression>
               | <expression> <add_sub> <expression>
               | ...
```

**Por que é problema:**
- Parsers LL(1) não conseguem processar recursão à esquerda
- Causa loop infinito no parsing
- Impede construção da tabela LL(1)

---

### 1.2 Ambiguidade em Precedência de Operadores

**Exemplo:** A expressão `2 + 3 * 4` pode ser interpretada como:
- `(2 + 3) * 4 = 20` (incorreto)
- `2 + (3 * 4) = 14` (correto)

**Problema:** A gramática original não define qual é a interpretação correta.

---

### 1.3 Ambiguidade em Associatividade

**Exemplo:** A expressão `5 - 3 - 2` pode ser interpretada como:
- `(5 - 3) - 2 = 0` (esquerda, correto)
- `5 - (3 - 2) = 4` (direita, incorreto)

**Problema:** A gramática permite ambas as interpretações.

---

### 1.4 Conflito LL(1) em Statements

**Problema:** Quando o parser vê IDENTIFIER no início de um statement, não consegue decidir se é:
- Assignment: `x = 5`
- Chamada de função: `print(x)`
- Expressão simples: `x + 5`
- Acesso a array: `arr[0]`

**Por que é problema:**
Parsers LL(1) precisam decidir qual produção usar olhando apenas o próximo token (lookahead = 1), mas aqui isso não é suficiente:
```bnf
<statement> ::= <assignmentStatement>      # começa com IDENTIFIER
              | <functionCallStatement>     # começa com IDENTIFIER
              | <expressionStatement>       # pode começar com IDENTIFIER
```

---

## 2. Soluções Aplicadas

### 2.1 Eliminação de Ambiguidade

**Técnica:** Estratificação de expressões por níveis de precedência

**Tabela de Precedência Definida:**

| Nível | Operadores | Associatividade | Regra |
|-------|-----------|----------------|-------|
| 0 (menor) | `=` | Direita | `<assignmentExpr>` |
| 1 | `or` | Esquerda | `<logicalOrExpr>` |
| 2 | `and` | Esquerda | `<logicalAndExpr>` |
| 3 | `not` | Direita | `<logicalNotExpr>` |
| 4 | `\|` | Esquerda | `<bitwiseOrExpr>` |
| 5 | `&` | Esquerda | `<bitwiseAndExpr>` |
| 6 | `==`, `!=`, `<`, `>`, `<=`, `>=` | Esquerda | `<comparisonExpr>` |
| 7 | `+`, `-` | Esquerda | `<additiveExpr>` |
| 8 | `*`, `/`, `%` | Esquerda | `<multiplicativeExpr>` |
| 9 | `**` | Direita | `<powerExpr>` |
| 10 | `-` (unário) | Direita | `<unaryExpr>` |
| 11 | `[]`, `()` | Esquerda | `<postfixExpr>` |
| 12 (maior) | primários | - | `<primary>` |

---

### 2.2 Eliminação de Recursão à Esquerda

**Padrão para Associatividade à ESQUERDA:**

**ANTES (recursão à esquerda):**
```bnf
A ::= A op B | B
```

**DEPOIS (sem recursão):**
```bnf
A ::= B (op B)*
```

**Exemplo - Operadores Aditivos:**

**ANTES:**
```bnf
<expression> ::= <expression> '+' <expression>
               | <expression> '-' <expression>
               | <term>
```

**DEPOIS:**
```bnf
<additiveExpr> ::= <multiplicativeExpr> (('+' | '-') <multiplicativeExpr>)*
```

---

**Padrão para Associatividade à DIREITA:**

**Para operadores UNÁRIOS:**
```bnf
<nivel> ::= 'operador' <nivel>
          | <proximoNivel>
```

**Para operadores BINÁRIOS:**
```bnf
<nivel> ::= <proximoNivel> ('operador' <nivel>)?
```

**Exemplo - Potência (associa à direita):**
```bnf
<powerExpr> ::= <unaryExpr> ('**' <powerExpr>)?
```

Isto garante que `2 ** 3 ** 2` seja calculado como `2 ** (3 ** 2) = 512`, não `(2 ** 3) ** 2 = 64`.

---

### 2.3 Unificação de Statements

**Solução para o Conflito LL(1):**

Para resolver o conflito em `<statement>`, assignments e chamadas de função foram transformados em expressões, seguindo o modelo de linguagens como C, Java e JavaScript.

**ANTES:**
```bnf
<statement> ::= <assignmentStatement>
              | <functionCallStatement>
              | <expressionStatement>
              | ...

<assignmentStatement> ::= IDENTIFIER '=' <expression>
<functionCallStatement> ::= IDENTIFIER '(' <argList>? ')'
```

**DEPOIS:**
```bnf
<statement> ::= <expressionStatement>
              | <ifStatement>
              | ...

<expressionStatement> ::= <expression>

<expression> ::= <assignmentExpr>
<assignmentExpr> ::= <logicalOrExpr> ('=' <assignmentExpr>)?
```

**Benefícios:**
- Remove ambiguidade: parser não precisa decidir entre assignment/call/expression ao ver IDENTIFIER
- Permite assignment em cadeia: `x = y = z = 5`
- Gramática verdadeiramente LL(1)
- Consistente com linguagens reais

**Trade-off:**
- Permite expressões sintaticamente válidas mas semanticamente inválidas (ex: `5 = x`)
- Esses erros serão detectados na análise semântica, não na sintática
- Esta é uma prática comum e aceita em compiladores

**Exemplo de derivação - Assignment em cadeia:**
```
x = y = 5

<assignmentExpr>
  → <logicalOrExpr> '=' <assignmentExpr>
  → IDENTIFIER '=' <assignmentExpr>
  → IDENTIFIER '=' <logicalOrExpr> '=' <assignmentExpr>
  → IDENTIFIER '=' IDENTIFIER '=' NUMBER

Resultado: x = (y = 5)  [associa à direita]
```

---

### 2.4 Verificação de Fatoração

**Fatoração** significa extrair prefixos comuns de produções alternativas para eliminar ambiguidade.

**Exemplo de gramática NÃO fatorada:**
```bnf
# PROBLEMA: ambas começam com 'if' <expression> ':'
<ifStatement> ::= 'if' <expression> ':' <block>
<ifStatement> ::= 'if' <expression> ':' <block> 'else' ':' <block>
```

**Após fatoração:**
```bnf
<ifStatement> ::= 'if' <expression> ':' <block> <optional_else>
<optional_else> ::= 'else' ':' <block>
<optional_else> ::= ε
```

#### Nossa Gramática - Análise de Fatoração

**1. Statements - FATORADA ✅**
```bnf
<statement> ::= <ifStatement>           # começa com 'if'
<statement> ::= <whileStatement>        # começa com 'while'
<statement> ::= <forStatement>          # começa com 'for'
<statement> ::= <doWhileStatement>      # começa com 'do'
<statement> ::= <breakStatement>        # começa com 'break'
<statement> ::= <continueStatement>     # começa com 'continue'
<statement> ::= <defStatement>          # começa com 'def'
<statement> ::= <expressionStatement>   # começa com IDENTIFIER, NUMBER, etc
```
**Cada alternativa começa com token diferente** → Não há prefixo comum!

**2. Primary - FATORADA ✅**
```bnf
<primary> ::= 'IDENTIFIER'              # IDENTIFIER
<primary> ::= 'NUMBER'                  # NUMBER
<primary> ::= 'STRING'                  # STRING
<primary> ::= 'True'                    # True
<primary> ::= 'False'                   # False
<primary> ::= '(' <expression> ')'      # (
<primary> ::= '[' <optional_expr_list> ']'  # [
```
**Todos os primeiros símbolos são distintos** → Não precisa fatorar!

**3. Operadores - FATORADA ✅**
```bnf
<comparison_op> ::= '=='    # ==
<comparison_op> ::= '!='    # !=
<comparison_op> ::= '<'     # <
<comparison_op> ::= '>'     # >
<comparison_op> ::= '<='    # <=
<comparison_op> ::= '>='    # >=
```
**Todos tokens diferentes** → Não precisa fatorar!

**Conclusão:** A gramática já está implicitamente fatorada após as transformações anteriores (eliminação de ambiguidade e unificação de statements). Nenhuma fatoração adicional foi necessária.

---

### 2.5 Conversão EBNF → BNF Pura

A gramática após eliminação de recursão ainda usava notação EBNF (`*`, `?`, `+`). Para implementação manual do parser LL(1), foi necessário converter para BNF pura.

#### Padrões de Conversão

**Padrão 1: A* (zero ou mais)**
```bnf
# EBNF:
<logicalOrExpr> ::= <logicalAndExpr> ('or' <logicalAndExpr>)*

# BNF pura:
<logicalOrExpr> ::= <logicalAndExpr> <logical_or_tail>
<logical_or_tail> ::= 'or' <logicalAndExpr> <logical_or_tail>
<logical_or_tail> ::= ε
```

**Padrão 2: A? (zero ou um / opcional)**
```bnf
# EBNF:
<expressionStatement> ::= <expression> ';'?

# BNF pura:
<expressionStatement> ::= <expression> <optional_semicolon>
<optional_semicolon> ::= ';'
<optional_semicolon> ::= ε
```

**Padrão 3: A+ (um ou mais)**
```bnf
# EBNF (hipotético):
<postfixExpr> ::= <primary> <postfix>+

# BNF pura (0 ou mais - nossa solução):
<postfixExpr> ::= <primary> <postfix_list>
<postfix_list> ::= <postfix> <postfix_list>
<postfix_list> ::= ε
```

#### Resultado da Conversão

**Estatísticas da gramática BNF pura:**
- **54 não-terminais** (incluindo auxiliares para EBNF)
- **43 terminais**
- **100 produções** totais
- **21 não-terminais com ε** (produções vazias)

**Não-terminais auxiliares criados:**
- `<statement_list>` - para `<statement>*`
- `<logical_or_tail>` - para `('or' <logicalAndExpr>)*`
- `<logical_and_tail>` - para `('and' <logicalNotExpr>)*`
- `<bitwise_or_tail>` - para `('|' <bitwiseAndExpr>)*`
- `<bitwise_and_tail>` - para `('&' <comparisonExpr>)*`
- `<comparison_tail>` - para `(<comparison_op> <additiveExpr>)*`
- `<additive_tail>` - para `(<add_op> <multiplicativeExpr>)*`
- `<multiplicative_tail>` - para `(<mul_op> <powerExpr>)*`
- `<postfix_list>` - para `<postfix>*`
- `<optional_semicolon>` - para `';'?`
- `<optional_else>` - para `('else' ':' <block>)?`
- `<optional_args>` - para `<argList>?`
- `<optional_expr_list>` - para `<expressionList>?`
- `<optional_params>` - para `<paramList>?`
- E outros (param_list_tail, arg_list_tail, expr_list_tail, etc)

---

### 2.6 Recursão à Direita Resultante

Ao eliminar recursão à **esquerda**, todas as regras auxiliares ficaram com recursão à **direita**:

```bnf
# Padrão geral das regras _tail:
<regra_tail> ::= operador <proximoNivel> <regra_tail>
                                          ^^^^^^^^^^^^
                                          recursão à DIREITA
<regra_tail> ::= ε
```

**Por que recursão à direita é aceitável em LL(1)?**
- Parsers LL(1) processam entrada da esquerda para direita
- Recursão à direita não causa loop infinito
- Permite associatividade à esquerda via acumulação na recursão

**Exemplo - Parsing de `2 + 3 + 4`:**
```
<additiveExpr>
  → <multiplicativeExpr> <additive_tail>
  → 2 <additive_tail>
  → 2 '+' <multiplicativeExpr> <additive_tail>
  → 2 '+' 3 <additive_tail>
  → 2 '+' 3 '+' <multiplicativeExpr> <additive_tail>
  → 2 '+' 3 '+' 4 <additive_tail>
  → 2 '+' 3 '+' 4 ε
```

A associatividade à esquerda `(2 + 3) + 4` é garantida pela **ordem de construção da árvore**, não pela recursão.

---

## 3. Pipeline Completo de Transformações

```
Gramática Original (ANTLR)
    ↓
┌─────────────────────────────────────────┐
│ 1. Eliminação de Ambiguidade            │
│    - Definir precedência (12 níveis)    │
│    - Definir associatividade (E/D)      │
│    ✅ Resultado: Precedência clara       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 2. Eliminação de Recursão à Esquerda    │
│    - A ::= A α | β  →  A ::= β A'       │
│    - A' ::= α A' | ε                    │
│    ✅ Criou recursão à direita           │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 3. Unificação de Statements             │
│    - Assignment como expressão          │
│    - Function call como expressão       │
│    ✅ Resolveu conflito LL(1)            │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 4. Verificação de Fatoração             │
│    - Buscar prefixos comuns             │
│    ✅ NÃO ENCONTROU (já fatorada)        │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ 5. Conversão EBNF → BNF Pura            │
│    - * → regras com ε                   │
│    - ? → regras com ε                   │
│    - (grupo) → regras auxiliares        │
│    ✅ 100 produções BNF puras            │
└─────────────────────────────────────────┘
    ↓
Gramática LL(1) Final ✅
- 54 não-terminais
- 43 terminais
- 100 produções
- 21 produções com ε
- Sem ambiguidade
- Sem recursão à esquerda
- Fatorada
- Pronta para tabela LL(1)
```

---

## 4. Estrutura Hierárquica Final

### Versão EBNF (Simplificada)

```bnf
<expression> ::= <assignmentExpr>
<assignmentExpr> ::= <logicalOrExpr> ('=' <assignmentExpr>)?
<logicalOrExpr> ::= <logicalAndExpr> ('or' <logicalAndExpr>)*
<logicalAndExpr> ::= <logicalNotExpr> ('and' <logicalNotExpr>)*
<logicalNotExpr> ::= 'not' <logicalNotExpr> | <bitwiseOrExpr>
<bitwiseOrExpr> ::= <bitwiseAndExpr> ('|' <bitwiseAndExpr>)*
<bitwiseAndExpr> ::= <comparisonExpr> ('&' <comparisonExpr>)*
<comparisonExpr> ::= <additiveExpr> (('==' | '!=' | '<' | '>' | '<=' | '>=') <additiveExpr>)*
<additiveExpr> ::= <multiplicativeExpr> (('+' | '-') <multiplicativeExpr>)*
<multiplicativeExpr> ::= <powerExpr> (('*' | '/' | '%') <powerExpr>)*
<powerExpr> ::= <unaryExpr> ('**' <powerExpr>)?
<unaryExpr> ::= '-' <unaryExpr> | <postfixExpr>
<postfixExpr> ::= <primary> <postfix>*
<postfix> ::= '[' <expression> ']' | '(' <argList>? ')'
<primary> ::= IDENTIFIER | NUMBER | STRING | 'True' | 'False'
            | '(' <expression> ')' | '[' <expressionList>? ']'
```

### Estrutura de Statements (Simplificada)

```bnf
<statement> ::= <ifStatement>
              | <whileStatement>
              | <forStatement>
              | <doWhileStatement>
              | <breakStatement>
              | <continueStatement>
              | <defStatement>
              | <expressionStatement>

<expressionStatement> ::= <expression> ';'?
```

**Sem conflitos:** Cada token inicial aponta para exatamente uma produção.

---

### Versão BNF Pura (Implementação Final)

#### Programa e Statements

```bnf
<program> ::= <statement_list> 'EOF'
<statement_list> ::= <statement> <statement_list>
<statement_list> ::= ε

<statement> ::= <ifStatement>
<statement> ::= <whileStatement>
<statement> ::= <forStatement>
<statement> ::= <doWhileStatement>
<statement> ::= <breakStatement>
<statement> ::= <continueStatement>
<statement> ::= <defStatement>
<statement> ::= <expressionStatement>

<expressionStatement> ::= <expression> <optional_semicolon>
<optional_semicolon> ::= ';'
<optional_semicolon> ::= ε
```

#### Hierarquia de Expressões (12 níveis - BNF Pura)

```bnf
# Nível 0: Assignment (direita)
<expression> ::= <assignmentExpr>
<assignmentExpr> ::= <logicalOrExpr> <assignment_tail>
<assignment_tail> ::= '=' <assignmentExpr>
<assignment_tail> ::= ε

# Nível 1: OR lógico (esquerda)
<logicalOrExpr> ::= <logicalAndExpr> <logical_or_tail>
<logical_or_tail> ::= 'or' <logicalAndExpr> <logical_or_tail>
<logical_or_tail> ::= ε

# Nível 2: AND lógico (esquerda)
<logicalAndExpr> ::= <logicalNotExpr> <logical_and_tail>
<logical_and_tail> ::= 'and' <logicalNotExpr> <logical_and_tail>
<logical_and_tail> ::= ε

# Nível 3: NOT lógico (direita, unário)
<logicalNotExpr> ::= 'not' <logicalNotExpr>
<logicalNotExpr> ::= <bitwiseOrExpr>

# Nível 4: OR bitwise (esquerda)
<bitwiseOrExpr> ::= <bitwiseAndExpr> <bitwise_or_tail>
<bitwise_or_tail> ::= '|' <bitwiseAndExpr> <bitwise_or_tail>
<bitwise_or_tail> ::= ε

# Nível 5: AND bitwise (esquerda)
<bitwiseAndExpr> ::= <comparisonExpr> <bitwise_and_tail>
<bitwise_and_tail> ::= '&' <comparisonExpr> <bitwise_and_tail>
<bitwise_and_tail> ::= ε

# Nível 6: Comparação (esquerda)
<comparisonExpr> ::= <additiveExpr> <comparison_tail>
<comparison_tail> ::= <comparison_op> <additiveExpr> <comparison_tail>
<comparison_tail> ::= ε

# Nível 7: Adição/Subtração (esquerda)
<additiveExpr> ::= <multiplicativeExpr> <additive_tail>
<additive_tail> ::= <add_op> <multiplicativeExpr> <additive_tail>
<additive_tail> ::= ε

# Nível 8: Multiplicação/Divisão/Módulo (esquerda)
<multiplicativeExpr> ::= <powerExpr> <multiplicative_tail>
<multiplicative_tail> ::= <mul_op> <powerExpr> <multiplicative_tail>
<multiplicative_tail> ::= ε

# Nível 9: Potência (direita)
<powerExpr> ::= <unaryExpr> <power_tail>
<power_tail> ::= '**' <powerExpr>
<power_tail> ::= ε

# Nível 10: Menos unário (direita)
<unaryExpr> ::= '-' <unaryExpr>
<unaryExpr> ::= <postfixExpr>

# Nível 11: Acesso a array e chamada de função (esquerda)
<postfixExpr> ::= <primary> <postfix_list>
<postfix_list> ::= <postfix> <postfix_list>
<postfix_list> ::= ε

<postfix> ::= '[' <expression> ']'
<postfix> ::= '(' <optional_args> ')'

# Nível 12: Valores primários
<primary> ::= 'IDENTIFIER'
<primary> ::= 'NUMBER'
<primary> ::= 'STRING'
<primary> ::= 'True'
<primary> ::= 'False'
<primary> ::= '(' <expression> ')'
<primary> ::= '[' <optional_expr_list> ']'
```

---

## 5. Exemplos de Cálculo

### Exemplo 1: `2 + 3 * 4`
- Multiplicação tem maior precedência (nível 8) que adição (nível 7)
- Calcula: `3 * 4 = 12`, depois `2 + 12 = 14`
- **Resultado:** 14

### Exemplo 2: `5 - 3 - 2`
- Subtração associa à esquerda
- Calcula: `(5 - 3) = 2`, depois `2 - 2 = 0`
- **Resultado:** 0

### Exemplo 3: `2 ** 3 ** 2`
- Potência associa à direita
- Calcula: `3 ** 2 = 9`, depois `2 ** 9 = 512`
- **Resultado:** 512

### Exemplo 4: `x = y = 10`
- Assignment associa à direita
- Calcula: `y = 10`, depois `x = (resultado anterior)`
- **Resultado:** x recebe 10, y recebe 10

### Exemplo 5: `arr[i] = x + 5`
- Assignment tem menor precedência
- Calcula: `x + 5`, depois `arr[i] = (resultado)`
- **Resultado:** arr[i] recebe o valor de x + 5

---

## 6. Verificação LL(1)

### Análise de Conflitos em `<statement>`:

| Próximo Token | Produção Escolhida |
|---------------|-------------------|
| `if` | `<ifStatement>` |
| `while` | `<whileStatement>` |
| `for` | `<forStatement>` |
| `do` | `<doWhileStatement>` |
| `break` | `<breakStatement>` |
| `continue` | `<continueStatement>` |
| `def` | `<defStatement>` |
| IDENTIFIER, NUMBER, STRING, `(`, `[`, `-`, `not` | `<expressionStatement>` |

**Resultado:** Sem conflitos. A gramática é LL(1).

### Análise de Conflitos em `<primary>`:

| Próximo Token | Produção Escolhida |
|---------------|-------------------|
| `'IDENTIFIER'` | `<primary> ::= 'IDENTIFIER'` |
| `'NUMBER'` | `<primary> ::= 'NUMBER'` |
| `'STRING'` | `<primary> ::= 'STRING'` |
| `'True'` | `<primary> ::= 'True'` |
| `'False'` | `<primary> ::= 'False'` |
| `'('` | `<primary> ::= '(' <expression> ')'` |
| `'['` | `<primary> ::= '[' <optional_expr_list> ']'` |

**Resultado:** Sem conflitos. A gramática é LL(1) ✅

---

## 7. Ferramentas Desenvolvidas

### 7.1 Classe Grammar (grammar.py)

Carrega e representa gramática BNF pura:

**Funcionalidades:**
- Leitura de arquivo `.bnf`
- Tokenização respeitando strings entre aspas
- Identificação automática de não-terminais vs terminais
- Suporte a epsilon (ε)
- Detecção de produções vazias
- Método `debug_print()` para visualização

**Estruturas de dados:**
```python
class Grammar:
    def __init__(self):
        self.productions = {}      # dict: non-terminal -> list of productions
        self.nonterminals = set()  # set de não-terminais
        self.terminals = set()      # set de terminais
        self.start_symbol = None   # símbolo inicial
```

**Uso:**
```python
from grammar import Grammar

g = Grammar()
g.load_from_file("gramatica_bnf_pura.bnf")
g.debug_print()

# Acessar estruturas
print(g.start_symbol)  # '<program>'
print(g.nonterminals)  # set de não-terminais
print(g.terminals)     # set de terminais
print(g.productions)   # dict de produções
```

**Arquivo gerado:**
- `gramatica_bnf_pura.bnf` - 100 produções em BNF pura ✅

---

## 8. Próximos Passos

### Fase Atual: ✅ Gramática LL(1) Completa

**Já realizado:**
1. ✅ Análise da gramática original (identificação de problemas)
2. ✅ Eliminação de ambiguidade (precedência e associatividade)
3. ✅ Eliminação de recursão à esquerda
4. ✅ Unificação de statements (assignment como expressão)
5. ✅ Verificação de fatoração
6. ✅ Conversão EBNF → BNF pura
7. ✅ Implementação da classe Grammar

### Próximas Etapas:

**Fase 2: Cálculo de FIRST e FOLLOW**
- [ ] Implementar algoritmo de cálculo de FIRST
- [ ] Implementar algoritmo de cálculo de FOLLOW
- [ ] Validar conjuntos com exemplos
- [ ] Gerar arquivos de saída (first_sets.txt, follow_sets.txt)

**Fase 3: Construção da Tabela LL(1)**
- [ ] Implementar construção da tabela de parsing
- [ ] Detectar conflitos (células com múltiplas entradas)
- [ ] Gerar visualização da tabela
- [ ] Validar que tabela não tem conflitos

**Fase 4: Implementação do Parser LL(1)**
- [ ] Implementar parser baseado em pilha
- [ ] Integrar com lexer ANTLR existente
- [ ] Processar tokens e executar derivações
- [ ] Gerar árvore de parsing

**Fase 5: Testes e Validação**
- [ ] Criar suite de testes (exemplos válidos e inválidos)
- [ ] Comparar com parser ANTLR (validação cruzada)
- [ ] Gerar relatórios de parsing
- [ ] Documentar casos de teste

**Fase 6: Documentação e Apresentação**
- [ ] Finalizar documentação técnica
- [ ] Criar slides para apresentação (10 min)
- [ ] Preparar demonstrações ao vivo
- [ ] Organizar repositório GitHub
- [ ] Preparar entrega Google Classroom

**Fase 7 (Opcional): Parser SLR (+1.0 ponto extra)**
- [ ] Adaptar gramática para SLR(1)
- [ ] Calcular coleção de itens LR(0)
- [ ] Construir tabela de parsing SLR(1)
- [ ] Implementar algoritmo de parsing SLR(1)

**Prazo:** 10/12/2025

---

## 9. Referências

**Arquivos de Gramática:**
- `gramatica_original.bnf` - Gramática extraída do ANTLR (com ambiguidade)
- `gramatica_sem_ambiguidade.bnf` - Versão EBNF (após eliminação de ambiguidade e recursão)
- `gramatica_bnf_pura.bnf` - Versão BNF final (100 produções, pronta para LL(1))

**Código Fonte:**
- `PythonParser.g4` - Gramática ANTLR original
- `PythonLexer.g4` - Lexer ANTLR
- `grammar.py` - Classe para carregar e representar gramática BNF

**Documentação:**
- Este arquivo (`transformacoes.md`) - Documentação completa das transformações

---

## Changelog

**Versão 3.0 (06/12/2024)**
- ✅ Adicionada seção 2.4 (Verificação de Fatoração)
- ✅ Adicionada seção 2.5 (Conversão EBNF → BNF Pura)
- ✅ Adicionada seção 2.6 (Recursão à Direita Resultante)
- ✅ Adicionada seção 3 (Pipeline Completo)
- ✅ Expandida seção 4 (Estrutura Hierárquica - EBNF + BNF Pura)
- ✅ Expandida seção 6 (Verificação LL(1) com análise de primary)
- ✅ Adicionada seção 7 (Ferramentas Desenvolvidas)
- ✅ Atualizada seção 8 (Próximos Passos com checklist detalhado)
- ✅ Expandida seção 9 (Referências completas)
- ✅ Adicionada seção Changelog

**Versão 2.0 (05/12/2024)**
- ✅ Adicionada seção 1.4 (Conflito LL(1) em Statements)
- ✅ Adicionada seção 2.3 (Unificação de Statements)
- ✅ Atualizada tabela de precedência (nível 0 = assignment)

**Versão 1.0 (04/12/2024)**
- ✅ Versão inicial
- ✅ Seções 1.1-1.3 (Problemas identificados)
- ✅ Seções 2.1-2.2 (Eliminação de ambiguidade e recursão)
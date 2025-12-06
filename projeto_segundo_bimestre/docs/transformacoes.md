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

## 3. Resumo das Transformações

### Estrutura Hierárquica das Expressões

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

## 4. Exemplos de Cálculo

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

## 5. Verificação LL(1)

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

---

## 6. Próximos Passos

- Calcular conjuntos FIRST para cada não-terminal
- Calcular conjuntos FOLLOW para cada não-terminal
- Construir tabela de parsing LL(1)
- Verificar ausência de conflitos na tabela (células com múltiplas entradas)
- Implementar parser LL(1) em Python
- Integrar com lexer ANTLR existente

---

## Referências

- Gramática ANTLR original: `PythonParser.g4`
- Arquivos de gramática BNF: `gramatica_original.bnf` e `gramatica_sem_ambiguidade.bnf`
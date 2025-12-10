# Análise Comparativa: LL(1) versus SLR(1)

A escolha entre diferentes técnicas de análise sintática é fundamental no projeto de compiladores. Este documento apresenta uma análise comparativa entre os analisadores LL(1) e SLR(1), destacando suas características teóricas, diferenças estruturais e implicações práticas.

---

## 1. Fundamentos Teóricos

Os analisadores sintáticos podem ser classificados em duas grandes categorias conforme a direção de construção da árvore de derivação: **top-down** (descendente) e **bottom-up** (ascendente).

### 1.1 Análise LL(1) — Abordagem Top-Down

O analisador LL(1) realiza a análise de forma **descendente**, partindo do símbolo inicial da gramática e aplicando derivações mais à esquerda (*leftmost derivation*) até alcançar a cadeia de entrada. A notação LL(1) representa:

- **L** (*Left-to-right*): leitura da entrada da esquerda para a direita
- **L** (*Leftmost derivation*): derivação mais à esquerda
- **1**: um símbolo de *lookahead* para decisão

O algoritmo utiliza uma **pilha de análise** e uma **tabela de parsing** M[A, a], onde A é um não-terminal e a é o terminal corrente. A cada passo, o parser consulta a tabela para determinar qual produção aplicar, expandindo o não-terminal no topo da pilha.

### 1.2 Análise SLR(1) — Abordagem Bottom-Up

O analisador SLR(1) realiza a análise de forma **ascendente**, construindo a árvore das folhas em direção à raiz através de reduções sucessivas. A notação SLR(1) representa:

- **S** (*Simple*): versão simplificada do LR
- **L** (*Left-to-right*): leitura da entrada da esquerda para a direita
- **R** (*Rightmost derivation*): derivação mais à direita em reverso
- **1**: um símbolo de *lookahead*

O algoritmo utiliza uma **pilha de estados** e duas tabelas: **ACTION** (ações de *shift*, *reduce* ou *accept*) e **GOTO** (transições entre estados para não-terminais).

---

## 2. Estruturas de Dados e Construção

### Comparação das Estruturas

| Aspecto | LL(1) | SLR(1) |
|---------|-------|--------|
| Conjuntos auxiliares | FIRST, FOLLOW | FIRST, FOLLOW |
| Estrutura principal | Tabela M[A, a] | Tabelas ACTION e GOTO |
| Estados | Não utiliza | Coleção canônica LR(0) |
| Itens | Não utiliza | Itens LR(0): [A → α • β] |
| Operações | Expansão | CLOSURE, GOTO |
| Pilha armazena | Símbolos | Estados e símbolos |

### 2.1 Construção da Tabela LL(1)

Para cada produção A → α da gramática:

1. Para cada terminal `a ∈ FIRST(α)`, adicionar `A → α` em `M[A, a]`
2. Se `ε ∈ FIRST(α)`, para cada terminal `b ∈ FOLLOW(A)`, adicionar `A → α` em `M[A, b]`

### 2.2 Construção da Tabela SLR(1)

A construção envolve três etapas principais:

**1. Coleção Canônica:** construir todos os estados I₀, I₁, ..., Iₙ usando as operações CLOSURE e GOTO sobre itens LR(0)

**2. Tabela ACTION:** para cada estado Iᵢ:
- Se `[A → α • a β] ∈ Iᵢ` e `GOTO(Iᵢ, a) = Iⱼ`: `ACTION[i, a] = shift j`
- Se `[A → α •] ∈ Iᵢ` e `A ≠ S'`: para cada `a ∈ FOLLOW(A)`, `ACTION[i, a] = reduce A → α`
- Se `[S' → S •] ∈ Iᵢ`: `ACTION[i, $] = accept`

**3. Tabela GOTO:** para cada não-terminal A, se `GOTO(Iᵢ, A) = Iⱼ`, então `GOTO[i, A] = j`

---

## 3. Classes de Gramáticas Reconhecidas

Uma diferença fundamental entre os dois métodos está na classe de gramáticas que cada um pode processar.

### Hierarquia de Inclusão

```
Gramáticas Livres de Contexto
    └── LR(1)
        └── LALR(1)
            └── SLR(1)

LL(1) ← Não é subconjunto de SLR(1), nem vice-versa
```

**Observação importante**: A classe LL(1) **não** é subconjunto de SLR(1), nem vice-versa. Existem gramáticas LL(1) que não são SLR(1) e gramáticas SLR(1) que não são LL(1). Contudo, na prática, SLR(1) aceita uma gama maior de gramáticas úteis para linguagens de programação.

---

## 4. Restrições Gramaticais

| Característica | LL(1) | SLR(1) |
|----------------|-------|--------|
| Recursão à esquerda | Proibida | Permitida |
| Fatoração obrigatória | Sim | Não |
| Prefixos comuns | Proibidos | Permitidos |
| Ambiguidade | Proibida | Proibida |
| Gramática aumentada | Não necessária | Obrigatória (S' → S) |

### 4.1 Recursão à Esquerda

A recursão à esquerda representa a diferença mais significativa entre os dois métodos. Considere a gramática para expressões aritméticas:

```
E → E + T | T
```

**Para LL(1):** Esta produção causa loop infinito, pois ao expandir E, o parser tentaria expandir E novamente sem consumir entrada. A solução requer eliminação de recursão:

```
E  → T E'
E' → + T E' | ε
```

**Para SLR(1):** A gramática original é aceita diretamente. O parser faz *shift* dos tokens até reconhecer T, então decide entre fazer *reduce* para `E → T` ou continuar com *shift* de `+`, baseando-se no *lookahead* e no conjunto FOLLOW.

### 4.2 Tipos de Conflitos

**LL(1) — Conflitos FIRST/FIRST e FIRST/FOLLOW:**
- Ocorrem quando múltiplas produções de um mesmo não-terminal possuem interseção em seus conjuntos FIRST
- Ou quando uma produção pode derivar ε e há interseção entre FIRST e FOLLOW

**SLR(1) — Conflitos Shift-Reduce e Reduce-Reduce:**
- **Shift-Reduce**: ocorre quando, em um estado, é possível tanto fazer *shift* de um terminal quanto *reduce* por uma produção completa
- **Reduce-Reduce**: ocorre quando, em um estado, existem duas ou mais produções completas cujos conjuntos FOLLOW possuem interseção

---

## 5. Algoritmos de Parsing

### 5.1 Algoritmo LL(1)

```
1. Empilhar $ e o símbolo inicial S
2. a ← próximo token
3. Enquanto pilha não vazia:
   4. X ← topo da pilha
   5. Se X é terminal:
      6. Se X = a:
         7. Desempilhar X (MATCH)
         8. a ← próximo token
      9. Senão: ERRO
   10. Se X = $:
       11. Se a = $: ACEITAR
       12. Senão: ERRO
   13. Se X é não-terminal:
       14. Se M[X, a] = X → Y₁Y₂...Yₖ:
           15. Desempilhar X
           16. Empilhar Yₖ, ..., Y₂, Y₁ (ordem reversa)
       17. Senão: ERRO
```

### 5.2 Algoritmo SLR(1)

```
1. Empilhar estado inicial 0
2. a ← próximo token
3. Repetir:
   4. s ← estado no topo da pilha
   5. Se ACTION[s, a] = shift t:
      6. Empilhar a e depois t
      7. a ← próximo token
   8. Se ACTION[s, a] = reduce A → β:
      9. Desempilhar 2 × |β| símbolos
      10. s' ← estado no topo da pilha
      11. Empilhar A e depois GOTO[s', A]
   12. Se ACTION[s, a] = accept:
       13. ACEITAR
   14. Senão: ERRO
```

---

## 6. Análise de Complexidade

| Operação | LL(1) | SLR(1) |
|----------|-------|--------|
| Cálculo de FIRST/FOLLOW | O(n²) | O(n²) |
| Construção da tabela | O(n × m) | O(n² × m) |
| Tamanho da tabela | O(n × m) | O(k × m) |
| Tempo de parsing | O(n) | O(n) |
| Espaço de parsing | O(n) | O(n) |

Onde:
- `n` = número de símbolos/produções
- `m` = número de terminais
- `k` = número de estados LR(0)

---

## 7. Vantagens e Desvantagens

### 7.1 Analisador LL(1)

**Vantagens:**
- Implementação mais simples e intuitiva
- Tabela de parsing menor (apenas não-terminais × terminais)
- Facilidade para implementação manual (parsers recursivos descendentes)
- Detecção de erros mais próxima do ponto de ocorrência
- Menor consumo de memória

**Desvantagens:**
- Requer transformações na gramática (eliminação de recursão à esquerda, fatoração)
- Classe de gramáticas aceitas mais restrita
- Gramáticas transformadas podem ficar menos legíveis
- Produções com ε requerem tratamento especial

### 7.2 Analisador SLR(1)

**Vantagens:**
- Aceita gramáticas com recursão à esquerda naturalmente
- Não requer fatoração da gramática
- Classe de gramáticas aceitas mais ampla
- Gramática pode permanecer em sua forma natural
- Base para analisadores mais poderosos (LALR, LR canônico)

**Desvantagens:**
- Implementação mais complexa
- Tabelas maiores (estados × símbolos)
- Construção da coleção canônica é computacionalmente mais cara
- Mensagens de erro podem ser menos precisas

---

## 8. Aplicação Prática: Linguagem Vython

Para a linguagem Vython desenvolvida neste trabalho, ambos os analisadores foram implementados.

### Resultados Comparativos

| Métrica | LL(1) | SLR(1) |
|---------|-------|--------|
| Produções | 105 | 104 |
| Não-terminais | 54 | 57 |
| Terminais | 43 | 45 |
| Estados/Entradas na tabela | 663 entradas | 174 estados |
| Conflitos detectados | 0 | 0 |
| Gramática aceita? | Sim | Sim |

**Observação:** A gramática Vython foi projetada para ser LL(1), o que automaticamente a torna compatível com SLR(1). A versão LL(1) exigiu eliminação de recursão à esquerda nas expressões, enquanto a versão SLR(1) poderia ter mantido a recursão original.

---

## 9. Considerações Finais

A escolha entre LL(1) e SLR(1) depende de diversos fatores:

| Critério | Recomendação |
|----------|--------------|
| Gramática com muita recursão à esquerda | SLR(1) |
| Implementação manual | LL(1) |
| Recursos de memória limitados | LL(1) |
| Mensagens de erro precisas | LL(1) |
| Gramática em forma natural | SLR(1) |
| Uso de geradores (Yacc/Bison) | SLR(1)/LALR(1) |
| Uso de ANTLR | LL(*) |

Para a linguagem Vython, a implementação de ambos os analisadores demonstrou a viabilidade de cada abordagem, sendo que a escolha final pode ser orientada pelo contexto de uso do compilador.

---

## Resumo Visual

```
+-------------------------------+-----------------------------------+
|            LL(1)              |             SLR(1)                |
+-------------------------------+-----------------------------------+
|     Análise TOP-DOWN          |       Análise BOTTOM-UP           |
|     (raiz -> folhas)          |       (folhas -> raiz)            |
+-------------------------------+-----------------------------------+
|   Derivação à ESQUERDA        |     Derivação à DIREITA           |
|   (leftmost)                  |     (rightmost, em reverso)       |
+-------------------------------+-----------------------------------+
|   Tabela: M[NT, T]            |   Tabelas: ACTION + GOTO          |
+-------------------------------+-----------------------------------+
|   Pilha de SIMBOLOS           |   Pilha de ESTADOS                |
+-------------------------------+-----------------------------------+
|   Operação: EXPAND            |   Operações: SHIFT, REDUCE        |
+-------------------------------+-----------------------------------+
|   Recursão esquerda: NAO      |   Recursão esquerda: SIM          |
+-------------------------------+-----------------------------------+
|   Implementação: SIMPLES      |   Implementação: COMPLEXA         |
+-------------------------------+-----------------------------------+
```

---

**Equipe:** Davi Maciel Cavalcante, Pablo Abdon , João Miguel, Liane 
**Disciplina:** Compiladores  
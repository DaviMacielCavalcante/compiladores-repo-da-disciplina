grammar Python;

// Regra principal - um programa é uma sequência de declarações
program: statement* EOF;

// Declarações
statement
    : assignmentStatement
    | printStatement
    | ifStatement
    | whileStatement
    | expressionStatement
    ;

// Atribuição: x = 5
assignmentStatement: IDENTIFIER '=' expression ';'?;

// Print: print(x)
printStatement: 'print' '(' expression ')' ';'?;

// If statement
ifStatement: 'if' '(' expression ')' ':' block ('else' ':' block)?;

// While loop
whileStatement: 'while' '(' expression ')' ':' block;

// Expressão como declaração
expressionStatement: expression ';'?;

// Bloco de código
block: '{' statement* '}' | statement;

// Expressões
expression
    : expression ('*' | '/') expression     # MulDiv
    | expression ('+' | '-') expression     # AddSub
    | expression ('==' | '!=' | '<' | '>' | '<=' | '>=') expression  # Comparison
    | '(' expression ')'                    # Parentheses
    | IDENTIFIER                           # Variable
    | NUMBER                               # Number
    | STRING                               # String
    | 'True'                              # BoolTrue
    | 'False'                             # BoolFalse
    ;

// Tokens
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER: [0-9]+ ('.' [0-9]+)?;
STRING: '"' (~["\r\n])* '"' | '\'' (~['\r\n])* '\'';
WS: [ \t\r\n]+ -> skip;
COMMENT: '#' ~[\r\n]* -> skip;
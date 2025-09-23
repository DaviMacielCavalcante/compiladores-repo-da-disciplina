grammar Python;

// Regra principal - um programa é uma sequência de declarações
program: statement* EOF;

// Declarações
statement
    : assignmentStatement
    | printStatement
    | ifStatement
    | whileStatement
    | forStatement
    | expressionStatement
    | doWhileStatement
    | breakStatement
    | continueStatement
    ;

// Atribuição: x = 5
assignmentStatement: IDENTIFIER '=' expression ';'?;

// Print: print(x)
printStatement: 'print' '(' expression ')' ';'?;

// If statement
ifStatement: 'if' expression ':' block ('else' ':' block)?;

// While loop
whileStatement: 'while' expression ':' block;

// For loop: for var in range(start, end, step)
forStatement: 'for' IDENTIFIER 'in' 'range' '(' expression (',' expression (',' expression)?)? ')' ':' block;

// Do-while loop: do: <block> while ( <expression> ) ;
doWhileStatement: 'do' ':' block 'while'  expression  ';'?;

// Break statement: break;
breakStatement: 'break' ';'?;

// Continue statement: continue;
continueStatement: 'continue' ';'?;

// Expressão como declaração
expressionStatement: expression ';'?;

// Bloco de código - permitindo blocos vazios
block: '{' statement* '}' | statement;

// Expressões
expression
    : expression pow_op expression #pow 
    | expression mul_div expression     # MulDiv
    | expression add_sub expression     # AddSub
    | expression comparison_op expression     # comparison
    | expression bitwise_and_or expression #bitwise
    | expression logical_op  expression  # logical
    | '(' expression ')'                    # Parentheses
    | IDENTIFIER                           # Variable
    | NUMBER                               # Number
    | STRING                               # String
    | 'True'                              # BoolTrue
    | 'False'                             # BoolFalse
    ;

//operadores

add_sub
    : ('+' | '-')
    ;

mul_div
    : ('*' | '/' | '%')
    ;

pow_op
    : '**'
    ;

comparison_op
    : ('==' | '!=' | '<' | '>' | '<=' | '>=' )
    ;

logical_op
    :  ('and' | 'or' | 'not')
    ;

bitwise_and_or
    : ('&' | '|' )
    ;

// Tokens
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER: [0-9]+ ('.' [0-9]+)?;
STRING: '"' (~["\r\n])* '"' | '\'' (~['\r\n])* '\'';
WS: [ \t\r\n]+ -> skip;
COMMENT: '#' ~[\r\n]* -> skip;
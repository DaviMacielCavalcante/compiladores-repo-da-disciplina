parser grammar PythonParser;

options { tokenVocab=PythonLexer; }

// Regra principal
program: statement* EOF;

// Declarações
statement
    : assignmentStatement
    | printStatement
    | inputStatement
    | ifStatement
    | whileStatement
    | forStatement
    | expressionStatement
    | doWhileStatement
    | breakStatement
    | continueStatement
    | defStatement
    ;

// Atribuição (suporta arrays)
assignmentStatement: IDENTIFIER (LBRACKET expression RBRACKET)* ASSIGN expression SEMICOLON?;

// Print
printStatement: PRINT LPAREN expression (COMMA expression)* RPAREN SEMICOLON?;

// Input - lê entrada do usuário
inputStatement: IDENTIFIER ASSIGN INPUT LPAREN STRING? RPAREN SEMICOLON?;

// If statement
ifStatement: IF expression COLON block (ELSE COLON block)?;

// While loop
whileStatement: WHILE expression COLON block;

// For loop
forStatement: FOR IDENTIFIER IN RANGE LPAREN expression (COMMA expression (COMMA expression)?)? RPAREN COLON block;

// Do-while loop
doWhileStatement: DO COLON block WHILE expression SEMICOLON?;

// Break
breakStatement: BREAK SEMICOLON?;

// Continue
continueStatement: CONTINUE SEMICOLON?;

// Def 
defStatement: DEF IDENTIFIER LPAREN expression* RPAREN COLON LBRACE statement* RBRACE SEMICOLON?;

// Expressão como declaração
expressionStatement: expression SEMICOLON?;

// Bloco de código
block: LBRACE statement* RBRACE | statement;

// Expressões (com suporte a arrays) - PRECEDÊNCIA CORRIGIDA
expression
    : expression logical_op expression          # logical    
    | expression bitwise_and_or expression      # bitwise    
    | expression comparison_op expression       # comparison 
    | expression add_sub expression             # AddSub     
    | expression mul_div expression             # MulDiv     
    | expression pow_op expression              # pow        
    | LPAREN expression RPAREN                  # Parenteses
    | IDENTIFIER (LBRACKET expression RBRACKET)+ # ArrayAccess
    | LBRACKET (expression (COMMA expression)*)? RBRACKET # ArrayLiteral
    | IDENTIFIER                                # Variable
    | NUMBER                                    # Number
    | STRING                                    # String
    | TRUE                                      # BoolTrue
    | FALSE                                     # BoolFalse
    ;

// Operadores
add_sub: (PLUS | MINUS);
mul_div: (MULT | DIV | MOD);
pow_op: POW;
comparison_op: (EQ | NEQ | LT | GT | LTE | GTE);
logical_op: (AND | OR | NOT);
bitwise_and_or: (BITAND | BITOR);
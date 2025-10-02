lexer grammar PythonLexer;

// Palavras-chave 
IF: 'if';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';
IN: 'in';
RANGE: 'range';
DO: 'do';
BREAK: 'break';
CONTINUE: 'continue';
TRUE: 'True';
FALSE: 'False';
DEF: 'def';

// Operadores
ASSIGN: '=';
PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';
MOD: '%';
POW: '**';

// Comparadores
EQ: '==';
NEQ: '!=';
LT: '<';
GT: '>';
LTE: '<=';
GTE: '>=';

// Lógicos
AND: 'and';
OR: 'or';
NOT: 'not';

// Bitwise
BITAND: '&';
BITOR: '|';

// Delimitadores
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACKET: '[';
RBRACKET: ']';
COLON: ':';
SEMICOLON: ';';
COMMA: ',';

// Tokens complexos
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER: [0-9]+ ('.' [0-9]+)?;
STRING: '"' (~["\r\n])* '"' | '\'' (~['\r\n])* '\'';

// Ignorar
WS: [ \t\r\n]+ -> skip;
COMMENT: '#' ~[\r\n]* -> skip;